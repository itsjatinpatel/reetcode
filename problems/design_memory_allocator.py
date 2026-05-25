"""
https://leetcode.com/problems/design-memory-allocator/description/

You are given an integer n representing the size of a 0-indexed memory array. All memory units are initially free.

You have a memory allocator with the following functionalities:

Allocate a block of size consecutive free memory units and assign it the id mID.
Free all memory units with the given id mID.
Note that:

Multiple blocks can be allocated to the same mID.
You should free all the memory units with mID, even if they were allocated in different blocks.
Implement the Allocator class:

Allocator(int n) Initializes an Allocator object with a memory array of size n.
int allocate(int size, int mID) Find the leftmost block of size consecutive free memory units and allocate it with the id mID. Return the block's first index. If such a block does not exist, return -1.
int freeMemory(int mID) Free all memory units with the id mID. Return the number of memory units you have freed.


Example 1:

Input
["Allocator", "allocate", "allocate", "allocate", "freeMemory", "allocate", "allocate", "allocate", "freeMemory", "allocate", "freeMemory"]
[[10], [1, 1], [1, 2], [1, 3], [2], [3, 4], [1, 1], [1, 1], [1], [10, 2], [7]]
Output
[null, 0, 1, 2, 1, 3, 1, 6, 3, -1, 0]

Explanation
Allocator loc = new Allocator(10); // Initialize a memory array of size 10. All memory units are initially free.
loc.allocate(1, 1); // The leftmost block's first index is 0. The memory array becomes [1,_,_,_,_,_,_,_,_,_]. We return 0.
loc.allocate(1, 2); // The leftmost block's first index is 1. The memory array becomes [1,2,_,_,_,_,_,_,_,_]. We return 1.
loc.allocate(1, 3); // The leftmost block's first index is 2. The memory array becomes [1,2,3,_,_,_,_,_,_,_]. We return 2.
loc.freeMemory(2); // Free all memory units with mID 2. The memory array becomes [1,_, 3,_,_,_,_,_,_,_]. We return 1 since there is only 1 unit with mID 2.
loc.allocate(3, 4); // The leftmost block's first index is 3. The memory array becomes [1,_,3,4,4,4,_,_,_,_]. We return 3.
loc.allocate(1, 1); // The leftmost block's first index is 1. The memory array becomes [1,1,3,4,4,4,_,_,_,_]. We return 1.
loc.allocate(1, 1); // The leftmost block's first index is 6. The memory array becomes [1,1,3,4,4,4,1,_,_,_]. We return 6.
loc.freeMemory(1); // Free all memory units with mID 1. The memory array becomes [_,_,3,4,4,4,_,_,_,_]. We return 3 since there are 3 units with mID 1.
loc.allocate(10, 2); // We can not find any free block with 10 consecutive free memory units, so we return -1.
loc.freeMemory(7); // Free all memory units with mID 7. The memory array remains the same since there is no memory unit with mID 7. We return 0.


Constraints:

1 <= n, size, mID <= 1000
At most 1000 calls will be made to allocate and freeMemory.
"""

# from collections import defaultdict


# class Allocator:
#     def __init__(self, n: int):
#         self._memory = [0] * n
#         self._allocations: dict[int, list] = defaultdict(list)

#     def _find_free_block(self, size: int) -> int:
#         block_start = 0
#         free_units = 0

#         for index, mID in enumerate(self._memory):
#             if mID == 0:
#                 if free_units == 0:
#                     block_start = index
#                 free_units += 1
#                 if free_units == size:
#                     return block_start
#             else:
#                 free_units = 0
#         return -1

#     def allocate(self, size: int, mID: int) -> int:
#         idx = self._find_free_block(size)
#         if idx == -1:
#             return -1

#         self._memory[idx : idx + size] = [mID] * size
#         self._allocations[mID].append((idx, size))
#         return idx

#     def freeMemory(self, mID: int) -> int:
#         freed_units = 0
#         for idx, size in self._allocations[mID]:
#             freed_units += size
#             self._memory[idx : idx + size] = [0] * size

#         del self._allocations[mID]
#         return freed_units

from __future__ import annotations

from collections import defaultdict


class _DLLNode:
    __slots__ = ("key", "value", "next", "prev")

    def __init__(self, key: int, value: int):
        self.key = key  # start index
        self.value = value  # block size
        self.next: _DLLNode | None = None
        self.prev: _DLLNode | None = None


class Allocator:
    def __init__(self, n: int):
        self._allocated: dict[int, list] = defaultdict(list)
        self._dummy_head = _DLLNode(-1, 0)

        initital_block = _DLLNode(0, n)
        self._dummy_head.next = initital_block
        initital_block.prev = self._dummy_head

    def _find_free_block(self, size: int) -> _DLLNode | None:
        block = self._dummy_head.next

        while block is not None:
            if block.value >= size:
                return block

            block = block.next

        return None

    def _allocate_block(self, block: _DLLNode, size: int) -> int:
        idx = block.key

        if block.value == size:
            self._del_block(block)
        else:
            block.key += size
            block.value -= size

        return idx

    def _deallocate_block(self, index: int, size: int) -> None:
        prev_block = self._dummy_head
        next_block = self._dummy_head.next

        while next_block is not None and next_block.key < index:
            prev_block = next_block
            next_block = next_block.next

        block = _DLLNode(index, size)
        self._insert_after(prev_block, block)

        self._merge_with_next(block)

        if prev_block is not self._dummy_head:
            self._merge_with_next(prev_block)

    def _insert_after(self, prev_block: _DLLNode, block: _DLLNode) -> None:
        next_block = prev_block.next

        block.prev = prev_block
        block.next = next_block
        prev_block.next = block

        if next_block is not None:
            next_block.prev = block

    def _del_block(self, block: _DLLNode) -> None:
        prev_block = block.prev
        next_block = block.next

        assert prev_block is not None

        prev_block.next = next_block

        if next_block is not None:
            next_block.prev = prev_block

    def _merge_with_next(self, block: _DLLNode) -> None:
        next_block = block.next

        if next_block is not None and block.key + block.value == next_block.key:
            block.value += next_block.value
            self._del_block(next_block)

    def allocate(self, size: int, mID: int) -> int:
        block = self._find_free_block(size)

        if block is None:
            return -1

        idx = self._allocate_block(block, size)
        self._allocated[mID].append((idx, size))
        return idx

    def freeMemory(self, mID: int) -> int:
        freed_units = 0

        for idx, size in self._allocated.pop(mID, []):
            self._deallocate_block(idx, size)
            freed_units += size

        return freed_units


# Your Allocator object will be instantiated and called as such:
# obj = Allocator(n)
# param_1 = obj.allocate(size,mID)
# param_2 = obj.freeMemory(mID)
