import asyncio

from fastapi import APIRouter

router = APIRouter()
code_queue = asyncio.Queue()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/auth/{code}")
async def auth(code: int):
    await code_queue.put(code)
    return {"message": "Authentication successful!"}
