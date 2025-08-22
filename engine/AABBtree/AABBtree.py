import pygame
from abc import ABC, abstractmethod
from engine.base_tile.modules.Position2DModule import RectType
from typing import Protocol
from engine.base_tile.modules.basic_modules import Context


class AABBModule(Protocol):
    def get_hitbox(self, rect_type: RectType) -> pygame.FRect: ...


class AABBNode(ABC):
    def __init__(self, head, leaf, layer, rect):
        self._head_node: AABBTreeHead = head
        self._leaf: bool = leaf
        self._layer: int = layer
        self._parent: AABBContainer | None = None
        self._rect: pygame.FRect = rect

    @property
    def head_node(self):
        return self._head_node

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

    def remove(self):
        if not self.parent:
            self._head_node.change_node(None)
        else:
            if self._parent.node1 is self:
                self._parent.remove_node1()
            else:
                self._parent.remove_node2()

    @staticmethod
    def get_nodes_rect(node1, node2) -> pygame.FRect:
        return node1.rect.union(node2.rect)

    @staticmethod
    def area(rect: pygame.FRect) -> int:
        return rect.width * rect.height

    @abstractmethod
    def get_rect(self) -> pygame.FRect: ...

    @abstractmethod
    def AABBcollision(self, rect: pygame.FRect, result: list) -> None: ...

    @abstractmethod
    def return_all(self, result: list) -> None: ...

    @abstractmethod
    def collidepoint(self, point: tuple, result: list) -> None: ...

# ----------------------------------------------------------------------


class AABBTreeHead:
    def __init__(self, rect_type: RectType):
        self._node: AABBLeaf | AABBContainer | None = None
        self._rect_type = rect_type

    def instert(self, node: AABBNode) -> None:
        if self._node is None:
            self.change_node(node)
        elif self._node.leaf:
            self.change_node(AABBContainer(self, self._node, node))
        else:
            Insertion.reset()
            self._node.insert(node)
            Insertion.add_new_node(node)

    @property
    def node(self):
        return self._node

    @property
    def rect_type(self):
        return self._rect_type

    def change_node(self, node: AABBNode):
        self._node = node
        node and node.set_parent(None)

    def rebalance(self):
        if node := Insertion.node_min:
            node.parent.rebalance()

    def print(self, display):
        if self._node is not None:
            self._node.print(display)

# ----------------------------------------------------------------------


class AABBLeaf(AABBNode):
    def __init__(self, head: AABBTreeHead, tile: AABBModule):
        self._tile = tile
        rect = tile.get_hitbox(head.rect_type)
        super().__init__(head, True, 0, rect)

    def reinsert(self):
        self.remove()
        self._head_node.instert(self)

    def get_rect(self) -> pygame.FRect:
        return self._tile.get_hitbox(self._head_node.rect_type)

    def return_all(self, result: list) -> None:
        result.append(self._tile.context)

    def insert(self, node: AABBNode) -> AABBNode | None:
        sum_area = self.area(self.get_nodes_rect(self, node))

        cost = sum_area + self.parent.delta_sum
        Insertion.update_cost(cost, self)

    def AABBcollision(self, rect: pygame.FRect, result: list) -> None:
        if self.rect.colliderect(rect):
            result.append(self._tile.context)

    def print(self, display: pygame.Surface) -> None:
        pygame.draw.rect(display, 'blue', self._rect, 2)

    def collidepoint(self, point: tuple, result: list):
        if self.rect.collidepoint(point):
            result.append(self._tile)

# ----------------------------------------------------------------------


class AABBContainer(AABBNode):
    def __init__(self, head: AABBTreeHead, node1: AABBNode, node2: AABBNode):
        self._delta_sum: int = 0
        self._node1: AABBLeaf | AABBContainer = node1
        self._node2: AABBLeaf | AABBContainer = node2

        self._node1.set_parent(self)
        self._node2.set_parent(self)

        new_layer = max(self._node1.layer, self._node2.layer) + 1
        super().__init__(head, False, new_layer, self.get_rect())

    @property
    def delta_sum(self):
        return self._delta_sum

    @property
    def node1(self):
        return self._node1

    @property
    def node2(self):
        return self._node2

    def set_node1(self, node: AABBNode):
        self._node1 = node
        self._node1.set_parent(self)
        self.update()

    def set_node2(self, node: AABBNode):
        self._node2 = node
        self._node2.set_parent(self)
        self.update()

    def remove_node1(self):
        self._remove_node_partner(self._node2)

    def remove_node2(self):
        self._remove_node_partner(self._node1)

    def _remove_node_partner(self, node: AABBNode):
        if not self.parent:
            self._head_node.change_node(node)
        else:
            if self._parent.node1 is self:
                self._parent.set_node1(node)
            else:
                self._parent.set_node2(node)

    def rebalance(self):
        if self._node1.layer - self._node2.layer > 1:

            node1 = self._node1.node1
            node2 = self._node1.node2

            self.remove_node1()

            self._head_node.instert(node2)
            self._head_node.instert(node1)

        self._parent and self._parent.rebalance()

    def get_rect(self) -> pygame.FRect:
        return self.get_nodes_rect(self._node1, self._node2)

    def insert(self, node: AABBNode) -> None:
        delta_sum = 0 if not self.parent else self.parent.delta_sum
        sum_area = self.area(self.get_nodes_rect(self, node))
        self._delta_sum = sum_area - self.area(self.rect) + delta_sum

        cost = sum_area + delta_sum
        Insertion.update_cost(cost, self)

        if self.delta_sum + self.area(node.rect) < Insertion.c_min:
            self._node1.insert(node)
            self._node2.insert(node)

    def update(self):
        self.update_direction()
        self.update_rect()
        self.update_layer()

        self._parent and self._parent.update()

    def update_rect(self):
        self._rect = self.get_rect()

    def update_layer(self):
        self._layer = self._node1.layer + 1

    def update_direction(self):
        if self._node2.layer > self._node1.layer:
            self._node1, self._node2 = self._node2, self._node1

    def AABBcollision(self, rect: pygame.FRect, result: list) -> None:
        if rect.contains(self.rect):
            self.return_all(result)
        elif self.rect.colliderect(rect):
            self._node1.AABBcollision(rect, result)
            self._node2.AABBcollision(rect, result)

    def return_all(self, result: list):
        self._node1.return_all(result)
        self._node2.return_all(result)

    def collidepoint(self, point: tuple, result: list) -> None:
        if self.rect.collidepoint(point):
            self._node1.collidepoint(point, result)
            self._node2.collidepoint(point, result)

    def print(self, display: pygame.Surface) -> None:
        color = min(self._layer * 20, 255)
        pygame.draw.rect(display, (color, color, color), self._rect, 1)
        self._node1.print(display)
        self._node2.print(display)

# ----------------------------------------------------------------------


class Insertion:
    c_min: int | None = None
    node_min: AABBNode | None = None

    @classmethod
    def reset(cls):
        cls.c_min = None
        cls.node_min = None

    @classmethod
    def update_cost(cls, cost, node):
        if cls.c_min is None or cls.c_min > cost:
            cls.c_min = cost
            cls.node_min = node

    @classmethod
    def add_new_node(cls, node: AABBNode):
        partner: AABBNode = cls.node_min
        parent: AABBContainer = partner.parent
        head = partner.head_node
        new_container = AABBContainer(head, partner, node)

        if not parent:
            head.change_node(new_container)
        else:
            if parent.node1 is partner:
                parent.set_node1(new_container)
            else:
                parent.set_node2(new_container)

# ----------------------------------------------------------------------


class AABBTree:
    def __init__(self, rect_type: RectType):
        self._head: AABBTreeHead = AABBTreeHead(rect_type)
        self._rect_type = rect_type

    def insert(self, tile) -> AABBLeaf:
        node = AABBLeaf(self._head, tile)
        self._head.instert(node)
        self._head.rebalance()
        return node

    def RectCollision(self, rect: pygame.FRect) -> list[Context]:
        result = []
        if node := self._head.node:
            node.AABBcollision(rect, result)
        return result

    def AABBCollision(self, tile: AABBModule) -> list[Context]:
        return self.RectCollision(tile.get_hitbox(self._rect_type))

    def update(self, dt: int, rect: pygame.FRect, *args):
        for tile in self.RectCollision(rect):
            tile.update(dt, *args)

    def print(self, display: pygame.Surface):
        self._head.print(display)
