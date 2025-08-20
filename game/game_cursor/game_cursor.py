import pygame


class Cursor:
    _pos = pygame.Vector2(0, 0)

    @classmethod
    def update(cls, offset: pygame.Vector2) -> None:
        cls._pos = offset + pygame.mouse.get_pos()

    @classmethod
    def get_pos(cls):
        return cls._pos

    @classmethod
    def get_vector(cls, vector: tuple[float, float]) -> pygame.Vector2:
        return cls._pos - vector
