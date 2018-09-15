# #104. 二叉树的最大深度 / Maximum Depth of Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-depth-of-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: 3
```

**Example 2:**

```
Input: root = [1,null,2]
Output: 2
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

**描述**  
给定一棵二叉树（binary tree）的根节点（root），返回它的最大深度（maximum depth）。  
二叉树的最大深度是从根节点向下到最远叶子节点（leaf node）之间最长路径上的节点数。

**示例 1**  
**示例 2**  

**约束条件**  
- 树中节点的数量在 `[0, 10^4]` 范围内。  
- `-100 <= Node.val <= 100`

**示例**  
**示例 1:**  
```
Input: root = [3,9,20,null,null,15,7]
Output: 3
```

**示例 2:**  
```
Input: root = [1,null,2]
Output: 2
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直观的想法是：从根节点出发，沿着每一条可能的路径一直往下走，记录走到叶子节点时走过的节点数，所有路径走完后取最大值。  
这相当于「把树的每条枝干都爬一遍」，所以我们可以用 **深度优先搜索（DFS）** 的递归方式实现：  

1. 对当前节点 `node`，分别递归求左子树的最大深度 `left_depth` 与右子树的最大深度 `right_depth`。  
2. 当前节点的深度就是 `max(left_depth, right_depth) + 1`（+1 表示把自己算进去）。  
3. 空树的深度为 0，作为递归的终止条件。  

> **类比**：递归求深度就像在查字典，`node` 是要查的词，左/右子树是词的两个解释，返回的数字是「解释的层数」。  

这个方法一定能得到正确答案，因为每个节点的深度都是由它的子树深度决定的，递归把所有可能的路径都考虑到了。

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def maxDepth(root: TreeNode) -> int:
    """递归版：求二叉树的最大深度"""
    if root is None:                     # 空树的深度是 0，递归终止
        return 0
    # 递归求左子树、右子树的深度
    left_depth = maxDepth(root.left)     
    right_depth = maxDepth(root.right)
    # 当前节点的深度 = 左右子树深度的较大者 + 1（自己这一层）
    return max(left_depth, right_depth) + 1
```

#### 复杂度  

- **时间复杂度：** `O(n)` —— 每个节点恰好被访问一次，`n` 为树中节点数。  
  > 大白话：如果树里有 1000 个节点，程序大概会跑 1000 次「检查」的动作。  
- **空间复杂度：** `O(h)` —— 递归栈的深度等于树的高度 `h`。最坏情况下（树呈链状）`h = n`，所以最坏空间是 `O(n)`。  

---  

### 2. 最优解  

#### 思路  
虽然递归写法已经是 **线性时间**，但它依赖系统调用栈，深度很大的树可能导致 **递归层数超过 Python 的递归深度限制**（默认约 1000），从而抛出 `RecursionError`。  
为了解决这个「瓶颈」并且让代码更「可控」，我们可以把递归改成 **显式的遍历**，常见的有两种：

1. **层序遍历（Breadth‑First Search，BFS）**：使用队列一次遍历一层，遍历完第 `k` 层后计数器加 1，直到队列为空。计数器的最终值就是树的最大深度。  
2. **迭代深度优先（DFS）**：使用栈手动模拟递归，同样可以记录每个节点对应的深度。  

这里选用 **BFS**，因为它把「层数」直接体现在遍历过程里，思路最直观，也避免了递归深度的风险。

**关键步骤的类比**：  
- 队列就像排队买票的队伍，先进入队列的节点先出队，保证「先看完上一层」再「进入下一层」。  
- 每轮循环结束时，队列里正好是当前层的所有节点，计数器加一相当于「记录已经走过了几层楼」。

#### 代码（Python）  

```python
from collections import deque  # 导入双端队列，效率高于 list 当队列使用

def maxDepth(root: TreeNode) -> int:
    """BFS 版：逐层遍历求二叉树最大深度"""
    if root is None:                     # 空树直接返回 0
        return 0

    queue = deque([root])                # 初始队列只装根节点
    depth = 0                            # 记录已经遍历的层数

    while queue:                         # 当还有节点未处理时循环
        depth += 1                       # 即将遍历新的一层，层数加 1
        level_size = len(queue)          # 当前层有多少节点

        # 依次把本层的所有节点弹出，并把它们的子节点加入队列
        for _ in range(level_size):
            node = queue.popleft()       # 取出队首节点
            if node.left:                # 左子树非空就加入队列
                queue.append(node.left)
            if node.right:               # 右子树非空也加入队列
                queue.append(node.right)

    return depth                         # 队列空时，depth 已是最大层数
```

#### 复杂度  

- **时间复杂度：** `O(n)` —— 每个节点恰好入队、出队各一次，仍是线性时间。  
- **空间复杂度：** `O(w)` —— `w` 为树的最大宽度（某一层的节点数），在最坏情况下（完全二叉树）`w ≈ n/2`，即 `O(n)`。  
  > 与递归版相比，空间从「递归深度」变成了「最宽层的节点数」，在高度非常大的「链状」树里会更省内存。

---  

## 心得  

- 这道题的核心是 **遍历二叉树并记录层数**，常用的手段是递归（DFS）或层序遍历（BFS）。  
- 类似的技巧可以用在：  
  1. **判断二叉树是否平衡**（需要每棵子树的高度）  
  2. **求二叉树的最小深度**（同样是层序遍历）  
  3. **层序遍历输出每层节点值**（典型的 BFS 练习）  
- **一句话总结解题钥匙**：`层层推进，计数即深度` —— 把「走了几层」当作答案，遍历时只要保证每层完整走完即可。

---  

## 反思  

- **第一反应**：看到「最大深度」立刻想到「递归求左右子树高度取最大」或「层序遍历计层数」。  
- **最容易踩的坑**：  
  - 忘记处理空树 (`root == None`) 会导致返回错误的 1。  
  - 递归版在极深的链状树上会触发 `RecursionError`。  
  - BFS 中忘记在每层结束后才 `depth += 1`，会把节点数算成深度。  
- **下次遇到同类题**，第一步应该思考「是要找最高层还是最低层」——如果是「层数」相关，**层序遍历**往往是最安全、最直观的选择；如果只需要「某个节点的高度」则**递归 DFS**更简洁。