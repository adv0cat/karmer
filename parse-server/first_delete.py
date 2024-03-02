from telethon import TelegramClient, hints


class FirstDelete:
    def __init__(self, tg: TelegramClient, chat: 'hints.EntityLike', msg_id: int):
        self.tg = tg
        self.chat = chat
        self.msg_id = msg_id

    async def send(self, message: str):
        await self.tg.delete_messages(self.chat, [self.msg_id])
        await self.tg.send_message(self.chat, message)
