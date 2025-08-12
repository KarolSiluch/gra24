from game.tiles.tile import BaseTile
from game.player.modules.collision import CollisionModule
from game.player.modules.movement import MoveModule
from events_handlers.handler import GameHandler
from game.tiles.modules.basic_modules import ModuleType
from game.assets_manager.assets_manager import AssetsManager
import pygame
from game.AABBtree.AABBModule import AABBModule
from game.tiles.modules.Position2DModule import Position2D, RectType
# from game.tiles.modules.renderer import RendererModule
from game.tiles.modules.basic_modules import Module
from game.assets_manager.animation import Animation


class Player(BaseTile):
    def __init__(self, groups):
        super().__init__()
        image = AssetsManager.get('player')

        position: Position2D = self.new_module(ModuleType.Position, Position2D, pygame.Vector2(100, 100))
        position.new_rect(RectType.Hitbox, (12, 5), 'center')
        position.new_rect(RectType.RenderRect, image.img().get_size(), 'center')

        self.new_module(ModuleType.Renderer, AnimatedRendererModule, image)

        self.new_module(ModuleType.AABB, AABBModule, groups)

        self.new_module(ModuleType.Collision, CollisionModule)

        self._move = MoveModule(self)
        self._move.start()

    def update(self, dt: float, events: GameHandler):
        self._move.update(dt, events)
        self.get_module(ModuleType.Renderer).update(dt)
        self.get_module(ModuleType.AABB).update()


class AnimatedRendererModule(Module):
    def start(self, animation: pygame.Surface):
        self._animation: Animation = animation
        position: Position2D = self._context.get_module(ModuleType.Position)
        self._rect = position.get_rect(RectType.RenderRect)

    def update(self, dt):
        self._animation.update(dt, True)

    @property
    def pos(self) -> tuple[float, float]:
        return self._rect.topleft

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        image = self._animation.img()
        if pygame.mouse.get_pos()[0] < self._rect.centerx:
            image = pygame.transform.flip(image, True, False)
        surface.blit(image, pos)
