import asyncio
import asyncpg
import os

from typing import Coroutine, Any
from const import get_max_offset
from parse import parse_telegram
from telegram_command import TCommand
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.types import User

PARSE_TELEGRAM_INTERVAL = 10


async def init_telegram_client(code_queue: asyncio.Queue, postgres: asyncpg.Connection):
    print('init telegram client')
    telegram_client = await get_telegram_client(code_queue)

    me = await telegram_client.get_me()
    pattern = f'.*@{me.username}'

    @telegram_client.on(events.NewMessage(incoming=True, forwards=False, pattern=pattern))
    async def handler(event: events.NewMessage.Event):
        message: Message = event.message
        if message.mentioned:
            sender: User = await message.get_sender()
            await event.reply(TCommand.get_list_for(sender))

    @telegram_client.on(events.NewMessage(incoming=True, forwards=False, pattern='^/'))
    async def handler(event: events.NewMessage.Event):
        message: Message = event.message
        raw_text = message.raw_text
        if TCommand.JUST_HELP in raw_text:
            await event.reply(f'Если ты спрашиваешь меня, жми {TCommand.HELP}')
        elif TCommand.HELP in raw_text:
            sender: User = await message.get_sender()
            await event.reply(TCommand.get_list_for(sender))
        elif TCommand.KARMA in raw_text:
            await event.reply(f'Coming soon...')
        elif TCommand.ALL_KARMA in raw_text:
            await event.reply(f'Coming soon...')

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
