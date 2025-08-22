from engine.base_tile.modules.basic_modules import Module
from game.player.modules.state_machine.states.idle_state import PlayerIdle
from game.player.modules.state_machine.states.run_state import PlayerRun
from game.player.modules.state_machine.states.dodge_state import PlayerDodge
from game.player.modules.state_machine.states.state import State


class PlayerStateMachine(Module):
    def start(self):
        self._states: dict[str, State] = {
            'idle': PlayerIdle(self._context, 0, {'run'}),
            'run': PlayerRun(self._context, 0, {'idle', 'dodge'}),
            'dodge': PlayerDodge(self._context, 70, {'idle', 'run'})
        }
        self._current_state = self._states['idle']
        self._current_state.enter()

    def change_state(self):
        new_state = self._current_state.change_state()
        if not self._current_state.can_change_state(new_state):
            return

        new_state = self._states[new_state]
        if not new_state.cooldown.ready():
            return

        self._current_state.exit()
        self._current_state = new_state
        self._current_state.enter()

    def update_cooldowns(self, dt):
        for state in self._states.values():
            state.cooldown.update(dt)

    def update(self, dt: float):
        self.update_cooldowns(dt)
        self.change_state()
        self._current_state.update(dt)
