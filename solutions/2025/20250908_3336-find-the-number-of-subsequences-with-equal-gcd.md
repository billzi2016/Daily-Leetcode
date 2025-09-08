# #3336. 寻找 GCD 相等的子序列对数 / Find the Number of Subsequences With Equal GCD

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Number Theory · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-subsequences-with-equal-gcd/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
Your task is to find the number of pairs of non-empty subsequences (seq1, seq2) of nums that satisfy the following conditions:
Return the total number of such pairs.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4]
Output: 10
Explanation:
The subsequence pairs which have the GCD of their elements equal to 1 are:
```

**Example 2:**

```
Input: nums = [10,20,30]
Output: 2
Explanation:
The subsequence pairs which have the GCD of their elements equal to 10 are:
```

**Example 3:**

```
Input: nums = [1,1,1,1]
Output: 50
```

**Constraints**

- 1 <= nums.length <= 200
- 1 <= nums[i] <= 200

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
你的任务是统计满足以下条件的 **非空子序列对** `(seq1, seq2)` 的数量：

- `seq1` 与 `seq2` 均为 `nums` 的子序列（subsequence），且均非空。  
- `seq1` 中所有元素的最大公约数（GCD）等于 `seq2` 中所有元素的最大公约数（GCD）。

返回满足条件的对子总数。由于答案可能非常大，请返回对 `10^9 + 7` 取模后的结果。

---

### 示例

**示例 1**  
```
Input: nums = [1,2,3,4]
Output: 10
Explanation:
具有 GCD 为 1 的子序列对如下：
```

**示例 2**  
```
Input: nums = [10,20,30]
Output: 2
Explanation:
具有 GCD 为 10 的子序列对如下：
```

**示例 3**  
```
Input: nums = [1,1,1,1]
Output: 50
```

---

### 约束条件

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 200`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把每个下标的元素想象成 **三选一** 的开关：

* 选进 `seq1`  
* 选进 `seq2`  
* 两个序列都不选  

于是一次遍历所有下标，就会得到 **所有** 满足「两个子序列互不相交」的有序配对。  
对每一种配对，分别求出 `seq1`、`seq2` 的 **最大公约数（GCD）**，如果相等就计数。

> **数据结构类比**：  
> 把「把元素放进哪儿」这件事看成 **哈希表** 的写入操作——键是下标，值是「放进哪个序列」的标记（1、2、0）。  
> 只不过这里我们不真的用哈希表，而是直接用递归/循环把每种写法枚举出来。

这种方法一定能得到正确答案，因为它把「所有可能」都穷举了一遍。

#### 代码（Python）

```python
import math
from itertools import product

MOD = 10**9 + 7

def brute(nums):
    n = len(nums)
    ans = 0
    # 对每个位置的三种状态做笛卡尔积，等价于 3^n 种配对
    for states in product([0, 1, 2], repeat=n):   # 0: none, 1: seq1, 2: seq2
        seq1 = [nums[i] for i in range(n) if states[i] == 1]
        seq2 = [nums[i] for i in range(n) if states[i] == 2]
        if not seq1 or not seq2:          # 任意一个为空都不计
            continue
        g1 = seq1[0]
        for v in seq1[1:]:
            g1 = math.gcd(g1, v)
        g2 = seq2[0]
        for v in seq2[1:]:
            g2 = math.gcd(g2, v)
        if g1 == g2:
            ans = (ans + 1) % MOD
    return ans
```

> 关键行解释  
> - `product([0,1,2], repeat=n)`：把每个下标的「三选一」全部列举出来，等价于遍历 `3^n` 种情况。  
> - `if not seq1 or not seq2:`：题目要求两个子序列都 **非空**，所以直接跳过空的情况。  
> - `math.gcd`：Python 自带的求最大公约数函数，帮助我们得到每个子序列的 GCD。

#### 复杂度  

- **时间复杂度**：`O(3^n)`  
  解释：每个元素有 3 种放法，全部遍历需要 `3 * 3 * … * 3 = 3^n` 次。对 `n=200` 来说，`3^200` 是天文数字，根本跑不完。  
- **空间复杂度**：`O(n)`（保存 `seq1`、`seq2` 的临时列表）  

显然，这种暴力方式只能用来验证思路或跑非常小的测试数据，不能作为正式解法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于「指数级」的枚举。  
实际上，每一次遍历只会把当前元素 **加入** `seq1`、**加入** `seq2`、或 **不加入**，这正好可以用 **动态规划**（DP）把状态压缩。

**状态定义**  

> `dp[g1][g2]` = **已经处理完前 i（i 从 0 开始计数）个元素后**，  
> `seq1` 的 GCD 为 `g1`、`seq2` 的 GCD 为 `g2` 的 **有序配对数量**。  
> 这里约定 `g = 0` 表示对应的子序列仍然是 **空的**（还没有选任何元素）。

因为 `nums[i] ≤ 200`，所有可能的 GCD 只会落在 `[0, 200]` 之间，状态空间只有 `201 × 201 ≈ 4·10⁴`。

**转移**  

遍历到新元素 `x` 时，有三种选择：

| 选择 | 新的 `g1` | 新的 `g2` |
|------|----------|----------|
| 不选 | `g1`     | `g2`     |
| 放进 `seq1` | `gcd(g1, x)`（若 `g1==0` 则直接是 `x`） | `g2` |
| 放进 `seq2` | `g1` | `gcd(g2, x)`（若 `g2==0` 则直接是 `x`） |

于是对每一对旧状态 `(g1, g2)`，我们把对应的计数分配到上述三条新状态上。

**答案提取**  

所有元素处理完后，`dp[g][g]`（`g>0`）表示「两个子序列非空且 GCD 相等」的配对数。把它们全部相加即为答案。

**为什么正确**  

- DP 的每一步都完整地考虑了「把当前元素放到哪儿」的三种可能，且不会遗漏也不会重复计数。  
- 状态只保留了 **GCD** 信息，而不是具体的子序列内容。因为后续的转移只依赖于当前的 GCD 与即将加入的元素的值，这正是 **最小充分信息**（即「马尔科夫性」）。  
- 通过约定 `g=0` 表示空子序列，最终只统计 `g>0` 的情况即可自动满足「非空」的要求。

**复杂度分析**  

- 状态数 `≈ 201²`，每个元素遍历所有状态一次，时间 `O(n·V²)`，其中 `V = 200`。  
  对于最大 `n=200`，约 `200·40 000 = 8·10⁶` 次基本运算，轻松跑完。  
- 只需要两个 `201×201` 的数组交替使用，空间 `O(V²)` ≈ `4·10⁴`，几乎可以忽略。

#### 代码（Python）

```python
import math

MOD = 10**9 + 7
MAXV = 200               # nums[i] 的上界，也是 GCD 的最大可能值

def number_of_pairs(nums):
    # dp[g1][g2] 表示处理到当前下标前，seq1 GCD=g1, seq2 GCD=g2 的配对数
    dp = [[0] * (MAXV + 1) for _ in range(MAXV + 1)]
    dp[0][0] = 1          # 两个子序列都还空，算作一种“起点”状态

    for x in nums:
        ndp = [[0] * (MAXV + 1) for _ in range(MAXV + 1)]
        for g1 in range(MAXV + 1):
            for g2 in range(MAXV + 1):
                cur = dp[g1][g2]
                if cur == 0:
                    continue

                # 1. 当前元素不放入任何序列
                ndp[g1][g2] = (ndp[g1][g2] + cur) % MOD

                # 2. 放进 seq1
                ng1 = x if g1 == 0 else math.gcd(g1, x)
                ndp[ng1][g2] = (ndp[ng1][g2] + cur) % MOD

                # 3. 放进 seq2
                ng2 = x if g2 == 0 else math.gcd(g2, x)
                ndp[g1][ng2] = (ndp[g1][ng2] + cur) % MOD
        dp = ndp          # 进入下一个元素的循环

    # 把所有 GCD 相等且均非空的配对相加
    ans = 0
    for g in range(1, MAXV + 1):      # g=0 表示空序列，不能计入答案
        ans = (ans + dp[g][g]) % MOD
    return ans
```

> 关键行解释  
> - `dp[0][0] = 1`：把「两个序列都还没有选任何元素」当作唯一的起始状态。后面的转移会把它逐步演化成真正的配对。  
> - `ng1 = x if g1 == 0 else math.gcd(g1, x)`：如果 `seq1` 之前为空（`g1==0`），加入第一个元素后 GCD 就是这个元素本身；否则把新元素和已有 GCD 再取一次 `gcd`。  
> - `ndp` 与 `dp` 交替使用，避免在同一次遍历里把「本轮新产生的状态」又当作「旧状态」继续转移，保证 **一次遍历对应一次元素**。  
> - 最后只统计 `g≥1` 的 `dp[g][g]`，恰好满足「两个子序列都非空且 GCD 相等」的要求。

#### 复杂度

- **时间复杂度**：`O(n·V²) = O(200·200²) ≈ 8·10⁶`  
  - 含义：虽然看起来是「平方」的操作，但 `V`（最大数值）只有 200，实际运行非常快。相比暴力的 `3ⁿ`，提升是指数级的。
- **空间复杂度**：`O(V²) = O(200²) ≈ 4·10⁴`  
  - 只需要两个二维数组，几乎可以忽略不计。

---

## 心得

- **核心技巧**：**状态压缩动态规划 + GCD 的可合并性**  
  把「把元素放进哪一个子序列」抽象成三选一，利用 DP 把指数枚举压缩到多项式时间。  
- **适用题型**（类似思路）  
  1. “统计满足某种数论条件的子序列/子集配对”——如 **子序列 GCD 为 1 的配对数**。  
  2. “两个子序列互不相交，且满足某种相等关系”——如 **两个子序列的和相等**（可用前缀和 DP）。  
  3. “把每个元素分配到若干组，组间满足可合并的属性”——如 **分配到两条递增序列**（利用最长递增子序列的 DP 思路）。  
- **一句话总结**：  
  “把每个位置的三种去向写成 DP 转移，只保留 GCD 这唯一必要的信息，就能在多项式时间内计数所有合法的子序列配对。”

---

## 反思

- **第一反应**：看到「子序列」和「GCD」就想到枚举所有子集，随后想到「两两配对」导致 `3ⁿ` 的爆炸式枚举。  
- **最容易踩的坑**  
  1. **忘记排除空子序列**：`g=0` 需要特殊处理，否则会把空序列计入答案。  
  2. **状态覆盖**：在同一次遍历中直接在 `dp` 上更新会导致同一个元素被使用多次，需要使用 `ndp`（新数组）实现“层层推进”。  
  3. **取模忘记**：答案可能非常大，所有加法都要取模，否则会出现整数溢出。  
- **下次类似题的第一步**：  
  “先把每个元素的可能去向（加入哪一个子结构或不加入）列出来，检查是否可以用 DP 只保留关键属性（如 GCD、和、最大值）进行状态压缩”。这样就能把指数搜索变成多项式 DP。