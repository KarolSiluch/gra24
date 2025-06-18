import pygame
from game.tiles.tile import Tile
from abc import ABC, abstractmethod


class AABBTree:
    def __init__(self):
        self._head: AABBLeaf | AABBContainer | None = None

    def instert(self, tile: Tile) -> None:
        if self._head is None:
            self._head = AABBLeaf(tile)
        elif self._head.leaf or not self._head.rect.contains(tile.rect):
            self._head = AABBContainer(None, self._head, AABBLeaf(tile))
        else:
            self._head.insert(tile)

    def print(self, display: pygame.Surface):
        self._head.print(display)


class AABBNode(ABC):
    def __init__(self, leaf, parent, rect):
        self._leaf: bool = leaf
        self._parent: AABBContainer = parent
        self._rect: pygame.FRect = rect

    @property
    def leaf(self):
        return self._leaf

    @property
    def rect(self):
        return self._rect

    def set_parent(self, node):
        self._parent = node

    @abstractmethod
    def get_rect(self) -> pygame.FRect: ...

    @abstractmethod
    def print(self, display: pygame.Surface) -> None: ...


class AABBLeaf(AABBNode):
    def __init__(self, tile):
        self._tile: Tile = tile
        super().__init__(True, None, self.get_rect())

    def get_rect(self) -> pygame.FRect:
        return self._tile.rect

    def print(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, 'blue', self._rect, 2)


class AABBContainer(AABBNode):
    def __init__(self, parent: AABBNode, node1: AABBNode, node2: AABBNode):
        self._node1: AABBLeaf | AABBContainer = node1
        self._node1.set_parent(self)
        self._node2: AABBLeaf | AABBContainer = node2
        self._node2.set_parent(self)
        super().__init__(False, parent, self.get_rect())
        print(self._parent)

    @staticmethod
    def get_nodes_rect(node1: AABBNode | Tile, node2: AABBNode | Tile) -> pygame.FRect:
        return node1.rect.union(node2.rect)

    @staticmethod
    def area(rect: pygame.FRect) -> int:
        return rect.width * rect.height

    def get_rect(self) -> None:
        return self.get_nodes_rect(self._node1, self._node2)

    def insert(self, tile: Tile) -> None:
        if not self._node1.leaf and self._node1.rect.contains(tile.rect):
            self._node1.insert(tile)
        elif not self._node2.leaf and self._node2.rect.contains(tile.rect):
            self._node2.insert(tile)
        else:
            rect1 = self.get_nodes_rect(self._node1, tile)
            rect2 = self.get_nodes_rect(self._node2, tile)
            if self.area(rect1) < self.area(rect2):
                self._node1 = AABBContainer(self._node1._parent, self._node1, AABBLeaf(tile))
            else:
                self._node2 = AABBContainer(self._node2._parent, self._node2, AABBLeaf(tile))

    def print(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, 'red', self._rect, 1)
        self._node1.print(display)
        self._node2.print(display)
