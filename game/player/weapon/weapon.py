import pygame
from game.tiles.tile import BaseTile
from game.tiles.modules.basic_modules import Module, Context, ModuleType
from game.tiles.modules.Position2DModule import Position2D
from game.assets_manager.assets_manager import AssetsManager


class Weapon(BaseTile):
    def __init__(self, owner: Context):
        super().__init__()
        image = AssetsManager.get('weapon')
        self.new_module(ModuleType.Renderer, WeaponRenderer, image, owner)


class WeaponRenderer(Module):
    def start(self, image: pygame.Surface, owner: Context):
        self._owner_position: Position2D = owner.get_module(ModuleType.Position)
        self._image = image

    def mouse_vector(self) -> pygame.Vector2:
        mx, my = pygame.mouse.get_pos()
        return pygame.Vector2(mx - self._owner_position.x, my - self._owner_position.y)

    def img(self):
        vector = self.mouse_vector()
        image = pygame.transform.flip(self._image, False, vector.x < 0)
        angle = vector.angle_to(pygame.Vector2(1, 0))
        return pygame.transform.rotate(image, angle)

    def get_pos(self, pos: tuple[int, int]):
        vector = self.mouse_vector()
        vector.scale_to_length(3)
        vector += pos
        return vector

    def render(self, surface: pygame.Surface, pos: tuple[int, int]):
        image = self.img()
        surface.blit(image, image.get_rect(center=self.get_pos(pos)))
