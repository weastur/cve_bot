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

NOT_FOUND = "*Not found*"


def _get_package_info_for_cve(session, cve):
    stmt = select(PackageCVE).where(PackageCVE.cve_name == cve.name)  # noqa: WPS221
    package_cve = session.execute(stmt).scalars().all()
    return format_cve_with_packages(cve, package_cve)


def get_package_info(user_input):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).join(CVE.packages).where(PackageCVE.package_name == user_input)  # noqa: WPS221
        cve = session.execute(stmt).scalars().all()
        if cve:
            return "".join(map(partial(_get_package_info_for_cve, session), cve))
        return NOT_FOUND


def get_cve_info(user_input):
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


def create_new_subscription(user_input):
    return f"create new subscription {user_input}"


def remove_subscription(user_input):
    return f"remove subscription {user_input}"


def get_my_subscriptions(chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).join(CVE.subscriptions).where(Subscription.chat_id == chat_id)  # noqa: WPS221
        subscriptions = session.execute(stmt).scalars().all()
        if subscriptions:
            return format_my_subscriptions(subscriptions)
        return NOT_FOUND
