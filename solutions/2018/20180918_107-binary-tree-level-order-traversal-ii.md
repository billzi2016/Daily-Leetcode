# #107. 二叉树层序遍历 II / Binary Tree Level Order Traversal II

> 难度：中等 · 标签：Tree、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-level-order-traversal-ii/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the bottom-up level order traversal of its nodes' values. (i.e., from left to right, level by level from leaf to root).

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: [[15,7],[9,20],[3]]
```

**Example 2:**

```
Input: root = [1]
Output: [[1]]
```

**Example 3:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 2000].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

给定二叉树的根节点 `root`，返回其节点值的自底向上的层序遍历（即从左到右、逐层从叶子节点到根节点）。

**示例 1**  
**输入**: `root = [3,9,20,null,null,15,7]`  
**输出**: `[[15,7],[9,20],[3]]`

**示例 2**  
**输入**: `root = [1]`  
**输出**: `[[1]]`

**示例 3**  
**输入**: `root = []`  
**输出**: `[]`

**约束条件**  
- 树中节点的数量在 `[0, 2000]` 范围内。  
- `-1000 <= Node.val <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**先算出树的高度**，再把每一层的节点逐层收集下来。  
- **树的高度**就像一座楼的层数，根节点在第 1 层，叶子节点所在的最深层就是树的总层数。我们可以用递归的方式求高度：左子树高度、右子树高度取较大者再加 1。  
- 知道总层数后，从 **最底层** 往上遍历（即从 height 到 1），每遍历一次就去整棵树里找出当前层的所有节点。这里的“找”可以再写一个递归函数：  
  - 如果当前层数为 1，说明我们已经来到目标层，直接把当前节点的值加入本层列表。  
  - 否则递归进入左、右子树，层数减 1。  

这样我们就能得到 **从叶子层到根层** 的层序遍历。

> 为什么它是对的？  
> - 每一次“找第 k 层”的递归都会恰好访问树中所有节点一次（因为每条路径都要走到第 k 层），所以第 k 层的所有节点一定会被收集完整。  
> - 我们从最高层（叶子层）开始收集，正好满足“自底向上”的要求。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def treeHeight(root: TreeNode) -> int:
    """递归求树的高度，空树高度为 0"""
    if not root:
        return 0
    # 左右子树高度取大 + 1（当前节点所在层）
    return max(treeHeight(root.left), treeHeight(root.right)) + 1


def collectLevel(root: TreeNode, level: int, cur: list) -> None:
    """
    把第 `level` 层的节点值放进列表 `cur` 中
    level = 1 表示当前节点所在层，就是目标层
    """
    if not root:
        return
    if level == 1:               # 到达目标层，直接记录值
        cur.append(root.val)
    else:                        # 继续向下走，层数减 1
        collectLevel(root.left, level - 1, cur)
        collectLevel(root.right, level - 1, cur)


def levelOrderBottom(root: TreeNode) -> list:
    """暴力实现：先算高度，再逐层收集（从底到顶）"""
    h = treeHeight(root)         # 树的总层数
    res = []
    for lvl in range(h, 0, -1):  # 从最高层（叶子层）往下遍历
        cur = []
        collectLevel(root, lvl, cur)
        res.append(cur)
    return res
```

#### 复杂度  

- **时间复杂度：** `O(n²)`  
  - 求高度只需 `O(n)`。  
  - 关键在 `collectLevel`：第 `k` 层的收集会遍历整棵树一次（`O(n)`），而我们要收集 `h` 层，最坏情况下 `h ≈ n`，于是总时间是 `n + n·h = O(n²)`。  
  - 用大白话说，就是如果树有 1000 个节点，最差情况下要跑 1000 次“全树遍历”，大约是 1,000,000 次基本操作。  

- **空间复杂度：** `O(n)`  
  - 递归调用栈的深度最多等于树高 `h`（最坏 `O(n)`），另外我们要保存最终的结果列表，也需要 `O(n)` 的空间。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看出，**瓶颈在于每层都要重新遍历整棵树**。我们只需要一次遍历就能把所有层的信息一次性收集完，这正是 **广度优先搜索（BFS）** 的强项。  

BFS 的核心是 **队列**（Queue），它的工作方式类似排队买票：  
- 先把根节点放进队列。  
- 每次从队列头部弹出一个节点，把它的左、右孩子（如果有）依次加入队列的尾部。  
- 这样弹出顺序恰好是**层序**（从上到下、从左到右）。  

为了实现**自底向上**的层序遍历，只需要在每遍历完一层后，把本层的节点值 **插入结果列表的最前面**（即 `result.insert(0, cur_level)`），或者遍历结束后直接 `result.reverse()`。这里我们采用后者，代码更简洁。

完整步骤如下：

1. **特殊情况**：如果根节点为空，直接返回空列表 `[]`。  
2. 初始化队列 `queue = collections.deque([root])`，以及一个空列表 `result = []` 用来保存每层的节点值。  
3. 进入 `while queue:` 循环，循环体内部先记录当前层的节点数 `size = len(queue)`（这一步相当于“把本层的所有人先拍照”，因为队列里此时正好是本层的所有节点）。  
4. 用 `for _ in range(size):` 逐个弹出本层节点，收集它们的值到 `cur_level`，并把它们的左、右孩子加入队列，为下一层做准备。  
5. 本层遍历完后，把 `cur_level` 加入 `result`。  
6. 循环结束后，`result` 中的层序是**从上到下**的。调用 `result.reverse()` 把顺序翻转，即得到**从下到上**的层序遍历。  

#### 代码（Python）  

```python
import collections
from typing import List, Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def levelOrderBottom(root: Optional[TreeNode]) -> List[List[int]]:
    """BFS 一遍完成，最后再翻转得到自底向上的层序遍历"""
    if not root:                     # 空树直接返回 []
        return []

    queue = collections.deque([root])   # 用双端队列模拟普通队列
    result = []                         # 用来保存每一层的节点值（先上后下）

    while queue:                        # 当队列不为空时继续遍历
        level_size = len(queue)         # 当前层的节点数
        cur_level = []                  # 本层收集的节点值

        for _ in range(level_size):     # 只遍历当前层的节点
            node = queue.popleft()      # 从队头弹出
            cur_level.append(node.val)  # 记录值

            # 把左右子节点（如果有）加入队列，供下一层使用
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

        result.append(cur_level)        # 本层结束后加入结果

    result.reverse()                    # 翻转，使顺序变为“自底向上”
    return result
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 每个节点恰好进入队列一次、弹出一次、访问一次，所以总操作次数与节点数成线性关系。  
  - 用大白话说，树里有 1000 个节点，就只会跑大约 1000 次基本操作，远比暴力解的 1,000,000 次少。  

- **空间复杂度：** `O(n)`  
  - 最坏情况下（完全二叉树的最后一层），队列里会同时存放约 `n/2` 个节点，仍然是 `O(n)` 级别。  
  - 结果列表 `result` 本身也需要保存所有节点的值，同样是 `O(n)`。  

---

## 心得  

- **核心技巧**：广度优先搜索（BFS） + 队列 + 最后一次翻转。  
- **适用的题型**：  
  1. **普通层序遍历**（LeetCode 102）  
  2. **二叉树的最小深度**（LeetCode 111）——利用 BFS 找到最先到达的叶子节点  
  3. **二叉树的右视图**（LeetCode 199）——同样是层序遍历，只取每层最右侧的节点  
- **一句话总结解题钥匙**：一次遍历把所有层的信息都记下来，最后再把顺序翻转即可。  

---

## 反思  

- **第一反应**：先想到“递归求每层”，于是写出了需要多次遍历整棵树的暴力方案。  
- **最容易踩的坑**：  
  - 忘记处理空树 `root = None`，会导致 `queue` 初始化时报错。  
  - 在 BFS 循环里不区分“当前层的节点数”，导致层与层之间的界限混乱，最终得到的不是层序而是整体顺序。  
- **下次遇到同类题**：第一步先想 **“一次遍历能否把所有层的信息都收集？”**，如果能，就立刻考虑 **BFS + 队列**（或者 DFS 记录深度）来一次完成。这样可以避免重复遍历，直接得到最优解。