from abc import ABC, abstractmethod
from game.tiles.modules.basic_modules import Context


class State(ABC):
    def __init__(self, context: Context, possible_next_states: set):
        self._context = context
        self._possible_next_states = possible_next_states

    def can_change_state(self, state: str):
        return state in self._possible_next_states

    def update(self, dt: float): ...

    @abstractmethod
    def change_state(self) -> None | list[str]: ...

    def enter(self): ...

    def exit(self): ...
