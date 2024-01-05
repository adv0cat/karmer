import os

from typing import Coroutine, Any
from telethon import TelegramClient


def init_telegram_client() -> Coroutine[Any, Any, TelegramClient]:
    print('init telegram client')
    api_id = int(os.environ.get('API_ID') or 0)
    api_hash = os.environ.get('API_HASH')

    telegram_client = TelegramClient(session='karmer', api_id=api_id, api_hash=api_hash)
    return telegram_client.start(phone=get_phone, password=get_password)  # type: ignore


def get_phone():
    return os.environ.get('PHONE')


def get_password():
    return os.environ.get('PASSWORD')
