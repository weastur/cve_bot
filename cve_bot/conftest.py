import os

import pytest
from alembic.command import upgrade as alembic_upgrade
from alembic.config import Config as AlembicConfig
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope="session")
def db():
    engine = create_engine("sqlite:///./test.db", echo=True)
    session_factory = sessionmaker(bind=engine)

    pkg_root = os.path.dirname(os.path.realpath(__file__))
    alembic_config = AlembicConfig(os.path.join(pkg_root, "alembic.ini"))
    alembic_config.set_main_option("sqlalchemy.url", "sqlite:///./test.db")
    alembic_config.set_main_option("script_location", os.path.join(pkg_root, "migrations"))
    alembic_upgrade(alembic_config, "head")
    yield {
        "engine": engine,
        "session_factory": session_factory,
    }
    engine.dispose()


@pytest.fixture(scope="function")
def session(db):
    session = db["session_factory"]()
    yield session
    session.rollback()
    session.close()
