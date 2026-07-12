"""
https://leetcode.com/problems/design-search-autocomplete-system/

Design a search autocomplete system for a search engine. Users may input a sentence (at least one word and end with a special character '#').

You are given a string array sentences and an integer array times both of length n where sentences[i] is a previously typed sentence and times[i] is the corresponding number of times the sentence was typed.
For each input character except '#', return the top 3 historical hot sentences that have the same prefix as the part of the sentence already typed.

Here are the specific rules:

The hot degree for a sentence is defined as the number of times a user typed the exactly same sentence before.
The returned top 3 hot sentences should be sorted by hot degree (The first is the hottest one). If several sentences have the same hot degree, use ASCII-code order (smaller one appears first).
If less than 3 hot sentences exist, return as many as you can.
When the input is a special character, it means the sentence ends, and in this case, you need to return an empty list.

Implement the AutocompleteSystem class:

AutocompleteSystem(String[] sentences, int[] times) Initializes the object with the sentences and times arrays.
List<String> input(char c) This indicates that the user typed the character c.
Returns an empty array [] if c == '#' and stores the inputted sentence in the system.
Returns the top 3 historical hot sentences that have the same prefix as the part of the sentence already typed. If there are fewer than 3 matches, return them all.


Example 1:

Input
["AutocompleteSystem", "input", "input", "input", "input"]
[[["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]], ["i"], [" "], ["a"], ["#"]]
Output
[null, ["i love you", "island", "i love leetcode"], ["i love you", "i love leetcode"], [], []]

Explanation
AutocompleteSystem obj = new AutocompleteSystem(["i love you", "island", "iroman", "i love leetcode"], [5, 3, 2, 2]);
obj.input("i"); // return ["i love you", "island", "i love leetcode"]. There are four sentences that have prefix "i". Among them, "ironman" and "i love leetcode" have same hot degree. Since ' ' has ASCII code 32 and 'r' has ASCII code 114, "i love leetcode" should be in front of "ironman".
Also we only need to output top 3 hot sentences, so "ironman" will be ignored.
obj.input(" "); // return ["i love you", "i love leetcode"]. There are only two sentences that have prefix "i ".
obj.input("a"); // return []. There are no sentences that have prefix "i a".
obj.input("#"); // return []. The user finished the input, the sentence "i a" should be saved as a historical sentence in system. And the following input will be counted as a new search.


Constraints:

n == sentences.length
n == times.length
1 <= n <= 100
1 <= sentences[i].length <= 100
1 <= times[i] <= 50
c is a lowercase English letter, a hash '#', or space ' '.
Each tested sentence will be a sequence of characters c that end with the character '#'.
Each tested sentence will have a length in the range [1, 200].
The words in each input sentence are separated by single spaces.
At most 5000 calls will be made to input.
"""



from collections import defaultdict


class _TrieNode:
    __slots__ = ('children', 'top_k')

    def __init__(self):
        self.children = {}
        self.top_k = []


class AutocompleteSystem:

    def __init__(self, sentences: list[str], times: list[int]):
        self._root = _TrieNode()
        self._hot_degree = defaultdict(int)
        self._curr_sentence = []
        self._curr_node = self._root

        for sentence, count in zip(sentences, times):
            self._insert(sentence, count)


    def input(self, ch: str) -> list[str]:
        if ch == '#':
            self._insert(''.join(self._curr_sentence))
            self._curr_sentence = []
            self._curr_node = self._root
            return []

        self._curr_sentence.append(ch)
        if self._curr_node is None or ch not in self._curr_node.children:
            self._curr_node = None
            return []
        
        self._curr_node = self._curr_node.children[ch]
        return self._curr_node.top_k


    def _insert(self, word: str, count: int = 1) -> None:
        self._hot_degree[word] += count
        node = self._root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = _TrieNode()
            node = node.children[ch]
            self._update_top_k(word, node)


    def _update_top_k(self, word: str, node: _TrieNode) -> None:
        if word not in node.top_k:
            if len(node.top_k) < 3:
                node.top_k.append(word)
            else:
                worst_match = node.top_k[-1]
                if (self._hot_degree[word] > self._hot_degree[worst_match]) or (self._hot_degree[word] == self._hot_degree[worst_match] and word < worst_match):
                    node.top_k[-1] = word
                else:
                    return

        # re-sort by count desc, then lexicographic asc
        node.top_k.sort(key=lambda w: (-self._hot_degree[w], w))
