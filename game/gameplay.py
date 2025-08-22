from engine.events_handlers.handler import EventsHandler
import pygame
from game.player.player import Player
import engine.camera.game_camera as camera
from game.tiles.tile import Tile
from engine.AABBtree.AABBtree import AABBTree
from random import randint
from engine.base_tile.modules.Position2DModule import RectType
from engine.map.map import GameMap, GroupType
from engine.assets_manager.assets_manager import AssetsManager
from engine.base_tile.modules.basic_modules import ModuleType
from engine.events_handlers.input_state import InputState
from engine.game_cursor.game_cursor import Cursor
from engine.base_tile.modules.renderer import BaseRenderer


class Gameplay:
    def __init__(self, handler: EventsHandler):
        self._events_handler = handler
        InputState.init(handler.keys())
        AssetsManager.init()

        self._map = {
            GroupType.Visible: AABBTree(RectType.RenderRect),
            GroupType.Obsticles: AABBTree(RectType.Hitbox),
            GroupType.Bullets: AABBTree(RectType.RenderRect)
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
    def events_handler(self):
        return self._events_handler

    @property
    def renderer(self):
        return self._renderer

    @property
    def camera(self):
        return self._camera

    def update(self, dt: float):
        Cursor.update(self._camera.offset)
        self._camera.update(dt, self)
        self._player.update(dt)
        self._map[GroupType.Bullets].update(dt, self._camera.rect)


class GameplayRenderer:
    def __init__(self, game: Gameplay):
        self._game = game

    def render(self, surface: pygame.Surface):
        surface.fill('#394541')
        visible_tiles = GameMap.get_group(GroupType.Visible)
        tiles: tuple[Tile] = self._game.camera.get_tiles(visible_tiles)
        # visible_tiles.print(surface)

        camera_offset = self._game.camera.offset
        for tile in sorted(tiles, key=lambda tile: tile.get_module(ModuleType.Position).y):
            rect: pygame.FRect = tile.get_module(ModuleType.Position).get_rect(RectType.RenderRect)
            renderer: BaseRenderer = tile.get_module(ModuleType.Renderer)
            renderer.render(surface, -camera_offset + rect.topleft)
