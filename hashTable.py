class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    def __init__(self, size=1000):
        self.size = size
        self.table = [None] * size

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        idx = self._hash(key)
        head = self.table[idx]

        while head:
            if head.key == key:
                head.value = value
                return
            head = head.next

        new_node = HashNode(key, value)
        new_node.next = self.table[idx]
        self.table[idx] = new_node

    def search(self, key):
        idx = self._hash(key)
        head = self.table[idx]

        while head:
            if head.key == key:
                return head.value
            head = head.next
        return None

    def delete(self, key):
        idx = self._hash(key)
        head = self.table[idx]
        prev = None

        while head:
            if head.key == key:
                if prev:
                    prev.next = head.next
                else:
                    self.table[idx] = head.next
                return
            prev, head = head, head.next
