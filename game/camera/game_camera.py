import pygame


class Camera:
    def __init__(self):
        self._screen_w = pygame.display.Info().current_w // 2
        self._screen_h = pygame.display.Info().current_h // 2

    def get_offset(self, game) -> pygame.Vector2:
        offset = pygame.Vector2(self._screen_w, self._screen_h)
        offset -= game._player._pos
        return offset
