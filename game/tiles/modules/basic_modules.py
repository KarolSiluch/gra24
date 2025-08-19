from enum import Enum
from abc import ABC, abstractmethod
from typing import Protocol


class ModuleType(Enum):
    Position = 0,
    Renderer = 1,
    AABB = 2,
    Movement = 3,
    Collision = 4,
    Weapon = 5,
    StateMachine = 6,
    Controls = 7


class Context(Protocol):
    def get_module(self, module_type: ModuleType): ...


class Module(ABC):
    def __init__(self, context: Context):
        self._context = context
        super().__init__()

    @abstractmethod
    def start(self) -> None: ...

    def update(self) -> None: ...
