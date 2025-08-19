import pygame
from game.tiles.modules.basic_modules import Module, ModuleType
from game.player.weapon.modules.position import WeaponPosition


class WeaponRenderer(Module):
    def start(self, image: pygame.Surface):
        self._position: WeaponPosition = self._context.get_module(ModuleType.Position)
        self._image = image

    def img(self):
        image = pygame.transform.flip(self._image, False, self._position.offset_vector.x < 0)
        return pygame.transform.rotate(image, self.rotation_angle())

    def render(self, surface: pygame.Surface, pos: tuple[int, int]):
        image = self.img()
        surface.blit(image, image.get_rect(center=self._position.get_pos(pos)))

    def rotation_angle(self) -> int:
        return self._position.offset_vector.angle_to(pygame.Vector2(1, 0))
