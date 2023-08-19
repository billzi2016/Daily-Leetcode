# #2367. 等差三元组的数量 / Number of Arithmetic Triplets

> 难度：简单 · 标签：Array、Hash Table、Two Pointers、Enumeration · [LeetCode 链接](https://leetcode.com/problems/number-of-arithmetic-triplets/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed, strictly increasing integer array nums and a positive integer diff. A triplet (i, j, k) is an arithmetic triplet if the following conditions are met:
Return the number of unique arithmetic triplets.

**Examples**

**Example 1:**

```
Input: nums = [0,1,4,6,7,10], diff = 3
Output: 2
Explanation:
(1, 2, 4) is an arithmetic triplet because both 7 - 4 == 3 and 4 - 1 == 3.
(2, 4, 5) is an arithmetic triplet because both 10 - 7 == 3 and 7 - 4 == 3.
```

**Example 2:**

```
Input: nums = [4,5,6,7,8,9], diff = 2
Output: 2
Explanation:
(0, 2, 4) is an arithmetic triplet because both 8 - 6 == 2 and 6 - 4 == 2.
(1, 3, 5) is an arithmetic triplet because both 9 - 7 == 2 and 7 - 5 == 2.
```

**Constraints**

- 3 <= nums.length <= 200
- 0 <= nums[i] <= 200
- 1 <= diff <= 50
- nums is strictly increasing.

---

## 题目（中文翻译）

给定一个 **0 索引**、严格递增的整数数组 `nums` 与一个正整数 `diff`。若三元组 `(i, j, k)` 满足以下条件，则称其为 **等差三元组（arithmetic triplet）**：

- `i < j < k`
- `nums[j] - nums[i] == diff`
- `nums[k] - nums[j] == diff`

返回唯一等差三元组的数量。

**示例 1**  
**输入**: `nums = [0,1,4,6,7,10]`, `diff = 3`  
**输出**: `2`  
**解释**:  
- `(1, 2, 4)` 是等差三元组，因为 `7 - 4 == 3` 且 `4 - 1 == 3`。  
- `(2, 4, 5)` 是等差三元组，因为 `10 - 7 == 3` 且 `7 - 4 == 3`。

**示例 2**  
**输入**: `nums = [4,5,6,7,8,9]`, `diff = 2`  
**输出**: `2`  
**解释**:  
- `(0, 2, 4)` 是等差三元组，因为 `8 - 6 == 2` 且 `6 - 4 == 2`。  
- `(1, 3, 5)` 是等差三元组，因为 `9 - 7 == 2` 且 `7 - 5 == 2`。

**约束条件**  
- `3 <= nums.length <= 200`  
- `0 <= nums[i] <= 200`  
- `1 <= diff <= 50`  
- `nums` 为严格递增序列。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的三元组 `(i, j, k)` 都枚举一遍，然后检查它们是否满足  

```
nums[j] - nums[i] == diff   且   nums[k] - nums[j] == diff
```

- **使用的数据结构**：只需要数组 `nums` 本身。  
  - 把数组想象成排好序的书架，每本书都有唯一的编号（下标）。我们要找的就是在书架上相隔固定距离 `diff` 的三本书。  

- **为什么正确**：因为我们把 **所有** 可能的 `(i, j, k)`（满足 `i < j < k`）都检查了一遍，只要有满足条件的，就一定会被计数。  

- **时间/空间复杂度**  
  - 我们用了三层循环：外层 `i`、中层 `j`、内层 `k`。每层最多遍历 `n` 次（`n = len(nums)`），所以总的比较次数是 `O(n³)`。  
    - 大白话：如果数组有 100 个元素，暴力法大约要做 100 × 100 × 100 = 1,000,000 次检查，显然会很慢。  
  - 只用了常数级别的额外空间（几个计数器），所以是 `O(1)`。

#### 代码（Python）

```python
def arithmeticTriplets(nums, diff):
    n = len(nums)
    cnt = 0                       # 记录满足条件的三元组个数

    # i < j < k 三重循环，枚举所有可能的下标组合
    for i in range(n):
        for j in range(i + 1, n):
            # 先检查第一个差值是否为 diff，若不等直接跳过 k 循环
            if nums[j] - nums[i] != diff:
                continue
            for k in range(j + 1, n):
                # 检查第二个差值是否为 diff
                if nums[k] - nums[j] == diff:
                    cnt += 1      # 找到一个合法的三元组
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 解释：三层循环每层最多遍历 `n` 次，整体是 `n × n × n`。  
- **空间复杂度**：`O(1)`  
  - 解释：只用了几个整数变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于三层循环导致的 `O(n³)`。观察题目条件：

1. `nums` 已经是 **严格递增** 的有序数组。  
2. `diff` 是已知的正整数。  

因为数组有序，我们只要判断 **是否存在** `x - diff` 和 `x + diff` 两个数，就能确定一个三元组。换句话说，若某个数 `num` 在数组中出现，并且 `num - diff` 与 `num + diff` 也都在数组中，那么这三个数必然构成一个等差三元组，且下标顺序自然满足 `i < j < k`。

所以我们可以把 “查找某个数是否出现” 的操作交给 **哈希表**（Python 中的 `set`）来完成，查询时间是 `O(1)`。遍历一次数组即可统计答案，时间降到 `O(n)`。

- **核心数据结构**：`set`（集合），类似于字典的查字典功能：给出一个“词”（这里是数值），立刻返回它是否在书中出现（是否在集合里）。  
- **步骤**  
  1. 把所有 `nums` 放进 `set_nums`，这样后面查询是否存在某个数只需要 `O(1)`。  
  2. 再遍历一次 `nums`，对每个 `num` 检查 `num - diff` 与 `num + diff` 是否都在 `set_nums`。  
  3. 若都在，则说明找到了一个合法的三元组，计数加一。  

因为数组是递增的，`num - diff` 必然对应更小的下标，`num + diff` 必然对应更大的下标，所以不会出现重复计数的情况。

#### 代码（Python）

```python
def arithmeticTriplets(nums, diff):
    # 把所有元素放进集合，后面查询是否存在某个数只需要 O(1)
    num_set = set(nums)

    cnt = 0
    for num in nums:
        # 检查左边的 num - diff 与右边的 num + diff 是否都在集合里
        if (num - diff) in num_set and (num + diff) in num_set:
            cnt += 1
    return cnt
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：第一次把数组转成集合是 `O(n)`，第二次遍历数组也是 `O(n)`，两者相加仍然是线性时间。相比暴力的 `O(n³)`，速度提升了几个数量级。  
- **空间复杂度**：`O(n)`  
  - 解释：我们额外用了一个集合来存储 `n` 个数，空间随输入规模线性增长。

---

## 心得

- **核心技巧**：利用 **哈希表（集合）** 在有序数组中快速判断某个数是否存在，从而把三层枚举压缩到一次线性扫描。  
- **适用的题型**  
  1. “找三元组满足固定差值” 类题（如本题）。  
  2. “找两个数之和为 target” 的变形（使用集合或字典快速查找配对）。  
  3. “判断数组中是否存在连续的等差序列” 等需要快速成员查询的场景。  
- **一句话总结**：**把“是否出现”交给集合，遍历一次即可完成计数**。

## 反思

- **第一反应**：看到“strictly increasing”和“小范围的 diff”，自然想到可以用哈希表快速查找。  
- **最容易踩的坑**  
  - **重复计数**：如果直接用三层循环并在内部判断 `num - diff` 与 `num + diff`，要注意只在 `num` 为中间元素时计数，避免把同一个三元组算两次。  
  - **边界条件**：当 `num - diff` 小于最小元素或 `num + diff` 大于最大元素时，集合查询仍然是 `False`，不需要额外判断。  
- **下次遇到同类题**：第一步先想 “能不能把查找改成 O(1) 的操作？”——如果可以，用哈希表/集合把枚举次数从指数级降到线性级。