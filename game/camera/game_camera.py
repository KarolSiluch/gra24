import pygame
from game.AABBtree.AABBtree import AABBTree


class Camera:
    def __init__(self):
        self._screen_w = pygame.display.Info().current_w
        self._screen_h = pygame.display.Info().current_h
        self._rect = pygame.FRect(0, 0, self._screen_w, self._screen_h)

    def get_offset(self, game) -> pygame.Vector2:
        offset = pygame.Vector2(self._screen_w // 2, self._screen_h // 2)
        offset -= game._player.rect.center
        return offset

    def get_tiles(self, visible_tiles: AABBTree):
        return visible_tiles.RectCollision(self._rect)
