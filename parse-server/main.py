import asyncio
import asyncpg

from typing import Optional
from dotenv import load_dotenv
from telegram import init_telegram_client
from postgres import init_postgres_db
from fast_api_router import router, code_queue
from contextlib import asynccontextmanager
from fastapi import FastAPI

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres_db: Optional[asyncpg.Connection] = None
    telegram_task: Optional[asyncio.Task] = None
    try:
        print('start main', app)
        postgres_db = await init_postgres_db()
        telegram_task = asyncio.create_task(init_telegram_client(code_queue, postgres_db))
        yield
    finally:
        if postgres_db is not None:
            print('end postgres_db')
            await postgres_db.close()
        if telegram_task is not None:
            print('end telegram_task')
            try:
                telegram_task.cancel()
            except asyncio.CancelledError:
                pass

    print('end main')

fast_api = FastAPI(responses={404: {"description": "Not found"}}, lifespan=lifespan)
fast_api.include_router(router)
