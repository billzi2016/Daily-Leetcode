# #1913. 两个数对之间的最大乘积差 / Maximum Product Difference Between Two Pairs

> 难度：简单 · 标签：Array、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-product-difference-between-two-pairs/)

---

## 题目（英文原版）

**Description**

The product difference between two pairs (a, b) and (c, d) is defined as (a * b) - (c * d).
Given an integer array nums, choose four distinct indices w, x, y, and z such that the product difference between pairs (nums[w], nums[x]) and (nums[y], nums[z]) is maximized.
Return the maximum such product difference.

**Examples**

**Example 1:**

```
Input: nums = [5,6,2,7,4]
Output: 34
Explanation: We can choose indices 1 and 3 for the first pair (6, 7) and indices 2 and 4 for the second pair (2, 4).
The product difference is (6 * 7) - (2 * 4) = 34.
```

**Example 2:**

```
Input: nums = [4,2,5,9,7,4,8]
Output: 64
Explanation: We can choose indices 3 and 6 for the first pair (9, 8) and indices 1 and 5 for the second pair (2, 4).
The product difference is (9 * 8) - (2 * 4) = 64.
```

**Constraints**

- 4 <= nums.length <= 104
- 1 <= nums[i] <= 104

---

## 题目（中文翻译）

两个数对 (a, b) 与 (c, d) 的乘积差（product difference）定义为 \((a \times b) - (c \times d)\)。  
给定一个整数数组（integer array）`nums`，选择四个互不相同的下标 `w, x, y, z`，使得数对 \((\text{nums}[w], \text{nums}[x])\) 与 \((\text{nums}[y], \text{nums}[z])\) 的乘积差达到最大。  
返回该最大乘积差的值。

**示例 1**  
**输入**: `nums = [5,6,2,7,4]`  
**输出**: `34`  
**解释**: 我们可以选取下标 1 和 3 组成第一个数对 \((6, 7)\)，选取下标 2 和 4 组成第二个数对 \((2, 4)\)。  
乘积差为 \((6 \times 7) - (2 \times 4) = 34\)。

**示例 2**  
**输入**: `nums = [4,2,5,9,7,4,8]`  
**输出**: `64`  
**解释**: 我们可以选取下标 3 和 6 组成第一个数对 \((9, 8)\)，选取下标 1 和 5 组成第二个数对 \((2, 4)\)。  
乘积差为 \((9 \times 8) - (2 \times 4) = 64\)。

**约束条件**  
- \(4 \leq \text{nums.length} \leq 10^4\)  
- \(1 \leq \text{nums}[i] \leq 10^4\)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有** 可能的四个下标 `(w, x, y, z)` 都枚举一遍，计算  
\[
(nums[w]\times nums[x])-(nums[y]\times nums[z])
\]
的值，取最大的那个。  

- **使用的数据结构**：这里只需要 Python 的列表 `nums`，以及四层 `for` 循环。可以把它想象成在超市里挑选四件商品，**每一种挑选方式** 都要尝试一次，看看能得到的“优惠”（即乘积差）有多大。  
- **为什么正确**：因为我们把所有合法的组合都遍历到了，最大值一定会在其中出现。  

> **提示**：题目要求四个下标必须互不相同，所以在枚举时要确保 `w、x、y、z` 互不相等。

#### 代码（Python）

```python
def maxProductDifference_bruteforce(nums):
    n = len(nums)
    best = float('-inf')                 # 用一个很小的数先占位
    # 四层循环枚举四个不同的下标
    for w in range(n):
        for x in range(n):
            if x == w:                    # 保证 w、x 不同
                continue
            for y in range(n):
                if y == w or y == x:      # 保证 y 与前面的下标不同
                    continue
                for z in range(n):
                    if z == w or z == x or z == y:   # 四个下标全不相等
                        continue
                    # 计算乘积差
                    diff = nums[w] * nums[x] - nums[y] * nums[z]
                    # 取最大值
                    if diff > best:
                        best = diff
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n⁴)`  
  四层循环每层都要遍历 `n` 次，整体就是 `n × n × n × n = n⁴`。  
  用大白话说，就是如果数组有 10 个元素，程序要检查大约 `10⁴ = 10,000` 种组合；如果是 1000 个元素，检查的次数会变成 `10¹²`，几乎不可能在合理时间内跑完。  
- **空间复杂度**：`O(1)`  
  只用了常数个额外变量（`best、diff`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们把所有四元组都遍历了一遍，实际上只需要关注 **四个数**：  

- 为了让 `(a*b) - (c*d)` 最大，显然 **`a*b` 要尽可能大**，**`c*d` 要尽可能小**。  
- 在一个只含正整数的数组里，**最大乘积** 必然由 **最大的两个数** 组成；**最小乘积** 必然由 **最小的两个数** 组成（因为所有数都是正的，乘积随数值增大而增大）。

所以问题可以化简为：

1. 找出数组中最大的两个数 `max1 ≥ max2`。  
2. 找出数组中最小的两个数 `min1 ≤ min2`。  
3. 计算 `max1 * max2 - min1 * min2`，即为答案。

> **类比**：想象你在选两支“最强”的拳击手去打比赛（最大乘积），再选两支“最弱”的拳击手去做防守（最小乘积），最终的“实力差距”就是这两个乘积的差。

**两种实现方式**  

- **排序**：把数组从小到大排好序，直接取前两位和后两位。时间 `O(n log n)`（排序的代价），代码最直观。  
- **一次遍历**：在遍历数组的过程中同步维护四个变量：`max1, max2, min1, min2`。时间 `O(n)`，空间 `O(1)`，更高效。

下面给出一次遍历的实现，因为它既快又容易理解。

#### 代码（Python）

```python
def maxProductDifference(nums):
    """
    在一次遍历中找出最大两个数和最小两个数，随后计算乘积差。
    由于题目保证 nums[i] 都是正整数，这种做法一定正确。
    """
    # 初始化四个变量
    # 为了方便比较，使用极大/极小的哨兵值
    max1 = max2 = -float('inf')   # 当前看到的最大、第二大
    min1 = min2 = float('inf')    # 当前看到的最小、第二小

    for v in nums:
        # 更新最大值
        if v > max1:
            max2 = max1          # 原来的最大变成第二大
            max1 = v
        elif v > max2:          # 只比第二大大，不超过最大
            max2 = v

        # 更新最小值
        if v < min1:
            min2 = min1          # 原来的最小变成第二小
            min1 = v
        elif v < min2:          # 只比第二小小，不低于最小
            min2 = v

    # 计算乘积差
    return max1 * max2 - min1 * min2
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  只遍历一次数组，每个元素做常数次比较和赋值。对比暴力的 `n⁴`，速度提升了 **指数级**，即使 `n=10⁴` 也能在毫秒级完成。  
- **空间复杂度**：`O(1)`  
  只用了四个额外变量，不随 `n` 增长。

---

## 心得

- **核心技巧**：在只要求“最大/最小乘积”时，**只需要关注极值**（最大两个、最小两个），不必考虑全部组合。  
- **适用的题型**：  
  1. “Maximum Sum/Difference of Two Pairs” 类似题目（求两对数的和/差的最大值）。  
  2. “Largest/Smallest Product of K Numbers” 需要挑选 K 个极值的题目。  
  3. “Maximum Area of a Triangle” 这类只与极值有关的几何题。  
- **一句话总结**：**把“最大化”转化为“挑选极值”，用一次遍历即可得到答案。**

---

## 反思

- **第一反应**：看到“两个乘积的差”，立刻想到“把所有四个数都枚举”，这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记下标必须互不相同（在暴力实现时要格外注意）。  
  - 只取最大两个数却忽视了最小两个数的贡献，导致答案不完整。  
  - 当数组中出现负数时（本题不存在），极值的选取方式会改变，需要考虑负数的相乘会变成正数。  
- **下次遇到同类题**：第一步先**思考极值**——“如果要让结果最大（或最小），哪些数应该参与？” 然后再决定是排序还是一次遍历。