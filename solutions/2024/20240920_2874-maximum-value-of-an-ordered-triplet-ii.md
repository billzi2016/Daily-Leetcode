# #2874. 有序三元组的最大值 II / Maximum Value of an Ordered Triplet II

> 难度：中等 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/maximum-value-of-an-ordered-triplet-ii/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
Return the maximum value over all triplets of indices (i, j, k) such that i < j < k. If all such triplets have a negative value, return 0.
The value of a triplet of indices (i, j, k) is equal to (nums[i] - nums[j]) * nums[k].

**Examples**

**Example 1:**

```
Input: nums = [12,6,1,2,7]
Output: 77
Explanation: The value of the triplet (0, 2, 4) is (nums[0] - nums[2]) * nums[4] = 77.
It can be shown that there are no ordered triplets of indices with a value greater than 77.
```

**Example 2:**

```
Input: nums = [1,10,3,4,19]
Output: 133
Explanation: The value of the triplet (1, 2, 4) is (nums[1] - nums[2]) * nums[4] = 133.
It can be shown that there are no ordered triplets of indices with a value greater than 133.
```

**Example 3:**

```
Input: nums = [1,2,3]
Output: 0
Explanation: The only ordered triplet of indices (0, 1, 2) has a negative value of (nums[0] - nums[1]) * nums[2] = -3. Hence, the answer would be 0.
```

**Constraints**

- 3 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `nums`。  
返回所有满足 `i < j < k` 的下标三元组 `(i, j, k)` 中的最大值。如果所有此类三元组的值均为负数，则返回 `0`。  

下标三元组 `(i, j, k)` 的值定义为 `(nums[i] - nums[j]) * nums[k]`。  

**示例**  

**示例 1**  
```
输入: nums = [12,6,1,2,7]
输出: 77
解释: 三元组 (0, 2, 4) 的值为 (nums[0] - nums[2]) * nums[4] = 77。
可以证明不存在值大于 77 的有序三元组。
```

**示例 2**  
```
输入: nums = [1,10,3,4,19]
输出: 133
解释: 三元组 (1, 2, 4) 的值为 (nums[1] - nums[2]) * nums[4] = 133。
可以证明不存在值大于 133 的有序三元组。
```

**示例 3**  
```
输入: nums = [1,2,3]
输出: 0
解释: 唯一的有序三元组 (0, 1, 2) 的值为 (nums[0] - nums[1]) * nums[2] = -3，为负数。因此答案为 0。
```

**约束条件**  

- `3 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把所有可能的三元组 `(i, j, k)` 都枚举一遍，计算它们的值 `(nums[i] - nums[j]) * nums[k]`，把最大的记下来。  
- **使用的数据结构**：只需要一个普通的 Python 列表 `nums`，以及几个整型变量来保存当前最大值。可以把它想象成我们在超市里把所有商品的组合都挑出来试吃，虽然慢，但一定能找到味道最好的那一组。  
- **为什么正确**：因为我们把所有满足 `i < j < k` 的组合都检查了一遍，答案一定在其中，所以最大值一定被找到。  
- **时间/空间复杂度**：  
  - 外层循环 `i`、中层循环 `j`、内层循环 `k`，每层最多遍历 `n` 次，整体是 `n × n × n = n³`。在大白话里，若数组长度是 1000，暴力解大约要跑 **10⁹** 次计算，几乎不可接受。  
  - 只用了常数级别的额外空间，记作 **O(1)**。

#### 代码（Python）

```python
def maximumTripletValue_bruteforce(nums):
    n = len(nums)
    max_val = 0                     # 记录最大值，题目要求全负返回 0
    # 枚举 i
    for i in range(n - 2):
        # 枚举 j，必须在 i 之后
        for j in range(i + 1, n - 1):
            # 枚举 k，必须在 j 之后
            for k in range(j + 1, n):
                cur = (nums[i] - nums[j]) * nums[k]   # 计算当前三元组的价值
                if cur > max_val:                     # 更新最大值
                    max_val = cur
    return max_val
```

#### 复杂度

- **时间复杂度**：**O(n³)** —— 三层循环，每层都要遍历 `n` 次。  
  - 大白话：如果 `n = 10⁴`，运算次数大约是 `10¹²`，普通电脑根本跑不完。  
- **空间复杂度**：**O(1)** —— 只用了几个额外的整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**重复遍历**：对同一个 `i`、`j`、`k` 位置的元素我们会多次比较。  
观察公式 `(nums[i] - nums[j]) * nums[k]`，可以把它拆成两部分：

1. **左侧**：`nums[i] - nums[j]`，只和 `i`、`j` 有关。  
   - 对于固定的 `j`，我们希望 `i` 尽可能小（因为 `nums[i]` 要最大），即在 `j` 左边取最大的 `nums[i]`。  
   - 用 **前缀最大** 数组 `prefix_max` 预处理：`prefix_max[t] = max(nums[0..t])`。这样 `prefix_max[j-1]` 就是 `j` 左边的最大值。

2. **右侧**：`* nums[k]`，只和 `k` 有关。  
   - 对于同一个 `j`，我们希望 `k` 在 `j` 右边且 `nums[k]` 最大。  
   - 用 **后缀最大** 数组 `suffix_max` 预处理：`suffix_max[t] = max(nums[t..n-1])`。于是 `suffix_max[j+1]` 就是 `j` 右边的最大值。

于是，对于每一个可能的中间下标 `j`，**最优的 i 与 k** 已经可以直接通过这两个预处理数组得到，计算式子变成：

```
value(j) = (prefix_max[j-1] - nums[j]) * suffix_max[j+1]
```

只要遍历一次所有 `j`（从 `1` 到 `n-2`），取最大的 `value(j)` 即可。如果所有 `value(j)` 都是负数，返回 `0`（我们在比较时已经把 `0` 作为初始最大值）。

**核心概念解释**  
- **前缀最大**：想象你在看一本书，从左到右读，每翻到一页就记下目前看到的最高分数，这个最高分数随时可以直接拿来使用。  
- **后缀最大**：类似地，从右往左看书，随时记下后面（即右边）出现的最高分数。

这两个数组只需要一次线性扫描即可得到，整体时间 **O(n)**，空间 **O(n)**（存两个额外数组）。

#### 代码（Python）

```python
def maximumTripletValue(nums):
    n = len(nums)
    if n < 3:
        return 0

    # 1️⃣ 预处理前缀最大
    prefix_max = [0] * n
    cur_max = nums[0]
    for i in range(n):
        cur_max = max(cur_max, nums[i])   # 当前的最大值
        prefix_max[i] = cur_max           # 保存到数组中

    # 2️⃣ 预处理后缀最大
    suffix_max = [0] * n
    cur_max = nums[-1]
    for i in range(n - 1, -1, -1):
        cur_max = max(cur_max, nums[i])   # 当前的最大值（从右往左）
        suffix_max[i] = cur_max           # 保存到数组中

    # 3️⃣ 枚举中间下标 j，计算可能的最大值
    ans = 0  # 题目要求全负返回 0
    for j in range(1, n - 1):               # j 必须有左边和右边
        left_best = prefix_max[j - 1]       # i 左侧的最大 nums[i]
        right_best = suffix_max[j + 1]      # k 右侧的最大 nums[k]
        cur = (left_best - nums[j]) * right_best
        if cur > ans:
            ans = cur
    return ans
```

#### 复杂度

- **时间复杂度**：**O(n)**  
  - 只做了三次线性遍历（一次构前缀，一次构后缀，一次枚举 `j`），所以即使 `n = 10⁵` 也能在毫秒级完成。  
  - 与暴力解的 `O(n³)` 相比，快了 **n²** 级别，若 `n = 10⁴`，从 **10¹²** 次下降到 **10⁴** 次。

- **空间复杂度**：**O(n)**  
  - 需要额外的两个长度为 `n` 的数组来存前缀最大和后缀最大。  
  - 若想进一步省空间，可以在遍历时仅维护一个变量保存左侧最大，右侧最大可以先算好再在遍历时逐步更新（仍是 O(n) 时间，O(1) 额外空间），这里为了代码可读性保留了两数组。

---

## 心得

- **核心技巧**：利用**前缀/后缀最大**（或最小）快速获取区间的极值，化简三元组/多元组的枚举问题。  
- **适用的题型**：  
  1. “Maximum Value of an Ordered Triplet I/II” 系列。  
  2. “Maximum Product of Three Numbers” 需要在左右两侧分别找最大/最小值。  
  3. “Best Sightseeing Pair” 等需要左侧最优 + 右侧最优的组合问题。  
- **一句话总结解题钥匙**：把“左边最好的 i”和“右边最好的 k”提前算好，遍历一次中间位置 `j` 即可得到全局最优。

---

## 反思

- **第一反应**：看到 `(nums[i] - nums[j]) * nums[k]`，自然想到“三层循环枚举”，因为这是最直观的做法。  
- **最容易踩的坑**：  
  - 忘记 `i < j < k` 的顺序限制，导致使用了错误的极值（比如在右侧用了已经在左侧出现的最大值）。  
  - 直接返回负数而不是 `0`（题目要求全负返回 `0`），需要在答案初始化时把 `0` 设为下界。  
  - 边界条件：`j` 不能是第一个或最后一个元素，否则左/右侧不存在合法的 `i` 或 `k`。  
- **下次遇到同类题**：第一步先思考“**能否把某一段的最优值提前算好**”，如果可以，就先做前缀/后缀（或单调栈）预处理，再在一次遍历里完成整体最优。