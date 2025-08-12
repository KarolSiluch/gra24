import pygame
from events_handlers.keyboard_handler import GameKeyboard
from game.gameplay import Gameplay
import time


def Render_Text(screen: pygame.Surface, what: str, color, where):
    font = pygame.font.Font(None, 30)
    text = font.render(what, True, pygame.Color(color))
    screen.blit(text, where)


class Game:
    def __init__(self):
        pygame.init()

        screen_size: list[int] = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        flags = pygame.FULLSCREEN | pygame.SCALED
        self._display: pygame. Surface = pygame.display.set_mode((screen_size[0] // 3, screen_size[1] // 3), flags)

        self._running = True
        self._gameplay = Gameplay(GameKeyboard())
        self._clock = pygame.time.Clock()
        self._previous_time = time.time()

    def render(self):
        self._gameplay.renderer.render(self._display)
        Render_Text(self._display, str(int(self._clock.get_fps())), (255, 0, 0), (self._display.width - 40, 3))
        pygame.display.update()

    def run(self):
        while self._running:
            self._clock.tick(500)
            dt = time.time() - self._previous_time
            self._previous_time = time.time()
            for event in self._gameplay.update_handler():
                if event.type == pygame.QUIT:
                    self._running = False

            self._gameplay.update(dt)
            self.render()


if __name__ == '__main__':
    Game().run()
