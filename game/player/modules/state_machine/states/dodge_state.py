from engine.base_tile.modules.basic_modules import Context, ModuleType
from game.player.modules.dodge import DodgeModule
from game.player.modules.movement import MoveModule
from game.player.modules.renderer import PlayerRenderer
# from events_handlers.input_state import InputState
# import pygame
from game.player.modules.state_machine.states.state import State


class PlayerDodge(State):
    def __init__(self, context: Context, possible_next_states: set):
        super().__init__(context, possible_next_states)
        self._dodge: DodgeModule = context.get_module(ModuleType.Dodge)
        self._movement: MoveModule = context.get_module(ModuleType.Movement)

    def enter(self):
        self._dodge.enter()
        renderer: PlayerRenderer = self._context.get_module(ModuleType.Renderer)
        renderer.change_animation('dodge')

    def exit(self):
        self._dodge.exit()

    def update(self, dt: float):
        self._dodge.update(dt)

    def change_state(self) -> None | list[str]:
        if not self._dodge.finished():
            return
        if not self._movement.direction.magnitude():
            return 'idle'
        else:
            return 'run'
