import enum
import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext, ConversationHandler


START_OVER = 'START_OVER'


class Stage(enum.IntEnum):
    direction = 0
    info = 1  # noqa: WPS110
    subscription = 2
    stopping = 3
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
        ]
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
        ]
    ]
    keyboard = InlineKeyboardMarkup(buttons)

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text, reply_markup=keyboard)

    return Stage.subscription


def info_by_cve(update: Update, _: CallbackContext) -> int:
    text = "CVE info"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return Stage.stopping


def info_by_package(update: Update, _: CallbackContext) -> int:
    text = "Package info"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return Stage.stopping


def subscriptions_my(update: Update, _: CallbackContext) -> int:
    text = "My subscriptions"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return Stage.subscription


def subscriptions_new(update: Update, _: CallbackContext) -> int:
    text = "New subscriptions"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return Stage.subscription


def subscriptions_remove(update: Update, _: CallbackContext) -> int:
    text = "Remove subscriptions"

    update.callback_query.answer()
    update.callback_query.edit_message_text(text=text)

    return Stage.subscription


def stop(update: Update, _: CallbackContext) -> int:
    update.message.reply_text('Okay, bye.')

    return Stage.end


def end_second_level(update: Update, context: CallbackContext) -> int:
    context.user_data[START_OVER] = True
    start(update, context)

    return Stage.end