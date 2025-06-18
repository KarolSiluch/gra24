from events_handlers.handler import GameHandler
import pygame
from game.player.player import Player
import game.camera.game_camera as camera


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
        self._player = Player()
        self._renderer = GameplayRenderer(self)
        self._camera = camera.Camera()

    @property
    def renderer(self):
        return self._renderer

    @property
    def camera(self):
        return self._camera

    def update(self):
        self._player.move(self._events_handler)


class GameplayRenderer:
    def __init__(self, game: Gameplay):
        self._game = game

    def render(self, surface: pygame.Surface):
        surface.fill('purple')
        player = self._game._player
        player.renderer.render(surface, player._pos + self._game.camera.get_offset(self._game))
