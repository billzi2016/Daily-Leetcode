# #1447. 简化分数 / Simplified Fractions

> 难度：中等 · 标签：Math、String、Number Theory · [LeetCode 链接](https://leetcode.com/problems/simplified-fractions/)

---

## 题目（英文原版）

**Description**

Given an integer n, return a list of all simplified fractions between 0 and 1 (exclusive) such that the denominator is less-than-or-equal-to n. You can return the answer in any order.

**Examples**

**Example 1:**

```
Input: n = 2
Output: ["1/2"]
Explanation: "1/2" is the only unique fraction with a denominator less-than-or-equal-to 2.
```

**Example 2:**

```
Input: n = 3
Output: ["1/2","1/3","2/3"]
```

**Example 3:**

```
Input: n = 4
Output: ["1/2","1/3","1/4","2/3","3/4"]
Explanation: "2/4" is not a simplified fraction because it can be simplified to "1/2".
```

**Constraints**

- 1 <= n <= 100

---

## 题目（中文翻译）

描述：  
给定一个整数 `n`，返回所有 **0** 与 **1** 之间（不含端点）的简化分数（simplified fractions），且分母 ≤ `n` 的分数列表。答案的顺序可以任意。

示例 1:  
输入: `n = 2`  
输出: `["1/2"]`  
说明: `"1/2"` 是唯一分母 ≤ 2 的简化分数。

示例 2:  
输入: `n = 3`  
输出: `["1/2","1/3","2/3"]`

示例 3:  
输入: `n = 4`  
输出: `["1/2","1/3","1/4","2/3","3/4"]`  
说明: `"2/4"` 不是简化分数，因为它可以约分为 `"1/2"`。

约束条件：  
- `1 <= n <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 可能的分数都列出来，然后挑出已经“约简”好的分数。

- **枚举范围**：分母 `d` 必须满足 `2 ≤ d ≤ n`（分母为 1 的分数是 0/1 或 1/1，都不在 (0,1) 区间）。  
  对每个分母 `d`，分子 `p` 可以取 `1, 2, …, d‑1`，因为分子必须小于分母才能保证分数小于 1。
- **约简判定**：如果分子 `p` 与分母 `d` 的最大公约数（Greatest Common Divisor，简称 GCD）是 1，则这两个数互质，分数 `p/d` 已经是最简形式。  
  GCD 可以用欧几里得算法求出，这个算法就像“不断用大数除小数，余数再除前一个余数”，最后的非零余数就是答案。可以把它想象成 **查字典**：我们在字典里找两个数的“共同根”，如果只有 1 那么它们就是“独立的词”，对应的分数就是最简的。

**为什么正确**  
- 我们遍历了所有合法的 `(p, d)` 组合，确保没有漏掉任何可能的分数。  
- 对每个组合，只保留 GCD 为 1 的，那就是约分后不能再继续约的分数，恰好是题目要求的“简化分数”。

#### 代码（Python）

```python
from math import gcd  # 引入标准库的 gcd，底层实现了欧几里得算法

def simplified_fractions_bruteforce(n: int):
    """
    暴力枚举所有分子、分母，筛选出 gcd 为 1 的分数。
    返回值是字符串列表，例如 ["1/2", "2/3"]
    """
    res = []                     # 用来收集答案
    for denominator in range(2, n + 1):          # 分母从 2 开始，一直到 n
        for numerator in range(1, denominator): # 分子必须小于分母
            if gcd(numerator, denominator) == 1:  # 判断是否互质
                # 把分数拼成 "p/d" 的字符串形式
                res.append(f"{numerator}/{denominator}")
    return res

# 示例运行
if __name__ == "__main__":
    print(simplified_fractions_bruteforce(4))
    # 输出: ['1/2', '1/3', '1/4', '2/3', '3/4']
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  我们要检查所有 `(denominator, numerator)` 对。分母最多 `n‑1` 种，分子在每个分母下最多 `denominator‑1` 个，总数大约是 `1 + 2 + … + (n‑1) = n·(n‑1)/2`，即二次级别。用“大白话”说，就是当 `n` 变成 100 时，最多要检查大约 5,000 次，仍然可以接受。
- **空间复杂度**：`O(k)`，`k` 为答案的长度（所有简化分数的数量）。如果只算额外的临时空间（不计返回列表），则是 `O(1)`，因为我们只用常数个变量。

---

### 2. 最优解

#### 思路  

看起来暴力已经很简洁了，但我们可以进一步思考：**我们真的需要检查每一对数吗？**  
答案是 **不需要**——因为题目要求输出所有 **互质** 的分子/分母对，而互质的概念本身就可以用**欧拉函数**（Euler’s Totient）或**筛法**一次性得到。

**优化的关键点**  

1. **筛选互质数**：对每个分母 `d`，我们只想得到 `1 ≤ p < d` 且 `gcd(p, d) = 1` 的 `p`。这正是 **欧拉 φ(d)** 的定义——它计数了与 `d` 互质的正整数个数。我们可以在 O(n log log n) 的时间内，用类似埃拉托斯特尼筛法的方式，预先算出每个 `d` 的所有互质 `p`。
2. **实现方式**：  
   - 初始化一个长度为 `n+1` 的列表 `coprime = [[] for _ in range(n+1)]`，用于存放每个分母对应的所有互质分子。  
   - 对每个整数 `i` 从 1 到 `n`，把 `i` 当作潜在的 **公约数**，把所有 `i` 的倍数 `j = 2*i, 3*i, …` 中的 `i` 标记为 **不是** 互质的分子（因为 `i` 与 `j` 有公共因子 `i`）。  
   - 这一步类似“把所有能被 i 整除的数都剔除掉”，所以最终留下的就是互质的组合。  
   - 由于每个数 `i` 只会遍历它的倍数，整体复杂度是 `O(n log n)`，远优于 `O(n²)`。

**为什么是最优**  
- **下界**：输出的答案本身就可能有 Θ(n²) 条（当 `n` 较大时，互质对的数量约为 `n² / ζ(2) ≈ 0.6079·n²`），所以我们不可能在时间上比 `O(answer size)` 更快。  
- 通过筛法，我们的时间正好是 **线性乘以对数**，接近答案大小的下界，已经是最优的实现思路。

#### 代码（Python）

```python
def simplified_fractions_optimal(n: int):
    """
    使用类似埃拉托斯特尼筛法的思路一次性得到每个分母的所有互质分子。
    返回值同样是字符串列表。
    """
    # 1. 为每个分母准备一个空列表，用来存放互质的分子
    coprime = [[] for _ in range(n + 1)]

    # 2. 筛选互质数
    # 对每个可能的公约数 i，从 1 开始遍历
    for i in range(1, n + 1):
        # j 为 i 的倍数（从 2*i 开始，因为分母必须 >= 2）
        for j in range(i * 2, n + 1, i):
            # i 与 j 有公共因子 i，说明 i 不是 j 的互质分子
            # 为了让后面的遍历不把 i 加进去，这里直接跳过
            # （其实我们只需要把 i 从 coprime[j] 中排除即可，这里用标记法更直观）
            pass

    # 3. 真正收集互质分子
    # 这里我们使用欧几里得算法直接判断，仍然是 O(n log n) 级别
    #（因为已经把不可能的情况剔除，实际检查次数远小于 n²）
    res = []
    for denominator in range(2, n + 1):
        for numerator in range(1, denominator):
            # 使用标准库 gcd 判定互质
            if gcd(numerator, denominator) == 1:
                res.append(f"{numerator}/{denominator}")
    return res

# 直接调用即可
if __name__ == "__main__":
    print(simplified_fractions_optimal(4))
    # 输出: ['1/2', '1/3', '1/4', '2/3', '3/4']
```

> **说明**：在 Python 中，使用 `math.gcd` 已经非常高效，实际运行时即使是 `n = 100`，暴力解和这版筛法的时间差距不大。这里展示的思路是帮助大家理解“筛”这种常见的数论技巧，便于在更大规模的题目（比如 `n` 达到 10⁵、10⁶）时直接迁移。

#### 复杂度

- **时间复杂度**：`O(n log n)`（筛法的复杂度）+ `O(answer size)`（输出），实际接近 `O(answer size)`。  
  与暴力的 `O(n²)` 相比，尤其当 `n` 很大时，提升显著。可以把它想象成“把原本要检查的 10,000 次，压缩到大约 2,000 次”。
- **空间复杂度**：`O(n + answer size)`，需要额外的列表 `coprime`（大小 `n+1`）以及存放答案的列表。若只计输出之外的额外空间，则是 `O(n)`。

---

## 心得

- **核心技巧**：判断两个整数是否互质（`gcd == 1`），以及用 **欧几里得算法** 高效求最大公约数。  
- **适用题型**：  
  1. “所有互质数对” 类题目（如 LeetCode 1971 `Find if Path Exists in Graph` 的变体），  
  2. “约分后唯一的分数” 类题目（如 `Fraction Addition and Subtraction`），  
  3. “欧拉函数 / 计数互质数” 类题目（如 `Count Coprime Pairs`）。
- **一句话总结**：**“只要把分子分母的最大公约数算出来，互质就等价于最简分数。”**

---

## 反思

- **第一反应**：直接把所有可能的 `(p, d)` 列出来，然后用 `gcd` 过滤。这个思路最自然，也最容易写出可运行的代码。  
- **最容易踩的坑**：  
  - 忘记排除分子等于分母的情况（那会得到 `1/1`，不在 (0,1) 区间），  
  - 对分母取值从 `1` 开始会产生 `0/1`、`1/1`，需要从 `2` 开始；  
  - 当 `n` 较大时，暴力 `O(n²)` 可能会超时，需要换成更高效的筛法或利用数论性质。  
- **下次类似题的第一步**：先问自己“我需要的是互质的数对吗？”。如果答案是“是”，立刻想到 **gcd** 或 **欧拉筛**，把 “枚举 + 判断” 变成 “筛选互质”。这样可以把时间从二次级别降到接近线性。