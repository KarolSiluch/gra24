import pygame
from game.tiles.modules.basic_modules import Module, ModuleType
from game.tiles.modules.Position2DModule import Position2D, RectType
from typing import Callable
# from events_handlers.handler import GameHandler
from game.map.map import GroupType
from game.player.modules.collision import CollisionModule


class MoveModule(Module):
    __slots__ = ('_position', '_collisions', '_velocity', '_direction')

    def start(self):
        self._position: Position2D = self._context.get_module(ModuleType.Position)
        self._collisions: CollisionModule = self._context.get_module(ModuleType.Collision)
        self._velocity = 200
        self._direction = pygame.Vector2(0, 0)

    @property
    def direction(self):
        return self._direction

    def move_axis(self, dt: float, direction: float, axis: str, set_pos_edge, set_neg_edge) -> None:
        new_pos = getattr(self._position, axis) + direction * self._velocity * dt
        setattr(self._position, axis, new_pos)
        for tile in self._collisions.get_collision(GroupType.Obsticles):
            position: Position2D = tile.get_module(ModuleType.Position)
            rect = position.get_rect(RectType.Hitbox)
            if direction > 0:
                set_pos_edge(rect)
            else:
                set_neg_edge(rect)

    def set_direction(self, new_direction: pygame.Vector2):
        self._direction = new_direction

    def move(self, dt: float, direction: pygame.Vector2):
        rtype = RectType.Hitbox

        set_pos_edge: Callable[[pygame.FRect], None] = lambda rect: self._position.set_right(rtype, rect.left)
        set_neg_edge: Callable[[pygame.FRect], None] = lambda rect: self._position.set_left(rtype, rect.right)
        self.move_axis(dt, direction.x, 'x', set_pos_edge, set_neg_edge)

        set_pos_edge: Callable[[pygame.FRect], None] = lambda rect: self._position.set_bottom(rtype, rect.top)
        set_neg_edge: Callable[[pygame.FRect], None] = lambda rect: self._position.set_top(rtype, rect.bottom)
        self.move_axis(dt, direction.y, 'y', set_pos_edge, set_neg_edge)
