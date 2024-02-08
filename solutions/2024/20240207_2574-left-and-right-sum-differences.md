# #2574. 左右和差 / Left and Right Sum Differences

> 难度：简单 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/left-and-right-sum-differences/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums of size n.
Define two arrays leftSum and rightSum where:
Return an integer array answer of size n where answer[i] = |leftSum[i] - rightSum[i]|.

**Examples**

**Example 1:**

```
Input: nums = [10,4,8,3]
Output: [15,1,11,22]
Explanation: The array leftSum is [0,10,14,22] and the array rightSum is [15,11,3,0].
The array answer is [|0 - 15|,|10 - 11|,|14 - 3|,|22 - 0|] = [15,1,11,22].
```

**Example 2:**

```
Input: nums = [1]
Output: [0]
Explanation: The array leftSum is [0] and the array rightSum is [0].
The array answer is [|0 - 0|] = [0].
```

**Constraints**

- 1 <= nums.length <= 1000
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `nums`，长度为 `n`。  
定义两个数组 `leftSum` 和 `rightSum`，其中  

- `leftSum[i]` 为下标 `i` 左侧所有元素之和（不包括 `nums[i]`），即 `leftSum[i] = Σ_{j < i} nums[j]`；  
- `rightSum[i]` 为下标 `i` 右侧所有元素之和（不包括 `nums[i]`），即 `rightSum[i] = Σ_{j > i} nums[j]`。  

返回一个长度为 `n` 的整数数组 `answer`，其中 `answer[i] = |leftSum[i] - rightSum[i]|`（`|·|` 表示绝对值）。

**示例**  

*示例 1*  
```
输入: nums = [10,4,8,3]
输出: [15,1,11,22]
解释: leftSum 为 [0,10,14,22]，rightSum 为 [15,11,3,0]。  
answer 为 [|0 - 15|, |10 - 11|, |14 - 3|, |22 - 0|] = [15,1,11,22]。
```

*示例 2*  
```
输入: nums = [1]
输出: [0]
解释: leftSum 为 [0]，rightSum 为 [0]。  
answer 为 [|0 - 0|] = [0]。
```

**约束条件**  

- `1 <= nums.length <= 1000`  
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个位置左边的数全部加起来得到 leftSum，右边的数全部加起来得到 rightSum**，再取两者的绝对差。  
- **使用的结构**：普通的 Python 列表 `list`，以及两个临时变量 `left_sum`、`right_sum`。  
- **生活化类比**：把数组想成一排排装满糖果的盒子，想知道第 `i` 盒子左边所有糖果的总重量和右边的总重量，只需要把左边盒子里的糖果一个一个搬出来称重，右边同理。  
- **为什么正确**：因为题目要求的 `leftSum[i]` 就是下标 `< i` 的所有元素之和，`rightSum[i]` 是下标 `> i` 的所有元素之和，暴力遍历恰好把这些元素都加进来了。  

**时间/空间复杂度**  
- 对每个 `i`（共 `n` 次），我们都要遍历左侧 `i` 个元素和右侧 `n‑i‑1` 个元素，最坏情况是 `i ≈ n/2`，于是一次循环的工作量是 `O(n)`，总共 `n` 次循环 → **时间复杂度 `O(n²)`**。  
  - 大白话：如果数组有 1000 个数，暴力解大概要做 1000 × 1000 = 1,000,000 次加法，明显有点慢。  
- 只用了常数个额外变量（不随 `n` 增长），**空间复杂度 `O(1)`**。  

#### 代码（Python）

```python
from typing import List

def left_right_diff_brute(nums: List[int]) -> List[int]:
    n = len(nums)
    answer = [0] * n                     # 用来存放最终结果

    for i in range(n):                   # 枚举每个位置 i
        left_sum = 0
        right_sum = 0

        # 累加 i 左侧所有元素 → left_sum
        for j in range(i):               # j 从 0 到 i-1
            left_sum += nums[j]          # 把左边的每个数加进来

        # 累加 i 右侧所有元素 → right_sum
        for j in range(i + 1, n):        # j 从 i+1 到 n-1
            right_sum += nums[j]         # 把右边的每个数加进来

        # 取绝对差并写入 answer
        answer[i] = abs(left_sum - right_sum)

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 每个下标都要再遍历一次数组，等价于“把数组的每个元素都加了 `n` 次”。  
- **空间复杂度**：`O(1)` — 只用了几个计数器，和数组长度无关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要重新遍历左侧和右侧**。  
如果我们事先把 **前缀和（prefix sum）** 算好，就可以 **在 O(1) 时间内得到任意区间的和**，从而把整体时间降到线性。

**前缀和是什么？**  
想象把数组的每个元素依次放进一个大盒子里，每放进一个元素，就把盒子里已有的重量记下来——这就是前缀和数组 `pre[i]`，表示 `nums[0] + nums[1] + … + nums[i‑1]`（注意下标差一个，方便计算）。  
有了前缀和：

- 左侧和 `leftSum[i] = pre[i]`（因为它正好是前 i 个数的总和）。  
- 右侧和 `rightSum[i] = total - pre[i+1]`，其中 `total` 是所有元素的总和，`pre[i+1]` 包含了下标 `i` 本身，所以把它减掉后剩下的就是右边的和。

**步骤**  
1. **一次遍历**算出 `total`（所有元素的和）。  
2. 再一次遍历，同时维护一个变量 `cur_pre`（当前前缀和）。  
   - `left = cur_pre`（左侧和）  
   - `right = total - cur_pre - nums[i]`（右侧和）  
   - 把 `abs(left - right)` 放进答案数组。  
   - 最后 `cur_pre += nums[i]`，为下一个位置准备前缀和。  

**核心算法**：前缀和 + 一次遍历。  

#### 代码（Python）

```python
from typing import List

def left_right_diff_opt(nums: List[int]) -> List[int]:
    n = len(nums)
    total = sum(nums)          # 所有元素的总和，O(n) 一次遍历得到
    answer = [0] * n

    cur_pre = 0                # 当前的前缀和（不包括当前位置 i）

    for i in range(n):
        left = cur_pre                         # 左侧和 = 已经累加的前缀和
        right = total - cur_pre - nums[i]      # 右侧和 = 总和 - 左侧和 - 当前元素

        answer[i] = abs(left - right)          # 绝对差

        cur_pre += nums[i]                      # 更新前缀和，为下一个 i 做准备

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历了两遍（一次求 `total`，一次算答案），相当于“每个元素只被看一次”。  
  - 与暴力解相比，从 `n²` 降到了 `n`，当 `n` 达到上限 1000 时，运算次数从 1,000,000 降到约 2,000，快了几个数量级。  
- **空间复杂度**：`O(1)` — 除了返回的答案数组（题目必须的），额外只用了常数个变量。

---

## 心得

- **核心技巧**：前缀和（Prefix Sum）。  
- **适用的题型**：  
  1. 求区间和或区间差的题目（如 “子数组和”等）。  
  2. 需要快速统计左/右累计信息的题目（如 “左侧最大乘积”）。  
- **解题钥匙**：把“每次都重新统计”转化为“一次预处理后直接读取”。  

---

## 反思

- **第一反应**：直接写两个循环求左、右和——这是最自然的暴力思路。  
- **最容易踩的坑**：  
  - 忘记把当前位置的元素从右侧和中剔除，导致右侧和比实际多一个 `nums[i]`。  
  - 边界情况 `i = 0` 或 `i = n‑1` 时，左侧或右侧应为 0，代码要保证不会出现负索引或遗漏。  
- **下次遇到同类题**：第一步先思考“能否用一次遍历把累计信息保存下来”，如果答案是“可以”，那么就尝试构造前缀和或后缀和。