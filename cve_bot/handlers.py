import enum
import logging
import types

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
)
from telegram.ext import CallbackContext, ConversationHandler

from cve_bot import actions
from cve_bot.messages import MessageSplitter

START_OVER = "START_OVER"
ACTION = "ACTION"
MAX_MSG_LEN = 4096


class Action(enum.IntEnum):
    info_by_package = 0
    info_by_cve = 1
    subscriptions_new = 2
    subscriptions_remove = 3


ACTION_MAPPING = types.MappingProxyType(
    {
        Action.info_by_package: actions.get_package_info,
        Action.info_by_cve: actions.get_cve_info,
        Action.subscriptions_new: actions.create_new_subscription,
        Action.subscriptions_remove: actions.remove_subscription,
    }
)


class Stage(enum.IntEnum):
    direction = 0
    info = 1  # noqa: WPS110
    subscription = 2
    stopping = 3
    info_typing = 4
    end = ConversationHandler.END


class CallBackData(str, enum.Enum):  # noqa: WPS600
    start = "start"
    info = "info"  # noqa: WPS110
    subscription = "subscriptions"
    info_by_package = "info_by_package"
    info_by_cve = "info_by_cve"
    info_back = "info_back"
    subscriptions_my = "subscriptions_my"
    subscriptions_new = "subscriptions_new"
    subscriptions_remove = "subscriptions_remove"
    subscriptions_back = "subscriptions_back"


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext) -> int:
    text = "You may choose to get info from CVE database or work with your subscriptions. To abort, simply type /stop."
    buttons = [
        [
            InlineKeyboardButton(text="Get info from DB", callback_data=CallBackData.info),
            InlineKeyboardButton(text="Subscriptions", callback_data=CallBackData.subscription),
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    if context.user_data.get(START_OVER):
        update.callback_query.answer()
        update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    else:
        update.message.reply_text(
            "Hi, I'm Package CVE bot and I'm here to help you gather information about debian packages CVE."
        )
        update.message.reply_text(text=text, reply_markup=keyboard)
    context.user_data[START_OVER] = False
    return Stage.direction


def select_info_type(update: Update, _: CallbackContext) -> int:
    text = "Get info by package or CVE name"
    buttons = [
        [
            InlineKeyboardButton(text="By package", callback_data=CallBackData.info_by_package),
            InlineKeyboardButton(text="By CVE", callback_data=CallBackData.info_by_cve),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=CallBackData.info_back),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return Stage.info


def select_subscription_type(update: Update, _: CallbackContext) -> int:
    text = "Subscriptions info"
    buttons = [
        [
            InlineKeyboardButton(text="My subscriptions", callback_data=CallBackData.subscriptions_my),
            InlineKeyboardButton(text="New", callback_data=CallBackData.subscriptions_new),
            InlineKeyboardButton(text="Remove", callback_data=CallBackData.subscriptions_remove),
        ],
        [
            InlineKeyboardButton(text="Back", callback_data=CallBackData.subscriptions_back),
        ],
    ]
    keyboard = InlineKeyboardMarkup(buttons)
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)
    return Stage.subscription


def info_by_cve(update: Update, context: CallbackContext) -> int:
    text = "Enter CVE number. `YYYY-XXXXX` from `CVE-YYYY-XXXXX`"
    context.user_data[ACTION] = Action.info_by_cve
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)
    return Stage.info_typing


def info_by_package(update: Update, context: CallbackContext) -> int:
    text = "Enter package name"
    context.user_data[ACTION] = Action.info_by_package
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)
    return Stage.info_typing


def subscriptions_my(update: Update, ctx: CallbackContext) -> int:
    reply_text_all = actions.get_my_subscriptions(update.effective_chat.id)
    update.callback_query.answer()
    for msg in MessageSplitter(reply_text_all):
        update.effective_chat.send_message(text=msg, parse_mode=ParseMode.HTML)
    return Stage.stopping


def subscriptions_new(update: Update, context: CallbackContext) -> int:
    text = "Enter CVE name to subscribe to. `YYYY-XXXXX` from `CVE-YYYY-XXXXX`"
    context.user_data[ACTION] = Action.subscriptions_new
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)
    return Stage.info_typing


def subscriptions_remove(update: Update, context: CallbackContext) -> int:
    text = "Enter CVE name to unsubscribe. `YYYY-XXXXX` from `CVE-YYYY-XXXXX`"
    context.user_data[ACTION] = Action.subscriptions_remove
    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, parse_mode=ParseMode.MARKDOWN)
    return Stage.info_typing


def stop(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Okay, bye.")
    return Stage.end


def end_second_level(update: Update, context: CallbackContext) -> int:
    context.user_data[START_OVER] = True
    start(update, context)
    return Stage.end


def stop_nested(update: Update, _: CallbackContext) -> int:
    update.message.reply_text("Okay, bye.")
    return Stage.stopping


def process_user_input(update: Update, context: CallbackContext):
    action = context.user_data.pop(ACTION)
    reply_text_all = ACTION_MAPPING[action](update.message.text, update.effective_chat["id"])
    for msg in MessageSplitter(reply_text_all):
        update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    return Stage.stopping
