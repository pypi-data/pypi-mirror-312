from dataclasses import dataclass


@dataclass
class ProxyData:
    proxy_type: int | str
    addr: str
    port: int
    rdns: bool
    username: str | None
    password: str | None
