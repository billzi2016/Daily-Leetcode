# #1751. **最多可以参加的活动数 II** / Maximum Number of Events That Can Be Attended II

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended-ii/)

---

## 题目（英文原版）

**Description**

You are given an array of events where events[i] = [startDayi, endDayi, valuei]. The ith event starts at startDayi and ends at endDayi, and if you attend this event, you will receive a value of valuei. You are also given an integer k which represents the maximum number of events you can attend.
You can only attend one event at a time. If you choose to attend an event, you must attend the entire event. Note that the end day is inclusive: that is, you cannot attend two events where one of them starts and the other ends on the same day.
Return the maximum sum of values that you can receive by attending events.

**Examples**

**Example 1:**

```
Input: events = [[1,2,4],[3,4,3],[2,3,1]], k = 2
Output: 7
Explanation: Choose the green events, 0 and 1 (0-indexed) for a total value of 4 + 3 = 7.
```

**Example 2:**

```
Input: events = [[1,2,4],[3,4,3],[2,3,10]], k = 2
Output: 10
Explanation: Choose event 2 for a total value of 10.
Notice that you cannot attend any other event as they overlap, and that you do not have to attend k events.
```

**Example 3:**

```
Input: events = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]], k = 3
Output: 9
Explanation: Although the events do not overlap, you can only attend 3 events. Pick the highest valued three.
```

**Constraints**

- 1 <= k <= events.length
- 1 <= k * events.length <= 106
- 1 <= startDayi <= endDayi <= 109
- 1 <= valuei <= 106

---

## 题目（中文翻译）

给定一个数组 `events`，其中 `events[i] = [startDay_i, endDay_i, value_i]` 表示第 `i` 场活动的开始时间 `startDay_i`、结束时间 `endDay_i`（均为整数），以及参加该活动可获得的价值 `value_i`。同时给定整数 `k`，表示最多可以参加的活动数量上限。

- 同一时间只能参加一场活动。  
- 若决定参加某场活动，必须完整参加整个活动。  
- 结束日是**闭区间**的，即如果一场活动的结束日与另一场活动的开始日在同一天，则这两场活动不能同时参加。

返回在最多参加 `k` 场活动的前提下，能够获得的价值总和的最大值。

### 示例

**示例 1**  
```text
Input: events = [[1,2,4],[3,4,3],[2,3,1]], k = 2
Output: 7
Explanation: 选择下标为 0 和 1（0 基） 的两场活动，总价值为 4 + 3 = 7。
```

**示例 2**  
```text
Input: events = [[1,2,4],[3,4,3],[2,3,10]], k = 2
Output: 10
Explanation: 选择第 2 场活动，价值为 10。由于该活动与其他活动时间重叠，不能再参加其他活动，而且不一定要恰好参加 k 场活动。
```

**示例 3**  
```text
Input: events = [[1,1,1],[2,2,2],[3,3,3],[4,4,4]], k = 3
Output: 9
Explanation: 虽然这些活动互不重叠，但最多只能参加 3 场。挑选价值最高的三场即可得到 9。
```

### 约束条件

- `1 <= k <= events.length`
- `1 <= k * events.length <= 10^6`
- `1 <= startDay_i <= endDay_i <= 10^9`
- `1 <= value_i <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的参加方案**，找出价值和最大的那一种。  
因为我们最多只能参加 `k` 场活动，所以可以把「参加哪几场」看成从 `events` 中挑 `≤k` 个元素的组合。  

- **数据结构**：使用普通的 Python `list` 保存所有活动。  
- **生活化类比**：把每个活动想象成一本书的章节，`startDay`、`endDay` 是章节的起止页码，`value` 是章节的收益。暴力做法就是把所有章节的挑选方式都列出来，像在字典里逐条查找所有可能的组合。  

**正确性**：只要遍历到了所有合法的挑选方式（即没有时间冲突且不超过 `k` 场），我们一定能在这些方式中找到价值最大的那一个。

**时间/空间复杂度**：  
- 设活动数为 `n`，`k ≤ n`。暴力枚举所有组合的数量是 `C(n,0)+C(n,1)+…+C(n,k)`，在最坏情况下接近 `O(2^n)`（因为 `k` 可能接近 `n`）。  
- 每检查一个组合都要遍历选中的活动判断是否冲突，最坏是 `O(k)`。  
- 因此总体时间复杂度约为 **指数级**，`O(2^n)`，在实际数据里根本跑不完。  
- 空间上只需要保存递归栈和当前组合，最多 `O(k)`。

> **大白话**：  
> `O(2^n)` 就像把所有可能的钥匙都试一遍，钥匙的数量随活动数翻倍增长，哪怕只有 20 场活动，也要试上几百万把钥匙，根本不现实。

#### 代码（Python）

```python
from itertools import combinations

def maxValue_bruteforce(events, k):
    """
    暴力枚举：遍历所有 ≤k 场活动的组合，返回价值最大且不冲突的方案。
    """
    n = len(events)
    best = 0

    # 先把事件按结束时间排序，方便后面冲突检测
    events_sorted = sorted(events, key=lambda x: x[1])

    # 枚举选 0~k 场活动的所有组合
    for cnt in range(1, k + 1):
        for combo in combinations(range(n), cnt):
            # 检查是否有时间冲突
            ok = True
            last_end = -1
            total = 0
            for idx in combo:
                s, e, v = events_sorted[idx]
                if s <= last_end:          # 与前一场重叠（包括同一天）
                    ok = False
                    break
                last_end = e
                total += v
            if ok:
                best = max(best, total)

    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n * k)`（指数级），因为要遍历几乎所有子集。  
- **空间复杂度**：`O(k)`，递归/组合生成时的临时存储。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**“是否选当前活动”** 是唯一的二选一决策，而**冲突检查**是瓶颈。  
我们可以把这个决策过程改写成**动态规划（DP）**：  

1. **先把活动按开始时间排序**（也可以按结束时间，只要统一）。  
   - 类比：把所有会议按“开会时间早晚”排好队，后面的决定只会受前面排好序的会议影响。  

2. **状态定义**  
   - `dp[i][j]`：考虑从第 `i` 场活动（`i` 从 0 开始）开始，最多还能参加 `j` 场时，能够得到的最大价值。  
   - 目标是 `dp[0][k]`（从第一场开始，最多 `k` 场）。

3. **状态转移**  
   - **不参加第 i 场**：价值等于 `dp[i+1][j]`（直接跳到下一场，仍然可以参加 `j` 场）。  
   - **参加第 i 场**：我们得到 `value_i`，随后只能参加 **下一个** 与它**不冲突**的活动。  
     - 用二分搜索在已排序的数组中找到**第一个** `startDay` 大于 `endDay_i` 的下标 `next_i`。  
     - 那么剩下的价值是 `dp[next_i][j-1]`（因为已经用了 1 场），总价值为 `value_i + dp[next_i][j-1]`。  
   - 取两者的最大值：  
     ```
     dp[i][j] = max(dp[i+1][j], value_i + dp[next_i][j-1])
     ```

4. **如何快速找到 `next_i`**  
   - 因为活动已按 **开始时间** 排序，`startDays` 是单调递增的数组。  
   - 使用 `bisect_left`（二分查找）在 `startDays` 中找第一个 `> end_i` 的位置，时间 `O(log n)`。

5. **实现细节**  
   - `n` 最多 `10^5`（因为 `k * n ≤ 10^6`），直接使用二维数组 `dp[n+1][k+1]` 可能占用太多内存（`~10^11`）。  
   - 观察到转移只依赖 **下一行**（`i+1`）和 **某个更远的行**（`next_i`），可以把 `dp` 设计为 **一维滚动数组**：`dp[j]` 表示从当前 `i` 开始，最多还能参加 `j` 场的最大价值。  
   - 为了能够在后面查询 `dp[next_i][*]`，我们仍需要保留所有 `i` 的结果。最常见的做法是 **从后往前遍历**，并把每一行的 `dp` 保存到 `dp_table[i]` 中，或者使用 **记忆化递归 + LRUCache**。  
   - 这里采用 **记忆化递归**（自顶向下）配合二分搜索，代码更直观，且只会计算 `n*k` 次状态，满足约束。

6. **复杂度分析**  
   - 每个状态 `dp(i, j)` 只计算一次，状态总数是 `n * k`（`≤ 10^6`），每次转移里有一次二分搜索 `O(log n)`。  
   - 所以时间复杂度 **`O(n * k * log n)`**，在最坏情况下约 `10^6 * log 10^5`，可以轻松跑完。  
   - 记忆化表存储 `n * k` 个整数，空间 **`O(n * k)`**，同样 ≤ `10^6`，符合题目限制。

> **类比图示**（文字版）  
> ```
>   i          i+1        ...   next_i
> ──────┬───────┬───────┬───────┬───────▶ 时间轴
>   ①   │   ②   │   ③   │   ④   │   ⑤
> 选/不选   →   根据二分找下一个不冲突的
> ```

#### 代码（Python）

```python
from bisect import bisect_left
from functools import lru_cache
from typing import List

def maxValue(events: List[List[int]], k: int) -> int:
    """
    动态规划 + 二分搜索的最优解
    1. 按 startDay 排序
    2. 用记忆化递归 dp(i, j) 表示：从第 i 场开始，最多还能参加 j 场，能够获得的最大价值
    3. 状态转移：
       - 不参加第 i 场 -> dp(i+1, j)
       - 参加第 i 场 -> value_i + dp(next_i, j-1)
       取两者最大
    """
    # 1️⃣ 按开始时间排序（若开始相同，按结束时间排序，保持唯一性）
    events.sort(key=lambda x: x[0])
    n = len(events)

    # 把所有的 startDay 拿出来，供二分使用
    starts = [ev[0] for ev in events]

    @lru_cache(maxsize=None)
    def dp(i: int, left: int) -> int:
        """递归求解子问题，i 为当前考虑的活动下标，left 为还能参加的次数"""
        if i == n or left == 0:          # 没有活动可选或已经用完名额
            return 0

        # ① 不参加第 i 场
        skip = dp(i + 1, left)

        # ② 参加第 i 场
        s, e, val = events[i]
        # 二分找下一个 startDay > e（不冲突的第一场）
        nxt = bisect_left(starts, e + 1, lo=i + 1)   # lo=i+1 保证向后搜索
        take = val + dp(nxt, left - 1)

        # ③ 取最大值
        return max(skip, take)

    return dp(0, k)
```

#### 复杂度

- **时间复杂度**：`O(n * k * log n)`  
  - `n * k` 是状态总数（上限 `10^6`），每个状态内部一次二分 `log n`（约 17），所以整体约几千万次操作，能够在 1 秒左右完成。  
  - 与暴力解的 `O(2^n)` 相比，**指数级**被压缩成了 **线性乘对数**，快得多。

- **空间复杂度**：`O(n * k)`（记忆化表） + 递归栈 `O(n)`，总体约 `10^6` 个整数，约几 MB，完全可接受。  

---

## 心得

- **核心技巧**：**动态规划 + 二分搜索**（把“下一个不冲突的活动”转化为快速查询）。  
- **适用的题型**  
  1. “选择若干不相交区间，求最大价值”——如 *Maximum Profit in Job Scheduling*。  
  2. “在序列上做有限次数的选择，每次选择后跳到满足条件的下一个位置”——如 *Maximum Number of Events That Can Be Attended*（k=1）或 *Best Time to Buy and Sell Stock IV*（交易次数限制）。  
- **一句话总结解题钥匙**：**把“下一个可选的活动”抽象成二分查找，再用 DP 把“选或不选”递归下来**。

---

## 反思

- **第一反应**：看到“最多参加 k 场，且不能重叠”，立刻想到**区间调度**的 DP 思路。  
- **最容易踩的坑**  
  - **二分的界限**：结束日是**包含**的，需要在二分时搜索 `endDay + 1`（而不是 `endDay`），否则会误把相邻的活动算作不冲突。  
  - **递归/迭代的顺序**：若从前往后遍历而没有记忆化，会出现重复计算，导致超时。  
  - **状态边界**：`left == 0` 或 `i == n` 时必须返回 0，防止访问负索引或无限递归。  
- **下次类似题的第一步**：先**排序**（通常是按开始或结束时间），然后**用二分找下一个合法位置**，最后**套上 DP（或记忆化递归）**。这样可以把指数级搜索压缩到可接受的规模。