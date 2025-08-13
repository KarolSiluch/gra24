from events_handlers.handler import GameHandler
import pygame
from game.player.player import Player
import game.camera.game_camera as camera
from game.tiles.tile import Tile
from game.AABBtree.AABBtree import AABBTree
from random import randint
from game.tiles.modules.Position2DModule import RectType
from game.map.map import GameMap, GroupType
from game.assets_manager.assets_manager import AssetsManager
from game.tiles.modules.basic_modules import ModuleType


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
        AssetsManager.init()

        self._map = {
            GroupType.Visible: AABBTree(RectType.RenderRect),
            GroupType.Obsticles: AABBTree(RectType.Hitbox)
        }
        GameMap.init(self._map)

        self._player = Player([GroupType.Visible])
        self._renderer = GameplayRenderer(self)
        self._camera = camera.Camera()

        for _ in range(10):
            tile_image = AssetsManager.get('tiles')[8]
            pos = (randint(20, 500), randint(20, 300))
            Tile([GroupType.Visible, GroupType.Obsticles], tile_image, topleft=pos)

    @property
    def renderer(self):
        return self._renderer

    @property
    def camera(self):
        return self._camera

    def update(self, dt: float):
        self._player.update(dt, self._events_handler)
        self._events_handler.reset_keys()


class GameplayRenderer:
    def __init__(self, game: Gameplay):
        self._game = game

    def render(self, surface: pygame.Surface):
        surface.fill('#394541')
        visible_tiles = GameMap.get_group(GroupType.Visible)
        tiles: tuple[Tile] = self._game.camera.get_tiles(visible_tiles)
        visible_tiles.print(surface)
        for tile in sorted(tiles, key=lambda tile: tile.get_module(ModuleType.Position).y):
            pos = tile.renderer.pos
            tile.renderer.render(surface, pos)
