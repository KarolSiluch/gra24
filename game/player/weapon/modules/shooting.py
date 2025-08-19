# import pygame
from game.tiles.modules.basic_modules import Module, ModuleType
from game.player.weapon.modules.position import WeaponPosition


class ShootingModule(Module):
    def start(self):
        self._position: WeaponPosition = self._context.get_module(ModuleType.Position)

    def shoot(self):
        print('shooting now!!')
