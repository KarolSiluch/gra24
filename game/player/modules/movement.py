import pygame
from game.tiles.modules.basic_modules import Module, ModuleType
from game.tiles.modules.Position2DModule import Position2D, RectType
from typing import Callable
# from events_handlers.handler import GameHandler
from game.map.map import GroupType
from game.player.modules.collision import CollisionModule


class MoveModule(Module):
    __slots__ = ('_position', '_collisions', '_velocity', '_direction')

    def start(self, velocity: int):
        self._position: Position2D = self._context.get_module(ModuleType.Position)
        self._collisions: CollisionModule = self._context.get_module(ModuleType.Collision)
        self._velocity = velocity
        self._direction = pygame.Vector2(0, 0)

        self.edge_handler: dict[str, dict[int, Callable[[Position2D, pygame.FRect], None]]] = {
            'x': {
                +1: lambda pos, rect: pos.set_right(RectType.Hitbox, rect.left),
                -1: lambda pos, rect: pos.set_left(RectType.Hitbox, rect.right),
            },
            'y': {
                +1: lambda pos, rect: pos.set_bottom(RectType.Hitbox, rect.top),
                -1: lambda pos, rect: pos.set_top(RectType.Hitbox, rect.bottom),
            }
        }

    @property
    def direction(self):
        return self._direction

    def move_axis(self, dt: float, direction: float, axis: str) -> None:
        new_pos = getattr(self._position, axis) + direction * self._velocity * dt
        setattr(self._position, axis, new_pos)

        handler = self.edge_handler[axis][1 if direction > 0 else -1]
        for tile in self._collisions.get_collision(GroupType.Obsticles):
            position: Position2D = tile.get_module(ModuleType.Position)
            rect = position.get_rect(RectType.Hitbox)
            handler(self._position, rect)

    def set_direction(self, new_direction: pygame.Vector2):
        self._direction = new_direction

    def move(self, dt: float, direction: pygame.Vector2):
        # print(self._position.get_rect(RectType.RenderRect).center)
        # print(self._position)
        self.move_axis(dt, direction.x, 'x')
        self.move_axis(dt, direction.y, 'y')
