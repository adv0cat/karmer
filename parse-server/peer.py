from typing import Union
from telethon.tl.types import PeerUser, PeerChat, PeerChannel


def get_peer_id(peer: Union[PeerUser, PeerChat, PeerChannel]) -> int:
    if isinstance(peer, PeerUser):
        return peer.user_id
    elif isinstance(peer, PeerChat):
        return peer.chat_id
    elif isinstance(peer, PeerChannel):
        return peer.channel_id
