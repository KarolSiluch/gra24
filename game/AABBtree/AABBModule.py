from typing import Protocol
from game.AABBtree.AABBtree import AABBTree
from game.tiles.modules.Position2DModule import RectType, Position2D
from game.tiles.modules.basic_modules import Module, ModuleType
from game.map.map import GameMap


class Context(Protocol):
    _position: Position2D


class AABBModule(Module):
    def start(self, groups: list[AABBTree]):
        self._g = [GameMap.get_group(group).insert(self) for group in groups]

    def get_hitbox(self, rect_type: RectType):
        position: Position2D = self._context.get_module(ModuleType.Position)
        return position.get_rect(rect_type)

    def update(self):
        for node in self._g:
            node.reinsert()

    def kill(self):
        for node in self._g:
            node.remove()

    @property
    def context(self):
        return self._context
