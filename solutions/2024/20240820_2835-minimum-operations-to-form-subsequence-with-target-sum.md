# #2835. 最少操作次数以形成目标和的子序列 / Minimum Operations to Form Subsequence With Target Sum

> 难度：困难 · 标签：Array、Greedy、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-form-subsequence-with-target-sum/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisting of non-negative powers of 2, and an integer target.
In one operation, you must apply the following changes to the array:
Return the minimum number of operations you need to perform so that nums contains a subsequence whose elements sum to target. If it is impossible to obtain such a subsequence, return -1.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [1,2,8], target = 7
Output: 1
Explanation: In the first operation, we choose element nums[2]. The array becomes equal to nums = [1,2,4,4].
At this stage, nums contains the subsequence [1,2,4] which sums up to 7.
It can be shown that there is no shorter sequence of operations that results in a subsequnce that sums up to 7.
```

**Example 2:**

```
Input: nums = [1,32,1,2], target = 12
Output: 2
Explanation: In the first operation, we choose element nums[1]. The array becomes equal to nums = [1,1,2,16,16].
In the second operation, we choose element nums[3]. The array becomes equal to nums = [1,1,2,16,8,8]
At this stage, nums contains the subsequence [1,1,2,8] which sums up to 12.
It can be shown that there is no shorter sequence of operations that results in a subsequence that sums up to 12.
```

**Example 3:**

```
Input: nums = [1,32,1], target = 35
Output: -1
Explanation: It can be shown that no sequence of operations results in a subsequence that sums up to 35.
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 230
- nums consists only of non-negative powers of two.
- 1 <= target < 231

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的数组 `nums`，其中每个元素都是非负的 2 的幂，以及一个整数 `target`。  

一次操作定义如下：选择数组中的任意一个元素 `nums[i]`（该元素一定是 2 的幂），将其替换为两个相等的元素 `nums[i] / 2`（即把它拆分成两个相同的数）。  

返回使得 `nums` 中存在一个子序列（subsequence）其元素之和等于 `target` 所需的最少操作次数。如果无法得到这样的子序列，返回 `-1`。  

子序列是指可以通过删除若干（也可以不删除）元素而不改变其余元素相对顺序得到的数组。

---

**示例**

**示例 1**  
```
Input: nums = [1,2,8], target = 7
Output: 1
Explanation: 第一次操作选择下标为 2 的元素 8，将其拆分为两个 4，数组变为 [1,2,4,4]。此时数组中存在子序列 [1,2,4]，其和为 7。可以证明不存在更少操作次数能够得到和为 7 的子序列。
```

**示例 2**  
```
Input: nums = [1,32,1,2], target = 12
Output: 2
Explanation: 第一次操作选择下标为 1 的元素 32，拆分后得到 [1,1,2,16,16]。第二次操作选择下标为 3（原始的 2）对应的元素 16，拆分后得到 [1,1,2,16,8,8]。此时数组中存在子序列 [1,1,2,8]，其和为 12。可以证明不存在更少的操作次数能够得到和为 12 的子序列。
```

**示例 3**  
```
Input: nums = [1,32,1], target = 35
Output: -1
Explanation: 可以证明无论进行多少次操作，都无法得到和为 35 的子序列。
```

---

**约束条件**  

- `1 <= nums.length <= 1000`  
- `1 <= nums[i] <= 2^30`  
- `nums` 中的每个元素都是非负的 2 的幂。  
- `1 <= target < 2^31`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的操作序列**，把每一次“把一个 2ⁿ 拆成两个 2ⁿ⁻¹”都记下来，随后检查拆完之后的数组里有没有一个子序列（不要求连续）恰好等于 `target`。  

- **数据结构**：我们可以把数组 `nums` 当成一本“字典”，键（key）是数值本身，值（value）是该数值出现的次数。比如 `[1,2,8]` → `{1:1, 2:1, 8:1}`，就像查字典时先找词（数值），再看它在第几页（出现次数）。  
- **为什么正确**：只要穷举了**所有**可能的拆分方式，就一定能找到一种能够拼出 `target` 的子序列（如果存在的话）。  
- **缺点**：数组长度最多 1000，数值最高到 2³⁰，拆分的次数可能非常多，枚举所有拆分方案会产生指数级的组合，根本不可算。  

**时间复杂度**  
- 假设我们把每个元素都可以拆到 `1`，最多会产生 `30 * n` 次拆分。暴力枚举每一种拆分的组合相当于在 `30n` 步里挑选子集，组合数是 `C(30n, k)`，这在最坏情况下相当于 `O(2^{30n})`，也就是 **指数级**（`2^{30n}` 远远大于我们能接受的计算量）。  
- **空间复杂度**：需要保存每一次拆分后的整条数组，最坏情况也会是指数级。  

显然，这种“最笨”办法根本不可行，只能作为思考的起点，帮助我们发现 **瓶颈**——不需要真的去枚举所有拆分，只要知道每个二进制位需要多少个 2ⁱ 就行。

---

#### 代码（Python）  

```python
from itertools import combinations
from copy import deepcopy

def brute_min_operations(nums, target):
    """
    暴力尝试所有拆分组合（仅作概念演示，实际会超时）。
    """
    # 先检查总和是否足够
    if sum(nums) < target:
        return -1

    # 记录所有可能的拆分序列（这里用递归暴力生成，仅用于说明思路）
    # 为了演示，这里只拆一次：把每个元素拆成两个更小的
    # 实际上需要无限次拆分，复杂度不可接受
    def split_once(arr):
        res = []
        for i, v in enumerate(arr):
            if v > 1:                     # 只对 2 的幂进行拆分
                new_arr = arr[:i] + [v // 2, v // 2] + arr[i+1:]
                res.append(new_arr)
        return res

    # BFS 暴力搜索（示意）
    from collections import deque
    q = deque()
    q.append((nums, 0))          # (当前数组, 已经用了多少次操作)

    seen = set()
    while q:
        cur, steps = q.popleft()
        # 检查是否存在子序列和为 target
        # 这里用暴力子集检验（不考虑顺序）
        for r in range(len(cur)+1):
            for comb in combinations(cur, r):
                if sum(comb) == target:
                    return steps

        # 继续拆分
        for nxt in split_once(cur):
            tup = tuple(sorted(nxt))
            if tup not in seen:
                seen.add(tup)
                q.append((nxt, steps+1))
    return -1
```

> **注意**：上述代码仅用于展示“暴力思路”。实际运行会因为组合爆炸而在极短时间内卡死，**不要在正式提交中使用**。

#### 复杂度  

- **时间复杂度**：`O(2^{30n})`（指数级），因为我们尝试了所有可能的拆分组合。  
- **空间复杂度**：`O(2^{30n})`，需要保存每一种状态的数组。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正关心的不是具体的拆分顺序，而是每一种 2 的幂出现了多少次**。  
这让我们想到 **位计数**（bit‑count）和 **贪心** 的结合：

1. **把所有数按二进制位计数**  
   - 统计数组里每个 `2^k` 出现了多少次，记作 `cnt[k]`。  
   - 想象这些 `cnt[k]` 是“仓库”里不同面值的硬币。

2. **从低位到高位检查目标的每一位**  
   - `target` 的第 `k` 位（`2^k`）如果是 `1`，说明我们**必须**凑出一个 `2^k`。  
   - 首先看看 `cnt[k]` 是否已经 ≥ 1，若够，就直接用掉一枚（相当于把它放进子序列），`cnt[k]--`。

3. **不足时向高位“借”**  
   - 如果 `cnt[k] == 0`，我们需要把更大的硬币 **拆** 成 `2^k`。  
   - 找到最近的更高位 `j > k`，使得 `cnt[j] > 0`（即还有未使用的 `2^j`），把它拆成两个 `2^{j-1}`，这算作一次操作。  
   - 拆完后 `cnt[j]--`，`cnt[j-1] += 2`。  
   - 继续检查 `cnt[k]`，如果仍不足，就继续向更高位拆，直到得到足够的 `2^k` 为止。  
   - 每一次拆分都计数一次操作。

4. **把多余的低位硬币向上“合并”**  
   - 在处理完第 `k` 位后，剩余的 `cnt[k]`（可能是 0、1、2…）可以两两合并成 `cnt[k+1] += cnt[k] // 2`（因为两个 `2^k` 可以组成一个 `2^{k+1}`），这一步不需要操作次数，只是为了后面位的计数更准确。

5. **遍历完所有位**  
   - 如果在遍历过程中找不到可以拆的更高位（即所有更高位的 `cnt` 都为 0），说明 **总和不足**，返回 `-1`。  
   - 否则累计的拆分次数即为最小操作数。

**为什么是最优的？**  

- 每一次拆分都是 **必要的**：如果当前位缺少 `2^k`，唯一办法只能把更大的数拆下来，拆一次就得到两个更小的数，无法用更少的操作完成同样的目标。  
- 由于我们始终从 **最低位** 开始满足需求，后面的高位只会在必要时才被拆，**不会产生多余的拆分**。  
- 合并低位硬币是“免费”的，因为两个相同的数本来就可以在后面的位直接使用，不影响操作次数。

**类比**：想象你在玩“找零钱”的游戏，手里有不同面值的硬币（1、2、4、8 …），目标是付出恰好 `target` 元。  
- 当缺少某个面值的硬币时，你只能把更大面值的硬币“撕开”成两张小的，这一次撕开算作一次操作。  
- 只要把零钱凑齐，就不需要再撕开别的硬币。  

#### 代码（Python）  

```python
from typing import List

def minOperations(nums: List[int], target: int) -> int:
    """
    贪心 + 位计数
    cnt[i] 表示当前数组中 2^i 的数量（未被选进子序列的部分）
    """
    MAX_BIT = 31                     # 因为 nums[i]、target < 2^31
    cnt = [0] * MAX_BIT

    # 1️⃣ 统计每个 2^i 的出现次数
    for v in nums:
        bit = v.bit_length() - 1     # 2^k -> k
        cnt[bit] += 1

    ops = 0                          # 记录总的拆分次数

    # 2️⃣ 从低位到高位检查 target 的每一位
    for i in range(MAX_BIT):
        # 第 i 位在 target 中是否需要 1 ?
        need = (target >> i) & 1

        # 先把当前位的多余硬币向上合并（两两变成更大的硬币）
        # 这一步不影响 ops，因为合并是“免费”的
        if i < MAX_BIT - 1:
            cnt[i + 1] += cnt[i] // 2

        # 如果本位不需要 1，直接进入下一位
        if need == 0:
            continue

        # 本位需要一个 2^i，但 cnt[i] 可能为 0
        if cnt[i] > 0:               # 有现成的，直接使用
            cnt[i] -= 1
            continue

        # 需要向更高位借，用拆分的方式得到 2^i
        j = i + 1
        while j < MAX_BIT and cnt[j] == 0:
            j += 1

        # 没有更高位的硬币可以拆，说明总和不足
        if j == MAX_BIT:
            return -1

        # 把第 j 位的硬币一直拆到第 i 位
        while j > i:
            # 拆一次：2^j -> 2^{j-1} + 2^{j-1}
            cnt[j] -= 1               # 用掉一个 2^j
            cnt[j - 1] += 2           # 得到两个 2^{j-1}
            ops += 1                  # 计一次操作
            j -= 1

        # 现在第 i 位一定有至少一个 2^i，可以直接使用
        cnt[i] -= 1
    return ops
```

**代码要点解释**  

| 行号 | 关键代码 | 中文注释 |
|------|----------|----------|
| 7‑9 | `bit = v.bit_length() - 1` | 把 `2^k` 的数值转成对应的位数 `k`（相当于查字典的“词条”） |
| 15‑18 | `if i < MAX_BIT - 1: cnt[i + 1] += cnt[i] // 2` | 把同一位的硬币两两“合并”成更高位，类似把两枚 2ⁱ 变成一枚 2ⁱ⁺¹，**不计操作** |
| 22‑23 | `if cnt[i] > 0: cnt[i] -= 1; continue` | 本位已经有可用的硬币，直接取走一枚 |
| 28‑30 | `while j < MAX_BIT and cnt[j] == 0: j += 1` | 向更高位寻找可以拆的硬币 |
| 38‑41 | `cnt[j] -= 1; cnt[j-1] += 2; ops += 1` | 把一个 `2^j` 拆成两个 `2^{j-1}`，计一次操作 |
| 46 | `cnt[i] -= 1` | 拆完后，用掉刚得到的 `2^i` |

#### 复杂度  

- **时间复杂度**：  
  - 统计次数 `O(n)`（遍历一次 `nums`）。  
  - 主循环最多遍历 31 位，每一位在最坏情况下会向更高位搜索一次，搜索距离最多 31 步。整体是 `O(31 * 31) = O(1)`（常数），因此总体 **O(n)**。  
  - 大白话：只看数组大小，时间随 `nums` 长度线性增长，几千个元素也能在毫秒级完成。

- **空间复杂度**：  
  - 只用了长度为 31 的数组 `cnt`，以及几个整数变量，**O(1)**（常数空间）。  

与暴力解相比，**时间从指数级降到线性**，**空间从指数级降到常数**，差距天壤之别。

---

## 心得  

- **核心技巧**：把“每个数是 2 的幂”这个限制转化为**位计数 + 贪心拆分**。  
- **适用题型**：  
  1. **“硬币找零”** 类问题（如把若干 2 的幂凑成指定和）。  
  2. **“把大数拆成小数”** 的贪心题（如 LeetCode 1800 系列的 “Maximum Subset … with Powers of Two”）。  
  3. **位运算结合计数** 的题目（如 “Minimum Number of Operations to Make Array XOR Zero”）。  
- **一句话总结解题钥匙**：**从低位到高位，用最少的拆分把更大的 2 的幂“分解”为目标位需要的硬币**。

---

## 反思  

- **第一反应**：看到“只能把 2ⁿ 拆成两个 2ⁿ⁻¹”，立刻想到二进制位和“拆硬币”。  
- **最容易踩的坑**：  
  - 忘记 **合并低位硬币**（`cnt[i] // 2`），导致后面高位找不到可用的硬币，误判为 `-1`。  
  - 没有提前检查 **总和是否足够**，在没有可拆硬币时盲目循环导致无限循环。  
  - 处理 **最高位** 时数组越界，需要把位数设为 31（因为 `2^30` 已经是上限）。  
- **下次遇到同类题**：第一步先 **统计每个 2 的幂出现次数**，再 **从最低位开始逐位满足需求**，缺少就 **向更高位拆**，多余就 **向上合并**。这样思路一上来就清晰，代码自然简洁。