import pygame
from events_handlers.handler import GameHandler
from game.tiles.tile import Tile


class Player(Tile):
    def __init__(self, groups):
        image = pygame.Surface((10, 20))
        image.fill('white')
        super().__init__(groups, image, center=(100, 100))

        self._move = MoveModule()
        self._move.start(self)

    def update(self, events: GameHandler):
        self._move.update(events)
        self.AABBmodule.update()


class MoveModule:
    def start(self, context: Player):
        self._context = context
        self._position = context._position

    def update(self, events: GameHandler):
        y_direction = events.get('down') - events.get('up')
        x_direction = events.get('right') - events.get('left')

        self._position.x += x_direction * 3
        self._position.y += y_direction * 3
