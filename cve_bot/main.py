import logging.config  # noqa: WPS301 WPS458

import sentry_sdk
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from cve_bot.config import get_config
from cve_bot.handlers import echo, help_command, start

config = get_config()

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "consoleFormatter": {
            "format": "%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s",
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": config["log_level"],
            "formatter": "consoleFormatter",
        }
    },
    "loggers": {"": {"level": "DEBUG", "handlers": ["console"], "propagate": True}},
}
if config["logzio_token"] is not None:
    LOGGING_CONFIG["formatters"]["logzioFormat"] = {"format": '{"additional_field": "value"}', "validate": False}
    LOGGING_CONFIG["handlers"]["logzio"] = {
        "class": "logzio.handler.LogzioHandler",
        "level": config["log_level"],
        "formatter": "logzioFormat",
        "token": config["logzio_token"],
        "logs_drain_timeout": 5,
        "url": "https://listener-uk.logz.io:8071",
    }
    LOGGING_CONFIG["loggers"][""]["handlers"].append("logzio")
logging.config.dictConfig(LOGGING_CONFIG)

if config["sentry_url"]:
    sentry_sdk.init(config["sentry_url"], traces_sample_rate=1.0)

logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(config["token"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
