from telethon.tl.types import User


def get_full_name(user: User) -> str:
    return f'`{user.first_name}{f" {user.last_name}" if user.last_name is not None else ""}`'
