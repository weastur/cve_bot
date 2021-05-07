from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine

from cve_bot.config import get_config


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


def get_engine(echo=False):
    config = get_config()
    return create_engine(f"sqlite:///{config['db_path']}", echo=echo)
