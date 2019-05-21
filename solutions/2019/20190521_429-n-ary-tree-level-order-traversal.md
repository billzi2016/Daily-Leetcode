# #429. N叉树层序遍历 / N-ary Tree Level Order Traversal

> 难度：中等 · 标签：Tree、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/n-ary-tree-level-order-traversal/)

---

## 题目（英文原版）

**Description**

Given an n-ary tree, return the level order traversal of its nodes' values.
Nary-Tree input serialization is represented in their level order traversal, each group of children is separated by the null value (See examples).

**Examples**

**Example 1:**

```
Input: root = [1,null,3,2,4,null,5,6]
Output: [[1],[3,2,4],[5,6]]
```

**Example 2:**

```
Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
Output: [[1],[2,3,4,5],[6,7,8,9,10],[11,12,13],[14]]
```

**Constraints**

- The height of the n-ary tree is less than or equal to 1000
- The total number of nodes is between [0, 104]

---

## 题目（中文翻译）

给定一棵 n 叉树（n-ary tree），返回其节点值的层序遍历（level order traversal）。  
n 叉树的序列化采用层序表示，每一组子节点之间以 `null` 分隔（参见示例）。

**示例 1**  
输入：`root = [1,null,3,2,4,null,5,6]`  
输出：`[[1],[3,2,4],[5,6]]`

**示例 2**  
输入：`root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]`  
输出：`[[1],[2,3,4,5],[6,7,8,9,10],[11,12,13],[14]]`

**约束条件**  

- n 叉树的高度 ≤ 1000  
- 节点总数在 `[0, 10^4]` 之间

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**一次只找出同一层的节点**。  
我们可以先知道树的高度（或最大层数），然后**逐层遍历**：

1. 先把根节点记作第 0 层。  
2. 对于第 `i` 层的每个节点，再遍历整棵树，找出所有深度恰好为 `i` 的节点，放进结果的第 `i` 行。  

这里用到的**遍历**可以是最熟悉的深度优先搜索（DFS），即递归地走遍每条路径，只要当前深度等于目标层，就把节点的值加入对应的列表。

> 类比：想象你在一座多层建筑里找第 3 层的所有房间。暴力做法是：先跑遍整座建筑，记录每个房间所在的层数；然后再一次遍历，挑出层数等于 3 的房间。虽然能得到答案，但每层都要重新跑一遍，显然很费时间。

**为什么正确**  
只要我们能够遍历到每个节点，并且在遍历时知道它的深度，就一定能把它放到对应的层级列表里。无论遍历顺序是先根后子（DFS）还是先子后根（BFS），只要记录深度就行。

**时间/空间复杂度**  
- **时间**：假设树有 `N` 个节点，树高（层数）为 `H`。我们对每一层都要遍历整棵树一次，时间 = `H * N`。在最坏情况下（比如链式的 N‑ary 树），`H` 接近 `N`，于是时间复杂度是 **O(N²)**。  
- **空间**：递归栈的最大深度是树高 `H`，再加上保存结果的列表，需要 `O(N)`（因为最终要存所有节点的值），额外空间是 **O(H)**，在最坏情况也是 **O(N)**。

#### 代码（Python）

```python
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val
        # children 是一个 list，可能为空
        self.children = children if children is not None else []


def dfs_collect(node: Node, depth: int, target: int, cur_level: list):
    """
    深度优先遍历整棵树，找到所有深度恰好等于 target 的节点
    """
    if not node:
        return
    if depth == target:                # 到达目标层
        cur_level.append(node.val)
        return
    # 继续往下走子节点，深度+1
    for child in node.children:
        dfs_collect(child, depth + 1, target, cur_level)


def levelOrder_bruteforce(root: Node):
    """
    暴力实现：对每一层都遍历一次整棵树
    """
    if not root:
        return []

    # 先算出树的最大深度（层数）
    def get_height(node: Node) -> int:
        if not node or not node.children:
            return 1
        # 子树的最大高度 + 当前层
        return 1 + max(get_height(child) for child in node.children)

    height = get_height(root)          # 树的层数
    res = []

    # 逐层收集节点值
    for level in range(height):
        cur = []                        # 当前层的结果
        dfs_collect(root, 0, level, cur)
        res.append(cur)
    return res
```

#### 复杂度

- **时间复杂度**：**O(N²)**  
  解释：如果树有 10 000 个节点，最坏情况下需要遍历 10 000 次，每次都要检查全部节点，等价于 100 000 000 次基本操作。`O(N²)` 就是指“随节点数的平方增长”。
- **空间复杂度**：**O(N)**（用于存放最终答案）+ 递归栈 **O(H)**，最坏情况仍是 **O(N)**。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复遍历整棵树是最大的瓶颈**。我们只需要一次遍历，就把所有层级的信息一次性收集完，这正是**广度优先搜索（Breadth‑First Search，BFS）**的特长。

**核心思路**  
- 使用一个**队列**（queue）一次性保存**当前层的所有节点**。  
- 取出队列中的节点，记录它们的值（这就是本层的答案），并把它们的子节点全部加入队列，准备进入**下一层**。  
- 循环直到队列为空。

> 类比：把每层的房间编号贴在一张“待访问”清单上，一次处理完这张清单后，再把下一层的房间编号全部写进新清单。这样每个房间只被“看”一次，省时又省力。

**为什么是最优**  
- 每个节点恰好进入队列一次、弹出一次，整体只遍历一次，时间是 **O(N)**。  
- 除了保存结果外，队列最多只会存放同一层的节点，最坏情况下是树的最大宽度 `W`，空间也是 **O(N)**（因为 `W` ≤ `N`）。

**关键数据结构解释**  

- **队列**：先入先出（FIFO），可以想象排队买票的人，最先进入的人最先买到票。Python 中用 `collections.deque` 实现，高效的 `append`（入队）和 `popleft`（出队）。

#### 代码（Python）

```python
from collections import deque
from typing import List

# 已经在前面定义过 Node，这里直接复用

def levelOrder_bfs(root: Node) -> List[List[int]]:
    """
    广度优先遍历一次完成层序遍历
    """
    if not root:
        return []

    result = []                # 最终返回的二维列表
    queue = deque([root])      # 初始化队列，只放根节点

    while queue:
        level_size = len(queue)        # 当前层有多少节点
        cur_level = []                 # 保存本层的值

        for _ in range(level_size):    # 只遍历当前层的节点
            node = queue.popleft()     # 取出队首节点
            cur_level.append(node.val) # 记录值

            # 把该节点的所有子节点加入队列，准备进入下一层
            for child in node.children:
                queue.append(child)

        result.append(cur_level)       # 本层结束，加入答案

    return result
```

#### 复杂度

- **时间复杂度**：**O(N)** — 每个节点只进出队列一次，操作次数随节点数线性增长。  
- **空间复杂度**：**O(N)** — 最坏情况下队列里可能装满一层的所有节点，层宽度最多等于节点总数 `N`，加上返回的结果同样需要 `O(N)` 空间。

---

## 心得

- **核心技巧**：**广度优先搜索（BFS） + 队列**，一次遍历即可完成层序遍历。  
- **适用题型**（类似思路）：
  1. 二叉树层序遍历（LeetCode 102）  
  2. 最小深度求解（LeetCode 111）  
  3. 以层为单位的树形翻转或镜像（LeetCode 1569）  
- **解题钥匙**：**“一次遍历、一次收集”**——把“本层节点”与“下一层节点”严格分开，用队列自然实现。

---

## 反思

- **第一反应**：看到“层序遍历”立刻想到 BFS，因为 BFS 天生按层访问。  
- **最容易踩的坑**：
  - 忘记在遍历每层时先记录 `level_size`，导致把下一层的节点也混进当前层的结果。  
  - 对空树（`root` 为 `None`）没有特殊处理，会导致 `queue` 初始化报错。  
  - 子节点列表可能为 `None`，使用 `node.children or []` 防止遍历时报 `TypeError`。  
- **下次思考路径**：看到“层次/分层”关键词时，第一步就想到 **“用队列一次遍历”**；如果是“从底向上”或“从右到左”，只需要在收集完每层后做一次简单的**翻转**或**逆序**即可。