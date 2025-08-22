import pygame
from engine.assets_manager.animation import Animation


class AssetsManager:
    @classmethod
    def init(cls):
        cls._assets = {
            'player': {
                'run': Animation(cls.import_cut_graphics((4, 1), 'assets/run.png'), animation_speed=9),
                'idle': Animation(cls.import_cut_graphics((5, 1), 'assets/idle.png'), animation_speed=7),
                'dodge': Animation(cls.import_cut_graphics((4, 1), 'assets/dodge.png'), animation_speed=0)
            },
            'weapon': {
                'ak': cls.load_image('assets/ak.png'),
                'bullet': cls.load_image('assets/bullet.png')
                },
            'tiles': cls.import_cut_graphics((3, 4), 'assets/walls.png')
        }

    @classmethod
    def get(cls, path: str):
        return cls._assets.get(path)

    @staticmethod
    def load_image(path: str) -> pygame.Surface:
        image = pygame.image.load(path).convert()
        image.set_colorkey((255, 0, 255))
        return image

    @classmethod
    def import_cut_graphics(cls, image_grid: tuple[int], path):
        combined_image = cls.load_image(path)
        image_width = int(combined_image.get_width() / image_grid[0])
        image_height = int(combined_image.get_height() / image_grid[1])
        result = []
        for y in range(image_grid[1]):
            for x in range(image_grid[0]):
                image = pygame.Surface((image_width, image_height), pygame.SRCALPHA)
                offset = (-x * image_width, -y * image_height)
                image.blit(combined_image, offset)
                result.append(image)
        return result
