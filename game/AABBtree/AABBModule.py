from typing import Protocol
from game.AABBtree.AABBtree import AABBTree
from game.player.modules.Position2DModule import RectType, Position2D


class Context(Protocol):
    _position: Position2D


class AABBModule:
    def start(self, context: Context, groups: list[AABBTree]):
        self._context = context
        self._hitbox = context._position.get_rect(RectType.Hitbox)
        self._g = [group.insert(self) for group in groups]

    def get_hitbox(self, rect_type: RectType):
        return self._context._position.get_rect(rect_type)

    def update(self):
        for node in self._g:
            node.reinsert()

    @property
    def context(self):
        return self._context
