# #1808. 最大化好因子的数量 / Maximize Number of Nice Divisors

> 难度：困难 · 标签：Math、Recursion、Number Theory · [LeetCode 链接](https://leetcode.com/problems/maximize-number-of-nice-divisors/)

---

## 题目（英文原版）

**Description**

You are given a positive integer primeFactors. You are asked to construct a positive integer n that satisfies the following conditions:
Return the number of nice divisors of n. Since that number can be too large, return it modulo 109 + 7.
Note that a prime number is a natural number greater than 1 that is not a product of two smaller natural numbers. The prime factors of a number n is a list of prime numbers such that their product equals n.

**Examples**

**Example 1:**

```
Input: primeFactors = 5
Output: 6
Explanation: 200 is a valid value of n.
It has 5 prime factors: [2,2,2,5,5], and it has 6 nice divisors: [10,20,40,50,100,200].
There is not other value of n that has at most 5 prime factors and more nice divisors.
```

**Example 2:**

```
Input: primeFactors = 8
Output: 18
```

**Constraints**

- 1 <= primeFactors <= 109

---

## 题目（中文翻译）

**题目描述**  
给定一个正整数 `primeFactors`。请构造一个正整数 `n`，使得 `n` 的质因子（prime factors）的总个数（计数时考虑重复）恰好等于 `primeFactors`，并且 `n` 的好因子（nice divisor）的数量尽可能多。返回能够得到的最大好因子数量。由于答案可能非常大，请返回该数量对 `10^9 + 7` 取模后的结果。

**好因子（nice divisor）定义**  
如果 `d` 是 `n` 的一个因子且 `d` 能被 `n` 的所有不同质因子整除，则称 `d` 为 `n` 的好因子。换句话说，`d` 必须同时包含 `n` 的每个质因子（至少出现一次）。

**约束条件**  
- `1 <= primeFactors <= 10^9`

**示例**

#### 示例 1
```
Input: primeFactors = 5
Output: 6
Explanation: 200 是一个合法的 n。  
它的质因子为 [2,2,2,5,5]（共 5 个），并且它拥有 6 个好因子：  
[10, 20, 40, 50, 100, 200]。  
不存在其他 n 在质因子不超过 5 个的前提下拥有更多的好因子。
```

#### 示例 2
```
Input: primeFactors = 8
Output: 18
```

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **把 `primeFactors` 看成一个整数 `n`，把它拆成若干个正整数的和**（每个正整数代表某个不同质因子的出现次数）。  
2. 对每一种拆分方式，计算这些正整数的乘积——这就是对应的 “nice divisors” 个数。  
3. 把所有拆分方式的乘积取最大值，就是答案。

> **类比**：把 `primeFactors` 当成一块巧克力，要求把它切成若干块（每块大小 ≥1），每种切法对应一种“分配方案”。每块的大小乘起来得到的分数越大，说明这块巧克力切得越“值”。我们只要找出分数最高的切法即可。

**为什么正确**  
- 任意合法的整数 `n` 都可以唯一写成若干质因子的乘积  
  \[
  n = p_1^{e_1}\;p_2^{e_2}\;\dots\;p_k^{e_k},
  \]  
  其中 `e_i`（即每种质因子的出现次数）之和恰好等于 `primeFactors`。  
- “nice divisor” 必须同时包含所有不同的质因子，因而对第 `i` 种质因子，它可以取 `1 … e_i` 次方的任意次数。可选次数的种类数正好是 `e_i`，所以所有 nice divisor 的总数是  
  \[
  \text{nice}(n)=\prod_{i=1}^{k} e_i .
  \]  
- 因此，只要遍历所有可能的 `e_i` 组合（即所有把 `primeFactors` 拆成若干正整数的方式），取乘积的最大值即可。

#### 代码（Python）

```python
from typing import List

def max_nice_bruteforce(primeFactors: int) -> int:
    """
    暴力递归枚举所有把 primeFactors 拆成若干正整数的方式，
    计算每种方式的乘积，返回最大乘积（不取模）。
    仅适用于 primeFactors 很小的情况。
    """
    best = 0                         # 记录目前找到的最大乘积

    def dfs(remaining: int, last: int, cur_prod: int):
        """
        remaining : 还剩多少个质因子要分配
        last      : 为了避免排列重复，只允许取 >= last 的数
        cur_prod  : 已经选好的数的乘积
        """
        nonlocal best
        if remaining == 0:            # 正好分配完
            best = max(best, cur_prod)
            return
        # 试着取一个数 i（i >= last，且 i <= remaining）
        for i in range(last, remaining + 1):
            dfs(remaining - i, i, cur_prod * i)

    dfs(primeFactors, 1, 1)
    return best
```

> **关键行中文注释**  
> - `dfs` 是深度优先搜索，递归地把剩余的质因子 `remaining` 分配成一个个正整数 `i`。  
> - `last` 用来保证拆分顺序不变（比如 `2+3` 与 `3+2` 视为同一种拆法），避免重复计算。  
> - 当 `remaining` 为 0 时，说明已经得到一种完整的拆分，更新全局最大乘积 `best`。

#### 复杂度  

- **时间复杂度**：  
  暴力枚举所有整数划分的数量是 **分拆数**（partition number），大约是 `exp(O(sqrt(primeFactors)))`，对 `primeFactors = 30` 已经有上万种情况。可以粗略记为 **指数级**，即 `O(2^primeFactors)`（实际更慢）。  
  > 大白话：随着 `primeFactors` 增大，计算时间会“炸裂”，几秒钟能算完的范围只能到十几左右。

- **空间复杂度**：  
  递归深度最多等于 `primeFactors`，每层保存常数个变量，故为 `O(primeFactors)`（栈空间）。  

---

### 2. 最优解

#### 思路  

从暴力解可以看出：**本质是把一个正整数 `primeFactors` 拆成若干正整数，使它们的乘积最大**。这其实是一个经典的“整数拆分求最大乘积”问题。我们要找出一种通用且高效的拆分规则。

1. **观察 “大数拆成小数会更好”**  
   - 若某个拆分块 `x ≥ 5`，把它换成 `2` 与 `x‑2`（或者更一般的 `⌊x/2⌋` 与 `⌈x/2⌉`），乘积会变大。  
   - 证明：设 `a = ⌊x/2⌋ , b = ⌈x/2⌉`，则 `a·b = a·(x‑a) = ax - a²`。对 `a = x/2`（即均分）可以得到 `a·b ≥ x`，且当 `x > 4` 时严格大于 `x`。  
   - **结论**：最优解里不会出现大于 `4` 的块。

2. **只剩 2、3、4**  
   - `4` 再继续拆成 `2+2`，乘积不变（`2·2 = 4`），所以我们可以把所有的 `4` 替换成两个 `2`，不影响最优性。  
   - 因此**只需要考虑 2 与 3**。

3. **3 更优于 2**  
   - `3·3 = 9` 大于 `2·2·2 = 8`，所以在能用 `3` 的地方尽量使用 `3`。  
   - 但 **三个 2** (`2+2+2`) 可以被 **两个 3** (`3+3`) 替换，乘积从 `8` 提升到 `9`。因此**最多只会出现两个 2**（否则可以改成更多的 3）。

4. **余数处理**  
   - 把 `primeFactors` 尽可能多地划分成 `3`（即 `cnt3 = primeFactors // 3`），剩余 `r = primeFactors % 3`。  
   - `r = 0`：全是 `3`，答案 `3^{cnt3}`。  
   - `r = 1`：直接留下一个 `1` 会导致乘积不变（因为乘以 1 不增益），所以把一个 `3` 拆成 `2+2`，即 `cnt3‑1` 个 `3` 加两个 `2`，乘积 `3^{cnt3‑1}·4`。  
   - `r = 2`：保留一个 `2`，即 `cnt3` 个 `3` 再乘以 `2`，乘积 `3^{cnt3}·2`。

5. **取模**  
   - 题目要求对 `10^9+7` 取模。指数可能非常大（`primeFactors` 最高 10⁹），所以使用 **快速幂**（二进制指数）在 `O(log exponent)` 时间内完成取模乘法。

> **类比**：想象你有 `primeFactors` 块糖果，要把它们拼成若干颗“糖球”。每颗糖球的体积越大，它的“价值”（乘积）越高。但如果一颗糖球太大（≥5），把它拆成两颗相等的糖球会让总价值上升。最终，你会发现只需要做 2 块或 3 块的糖球，且尽量多做 3 块——因为 3 块的性价比最高。剩下的 1 块只能和一个 3 合并成两个 2。

#### 代码（Python）

```python
MOD = 10**9 + 7

def mod_pow(base: int, exp: int) -> int:
    """
    快速幂：在 O(log exp) 时间内计算 (base ** exp) % MOD
    """
    result = 1
    base %= MOD               # 防止 base 本身超出范围
    while exp > 0:
        if exp & 1:           # exp 为奇数时，乘入当前 base
            result = (result * base) % MOD
        base = (base * base) % MOD   # base 翻倍（相当于平方）
        exp >>= 1            # exp //= 2
    return result

def maxNiceDivisors(primeFactors: int) -> int:
    """
    最优解：只用 2 与 3 进行划分，返回乘积对 1e9+7 取模后的结果。
    """
    if primeFactors <= 3:          # 小于等于 3 时直接返回自身
        return primeFactors

    cnt3, rem = divmod(primeFactors, 3)   # cnt3 = primeFactors // 3, rem = %3

    if rem == 0:
        # 全部是 3
        return mod_pow(3, cnt3)
    elif rem == 1:
        # 把一个 3 拆成两个 2，乘积 3^(cnt3-1) * 4
        return (mod_pow(3, cnt3 - 1) * 4) % MOD
    else:   # rem == 2
        # 直接加一个 2，乘积 3^cnt3 * 2
        return (mod_pow(3, cnt3) * 2) % MOD
```

> **关键行中文注释**  
> - `mod_pow` 使用二进制拆分指数，循环次数约为 `log₂(exp)`，即使 `exp` 为 10⁹ 也只需要约 30 次迭代。  
> - `divmod` 同时得到商 `cnt3` 与余数 `rem`，代码更简洁。  
> - 三种余数情况分别对应前面推导的三种最优拆分方式。

#### 复杂度  

- **时间复杂度**：`O(log primeFactors)`（快速幂的对数时间），因为只做了常数次的乘法与一次对数次的幂运算。  
  > 与暴力解的指数级时间相比，几乎是瞬间完成，即使 `primeFactors = 10⁹` 也只需要约 30 次循环。

- **空间复杂度**：`O(1)`，只使用了若干个整数变量，没有递归或额外的数据结构。

---

## 心得  

- **核心技巧**：整数拆分的“最大乘积”策略——尽可能使用 3，余数为 1 时改成两个 2。  
- **适用题型**（类似思路可复用）：  
  1. LeetCode 343 – “整数拆分”  
  2. LeetCode 1563 – “石子游戏 V” 中的分段最大乘积  
  3. “最大化产品的子数组” 这类需要把总和固定的情况下求乘积最大的问题。  
- **一句话总结解题钥匙**：**把所有大于 4 的块拆成 2 与 3，只保留最多两个 2，其余全是 3**。

---

## 反思  

- **第一反应**：看到 “primeFactors” 与 “nice divisor” 立刻想到质因子指数的乘积，进而想到“把总和拆成若干整数求最大乘积”。  
- **最容易踩的坑**：  
  - 忽视 `primeFactors ≤ 3` 的特殊处理（直接返回自身），会导致 `cnt3‑1` 为负数。  
  - 余数为 1 时忘记把一个 3 拆成两个 2，导致答案偏小。  
  - 在取模时直接使用 `pow(3, cnt3, MOD)` 也是可行的，但若自行实现快速幂，必须注意 `base %= MOD` 防止溢出。  
- **下次类似题的第一步**：**先判断是否可以把问题转化为“固定和的整数划分求最大乘积”，然后记住“3 是最优块，余数为 1 时用两个 2 替代一个 3”。**