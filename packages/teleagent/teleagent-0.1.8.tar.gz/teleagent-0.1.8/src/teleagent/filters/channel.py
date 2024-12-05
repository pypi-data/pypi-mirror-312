from telethon import types

from ..utils.filters import TelethonFilter

__all__ = [
    "is_channel",
    "is_group_channel",
]

is_channel = TelethonFilter(self__isinstance=types.Channel)
is_group_channel = TelethonFilter(megagroup__is=True)
