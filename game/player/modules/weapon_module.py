from game.tiles.modules.basic_modules import Module, Context


class WeaponModule(Module):
    def start(self, weapon: Context):
        self._weapon = weapon

    @property
    def weapon(self):
        return self._weapon
