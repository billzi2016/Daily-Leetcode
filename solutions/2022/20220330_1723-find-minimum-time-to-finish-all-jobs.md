# #1723. 寻找完成所有工作的最小时间 / Find Minimum Time to Finish All Jobs

> 难度：困难 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/find-minimum-time-to-finish-all-jobs/)

---

## 题目（英文原版）

**Description**

You are given an integer array jobs, where jobs[i] is the amount of time it takes to complete the ith job.
There are k workers that you can assign jobs to. Each job should be assigned to exactly one worker. The working time of a worker is the sum of the time it takes to complete all jobs assigned to them. Your goal is to devise an optimal assignment such that the maximum working time of any worker is minimized.
Return the minimum possible maximum working time of any assignment.

**Examples**

**Example 1:**

```
Input: jobs = [3,2,3], k = 3
Output: 3
Explanation: By assigning each person one job, the maximum time is 3.
```

**Example 2:**

```
Input: jobs = [1,2,4,7,8], k = 2
Output: 11
Explanation: Assign the jobs the following way:
Worker 1: 1, 2, 8 (working time = 1 + 2 + 8 = 11)
Worker 2: 4, 7 (working time = 4 + 7 = 11)
The maximum working time is 11.
```

**Constraints**

- 1 <= k <= jobs.length <= 12
- 1 <= jobs[i] <= 107

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `jobs`，其中 `jobs[i]` 表示第 i 个工作的所需时间。  
现在有 `k` 名工人，你需要将所有工作分配给这些工人。每个工作必须恰好分配给一名工人。  
某名工人的工作时长等于分配给他的所有工作时间之和。  
你的目标是设计一种最优的分配方案，使得所有工人中**最大工作时长**（maximum working time）最小化。  
返回在所有可能的分配方式中能够得到的最小的最大工作时长。

**示例 1**  
> **输入**: `jobs = [3,2,3]`, `k = 3`  
> **输出**: `3`  
> **解释**: 将每个人各分配一个工作，最大工作时长为 3。

**示例 2**  
> **输入**: `jobs = [1,2,4,7,8]`, `k = 2`  
> **输出**: `11`  
> **解释**: 按如下方式分配工作：  
> - 工人 1: 1, 2, 8 → 工作时长 = 1 + 2 + 8 = 11  
> - 工人 2: 4, 7 → 工作时长 = 4 + 7 = 11  
> 此时的最大工作时长为 11。

**约束条件**  
- `1 <= k <= jobs.length <= 12`  
- `1 <= jobs[i] <= 10^7`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把 **每一份工作** 按顺序交给 **k 位工人中的任意一位**，把所有可能的分配方式都枚举一遍，最后取所有方案里“最大工时最小”的那个。  

- **数据结构**：我们只需要一个长度为 `k` 的数组 `load` 来记录每位工人当前已经分配的工作总时长。把 `load[i]` 想象成 **工人的背包**，往背包里放工作时间，就是在往背包里加重量。  
- **为什么正确**：因为我们遍历了所有合法的分配（每个工作恰好被分配一次），所以一定能找到最优解。  
- **复杂度大白话**：如果有 `n` 份工作，每份工作都有 `k` 种放法，那么总共要检查 `k × k × … × k = kⁿ` 种情况。这里的 `kⁿ` 看起来像 `k` 的 `n` 次方，意思是“指数级增长”，即 **随着工作数量稍微多一点，计算量就会爆炸**。  

#### 代码（Python）  

```python
from typing import List

def minimumTimeRequired(jobs: List[int], k: int) -> int:
    n = len(jobs)
    # 为了加速剪枝，把大的工作先安排（大工作先放容易提前发现“超限”）
    jobs.sort(reverse=True)

    # 记录每位工人的当前工作总时长
    load = [0] * k
    ans = sum(jobs)                     # 初始答案设为所有工作时间之和（最坏情况）

    def dfs(idx: int):
        """把第 idx 份工作分配给某位工人"""
        nonlocal ans
        if idx == n:                     # 所有工作都已分配完
            ans = min(ans, max(load))    # 更新最小的最大工时
            return

        cur = jobs[idx]
        visited = set()                  # 用来避免把相同负载的工人重复尝试
        for i in range(k):
            if load[i] in visited:       # 同样负载的工人已经尝试过，跳过
                continue
            if load[i] + cur >= ans:     # 剪枝：已经不可能比当前最优更好
                continue
            visited.add(load[i])
            load[i] += cur                # 把当前工作放进第 i 位工人的背包
            dfs(idx + 1)                  # 递归分配下一份工作
            load[i] -= cur                # 回溯，撤销这一步

    dfs(0)
    return ans
```

> **关键行中文注释**  
> - `jobs.sort(reverse=True)`：把“大工作”先安排，类似先把重的砖块放到底部，容易提前发现不合法。  
> - `visited`：防止把“负载相同的工人”重复尝试，等价于“把相同的钥匙只用一次”。  
> - `if load[i] + cur >= ans`：如果这一步已经让某位工人的工作时间不小于当前最好的答案，就没有必要继续往下搜了——这叫 **剪枝**，可以大幅削减搜索树。

#### 复杂度  

- **时间复杂度**：最坏情况是 `O(kⁿ)`，因为我们会尝试每份工作 `k` 种放法。指数级的 `kⁿ` 意味着即使 `n=12、k=3` 也已经有 `3¹² ≈ 531,441` 种情况。  
- **空间复杂度**：`O(k + n)`，主要是递归栈深度 `n`（最多 12）和 `k` 长度的 `load` 数组，都是常数级别的额外空间。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“每次都要遍历所有 k 位工人”**，导致搜索树呈指数增长。  
观察到 **工作数量最多只有 12**，这让我们可以把“哪些工作已经被安排”用一个 **位掩码 (bitmask)** 来表示：  
- 用二进制的 12 位表示 12 份工作，`1` 表示这份工作已经被分配，`0` 表示未分配。  
- 这样，一个状态只用一个整数（最多 `2¹² = 4096`）就能完整描述。  

接下来我们把 **“是否可以在不超过某个上限 limit 的情况下，把所有工作分配给 k 位工人”** 这个判定问题转化为 **子集划分**：  
1. **二分搜索** `limit`：答案一定在 `[max(jobs), sum(jobs)]` 之间，二分可以在对数次数内逼近最小的可行上限。  
2. 对每个 `limit`，用 **DP + 位掩码** 检查是否可以把所有工作划分成不超过 `k` 组，每组的工作时间 ≤ `limit`。  

DP 的核心是：  
- 预先计算每个子集 `mask` 的工作总时长 `sum[mask]`（相当于把“这几块砖的重量”提前算好）。  
- `dp[mask]` 表示 **把子集 `mask` 分配完以后，当前正在使用的工人的已使用时间**（如果已经用了 `cnt` 位工人，则 `dp[mask]` 必然 < `limit`）。  
- 转移时：尝试把一个未分配的子集 `sub` 加入当前工人，如果 `dp[mask] + sum[sub] ≤ limit`，则 `dp[mask | sub] = dp[mask] + sum[sub]`；否则说明需要新开一位工人，`dp[mask | sub] = sum[sub]`（只要新工人的负载不超过 `limit`）。  

只要最终状态 `dp[(1<<n)-1]`（全部工作都分配完）对应的工人数 ≤ `k`，说明在当前 `limit` 下可行。  

**类比**：想象我们有一堆重量不等的行李，要装进 **最多 k 个行李箱**，每个行李箱的容量上限是 `limit`。我们先把所有行李的组合重量算好（子集求和），再用 DP “把行李箱装满” 看看能否在 `k` 个箱子里装完。  

#### 代码（Python）  

```python
from typing import List
from functools import lru_cache

def minimumTimeRequired(jobs: List[int], k: int) -> int:
    n = len(jobs)
    # 预处理：子集对应的总工作时间
    total = [0] * (1 << n)               # total[mask] = jobs 中对应位为 1 的工作时间之和
    for mask in range(1 << n):
        s = 0
        for i in range(n):
            if mask >> i & 1:            # mask 的第 i 位为 1，说明第 i 份工作在这个子集中
                s += jobs[i]
        total[mask] = s

    # 二分搜索答案的上界
    left, right = max(jobs), sum(jobs)

    def can(limit: int) -> bool:
        """
        判断是否能在每位工人工作时间 ≤ limit 的前提下，把所有工作分配给不超过 k 位工人。
        """
        # dp[mask] = 当前正在使用的工人的已占用时间（一定 < limit），
        #            如果 dp[mask] = -1 说明该状态不可达
        dp = [-1] * (1 << n)
        dp[0] = 0                         # 什么工作都没安排时，已占用时间为 0

        for mask in range(1 << n):
            if dp[mask] == -1:            # 这个子集不可达，直接跳过
                continue
            # 尝试把剩余的工作再划分一个子集 sub 加进去
            remaining = ((1 << n) - 1) ^ mask      # 还没安排的工作位集合
            sub = remaining
            while sub:
                # 只考虑子集 sum 不超过 limit 的情况
                if total[sub] <= limit:
                    # 如果当前工人还能再装下 sub，则不需要新开工人
                    if dp[mask] + total[sub] <= limit:
                        nxt = mask | sub
                        if dp[nxt] == -1 or dp[nxt] > dp[mask] + total[sub]:
                            dp[nxt] = dp[mask] + total[sub]
                    else:
                        # 需要新开一位工人来装 sub（只要 sub 本身不超 limit）
                        nxt = mask | sub
                        if dp[nxt] == -1 or dp[nxt] > total[sub]:
                            dp[nxt] = total[sub]
                sub = (sub - 1) & remaining   # 枚举 remaining 的所有非空子集

        # 最终状态是否只用了不超过 k 位工人？
        # dp[full] 保存的是最后一位工人的已占用时间，只要它不是 -1，说明能安排
        # 再算出用了多少工人：每次“新开工人”相当于一次 reset，最多 k 次
        # 为了简化，这里直接用 BFS 方式检查工人数是否 ≤ k（因为 n≤12，状态少）
        from collections import deque
        q = deque()
        q.append((0, 0))                     # (已安排的 mask, 已使用的工人数)
        visited = set()
        visited.add((0, 0))
        while q:
            cur_mask, used = q.popleft()
            if cur_mask == (1 << n) - 1:
                if used <= k:
                    return True
                continue
            if used >= k:                    # 已经用完 k 位工人，不能再继续
                continue
            # 继续为第 used 位工人挑选一个子集
            remain = ((1 << n) - 1) ^ cur_mask
            sub = remain
            while sub:
                if total[sub] <= limit:
                    nxt_mask = cur_mask | sub
                    state = (nxt_mask, used + 1)
                    if state not in visited:
                        visited.add(state)
                        q.append(state)
                sub = (sub - 1) & remain
        return False

    # 二分搜索最小的可行 limit
    while left < right:
        mid = (left + right) // 2
        if can(mid):
            right = mid          # 还能更小，收紧上界
        else:
            left = mid + 1       # 需要更大的上限
    return left
```

> **代码要点中文注释**  
> - `total[mask]`：把每个子集的工作时间提前算好，类似 **先把每袋子里装了多少货先记下来**，后面查询时 O(1)。  
> - `while sub:` 循环：在位运算里 `sub = (sub - 1) & remaining` 可以 **高效遍历一个集合的所有子集**，不需要额外的循环。  
> - `can(limit)`：使用 **二分 + 子集 DP** 判定是否可行。二分把搜索范围从线性降到对数，DP 把指数搜索树压缩到 `2ⁿ`（最多 4096）状态。  

#### 复杂度  

- **时间复杂度**：  
  - 预处理 `total[mask]`：`O(n * 2ⁿ)`（每个子集遍历最多 `n` 位），这里 `n ≤ 12`，约 `12·4096 ≈ 5e4`。  
  - 二分搜索次数是 `log₂(sum(jobs) - max(jobs) + 1)`，最多约 **30 次**（因为 `jobs[i] ≤ 10⁷`）。  
  - 每次判定 `can(limit)` 里我们遍历所有子集并对每个子集再遍历其子集，最坏是 `O(3ⁿ)`，但实际因为 `n` 很小且剪枝（`total[sub] ≤ limit`）会大幅削减。整体时间约为 `O( log(S) * 3ⁿ )`，在 `n ≤ 12` 时运行毫秒级。  
- **空间复杂度**：`O(2ⁿ)` 用于存 `total` 与 `dp`（最多 4096），再加上递归/队列的额外 O(2ⁿ) 状态，整体是 **线性于子集数**，即几千个整数，几乎可以忽略不计。  

相比暴力的 `O(kⁿ)`（指数底为 `k`），这里的底是 **3**（因为每个元素在子集划分中有三种状态：在当前工人、在新工人、未使用），且加入了二分搜索，大幅提升效率。  

---  

## 心得  

- **核心技巧**：**位掩码 + 子集 DP + 二分搜索**。  
- **适用的题型**：  
  1. “把 N（≤ 15）个物品分配到 K（≤ N）个桶，使最大桶容量最小”——如 **分配工作、装箱、任务调度**。  
  2. “判断是否可以把集合划分为若干子集，每个子集满足某个约束”——如 **分割等和子集、背包的多子集变体**。  
  3. “最小化最大值” 的二分 + 可行性判定模板——如 **分配香蕉、分配文件**。  
- **一句话总结**：把“所有工作是否能在上限 limit 下分配完”抽象成 **子集可行性判定**，用位掩码高效枚举，再用二分搜索逼近最小的可行 limit。  

---  

## 反思  

- **第一反应**：看到 “最大工作时间最小化”，自然想到 **二分答案 + 回溯**，但没立刻想到用 **位掩码** 来压缩状态。  
- **最容易踩的坑**：  
  1. **子集遍历的顺序**：`sub = (sub - 1) & remaining` 必须放在循环体的最后，否则会陷入死循环。  
  2. **剪枝条件**：忘记 `total[sub] ≤ limit` 会导致尝试无效子集，时间爆炸。  
  3. **边界**：答案下界是 `max(jobs)`（单个工作必须完整给一个人），上界是 `sum(jobs)`（所有工作都交给同一个人），二分时一定要包含这两个端点。  
- **下次遇到同类题**：第一步先 **确定搜索空间**（最小/最大可能值），再 **用二分搜索** 把“是否可行”变成子问题；子问题若涉及“是否能把集合划分成若干满足约束的子集”，就考虑 **位掩码 + 子集 DP**。