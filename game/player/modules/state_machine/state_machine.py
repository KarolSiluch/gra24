from game.tiles.modules.basic_modules import Module
from game.player.modules.state_machine.states.idle_state import PlayerIdle
from game.player.modules.state_machine.states.run_state import PlayerRun
from game.player.modules.state_machine.states.state import State


class PlayerStateMachine(Module):
    def start(self):
        self._states: dict[str, State] = {
            'idle': PlayerIdle(self._context, {'run'}),
            'run': PlayerRun(self._context, {'idle'})
        }
        self._current_state = self._states['idle']
        self._current_state.enter()

    def change_state(self):
        new_state = self._current_state.change_state()
        if not self._current_state.can_change_state(new_state):
            return

        self._current_state.exit()
        self._current_state = self._states[new_state]
        self._current_state.enter()

    def update(self, dt: float):
        self.change_state()
        self._current_state.update(dt)
