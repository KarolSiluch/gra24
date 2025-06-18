import pygame


class Tile:
    def __init__(self, image: pygame.Surface, **pos):
        self._image = image
        self._rect = self._image.get_frect(**pos)
        self._renderer = Renderer(self)

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self._rect

    @property
    def renderer(self):
        return self._renderer


class Renderer:
    def __init__(self, player: Tile):
        self._player = player

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        surface.blit(self._player._image, pos)
