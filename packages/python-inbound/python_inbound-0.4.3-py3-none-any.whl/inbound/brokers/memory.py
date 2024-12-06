import asyncio
from typing import Tuple

from inbound.brokers.base import Broker
from inbound.event import Event


class MemoryBroker(Broker):
    """
    An in-memory queue broker
    """

    backend = "memory"

    _channels: set[str] = set()
    _consumer: asyncio.Queue[tuple[str, Event]]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def connect(self) -> None:
        self._consumer = asyncio.Queue()

    async def disconnect(self) -> None:
        pass

    async def subscribe(self, channel: str) -> None:
        self._channels.add(channel)

    async def unsubscribe(self, channel: str) -> None:
        if channel in self._channels:
            self._channels.remove(channel)

    async def publish(self, channel: str, event: Event, **kwargs) -> None:
        assert channel, "Must specify a channel in the Event"
        await self._consumer.put((channel, event))

    async def next(self) -> Tuple[str, Event]:
        while True:
            channel, event = await self._consumer.get()
            if channel in self._channels:
                return channel, event
