import pygame
from events_handlers.handler import GameHandler


class Player:
    def __init__(self):
        self._pos = pygame.Vector2(100, 100)
        self._image = pygame.Surface((10, 20))
        self._image.fill('white')
        self._renderer = PlayerRenderer(self)

    def move(self, events: GameHandler):
        y_direction = events.get('down') - events.get('up')
        x_direction = events.get('right') - events.get('left')

        self._pos.x += x_direction * 7
        self._pos.y += y_direction * 7

    @property
    def renderer(self):
        return self._renderer


class PlayerRenderer:
    def __init__(self, player: Player):
        self._player = player

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        surface.blit(self._player._image, pos)
