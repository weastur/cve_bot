import logging
import logging.config  # noqa: WPS301 WPS458
import os

import sentry_sdk
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


def configure_logging(logzio_token=None, loglevel="INFO"):
    config = {
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
                "level": loglevel,
                "formatter": "consoleFormatter",
            }
        },
        "loggers": {"": {"level": "DEBUG", "handlers": ["console"], "propagate": True}},
    }
    if logzio_token is not None:
        config["formatters"]["logzioFormat"] = {"format": '{"additional_field": "value"}', "validate": False}
        config["handlers"]["logzio"] = {
            "class": "logzio.handler.LogzioHandler",
            "level": loglevel,
            "formatter": "logzioFormat",
            "token": logzio_token,
            "logs_drain_timeout": 5,
            "url": "https://listener-uk.logz.io:8071",
        }
        config["loggers"][""]["handlers"].append("logzio")
    logging.config.dictConfig(config)


configure_logging(os.environ.get("CVE_BOT_LOGZIO_TOKEN"), os.environ.get("CVE_BOT_LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

sentry_url = os.environ.get("CVE_BOT_SENTRY_URL")
if sentry_url:
    sentry_sdk.init(sentry_url, traces_sample_rate=1.0)


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Hi!")


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Help!")


def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)


def main() -> None:
    updater = Updater(os.environ["CVE_BOT_TOKEN"])

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
