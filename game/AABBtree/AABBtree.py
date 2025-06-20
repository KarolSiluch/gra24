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
            self._head = AABBLeaf(tile)
        elif self._head.leaf:
            self._head = AABBContainer(None, self._head, AABBLeaf(tile))
        else:
            self._head = self._head.insert(tile) or self._head
            self.rebelance()
        print(self.x)

    def rebelance(self) -> None:
        node = self._head
        if node.balanced():
            print('the tree is balanced')
            return
        print('the tree is not balanced')
        while not node._node1.balanced():
            node = node._node1
            print('skipped layer!')
        print('layer to balance: ', node.layer)
        print('layer of node1: ', node._node1.layer)
        print('layer of node2: ', node._node2.layer)
        node.rebalance()
        if node.balanced():
            print('the tree is now balanced')

        # node1 = node._node1._node1
        # node1.set_parent(node)
        # node2 = node._node2
        # node2.set_parent(node._node1)

        # node._node2 = node1
        # node._node1._node1 = node2

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

    @abstractmethod
    def get_rect(self) -> pygame.FRect: ...

    @abstractmethod
    def AABBcollision(self, rect: pygame.FRect, result: list) -> None: ...

    @abstractmethod
    def print(self, display: pygame.Surface) -> None: ...


class AABBLeaf(AABBNode):
    def __init__(self, tile):
        self._tile: Tile = tile
        super().__init__(True, 0, None, self.get_rect())

    def get_rect(self) -> pygame.FRect:
        return self._tile.rect

    def AABBcollision(self, rect: pygame.FRect, result: list, id) -> None:
        print(id)
        if self.rect.colliderect(rect):
            result.append(self._tile)

    def print(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, 'blue', self._rect, 2)


class AABBContainer(AABBNode):
    def __init__(self, parent: AABBNode, node1: AABBNode, node2: AABBNode):
        self._node1: AABBLeaf | AABBContainer = node1
        self._node2: AABBLeaf | AABBContainer = node2

        self._node1.set_parent(self)
        self._node2.set_parent(self)

        super().__init__(False, max(self._node1.layer, self._node2.layer) + 1, parent, self.get_rect())
        self.set_new_layer()

    @staticmethod
    def get_nodes_rect(node1: AABBNode | Tile, node2: AABBNode | Tile) -> pygame.FRect:
        return node1.rect.union(node2.rect)

    @staticmethod
    def area(rect: pygame.FRect) -> int:
        return rect.width * rect.height

    def rebalance(self):
        bottom_tree = self._node1._node1
        mid_tree = self._node1

        # total_area = self.area(self._rect) + self.area(bottom_tree.rect)
        total_area = self.area(bottom_tree.rect) + self.area(self.get_nodes_rect(mid_tree._node2, self._node2))
        print(total_area)

        new_area1 = self.area(self.get_nodes_rect(bottom_tree._node1, self._node2))
        new_area2 = self.area(self.get_nodes_rect(bottom_tree._node2, mid_tree._node2))
        print(new_area1 + new_area2)
        if new_area1 + new_area2 < total_area:
            print('wybrano to na górze')
            total_area = new_area1 + new_area2
            mid_tree._node2, bottom_tree._node1 = bottom_tree._node1, mid_tree._node2
            bottom_tree._node1.set_parent(bottom_tree)
            mid_tree._node2.set_parent(mid_tree)

        new_area1 = self.area(self.get_nodes_rect(bottom_tree._node1, mid_tree._node2))
        new_area2 = self.area(self.get_nodes_rect(bottom_tree._node2, self._node2))
        print(new_area1 + new_area2)
        if new_area1 + new_area2 < total_area:
            print('wybrano jednak to na górze')
            mid_tree._node2, bottom_tree._node2 = bottom_tree._node2, mid_tree._node2
            bottom_tree._node2.set_parent(bottom_tree)
            mid_tree._node2.set_parent(mid_tree)

        bottom_tree._rect = bottom_tree.get_rect()
        self._node2, mid_tree._node1 = mid_tree._node1, self._node2
        self._node2.set_parent(self)
        bottom_tree.set_parent(mid_tree)
        mid_tree._layer -= 1
        self.update_rect()
        mid_tree.update_rect()
        self.set_new_layer()

    def set_new_layer(self):
        node = self
        while node._parent is not None:
            node._parent._layer = max(node._parent.layer, node.layer + 1)
            node = node._parent

    def update_rect(self):
        if self._node2.layer > self._node1.layer:
            self._node1, self._node2 = self._node2, self._node1

        self._rect = self.get_rect()
        if self._parent is not None:
            self._parent.update_rect()

    def get_rect(self) -> pygame.FRect:
        return self.get_nodes_rect(self._node1, self._node2)

    def insert(self, tile: Tile) -> AABBNode | None:
        rect1_area = self.area(self.get_nodes_rect(self._node1, tile))
        rect2_area = self.area(self.get_nodes_rect(self._node2, tile))

        if not self._node1.leaf and self._node1.rect.contains(tile.rect):
            self._node1 = self._node1.insert(tile) or self._node1

        elif not self._node2.leaf and self._node2.rect.contains(tile.rect):
            self._node2 = self._node2.insert(tile) or self._node2

        elif rect1_area > self.area(self._rect) and rect2_area > self.area(self._rect):
            return AABBContainer(self._parent, self, AABBLeaf(tile))

        elif rect1_area < rect2_area:
            if self._node1.leaf:
                self._node1 = AABBContainer(self, self._node1, AABBLeaf(tile))
            else:
                self._node1 = self._node1.insert(tile) or self._node1
        else:
            if self._node2.leaf:
                self._node2 = AABBContainer(self, self._node2, AABBLeaf(tile))
            else:
                self._node2 = self._node2.insert(tile) or self._node2
        self.update_rect()

    def balanced(self) -> bool:
        if self._node1.leaf and self._node2.leaf:
            return True
        return self._node1.layer - self._node2.layer < 2 and self._node1.balanced()

    def AABBcollision(self, rect: pygame.FRect, result: list, id) -> None:
        if self.rect.colliderect(rect):
            self._node1.AABBcollision(rect, result, id + 1)
            self._node2.AABBcollision(rect, result, id + 1)

    def print(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, (self._layer * 20, self._layer * 20, self._layer * 20), self._rect, 1)
        self._node1.print(display)
        self._node2.print(display)
