import pygame
from game.tiles.tile import Tile
from abc import ABC, abstractmethod


class AABBTree:
    def __init__(self):
        self._head: AABBLeaf | AABBContainer | None = None
        self.x = 0

    def instert(self, tile: Tile) -> None:
        self.x += 1
        if self._head is None:
            self._head = AABBLeaf(0, tile)
        elif self._head.leaf:
            self._head = AABBContainer(None, 0, self._head, AABBLeaf(0, tile))
        else:
            self._head = self._head.insert(tile) or self._head
        print(self.x)

    def AABBcollision(self, rect: pygame.FRect) -> list[Tile]:
        result = []
        if self._head is not None:
            self._head.AABBcollision(rect, result, 0)
        return result

    def print(self, display: pygame.Surface):
        if self._head is not None:
            self._head.print(display)


class AABBNode(ABC):
    def __init__(self, leaf, layer, parent, rect):
        self._leaf: bool = leaf
        self._layer: int = layer
        self._parent: AABBContainer = parent
        self._rect: pygame.FRect = rect

    @property
    def leaf(self):
        return self._leaf

    @property
    def layer(self):
        return self._layer

    @property
    def rect(self):
        return self._rect

    def set_parent(self, node):
        self._parent = node

    def set_new_layer(self, layer: int):
        self._layer = layer

    @abstractmethod
    def get_rect(self) -> pygame.FRect: ...

    @abstractmethod
    def AABBcollision(self, rect: pygame.FRect, result: list) -> None: ...

    @abstractmethod
    def print(self, display: pygame.Surface) -> None: ...


class AABBLeaf(AABBNode):
    def __init__(self, layer, tile):
        self._tile: Tile = tile
        super().__init__(True, layer, None, self.get_rect())

    def get_rect(self) -> pygame.FRect:
        return self._tile.rect

    def AABBcollision(self, rect: pygame.FRect, result: list, id) -> None:
        print(id)
        if self.rect.colliderect(rect):
            result.append(self._tile)

    def print(self, display: pygame.Surface) -> None:
        print(self._layer)
        pygame.draw.rect(display, 'blue', self._rect, 2)


class AABBContainer(AABBNode):
    def __init__(self, parent: AABBNode, layer: int, node1: AABBNode, node2: AABBNode):
        self._node1: AABBLeaf | AABBContainer = node1
        self._node1.set_parent(self)
        self._node1.set_new_layer(layer + 1)

        self._node2: AABBLeaf | AABBContainer = node2
        self._node2.set_parent(self)
        self._node2.set_new_layer(layer + 1)

        super().__init__(False, layer, parent, self.get_rect())

    @staticmethod
    def get_nodes_rect(node1: AABBNode | Tile, node2: AABBNode | Tile) -> pygame.FRect:
        return node1.rect.union(node2.rect)

    @staticmethod
    def area(rect: pygame.FRect) -> int:
        return rect.width * rect.height

    def set_new_layer(self, layer):
        super().set_new_layer(layer)
        self._node1.set_new_layer(layer)
        self._node1.set_new_layer(layer)

    def update_rect(self, rect: pygame.FRect):
        self._rect = self._rect.union(rect)
        if self._parent is not None:
            self._parent.update_rect(self._rect)

    def get_rect(self) -> None:
        return self.get_nodes_rect(self._node1, self._node2)

    def insert(self, tile: Tile) -> AABBNode | None:
        rect1_area = self.area(self.get_nodes_rect(self._node1, tile))
        rect2_area = self.area(self.get_nodes_rect(self._node2, tile))

        if not self._node1.leaf and self._node1.rect.contains(tile.rect):
            self._node1 = self._node1.insert(tile) or self._node1
            self.update_rect(self._node1.rect)

        elif not self._node2.leaf and self._node2.rect.contains(tile.rect):
            self._node2 = self._node2.insert(tile) or self._node2
            self.update_rect(self._node2.rect)

        elif rect1_area > self.area(self._rect) and rect2_area > self.area(self._rect):
            return AABBContainer(self._parent, self._layer, self, AABBLeaf(self._layer, tile))

        elif rect1_area < rect2_area:
            if self._node1.leaf:
                self._node1 = AABBContainer(self, self._layer + 1, self._node1, AABBLeaf(self._layer + 1, tile))
            else:
                self._node1 = self._node1.insert(tile) or self._node1
            self.update_rect(self._node1.rect)
        else:
            if self._node2.leaf:
                self._node2 = AABBContainer(self, self._layer + 1, self._node2, AABBLeaf(self._layer + 1, tile))
            else:
                self._node2 = self._node2.insert(tile) or self._node2
            self.update_rect(self._node2.rect)

    # def restructure(self):
    #     if self

    def AABBcollision(self, rect: pygame.FRect, result: list, id) -> None:
        if self.rect.colliderect(rect):
            self._node1.AABBcollision(rect, result, id + 1)
            self._node2.AABBcollision(rect, result, id + 1)

    def print(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (self._layer * 20, self._layer * 20, self._layer * 20), self._rect, 1)
        self._node1.print(display)
        self._node2.print(display)
