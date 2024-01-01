from typing import Union
from telethon.tl.types import ReactionEmoji, ReactionCustomEmoji, ReactionEmpty


def get_emoticon(reaction: Union[ReactionEmpty, ReactionEmoji, ReactionCustomEmoji]) -> Union[str, int, None]:
    if isinstance(reaction, ReactionEmoji):
        return reaction.emoticon
    elif isinstance(reaction, ReactionCustomEmoji):
        return reaction.document_id
    elif isinstance(reaction, ReactionEmpty):
        return None
