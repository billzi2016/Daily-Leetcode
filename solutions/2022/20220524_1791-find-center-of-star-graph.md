# #1791. 寻找星形图的中心 / Find Center of Star Graph

> 难度：简单 · 标签：Graph · [LeetCode 链接](https://leetcode.com/problems/find-center-of-star-graph/)

---

## 题目（英文原版）

**Description**

There is an undirected star graph consisting of n nodes labeled from 1 to n. A star graph is a graph where there is one center node and exactly n - 1 edges that connect the center node with every other node.
You are given a 2D integer array edges where each edges[i] = [ui, vi] indicates that there is an edge between the nodes ui and vi. Return the center of the given star graph.

**Examples**

**Example 1:**

```
Input: edges = [[1,2],[2,3],[4,2]]
Output: 2
Explanation: As shown in the figure above, node 2 is connected to every other node, so 2 is the center.
```

**Example 2:**

```
Input: edges = [[1,2],[5,1],[1,3],[1,4]]
Output: 1
```

**Constraints**

- 3 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 1 <= ui, vi <= n
- ui != vi
- The given edges represent a valid star graph.

---

## 题目（中文翻译）

有一个无向星形图（star graph），其中包含 n 个节点，编号为 1 到 n。星形图是一种图结构，只有一个中心节点，并且恰好有 n‑1 条边，每条边都连接中心节点与其他任意一个节点。

给定一个二维整数数组 `edges`，其中 `edges[i] = [ui, vi]` 表示节点 `ui` 与节点 `vi` 之间存在一条边。返回该星形图的中心节点编号。

**示例 1**  
**示例 2**  
**约束条件**  

### 示例

**示例 1**  
```
Input: edges = [[1,2],[2,3],[4,2]]
Output: 2
Explanation: 如上图所示，节点 2 与所有其他节点相连，因此 2 是中心节点。
```

**示例 2**  
```
Input: edges = [[1,2],[5,1],[1,3],[1,4]]
Output: 1
```

### 约束条件
- 3 <= n <= 10^5
- `edges.length == n - 1`
- `edges[i].length == 2`
- 1 <= ui, vi <= n
- ui != vi
- 给定的边集合一定能构成一棵有效的星形图。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历所有节点，找出与它相连的边有多少条**，出现次数最多的那个节点就是星形图的中心。  

- **使用的数据结构**：我们可以用 **哈希表（dictionary）** 来记录每个节点出现的次数。哈希表就像一本词典，单词是“键”（key），对应的解释或页码是“值”（value），查找和插入的时间都非常快（≈ O(1)）。
- **为什么正确**：在星形图里，唯一的中心节点会和 **每一个其它节点** 都有一条边，所以它的出现次数是 `n‑1`（总边数），而其他所有节点只出现一次。出现次数最多的就是中心。
- **复杂度分析**：我们要遍历 `edges` 中的每条边，边的条数是 `n‑1`，对每条边的两个端点各做一次哈希表的加一操作，整体是线性的。  
  - 时间复杂度：`O(n)`，这里的 `n` 实际指的是节点数（因为 `edges` 长度是 `n‑1`），也就是说随着节点增多，耗时几乎和节点数等比例增长。  
  - 空间复杂度：`O(n)`，我们需要一个哈希表存放每个节点的计数，最坏情况下会保存所有 `n` 个节点。

> **大白话**：如果你把每条边看成两个人握手，那么中心节点就是“握手次数最多的那个人”。我们只要把每个人握手的次数记下来，次数最多的就是答案。

#### 代码（Python）

```python
from typing import List

def findCenter(edges: List[List[int]]) -> int:
    # 用字典统计每个节点出现的次数
    cnt = {}                     # key: 节点编号, value: 出现次数
    for u, v in edges:           # 遍历每条边
        cnt[u] = cnt.get(u, 0) + 1   # u 的计数加 1
        cnt[v] = cnt.get(v, 0) + 1   # v 的计数加 1

    # 找出计数最大的节点（必然是中心）
    for node, times in cnt.items():
        if times > 1:            # 中心的次数一定大于 1（因为 n≥3）
            return node
    # 题目保证一定有中心，代码理论上不会走到这里
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次 `edges`（`n‑1` 条），每次操作都是常数时间。
- **空间复杂度**：`O(n)` —— 需要存储每个节点的计数，最坏情况保存全部 `n` 个节点。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**统计每个节点的出现次数** 已经是线性时间，已经是最优的时间复杂度了。  
但我们可以进一步 **省掉哈希表**，因为题目已经保证输入是一棵星形图：**任意两条边一定会有公共节点**，而这个公共节点就是中心。利用这一点，只要看前两条边的两个端点，找出它们的公共节点即可。

步骤如下：

1. 取 `edges[0]` 和 `edges[1]`，分别记为 `[a, b]` 与 `[c, d]`。  
2. 比较这四个数，必有一个数同时出现在这两条边里——那就是中心。  
   - 若 `a` 与 `c`、`d` 中任意一个相同，则 `a` 为中心。  
   - 否则 `b` 必然是中心（因为题目保证是星形图，必有公共节点）。

这样我们只检查常数条边，**时间 O(1)**，**空间 O(1)**。

> **类比**：想象有很多条绳子都系在同一个柱子上，任意挑两条绳子，它们必然在柱子处相交。只要找出这两条绳子共同系在哪根柱子上，就找到了答案。

#### 代码（Python）

```python
from typing import List

def findCenter(edges: List[List[int]]) -> int:
    # 取前两条边
    a, b = edges[0]          # 第一条边的两个端点
    c, d = edges[1]          # 第二条边的两个端点

    # 判断哪一个端点在两条边里都出现
    if a == c or a == d:
        return a            # a 同时在两条边里，是中心
    else:
        return b            # 否则 b 必然是中心
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 只检查两条边，常数时间。相比于遍历全部边的 `O(n)`，这在大数据量时更快。
- **空间复杂度**：`O(1)` —— 只用了几条临时变量，不随 `n` 增长。

---

## 心得

- **核心技巧**：利用星形图的结构特性——所有边必共享同一个公共节点。  
- **适用的题型**  
  1. “找出所有边的公共点” 类似题（如 LeetCode 1791 Find Center of Star Graph）。  
  2. “寻找唯一出现次数超过一次的元素” （比如多数元素题目）。  
  3. “在已知图为树且有特殊形状时的快速定位” （如找根节点、叶子等）。  
- **一句话总结**：**只要抓住“任意两条边都有公共点”这一关键，就能用常数时间直接定位中心**。

---

## 反思

- **第一反应**：看到“星形图”，立刻想到“度最大的节点是中心”，于是写了统计度的解法。  
- **最容易踩的坑**：  
  - 忘记题目保证是合法的星形图，盲目写通用图算法会导致不必要的复杂度。  
  - 对于 `n` 很大时，使用额外的哈希表会占用较多内存，虽然仍在限制范围内，但不是最优。  
- **下次遇到同类题**：**先判断是否有全局唯一的结构特征（如所有边共点、所有路径必经某点），若有，尝试用常数时间的“抽样”方法直接定位**。