class HashTable:
    """
    A simple implementation of a hash table using chaining for collision resolution.
    """

    def __init__(self, size=40):
        """
        Initialize the hash table with a given size.

        Args:
            size: The size of the hash table. Defaults to 40.
        """
        self.size = size
        self.table = [[] for not_used in range(self.size)]
    
    def _hash(self, key):
        """
        Generate a hash value for the given key.

        Args:
            key: The key to be hashed.

        Returns:
            The hash value, which is an index in the hash table.
        """
        return hash(key) % self.size

    def insert(self, key, value):
        """
        Insert a key-value pair into the hash table.

        If the key already exists, update its value.

        Args:
            key: The key to be inserted.
            value: The value associated with the key.
        """
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                item[1] == value
                return
        self.table[hash_key].append([key, value])

    def lookup(self, key):
        """
        Look up a value in the hash table by its key.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        hash_key = self._hash(key)
        for item in self.table[hash_key]:
            if item[0] == key:
                return item[1]
        return None

    def __str__(self):
        """
        Return a string representation of the hash table.

        Returns:
            A string representation of the hash table's contents.
        """
        return str(self.table)
