"""
https://leetcode.com/problems/lru-cache/

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
0 <= key <= 10^4
0 <= value <= 10^5
At most 2 * 105 calls will be made to get and put.
"""


class DLLNode:
    __slots__ = ("key", "value", "prev", "next")

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = self
        self.next = self


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity

        self._cache: dict[int, DLLNode] = {}
        self._head = DLLNode()
        self._tail = DLLNode()
        self._head.next, self._tail.prev = self._tail, self._head

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

        node = DLLNode(key, value)
        self._cache[key] = node
        self._add_to_mru(node)

        if len(self._cache) > self.capacity:
            self._evict_lru()

    def _evict_lru(self) -> None:
        node = self._head.next

        self._remove(node)
        del self._cache[node.key]

    def _remove(self, node: DLLNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_to_mru(self, node: DLLNode) -> None:
        prev_mru = self._tail.prev

        node.prev = prev_mru
        node.next = self._tail
        prev_mru.next = node
        self._tail.prev = node

    def _move_to_mru(self, node: DLLNode) -> None:
        self._remove(node)
        self._add_to_mru(node)
