"""
https://leetcode.com/problems/lru-cache/description/

Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.

Implement the LRUCache class:

LRUCache(int capacity) Initialize the LRU cache with positive size capacity.
int get(int key) Return the value of the key if the key exists, otherwise return -1.
void put(int key, int value) Update the value of the key if the key exists. Otherwise, add the key-value pair to the cache. If the number of keys exceeds the capacity from this operation, evict the least recently used key.
The functions get and put must each run in O(1) average time complexity.



Example 1:

Input
["LRUCache", "put", "put", "get", "put", "get", "put", "get", "get", "get"]
[[2], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [1], [3], [4]]
Output
[null, null, null, 1, null, -1, null, -1, 3, 4]

Explanation
LRUCache lRUCache = new LRUCache(2);
lRUCache.put(1, 1); // cache is {1=1}
lRUCache.put(2, 2); // cache is {1=1, 2=2}
lRUCache.get(1);    // return 1
lRUCache.put(3, 3); // LRU key was 2, evicts key 2, cache is {1=1, 3=3}
lRUCache.get(2);    // returns -1 (not found)
lRUCache.put(4, 4); // LRU key was 1, evicts key 1, cache is {4=4, 3=3}
lRUCache.get(1);    // return -1 (not found)
lRUCache.get(3);    // return 3
lRUCache.get(4);    // return 4


Constraints:

1 <= capacity <= 3000
0 <= key <= 104
0 <= value <= 105
At most 2 * 105 calls will be made to get and put.
"""

from __future__ import annotations


class _DLLNode:
    __slots__ = ("key", "value", "next", "prev")

    def __init__(self, key: int, value: int):
        self.key = key
        self.value = value
        self.prev: _DLLNode | None = None
        self.next: _DLLNode | None = None


class LRUCache:
    __slots__ = ("capacity", "_cache", "_head", "_tail")

    def __init__(self, capacity: int):
        self.capacity = capacity
        self._cache: dict[int, _DLLNode] = {}

        self._head = _DLLNode(-1, -1)  # least recently used side
        self._tail = _DLLNode(-1, -1)  # most recently used side
        self._head.next = self._tail
        self._tail.prev = self._head

    def _remove(self, node: _DLLNode) -> None:
        prev_node = node.prev
        next_node = node.next

        assert prev_node is not None
        assert next_node is not None

        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_mru(self, node: _DLLNode) -> None:
        prev_mru = self._tail.prev
        assert prev_mru is not None

        node.prev = prev_mru
        node.next = self._tail
        prev_mru.next = node
        self._tail.prev = node

    def _move_to_mru(self, node: _DLLNode) -> None:
        self._remove(node)
        self._add_to_mru(node)

    def _evict_lru(self) -> None:
        lru = self._head.next
        assert lru is not None

        self._remove(lru)
        del self._cache[lru.key]

    def get(self, key: int) -> int:
        node = self._cache.get(key)
        if node is None:
            return -1

        self._move_to_mru(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        node = self._cache.get(key)

        if node is not None:
            node.value = value
            self._move_to_mru(node)
            return

        node = _DLLNode(key, value)
        self._cache[key] = node
        self._add_to_mru(node)

        if len(self._cache) > self.capacity:
            self._evict_lru()


# Your LRUCache object will be instantiated and called as such:
# obj = LRUCache(capacity)
# param_1 = obj.get(key)
# obj.put(key,value)
