import abc
import typing as tp
from dataclasses import asdict

from telethon import TelegramClient, sessions

from ..structures import AppData, ProxyData

if tp.TYPE_CHECKING:
    from .agent import TelegramAgent


class TelegramAgentBase(abc.ABC):
    def __init__(
        self: "TelegramAgent",
        session: sessions.Session,
        app: AppData,
        *,
        proxy: ProxyData | None = None,
        **kwargs: tp.Any,
    ) -> None:
        telegram_client_kwargs: dict[str, tp.Any] = {}

        if app is not None:
            kwargs.update(asdict(app))
            kwargs.pop("lang_pack")

        if proxy is not None:
            kwargs["proxy"] = asdict(proxy)

        telegram_client_kwargs.update(kwargs)

        self._client = TelegramClient(session, **telegram_client_kwargs)

        if app is not None:
            self._client._init_request.lang_pack = app.lang_pack  # noqa

    @property
    def client(self: "TelegramAgent") -> TelegramClient:
        return self._client
