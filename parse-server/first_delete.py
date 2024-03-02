from pydantic import BaseModel, PositiveInt
from telethon import TelegramClient, hints


class FirstDelete(BaseModel):
    tg: TelegramClient
    chat: 'hints.EntityLike'
    msg_id: PositiveInt

    async def send(self, message: str):
        await self.tg.delete_messages(self.chat, [self.msg_id])
        await self.tg.send_message(self.chat, message)
