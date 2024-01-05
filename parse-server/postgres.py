import os
import asyncpg


async def init_postgres_db() -> asyncpg.Connection:
    print('init postgres db')
    host = os.environ.get("POSTGRES_HOST") or 'localhost'
    port = int(os.environ.get("POSTGRES_PORT") or '5432')
    database = os.environ.get("POSTGRES_DB")
    user = os.environ.get("POSTGRES_USER")
    password = os.environ.get("POSTGRES_PASSWORD")

    # Connecting
    return await asyncpg.connect(user=user, password=password, database=database, host=host, port=port)


class Reaction:
    def __init__(self, channel_id: int = 0, msg_id: int = 0, from_user_id: int = 0, to_user_id: int = 0,
                 emoticon: str = '', count: int = 0):
        self.channel_id = channel_id
        self.msg_id = msg_id
        self.from_user_id = from_user_id
        self.to_user_id = to_user_id
        self.emoticon = emoticon
        self.count = count

    @classmethod
    def from_record(cls, record: asyncpg.Record):
        return cls(channel_id=record['channel_id'], msg_id=record['msg_id'], from_user_id=record['from_user_id'],
                   to_user_id=record['to_user_id'], emoticon=record['emoticon'], count=record['count'])

    def to_tuple(self):
        return (
            self.channel_id,
            self.msg_id,
            self.from_user_id,
            self.to_user_id,
            self.emoticon,
            self.count
        )

    def __repr__(self):
        return (f'Reaction(channel_id={self.channel_id}, msg_id={self.msg_id}, '
                f'from_user_id={self.from_user_id}, to_user_id={self.to_user_id}, '
                f'emoticon="{self.emoticon}", count={self.count})')


class ReactionCost:
    def __init__(self, emoticon: str = '', cost: int = 0):
        self.emoticon = emoticon
        self.cost = cost

    @classmethod
    def from_record(cls, record: asyncpg.Record):
        return cls(emoticon=record['emoticon'], cost=record['cost'])

    def __repr__(self):
        return f'ReactionCost(emoticon="{self.emoticon}", cost={self.cost})'
