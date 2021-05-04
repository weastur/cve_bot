from unittest.mock import Mock, patch

from sqlalchemy import select

from cve_bot.models import Notification
from cve_bot.notifications import send_notifications


def test_send_notifications(db, session):
    context = Mock()
    with patch("cve_bot.notifications.db.get_engine", return_value=db["engine"]):
        send_notifications(context)
    assert context.bot.send_message.call_count == 6

    stmt = select(Notification)
    assert session.execute(stmt).scalars().all() == []  # noqa: WPS520
