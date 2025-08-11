from game.map.map import GameMap, GroupType
from game.AABBtree.AABBModule import AABBModule
from game.tiles.tile import Tile
from game.tiles.modules.basic_modules import Module, ModuleType


class CollisionModule(Module):
    __slots__ = ('_AABB')

    def start(self):
        self._AABB: AABBModule = self._context.get_module(ModuleType.AABB)

    def get_collision(self, group_type: GroupType) -> list[Tile]:
        return GameMap.get_group(group_type).AABBCollision(self._AABB)
