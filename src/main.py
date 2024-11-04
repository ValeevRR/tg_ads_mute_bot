import telebot
import logging
import os

from db import (
    create_db,
    mute_user_db,
    unmute_user_db,
    is_muted_user,
    get_chat_mutes
)

logging.basicConfig(level=logging.INFO)


API_TOKEN = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(API_TOKEN)

create_db()


def mute_user(message):
    chat_id = message.chat.id
    username = message.text
    mute_user_db(chat_id, username)


def unmute_user(message):
    chat_id = message.chat.id
    username = message.text
    unmute_user_db(chat_id, username)


@bot.message_handler(content_types=['photo'])
def group_chat_photo_handler(message):
    if is_muted_user(message.chat.id, message.from_user.username):
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.message_handler(commands=["mute"])
def mute_user_handler(message):
    message = bot.send_message(message.chat.id, 'Введите username')
    bot.register_next_step_handler(message, mute_user)


@bot.message_handler(commands=["unmute"])
def unmute_user_handler(message):
    message = bot.send_message(message.chat.id, 'Введите username')
    bot.register_next_step_handler(message, unmute_user)


@bot.message_handler(commands=["mutes"])
def chat_mutes_handler(message):
    mutes = get_chat_mutes(message.chat.id)
    bot.send_message(message.chat.id, f"Заблокированные:\n{', '.join(mutes)}")


bot.infinity_polling()
