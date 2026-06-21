"""
https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/

Given two integer arrays inorder and postorder where inorder is the inorder traversal of a binary tree and postorder is the postorder traversal of the same tree, construct and return the binary tree.



Example 1:


Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
Output: [3,9,20,null,null,15,7]
Example 2:

Input: inorder = [-1], postorder = [-1]
Output: [-1]


Constraints:

1 <= inorder.length <= 3000
postorder.length == inorder.length
-3000 <= inorder[i], postorder[i] <= 3000
inorder and postorder consist of unique values.
Each value of postorder also appears in inorder.
inorder is guaranteed to be the inorder traversal of the tree.
postorder is guaranteed to be the postorder traversal of the tree.
"""

import dataclasses
from typing import Optional


# Definition for a binary tree node.
@dataclasses.dataclass(slots=True)
class TreeNode:
    val: int = 0
    left: Optional[TreeNode] = None
    right: Optional[TreeNode] = None


class Solution:
    def buildTree(self, inorder: list[int], postorder: list[int]) -> Optional[TreeNode]:
        idx = {v: i for i, v in enumerate(inorder)}

        def build(start: int, end: int) -> Optional[TreeNode]:
            if start > end:
                return None

            root = TreeNode(postorder.pop())
            mid = idx[root.val]
            root.right = build(mid + 1, end)
            root.left = build(start, mid - 1)
            return root

        return build(0, len(inorder) - 1)
