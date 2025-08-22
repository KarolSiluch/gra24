from engine.base_tile.modules.basic_modules import Context, ModuleType
from game.player.modules.movement import MoveModule
from game.player.modules.renderer import PlayerRenderer
from game.player.modules.dodge import DodgeModule
from game.player.modules.state_machine.states.state import State


class PlayerRun(State):
    def __init__(self, context: Context, cooldown: int, possible_next_states: set):
        super().__init__(context, cooldown, possible_next_states)
        self._movement: MoveModule = context.get_module(ModuleType.Movement)
        self._dodge: DodgeModule = context.get_module(ModuleType.Dodge)

    def enter(self):
        super().enter()
        self._movement.set_velocity(200)
        renderer: PlayerRenderer = self._context.get_module(ModuleType.Renderer)
        renderer.change_animation('run')

    def exit(self): ...

    def update(self, dt: float):
        self._movement.move(dt, self._movement.direction)

    def change_state(self) -> None | list[str]:
        if not self._movement.direction.magnitude():
            return 'idle'
        if self._dodge.strt_dodge:
            return 'dodge'
