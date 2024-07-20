# #2787. 整数表示为幂之和的方案数 / Ways to Express an Integer as Sum of Powers

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/ways-to-express-an-integer-as-sum-of-powers/)

---

## 题目（英文原版）

**Description**

Given two positive integers n and x.
Return the number of ways n can be expressed as the sum of the xth power of unique positive integers, in other words, the number of sets of unique integers [n1, n2, ..., nk] where n = n1x + n2x + ... + nkx.
Since the result can be very large, return it modulo 109 + 7.
For example, if n = 160 and x = 3, one way to express n is n = 23 + 33 + 53.

**Examples**

**Example 1:**

```
Input: n = 10, x = 2
Output: 1
Explanation: We can express n as the following: n = 32 + 12 = 10.
It can be shown that it is the only way to express 10 as the sum of the 2nd power of unique integers.
```

**Example 2:**

```
Input: n = 4, x = 1
Output: 2
Explanation: We can express n in the following ways:
- n = 41 = 4.
- n = 31 + 11 = 4.
```

**Constraints**

- 1 <= n <= 300
- 1 <= x <= 5

---

## 题目（中文翻译）

给定两个正整数 `n` 和 `x`。  
返回将 `n` 表示为 **唯一的正整数 (unique positive integers)** 的 `x` 次幂 (xth power) 之和的方案数，即满足  

```
n = n1^x + n2^x + ... + nk^x
```  

的 **集合 (sets)** `[n1, n2, ..., nk]` 的个数。  
由于结果可能非常大，请返回 **取模 (modulo)** `10^9 + 7` 后的值。  

例如，`n = 160` 且 `x = 3` 时，一种表达方式为 `160 = 2^3 + 3^3 + 5^3`。  

**示例 1**  
**输入**  
```
n = 10, x = 2
```  
**输出**  
```
1
```  
**解释**  
我们可以这样表达 `n`：`10 = 3^2 + 1^2 = 10`。  
可以证明，这是一唯一的将 `10` 表示为唯一整数的二次幂之和的方案。  

**示例 2**  
**输入**  
```
n = 4, x = 1
```  
**输出**  
```
2
```  
**解释**  
我们可以这样表达 `n`：  
- `4 = 4^1 = 4`。  
- `4 = 3^1 + 1^1 = 4`。  

**约束条件**  
- `1 <= n <= 300`  
- `1 <= x <= 5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把所有可能的正整数 **逐个尝试**，看能不能挑出一部分（且每个数只能选一次）使它们的 **x 次方** 加起来正好等于 `n`。  
这其实就是 **“背包/子集和”** 的暴力搜索，只是背包里的“重量”是 `i**x`，而我们要求恰好装满容量 `n`。

- **数据结构**：用一个列表 `candidates = [1, 2, 3, …]` 保存所有可以使用的基数。  
  - 这里的列表可以类比为 **字典**，只不过我们只关心“词”（基数）本身，不需要查“页码”。  
- **递归/回溯**：从小到大遍历 `candidates`，每次决定 **选** 或 **不选** 当前基数的 `x 次方`。  
  - 选了就把 `n` 减去该基数的 `x 次方`，继续往后找；不选则直接往后找。  
- **终止条件**：  
  - `n == 0` → 找到一种合法组合，计数 +1。  
  - `n < 0` 或者已经没有更大的基数可以选了 → 这条路走不通，直接返回。

> **为什么一定对？**  
> 因为我们遍历了 **所有** 可能的基数组合（每个基数要么出现，要么不出现），只要有一种组合满足 `sum(i**x) = n`，递归一定会走到 `n == 0`，于是计数。

#### 代码（Python）  
```python
MOD = 10 ** 9 + 7

def count_ways_bruteforce(n: int, x: int) -> int:
    # 先算出所有可能的基数（因为 i**x 不能超过 n）
    max_base = int(round(n ** (1.0 / x)))   # 最大的 i，使得 i**x <= n
    bases = list(range(1, max_base + 1))

    def dfs(idx: int, remaining: int) -> int:
        """从 bases[idx:] 中挑选，剩余需要凑的和为 remaining"""
        if remaining == 0:          # 正好凑出 n
            return 1
        if remaining < 0 or idx == len(bases):
            return 0                # 超支或已没有基数可选

        # 不选当前基数
        ways = dfs(idx + 1, remaining)

        # 选当前基数（唯一一次，保证不重复）
        power = bases[idx] ** x
        ways += dfs(idx + 1, remaining - power)

        return ways % MOD          # 防止递归层数太深导致整数爆炸

    return dfs(0, n)
```

#### 复杂度  
- **时间复杂度**：`O(2^m)`，其中 `m` 是可选基数的个数（约等于 `n^{1/x}`）。  
  - 直观解释：每个基数都有两种决定（选或不选），所以总共会尝试 `2 * 2 * … * 2 = 2^m` 种组合。  
- **空间复杂度**：`O(m)`，递归栈的深度最多等于基数个数。  

> 当 `n = 300, x = 1` 时，`m = 300`，`2^300` 是天文数字，显然暴力不可行。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到 **瓶颈** 在于“每条路径都要走到最底”。  
我们其实只关心 **“子问题的答案”**，而不是每条完整的路径。  
这正是 **动态规划（DP）** 能帮忙的地方——把“大问题”拆成“小问题”，把已经算好的结果记下来，后面再需要时直接查表。

**子问题定义**  
> `dp[i][j]` = 用 **不大于 j 的基数**（即只能使用 `1…j`）的 **x 次方**，凑出和为 `i` 的方案数。

- `i` 表示目标和，范围 `0 … n`。  
- `j` 表示可选的最大基数，范围 `0 … max_base`（`max_base` 同上）。

**递推公式**  
对于当前的 `j`，我们有两种选择：

1. **不使用 j**：方案数等于 `dp[i][j-1]`（只用更小的基数）。
2. **使用 j**：前提是 `i >= j**x`，此时把 `j**x` 从目标和里减掉，剩下的 `i - j**x` 必须用 **不大于 j-1 的基数** 完成，方案数为 `dp[i - j**x][j-1]`。

于是：
```
dp[i][j] = dp[i][j-1]                      # 不选 j
if i >= j**x:
    dp[i][j] += dp[i - j**x][j-1]          # 选 j
dp[i][j] %= MOD
```

**初始化**  
- `dp[0][*] = 1`：凑出 0 的唯一方法是“什么也不选”。  
- `dp[*][0] = 0`（除 `dp[0][0]` 之外）：如果没有任何基数可用，正数目标和根本凑不出来。

**求答案**  
最终答案就是 `dp[n][max_base]`——使用所有可能的基数，凑出目标 `n`。

**空间优化**  
注意到递推只用到 `j-1` 那一列，于是可以把二维数组压成 **一维**：`dp[i]` 表示当前考虑的最大基数为 `j` 时的方案数。遍历 `j` 时，要 **倒序** 更新 `i`，防止同一轮中把已经使用了 `j` 的结果再次加进去。

#### 代码（Python）  
```python
MOD = 10 ** 9 + 7

def count_ways_dp(n: int, x: int) -> int:
    # 计算所有可能的基数上限
    max_base = int(round(n ** (1.0 / x)))
    # dp[i] 表示在当前遍历到的最大基数 j 时，凑出 i 的方案数
    dp = [0] * (n + 1)
    dp[0] = 1                     # “凑出 0” 的基准

    # 逐个加入基数 1, 2, ..., max_base
    for base in range(1, max_base + 1):
        power = base ** x
        # 必须倒序遍历 i，防止本轮中同一个 base 被重复使用
        for i in range(n, power - 1, -1):
            # dp[i - power] 已经是“只用更小基数”时的方案数
            dp[i] = (dp[i] + dp[i - power]) % MOD

    return dp[n]
```

#### 复杂度  
- **时间复杂度**：`O(n * max_base)`。  
  - 直白解释：外层遍历所有基数（最多约 `n^{1/x}` 次），内层遍历目标和 `0…n`，所以总操作数约为 `n * n^{1/x}`。  
  - 以最大约束 `n=300, x=1` 为例，`max_base = 300`，时间约为 `300 * 300 = 90,000`，在一毫秒级别可以轻松跑完。  
- **空间复杂度**：`O(n)`，只用了长度为 `n+1` 的一维数组。  

> 与暴力的 `2^m` 相比，DP 把指数级别降到了多项式级别，真正可以在限制范围内通过。

---

## 心得  

- **核心技巧**：把“唯一整数的 x 次方之和”看成**背包/子集和**问题，用**动态规划**把每个基数的选择状态记录下来。  
- **适用场景**（类似题目）  
  1. “完全平方数的组合数” – 统计把 `n` 表示为若干不同平方数之和的方案数。  
  2. “不同硬币凑金额” – 每种硬币只能使用一次，求凑出目标金额的方案数。  
  3. “不同字母的子序列计数” – 把字符当作“基数”，只允许每个字符出现一次。  
- **一句话总结**：**“把每个可选的幂看成背包里的唯一物品，用 DP 记录‘用前 i 件物品能凑出多少’”。**  

---

## 反思  

- **第一反应**：直接写递归暴力搜索，想把所有组合枚举出来。  
- **最容易踩的坑**  
  - **基数上限**：忘记只取 `i**x <= n` 的基数，导致不必要的递归或数组越界。  
  - **重复计数**：在 DP 中如果正向遍历 `i`，同一个基数会被多次计入，需要倒序遍历保证“只能选一次”。  
  - **模运算**：答案可能非常大，忘记在每一步取模会导致整数溢出或运行超时。  
- **下次思路**：看到“唯一的、幂次/权值”这种**只能使用一次**的组合问题时，第一时间想到 **0/1 背包 DP**（即子集和 DP），并先确定状态转移方程再写代码。