import events_handlers.handler as EventHandlers
import pygame


class Keyboardhandler(EventHandlers.EventsHandler):
    def __init__(self):
        super().__init__()
        self._keys = {
            pygame.K_w: 'up',
            pygame.K_s: 'down',
            pygame.K_a: 'left',
            pygame.K_d: 'right'
        }

    def set_events(self, event: pygame.Event) -> None:
        if event.type not in {pygame.KEYDOWN, pygame.KEYUP}:
            return
        if event.key not in self._keys:
            return
        self._input_state.set_action(self._keys[event.key], event.type == pygame.KEYDOWN)
