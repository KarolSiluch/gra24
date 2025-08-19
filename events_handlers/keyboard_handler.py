import events_handlers.handler as EventHandlers
import pygame


class Keyboardhandler(EventHandlers.EventsHandler):
    def set_events(self, event: pygame.Event) -> None:
        if event.type in {pygame.KEYDOWN, pygame.KEYUP}:
            if event.key == pygame.K_w:
                self._input_state.set_action('up', event.type == pygame.KEYDOWN)
            elif event.key == pygame.K_s:
                self._input_state.set_action('down', event.type == pygame.KEYDOWN)
            elif event.key == pygame.K_a:
                self._input_state.set_action('left', event.type == pygame.KEYDOWN)
            elif event.key == pygame.K_d:
                self._input_state.set_action('right', event.type == pygame.KEYDOWN)

        elif event.type in {pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP}:
            if event.button == 1:
                self._input_state.set_action('shoot', event.type == pygame.MOUSEBUTTONDOWN)
