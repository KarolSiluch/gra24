import pygame
from game.AABBtree.AABBtree import AABBTree
from game.tiles.modules.basic_modules import ModuleType
from game.tiles.modules.Position2DModule import Position2D
from game.tiles.modules.Position2DModule import RectType
from game.game_cursor.game_cursor import Cursor


class Camera:
    def __init__(self):
        self._screen_offset = pygame.Vector2(pygame.display.Info().current_w, pygame.display.Info().current_h)
        self._rect = pygame.FRect((0, 0), self._screen_offset)
        self._camera_offset = pygame.Vector2(0, 0)

    @property
    def rect(self):
        return self._rect

    @property
    def offset(self):
        return self._camera_offset

    def update(self, dt: float, game):
        player_pos: Position2D = game._player.get_module(ModuleType.Position)
        player_pos = player_pos.get_rect(RectType.RenderRect).center

        cursor_vector = Cursor.get_vector(player_pos)
        size = min(cursor_vector.magnitude() / 7, 50)
        cursor_vector and cursor_vector.scale_to_length(size)

        x_pos = player_pos[0] + cursor_vector.x - self._screen_offset.x // 2 - self._camera_offset.x
        self._camera_offset.x += (x_pos) * dt * 9
        y_pos = player_pos[1] + cursor_vector.y - self._screen_offset.y // 2 - self._camera_offset.y
        self._camera_offset.y += (y_pos) * dt * 9

        self._rect.topleft = self._camera_offset

    def get_tiles(self, visible_tiles: AABBTree):
        return visible_tiles.RectCollision(self._rect)
