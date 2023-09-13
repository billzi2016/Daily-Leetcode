# #2400. 恰好 k 步后到达指定位置的方法数 / Number of Ways to Reach a Position After Exactly k Steps

> 难度：中等 · 标签：Math、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-reach-a-position-after-exactly-k-steps/)

---

## 题目（英文原版）

**Description**

You are given two positive integers startPos and endPos. Initially, you are standing at position startPos on an infinite number line. With one step, you can move either one position to the left, or one position to the right.
Given a positive integer k, return the number of different ways to reach the position endPos starting from startPos, such that you perform exactly k steps. Since the answer may be very large, return it modulo 109 + 7.
Two ways are considered different if the order of the steps made is not exactly the same.
Note that the number line includes negative integers.

**Examples**

**Example 1:**

```
Input: startPos = 1, endPos = 2, k = 3
Output: 3
Explanation: We can reach position 2 from 1 in exactly 3 steps in three ways:
- 1 -> 2 -> 3 -> 2.
- 1 -> 2 -> 1 -> 2.
- 1 -> 0 -> 1 -> 2.
It can be proven that no other way is possible, so we return 3.
```

**Example 2:**

```
Input: startPos = 2, endPos = 5, k = 10
Output: 0
Explanation: It is impossible to reach position 5 from position 2 in exactly 10 steps.
```

**Constraints**

- 1 <= startPos, endPos, k <= 1000

---

## 题目（中文翻译）

你得到两个正整数 `startPos` 和 `endPos`。最初，你站在无限数轴上的位置 `startPos`。每走一步，你可以向左移动一个单位，也可以向右移动一个单位。  
给定正整数 `k`，返回恰好走完 `k` 步后，从 `startPos` 到达 `endPos` 的不同路径数。由于答案可能非常大，请返回 **10⁹ + 7** 取模后的结果。  

两条路径如果走的步序不同，则视为不同的路径。  
注意，数轴上包含负整数。

### 示例

#### 示例 1
**输入**: `startPos = 1, endPos = 2, k = 3`  
**输出**: `3`  
**解释**: 恰好用 3 步从 1 到达 2 有三种方式：
- `1 -> 2 -> 3 -> 2`
- `1 -> 2 -> 1 -> 2`
- `1 -> 0 -> 1 -> 2`  

可以证明不存在其他方式，所以返回 3。

#### 示例 2
**输入**: `startPos = 2, endPos = 5, k = 10`  
**输出**: `0`  
**解释**: 在恰好 10 步内不可能从位置 2 到达位置 5。

### 约束条件
- `1 <= startPos, endPos, k <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把每一步都「枚举」出来：  
- 从 `startPos` 开始，每走一步可以往左（-1）也可以往右（+1）。  
- 用递归（或 BFS）把所有长度为 `k` 的步序列全部遍历一遍，看看走完后是否恰好落在 `endPos`。  

> **类比**：把整数轴想成一条无尽的走廊，你站在 `startPos`，每次可以左转或右转。暴力做法就像让你把每一种可能的转向顺序全部写在纸上，然后逐一检查哪一种最后正好站在 `endPos`。

只要把所有可能的「左/右」序列都生成出来，统计其中满足条件的序列数即可。  

#### 代码（Python）

```python
MOD = 10**9 + 7

def brute_force(startPos: int, endPos: int, k: int) -> int:
    """
    暴力递归：遍历所有 2^k 种走法，统计恰好在第 k 步到达 endPos 的路径数
    """
    def dfs(pos: int, steps: int) -> int:
        # 已经走了 steps 步
        if steps == k:                     # 基线：走满 k 步
            return 1 if pos == endPos else 0
        # 继续往左或往右走一步
        left = dfs(pos - 1, steps + 1)     # 往左一步
        right = dfs(pos + 1, steps + 1)    # 往右一步
        return (left + right) % MOD

    return dfs(startPos, 0)
```

> **关键行解释**  
> - `if steps == k:` 判断是否已经走完 `k` 步，是递归的结束条件。  
> - `dfs(pos - 1, steps + 1)` 与 `dfs(pos + 1, steps + 1)` 分别对应「左走」和「右走」两条分支。  
> - 最后把左右两条分支的计数相加（取模）得到当前状态的答案。

#### 复杂度

- **时间复杂度**：`O(2^k)`  
  每一步都有两种选择，`k` 步下来总共有 `2^k` 条路径要枚举。`2^k` 在实际编程里可以想象成「每增加一步，可能的走法就翻一番」，当 `k` 达到 30 左右就已经是上千万条，远远超出计算机在 1 秒内能处理的范围。

- **空间复杂度**：`O(k)`  
  递归调用栈的深度最多是 `k`，因此只需要 `k` 层空间。  

> **大白话**：暴力方法就像把所有可能的步序列写成一本厚厚的书，书的页数随 `k` 的增长呈指数级增长，根本不可能在限定时间内读完。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于「枚举每一步的方向」。实际上，我们只关心 **最终** 落在 `endPos` 的方式，而不在乎每一步的具体顺序，只要满足以下两个等式即可：

1. **步数总和**  
   设向右走的次数为 `R`，向左走的次数为 `L`。显然  
   ```
   R + L = k                (所有步数加起来正好是 k 步)
   ```

2. **位移要求**  
   设目标距离 `d = |endPos - startPos|`（绝对值，左/右方向不影响距离）。  
   - 如果 `endPos >= startPos`，则右走的次数比左走多 `d`：  
     `R - L = d`
   - 如果 `endPos < startPos`，则左走的次数比右走多 `d`：  
     `L - R = d`（等价于把 `d` 当成正数，同上式只要把 `d` 取绝对值即可）

把两式相加、相减可以直接求出 `R` 与 `L`：

```
R = (k + d) / 2
L = (k - d) / 2
```

**必须满足的条件**：

- `k >= d` —— 步数不够根本到达目标。  
- `k` 与 `d` 同奇偶（即 `(k - d)` 为偶数），否则 `(k ± d)/2` 不是整数，左/右步数无法取整。

当上述条件都满足时，**路径的不同只体现在「哪 k 步里是向右」**。我们只需要从 `k` 步中挑选 `R` 步当右走，其余自然是左走。挑选的方式数正是组合数：

```
答案 = C(k, R)   （从 k 步中选 R 步作为向右的步）
```

> **类比**：把 `k` 步看成 `k` 张卡片，右走的步子是一种特殊的卡片，需要选出 `R` 张。选哪几张不同，顺序自然已经决定（因为左/右已经固定），于是不同的选法就是不同的走法。

**组合数的计算**  
`k ≤ 1000`，我们可以预先计算 **阶乘** `fact[i] = i! (mod MOD)`，以及 **逆元** `inv_fact[i] = (i!)^{-1} (mod MOD)`，利用公式  

```
C(n, r) = fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD
```

逆元使用 **费马小定理**（因为 `MOD = 1e9+7` 是质数）：

```
a^{-1} ≡ a^{MOD-2} (mod MOD)
```

这样一次预处理 O(k) 时间后，求任意组合数只需 O(1)。

#### 代码（Python）

```python
MOD = 10**9 + 7

def number_of_ways(startPos: int, endPos: int, k: int) -> int:
    """
    最优解：利用组合数计算恰好走 k 步到达 endPos 的方案数
    """
    d = abs(endPos - startPos)          # 必须走的最小距离（绝对值）

    # ① 先判断能否到达：步数够且奇偶相同
    if k < d or (k - d) % 2 != 0:
        return 0

    # ② 计算需要向右走的步数 R（或者向左走的步数 L，二者只要算一个）
    right = (k + d) // 2                # R = (k + d) / 2 必为整数

    # ③ 预计算阶乘和逆元（只需要到 k）
    fact = [1] * (k + 1)
    for i in range(1, k + 1):
        fact[i] = fact[i - 1] * i % MOD

    # 逆元使用快速幂（pow 第三个参数自动取模）
    inv_fact = [1] * (k + 1)
    inv_fact[k] = pow(fact[k], MOD - 2, MOD)   # (k!)^{-1}
    # 由后往前递推求其余逆元：inv_fact[i-1] = inv_fact[i] * i % MOD
    for i in range(k, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    # ④ 组合数 C(k, right) = k! / (right! * (k-right)!)
    ans = fact[k] * inv_fact[right] % MOD
    ans = ans * inv_fact[k - right] % MOD
    return ans
```

> **关键行解释**  
> - `d = abs(endPos - startPos)`：把左/右方向统一为「距离」，不必分别讨论。  
> - `if k < d or (k - d) % 2 != 0:`：两个必要条件的快速检查，直接返回 0。  
> - `right = (k + d) // 2`：求出必须向右的步数（左步数会自动满足 `k-right`）。  
> - `fact[i] = fact[i - 1] * i % MOD`：递推计算阶乘并取模，防止数字爆炸。  
> - `inv_fact[k] = pow(fact[k], MOD - 2, MOD)`：费马小定理求逆元，`pow` 自带模幂运算，时间对数级。  
> - `inv_fact[i - 1] = inv_fact[i] * i % MOD`：逆元的逆向递推，只需 O(k) 而不必每次都用 `pow`。  
> - 最后三行完成组合数的乘法并取模，得到答案。

#### 复杂度

- **时间复杂度**：`O(k)`  
  只需要一次线性遍历来构造阶乘与逆元表，随后组合数查询是常数时间。相比暴力的指数级 `2^k`，提升巨大。  

- **空间复杂度**：`O(k)`  
  用两个长度为 `k+1` 的数组保存阶乘和逆元。`k ≤ 1000`，几千个整数的空间在现代机器上几乎可以忽略不计。

> 与暴力解对比：  
> - 暴力 `O(2^k)` 随 `k` 指数增长，几乎不可能在 `k = 1000` 时跑完。  
> - 最优解 `O(k)` 线性增长，即使 `k = 1000` 也只需要几千次简单运算，轻松在毫秒级完成。

---

## 心得

- **核心技巧**：把「路径」转化为「组合」——只要知道向右（或向左）需要走多少步，路径的不同仅在于这些步出现的顺序，使用组合数直接计数。  
- **适用的题型**  
  1. “在 k 步内从 A 到 B 的不同走法” 系列（如 LeetCode 1266、2024 等）。  
  2. “给定正负步长的总和为目标值的计数” 类的组合/排列问题。  
  3. “在固定步数内达到某个高度/距离”的 DP/组合混合题。  
- **一句话总结**：**把步数分配为“右多少、左多少”，再用组合数 `C(k, right)` 直接算出所有排列**。

---

## 反思

- **第一反应**：把每一步都列举出来，写递归或 BFS——这自然是最容易想到的办法，却忽略了步序列的对称性。  
- **最容易踩的坑**  
  - 忘记检查 **奇偶性**：`k` 与目标距离 `d` 必须同奇偶，否则 `(k±d)/2` 不是整数，导致错误的负数或非整数步数。  
  - 直接使用普通阶乘会导致 **整数溢出**，必须在每一步取模并使用模逆元。  
  - 当 `k < d` 时直接返回 0，防止后面出现负数索引。  
- **下次遇到同类题**：第一步先 **写出“右步数 = (k + distance)/2”**，检查合法性；合法后立即转向 **组合数** 计数，而不是继续枚举。这样思路清晰、实现简洁且高效。