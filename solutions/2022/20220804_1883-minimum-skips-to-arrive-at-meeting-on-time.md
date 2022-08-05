# #1883. 最少跳过次数以准时到达会议 / Minimum Skips to Arrive at Meeting On Time

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-skips-to-arrive-at-meeting-on-time/)

---

## 题目（英文原版）

**Description**

You are given an integer hoursBefore, the number of hours you have to travel to your meeting. To arrive at your meeting, you have to travel through n roads. The road lengths are given as an integer array dist of length n, where dist[i] describes the length of the ith road in kilometers. In addition, you are given an integer speed, which is the speed (in km/h) you will travel at.
After you travel road i, you must rest and wait for the next integer hour before you can begin traveling on the next road. Note that you do not have to rest after traveling the last road because you are already at the meeting.
However, you are allowed to skip some rests to be able to arrive on time, meaning you do not need to wait for the next integer hour. Note that this means you may finish traveling future roads at different hour marks.
Return the minimum number of skips required to arrive at the meeting on time, or -1 if it is impossible.

**Examples**

**Example 1:**

```
Input: dist = [1,3,2], speed = 4, hoursBefore = 2
Output: 1
Explanation:
Without skipping any rests, you will arrive in (1/4 + 3/4) + (3/4 + 1/4) + (2/4) = 2.5 hours.
You can skip the first rest to arrive in ((1/4 + 0) + (3/4 + 0)) + (2/4) = 1.5 hours.
Note that the second rest is shortened because you finish traveling the second road at an integer hour due to skipping the first rest.
```

**Example 2:**

```
Input: dist = [7,3,5,5], speed = 2, hoursBefore = 10
Output: 2
Explanation:
Without skipping any rests, you will arrive in (7/2 + 1/2) + (3/2 + 1/2) + (5/2 + 1/2) + (5/2) = 11.5 hours.
You can skip the first and third rest to arrive in ((7/2 + 0) + (3/2 + 0)) + ((5/2 + 0) + (5/2)) = 10 hours.
```

**Example 3:**

```
Input: dist = [7,3,5,5], speed = 1, hoursBefore = 10
Output: -1
Explanation: It is impossible to arrive at the meeting on time even if you skip all the rests.
```

**Constraints**

- n == dist.length
- 1 <= n <= 1000
- 1 <= dist[i] <= 105
- 1 <= speed <= 106
- 1 <= hoursBefore <= 107

---

## 题目（中文翻译）

**题目描述**  
给定整数 `hoursBefore`，表示你需要在多少小时内到达会议。要参加会议，你必须依次行驶 `n` 条道路。道路长度由长度为 `n` 的整数数组 `dist` 给出，其中 `dist[i]` 表示第 `i` 条道路的长度（公里）。另外，给定整数 `speed`，表示你的行驶速度（km/h）。

在行驶完第 `i` 条道路后，你必须休息并等待到下一个整数小时才能开始行驶下一条道路。注意，行驶完最后一条道路后不需要休息，因为已经到达会议地点。  

然而，你可以选择**跳过**（skip）某些休息，以便准时到达，这意味着可以不等待下一个整数小时。跳过休息后，后续道路的结束时间可能不再是整数小时。  

返回为准时到达会议所需的最小跳过次数。如果无法在规定时间内到达，返回 `-1`。

**示例**  

*示例 1*  
```
Input: dist = [1,3,2], speed = 4, hoursBefore = 2
Output: 1
Explanation:
不跳过任何休息时，你的总耗时为 (1/4 + 3/4) + (3/4 + 1/4) + (2/4) = 2.5 小时。
如果跳过第一次休息，则耗时为 ((1/4 + 0) + (3/4 + 0)) + (2/4) = 1.5 小时。
注意，由于跳过了第一次休息，第二次休息被缩短，因为此时你在整数小时结束了第二条道路的行驶。
```

*示例 2*  
```
Input: dist = [7,3,5,5], speed = 2, hoursBefore = 10
Output: 2
Explanation:
不跳过任何休息时，总耗时为 (7/2 + 1/2) + (3/2 + 1/2) + (5/2 + 1/2) + (5/2) = 11.5 小时。
如果跳过第一次和第三次休息，则耗时为 ((7/2 + 0) + (3/2 + 0)) + ((5/2 + 0) + (5/2)) = 10 小时。
```

*示例 3*  
```
Input: dist = [7,3,5,5], speed = 1, hoursBefore = 10
Output: -1
Explanation:
即使跳过所有休息，也无法在规定时间内到达会议，答案为 -1。
```

**约束条件**  
- `n == dist.length`
- `1 <= n <= 1000`
- `1 <= dist[i] <= 10^5`
- `1 <= speed <= 10^6`
- `1 <= hoursBefore <= 10^7`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每一段路的“是否跳过休息”全部枚举**，然后算出总用时，挑出满足 `hoursBefore` 的最小跳过次数。  
- **数据结构**：我们可以用 **递归**（或者显式的 `for` 循环）把每一条路当成一次“决定”。递归的参数是当前所在的道路下标 `i`、已经用了多少跳（`skip`）以及当前累计的时间 `curTime`。  
- **生活化类比**：想象你在走一条长长的走廊，每走完一段就要等电梯到达整点才能继续前进。你可以选择不等电梯（即“跳过休息”），直接继续走。暴力做法就是把每段走廊的“等不等电梯”全部写成一张**决策表**，每行对应一种决策组合。  
- **为什么正确**：因为我们把 **所有** 可能的跳过方式都遍历了一遍，必然能找到最少跳次数的那一种（如果有解的话）。  

**缺点**：  
- 当路的数量 `n` 达到 1000 时，决策的组合数是 `2^n`，根本算不完。  
- 甚至在 `n=20` 时，组合数已接近一百万，已经超出常规的时间限制。  

#### 代码（Python）  

```python
import math
from typing import List

def minSkips_bruteforce(dist: List[int], speed: int, hoursBefore: int) -> int:
    n = len(dist)

    # 递归尝试每条路是否跳过休息
    def dfs(i: int, skips: int, cur: float) -> int:
        # 已经走完所有道路
        if i == n:
            # 判断是否在规定时间内到达
            return skips if cur <= hoursBefore else float('inf')
        # 走完第 i 条路需要的时间
        travel = dist[i] / speed
        cur += travel

        # 1️⃣ 不跳休息（除最后一条路外必须等到下一个整数小时）
        if i != n - 1:
            nxt = math.ceil(cur)          # 向上取整到最近的整数小时
            res_no_skip = dfs(i + 1, skips, nxt)
        else:   # 最后一条路不需要等
            res_no_skip = dfs(i + 1, skips, cur)

        # 2️⃣ 跳过休息（直接进入下一段路）
        res_skip = dfs(i + 1, skips + 1, cur)

        # 取两种情况的最小跳数
        return min(res_no_skip, res_skip)

    ans = dfs(0, 0, 0.0)
    return -1 if ans == float('inf') else ans
```

> **注释**  
> - `math.ceil(cur)` 把当前时间向上取整，相当于“等到下一个整数小时”。  
> - `float('inf')` 用来表示一种不可能的状态（超时），最后再转换成 `-1`。  

#### 复杂度  

- **时间复杂度**：`O(2^n)`——每条路都有“跳/不跳”两种选择，整体是指数级别的。  
- **空间复杂度**：`O(n)`——递归栈的深度最多为 `n`，每层只保存少量变量。  

> **大白话解释**：  
> - `2^n` 就像把 `n` 个人排成一排，每个人都可以举手或不举手，所有可能的手势组合总数。随着人数（道路）增多，组合数会飞快增长，根本算不过来。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**“到底在第几条路、用了多少次跳”** 是决定后续状态的关键信息。我们可以把这两个量做成**状态**，用 **动态规划（DP）** 把所有可能的状态一次性算出来，而不是一次次重复递归。

**状态定义**  
- `dp[i][k]` = **走完前 i 条路（下标 0 … i‑1），恰好用了 k 次跳过休息后，累计的最小时间**。  
- `i` 的取值范围是 `1 … n`（第 i 条路已经走完），`k` 的取值范围是 `0 … i‑1`（最多每条路都跳一次）。

**状态转移**  
假设我们已经知道 `dp[i][k]`（走完第 `i` 条路的最小时间），要计算走完第 `i+1` 条路的时间，有两种选择：

1. **不跳**  
   - 先走第 `i+1` 条路，需要 `dist[i] / speed` 小时。  
   - 如果这不是最后一条路，需要等到下一个整数小时再继续，即 `ceil(dp[i][k] + dist[i]/speed)`。  
   - 对应转移式  
     ```text
     dp[i+1][k] = min(dp[i+1][k], ceil(dp[i][k] + travel))
     ```
   - 这里的 `ceil` 只在 `i+1 != n` 时生效（最后一条路不需要等）。

2. **跳**  
   - 直接在当前时间上加上路程时间，不再向上取整。  
   - 跳一次会让已使用的跳数加 1。  
   - 对应转移式  
     ```text
     dp[i+1][k+1] = min(dp[i+1][k+1], dp[i][k] + travel)
     ```

**为什么是最优**  
- DP 把所有 **“走到第 i 条路、用了 k 次跳”** 的可能时间都记住了，后面的决定只会基于这些**最小**时间继续扩展。  
- 因为每一次转移都取了 **最小**，最终 `dp[n][k]`（走完所有道路）必然是对应跳数 `k` 的最小耗时。  

**如何得到答案**  
遍历所有可能的跳数 `k`（从 `0` 到 `n-1`），找到第一个满足 `dp[n][k] ≤ hoursBefore` 的 `k`，即为最少跳数。如果没有任何 `k` 能满足，则返回 `-1`。

**实现细节**  
- `ceil` 可以用 `math.ceil`，但因为我们只处理 **正数**，也可以写成 `(t + 1e-9).is_integer()` 之类的技巧，这里直接用 `math.ceil` 更直观。  
- 为了节约空间，只需要保留上一行的 DP 数组即可（因为转移只依赖 `i` 那一层），所以整体空间可以压缩到 `O(n)`。  

**类比**：  
想象你在玩一款“层层闯关”的游戏，每闯过一关会记录下当前的时间以及已经用了多少次“加速道具”。每一次你可以决定是否使用道具（跳过休息），系统会帮你记住每种道具使用次数对应的最快通关时间。最后，只要找出最少道具数能在规定时间内通关的那一次，就得到答案。

#### 代码（Python）  

```python
import math
from typing import List

def minSkips(dist: List[int], speed: int, hoursBefore: int) -> int:
    n = len(dist)
    # dp[k] 表示已经走完当前处理的道路，恰好用了 k 次跳的最小时间
    # 初始只走完 0 条路，时间为 0，跳数 0
    dp = [float('inf')] * (n + 1)
    dp[0] = 0.0

    for i in range(n):                     # 逐条道路处理
        travel = dist[i] / speed           # 走完第 i 条路需要的时间
        ndp = [float('inf')] * (n + 1)     # 为第 i+1 条路准备新表

        for k in range(i + 1):             # 已经最多用了 i 次跳
            cur = dp[k]
            if cur == float('inf'):
                continue

            # 1️⃣ 不跳（如果不是最后一条路，需要向上取整）
            if i == n - 1:                 # 最后一条路不需要等
                nxt = cur + travel
            else:
                nxt = math.ceil(cur + travel)   # 等到下一个整数小时
            ndp[k] = min(ndp[k], nxt)

            # 2️⃣ 跳过休息（跳数 +1，时间直接相加）
            ndp[k + 1] = min(ndp[k + 1], cur + travel)

        dp = ndp                           # 换成新一层的结果

    # 在所有可能的跳数中找最小的满足时间限制的 k
    for k in range(n + 1):
        if dp[k] <= hoursBefore + 1e-9:   # 加个极小容差防止浮点误差
            return k
    return -1
```

> **关键行中文注释**  
> - `travel = dist[i] / speed` # 第 i 条路的行驶时间（公里 ÷ 公里/小时）  
> - `math.ceil(cur + travel)` # “不跳”时需要等到下一个整数小时，向上取整  
> - `ndp[k + 1] = min(ndp[k + 1], cur + travel)` # “跳”时直接累加时间，跳数加 1  
> - `if dp[k] <= hoursBefore + 1e-9` # 浮点数比较时加一点容差，防止 2.0000000001 被误判  

#### 复杂度  

- **时间复杂度**：`O(n^2)`  
  - 外层循环 `n` 次（遍历每条路），内层最多遍历 `i+1 ≤ n` 种跳数，总共约 `n*(n+1)/2` 次更新。  
  - 与暴力的 `2^n` 相比，`n^2`（例如 `1000^2 = 1,000,000`）在机器上毫秒级即可完成。  

- **空间复杂度**：`O(n)`  
  - 只保留当前层和下一层的 DP 数组，各长 `n+1`，而不是完整的 `n×n` 表。  

> **大白话解释**：  
> - `O(n^2)` 就像在一个 `1000×1000` 的格子里走一次遍历，最多走一百万步，电脑可以轻松完成。  
> - `O(n)` 只需要存一行数据，就像只记住当前这条路的状态，而不必记住所有之前的细节。  

---  

## 心得  

- **核心技巧**：把“已走路段数 + 已使用跳数”作为状态，用**动态规划**一次性算出每种跳数对应的最小时间。  
- **适用的题型**：  
  1. 需要在每一步做“是否使用资源”的二选一决策，且后续结果只依赖当前累计值的题目（如「最小修改次数使数组递增」）。  
  2. 需要在每一步「向上取整」或「保持原值」的情形（如「最小跳数到达终点」的时间取整版）。  
- **一句话总结解题钥匙**：**把“跳的次数”放进 DP 状态，利用向上取整的规则在转移时分别处理“跳/不跳”。**  

## 反思  

- **第一反应**：看到“每段路后要等到整数小时”，立刻想到“向上取整”，于是把每段路的结束时间视为离散的整数点。  
- **最容易踩的坑**：  
  - **浮点数误差**：`dist[i] / speed` 可能产生 0.999999…，直接比较会出错，最好加个极小容差或使用分数（`Fraction`）实现。  
  - **最后一段路不需要等**：忘记在 `i == n-1` 时不进行 `ceil`，会导致答案偏大。  
  - **跳次数上限**：最多只能跳 `n-1` 次（最后一段路不需要休息），但 DP 表预留了 `n`，不影响正确性，只是要注意遍历范围。  
- **下次类似题的第一步**：先**明确哪些信息会影响后续**（这里是“已使用的跳次数”），把它们加入 DP 状态，再**写出两种转移**（使用资源 / 不使用资源），最后在所有状态中寻找满足约束的最优解。