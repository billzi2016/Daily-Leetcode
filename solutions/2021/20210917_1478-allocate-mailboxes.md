# #1478. **分配邮箱** / Allocate Mailboxes

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/allocate-mailboxes/)

---

## 题目（英文原版）

**Description**

Given the array houses where houses[i] is the location of the ith house along a street and an integer k, allocate k mailboxes in the street.
Return the minimum total distance between each house and its nearest mailbox.
The test cases are generated so that the answer fits in a 32-bit integer.

**Examples**

**Example 1:**

```
Input: houses = [1,4,8,10,20], k = 3
Output: 5
Explanation: Allocate mailboxes in position 3, 9 and 20.
Minimum total distance from each houses to nearest mailboxes is |3-1| + |4-3| + |9-8| + |10-9| + |20-20| = 5
```

**Example 2:**

```
Input: houses = [2,3,5,12,18], k = 2
Output: 9
Explanation: Allocate mailboxes in position 3 and 14.
Minimum total distance from each houses to nearest mailboxes is |2-3| + |3-3| + |5-3| + |12-14| + |18-14| = 9.
```

**Constraints**

- 1 <= k <= houses.length <= 100
- 1 <= houses[i] <= 104
- All the integers of houses are unique.

---

## 题目（中文翻译）

给定数组 `houses`，其中 `houses[i]` 表示第 `i` 栋房子在街道上的位置，以及整数 `k`，在这条街道上分配 `k` 个邮箱（mailboxes）。  
返回每栋房子到最近邮箱的距离之和的最小可能值。  
测试用例保证答案可以放入 32 位整数。

**示例 1**

```text
Input: houses = [1,4,8,10,20], k = 3
Output: 5
```

**解释**：在位置 3、9 和 20 处各放置一个邮箱。  
每栋房子到最近邮箱的距离之和为 `|3-1| + |4-3| + |9-8| + |10-9| + |20-20| = 5`。

**示例 2**

```text
Input: houses = [2,3,5,12,18], k = 2
Output: 9
```

**解释**：在位置 3 和 14 处各放置一个邮箱。  
每栋房子到最近邮箱的距离之和为 `|2-3| + |3-3| + |5-3| + |12-14| + |18-14| = 9`。

**约束条件**

- `1 <= k <= houses.length <= 100`
- `1 <= houses[i] <= 10^4`
- `houses` 中的所有整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的 mailbox 位置**，然后计算每个房子到最近 mailbox 的距离之和，取最小值。

- **数据结构**：我们可以把街道想象成一条数轴，`houses` 是数轴上的若干点。枚举 mailbox 位置时，只需要一个普通的 `list` 来保存当前的 mailbox 坐标集合。
- **正确性**：只要把所有合法的 mailbox 组合都尝试一次，就一定会碰到最优的那一组。因为题目要求的答案是“最小的总距离”，遍历完所有可能后取最小即可保证正确。
- **时间/空间复杂度**：  
  - 若街道上有 `n` 栋房子，`k` 个 mailbox，枚举所有可能的坐标组合相当于从 **无序的整数集合**（这里可以取 `houses` 所有可能的坐标或更大范围）中挑 `k` 个。即使只在 `houses` 位置上放 mailbox，也要遍历 `C(n, k)` 种组合，`C` 是组合数。  
  - 对每一种组合，我们需要遍历所有房子求最近的 mailbox，时间是 `O(n·k)`。  
  - 整体时间复杂度约为 `O(C(n, k) * n * k)`，当 `n = 100`、`k = 50` 时已经天文数字，根本不可接受。  
  - 空间只需要保存当前组合，`O(k)`。

> **大白话**：`O(C(n,k))` 就像从 100 本书里挑 50 本的所有挑法，几乎是无穷多。`O(n²)`、`O(n³)` 这种“几百次、几千次”我们还能接受，但这里的组合数会爆炸到 **10^28** 级别。

#### 代码（Python）

```python
import itertools
from typing import List

def min_total_distance_bruteforce(houses: List[int], k: int) -> int:
    # 为了把问题限制在有限范围，这里只在 houses 的位置上放 mailbox
    # 实际上最优解一定落在某两个相邻房子之间的中点或房子本身，
    # 但这里仍然使用最朴素的枚举方式说明思路。
    n = len(houses)
    best = float('inf')

    # 所有从 houses 中挑 k 个位置的组合
    for mail_pos in itertools.combinations(houses, k):
        total = 0
        # 对每个房子，找最近的 mailbox（线性扫描）
        for h in houses:
            # 计算当前房子到所有 mailbox 的距离，取最小
            dist = min(abs(h - m) for m in mail_pos)
            total += dist
        best = min(best, total)   # 维护全局最小值

    return best
```

#### 复杂度

- **时间复杂度**：`O(C(n, k) * n * k)` —— 组合数会导致指数级爆炸，实际运行会超时。  
- **空间复杂度**：`O(k)` —— 只存放当前枚举的 mailbox 坐标集合。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举 mailbox 的位置**。我们需要一种方式，只在**必要的候选位置**上考虑，而不是全部组合。观察可以发现：

1. **单个 mailbox 的最优位置**  
   - 当 `k = 1` 时，最小总距离等价于把 mailbox 放在所有房子坐标的**中位数**（median）上。因为中位数把数列左右两边的点数平衡，使得绝对距离之和最小。  
   - 这一步可以用**前缀和**快速求出任意区间 `[i, j]` 放一个 mailbox 的最小距离。

2. **把问题拆分成子区间**  
   - 把所有房子先排序（因为距离只和相对位置有关），记为 `houses[0] … houses[n-1]`。  
   - 如果我们决定把第 `i`~`j`（包含）的房子统一由同一个 mailbox 服务，那么最优的 mailbox 必须放在这段房子的中位数位置，费用可以预先算好。  

3. **动态规划**  
   - 设 `dp[i][m]` 为前 `i` 栋房子（下标 `0..i-1`）使用 `m` 个 mailbox 时的最小总距离。目标是 `dp[n][k]`。  
   - 转移：把第 `t`~`i-1` 栋房子交给第 `m` 个 mailbox 负责，前面 `t` 栋房子使用 `m-1` 个 mailbox。  
     \[
     dp[i][m] = \min_{0 \le t < i} \big( dp[t][m-1] + cost[t][i-1] \big)
     \]
     其中 `cost[t][i-1]` 是区间 `[t, i-1]` 放一个 mailbox 的最小距离（已预处理）。  
   - 初始条件：`dp[0][0] = 0`（0 栋房子配 0 个 mailbox），其余设为无穷大。

4. **如何快速得到 `cost[l][r]`**  
   - 对区间 `[l, r]`，中位数下标为 `mid = (l + r) // 2`。  
   - 把所有房子距离中位数的绝对值相加。若提前准备前缀和 `pre[i] = sum_{0..i-1} houses[i]`，则可以在 `O(1)` 时间算出左侧和右侧的距离和：  
     \[
     \text{左侧} = houses[mid] * (mid - l) - (pre[mid] - pre[l])
     \]
     \[
     \text{右侧} = (pre[r+1] - pre[mid+1]) - houses[mid] * (r - mid)
     \]
   - 两部分相加即为 `cost[l][r]`。

5. **复杂度分析**  
   - 预处理 `cost`：`O(n²)`（遍历所有 `l,r`），每个 `cost` 用 `O(1)` 计算。  
   - DP 主循环：外层遍历 `i = 1..n`，`m = 1..k`，内层遍历 `t = 0..i-1`，总共 `O(k * n²)`。  
   - 由于 `n ≤ 100`，`k ≤ n`，`O(k·n²)` ≤ `10⁶`，在 Python 中完全可接受。

#### 代码（Python）

```python
from typing import List

def min_total_distance(houses: List[int], k: int) -> int:
    # 1. 排序，方便后面使用区间中位数
    houses.sort()
    n = len(houses)

    # 2. 前缀和（pre[i] = houses[0] + ... + houses[i-1]），便于 O(1) 求区间和
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] + houses[i]

    # 3. 预处理 cost[l][r]：区间 [l, r] 放一个 mailbox 的最小距离
    #    使用中位数位置 houses[mid]，mid = (l+r)//2
    cost = [[0] * n for _ in range(n)]
    for l in range(n):
        for r in range(l, n):
            mid = (l + r) // 2
            # 左侧房子到中位数的距离之和
            left = houses[mid] * (mid - l) - (pre[mid] - pre[l])
            # 右侧房子到中位数的距离之和
            right = (pre[r + 1] - pre[mid + 1]) - houses[mid] * (r - mid)
            cost[l][r] = left + right   # total distance for this segment

    # 4. 动态规划
    INF = 10 ** 18
    # dp[i][m] 表示前 i 栋房子（0..i-1）使用 m 个 mailbox 的最小距离
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0   # 0 栋房子配 0 个 mailbox，费用为 0

    for i in range(1, n + 1):          # i 为前缀长度
        for m in range(1, min(k, i) + 1):   # m 不能超过 i
            # 枚举第 m 个 mailbox 负责的区间起点 t
            # 前 t 栋房子使用 m-1 个 mailbox，t..i-1 这段用第 m 个 mailbox
            best = INF
            for t in range(m - 1, i):   # 至少要留下 m-1 栋房子给前面的 mailbox
                cur = dp[t][m - 1] + cost[t][i - 1]
                if cur < best:
                    best = cur
            dp[i][m] = best

    return dp[n][k]
```

#### 复杂度

- **时间复杂度**：`O(k * n²)`  
  - 预处理 `cost` 需要遍历所有区间 `O(n²)`。  
  - DP 主循环的三层嵌套同样是 `O(k·n²)`。  
  - 对于本题的上限 `n ≤ 100`，这大约是 `10⁶` 次基本操作，运行毫秒级。

- **空间复杂度**：`O(n²)`  
  - `cost` 表占 `n²` 的空间（`100×100 = 10⁴`，非常小）。  
  - DP 表使用 `(n+1)*(k+1)`，同样在千级别。  
  - 与暴力解的指数级空间相比，已是线性/平方级的友好占用。

---

## 心得

- **核心技巧**：**区间中位数 + 动态规划**。先把“单个 mailbox 的最优位置”抽象为区间费用，再通过 DP 把多个 mailbox 的划分问题转化为最优子结构的求解。
- **适用的题型**  
  1. **分割数组使代价最小**（如 “分割数组的最大和”、 “划分数组的最小代价”）  
  2. **在数轴上放点使总距离最小**（如 “最小总移动距离”、 “把学生安排到教室”）  
  3. **使用前缀和快速求区间代价** 的 DP 题（如 “划分字符串使回文代价最小”）。
- **一句话总结**：把每个 mailbox 看成“区间的中位数”，用 DP 把全局划分成若干最优区间，即可得到最小总距离。

---

## 反思

- **第一反应**：看到“k 个 mailbox”，本能想到“把街道切成 k 段”，每段放一个 mailbox，于是想到“枚举切点”或“暴力枚举所有位置”。这导致了指数级的时间。
- **最容易踩的坑**  
  - 忘记先对 `houses` **排序**，导致中位数不再是最优位置。  
  - 在计算区间费用时直接遍历导致 `O(n³)`，而不是利用前缀和实现 `O(1)`。  
  - DP 初始化不完整（如 `dp[0][0]`），会产生错误的最小值。  
  - 边界条件：`k` 可能等于 `n`，此时每栋房子一个 mailbox，答案应为 `0`，代码要能正确处理。
- **下次类似题目**：第一步先**寻找局部最优结构**（单个 mailbox 的最优放置），**预处理区间代价**，再**用 DP 把全局划分**。把“暴力枚举所有组合”转化为“枚举切分点”，复杂度立刻从指数级降到多项式。