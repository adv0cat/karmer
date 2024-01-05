import asyncio
import asyncpg

from dotenv import load_dotenv
from datetime import datetime, timezone
from telethon import TelegramClient
from telethon.tl.types import PeerChannel
from emoticon import get_emoticon
from peer import get_peer_id
from const import get_max_offset
from sql_query import INSERT_REACTIONS_SQL
from telegram import init_telegram_client
from postgres import init_postgres_db, Reaction, ReactionCost

load_dotenv()

PARSE_TELEGRAM_INTERVAL = 10
MAX_OFFSET = get_max_offset()


async def parse_channels(app: TelegramClient) -> list[PeerChannel]:
    channels = []
    print("start iter dialogs")
    async for dialog in app.iter_dialogs():
        if dialog.is_channel:
            channels.append(dialog.dialog.peer)

    return channels


async def parse_reactions(app: TelegramClient, peer_channel: PeerChannel):
    reactions_data = []
    offset_date = datetime.now(timezone.utc) - MAX_OFFSET
    async for message in app.iter_messages(entity=peer_channel):
        if message.date < offset_date:
            return reactions_data

        if message.reactions is not None:
            channel_id = peer_channel.channel_id
            msg_id = message.id
            to_user_id = message.replies.channel_id if message.post else get_peer_id(message.from_id)

            if to_user_id is not None and message.fwd_from is None:
                recent_reactions = message.reactions.recent_reactions
                if recent_reactions is not None and len(recent_reactions):
                    reactions_data.extend([Reaction(
                        channel_id=channel_id,
                        msg_id=msg_id,
                        from_user_id=reaction.peer_id.user_id,
                        to_user_id=to_user_id,
                        emoticon=get_emoticon(reaction.reaction),
                        count=1
                    ) for reaction in recent_reactions])
                elif message.reactions.results is not None:
                    reactions_data.extend([Reaction(
                        channel_id=channel_id,
                        msg_id=msg_id,
                        from_user_id=0,
                        to_user_id=to_user_id,
                        emoticon=get_emoticon(reaction_count.reaction),
                        count=reaction_count.count
                    ) for reaction_count in message.reactions.results])

    return reactions_data


async def parse_telegram(app: TelegramClient, postgres: asyncpg.Connection):
    print('start parse telegram')
    channels = await parse_channels(app)
    print("channels:", [channel.channel_id for channel in channels])
    for channel in channels:
        reactions = await parse_reactions(app, channel)
        print(f'[{channel.channel_id}] reactions({len(reactions)}):', reactions)
        reactions = [v.to_tuple() for v in reactions]
        await postgres.executemany(INSERT_REACTIONS_SQL, reactions)
    print("end parse telegram")


async def run_telegram_loop(app: TelegramClient, postgres: asyncpg.Connection):
    while True:
        print('start telegram loop')
        await parse_telegram(app, postgres)
        print(f'{PARSE_TELEGRAM_INTERVAL}s waiting...')
        await asyncio.sleep(PARSE_TELEGRAM_INTERVAL)


async def main():
    print('start main')
    postgres_db = await init_postgres_db()
    telegram_client = await init_telegram_client()

    # reactions = [Reaction.from_record(v) for v in await postgres_db.fetch('SELECT * FROM Reactions')]
    # print('reactions:', reactions)
    # reaction_cost = [ReactionCost.from_record(v) for v in await postgres_db.fetch('SELECT * FROM ReactionCost')]
    # print('reaction_cost:', reaction_cost)

    await asyncio.create_task(run_telegram_loop(telegram_client, postgres_db))

    print('end postgres_db')
    await postgres_db.close()

    print('end main')


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
