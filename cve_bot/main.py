import logging.config  # noqa: WPS301 WPS458

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ConversationHandler,
    Filters,
    MessageHandler,
    Updater,
)

from cve_bot.config import get_config
from cve_bot.handlers import (
    CallBackData,
    Stage,
    end_second_level,
    info_by_cve,
    info_by_package,
    process_user_input,
    select_info_type,
    select_subscription_type,
    start,
    stop,
    stop_nested,
    subscriptions_my,
    subscriptions_new,
    subscriptions_remove,
)
from cve_bot.notifications import send_notifications
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
    sentry_logging = LoggingIntegration(level=logging.INFO, event_level=logging.WARNING)
    sentry_sdk.init(config["sentry_url"], traces_sample_rate=1.0, integrations=[sentry_logging])

logger = logging.getLogger(__name__)


def main() -> None:
    updater = Updater(config["token"], workers=config["workers"])
    dispatcher = updater.dispatcher

    logger.info("Run DB update every %d sec", config["update_interval"])
    updater.job_queue.run_repeating(debian_update, interval=config["update_interval"], job_kwargs={"max_instances": 1})
    logger.info("Run notificator every %d sec", config["update_interval"])
    updater.job_queue.run_repeating(
        send_notifications,
        first=config["notifications_offset"],
        interval=config["update_interval"],
        job_kwargs={"max_instances": 1},
    )

    subscriptions_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_subscription_type, pattern=f"^{CallBackData.subscription}$")],
        states={
            Stage.subscription: [
                CallbackQueryHandler(subscriptions_my, pattern=f"^{CallBackData.subscriptions_my}$"),
                CallbackQueryHandler(subscriptions_remove, pattern=f"^{CallBackData.subscriptions_remove}$"),
                CallbackQueryHandler(subscriptions_new, pattern=f"^{CallBackData.subscriptions_new}$"),
            ],
            Stage.info_typing: [MessageHandler(Filters.text & ~Filters.command, process_user_input)],
        },
        fallbacks=[
            CallbackQueryHandler(end_second_level, pattern=f"^{CallBackData.subscriptions_back}$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={Stage.end: Stage.direction, Stage.stopping: Stage.end},
    )

    info_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(select_info_type, pattern=f"^{CallBackData.info}$")],
        states={
            Stage.info: [
                CallbackQueryHandler(info_by_package, pattern=f"^{CallBackData.info_by_package}$"),
                CallbackQueryHandler(info_by_cve, pattern=f"^{CallBackData.info_by_cve}$"),
            ],
            Stage.info_typing: [MessageHandler(Filters.text & ~Filters.command, process_user_input)],
        },
        fallbacks=[
            CallbackQueryHandler(end_second_level, pattern=f"^{CallBackData.info_back}$"),
            CommandHandler("stop", stop_nested),
        ],
        map_to_parent={Stage.end: Stage.direction, Stage.stopping: Stage.end},
    )

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            Stage.direction: [
                info_conv_handler,
                subscriptions_conv_handler,
            ],
            Stage.stopping: [CommandHandler("start", start)],
        },
        fallbacks=[CommandHandler("stop", stop)],
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
