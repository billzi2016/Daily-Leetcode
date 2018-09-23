# #111. 二叉树的最小深度 / Minimum Depth of Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/minimum-depth-of-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree, find its minimum depth.
The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
Note: A leaf is a node with no children.

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: 2
```

**Example 2:**

```
Input: root = [2,null,3,null,4,null,5,null,6]
Output: 5
```

**Constraints**

- The number of nodes in the tree is in the range [0, 105].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵二叉树，求它的最小深度。  
最小深度是指从根节点（root）到最近的叶子节点（leaf）之间的最短路径上经过的节点数。  
注意：叶子节点是指没有子节点（children）的节点。

约束条件：

- 树中节点的数量在范围 `[0, 10^5]` 内。  
- `-1000 <= Node.val <= 1000`

示例 1:
Input: root = [3,9,20,null,null,15,7]
Output: 2

示例 2:
Input: root = [2,null,3,null,4,null,5,null,6]
Output: 5

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把树的所有路径都走一遍，找到最短的那条**。  
这相当于在树里“深度优先搜索”(Depth‑First Search，简称 DFS)。  
我们可以用递归的方式，从根节点出发，分别递归左子树和右子树，得到它们的最小深度，再取较小的那个加一（因为根节点本身算一层）。

> **类比**：想象你在一座山上寻找最近的山脚，DFS 就像让你先爬完左边的所有小路，再爬右边的所有小路，最后比较哪条路最短。

需要注意的是：**只有叶子节点（左右子树都为空）才算结束**。如果某个子树为空，而另一个子树不为空，不能直接把空的子树当作深度 0，而是要把有节点的那条子树的深度算进去。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def minDepth(root: TreeNode) -> int:
    # 空树的最小深度是 0
    if not root:
        return 0

    # 递归左、右子树的最小深度
    left = minDepth(root.left)
    right = minDepth(root.right)

    # 两个子树都非空，取较小的那个再加上根节点自己
    if left and right:
        return min(left, right) + 1
    # 只有左子树或右子树非空，必须走那条有节点的路径
    else:
        return max(left, right) + 1
```

#### 复杂度  

- **时间复杂度：**`O(N)`  
  这里的 `N` 是树中节点的个数。我们会访问每个节点恰好一次，跟树的大小成线性关系。  
  **大白话**：如果树里有 1000 个节点，程序大概会跑 1000 次「检查」操作。

- **空间复杂度：**`O(H)`（递归栈的深度）  
  `H` 是树的高度。最坏情况下（树退化成链表），递归栈会占用 `N` 层空间；在平衡树中，大约是 `log N` 层。  
  **大白话**：递归时会像一层层叠加的纸条，最多叠到树的深度那么高。

---

### 2. 最优解

#### 思路  

虽然 DFS 已经是 `O(N)`，但它仍然会遍历整棵树，即使已经找到了最近的叶子。  
**我们可以在「遍历」的过程中，一旦碰到第一个叶子就立刻停止**，这正好是**广度优先搜索**（Breadth‑First Search，简称 BFS） 的特性。

BFS 按层（depth）一次遍历整棵树：

1. 把根节点放进队列（queue），记住当前层数是 1。  
2. 取出队首节点，检查它是否是叶子（左、右子树都为空）。  
   - 如果是叶子，当前层数就是最小深度，直接返回。  
3. 否则把它的左右子节点（如果存在）加入队列，并继续下一轮。  
4. 当所有节点都被处理完，仍未找到叶子（只有空树的情况），返回 0。

> **类比**：想象你在一座建筑里找最近的出口，BFS 就像先检查 1 层的所有房间，若没找到再检查第 2 层，依次类推，最先碰到的出口就是最近的。

#### 代码（Python）

```python
from collections import deque  # 导入双端队列，效率高

def minDepth(root: TreeNode) -> int:
    if not root:                     # 空树直接返回 0
        return 0

    q = deque([root])                # 队列里先放根节点
    depth = 1                        # 当前层数，从根节点算起

    while q:                         # 当队列不为空时循环
        level_size = len(q)          # 本层有多少节点
        for _ in range(level_size):  # 逐个处理本层的节点
            node = q.popleft()       # 取出队首

            # 判断是否为叶子节点
            if not node.left and not node.right:
                return depth        # 第一次碰到叶子，depth 就是最小深度

            # 把子节点加入队列，供下一层使用
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        depth += 1                    # 本层处理完，层数加一

    # 理论上不会走到这里，因为一定会在某层返回
    return depth
```

#### 复杂度  

- **时间复杂度：**`O(N)`（最坏仍然会遍历所有节点）  
  但**实际运行时往往会提前结束**。如果最短路径只在前几层，后面的节点根本不会被访问。  
  **大白话**：仍然是线性，但在多数情况下会比 DFS “跑得更快”。

- **空间复杂度：**`O(W)`，其中 `W` 是树的**最大宽度**（任意一层的节点数）。  
  对于完全二叉树，最大宽度大约是 `2^{H-1}`，但这仍然是 `O(N)` 的上界。  
  **大白话**：队列里最多装下一层的所有节点，最宽的那层决定了占用多少“空间”。

---

## 心得

- **核心技巧**：**层序遍历（BFS）** 能在找到第一个叶子时立即停止，从而得到最小深度。  
- **适用的题型**：  
  1. “最短路径”类树题，如 *Binary Tree Level Order Traversal*（层序遍历）。  
  2. “最近的目标”类题，如 *Find the Closest Leaf in a Binary Tree*。  
  3. 需要**按层次**处理数据的场景，如 *Zigzag Level Order Traversal*。  
- **一句话总结**：**“先把树按层‘剥开’，第一层出现叶子时就停”**——这就是最小深度的钥匙。

---

## 反思

- **第一反应**：直接想到递归 DFS，写出完整遍历的代码。  
- **最容易踩的坑**：  
  - 当左子树为空而右子树不为空时，不能把左子树的深度当作 0 再取 `min`，否则会把根直接算成叶子。  
  - 空树 (`root = None`) 的返回值必须是 0。  
  - BFS 实现时要注意层数的递增位置，不能在检查完一个节点后就加层。  
- **下次遇到同类题**：第一步先思考**“是最短路径还是最长路径”**。如果是最短路径，立刻考虑 **BFS**；如果是最长路径，再考虑 **DFS + DP**。这样可以快速定位最合适的遍历方式。