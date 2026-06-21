"""
https://leetcode.com/problems/sort-an-array/

Given an array of integers nums, sort the array in ascending order and return it.

You must solve the problem without using any built-in functions in O(nlog(n)) time complexity and with the smallest space complexity possible.



Example 1:

Input: nums = [5,2,3,1]
Output: [1,2,3,5]
Explanation: After sorting the array, the positions of some numbers are not changed (for example, 2 and 3), while the positions of other numbers are changed (for example, 1 and 5).
Example 2:

Input: nums = [5,1,1,2,0,0]
Output: [0,0,1,1,2,5]
Explanation: Note that the values of nums are not necessarily unique.


Constraints:

1 <= nums.length <= 5 * 10^4
-5 * 10^4 <= nums[i] <= 5 * 10^4
"""


class Solution:
    def sortArray(self, nums: list[int]) -> list[int]:
        n = len(nums)
        if n <= 1:
            return nums

        aux = [0] * n

        width = 1
        while width < n:
            for left in range(0, n, 2 * width):
                mid = min(left + width - 1, n - 1)
                right = min(left + 2 * width - 1, n - 1)

                if mid >= right:
                    continue
                if nums[mid] <= nums[mid + 1]:
                    continue

                self.merge(nums, aux, left, mid, right)
            width *= 2
        return nums

    def merge(
        self, nums: list[int], aux: list[int], left: int, mid: int, right: int
    ) -> None:
        for k in range(left, mid + 1):
            aux[k] = nums[k]

        i = left
        j = mid + 1
        k = left

        while i <= mid and j <= right:
            if aux[i] <= nums[j]:
                nums[k] = aux[i]
                i += 1
            else:
                nums[k] = nums[j]
                j += 1
            k += 1

        while i <= mid:
            nums[k] = aux[i]
            i += 1
            k += 1
