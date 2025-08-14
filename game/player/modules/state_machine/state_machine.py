from game.tiles.modules.basic_modules import Module
from game.player.modules.state_machine.states.idle_state import PlayerIdle
from game.player.modules.state_machine.states.run_state import PlayerRun
from events_handlers.handler import GameHandler


class PlayerStateMachine(Module):
    def start(self):
        self._states = {
            'idle': PlayerIdle(self._context, {'run'}),
            'run': PlayerRun(self._context, {'idle'})
        }
        self._current_state = self._states['idle']

    def change_state(self):
        new_state = self._current_state.change_state()
        if not self._current_state.can_be_next_state(new_state):
            return

        self._current_state.exit()
        self._current_state = self._states[new_state]
        self._current_state.enter()

    def update(self, dt: float, events: GameHandler):
        self.change_state()
        self._current_state.update(dt, events)
