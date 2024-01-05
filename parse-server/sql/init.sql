CREATE TABLE Reactions
(
    channel_id   INTEGER NOT NULL,
    msg_id       INTEGER NOT NULL,
    from_user_id INTEGER,
    to_user_id   INTEGER NOT NULL,
    emoticon     TEXT    NOT NULL CHECK (CHAR_LENGTH(emoticon) <= 50),
    count        INTEGER DEFAULT 1,
    PRIMARY KEY (channel_id, msg_id, from_user_id, to_user_id, emoticon)
);

CREATE TABLE ReactionCost
(
    emoticon TEXT CHECK (CHAR_LENGTH(emoticon) <= 50) PRIMARY KEY,
    cost     INTEGER NOT NULL
);

