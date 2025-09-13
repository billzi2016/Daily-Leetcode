# #3343. **平衡排列的计数** / Count Number of Balanced Permutations

> 难度：困难 · 标签：Math、String、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-number-of-balanced-permutations/)

---

## 题目（英文原版）

**Description**

You are given a string num. A string of digits is called balanced if the sum of the digits at even indices is equal to the sum of the digits at odd indices.
Return the number of distinct permutations of num that are balanced.
Since the answer may be very large, return it modulo 109 + 7.
A permutation is a rearrangement of all the characters of a string.

**Examples**

**Example 1:**

```
Input: num = "123"
Output: 2
Explanation:
```

**Example 2:**

```
Input: num = "112"
Output: 1
Explanation:
```

**Example 3:**

```
Input: num = "12345"
Output: 0
Explanation:
```

**Constraints**

- 2 <= num.length <= 80
- num consists of digits '0' to '9' only.

---

## 题目（中文翻译）

You are given a string `num`. A string of digits is called **balanced**（平衡的） if the sum of the digits at even indices is equal to the sum of the digits at odd indices.  
Return the number of distinct permutations（全排列） of `num` that are balanced.  
Since the answer may be very large, return it modulo `10^9 + 7`.  
A permutation is a rearrangement of all the characters of a string.

**Example 1:**  
**Example 2:**  
**Example 3:**  

**Constraints:**

**示例：**  

**示例 1:**  
Input: `num = "123"`  
Output: `2`  
**解释：**  

**示例 2:**  
Input: `num = "112"`  
Output: `1`  
**解释：**  

**示例 3:**  
Input: `num = "12345"`  
Output: `0`  
**解释：**  

**约束条件：**  
- `2 <= num.length <= 80`  
- `num` 仅由字符 `'0'` 到 `'9'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 `num` 的所有字符全排列列举出来，逐个检查：

1. 先把字符串里每个字符的顺序全部换一种（全排列）。  
2. 把得到的排列当成新的字符串，分别把下标为 **偶数**（0、2、4 …）的位上的数字相加，得到 `even_sum`；把 **奇数**（1、3、5 …）的位上的数字相加，得到 `odd_sum`。  
3. 如果 `even_sum == odd_sum`，说明这是一条 **平衡** 的排列，计数加一。  

> **类比**：全排列就像把一副扑克牌的顺序全部洗出来，逐一检查每副牌的红黑花色之和是否相等。  
> **数据结构**：我们只需要用 Python 的列表保存当前的排列，`itertools.permutations` 就相当于一台“全排列机器”。  

**为什么一定正确**  
因为我们把 *所有* 可能的排列都枚举了一遍，凡是满足条件的必然被统计，凡是不满足的必然被过滤掉。

**时间/空间复杂度**  
- **时间**：字符串长度记为 `n`，全排列的数量是 `n!`（即 `n` 的阶乘）。每一次检查要遍历 `n` 个字符求和，所以总时间是 `O(n! × n)`。  
  - `O` 符号里的 `n!` 代表“超指数级”，比如 `n=8` 时已经是 `40320`，`n=10` 时是 `3628800`，几乎不可能在计算机里跑完。  
- **空间**：只需要保存当前的一个排列，空间是 `O(n)`。

显然，这种 **暴力** 方法只能在 `n ≤ 8` 左右的小样例上跑通，根本不能应对题目给出的 `n ≤ 80`。

#### 代码（Python）

```python
import itertools

MOD = 10**9 + 7

def count_balanced_bruteforce(num: str) -> int:
    n = len(num)
    # 用 set 去重，防止相同字符导致的重复排列
    seen = set()
    ans = 0

    for perm in itertools.permutations(num):
        if perm in seen:               # 已经统计过的相同排列
            continue
        seen.add(perm)

        even_sum = 0
        odd_sum = 0
        for idx, ch in enumerate(perm):
            digit = int(ch)
            if idx % 2 == 0:           # 偶数下标
                even_sum += digit
            else:                      # 奇数下标
                odd_sum += digit

        if even_sum == odd_sum:
            ans = (ans + 1) % MOD

    return ans
```

#### 复杂度

- 时间复杂度：`O(n! × n)` — 先把所有排列都列出来（`n!`），每个排列再遍历 `n` 位求和。  
- 空间复杂度：`O(n)` — 只存当前的排列和几个计数变量。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有排列**。我们需要在不枚举的前提下，直接统计满足条件的排列数。  
下面一步步把问题抽象出来：

1. **把条件写成等式**  
   - 假设字符串长度为 `n`，偶数下标的个数记为 `E = (n + 1) // 2`，奇数下标的个数记为 `O = n // 2`。  
   - 整个字符串所有数字的和记为 `S`。如果偶数位的和等于奇数位的和，那么必然有  
     \[
     \text{even\_sum} = \text{odd\_sum} = \frac{S}{2}
     \]  
     因此 **`S` 必须是偶数**，否则答案直接为 0。

2. **把问题转化为“选哪些数字放到偶数位”**  
   - 统计每个数字 `0~9` 在原字符串中出现的次数，记为 `cnt[d]`。  
   - 设 `x_d` 为数字 `d` 被放到偶数位的个数（`0 ≤ x_d ≤ cnt[d]`）。  
   - 必须满足两个约束  
     1. **位数约束**：`∑ x_d = E`（恰好占满所有偶数位）  
     2. **和的约束**：`∑ d * x_d = S/2`（偶数位的数字和正好是目标值）  

   只要找到了满足这两个约束的 `(x_0,…,x_9)`，剩下的 `cnt[d] - x_d` 自动落在奇数位，奇数位的和自然也是 `S/2`。

3. **计数每一种合法的分配**  
   - 偶数位内部的排列方式：`E! / (∏ x_d!)`（把 `E` 个位置分配给各数字的多重排列）  
   - 奇数位内部的排列方式：`O! / (∏ (cnt[d] - x_d)!)`  
   - 两者相乘即为该 `x` 向量对应的 **不同排列数**：  
     \[
     \text{ways}(x) = \frac{E! \; O!}{\prod\limits_{d=0}^{9} x_d! \; (cnt[d]-x_d)!}
     \]

4. **动态规划求所有合法 `x` 的贡献**  
   - 由于数字种类只有 10（`0~9`），我们可以按数字逐个“放进去”。  
   - 状态 `dp[i][s][k]` 表示：**已经处理了前 `i` 种数字**（`0 … i-1`），  
     - 偶数位的当前数字和为 `s`，  
     - 已经使用了 `k` 个数字放到偶数位，  
     - **累加的值** 为 `∑ 1/(x_d! (cnt[d]-x_d)!)`（即分母的逆元乘积），这样在最后乘上 `E!·O!` 就得到完整答案。  

   - 转移时，对第 `i` 种数字（记作 `d`）我们可以选 `x`（`0 ≤ x ≤ cnt[d]`）个放到偶数位：  
     \[
     dp[i+1][s + d·x][k + x] \;+=\; dp[i][s][k] \times \text{invFact}[x] \times \text{invFact}[cnt[d]-x]
     \]  
     这里 `invFact[t]` 是 `t!` 的模逆（即 `1 / t! (mod M)`），因为我们要累计分母的乘积。

5. **答案**  
   - 目标和 `target = S // 2`，目标偶数位个数 `E`。  
   - 最终 `dp[10][target][E]`（已经遍历完 0~9）保存了所有合法分配的 **分母逆元乘积之和**。  
   - 乘上 `fact[E] * fact[O]`（即 `E!·O!`），再取模，即得到答案。  

> **类比**：想象有 10 种颜色的球，每种颜色有 `cnt[d]` 个。我们要把这些球分成两盒——“偶数盒”与“奇数盒”。盒子里球的数量和颜色权值（数字本身）必须满足两个条件。DP 就像在一次次把颜色放进盒子时，记录“已经装了多少球、重量是多少”，最后把所有合法的装法加起来。

#### 代码（Python）

```python
MOD = 10**9 + 7

# 预计算 0! ~ 80! 以及它们的模逆元
MAX_N = 80
fact = [1] * (MAX_N + 1)
inv_fact = [1] * (MAX_N + 1)

for i in range(1, MAX_N + 1):
    fact[i] = fact[i - 1] * i % MOD

# 快速幂求逆元（费马小定理，MOD 为质数）
def mod_pow(a: int, e: int) -> int:
    res = 1
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

inv_fact[MAX_N] = mod_pow(fact[MAX_N], MOD - 2)
for i in range(MAX_N, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD


def count_balanced(num: str) -> int:
    n = len(num)
    cnt = [0] * 10                # 统计每个数字出现次数
    total_sum = 0
    for ch in num:
        d = int(ch)
        cnt[d] += 1
        total_sum += d

    # 总和必须为偶数，否则不可能平衡
    if total_sum % 2 == 1:
        return 0

    target = total_sum // 2               # 偶数位需要达到的和
    E = (n + 1) // 2                      # 偶数下标的位数
    O = n // 2                            # 奇数下标的位数

    # dp[i][s][k] 只保留当前 i 层，使用滚动数组降低空间
    # 维度解释：处理到第 i 种数字，和为 s，已经用了 k 个数字放到偶数位
    max_sum = target                       # 只需要关心 ≤ target 的和
    dp = [[[0] * (E + 1) for _ in range(max_sum + 1)] for _ in range(2)]
    cur, nxt = 0, 1
    dp[cur][0][0] = 1                      # 初始状态：什么都没放

    for d in range(10):                    # 按数字 0~9 逐个考虑
        c = cnt[d]
        # 清空 nxt 层
        for s in range(max_sum + 1):
            for k in range(E + 1):
                dp[nxt][s][k] = 0

        # 对当前数字的放置枚举 x（放到偶数位的个数）
        for s in range(max_sum + 1):
            for k in range(E + 1):
                val = dp[cur][s][k]
                if val == 0:
                    continue
                # x 可以从 0 到 c
                for x in range(c + 1):
                    ns = s + d * x
                    nk = k + x
                    if ns > max_sum or nk > E:
                        break          # 超出范围直接跳出
                    add = val * inv_fact[x] % MOD
                    add = add * inv_fact[c - x] % MOD
                    dp[nxt][ns][nk] = (dp[nxt][ns][nk] + add) % MOD

        # 交换角色，准备处理下一个数字
        cur, nxt = nxt, cur

    # dp[cur] 已经是处理完 0~9 的结果
    ways_denominator = dp[cur][target][E]          # Σ 1/(x!·(cnt-x)!)
    ans = ways_denominator * fact[E] % MOD
    ans = ans * fact[O] % MOD
    return ans


# ------------------- 示例 -------------------
if __name__ == "__main__":
    print(count_balanced("123"))    # 2
    print(count_balanced("112"))    # 1
    print(count_balanced("12345"))  # 0
```

> **代码要点解释**  
> 1. `fact` / `inv_fact`：阶乘和阶乘的模逆元，用来快速算 `1 / x!`（因为在模运算下除法要转成乘逆元）。  
> 2. `dp` 使用 **滚动数组**（只保留当前与下一层），把空间从 `10 × 721 × 81` 降到 `2 × 721 × 81`，仍然很小。  
> 3. 内层循环 `for x in range(c + 1)` 负责把第 `d` 种数字的 `x` 个放进偶数位，更新和、已用位数以及分母的逆元乘积。  
> 4. 最后把累计的 “分母逆元乘积” 乘上 `E!·O!`，即得到完整的排列数。  

#### 复杂度

- 时间复杂度：`O(10 × E × target × avg_cnt)`  
  - 实际上等价于 `O(10 × 80 × 720 × 8)`（因为每个数字最多出现 8 次），约 `3.6×10⁵` 次基本运算，远低于 1 秒。  
  - 与暴力解的 `O(n!·n)` 相比，**指数级下降**，可以轻松处理 `n = 80`。  

- 空间复杂度：`O(E × target)` ≈ `O(80 × 720)` ≈ `6×10⁴`，使用滚动数组再除以 2，只有几百 KB。

---

## 心得

- **核心技巧**：把“偶数位和等于奇数位和”转化为“选出恰好 `E` 个数字，使其和为 `S/2`”。随后利用 **多重背包 / 组合计数 DP**（每种数字是一个物品，数量有限）求所有合法选法，再乘以排列的阶乘得到最终答案。  
- **适用的题型**  
  1. **数字/字符分配类**：如 “把字符分成两组，使两组的 ASCII 码和相等”。  
  2. **多重背包计数**：如 “有若干硬币，求恰好组成指定价值的方案数”。  
  3. **平衡序列**：如 “把括号序列平衡成左右相同数量”。  
- **一句话总结**：**把全排列的计数拆成“先挑选放哪儿”，再乘以位置排列的阶乘**，这样就把指数级的枚举压缩成多项式 DP。

---

## 反思

- **第一反应**：直接把所有排列写出来检验——这在面试或比赛里往往是最先想到的，但会因为爆炸的时间复杂度立刻卡住。  
- **最容易踩的坑**  
  1. **总和奇偶性**：忘记先检查 `S` 是否为偶数，导致 DP 仍然跑却返回 0，浪费时间。  
  2. **模逆元**：在计数公式里出现了除法，需要用 `fact` 的模逆元来代替，否则会出现除不尽的错误。  
  3. **位数不均**：当 `n` 为奇数时，偶数位比奇数位多 1，必须用 `(n+1)//2` 来计算 `E`，否则约束会错位。  
- **下次类似题的第一步**：**先把约束写成等式/不等式，检查是否可以用“选取子集满足和/个数”来描述**，随后考虑使用 “多重背包 DP + 组合计数” 来统计。这样可以快速跳过暴力搜索，直接进入可行的多项式解法。