import events_handlers.handler as EventHandlers
import pygame


class Keyboardhandler(EventHandlers.EventsHandler):
    def set_events(self, event: pygame.Event) -> None:
        if event.type not in {pygame.KEYDOWN, pygame.KEYUP}:
            return
        if event.key == pygame.K_w:
            self._input_state.set_action('up', event.type == pygame.KEYDOWN)
        elif event.key == pygame.K_s:
            self._input_state.set_action('down', event.type == pygame.KEYDOWN)
        elif event.key == pygame.K_a:
            self._input_state.set_action('left', event.type == pygame.KEYDOWN)
        elif event.key == pygame.K_d:
            self._input_state.set_action('right', event.type == pygame.KEYDOWN)
