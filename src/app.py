import os
import traceback

import requests
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from . import utils

TELEGRAM_CHANNEL_TOKEN = os.environ["TELEGRAM_CHANNEL_TOKEN"]
CHINESE_ID_CARD_API_HOST = os.environ["CHINESE_ID_CARD_API_HOST"]


def hello(update, context):
    del context
    update.message.reply_text(
        f"Hello, {update.message.from_user.first_name}!\n"
        f"You can send photo of chinese id card here, and I will try to recognize all text on it."
    )


def recognize_text(update, context):
    del context
    if update.message.document.mime_type == "image/jpeg":
        try:
            print_file_details(update.message.document)
            byte_array = update.message.document.get_file().download_as_bytearray()
            resp = requests.post(
                f"http://{CHINESE_ID_CARD_API_HOST}/get_text",
                files={"file": (update.message.document.file_name, byte_array, "image/jpeg")},
            )
            if not is_response_correct(resp, bot=update):
                return
            message = "\n".join(f"{key.capitalize()}: {value}" for key, value in resp.json().items())
            update.message.reply_text(message)
        except:
            traceback.print_exc()
            update.message.reply_text(traceback.format_exc())


def print_file_details(document):
    name = f"{document.file_name[:20]}..." if len(document.file_name) > 20 else document.file_name
    print(f"Received img: {name} ({utils.sizeof_fmt(document.file_size)})")


def is_response_correct(resp, bot) -> bool:
    if resp.status_code != 200:
        handle_bad_response(resp, bot)
        return False
    card_text = resp.json()
    if not isinstance(card_text, dict):
        handle_bad_response(resp, bot)
        return False
    return True


def handle_bad_response(resp, bot):
    msg = f"response status: {resp.status_code}; text: {resp.text}"
    print(msg)
    bot.message.reply_text(msg)


if __name__ == "__main__":
    print(f"TELEGRAM_CHANNEL_TOKEN: {TELEGRAM_CHANNEL_TOKEN}")
    print(f"CHINESE_ID_CARD_API_HOST: {CHINESE_ID_CARD_API_HOST}")

    updater = Updater(TELEGRAM_CHANNEL_TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("hello", hello))

    updater.dispatcher.add_handler(MessageHandler(Filters.document.image, recognize_text))

    updater.start_polling()
    updater.idle()
