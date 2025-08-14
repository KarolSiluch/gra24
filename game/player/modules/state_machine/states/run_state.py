from game.tiles.modules.basic_modules import Context, ModuleType
from game.player.modules.movement import MoveModule
from game.player.modules.renderer import PlayerRenderer
from events_handlers.handler import GameHandler
import pygame


class PlayerRun:
    def __init__(self, context: Context, possible_next_states: set):
        self._context = context
        self._possible_next_states = possible_next_states
        self._movement: MoveModule = context.get_module(ModuleType.Movement)

    def can_be_next_state(self, state: str):
        return state in self._possible_next_states

    def enter(self):
        renderer: PlayerRenderer = self._context.get_module(ModuleType.Renderer)
        renderer.change_animation('run')

    def exit(self): ...

    def update(self, dt: float, events: GameHandler):
        direction = pygame.Vector2(events.get('right') - events.get('left'), events.get('down') - events.get('up'))
        direction and direction.normalize_ip()
        self._movement.move(dt, direction)

    def change_state(self) -> None | list[str]:
        if not self._movement.direction.magnitude():
            return 'idle'
