CREATE TABLE IF NOT EXISTS mutes (
    chat_id INTEGER,
    username TEXT,
    PRIMARY KEY(chat_id, username)
);

CREATE TABLE IF NOT EXISTS allowed_substr (
    muted_chat_id INTEGER,
    muted_username TEXT,
    allowed_substr TEXT,
    FOREIGN KEY(muted_chat_id, muted_username) REFERENCES mutes(chat_id, username)
);