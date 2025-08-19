from game.tiles.tile import BaseTile
from game.tiles.modules.basic_modules import ModuleType, Module
from game.assets_manager.assets_manager import AssetsManager
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.AABBtree.AABBModule import AABBModule
from game.map.map import GroupType
import pygame


class Bullet(BaseTile):
    def __init__(self, pos: tuple[int, int], direction: pygame.Vector2):
        super().__init__()
        self.new_module(ModuleType.Position, Position2D, pos)

        self.new_module(ModuleType.Movement, MoveModule, 600, direction)

        image: pygame.Surface = AssetsManager.get('weapon').get('bullet')
        self.new_module(ModuleType.Renderer, BulletRenderer, image)

        self.new_module(ModuleType.AABB, AABBModule, [GroupType.Visible])

    def update(self, dt):
        self.get_module(ModuleType.AABB).update()


class MoveModule(Module):
    __slots__ = ('_position', '_velocity', '_direction')

    def start(self, velocity: int, direction: pygame.Vector2):
        self._position: Position2D = self._context.get_module(ModuleType.Position)
        self._velocity = velocity
        self._direction = direction

    @property
    def direction(self):
        return self._direction

    def move_axis(self, dt: float, direction: float, axis: str) -> None:
        new_pos = getattr(self._position, axis) + direction * self._velocity * dt
        setattr(self._position, axis, new_pos)

    def update(self, dt: float):
        self.move_axis(dt, self._direction.x, 'x')
        self.move_axis(dt, self._direction.y, 'y')


class BulletRenderer(Module):
    def start(self, image: pygame.Surface):
        self._position: Position2D = self._context.get_module(ModuleType.Position)
        self._image = self.rotation_image(image)

        self._position.new_rect(RectType.RenderRect, self._image.size, 'center')

    @property
    def pos(self) -> tuple[float, float]:
        return self._position.get_rect(RectType.RenderRect).topleft

    def render(self, surface: pygame.Surface, pos: tuple[int, int]):
        surface.blit(self._image, pos)

    def rotation_image(self, image) -> pygame.Surface:
        module: MoveModule = self._context.get_module(ModuleType.Movement)
        angle = module.direction.angle_to(pygame.Vector2(1, 0))
        return pygame.transform.rotate(image, angle)
