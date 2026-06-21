"""
https://leetcode.com/problems/reverse-pairs/

Given an integer array nums, return the number of reverse pairs in the array.

A reverse pair is a pair (i, j) where:

0 <= i < j < nums.length and
nums[i] > 2 * nums[j].


Example 1:

Input: nums = [1,3,2,3,1]
Output: 2
Explanation: The reverse pairs are:
(1, 4) --> nums[1] = 3, nums[4] = 1, 3 > 2 * 1
(3, 4) --> nums[3] = 3, nums[4] = 1, 3 > 2 * 1
Example 2:

Input: nums = [2,4,3,5,1]
Output: 3
Explanation: The reverse pairs are:
(1, 4) --> nums[1] = 4, nums[4] = 1, 4 > 2 * 1
(2, 4) --> nums[2] = 3, nums[4] = 1, 3 > 2 * 1
(3, 4) --> nums[3] = 5, nums[4] = 1, 5 > 2 * 1


Constraints:

1 <= nums.length <= 5 * 10^4
-2^31 <= nums[i] <= 23^1 - 1
"""


class Solution:
    def reversePairs(self, nums: list[int]) -> int:
        def merge_and_count(low: int, high: int) -> int:
            if high - low <= 1:
                return 0

            mid = (low + high) // 2
            count = merge_and_count(low, mid) + merge_and_count(mid, high)

            j = mid
            for i in range(low, mid):
                while j < high and nums[i] > 2 * nums[j]:
                    j += 1
                count += j - mid
            nums[low:high] = sorted(nums[low:high])
            return count

        return merge_and_count(0, len(nums))
