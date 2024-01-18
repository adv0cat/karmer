import os
import asyncpg

from datetime import datetime, timezone
from pydantic import BaseModel, PositiveInt, Field


async def init_postgres_db() -> asyncpg.Connection:
    print('init postgres db')
    host = os.environ.get("POSTGRES_HOST") or 'localhost'
    port = int(os.environ.get("POSTGRES_PORT") or '5432')
    database = os.environ.get("POSTGRES_DB")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")

    # Connecting
    return await asyncpg.connect(user=user, password=password, database=database, host=host, port=port)


class Reaction(BaseModel):
    channel_id: PositiveInt
    msg_id: PositiveInt
    from_user_id: PositiveInt
    to_user_id: PositiveInt
    emoticon: str = ''
    count: PositiveInt
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def to_tuple(self):
        return (
            self.channel_id,
            self.msg_id,
            self.from_user_id,
            self.to_user_id,
            self.emoticon,
            self.count,
            self.date
        )

    def to_pkey_tuple(self):
        return (
            self.channel_id,
            self.msg_id,
            self.from_user_id,
            self.emoticon
        )

    def is_valid(self):
        return self.from_user_id is not self.to_user_id


class ReactionCost(BaseModel):
    emoticon: str = ''
    cost: PositiveInt
