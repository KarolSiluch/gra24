from game.tiles.modules.basic_modules import Module, ModuleType
from game.player.weapon.weapon import Weapon
from game.player.weapon.modules.shooting import ShootingModule


class WeaponModule(Module):
    def start(self, weapon: Weapon):
        self._weapon = weapon

    @property
    def weapon(self):
        return self._weapon

    def update(self):
        self._weapon.update()

    def shoot(self):
        module: ShootingModule = self._weapon.get_module(ModuleType.Shooting)
        module.shoot()
