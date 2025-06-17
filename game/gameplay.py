from events_handlers.handler import GameHandler
import pygame
import game.game_states.game_machine as gm


class Gameplay:
    _events_handler: GameHandler = None

    @classmethod
    def set_handler(cls, handler) -> None:
        cls._events_handler = handler

    def update_handler(self) -> list[pygame.Event]:
        return self._events_handler.update()

    @classmethod
    def events_handler(cls) -> GameHandler:
        return cls._events_handler

    def __init__(self, handler: GameHandler):
        self.set_handler(handler)
        self._game_machine = gm.GameMachine(self)

    def update_states(self):
        self._game_machine.change_state()
        self._game_machine.update()

    def update(self): ...
