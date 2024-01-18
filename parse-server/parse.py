import asyncio
import asyncpg

from typing import AsyncIterator, Tuple
from datetime import datetime, timezone, timedelta
from telethon.tl.types import PeerChannel
from emoticon import get_emoticon
from peer import get_peer_id
from sql_query import INSERT_REACTIONS_SQL, DELETE_REACTIONS_SQL
from pg_pool import Reaction, ReactionTuple, ReactionPKey
from telethon import TelegramClient
from telethon.tl.custom.message import Message

Reactions = Tuple[list[ReactionTuple], list[ReactionPKey], list[int]]

MIN_REACTIONS = 20
MAX_MESSAGES = 100


async def parse_telegram(tg: TelegramClient, pg_pool: asyncpg.Pool, max_offset: timedelta):
    print('start parse telegram')
    channels = [dialog.dialog.peer async for dialog in tg.iter_dialogs() if dialog.is_channel]
    print("channels:", [channel.channel_id for channel in channels])
    offset_date = datetime.now(timezone.utc) - max_offset
    await asyncio.gather(*[parse_channel(
        channel_id=channel.channel_id,
        pg_pool=pg_pool,
        reactions_iter=parse_reactions(
            tg=tg,
            channel=channel,
            offset_date=offset_date
        )
    ) for channel in channels])
    print("end parse telegram")


async def parse_channel(channel_id: int, pg_pool: asyncpg.Pool, reactions_iter: AsyncIterator[Reactions]) -> None:
    print(f'[{channel_id}] start parse channel')
    async with pg_pool.acquire() as pg_conn:
        async for tuples, p_keys, msg_ids in reactions_iter:
            if len(msg_ids) > 0:
                async with pg_conn.transaction():
                    print(f'\t\t[{channel_id}] start transaction ({len(msg_ids)}):', msg_ids)
                    await pg_conn.execute(DELETE_REACTIONS_SQL, channel_id, msg_ids, p_keys)
                    await pg_conn.executemany(INSERT_REACTIONS_SQL, tuples)

    print(f'[{channel_id}] end parse channel')


async def parse_reactions(tg: TelegramClient, channel: PeerChannel, offset_date: datetime) -> AsyncIterator[Reactions]:
    tuples: list[ReactionTuple] = []
    p_keys: list[ReactionPKey] = []
    msg_ids: list[int] = []
    async for messages in batch_messages(tg.iter_messages(entity=channel), offset_date):
        print(f'\t[{channel.channel_id}] parse batch messages ({len(messages)})')
        for message in messages:
            for reaction in get_reactions(channel.channel_id, message):
                if reaction.is_valid():
                    tuples.append(reaction.to_tuple())
                    p_keys.append(reaction.to_pkey())
                    if reaction.msg_id not in msg_ids:
                        msg_ids.append(reaction.msg_id)
        if len(msg_ids) >= MIN_REACTIONS:
            yield tuples, p_keys, msg_ids
            tuples = []
            p_keys = []
            msg_ids = []

    if len(msg_ids) > 0:
        yield tuples, p_keys, msg_ids


async def batch_messages(messages: AsyncIterator[Message], offset_date: datetime) -> AsyncIterator[list[Message]]:
    batch: list[Message] = []
    async for message in messages:
        message: Message
        if message.date < offset_date:
            break

        batch.append(message)
        if len(batch) == MAX_MESSAGES:
            yield filter_messages(batch)
            batch = []

    if len(batch) > 0:
        yield filter_messages(batch)


def filter_messages(messages: list[Message]) -> list[Message]:
    return [m for m in messages if m.reactions is not None and m.fwd_from is None]


def get_reactions(channel_id: int, message: Message) -> list[Reaction]:
    msg_id = message.id
    to_user_id = message.replies.channel_id if message.post else get_peer_id(message.from_id)

    if to_user_id is not None:
        recent_reactions = message.reactions.recent_reactions
        if recent_reactions is not None and len(recent_reactions):
            return [Reaction(
                channel_id=channel_id,
                msg_id=msg_id,
                from_user_id=reaction.peer_id.user_id,
                to_user_id=to_user_id,
                emoticon=get_emoticon(reaction.reaction),
                count=1,
                date=reaction.date
            ) for reaction in recent_reactions]
        elif message.reactions.results is not None:
            return [Reaction(
                channel_id=channel_id,
                msg_id=msg_id,
                from_user_id=0,
                to_user_id=to_user_id,
                emoticon=get_emoticon(reaction_count.reaction),
                count=reaction_count.count,
                date=message.date
            ) for reaction_count in message.reactions.results]

    return []
