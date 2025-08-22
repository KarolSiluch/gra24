from engine.events_handlers.handler import EventsHandler
import pygame
from game.player.player import Player
import engine.camera.game_camera as camera
from game.tiles.tile import Tile
from engine.AABBtree.AABBtree import AABBTree
# from random import randint
from engine.base_tile.modules.Position2DModule import RectType
from engine.map.map import GameMap, GroupType
from engine.assets_manager.assets_manager import AssetsManager
from engine.base_tile.modules.basic_modules import ModuleType
from engine.events_handlers.input_state import InputState
from engine.game_cursor.game_cursor import Cursor
from engine.base_tile.modules.renderer import BaseRenderer
from random import randint


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
        self._renderer.update(dt)
        self._camera.update(dt, self)
        self._player.update(dt)
        self._map[GroupType.Bullets].update(dt, self._camera.rect)


class GameplayRenderer:
    class BackgroundRect:
        def __init__(self, speed_range, rotation_speed_range, r_range):
            self._display_w = pygame.display.Info().current_w
            self._display_h = pygame.display.Info().current_h

            self._speed_range = speed_range
            self._rotation_speed_range = rotation_speed_range
            self._r_range = r_range

            self._r = self.new_r()
            self._x = self.new_x()
            self._y = randint(-self._display_h, self._display_h)
            self._speed = self.new_speed()
            self._angle = randint(0, 360)

        def new_x(self):
            return randint(-2 * self._r, self._display_w + 2 * self._r)

        def new_r(self):
            return randint(*self._r_range)

        def new_speed(self):
            return randint(*self._speed_range)

        def update(self, dt: float):
            self._angle += dt * 10
            self._y += dt * self._speed
            if self._y > self._display_h + 2 * self._r:
                self.reset()

        def reset(self):
            self._r = self.new_r()
            self._x = self.new_x()
            self._y = randint(-self._display_h, -2 * self._r)
            self._speed = self.new_speed()

        def render(self, surface: pygame.Surface):
            image = pygame.Surface((self._r, self._r), flags=pygame.SRCALPHA)
            image.fill('#323745')
            image = pygame.transform.rotate(image, self._angle)
            rect = image.get_rect(center=(self._x, self._y))
            surface.blit(image, rect)

    def __init__(self, game: Gameplay):
        self._game = game
        self._offset = 0
        self._rects = [self.BackgroundRect((30, 50), (30, 70), (30, 70)) for _ in range(20)]
        self._rects.extend([self.BackgroundRect((50, 80), (30, 70), (7, 30)) for _ in range(20)])

    def update(self, dt: float):
        self._offset += dt * 10
        for rect in self._rects:
            rect.update(dt)

    def render_backgrounf(self, surface: pygame.Surface):
        surface.fill('#394541')

        for rect in self._rects:
            rect.render(surface)

        width, height = surface.size
        distance = 30
        tilt = 100

        for i in range(-1, height // distance + tilt // distance):
            offset = self._offset % distance
            y = i * distance - offset
            pygame.draw.line(surface, '#323745', (0, y), (width, y + 60), 15)

    def render(self, surface: pygame.Surface):
        self.render_backgrounf(surface)
        visible_tiles = GameMap.get_group(GroupType.Visible)
        tiles: tuple[Tile] = self._game.camera.get_tiles(visible_tiles)
        # visible_tiles.print(surface)

        camera_offset = self._game.camera.offset
        for tile in sorted(tiles, key=lambda tile: tile.get_module(ModuleType.Position).y):
            rect: pygame.FRect = tile.get_module(ModuleType.Position).get_rect(RectType.RenderRect)
            renderer: BaseRenderer = tile.get_module(ModuleType.Renderer)
            renderer.render(surface, -camera_offset + rect.topleft)
