# import pygame
from game.tiles.tile import Tile
from game.player.modules.collision import CollisionModule
from game.player.modules.movement import MoveModule
from events_handlers.handler import GameHandler
from game.tiles.modules.basic_modules import ModuleType
from game.assets_manager.assets_manager import AssetsManager


class Player(Tile):
    def __init__(self, groups):
        image = AssetsManager.get('player')
        super().__init__(groups, image, center=(100, 100))

        self.new_module(ModuleType.Collision, CollisionModule)

        self._move = MoveModule(self)
        self._move.start()

    def update(self, dt: float, events: GameHandler):
        self._move.update(dt, events)
        self.get_module(ModuleType.AABB).update()
