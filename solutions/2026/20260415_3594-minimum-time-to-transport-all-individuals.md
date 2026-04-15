# #3594. 运输所有人员的最短时间 / Minimum Time to Transport All Individuals

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Graph、Heap (Priority Queue)、Shortest Path、Bitmask · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-transport-all-individuals/)

---

## 题目（英文原版）

**Description**

You are given n individuals at a base camp who need to cross a river to reach a destination using a single boat. The boat can carry at most k people at a time. The trip is affected by environmental conditions that vary cyclically over m stages.
Each stage j has a speed multiplier mul[j]:
Each individual i has a rowing strength represented by time[i], the time (in minutes) it takes them to cross alone in neutral conditions.
Rules:
Return the minimum total time required to transport all individuals. If it is not possible to transport all individuals to the destination, return -1.

**Examples**

**Example 1:**

```
Input: n = 1, k = 1, m = 2, time = [5], mul = [1.0,1.3]
Output: 5.00000
Explanation:
```

**Example 2:**

```
Input: n = 3, k = 2, m = 3, time = [2,5,8], mul = [1.0,1.5,0.75]
Output: 14.50000
Explanation:
The optimal strategy is:
```

**Example 3:**

```
Input: n = 2, k = 1, m = 2, time = [10,10], mul = [2.0,2.0]
Output: -1.00000
Explanation:
```

**Constraints**

- 1 <= n == time.length <= 12
- 1 <= k <= 5
- 1 <= m <= 5
- 1 <= time[i] <= 100
- m == mul.length
- 0.5 <= mul[i] <= 2.0

---

## 题目（中文翻译）

**题目描述**  
你有 `n` 名待在营地的个人，需要使用一只单独的船把他们运送到对岸的目的地。船一次最多只能承载 `k` 人。船行进的速度会受到循环变化的环境条件影响，共有 `m` 个阶段。

- 第 `j` 个阶段有一个速度倍率 `mul[j]`（speed multiplier）。
- 第 `i` 个人的划船能力用 `time[i]` 表示，即在中性条件下他单独划船通过的时间（分钟）。

**要求**  
返回将所有个人全部运送到目的地所需的最小总时间。如果无法把所有个人运送到对岸，返回 `-1`。

**示例**

**示例 1**  
```
Input: n = 1, k = 1, m = 2, time = [5], mul = [1.0,1.3]
Output: 5.00000
Explanation:
```

**示例 2**  
```
Input: n = 3, k = 2, m = 3, time = [2,5,8], mul = [1.0,1.5,0.75]
Output: 14.50000
Explanation:
The optimal strategy is:
```

**示例 3**  
```
Input: n = 2, k = 1, m = 2, time = [10,10], mul = [2.0,2.0]
Output: -1.00000
Explanation:
```

**约束条件**  

- `1 <= n == time.length <= 12`
- `1 <= k <= 5`
- `1 <= m <= 5`
- `1 <= time[i] <= 100`
- `m == mul.length`
- `0.5 <= mul[i] <= 2.0`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题的本质是把 **人** 从左岸运到右岸，船一次最多坐 `k` 个人，环境的“风速倍率”会每趟轮流在 `mul[0] … mul[m‑1]` 循环出现。  
最直接的想法就是 **把所有可能的运送顺序枚举出来**，逐个算出总耗时，最后取最小值。

- **状态**：用一个二进制掩码 `mask` 表示已经在右岸的人员。`mask` 的第 `i` 位为 `1` 表示第 `i` 个人已经到达目的地。因为 `n ≤ 12`，所以最多只有 `2¹² = 4096` 种不同的 `mask`。  
- **当前阶段**：因为倍率是循环的，需要记住当前正处于第几阶段（`stage ∈ [0, m‑1]`），这相当于在 **时间轴上走了多少趟**。  
- **一次完整的往返**：  
  1. **去程**：从左岸挑选 `1 … k` 个人（记为集合 `S`）坐船过去。去程的耗时 = `max(time[i] for i∈S) * mul[stage]`（最慢的那个人决定船速）。  
  2. **如果已经把所有人运完**，则不需要回程，直接结束。  
  3. **回程**：必须让船回到左岸继续接人，回程可以让已经在右岸的 `1 … k` 个人（记为集合 `T`）划船回去，耗时 = `max(time[i] for i∈T) * mul[(stage+1) % m]`。  
  4. **阶段递增**：每走完一次去程或回程，`stage` 向后移动一位（取模 `m`），因为倍率是循环的。  

把上述过程一直递归下去，遍历 **所有** 合法的 `S`、`T` 组合，就能得到每一种运送方案的总时间。

> **生活化类比**：  
> - `mask` 就像一本“人员登记册”，每翻一页（0/1）就代表这位同学是否已经到达终点。  
> - `stage` 类似于天气预报的“今天/明天/后天”循环，决定了船在这趟的“风速”。  

只要把所有可能的 `S`、`T` 组合都尝试一次，必然能找到最优解——因为我们没有遗漏任何合法的搬运顺序。

#### 代码（Python）

```python
import itertools
import math
from functools import lru_cache

def minTime_bruteforce(n, k, m, time, mul):
    ALL = (1 << n) - 1                      # 所有人员都在右岸的 mask
    INF = float('inf')

    @lru_cache(None)
    def dfs(mask, stage):
        """返回从当前状态 (mask, stage) 把剩余人员全部运完的最小时间。
           mask: 已经在右岸的人员集合（二进制），船在左岸。
        """
        if mask == ALL:                     # 所有人已经到达终点
            return 0.0

        best = INF

        # ---------- 去程：从左岸挑选 S ----------
        left_people = [i for i in range(n) if not (mask >> i) & 1]
        # 至少要挑选一个人，否则船无法前进
        for sz in range(1, min(k, len(left_people)) + 1):
            for S in itertools.combinations(left_people, sz):
                # 去程耗时 = 最慢的那个人的单独时间 × 当前倍率
                cost_go = max(time[i] for i in S) * mul[stage]

                new_mask = mask
                for i in S:                  # 把这些人搬到右岸
                    new_mask |= 1 << i

                # 如果已经全部运完，则不必回程
                if new_mask == ALL:
                    best = min(best, cost_go)
                    continue

                # ---------- 回程：从右岸挑选 T ----------
                right_people = [i for i in range(n) if (new_mask >> i) & 1]
                for sz2 in range(1, min(k, len(right_people)) + 1):
                    for T in itertools.combinations(right_people, sz2):
                        # 回程耗时 = 最慢的那个人的单独时间 × 下一阶段倍率
                        cost_back = max(time[i] for i in T) * mul[(stage + 1) % m]
                        # 递归进入下一个状态，阶段已经向后走了两步
                        total = cost_go + cost_back + dfs(new_mask, (stage + 2) % m)
                        best = min(best, total)

        return best

    ans = dfs(0, 0)
    return -1.0 if math.isinf(ans) else ans
```

> **关键行中文注释** 已经写在代码里，帮助你快速定位每一步的意义。  

#### 复杂度  

- **时间复杂度**：  
  - 对每个 `mask`（最多 `2ⁿ` 种）我们都要尝试所有合法的去程组合 `S`（至多 `C(n,1)+…+C(n,k) ≤ k·C(n,k)`）以及对应的回程组合 `T`。  
  - 粗略估计：`O( 2ⁿ * (C(n,k))² )`。  
  - 当 `n=12、k=5` 时，这个数已经接近 **几千万**，在 Python 中会超时。  
- **空间复杂度**：  
  - 递归记忆化表保存 `mask × stage` 的结果，大小为 `2ⁿ * m ≤ 4096 * 5 ≈ 2·10⁴`，即 **O(2ⁿ·m)**，非常小。  

> **大白话解释**：  
> - `O(2ⁿ)` 就像把所有可能的“谁已经到达终点”的情况列出来，人数多一点，情况就会翻倍增长。  
> - `C(n,k)` 是从 `n` 个人里挑 `k` 个人的组合数，想象成从一堆球里挑出最多 `k` 球的所有方式。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到两点 **瓶颈**：

1. **大量重复计算**：相同的 `(mask, stage)` 会被不同的路径反复访问，虽然记忆化缓存了一次，但仍然需要遍历所有组合 `S`、`T`，导致指数级的枚举。  
2. **每一次“去‑回”都被当作一次完整的转移**，实际上这两步可以拆成两条 **有向边**：  
   - **去程边**：`(mask, stage) → (mask∪S, (stage+1)%m)`，权重 = `max(time[i] for i∈S) * mul[stage]`。  
   - **回程边**：`(mask, stage) → (mask∖T, (stage+1)%m)`，权重 = `max(time[i] for i∈T) * mul[stage]`。  

把所有状态当成 **图的节点**，每一次合法的划船行为当成 **带权有向边**，整个问题就转化为：

> **在一个正权重图中，从起点 `(mask=0, stage=0)` 到任意终点 `(mask=ALL, any stage)` 的最短路径**。

这正是 **Dijkstra 最短路** 的使用场景——所有边权都是正数（时间不可能为负），我们只需要在 `2ⁿ * m` 个节点上跑一次 Dijkstra，即可得到最小总时间。

**关键细节**  

- **节点数量**：`2ⁿ`（mask） × `m`（阶段） ≤ `4096 * 5 = 20480`，非常适合 Dijkstra。  
- **边的生成**：对每个弹出的节点，只需要枚举 **去程**（从左岸挑 `1…k` 人）和 **回程**（从右岸挑 `1…k` 人）两类组合，各自产生若干条边。  
- **终止条件**：只要第一次弹出 `mask == ALL` 的节点，即得到最短路径（因为 Dijkstra 保证首次访问到达目标的距离即为最小）。  

#### 代码（Python）

```python
import heapq
import itertools
import math

def minimumTime(n, k, m, time, mul):
    """
    Dijkstra on state graph:
        state = (mask, stage)
        mask : bitmask of people already on the destination side
        stage: which multiplier (0 .. m-1) will be used for the next crossing
    """
    ALL = (1 << n) - 1               # 所有人员已到达右岸的 mask
    INF = float('inf')
    # dist[mask][stage] = 当前已知的最小时间
    dist = [[INF] * m for _ in range(1 << n)]
    dist[0][0] = 0.0

    # 小根堆，元素为 (已用时间, mask, stage)
    heap = [(0.0, 0, 0)]

    while heap:
        cur_time, mask, stage = heapq.heappop(heap)

        # 已经弹出的状态是最优的，若已经把所有人运完直接返回
        if mask == ALL:
            return cur_time

        # 如果当前记录的距离更小，说明这个条目是过期的，直接跳过
        if cur_time > dist[mask][stage] + 1e-12:
            continue

        # ---------- 去程：从左岸挑选 S ----------
        left = [i for i in range(n) if not (mask >> i) & 1]
        for sz in range(1, min(k, len(left)) + 1):
            for S in itertools.combinations(left, sz):
                cost = max(time[i] for i in S) * mul[stage]
                new_mask = mask
                for i in S:
                    new_mask |= 1 << i
                next_stage = (stage + 1) % m
                nd = cur_time + cost
                if nd + 1e-12 < dist[new_mask][next_stage]:
                    dist[new_mask][next_stage] = nd
                    heapq.heappush(heap, (nd, new_mask, next_stage))

        # ---------- 回程：从右岸挑选 T ----------
        # 只有当还有人已经在右岸且还没全部运完时才需要考虑回程
        if mask != 0:                     # 至少有一个人可以划船回去
            right = [i for i in range(n) if (mask >> i) & 1]
            for sz in range(1, min(k, len(right)) + 1):
                for T in itertools.combinations(right, sz):
                    cost = max(time[i] for i in T) * mul[stage]
                    new_mask = mask
                    for i in T:
                        new_mask &= ~(1 << i)   # 把这些人送回左岸
                    next_stage = (stage + 1) % m
                    nd = cur_time + cost
                    if nd + 1e-12 < dist[new_mask][next_stage]:
                        dist[new_mask][next_stage] = nd
                        heapq.heappush(heap, (nd, new_mask, next_stage))

    # 若所有节点都遍历完仍未到达 ALL，说明无解
    return -1.0
```

> **代码要点解释**  
> 1. **状态压缩**：`mask` 用二进制直接把 12 个人的在/不在右岸信息装进一个整数，省空间也方便位运算。  
> 2. **堆（priority queue）**：每次取出当前已知最小耗时的状态，符合 Dijkstra “贪心”原则。  
> 3. **边的生成**：`itertools.combinations` 把所有合法的 `S`、`T`（人数 ≤ k）一次性列出，随后计算对应的时间代价。  
> 4. **提前结束**：一旦弹出 `mask == ALL` 的节点，就可以直接返回，因为 Dijkstra 保证这是最短路径。  

#### 复杂度  

- **时间复杂度**  
  - 节点数：`V = 2ⁿ * m ≤ 2¹² * 5 ≈ 2·10⁴`。  
  - 对每个弹出的节点，我们枚举最多 `C(n,1)+…+C(n,k) ≤ k·C(n,k)` 个去程和同等数量的回程组合。最坏情况下约为 `O(k * C(n,k))`（`n=12, k=5` 时约 7920）。  
  - 因此总体时间约为 `O( V * k * C(n,k) * log V )`，在题目给出的上限下约 **几百万次**运算，能够在毫秒级通过。  
- **空间复杂度**  
  - `dist` 表占 `O(2ⁿ * m)`，约 `2·10⁴` 个浮点数。  
  - 堆中最多也会存放同等数量的状态。整体是 `O(2ⁿ * m)`，即 **线性** 与状态数。  

> **对比**：暴力解的时间是指数级 `O(2ⁿ * (C(n,k))²)`，而 Dijkstra 把 **回程** 和 **去程** 拆成两条独立的边，只遍历一次图，复杂度从 “指数的平方” 降到 “指数 * 多项式”，在本题规模上有质的提升。  

---

## 心得  

- **核心技巧**：把「状态 + 转移」抽象成 **图**，再用 **最短路（Dijkstra）** 求解。  
- **适用的题型**  
  1. **状态压缩 + DP + 最短路**（如 “最小时间搬运所有货物”）。  
  2. **带有循环资源的调度问题**（如 “循环风向下的机器人移动”）。  
  3. **任意正权重转移图的最优路径**（如 “最小费用流的离散版”）。  
- **一句话总结**：  
  > “当状态可以用掩码表示且转移代价为正数时，构图 + Dijkstra 往往是最直接、最快的求最优解方式。”  

---

## 反思  

- **第一反应**：直接写递归/DFS 暴力搜索，想着把所有搬运顺序枚举完。  
- **最容易踩的坑**  
  1. **忘记阶段循环**：`stage` 必须在每一次去程或回程后 **模 m** 前进，否则倍率会错位。  
  2. **回程必须有人划船**：如果只让船空驶返回，题目会认为不合法，导致错误的最小时间。  
  3. **浮点精度**：倍率是小数，累计误差会放大，输出时应使用 `float` 并保留合适的小数位。  
- **下次类似题的第一步**：  
  > “先把每一种‘局部行为’（这里是一次划船）抽象成有向边，检查所有状态的数量是否可以接受（通常是 2ⁿ·something），然后考虑用最短路或 BFS 在状态图上搜索最优解。”