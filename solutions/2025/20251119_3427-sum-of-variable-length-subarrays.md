# #3427. 可变长度子数组之和 / Sum of Variable Length Subarrays

> 难度：简单 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/sum-of-variable-length-subarrays/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of size n. For each index i where 0 <= i < n, define a subarray nums[start ... i] where start = max(0, i - nums[i]).
Return the total sum of all elements from the subarray defined for each index in the array.

**Examples**

**Example 1:**

```
Input: nums = [2,3,1]
Output: 11
Explanation:
The total sum is 11. Hence, 11 is the output.
```

**Example 2:**

```
Input: nums = [3,1,1,2]
Output: 13
Explanation:
The total sum is 13. Hence, 13 is the output.
```

**Constraints**

- 1 <= n == nums.length <= 100
- 1 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`（array）。对于每个满足 `0 <= i < n` 的索引 `i`，定义子数组（subarray） `nums[start ... i]`，其中 `start = max(0, i - nums[i])`。返回对数组中每个索引所定义的子数组中所有元素的总和。

**示例 1**  
输入: `nums = [2,3,1]`  
输出: `11`  
解释:  
总和为 11。因此输出 11。

**示例 2**  
输入: `nums = [3,1,1,2]`  
输出: `13`  
解释:  
总和为 13。因此输出 13。

**约束条件**  
- `1 <= n == nums.length <= 100`  
- `1 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**逐个索引**去算它对应的子数组之和，然后把所有这些和累加起来。

- **子数组的起点**：`start = max(0, i - nums[i])`  
  这里的 `max` 可以想象成“把指针往左走 `nums[i]` 步，但不能走出数组左边界”。  
- **子数组本身**：`nums[start … i]` 就像我们在数组里从 `start` 位置一直往右读到 `i`。  
- **把所有子数组的和相加**：对每个 `i`，把它对应子数组里所有元素相加，然后把这些结果再相加。

因为题目只要求**总和**，不需要保存每个子数组的和，只要在遍历时把它们加进去即可。

**为什么正确**  
每个索引 `i` 的子数组都是题目明确规定的，暴力遍历正好把它们全部算出来并相加，等价于题目要求的“总和”。

**复杂度分析（大白话）**  

- 外层循环遍历 `n` 次（每个位置一次），  
- 内层循环在最坏情况下也要遍历 `n` 次（比如 `nums[i]` 很大，子数组几乎是从 0 到 `i`），  
- 所以总的操作次数大约是 `n × n`，记作 **O(n²)**。  
  用生活中的例子说，假如有 100 本书，逐本书去检查前面所有书的页数，总共要检查 10 000 次，这就是二次方的规模。  
- 额外使用的空间只有几个整数变量，**O(1)**（常数级）空间。

#### 代码（Python）

```python
def sumVariableLengthSubarrays(nums):
    n = len(nums)
    total = 0                     # 最终答案

    for i in range(n):            # 逐个索引 i
        start = max(0, i - nums[i])   # 子数组左边界，不能小于 0
        # 把子数组 nums[start … i] 的所有元素加到 total
        for j in range(start, i + 1):
            total += nums[j]      # 累加每个元素

    return total
```

#### 复杂度

- **时间复杂度：O(n²)**  
  解释：如果 `n=100`，最坏情况下要做约 `100×100 = 10 000` 次加法。  
- **空间复杂度：O(1)**  
  只用了几个整型变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在**每次都要遍历子数组**，导致重复计算。  
例如，`i=5` 时我们把 `nums[2]…nums[5]` 加了一遍，`i=6` 时又要把 `nums[2]…nums[6]` 再加一次，其中 `nums[2]…nums[5]` 被重复算了两次。

**前缀和**（Prefix Sum）可以一次性把「从数组开头到任意位置」的累计和保存下来，后面求任意区间的和就只需要两次查表相减，时间是 **O(1)**。

前缀和的定义：

```
pref[0] = 0
pref[k] = nums[0] + nums[1] + … + nums[k-1]   (k ≥ 1)
```

可以把它想象成一本“累计总页数的字典”：`pref[k]` 记录了前 `k` 本书的总页数。

有了 `pref`，子数组 `nums[start … i]` 的和就是：

```
sum(start, i) = pref[i+1] - pref[start]
```

因为 `pref[i+1]` 包含了 `0 … i`，而 `pref[start]` 包含了 `0 … start-1`，两者相减正好剩下 `start … i`。

**整体步骤**：

1. 先一次遍历构造前缀和数组 `pref`（O(n)）。
2. 再遍历每个 `i`，利用 `start = max(0, i - nums[i])`，用前缀和快速算出子数组和 `pref[i+1] - pref[start]`，累加到答案中。

这样每个 `i` 只做 **常数次** 操作，整体时间降到 **O(n)**，空间使用 `pref`（长度 `n+1`），即 **O(n)**。

#### 代码（Python）

```python
def sumVariableLengthSubarrays(nums):
    n = len(nums)

    # 1️⃣ 构造前缀和数组，pref[k] = nums[0] + … + nums[k-1]
    pref = [0] * (n + 1)          # 长度 n+1，pref[0] = 0
    for i in range(n):
        pref[i + 1] = pref[i] + nums[i]   # 累计前 i+1 个元素的和

    total = 0                     # 最终答案

    # 2️⃣ 逐个索引计算对应子数组的和，利用前缀和 O(1) 求区间和
    for i in range(n):
        start = max(0, i - nums[i])          # 子数组左边界
        sub_sum = pref[i + 1] - pref[start]  # 区间和 = 前缀和差
        total += sub_sum                     # 累加到整体答案

    return total
```

#### 复杂度

- **时间复杂度：O(n)**  
  只遍历两遍数组（一次建前缀和，一次求答案），如果 `n=100`，最多做 200 次加法/减法，远远快于 10 000 次的暴力解。  
- **空间复杂度：O(n)**  
  需要额外的前缀和数组 `pref`，长度是 `n+1`，相当于再开了一个和原数组等长的空间。若在意空间，还可以把前缀和压缩为单个变量（滚动前缀），但这里保持可读性。

---

## 心得

- **核心技巧**：前缀和（Prefix Sum）把「区间求和」从线性时间压缩到常数时间。  
- **适用的题型**：  
  1. 求多个子数组/区间的和（如 LeetCode 560 子数组和为 K）。  
  2. 统计满足某种区间条件的子数组数量（如 896. 单调数列的子数组计数）。  
  3. 需要快速求任意区间累计值的题目（如 209. 长度最小的子数组）。  
- **一句话总结**：**把“从头到任意位置的累计和”提前算好，后面每次只要两次查表相减，就能瞬间得到任意子数组的和。**

---

## 反思

- **拿到题目第一反应**：直接按定义遍历每个 `i`，把对应子数组的所有元素累加——也就是暴力解。  
- **最容易踩的坑**：  
  - `start` 可能为负数，需要 `max(0, …)` 防止越界。  
  - 计算子数组和时别忘了包含 `i` 本身（区间是闭区间），所以前缀和要取 `pref[i+1]`。  
- **下次遇到同类题，第一步该想到**：**是否可以用前缀和把“区间求和”一次性预处理？**如果答案是“是”，就可以把时间从二次方降到线性。