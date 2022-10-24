# #1984. K 名学生成绩的最高分与最低分的最小差值 / Minimum Difference Between Highest and Lowest of K Scores

> 难度：简单 · 标签：Array、Sliding Window、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums, where nums[i] represents the score of the ith student. You are also given an integer k.
Pick the scores of any k students from the array so that the difference between the highest and the lowest of the k scores is minimized.
Return the minimum possible difference.

**Examples**

**Example 1:**

```
Input: nums = [90], k = 1
Output: 0
Explanation: There is one way to pick score(s) of one student:
- [90]. The difference between the highest and lowest score is 90 - 90 = 0.
The minimum possible difference is 0.
```

**Example 2:**

```
Input: nums = [9,4,1,7], k = 2
Output: 2
Explanation: There are six ways to pick score(s) of two students:
- [9,4,1,7]. The difference between the highest and lowest score is 9 - 4 = 5.
- [9,4,1,7]. The difference between the highest and lowest score is 9 - 1 = 8.
- [9,4,1,7]. The difference between the highest and lowest score is 9 - 7 = 2.
- [9,4,1,7]. The difference between the highest and lowest score is 4 - 1 = 3.
- [9,4,1,7]. The difference between the highest and lowest score is 7 - 4 = 3.
- [9,4,1,7]. The difference between the highest and lowest score is 7 - 1 = 6.
The minimum possible difference is 2.
```

**Constraints**

- 1 <= k <= nums.length <= 1000
- 0 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个 **0 索引** 的整数数组 `nums`，其中 `nums[i]` 表示第 `i` 位学生的成绩。再给定一个整数 `k`。  
从数组中挑选任意 `k` 名学生的成绩，使这 `k` 个成绩中的最高分与最低分的差值 **最小化**。  
返回可能的最小差值。

**示例 1**  
```
Input: nums = [90], k = 1
Output: 0
Explanation: 只有一种选取方式，即选取唯一的学生成绩 [90]。最高分与最低分的差值为 90 - 90 = 0。最小可能的差值为 0。
```

**示例 2**  
```
Input: nums = [9,4,1,7], k = 2
Output: 2
Explanation: 选取两名学生的方式共有 6 种，分别计算最高分与最低分的差值如下：
- 选取 [9,4]，差值为 9 - 4 = 5。
- 选取 [9,1]，差值为 9 - 1 = 8。
- 选取 [9,7]，差值为 9 - 7 = 2。
- 选取 [4,1]，差值为 4 - 1 = 3。
- 选取 [4,7]，差值为 7 - 4 = 3。
- 选取 [1,7]，差值为 7 - 1 = 6。
其中最小的差值为 2。
```

**约束条件**
- `1 <= k <= nums.length <= 1000`
- `0 <= nums[i] <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 可能的 `k` 名学生组合列举出来，逐个计算它们的最高分和最低分之差，最后取最小值。  

- **组合**：可以把它想成在超市里挑 `k` 件商品的所有挑法，挑完后再看看这 `k` 件商品的价格跨度有多大。  
- **数据结构**：这里主要用到 **列表（list）** 来保存当前挑的 `k` 个分数，用 **循环** 来遍历所有可能的挑法。  

为什么这个方法一定能得到正确答案？因为我们把**所有**合法的挑选方式都检查了一遍，最小的差值必然在其中。  

不过，这种“全部尝试”会非常慢。设数组长度为 `n`，挑 `k` 个的组合数是 `C(n, k)`（即 “从 n 里挑 k”，数学上叫**组合数**），它会随着 `n` 的增大而指数级爆炸。  

#### 代码（Python）

```python
from itertools import combinations   # itertools 就像一个“组合工具箱”

def minimum_difference_bruteforce(nums, k):
    """
    暴力枚举所有长度为 k 的子集合，返回最小的最高分-最低分
    """
    min_diff = float('inf')               # 先设一个很大的初始值
    for combo in combinations(nums, k):   # 逐个取出所有 k 元组
        cur_diff = max(combo) - min(combo)   # 最高分减最低分
        if cur_diff < min_diff:               # 找到更小的就更新
            min_diff = cur_diff
    return min_diff
```

#### 复杂度  

- **时间复杂度**：`O(C(n, k) * k)`  
  - `C(n, k)` 表示组合的数量，等价于 `n! / (k! * (n-k)!)`，随 `n` 增长非常快。  
  - 对每个组合我们还要遍历 `k` 次来求最大最小，所以再乘以 `k`。  
  - 用大白话说，就是“随人数增加，时间会呈指数级增长”。  

- **空间复杂度**：`O(k)`  
  - 只需要保存当前遍历到的 `k` 个分数（`combo`），因此最多占用 `k` 个位置的空间。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈**在于我们不断地在全局范围里寻找 `k` 个分数，而每一次都要重新算最大最小。  
其实，如果把所有分数从小到大排好序，**相邻的 `k` 个数** 必然是“最靠近”的 `k` 个数。原因如下：

1. 排序后，数列是单调递增的。  
2. 设我们挑了 `k` 个数，它们的最小值是 `a`，最大值是 `b`。  
3. 在排好序的数组里，`a` 与 `b` 之间的所有数都会出现在它们之间的**连续片段**里。  
4. 因此，只要检查每一个长度为 `k` 的**连续窗口**（滑动窗口），计算窗口首尾的差值 `nums[i+k-1] - nums[i]`，最小的那个就是答案。

这就把“组合枚举”转化为“滑动窗口”，把时间从指数级降到了线性级（加一次排序的开销）。  

核心概念：  

- **排序（Sorting）**：把数组从小到大排列，就像把学生成绩从低到高排好座位，方便一次性比较相邻的成绩。Python 的 `list.sort()` 底层使用的是 **Timsort**，时间复杂度是 `O(n log n)`。  
- **滑动窗口（Sliding Window）**：想象有一个长度为 `k` 的尺子，左端从数组最左侧开始，每次向右移动一格，尺子覆盖的 `k` 个数就是当前的候选集合。  

#### 代码（Python）

```python
def minimum_difference(nums, k):
    """
    先排序，然后用滑动窗口遍历所有长度为 k 的连续子数组，
    返回窗口首尾差值的最小值。
    """
    nums.sort()                     # O(n log n) 的排序
    min_diff = float('inf')         # 初始设为无限大

    # i 为窗口左端的索引，右端自然是 i + k - 1
    for i in range(len(nums) - k + 1):
        cur_diff = nums[i + k - 1] - nums[i]   # 只需比较窗口首尾
        if cur_diff < min_diff:                # 更新最小差值
            min_diff = cur_diff

    return min_diff
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`，遍历窗口是 `O(n)`，二者相加仍然是 `O(n log n)`。  
  - 用大白话说，就是“先花点时间把成绩排好序，然后再线性扫描一次”。  

- **空间复杂度**：`O(1)`（不计排序的原地改动）  
  - 只使用了常数级别的额外变量 `min_diff`、`i` 等。若使用 Python 的原地排序 `list.sort()`，不需要额外的数组空间。  

---

## 心得  

- **核心技巧**：先排序，再用滑动窗口在有序数组中找最小差值。  
- **适用的题型**  
  1. “最小化最大值与最小值差”类题目（如 LeetCode 1984、1433 等）。  
  2. “在有序序列中找长度为 k 的子数组满足某种最值条件” （如滑动窗口求子数组和、最长子串等）。  
- **一句话总结**：**先把乱序的东西排好序，连续窗口就能一次遍历得到最优解。**  

---

## 反思  

- **第一反应**：看到“挑 k 名学生”，马上想到“组合”，于是想到暴力枚举。  
- **最容易踩的坑**  
  - 忘记先排序导致窗口不是“最靠近”的 `k` 个数，结果会错误。  
  - 边界条件：`k = 1` 时差值应为 `0`，循环 `range(len(nums) - k + 1)` 必须写对，否则会出现负数范围。  
- **下次类似题的第一步**：先问自己“如果把数据排好序，问题会不会变得简单？”——如果答案是肯定的，立刻考虑**排序 + 滑动窗口**的套路。