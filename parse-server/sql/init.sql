CREATE TABLE Reactions
(
    channel_id   INTEGER,
    msg_id       INTEGER,
    from_user_id INTEGER,
    to_user_id   INTEGER,
    emoticon     TEXT CHECK (CHAR_LENGTH(emoticon) <= 50),
    count        INTEGER DEFAULT 1,
    created_at   TIMESTAMP WITH TIME ZONE NOT NULL,
    PRIMARY KEY (channel_id, msg_id, from_user_id, emoticon)
);

CREATE TABLE ReactionCost
(
    emoticon TEXT CHECK (CHAR_LENGTH(emoticon) <= 50) PRIMARY KEY,
    cost     INTEGER NOT NULL
);

