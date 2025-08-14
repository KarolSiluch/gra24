import pygame
from game.tiles.modules.basic_modules import Module, ModuleType, Context
from game.assets_manager.animation import Animation
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.player.weapon.weapon import WeaponRenderer
from game.player.modules.weapon_module import WeaponModule


class PlayerAnimation:
    def __init__(self, context: Context, animation: Animation):
        self._animation = animation
        self._position: Position2D = context.get_module(ModuleType.Position)

        x, y = self._position.get_rect(RectType.RenderRect).size
        self._rect = self._animation.img().get_rect(center=(x // 2, y // 2))

    @property
    def rect(self):
        return self._rect

    def reset(self):
        self._animation.reset()

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

        self._shadow_image = pygame.Surface((15, 7), flags=pygame.SRCALPHA)
        pygame.draw.ellipse(self._shadow_image, (20, 20, 20), pygame.Rect((0, 0), self._shadow_image.size))
        self._shadow_rect = self._shadow_image.get_rect(center=(self._rect.width // 2, self._rect.height - 6))

        self._animations = self._create_animations(animations)
        self._current_animation = self._animations['run']

        weapon_module: WeaponModule = self._context.get_module(ModuleType.Weapon)
        self._weapon_renderer: WeaponRenderer = weapon_module.weapon.get_module(ModuleType.Renderer)

    def _create_animations(self, animations):
        animation_classes = {
            'idle': PlayerAnimation,
            'run': PlayerAnimation
        }
        return {key: cls(self._context, animations[key]) for key, cls in animation_classes.items()}

    def change_animation(self, animation: str):
        self._current_animation = self._animations.get(animation)
        self._current_animation.reset()

    def update(self, dt):
        self._current_animation.update(dt, True)

    @property
    def pos(self) -> tuple[float, float]:
        return self._rect.topleft

    def img(self, surface: pygame.Surface) -> pygame.Surface:
        # clear
        surface.fill((0, 0, 0, 0))
        # shadow
        surface.blit(self._shadow_image, self._shadow_rect)
        # player
        image = self._current_animation.img()
        surface.blit(image, self._current_animation.rect)
        # weapon
        rotation_point = (self._surface.width // 2, self._surface.height // 2 + 4)
        self._weapon_renderer.render(surface, rotation_point)

        return surface

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        surface.blit(self.img(self._surface), pos)
