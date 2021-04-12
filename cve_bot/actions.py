from sqlalchemy import select
from sqlalchemy.orm import Session

from cve_bot import db
from cve_bot.models import CVE, Subscription


def get_package_info(user_input):
    return f"{user_input} info"


def get_cve_info(user_input):
    return f"{user_input} info"


def create_new_subscription(user_input):
    return f"create new subscription {user_input}"


def remove_subscription(user_input):
    return f"remove subscription {user_input}"


def _format_my_subscriptions(result_cve):
    reply_text = ""
    for cve in result_cve:
        reply_text = f"{reply_text}*{cve.name}*\n```\n{cve.description}\n```\n"
    return reply_text


def get_my_subscriptions(chat_id):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(CVE).join(CVE.subscriptions).where(Subscription.chat_id == chat_id)  # noqa: WPS221
        return _format_my_subscriptions(session.execute(stmt).scalars().all())
