from __future__ import annotations

import asyncio
from functools import partial
from typing import Any, Awaitable, Callable, Generic, ParamSpec, Type, TypeVar

from inbound.utils import is_async_callable


P = ParamSpec("P")
R = TypeVar("R")

CallbackType = Callable[..., R | Awaitable[R]]


class EventCallback(Generic[P, R]):
    def __init__(
        self,
        _fn: CallbackType,
        channel: str,
        event_type: str = "event",
    ):
        if not callable(_fn):
            raise TypeError("`_fn` must be callable.")

        assert channel, "EventCallback `channel` must not be empty"
        assert event_type, "EventCallback `event_type` must not be empty"

        self._fn = _fn
        self._is_async = is_async_callable(self._fn)
        self._name = self._fn.__name__

        self.channel = channel
        self.event_type = event_type

    @property
    def is_async(self) -> bool:
        return self._is_async

    @property
    def name(self) -> str:
        return self._name

    def match_event_type(self, event_type: str) -> bool:
        return self.event_type == event_type or self.event_type == "*"

    async def __call__(self, *args: P.args, **kwargs: P.kwargs):
        if not self.is_async:
            loop = asyncio.get_running_loop()
            return loop.run_in_executor(None, partial(self._fn, *args, **kwargs))
        else:
            return await self._fn(*args, **kwargs)


class CallbackGroup:
    def __init__(self, callback_cls: Type[EventCallback] = EventCallback) -> None:
        self._callback_cls = callback_cls
        self._callbacks: dict[str, list[EventCallback]] = {}

    @property
    def callbacks(self):
        return self._callbacks

    @property
    def channels(self):
        return self._callbacks.keys()

    def add_group(self, group: CallbackGroup) -> None:
        """
        Add a group of callbacks to the current group.

        :param group: The group of callbacks to add
        :type group: CallbackGroup
        """
        for _, callbacks in group.callbacks.items():
            for callback in callbacks:
                self.register_callback(callback)

    def get_callbacks(self, channel: str, event_type: str) -> list[EventCallback]:
        """
        Get all callbacks that match the channel and event_type.

        :param channel: The channel to match
        :type channel: str
        :param event_type: The event_type to match
        :type event_type: str
        :return: A list of callbacks that match the channel and event_type
        :rtype: list[EventCallback]
        """
        return [
            callback
            for callback in self.callbacks.get(channel, [])
            if callback.match_event_type(event_type)
        ]

    def remove_callback(self, callback: EventCallback) -> None:
        """
        Remove a callback from the group.

        :param callback: The callback to remove
        :type callback: EventCallback
        """
        self._callbacks[callback.channel].remove(callback)
        if not self._callbacks[callback.channel]:
            del self._callbacks[callback.channel]

    def register_callback(self, callback: EventCallback) -> None:
        """
        Register a callback to the group.

        :param callback: The callback to register
        :type callback: EventCallback
        """
        if callback.channel in self._callbacks.keys():
            self._callbacks[callback.channel].append(callback)
        else:
            self._callbacks[callback.channel] = [callback]

    def add_callback(self, callback: CallbackType, channel: str, event_type: str) -> None:
        """
        Add a callback to the group.

        :param callback: The callback to add
        :type callback: CallbackType
        :param channel: The channel to match
        :type channel: str
        :param event_type: The event_type to match
        :type event_type: str
        """
        self.register_callback(self._callback_cls(callback, channel, event_type))

    def callback(self, channel: str, event_type: str) -> Callable[..., Any]:
        """
        Decorator to add a callback to the group.

        :param channel: The channel to match
        :type channel: str
        :param event_type: The event_type to match
        :type event_type: str
        :return: The decorator
        :rtype: Callable[..., Any]
        """

        def decorator(func: CallbackType) -> CallbackType:
            self.add_callback(callback=func, channel=channel, event_type=event_type)
            return func

        return decorator
