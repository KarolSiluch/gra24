import pygame
from engine.base_tile.modules.Position2DModule import Position2D, RectType
from engine.base_tile.modules.basic_modules import Module, ModuleType
from abc import abstractmethod


class BaseRenderer(Module):
    @abstractmethod
    def render(self, surface: pygame.Surface, pos: pygame.Vector2) -> None: ...


class RendererModule(BaseRenderer):
    def start(self, image: pygame.Surface):
        self._image = image
        position: Position2D = self._context.get_module(ModuleType.Position)
        self._rect = position.get_rect(RectType.RenderRect)

    def render(self, surface: pygame.Surface, pos: pygame.Vector2) -> None:
        surface.blit(self._image, pos)
