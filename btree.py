from typing import Tuple, List, Any


class TreeNode:
    def __init__(self, t: int, leaf: bool = True):
        self.t = t  # Minimum degree
        self.leaf = leaf
        self.keys: List[Tuple[Any, Any]] = []
        self.children: List["TreeNode"] = []


class BTree:
    def __init__(self, t: int):
        self.t = t
        self.root = TreeNode(t)

    def traverse(self, node=None):
        if node is None:
            node = self.root
        for i in range(len(node.keys)):
            if not node.leaf:
                self.traverse(node.children[i])
            print(node.keys[i], end=" ")
        if not node.leaf:
            self.traverse(node.children[-1])

    def search(self, k, node=None):
        if node is None:
            node = self.root
        i = 0
        #error here
        while i < len(node.keys) and k > node.keys[i][0]:
            i += 1
        if i < len(node.keys) and node.keys[i][0] == k:
            return node.keys[i][1]
        elif node.leaf:
            return None
        else:
            return self.search(k, node.children[i])

    def insert(self, k, v):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:
            new_root = TreeNode(self.t, leaf=False)
            new_root.children.insert(0, root)
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, k, v)
            self.root = new_root
        else:
            self._insert_non_full(root, k, v)

    def _insert_non_full(self, node: TreeNode, k, v):
        i = len(node.keys) - 1
        if node.leaf:
            node.keys.append((None, None))  # Placeholder
            while i >= 0 and k < node.keys[i][0]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = (k, v)
        else:
            while i >= 0 and k < node.keys[i][0]:
                i -= 1
            i += 1
            if len(node.children[i].keys) == 2 * self.t - 1:
                self._split_child(node, i)
                if k > node.keys[i][0]:
                    i += 1
            self._insert_non_full(node.children[i], k, v)

    def _split_child(self, parent: TreeNode, i: int):
        t = self.t
        full_child = parent.children[i]
        new_child = TreeNode(t, leaf=full_child.leaf)

        parent.children.insert(i + 1, new_child)
        parent.keys.insert(i, full_child.keys[t - 1])

        new_child.keys = full_child.keys[t : (2 * t - 1)]
        full_child.keys = full_child.keys[: t - 1]

        if not full_child.leaf:
            new_child.children = full_child.children[t : (2 * t)]
            full_child.children = full_child.children[:t]
