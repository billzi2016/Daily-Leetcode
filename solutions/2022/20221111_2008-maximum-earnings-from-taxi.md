# #2008. 出租车最大收益 / Maximum Earnings From Taxi

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-earnings-from-taxi/)

---

## 题目（英文原版）

**Description**

There are n points on a road you are driving your taxi on. The n points on the road are labeled from 1 to n in the direction you are going, and you want to drive from point 1 to point n to make money by picking up passengers. You cannot change the direction of the taxi.
The passengers are represented by a 0-indexed 2D integer array rides, where rides[i] = [starti, endi, tipi] denotes the ith passenger requesting a ride from point starti to point endi who is willing to give a tipi dollar tip.
For each passenger i you pick up, you earn endi - starti + tipi dollars. You may only drive at most one passenger at a time.
Given n and rides, return the maximum number of dollars you can earn by picking up the passengers optimally.
Note: You may drop off a passenger and pick up a different passenger at the same point.

**Examples**

**Example 1:**

```
Input: n = 5, rides = [[2,5,4],[1,5,1]]
Output: 7
Explanation: We can pick up passenger 0 to earn 5 - 2 + 4 = 7 dollars.
```

**Example 2:**

```
Input: n = 20, rides = [[1,6,1],[3,10,2],[10,12,3],[11,12,2],[12,15,2],[13,18,1]]
Output: 20
Explanation: We will pick up the following passengers:
- Drive passenger 1 from point 3 to point 10 for a profit of 10 - 3 + 2 = 9 dollars.
- Drive passenger 2 from point 10 to point 12 for a profit of 12 - 10 + 3 = 5 dollars.
- Drive passenger 5 from point 13 to point 18 for a profit of 18 - 13 + 1 = 6 dollars.
We earn 9 + 5 + 6 = 20 dollars in total.
```

**Constraints**

- 1 <= n <= 105
- 1 <= rides.length <= 3 * 104
- rides[i].length == 3
- 1 <= starti < endi <= n
- 1 <= tipi <= 105

---

## 题目（中文翻译）

道路上有 `n` 个点，你正在开出租车。道路上的点按照你前进的方向从 `1` 编号到 `n`，你只能从点 `1` 开始，一直向前行驶到点 `n`，并通过接乘客来赚钱。**不能改变行驶方向**。

乘客信息由一个 **0 索引的二维整数数组** `rides` 表示，其中 `rides[i] = [start_i, end_i, tip_i]` 表示第 `i` 位乘客希望从点 `start_i` 前往点 `end_i`，并愿意给 `tip_i` 美元的小费。

- 接到第 `i` 位乘客后，你可以获得 `end_i - start_i + tip_i` 美元的收入。
- 同一时刻只能载 **至多一位** 乘客。
- 你可以在同一点下车并立刻接另一位乘客。

给定 `n` 和 `rides`，返回通过 **最优接客** 所能获得的 **最大美元数**。

> **注意**：在同一点下车后可以立即接另一位乘客。

---

## 示例

### 示例 1

**输入**  
`n = 5, rides = [[2,5,4],[1,5,1]]`

**输出**  
`7`

**解释**  
我们可以接乘客 `0`，获得 `5 - 2 + 4 = 7` 美元的收入。

### 示例 2

**输入**  
`n = 20, rides = [[1,6,1],[3,10,2],[10,12,3],[11,12,2],[12,15,2],[13,18,1]]`

**输出**  
`20`

**解释**  
我们可以依次接以下乘客：

- 从点 `3` 开到点 `10` 接乘客 `1`，收益 `10 - 3 + 2 = 9` 美元。  
- 从点 `10` 开到点 `12` 接乘客 `2`，收益 `12 - 10 + 3 = 5` 美元。  
- 从点 `13` 开到点 `18` 接乘客 `5`，收益 `18 - 13 + 1 = 6` 美元。  

总收益 `9 + 5 + 6 = 20` 美元。

---

## 约束条件

- `1 <= n <= 10^5`
- `1 <= rides.length <= 3 * 10^4`
- `rides[i].length == 3`
- `1 <= start_i < end_i <= n`
- `1 <= tip_i <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有乘客的订单都列举出来，然后枚举所有可能的接客顺序**，找出合法且收益最大的那一种。  
- **合法**指的是：  
  1. 只能向前开车（编号只能增大），所以如果我们已经在 `endA` 点下车，下一位乘客的 `start` 必须 **≥ endA**。  
  2. 同一时间只能载一个乘客。  

可以把每个乘客想象成一张**车票**，我们要挑选一组不冲突的车票，使得总票价（`end - start + tip`）最大。  
这其实是「**区间调度**」的最优子集问题，最暴力的做法就是 **递归/回溯**：  
1. 按照 `start`（或 `end`）把所有订单排好序，方便判断是否冲突。  
2. 从第 0 张车票开始，**两条路**：  
   - **接这张车票** → 收益加上它的利润，然后递归处理后面所有 `start >= 当前车票的 end` 的车票。  
   - **不接这张车票** → 直接递归处理下一张车票。  
3. 两条路的最大值即为答案。  

> **生活类比**：把每张车票想象成一本书的章节，章节之间不能交叉阅读。我们只能顺序读下去，想办法挑选章节组合，使得阅读的“价值”最大。  

**为什么正确**：因为我们遍历了所有可能的接客组合（每张票要么接要么不接），所以一定能找到最优解。  

**时间/空间复杂度**：  
- 每张车票都有「接」或「不接」两种选择，递归树的规模是 `2^m`（`m = rides.length`），**指数级**，在最坏情况下会爆炸。  
- 递归调用栈的深度最多 `m`，所以空间是 `O(m)`。  

> **大白话解释**：  
> - `O(2^m)` 就好比把每张票都当成一次“是/否”的投票，所有投票的组合数就是 2 的 m 次方，随着票数增多，组合数会疯狂增长，根本跑不完。  

#### 代码（Python）  

```python
from typing import List

def max_earnings_bruteforce(n: int, rides: List[List[int]]) -> int:
    # 先把每趟车的利润算好，方便后面使用
    rides = [[s, e, e - s + tip] for s, e, tip in rides]
    # 按照起点排序，保证递归时后面的车票都在后面
    rides.sort(key=lambda x: x[0])

    # 记忆化搜索，避免重复子问题（仍然是指数级，但稍微快点）
    from functools import lru_cache

    @lru_cache(None)
    def dfs(idx: int, cur_pos: int) -> int:
        """
        从 rides[idx:] 开始考虑，当前已经开到 cur_pos（上一次下车点）。
        返回能够得到的最大收益。
        """
        if idx == len(rides):
            return 0

        start, end, profit = rides[idx]

        # 方案1：不接当前乘客
        skip = dfs(idx + 1, cur_pos)

        # 方案2：如果可以接（不逆行），就接它
        take = 0
        if start >= cur_pos:                 # 能够顺序接上
            take = profit + dfs(idx + 1, end)

        # 取两者的最大值
        return max(skip, take)

    # 初始位置在点 1
    return dfs(0, 1)
```

#### 复杂度  

- **时间复杂度**：`O(2^m)`（指数级），因为每个乘客都有「接」或「不接」两种选择。即使加了记忆化（`lru_cache`），状态仍然是 `(idx, cur_pos)`，`cur_pos` 可能取 `n` 种，整体仍然不可接受。  
- **空间复杂度**：`O(m + n)`  
  - 递归栈最深 `m`（乘客数）。  
  - 记忆化表最多保存 `m * n` 条记录（`idx` * `cur_pos`），在最坏情况下会占用 `O(m·n)` 空间。  

> 暴力解只能帮助我们理解「每一次选择」的本质，随后我们会寻找一种方式，**把状态压缩**，从指数级降到多项式级。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们知道：  
- **关键点**是「在某个位置 `x`（路点）时，已经能赚到的最大钱」——这正是**动态规划**的思路。  
- 暴力解的瓶颈在于：每次递归都要遍历所有后面的乘客，导致指数级。我们需要**一次遍历**就能得到答案。  

**优化方向**：  
1. **把所有路点（1 … n）视为状态**，`dp[i]` 表示“开到第 `i` 点时，能够获得的最大收益”。  
2. 对每一趟乘客 `ride = [s, e, tip]`，它的利润是 `e - s + tip`。如果我们在 `s` 点之前已经得到的最大收益是 `dp[s]`，那么接这趟车后，在 `e` 点的收益可以提升为 `dp[s] + profit`。  
3. 为了让 `dp` 正确，我们需要**按照终点递增**的顺序处理乘客，这样在处理某趟车时，`dp[s]` 已经是**最优**的（因为所有 `s` 小于当前 `e` 的车都已经考虑过）。  
4. 具体做法：  
   - **按 `end` 升序**把所有乘客排序。  
   - 同时维护一个数组 `dp[0…n]`（下标从 0 开始，`dp[i]` 对应路点 `i`），初始全为 0。  
   - 遍历每个路点 `i`（从 1 到 n），`dp[i]` 先继承 `dp[i-1]`（不做任何事，保持之前的最大值）。  
   - 同时检查所有以 `i` 为终点的乘客（因为已经排序，可以用指针一次扫完），对每个 `[s, i, tip]`，计算 `candidate = dp[s] + (i - s + tip)`，取 `dp[i] = max(dp[i], candidate)`。  
5. **二分搜索**（可选）：如果我们不想在每个路点都遍历所有乘客，而是直接对每趟乘客查找它的 `dp[s]`，可以先把乘客按 `start` 排序，用二分搜索在 `dp` 中找到对应位置。另一种更常见的实现是：**把乘客按起点排序**，对每个乘客用二分在已处理好的 `end` 列表中寻找 `dp[start]`。  
6. 最终答案是 `dp[n]`，因为到达终点 `n` 时的最大收益即为所求。  

**核心数据结构**：  
- **数组 `dp`**（类似“前缀最大”），把每个路点的最优收益记下来。  
- **排序**（按 `end`），帮助我们一次遍历即可得到所有需要的转移。  
- **二分搜索（可选）**：在更紧凑的实现里，用 `bisect` 在已经计算好的 `ends` 列表中快速找到对应的 `dp`。  

**类比**：把路点看成“一天的时间”，`dp[t]` 表示“截至时间 `t` 能赚到的最多钱”。每接一次乘客，就相当于在某个时间点插入一个任务，收益是这段时间的“工资”。我们要在不冲突的前提下，把这些任务安排得最赚钱——这正是“**带权区间调度**”。  

#### 代码（Python）  

下面给出两种等价实现，**第一种**更直观（按终点遍历），**第二种**利用二分搜索，使代码更简洁。

```python
from typing import List
import bisect

def max_earnings(n: int, rides: List[List[int]]) -> int:
    """
    动态规划 + 排序 + 二分搜索
    dp[i] : 开到第 i 点（含）时的最大收益
    """
    # 计算每趟乘客的实际利润
    rides = [(s, e, e - s + tip) for s, e, tip in rides]
    # 按终点升序排列，方便一次遍历
    rides.sort(key=lambda x: x[1])

    dp = [0] * (n + 1)          # dp[0] = 0, dp[1] … dp[n] 待求
    idx = 0                     # rides 的指针，指向当前还未处理的乘客

    for point in range(1, n + 1):
        # 先把前一点的最大收益带过来（不接任何新乘客）
        dp[point] = dp[point - 1]

        # 处理所有终点恰好是 point 的乘客
        while idx < len(rides) and rides[idx][1] == point:
            start, end, profit = rides[idx]
            # 如果在 start 点已经获得的最大收益是 dp[start]，
            # 那么接这趟车后在 end 点的收益就是 dp[start] + profit
            candidate = dp[start] + profit
            if candidate > dp[point]:
                dp[point] = candidate   # 更新到达 point 的最大收益
            idx += 1

    return dp[n]
```

**如果想用二分搜索进一步简化**（不需要在每个点遍历乘客）：

```python
def max_earnings_bs(n: int, rides: List[List[int]]) -> int:
    # 计算利润并按起点升序排列
    rides = [(s, e, e - s + tip) for s, e, tip in rides]
    rides.sort(key=lambda x: x[0])   # 按 start 排序

    # ends 用来记录已经处理好的乘客的终点，dp_vals 与之对应保存对应的 dp 值
    ends = [0]          # 虚拟的结束点 0，dp[0] = 0
    dp_vals = [0]       # dp_vals[i] = 在 ends[i] 点的最大收益

    for s, e, profit in rides:
        # 在已知的 ends 中，找到最靠左且 <= s 的位置（即上一次可以在 s 前赚到的最大收益）
        i = bisect.bisect_right(ends, s) - 1
        best_before_s = dp_vals[i]

        # 这趟车结束后能得到的收益
        cand = best_before_s + profit

        # 如果 cand 超过当前已知的最大收益，就把它加入列表
        if cand > dp_vals[-1]:
            ends.append(e)
            dp_vals.append(cand)
        # 否则直接跳过，保持 dp 的单调递增（因为收益不会下降）

    return dp_vals[-1]   # 最后一个 dp 值即为最大收益
```

> **代码要点注释**：  
> - `bisect_right(ends, s) - 1` 找到「不超过 `s` 的最大终点」对应的最优收益。相当于在已经算好的「前缀最大」中快速查询。  
> - `ends` 与 `dp_vals` 始终保持**单调递增**，这样二分搜索才能工作。  

#### 复杂度  

- **时间复杂度**：`O(m log m + n)`（或 `O(m log m)`，因为 `n ≤ 10^5` 与 `m ≤ 3·10^4` 同阶）  
  - 对 `rides` 排序需要 `O(m log m)`。  
  - 主循环遍历 `1 … n`（第一种实现）或对每趟乘客二分一次（第二种实现），均为 `O(m log m)`。  
  - 与暴力解的指数级 `2^m` 相比，这里只需要对数级的额外开销，速度快得多。  

- **空间复杂度**：`O(n)`（第一种实现）或 `O(m)`（第二种实现）  
  - `dp` 数组大小为 `n+1`，最多 `10^5+1`，完全可以接受。  
  - 二分实现只保存 `ends`、`dp_vals` 两个列表，长度最多等于乘客数 `m`。  

> **对比**：  
> - 暴力解的 `O(2^m)` 随着乘客数稍微增大就会爆炸。  
> - 最优解的 `O(m log m)` 在本题约束（`m ≤ 3·10^4`）下几乎是瞬间完成的。  

---  

## 心得  

- **核心技巧**：**带权区间调度的动态规划**——把「在某点的最大收益」记下来，利用排序和前缀最大（或二分）实现状态转移。  
- **适用的题型**（类似思路）：  
  1. *Maximum Profit in Job Scheduling*（LeetCode 1235）  
  2. *Maximum Number of Events That Can Be Attended*（LeetCode 1353）  
  3. *Delete and Earn*（LeetCode 740）——本质上也是「把数值看成区间」的 DP。  
- **一句话总结**：**把每段行程当成「在某点前的最佳收益 + 本段利润」的递推，即可用一次遍历/二分完成最优调度。**  

---  

## 反思  

- **第一反应**：看到“只能向前开，不能同时载客”，立刻想到「区间不冲突」的调度问题，进而想到「枚举所有子集」的暴力解。  
- **最容易踩的坑**：  
  - **忘记把 `start` 点的收益也算进来**（`dp[start]`），导致少算了一段路程的利润。  
  - **边界条件**：`dp[0]` 必须初始化为 0，且在查询 `dp[start]` 时要保证 `start` 已经被计算。  
  - **同一点上下车**：题目允许在同一点下车后立即接另一位乘客，需要在 DP 转移时使用「`>=`」而不是「`>`」的比较。  
- **下次类似题目**：第一步先 **把每个任务的「收益」写出来**，然后 **按结束时间排序**，构造 **`dp[i] = max(dp[i‑1], dp[start] + profit)`** 的递推式。这样思路就已经完整了。