import pygame
from engine.base_tile.modules.AABBModule import AABBModule
from engine.base_tile.modules.Position2DModule import Position2D, RectType
from engine.base_tile.modules.renderer import RendererModule
from engine.base_tile.modules.basic_modules import ModuleType
from engine.base_tile.base_tile import BaseTile


class Tile(BaseTile):
    def __init__(self, groups, image: pygame.Surface, **pos):
        super().__init__()

        (offset, position), = pos.items()
        position: Position2D = self.new_module(ModuleType.Position, Position2D, pygame.Vector2(position))
        position.new_rect(RectType.Hitbox, image.get_size(), offset)
        position.new_rect(RectType.RenderRect, image.get_size(), offset)

        self.new_module(ModuleType.Renderer, RendererModule, image)

        self.new_module(ModuleType.AABB, AABBModule, groups)
