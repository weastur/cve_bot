import logging
from functools import partial

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from cve_bot import db
from cve_bot.formatters import (
    format_cve,
    format_cve_with_packages,
    format_my_subscriptions,
    format_package_cve_list,
)
from cve_bot.models import CVE, PackageCVE, Subscription
from cve_bot.perf import track

logger = logging.getLogger(__name__)

NOT_FOUND = "<b>Not found</b>"
DONE = "<b>Done</b>"


def _get_package_info_for_cve(session, cve):
    stmt = select(PackageCVE).where(PackageCVE.cve_name == cve.name)  # noqa: WPS221
    package_cve = session.execute(stmt).scalars().all()
    return format_cve_with_packages(cve, package_cve)


def get_package_info(user_input, chat_id):
    db_engine = db.get_engine()
    logger.info("Get info for %s package", user_input)
    with Session(db_engine) as session:
        stmt = select(CVE).join(CVE.packages).where(PackageCVE.package_name == user_input.lower())  # noqa: WPS221
        cve = session.execute(stmt).scalars().all()
        if cve:
            return "".join(map(partial(_get_package_info_for_cve, session), cve))
        logger.info("Get info for %s package - NOT FOUND", user_input)
        return NOT_FOUND


@track()
def get_cve_info(user_input, chat_id):
    db_engine = db.get_engine()
    logger.info("Get info for %s CVE", user_input)
    with Session(db_engine) as session:
        stmt = select(CVE).where(CVE.name == f"CVE-{user_input}")  # noqa: WPS221
        cve = session.execute(stmt).scalars().first()
        if cve:
            stmt = select(PackageCVE).where(PackageCVE.cve_name == cve.name)
            package_cve = session.execute(stmt).scalars().all()
            return "{cve_info}\n{package_cve_info}".format(
                cve_info=format_cve(cve), package_cve_info=format_package_cve_list(package_cve)
            )
        logger.info("Get info for %s CVE - NOT FOUND", user_input)
        return NOT_FOUND


@track()
def create_new_subscription(user_input, chat_id):
    db_engine = db.get_engine()
    logger.info("Subscribe chat %d to CVE %s", chat_id, user_input)
    with Session(db_engine) as session:
        stmt = select(Subscription).where(
            Subscription.chat_id == chat_id, Subscription.cve_name == f"CVE-{user_input}"
        )  # noqa: WPS221
        subscription = session.execute(stmt).scalars().first()
        if subscription:
            return DONE
        subscription = Subscription(chat_id=chat_id, cve_name=f"CVE-{user_input}")
        session.add(subscription)
        try:
            session.commit()
        except IntegrityError:
            return NOT_FOUND
        return DONE


@track()
def remove_subscription(user_input, chat_id):
    db_engine = db.get_engine()
    logger.info("Unsubscribe chat %d from CVE %s", chat_id, user_input)
    with Session(db_engine) as session:
        stmt = select(Subscription).where(
            Subscription.cve_name == f"CVE-{user_input}", Subscription.chat_id == chat_id
        )  # noqa: WPS221
        subscription = session.execute(stmt).scalars().first()
        if subscription:
            session.delete(subscription)
            session.commit()
            return DONE
        logger.info("Unsubscribe chat %d from CVE %s failed: subscription not found", chat_id, user_input)
        return NOT_FOUND


@track()
def get_my_subscriptions(chat_id):
    db_engine = db.get_engine()
    logger.info("Get all subscriptions for chat %d", chat_id)
    with Session(db_engine) as session:
        stmt = select(Subscription).where(Subscription.chat_id == chat_id)
        subscriptions = session.execute(stmt).scalars().all()
        if subscriptions:
            return format_my_subscriptions(subscriptions)
        logger.info("Get all subscriptions for chat %d failed: not found", chat_id)
        return NOT_FOUND
