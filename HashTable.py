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
        self.table = [[] for _ in range(self.size)]

    def __str__(self):
        """
        Return a string representation of the hash table.

        Returns:
            A string representation of the hash table's contents.
        """
        return str(self.table)

    
    def _hash(self, key):
        """
        Generate a hash value for the given key.

        Args:
            key: The key to be hashed.

        Returns:
            The hash value, which is an index in the hash table.
        """
        return hash(key) % self.size

    def insert(self, pkg):
        """
        Insert a key-value pair into the hash table.

        If the key already exists, update its value.

        Args:
            key: The key to be inserted.
            value: The value associated with the key.
        """
        hash_key = self._hash(pkg.id)
        for item in self.table[hash_key]:
            if item[0] == pkg.id:
                item[1] == pkg
                return
        self.table[hash_key].append([pkg.id, pkg])

    def lookup(self, pkgID):
        """
        Look up a value in the hash table by its key.

        Args:
            key: The key to look up.

        Returns:
            The value associated with the key, or None if the key is not found.
        """
        hash_key = self._hash(pkgID)
        for item in self.table[hash_key]:
            if item[0] == pkgID:
                return item[1]
        return None
