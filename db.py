import sqlite3
import logging

DB = "mute_users.db"


def create_db():
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        with open("./src/init.sql", "r") as sql_file:
            init_script = sql_file.read()
        cur.executescript(init_script)
        logging.info("Database created.")


def mute_user_db(chat_id: int, username: str):
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        try:
            cur.execute("INSERT INTO mutes (chat_id, username) VALUES (%s, '%s');" % (chat_id, username))
        except sqlite3.IntegrityError:
            pass


def unmute_user_db(chat_id: int, username: str):
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute(
            f"DELETE FROM mutes WHERE chat_id={chat_id} AND username='{username}';"
        )


def add_allowed_substr_db(chat_id: int, username: str, allowed_substr: str):
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        try:
            cur.execute(
                "INSERT INTO allowed_substr (muted_chat_id, muted_username, allowed_substr) VALUES (%s, '%s', '%s');"
                % (chat_id, username, allowed_substr))
        except sqlite3.IntegrityError:
            pass


def remove_allowed_substr_db(chat_id: int, username: str, allowed_substr: str):
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute(
            f"DELETE FROM allowed_substr WHERE muted_chat_id={chat_id} AND muted_username='{username}' AND allowed_substr='{allowed_substr}';"
        )


def get_chat_mute_usernames(chat_id: int) -> list[str]:
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute(f"SELECT username FROM mutes WHERE chat_id={chat_id}")
        return [(r[0]) for r in cur.fetchall()]


def is_muted_user(chat_id: int, username: str) -> bool:
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        user = cur.execute(f"SELECT username FROM mutes WHERE chat_id={chat_id} AND username='{username}'").fetchone()
        return bool(user)


def get_allowed_substrings_by_usernames(chat_id: int, usernames: list[str]) -> list[tuple[str, str]]:
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        usernames_str = ','.join([f"'{u}'" for u in usernames])
        cur.execute(
            f"SELECT allowed_substr, muted_username FROM allowed_substr WHERE muted_chat_id={chat_id} AND muted_username IN ({usernames_str});"
        )
        return [(r[0], r[1]) for r in cur.fetchall()]
