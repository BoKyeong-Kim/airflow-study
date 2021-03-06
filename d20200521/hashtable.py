from typing import Any

# Capacity for internal array
INITIAL_CAPACITY = 50


# Node data structure - essentially a LinkedList node
class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return f"<Node: ({self.key}, {self.value}, next: {self.next != None}>"

    def __repr__(self):
        return str(self)


# Hash table with separate chaining
class HashTable:
    # Initialize hash table
    def __init__(self):
        self.capacity = INITIAL_CAPACITY
        self.size = 0
        self.buckets = [None] * self.capacity

    def hash(self, key: str) -> int:
        """
        Generate a hash for a given key

        :param key: key value
        :return: Index from 0 to self.capacity
        """
        hashsum = 0
        # For each character in the key
        for idx, c in enumerate(key):
            # Add (index + length of key) ^ (current char code)
            hashsum += (idx + len(key)) ** ord(c)
            # Perform modulus to keep hashsum in range [0, self.capacity - 1]
            hashsum = hashsum % self.capacity

        return hashsum

    def insert(self, key: str, value: Any) -> None:
        """Insert a key, value pair to the hashtable"""
        # 1. Increment size
        # 2. Compute index of key
        index = self.hash(key)
        # Go to the node corresponding to the hash
        node = self.buckets[index]
        # 3. If bucket is empty
        if node is None:
            # Create node, add it, return
            self.size += 1
            self.buckets[index] = Node(key, value)
            return

        # 4. Iterate to the end of the linked list at provided index
        prev = node
        while node is not None:
            # Check if node has same key
            if node.key == key:
                node.value = value
                return

            prev = node
            node = node.next
        # Add a new node at the end of the list with provided key/value
        self.size += 1
        prev.next = Node(key, value)

    def find(self, key: str) -> Any:
        """Find a data value based on key"""
        # 1. Compute hash
        index = self.hash(key)
        # 2. Go to the first node in list at bucket
        node = self.buckets[index]
        # 3. Traverse the linked list at this node
        while node is not None and node.key != key:
            node = node.next

        # 4. Now node is the requested key/value pair or None
        if node is None:
            # Not found
            return None
        else:
            # Found - return the data value
            return node.value

    def __setitem__(self, key, value):
        return self.insert(key, value)

    def __getitem__(self, key):
        return self.find(key)

    def remove(self, key: str) -> Any:
        """Remove node stored at key and return value"""
        # 1. Compute hash
        index = self.hash(key)
        node = self.buckets[index]
        prev = None
        # 2. Iterate to the requested node
        while node is not None and node.key != key:
            prev = node
            node = node.next

        # Now, node is either the requested node or none
        if node is None:
            # 3. Key not found
            return None
        else:
            # 4. The key was found
            self.size -= 1
            result = node.value
            # Delete this element in linked list
            if prev is None:
                self.buckets[index] = node.next  # May be None, or the next match
            else:
                prev.next = prev.next.next

            return result
