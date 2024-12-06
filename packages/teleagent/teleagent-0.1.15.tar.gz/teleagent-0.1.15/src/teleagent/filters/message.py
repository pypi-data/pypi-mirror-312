from telethon import types

from ..utils.filters import TelethonFilter

__all__ = [
    "is_message",
    "is_user_message",
    "is_channel_message",
    "is_by_user_message",
    "is_by_channel_message",
]

is_message = TelethonFilter(self__isinstance=types.Message)
is_user_message = TelethonFilter(peer_id__isinstance=types.PeerUser)
is_channel_message = TelethonFilter(peer_id__isinstance=types.PeerChannel)
is_by_user_message = TelethonFilter(from_id__isinstance=types.PeerUser)
is_by_channel_message = TelethonFilter(from_id__isinstance=types.PeerChannel)
