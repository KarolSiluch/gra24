import pygame
from events_handlers.keyboard_handler import GameKeyboard
from game.gameplay import Gameplay


class Game:
    def __init__(self):
        pygame.init()

        screen_size: list[int] = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        flags = pygame.FULLSCREEN | pygame.SCALED
        self._display: pygame. Surface = pygame.display.set_mode((screen_size[0] // 3, screen_size[1] // 3), flags)

        self._running = True
        self._gameplay = Gameplay(GameKeyboard())
        self._clock = pygame.time.Clock()

    def render(self):
        self._gameplay.renderer.render(self._display)
        pygame.display.update()

    def run(self):
        while self._running:
            self._clock.tick(60)
            for event in self._gameplay.update_handler():
                if event.type == pygame.QUIT:
                    self._running = False

            self._gameplay.update()
            self.render()


if __name__ == '__main__':
    Game().run()
