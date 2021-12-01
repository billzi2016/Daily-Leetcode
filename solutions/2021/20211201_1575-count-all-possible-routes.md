# #1575. 统计所有可能的路线 / Count All Possible Routes

> 难度：困难 · 标签：Array、Dynamic Programming、Memoization · [LeetCode 链接](https://leetcode.com/problems/count-all-possible-routes/)

---

## 题目（英文原版）

**Description**

You are given an array of distinct positive integers locations where locations[i] represents the position of city i. You are also given integers start, finish and fuel representing the starting city, ending city, and the initial amount of fuel you have, respectively.
At each step, if you are at city i, you can pick any city j such that j != i and 0 <= j < locations.length and move to city j. Moving from city i to city j reduces the amount of fuel you have by |locations[i] - locations[j]|. Please notice that |x| denotes the absolute value of x.
Notice that fuel cannot become negative at any point in time, and that you are allowed to visit any city more than once (including start and finish).
Return the count of all possible routes from start to finish. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: locations = [2,3,6,8,4], start = 1, finish = 3, fuel = 5
Output: 4
Explanation: The following are all possible routes, each uses 5 units of fuel:
1 -> 3
1 -> 2 -> 3
1 -> 4 -> 3
1 -> 4 -> 2 -> 3
```

**Example 2:**

```
Input: locations = [4,3,1], start = 1, finish = 0, fuel = 6
Output: 5
Explanation: The following are all possible routes:
1 -> 0, used fuel = 1
1 -> 2 -> 0, used fuel = 5
1 -> 2 -> 1 -> 0, used fuel = 5
1 -> 0 -> 1 -> 0, used fuel = 3
1 -> 0 -> 1 -> 0 -> 1 -> 0, used fuel = 5
```

**Example 3:**

```
Input: locations = [5,2,1], start = 0, finish = 2, fuel = 3
Output: 0
Explanation: It is impossible to get from 0 to 2 using only 3 units of fuel since the shortest route needs 4 units of fuel.
```

**Constraints**

- 2 <= locations.length <= 100
- 1 <= locations[i] <= 109
- All integers in locations are distinct.
- 0 <= start, finish < locations.length
- 1 <= fuel <= 200

---

## 题目（中文翻译）

**题目描述**

给定一个由互不相同的正整数构成的数组 `locations`，其中 `locations[i]` 表示城市 `i` 的坐标。另给定整数 `start`、`finish` 和 `fuel`，分别表示起始城市、目标城市以及初始的燃料量。

在每一步，如果你当前位于城市 `i`，可以选择任意另一个城市 `j`（`j != i` 且 `0 <= j < locations.length`），前往城市 `j`。从城市 `i` 移动到城市 `j` 会消耗 `|locations[i] - locations[j]|` 单位的燃料（`|x|` 表示 `x` 的绝对值）。

- 燃料量在任何时刻都不能为负；
- 你可以多次访问同一城市（包括起始城市和目标城市）。

返回从 `start` 到 `finish` 的所有可能路线的数量。由于答案可能非常大，请返回 `10^9 + 7` 取模后的结果。

**示例**

*示例 1*  
输入: `locations = [2,3,6,8,4]`, `start = 1`, `finish = 3`, `fuel = 5`  
输出: `4`  
解释: 以下都是使用恰好 5 单位燃料的可行路线:
- `1 -> 3`
- `1 -> 2 -> 3`
- `1 -> 4 -> 3`
- `1 -> 4 -> 2 -> 3`

*示例 2*  
输入: `locations = [4,3,1]`, `start = 1`, `finish = 0`, `fuel = 6`  
输出: `5`  
解释: 以下都是可行路线:
- `1 -> 0`，消耗燃料 = 1
- `1 -> 2 -> 0`，消耗燃料 = 5
- `1 -> 2 -> 1 -> 0`，消耗燃料 = 5
- `1 -> 0 -> 1 -> 0`，消耗燃料 = 3
- `1 -> 0 -> 1 -> 0 -> 1 -> 0`，消耗燃料 = 5

*示例 3*  
输入: `locations = [5,2,1]`, `start = 0`, `finish = 2`, `fuel = 3`  
输出: `0`  
解释: 仅用 3 单位燃料无法从城市 0 到达城市 2，因为最短路径需要 4 单位燃料。

**约束条件**

- `2 <= locations.length <= 100`
- `1 <= locations[i] <= 10^9`
- `locations` 中的所有整数互不相同
- `0 <= start, finish < locations.length`
- `1 <= fuel <= 200`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是 **枚举所有可能的行程**，只要剩余油量足够，就可以从当前位置 `i` 移动到任意其它城市 `j`（`j != i`），随后继续在新城市继续枚举。  
这类似于在一张**完全图**（每个城市都和其它城市有一条边）上进行**深度优先搜索（DFS）**，每走一步就把消耗的油量 `|locations[i] - locations[j]|` 从剩余油量里减掉。  

- **数据结构**：我们只需要一个列表 `locations` 保存城市坐标，递归函数的参数里带上当前所在的城市下标 `i`、剩余油量 `fuel`，以及已经走过的路径计数。  
  - 可以把「剩余油量」想象成「钱包里的零钱」，每走一步就要付出相应的「车费」，付不出就不能继续走。  

- **为什么正确**：递归会尝试所有合法的下一步（即油量足够的城市），只要在递归过程中恰好到达 `finish`，就算一种合法路线。因为我们没有对路径做任何剪枝（除了油不够的情况），所以每一种可能的走法都会被枚举到。  

- **复杂度分析**：  
  - 假设城市数为 `n`（`n ≤ 100`），每一步可以选择 `n‑1` 条出路，最坏情况下会一直走到油耗耗尽（油量上限 `fuel ≤ 200`），于是递归树的深度最多是 `fuel`（每走一步至少消耗 1 单位油）。  
  - 因此时间复杂度大致是 `O((n‑1)^fuel)`，这在最坏情况下是指数级的，几乎不可能在规定时间内跑完。  
  - 空间复杂度主要是递归栈的深度，最坏 `O(fuel)`，即最多 200 层。  

> **大白话**：`O((n‑1)^fuel)` 就像是“每次都有 `n‑1` 种选择，连续做 `fuel` 次”，数量会像滚雪球一样爆炸，根本算不完。  

#### 代码（Python）  

```python
MOD = 10 ** 9 + 7

def countRoutes_bruteforce(locations, start, finish, fuel):
    n = len(locations)

    # 深度优先搜索，返回从 city 出发、剩余 fuel 的合法路线数
    def dfs(city, remain):
        # 如果油已经不够，直接返回 0（不能继续走）
        if remain < 0:
            return 0

        # 每次来到 finish 都算一条合法路线（即使后面还能继续走）
        ans = 1 if city == finish else 0

        # 枚举所有可能的下一站
        for nxt in range(n):
            if nxt == city:          # 不能原地不动
                continue
            cost = abs(locations[city] - locations[nxt])
            if cost <= remain:       # 油够就可以走
                ans += dfs(nxt, remain - cost)
                ans %= MOD           # 防止整数爆炸

        return ans

    return dfs(start, fuel)
```

#### 复杂度  

- **时间复杂度**：`O((n‑1)^fuel)` —— 指数级增长，实际会在 2~3 秒内超时。  
- **空间复杂度**：`O(fuel)` —— 递归栈最多 `fuel` 层（ ≤ 200），可以接受。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **大量重复子问题**：  
- 例如从城市 `2`、剩余油量 `10` 开始的所有后续路线，会在不同的递归路径里被重复计算很多次。  
- 只要我们把「**当前所在城市**」和「**剩余油量**」这两个信息记下来，下次再遇到同样的状态时直接复用之前的结果，就能把指数级的搜索压缩成多项式级。  

这正是**记忆化搜索（Memoization）**或**动态规划（DP）**的核心思想：  
- 把每一种「状态」看成一个子问题，状态 = `(city, remain_fuel)`。  
- 用一个哈希表（Python 中的 `dict`）或二维数组把已经算好的子问题结果保存下来，后面直接查表。  

**为什么可以这么做**：  
- 题目保证 `locations` 中的坐标互不相同，且每次移动都会消耗正数油量（因为距离是正数），所以**油量只能单调递减**，不会出现「油量不变」的循环。  
- 因此状态空间是有限的：城市最多 100 种，油量最多 200，最多 `100 * 201 = 20100` 种不同的 `(city, fuel)` 组合。  

**核心算法**：  
1. 定义 `dp[i][f]` 为「从城市 `i` 出发、剩余油量恰好为 `f` 时，能够到达 `finish` 的路线数」。  
2. 初始时：`dp[finish][f] = 1`（因为已经在终点，算作一条合法路线），对所有合法的 `f` 都如此。  
3. 对每个状态 `(i, f)`，遍历所有可以前往的城市 `j`（`j != i`），如果 `cost = |locations[i] - locations[j]| ≤ f`，则  
   `dp[i][f] += dp[j][f - cost]`（把从 `j` 继续走的路线加进来）。  
4. 由于 `f - cost < f`，我们可以按 **燃料从小到大** 的顺序填表，或者直接用递归+记忆化实现（更直观）。  

这里采用 **递归 + 记忆化**，因为代码更易读，且 Python 的字典查询很快。  

**类比**：把每个状态想象成「一本练习册的第 `i` 题，第 `f` 分的答案」，一旦写好答案，后面再碰到同样的题目和分数，就直接抄答案，不用重新思考。  

#### 代码（Python）  

```python
from functools import lru_cache

MOD = 10 ** 9 + 7

def countRoutes(locations, start, finish, fuel):
    n = len(locations)

    @lru_cache(maxsize=None)                     # 记忆化装饰器，自动保存 (city, remain) 的结果
    def dfs(city, remain):
        # 只要油不为负，就可以继续尝试
        # 到达 finish 时计数 +1（即使后面还能继续走，后面的路线会在后续递归里再计数）
        total = 1 if city == finish else 0

        # 遍历所有可能的下一站
        for nxt in range(n):
            if nxt == city:
                continue
            cost = abs(locations[city] - locations[nxt])
            if cost <= remain:                    # 油够就递归
                total += dfs(nxt, remain - cost)
                total %= MOD                       # 取模防止溢出

        return total

    return dfs(start, fuel)
```

**代码说明（逐行注释）**  

| 行号 | 中文注释 |
|------|----------|
| 1    | 导入 `lru_cache`，它可以把函数调用的结果缓存起来，实现记忆化。 |
| 3    | 定义常量 `MOD = 10^9 + 7`，因为答案可能很大，需要取模。 |
| 5    | 主函数 `countRoutes` 接收城市坐标、起点、终点和初始油量。 |
| 7    | `n` 为城市数量。 |
| 9‑10 | 使用装饰器 `@lru_cache`，把 `(city, remain)` 这对参数的返回值缓存。 |
| 12   | `total` 记录从当前状态出发能够到达终点的路线数。 |
| 13   | 如果当前就在终点，先算一条合法路线（即使不走也算）。 |
| 16‑22 | 遍历所有城市 `nxt`，尝试移动。若油够 (`cost <= remain`)，递归计算从 `nxt` 出发的路线数并累加。 |
| 24   | 返回当前状态的总路线数（已经取模）。 |
| 26   | 从起点 `start`、初始油量 `fuel` 开始递归，得到答案。 |

#### 复杂度  

- **时间复杂度**：`O(n * fuel * n)` → 实际上是 `O(n^2 * fuel)`。  
  - 每个状态 `(city, remain)`（最多 `n * (fuel+1)` 个）只会被计算一次。  
  - 在计算一个状态时，需要遍历所有 `n‑1` 条可能的出路，故乘以 `n`。  
  - 对于 `n ≤ 100`、`fuel ≤ 200`，最多约 `100 * 100 * 200 = 2,000,000` 次基本操作，能够在毫秒级完成。  

- **空间复杂度**：`O(n * fuel)` 用于缓存表（`lru_cache`），加上递归栈深度 `O(fuel)`，总体约 `O(n * fuel)`，即最多约 20,000 个整数，内存占用极小。  

---

## 心得  

- **核心技巧**：**记忆化搜索 / 动态规划**，把「当前位置 + 剩余油量」作为状态，避免重复子问题。  
- **适用场景**：  
  1. 所有「状态只依赖于当前信息且转移只向一个方向」的问题（如背包、爬楼梯等）。  
  2. **路径计数** 类题目，需要统计满足条件的所有可能路径（如「不同路径计数」）。  
  3. 有「资源限制」且每一步都会消耗资源的搜索（如「最大收益」「最少费用」等）。  
- **一句话总结**：**把“现在在哪里、还能剩多少油”记下来，重复出现时直接复用，搜索就不再爆炸**。  

---

## 反思  

- **第一反应**：看到「可以任意来回、油量限制」就想到暴力 DFS，先把所有路径枚举一遍。  
- **最容易踩的坑**：  
  - **忘记在到达终点时立即计数**，导致只统计恰好在油耗用完时到达的路径。  
  - **没有取模**，递归累计的整数会非常大，导致 Python 整数运算变慢甚至内存溢出。  
  - **忽略油量为 0 时仍可能在终点** 的情况，需要在 `remain < 0` 时直接返回 0，而不是在 `remain == 0` 时结束搜索。  
- **下次类似题目**：第一步先**明确状态（位置 + 资源）**，判断是否有**单调性（资源只会递减）**，再决定是否可以使用记忆化/动态规划来剪枝。