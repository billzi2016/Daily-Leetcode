# #1584. 连接所有点的最小费用 / Min Cost to Connect All Points

> 难度：中等 · 标签：Array、Union Find、Graph、Minimum Spanning Tree · [LeetCode 链接](https://leetcode.com/problems/min-cost-to-connect-all-points/)

---

## 题目（英文原版）

**Description**

You are given an array points representing integer coordinates of some points on a 2D-plane, where points[i] = [xi, yi].
The cost of connecting two points [xi, yi] and [xj, yj] is the manhattan distance between them: |xi - xj| + |yi - yj|, where |val| denotes the absolute value of val.
Return the minimum cost to make all points connected. All points are connected if there is exactly one simple path between any two points.

**Examples**

**Example 1:**

```
Input: points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
Output: 20
Explanation: 

We can connect the points as shown above to get the minimum cost of 20.
Notice that there is a unique path between every pair of points.
```

**Example 2:**

```
Input: points = [[3,12],[-2,5],[-4,1]]
Output: 18
```

**Constraints**

- 1 <= points.length <= 1000
- -106 <= xi, yi <= 106
- All pairs (xi, yi) are distinct.

---

## 题目（中文翻译）

**描述**  
给定一个数组 `points`，其中每个元素表示平面上一个点的整数坐标，`points[i] = [xi, yi]`。  
连接两个点 `[xi, yi]` 与 `[xj, yj]` 的费用为它们之间的曼哈顿距离（Manhattan distance）：`|xi - xj| + |yi - yj|`，其中 `|val|` 表示 `val` 的绝对值。  
返回使所有点都相连的最小费用。若任意两点之间恰好只有唯一的一条简单路径，则称所有点已相连。

**示例 1**  
**输入**: `points = [[0,0],[2,2],[3,10],[5,2],[7,0]]`  
**输出**: `20`  
**解释**:  

我们可以按图示方式连接这些点，得到的最小费用为 20。可以看到，每一对点之间都有唯一的路径。

**示例 2**  
**输入**: `points = [[3,12],[-2,5],[-4,1]]`  
**输出**: `18`

**约束条件**  
- `1 <= points.length <= 1000`  
- `-10^6 <= xi, yi <= 10^6`  
- 所有点 `(xi, yi)` 均互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把所有点两两连接，得到一张完整的无向图：  

* **点** → 图中的**节点**  
* **两点之间的曼哈顿距离** → 这条边的**权重**（费用）  

这相当于在“城市”和“道路”之间建立一张**完整地图**，每条道路的造价就是两座城市的距离。  

现在的问题就变成：**在这张图里挑选若干条道路，使所有城市连通且总造价最小**。这正是**最小生成树（Minimum Spanning Tree，MST）**的定义。  

> **为什么暴力方法能得到正确答案？**  
> 只要把所有可能的边都列出来，然后在这些边中挑选出一棵连接所有点且费用最小的树，就一定满足题目要求。因为 MST 本身就满足“任意两点之间恰好有唯一一条简单路径”。

**实现思路（暴力版）**  

1. 先算出所有点对之间的曼哈顿距离，生成 `edges` 列表。  
2. 把 `edges` 按照距离从小到大排序。  
3. 按顺序遍历 `edges`，使用**并查集（Union‑Find）**判断这条边的两个端点是否已经在同一个连通块里。  
   * 并查集可以类比为“查字典”：词（点）对应的页码（根节点）告诉我们它们是否已经在同一个集合。  
4. 如果两个端点不在同一集合，就把这条边加入答案，同时把两个集合合并（union）。  
5. 重复第 3、4 步，直到已经选了 `n-1` 条边（`n` 为点的数量），此时所有点已经连通。  

#### 代码（Python）

```python
from typing import List

class UnionFind:
    """并查集（Union‑Find）实现，负责维护点的连通关系"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个点最初自己是根
        self.rank = [0] * n            # 用于按秩合并，保持树的高度尽量小

    def find(self, x: int) -> int:
        """寻找 x 的根节点，并做路径压缩（让后面的查找更快）"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归压缩路径
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """把 x、y 所在的集合合并，返回是否真的合并成功"""
        xr, yr = self.find(x), self.find(y)
        if xr == yr:                # 已经在同一个集合，不能再合并
            return False
        # 按秩合并：把秩小的根挂到秩大的根下面
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1
        return True


def minCostConnectPoints_bruteforce(points: List[List[int]]) -> int:
    """暴力 Kruskal 实现——先列出所有边再排序"""
    n = len(points)
    edges = []                               # 存放 (距离, 点i, 点j)

    # 1️⃣ 计算所有点对的曼哈顿距离
    for i in range(n):
        x1, y1 = points[i]
        for j in range(i + 1, n):
            x2, y2 = points[j]
            dist = abs(x1 - x2) + abs(y1 - y2)
            edges.append((dist, i, j))

    # 2️⃣ 按距离从小到大排序
    edges.sort(key=lambda e: e[0])

    uf = UnionFind(n)
    total = 0          # 累计已选边的总费用
    used = 0           # 已经选了多少条边

    # 3️⃣ 按序尝试加入每条边
    for dist, i, j in edges:
        if uf.union(i, j):          # 如果两点不在同一集合，就把这条边加入 MST
            total += dist
            used += 1
            if used == n - 1:       # 已经连通所有点，提前结束
                break
    return total
```

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - 计算所有点对距离需要 `n·(n‑1)/2 ≈ O(n²)` 次操作。  
  - 排序 `edges` 列表的时间是 `O(m log m)`，其中 `m = n·(n‑1)/2`，所以整体是 `O(n² log n²) = O(n² log n)`。  
  - “log n” 就是把 “对数” 这件事形象化：当数据量翻倍时，排序的额外工作只会稍微多一点（大约再多 `log2` 次比较），而不是成倍增长。  

- **空间复杂度**：`O(n²)`  
  - 需要存储所有的边（约 `n²/2` 条），所以空间随点的数量呈二次方增长。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“列出所有边并排序”** 这一步：当点的数量达到 1000 时，`n²` 已经是 10⁶ 条边，排序会消耗不少时间和内存。  

其实我们并不需要一次性把所有边都准备好，只要**每次挑选当前还能加入的最小费用的边** 即可。这正是 **Prim 算法** 的核心思想：

1. 任意挑选一个起点（比如第 0 个点），把它加入已连通的集合 `S`。  
2. 对于所有不在 `S` 中的点，记录它们到集合 `S` 的**最近距离**（即最小的曼哈顿距离）。  
3. 每次从这些“候选点”里挑选距离最小的那个点加入 `S`，并把这条距离累加到答案中。  
4. 加入新点后，重新更新剩余点到 `S` 的最近距离（如果新点更近，就替换掉旧的记录）。  
5. 重复步骤 2‑4，直到所有点都在 `S` 中。

> **为什么 Prim 能快？**  
> 它只维护 `n` 条“最近距离”，而不是 `n²` 条完整的边。每加入一个点，只需要遍历一次所有未加入的点来更新距离，整体是 `O(n²)` 的时间且只用 `O(n)` 的额外空间。

**数据结构说明**  

- **数组 `minDist[i]`**：记录点 `i`（如果还未加入 `S`）到已连通集合 `S` 的最近距离。可以把它想象成“每个城市到已经建好高速公路网络的最近出入口的距离”。  
- **布尔数组 `in_mst[i]`**：标记点 `i` 是否已经在生成树 `S` 中。  

如果想把 “挑选最小距离的点” 这一步再提速，可以用**最小堆**（priority queue），但在本题 `n ≤ 1000` 时，直接线性扫描 `minDist` 已经足够快，代码更简洁。

#### 代码（Python）

```python
from typing import List

def minCostConnectPoints(points: List[List[int]]) -> int:
    """
    Prim 算法（无需显式构造所有边）实现最小生成树。
    时间复杂度 O(n^2)，空间复杂度 O(n)。
    """
    n = len(points)
    # 记录每个点到已构造树的最小距离，初始设为无限大
    INF = 10 ** 9
    minDist = [INF] * n
    in_mst = [False] * n          # 是否已经被加入生成树

    # 任意选第 0 个点作为起点，距离设为 0，保证第一次一定被选中
    minDist[0] = 0
    total_cost = 0                # 累计答案

    for _ in range(n):
        # 1️⃣ 选出当前未加入且距离最小的点
        cur = -1
        cur_dist = INF
        for i in range(n):
            if not in_mst[i] and minDist[i] < cur_dist:
                cur = i
                cur_dist = minDist[i]

        # 2️⃣ 将该点加入生成树
        in_mst[cur] = True
        total_cost += cur_dist     # 第一次加入的点距离为 0，不影响答案

        # 3️⃣ 更新其余未加入点到生成树的最近距离
        x_cur, y_cur = points[cur]
        for j in range(n):
            if not in_mst[j]:
                x_j, y_j = points[j]
                dist = abs(x_cur - x_j) + abs(y_cur - y_j)
                if dist < minDist[j]:
                    minDist[j] = dist   # 找到更近的入口，更新记录

    return total_cost
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环执行 `n` 次，每次要遍历全部 `n` 个点找最小 `minDist`（`O(n)`），再遍历一次所有未加入的点更新距离（`O(n)`），所以总体是 `n·2·O(n) = O(n²)`。  
  - 与暴力解的 `O(n² log n)` 相比，去掉了排序的对数因子，运行更快。  

- **空间复杂度**：`O(n)`  
  - 只用了 `minDist`、`in_mst` 两个长度为 `n` 的数组，以及常数级的临时变量。相比暴力解的 `O(n²)` 边表，节省了大量内存。  

---

## 心得  

- **核心技巧**：**最小生成树（MST）**，特别是 **Prim 算法** 的“逐点扩张 + 最近距离维护”。  
- **该技巧适用的题型**：  
  1. **连接所有岛屿的最小费用**（LeetCode 1168 – Optimize Water Distribution）。  
  2. **构造城市网络的最低成本**（LeetCode 1584 – Min Cost to Connect All Points，正是本题）。  
  3. **在平面上搭建光纤网络**（类似的几何 MST 题目）。  
- **一句话总结解题钥匙**：把“所有点两两相连的完整图”想象成“城市 + 所有可能的道路”，然后用 **Prim** 按“最近的道路”一步步扩展网络，即可得到最小花费。

---

## 反思  

- **第一反应**：把所有点对的距离算出来，直接做 **Kruskal**（排序所有边）——这是一种“先把所有道路画好再挑选”的思路。  
- **最容易踩的坑**：  
  - **曼哈顿距离**的计算要使用绝对值 `abs`，别忘了加上 `|yi - yj|`。  
  - **边界条件**：点的数量可能只有 1，答案应为 0，代码要能处理 `n = 1` 的情况（本实现自然返回 0）。  
  - **整数溢出**：在 Python 中不存在，但如果用其他语言，要注意距离可能达到 `2·10⁶`，累加后仍在 32 位整数范围内。  
- **下次类似题的第一步**：先判断是否可以直接使用 **Prim**（只需要维护每个未连接点到已连接集合的最小代价），而不是先把所有边都列出来。这样往往能省去排序的时间和大量内存。