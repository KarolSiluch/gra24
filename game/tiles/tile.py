import pygame
from game.AABBtree.AABBModule import AABBModule
from game.player.modules.Position2DModule import Position2D, RectType


class Tile:
    def __init__(self, groups, image: pygame.Surface, **pos):
        self._rect = image.get_frect(**pos)

        self._position = Position2D()
        (offset, position), = pos.items()
        self._position.start(pygame.Vector2(position))
        self._position.new_rect(RectType.Hitbox, image.get_size(), offset)
        self._position.new_rect(RectType.RenderRect, image.get_size(), offset)

        self._renderer = RendererModule()
        self._renderer.start(self, image)

        self.AABBmodule = AABBModule()
        self.AABBmodule.start(self, groups)

    @property
    def image(self):
        return self._renderer._image

    @property
    def rect(self):
        return self._rect

    @property
    def renderer(self):
        return self._renderer


class RendererModule:
    def start(self, context: Tile, image: pygame.Surface):
        self._context = context
        self._image = image
        self._rect = self._context._position.get_rect(RectType.RenderRect)

    @property
    def pos(self) -> tuple[float, float]:
        return self._rect.topleft

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        surface.blit(self._image, pos)
