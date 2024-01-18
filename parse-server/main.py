import asyncio
import asyncpg

from typing import Optional
from dotenv import load_dotenv
from telegram import init_telegram_client
from pg_pool import init_pg_pool
from fast_api_router import router, code_queue
from contextlib import asynccontextmanager
from fastapi import FastAPI

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    pg_pool: Optional[asyncpg.Pool] = None
    tg_task: Optional[asyncio.Task] = None
    try:
        print('start main', app)
        pg_pool = await init_pg_pool()
        tg_task = asyncio.create_task(init_telegram_client(code_queue, pg_pool))
        yield
    finally:
        if pg_pool is not None:
            print('end pg_pool')
            await pg_pool.close()
        if tg_task is not None:
            print('end tg_task')
            try:
                tg_task.cancel()
            except asyncio.CancelledError:
                pass

    print('end main')

fast_api = FastAPI(responses={404: {"description": "Not found"}}, lifespan=lifespan)
fast_api.include_router(router)
