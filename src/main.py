import telebot
import logging
import os

from db import (
    create_db,
    is_muted_user,
)
from const import REQUEST_USERNAME
from helpers import (
    mute_user,
    unmute_user,
    is_allowed_message,
    get_chat_mutes_message,
    add_allowed_substr,
    remove_allowed_substr
)

logging.basicConfig(level=logging.INFO)


API_TOKEN = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

create_db()


def request_allowed_substr(message, callback):
    request_message = bot.send_message(message.chat.id, 'Введите подстроку:')
    bot.register_next_step_handler(request_message, callback, message.text)


@bot.message_handler(commands=["mute"])
def mute_user_handler(message):
    message = bot.send_message(message.chat.id, REQUEST_USERNAME)
    bot.register_next_step_handler(message, mute_user)


@bot.message_handler(commands=["unmute"])
def unmute_user_handler(message):
    message = bot.send_message(message.chat.id, REQUEST_USERNAME)
    bot.register_next_step_handler(message, unmute_user)


@bot.message_handler(commands=["add_allowed_substr"])
def allow_substr_handler(message):
    request_message = bot.send_message(message.chat.id, REQUEST_USERNAME)
    bot.register_next_step_handler(request_message, request_allowed_substr, add_allowed_substr)


@bot.message_handler(commands=["remove_allowed_substr"])
def unallow_substr_handler(message):
    request_message = bot.send_message(message.chat.id, REQUEST_USERNAME)
    bot.register_next_step_handler(request_message, request_allowed_substr, remove_allowed_substr)


@bot.message_handler(commands=["mutes"])
def chat_mutes_handler(message):
    mutes_message = get_chat_mutes_message(message.chat.id)
    bot.send_message(message.chat.id, mutes_message)


@bot.message_handler()
def message_handler(message):
    if is_muted_user(message.chat.id, message.from_user.username) and not (
        is_allowed_message(message.text, message.from_user.username, message.chat.id)
    ):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


bot.infinity_polling()
