from functools import partial

from sqlalchemy import select
from sqlalchemy.orm import Session

from cve_bot import db
from cve_bot.formatters import (
    format_cve,
    format_cve_with_packages,
    format_my_subscriptions,
    format_package_cve_list,
)
from cve_bot.models import CVE, PackageCVE, Subscription

NOT_FOUND = "<b>Not found</b>"
DONE = "<b>Done</b>"


def _get_package_info_for_cve(session, cve):
    stmt = select(PackageCVE).where(PackageCVE.cve_name == cve.name)  # noqa: WPS221
    package_cve = session.execute(stmt).scalars().all()
    return format_cve_with_packages(cve, package_cve)


def get_package_info(user_input, chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).join(CVE.packages).where(PackageCVE.package_name == user_input)  # noqa: WPS221
        cve = session.execute(stmt).scalars().all()
        if cve:
            return "".join(map(partial(_get_package_info_for_cve, session), cve))
        return NOT_FOUND


def get_cve_info(user_input, chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).where(CVE.name == f"CVE-{user_input}")  # noqa: WPS221
        cve = session.execute(stmt).scalars().first()
        if cve:
            stmt = select(PackageCVE).where(PackageCVE.cve_name == cve.name)
            package_cve = session.execute(stmt).scalars().all()
            return "{cve_info}\n{package_cve_info}".format(
                cve_info=format_cve(cve), package_cve_info=format_package_cve_list(package_cve)
            )
        return NOT_FOUND


def create_new_subscription(user_input, chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        subscription = Subscription(chat_id=chat_id)
        stmt = select(CVE).where(CVE.name == f"CVE-{user_input}")
        cve = session.execute(stmt).scalars().first()
        if not cve:
            return NOT_FOUND
        subscription.cve.append(cve)
        session.add(subscription)
        session.commit()
        return DONE


def remove_subscription(user_input, chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = (
            select(Subscription)
            .join(Subscription.cve)
            .where(CVE.name == f"CVE-{user_input}", Subscription.chat_id == chat_id)
        )
        subscription = session.execute(stmt).scalars().first()
        if subscription:
            session.delete(subscription)
            session.commit()
            return DONE
        return NOT_FOUND


def get_my_subscriptions(chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).join(CVE.subscriptions).where(Subscription.chat_id == chat_id)  # noqa: WPS221
        subscriptions = session.execute(stmt).scalars().all()
        if subscriptions:
            return format_my_subscriptions(subscriptions)
        return NOT_FOUND
