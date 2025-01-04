class HashTable:
    def __init__(self, size=40):
        self.size = size
        self.table = [[] for not_used in range(self.size)]
    
    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                item[1] == value
                return
        self.table[hash_key].append([key, value])

    def lookup(self, key):
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                return item[1]
        return None

    def __str__(self):
        return str(self.table)
