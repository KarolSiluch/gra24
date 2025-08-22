from engine.base_tile.modules.basic_modules import Module, ModuleType
from game.player.modules.movement import MoveModule


class DodgeModule(Module):
    def start(self):
        self._movement: MoveModule = self._context.get_module(ModuleType.Movement)
        self._velocity = 320
        self._rotation_speed = 1100
        self._start_dode = False
        self._angle = 0

    @property
    def strt_dodge(self):
        return self._start_dode

    def set_status(self, status: bool) -> None:
        self._start_dode = status

    def enter(self):
        self._moving_direction = self._movement.direction
        self._movement.set_velocity(self._velocity)

    def exit(self):
        self._angle = 0

    def update(self, dt: float):
        self._angle += self._rotation_speed * dt
        self._movement.move(dt, self._moving_direction)

    def progression(self) -> float:
        return self._angle / 360

    def finished(self):
        return self._angle >= 360
