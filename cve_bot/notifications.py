from sqlalchemy import select
from sqlalchemy.orm import Session
from telegram import ParseMode

from cve_bot import db
from cve_bot.formatters import format_cve, format_notification
from cve_bot.models import Notification


def send_notifications(context):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(Notification).join(Notification.subscription)
        for notification in session.execute(stmt).scalars().all():
            context.bot.send_message(
                chat_id=notification.subscription.chat_id, text=format_cve(notification.subscription.cve[0])
            )
            context.bot.send_message(
                chat_id=notification.subscription.chat_id,
                text=format_notification(notification),
                parse_mode=ParseMode.HTML,
            )
            session.delete(notification)
            session.commit()
