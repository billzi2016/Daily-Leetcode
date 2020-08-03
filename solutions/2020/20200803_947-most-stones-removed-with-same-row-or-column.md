# #947. 同一行或同一列可移除的最多石子数 / Most Stones Removed with Same Row or Column

> 难度：中等 · 标签：Hash Table、Depth-First Search、Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/)

---

## 题目（英文原版）

**Description**

On a 2D plane, we place n stones at some integer coordinate points. Each coordinate point may have at most one stone.
A stone can be removed if it shares either the same row or the same column as another stone that has not been removed.
Given an array stones of length n where stones[i] = [xi, yi] represents the location of the ith stone, return the largest possible number of stones that can be removed.

**Examples**

**Example 1:**

```
Input: stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
Output: 5
Explanation: One way to remove 5 stones is as follows:
1. Remove stone [2,2] because it shares the same row as [2,1].
2. Remove stone [2,1] because it shares the same column as [0,1].
3. Remove stone [1,2] because it shares the same row as [1,0].
4. Remove stone [1,0] because it shares the same column as [0,0].
5. Remove stone [0,1] because it shares the same row as [0,0].
Stone [0,0] cannot be removed since it does not share a row/column with another stone still on the plane.
```

**Example 2:**

```
Input: stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
Output: 3
Explanation: One way to make 3 moves is as follows:
1. Remove stone [2,2] because it shares the same row as [2,0].
2. Remove stone [2,0] because it shares the same column as [0,0].
3. Remove stone [0,2] because it shares the same row as [0,0].
Stones [0,0] and [1,1] cannot be removed since they do not share a row/column with another stone still on the plane.
```

**Example 3:**

```
Input: stones = [[0,0]]
Output: 0
Explanation: [0,0] is the only stone on the plane, so you cannot remove it.
```

**Constraints**

- 1 <= stones.length <= 1000
- 0 <= xi, yi <= 104
- No two stones are at the same coordinate point.

---

## 题目（中文翻译）

在二维平面（2D plane）上，我们在若干整数坐标点放置 **n** 颗石子（stone）。每个坐标点至多放置一颗石子。  
如果一颗石子与另一颗仍未被移除的石子共享同一行（row）或同一列（column），则可以将该石子移除。  
给定长度为 **n** 的数组 `stones`，其中 `stones[i] = [xi, yi]` 表示第 **i** 颗石子的坐标，返回最多可以移除的石子数量。

### 示例

#### 示例 1
**输入**  
```json
stones = [[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]
```
**输出**  
```
5
```
**解释**  
一种移除 5 颗石子的方法如下：
1. 移除石子 `[2,2]`，因为它与 `[2,1]` 共享同一行。  
2. 移除石子 `[2,1]`，因为它与 `[0,1]` 共享同一列。  
3. 移除石子 `[1,2]`，因为它与 `[1,0]` 共享同一行。  
4. 移除石子 `[1,0]`，因为它与 `[0,0]` 共享同一列。  
5. 移除石子 `[0,1]`，因为它与 `[0,0]` 共享同一行。  

石子 `[0,0]` 无法被移除，因为此时它不再与平面上其他任何石子共享行或列。

#### 示例 2
**输入**  
```json
stones = [[0,0],[0,2],[1,1],[2,0],[2,2]]
```
**输出**  
```
3
```
**解释**  
一种实现 3 步的方案如下：
1. 移除石子 `[2,2]`，因为它与 `[2,0]` 共享同一行。  
2. 移除石子 `[2,0]`，因为它与 `[0,0]` 共享同一列。  
3. 移除石子 `[0,2]`，因为它与 `[0,0]` 共享同一行。  

石子 `[0,0]` 和 `[1,1]` 无法被移除，因为它们不再与平面上其他任何石子共享行或列。

#### 示例 3
**输入**  
```json
stones = [[0,0]]
```
**输出**  
```
0
```
**解释**  
`[0,0]` 是平面上唯一的一颗石子，无法移除。

### 约束条件
- `1 <= stones.length <= 1000`
- `0 <= xi, yi <= 10^4`
- 没有两颗石子位于相同的坐标点。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**模拟所有可能的移除顺序**，每一次挑选一块可以被移除的石头（即它所在的行或列上还有其他石头），把它从平面上删掉，然后继续递归。  
- **数据结构**：用一个 `set` 保存当前还在平面上的石头坐标，`set` 就像一本“字典”，可以把坐标当作“单词”，快速判断某个坐标是否存在。  
- **为什么正确**：只要我们遍历了**所有**合法的移除顺序，必然能找到能够移除最多石头的那条路径，答案就是最大的移除次数。  

然而，这种做法的**瓶颈**在于：  
- 每一次递归都要遍历全部石头去找可移除的，那是 **O(n)** 的工作。  
- 石头的数量最多 1000，递归深度最多也是 1000，所有可能的移除顺序的数量是指数级的（类似 `2^n`），根本不可在 1 秒内算完。  

#### 代码（Python）  

```python
from typing import List, Set, Tuple

def removeStones_bruteforce(stones: List[List[int]]) -> int:
    # 把列表转成 set，方便 O(1) 判断是否存在
    stone_set: Set[Tuple[int, int]] = {tuple(p) for p in stones}
    n = len(stones)

    # 记录已经移除的最大数量
    best = 0

    def dfs(cur_set: Set[Tuple[int, int]], removed: int) -> None:
        nonlocal best
        # 每走到这里，就已经得到一种合法的移除方案
        best = max(best, removed)

        # 逐个尝试把还能移除的石头删掉
        for x, y in list(cur_set):                # 把 set 转成 list 防止遍历时修改
            # 判断 (x, y) 是否还有同行或同列的石头
            has_same = any((x, yy) in cur_set for yy in range(0, 10001) if yy != y) \
                    or any((xx, y) in cur_set for xx in range(0, 10001) if xx != x)
            # 实际上这里的检查非常慢，下面的实现只演示思路
            if not has_same:
                continue
            # 删除当前石头，递归继续
            cur_set.remove((x, y))
            dfs(cur_set, removed + 1)
            # 回溯：把石头放回去
            cur_set.add((x, y))

    dfs(stone_set, 0)
    return best
```

> **注意**：上面的 `has_same` 检查用了遍历所有可能的行/列，只是为了把“暴力”思路写得完整。实际运行会非常慢，甚至会因递归深度超限而崩溃。  

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`（指数级）。  
  - “`2^n`” 表示所有可能的石头移除子集；每一次递归内部还要遍历 `n` 个石头去找可移除的。  
  - 用大白话说，就是“石头越多，时间会像翻倍一样飞速增长”，根本不可能在 1 秒内跑完。  
- **空间复杂度**：`O(n)`（递归栈 + `set`）。  

---

### 2. 最优解  

#### 思路  

**从暴力解出发**，我们发现**唯一真正耗时的地方**是：每次都要去“寻找同行或同列的石头”。如果能一次性把“同行/同列关系”全部记录下来，就不需要在递归里反复搜索了。  

观察题目可以得到以下关键点：  

1. **石头之间的可移除关系其实构成了一个无向图**。  
   - 两块石头如果在同一行或同一列，它们之间就有一条边。  
   - 只要一块石头还能和图中其它石头相连，就可以最终被移除（只剩下图中每个连通分量的一个根节点）。  

2. **每个连通分量最多只能保留一块石头**。  
   - 想象把所有连在一起的石头视作“一堆”。只要还有两块以上的石头在同一堆里，就一定能挑出一块和其它石头同排/同列并把它删掉，直到只剩下最后一块。  
   - 因此 **答案 = 总石头数 - 连通分量的数量**。  

3. **如何快速求连通分量**？  
   - **并查集（Union‑Find）** 是专门用来维护“哪些元素在同一个集合” 的数据结构，支持 `union(a,b)` 合并集合，`find(a)` 找根节点，均摊时间几乎是 O(1)。  
   - 这里的“元素”可以是行坐标或列坐标。我们把行 `x` 当作一个节点，列 `y` 当作另一个节点。为了避免行号和列号冲突（比如 `x=1` 与 `y=1` 会被误认为同一个节点），我们把列的编号整体向右平移一个很大的偏移量（如 `10^4 + 1`），这相当于在“行”和“列”之间画了一道“防护墙”。  

4. **并查集的并合过程**：  
   - 对每块石头 `[x, y]`，把 `x`（行）和 `y + OFFSET`（列）合并到同一个集合。  
   - 最后遍历所有出现过的节点，统计有多少不同的根节点，这就是连通分量的数量。  

5. **为什么还能用哈希表**：  
   - 我们只需要记录出现过的行号和列号，数量至多是 `2 * n`（因为每块石头贡献一个行和一个列），用字典（哈希表）存储 `parent` 完全可以。  

**类比**：把每一行想象成一本书的“章节”，每一列想象成一本书的“页码”。一块石头把它所在的章节和页码用一根绳子系在一起。所有被绳子间接相连的章节/页码形成一条“大链”。每条大链只能保留最后一块石头，其他都能被拔掉。  

#### 代码（Python）  

```python
from typing import List

class UnionFind:
    """并查集（Union‑Find）实现，内部用 dict 存储父节点"""
    def __init__(self):
        self.parent = {}          # key: 节点，value: 其父节点
        self.rank = {}            # 用来做按秩合并，保持树的高度低

    def find(self, x):
        """寻找根节点，并路径压缩"""
        if self.parent[x] != x:
            # 递归找根的同时，把路径上的节点直接指向根，后面查找会更快
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        """把 x、y 所在的集合合并"""
        # 若节点还未出现，先把它们初始化为自己
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
        if y not in self.parent:
            self.parent[y] = y
            self.rank[y] = 0

        xr, yr = self.find(x), self.find(y)
        if xr == yr:               # 已经在同一个集合，无需合并
            return

        # 按秩合并：把秩小的树挂到秩大的树下面
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1    # 秩相同的情况下，挂完后根的秩加 1

def removeStones(stones: List[List[int]]) -> int:
    """
    最优解：使用并查集 + 哈希表
    思路：把每个行坐标 x 当作一个节点，把每个列坐标 y 当作另一个节点（偏移后）。
    对每块石头 [x, y] 执行 union(x, y+OFFSET)。
    最后不同根的数量 = 连通分量的个数，答案 = n - components。
    """
    OFFSET = 10 ** 4 + 1          # 列坐标整体右移，防止与行坐标冲突
    uf = UnionFind()

    for x, y in stones:
        uf.union(x, y + OFFSET)   # 把行节点和列节点连在一起

    # 统计出现过的所有节点的根节点数量
    roots = set()
    for x, y in stones:
        roots.add(uf.find(x))
        roots.add(uf.find(y + OFFSET))

    components = len(roots)       # 连通分量的个数
    return len(stones) - components

# ------------------- 示例测试 -------------------
if __name__ == "__main__":
    print(removeStones([[0,0],[0,1],[1,0],[1,2],[2,1],[2,2]]))  # 5
    print(removeStones([[0,0],[0,2],[1,1],[2,0],[2,2]]))      # 3
    print(removeStones([[0,0]]))                              # 0
```

> **代码要点注释**  
> - `OFFSET` 把列坐标平移，防止 `x = 1` 与 `y = 1` 被误认为同一个节点。  
> - `union` 时如果节点之前没有出现，先把它们初始化为自己的根。  
> - `find` 中的“路径压缩”让后续查询几乎是 O(1)。  

#### 复杂度  

- **时间复杂度**：`O(n * α(n))`，其中 `α` 为 Ackermann 函数的反函数，几乎可以看作常数。  
  - 解释：我们遍历每块石头一次，执行 `union`（几乎 O(1)），再遍历一次收集根节点。整体线性随石头数量增长。  
- **空间复杂度**：`O(n)`，因为我们最多存储 `2 * n` 个节点（每块石头的行和列各一个）以及它们的父指针和秩。  

---

## 心得  

- **核心技巧**：把“同行/同列”关系抽象成 **图的连通分量**，使用 **并查集（Union‑Find）** 快速求出连通块的数量。  
- **适用的题型**  
  1. “相同属性连通”类问题，如 **LeetCode 261. Graph Valid Tree**（判断树的连通性）  
  2. “同一行/列/颜色/字母”等可以视为 **等价关系** 的题目，如 **LeetCode 200. Number of Islands**（岛屿计数）可以用并查集或 DFS。  
  3. “把二维坐标映射到一维节点” 的场景，如 **LeetCode 839. Similar String Groups**（相似字符串分组）。  
- **一句话总结解题钥匙**：**把每块石头看成把行号和列号绑在一起的绳子，所有相互绑住的石头形成一个连通块，答案 = 总石头数 - 连通块数**。  

---

## 反思  

- **第一反应**：看到“同一行或同一列可以移除”，自然会想到 **图的遍历**（DFS/BFS）来找连通块。  
- **最容易踩的坑**  
  1. **行列编号冲突**：直接把行 `x` 与列 `y` 当成同一集合的节点会导致错误，需要把列整体偏移（如 `OFFSET = 10^4+1`）。  
  2. **忘记把所有出现的节点都加入集合**：仅统计根节点时要确保行、列都被 `find` 一遍，否则会少算连通块。  
  3. **递归深度**：如果使用 DFS 递归，需要注意 Python 默认递归深度（约 1000），在极端情况下可能需要 `sys.setrecursionlimit`。  
- **下次类似题的第一步**：先把 **“相同属性”** 抽象成 **等价关系**，决定是用 **并查集**（快速合并）还是 **DFS/BFS**（更直观），再统一处理。