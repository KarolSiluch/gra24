from events_handlers.handler import GameHandler
import pygame
from game.player.player import Player
import game.camera.game_camera as camera
from game.tiles.tile import Tile
from game.AABBtree.AABBtree import AABBTree
from random import randint
from game.player.modules.Position2DModule import RectType


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

        self.AABB_tree = AABBTree(RectType.RenderRect)
        self._player = Player([self.AABB_tree])
        self._renderer = GameplayRenderer(self)
        self._camera = camera.Camera()

        tile_size = 16
        for _ in range(10):
            tile_image = pygame.Surface((tile_size, tile_size))
            tile_image.fill('green')
            pos = (randint(20, 500), randint(20, 300))
            Tile([self.AABB_tree], tile_image, topleft=pos)

        # for i in range(64):
        #     tile_image = pygame.Surface((tile_size, tile_size))
        #     tile_image.fill('green')
        #     pos = (i + i * tile_size, i * tile_size / 2)
        #     Tile([self.AABB_tree], tile_image, topleft=pos)

    @property
    def renderer(self):
        return self._renderer

    @property
    def camera(self):
        return self._camera

    def update(self):
        self._player.update(self._events_handler)

        if self._events_handler.get('mouse1'):
            tile_image = pygame.Surface((16, 16))
            tile_image.fill('green')
            Tile([self.AABB_tree], tile_image, center=pygame.mouse.get_pos())

        self._events_handler.reset_keys()


class GameplayRenderer:
    def __init__(self, game: Gameplay):
        self._game = game

    def render(self, surface: pygame.Surface):
        surface.fill('purple')
        tiles: tuple[Tile] = self._game.camera.get_tiles(self._game.AABB_tree)
        self._game.AABB_tree.print(surface)
        for tile in tiles:
            pos = tile.renderer.pos
            tile.renderer.render(surface, pos)
