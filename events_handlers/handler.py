from abc import ABC, abstractmethod
import pygame
from events_handlers.input_state import InputState


class EventsHandler(ABC):
    def __init__(self):
        self._input_state = InputState

    @staticmethod
    def keys():
        return {'up', 'down', 'left', 'right', 'shoot'}

    @abstractmethod
    def set_events(self, event: pygame.Event) -> None: ...
