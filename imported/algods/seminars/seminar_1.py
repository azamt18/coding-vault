"""
A Hash Map (key_to_node):
Maps each key to its corresponding bucket node in a doubly linked list.

A Doubly Linked List (DLL) of Buckets:
Each bucket (or node) contains a frequency count and a set of keys with that count. The list is sorted by frequency in ascending order.
"""
from distutils.core import setup_keywords
from itertools import count


class Node:
    def __init__(self, count):
        self.count = count
        self.keys = set()
        self.prev = None
        self.next = None


class AllOne:

    def __init__(self):
        self.hash_map = {}

        self.dummy_head = Node(0)
        self.dummy_tail = Node(0)
        self.dummy_head.next = self.dummy_tail
        self.dummy_tail.prev = self.dummy_head

    def _insert_node_after(self, new_node, prev_node):
        new_node.prev = prev_node
        new_node.next = prev_node.next
        prev_node.next.prev = new_node
        prev_node.next = new_node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def inc(self, key: str) -> None:
        if key not in self.hash_map:
            # when key is new
            if self.dummy_head.next.count != 1:
                node = Node(1)
                self._insert_node_after(node, self.dummy_head)

            self.dummy_head.next.keys.add(key)
            self.hash_map[key] = self.dummy_head.next

        else:
            # when key exists
            current_bucket = self.hash_map[key]
            next_count = current_bucket.count + 1

            # remove key from current node
            current_bucket.keys.remove(key)

            # insert key into next bucket
            if current_bucket.next.count != next_count:
                node = Node(next_count)
                self._insert_node_after(node, current_bucket)

            current_bucket.next.keys.add(key)
            self.hash_map[key] = current_bucket.next

            # remove current bucket if it becomes empty
            if len(current_bucket.keys) == 0:
                self._remove_node(current_bucket)

    def dec(self, key: str) -> None:
        if key not in self.hash_map:
            return

        current_bucket = self.hash_map[key]
        if current_bucket.count == 1:
            # remove key completely if it becomes 0
            del self.hash_map[key]
            current_bucket.keys.discard(key)
        else:
            prev_count = current_bucket.count - 1
            current_bucket.keys.discard(key)

            # insert key into previous bucket
            if current_bucket.prev.count != prev_count:
                new_node = Node(prev_count)
                self._insert_node_after(new_node, current_bucket.prev)

            current_bucket.prev.keys.add(key)
            self.hash_map[key] = current_bucket.prev

        # remove current bucket if empty
        if len(current_bucket.keys) == 0:
            self._remove_node(current_bucket)

    def getMaxKey(self) -> str:
        if self.dummy_tail.prev == self.dummy_head:
            return ""

        max_bucket = self.dummy_tail.prev
        if not max_bucket.keys:
            return ""

        return next(iter(max_bucket.keys))

    def getMinKey(self) -> str:
        if self.dummy_head.next == self.dummy_tail:
            return ""

        min_bucket = self.dummy_head.next
        if not min_bucket.keys:
            return ""

        return next(iter(min_bucket.keys))


# Your AllOne object will be instantiated and called as such:
# obj = AllOne()
# obj.inc(key)
# obj.dec(key)
# param_3 = obj.getMaxKey()
# param_4 = obj.getMinKey()

allOne = AllOne()
allOne.inc("hello")
allOne.inc("hello")
allOne.getMaxKey() # return "hello"
allOne.getMinKey() # return "hello"
allOne.inc("leet")
allOne.getMaxKey() # return "hello"
allOne.getMinKey() # return "leet"