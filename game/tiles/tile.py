import pygame
from game.AABBtree.AABBModule import AABBModule
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.tiles.modules.renderer import RendererModule
from game.tiles.modules.basic_modules import Module, ModuleType


class BaseTile:
    def __init__(self):
        self._modules: dict[ModuleType, Module] = {}

    @property
    def renderer(self):
        return self.get_module(ModuleType.Renderer)

    def update(self): ...

    def new_module(self, module_type, module, *atributes) -> Module:
        new_module: Module = module(self)
        self._modules[module_type] = new_module
        new_module.start(*atributes)
        return new_module

    def get_module(self, module_type: ModuleType):
        return self._modules.get(module_type)


class Tile(BaseTile):
    def __init__(self, groups, image: pygame.Surface, **pos):
        super().__init__()

        (offset, position), = pos.items()
        position: Position2D = self.new_module(ModuleType.Position, Position2D, pygame.Vector2(position))
        position.new_rect(RectType.Hitbox, image.get_size(), offset)
        position.new_rect(RectType.RenderRect, image.get_size(), offset)

        self.new_module(ModuleType.Renderer, RendererModule, image)

        self.new_module(ModuleType.AABB, AABBModule, groups)
