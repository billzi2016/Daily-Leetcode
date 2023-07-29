# #2338. 统计理想数组的数量 / Count the Number of Ideal Arrays

> 难度：困难 · 标签：Math、Dynamic Programming、Combinatorics、Number Theory · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-ideal-arrays/)

---

## 题目（英文原版）

**Description**

You are given two integers n and maxValue, which are used to describe an ideal array.
A 0-indexed integer array arr of length n is considered ideal if the following conditions hold:
Return the number of distinct ideal arrays of length n. Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 2, maxValue = 5
Output: 10
Explanation: The following are the possible ideal arrays:
- Arrays starting with the value 1 (5 arrays): [1,1], [1,2], [1,3], [1,4], [1,5]
- Arrays starting with the value 2 (2 arrays): [2,2], [2,4]
- Arrays starting with the value 3 (1 array): [3,3]
- Arrays starting with the value 4 (1 array): [4,4]
- Arrays starting with the value 5 (1 array): [5,5]
There are a total of 5 + 2 + 1 + 1 + 1 = 10 distinct ideal arrays.
```

**Example 2:**

```
Input: n = 5, maxValue = 3
Output: 11
Explanation: The following are the possible ideal arrays:
- Arrays starting with the value 1 (9 arrays): 
   - With no other distinct values (1 array): [1,1,1,1,1] 
   - With 2nd distinct value 2 (4 arrays): [1,1,1,1,2], [1,1,1,2,2], [1,1,2,2,2], [1,2,2,2,2]
   - With 2nd distinct value 3 (4 arrays): [1,1,1,1,3], [1,1,1,3,3], [1,1,3,3,3], [1,3,3,3,3]
- Arrays starting with the value 2 (1 array): [2,2,2,2,2]
- Arrays starting with the value 3 (1 array): [3,3,3,3,3]
There are a total of 9 + 1 + 1 = 11 distinct ideal arrays.
```

**Constraints**

- 2 <= n <= 104
- 1 <= maxValue <= 104

---

## 题目（中文翻译）

给定两个整数 `n` 和 `maxValue`，用它们来描述一个 **理想数组（ideal array）**。

一个下标从 0 开始、长度为 `n` 的整数数组 `arr` 若满足以下条件，则被视为理想数组：

1. `1 <= arr[0] <= maxValue`；
2. 对于所有 `1 <= i < n`，都有 `arr[i]` 是 `arr[i‑1]` 的倍数。

返回长度为 `n` 的不同理想数组的数量。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

---

### 示例

#### 示例 1
**输入**  
`n = 2, maxValue = 5`

**输出**  
`10`

**解释**  
以下是所有可能的理想数组：

- 以值 `1` 开头的数组（5 种）：`[1,1]`, `[1,2]`, `[1,3]`, `[1,4]`, `[1,5]`
- 以值 `2` 开头的数组（2 种）：`[2,2]`, `[2,4]`
- 以值 `3` 开头的数组（1 种）：`[3,3]`
- 以值 `4` 开头的数组（1 种）：`[4,4]`
- 以值 `5` 开头的数组（1 种）：`[5,5]`

共计 `10` 种。

#### 示例 2
**输入**  
`n = 5, maxValue = 3`

**输出**  
`11`

**解释**  
以下是所有可能的理想数组：

- 以值 `1` 开头的数组（9 种）  
  - 不含其他不同值的情况（1 种）：`[1,1,1,1,1]`  
  - 第二个不同值为 `2` 的情况（4 种）：`[1,1,1,1,2]`, `[1,1,1,2,2]`, `[1,1,2,2,2]`, `[1,2,2,2,2]`  
  - 第二个不同值为 `3` 的情况（4 种）：`[1,1,1,1,3]`, `[1,1,1,3,3]`, `[1,1,3,3,3]`, `[1,3,3,3,3]`

- 以值 `2` 开头的数组（2 种）  
  - `[2,2,2,2,2]`  
  - `[2,2,2,2,4]`（但由于 `maxValue = 3`，该数组不合法，实际只剩 `[2,2,2,2,2]`，所以计数为 1）  

- 以值 `3` 开头的数组（0 种）  

总计 `11` 种合法理想数组。

---

### 约束

- `2 <= n <= 10^4`
- `1 <= maxValue <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的数组枚举出来**，然后逐个检查它们是否满足 “理想数组” 的两个条件：

1. **非递减**（array[i] ≤ array[i+1]）  
   - 可以把它想象成排队：后面的人不能比前面的人矮。  
2. **后面的数是前面数的倍数**（array[i+1] % array[i] == 0）  
   - 把它类比成“字典查词”：每个词（前面的数）都有一页码（后面的数），后面的页码一定是前面页码的整数倍。

枚举时我们只需要在 `[1 … maxValue]` 的范围内挑选 `n` 个数，保持非递减顺序即可。  
检查完所有数组后，计数就是答案。

> **为什么这个方法一定对？**  
> 因为我们没有遗漏任何可能的数组：所有满足约束的数组都在枚举的搜索树里出现。只要检查条件正确，就一定得到正确的计数。

> **时间/空间分析**  
> - **时间**：每个位置可以选 `maxValue` 种数，长度为 `n`，所以最坏情况是 `O(maxValue^n)`。  
>   对于 `n = 10⁴、maxValue = 10⁴` 这种规模，这个指数级时间根本不可接受。  
> - **空间**：递归深度为 `n`，再加上保存当前数组的空间，都是 `O(n)`，这在理论上是可以的，但时间已经让它失去意义。

> **大白话解释**：  
> `O(maxValue^n)` 就像在一棵每层有 `maxValue` 条枝的树上走 `n` 步，枝条数会指数级增长，走到第 10 步已经有 `maxValue^10` 条不同的路径，根本不可能在电脑里跑完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def count_ideal_bruteforce(n: int, maxValue: int) -> int:
    """暴力枚举全部非递减数组，检查是否为理想数组"""
    ans = 0
    arr = [0] * n                     # 用来存当前递归路径的数组

    def dfs(pos: int, last: int):
        """在第 pos 位填数，要求不小于 last（保证非递减）"""
        nonlocal ans
        if pos == n:                  # 已经填满 n 位
            # 检查是否满足“后者是前者的倍数”这一条件
            ok = True
            for i in range(n - 1):
                if arr[i + 1] % arr[i] != 0:
                    ok = False
                    break
            if ok:
                ans = (ans + 1) % MOD
            return

        # 在合法范围 [last, maxValue] 内枚举当前位的数
        for v in range(last, maxValue + 1):
            arr[pos] = v
            dfs(pos + 1, v)           # 递归填下一位

    dfs(0, 1)                         # 从第 0 位开始，最小值是 1
    return ans
```

> **关键注释**  
> - `last` 参数保证了数组始终保持非递减。  
> - 当数组填满后，用一次遍历检查 “倍数” 条件。  

#### 复杂度

- **时间复杂度**：`O(maxValue^n)`  
  - 含义：搜索树的每一层有 `maxValue` 条分支，深度是 `n`，总节点数呈指数增长，根本不可算。  
- **空间复杂度**：`O(n)`  
  - 只保存递归栈和当前数组，随 `n` 线性增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 完全在于 **枚举所有数组**。我们需要 **把枚举的过程压缩**，只统计满足条件的数组数量，而不真的生成它们。

观察题目可以得到两条关键性质：

1. **非递减 + 每个后者是前者的倍数 ⇒**  
   若把数组中 **不同的数** 按出现顺序取出来，这些数必然 **严格递增**（因为相等的数已经被归类为同一个“块”），并且每个数仍然是前一个数的倍数。  
   换句话说，一个理想数组可以看成：
   - 先选出一条 **严格递增且相邻数互为倍数** 的“骨架”，长度记为 `k`（`k` ≤ `n`）。  
   - 再把这 `k` 个不同的数 **按任意方式填满 n 个位置**，只要保持非递减即可——这相当于把 `n` 个位置划分成 `k` 组，每组内部全是同一个数。

2. **把第 1 步的骨架计数 + 第 2 步的组合数相乘** 就得到完整答案。  
   - 第 1 步可以用 **动态规划（DP）** 来统计所有可能的严格递增骨架。  
   - 第 2 步只和 `n` 与 `k` 有关，完全可以用 **组合数学**（“把 n‑1 个分隔符放进 k‑1 个槽里”）来算。

下面一步步展开这两个子问题。

---

#### 2.1 动态规划统计“严格递增且相邻数互为倍数”的序列

设 `dp[l][v]` 表示 **长度为 `l`、以数 `v` 结尾** 的递增骨架的数量（这里的递增保证了所有数互不相同）。  

- 初始状态：`dp[1][v] = 1`，因为长度为 1、结尾为 `v` 的序列只有 `[v]` 一种。  
- 转移：要在 `v` 前面再加一个数 `u`，必须满足 `u | v`（`u` 能整除 `v`）且 `u < v`。于是  

```
dp[l][v] = Σ dp[l-1][u]   (u 为 v 的所有真因子)
```

这一步可以把 “所有能接在 v 前面的数” 看成 **“v 的因子集合”**，就像查字典时“词条”指向它的“解释”。  

实现细节：

- 为了快速得到每个 `v` 的因子列表，先 **预处理所有数的因子**（时间 `O(maxValue log maxValue)`）。  
- `l` 最大只需要到 `log₂(maxValue)`，因为每次至少翻倍，长度再大也不可能在 `maxValue` 范围内继续递增。对 `maxValue ≤ 10⁴`，`log₂` 约为 14，足够小。

---

#### 2.2 组合数学：把骨架扩展成完整的理想数组

假设我们已经得到一个长度为 `k` 的骨架 `[b₁, b₂, …, b_k]`（严格递增且相邻互为倍数）。  
要把它变成长度为 `n` 的完整数组，只需要决定 **每个数出现多少次**，且这些次数之和等于 `n`，顺序自然保持非递减。

这等价于把 `n` 个位置中的 **`n-1` 个间隔**（想象成 `|`）放进 **`k-1` 个“箱子”**（每两个相邻的不同数之间必须至少有一个间隔），于是：

```
方式数 = C(n-1, k-1)
```

其中 `C` 表示组合数 “从 n‑1 个位置中挑 k‑1 个”。  
这一步只依赖 `n` 与 `k`，与具体的数值 `b_i` 完全无关。

---

#### 2.3 综合答案

把两部分乘起来并对所有可能的 `k`、`v` 求和：

```
answer = Σ_{k=1}^{maxLen} Σ_{v=1}^{maxValue} dp[k][v] * C(n-1, k-1)
```

- `maxLen` 为 `⌊log₂(maxValue)⌋ + 1`（因为最短的递增骨架是 1，最长的在每一步至少翻倍）。
- 所有运算都在模 `MOD = 1_000_000_007` 下进行。

---

#### 代码（Python）

```python
MOD = 10**9 + 7

def count_ideal_arrays(n: int, maxValue: int) -> int:
    """
    最优解：DP + 组合数学
    复杂度约为 O(maxValue * log maxValue + maxLen * maxValue)
    """
    # ---------- 1. 预处理每个数的因子 ----------
    # 因子列表：factor[v] = 所有能整除 v 且小于 v 的正整数
    factor = [[] for _ in range(maxValue + 1)]
    for d in range(1, maxValue + 1):
        for multiple in range(d * 2, maxValue + 1, d):   # 只收集真因子（不包括自身）
            factor[multiple].append(d)

    # ---------- 2. 动态规划统计严格递增骨架 ----------
    # maxLen 为可能的最长骨架长度（因为每一步至少翻倍）
    import math
    maxLen = int(math.log2(maxValue)) + 1

    # dp[l][v] 用两层列表实现，节约空间只保留上一层
    dp_prev = [0] * (maxValue + 1)   # 对应长度为 l-1 的状态
    dp_curr = [0] * (maxValue + 1)   # 对应长度为 l   的状态

    # 初始化：长度为 1 的序列只有自身一种
    for v in range(1, maxValue + 1):
        dp_prev[v] = 1

    # 存放所有长度的 dp 结果，后面需要遍历求和
    dp_all = [dp_prev[:]]   # dp_all[0] 对应长度 1

    for l in range(2, maxLen + 1):
        # 计算长度为 l 的 dp
        for v in range(1, maxValue + 1):
            total = 0
            for u in factor[v]:          # 所有真因子 u
                total += dp_prev[u]
            dp_curr[v] = total % MOD
        dp_all.append(dp_curr[:])        # 保存本层结果
        dp_prev, dp_curr = dp_curr, [0] * (maxValue + 1)   # 为下一层准备

    # ---------- 3. 预计算组合数 C(n-1, k-1) ----------
    # 使用阶乘 + 逆元（费马小定理）求组合数
    maxK = maxLen                     # k 最大不会超过 maxLen
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)   # 费马小定理求逆元
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD

    def comb(N: int, K: int) -> int:
        """计算 C(N, K)（N, K 均在 0..n 范围）"""
        if K < 0 or K > N:
            return 0
        return fact[N] * inv_fact[K] % MOD * inv_fact[N - K] % MOD

    # ---------- 4. 合并 DP 与组合数 ----------
    ans = 0
    for k in range(1, maxLen + 1):          # 骨架长度
        ways_to_place = comb(n - 1, k - 1)  # C(n-1, k-1)
        dp_len_k = dp_all[k - 1]            # dp_all 索引从 0 开始
        for v in range(1, maxValue + 1):
            ans = (ans + dp_len_k[v] * ways_to_place) % MOD

    return ans
```

**代码要点注释**

| 行号 | 说明 |
|------|------|
| 8‑13 | 用筛法把每个数的 **真因子**（不包括自身）收集到 `factor`，相当于“字典里每个词对应的解释”。 |
| 20‑27| 计算最长可能的骨架长度 `maxLen`（每一步至少翻倍）。 |
| 31‑36| 初始化 `dp`：长度为 1 时每个数都有唯一序列 `[v]`。 |
| 38‑45| DP 转移：`dp[l][v] = Σ dp[l‑1][u]`，`u` 为 `v` 的因子。 |
| 53‑64| 预计算阶乘与逆元，用来快速求组合数 `C(N, K)`（费马小定理）。 |
| 71‑78| 主循环：对每个可能的骨架长度 `k`，把 **骨架数量** 与 **填充方式** 相乘累加。 |

---

#### 复杂度

- **时间复杂度**  
  - 因子预处理：`O(maxValue log maxValue)`（类似筛法的复杂度）。  
  - DP：`O(maxLen * maxValue * avg_factor_cnt)`，其中 `avg_factor_cnt` 是每个数因子个数的平均值，约为 `log maxValue`。整体约为 `O(maxValue * log² maxValue)`，对 `10⁴` 的规模约几万次运算，完全可以接受。  
  - 组合数预处理：`O(n)`。  
  - 合并求和：`O(maxLen * maxValue)`。  

  综合下来 **约为 `O(maxValue * log² maxValue)`**，在题目限制下运行毫秒级。

- **空间复杂度**  
  - 因子表：`O(maxValue log maxValue)`（每个数的因子列表）。  
  - DP 表只保留两层，加上 `dp_all` 保存每层结果，总共 `O(maxLen * maxValue)`。  
  - 组合数数组 `O(n)`。  
  整体 **约为 `O(maxValue * log maxValue)`**，约几百 KB~几 MB，符合限制。

> **与暴力解对比**：  
> - 暴力需要指数级时间，根本不可能完成。  
> - 最优解把问题拆成“骨架计数 + 组合填充”，每一步都是多项式时间，真正可运行。

---

## 心得

- **核心技巧**：把“非递减 + 整除”这两个约束拆解成  
  1. **严格递增且相邻数互为倍数的骨架**（用 DP 统计）  
  2. **把骨架扩展成完整数组的组合数**（用组合数学）。  

- **适用的题型**  
  1. **需要统计满足“相邻元素满足某种关系（如整除、相等、相差固定）”的序列**，例如 “Count Number of Good Subarrays”。  
  2. **把序列压缩为“不同元素的顺序”再做组合计数**，如 “Number of Permutations with Fixed Points”。  
  3. **涉及“每一步至少翻倍/递增” 的计数问题**，常用 **因子/倍数 DP + 组合** 的思路。

- **一句话总结解题钥匙**：  
  **“先数‘骨架’（严格递增且满足关系），后乘以‘填充方式’（组合数）”。**

---

## 反思

- **拿到题目第一反应**：直接想枚举所有数组，检查条件。  
- **最容易踩的坑**  
  1. **忘记非递减与严格递增的区别**：相同的数可以出现多次，必须在 DP 中只统计“不同数”的序列。  
  2. **组合数的下标**：是 `C(n‑1, k‑1)` 而不是 `C(n, k)`，因为我们在 `n‑1` 个间隔里放 `k‑1` 个“切割”。  
  3. **模运算的时机**：乘法、加法都要及时取模，防止整数溢出。  
  4. **因子预处理的效率**：直接对每个数遍历 `1…v` 会导致 `O(maxValue²)`，应该用筛法（倍数遍历）降低到 `O(maxValue log maxValue)`。  

- **下次遇到同类题**，第一步应该先 **抽象出“不同元素的递增骨架”**，判断是否可以用 **DP+因子/倍数** 或 **DP+最长递增子序列** 来计数，再考虑 **组合数** 或 **排列数** 把骨架扩展到完整答案。这样就能从一开始就走在最优解的道路上。