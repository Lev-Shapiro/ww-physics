from __future__ import annotations
from collections import defaultdict
from typing import Callable, Type, TypeVar

T = TypeVar("T")

class EventBus:
    """Synchronous in-process event bus for decoupled domain communication."""

    def __init__(self) -> None:
        self._handlers: dict[type, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: Type[T], handler: Callable[[T], None]) -> None:
        self._handlers[event_type].append(handler)

    def publish(self, event: object) -> None:
        for handler in self._handlers.get(type(event), []):
            handler(event)
