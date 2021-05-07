import os
import sys

import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy import create_engine, delete, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from cve_bot.models import Base


def pytest_configure(config):
    sys._called_from_test = True  # noqa: WPS437


def pytest_unconfigure(config):
    del sys._called_from_test  # noqa: WPS437 WPS420


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture(scope="session")
def db():
    pkg_root = os.path.dirname(os.path.realpath(__file__))
    db_path = os.path.join(pkg_root, "test.db")
    if os.path.exists(db_path):
        os.remove(db_path)
    engine = create_engine(f"sqlite:///{db_path}", echo=True)
    session_factory = sessionmaker(bind=engine)

    alembic_config = AlembicConfig(os.path.join(pkg_root, "alembic.ini"))
    alembic_config.set_main_option("sqlalchemy.url", f"sqlite:///{db_path}")
    alembic_config.set_main_option("script_location", os.path.join(pkg_root, "migrations"))
    alembic_upgrade(alembic_config, "head")

    yield {
        "engine": engine,
        "session_factory": session_factory,
    }
    engine.dispose()


def load_sql_fixture(pkg_root, session_factory):
    session = session_factory()
    with open(os.path.join(pkg_root, "fixture.sql")) as sql_fixture:
        for stmt in sql_fixture:
            session.execute(text(stmt))
    session.commit()
    session.close()


@pytest.fixture(scope="function")
def session(db):
    pkg_root = os.path.dirname(os.path.realpath(__file__))
    load_sql_fixture(pkg_root, db["session_factory"])
    session = db["session_factory"]()
    yield session
    session.rollback()
    for table in Base.metadata.sorted_tables:
        session.execute(delete(table))
    session.commit()
    session.close()
