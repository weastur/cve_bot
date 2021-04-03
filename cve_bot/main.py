import logging.config  # noqa: WPS301 WPS458

import sentry_sdk
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Updater,
)

from cve_bot.config import get_config
from cve_bot.handlers import (
    CallBackData,
    Stage,
    info_by_cve,
    info_by_package,
    select_info_type,
    select_subscription_type,
    start,
    subscriptions_my,
    subscriptions_new,
    subscriptions_remove,
    stop,
)
from cve_bot.updaters import debian_update

config = get_config()

logging_config = {
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
    logging_config["formatters"]["logzioFormat"] = {"format": '{"additional_field": "value"}', "validate": False}
    logging_config["handlers"]["logzio"] = {
        "class": "logzio.handler.LogzioHandler",
        "level": config["log_level"],
        "formatter": "logzioFormat",
        "token": config["logzio_token"],
        "logs_drain_timeout": 5,
        "url": "https://listener-uk.logz.io:8071",
    }
    logging_config["loggers"][""]["handlers"].append("logzio")
logging.config.dictConfig(logging_config)

if config["sentry_url"]:
    sentry_sdk.init(config["sentry_url"], traces_sample_rate=1.0)

logger = logging.getLogger(__name__)


def main() -> None:
    scheduler = BackgroundScheduler(
        {
            "apscheduler.executors.default": {
                "class": "apscheduler.executors.pool:ThreadPoolExecutor",
                "max_workers": "1",
            },
        }
    )
    scheduler.add_job(debian_update, CronTrigger.from_crontab(config["update_cron"]))
    scheduler.start()

    updater = Updater(config["token"])

    dispatcher = updater.dispatcher

    subscriptions_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_subscription_type, pattern=f"^{CallBackData.subscription}$")],
        states={
            Stage.subscription: [
                CallbackQueryHandler(subscriptions_my, pattern=f"^{CallBackData.subscriptions_my}$"),
                CallbackQueryHandler(subscriptions_remove, pattern=f"^{CallBackData.subscriptions_remove}$"),
                CallbackQueryHandler(subscriptions_new, pattern=f"^{CallBackData.subscriptions_new}$"),
            ],
        },
        fallbacks=[CallbackQueryHandler(select_subscription_type, pattern=f"^{CallBackData.subscription}$")],
    )

    info_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_info_type, pattern=f"^{CallBackData.info}$")],
        states={
            Stage.info: [
                CallbackQueryHandler(info_by_package, pattern=f"^{CallBackData.info_by_package}$"),
                CallbackQueryHandler(info_by_cve, pattern=f"^{CallBackData.info_by_cve}$"),
            ],
        },
        fallbacks=[CallbackQueryHandler(select_info_type, pattern=f"^{CallBackData.info}$")],
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            Stage.direction: [
                info_conv_handler,
                subscriptions_conv_handler,
            ],
        },
        fallbacks=[CommandHandler("start", stop)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
