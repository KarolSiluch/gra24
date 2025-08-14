from game.tiles.modules.basic_modules import Context, ModuleType
from game.player.modules.movement import MoveModule
from game.player.modules.renderer import PlayerRenderer
from events_handlers.input_state import InputState
import pygame
from game.player.modules.state_machine.states.state import State


class PlayerIdle(State):
    def __init__(self, context: Context, possible_next_states: set):
        super().__init__(context, possible_next_states)
        self._movement: MoveModule = context.get_module(ModuleType.Movement)

    def enter(self):
        renderer: PlayerRenderer = self._context.get_module(ModuleType.Renderer)
        renderer.change_animation('idle')

    def change_state(self) -> None | str:
        events = InputState
        x = events.pressed('right') - events.pressed('left')
        y = events.pressed('down') - events.pressed('up')
        if pygame.Vector2(x, y).magnitude():
            return 'run'
