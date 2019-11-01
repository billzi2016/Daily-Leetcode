# #643. 最大平均子数组 I / Maximum Average Subarray I

> 难度：简单 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-average-subarray-i/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums consisting of n elements, and an integer k.
Find a contiguous subarray whose length is equal to k that has the maximum average value and return this value. Any answer with a calculation error less than 10-5 will be accepted.

**Examples**

**Example 1:**

```
Input: nums = [1,12,-5,-6,50,3], k = 4
Output: 12.75000
Explanation: Maximum average is (12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75
```

**Example 2:**

```
Input: nums = [5], k = 1
Output: 5.00000
```

**Constraints**

- n == nums.length
- 1 <= k <= n <= 105
- -104 <= nums[i] <= 104

---

## 题目（中文翻译）

给定一个整数数组 `nums`，其长度为 `n`，以及一个整数 `k`。  
找出长度恰好为 `k` 的连续子数组（subarray），使其平均值（average）最大，并返回该最大平均值。  
只要答案的计算误差小于 `10⁻⁵`，即视为正确。

**示例 1**  
输入: `nums = [1,12,-5,-6,50,3]`, `k = 4`  
输出: `12.75000`  
解释: 最大平均值为 `(12 - 5 - 6 + 50) / 4 = 51 / 4 = 12.75`

**示例 2**  
输入: `nums = [5]`, `k = 1`  
输出: `5.00000`

**约束条件**  
- `n == nums.length`  
- `1 <= k <= n <= 10⁵`  
- `-10⁴ <= nums[i] <= 10⁴`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有长度为 `k` 的连续子数组都枚举一遍，逐个算出它们的平均值，最后取最大值。  
- **枚举**：把数组看成一排座位，从左到右依次取出 `k` 张连续的座位（子数组）。  
- **求和**：把这 `k` 张座位上的数字加起来，就是子数组的 **和**。  
- **求平均**：把和除以 `k`，得到平均值。  
- **比较**：把每一次算出的平均值和当前已知的最大平均值比较，保留更大的那个。

这里用到的唯一数据结构是 **数组本身**，因为我们只需要顺序访问元素。  
这种做法之所以 **正确**，是因为题目要求的“所有长度为 `k` 的连续子数组”，我们没有遗漏任何一种可能，遍历完之后自然能得到最大值。

#### 代码（Python）

```python
from typing import List

def findMaxAverage_bruteforce(nums: List[int], k: int) -> float:
    n = len(nums)
    max_avg = float('-inf')          # 用一个很小的数先占位
    # 枚举所有起始位置 i，使得子数组 [i, i+k) 在数组范围内
    for i in range(n - k + 1):
        cur_sum = 0
        # 计算子数组 nums[i:i+k] 的和
        for j in range(i, i + k):
            cur_sum += nums[j]        # 累加每个元素
        cur_avg = cur_sum / k         # 求平均
        if cur_avg > max_avg:         # 更新最大平均值
            max_avg = cur_avg
    return max_avg
```

#### 复杂度

- **时间复杂度**：`O(n * k)`  
  解释：外层循环要跑 `n‑k+1` 次（约等于 `n` 次），每次内部还要遍历 `k` 个元素，所以总共大约是 `n × k` 次加法操作。  
  当 `n` 是 10⁵、`k` 也是 10⁵ 时，最坏会达到 10¹⁰ 次运算，显然太慢。

- **空间复杂度**：`O(1)`  
  只用了常数个额外变量（`max_avg、cur_sum、cur_avg`），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算子数组的和**。  
比如在窗口 `[i, i+k)` 与 `[i+1, i+1+k)` 之间，只相差最左边的一个元素 `nums[i]` 被踢出，最右边的一个元素 `nums[i+k]` 被加入。  
如果我们已经知道窗口 `[i, i+k)` 的和 `sum_i`，那么下一个窗口的和 `sum_{i+1}` 可以 **在 O(1) 时间内** 通过下面的公式得到：

```
sum_{i+1} = sum_i - nums[i] + nums[i+k]
```

这就是 **滑动窗口（Sliding Window）** 的核心思想：  
- **窗口**：长度固定为 `k` 的“滑动的子数组”。  
- **滑动**：每次向右移动一格，只更新进出窗口的两个元素的贡献，而不重新遍历整个窗口。

实现步骤：

1. 先算出第一个窗口 `[0, k)` 的和 `window_sum`。  
2. 用 `max_sum` 记录目前为止出现的最大窗口和（因为 `k` 固定，最大平均值对应最大和）。  
3. 从下标 `k` 开始遍历数组，每次把左侧即将离开的元素 `nums[i-k]` 减去，把右侧新进来的元素 `nums[i]` 加上，得到新的窗口和。  
4. 更新 `max_sum`。  
5. 最后返回 `max_sum / k` 即为最大平均值。

> **为什么可以只比较和而不是平均？**  
> 因为 `k` 是常数，对所有窗口都是一样的。比较 `sum1/k` 与 `sum2/k` 的大小，其实等价于比较 `sum1` 与 `sum2`，省去一次除法运算。

#### 代码（Python）

```python
from typing import List

def findMaxAverage(nums: List[int], k: int) -> float:
    # 1. 计算第一个长度为 k 的窗口和
    window_sum = sum(nums[:k])       # 直接使用 sum 内置函数
    max_sum = window_sum              # 当前最大窗口和

    # 2. 从第 k 个元素开始，逐个滑动窗口
    for i in range(k, len(nums)):
        # 把左边离开的元素减掉，把右边进来的元素加上
        window_sum += nums[i] - nums[i - k]
        # 更新最大和
        if window_sum > max_sum:
            max_sum = window_sum

    # 3. 最大平均值 = 最大和 / k
    return max_sum / k
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：只遍历数组一次（第一次算前 `k` 个数，之后每次只做常数次加减），所以运算次数与数组长度 `n` 成线性关系。相比暴力的 `O(n·k)`，提升巨大。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量 `window_sum、max_sum`，不随 `n` 增长。

---

## 心得

- **核心技巧**：滑动窗口（Sliding Window）——在固定长度的子数组之间“滑动”，利用前一次的结果快速得到下一次的结果。  
- **适用的题型**：  
  1. “最大/最小子数组和”（如 LeetCode 53 Maximum Subarray，变形为固定长度）  
  2. “子数组满足某种条件的最短/最长长度”（如 LeetCode 209 最小覆盖子串）  
  3. “固定窗口统计”（如求窗口内最大值、最小值、出现次数等）  
- **一句话总结**：**把重复计算的部分“记下来”，每次只更新改变的那一点，就是滑动窗口的钥匙。**

---

## 反思

- **第一反应**：直接想到遍历所有长度为 `k` 的子数组并逐个求和，没考虑到可以复用前一次的计算。  
- **最容易踩的坑**：  
  - **边界**：当 `k = n` 时，只会有一个窗口，代码仍需正常工作。  
  - **负数**：数组里可能全是负数，初始化 `max_sum` 时不能用 `0`（会误判），应该用第一个窗口的和或 `-inf`。  
  - **整数溢出**：在 Python 中整数自动大数化，但在其他语言需要注意使用 64 位整数。  
- **下次类似题的第一步**：先判断是否可以用**固定长度滑动窗口**，如果可以，就把“先算第一个窗口”，再**增量更新**，而不是每次全遍历。