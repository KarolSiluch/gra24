class Cooldown:
    def __init__(self, delay: int, ready: bool = False):
        self._delay = delay
        self._time = delay if ready else 0

    def update(self, dt: float) -> None:
        self._time += dt * 100

    def ready(self) -> bool:
        return self._time >= self._delay

    def reset(self) -> None:
        self._time = 0
