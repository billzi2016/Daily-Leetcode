# #2924. 寻找冠军 II / Find Champion II

> 难度：中等 · 标签：Graph · [LeetCode 链接](https://leetcode.com/problems/find-champion-ii/)

---

## 题目（英文原版）

**Description**

There are n teams numbered from 0 to n - 1 in a tournament; each team is also a node in a DAG.
You are given the integer n and a 0-indexed 2D integer array edges of length m representing the DAG, where edges[i] = [ui, vi] indicates that there is a directed edge from team ui to team vi in the graph.
A directed edge from a to b in the graph means that team a is stronger than team b and team b is weaker than team a.
Team a will be the champion of the tournament if there is no team b that is stronger than team a.
Return the team that will be the champion of the tournament if there is a unique champion, otherwise, return -1.
Notes

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1],[1,2]]
Output: 0
Explanation: Team 1 is weaker than team 0. Team 2 is weaker than team 1. So the champion is team 0.
```

**Example 2:**

```
Input: n = 4, edges = [[0,2],[1,3],[1,2]]
Output: -1
Explanation: Team 2 is weaker than team 0 and team 1. Team 3 is weaker than team 1. But team 1 and team 0 are not weaker than any other teams. So the answer is -1.
```

**Constraints**

- 1 <= n <= 100
- m == edges.length
- 0 <= m <= n * (n - 1) / 2
- edges[i].length == 2
- 0 <= edge[i][j] <= n - 1
- edges[i][0] != edges[i][1]
- The input is generated such that if team a is stronger than team b, team b is not stronger than team a.
- The input is generated such that if team a is stronger than team b and team b is stronger than team c, then team a is stronger than team c.

---

## 题目（中文翻译）

**描述**  
有 `n` 支球队，编号为 `0` 到 `n - 1`，每支球队在锦标赛中对应图中的一个节点，且该图是有向无环图（DAG）。  
给定整数 `n` 和一个长度为 `m` 的 0 索引二维整数数组 `edges`，其中 `edges[i] = [ui, vi]` 表示图中存在一条从球队 `ui` 指向球队 `vi` 的有向边。  

图中的有向边 `a → b` 表示球队 `a` 比球队 `b` 更强，球队 `b` 比球队 `a` 更弱。  
如果不存在任何球队 `b` 比球队 `a` 更强，则球队 `a` 将成为锦标赛的冠军。  

返回唯一的冠军球队编号；如果不存在唯一冠军，则返回 `-1`。

**示例 1**  
**输入**: `n = 3, edges = [[0,1],[1,2]]`  
**输出**: `0`  
**解释**: 球队 `1` 比球队 `0` 弱。球队 `2` 比球队 `1` 弱。因此冠军是球队 `0`。

**示例 2**  
**输入**: `n = 4, edges = [[0,2],[1,3],[1,2]]`  
**输出**: `-1`  
**解释**: 球队 `2` 同时比球队 `0` 和球队 `1` 弱。球队 `3` 比球队 `1` 弱。但球队 `1` 和球队 `0` 都没有比它们更强的球队。所以不存在唯一冠军，答案为 `-1`。

**约束条件**  
- `1 <= n <= 100`  
- `m == edges.length`  
- `0 <= m <= n * (n - 1) / 2`  
- `edges[i].length == 2`  
- `0 <= edges[i][j] <= n - 1`  
- `edges[i][0] != edges[i][1]`  
- 输入保证若球队 `a` 比球队 `b` 强，则球队 `b` 不会比球队 `a` 强。  
- 输入保证若球队 `a` 比球队 `b` 强且球队 `b` 比球队 `c` 强，则球队 `a` 必定比球队 `c` 强。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每支队伍都当成“可能的冠军”，逐个检查它是否真的没有比它更强的队伍**。  
具体做法：

1. 对于编号 `i`（`0 … n-1`）遍历所有边 `edges`。  
2. 如果在任意一条边 `[u, v]` 中出现 `v == i`，说明有队伍 `u` 比 `i` 强，`i` 不能是冠军。  
3. 若遍历完所有边都没有发现 `v == i`，则 `i` 的入度（指向它的边数）为 `0`，它就是“潜在冠军”。  
4. 把所有满足条件的 `i` 收集起来，最后判断是否只有 **唯一** 一个。如果唯一，返回它的编号；否则返回 `-1`。

> **类比**：把 `edges` 看成一本词典，词条是“谁比谁强”。要判断某个词条（队伍）是否“没有前面的词条”（没有更强的队伍），只能把整本词典逐页翻阅，看看有没有指向它的条目。

**正确性**：  
如果一支队伍 `i` 没有任何指向它的有向边，则不存在任何 `u` 使得 `u → i`，即没有队伍比 `i` 强，满足题目“没有比它更强的队伍”。反之，若存在一条 `u → i`，则 `i` 必然被 `u` 强于，不能是冠军。于是遍历所有 `i` 并检查是否有入边，恰好找出所有“入度为 0”的节点。

**复杂度**：  
- **时间**：我们对每支队伍 (`n` 次) 都遍历一遍全部边 (`m` 条)，所以是 `O(n·m)`。  
  - 举例来说，若 `n = 100`、`m = 4950`（完全有向无环图的最大边数），最坏需要检查 `100 × 4950 ≈ 5×10⁵` 次，仍在可接受范围，但不是最优的。  
- **空间**：只用了常数级别的额外变量（计数器、结果列表），即 `O(1)`。

#### 代码（Python）

```python
from typing import List

def findChampion_bruteforce(n: int, edges: List[List[int]]) -> int:
    candidates = []                     # 用来保存所有入度为 0 的队伍

    # 对每支队伍 i 检查是否有指向它的边
    for i in range(n):
        has_stronger = False            # 标记 i 是否被别的队伍强于

        # 逐条遍历所有有向边
        for u, v in edges:
            if v == i:                  # 找到一条 u -> i，说明 u 更强
                has_stronger = True
                break                   # 已经知道 i 不是冠军，提前退出内层循环

        if not has_stronger:            # 没有任何入边，i 可能是冠军
            candidates.append(i)

    # 必须唯一才能返回，否则返回 -1
    return candidates[0] if len(candidates) == 1 else -1
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  - “n” 代表要检查的队伍数，“m” 代表要遍历的边数。把每支队伍和所有边都配对检查，就是乘法的意思。
- **空间复杂度**：`O(1)`（不计返回值的 `candidates` 列表）  
  - 只用了几个整数变量，没有额外的随 `n` 或 `m` 增长的数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复遍历所有边**：对每支队伍都要重新扫描一遍 `edges`。  
其实我们只需要 **一次遍历** 就能知道每支队伍的入度（有多少条边指向它），因为每条边只会贡献一次入度。  

优化步骤：

1. **一次遍历** `edges`，构造一个长度为 `n` 的数组 `indeg`，`indeg[v]` 记录指向 `v` 的边数。  
   - 这相当于在词典里一次性把每个词条的“被引用次数”统计出来，类似 **哈希表**（字典）里记录每个单词出现的次数，只是这里用数组下标直接对应队伍编号。  
2. 扫描 `indeg`，找出所有值为 `0` 的下标，这些就是 **入度为 0** 的队伍。  
3. 如果恰好只有一个下标满足条件，返回它；否则返回 `-1`。

**为什么一次遍历就够了？**  
每条有向边 `[u, v]` 只会影响 **唯一** 的目标节点 `v` 的入度。把所有边的贡献累加到 `indeg` 中，就等价于把所有“谁比谁强”的信息压缩成了每个节点的“被强于次数”。因此不需要再对每个节点单独去找它的入边。

#### 代码（Python）

```python
from typing import List

def findChampion_optimal(n: int, edges: List[List[int]]) -> int:
    indeg = [0] * n                     # indeg[i] 表示指向 i 的边数（入度）

    # 只遍历一次 edges，统计每个节点的入度
    for u, v in edges:
        indeg[v] += 1                   # v 被 u 强于一次，入度加 1

    champions = [i for i in range(n) if indeg[i] == 0]   # 收集所有入度为 0 的队伍

    # 必须唯一才能返回，否则返回 -1
    return champions[0] if len(champions) == 1 else -1
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - 只遍历一次 `edges`（`m` 条）来填充 `indeg`，再遍历一次长度为 `n` 的数组找零入度。  
  - 与暴力解的 `O(n·m)` 相比，规模大时差距非常明显（比如 `n=100, m=4950` 时，`n+m≈5050` vs `n·m≈5×10⁵`）。
- **空间复杂度**：`O(n)`  
  - 需要一个大小为 `n` 的 `indeg` 数组来保存每支队伍的入度信息。`n` 最多 100，几乎可以忽略不计。

---

## 心得

- **核心技巧**：利用 **入度**（in‑degree）判断 DAG 中的“源点”。在有向无环图里，**没有入边的节点** 正好对应“没有比它更强的队伍”。  
- **适用的题型**  
  1. **寻找唯一源点 / 受控节点**（如 LeetCode 1582 “找出所有的孤独节点”）。  
  2. **拓扑排序的起点**（判断是否存在唯一的拓扑序列起点）。  
  3. **判断图中是否存在唯一的“最强”或“最弱”元素**（如找出唯一的“老板”或“根节点”）。  
- **一句话总结**：**“只要统计每个节点的入度，零入度即是潜在冠军，唯一才算真正冠军”。**

---

## 反思

- **第一反应**：看到“有向无环图”和“没有比它强的队伍”，立刻想到 **入度为 0** 的节点，因为入度正好表示“有多少比它强”。  
- **最容易踩的坑**  
  - **未判断唯一性**：即使有多个入度为 0 的节点，也不能直接返回其中一个，需要返回 `-1`。  
  - **边界条件**：`m = 0` 时，所有节点入度都是 0，答案必然是 `-1`（因为不唯一）。  
  - **误把出度当入度**：出度表示“它强于多少人”，但题目要求的是“没有比它强的人”。  
- **下次遇到同类题**：第一步先 **统计入度**（或出度），随后检查 **是否只有唯一的零入度（或零出度）** 节点。这样思路清晰，代码也自然简洁。