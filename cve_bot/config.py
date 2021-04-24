import multiprocessing
import os
import types

CPU_MULTIPLIER = 4


def get_config():
    return types.MappingProxyType(
        {
            "token": os.environ.get("CVE_BOT_TOKEN"),
            "logzio_token": os.environ.get("CVE_BOT_LOGZIO_TOKEN"),
            "sentry_url": os.environ.get("CVE_BOT_SENTRY_URL"),
            "log_level": os.environ.get("CVE_BOT_LOG_LEVEL", "INFO"),
            "db_path": os.environ.get("CVE_BOT_DB_PATH", "./main.db"),
            "update_interval": int(os.environ.get("CVE_BOT_UPDATE_INTERVAL", "10")),
            "notifications_offset": int(os.environ.get("CVE_BOT_NOTIFICATIONS_OFFSET", "5")),
            "workers": int(os.environ.get("CVE_BOT_WORKERS", multiprocessing.cpu_count() * CPU_MULTIPLIER)),
        }
    )
