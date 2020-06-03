# #886. 可能的二分 / Possible Bipartition

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/possible-bipartition/)

---

## 题目（英文原版）

**Description**

We want to split a group of n people (labeled from 1 to n) into two groups of any size. Each person may dislike some other people, and they should not go into the same group.
Given the integer n and the array dislikes where dislikes[i] = [ai, bi] indicates that the person labeled ai does not like the person labeled bi, return true if it is possible to split everyone into two groups in this way.

**Examples**

**Example 1:**

```
Input: n = 4, dislikes = [[1,2],[1,3],[2,4]]
Output: true
Explanation: The first group has [1,4], and the second group has [2,3].
```

**Example 2:**

```
Input: n = 3, dislikes = [[1,2],[1,3],[2,3]]
Output: false
Explanation: We need at least 3 groups to divide them. We cannot put them in two groups.
```

**Constraints**

- 1 <= n <= 2000
- 0 <= dislikes.length <= 104
- dislikes[i].length == 2
- 1 <= ai < bi <= n
- All the pairs of dislikes are unique.

---

## 题目（中文翻译）

我们希望把 n 个人（编号为 1 到 n）划分为任意大小的两个组（group）。每个人可能会不喜欢（dislike）其他人，而这些不喜欢的两个人不能被放在同一个组中。

给定整数 n 和数组 dislikes，其中 dislikes[i] = [a_i, b_i] 表示编号为 a_i 的人不喜欢编号为 b_i 的人。若能够按照上述要求把所有人划分到两个组中，返回 true；否则返回 false。

**示例 1**  
输入: n = 4, dislikes = [[1,2],[1,3],[2,4]]  
输出: true  
解释: 第一个组为 [1,4]，第二个组为 [2,3]。

**示例 2**  
输入: n = 3, dislikes = [[1,2],[1,3],[2,3]]  
输出: false  
解释: 需要至少 3 个组才能将他们划分开，无法用两组完成划分。

**约束条件**  
- 1 ≤ n ≤ 2000  
- 0 ≤ dislikes.length ≤ 10⁴  
- dislikes[i].length == 2  
- 1 ≤ a_i < b_i ≤ n  
- 所有不喜欢的配对都是唯一的。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的分组方式**，然后看哪一种满足“所有互相不喜欢的两个人不在同一组”。  
因为每个人只能在「组 A」或「组 B」两种状态里挑一种，实际上这相当于把 `n` 个人的状态写成一个长度为 `n` 的二进制串：

- `0` 表示该人进入组 A  
- `1` 表示该人进入组 B  

于是我们只要遍历 `0 … 2^n‑1`（所有的二进制串），把每一种分配方式代入题目中的不喜欢关系 `dislikes`，检查是否有冲突即可。

**用到的数据结构**  
- **列表** `dislikes`：存放所有「不喜欢」的配对，就像我们平时记的「谁和谁不合」的名单。  
- **整数的位运算**：把一个整数的第 `i` 位当作第 `i` 个人的组别，类似把一本字典的页码当成「这本词在第几页」的映射。

**为什么这个方法正确**  
只要遍历了所有 `2^n` 种可能的分配方式，就一定会碰到最优（如果有的话）。只要在某一次遍历中，所有不喜欢的配对都落在不同的组，就返回 `True`；如果所有遍历都失败，说明根本不存在合法的两组划分，返回 `False`。

**时间/空间复杂度**  
- **时间**：我们要检查 `2^n` 种分配方式，每一种都要遍历全部的 `m = len(dislikes)` 条不喜欢关系。于是总时间是 `O(2^n * m)`。这里的 `2^n` 在 n 较大时会非常快爆炸，就像把一棵树的每一根枝条都枚举一遍。  
- **空间**：只用了常数级别的额外空间 `O(1)`（只存几个计数器和临时变量），不随 `n` 增长。

#### 代码（Python）

```python
from typing import List

def possible_bipartition_bruteforce(n: int, dislikes: List[List[int]]) -> bool:
    """
    暴力枚举所有 2^n 种分配方式，检查是否满足所有不喜欢的约束。
    """
    m = len(dislikes)                     # 不喜欢关系的条数
    # 用整数 mask 表示一种分配方式，mask 的第 i 位（0-index）对应第 i+1 个人的组别
    for mask in range(1 << n):            # 0 … 2^n-1
        ok = True
        for a, b in dislikes:             # 遍历所有不喜欢的配对
            # 取出 a、b 的组别（0 或 1），注意 a、b 是 1-index，需要 -1 转成 0-index
            group_a = (mask >> (a - 1)) & 1
            group_b = (mask >> (b - 1)) & 1
            if group_a == group_b:        # 同组则冲突，直接退出当前 mask
                ok = False
                break
        if ok:                             # 找到一种合法划分
            return True
    return False                           # 所有 mask 都不合法
```

#### 复杂度

- **时间复杂度**：`O(2^n * m)`  
  - `2^n` 代表所有可能的「二进制分配」；`m` 代表每次检查所有不喜欢关系。  
  - 当 `n = 20` 时，`2^n ≈ 1,048,576`，已经很难在一秒内跑完，更别提题目上 `n ≤ 2000`。
- **空间复杂度**：`O(1)`  
  - 只用了若干整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有可能的分配**，而实际上我们只需要判断图是否**二分**（bipartite），不必真的列举每一种情况。

把每个人看成图中的一个**节点**，每条「不喜欢」关系 ` [a, b] ` 看成**无向边**，意思是 `a` 与 `b` 必须在不同的组。  
于是问题等价于：

> **给定一个无向图，能否用两种颜色给每个节点涂色，使得相邻的两个节点颜色不同？**

这正是**二分图判定**的经典模型。常用的做法有两种：

1. **DFS / BFS 染色**  
   - 从任意未染色的节点出发，随意把它染成「红」；所有它的邻居必须染成「蓝」；再把蓝色节点的邻居染成红色……层层推进。  
   - 如果在这个过程中发现「已经染色的相邻节点颜色相同」，说明冲突，图不是二分的，返回 `False`。  
   - 否则遍历完所有连通块，返回 `True`。

2. **并查集（Union‑Find）带「相反」概念**  
   - 维护每个人的「自己」和「自己对应的另一组」两个元素。  
   - 当 `a` 与 `b` 必须不同组时，把 `a` 与 `b` 的「另一组」合并，把 `a` 的「另一组」与 `b` 合并。  
   - 若出现「某个人」与「自己的另一组」在同一个集合里，则冲突，返回 `False`。

这里我们选用 **BFS 染色**，因为概念更直观，且实现起来更简洁。下面一步步解释核心概念：

- **图**：把每个人想象成城市，把「不喜欢」想象成两城之间的禁止通行的道路。我们要把城市划分为两块区域，使得相连的城市永远不在同一区域。
- **颜色**：相当于给每块区域贴上「红」或「蓝」的标签。相连的城市必须贴不同颜色的标签。
- **遍历**：从未访问的城市开始，像水波一样向外扩散，给每层城市交替涂色。若某层已经有颜色却需要换成另一种颜色，就说明冲突。

**步骤概览**  

1. **建图**：用邻接表（`defaultdict(list)`）存每个人的“不喜欢”列表。  
2. **颜色数组**：`color[i] = 0` 表示未染色，`1` 表示红，`-1` 表示蓝。  
3. **遍历所有节点**：因为图可能不连通，需要对每个未染色的节点启动一次 BFS。  
4. **BFS 过程**：  
   - 把起始节点设为红 (`1`) 并放入队列。  
   - 取出队首节点 `u`，遍历它的所有邻居 `v`：  
     - 若 `v` 未染色，给它涂成 `-color[u]`（相反颜色），并加入队列。  
     - 若 `v` 已经染色且颜色等于 `color[u]`，说明相邻两人被涂成同色，冲突，直接返回 `False`。  
5. **全部遍历完未出现冲突**，返回 `True`。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def possible_bipartition(n: int, dislikes: List[List[int]]) -> bool:
    """
    使用 BFS 对图进行二分染色，判断是否能划分为两组。
    """
    # 1. 建立邻接表（无向图）
    graph = defaultdict(list)          # key: 人的编号，value: 不喜欢的人的列表
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)             # 因为是无向关系，双向加入

    # 2. 颜色数组，0 表示未访问，1 表示红组，-1 表示蓝组
    color = [0] * (n + 1)               # 1-index，方便直接使用人编号

    # 3. 对每一个可能未被遍历到的连通块进行 BFS
    for person in range(1, n + 1):
        if color[person] != 0:          # 已经染色，说明已经在之前的 BFS 中处理过
            continue

        # 4. 以当前 person 为起点，开始染色（默认红色）
        queue = deque([person])
        color[person] = 1               # 设为红组

        while queue:
            u = queue.popleft()
            for v in graph[u]:          # 遍历 u 的所有“不喜欢”对象
                if color[v] == 0:       # v 还未染色，给它涂相反的颜色
                    color[v] = -color[u]
                    queue.append(v)
                elif color[v] == color[u]:
                    # 相邻的两个节点颜色相同，冲突！不是二分图
                    return False
    # 所有连通块都没有冲突，说明可以二分
    return True
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - `n` 是节点数（人数），`m` 是不喜欢关系的条数。我们只遍历一次所有节点和所有边，就像一次完整的“水波扩散”。相比暴力的 `2^n`，线性时间在 `n ≤ 2000`、`m ≤ 10⁴` 的限制下毫无压力。  
- **空间复杂度**：`O(n + m)`  
  - 用邻接表存图需要 `O(m)` 的空间；颜色数组占 `O(n)`。整体与输入规模同阶。

---

## 心得

- **核心技巧**：把“互斥关系”抽象成**无向图**，判断图是否**二分**（Bipartite）。  
- **适用的题型**：  
  1. **判断图是否二分**（如 LeetCode 886 `Possible Bipartition` 本身）。  
  2. **对立关系分组**（如 LeetCode 785 `Is Graph Bipartite?`、LeetCode 1108 `Path With Maximum Minimum Value` 中的二分思想）。  
  3. **奇偶约束问题**（如 1042 `Flower Planting With No Adjacent` 也可以用二分图思路）。  
- **一句话总结**：**只要把“不能同组”的约束建成图，用两种颜色交替涂，冲突即为“不可能”。**

---

## 反思

- **第一反应**：直接想枚举所有分配（暴力），因为“分两组”看起来像把人“标记为 0/1”。  
- **最容易踩的坑**：  
  - **图不连通**：有可能出现多个互相独立的子图，必须对每个未访问的节点重新启动 BFS/DFS。  
  - **索引错误**：题目编号从 `1` 开始，邻接表和颜色数组也要相应使用 `n+1` 长度，防止把 `0` 当成有效节点。  
  - **重复边**：虽然题目保证唯一，但在构图时仍要小心双向加入导致的重复遍历。  
- **下次遇到同类题**：第一步立刻把“不喜欢”关系写成**邻接表**，判断“是否可以二分”而不是去枚举所有可能的分配。这样思路清晰、实现简洁。