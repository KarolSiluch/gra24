from abc import ABC, abstractmethod
from engine.base_tile.modules.basic_modules import Context
from engine.cooldown.cooldown import Cooldown


class State(ABC):
    def __init__(self, context: Context, cooldown: int, possible_next_states: set):
        self._context = context
        self._cooldown = Cooldown(cooldown, True)
        self._possible_next_states = possible_next_states

    @property
    def cooldown(self) -> Cooldown:
        return self._cooldown

    def can_change_state(self, state: str):
        return state in self._possible_next_states

    def update(self, dt: float): ...

    @abstractmethod
    def change_state(self) -> None | list[str]: ...

    def enter(self):
        self._cooldown.reset()

    def exit(self): ...
