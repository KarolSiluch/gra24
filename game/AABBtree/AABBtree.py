import pygame
from game.tiles.tile import Tile
from abc import ABC, abstractmethod


class AABBTree:
    def __init__(self):
        self._head: AABBTreeHead = AABBTreeHead()
        self.x = 0

    def instert(self, tile: Tile) -> None:
        self._head.instert(tile)

    def AABBcollision(self, rect: pygame.FRect) -> list[Tile]:
        pass
        # result = []
        # if self._head is not None:
        #     self._head.AABBcollision(rect, result, 0)
        # return result

    def print(self, display: pygame.Surface):
        self._head.print(display)

# ----------------------------------------------------------------------


class Node(ABC):
    def __init__(self, head):
        self._head: bool = head

    @property
    def head(self):
        return self._head

    @abstractmethod
    def print(self, display: pygame.Surface) -> None: ...

# ----------------------------------------------------------------------


class AABBNode(Node):
    def __init__(self, leaf, layer, rect):
        super().__init__(False)
        self._leaf: bool = leaf
        self._layer: int = layer
        self._parent: AABBContainer | AABBTreeHead | None = None
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

    @property
    def parent(self):
        return self._parent

    def set_parent(self, node):
        self._parent = node

    @abstractmethod
    def get_rect(self) -> pygame.FRect: ...

    @abstractmethod
    def AABBcollision(self, rect: pygame.FRect, result: list) -> None: ...

# ----------------------------------------------------------------------


class AABBTreeHead(Node):
    def __init__(self):
        super().__init__(True)
        self._node: AABBLeaf | AABBContainer | None = None

    def instert(self, tile: Tile) -> None:
        print('----------------')
        if self._node is None:
            self._node = AABBLeaf(tile)
        elif self._node.leaf:
            self._node = AABBContainer(self._node, AABBLeaf(tile))
            self._node.set_parent(self)
        else:
            if new_node := self._node.insert(tile):
                self._node = new_node
                self._node.set_parent(self)
                self._node.update()

    def change_node(self, node: AABBNode):
        self._node = node
        node.set_parent(self)

    def print(self, display):
        if self._node is not None:
            self._node.print(display)

# ----------------------------------------------------------------------


class AABBLeaf(AABBNode):
    def __init__(self, tile):
        self._tile: Tile = tile
        super().__init__(True, 0, self.get_rect())

    def get_rect(self) -> pygame.FRect:
        return self._tile.rect

    def AABBcollision(self, rect: pygame.FRect, result: list, id) -> None:
        print(id)
        if self.rect.colliderect(rect):
            result.append(self._tile)

    def print(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, 'blue', self._rect, 2)

# ----------------------------------------------------------------------


class AABBContainer(AABBNode):
    def __init__(self, node1: AABBNode, node2: AABBNode):
        self._node1: AABBLeaf | AABBContainer = node1
        self._node2: AABBLeaf | AABBContainer = node2

        self._node1.set_parent(self)
        self._node2.set_parent(self)

        new_layer = max(self._node1.layer, self._node2.layer) + 1
        super().__init__(False, new_layer, self.get_rect())

    @staticmethod
    def get_nodes_rect(node1: AABBNode | Tile, node2: AABBNode | Tile) -> pygame.FRect:
        return node1.rect.union(node2.rect)

    @staticmethod
    def perimeter(rect: pygame.FRect) -> int:
        return (rect.width * rect.height)

    def set_node1(self, node: AABBNode):
        self._node1 = node
        self._node1.set_parent(self)

    def set_node2(self, node: AABBNode):
        self._node2 = node
        self._node2.set_parent(self)

    def rebalance(self):
        if self._node1.layer - self._node2.layer <= 1:
            return

        bottom_tree = self._node1._node1
        mid_tree = self._node1

        # total_perimeter = self.perimeter(self._rect) + self.perimeter(bottom_tree.rect)
        total_perimeter = self.perimeter(bottom_tree.rect) + self.perimeter(self.get_nodes_rect(mid_tree._node2, self._node2))
        print(total_perimeter)

        new_perimeter1 = self.perimeter(self.get_nodes_rect(bottom_tree._node1, self._node2))
        new_perimeter2 = self.perimeter(self.get_nodes_rect(bottom_tree._node2, mid_tree._node2))
        print(new_perimeter1 + new_perimeter2)
        if mid_tree._node2.layer == bottom_tree._node1.layer and new_perimeter1 + new_perimeter2 < total_perimeter:
            print('wybrano to na górze')
            total_perimeter = new_perimeter1 + new_perimeter2
            mid_tree._node2, bottom_tree._node1 = bottom_tree._node1, mid_tree._node2
            bottom_tree._node1.set_parent(bottom_tree)
            mid_tree._node2.set_parent(mid_tree)

        new_perimeter1 = self.perimeter(self.get_nodes_rect(bottom_tree._node1, mid_tree._node2))
        new_perimeter2 = self.perimeter(self.get_nodes_rect(bottom_tree._node2, self._node2))
        print(new_perimeter1 + new_perimeter2)
        if mid_tree._node2.layer == bottom_tree._node2.layer and new_perimeter1 + new_perimeter2 < total_perimeter:
            print('wybrano jednak to na górze')
            mid_tree._node2, bottom_tree._node2 = bottom_tree._node2, mid_tree._node2
            bottom_tree._node2.set_parent(bottom_tree)
            mid_tree._node2.set_parent(mid_tree)

        bottom_tree._rect = bottom_tree.get_rect()
        self._node2, mid_tree._node1 = mid_tree._node1, self._node2
        self._node2.set_parent(self)
        bottom_tree.set_parent(mid_tree)
        mid_tree._layer -= 1
        mid_tree.update_rect()

    def get_rect(self) -> pygame.FRect:
        return self.get_nodes_rect(self._node1, self._node2)

    def insert(self, tile: Tile) -> AABBNode | None:
        if not self._node1.leaf and self._node1.rect.contains(tile.rect):
            if new_node := self._node1.insert(tile):
                self._node1 = new_node
                new_node.set_parent(self)

        elif not self._node2.leaf and self._node2.rect.contains(tile.rect):
            if new_node := self._node2.insert(tile):
                self._nodes = new_node
                new_node.set_parent(self)

        else:
            rect1_perimeter = self.perimeter(self.get_nodes_rect(self._node1, tile)) + self.perimeter(self._node2.rect)
            rect2_perimeter = self.perimeter(self.get_nodes_rect(self._node2, tile)) + self.perimeter(self._node1.rect)
            self_perimeter = self.perimeter(self.rect)

            min_perimeter = min(rect1_perimeter, rect2_perimeter, self_perimeter)

            if min_perimeter == self_perimeter:
                return AABBContainer(self, AABBLeaf(tile))

            elif min_perimeter == rect1_perimeter:
                if self._node1.leaf:
                    self.set_node1(AABBContainer(self._node1, AABBLeaf(tile)))
                else:
                    if new_node := self._node1.insert(tile):
                        self.set_node1(new_node)

            elif min_perimeter == rect2_perimeter:
                if self._node2.leaf:
                    self.set_node2(AABBContainer(self._node2, AABBLeaf(tile)))
                else:
                    if new_node := self._node2.insert(tile):
                        self.set_node2(new_node)

        self.update()

    def update(self):
        self.update_direction()
        # print("node1:", self._node1.layer, "node2: ", self._node2.layer)
        self.rebalance()
        self.update_rect()
        self.update_layer()

    def update_rect(self):
        self._rect = self.get_rect()

    def update_layer(self):
        self._layer = max(self._node1.layer, self._node2.layer) + 1

    def update_direction(self):
        if self._node2.layer > self._node1.layer:
            self._node1, self._node2 = self._node2, self._node1

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
