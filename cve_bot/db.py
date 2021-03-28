from sqlalchemy import create_engine

from cve_bot.config import get_config


def get_engine():
    config = get_config()
    return create_engine(f"sqlite:///{config['db_path']}")
