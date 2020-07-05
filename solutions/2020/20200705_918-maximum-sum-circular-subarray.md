# #918. **环形子数组的最大和** / Maximum Sum Circular Subarray

> 难度：中等 · 标签：Array、Divide and Conquer、Dynamic Programming、Queue、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-circular-subarray/)

---

## 题目（英文原版）

**Description**

Given a circular integer array nums of length n, return the maximum possible sum of a non-empty subarray of nums.
A circular array means the end of the array connects to the beginning of the array. Formally, the next element of nums[i] is nums[(i + 1) % n] and the previous element of nums[i] is nums[(i - 1 + n) % n].
A subarray may only include each element of the fixed buffer nums at most once. Formally, for a subarray nums[i], nums[i + 1], ..., nums[j], there does not exist i <= k1, k2 <= j with k1 % n == k2 % n.

**Examples**

**Example 1:**

```
Input: nums = [1,-2,3,-2]
Output: 3
Explanation: Subarray [3] has maximum sum 3.
```

**Example 2:**

```
Input: nums = [5,-3,5]
Output: 10
Explanation: Subarray [5,5] has maximum sum 5 + 5 = 10.
```

**Example 3:**

```
Input: nums = [-3,-2,-3]
Output: -2
Explanation: Subarray [-2] has maximum sum -2.
```

**Constraints**

- n == nums.length
- 1 <= n <= 3 * 104
- -3 * 104 <= nums[i] <= 3 * 104

---

## 题目（中文翻译）

给定一个长度为 `n` 的环形整数数组 `nums`，返回 `nums` 中非空子数组（subarray）可能得到的最大和。

环形数组（circular array）指数组的末尾与开头相连。形式上，`nums[i]` 的下一个元素是 `nums[(i + 1) % n]`，前一个元素是 `nums[(i - 1 + n) % n]`。

子数组（subarray）在取值时，每个元素在固定缓冲区（fixed buffer）`nums` 中至多出现一次。形式上，对于子数组 `nums[i], nums[i + 1], ..., nums[j]`，不存在满足 `i ≤ k1, k2 ≤ j` 且 `k1 % n == k2 % n` 的 `k1` 与 `k2`。

---

### 示例

**示例 1**  
输入: `nums = [1,-2,3,-2]`  
输出: `3`  
解释: 子数组 `[3]` 的和最大，为 `3`。

**示例 2**  
输入: `nums = [5,-3,5]`  
输出: `10`  
解释: 子数组 `[5,5]` 的和为 `5 + 5 = 10`，为最大和。

**示例 3**  
输入: `nums = [-3,-2,-3]`  
输出: `-2`  
解释: 子数组 `[-2]` 的和最大，为 `-2`。

---

### 约束条件

- `n == nums.length`
- `1 <= n <= 3 * 10^4`
- `-3 * 10^4 <= nums[i] <= 3 * 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有可能的子数组** 都枚举一遍，求它们的和，然后取最大值。  
因为数组是环形的，子数组可以跨过数组的结尾回到开头。一个常用的“生活化”类比是：

> 想象把这条环形跑道的数字贴在一条无限长的纸带上，先把纸带复制两遍（`nums + nums`），这样环形就变成了一条直线。  
> 只要我们保证子数组的长度不超过原始数组的长度 `n`，就不会出现同一个元素被使用两次的情况。

实现细节：  
1. 先把数组复制一遍得到 `extended = nums + nums`。  
2. 对每个起始位置 `i`（0 ≤ i < n），枚举结束位置 `j`（i ≤ j < i + n），计算 `extended[i:j+1]` 的和。  
3. 记录出现的最大和即为答案。  

为什么正确？  
- 我们遍历了所有起点 `i`，以及所有合法的终点 `j`（长度 ≤ n），正好覆盖了 **环形数组** 中的每一种连续子序列。  
- 只要取最大和，就一定是题目要求的“非空子数组的最大可能和”。  

时间/空间复杂度的大白话：  
- 时间复杂度是 **O(n²)**，意思是如果数组长度是 1000，程序大概要跑 1000 × 1000 = 1 000 000 次基本操作；如果长度是 10 000，操作次数会增长到 100 000 000，明显会慢。  
- 空间复杂度是 **O(n)**，因为我们多开辟了一段长度为 2n 的数组来存放复制后的内容，相当于原数组的两倍大小。

#### 代码（Python）  

```python
def maxSubarraySumCircular_bruteforce(nums):
    """
    暴力枚举所有合法的环形子数组，返回最大子数组和。
    时间复杂度 O(n^2)，空间复杂度 O(n)。
    """
    n = len(nums)
    # 复制一次，使环形变成直线，后面取子数组时只要不超过 n 长度即可
    extended = nums + nums          # 例如 [1,-2,3,-2] -> [1,-2,3,-2,1,-2,3,-2]

    max_sum = -10**9                # 题目保证至少有一个元素，先放一个很小的初始值
    # 枚举所有可能的起点（只能在前 n 个位置起，因为后面的都是复制来的）
    for i in range(n):
        cur_sum = 0
        # 终点 j 不能超过 i + n - 1，保证子数组长度 ≤ n
        for j in range(i, i + n):
            cur_sum += extended[j]   # 累加当前元素，等价于求子数组的和
            if cur_sum > max_sum:    # 更新全局最大值
                max_sum = cur_sum
    return max_sum
```

#### 复杂度  

- **时间复杂度：O(n²)** —— 两层循环，外层 `n` 次，内层最坏也要遍历 `n` 次。  
- **空间复杂度：O(n)** —— 需要额外的 `2n` 长度的数组 `extended`，相当于原数组的常数倍空间。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**真正的瓶颈** 是我们对每个起点都重新累计求和，导致了二次遍历。  
要想快，就要**在一次遍历中同时得到子数组的最大和**。这正是 **Kadane 算法**（也叫最大子段和算法）能做到的——它只用一次线性扫描，就能找出普通（非环形）数组的最大子段和。

环形数组的最大子段和其实有两种可能：

1. **不跨越数组结尾**（普通情况）  
   这时答案就是普通数组的最大子段和，直接用 Kadane 就能得到。  

2. **跨越数组结尾**（即子段在数组末尾和开头都有元素）  
   想象把环形数组的“跨越子段”看成**去掉了一个最小子段**后剩下的部分。  
   - 设 `total` 为整个数组的元素和。  
   - 若我们把一个 **最小子段**（同样是连续的、长度 ≤ n）从 `total` 中减去，剩下的就是跨越的子段的和。  
   - 因此，跨越情况的最大和 = `total - (最小子段和)`。  
   - 求最小子段和同样可以用 Kadane 的思路，只是把 “最大” 换成 “最小”。  

**特殊情况**：如果所有元素都是负数，`total - min_subarray` 会得到 0（因为最小子段会是整个数组），这不是合法答案。此时我们只能选普通 Kadane 的结果，即最大的负数。  

**步骤概览**（一次遍历搞定）  
- 用 Kadane 正向遍历得到 `max_kadane`（普通最大子段和）。  
- 用 Kadane 反向（或在同一次遍历中记录最小子段）得到 `min_kadane`（普通最小子段和）。  
- 计算数组总和 `total`。  
- 若 `max_kadane` 为负（即全负），直接返回 `max_kadane`。  
- 否则答案 = `max(max_kadane, total - min_kadane)`。  

下面把 Kadane 的核心思想先解释一下，帮助零基础的同学理解：

- **Kadane 思想**：在遍历数组时，维护一个 “以当前元素结尾的最大子段和” `cur_max`。  
  - 若 `cur_max` 加上当前元素仍然比单独当前元素大，就说明把前面的子段继续保留更好；否则就从当前元素重新开始。  
  - 同时全局维护一个 `best`，记录遍历过程中出现的最大 `cur_max`。  
  - 只用 O(1) 额外空间，就能一次遍历得到答案。  

**类比**：把每个元素看成“一天的收益”。`cur_max` 就是“截至今天为止，连续赚钱的最佳方案”。如果今天的收益是负的，继续往下算会让总收益下降，那我们就“重新开张”，从今天重新算起。  

#### 代码（Python）  

```python
def maxSubarraySumCircular(nums):
    """
    使用 Kadane 算法一次遍历求解环形子数组最大和。
    时间复杂度 O(n)，空间复杂度 O(1)。
    """
    total = 0               # 整个数组的总和
    max_cur = min_cur = 0   # 分别记录以当前元素结尾的最大/最小子段和
    max_kadane = -10**9      # 全局最大子段和（普通情况）
    min_kadane = 10**9       # 全局最小子段和（用于跨越情况）

    for x in nums:
        total += x

        # ---- Kadane 求最大子段和 ----
        # 若 max_cur + x 更大，就把 x 加进去；否则重新从 x 开始
        max_cur = max(x, max_cur + x)
        max_kadane = max(max_kadane, max_cur)

        # ---- Kadane 求最小子段和 ----
        # 与上面相反，想让和尽可能小，就取 min(x, min_cur + x)
        min_cur = min(x, min_cur + x)
        min_kadane = min(min_kadane, min_cur)

    # 如果全部为负数，max_kadane 已经是最大元素，直接返回
    if max_kadane < 0:
        return max_kadane

    # 跨越结尾的情况 = 总和 - 最小子段和
    max_wrap = total - min_kadane

    # 两种情况取较大者
    return max(max_kadane, max_wrap)
```

#### 复杂度  

- **时间复杂度：O(n)** —— 只遍历一次数组，n 为数组长度。  
  与暴力解的 O(n²) 相比，速度提升了一个数量级，1000 → 1 000 000 次运算变成 1 000 次，几乎是瞬间完成。  
- **空间复杂度：O(1)** —— 只用了常数个额外变量（`total、max_cur、min_cur…`），不随 `n` 增长。  

---

## 心得  

- **核心技巧**：把环形数组的“跨越子段”转化为 “总和 - 最小子段”，再配合 Kadane 求最大/最小子段和。  
- **适用的题型**  
  1. “最大子数组和”系列（如 LeetCode 53）。  
  2. “环形数组最大子数组和”系列（本题）。  
  3. “最小子数组和”或 “最大环形子数组乘积”等需要把数组拆成两段的变形题。  
- **一句话总结解题钥匙**：**先用 Kadane 求普通最大子段，若想跨越环形再用 “总和‑最小子段” 组合，二者取大即可。**  

---

## 反思  

- **第一反应**：看到“环形”二字，第一时间想到把数组拼接两遍，再套用普通的最大子段算法。  
- **最容易踩的坑**  
  - **全负数**：`total - min_subarray` 会得到 0，实际上不合法，需要单独处理。  
  - **最小子段恰好是整个数组**：此时跨越情况等价于空子数组，需要排除。  
  - **边界条件**：数组长度为 1 时，直接返回唯一元素。  
- **下次遇到同类题**：第一步先思考“是否可以把环形/循环结构线性化”，随后检查“是否可以用总和减去某个子结构”来得到另一种情况，再决定是否需要 Kadane（或前缀和）来线性求解。