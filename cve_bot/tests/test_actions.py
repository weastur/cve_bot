from unittest.mock import patch

from sqlalchemy import func, select

from cve_bot.actions import (
    DONE,
    NOT_FOUND,
    create_new_subscription,
    get_cve_info,
    get_my_subscriptions,
    get_package_info,
    remove_subscription,
)
from cve_bot.models import Subscription


def test_get_my_subscirptions(db, session):
    with patch("cve_bot.actions.db.get_engine", return_value=db["engine"]):
        assert get_my_subscriptions(100) == NOT_FOUND
        assert get_my_subscriptions(1) != NOT_FOUND


def test_get_cve_info(db, session):
    with patch("cve_bot.actions.db.get_engine", return_value=db["engine"]):
        assert get_cve_info("0000-00000", 1) == NOT_FOUND
        assert get_cve_info("2021-0001", 1) != NOT_FOUND


def test_get_package_info(db, session):
    with patch("cve_bot.actions.db.get_engine", return_value=db["engine"]):
        assert get_package_info("my-supercool-package", 1) == NOT_FOUND
        assert get_package_info("package0", 1) != NOT_FOUND


def test_remove_subscirption(db, session):
    with patch("cve_bot.actions.db.get_engine", return_value=db["engine"]):
        assert remove_subscription("1234-0000", 1) == NOT_FOUND
        assert remove_subscription("2021-0001", 1) == DONE
        stmt = select(func.count("*")).select_from(Subscription)
        assert session.execute(stmt).scalars().one() == 2


def test_create_new_subscirption(db, session):
    with patch("cve_bot.actions.db.get_engine", return_value=db["engine"]):
        assert create_new_subscription("1234-0000", 1) == NOT_FOUND
        assert create_new_subscription("2021-0003", 2) == DONE
        stmt = select(func.count("*")).select_from(Subscription)
        assert session.execute(stmt).scalars().one() == 4
