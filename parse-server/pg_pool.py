import os
from typing import Tuple

import asyncpg

from datetime import datetime, timezone
from pydantic import BaseModel, PositiveInt, Field

ReactionTuple = Tuple[int, int, int, int, str, int, datetime]
ReactionPKey = Tuple[int, int, int, str]


async def init_pg_pool() -> asyncpg.Pool:
    print('init postgres pool')
    host = os.environ.get("POSTGRES_HOST") or 'localhost'
    port = int(os.environ.get("POSTGRES_PORT") or '5432')
    database = os.environ.get("POSTGRES_DB")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")

    # Connecting
    return await asyncpg.create_pool(user=user, password=password, database=database, host=host, port=port)


class Reaction(BaseModel):
    channel_id: PositiveInt
    msg_id: PositiveInt
    from_user_id: PositiveInt
    to_user_id: PositiveInt
    emoticon: str = ''
    count: PositiveInt
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_tuple(self) -> ReactionTuple:
        return (
            self.channel_id,
            self.msg_id,
            self.from_user_id,
            self.to_user_id,
            self.emoticon,
            self.count,
            self.date
        )

    def to_pkey(self) -> ReactionPKey:
        return (
            self.channel_id,
            self.msg_id,
            self.from_user_id,
            self.emoticon
        )

    def is_valid(self) -> bool:
        return self.from_user_id is not self.to_user_id


class ReactionCost(BaseModel):
    emoticon: str = ''
    cost: PositiveInt
