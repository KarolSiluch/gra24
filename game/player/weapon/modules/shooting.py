# import pygame
from game.tiles.modules.basic_modules import Module, ModuleType
from game.player.weapon.modules.position import WeaponPosition
from game.player.weapon.bullet.bullet import Bullet


class ShootingModule(Module):
    def start(self):
        self._position: WeaponPosition = self._context.get_module(ModuleType.Position)

    def shoot(self):
        Bullet(self._position.pos, self._position.offset_vector.normalize())
