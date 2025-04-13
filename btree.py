from typing import Self
from typing import Tuple

class TreeNode:
    def __init__(self, keys: list[Tuple[any, int]], children: list[Self], leaf: bool):
        self.keys = []
        self.children = []
        self.leaf = False


class BTree:
    def __init__(self, n: int):
        self.n = n
        self.root = TreeNode(keys=[], children=[], leaf=True)
    
    def split_child(self, node: TreeNode, key_pos: int):
        split_key = node.children[key_pos]

    
    def insert_non_full(self):
        x = 1
    
    def traverse(self):
        x = 1
    
    def search(self, key: any, node: TreeNode=None) -> Tuple[any, int]:
        if node is None:
            return search(self, key, self.root)

        for i in range(len(node.keys)):
            if(node.keys[i] == key):
                return key
            elif(node.keys[i] > key):
                None
    
    def get_predecessor(self):
        x = 1

    def get_successor(self):
        x = 1

    def fill(self):
        x = 1

    def borrow_from_prev(self):
        x = 1

    def borrow_from_next(self):
        x = 1
    
