import pygame
from events_handlers.handler import GameHandler
from game.tiles.tile import Tile
from game.tiles.modules.basic_modules import Module, ModuleType
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.map.map import GameMap, GroupType
from game.AABBtree.AABBModule import AABBModule


class Player(Tile):
    def __init__(self, groups):
        image = pygame.Surface((10, 20))
        image.fill('white')
        super().__init__(groups, image, center=(100, 100))

        self.new_module(ModuleType.Collision, CollisionModule, (GroupType.Obsticles,))

        self._move = MoveModule(self)
        self._move.start()

    def update(self, events: GameHandler):
        self._move.update(events)
        self.get_module(ModuleType.AABB).update()


class MoveModule(Module):
    def start(self):
        self._position: Position2D = self._context.get_module(ModuleType.Position)
        self._collisions: CollisionModule = self._context.get_module(ModuleType.Collision)

    def move(self, events: GameHandler):
        x_direction = events.get('right') - events.get('left')
        self._position.x += x_direction * 3
        self._collisions.update()
        for tile in self._collisions.get_tiles(GroupType.Obsticles):
            position: Position2D = tile.get_module(ModuleType.Position)
            rect = position.get_rect(RectType.Hitbox)
            if x_direction > 0:
                self._position.set_right(RectType.Hitbox, rect.left)
            else:
                self._position.set_left(RectType.Hitbox, rect.right)

        y_direction = events.get('down') - events.get('up')
        self._position.y += y_direction * 3
        self._collisions.update()
        for tile in self._collisions.get_tiles(GroupType.Obsticles):
            position: Position2D = tile.get_module(ModuleType.Position)
            rect = position.get_rect(RectType.Hitbox)
            if y_direction > 0:
                self._position.set_bottom(RectType.Hitbox, rect.top)
            else:
                self._position.set_top(RectType.Hitbox, rect.bottom)

    def update(self, events: GameHandler):
        self.move(events)


class CollisionModule(Module):
    def start(self, collision_types: tuple[GroupType]):
        self._collisions = {group_type: [] for group_type in collision_types}
        self._AABB: AABBModule = self._context.get_module(ModuleType.AABB)

    def update(self):
        for group_type in self._collisions.keys():
            self._collisions[group_type] = GameMap.get_group(group_type).AABBCollision(self._AABB)

    def get_tiles(self, group_type: GroupType) -> list[Tile]:
        return self._collisions.get(group_type, [])
