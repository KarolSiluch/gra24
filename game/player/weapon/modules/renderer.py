import pygame
from engine.base_tile.modules.basic_modules import ModuleType
from game.player.weapon.modules.position import WeaponPosition
from engine.base_tile.modules.renderer import BaseRenderer


class WeaponRenderer(BaseRenderer):
    def start(self, image: pygame.Surface):
        self._position: WeaponPosition = self._context.get_module(ModuleType.Position)
        self._image = image

    def img(self, scale):
        image = pygame.transform.flip(self._image, False, self._position.offset_vector.x < 0)
        image = pygame.transform.scale(image, (image.width * scale, image.height * scale))
        return pygame.transform.rotate(image, self.rotation_angle())

    def render(self, surface: pygame.Surface, pos: tuple[int, int], scale: float):
        image = self.img(scale)
        surface.blit(image, image.get_rect(center=self._position.get_pos(pos)))

    def rotation_angle(self) -> int:
        return self._position.offset_vector.angle_to(pygame.Vector2(1, 0))
