import pygame
from game.tiles.tile import Tile
from game.player.modules.collision import CollisionModule
from game.player.modules.movement import MoveModule
from events_handlers.handler import GameHandler
from game.tiles.modules.basic_modules import ModuleType


class Player(Tile):
    def __init__(self, groups):
        image = pygame.Surface((10, 20))
        image.fill('white')
        super().__init__(groups, image, center=(100, 100))

        self.new_module(ModuleType.Collision, CollisionModule)

        self._move = MoveModule(self)
        self._move.start()

    def update(self, events: GameHandler):
        self._move.update(events)
        self.get_module(ModuleType.AABB).update()
