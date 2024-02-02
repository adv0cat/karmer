from typing import Union

from telethon.tl.types import User, InputUser


def get_full_name(user: Union[User, InputUser]) -> str:
    return f'`{user.first_name}{f" {user.last_name}" if user.last_name is not None else ""}`'
