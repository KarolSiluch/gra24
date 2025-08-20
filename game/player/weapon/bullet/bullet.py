from game.tiles.tile import BaseTile
from game.tiles.modules.basic_modules import ModuleType, Module
from game.assets_manager.assets_manager import AssetsManager
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.AABBtree.AABBModule import AABBModule
from game.player.modules.collision import CollisionModule
from game.map.map import GroupType
import pygame


class Bullet(BaseTile):
    def __init__(self, pos: tuple[int, int], direction: pygame.Vector2):
        super().__init__()
        image: pygame.Surface = AssetsManager.get('weapon').get('bullet')

        position: Position2D = self.new_module(ModuleType.Position, Position2D, pos)
        size = image.width + image.height
        position.new_rect(RectType.RenderRect, (size, size), 'center')
        position.new_rect(RectType.Hitbox, (3, 3), 'center')

        self.new_module(ModuleType.AABB, AABBModule, [GroupType.Visible, GroupType.Bullets])

        self.new_module(ModuleType.Collision, CollisionModule)

        self.new_module(ModuleType.Movement, MoveModule, 300, direction)

        self.new_module(ModuleType.Renderer, BulletRenderer, image)

    def update(self, dt):
        self.get_module(ModuleType.AABB).update()
        self.get_module(ModuleType.Movement).update(dt)


class MoveModule(Module):
    __slots__ = ('_position', '_velocity', '_direction')

    def start(self, velocity: int, direction: pygame.Vector2):
        self._position: Position2D = self._context.get_module(ModuleType.Position)
        self._collisions: CollisionModule = self._context.get_module(ModuleType.Collision)
        self._AABB: AABBModule = self._context.get_module(ModuleType.AABB)

        self._velocity = velocity
        self._direction = direction

    @property
    def direction(self):
        return self._direction

    def update(self, dt: float):
        self._position.x += self._direction.x * self._velocity * dt
        self._position.y += self._direction.y * self._velocity * dt

        if self._collisions.get_collision(GroupType.Obsticles):
            self._AABB.kill()


class BulletRenderer(Module):
    def start(self, image: pygame.Surface):
        self._position: Position2D = self._context.get_module(ModuleType.Position)
        self._image = pygame.Surface(self._position.get_rect(RectType.RenderRect).size, flags=pygame.SRCALPHA)
        image = self.rotate_image(image)
        self._image.blit(image, image.get_rect(center=(self._image.width // 2, self._image.height // 2)))

    @property
    def pos(self) -> tuple[float, float]:
        return self._position.get_rect(RectType.RenderRect).topleft

    def render(self, surface: pygame.Surface, pos: tuple[int, int]):
        surface.blit(self._image, pos)

    def rotate_image(self, image) -> pygame.Surface:
        module: MoveModule = self._context.get_module(ModuleType.Movement)
        angle = module.direction.angle_to(pygame.Vector2(1, 0))
        return pygame.transform.rotate(image, angle)
