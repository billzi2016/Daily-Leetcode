# #3048. 标记索引的最早秒数 I / Earliest Second to Mark Indices I

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/earliest-second-to-mark-indices-i/)

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
Input: nums = [2,2,0], changeIndices = [2,2,2,2,3,2,2,1]
Output: 8
Explanation: In this example, we have 8 seconds. The following operations can be performed to mark all indices:
Second 1: Choose index 1 and decrement nums[1] by one. nums becomes [1,2,0].
Second 2: Choose index 1 and decrement nums[1] by one. nums becomes [0,2,0].
Second 3: Choose index 2 and decrement nums[2] by one. nums becomes [0,1,0].
Second 4: Choose index 2 and decrement nums[2] by one. nums becomes [0,0,0].
Second 5: Mark the index changeIndices[5], which is marking index 3, since nums[3] is equal to 0.
Second 6: Mark the index changeIndices[6], which is marking index 2, since nums[2] is equal to 0.
Second 7: Do nothing.
Second 8: Mark the index changeIndices[8], which is marking index 1, since nums[1] is equal to 0.
Now all indices have been marked.
It can be shown that it is not possible to mark all indices earlier than the 8th second.
Hence, the answer is 8.
```

**Example 2:**

```
Input: nums = [1,3], changeIndices = [1,1,1,2,1,1,1]
Output: 6
Explanation: In this example, we have 7 seconds. The following operations can be performed to mark all indices:
Second 1: Choose index 2 and decrement nums[2] by one. nums becomes [1,2].
Second 2: Choose index 2 and decrement nums[2] by one. nums becomes [1,1].
Second 3: Choose index 2 and decrement nums[2] by one. nums becomes [1,0].
Second 4: Mark the index changeIndices[4], which is marking index 2, since nums[2] is equal to 0.
Second 5: Choose index 1 and decrement nums[1] by one. nums becomes [0,0].
Second 6: Mark the index changeIndices[6], which is marking index 1, since nums[1] is equal to 0.
Now all indices have been marked.
It can be shown that it is not possible to mark all indices earlier than the 6th second.
Hence, the answer is 6.
```

**Example 3:**

```
Input: nums = [0,1], changeIndices = [2,2,2]
Output: -1
Explanation: In this example, it is impossible to mark all indices because index 1 isn't in changeIndices.
Hence, the answer is -1.
```

**Constraints**

- 1 <= n == nums.length <= 2000
- 0 <= nums[i] <= 109
- 1 <= m == changeIndices.length <= 2000
- 1 <= changeIndices[i] <= n

---

## 题目（中文翻译）

给定两个下标从 **1** 开始的整数数组（integer array）`nums` 和 `changeIndices`，长度分别为 `n` 和 `m`。  
最初，`nums` 中的所有下标均未标记。你的任务是将 `nums` 中的所有下标全部标记。

在每一秒 `s`（从 **1** 到 **m**，含 `m`）内，你可以执行以下操作之一：

- 选择一个下标 `i`（`1 <= i <= n`），将 `nums[i]` 减一。如果 `nums[i]` 变为 **0**，则该下标被标记。

返回一个整数，表示在区间 **[1, m]** 内能够使所有下标都被标记的最早秒数；如果无法完成标记，则返回 **-1**。

## 示例

### 示例 1
**输入**  
`nums = [2,2,0]`  
`changeIndices = [2,2,2,2,3,2,2,1]`

**输出**  
`8`

**解释**  
本例共有 **8** 秒。可以按如下方式执行操作以标记全部下标：

- 第 1 秒：选择下标 `1`，`nums[1]` 减一，数组变为 `[1,2,0]`。  
- 第 2 秒：选择下标 `1`，`nums[1]` 再减一，数组变为 `[0,2,0]`（下标 1 被标记）。  
- 第 3 秒：选择下标 `2`，`nums[2]` 减一，数组变为 `[0,1,0]`。  
- 第 4 秒：选择下标 `2`，`nums[2]` 再减一，数组变为 `[0,0,0]`（下标 2 被标记）。  
- 第 5~8 秒：可以任选 `changeIndices` 中的其余下标进行操作，所有下标已全部标记。

因此最早的秒数为 **8**。  
（后续操作已截断）

### 示例 2
**输入**  
`nums = [1,3]`  
`changeIndices = [1,1,1,2,1,1,1]`

**输出**  
`6`

**解释**  
本例共有 **7** 秒。可以按如下方式执行操作以标记全部下标：

- 第 1 秒：选择下标 `2`，`nums[2]` 减一，数组变为 `[1,2]`。  
- 第 2 秒：选择下标 `2`，`nums[2]` 再减一，数组变为 `[1,1]`。  
- 第 3 秒：选择下标 `2`，`nums[2]` 再减一，数组变为 `[1,0]`（下标 2 被标记）。  
- 第 4 秒：选择下标 `1`，`nums[1]` 减一，数组变为 `[0,0]`（下标 1 被标记）。  
- 第 5~6 秒：可以任选 `changeIndices` 中的其余下标进行操作，所有下标已全部标记。

因此最早的秒数为 **6**。  
（后续操作已截断）

### 示例 3
**输入**  
`nums = [0,1]`  
`changeIndices = [2,2,2]`

**输出**  
`-1`

**解释**  
在本例中无法标记所有下标，因为下标 `1` 并未出现在 `changeIndices` 中。因此答案为 **-1**。

## 约束条件
- `1 <= n == nums.length <= 2000`
- `0 <= nums[i] <= 10^9`
- `1 <= m == changeIndices.length <= 2000`
- `1 <= changeIndices[i] <= n`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟每一秒到底能否把所有下标都标记完**。  
- 我们把 `nums` 看成一排盒子，每个盒子里有若干颗“糖”（`nums[i]` 表示第 `i` 个下标需要被减到 `0` 才算标记）。  
- `changeIndices` 就是一张“指令表”，第 `s` 秒我们可以选择把指令表里第 `s` 个下标对应的盒子减一颗糖（如果该盒子已经是 `0`，再减也没意义，只是浪费时间）。  

暴力做法就是：从第 `1` 秒到第 `m` 秒，**枚举**每一秒我们到底选哪个下标去减，尝试所有可能的选择，看有没有一种选择方式能在某个时刻把所有盒子都减到 `0`。  

这相当于在每一秒做一次**分支选择**，总共 `m` 秒，分支数是 `n`（每秒可以选任意下标），时间复杂度是 `O(n^m)`，根本不可行。  

不过，作为“暴力”解，我们可以 **把每秒都贪心地选** 那个当前糖最多的下标（或者随便选一个），只为说明**“只要有足够的指令次数，最终一定可以把所有盒子减到 0”**。  

实现上，只要遍历一次 `changeIndices`，把对应的 `nums` 减一，记录哪些下标已经变成 `0`。遍历结束后检查是否全部为 `0`，如果是则返回遍历的秒数，否则返回 `-1`。  

> 这其实是**不带优化的模拟**，只能在极小的输入下跑通，主要用于帮助我们验证思路的正确性。

#### 代码（Python）

```python
def earliestSecond_bruteforce(nums, changeIndices):
    # 把 nums 拷贝一份，防止修改原数组
    a = nums[:]
    n = len(a)

    # 标记每个下标是否已经被 “标记”（即值已经降到 0）
    marked = [False] * n

    for sec, idx in enumerate(changeIndices, start=1):   # sec 从 1 开始计数
        i = idx - 1                # 1-indexed → 0-indexed
        if a[i] > 0:               # 还有糖可以减
            a[i] -= 1
            if a[i] == 0:
                marked[i] = True   # 第 i 个下标被标记

        # 检查是否全部标记完
        if all(marked):
            return sec

    # 循环结束仍未全部标记
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(m)`。我们只遍历一次 `changeIndices`（最多 `2000` 次），每一步的操作是 `O(1)`。  
  - 大白话：如果 `m` 是 2000，最多只会算两千次，几乎是瞬间完成。  
- **空间复杂度**：`O(n)`。我们额外用了一个长度为 `n` 的布尔数组 `marked` 来记录是否已经标记。  

> 这已经比指数级的“枚举所有选择”好太多，但仍**不是最优**：它把每秒都随意选了一个下标，根本没有利用题目给出的“可以自由选择”这一点来尽可能提前完成标记。

---

### 2. 最优解  

#### 思路  

**核心难点**：我们可以在第 `s` 秒**自由决定**把哪一个下标减一。目标是**尽可能早**让所有下标的 `nums[i]` 都降到 `0`。  

观察提示：  
> “假设答案 ≤ x，则我们可以把每个下标尽可能 **晚** 地标记——在 `changeIndices[1..x]` 中出现的**最后一次**出现的位置标记它”。  

这句话的意思是：如果我们已经决定只用前 `x` 秒，那么**最宽容的做法**是把每个下标的标记时间推迟到它在前 `x` 秒里出现的**最靠后**的那一次。因为把标记推迟会给我们更多的“减糖”机会（即在之前的秒数里可以用来把该下标的值降到 `0`）。  

所以，**判定**“前 `x` 秒能否完成所有标记”可以这样做：

1. **统计** 前 `x` 秒里每个下标的**最后出现位置**（记作 `last[i]`），如果某个下标根本没有出现，则 `last[i] = -1`，说明在前 `x` 秒根本无法标记它，直接判定失败。  
2. 把这些出现位置按从小到大排序。设排序后的序列为 `pos_1 ≤ pos_2 ≤ … ≤ pos_k`（`k = n`，因为每个下标都必须出现）。  
3. 从左到右遍历这些位置，**模拟把糖减到 0 的过程**。  
   - 在第 `t` 个位置 `pos_t` 时，我们已经用掉了 `pos_t` 秒（因为要等到第 `pos_t` 秒才能真正标记该下标）。  
   - 之前已经标记好的 `t-1` 个下标，各自的 `nums` 已经被减到了 `0`，所以它们不再占用资源。  
   - 现在要标记第 `t` 个下标 `idx = changeIndices[pos_t]`，它的原始糖数是 `nums[idx]`。  
   - 在 `pos_t` 之前（即 `pos_t - 1` 秒），我们已经有 `pos_t - 1` 次“减糖”机会。**这些机会已经被前面已经标记的下标消耗**，每标记一次会消耗 `nums[idx]` 次减糖（因为要把它从原始值降到 0）。  
   - 更直观的判定式（提示里给出的）是：  

\[
\text{pos}_t - \underbrace{\sum_{j=1}^{t-1} \text{nums}[idx_j]}_{\text{已用掉的减糖次数}} - (t-1) \ge \text{nums}[idx_t]
\]

   - 左边是**剩余的减糖次数**（总秒数 `pos_t` 减去已经用掉的减糖次数和已经标记的次数），右边是当前下标需要的减糖次数。只要左边 ≥ 右边，就说明在 `pos_t` 秒之前我们有足够的“空闲”减糖操作把当前下标降到 0。  

4. 如果所有 `t = 1..n` 都满足上述不等式，则说明 **前 `x` 秒足够**；否则不够。  

由于 `x` 的取值范围是 `[1, m]`，我们可以**二分搜索**最小的可行 `x`。二分的每一步都执行上述检查，时间复杂度是 `O(n log m)`（`n ≤ 2000, m ≤ 2000`，完全可以接受）。

**关键数据结构**：

- `last` 数组（长度 `n+1`），存每个下标在前 `mid` 秒的最后出现位置。  
- `pairs` 列表，保存 `(lastPos, idx)`，随后按 `lastPos` 排序。  

**类比**：想象我们在排队买票，每个人只能在自己的**最后一次出现**那一刻买票。我们想知道排队的总时长是否足够让所有人买完票。排队的每一秒都是一次“减糖”机会，已经买票的人会占用一秒，而每个人还需要额外的“糖”秒数（`nums[i]`），二者之和不能超过当前排队的长度。

#### 代码（Python）

```python
from typing import List
import bisect

def earliestSecond(nums: List[int], changeIndices: List[int]) -> int:
    n = len(nums)                     # 下标个数
    m = len(changeIndices)            # 秒数上限

    # ---------- 判定函数 ----------
    def can_finish(limit: int) -> bool:
        """
        判断只使用前 limit 秒（即 changeIndices[:limit]）是否能把所有下标标记完。
        """
        # 1. 统计每个下标在前 limit 秒的最后出现位置（1-indexed）
        last = [-1] * (n + 1)         # 使用 1-index，0 位置不使用
        for sec in range(limit):
            idx = changeIndices[sec]   # 已经是 1-index
            last[idx] = sec + 1        # 保存出现的秒数（1-index）

        # 2. 若有下标根本没有出现，直接返回 False
        for i in range(1, n + 1):
            if last[i] == -1:
                return False

        # 3. 把 (最后出现位置, 下标) 收集起来并按位置升序排列
        pairs = [(last[i], i) for i in range(1, n + 1)]
        pairs.sort()                  # 按 last[i] 从小到大

        # 4. 逐个检查是否有足够的“减糖”次数
        used_decrements = 0           # 已经消耗的 nums 值之和
        marked_cnt = 0                # 已经标记的下标数量

        for pos, idx in pairs:        # pos 为该下标的最后出现秒数（1-index）
            # 剩余的减糖次数 = 已经过去的秒数 - 已经用掉的减糖次数 - 已标记的次数
            remaining = pos - used_decrements - marked_cnt
            need = nums[idx - 1]       # nums 是 0-index，需要转换

            if remaining < need:       # 不够减到 0，失败
                return False

            # 成功标记当前下标，更新统计量
            used_decrements += need
            marked_cnt += 1

        # 所有下标都检查通过
        return True

    # ---------- 二分搜索最小可行的秒数 ----------
    lo, hi = 1, m
    ans = -1
    while lo <= hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            ans = mid          # 记录一个可行解，继续往左找更小的
            hi = mid - 1
        else:
            lo = mid + 1

    return ans
```

> **代码要点注释**  
> 1. `last[idx] = sec + 1` 用 1-index 保存出现的秒数，方便后面的不等式直接使用。  
> 2. `remaining = pos - used_decrements - marked_cnt` 正是提示中给出的公式的左边。  
> 3. `need = nums[idx - 1]` 因为 `nums` 本身是 0-index，题目下标是 1-index，需要转换。  
> 4. 二分搜索的范围是 `[1, m]`，若整个 `can_finish(m)` 仍然返回 `False`，答案保持 `-1`。

#### 复杂度  

- **时间复杂度**：`O((n + m) log m)`  
  - 每次二分检查 `can_finish` 需要遍历至多 `limit ≤ m` 次来填充 `last`（`O(m)`），随后对 `n` 个下标排序（`O(n log n)`）并线性扫描。因为 `n, m ≤ 2000`，`log m ≤ 11`，整体非常快。  
  - 与暴力 `O(m)` 的单次遍历相比，多了一个 `log m` 的因子，但换来了**最小可行秒数**的精确求解。  

- **空间复杂度**：`O(n + m)`  
  - `last` 长度 `n+1`，`pairs` 长度 `n`，以及遍历 `changeIndices` 时的临时变量。均为线性空间。  

> 相比暴力只判断 **能否在全部 `m` 秒完成**，二分+检查能够找出**最早**的秒数，且在最坏情况下仍然只需要几千次操作，轻松满足题目限制。

---

## 心得  

- **核心技巧**：**二分搜索 + “最晚标记” 贪心检查**。  
- 该技巧适用于 **“在前缀序列中是否满足某种资源约束”** 的题目，例如  
  1. *Maximum Number of Darts Inside a Circular Dartboard*（二分 + 前缀可行性）  
  2. *Maximum Number of Removable Edges to Keep Graph Fully Traversable*（二分 + 前缀可行性）  
  3. *Find Minimum Time to Complete All Jobs*（二分 + 任务调度检查）  

- **一句话总结解题钥匙**：  
  > “把每个下标的标记时间推迟到它在前缀里出现的最靠后位置，用二分确定最小前缀，使得剩余的秒数足以把所有下标的值降为 0”。  

---

## 反思  

- **第一反应**：直接模拟每秒的操作，想把所有下标都尽快减到 0。  
- **最容易踩的坑**：  
  1. 忽视 **“可以自由选择下标”** 的自由度，导致把每秒都固定在某个下标上，浪费了大量潜在的减糖机会。  
  2. 没有考虑 **“最晚标记”** 的贪心思想，导致检查时无法得到最宽容的资源利用情况。  
  3. 边界条件：某个下标根本不在 `changeIndices` 中出现，需要立刻返回 `-1`。  
- **下次类似题**的第一步：**先思考“在给定前缀内是否可能完成”，并尝试把约束放宽（最晚/最早）来得到一个单调性，然后用二分搜索定位最小满足的前缀**。