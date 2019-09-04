# #559. N叉树的最大深度 / Maximum Depth of N-ary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/maximum-depth-of-n-ary-tree/)

---

## 题目（英文原版）

**Description**

Given a n-ary tree, find its maximum depth.
The maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.
Nary-Tree input serialization is represented in their level order traversal, each group of children is separated by the null value (See examples).

**Examples**

**Example 1:**

```
Input: root = [1,null,3,2,4,null,5,6]
Output: 3
```

**Example 2:**

```
Input: root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]
Output: 5
```

**Constraints**

- The total number of nodes is in the range [0, 104].
- The depth of the n-ary tree is less than or equal to 1000.

---

## 题目（中文翻译）

给定一棵 N叉树（n-ary tree），求其最大深度。  
最大深度定义为从根节点（root node）到最远叶子节点（leaf node）之间的最长路径上的节点数。  
N叉树的输入序列化采用层序遍历（level order traversal）的形式，每一组子节点之间使用 `null` 值分隔（参见示例）。

## 示例

### 示例 1
**输入:** `root = [1,null,3,2,4,null,5,6]`  
**输出:** `3`

### 示例 2
**输入:** `root = [1,null,2,3,4,5,null,null,6,7,null,8,null,9,10,null,null,11,null,12,null,13,null,null,14]`  
**输出:** `5`

## 约束条件
- 节点总数在 `[0, 10^4]` 区间内。  
- N叉树的深度不超过 `1000`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有根到叶子的路径都走一遍**，记录下走过的节点数，最后取最大的那个。  
- **遍历方式**：我们可以用递归（深度优先搜索，DFS）来实现。从根节点出发，依次访问每一个子节点，直到没有子节点（叶子）为止。  
- **数据结构类比**：递归调用栈就像一本“探险日志”，每进入一层树，就在日志里写下当前所在的节点，返回上一层时再把这页日志撕掉。  
- **为什么正确**：因为递归会把每条从根到叶的路径都完整走一遍，途中统计的路径长度自然就是这条路径的深度。取所有路径深度的最大值，就是整棵树的最大深度。  

> **提示**：如果你不熟悉递归，可以把它想成“把大问题拆成一模一样的小问题”。这里的大问题是“求整棵树的深度”，小问题是“求某个子树的深度”。

#### 代码（Python）

```python
# Definition for a Node.
class Node:
    def __init__(self, val=None, children=None):
        self.val = val                # 节点的值
        self.children = children or []   # 子节点列表（可能为空）

class Solution:
    def maxDepth(self, root: 'Node') -> int:
        """
        递归遍历所有根→叶路径，返回最大深度
        """
        if not root:                     # 空树的深度是 0
            return 0

        # 对每个子树求深度，取最大的那个
        max_child_depth = 0
        for child in root.children:      # 逐个子节点递归
            child_depth = self.maxDepth(child)
            if child_depth > max_child_depth:
                max_child_depth = child_depth

        # 当前节点算 1 层，加上子树的最大深度
        return 1 + max_child_depth
```

- 第 7 行 `if not root:` 处理边界：如果根本没有节点，深度自然是 0。  
- 第 11‑14 行遍历所有子节点，递归求每棵子树的深度，记录最大的那一棵。  
- 第 17 行 `1 + max_child_depth` 表示：当前节点占一层，加上子树里最深的那层。

#### 复杂度

- **时间复杂度：O(N)** — 这里的 `N` 是树中节点的总数。每个节点只会被访问一次，跟“走遍所有房间”一样，一次遍历完所有房间的时间正比于房间数。  
- **空间复杂度：O(H)** — 递归调用会占用栈空间，最坏情况下栈的深度等于树的高度 `H`（题目保证 `H ≤ 1000`），所以额外空间随树的层数线性增长。

---

### 2. 最优解

#### 思路  

上面的递归实现已经是 **线性时间**，但它使用了递归栈。  
在 Python 中递归层数受限（默认 1000），如果树的深度恰好达到上限，就会出现 `RecursionError`。  
因此，我们可以把 **深度优先改成层序遍历（广度优先搜索，BFS）**，用显式的队列来控制遍历顺序，既避免递归深度限制，又保持 O(N) 的时间。

**核心概念——队列**  
队列像排队买票的队伍，**先进入的先离开**（FIFO）。我们把每一层的所有节点一次性放进队列，遍历完这一层后，队列里剩下的就是下一层的节点。遍历的层数计数器最终就是树的最大深度。

**步骤**：

1. **特判空树**：如果根节点为空，深度为 0。  
2. **初始化队列**：把根节点放进去。  
3. **层循环**：只要队列不空，就说明还有未访问的层。  
   - 记录本层节点数 `size = len(queue)`，这一步相当于“把本层的所有人叫出来”。  
   - 依次弹出 `size` 次，每弹出一个节点，就把它的所有子节点加入队列（为下一层做准备）。  
   - 本层遍历完后，深度计数器 `depth += 1`。  
4. 循环结束时，`depth` 就是树的最大深度。

#### 代码（Python）

```python
from collections import deque   # 双端队列，提供高效的 O(1) 入队/出队

# 同样使用前面的 Node 定义
class Solution:
    def maxDepth(self, root: 'Node') -> int:
        """
        使用 BFS（层序遍历）求最大深度，避免递归深度限制
        """
        if not root:                 # 空树直接返回 0
            return 0

        queue = deque([root])        # 初始化队列，只装根节点
        depth = 0                    # 已遍历的层数

        while queue:                 # 只要还有节点未遍历
            depth += 1               # 进入新的一层，深度+1
            level_size = len(queue)  # 当前层有多少节点

            for _ in range(level_size):   # 逐个处理本层节点
                node = queue.popleft()    # 取出队首节点
                # 把该节点的所有子节点放进队列，准备遍历下一层
                for child in node.children:
                    queue.append(child)

        return depth
```

- 第 6 行 `if not root:` 处理空树。  
- 第 9‑10 行创建 `deque` 并把根节点加入。  
- 第 13‑14 行 `while queue:` 循环，每轮对应树的一层，`depth` 累加。  
- 第 16 行 `level_size = len(queue)` 确定本层节点数，防止在遍历本层时把新加入的下一层节点也算进去。  
- 第 18‑22 行弹出本层节点并把子节点加入队列。

#### 复杂度

- **时间复杂度：O(N)** — 每个节点恰好进队一次、出队一次，整体操作次数正比于节点数。  
- **空间复杂度：O(W)** — 队列里最多同时存放同一层的所有节点，`W` 是树的**最大宽度**（最宽层的节点数），这通常要比递归的深度 `H` 小，尤其是“扁平”树。

> 与递归版相比，时间相同，但空间从 “树高” 变成了 “最大宽度”，在最坏情况下（完全平衡的 N 叉树）两者差距不大；而且 BFS 完全不受递归深度限制，更安全。

---

## 心得

- **核心技巧**：层序遍历（BFS）配合计数器求树的深度。  
- **适用场景**：  
  1. 求二叉树或 N 叉树的最大/最小深度。  
  2. 计算树的层数或逐层输出节点值（层序遍历本身）。  
  3. “最短路径”类问题（例如在无权图中求最短距离），因为 BFS 能保证先到达的节点距离最短。  
- **一句话总结**：**把每一层的节点一次性“叫出来”，层数计数器自然等于树的最大深度**。

---

## 反思

- **第一反应**：看到“最大深度”，本能想到递归的深度优先搜索，因为递归自然能把“根到叶的路径长度”算出来。  
- **最容易踩的坑**：  
  - **空树**：忘记 `root == None` 的情况，会导致 `None.val` 报错。  
  - **递归深度限制**：在 Python 中递归层数超过 1000 会抛异常，需要改用显式栈或 BFS。  
  - **层计数错误**：在 BFS 中，如果不先记录本层节点数就直接遍历队列，可能会把新加入的下一层节点也算进本层，导致深度偏大。  
- **下次遇到同类题**：第一步先判断是“**层数**”还是“**路径长度**”。如果是层数，立刻想到 **BFS + 层计数**；如果是路径长度且不受深度限制，递归的 DFS 也是可靠选择。