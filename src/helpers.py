from collections import defaultdict

from src.db import (
    mute_user_db,
    unmute_user_db,
    get_chat_mute_usernames,
    get_allowed_substrings_by_usernames,
    add_allowed_substr_db,
    remove_allowed_substr_db, is_muted_user
)


def mute_user(message):
    mute_user_db(message.chat.id, message.text)


def unmute_user(message):
    unmute_user_db(message.chat.id, message.text)


def add_allowed_substr(message, username):
    is_muted = is_muted_user(message.chat.id, username)
    if is_muted:
        add_allowed_substr_db(message.chat.id, username, message.text)


def remove_allowed_substr(message, username):
    is_muted = is_muted_user(message.chat.id, username)
    if is_muted:
        remove_allowed_substr_db(message.chat.id, username, message.text)


def get_chat_mutes_message(chat_id: int):
    muted_usernames = get_chat_mute_usernames(chat_id)
    if not muted_usernames:
        return "Нет заблокированных пользователей."

    message = "Заблокированные пользователи:\n"
    allowed_substrings = get_allowed_substrings_by_usernames(chat_id, muted_usernames)
    allowed_by_user_map = defaultdict(list)
    for substr, username in allowed_substrings:
        allowed_by_user_map[username].append(substr)

    for username in muted_usernames:
        allowed_for_user = allowed_by_user_map[username]
        message += f"{username}{" (Разрешенные: " + ', '.join(allowed_for_user) + ")" if allowed_for_user else ""}\n"
    return message


def is_allowed_message(message: str, username: str, chat_id: int) -> bool:
    allowed_substrings = get_allowed_substrings_by_usernames(chat_id, [username,])
    for al_substr, _ in allowed_substrings:
        if al_substr in message:
            return True
    return False
