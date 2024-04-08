# #2644. 寻找最大可整除得分 / Find the Maximum Divisibility Score

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/find-the-maximum-divisibility-score/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums and divisors.
The divisibility score of divisors[i] is the number of indices j such that nums[j] is divisible by divisors[i].
Return the integer divisors[i] with the maximum divisibility score. If multiple integers have the maximum score, return the smallest one.

**Examples**

**Example 1:**

```
Input: nums = [2,9,15,50], divisors = [5,3,7,2]
Output: 2
Explanation:
The divisibility score of divisors[0] is 2 since nums[2] and nums[3] are divisible by 5.
The divisibility score of divisors[1] is 2 since nums[1] and nums[2] are divisible by 3.
The divisibility score of divisors[2] is 0 since none of the numbers in nums is divisible by 7.
The divisibility score of divisors[3] is 2 since nums[0] and nums[3] are divisible by 2.
As divisors[0] , divisors[1] , and divisors[3] have the same divisibility score, we return the smaller one which is divisors[3] .
```

**Example 2:**

```
Input: nums = [4,7,9,3,9], divisors = [5,2,3]
Output: 3
Explanation:
The divisibility score of divisors[0] is 0 since none of numbers in nums is divisible by 5.
The divisibility score of divisors[1] is 1 since only nums[0] is divisible by 2.
The divisibility score of divisors[2] is 3 since nums[2] , nums[3] and nums[4] are divisible by 3.
```

**Example 3:**

```
Input: nums = [20,14,21,10], divisors = [10,16,20]
Output: 10
Explanation:
The divisibility score of divisors[0] is 2 since nums[0] and nums[3] are divisible by 10.
The divisibility score of divisors[1] is 0 since none of the numbers in nums is divisible by 16.
The divisibility score of divisors[2] is 1 since nums[0] is divisible by 20.
```

**Constraints**

- 1 <= nums.length, divisors.length <= 1000
- 1 <= nums[i], divisors[i] <= 109

---

## 题目（中文翻译）

给定两个整数数组 `nums` 和 `divisors`。  
`divisors[i]` 的 **可整除得分（divisibility score）** 定义为满足 `nums[j]` 能被 `divisors[i]` 整除的下标 `j` 的个数。  

返回可整除得分最高的 `divisors[i]`。如果有多个整数的得分相同，返回其中最小的那个。

**示例 1**  
```text
Input: nums = [2,9,15,50], divisors = [5,3,7,2]
Output: 2
Explanation:
divisors[0] 的可整除得分为 2，因为 nums[2] 和 nums[3] 能被 5 整除。
divisors[1] 的可整除得分为 2，因为 nums[1] 和 nums[2] 能被 3 整除。
divisors[2] 的可整除得分为 0，因为 nums 中没有数能被 7 整除。
divisors[3] 的可整除得分为 2，因为 nums[0] 和 nums[3] 能被 2 整除。
```

**示例 2**  
```text
Input: nums = [4,7,9,3,9], divisors = [5,2,3]
Output: 3
Explanation:
divisors[0] 的可整除得分为 0，因为 nums 中没有数能被 5 整除。
divisors[1] 的可整除得分为 1，因为只有 nums[0] 能被 2 整除。
divisors[2] 的可整除得分为 3，因为 nums[2]、nums[3] 和 nums[4] 能被 3 整除。
```

**示例 3**  
```text
Input: nums = [20,14,21,10], divisors = [10,16,20]
Output: 10
Explanation:
divisors[0] 的可整除得分为 2，因为 nums[0] 和 nums[3] 能被 10 整除。
divisors[1] 的可整除得分为 0，因为 nums 中没有数能被 16 整除。
divisors[2] 的可整除得分为 1，因为 nums[0] 能被 20 整除。
```

**约束条件**  
- `1 <= nums.length, divisors.length <= 1000`  
- `1 <= nums[i], divisors[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**对每一个 divisor**，把 **nums 中所有能被它整除的元素** 逐个检查一遍，统计出它的“可整除个数”。  

- **使用的数据结构**：  
  - `list`（数组）保存 `nums` 与 `divisors` 本身。  
  - `int` 计数器记录当前 divisor 的得分。  
  - `dict`（哈希表）可以用来把每个 divisor 与它的得分对应起来，哈希表就像一本**查字典**，键（key）是 divisor，值（value）是它的得分。  

- **为什么正确**：  
  对每个 divisor，遍历所有的 nums，**只要出现 `nums[j] % divisor == 0`**（余数为 0），就说明这条记录符合题意，计数器加一。遍历完所有 nums，计数器的值就是该 divisor 的“可整除个数”。对所有 divisor 做同样的统计后，挑选得分最高且数值最小的那个即可，完全符合题目要求。  

- **复杂度分析（大白话）**：  
  - 外层循环遍历 `divisors`（最多 1000 次），内层循环遍历 `nums`（最多 1000 次），两层相乘得到 **大约一百万次**的基本操作。  
  - 用 **O(n·m)** 来表示，其中 `n = len(nums)`，`m = len(divisors)`。  
  - 空间上只用了几个计数器和一个保存得分的哈希表，大小与 `divisors` 长度成正比，即 **O(m)**。  

#### 代码（Python）  

```python
from typing import List

def maxDivScore(nums: List[int], divisors: List[int]) -> int:
    # 用字典记录每个 divisor 的得分，key 是 divisor，value 是可整除的个数
    score = {}

    # 暴力遍历：对每个 divisor，检查所有 nums
    for d in divisors:
        cnt = 0                     # 当前 divisor 的计数器
        for x in nums:
            if x % d == 0:          # 能整除吗？如果能，计数器加一
                cnt += 1
        score[d] = cnt              # 把结果放进字典

    # 找到最大得分，同时在得分相同的情况下取最小的 divisor
    best_divisor = None
    best_score = -1
    for d, cnt in score.items():
        # 如果当前得分更高，或者得分相同但 divisor 更小，就更新答案
        if cnt > best_score or (cnt == best_score and d < best_divisor):
            best_score = cnt
            best_divisor = d

    return best_divisor
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - 这里的 `n` 是 `nums` 长度，`m` 是 `divisors` 长度。  
  - 想象一下两层循环像是把两本书的每一页都配对检查，一共检查 `n×m` 次。  

- **空间复杂度**：`O(m)`  
  - 只用了一个字典保存每个 divisor 的得分，大小和 `divisors` 的数量成正比。  

---  

### 2. 最优解  

#### 思路  

对这道题来说，**暴力解已经是最优的**。  
- 题目约束只有 `1000 × 1000 = 10⁶` 次基本运算，完全可以在毫秒级完成。  
- 想要进一步降低时间复杂度，需要利用 **数的因子** 或 **计数前缀**，但由于 `nums[i]`、`divisors[i]` 的取值可达 `10⁹`，无法预处理所有可能的因子，也无法使用类似筛法的技巧。  

因此我们只需要把 **实现细节** 再优化一下，使代码更简洁、常数更小：

1. **一次遍历**：先把 `divisors` 的计数器全部初始化为 0（使用 `defaultdict(int)`），随后遍历 `nums`，对每个 `num` 再遍历所有 `divisors`，若能整除就把对应计数器加一。这样把两层循环的顺序换成 “先遍历 nums 再遍历 divisors”，对缓存友好，实际运行更快。  
2. **利用 `max` 的 `key` 参数**：在找出最佳 divisor 时，直接使用 `max` 函数配合自定义比较键，代码更简洁。  

核心思想仍然是 **对每个 divisor 统计可整除的 nums 个数**，但实现更紧凑，常数更低。  

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

def maxDivScore(nums: List[int], divisors: List[int]) -> int:
    # 初始化每个 divisor 的得分为 0，使用 defaultdict 能省去显式的赋值步骤
    score = defaultdict(int)

    # 先遍历 nums，再遍历所有 divisors，若能整除则计数器加一
    for x in nums:
        for d in divisors:
            if x % d == 0:          # 能整除就记一次分
                score[d] += 1

    # 使用 max 找出得分最高且数值最小的 divisor
    # key = (score, -divisor) 这里先比较得分，得分相同再比较 -divisor（因为 max 会取更大的 -divisor，即更小的 divisor）
    best = max(divisors, key=lambda d: (score[d], -d))
    return best
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - 与暴力解相同，只是把循环顺序调换，实际运行时间略有提升。  
  - 仍然是遍历 `nums`（`n` 次） × 遍历 `divisors`（`m` 次）。  

- **空间复杂度**：`O(m)`  
  - 只用了一个 `defaultdict` 保存每个 divisor 的计数，大小随 `divisors` 长度线性增长。  

---  

## 心得  

- **核心技巧**：对每个候选 divisor 统计满足“可整除”条件的元素个数，这是一次**双层遍历 + 计数**的典型模式。  
- **适用的题型**：  
  1. “统计数组中满足某种关系的配对数”——如 **Count Pairs With Absolute Difference K**。  
  2. “寻找使某种统计量最大的元素”——如 **Maximum Frequency Stack**（统计出现次数）。  
  3. “对每个查询值做线性检查”——如 **Number of Good Pairs**。  
- **一句话总结解题钥匙**：**把“能否整除”抽象成布尔检查，用计数器累计，最后挑最大/最小**。  

## 反思  

- **第一反应**：看到“可整除”就想到**遍历检查**，直接写双层循环。  
- **最容易踩的坑**：  
  - **忘记处理平局**：得分相同要返回 **最小的 divisor**，需要在比较时加入“数值更小”这一条。  
  - **边界条件**：`nums`、`divisors` 长度可能为 1，需要确保代码在只有一个元素时也能正常返回。  
- **下次遇到同类题**：第一步先 **明确计数目标**（比如“多少个数能被 X 整除”），然后决定是 **逐个检查** 还是 **利用额外结构**（如哈希表、前缀和）来加速。对本题来说，直接的双层遍历已经足够快。