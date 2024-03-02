import asyncio
import re

import asyncpg
import os

from typing import Coroutine, Any
from datetime import timedelta
from const import get_max_offset
from parse import parse_telegram
from tg_command import TgCommand
from peer import get_peer_id
from full_name import get_full_name
from sql_query import GET_MY_KARMA_SQL, GET_ALL_KARMA_SQL
from pg_pool import UserKarma
from mute_user import mute_user
from first_delete import FirstDelete
from telethon import TelegramClient, events
from telethon.tl.custom.message import Message
from telethon.tl.types import User
from telethon.tl.types import ChannelParticipantCreator, ChannelParticipantAdmin, ChannelParticipantBanned, \
    ChannelParticipantLeft, ChannelParticipantSelf, ChannelParticipant, channels
from telethon.tl.functions.channels import GetParticipantRequest

PARSE_TELEGRAM_INTERVAL = 10
BAN_MINUTES = 5


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
            # TODO: check working
            await event.reply(TgCommand.get_list_for(sender))

    @tg.on(events.NewMessage(incoming=True, forwards=False, pattern=r'^!(\w+[\w-]*)\s*(.*)'))
    async def handler(event: events.NewMessage.Event):
        if event.is_private:
            return

        message: Message = event.message
        pattern_match: re.Match = event.pattern_match

        command = pattern_match.group(1)
        command_msg = pattern_match.group(2)

        chat = await message.get_chat()
        sender = await message.get_sender()
        sender_full_name = get_full_name(sender)

        first_delete = FirstDelete(tg=tg, chat=chat, msg_id=message.id)

        if command == TgCommand.MUTE:
            participant: channels.ChannelParticipant = await tg(GetParticipantRequest(chat, sender))
            if participant is None or participant.participant is None:
                return

            is_banned = isinstance(participant.participant, ChannelParticipantBanned)
            is_left = isinstance(participant.participant, ChannelParticipantLeft)
            if is_banned or is_left:
                await first_delete.send(f'Что ты такое?!')
                return

            if isinstance(participant.participant, ChannelParticipantSelf):
                await first_delete.send(f'Ты зачем себя трогаешь?')
                return

            if isinstance(participant.participant, ChannelParticipant):
                await first_delete.send(f'У тебя нет здесь власти {sender_full_name}')
                return

            is_admin = isinstance(participant.participant, ChannelParticipantAdmin)
            is_owner = isinstance(participant.participant, ChannelParticipantCreator)
            if (is_admin or is_owner) and participant.participant.admin_rights.ban_users is not True:
                await first_delete.send(f'{sender_full_name}, тебе нельзя мьютить юзеров')
                return

            reason = f' по причине "{command_msg}"' if command_msg is not None else ', причина умалчивается'
            await mute_user(tg, message, timedelta(minutes=BAN_MINUTES), reason)

        elif command == TgCommand.HELP:
            await first_delete.send(f'{sender_full_name}, вот мои команды:' + TgCommand.get_list_for())

        elif command == TgCommand.KARMA:
            async with pg_pool.acquire() as pg_conn:
                pg_conn: asyncpg.Connection
                user_id = get_peer_id(message.from_id)
                channel_id = get_peer_id(message.peer_id)
                my_karma = await pg_conn.fetchval(GET_MY_KARMA_SQL, channel_id, user_id)

            await first_delete.send(f'{sender_full_name}, вот твоя карма: `{my_karma}`')

        elif command == TgCommand.ALL_KARMA:
            async with pg_pool.acquire() as pg_conn:
                pg_conn: asyncpg.Connection
                channel_id = get_peer_id(message.peer_id)
                raw_all_karma: list[asyncpg.Record] = await pg_conn.fetch(GET_ALL_KARMA_SQL, channel_id)

            all_karma = [UserKarma.model_validate(dict(v)) for v in raw_all_karma]
            await asyncio.gather(*[user.parse_tg(tg) for user in all_karma])

            all_karma_str_list = [f'{i}. {v.full_name} - {v.total_karma}' for i, v in enumerate(all_karma, start=1)]
            all_karma_str = '\n'.join(all_karma_str_list)
            await first_delete.send(f'{sender_full_name}, вот карма юзеров этого чатика:\n\n' + all_karma_str)

        else:
            await first_delete.send(f'И что теперь делать 🤷‍♂️'
                                    f'\nЧто значит "{command}"?\nНет такой команды...')

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
