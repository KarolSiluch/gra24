import pygame


class AssetsManager:
    @classmethod
    def init(cls):
        cls._assets = {
            'player': cls.import_image('assets/Accelerator.png')
        }

    @classmethod
    def get(cls, path: str):
        return cls._assets.get(path)

    @staticmethod
    def import_image(path: str) -> pygame.Surface:
        image = pygame.image.load(path).convert()
        image.set_colorkey((255, 0, 255))
        return image
