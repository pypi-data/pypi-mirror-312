# -*- coding: utf-8 -*-

from queue import Queue
from typing import List


class BinaryTree:
    """
    In computer science, a binary tree is a tree data structure in which
    each node has at most two children, which are referred to as the
    left child and the right child...
    """

    def __init__(self, value):
        self.value = value
        self.right = None
        self.left = None

    @staticmethod
    def create_example_tree():
        root = BinaryTree(1)
        tree_node2, tree_node3 = BinaryTree(2), BinaryTree(3)
        tree_node4, tree_node5 = BinaryTree(4), BinaryTree(5)
        tree_node6, tree_node7 = BinaryTree(6), BinaryTree(7)
        tree_node8, tree_node9 = BinaryTree(8), BinaryTree(9)
        tree_node10, tree_node11 = BinaryTree(10), BinaryTree(11)
        tree_node12, tree_node13 = BinaryTree(12), BinaryTree(13)
        tree_node14, tree_node15 = BinaryTree(14), BinaryTree(15)

        root.left, root.right = tree_node2, tree_node3
        tree_node2.left, tree_node2.right = tree_node4, tree_node5
        tree_node3.left, tree_node3.right = tree_node6, tree_node7
        tree_node4.left, tree_node4.right = tree_node8, tree_node9
        tree_node5.left, tree_node5.right = tree_node10, tree_node11
        tree_node6.left, tree_node6.right = tree_node12, tree_node13
        tree_node7.left, tree_node7.right = tree_node14, tree_node15
        return root

    def pre_order(self) -> List:
        """
        >>> root = BinaryTree.create_example_tree()
        >>> root.pre_order()
        [1, 2, 4, 8, 9, 5, 10, 11, 3, 6, 12, 13, 7, 14, 15]
        """

        res = [self.value]
        if self.left:
            res.extend(self.left.pre_order())

        if self.right:
            res.extend(self.right.pre_order())

        return res

    def pre_order_iterative(self) -> List:
        """
        >>> root = BinaryTree.create_example_tree()
        >>> root.pre_order_iterative()
        [1, 2, 4, 8, 9, 5, 10, 11, 3, 6, 12, 13, 7, 14, 15]
        """

        stack: List[BinaryTree] = []
        node, res = self, []

        while stack or node:
            while node:
                res.append(node.value)
                stack.append(node)
                node = node.left

            node = stack.pop()
            node = node.right

        return res

    def in_order(self) -> List:
        """
        >>> root = BinaryTree.create_example_tree()
        >>> root.in_order()
        [8, 4, 9, 2, 10, 5, 11, 1, 12, 6, 13, 3, 14, 7, 15]
        """

        res = []
        if self.left:
            res.extend(self.left.in_order())

        res.append(self.value)

        if self.right:
            res.extend(self.right.in_order())

        return res

    def in_order_iterative(self) -> List:
        """
        >>> root = BinaryTree.create_example_tree()
        >>> root.in_order_iterative()
        [8, 4, 9, 2, 10, 5, 11, 1, 12, 6, 13, 3, 14, 7, 15]
        """

        res = []
        stack: List[BinaryTree] = []
        node = self

        while stack or node:
            while node:
                stack.append(node)
                node = node.left

            node = stack.pop()
            res.append(node.value)
            node = node.right

        return res

    def post_order(self) -> List:
        """
        >>> root = BinaryTree.create_example_tree()
        >>> root.post_order()
        [8, 9, 4, 10, 11, 5, 2, 12, 13, 6, 14, 15, 7, 3, 1]
        """

        res = []
        if self.left:
            res.extend(self.left.post_order())

        if self.right:
            res.extend(self.right.post_order())

        res.append(self.value)
        return res

    def post_order_iterative(self) -> List:
        """
        >>> root = BinaryTree.create_example_tree()
        >>> root.post_order_iterative()
        [8, 9, 4, 10, 11, 5, 2, 12, 13, 6, 14, 15, 7, 3, 1]
        """

        stack: List[BinaryTree] = [self]
        stack_tmp: List[BinaryTree] = []

        while stack:
            node = stack.pop()
            if node.left:
                stack.append(node.left)

            if node.right:
                stack.append(node.right)

            stack_tmp.append(node)

        res = []
        while stack_tmp:
            res.append(stack_tmp.pop().value)

        return res

    def level_order(self) -> List:
        """
        >>> root = BinaryTree.create_example_tree()
        >>> root.level_order()
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
        """

        res = []
        q = Queue()
        q.put(self)

        while not q.empty():
            node_dequeued = q.get()
            res.append(node_dequeued.value)

            if node_dequeued.left:
                q.put(node_dequeued.left)

            if node_dequeued.right:
                q.put(node_dequeued.right)

        return res

    # def level_order_iterative(self) -> List:
    #     """
    #     >>> root = BinaryTree.create_example_tree()
    #     >>> root.post_order_iterative()
    #     [8, 9, 4, 10, 11, 5, 2, 12, 13, 6, 14, 15, 7, 3, 1]
    #     """
    #
    #     stack: List[BinaryTree] = []
    #     node, res = self, []
    #
    #     while stack or node:
    #         while node.left:
    #             stack.append(node)
    #             node = node.left
    #
    #         res.append(node.value)
    #         node = stack.pop()
    #         node = node.right
    #
    #     return res

    def depth(self):
        """
        The maximum depth of a binary tree is the number of nodes from the
        root down to the furthest leaf node. In other words, it is
        the height of a binary tree.

        >>> root = BinaryTree.create_example_tree()
        >>> root.depth()
        4
        """

        if not self.left and not self.right:
            return 1

        depth_left = 0
        if self.left:
            depth_left = self.left.depth()

        depth_right = 0
        if self.right:
            depth_right = self.right.depth()

        return 1 + max(depth_left, depth_right)
