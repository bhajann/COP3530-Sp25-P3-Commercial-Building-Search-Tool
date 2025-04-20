class HashNode:
    def __init__(self, key, value):
        self.key = key
        self.value = value
#specialized node class

class HashTable:
    #default size is 1000 but when working with such a large dataset. table creates empty lists for each element
    def __init__(self, size=1000):
        self.size = size
        self.table = [[] for i in range(size)]
    #hash function
    def _hash(self, key):
        return hash(key) % self.size
    #inserts each hashed element into the table and uses array buckets (seperate chaining) to resolve collisions
    def insert(self, key, value):
        idx = self._hash(key)
        arrayBucket = self.table[idx]
        #checks if its a duplicate value, if it is it does nothing
        #else it just adds the key, value to the bucket at the hash value in the table
        for i, (k, v) in enumerate(arrayBucket):
            if k == key:
                arrayBucket[i] = (key, value)
                return
        arrayBucket.append((key, value))
    #searches through the array buckets
    def search(self, key):
        idx = self._hash(key)
        arrayBucket = self.table[idx]
        for k, v in arrayBucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._hash(key)
        arrayBucket = self.table[idx]
        for i, (k, v) in enumerate(arrayBucket):
            if k == key:
                del arrayBucket[i]
                return

