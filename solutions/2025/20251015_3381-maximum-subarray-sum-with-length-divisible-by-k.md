# #3381. 长度能被 K 整除的最大子数组和 / Maximum Subarray Sum With Length Divisible by K

> 难度：中等 · 标签：Array、Hash Table、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-subarray-sum-with-length-divisible-by-k/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums and an integer k.
Return the maximum sum of a subarray of nums, such that the size of the subarray is divisible by k.

**Examples**

**Example 1:**

```
Input: nums = [1,2], k = 1
Output: 3
Explanation:
The subarray [1, 2] with sum 3 has length equal to 2 which is divisible by 1.
```

**Example 2:**

```
Input: nums = [-1,-2,-3,-4,-5], k = 4
Output: -10
Explanation:
The maximum sum subarray is [-1, -2, -3, -4] which has length equal to 4 which is divisible by 4.
```

**Example 3:**

```
Input: nums = [-5,1,2,-3,4], k = 2
Output: 4
Explanation:
The maximum sum subarray is [1, 2, -3, 4] which has length equal to 4 which is divisible by 2.
```

**Constraints**

- 1 <= k <= nums.length <= 2 * 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。返回 `nums` 中 **子数组**（subarray） 的最大和，要求该子数组的长度能够被 `k` 整除。

## 示例

### 示例 1  
**输入**: `nums = [1,2], k = 1`  
**输出**: `3`  
**解释**: 子数组 `[1, 2]` 的和为 3，长度为 2，能够被 1 整除。

### 示例 2  
**输入**: `nums = [-1,-2,-3,-4,-5], k = 4`  
**输出**: `-10`  
**解释**: 最大和的子数组是 `[-1, -2, -3, -4]`，其长度为 4，能够被 4 整除。

### 示例 3  
**输入**: `nums = [-5,1,2,-3,4], k = 2`  
**输出**: `4`  
**解释**: 最大和的子数组是 `[1, 2, -3, 4]`，其长度为 4，能够被 2 整除。

## 约束条件
- `1 <= k <= nums.length <= 2 * 10^5`
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有可能的子数组** 都枚举一遍，计算它们的和，然后挑选长度能被 `k` 整除且和最大的那一个。  

- **枚举子数组**：用两层循环，外层 `i` 表示子数组的左端点，内层 `j` 表示右端点（`i ≤ j`）。  
- **检查长度**：子数组长度是 `j - i + 1`，只要 ` (j - i + 1) % k == 0` 就符合要求。  
- **求和**：在枚举的过程中把 `nums[i] … nums[j]` 累加得到子数组的和。  

> **类比**：想象你在一本书里找连续的页码，使得页数正好是 `k` 的倍数，并且这些页码上写的数字之和最大。最笨的办法就是把每一种可能的起始页和结束页都试一遍。

这个方法一定能得到正确答案，因为它遍历了所有合法子数组，必然包含最优解。

#### 代码（Python）

```python
def maxSubArrayDivByK_bruteforce(nums, k):
    n = len(nums)
    best = float('-inf')                 # 记录目前找到的最大和
    for i in range(n):                   # 左端点
        cur_sum = 0
        for j in range(i, n):            # 右端点
            cur_sum += nums[j]           # 累加得到 nums[i..j] 的和
            length = j - i + 1
            if length % k == 0:          # 长度能被 k 整除才考虑
                best = max(best, cur_sum)
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 两层循环，每层最坏会遍历 `n` 次，整体是 `n * n`，即平方级。  
  - 用大白话说，就是如果数组有 10,000 个元素，程序要做大约 100,000,000 次加法，明显太慢。  

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`best、cur_sum、i、j`），不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **重复计算子数组的和**。  
我们可以把子数组求和的过程改写为「前缀和」的差值：

> 前缀和 `pre[i]` 表示数组前 `i` 个元素的累计和（`pre[0] = 0`，`pre[1] = nums[0]` ……）。  
> 任意子数组 `nums[l..r]` 的和 = `pre[r+1] - pre[l]`。

所以只要我们知道 **在某个位置之前，哪个前缀和最小**，就能快速算出以当前元素结尾、长度满足 `k` 整除的子数组最大和。

**关键观察**：  
子数组长度要能被 `k` 整除，等价于「左端点 `l` 与右端点 `r+1` 的下标同余 modulo `k`」。  
因为 `length = r - l + 1`，要求 `length % k == 0` → `(r+1 - l) % k == 0` → `(r+1) % k == l % k`。

因此，对每一种余数 `m = index % k`（`m ∈ [0, k-1]`），我们只需要在遍历过程中维护 **当前余数对应的最小前缀和**。  

实现步骤：

1. 计算前缀和 `pre`，同时遍历数组。  
2. 用一个大小为 `k` 的数组 `min_pre`（或字典）记录每个余数 `m` 出现过的最小前缀和，初始为正无穷，`min_pre[0] = 0`（因为 `pre[0] = 0`，余数为 0）。  
3. 当遍历到位置 `i`（对应前缀和 `pre[i]`，`i` 从 1 到 `n`）时：  
   - 余数 `m = i % k`。  
   - 用 `pre[i] - min_pre[m]` 计算**以 `i-1` 为右端点、长度能被 `k` 整除的最大子数组和**。  
   - 更新答案 `ans = max(ans, pre[i] - min_pre[m])`。  
   - 再把 `min_pre[m] = min(min_pre[m], pre[i])`，确保以后出现相同余数时使用更小的前缀和。  

> **类比**：把数组想象成一条路，路上每走一步都会记录累计的风景分数（前缀和）。我们只关心「同一颜色的路标」（余数相同）之间的分数差值，因为只有这样两段路的长度才是 `k` 的倍数。于是我们把每种颜色的“最低风景分数”记下来，遇到同颜色的路标时，立刻算出这段路的分数，找最大值。

#### 代码（Python）

```python
def maxSubArrayDivByK(nums, k):
    """
    返回长度能被 k 整除的子数组的最大和
    """
    n = len(nums)
    # 前缀和，pre[0] = 0，pre[i] 表示前 i 个元素的和
    pre = 0

    # 对每个余数保存出现过的最小前缀和，初始为正无穷
    INF = float('inf')
    min_pre = [INF] * k
    min_pre[0] = 0               # 前缀和为 0 时余数为 0

    ans = -float('inf')          # 因为数组可能全是负数

    for idx, val in enumerate(nums, 1):   # idx 从 1 开始对应 pre 的下标
        pre += val                         # 更新到当前位置的前缀和
        m = idx % k                        # 计算余数

        # 以当前位置为右端点、长度可被 k 整除的子数组最大和
        candidate = pre - min_pre[m]
        if candidate > ans:
            ans = candidate

        # 更新当前余数对应的最小前缀和
        if pre < min_pre[m]:
            min_pre[m] = pre

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，每一步做常数时间的运算（求余、加减、比较），所以线性时间。  
  - 相比暴力的 `O(n²)`，快了很多；如果 `n = 200,000`，只需要大约 200,000 次操作，几乎瞬间完成。  

- **空间复杂度**：`O(k)`  
  - 只用了长度为 `k` 的 `min_pre` 数组（`k ≤ n ≤ 2·10⁵`），不随 `n` 增长太多。  
  - 用大白话说，就是我们只需要记住 `k` 种颜色的最小前缀分数，而不是记住全部 `n` 个位置。

---

## 心得  

- **核心技巧**：利用**前缀和 + 同余分组（余数哈希）**，把“子数组长度能被 `k` 整除”转化为“左右端点的下标余数相同”。  
- **适用题型**：  
  1. “子数组和等于某个值且长度满足特定模数”  
  2. “最长子数组长度能被 `k` 整除且和为正”  
  3. “最大子数组和，要求子数组长度是 `k` 的倍数”  
- **一句话总结**：**把长度约束映射到下标余数，用最小前缀和把差值最大化**。

---

## 反思  

- **第一反应**：直接想到枚举子数组（暴力），因为最直观。  
- **最容易踩的坑**：  
  - 忘记在 `min_pre` 中预先放入 `0`（对应余数 0），导致第一个合法子数组被遗漏。  
  - 负数数组时要把答案初始化为负无穷，否则可能返回错误的 0。  
  - `idx` 的起始要从 `1` 开始，这样余数对应的是前缀和的下标，而不是数组元素下标。  
- **下次类似题的第一步**：先写出前缀和公式，检查约束能否转化为“下标同余”，再决定是否需要维护每种余数的极值（最小或最大）。这样可以快速从 `O(n²)` 进入 `O(n)`。