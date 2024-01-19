import asyncio
import asyncpg
import os

from typing import Coroutine, Any
from const import get_max_offset
from parse import parse_telegram
from tg_command import TgCommand
from peer import get_peer_id
from full_name import get_full_name
from sql_query import GET_MY_KARMA_SQL, GET_ALL_KARMA_SQL
from pg_pool import UserKarma
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.types import User

PARSE_TELEGRAM_INTERVAL = 10


async def init_telegram_client(code_queue: asyncio.Queue, pg_pool: asyncpg.Pool):
    print('init telegram client')
    tg = await get_telegram_client(code_queue)

    me = await tg.get_me()
    pattern = f'.*@{me.username}'

    @tg.on(events.NewMessage(incoming=True, forwards=False, pattern=pattern))
    async def handler(event: events.NewMessage.Event):
        message: Message = event.message
        if message.mentioned:
            sender: User = await message.get_sender()
            await event.reply(TgCommand.get_list_for(sender))

    @tg.on(events.NewMessage(incoming=True, forwards=False, pattern='^/'))
    async def handler(event: events.NewMessage.Event):
        message: Message = event.message
        raw_text = message.raw_text
        if TgCommand.JUST_HELP in raw_text:
            await event.reply(f'Если ты спрашиваешь меня, жми {TgCommand.HELP}')
        elif TgCommand.HELP in raw_text:
            sender: User = await message.get_sender()
            await event.reply(TgCommand.get_list_for(sender))
        elif TgCommand.KARMA in raw_text:
            async with pg_pool.acquire() as pg_conn:
                pg_conn: asyncpg.Connection
                user_id = get_peer_id(message.from_id)
                channel_id = get_peer_id(message.peer_id)
                my_karma = await pg_conn.fetchval(GET_MY_KARMA_SQL, channel_id, user_id)
            sender: User = await message.get_sender()
            await event.reply(f'{get_full_name(sender)}, вот твоя карма: {my_karma}')
        elif TgCommand.ALL_KARMA in raw_text:
            async with pg_pool.acquire() as pg_conn:
                pg_conn: asyncpg.Connection
                channel_id = get_peer_id(message.peer_id)
                raw_all_karma: list[asyncpg.Record] = await pg_conn.fetch(GET_ALL_KARMA_SQL, channel_id)
            all_karma = [UserKarma.model_validate(dict(v)) for v in raw_all_karma]
            await asyncio.gather(*[user.parse_tg(tg) for user in all_karma])
            all_karma_str = [f'{i}. {v.full_name} - {v.total_karma}' for i, v in enumerate(all_karma, start=1)]
            await event.reply(f'Карма юзеров этого чатика:\n\n' + '\n'.join(all_karma_str))

    max_offset = get_max_offset()
    async for _ in run_infinite_loop():
        print('ready to parse telegram')
        await parse_telegram(tg, pg_pool, max_offset)


def get_telegram_client(code_queue: asyncio.Queue) -> Coroutine[Any, Any, TelegramClient]:
    print('get telegram client')
    api_id = int(os.environ.get('API_ID') or 0)
    api_hash = os.environ.get('API_HASH')

    tg = TelegramClient(session='__session/karmer-docker', api_id=api_id, api_hash=api_hash)
    return tg.start(phone=get_phone, password=get_password, code_callback=code_queue.get)  # type: ignore


async def run_infinite_loop():
    while True:
        yield
        print(f'{PARSE_TELEGRAM_INTERVAL}s waiting...')
        await asyncio.sleep(PARSE_TELEGRAM_INTERVAL)


def get_phone():
    return os.environ.get('PHONE')


def get_password():
    return os.environ.get('PASSWORD')
