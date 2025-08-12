import pygame
from game.tiles.modules.basic_modules import Module, Context, ModuleType
from game.assets_manager.animation import Animation
from game.tiles.modules.Position2DModule import Position2D, RectType


class PlayerAnimation:
    def __init__(self, context: Context, animation: Animation):
        self._animation = animation
        self._position: Position2D = context.get_module(ModuleType.Position)

    @property
    def rect(self):
        return self._rect

    def enter(self):
        self._position.new_rect(RectType.RenderRect, self._animation.img().size, 'center')
        self._rect = self._position.get_rect(RectType.RenderRect)

    def update(self, dt, direction):
        self._animation.update(dt, direction)

    def img(self):
        image = self._animation.img()
        flip = pygame.mouse.get_pos()[0] < self._rect.centerx
        return pygame.transform.flip(image, flip, False)


class PlayerRenderer(Module):
    def start(self, animations: dict[str, Animation]):
        self._animations = self._create_animations(animations)
        self._current_animation = self._animations['run']
        self._current_animation.enter()

    def _create_animations(self, animations):
        animation_classes = {
            'idle': PlayerAnimation,
            'run': PlayerAnimation
        }
        return {key: cls(self._context, animations[key]) for key, cls in animation_classes.items()}

    def update(self, dt):
        self._current_animation.update(dt, True)

    @property
    def pos(self) -> tuple[float, float]:
        return self._current_animation.rect.topleft

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        image = self._current_animation.img()
        surface.blit(image, pos)
