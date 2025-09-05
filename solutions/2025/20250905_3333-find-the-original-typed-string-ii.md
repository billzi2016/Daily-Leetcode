# #3333. 找出原始键入字符串 II / Find the Original Typed String II

> 难度：困难 · 标签：String、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-original-typed-string-ii/)

---

## 题目（英文原版）

**Description**

Alice is attempting to type a specific string on her computer. However, she tends to be clumsy and may press a key for too long, resulting in a character being typed multiple times.
You are given a string word, which represents the final output displayed on Alice's screen. You are also given a positive integer k.
Return the total number of possible original strings that Alice might have intended to type, if she was trying to type a string of size at least k.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: word = "aabbccdd", k = 7
Output: 5
Explanation:
The possible strings are: "aabbccdd" , "aabbccd" , "aabbcdd" , "aabccdd" , and "abbccdd" .
```

**Example 2:**

```
Input: word = "aabbccdd", k = 8
Output: 1
Explanation:
The only possible string is "aabbccdd" .
```

**Example 3:**

```
Input: word = "aaabbb", k = 3
Output: 8
```

**Constraints**

- 1 <= word.length <= 5 * 105
- word consists only of lowercase English letters.
- 1 <= k <= 2000

---

## 题目（中文翻译）

Alice 正在尝试在电脑上键入一个特定的字符串。然而，她有点笨拙，可能会把某个键（key）按得太久，导致同一个字符（character）被输入多次。  
给定一个字符串（string）`word`，表示 Alice 屏幕上最终显示的输出。再给定一个正整数 `k`。  
返回 Alice 可能原本想要键入的、长度至少为 `k` 的原始字符串（original strings）的总数。由于答案可能非常大，请返回其对 `10^9 + 7` 取模的结果。

**Example 1:**  
**Input:** `word = "aabbccdd", k = 7`  
**Output:** `5`  
**Explanation:**  
可能的原始字符串有：`"aabbccdd"`、`"aabbccd"`、`"aabbcdd"`、`"aabccdd"` 和 `"abbccdd"`。

**Example 2:**  
**Input:** `word = "aabbccdd", k = 8`  
**Output:** `1`  
**Explanation:**  
唯一可能的原始字符串是 `"aabbccdd"`。

**Example 3:**  
**Input:** `word = "aaabbb", k = 3`  
**Output:** `8`

**约束条件：**  
- `1 <= word.length <= 5 * 10^5`  
- `word` 仅由小写英文字母组成。  
- `1 <= k <= 2000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把 `word` 看成若干 **相同字符的连续块**（也叫 **run**）：

```
word = a a a b b c c c d
        └─run1─┘ └─run2─┘ ...
```

- 每个块的长度记为 `L[i]`（比如 `run1` 长度是 3）。
- Alice 原本想敲的字符序列里，每出现一次这个字符，就会在屏幕上产生 **至少一次** 的该字符。  
  如果她把键按得太久，这一次按键会被 **重复** 若干次，于是形成一个块 `L[i]`。  
- 因此，一个块可以被 **切分** 成若干个 **子块**，每个子块对应一次真正的按键。  
  把长度为 `L` 的块切成 `p` 个子块的方法数等价于把 `L-1` 条“分割线”里挑 `p-1` 条来截断，  
  于是有  

\[
\text{Ways}(L,\;p)=\binom{L-1}{p-1}
\]

  这跟把 **一本字典** 的页码（`L-1`）里挑出 `p-1` 页的做法是一样的——把页码当作分割点，挑几页就能把书分成几段。

- 对所有块独立选择切分方式后，把每段的字符依次连起来，就是一种可能的 **原始字符串**。

所以暴力的思路就是：

1. 把 `word` 分块，得到长度数组 `L[0…m-1]`（`m` 为块的个数）。  
2. 对每个块枚举它可能被切成的子块数 `p = 1 … L[i]`，计算组合数 `C(L[i]-1, p-1)`。  
3. 用 **多重循环** 把所有块的选择相乘、累加，得到所有满足 `原始长度 ≥ k` 的方案数。

> 这相当于在求  
> \[
> \sum_{p_0=1}^{L_0}\sum_{p_1=1}^{L_1}\dots
> \Big[ \sum_i p_i \ge k \Big]\;
> \prod_i \binom{L_i-1}{p_i-1}
> \]

#### 代码（Python）

```python
MOD = 10**9 + 7

def brute(word: str, k: int) -> int:
    # 1️⃣ 把 word 分块
    runs = []
    cnt = 1
    for i in range(1, len(word)):
        if word[i] == word[i-1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1
    runs.append(cnt)                     # 最后一个块

    m = len(runs)

    # 2️⃣ 预先算组合数（这里直接用 Python 的 math.comb，实际会超时）
    from math import comb

    ans = 0
    # 3️⃣ 多重循环：暴力枚举每个块的子块数
    def dfs(idx: int, cur_len: int, cur_ways: int):
        nonlocal ans
        if idx == m:                     # 所有块都决定完了
            if cur_len >= k:
                ans = (ans + cur_ways) % MOD
            return
        L = runs[idx]
        for p in range(1, L + 1):        # p 是本块切成的子块数
            ways = comb(L - 1, p - 1)    # 该块的切分方式数
            dfs(idx + 1, cur_len + p, cur_ways * ways % MOD)

    dfs(0, 0, 1)
    return ans
```

> 代码里每一步都有中文注释，帮助你对照思路。  
> **注意**：`math.comb` 在大数情况下会非常慢，且递归的深度会随块的数量爆炸——这就是暴力解的 **瓶颈**。

#### 复杂度  

- 时间复杂度：  
  对每个块我们要枚举 `1 … L[i]`，总的枚举次数是 `∏ L[i]`（指数级），  
  甚至在最坏情况下（`word = "aaaaaaaa…"`）是 `O(2^{n})`，根本不可接受。  
- 空间复杂度：  
  递归栈的深度是块的个数 `m ≤ n`，额外空间 `O(m)`。

> **大白话**：  
> - `O(2^{n})` 意味着如果 `n` 再大一点（比如 30），计算次数就已经是 **十亿级**，普通电脑根本跑不完。  
> - 这就是我们需要 **更聪明的办法**。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，真正的难点在于 **“长度 ≥ k”** 这个条件。  
如果我们能先算出 **所有可能的原始字符串数目**，再减去 **长度 < k** 的那些，就得到答案。

> **关键观察 1**：  
> 对每个块 `L`，把它切成 `p` 部分的方式数是组合数 `C(L-1, p-1)`，  
> 而 **所有可能的原始字符串总数** 等于把每块的所有切法相乘后求和：  
> \[
> \text{TOTAL} = \prod_{i=0}^{m-1} \Big(\sum_{p=1}^{L_i} \binom{L_i-1}{p-1}\Big)
>               = \prod_{i=0}^{m-1} 2^{L_i-1}
> \]
> 因为 \(\sum_{p=1}^{L} \binom{L-1}{p-1}=2^{L-1}\)。  
> 所以 `TOTAL = 2^{|word| - m}`（`|word|` 是原字符串长度，`m` 是块数），计算很快。

> **关键观察 2**（把 “长度 < k” 变成 “长度 ≤ k‑1”）：  
> 设每块切成 `p_i` 部分，则原始字符串的长度是 `∑ p_i`。  
> 为了统计 **长度 ≤ k‑1** 的情况，只需要 **限制** `∑ p_i ≤ k-1`。

> **关键观察 3**（块的数量上限）：  
> 每个块至少贡献 **1** 个字符。  
> 若块的总数 `m` 已经大于 `k-1`，即使所有块都只贡献 1，长度也 **≥ m > k-1**，  
> 那么 **不存在** 长度 ≤ k‑1 的原始字符串。  
> 因此在求 “短字符串” 时，只需要考虑 **前 `k-1` 个块**（或者全部块，但 `m ≤ k-1` 时才会全部遍历）。

> **把问题转化为“背包”**：  
> 对每块我们可以选择 **额外的字符数** `e = p_i-1`（0 ~ `L_i-1`），  
> 对应的方式数是 `C(L_i-1, e)`。  
> 设 `base = m`（每块必选的 1），则  
> \[
> \text{len} = base + \sum e_i
> \]
> 需要 `base + Σe_i ≤ k-1` → `Σe_i ≤ limit`，其中 `limit = k-1 - base`（如果 `limit < 0`，说明根本不可能）。

> **动态规划（DP）**  
> - `dp[t]` = 用已经处理好的块，**额外字符数**恰好为 `t` 的方案数（模 `MOD`）。  
> - 初始化 `dp[0] = 1`（还没有块时，额外字符数为 0）。  
> - 对每个块（只遍历 **最多 `k-1` 个块**），做如下转移：

\[
\text{new}[t+e] \;+=\; dp[t] \times \binom{L_i-1}{e}
\qquad (0 \le e \le \min(L_i-1,\;limit-t))
\]

> 这就是 **有限背包**，每件物品（块）可以选择 0~`L_i-1` 的重量 `e`，价值是对应的组合数。

> **复杂度分析**  
> - 只会遍历 `min(m, k-1) ≤ 2000` 个块。  
> - `limit ≤ k-1 ≤ 1999`，所以 DP 表大小是 `O(k)`。  
> - 每个块的转移最多枚举 `e = 0 … limit`，整体时间 `O(k²) ≈ 4·10⁶`，完全可以接受。  
> - 预计算组合数需要 `O(N)`（`N = |word| ≤ 5·10⁵`）的阶乘和逆元，空间 `O(N)`。

> **一步步的优化路线**  
> 1. **先算总数**：`TOTAL = 2^{|word|-m}`（常数时间）。  
> 2. **如果块数 > k-1**，直接返回 `TOTAL`（因为没有短的）。  
> 3. **否则** 用 DP 计算 **短字符串数** `shortWays`（长度 ≤ k‑1）。  
> 4. **答案** = `TOTAL - shortWays`（取模）。

#### 代码（Python）

```python
MOD = 10**9 + 7

# --------------------------------------------------------------
# 预处理：阶乘、逆元、组合数
# --------------------------------------------------------------
def prepare_factorials(n: int):
    """返回 fact, inv_fact，长度为 n+1"""
    fact = [1] * (n + 1)
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)
    # 费马小定理求逆元：a^(MOD-2) ≡ a^{-1} (mod MOD)
    inv_fact[n] = pow(fact[n], MOD - 2, MOD)
    for i in range(n, 0, -1):
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    return fact, inv_fact


def nCr(fact, inv_fact, n: int, r: int) -> int:
    """安全的组合数 C(n, r)（若 r<0 或 r>n 返回 0）"""
    if r < 0 or r > n:
        return 0
    return fact[n] * inv_fact[r] % MOD * inv_fact[n - r] % MOD


# --------------------------------------------------------------
# 主函数
# --------------------------------------------------------------
def numberOfPossibleOriginalStrings(word: str, k: int) -> int:
    # 1️⃣ 把 word 分块，得到每段的长度
    runs = []
    cnt = 1
    for i in range(1, len(word)):
        if word[i] == word[i - 1]:
            cnt += 1
        else:
            runs.append(cnt)
            cnt = 1
    runs.append(cnt)                     # 最后一个块

    m = len(runs)                        # 块的个数
    n = len(word)                        # 原字符串长度

    # 2️⃣ 预处理组合数（需要的最大 n 为 max(run_len)-1 ≤ n-1）
    max_len = max(runs)
    fact, inv_fact = prepare_factorials(max_len)   # 只要到 max_len 即可

    # 3️⃣ 计算所有可能的原始字符串数目（不考虑长度限制）
    #    每个块的所有切法数为 2^{L-1}
    total = pow(2, n - m, MOD)           # 2^{|word|-m}
    
    # 4️⃣ 若块数已经 > k-1，说明不可能出现 “长度 ≤ k-1”，直接返回 total
    if m > k - 1:
        return total

    # 5️⃣ DP 统计 “长度 ≤ k-1” 的方案数
    limit = k - 1 - m                     # 额外字符数的上限
    dp = [0] * (limit + 1)
    dp[0] = 1

    for L in runs:                        # 对每个块
        # 本块可以贡献的额外字符数 e = 0 … min(L-1, limit)
        max_extra = min(L - 1, limit)
        # 预先把所有 C(L-1, e) 取出来，避免重复计算
        combs = [nCr(fact, inv_fact, L - 1, e) for e in range(max_extra + 1)]

        new = [0] * (limit + 1)
        for e in range(max_extra + 1):
            coeff = combs[e]               # C(L-1, e)
            if coeff == 0:
                continue
            for cur in range(limit - e + 1):
                if dp[cur]:
                    new[cur + e] = (new[cur + e] + dp[cur] * coeff) % MOD
        dp = new

    # 6️⃣ 把所有额外字符数 ≤ limit 的方案相加，得到 shortWays
    shortWays = sum(dp) % MOD

    # 7️⃣ 最终答案 = total - shortWays（注意取模正数）
    ans = (total - shortWays) % MOD
    return ans
```

**代码要点（中文注释）**

| 行号 | 说明 |
|------|------|
| 1‑4 | 常量 `MOD`。 |
| 7‑20 | 预计算阶乘 `fact` 与逆元 `inv_fact`，为后面求组合数做准备。 |
| 22‑25 | `nCr`：安全的组合数函数，超出范围直接返回 0。 |
| 29‑42 | 把 `word` 压缩成连续相同字符的块，得到每块长度 `runs`。 |
| 44‑46 | `total = 2^{|word|-m}`：所有可能的原始字符串数目（不考虑长度）。 |
| 48‑50 | 若块数已经大于 `k-1`，则不可能出现 “长度 ≤ k‑1”，直接返回 `total`。 |
| 53‑60 | DP 初始化：`limit` 是额外字符数的上限，`dp[t]` 表示额外字符数恰为 `t` 的方案数。 |
| 62‑73 | 对每块进行转移：枚举本块可以贡献的额外字符 `e`，用组合数 `C(L-1, e)` 加权。 |
| 76‑77 | 把所有 `t ≤ limit` 的方案相加得到 `shortWays`（长度 ≤ k‑1 的方案数）。 |
| 80‑82 | 用总数减去短数，取模得到最终答案。 |

#### 复杂度

- **时间复杂度**  
  - 预处理阶乘：`O(n)`（`n ≤ 5·10⁵`）。  
  - DP：`O(min(m, k) * k)` ≤ `O(k²)`，因为我们最多只会遍历 `k-1 ≤ 1999` 个块，`k` 也是 2000 左右。  
  - 整体约为 `O(n + k²)`，在最坏情况下约 `5·10⁵ + 4·10⁶`，轻松跑在 1 秒以内。

- **空间复杂度**  
  - 阶乘数组 `O(n)`。  
  - DP 数组 `O(k)`。  
  - 总计 `O(n + k)`，约 `5·10⁵` 的整数数组，完全可以接受。

> **大白话**：  
> - 只需要把字符串一次扫描成块（线性时间），  
> - 再做一个 “最多 2000 × 2000 的小表格” 的 DP，  
> - 这比暴力的指数级爆炸要安全得多。

---

## 心得

- **核心技巧**：把每个连续字符块看成 “可以被切分的物品”，切分方式用组合数描述，原问题转化为 **受限背包 DP**（额外字符数 ≤ limit）。
- **适用的题型**  
  1. “把字符串压缩后，每段可以任意划分” 类似的计数题（例如 LeetCode 1735 “Count Ways to Make Array With K Different Integers” 的思路）。  
  2. “在限制总和 ≤ K 的情况下，求所有组合数的乘积”——常见于 **组合计数 + 长度约束** 的问题。  
  3. “把一个大数拆成若干段，每段有不同的取值范围”，如 “拆分数组使每段和满足条件”。
- **一句话总结**：**把“原始长度 ≥ k”转为 “总数 – 长度 ≤ k‑1”，然后用 DP 在额外字符数 ≤ 2000 的小范围内完成计数**。

---

## 反思

- **第一反应**：看到“键按太久会出现重复”，立刻想到把相同字符的连续段拆分成若干次按键，这就是**块切分**的模型。
- **最容易踩的坑**  
  1. **忘记每块至少贡献 1**，导致 DP 边界错误。  
  2. **直接对所有块做 DP**，忽视 `m > k-1` 时可以提前返回的优化，导致超时。  
  3. **组合数取模**时没有预处理逆元，导致在循环里频繁求幂，时间爆炸。  
  4. **负数取模**：`total - shortWays` 可能为负，需要加 `MOD` 再取模。
- **下次遇到同类题**：第一步先 **把问题抽象成“每段可以选多少额外单位”**，判断是否可以 **把约束转为 “≤ 某值”**，再决定是 **背包 DP**、**前缀和** 还是 **快速乘法**。这样思路更清晰，代码也更容易写对。