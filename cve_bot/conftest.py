import os
import sys

import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker


def pytest_configure(config):
    sys._called_from_test = True  # noqa: WPS437


def pytest_unconfigure(config):
    del sys._called_from_test  # noqa: WPS437 WPS420


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

    load_sql_fixture(pkg_root, session_factory)
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
    session = db["session_factory"]()
    yield session
    session.rollback()
    session.close()
