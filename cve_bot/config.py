import os
import types


def get_config():
    return types.MappingProxyType(
        {
            "token": os.environ.get("CVE_BOT_TOKEN"),
            "logzio_token": os.environ.get("CVE_BOT_LOGZIO_TOKEN"),
            "sentry_url": os.environ.get("CVE_BOT_SENTRY_URL"),
            "log_level": os.environ.get("CVE_BOT_LOG_LEVEL", "INFO"),
            "db_path": os.environ.get("CVE_BOT_DB_PATH", "./main.db"),
        }
    )
