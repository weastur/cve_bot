import logging

from sqlalchemy import select
from sqlalchemy.orm import Session
from telegram import ParseMode

from cve_bot import db
from cve_bot.formatters import format_cve, format_notification
from cve_bot.messages import MessageSplitter
from cve_bot.models import Notification
from cve_bot.perf import track

logger = logging.getLogger(__name__)


@track(10)
def send_notifications(context):
    db_engine = db.get_engine()
    with Session(db_engine) as session:
        stmt = select(Notification).join(Notification.subscription)
        for notification in session.execute(stmt).scalars().all():
            logger.info("Send notification to chat: %d", notification.subscription.chat_id)
            for cve_msg in MessageSplitter(format_cve(notification.subscription.cve)):
                context.bot.send_message(
                    chat_id=notification.subscription.chat_id, text=cve_msg, parse_mode=ParseMode.HTML
                )
            for notification_msg in MessageSplitter(format_notification(notification)):
                context.bot.send_message(
                    chat_id=notification.subscription.chat_id,
                    text=notification_msg,
                    parse_mode=ParseMode.HTML,
                )
            session.delete(notification)
            session.commit()
