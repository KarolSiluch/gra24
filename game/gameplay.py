from events_handlers.handler import GameHandler
import pygame
from game.player.player import Player
import game.camera.game_camera as camera
from game.tiles.tile import Tile
from game.AABBtree.AABBtree import AABBTree


class Gameplay:
    _events_handler: GameHandler = None

    @classmethod
    def set_handler(cls, handler) -> None:
        cls._events_handler = handler

    def update_handler(self) -> list[pygame.Event]:
        return self._events_handler.update()

    @classmethod
    def events_handler(cls) -> GameHandler:
        return cls._events_handler

    def __init__(self, handler: GameHandler):
        self.set_handler(handler)
        self._player = Player()
        self._renderer = GameplayRenderer(self)
        self._camera = camera.Camera()

        tile_image = pygame.Surface((16, 16))
        tile_image.fill('green')
        self.tiles = [
            self._player,
            Tile(tile_image, center=(150, 150)),
            Tile(tile_image, center=(400, 200)),
            Tile(tile_image, center=(380, 180)),
        ]

        self.AABB_tree = AABBTree()
        for tile in self.tiles:
            self.AABB_tree.instert(tile)

    @property
    def renderer(self):
        return self._renderer

    @property
    def camera(self):
        return self._camera

    def update(self):
        self._player.move(self._events_handler)
        if self._events_handler.get('mouse1'):
            tile_image = pygame.Surface((16, 16))
            tile_image.fill('green')
            tile = Tile(tile_image, center=pygame.mouse.get_pos())
            self.tiles.append(tile)
            self.AABB_tree.instert(tile)


class GameplayRenderer:
    def __init__(self, game: Gameplay):
        self._game = game

    def render(self, surface: pygame.Surface):
        surface.fill('purple')
        tiles: tuple[Tile] = self._game.tiles
        for tile in tiles:
            tile.renderer.render(surface, tile.rect.topleft)
        self._game.AABB_tree.print(surface)
