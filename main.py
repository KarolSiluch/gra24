import pygame
from game.events_handlers.keyboard_handler import GameKeyboard
# from game.events_handlers.handler import EventsHandler
from game.gameplay import Gameplay


class Game:
    def __init__(self):
        self._display = pygame.display.set_mode((800, 600))
        self._running = True
        self._gameplay = Gameplay(GameKeyboard())
        self._clock = pygame.Clock()

    def run(self):
        self._clock.tick(60)
        while self._running:
            for event in self._gameplay.update_handler():
                if event.type == pygame.QUIT:
                    self._running = False


if __name__ == '__main__':
    Game().run()
