# #2385. 二叉树感染所需时间 / Amount of Time for Binary Tree to Be Infected

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/amount-of-time-for-binary-tree-to-be-infected/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree with unique values, and an integer start. At minute 0, an infection starts from the node with value start.
Each minute, a node becomes infected if:
Return the number of minutes needed for the entire tree to be infected.

**Examples**

**Example 1:**

```
Input: root = [1,5,3,null,4,10,6,9,2], start = 3
Output: 4
Explanation: The following nodes are infected during:
- Minute 0: Node 3
- Minute 1: Nodes 1, 10 and 6
- Minute 2: Node 5
- Minute 3: Node 4
- Minute 4: Nodes 9 and 2
It takes 4 minutes for the whole tree to be infected so we return 4.
```

**Example 2:**

```
Input: root = [1], start = 1
Output: 0
Explanation: At minute 0, the only node in the tree is infected so we return 0.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 105].
- 1 <= Node.val <= 105
- Each node has a unique value.
- A node with a value of start exists in the tree.

---

## 题目（中文翻译）

给定一棵节点值唯一的二叉树（binary tree）`root`，以及一个整数 `start`。在第 0 分钟时，感染从值为 `start` 的节点开始。

每过一分钟，若一个节点与已感染的节点直接相连（即是已感染节点的父节点（parent）或子节点（child）），则该节点会被感染。

返回使整棵树全部感染所需的分钟数。

**示例 1**  
**输入**  
```text
root = [1,5,3,null,4,10,6,9,2], start = 3
```
**输出**  
```text
4
```
**解释**  
感染过程如下：

- 第 0 分钟：节点 3  
- 第 1 分钟：节点 1、10 和 6  
- 第 2 分钟：节点 5  
- 第 3 分钟：节点 4  
- 第 4 分钟：节点 9 和 2  

整棵树在第 4 分钟全部被感染，故返回 4。

**示例 2**  
**输入**  
```text
root = [1], start = 1
```
**输出**  
```text
0
```
**解释**  
第 0 分钟时唯一的节点已经被感染，返回 0。

**约束条件**

- 树中节点的数量在 `[1, 10^5]` 区间内。  
- `1 <= Node.val <= 10^5`。  
- 每个节点的值均唯一。  
- 树中一定存在值为 `start` 的节点。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**模拟每一分钟的感染过程**。  
1. 先遍历整棵二叉树，找到值等于 `start` 的节点，把它标记为已感染。  
2. 进入第 `minute = 1`，遍历 **所有节点**，如果它的左子树、右子树或父节点在上一分钟已经感染，则在本分钟把它也感染。  
3. 重复第 2 步，直到没有未感染的节点为止，统计用了多少分钟。  

- **用到的数据结构**：  
  - `dict`（哈希表）把每个节点的 `val` 映射到对应的 `TreeNode` 对象，类似于“查字典”：键是单词（这里是节点的值），值是页码（这里是节点本身）。  
  - `set` 用来记录已经感染的节点值，像是“已经涂过颜色的格子”。  

- **为什么正确**：  
  每一分钟我们都检查所有可能的感染来源（左子、右子、父亲），只要有相邻的已感染节点，就会在本分钟被感染。这样严格按照题目描述的感染规则进行，最终一定会把所有能到达的节点都感染完。

- **时间/空间复杂度**：  
  - 时间复杂度：每一分钟我们都要遍历 **全部 N 个节点**，而最坏情况下需要感染 `N‑1` 次（从根到最远的叶子），所以时间是 `O(N²)`。用大白话说，就是“如果树有 10 万个节点，可能要检查 10 万次 * 10 万次 = 1 亿次”。  
  - 空间复杂度：我们需要保存节点的哈希表和已感染集合，都是 `O(N)` 的额外空间。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def amountOfTime_bruteforce(root: TreeNode, start: int) -> int:
    # 1️⃣ 建立 val -> TreeNode 的映射，顺便把每个节点的父节点也记录下来
    node_map = {}          # 哈希表：值 -> 节点对象
    parent = {}            # 哈希表：节点值 -> 父节点值（如果有）

    def dfs(node, par):
        if not node:
            return
        node_map[node.val] = node
        if par:
            parent[node.val] = par.val
        dfs(node.left, node)
        dfs(node.right, node)

    dfs(root, None)

    # 2️⃣ 初始化已感染集合，只感染 start 节点
    infected = {start}
    minutes = 0

    # 3️⃣ 只要还有未感染的节点，就继续模拟下一分钟
    while len(infected) < len(node_map):
        # 收集本分钟将要被感染的节点
        new_infected = set()
        for val, node in node_map.items():
            if val in infected:
                continue
            # 检查左、右、父三个相邻节点是否已经感染
            left = node.left.val if node.left else None
            right = node.right.val if node.right else None
            par = parent.get(val)

            if (left and left in infected) or \
               (right and right in infected) or \
               (par and par in infected):
                new_infected.add(val)

        # 没有新感染的说明已经全部感染完，直接退出
        if not new_infected:
            break
        infected.update(new_infected)
        minutes += 1

    return minutes
```

#### 复杂度  

- **时间复杂度**：`O(N²)`  
  > 每分钟遍历所有 N 个节点，最坏需要 N‑1 分钟。  
- **空间复杂度**：`O(N)`  
  > 哈希表保存所有节点和父指针，需要与节点数等量的空间。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**每分钟都要遍历整棵树**。如果我们一次性把树的结构转成**无向图**（每条边都可以双向传播），那么感染过程就等价于**从起点出发的层序遍历（BFS）**，只要一次 BFS 就能得到每个节点到 `start` 的最短距离，最大距离即为答案。  

**关键步骤**  

1. **把二叉树看成无向图**  
   - 对每个节点，和它的左子节点、右子节点各连一条无向边。  
   - 用 `defaultdict(list)` 把 `val` 视作图的“城市”，相邻的 `val` 放进同一个列表，类似“街道”。  

2. **从 `start` 开始做 BFS**  
   - 使用队列 `deque` 按层遍历，每遍历完一层就代表时间 +1。  
   - 用 `visited` 集合防止走回头路（避免无限循环），就像在城市里已经走过的路不再重复计数。  

3. **记录遍历的层数**  
   - BFS 结束时的层数（不包括第 0 层）就是所有节点被感染所需的最久时间。  

**为什么正确**：  
在无向图里，感染每分钟可以向所有相邻节点扩散一次，这正好是 **最短路径** 的概念。BFS 正好能在最少的步数（分钟）到达每个节点。因为每条边的传播时间都是 1 分钟，BFS 计算出的层数就是节点到 `start` 的最短距离，最大距离就是整个树被感染的最慢时刻。

**核心算法**：  
- **深度优先搜索（DFS）** 用来把树转成图（一次遍历 O(N)）。  
- **广度优先搜索（BFS）** 用来求最远距离（一次遍历 O(N)）。  

#### 代码（Python）  

```python
from collections import defaultdict, deque
from typing import Optional


# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def amountOfTime(root: TreeNode, start: int) -> int:
    """
    将二叉树转成无向图 + BFS 求最远距离
    """
    # 1️⃣ 建图：val -> 相邻的 val 列表
    graph = defaultdict(list)

    def build(u: Optional[TreeNode]):
        if not u:
            return
        if u.left:
            # 双向连边，左子节点 <-> 当前节点
            graph[u.val].append(u.left.val)
            graph[u.left.val].append(u.val)
            build(u.left)
        if u.right:
            # 双向连边，右子节点 <-> 当前节点
            graph[u.val].append(u.right.val)
            graph[u.right.val].append(u.val)
            build(u.right)

    build(root)                     # O(N) 完成建图

    # 2️⃣ BFS 从 start 开始，记录层数（分钟）
    q = deque([start])              # 队列里放当前层的节点
    visited = {start}               # 已经访问过的节点集合
    minutes = -1                    # 初始为 -1，遍历完第 0 层后会变成 0

    while q:
        minutes += 1                # 进入新的一层，时间 +1
        for _ in range(len(q)):     # 只遍历当前层的节点
            cur = q.popleft()
            for nb in graph[cur]:   # 检查所有相邻节点
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)    # 加入下一层

    return minutes                  # 最后一次循环结束时的 minutes 就是答案
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  > 建图遍历一次树 `O(N)`，BFS 再遍历所有节点和边 `O(N)`（二叉树的边数最多是 `2·(N‑1)`），所以整体线性。相比暴力的 `O(N²)`，快了很多。  
- **空间复杂度**：`O(N)`  
  > 图的邻接表、队列、visited 集合都需要存每个节点的信息，和节点数成正比。  

---  

## 心得  

- **核心技巧**：把树视作**无向图**，利用 **BFS** 计算最远距离。  
- **适用的题型**（类似思路）：  
  1. **“感染/传播”类问题**：如 *“感染二叉树的最短时间”*、*“网络感染”*。  
  2. **树的最长路径**：如 *“二叉树中最长的连续路径”*（把树转成图后求直径）。  
  3. **多源最短路径**：如 *“在树上同时从多个节点扩散”*（多源 BFS）。  
- **一句话总结解题钥匙**：  
  > “把树的父子关系变成可以双向走的道路，用层层扩散的广度优先搜索，最大层数就是感染全部节点所需的时间。”  

---  

## 反思  

- **第一反应**：看到“每分钟向相邻节点扩散”，第一时间会想到**BFS**，但往往会忘记二叉树的父节点没有显式指针，需要先**构建无向图**或记录父指针。  
- **最容易踩的坑**：  
  1. **忘记把父子边做成双向**，导致只能向下感染，结果时间会错误。  
  2. **未处理单节点树**，BFS 循环一次就返回 `0`，要保证初始 `minutes = -1` 才能得到正确答案。  
  3. **递归建图时栈溢出**（节点数可达 10⁵），可以改成显式栈或使用迭代方式，这里递归深度一般在 Python 默认限制（约 1000）以内，实际提交时要注意。  
- **下次遇到同类题**的第一步：  
  > “先把树转换成可以双向遍历的结构（邻接表或记录父指针），然后用 BFS 从起点层层扩散，最大层数即答案。”