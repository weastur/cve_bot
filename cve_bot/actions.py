from sqlalchemy import select
from sqlalchemy.orm import Session

from cve_bot import db
from cve_bot.models import CVE, Subscription

NOT_FOUND = "*Not found*"


def get_package_info(user_input):
    return f"{user_input} info"


def get_cve_info(user_input):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).where(CVE.name == f"CVE-{user_input}")  # noqa: WPS221
        cve = session.execute(stmt).scalars().first()
        if cve:
            return _format_cve(cve)
        return NOT_FOUND


def create_new_subscription(user_input):
    return f"create new subscription {user_input}"


def remove_subscription(user_input):
    return f"remove subscription {user_input}"


def _format_cve(cve):
    return f"*{cve.name}*\n```\n{cve.description}\n```\n"


def _format_my_subscriptions(result_cve):
    reply_text = ""
    for cve in result_cve:
        reply_text = "{reply_text}{formatted_cve}".format(reply_text=reply_text, formatted_cve=_format_cve(cve))
    return reply_text


def get_my_subscriptions(chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).join(CVE.subscriptions).where(Subscription.chat_id == chat_id)  # noqa: WPS221
        subscriptions = session.execute(stmt).scalars().all()
        if subscriptions:
            return _format_my_subscriptions(subscriptions)
        return NOT_FOUND
