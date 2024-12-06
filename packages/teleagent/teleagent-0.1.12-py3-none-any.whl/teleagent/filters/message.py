from telethon import types

from ..utils.filters import TelethonFilter

__all__ = [
    "is_message",
    "is_direct_message",
    "is_channel_message",
]

is_message = TelethonFilter(self__isinstance=types.Message)
is_direct_message = TelethonFilter(peer_id__isinstance=types.PeerUser)
is_channel_message = TelethonFilter(peer_id__isinstance=types.PeerChannel)
