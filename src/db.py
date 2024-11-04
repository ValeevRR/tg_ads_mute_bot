import sqlite3

DB = "mute_users.db"

def create_db():
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS mutes(chat_id INTEGER, username TEXT, PRIMARY KEY(chat_id, username));")


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
        cur.execute(f"DELETE FROM mutes WHERE chat_id={chat_id} AND username='{username}'")


def get_chat_mutes(chat_id: int):
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        cur.execute(f"SELECT username FROM mutes WHERE chat_id={chat_id}")
        return [username[0] for username in cur.fetchall()]


def is_muted_user(chat_id: int, username: str) -> bool:
    with sqlite3.connect(DB) as con:
        cur = con.cursor()
        user = cur.execute(f"SELECT username FROM mutes WHERE chat_id={chat_id} AND username='{username}'").fetchone()
        return bool(user)
