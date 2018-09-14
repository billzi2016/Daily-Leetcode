# #102. 二叉树层序遍历 / Binary Tree Level Order Traversal

> 难度：中等 · 标签：Tree、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-tree-level-order-traversal/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: [[3],[9,20],[15,7]]
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

给定一棵二叉树（binary tree）的根节点（root），返回其节点（node）值的层序遍历（level order traversal），即按从左到右、逐层的顺序访问所有节点的值。

**示例 1：**  
**输入：** `root = [3,9,20,null,null,15,7]`  
**输出：** `[[3],[9,20],[15,7]]`

**示例 2：**  
**输入：** `root = [1]`  
**输出：** `[[1]]`

**示例 3：**  
**输入：** `root = []`  
**输出：** `[]`

**约束条件：**  
- 树中节点的数量在 `[0, 2000]` 区间内。  
- `-1000 <= Node.val <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**一次只求出一层的节点**，然后把每层的结果放进最终的列表。  
实现方式可以用递归（深度优先搜索）配合“层数”这把钥匙：

1. 先写一个 `dfs(node, depth)`，每访问到一个节点，就把它的值放到 `levels[depth]`（如果 `levels` 里还没有第 `depth` 层，就先新建一个子列表）。  
2. 对左子树递归 `depth+1`，右子树同理。  
3. 最后 `levels` 就是层序遍历的结果。

> **类比**：把二叉树想象成一本书的章节结构，`depth` 就是章节号。我们从根章节（第 0 章）开始，遇到子章节就往后推一层，记下来。

这种做法一定能得到正确答案，因为我们把每个节点恰好放进了它所在的层。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def levelOrder_bruteforce(root: TreeNode) -> list[list[int]]:
    """暴力版：DFS + 按层收集"""
    if not root:
        return []               # 空树直接返回空列表

    levels: list[list[int]] = []   # 用来保存每一层的节点值

    def dfs(node: TreeNode, depth: int) -> None:
        """深度优先遍历，同时把节点放入对应层的列表"""
        if not node:
            return
        # 如果当前层还没有对应的子列表，就创建一个
        if depth == len(levels):
            levels.append([])   # 新建第 depth 层
        # 把当前节点值加入第 depth 层
        levels[depth].append(node.val)

        # 继续向左、右子树遍历，层数+1
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)                  # 从根节点、第 0 层开始
    return levels
```

#### 复杂度

- **时间复杂度：** `O(n²)`（最坏情况）  
  - 对每个节点，我们都要遍历一次它所在的层的列表（`append` 本身是 `O(1)`，但创建层列表的次数是 `depth`，在极端的“链状”树里，深度≈`n`，导致整体近似 `1 + 2 + … + n = O(n²)`）。
  - 用大白话说，就是如果树像一条长长的链子，程序会一次一次“爬坡”，每爬一级都要重新走过去，累计的工作量会像等差数列一样增长。

- **空间复杂度：** `O(n)`  
  - `levels` 最终会存放所有节点的值（`n` 个），再加上递归栈的深度 `O(h)`，`h ≤ n`，所以总体是线性的。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**层与层之间的界限是瓶颈**：我们在遍历整棵树的同时，还要不停地检查“当前到底在第几层”。  
如果我们能够一次性把同一层的所有节点全部取出来，就不需要再“回头”检查层号了。

这正是**广度优先搜索（Breadth‑First Search，BFS）**的核心思想：  
- 用 **队列**（Queue）来保存**待访问的节点**，先进去的先出来，保证同层的节点一次性被处理。  
- 具体做法：  
  1. 把根节点放进队列。  
  2. 只要队列不为空，就**记录本轮队列的长度**（这就是当前层的节点数）。  
  3. 按这个长度依次弹出节点，收集它们的值，同时把它们的左、右子节点（如果有）加入队列。弹完一轮后，队列里剩下的就是**下一层**的节点。  
  4. 重复步骤 2‑3，直到队列空。

> **类比**：把队列想象成一条排队买票的队伍。第一批进来的都是同一层的观众，等他们买完票（出队）后，后面排队的就是下一层的观众。这样我们天然地把层划分好了。

这种做法只遍历每个节点一次，且不需要额外的层计数结构，因而是最优的。

#### 代码（Python）

```python
from collections import deque  # deque 是双端队列，popleft 是 O(1) 的出队操作

def levelOrder_bfs(root: TreeNode) -> list[list[int]]:
    """最优版：使用队列的层序遍历（BFS）"""
    if not root:
        return []               # 空树直接返回空列表

    result: list[list[int]] = []   # 最终的层序结果
    q = deque([root])              # 初始化队列，先把根节点放进去

    while q:                       # 当队列不为空时循环
        level_size = len(q)        # 本层有多少节点（当前队列长度）
        level_vals: list[int] = [] # 用来收集本层的节点值

        for _ in range(level_size):   # 只遍历本层的节点数次
            node = q.popleft()         # 取出队首节点
            level_vals.append(node.val)  # 记录它的值

            # 把左子节点、右子节点（如果存在）加入队列，供下一层使用
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        result.append(level_vals)   # 本层处理完，加入结果

    return result
```

#### 复杂度

- **时间复杂度：** `O(n)`  
  - 每个节点恰好被 `popleft` 一次、`append`（子节点）一次，所有操作都是常数时间，总工作量随节点数线性增长。  
  - 用大白话说，就是“不管树长啥样，我们只走一遍所有的节点”，所以和节点数成正比。

- **空间复杂度：** `O(m)`（`m` 为任意时刻队列中的节点数）  
  - 最坏情况下，队列里会装满某一层的所有节点。对于完全二叉树，最大的那层大约是 `n/2`，所以空间仍然是 `O(n)`。  
  - 这和保存结果的 `result` 一起，仍是线性空间。

---

## 心得

- **核心技巧**：**广度优先搜索（BFS） + 队列**，能够一次性把同一层的节点全部取出，避免层间来回检查。
- **适用题型**：  
  1. 二叉树的层序遍历（本题）。  
  2. 求二叉树最小深度（先到达叶子层即停止）。  
  3. 图的最短路径（无权图），比如 “岛屿的最大面积” 这类 BFS 题。
- **一句话总结**：**层序遍历 = “把同层的节点排成一队，先出队的自然是上一层”。**

---

## 反思

- **第一反应**：看到“层序遍历”这四个字，就想到“从上到下、从左到右”，自然联想到 **队列** 这种“先来先服务”的结构。
- **最容易踩的坑**：  
  - **空树**：根本没有节点，需要提前返回 `[]`，否则 `while q:` 会因为 `q` 为 `None` 报错。  
  - **层大小的获取**：必须在每轮循环开始时 **先记录 `len(q)`**，否则在循环内部 `append` 子节点会把下一层的节点也算进去，导致层划分错误。  
  - **递归深度**（如果用 DFS）在极端链状树会超过 Python 默认递归限制，需要手动调大或改用迭代。
- **下次类似题的第一步**：**先判断是要“层级”信息还是“路径”信息**。如果是层级，立刻想到 BFS + 队列；如果是路径最短，仍然是 BFS；如果是子结构的最优子问题，可能要考虑 DP。这样就能快速锁定最合适的算法框架。