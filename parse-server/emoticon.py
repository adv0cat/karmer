from typing import Union
from telethon.tl.types import ReactionEmoji, ReactionCustomEmoji, ReactionEmpty


def get_emoticon(reaction: Union[ReactionEmpty, ReactionEmoji, ReactionCustomEmoji]) -> Union[str, None]:
    if isinstance(reaction, ReactionEmoji):
        return reaction.emoticon
    elif isinstance(reaction, ReactionCustomEmoji):
        return str(reaction.document_id)
    elif isinstance(reaction, ReactionEmpty):
        return None
