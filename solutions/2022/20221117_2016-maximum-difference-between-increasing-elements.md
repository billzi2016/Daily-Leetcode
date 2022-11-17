# #2016. 递增元素间的最大差值 / Maximum Difference Between Increasing Elements

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/maximum-difference-between-increasing-elements/)

---

## 题目（英文原版）

**Description**

Given a 0-indexed integer array nums of size n, find the maximum difference between nums[i] and nums[j] (i.e., nums[j] - nums[i]), such that 0 <= i < j < n and nums[i] < nums[j].
Return the maximum difference. If no such i and j exists, return -1.

**Examples**

**Example 1:**

```
Input: nums = [7,1,5,4]
Output: 4
Explanation:
The maximum difference occurs with i = 1 and j = 2, nums[j] - nums[i] = 5 - 1 = 4.
Note that with i = 1 and j = 0, the difference nums[j] - nums[i] = 7 - 1 = 6, but i > j, so it is not valid.
```

**Example 2:**

```
Input: nums = [9,4,3,2]
Output: -1
Explanation:
There is no i and j such that i < j and nums[i] < nums[j].
```

**Example 3:**

```
Input: nums = [1,5,2,10]
Output: 9
Explanation:
The maximum difference occurs with i = 0 and j = 3, nums[j] - nums[i] = 10 - 1 = 9.
```

**Constraints**

- n == nums.length
- 2 <= n <= 1000
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`（长度为 `n`），求满足 `0 <= i < j < n` 且 `nums[i] < nums[j]` 的下标对 `(i, j)` 中 `nums[j] - nums[i]` 的 **最大差值**。  
返回该最大差值；如果不存在满足条件的 `(i, j)`，返回 `-1`。

**示例**

```text
示例 1:
Input: nums = [7,1,5,4]
Output: 4
Explanation:
最大差值出现在 i = 1, j = 2 时，nums[j] - nums[i] = 5 - 1 = 4。
注意 i = 1, j = 0 时差值为 7 - 1 = 6，但 i > j，不符合要求。

示例 2:
Input: nums = [9,4,3,2]
Output: -1
Explanation:
不存在 i < j 且 nums[i] < nums[j] 的下标对。

示例 3:
Input: nums = [1,5,2,10]
Output: 9
Explanation:
最大差值出现在 i = 0, j = 3 时，nums[j] - nums[i] = 10 - 1 = 9。
```

**约束条件**

- `n == nums.length`
- `2 <= n <= 1000`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是把所有满足 `i < j` 的下标对枚举一遍，计算 `nums[j] - nums[i]`，只保留 **正数**（即 `nums[i] < nums[j]`）中的最大值。  

- **数据结构**：只需要一个普通的 Python 列表 `nums`，不需要额外的结构。  
- **生活化类比**：想象你在看一排排标号的盒子，每个盒子里放了一个数字。你要把左边的盒子（i）和右边的盒子（j）配对，找出“左边数字小、右边数字大”且差值最大的那对。就像在超市里挑选两件商品，左边的便宜，右边的贵，想让省的钱最多。  
- **为什么正确**：因为我们遍历了**所有**可能的 i、j 组合，只要有符合条件的组合，最大差值一定会在这些遍历的结果里出现。  

#### 代码（Python）

```python
def maximumDifference_bruteforce(nums):
    n = len(nums)
    max_diff = -1                     # 初始化答案为 -1，表示暂未找到合法的 i、j
    for i in range(n - 1):            # i 只能到倒数第二个，因为后面还要有 j
        for j in range(i + 1, n):     # j 必须在 i 右侧
            if nums[i] < nums[j]:     # 只关心左边数字更小的情况
                diff = nums[j] - nums[i]
                if diff > max_diff:   # 更新最大差值
                    max_diff = diff
    return max_diff
```

#### 复杂度  

- **时间复杂度**：`O(n²)`。  
  - 这里的 `n²` 可以想象成 **“把每个盒子都和后面的所有盒子配对一次”**，如果 `n = 1000`，大约要进行 1,000,000 次比较，算力上会明显慢下来。  
- **空间复杂度**：`O(1)`。只用了常数级别的额外变量 `max_diff`、`i`、`j`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**瓶颈**在于对每个 `i` 都要去遍历它右边的所有 `j`，导致二次循环。实际上我们只需要在遍历数组的过程中，**随时记住左侧出现的最小值**，因为：

- 对于当前位置 `j`，如果左侧出现过比 `nums[j]` 更小的数 `min_sofar`，那么 `nums[j] - min_sofar` 就是以 `j` 为结尾的合法差值的最大可能（因为更小的左侧数只能让差值更大）。  
- 只要我们在一次遍历中同步维护 `min_sofar`（即前缀最小值）和当前的最大差值 `ans`，就能在 **O(n)** 时间内得到答案。

**核心算法**：一次线性扫描 + 前缀最小值（Prefix Minimum）。

**类比**：把数组想象成一条河流从左往右流动，河里会出现不同高度的石头（数字）。我们每走一步，都记录下到目前为止遇到的**最低的石头**（最小值），然后看当前石头比那个最低石头高多少——这就是我们能得到的“最高的落差”。只要保持这两个变量，就不必回头再检查以前的石头。

#### 代码（Python）

```python
def maximumDifference(nums):
    """
    返回满足 i < j 且 nums[i] < nums[j] 的最大差值，
    若不存在则返回 -1。
    """
    # 前缀最小值初始化为第一个元素
    min_sofar = nums[0]
    ans = -1                         # 当前找到的最大差值，默认 -1 表示不存在合法对

    # 从第二个元素开始遍历，因为 j 必须大于 i
    for j in range(1, len(nums)):
        if nums[j] > min_sofar:      # 只在左侧出现更小值的情况下才可能产生正差
            diff = nums[j] - min_sofar
            if diff > ans:           # 更新全局最大差值
                ans = diff
        # 更新前缀最小值，确保后面的 j 能看到更小的左侧数
        if nums[j] < min_sofar:
            min_sofar = nums[j]

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`。只遍历了一遍数组，每个元素做了常数次的比较和赋值。相当于“只走了一趟河”，比起暴力的“每块石头都要回头再检查一次”快很多。  
- **空间复杂度**：`O(1)`。只用了两个额外变量 `min_sofar`、`ans`，不随 `n` 增长。

---

## 心得

- **核心技巧**：**前缀最小值**（或前缀最大值）配合一次遍历求最值差。  
- **适用题型**：  
  1. “最大利润”类问题（如买卖股票的最佳时机）。  
  2. “最大升序差”类问题（如找数组中递增子序列的最大跨度）。  
  3. “最小/最大前缀和”类问题（如子数组最大和的线性解法）。  
- **一句话总结**：**保持左侧最小值，实时计算右侧与之的差，即可在 O(n) 内得到最大递增差**。

---

## 反思

- **第一反应**：直接想把所有 i、j 配对枚举——这在面试里是最安全的起点，但会被面试官追问是否能优化。  
- **最容易踩的坑**：  
  - 忘记更新 `min_sofar`（如果当前元素更小），导致后面的差值计算基于一个已经不是最小的左侧值。  
  - 把 `ans` 初始值设成 `0` 而不是 `-1`，在全为递减的数组中会错误返回 `0`（其实应该返回 `-1` 表示不存在合法对）。  
- **下次思路**：遇到 “在 i < j 的前提下，比较两个位置的数值关系” 时，第一步就想到 **“维护前缀极值（最小或最大）”**，再在遍历中实时计算答案。这样往往能直接得到线性时间的最优解。