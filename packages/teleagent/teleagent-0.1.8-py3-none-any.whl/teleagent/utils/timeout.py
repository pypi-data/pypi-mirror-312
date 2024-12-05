import asyncio
import random
import typing as tp

__all__ = ["delay"]


@tp.overload
async def delay(seconds: float, *, disp: float = None) -> None:
    pass


@tp.overload
async def delay(min_value: float, max_value: float) -> None:
    pass


async def delay(x: float, y: float = None, *, disp: float = None) -> None:  # type: ignore[misc]
    if y is None:
        if disp is not None:
            y = x * (1 + disp)
        else:
            return await asyncio.sleep(x)

    await asyncio.sleep(random.uniform(x, y))
