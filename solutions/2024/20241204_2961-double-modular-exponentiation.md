# #2961. 双模指数运算 / Double Modular Exponentiation

> 难度：中等 · 标签：Array、Math、Simulation · [LeetCode 链接](https://leetcode.com/problems/double-modular-exponentiation/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D array variables where variables[i] = [ai, bi, ci, mi], and an integer target.
An index i is good if the following formula holds:
Return an array consisting of good indices in any order.

**Examples**

**Example 1:**

```
Input: variables = [[2,3,3,10],[3,3,3,1],[6,1,1,4]], target = 2
Output: [0,2]
Explanation: For each index i in the variables array:
1) For the index 0, variables[0] = [2,3,3,10], (23 % 10)3 % 10 = 2.
2) For the index 1, variables[1] = [3,3,3,1], (33 % 10)3 % 1 = 0.
3) For the index 2, variables[2] = [6,1,1,4], (61 % 10)1 % 4 = 2.
Therefore we return [0,2] as the answer.
```

**Example 2:**

```
Input: variables = [[39,3,1000,1000]], target = 17
Output: []
Explanation: For each index i in the variables array:
1) For the index 0, variables[0] = [39,3,1000,1000], (393 % 10)1000 % 1000 = 1.
Therefore we return [] as the answer.
```

**Constraints**

- 1 <= variables.length <= 100
- variables[i] == [ai, bi, ci, mi]
- 1 <= ai, bi, ci, mi <= 103
- 0 <= target <= 103

---

## 题目（中文翻译）

给定一个 0 索引的二维数组 `variables`，其中 `variables[i] = [a_i, b_i, c_i, m_i]`，以及一个整数 `target`。  
如果下列公式成立，则下标 `i` 为 **好下标**（good index）：

\[
\bigl( (a_i^{\,b_i} \bmod m_i)^{\,c_i} \bmod m_i \bigr) = \text{target}
\]

返回包含所有好下标的数组，顺序不限。

**示例 1**

```text
Input: variables = [[2,3,3,10],[3,3,3,1],[6,1,1,4]], target = 2
Output: [0,2]
Explanation:
对于每个下标 i：
1) i = 0, variables[0] = [2,3,3,10]  
   (2^3 % 10)^3 % 10 = 2
2) i = 1, variables[1] = [3,3,3,1]  
   (3^3 % 1)^3 % 1 = 0
3) i = 2, variables[2] = [6,1,1,4]  
   (6^1 % 4)^1 % 4 = 2
因此返回 [0,2]。
```

**示例 2**

```text
Input: variables = [[39,3,1000,1000]], target = 17
Output: []
Explanation:
i = 0, variables[0] = [39,3,1000,1000]  
(39^3 % 1000)^1000 % 1000 = 1
不等于 target，故返回空数组。
```

**约束条件**

- `1 <= variables.length <= 100`
- `variables[i] == [a_i, b_i, c_i, m_i]`
- `1 <= a_i, b_i, c_i, m_i <= 10^3`
- `0 <= target <= 10^3`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把公式 **`((a^b) % m) ^ c % m`** 按字面意义一步步算出来：

1. 先算 `a^b`（把 `a` 连乘 `b` 次），得到一个可能非常大的整数。  
2. 把上一步的结果对 `m` 取模，得到 `x = (a^b) % m`。  
3. 再算 `x^c`（把 `x` 连乘 `c` 次），同样会得到一个巨大的数。  
4. 最后再对 `m` 取模，得到最终结果 `res = (x^c) % m`。  

> **类比**：把 `a^b` 想成“把 `a` 放进一个装满 `b` 个相同球的盒子”，盒子里球的数量会指数级增长。  
> `mod` 操作就像在盒子外面装了一个“筛子”，只保留除以 `m` 的余数，筛掉了“大部分”球。  

只要把每一步都算出来，就能判断 `res` 是否等于 `target`，如果相等就把下标记为 “good”。  

**为什么这个方法正确？**  
公式本身没有任何隐藏的技巧，直接按顺序执行每一步得到的值必然就是题目要求的结果。只要不在中间的乘法里出现错误（比如整数溢出），答案一定对。

**时间/空间复杂度**  
- 对每个 `i`，我们要做 `b_i` 次乘法再做 `c_i` 次乘法，时间复杂度是 **O(b_i + c_i)**。在最坏情况下 `b_i`、`c_i` 都可能是 1000，所以单个元素的耗时大约是 2000 次基本运算。  
- 需要保存 `variables` 本身以及常数级的临时变量，空间复杂度是 **O(1)**（不计输入数组本身）。

> **大白话解释**：`O(b_i + c_i)` 可以理解为“运行时间随 `b` 和 `c` 的大小线性增长”。如果 `b`、`c` 都是 1000，算法大概要跑 2000 步；如果它们是 10，算法只要跑 20 步。

#### 代码（Python）  

```python
from typing import List

def goodIndices_bruteforce(variables: List[List[int]], target: int) -> List[int]:
    """
    暴力解：直接按照 ((a^b) % m) ^ c % m 的顺序逐步计算
    """
    good = []                                   # 用来收集满足条件的下标
    for idx, (a, b, c, m) in enumerate(variables):
        # 1. 计算 a^b（直接乘 b 次）
        power_ab = 1
        for _ in range(b):
            power_ab *= a                       # 逐次相乘，可能会得到非常大的数

        # 2. 对 m 取模
        x = power_ab % m

        # 3. 计算 x^c（直接乘 c 次）
        power_xc = 1
        for _ in range(c):
            power_xc *= x

        # 4. 再次取模得到最终结果
        res = power_xc % m

        # 5. 与 target 比较
        if res == target:
            good.append(idx)                    # 记录满足条件的下标
    return good
```

#### 复杂度  

- **时间复杂度**：`O( Σ (b_i + c_i) )`，最坏情况下约为 `O(n * 2000)`，其中 `n = len(variables)`。  
  - **含义**：运行时间随所有 `b`、`c` 的总和线性增长。  
- **空间复杂度**：`O(1)`（只使用常数个额外变量），不计输入数组本身。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于直接把 `a^b`、`x^c` 逐个相乘**，当指数稍大时，数值会爆炸，乘法次数也会非常多。  
我们可以利用 **“模幂”**（modular exponentiation）这个数学技巧来把指数运算的复杂度从线性降到对数。

**核心思想：**  
- `(a^b) % m` 可以用 **快速幂**（Repeated Squaring）在 `O(log b)` 步内算完。Python 的内置函数 `pow(a, b, m)` 已经帮我们实现了这一步。  
- 同理，`(x^c) % m` 也可以在 `O(log c)` 步内完成。  

**为什么快速幂有效？**  
把指数二进制拆分，例如 `b = 13 = 1101₂`，则  
`a^13 = a^(8+4+1) = a^8 * a^4 * a^1`。  
我们只需要先算 `a^1, a^2, a^4, a^8 …`（每次把前一次的结果平方），然后把对应位为 1 的结果相乘。  
每次平方或相乘后立刻对 `m` 取模，保证中间值始终保持在 `[0, m-1]` 范围内，既防止溢出又省时间。

**完整流程**（对每个四元组）：

1. 用 `pow(a, b, m)` 直接得到 `x = (a^b) % m`（一步搞定，时间 `O(log b)`）。  
2. 再用 `pow(x, c, m)` 直接得到 `res = (x^c) % m`（时间 `O(log c)`）。  
3. 比较 `res` 与 `target`，相等则把下标加入答案。  

这样每个元素只需要 `log` 级的运算，整体复杂度降到 `O(n * (log b + log c))`，在本题的约束下几乎是瞬间完成。

#### 代码（Python）  

```python
from typing import List

def goodIndices_optimal(variables: List[List[int]], target: int) -> List[int]:
    """
    最优解：利用 Python 内置的 pow(base, exp, mod) 实现快速模幂
    """
    good = []                                   # 保存满足条件的下标
    for idx, (a, b, c, m) in enumerate(variables):
        # 第一步：计算 (a^b) % m，时间复杂度 O(log b)
        x = pow(a, b, m)                       # pow 自动在每一步取模，避免大数爆炸

        # 第二步：计算 (x^c) % m，时间复杂度 O(log c)
        res = pow(x, c, m)

        # 检查是否等于 target
        if res == target:
            good.append(idx)
    return good
```

#### 复杂度  

- **时间复杂度**：`O( Σ (log b_i + log c_i) )`，即 `O(n * (log B + log C))`，其中 `B = max(b_i)`、`C = max(c_i)`。  
  - **含义**：相较于暴力的线性乘法，运行时间随指数的 **对数** 增长。即使 `b`、`c` 达到 1000，`log2(1000) ≈ 10`，所以每个四元组只需要约 20 次基本运算。  
- **空间复杂度**：`O(1)`（只用常数级额外变量），不计输入数组本身。

---

## 心得  

- **核心技巧**：**快速模幂**（modular exponentiation），即在指数运算过程中随时取模，利用二进制分解把指数从线性降低到对数。  
- **适用的题型**：  
  1. “大数取模” 类问题，如 `a^b % m`、`(a^b * c) % m` 等。  
  2. “指数递推” 类题目，例如求 `fib(n) % m`（可用矩阵快速幂），或者 “Power of Two” 变形。  
- **一句话总结解题钥匙**：**“指数大时先模，再用快速幂”。**  

---

## 反思  

- **第一反应**：看到 `a^b`、`x^c`，立刻想用循环相乘，因为这是最直观的实现方式。  
- **最容易踩的坑**：  
  - 直接相乘会产生 **超大整数**，导致运行慢甚至内存爆炸（虽然 Python 能处理大整数，但效率极低）。  
  - 忘记在 **每一步** 取模，导致中间结果远超 `m`，失去快速幂的优势。  
  - 边界情况：`m = 1` 时，任何数对 1 取模都是 0，需要确保 `pow(..., 1)` 能正确返回 0（Python 已经处理好）。  
- **下次遇到同类题**：第一步就问自己 “**指数是否太大，能否用模幂**”，如果答案是肯定的，就直接使用 `pow(base, exp, mod)` 或手写快速幂。这样既安全又高效。