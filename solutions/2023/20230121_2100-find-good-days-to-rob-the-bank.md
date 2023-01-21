# #2100. 寻找适合抢劫银行的好日子 / Find Good Days to Rob the Bank

> 难度：中等 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-good-days-to-rob-the-bank/)

---

## 题目（英文原版）

**Description**

You and a gang of thieves are planning on robbing a bank. You are given a 0-indexed integer array security, where security[i] is the number of guards on duty on the ith day. The days are numbered starting from 0. You are also given an integer time.
The ith day is a good day to rob the bank if:
More formally, this means day i is a good day to rob the bank if and only if security[i - time] >= security[i - time + 1] >= ... >= security[i] <= ... <= security[i + time - 1] <= security[i + time].
Return a list of all days (0-indexed) that are good days to rob the bank. The order that the days are returned in does not matter.

**Examples**

**Example 1:**

```
Input: security = [5,3,3,3,5,6,2], time = 2
Output: [2,3]
Explanation:
On day 2, we have security[0] >= security[1] >= security[2] <= security[3] <= security[4].
On day 3, we have security[1] >= security[2] >= security[3] <= security[4] <= security[5].
No other days satisfy this condition, so days 2 and 3 are the only good days to rob the bank.
```

**Example 2:**

```
Input: security = [1,1,1,1,1], time = 0
Output: [0,1,2,3,4]
Explanation:
Since time equals 0, every day is a good day to rob the bank, so return every day.
```

**Example 3:**

```
Input: security = [1,2,3,4,5,6], time = 2
Output: []
Explanation:
No day has 2 days before it that have a non-increasing number of guards.
Thus, no day is a good day to rob the bank, so return an empty list.
```

**Constraints**

- 1 <= security.length <= 105
- 0 <= security[i], time <= 105

---

## 题目（中文翻译）

**题目描述**

你和一帮盗贼计划抢劫银行。给定一个下标从 0 开始的整数数组（`security`），其中 `security[i]` 表示第 `i` 天值班的警卫人数。天数也从 0 开始编号。同时给定一个整数 `time`。

第 `i` 天是一个**适合抢劫银行的好日子**，当且仅当满足以下条件：

```
security[i - time] >= security[i - time + 1] >= ... >= security[i] <= ... <= security[i + time - 1] <= security[i + time]
```

也即，`i` 前 `time` 天的警卫人数是**非递增**的，而 `i` 后 `time` 天的警卫人数是**非递减**的。

返回所有适合抢劫银行的好日子的下标（0 索引），返回顺序不限。

**示例**

> 示例 1  
> 输入: `security = [5,3,3,3,5,6,2]`, `time = 2`  
> 输出: `[2,3]`  
> 解释:  
> - 在第 2 天，满足 `security[0] >= security[1] >= security[2] <= security[3] <= security[4]`。  
> - 在第 3 天，满足 `security[1] >= security[2] >= security[3] <= security[4] <= security[5]`。  
> 其余天数均不满足条件，因此只有第 2 天和第 3 天是好日子。

> 示例 2  
> 输入: `security = [1,1,1,1,1]`, `time = 0`  
> 输出: `[0,1,2,3,4]`  
> 解释:  
> 当 `time` 为 0 时，所有天数都满足条件，所以返回所有下标。

> 示例 3  
> 输入: `security = [1,2,3,4,5,6]`, `time = 2`  
> 输出: `[]`  
> 解释:  
> 没有任何一天的前 2 天警卫人数呈非递增，因此不存在好日子，返回空列表。

**约束条件**

- `1 <= security.length <= 10^5`
- `0 <= security[i], time <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法就是：**把每一天都当作“候选”，逐个检查它左右各 `time` 天的 guard 数量是否满足题目要求**。  

- **检查方式**：  
  1. 向左看 `time` 天，判断 `security[i-time] >= security[i-time+1] >= … >= security[i]`。  
  2. 向右看 `time` 天，判断 `security[i] <= security[i+1] <= … <= security[i+time]`。  
- **用到的数据结构**：只需要原数组 `security`，不需要额外的数据结构。可以把它想象成一本**日记本**，我们把手指从左往右一点点翻页，检查相邻两页的 guard 数是否满足“递减”或“递增”。  
- **为什么正确**：因为题目本身就是要检查这两个序列是否满足单调性，只要全部检查完就没有遗漏。  

**时间复杂度**：  
- 对每个下标 `i`（最多 `n` 次），我们要检查左边 `time` 天和右边 `time` 天，**最坏情况**是 `2 * time` 次比较。  
- 所以总体是 `O(n * time)`。如果 `time` 和 `n` 同级（比如都是 10⁵），这个复杂度会变成 `10¹⁰`，在实际运行中会超时。  
- 大白话：**把每件事都重新算一遍**，没有利用已经算过的结果，等于“重复搬砖”。  

**空间复杂度**：只用了常数级别的临时变量，`O(1)`。  

#### 代码（Python）  
```python
from typing import List

def goodDaysToRobBank_bruteforce(security: List[int], time: int) -> List[int]:
    n = len(security)
    ans = []

    # 把每一天都当作候选 i
    for i in range(n):
        # 如果左边或右边的天数不够，直接跳过
        if i - time < 0 or i + time >= n:
            continue

        # 检查左侧：从 i-time 到 i 是否是非递增的
        left_ok = True
        for j in range(i - time, i):
            if security[j] < security[j + 1]:   # 破坏了递减
                left_ok = False
                break

        # 检查右侧：从 i 到 i+time 是否是非递增的（即非递减）
        right_ok = True
        for j in range(i, i + time):
            if security[j] > security[j + 1]:   # 破坏了递增
                right_ok = False
                break

        if left_ok and right_ok:
            ans.append(i)

    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n * time)`  
  - 这里的 `n` 是天数，`time` 是需要检查的左右天数。  
  - 当 `time` 很大时，这个乘积会非常大，实际运行会慢。  
- **空间复杂度**：`O(1)`（不计返回结果的空间）  
  - 只用了几个临时变量，额外占用的内存几乎可以忽略不计。  

---  

### 2. 最优解  

#### 思路  
从暴力解我们可以看到**重复计算**是瓶颈所在。  
- 左侧的 “非递增天数” 可以提前算好，右侧的 “非递减天数” 同理。  
- 具体做法：  
  1. **左数组** `left[i]` 表示 **在第 `i` 天之前，连续满足 `security[k-1] >= security[k]` 的天数**（不包括第 `i` 天本身）。换句话说，`left[i]` 是从 `i` 往左数，能连续往左走多少天仍然保持非递增。  
  2. **右数组** `right[i]` 表示 **在第 `i` 天之后，连续满足 `security[k] <= security[k+1]` 的天数**（不包括第 `i` 天本身）。即从 `i` 往右走多少天仍然保持非递减。  
- 这两个数组只需要 **一次线性遍历** 就能得到，类似于**前缀和**的思想，只是这里记录的是“连续满足条件的长度”。  

**构造左数组**（从左往右）  
```
left[0] = 0                         # 第 0 天左边没有天
for i in range(1, n):
    if security[i-1] >= security[i]:
        left[i] = left[i-1] + 1    # 前一天已经满足，继续累计
    else:
        left[i] = 0                # 断了，重新计数
```

**构造右数组**（从右往左）  
```
right[n-1] = 0                     # 最后一天右边没有天
for i in range(n-2, -1, -1):
    if security[i] <= security[i+1]:
        right[i] = right[i+1] + 1
    else:
        right[i] = 0
```

**判断好日子**  
- 对每个下标 `i`，只要 `left[i] >= time` 且 `right[i] >= time`，说明左边至少有 `time` 天连续非递增，右边至少有 `time` 天连续非递减，**即满足题目要求**。  

**为什么是 O(n)**：  
- 两次线性遍历分别得到 `left`、`right`，每次遍历都是 `O(n)`。  
- 最后一次遍历检查每个 `i` 是否满足条件，也是 `O(n)`。  
- 整体时间是 `O(3n) = O(n)`，没有乘以 `time`，大幅提升效率。  

**空间**：我们用了两个长度为 `n` 的额外数组，**`O(n)`** 的空间。如果想进一步压缩，可以只保留一个数组或在原数组上做标记，但 `O(n)` 已经足够满足题目限制（`n ≤ 10⁵`）。  

#### 代码（Python）  
```python
from typing import List

def goodDaysToRobBank(security: List[int], time: int) -> List[int]:
    n = len(security)
    if time == 0:                     # time 为 0 时所有天都是好日子，直接返回
        return list(range(n))

    # left[i] = 连续满足 security[k-1] >= security[k] 的天数，k 从 i-time 到 i
    left = [0] * n
    for i in range(1, n):
        if security[i - 1] >= security[i]:
            left[i] = left[i - 1] + 1
        else:
            left[i] = 0                # 断了，重新计数

    # right[i] = 连续满足 security[k] <= security[k+1] 的天数，k 从 i 到 i+time
    right = [0] * n
    for i in range(n - 2, -1, -1):
        if security[i] <= security[i + 1]:
            right[i] = right[i + 1] + 1
        else:
            right[i] = 0

    # 收集满足 left[i] >= time 且 right[i] >= time 的下标
    ans = [i for i in range(n) if left[i] >= time and right[i] >= time]
    return ans
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 只需要三次线性遍历（两次预处理 + 一次结果筛选），即使 `n = 10⁵` 也能在毫秒级完成。  
  - 与暴力解相比，省去了每次检查 `time` 天的重复比较，**把 “每次都重新搬砖” 变成了 “一次搬完所有砖”**。  
- **空间复杂度**：`O(n)`  
  - 两个额外数组 `left`、`right` 各占 `n` 个整数的空间。  
  - 对于本题的规模，这属于合理的线性空间。  

---  

## 心得  

- **核心技巧**：**前缀计数（前缀递增/递减长度）**，即在一次遍历中累计满足单调性的连续天数。  
- **适用的题型**：  
  1. “连续子数组满足单调/相等条件” 类似题，如 LeetCode 2289 *Steps to Make Array Non-decreasing*。  
  2. “左右两侧满足某种约束” 的滑动窗口/前缀计数题，例如 2398 *Maximum Number of Robots Within Budget*（需要左右累计费用）。  
  3. “子数组最长递增/递减” 的变形，如 300 *Longest Increasing Subsequence* 的 DP 优化版。  
- **一句话总结**：**把“每次都重新检查”改成“先把每天的连续满足长度算好”，再直接比较即可**。  

---  

## 反思  

- **第一反应**：看到左右各 `time` 天的条件，马上想到双层循环逐个检查，没意识到会有大量重复比较。  
- **最容易踩的坑**：  
  - **边界条件**：当 `i - time < 0` 或 `i + time >= n` 时直接不满足，需要提前过滤。  
  - **time = 0**：此时题目说所有天都是好日子，若忘记特判会导致 `left[i] >= 0` 与 `right[i] >= 0` 永远为真，但仍需返回完整的下标列表。  
  - **整数溢出**：本题数值范围不大，但在其他语言实现时要注意 `left/right` 计数可能超过 `int` 范围。  
- **下次类似题的第一步**：**先问自己“有没有可以一次遍历就把需要的状态预先算好？”**（前缀和、前缀计数、滑动窗口累计等），把重复工作转化为一次性统计。