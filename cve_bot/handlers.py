from telegram import Update
from telegram.ext import CallbackContext


def start(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Hi!")


def help_command(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Help!")


def echo(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(update.message.text)
