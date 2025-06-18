from state_machine.state import State


class GameState(State):
    def __init__(self, game):
        super().__init__()
        self._game = game

    def update(self): ...

    def enter(self):
        print('to jest gra')

    def exit(self):
        print('gra się skończyła')

    def change_state(self) -> None | list[str]:
        return None
