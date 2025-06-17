from state_machine.state_machine import StateMachine
from game.game_states.gameplay import GameState


class GameMachine(StateMachine):
    def __init__(self, game):
        super().__init__(self.get_states(game), 'game')

    @staticmethod
    def get_states(game):
        return {'game': GameState(game)}
