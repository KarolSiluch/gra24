import pygame
from game.tiles.modules.basic_modules import Module, Context, ModuleType
from game.tiles.modules.Position2DModule import Position2D


class WeaponPosition(Module):
    def start(self, owner: Context):
        self._owner_position: Position2D = owner.get_module(ModuleType.Position)
        self._offset_size = 4
        self._offset_vector = self.cursor_vector(self._offset_size)

    @property
    def offset_vector(self):
        return self._offset_vector

    def update(self):
        self._offset_vector = self.cursor_vector(self._offset_size)

    def cursor_vector(self, size: int):
        mx, my = pygame.mouse.get_pos()
        vector = pygame.Vector2(mx - self._owner_position.x, my - self._owner_position.y)
        vector and vector.scale_to_length(size)
        return vector

    def get_pos(self, pos: tuple[int, int]) -> pygame.Vector2:
        return self._offset_vector + pos
