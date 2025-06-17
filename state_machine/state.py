from abc import ABC, abstractmethod


class State(ABC):
    @abstractmethod
    def update(self): ...

    @abstractmethod
    def change_state(self) -> None | list[str]: ...

    @abstractmethod
    def enter(self): ...

    @abstractmethod
    def exit(self): ...
