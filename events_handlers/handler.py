from abc import ABC, abstractmethod
import pygame


class EventsHandler(ABC):
    __slots__ = ('_events')

    def __init__(self, *events: list[str]):
        super().__init__()
        self._events: dict[str, bool] = {key: False for key in events}

    def get(cls, event: str) -> bool:
        return cls._events.get(event, False)

    @abstractmethod
    def update(self) -> list[pygame.Event]: ...


class GameHandler(EventsHandler):
    def __init__(self):
        super().__init__('up', 'down', 'left', 'right', 'mouse1')
