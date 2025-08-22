from game.tiles.tile import BaseTile
from engine.base_tile.modules.basic_modules import Context, ModuleType
from engine.assets_manager.assets_manager import AssetsManager
from game.player.weapon.modules.renderer import WeaponRenderer
from game.player.weapon.modules.position import WeaponPosition
from game.player.weapon.modules.shooting import ShootingModule


class Weapon(BaseTile):
    def __init__(self, owner: Context):
        super().__init__()
        self.new_module(ModuleType.Position, WeaponPosition, owner)

        self.new_module(ModuleType.Shooting, ShootingModule)

        image = AssetsManager.get('weapon').get('ak')
        self.new_module(ModuleType.Renderer, WeaponRenderer, image)

    def update(self):
        self.get_module(ModuleType.Position).update()
