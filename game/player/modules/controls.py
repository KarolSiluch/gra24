from game.tiles.modules.basic_modules import Module, ModuleType
from game.player.modules.movement import MoveModule
from game.player.modules.weapon_module import WeaponModule
from events_handlers.input_state import InputState
from game.player.modules.dodge import DodgeModule
import pygame


class ControlsModule(Module):
    def start(self):
        self._movement: MoveModule = self._context.get_module(ModuleType.Movement)
        self._weapon: WeaponModule = self._context.get_module(ModuleType.Weapon)
        self._dodge: DodgeModule = self._context.get_module(ModuleType.Dodge)

    def update(self):
        x = InputState.pressed('right') - InputState.pressed('left')
        y = InputState.pressed('down') - InputState.pressed('up')
        new_direction = pygame.Vector2(x, y)
        new_direction and new_direction.normalize_ip()
        self._movement.set_direction(new_direction)

        if InputState.just_pressed('shoot'):
            self._weapon.shoot()

        self._dodge.set_status(InputState.just_pressed('dodge'))
