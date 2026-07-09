"""
https://leetcode.com/problems/shortest-word-distance-ii/

Design a data structure that will be initialized with a string array, and then it should answer queries of the shortest distance between two different strings from the array.

Implement the WordDistance class:

WordDistance(String[] wordsDict) initializes the object with the strings array wordsDict.
int shortest(String word1, String word2) returns the shortest distance between word1 and word2 in the array wordsDict.


Example 1:

Input
["WordDistance", "shortest", "shortest"]
[[["practice", "makes", "perfect", "coding", "makes"]], ["coding", "practice"], ["makes", "coding"]]
Output
[null, 3, 1]

Explanation
WordDistance wordDistance = new WordDistance(["practice", "makes", "perfect", "coding", "makes"]);
wordDistance.shortest("coding", "practice"); // return 3
wordDistance.shortest("makes", "coding");    // return 1


Constraints:

1 <= wordsDict.length <= 3 * 10^4
1 <= wordsDict[i].length <= 10
wordsDict[i] consists of lowercase English letters.
word1 and word2 are in wordsDict.
word1 != word2
At most 5000 calls will be made to shortest.

"""


from collections import defaultdict


class WordDistance:

    def __init__(self, wordsDict: list[str]):
        self._map = defaultdict(list)
        self._len = len(wordsDict)

        for idx, word in enumerate(wordsDict):
            self._map[word].append(idx)


    def shortest(self, word1: str, word2: str) -> int:
        shortest = self._len
        word1_indices, word2_indices = self._map[word1], self._map[word2]
        p1 = p2 = 0
        while p1 < len(word1_indices) and p2 < len(word2_indices):
            shortest = min(shortest, abs(word1_indices[p1] - word2_indices[p2]))
            if word1_indices[p1] <= word2_indices[p2]:
                p1 += 1
            else:
                p2 += 1
        return shortest
