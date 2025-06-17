from state_machine.state import State


class StateMachine(State):
    def __init__(self, states: dict[str, State], first_state) -> None:
        super().__init__()
        self._first_state = first_state
        self._state: str = first_state
        self._states: dict[str, State] = states
        self.enter()

    def replace_state(self, state):
        self._current_state: State = self._states.get(state)

    def enter(self):
        self.replace_state(self._first_state)
        self._current_state.enter()

    def update(self) -> None:
        self._current_state.update()

    def set_state(self, state: str) -> None:
        self._current_state.exit()
        self.replace_state(state)
        self._current_state.enter()
        self._state = state

    def change_state(self) -> None | list[str]:
        new_state = self._current_state.change_state()
        if new_state is None:
            return None
        elif len(new_state) == 1:
            self.set_state(new_state[0])
        elif new_state[0] == '..':
            return new_state[1::]

    def exit(self): ...
