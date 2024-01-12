import asyncio
import asyncpg
import os

from typing import Coroutine, Any
from const import get_max_offset
from parse import parse_telegram
from telethon import TelegramClient

PARSE_TELEGRAM_INTERVAL = 10


async def init_telegram_client(code_queue: asyncio.Queue, postgres: asyncpg.Connection):
    print('init telegram client')
    telegram_client = await get_telegram_client(code_queue)
    await run_telegram_loop(telegram_client, postgres)


def get_telegram_client(code_queue: asyncio.Queue) -> Coroutine[Any, Any, TelegramClient]:
    print('get telegram client')
    api_id = int(os.environ.get('API_ID') or 0)
    api_hash = os.environ.get('API_HASH')

    telegram_client = TelegramClient(session='__session/karmer-docker', api_id=api_id, api_hash=api_hash)
    return telegram_client.start(phone=get_phone, password=get_password, code_callback=code_queue.get)  # type: ignore


async def run_telegram_loop(app: TelegramClient, postgres: asyncpg.Connection):
    max_offset = get_max_offset()
    while True:
        print('start telegram loop')
        await parse_telegram(app, postgres, max_offset)
        print(f'{PARSE_TELEGRAM_INTERVAL}s waiting...')
        await asyncio.sleep(PARSE_TELEGRAM_INTERVAL)


def get_phone():
    return os.environ.get('PHONE')


def get_password():
    return os.environ.get('PASSWORD')
