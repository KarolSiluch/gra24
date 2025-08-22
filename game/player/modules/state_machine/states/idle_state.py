from engine.base_tile.modules.basic_modules import Context, ModuleType
from game.player.modules.movement import MoveModule
from game.player.modules.renderer import PlayerRenderer
# from events_handlers.input_state import InputState
# import pygame
from game.player.modules.state_machine.states.state import State


class PlayerIdle(State):
    def __init__(self, context: Context, cooldown: int, possible_next_states: set):
        super().__init__(context, cooldown, possible_next_states)
        self._movement: MoveModule = context.get_module(ModuleType.Movement)

    def enter(self):
        super().enter()
        renderer: PlayerRenderer = self._context.get_module(ModuleType.Renderer)
        renderer.change_animation('idle')

    def update(self, dt: float):
        self._movement.move(dt, self._movement.direction)

    def change_state(self) -> None | str:
        if self._movement.direction.magnitude():
            return 'run'
