# #2962. 计数最大元素出现至少 K 次的子数组 / Count Subarrays Where Max Element Appears at Least K Times

> 难度：中等 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and a positive integer k.
Return the number of subarrays where the maximum element of nums appears at least k times in that subarray.
A subarray is a contiguous sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,3,2,3,3], k = 2
Output: 6
Explanation: The subarrays that contain the element 3 at least 2 times are: [1,3,2,3], [1,3,2,3,3], [3,2,3], [3,2,3,3], [2,3,3] and [3,3].
```

**Example 2:**

```
Input: nums = [1,4,2,1], k = 3
Output: 0
Explanation: No subarray contains the element 4 at least 3 times.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106
- 1 <= k <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums` 和一个正整数 `k`。  
返回满足以下条件的子数组（subarray）数量：该子数组中的最大元素在子数组内出现的次数不少于 `k` 次。  
子数组是数组中连续（contiguous）的元素序列。

**示例**

**示例 1**  
Input: `nums = [1,3,2,3,3]`, `k = 2`  
Output: `6`  
Explanation: 出现元素 `3` 至少两次的子数组有：`[1,3,2,3]`、`[1,3,2,3,3]`、`[3,2,3]`、`[3,2,3,3]`、`[2,3,3]` 和 `[3,3]`。

**示例 2**  
Input: `nums = [1,4,2,1]`, `k = 3`  
Output: `0`  
Explanation: 没有子数组中出现元素 `4` 至少三次。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^6`  
- `1 <= k <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有子数组**，对每一个子数组求出它的最大值 `max`，再统计 `max` 在这个子数组里出现了多少次，判断是否 `≥ k`。  

- **枚举子数组**：使用两个循环，外层固定左端点 `l`，内层逐步向右扩展右端点 `r`。  
- **维护最大值及出现次数**：在把 `nums[r]` 加入当前子数组时，只需要比较 `nums[r]` 与当前的最大值 `cur_max`：  
  - 如果 `nums[r] > cur_max`，说明出现了一个更大的数，`cur_max` 需要更新为 `nums[r]`，同时把计数器 `cnt` 重新置为 `1`（因为新最大值刚出现一次）。  
  - 如果 `nums[r] == cur_max`，则把计数器 `cnt` 加 `1`。  
  - 否则 `cur_max` 与 `cnt` 都保持不变。  
- **判断**：每次扩展完 `r`，只要 `cnt ≥ k`，说明以 `l` 为左端点、`r` 为右端点的子数组满足条件，答案加一。

> **类比**：把数组想象成一本书的章节，左指针 `l` 代表从哪一页开始阅读，右指针 `r` 代表阅读到哪一页。我们每翻一页，就看看这段文字里出现次数最多的单词（即最大值）出现了几次，满足要求就记下来。

这种做法**一定是对的**，因为我们把所有可能的子数组都遍历了一遍，且对每个子数组都精确地判断了是否满足条件。

#### 代码（Python）

```python
def countSubarrays_bruteforce(nums, k):
    n = len(nums)
    ans = 0
    # 枚举左端点
    for l in range(n):
        cur_max = -1          # 当前子数组的最大值
        cnt = 0               # 最大值出现的次数
        # 逐步扩展右端点
        for r in range(l, n):
            if nums[r] > cur_max:          # 出现更大的数
                cur_max = nums[r]
                cnt = 1                    # 重新计数
            elif nums[r] == cur_max:       # 与当前最大值相等
                cnt += 1
            # else: nums[r] < cur_max，cnt 不变

            if cnt >= k:                   # 满足 “最大值出现至少 k 次”
                ans += 1
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。外层循环 `n` 次，内层平均也会遍历约 `n/2` 次，所以大约是 `n²/2`，在大 O 记号里写成 `O(n²)`。  
  - **直观解释**：如果把数组的每一个元素想象成一颗星星，暴力解会把所有可能的星星对（左端点、右端点）都检查一遍，星星对的数量随 `n` 的增大呈二次增长。  
- **空间复杂度**：`O(1)`。只用了常数个额外变量（`cur_max`、`cnt`、`ans`），不随输入规模增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每一次扩展右端点都要重新检查所有已加入的元素**，导致 `O(n²)`。  
要把时间降到 `O(n log n)`（甚至 `O(n)`），我们需要利用**“最大值出现的次数”只与等于该最大值的元素有关**的特点。  

关键观察：

1. **子数组的最大值一定是数组中的某个具体元素**（记作 `v`），且子数组里 **不允许出现比 `v` 更大的数**。  
2. 因此，对于每一种可能的最大值 `v`，我们只需统计 **在没有更大元素的区间（我们称之为 “块”）** 中，`v` 出现 **至少 `k` 次** 的子数组数量。  

> **类比**：把数组想象成一条河，河里有不同高度的岩石。我们想统计“最高的岩石出现不少于 `k` 次的河段”。如果把所有比某块岩石更高的岩石当成“堤坝”，那么每块堤坝之间的水面就是 **“没有更高岩石的块”**。在每块水面里，只关心该高度岩石出现多少次。

**步骤概览**  

| 步骤 | 说明 |
|------|------|
| 1️⃣ 收集位置 | 建立 `value → [下标列表]` 的映射，所有下标列表均已排序。 |
| 2️⃣ 按值降序遍历 | 从最大值到最小值依次处理。遍历时维护一个有序集合 `greater_pos`，保存 **已处理（即更大的）元素的下标**。这些下标相当于“堤坝”，把数组划分成若干块。 |
| 3️⃣ 统计当前值的贡献 | 对当前值 `v` 的所有下标 `pos_v`，利用 `greater_pos` 找到它们所在的块 `[L+1, R-1]`（`L` 为左侧最近的更大元素下标，`R` 为右侧最近的更大元素下标）。<br>在同一个块里，用**滑动窗口**统计 **“在该块内，`v` 至少出现 `k` 次的子数组数”**，公式为：<br>```\nfor i in range(len(block_pos) - k + 1):\n    left  = block_pos[i]   - (prev if i>0 else block_left-1)\n    right = (next if i+k < len(block_pos) else block_right+1) - block_pos[i+k-1]\n    ans += left * right\n```<br>这一步只遍历一次 `pos_v`，所以整体是线性的。 |
| 4️⃣ 更新堤坝 | 处理完 `v` 后，把 `v` 的所有下标加入 `greater_pos`（`insort`），为后面更小的值提供 “更大的元素”。 |

**为什么可以做到 `O(n log n)`**  

- 每个元素的下标只会被 **插入一次** 到有序集合 `greater_pos`，插入代价 `O(log n)`（二分）。  
- 对每个不同的值 `v`，我们只遍历一次它出现的位置列表 `pos_v`，并在同一块里做一次线性滑动窗口统计，**总计 O(n)** 次操作。  
- 所以总体时间为 `O(n log n)`（主要来自插入/二分），空间为 `O(n)`（存储位置列表和有序集合）。

#### 代码（Python）

```python
from bisect import bisect_left, insort
from collections import defaultdict

def countSubarrays(nums, k):
    n = len(nums)
    if k == 0:          # k 为正数，题目保证，但防御性写法
        return n * (n + 1) // 2

    # 1️⃣ 收集每个数值出现的下标（从左到右已排序）
    pos_of = defaultdict(list)
    for idx, val in enumerate(nums):
        pos_of[val].append(idx)

    # 2️⃣ 按值从大到小遍历
    unique_vals = sorted(pos_of.keys(), reverse=True)

    greater_pos = []            # 已处理（更大）的下标，始终保持有序
    ans = 0

    for v in unique_vals:
        positions = pos_of[v]   # 当前值 v 的所有下标（已排序）

        # 3️⃣ 统计 v 作为最大值且出现 ≥k 次的子数组数
        i = 0
        while i < len(positions):
            # 找到当前位置所在的块：左侧最近的更大元素 L，右侧最近的更大元素 R
            p = positions[i]
            idx = bisect_left(greater_pos, p)   # greater_pos[idx] 是第一个 > p 的位置
            L = greater_pos[idx - 1] if idx > 0 else -1
            R = greater_pos[idx]     if idx < len(greater_pos) else n

            # 收集同一块内的所有 v 的下标
            block = []
            while i < len(positions) and L < positions[i] < R:
                block.append(positions[i])
                i += 1

            # 若块内 v 的出现次数不足 k，直接跳过
            if len(block) < k:
                continue

            # 在该块里使用滑动窗口计数
            # block_left = L + 1, block_right = R - 1
            block_left = L + 1
            block_right = R - 1
            m = len(block)
            for start in range(m - k + 1):
                # 左边界可以取的位置数
                left_options = block[start] - (block[start - 1] if start > 0 else block_left - 1)
                # 右边界可以取的位置数
                end_idx = start + k - 1
                right_options = (block[end_idx + 1] if end_idx + 1 < m else block_right + 1) - block[end_idx]
                ans += left_options * right_options

        # 4️⃣ 把当前值的下标加入更大的集合，供后续更小的值使用
        for p in positions:
            insort(greater_pos, p)

    return ans
```

> **代码要点注释**  
> - `bisect_left` 用来在有序的 `greater_pos` 中快速定位左侧最近的更大元素 `L` 与右侧最近的更大元素 `R`（堤坝）。  
> - `insort` 把当前值的下标插入 `greater_pos`，保持有序，时间 `O(log n)`。  
> - 统计块内子数组的公式来源于“**第一个出现的 v** 在左边界左侧可以随意伸展，**第 k 个出现的 v** 在右边界右侧可以随意伸展”。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`。  
  - 插入每个下标到 `greater_pos`：`n` 次 `log n`。  
  - 对每个不同的数值，只遍历一次它出现的下标，累计 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，**当 `n` 达到 10⁵ 时，速度提升数百倍**。  
- **空间复杂度**：`O(n)`。  
  - `pos_of` 保存所有下标（共 `n` 个）。  
  - `greater_pos` 同样最多保存 `n` 个下标。  
  - 只使用了常数级的额外变量。

---

## 心得  

- **核心技巧**：把“最大值出现至少 k 次”转化为“在没有更大元素的块里，固定值出现至少 k 次”。利用 **有序集合（模拟堤坝） + 滑动窗口** 完成计数。  
- **适用场景**：  
  1. 需要统计 **子数组的最大/最小值满足某种出现次数** 的题目（如 “子数组的最小值出现恰好 k 次”）。  
  2. “在区间内，某个元素出现次数≥k” 并且 **区间被更大/更小元素划分** 的情形。  
- **解题钥匙**：**把全局的 “最大值” 约束拆解为局部的 “没有更大元素的连续块”，在每块里只关注该值本身**。

---

## 反思  

- **第一反应**：直接枚举子数组，想到维护最大值和计数——这就是暴力解。  
- **最容易踩的坑**：  
  - 忽视 **更大元素的干扰**：子数组的最大值不是随便一个数，而是受更大数的限制，需要划分块。  
  - 边界处理：块的左边界是 `L+1`（`L` 为左侧更大元素的下标），右边界是 `R-1`。如果不加 `+1/-1`，会导致计数多算或少算。  
  - 当 `k` 大于某块内 `v` 的出现次数时必须直接跳过，否则滑动窗口会出现负索引错误。  
- **下次思路**：看到 “子数组的最大/最小值 + 出现次数” 时，先 **思考“更大/更小元素把数组切成若干段”**，再在每段里只关注目标值的出现次数，使用 **滑动窗口或前缀计数** 进行 O(n) 统计。