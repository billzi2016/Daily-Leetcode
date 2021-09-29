# #1492. 第 k 个因数 / The kth Factor of n

> 难度：中等 · 标签：Math、Number Theory · [LeetCode 链接](https://leetcode.com/problems/the-kth-factor-of-n/)

---

## 题目（英文原版）

**Description**

You are given two positive integers n and k. A factor of an integer n is defined as an integer i where n % i == 0.
Consider a list of all factors of n sorted in ascending order, return the kth factor in this list or return -1 if n has less than k factors.
Follow up:
Could you solve this problem in less than O(n) complexity?

**Examples**

**Example 1:**

```
Input: n = 12, k = 3
Output: 3
Explanation: Factors list is [1, 2, 3, 4, 6, 12], the 3rd factor is 3.
```

**Example 2:**

```
Input: n = 7, k = 2
Output: 7
Explanation: Factors list is [1, 7], the 2nd factor is 7.
```

**Example 3:**

```
Input: n = 4, k = 4
Output: -1
Explanation: Factors list is [1, 2, 4], there is only 3 factors. We should return -1.
```

**Constraints**

- 1 <= k <= n <= 1000

---

## 题目（中文翻译）

给定两个正整数 `n` 和 `k`。整数（integer）`n` 的因数（factor）定义为满足 `n % i == 0` 的整数 `i`。  
将 `n` 的所有因数按升序（ascending order）排列成一个列表（list），返回该列表中的第 `k` 个因数；如果 `n` 的因数少于 `k` 个，则返回 `-1`。

**示例 1**  
**示例 2**  
**示例 3**  

**进阶**  
你能在时间复杂度低于 `O(n)` 的情况下解决此问题吗？

---

### 示例

**示例 1**  
```
Input: n = 12, k = 3
Output: 3
Explanation: 因数列表为 [1, 2, 3, 4, 6, 12]，第 3 个因数是 3。
```

**示例 2**  
```
Input: n = 7, k = 2
Output: 7
Explanation: 因数列表为 [1, 7]，第 2 个因数是 7。
```

**示例 3**  
```
Input: n = 4, k = 4
Output: -1
Explanation: 因数列表为 [1, 2, 4]，只有 3 个因数，因此返回 -1。
```

### 约束条件
- `1 <= k <= n <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：从 **1** 遍历到 **n**，把所有能整除 `n` 的数记下来。  
- **数据结构**：用一个普通的 Python `list`（列表）保存找到的因子。列表就像装东西的盒子，后面可以直接取第 `k` 个元素。  
- **为什么正确**：如果 `i` 能整除 `n`（`n % i == 0`），那么 `i` 就是 `n` 的因子。把所有满足条件的 `i` 按顺序放进列表，列表天然是升序的（因为我们是从小到大遍历的），于是第 `k` 个元素就是第 `k` 小的因子。  
- **复杂度大白话**：我们要检查 **每一个** 从 `1` 到 `n` 的数是否是因子，最坏情况下要做 `n` 次除法运算，这就是 **O(n)**。如果 `n` 很大，这一步会比较慢。空间上我们需要把所有因子都存下来，最多可能有 `n` 个因子（比如 `n = 1`），所以是 **O(n)** 的额外空间。

#### 代码（Python）

```python
def kth_factor_bruteforce(n: int, k: int) -> int:
    """暴力枚举所有因子，返回第 k 小的因子或 -1"""
    factors = []                         # 用列表收集因子
    for i in range(1, n + 1):            # 从 1 遍历到 n
        if n % i == 0:                   # 能整除说明是因子
            factors.append(i)            # 把因子放进列表
    # 判断第 k 个因子是否存在（列表索引从 0 开始）
    if k <= len(factors):
        return factors[k - 1]            # 第 k 小的因子
    return -1                            # 因子不足 k 个
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 需要检查 `1 … n` 共 `n` 次除法。  
- **空间复杂度**：`O(n)` —— 最坏情况下把所有因子（最多 `n` 个）都存进列表。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**遍历整个区间 `[1, n]`**。事实上，因子是成对出现的：如果 `i` 是因子，则 `n / i` 也是因子。例如 `12` 的因子对有 `(1,12)`, `(2,6)`, `(3,4)`。  
- **关键观察**：每一对因子中，较小的那个一定不超过 `√n`（因为如果两个数都大于 `√n`，乘积会超过 `n`）。  
- 因此，只需要检查 **`1 … √n`**，就能找到所有因子对。我们把较小的因子放进一个列表 `small`，把对应的较大因子（`n // i`）放进另一个列表 `large`。`large` 里的元素天然是 **降序** 的（因为 `i` 从小到大，`n // i` 从大到小），我们只需要在最后把 `large` 反转成升序，或者直接在取第 `k` 个因子时考虑顺序。  

**实现步骤**  

1. 遍历 `i` 从 `1` 到 `int(sqrt(n))`（含），如果 `i` 能整除 `n`：  
   - 把 `i` 加入 `small`（这已经是升序）。  
   - 如果 `i != n // i`（不是平方根自身），把 `n // i` 加入 `large`（此时 `large` 是降序）。  
2. 合并 `small` 与 `reversed(large)`，得到完整的升序因子列表。  
3. 判断 `k` 是否超出列表长度，若超出返回 `-1`，否则返回第 `k` 个因子。  

**复杂度大白话**：我们只遍历到 `√n`，如果 `n = 10⁶`，只需要检查约 **1000** 次，比遍历一百万次快很多。空间上我们只存因子本身，最多也不超过 `2 * √n`（因为每次最多产生一对），所以是 `O(√n)`。

#### 代码（Python）

```python
import math

def kth_factor_optimal(n: int, k: int) -> int:
    """利用因子成对的特性，只遍历到 sqrt(n) 求第 k 小的因子"""
    small = []   # 存放较小的因子，升序
    large = []   # 存放较大的因子，降序（后面会反转）

    limit = int(math.isqrt(n))          # sqrt(n) 的整数部分
    for i in range(1, limit + 1):
        if n % i == 0:                  # i 是因子
            small.append(i)             # 较小的因子直接加入
            other = n // i
            if other != i:               # 防止平方根重复计数
                large.append(other)      # 较大的因子加入 large

    # 合并得到完整的升序因子序列
    factors = small + large[::-1]       # large[::-1] 把降序翻转成升序

    if k <= len(factors):
        return factors[k - 1]
    return -1
```

#### 复杂度  

- **时间复杂度**：`O(√n)` —— 只循环到 `sqrt(n)`，每次做常数时间的除法和列表操作。  
- **空间复杂度**：`O(√n)` —— 最多存 `2 * √n` 个因子（每个因子最多出现一次），远小于 `O(n)`。  

---

## 心得  

- **核心技巧**：**因子成对**（小因子 ≤ √n，大因子 = n / 小因子）以及 **只遍历到 √n** 的思想。  
- **适用的题型**：  
  1. “找出所有因子” 类题目（如 LeetCode 1025 – *Divisor Game* 的因子统计）。  
  2. “判断是否为完全平方数” 或 “判断是否为回文数的因子” 等涉及因子对的数论题。  
- **一句话总结**：**把大问题压缩到 √n，因子对让我们只需检查一半的数即可得到全部答案。**  

---

## 反思  

- **第一反应**：直接暴力枚举 `1 … n`，因为最直观、代码最简单。  
- **最容易踩的坑**：  
  - 忘记处理 **平方根** 本身（如 `n = 9`，因子对是 `(3,3)`，只应计数一次）。  
  - 当 `k` 超出因子总数时要返回 `-1`，否则会出现索引错误。  
  - 对于大 `n`，若仍用 `O(n)` 会超时或运行慢。  
- **下次遇到同类题**：第一步先思考 **是否有对称结构**（如因子、约数、配对等），尝试把搜索范围压到 **√n**，再决定是否需要额外的数据结构来保存中间结果。