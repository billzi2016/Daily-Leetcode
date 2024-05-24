# #2708. 分组的最大强度 / Maximum Strength of a Group

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Greedy、Bit Manipulation、Sorting、Enumeration · [LeetCode 链接](https://leetcode.com/problems/maximum-strength-of-a-group/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums representing the score of students in an exam. The teacher would like to form one non-empty group of students with maximal strength, where the strength of a group of students of indices i0, i1, i2, ... , ik is defined as nums[i0] * nums[i1] * nums[i2] * ... * nums[ik​].
Return the maximum strength of a group the teacher can create.

**Examples**

**Example 1:**

```
Input: nums = [3,-1,-5,2,5,-9]
Output: 1350
Explanation: One way to form a group of maximal strength is to group the students at indices [0,2,3,4,5]. Their strength is 3 * (-5) * 2 * 5 * (-9) = 1350, which we can show is optimal.
```

**Example 2:**

```
Input: nums = [-4,-5,-4]
Output: 20
Explanation: Group the students at indices [0, 1] . Then, we’ll have a resulting strength of 20. We cannot achieve greater strength.
```

**Constraints**

- 1 <= nums.length <= 13
- -9 <= nums[i] <= 9

---

## 题目（中文翻译）

你得到一个 **0 索引** 的整数数组 `nums`，其中 `nums[i]` 表示第 `i` 位学生在考试中的分数。老师希望组成一个 **非空** 的学生组，使该组的 **强度**（strength）最大。  
强度的定义为：若选中的学生下标为 `i0, i1, i2, …, ik`，则  

```
strength = nums[i0] * nums[i1] * nums[i2] * … * nums[ik]
```

返回老师能够创建的组的最大强度。

### 示例

**示例 1**  
输入: `nums = [3,-1,-5,2,5,-9]`  
输出: `1350`  
解释: 一种获得最大强度的分组方式是选择下标 `[0,2,3,4,5]` 的学生。它们的强度为  
`3 * (-5) * 2 * 5 * (-9) = 1350`，可以证明这是最优解。

**示例 2**  
输入: `nums = [-4,-5,-4]`  
输出: `20`  
解释: 将下标 `[0,1]` 的学生分在一起，得到的强度为 `(-4) * (-5) = 20`。无法得到更大的强度。

### 约束条件

- `1 <= nums.length <= 13`
- `-9 <= nums[i] <= 9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一种可能的分组** 都枚举一遍，然后把它们的乘积算出来，取最大值。  

- **数据结构**：我们只需要用到 **位掩码（bit mask）** 来表示一个子集。把数组下标 `0 … n‑1` 看成二进制位，`1` 表示该下标被选进分组，`0` 表示不选。  
  - 类比：把每个学生的名字写在一本字典里，想挑出哪些名字，就像打开字典的对应页码（bit）来看是否有内容。  
- **正确性**：位掩码遍历 `1 … (1<<n)-1`（排除全 0，因为分组不能为空），恰好覆盖了所有非空子集。对每个子集计算乘积，比较即可得到最大值。  

**为什么会对？**  
因为题目要求“最大强度”，而我们把**所有可能的强度**都算了一遍，最大值自然不会漏掉。

#### 代码（Python）

```python
from typing import List
import math

def maxStrength_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    best = -math.inf                     # 记录当前找到的最大乘积

    # 1 << n 等价于 2**n，遍历所有非空子集的位掩码
    for mask in range(1, 1 << n):
        prod = 1                         # 子集的乘积，初始为 1（乘法的中性元）
        for i in range(n):
            if mask & (1 << i):          # 第 i 位为 1，说明选了 nums[i]
                prod *= nums[i]          # 把这个学生的分数加入乘积
        best = max(best, prod)          # 更新最大值

    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  - 解释：`2^n` 是子集的数量（比如 n=13 时约 8192），每个子集我们要遍历 `n` 次检查哪些位为 1，故乘积为 `2^n * n`。这在题目给的上限（n≤13）下是完全可以接受的。  
- **空间复杂度**：`O(1)`（不计返回值）  
  - 只用了几个常数级的变量 `best、prod、mask`，不随 `n` 增长。

---

### 2. 最优解

#### 思路  

虽然 `n` 很小，但我们仍可以把这道题当作 **“最大乘积子集”** 来思考，从而得到 **O(n log n)** 的贪心解法。核心观察如下：

1. **正数**  
   - 正数乘正数会让乘积更大，**全部保留**（除非数组里全是负数或 0，后面会讨论）。  
2. **负数**  
   - 两个负数相乘会变成正数，**成对出现**可以提升乘积。  
   - 若负数的个数是 **偶数**，直接把它们全都拿进来；  
   - 若负数的个数是 **奇数**，必须丢掉 **绝对值最小的那个负数**（即 “最不“负的），这样剩下的负数仍是偶数个，乘积为正且最大。  
3. **零**  
   - 零乘任何数都会把乘积变成 0，只有在 **没有任何正数或成对负数** 时才考虑选一个零（因为必须选非空组）。  
4. **全部为负数且个数为奇数**  
   - 只能选出 **除绝对值最小的那个负数之外的所有负数**（这时乘积为正），或者只选 **一个负数**（如果没有正数也没有零），这时最大的乘积是 **绝对值最大的负数**（因为负数越大（绝对值越小）乘积越小）。  

**一步步推导**  

- 把数组按 **绝对值从大到小** 排序（或者只把负数单独排序），这样我们可以快速找到 “绝对值最小的负数”。  
- 统计正数、负数、零的个数。  
- 按上述规则决定是否丢掉一个负数、是否全体取正数、是否只能返回 0 或单个负数。  

**核心算法**：**贪心 + 排序**（不需要 DP、回溯等高级技巧），只要一次遍历就能得到答案。

#### 代码（Python）

```python
from typing import List
import math

def maxStrength_opt(nums: List[int]) -> int:
    # 1. 统计正数、负数、零，并把负数收集起来
    positives = [x for x in nums if x > 0]
    negatives = [x for x in nums if x < 0]
    zeros = [x for x in nums if x == 0]

    # 2. 如果全是零，唯一合法的组就是选一个零，乘积为 0
    if not positives and not negatives:
        return 0

    # 3. 处理负数：若数量为奇数，去掉绝对值最小的（即最大的负数）
    if len(negatives) % 2 == 1:
        # 找出 “最大负数” （例如 -1 > -5），它的绝对值最小
        max_negative = max(negatives)          # 因为负数，max 实际是绝对值最小的
        negatives.remove(max_negative)         # 丢掉它

    # 4. 现在 negatives 的个数是偶数（可能为 0），可以放心相乘
    #    正数全部保留，负数成对保留
    product = 1
    for v in positives + negatives:
        product *= v

    # 5. 可能出现的特殊情况：
    #    - 只剩下负数且数量为 0（即原来只有一个负数且没有正数、零）
    #    - 此时 product 为 1（因为循环体没执行），需要返回那唯一的负数
    if product == 1:          # 说明没有正数，也没有成对负数
        # 此时 nums 中只能是单个负数或全是零（已在第 2 步处理）
        # 直接返回绝对值最大的负数（即数值最大的负数）
        return max(nums)      # 例如 [-4] => -4

    # 6. 若 product 已经是正数，直接返回
    return product
```

> **代码要点注释**  
> - 第 1 步把数组拆成三类，便于后面分别处理。  
> - 第 3 步使用 `max(negatives)` 找到 **绝对值最小的负数**（因为负数越大，绝对值越小），随后删除。  
> - 第 5 步处理 “唯一负数” 的极端情况，防止返回默认的 `1`（乘法的中性元）而出错。  

#### 复杂度

- **时间复杂度**：`O(n log n)`（主要是对负数进行一次排序或在 `max()` 中遍历一次，`n ≤ 13`，实际开销极小）。  
  - 与暴力解的 `O(2^n * n)` 相比，**指数级的差距** 在 `n=13` 时已经可以感受到：`2^13≈8192` 次循环 vs 只需要几次遍历和一次排序。  
- **空间复杂度**：`O(n)`（用于存放 `positives、negatives、zeros` 三个列表），这在题目规模下同样是常数级别的开销。

---

## 心得

- **核心技巧**：**把负数成对使用，必要时丢掉绝对值最小的负数**，并且**正数全部保留**。这是一种典型的“符号配对 + 贪心”思路。  
- **适用的题型**  
  1. *Maximum Product Subset*（最大乘积子集）  
  2. *Maximum Strength of a Group*（本题）  
  3. *Maximum Product of Three Numbers*（找出三个数的最大乘积）  
- **一句话总结解题钥匙**：**让乘积保持正向，尽量把大绝对值的数留下，负数只能成偶数出现**。

---

## 反思

- **第一反应**：看到“乘积最大”，立刻想到枚举所有子集（暴力搜索），因为乘积不像求和那样容易使用前缀和。  
- **最容易踩的坑**  
  - 忘记 **必须选非空组**，导致在全负数、全零的情况下返回错误的默认值 `1`。  
  - 负数个数为奇数时，错误地去掉最小（绝对值最大的）负数，而不是 **绝对值最小的**。  
  - 没考虑 **只有一个负数且没有正数/零** 的情况，应该返回该负数本身。  
- **下次遇到同类题**，第一步应该思考 **符号配对**：  
  - 正数直接保留，  
  - 负数看数量是奇数还是偶数，  
  - 必要时丢掉绝对值最小的负数，  
  - 零只在没有其他合法选择时才使用。这样即可快速得到最优方案。