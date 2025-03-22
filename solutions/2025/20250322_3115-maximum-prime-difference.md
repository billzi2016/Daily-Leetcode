# #3115. 最大质数差 / Maximum Prime Difference

> 难度：中等 · 标签：Array、Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/maximum-prime-difference/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Return an integer that is the maximum distance between the indices of two (not necessarily different) prime numbers in nums.

**Examples**

**Example 1:**

```
Input: nums = [4,2,9,5,3]
Output: 3
Explanation: nums[1] , nums[3] , and nums[4] are prime. So the answer is |4 - 1| = 3 .
```

**Example 2:**

```
Input: nums = [4,8,2,8]
Output: 0
Explanation: nums[2] is prime. Because there is just one prime number, the answer is |2 - 2| = 0 .
```

**Constraints**

- 1 <= nums.length <= 3 * 105
- 1 <= nums[i] <= 100
- The input is generated such that the number of prime numbers in the nums is at least one.

---

## 题目（中文翻译）

给定一个整数数组 `nums`。返回一个整数，表示 `nums` 中两个（不一定不同的）质数（prime）所在下标之间的最大距离。

**示例 1**  
输入：`nums = [4,2,9,5,3]`  
输出：`3`  
解释：`nums[1]`、`nums[3]` 和 `nums[4]` 为质数。因此答案为 `|4 - 1| = 3`。

**示例 2**  
输入：`nums = [4,8,2,8]`  
输出：`0`  
解释：`nums[2]` 为质数。因为只有一个质数，答案为 `|2 - 2| = 0`。

**约束条件**  
- `1 <= nums.length <= 3 * 10^5`  
- `1 <= nums[i] <= 100`  
- 输入保证 `nums` 中至少存在一个质数（prime）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把数组里所有是质数的下标全部找出来，然后**两两比较**它们之间的距离，取最大的那个。  
- **质数判断**：把每个元素 `nums[i]` 当成一个数，判断它是不是只能被 1 和它本身整除的“素数”。这一步可以把「质数」想象成「只能用唯一钥匙打开的锁」——如果钥匙（除数）只有 1 和它自己，就算是质数。  
- **数据结构**：我们用一个普通的列表 `prime_idx` 来保存所有质数出现的下标，类似把所有“钥匙位置”记在一本小册子里。  
- **遍历所有配对**：对 `prime_idx` 中的每一对下标 `(i, j)`（`i ≤ j`），计算 `|j - i|`，记录最大值。  

因为我们要检查 **每一对** 质数下标，所以这个方法一定能得到正确答案，只是会比较慢。

#### 代码（Python）

```python
def is_prime(x: int) -> bool:
    """判断 x 是否为质数（1 ≤ x ≤ 100）"""
    if x < 2:
        return False
    # 只需要检查到 sqrt(x) 即可，像是把锁的钥匙从小到大尝试
    i = 2
    while i * i <= x:
        if x % i == 0:
            return False
        i += 1
    return True


def maximumPrimeDifference_bruteforce(nums):
    # 1. 收集所有质数的下标
    prime_idx = []
    for idx, val in enumerate(nums):
        if is_prime(val):
            prime_idx.append(idx)          # 记录质数出现的位置

    # 2. 两两比较，找最大距离
    max_dist = 0
    n = len(prime_idx)
    for i in range(n):
        for j in range(i, n):
            dist = abs(prime_idx[j] - prime_idx[i])
            if dist > max_dist:
                max_dist = dist
    return max_dist
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - `n` 为质数下标的个数（最坏情况下等于数组长度）。我们要遍历所有的 `(i, j)` 配对，类似“每个人和所有其他人握手”，所以是二次方的工作量。  
- **空间复杂度**：`O(k)`（`k` 为质数的个数）  
  - 需要额外的列表保存所有质数下标，最多占用和原数组一样多的空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定答案的只有最左边的质数下标和最右边的质数下标**。  
- 为什么？因为距离是下标之差的绝对值，若我们已经找到了最左（最小下标）和最右（最大下标）的两个质数，它们之间的距离自然是最大的。任何其他两点之间的距离都不可能超过这两个极端点之间的距离。  
- 因此，我们只需要 **一次遍历**，记录出现的第一个质数下标 `first` 和最后一个质数下标 `last`，答案就是 `last - first`（若只出现一次质数，`first == last`，答案为 0）。

**质数的判断** 仍然需要，但因为 `nums[i] ≤ 100`，我们可以一次性用 **埃拉托斯特尼筛法（Sieve of Eratosthenes）** 预计算出 1~100 的所有质数，这相当于提前把“所有可以打开的锁的钥匙”写在一本字典里，查询时只需要 O(1) 时间。

#### 代码（Python）

```python
def sieve(limit: int) -> set:
    """返回 ≤ limit 的所有质数集合，使用埃拉托斯特尼筛法"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    p = 2
    while p * p <= limit:
        if is_prime[p]:
            # 把 p 的所有倍数都标记为非质数
            for multiple in range(p * p, limit + 1, p):
                is_prime[multiple] = False
        p += 1
    return {i for i, val in enumerate(is_prime) if val}


def maximumPrimeDifference(nums):
    # 1. 预计算 1~100 的质数集合（常数时间查询）
    prime_set = sieve(100)

    first = None   # 最左侧质数的下标
    last = None    # 最右侧质数的下标

    # 2. 一次遍历数组，更新 first / last
    for idx, val in enumerate(nums):
        if val in prime_set:          # O(1) 判断是否为质数
            if first is None:         # 第一次遇到质数
                first = idx
            last = idx                # 每次遇到质数都更新为最新的下标

    # 根据题意，至少会出现一次质数
    return last - first   # 若只出现一次，first == last，返回 0
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只需要一次线性遍历数组（`n = len(nums)`），每次检查是否为质数是 O(1) 的集合查询。相比暴力的二次方，这就像“只走一次路，直接从左端走到右端”。  
- **空间复杂度**：`O(1)`（不计输入输出）  
  - 只使用了常数级别的额外空间：一个长度为 101 的布尔数组（或质数集合）以及两个整数变量 `first`、`last`。不随 `n` 增长。

---

## 心得

- **核心技巧**：利用**极值**（最左/最右）来简化“最大距离”这类问题。  
- **适用的题型**  
  1. “数组中最大相同元素的距离”  
  2. “找出数组中满足某条件的最早和最晚出现位置”  
  3. “最大子数组长度（满足某种属性）”  
- **解题钥匙**：**先找极端点**，而不是枚举所有组合。

## 反思

- **第一反应**：看到“最大距离”，本能地想到两两比较（暴力）。  
- **最容易踩的坑**  
  - **质数判断的效率**：若每次都用 O(√x) 的检查，在极端数据（如 3×10⁵ 个 100）下仍可接受，但如果上限更大就会超时。  
  - **边界情况**：只有一个质数时，需要返回 `0`，不能忘记 `first == last` 的处理。  
- **下次遇到同类题**：第一步先思考“答案是否只依赖于最左和最右的满足条件的元素”，如果是，就直接记录极值，避免不必要的枚举。