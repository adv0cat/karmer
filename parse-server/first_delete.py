from telethon import TelegramClient, hints


class FirstDelete:
    def __init__(self, tg: TelegramClient):
        self.tg = tg

    async def send(self, chat: 'hints.EntityLike', message_id: int, message: str):
        await self.tg.delete_messages(chat, [message_id])
        await self.tg.send_message(chat, message)
