import pygame
from events_handlers.handler import GameHandler
from game.tiles.tile import Tile


class Player(Tile):
    def __init__(self):
        image = pygame.Surface((10, 20))
        image.fill('white')
        super().__init__(image, center=(100, 100))

    def move(self, events: GameHandler):
        y_direction = events.get('down') - events.get('up')
        x_direction = events.get('right') - events.get('left')

        self._rect.x += x_direction * 3
        self._rect.y += y_direction * 3
