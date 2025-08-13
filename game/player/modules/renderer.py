import pygame
from game.tiles.modules.basic_modules import Module, ModuleType, Context
from game.assets_manager.animation import Animation
from game.tiles.modules.Position2DModule import Position2D, RectType


class PlayerAnimation:
    def __init__(self, context: Context, animation: Animation):
        self._animation = animation
        self._position: Position2D = context.get_module(ModuleType.Position)

        x, y = self._position.get_rect(RectType.RenderRect).size
        self._rect = self._animation.img().get_rect(center=(x // 2, y // 2))

    @property
    def rect(self):
        return self._rect

    def update(self, dt, direction):
        self._animation.update(dt, direction)

    def img(self):
        image = self._animation.img()
        flip = pygame.mouse.get_pos()[0] < self._position.x
        return pygame.transform.flip(image, flip, False)


class PlayerRenderer(Module):
    def start(self, animations: dict[str, Animation]):
        position: Position2D = self._context.get_module(ModuleType.Position)
        self._rect = position.get_rect(RectType.RenderRect)
        self._surface = pygame.Surface(self._rect.size, flags=pygame.SRCALPHA)

        self._shadow = pygame.Surface((15, 7)).get_rect(center=(self._rect.width // 2, self._rect.height - 6))

        self._animations = self._create_animations(animations)
        self._current_animation = self._animations['idle']

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
        return self._rect.topleft

    def img(self, surface: pygame.Surface) -> pygame.Surface:
        surface.fill((0, 0, 0, 0))
        pygame.draw.ellipse(surface, (20, 20, 20), self._shadow)
        image = self._current_animation.img()
        surface.blit(image, self._current_animation.rect)
        return surface

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        surface.blit(self.img(self._surface), pos)
