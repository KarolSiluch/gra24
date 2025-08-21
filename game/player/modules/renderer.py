import pygame
from game.tiles.modules.basic_modules import Module, ModuleType, Context
from game.assets_manager.animation import Animation
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.player.modules.movement import MoveModule
from game.player.modules.dodge import DodgeModule
from game.player.weapon.weapon import WeaponRenderer
from game.player.modules.weapon_module import WeaponModule
from game.game_cursor.game_cursor import Cursor
from math import copysign


class PlayerDodgeAnimation:
    def __init__(self, context: Context, animation: Animation):
        self._animation = animation
        self._dodge: DodgeModule = context.get_module(ModuleType.Dodge)

        self._position: Position2D = context.get_module(ModuleType.Position)
        x, y = self._position.get_rect(RectType.RenderRect).size
        self._x, self._y = x // 2, y // 2

        weapon_module: WeaponModule = context.get_module(ModuleType.Weapon)
        self._weapon_renderer: WeaponRenderer = weapon_module.weapon.get_module(ModuleType.Renderer)

        self.y_offsey = lambda x: 0.0002 * x * (x - 360)

    def reset(self):
        self._flip = Cursor.get_pos().x < self._position.x

        self._directionx = -copysign(1, self._dodge._moving_direction.x)
        self._animation.reset()

    def update(self, dt: float):
        self._animation.set_frame(self._animation.length() * self._dodge.progression())

    def blit_ip(self, surface: pygame.Surface):
        y_offset = self.y_offsey(self._dodge._angle)

        image = self._animation.img()
        image = pygame.transform.flip(image, self._flip, False)
        image = pygame.transform.rotate(image, self._dodge._angle * self._directionx)
        surface.blit(image, image.get_rect(center=(self._x, self._y + y_offset)))

        rotation_point = (surface.width // 2, surface.height // 2 + 4 + y_offset)
        self._weapon_renderer.render(surface, rotation_point, 1 - self._dodge.progression())


class PlayerAnimation:
    def __init__(self, context: Context, animation: Animation):
        self._animation = animation
        self._position: Position2D = context.get_module(ModuleType.Position)
        self._movement: MoveModule = context.get_module(ModuleType.Movement)

        x, y = self._position.get_rect(RectType.RenderRect).size
        self._rect = self._animation.img().get_rect(center=(x // 2, y // 2))

        weapon_module: WeaponModule = context.get_module(ModuleType.Weapon)
        self._weapon_renderer: WeaponRenderer = weapon_module.weapon.get_module(ModuleType.Renderer)

    @property
    def rect(self):
        return self._rect

    def reset(self):
        self._animation.reset()

    def update(self, dt):
        direction = 1
        if self._movement.direction.x:
            direction_x = copysign(1, self._movement.direction.x)
            cursor_x = copysign(1, Cursor.get_pos().x - self._position.x)
            direction = direction_x * cursor_x
        self._animation.update(dt, direction)

    def blit_ip(self, surface: pygame.Surface):
        image = self._animation.img()
        flip = Cursor.get_pos().x < self._position.x
        image = pygame.transform.flip(image, flip, False)
        surface.blit(image, self._rect)

        rotation_point = (self._rect.centerx, self._rect.centery + 4)
        self._weapon_renderer.render(surface, rotation_point, 1)


class PlayerRenderer(Module):
    def start(self, animations: dict[str, Animation]):
        position: Position2D = self._context.get_module(ModuleType.Position)
        self._rect = position.get_rect(RectType.RenderRect)
        self._surface = pygame.Surface(self._rect.size, flags=pygame.SRCALPHA)

        self._shadow_image = pygame.Surface((15, 7), flags=pygame.SRCALPHA)
        pygame.draw.ellipse(self._shadow_image, (20, 20, 20, 150), pygame.Rect((0, 0), self._shadow_image.size))
        self._shadow_rect = self._shadow_image.get_rect(center=(self._rect.width // 2, self._rect.height - 6))

        self._animations = self._create_animations(animations)
        self._current_animation = self._animations['idle']

    def _create_animations(self, animations):
        animation_classes = {
            'idle': PlayerAnimation,
            'run': PlayerAnimation,
            'dodge': PlayerDodgeAnimation
        }
        return {key: cls(self._context, animations[key]) for key, cls in animation_classes.items()}

    def change_animation(self, animation: str):
        self._current_animation = self._animations.get(animation)
        self._current_animation.reset()

    def update(self, dt):
        self._current_animation.update(dt)

    @property
    def pos(self) -> tuple[float, float]:
        return self._rect.topleft

    def img(self, surface: pygame.Surface) -> pygame.Surface:
        # clear
        surface.fill((0, 0, 0, 0))
        # shadow
        surface.blit(self._shadow_image, self._shadow_rect)
        # player
        self._current_animation.blit_ip(surface)

        return surface

    def render(self, surface: pygame.Surface, pos: pygame.Vector2):
        surface.blit(self.img(self._surface), pos)
