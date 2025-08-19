from game.tiles.modules.basic_modules import Module, ModuleType
from game.player.modules.movement import MoveModule
from events_handlers.input_state import InputState
import pygame


class ControlsModule(Module):
    def start(self):
        self._movement: MoveModule = self._context.get_module(ModuleType.Movement)

    def update(self):
        x = InputState.pressed('right') - InputState.pressed('left')
        y = InputState.pressed('down') - InputState.pressed('up')
        new_direction = pygame.Vector2(x, y)
        new_direction and new_direction.normalize_ip()
        self._movement.set_direction(new_direction)
