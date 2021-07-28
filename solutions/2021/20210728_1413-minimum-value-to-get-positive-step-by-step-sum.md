# #1413. 最小正数起始值使逐步累计和始终为正 / Minimum Value to Get Positive Step by Step Sum

> 难度：简单 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-value-to-get-positive-step-by-step-sum/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums, you start with an initial positive value startValue.
In each iteration, you calculate the step by step sum of startValue plus elements in nums (from left to right).
Return the minimum positive value of startValue such that the step by step sum is never less than 1.

**Examples**

**Example 1:**

```
Input: nums = [-3,2,-3,4,2]
Output: 5
Explanation: If you choose startValue = 4, in the third iteration your step by step sum is less than 1.
step by step sum
startValue = 4 | startValue = 5 | nums
  (4 -3 ) = 1  | (5 -3 ) = 2    |  -3
  (1 +2 ) = 3  | (2 +2 ) = 4    |   2
  (3 -3 ) = 0  | (4 -3 ) = 1    |  -3
  (0 +4 ) = 4  | (1 +4 ) = 5    |   4
  (4 +2 ) = 6  | (5 +2 ) = 7    |   2
```

**Example 2:**

```
Input: nums = [1,2]
Output: 1
Explanation: Minimum start value should be positive.
```

**Example 3:**

```
Input: nums = [1,-2,-3]
Output: 5
```

**Constraints**

- 1 <= nums.length <= 100
- -100 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个整数（integer）数组 `nums`，你需要选择一个初始的正数起始值 `startValue`。  
在每一次迭代（iteration）中，你计算 `startValue` 加上 `nums` 中元素（从左到右）的**逐步累计和（step by step sum）**。  
返回能够保证 **逐步累计和** 始终不小于 `1` 的最小正整数 `startValue`。

**示例 1**  
```text
Input: nums = [-3,2,-3,4,2]
Output: 5
Explanation: 如果选择 `startValue = 4`，在第三次迭代时，逐步累计和会小于 1。
逐步累计和
startValue = 4 | startValue = 5 | nums
  (4 -3 ) = 1  | (5 -3 ) = 2    |  -3
  (1 +2 ) = 3  | (2 +2 ) = 4    |   2
  (3 -3 ) = 0  | (4 -3 ) = 1    |  -3
  (0 +4 ) = 4  | (1 +4 ) = 5    |   4
  (4 +2 ) = 6  | (5 +2 ) = 7    |   2
```

**示例 2**  
```text
Input: nums = [1,2]
Output: 1
Explanation: 最小的起始值必须为正数。
```

**示例 3**  
```text
Input: nums = [1,-2,-3]
Output: 5
```

**约束条件**  
- `1 <= nums.length <= 100`  
- `-100 <= nums[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从 1 开始尝试所有可能的 startValue**，每尝一个值就模拟一次“从左到右累计求和”的过程，检查累计和在任何一步是否小于 1。  
- **数据结构**：只需要一个普通的整数 `cur` 来保存当前的累计和，相当于我们手里的一支笔，一边算一边写。  
- **正确性**：如果某个 `startValue` 能让所有中间累计和都 ≥ 1，那么它必然是满足题目要求的解。因为我们是从最小的正整数 1 开始逐个递增检查的，第一个成功的 `startValue` 就是答案。  

#### 代码（Python）

```python
def minStartValue_bruteforce(nums):
    start = 1                     # 从最小的正整数开始尝试
    while True:                   # 无限循环，直到找到答案
        cur = start               # 当前累计和，从 start 开始
        ok = True                 # 标记该 start 是否满足条件
        for x in nums:            # 依次遍历数组
            cur += x              # 累计求和
            if cur < 1:          # 一旦出现小于 1 的情况
                ok = False        # 说明这个 start 不行
                break
        if ok:                    # 如果整个遍历都没有 break
            return start          # 找到答案，直接返回
        start += 1                # 否则尝试更大的 start
```

#### 复杂度  

- **时间复杂度**：`O(k·n)`，其中 `n = len(nums)`，`k` 是答案的大小。最坏情况下我们要从 1 试到答案 `k`，每次遍历全部 `n` 个元素。  
  - **大白话**：如果答案是 100，需要跑 100 次，每次看 100 个数，整体大概是 10 000 步。
- **空间复杂度**：`O(1)`，只用了几个整数变量，和数组大小无关。

---

### 2. 最优解

#### 思路  

暴力解的慢点在于**不断重复遍历数组**。实际上，我们只需要一次遍历就能得到答案：

1. 设 `prefix` 为从数组起点到当前位置的**前缀和**（不包括 startValue）。  
2. 记录遍历过程中出现的**最小前缀和** `min_prefix`。  
3. 为了让“起始值 + 前缀和”在每一步都 ≥ 1，最差的情况就是在出现最小前缀和的那一步。  
   - 设 `startValue + min_prefix ≥ 1` → `startValue ≥ 1 - min_prefix`。  
4. 因为 `startValue` 必须是**正整数**，所以答案就是 `max(1, 1 - min_prefix)`。

> **类比**：把前缀和想象成一条河流的水位，`min_prefix` 是河谷最低的水位。我们要把河流的起始水位（`startValue`）调高，让整条河流的水位永远不低于 1。

#### 代码（Python）

```python
def minStartValue(nums):
    """
    返回能够保证每一步累计和都不小于 1 的最小正整数 startValue
    """
    prefix = 0          # 当前前缀和（不含 startValue）
    min_prefix = 0      # 记录遍历过程中出现的最小前缀和

    for x in nums:      # 只遍历一次数组
        prefix += x
        if prefix < min_prefix:   # 更新最小前缀和
            min_prefix = prefix

    # 根据公式 startValue >= 1 - min_prefix
    # 若 min_prefix 已经 >= 0，则 1 - min_prefix <= 1，答案就是 1
    return max(1, 1 - min_prefix)
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次数组。  
  - **大白话**：如果数组有 100 个数，我们只看一次，最多走 100 步。
- **空间复杂度**：`O(1)`，只用了常数个整数变量。

---

## 心得

- **核心技巧**：**前缀和 + 最小前缀值**。通过一次遍历求出最小前缀和，再利用简单的代数关系得到答案。  
- **适用的题型**：  
  1. “寻找最小初始值使累计和不低于阈值”类（如 LeetCode 1413）。  
  2. “数组子段和的最小/最大值”问题（如最大子数组和）。  
  3. “累计和不出现负数”类（如平衡括号的前缀计数）。  
- **一句话总结**：**把整个过程抽象成“起始值 + 前缀和”，只要找出最低的前缀点，就能一次算出最小起始值**。

---

## 反思

- **第一反应**：看到“每一步累计和不小于 1”，自然会想到**模拟**每一次累加，检查是否满足条件。  
- **最容易踩的坑**：  
  - 忘记**起始值必须是正整数**，直接返回 `1 - min_prefix` 可能得到 0 或负数。  
  - 错误地把 `startValue` 包含进前缀和的累计，导致公式出错。  
  - 忽视空数组的极端情况（虽然题目保证长度 ≥ 1）。  
- **下次遇到同类题**，第一步应该：**把问题转化为“起始值 + 前缀和 ≥ 常数”，先求最小前缀和，再用代数公式直接求解**。这样可以立刻从 O(n²) 降到 O(n)。