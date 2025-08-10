import pygame
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.tiles.modules.basic_modules import Module, ModuleType


class RendererModule(Module):
    def start(self, image: pygame.Surface):
        self._image = image
        position: Position2D = self._context.get_module(ModuleType.Position)
        self._rect = position.get_rect(RectType.RenderRect)

    @property
    def pos(self) -> tuple[float, float]:
        return self._rect.topleft

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        surface.blit(self._image, pos)
