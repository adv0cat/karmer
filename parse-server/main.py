import os
from dotenv import load_dotenv
from datetime import timedelta, datetime, timezone
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from util.get_emoticon import get_emoticon

load_dotenv()

API_ID = int(os.getenv('API_ID') or 0)
API_HASH = os.getenv('API_HASH')

MAX_DELTA = timedelta(hours=3, minutes=30)

client = TelegramClient(session='karmer', api_id=API_ID, api_hash=API_HASH)
client.start(phone=lambda: os.getenv('PHONE'), password=lambda: os.getenv('PASSWORD'))


async def parse_channels(app: TelegramClient) -> list[PeerChannel]:
    channels = []
    print("start iter dialogs")
    async for dialog in app.iter_dialogs():
        if dialog.is_channel:
            channels.append(dialog.dialog.peer)

    return channels


async def parse_reactions(app: TelegramClient, peer_channel: PeerChannel):
    reactions_data = []
    async for message in app.iter_messages(entity=peer_channel):
        offset_date = datetime.now(timezone.utc) - MAX_DELTA
        if message.date < offset_date:
            return reactions_data

        if message.reactions is not None and message.reactions.recent_reactions is not None:
            reactions_data.append([{
                'channel_id': peer_channel.channel_id,
                'msd_id': message.id,
                'from': reaction.peer_id.user_id,
                'to': message.from_id.user_id,
                'emoticon': get_emoticon(reaction.reaction),
            } for reaction in message.reactions.recent_reactions])

    return reactions_data


async def main():
    print('start main')
    async with client as app:
        print("parse channels")
        channels = await parse_channels(app)
        print("channels:", [channel.channel_id for channel in channels])
        for channel in channels:
            reactions = await parse_reactions(app, channel)
            print(f'[{channel.channel_id}] reactions({len(reactions)}):', reactions)
        print("app ending...")


if __name__ == '__main__':
    client.loop.run_until_complete(main())
