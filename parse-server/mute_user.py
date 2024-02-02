import asyncio
from datetime import datetime, timezone, timedelta
from typing import Optional

from telethon import TelegramClient
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import User, ChatBannedRights, InputPeerUser, MessageEntityMention
from telethon.tl.custom.message import Message
from full_name import get_full_name


async def mute_user(tg: TelegramClient, message: Message, offset: timedelta, reason: str):
    minutes = round(offset.total_seconds() / 60)
    rights = ChatBannedRights(
        until_date=datetime.now(timezone.utc) + offset,
        send_messages=True,
        send_media=True
    )

    reply_msg: Optional[Message] = await message.get_reply_message()
    has_replay = reply_msg is not None

    users: list[User] = []
    if has_replay:
        users.append(await reply_msg.get_sender())
    elif message.entities is not None:
        entities = await asyncio.gather(*[
            tg.get_entity(message.text[entity.offset:entity.offset + entity.length])
            for entity in message.entities
            if isinstance(entity, MessageEntityMention)
        ])
        if len(entities) > 0:
            users = [user for user in entities if isinstance(user, User)]

    chat = await message.get_chat()
    await tg.delete_messages(chat, [message.id])
    if len(users) == 0:
        sender = await message.get_sender()
        msg = (f'Ну и кого я мьютить должен {get_full_name(sender)}?'
               f'\nИли реплай того, кого мьютить и пиши команду, '
               f'или просто в чат "!mute @nickname" кого мьютить...')
        await tg.send_message(chat, msg)
        return

    for user_to_mute in users:
        mute_msg = f'{get_full_name(user_to_mute)}, ты замьючен на {minutes} минут{reason}'
        try:
            await tg(EditBannedRequest(chat, to_input(user_to_mute), rights))
            await (reply_msg.reply(mute_msg) if has_replay else tg.send_message(chat, mute_msg))
        except Exception as e:
            error_msg = f'{get_full_name(user_to_mute)}, тебе повезло... Произошла ошибка: {str(e)}'
            await (reply_msg.reply(error_msg) if has_replay else tg.send_message(chat, error_msg))


def to_input(user: User):
    return InputPeerUser(user_id=user.id, access_hash=user.access_hash)

# if has_replay:
#     reply_msg: Message = await message.get_reply_message()
#     user_to_mute = await reply_msg.get_sender()
#     try:
#         await tg(EditBannedRequest(chat, user_to_mute, rights))
#         await tg.delete_messages(chat, [message.id])
#         await reply_msg.reply(
#             f'{get_full_name(user_to_mute)}, ты замьючен на {ban_minutes} минут{reason}...')
#     except Exception as e:
#         await reply_msg.reply(f'{get_full_name(user_to_mute)}, тебе повезло... Произошла ошибка: {str(e)}')
# else:
#     entities = await asyncio.gather(*[
#         tg.get_entity(message.text[entity.offset:entity.offset + entity.length])
#         for entity in message.entities
#         if isinstance(entity, MessageEntityMention)
#     ])
#     users = [user for user in entities if isinstance(user, User)]
#     await tg.delete_messages(chat, [message.id])
#     if len(users):
#         await tg.send_message(chat, f'Без реплая не могу пока-что понять, кого банить?')
#     else:
#         await tg.send_message(chat, f'Без реплая не могу пока-что понять, кого банить?')
#         # await message.reply(f'Без реплая не могу пока-что понять, кого банить?')
#     return
