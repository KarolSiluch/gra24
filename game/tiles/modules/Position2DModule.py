import pygame
from enum import Enum
from game.tiles.modules.basic_modules import Module


class RectType(Enum):
    RenderRect = 0,
    Hitbox = 1


class Position2D(Module):
    def start(self, pos: pygame.Vector2):
        self._pos = pos
        self._rects: dict[RectType, pygame.FRect] = {}
        self._offset = {
            'topleft': lambda size: self._pos,
            'center': lambda size: self._pos - (size[0] / 2, size[1] / 2)
        }

    def new_rect(self, rect_type: RectType, size, offset: str, custom_offset=(0, 0)):
        direct_pos = self._offset.get(offset)(size) + custom_offset
        self._rects[rect_type] = pygame.FRect(direct_pos, size)

    @property
    def x(self):
        return self._pos.x

    @x.setter
    def x(self, new_x):
        delta = new_x - self._pos.x
        self._pos.x = new_x

        for rect in self._rects.values():
            rect.x += delta

    @property
    def y(self):
        return self._pos.y

    @y.setter
    def y(self, new_y):
        delta = new_y - self._pos.y
        self._pos.y = new_y

        for rect in self._rects.values():
            rect.y += delta

    def get_rect(self, rect_type: RectType):
        return self._rects.get(rect_type)

    def set_top(self, rect_type: RectType, top: float):
        rect = self.get_rect(rect_type)
        self.y += top - rect.top

    def set_bottom(self, rect_type: RectType, bottom: float):
        rect = self.get_rect(rect_type)
        self.y += bottom - rect.bottom

    def set_right(self, rect_type: RectType, right: float):
        rect = self.get_rect(rect_type)
        self.x += right - rect.right

    def set_left(self, rect_type: RectType, left: float):
        rect = self.get_rect(rect_type)
        self.x += left - rect.left
