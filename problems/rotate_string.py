"""
https://leetcode.com/problems/rotate-string/description/

Given two strings s and goal, return true if and only if s can become goal after some number of shifts on s.

A shift on s consists of moving the leftmost character of s to the rightmost position.

For example, if s = "abcde", then it will be "bcdea" after one shift.


Example 1:

Input: s = "abcde", goal = "cdeab"
Output: true
Example 2:

Input: s = "abcde", goal = "abced"
Output: false


Constraints:

1 <= s.length, goal.length <= 100
s and goal consist of lowercase English letters.
"""


class Solution:
    def rotateString(self, s: str, goal: str) -> bool:
        if len(s) != len(goal):
            return False
        s = s + s

        return self._kmpSearch(goal, s)

    def _constructLps(self, pattern: str, lps: list[int]) -> None:
        len_ = 0
        m = len(lps)

        lps[0] = 0

        mp = 1
        while mp < m:
            if pattern[mp] == pattern[len_]:
                len_ += 1
                lps[mp] = len_
                mp += 1
            else:
                if len_ != 0:
                    len_ = lps[len_ - 1]
                else:
                    lps[mp] = 0
                    mp += 1

    def _kmpSearch(self, pattern: str, text: str) -> bool:
        n, m, np, mp = len(text), len(pattern), 0, 0

        lps = [0] * m
        self._constructLps(pattern, lps)

        while np < n:
            if text[np] == pattern[mp]:
                np += 1
                mp += 1

                if mp == m:
                    return True
            else:
                if mp != 0:
                    mp = lps[mp - 1]
                else:
                    np += 1
        return False
