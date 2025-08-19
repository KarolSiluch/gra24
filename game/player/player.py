import pygame
from game.tiles.tile import BaseTile
from game.player.modules.collision import CollisionModule
from game.player.modules.movement import MoveModule
from game.tiles.modules.basic_modules import ModuleType
from game.assets_manager.assets_manager import AssetsManager
from game.AABBtree.AABBModule import AABBModule
from game.tiles.modules.Position2DModule import Position2D, RectType
from game.player.modules.renderer import PlayerRenderer
from game.player.modules.weapon_module import WeaponModule
from game.player.weapon.weapon import Weapon
from game.player.modules.controls import ControlsModule
from game.player.modules.state_machine.state_machine import PlayerStateMachine


class Player(BaseTile):
    def __init__(self, groups):
        super().__init__()
        position: Position2D = self.new_module(ModuleType.Position, Position2D, pygame.Vector2(100, 100))
        position.new_rect(RectType.Hitbox, (12, 5), 'center')
        position.new_rect(RectType.RenderRect, (30, 35), 'center')

        self.new_module(ModuleType.AABB, AABBModule, groups)

        self.new_module(ModuleType.Collision, CollisionModule)

        self.new_module(ModuleType.Movement, MoveModule, 200)

        self.new_module(ModuleType.Weapon, WeaponModule, Weapon(self))

        self.new_module(ModuleType.Controls, ControlsModule)

        animation = AssetsManager.get('player')
        self.new_module(ModuleType.Renderer, PlayerRenderer, animation)

        self.new_module(ModuleType.StateMachine, PlayerStateMachine)

    def update(self, dt: float):
        self.get_module(ModuleType.Controls).update()
        self.get_module(ModuleType.Weapon).update()
        self.get_module(ModuleType.StateMachine).update(dt)
        self.get_module(ModuleType.Renderer).update(dt)
        self.get_module(ModuleType.AABB).update()
