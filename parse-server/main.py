import os
from dotenv import load_dotenv
from telethon import TelegramClient

load_dotenv()

API_ID = int(os.getenv('API_ID') or 0)
API_HASH = os.getenv('API_HASH')

client = TelegramClient(session='karmer', api_id=API_ID, api_hash=API_HASH)
client.start(phone=lambda: os.getenv('PHONE'))


async def main():
    print('start main')
    async with client as app:
        print("parse dialogs")
        print("...")
        print("app ending...")


if __name__ == '__main__':
    client.loop.run_until_complete(main())
