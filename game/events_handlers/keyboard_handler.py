import game.events_handlers.handler as EventHandlers
import pygame


class GameKeyboard(EventHandlers.GameHandler):
    def set_events(self, events: list[pygame.Event]) -> None:
        for event in events:
            if event.type == pygame.QUIT:
                self._events['quit'] = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    self._events['up'] = True
                if event.key == pygame.K_s:
                    self._events['down'] = True
                if event.key == pygame.K_w:
                    self._events['left'] = True
                if event.key == pygame.K_w:
                    self._events['right'] = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w:
                    self._events['up'] = False
                if event.key == pygame.K_s:
                    self._events['down'] = False
                if event.key == pygame.K_w:
                    self._events['left'] = False
                if event.key == pygame.K_w:
                    self._events['right'] = False

    def update(self) -> list[pygame.Event]:
        events = pygame.event.get()
        self.set_events(events)
        return events
