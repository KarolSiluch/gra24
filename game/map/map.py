from enum import Enum
from game.AABBtree.AABBtree import AABBTree


class GroupType(Enum):
    Visible = 1
    Obsticles = 2


class GameMap:
    _groups: dict[GroupType, AABBTree] = {}

    @classmethod
    def init(cls, groups: dict[GroupType, AABBTree]) -> None:
        cls._groups = groups
        cls._groups.get(GroupType.Visible)

    @classmethod
    def get_group(cls, group_type: GroupType) -> AABBTree:
        return cls._groups.get(group_type)

    @classmethod
    def get_groups(cls, *group_types: tuple[GroupType]) -> list[AABBTree]:
        return [cls.get_group(group_type) for group_type in group_types]
