import pygame


class Animation:
    def __init__(self, images, animation_speed=5, loop=True):
        self.images = images
        self.loop = loop
        self.animation_speed = animation_speed
        self.reset()

    def reset(self):
        self.done = False
        self.frame = 0

    def length(self):
        return len(self.images)

    def set_frame(self, frame: float):
        self.frame = frame

    # True: +, False: -
    def update(self, dt, direction: int):
        if self.loop:
            self.frame += direction * self.animation_speed * dt
        else:
            self.frame = min(self.frame + direction * self.animation_speed * dt, self.length() - 1)
            if self.frame >= self.length() - 1:
                self.done = True

    def img(self) -> pygame.Surface:
        return self.images[int(self.frame % (self.length() - 1))]
