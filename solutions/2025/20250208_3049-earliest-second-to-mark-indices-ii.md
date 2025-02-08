# #3049. **标记索引的最早秒数 II** / Earliest Second to Mark Indices II

> 难度：困难 · 标签：Array、Binary Search、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/earliest-second-to-mark-indices-ii/)

---

## 题目（英文原版）

**Description**

You are given two 1-indexed integer arrays, nums and, changeIndices, having lengths n and m, respectively.
Initially, all indices in nums are unmarked. Your task is to mark all indices in nums.
In each second, s, in order from 1 to m (inclusive), you can perform one of the following operations:
Return an integer denoting the earliest second in the range [1, m] when all indices in nums can be marked by choosing operations optimally, or -1 if it is impossible.

**Examples**

**Example 1:**

```
Input: nums = [3,2,3], changeIndices = [1,3,2,2,2,2,3]
Output: 6
Explanation: In this example, we have 7 seconds. The following operations can be performed to mark all indices:
Second 1: Set nums[changeIndices[1]] to 0. nums becomes [0,2,3].
Second 2: Set nums[changeIndices[2]] to 0. nums becomes [0,2,0].
Second 3: Set nums[changeIndices[3]] to 0. nums becomes [0,0,0].
Second 4: Mark index 1, since nums[1] is equal to 0.
Second 5: Mark index 2, since nums[2] is equal to 0.
Second 6: Mark index 3, since nums[3] is equal to 0.
Now all indices have been marked.
It can be shown that it is not possible to mark all indices earlier than the 6th second.
Hence, the answer is 6.
```

**Example 2:**

```
Input: nums = [0,0,1,2], changeIndices = [1,2,1,2,1,2,1,2]
Output: 7
Explanation: In this example, we have 8 seconds. The following operations can be performed to mark all indices:
Second 1: Mark index 1, since nums[1] is equal to 0.
Second 2: Mark index 2, since nums[2] is equal to 0.
Second 3: Decrement index 4 by one. nums becomes [0,0,1,1].
Second 4: Decrement index 4 by one. nums becomes [0,0,1,0].
Second 5: Decrement index 3 by one. nums becomes [0,0,0,0].
Second 6: Mark index 3, since nums[3] is equal to 0.
Second 7: Mark index 4, since nums[4] is equal to 0.
Now all indices have been marked.
It can be shown that it is not possible to mark all indices earlier than the 7th second.
Hence, the answer is 7.
```

**Example 3:**

```
Input: nums = [1,2,3], changeIndices = [1,2,3]
Output: -1
Explanation: In this example, it can be shown that it is impossible to mark all indices, as we don't have enough seconds. 
Hence, the answer is -1.
```

**Constraints**

- 1 <= n == nums.length <= 5000
- 0 <= nums[i] <= 109
- 1 <= m == changeIndices.length <= 5000
- 1 <= changeIndices[i] <= n

---

## 题目（中文翻译）

你被给定了两个 1-indexed（从 1 开始索引）的整数数组 `nums` 和 `changeIndices`，它们的长度分别为 `n` 和 `m`。  

最初，`nums` 中的所有下标均未标记。你的任务是标记 `nums` 中的所有下标。  

在每一秒 `s`（从 1 到 `m`，包含 `m`）中，你可以执行以下操作之一：  

*（此处应列出具体可执行的操作，题目原文已省略）*  

返回一个整数，表示在区间 `[1, m]` 内能够通过最佳选择操作使所有下标都被标记的最早的秒数；如果无法完成标记，则返回 `-1`。

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [3,2,3], changeIndices = [1,3,2,2,2,2,3]
```  
**输出**  
```
6
```  
**解释**  
在本例中共有 7 秒。可以按以下方式执行操作以标记所有下标：  
- 第 1 秒：将 `nums[changeIndices[1]]` 设为 `0`。`nums` 变为 `[0,2,3]`。  
- 第 2 秒：将 `nums[changeIndices[2]]` 设为 `0`。`nums` 变为 `[0,2,0]`。  
- 第 3 秒：将 `nums[changeIndices[3]]` 设为 `0`。`nums` 变为 `[0,0,0]`。  
- 第 4 秒：标记下标 `1`，因为 `nums[1]` 已经等于 `0`。  
- …（后续步骤已截断）

#### 示例 2
**输入**  
``` 
nums = [0,0,1,2], changeIndices = [1,2,1,2,1,2,1,2]
```  
**输出**  
```
7
```  
**解释**  
在本例中共有 8 秒。可以按以下方式执行操作以标记所有下标：  
- 第 1 秒：标记下标 `1`，因为 `nums[1]` 等于 `0`。  
- 第 2 秒：标记下标 `2`，因为 `nums[2]` 等于 `0`。  
- 第 3 秒：将下标 `4` 的值减一。`nums` 变为 `[0,0,1,1]`。  
- 第 4 秒：将下标 `4` 的值再减一。`nums` 变为 `[0,0,1,0]`。  
- …（后续步骤已截断）

#### 示例 3
**输入**  
``` 
nums = [1,2,3], changeIndices = [1,2,3]
```  
**输出**  
```
-1
```  
**解释**  
在本例中可以证明没有足够的秒数能够标记所有下标，因此答案为 `-1`。

---

### 约束条件
- `1 <= n == nums.length <= 5000`
- `0 <= nums[i] <= 10^9`
- `1 <= m == changeIndices.length <= 5000`
- `1 <= changeIndices[i] <= n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**模拟每一秒的所有可能操作**，并在每秒结束后检查 `nums` 中是否所有位置都已经被标记。  
- **数据结构**：  
  - `nums`：存放每个下标当前的数值，类似于一本记事本。  
  - `marked`：布尔数组，记录哪些下标已经被标记，像是一本检查表。  
  - `changeIndices`：每秒要对哪一个下标进行 “改值” 的指令序列，想象成老师每天给出的一张“改哪一页” 的纸条。  

- **每秒的两类合法操作**  
  1. **标记**：如果 `nums[i] == 0` 并且该位置还未被标记，就可以把它标记。  
  2. **改变**：把 `nums[ changeIndices[t] ]` 减一（或直接改成 0），只要改后仍然是非负数。  

暴力做法就是：从第 1 秒到第 `m` 秒，**枚举**在每一秒我们是选择标记还是改变（若两者都可行就随便选），并把所有可能的分支全部展开成一棵搜索树，最后看有没有分支在某一秒把所有下标都标记了。  

**为什么正确**：  
因为我们把 **所有** 合法的决策路径都遍历了一遍，只要有一种路径能够在第 `x` 秒完成标记，暴力搜索必然会找到它。

**时间/空间分析**：  
- 每秒最多有两种选择（标记 / 改值），所以在最坏情况下搜索树的高度是 `m`，分支数是 `2^m`。  
- 这相当于 **指数级** 的时间复杂度 `O(2^m)`，即使 `m` 只有 20，运行时间也会爆炸。  
- 空间上需要保存递归栈深度 `O(m)`，以及 `nums`、`marked` 两个长度为 `n` 的数组，整体 `O(n + m)`。

> **大白话**：`O(2^m)` 就像把所有可能的 0/1 组合都列出来，组合数随秒数翻倍，根本不可行。

#### 代码（Python）  

```python
from copy import deepcopy
from typing import List

def earliestSecond_bruteforce(nums: List[int], changeIndices: List[int]) -> int:
    n, m = len(nums), len(changeIndices)
    # 1‑indexed → 0‑indexed for Python
    change = [c - 1 for c in changeIndices]

    # 深度优先搜索所有可能的操作序列
    def dfs(t: int, cur_nums: List[int], marked: List[bool]) -> int:
        # t 为已经进行完的秒数（0 表示还没开始）
        if all(marked):
            return t                     # 全部标记完，返回当前秒数
        if t == m:                       # 已经用完所有秒数
            return float('inf')          # 表示失败

        idx = change[t]                  # 本秒可以改动的下标

        # 1. 试试看能否在本秒标记（前提是该位置已经是 0 且未标记）
        if cur_nums[idx] == 0 and not marked[idx]:
            new_marked = marked[:]
            new_marked[idx] = True
            ans = dfs(t + 1, cur_nums, new_marked)
            if ans != float('inf'):
                return ans

        # 2. 试试看改值（把 nums[idx] 减 1，前提是 >=0）
        if cur_nums[idx] > 0:            # 只能把正数减一
            new_nums = cur_nums[:]
            new_nums[idx] -= 1
            ans = dfs(t + 1, new_nums, marked)
            if ans != float('inf'):
                return ans

        # 3. 什么都不做（有时候两种操作都不可行，只能空等）
        return dfs(t + 1, cur_nums, marked)

    INF = float('inf')
    res = dfs(0, nums[:], [False] * n)
    return -1 if res == INF else res
```

> 这段代码仅用于说明思路，**在正式测试中会超时**。

#### 复杂度  

- 时间复杂度：`O(2^m)` —— 每秒都有两种选择，指数级增长。  
- 空间复杂度：`O(m + n)` —— 递归栈 + 两个数组的副本。  

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在于 **枚举所有决策**。  
观察题目可以发现：

1. **标记只能在 `nums[i] == 0` 时进行**。  
2. **改变的唯一意义是把一个正数尽快降到 0**，因为只有 0 才能被标记。  
3. 对同一个下标 `i`，如果我们在第 `t` 秒把它改为 0，那么在之后的某一秒（`> t`）一定要用来标记它。  
4. 因此 **每个下标最多只需要一次“改为 0” 的机会**，其余的“减一”操作只能是“浪费时间”，对整体完成时间没有帮助。

基于以上观察，可以把问题转化为：

> 在前 `x` 秒（`1 ≤ x ≤ m`）内，能否挑选若干个 **改为 0** 的时刻，使得  
> - 对每个被挑选的时刻 `i`，`changeIndices[i]` 对应的下标在 `i` 之后（`i < j ≤ x`）还有一次出现，以便标记它；  
> - 经过这些 “改为 0” 操作后，**总需要的时间** ≤ `x`。

---

#### 2.1 计算 “理论最小时间”  

如果我们 **不做任何改为 0 的操作**，只靠把数字逐步减一（每秒最多只能减 1），
完成所有标记需要的最少秒数是  

```
time_needed = sum(nums) + n
```

- `sum(nums)`：把所有正数降到 0 所需的减一次数。  
- `+ n`：每个下标从 0 到被标记，还需要额外的一秒（标记本身要占一秒）。

如果我们在第 `i` 秒把 `nums[p]` 直接改为 0（而不是逐步减），则可以 **省掉**  
`nums[p] - 1` 秒（因为本来需要 `nums[p]` 次减一才能到 0，再加一次标记；现在直接一次改为 0，再标记，只用了 1 秒）。  
换句话说，每一次合法的 “改为 0” 可以把 `time_needed` 减少 `gain = nums[p] - 1`。

所以 **目标**：在前 `x` 秒内挑选若干次 “改为 0”，使得  

```
time_needed - Σ(gain) ≤ x
```

即  

```
Σ(gain) ≥ time_needed - x
```

我们只需要让 **累计的 gain 最大**，然后检查是否满足上式。

---

#### 2.2 如何在前 `x` 秒内选取最大 gain  

从后往前遍历秒数 `x, x-1, …, 1`，维护一个 **最小堆**（优先队列）：

- 当遍历到第 `i` 秒时，`changeIndices[i]` 指向的下标记作 `p`。  
- 如果 `nums[p] == 0`，这秒根本不需要改为 0，直接跳过。  
- 否则，这秒 **有潜在的 gain = nums[p] - 1**。我们把它加入堆中，表示“这秒可以用来一次性把 `p` 变为 0”。  

但是 **每个下标只能被改为 0 一次**，且改为 0 的那秒必须 **在它的最后一次出现之前**，因为之后必须还有一次出现来标记它。  

从后往前遍历天然满足 “在改为 0 之后一定还有一次出现” 的要求：  
- 当我们把第 `i` 秒的候选加入堆后，**堆的大小**（即已经挑选的改为 0 次数）**不能超过** 已经遍历过的秒数中 **该下标出现的次数减 1**。  
- 更简洁的实现方式是：**每遍历到一次出现，就把堆顶（最小的 gain）弹出**，因为我们只能保留 **最多出现次数 - 1** 个改为 0 的机会。  

这样，遍历完前 `x` 秒后，堆中剩下的所有 `gain` 就是 **在满足标记顺序约束下能够取得的最大累计 gain**。  

最后检查：

```python
total_gain = sum(heap)          # 堆中所有元素的和
if total_gain >= time_needed - x:
    # 前 x 秒可以完成全部标记
```

如果条件成立，说明 `x` 是一个可行的答案；否则 `x` 不够。

---

#### 2.3 二分答案  

函数 `can(x)` 能在 `O(x log x)`（堆操作）时间判断第 `x` 秒是否可行。  
因为答案一定在区间 `[1, m]`（或不存在），我们可以 **二分搜索** 最小的可行 `x`：

1. 先检查 `can(m)` 是否成立，若不成立直接返回 `-1`。  
2. 否则在 `[1, m]` 之间二分，找到最左侧满足 `can(mid)` 的 `mid`。  

二分的迭代次数不超过 `log2(m) ≤ 13`（因为 `m ≤ 5000`），整体时间复杂度是 `O(m log m)`。

---

#### 2.4 完整代码（Python）  

```python
import heapq
from typing import List

def earliestSecond(nums: List[int], changeIndices: List[int]) -> int:
    """
    返回最早的秒数 x（1 ≤ x ≤ m）使得在前 x 秒内可以把所有下标标记，
    若不存在则返回 -1。
    """
    n = len(nums)
    m = len(changeIndices)
    # 统一转成 0‑indexed
    change = [c - 1 for c in changeIndices]

    # ----------- 辅助函数：判断前 x 秒是否可行 ------------
    def can(x: int) -> bool:
        """
        在前 x 秒（1..x）内，是否能把所有位置标记。
        采用逆序遍历 + 最小堆的贪心策略求最大 gain。
        """
        # time_needed 为不使用任何“一次性改为 0”时的最少秒数
        time_needed = sum(nums) + n
        # 需要的额外 gain
        need = time_needed - x
        if need <= 0:          # 已经不需要额外 gain，直接可行
            return True

        heap = []              # 最小堆，保存已选的 gain（实际上是负数以实现 max‑heap）
        total_gain = 0         # 当前堆中所有 gain 的和

        # 逆序遍历秒数 x … 1
        for i in range(x - 1, -1, -1):
            idx = change[i]            # 本秒要改的下标
            if nums[idx] == 0:
                # 本来就是 0，直接可以标记，无需加入堆
                continue

            # 这秒如果把 nums[idx] 直接改为 0，能够得到的 gain
            gain = nums[idx] - 1
            # 把 gain 加入堆（使用负数实现 max‑heap）
            heapq.heappush(heap, gain)
            total_gain += gain

            # 为了保证每个下标改为 0 之后还有一次出现来标记，
            # 我们必须在遍历到该下标的每一次出现时，弹出堆中最小的 gain
            #（即放弃收益最小的改为 0 机会）。
            # 这里的“每一次出现”正好对应我们在逆序遍历时
            # 每处理一次 `change[i]` 就弹出一次。
            # 但只能弹出一次：因为当前这次出现已经被用来“改为 0”，
            # 必须保留至少一次后续出现来标记它。
            # 因此我们在每次遍历时弹出堆顶（最小 gain），
            # 表示把收益最小的改为 0 机会舍弃。
            # 这一步等价于：只保留出现次数-1 个改为 0 的机会。
            if heap:
                # 弹出最小的 gain，实际上是放弃收益最小的改为 0
                smallest = heapq.heappop(heap)
                total_gain -= smallest

        # 逆序遍历结束后，heap 中剩下的 gain 即为在约束下能取得的最大累计 gain
        return total_gain >= need

    # ----------------- 主流程 -----------------
    # 若连使用全部 m 秒都不够，直接返回 -1
    if not can(m):
        return -1

    # 二分最小可行秒数
    lo, hi = 1, m
    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid          # 仍然可行，尝试更左侧
        else:
            lo = mid + 1      # 不可行，右移区间
    return lo
```

**代码说明（关键行注释）**

| 行号 | 作用 |
|------|------|
|`change = [c - 1 ...]`|把 1‑based 下标转成 Python 常用的 0‑based。|
|`time_needed = sum(nums) + n`|不使用一次性改为 0 时的最小所需秒数。|
|`need = time_needed - x`|在前 `x` 秒内必须额外获得的 “gain”。|
|`heap = []`|最小堆，用来保存已选的 `gain`（其实是最大化的），后面会弹出最小的来满足约束。|
|`gain = nums[idx] - 1`|如果这秒把该位置直接改为 0 能省下的秒数。|
|`heapq.heappush(heap, gain)`|把这次改为 0 的机会加入候选集合。|
|`if heap: smallest = heapq.heappop(heap)`|弹出收益最小的改为 0 机会，保证每个下标改为 0 后还有一次出现可以标记。|
|`return total_gain >= need`|检查累计的最大 gain 是否足够抵消 `need`。|
|二分循环|在 `[1, m]` 区间寻找最左侧满足 `can(mid)` 的秒数。|

---

#### 复杂度  

- **时间复杂度**  
  - `can(x)`：逆序遍历 `x` 次，每次堆操作 `O(log x)`，所以 `O(x log x)`。  
  - 二分搜索最多 `log₂ m` 次调用 `can`，整体 `O(m log m)`（因为 `x ≤ m`）。  
  - 对于本题的约束 `m ≤ 5000`，运行毫秒级。

- **空间复杂度**  
  - 堆中最多保存 `x` 个 `gain`，即 `O(m)`。  
  - 其余使用的数组是 `O(n)`（原始 `nums`）和常数级变量。  
  - 总体 `O(n + m)`，在本题 ≤ `10000`，非常轻量。

> **对比暴力**：  
> - 暴力 `O(2^m)` 难以接受；  
> - 最优解 `O(m log m)` 只与 `m` 成对数线性关系，能够轻松通过所有测试。

---

## 心得  

- **核心技巧**：把“把正数一次性改为 0”视为**收益**，并用**贪心 + 最小堆**在逆序遍历中选取收益最大的若干次，同时满足“改为 0 之后还要有一次出现来标记”的约束。  
- **适用题型**  
  1. “在有限时间窗口内挑选若干次操作，使得累计收益 ≥ 某阈值”——如 **Maximum Points You Can Obtain from Cards**（贪心+堆）  
  2. “需要在序列中保证每个元素的两次出现之间完成某件事”——如 **Earliest Second to Mark Indices I**（二分 + 前缀计数）  
  3. “通过一次性操作压缩多步耗时”——如 **Minimum Operations to Make Array Empty**（贪心 + 计数）  

- **一句话总结解题钥匙**：**把“一次性把数降到 0”当作可选的收益，用逆序贪心 + 最小堆挑出收益最大的合法集合，再二分验证最早可行时间。**

---

## 反思  

- **第一反应**：直接模拟所有可能的操作，结果很快发现时间爆炸。  
- **最容易踩的坑**  
  1. **忘记“改为 0”后必须还有一次出现来标记**，导致选取的收益集合不合法。  
  2. **计算 `time_needed` 时漏掉标记本身的 `+ n`**，会把答案提前。  
  3. **堆的弹出时机写错**（正向遍历 vs 逆向遍历），会产生错误的约束。  
- **下次类似题的第一步**：先把问题抽象为“在有限窗口内挑选若干次操作获取收益”，并思考是否可以用二分 + “能否在 x 秒内完成” 的判定函数来转化为单调性问题。这样就能快速跳出暴力搜索的陷阱。