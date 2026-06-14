"""
https://leetcode.com/problems/repeated-string-match/description/

Given two strings a and b, return the minimum number of times you should repeat string a so that string b is a substring of it. If it is impossible for b​​​​​​ to be a substring of a after repeating it, return -1.

Notice: string "abc" repeated 0 times is "", repeated 1 time is "abc" and repeated 2 times is "abcabc".



Example 1:

Input: a = "abcd", b = "cdabcdab"
Output: 3
Explanation: We return 3 because by repeating a three times "abcdabcdabcd", b is a substring of it.
Example 2:

Input: a = "a", b = "aa"
Output: 2


Constraints:

1 <= a.length, b.length <= 104
a and b consist of lowercase English letters.
"""

import math


class Solution:
    def repeatedStringMatch(self, a: str, b: str) -> int:
        k = math.ceil(len(b) / len(a))
        text1, text2 = a * k, a * (k + 1)

        return (
            k
            if self._kmpSearch(b, text1)
            else (k + 1)
            if self._kmpSearch(b, text2)
            else -1
        )

    def _constructLps(self, pattern: str, lps: list[int]) -> None:
        len_ = 0
        mp = 1
        m = len(pattern)

        lps[0] = 0

        while mp < m:
            if pattern[mp] == pattern[len_]:
                len_ += 1
                lps[mp] = len_
                mp += 1
            else:
                if len_ > 0:
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
                if mp > 0:
                    mp = lps[mp - 1]
                else:
                    np += 1
        return False
