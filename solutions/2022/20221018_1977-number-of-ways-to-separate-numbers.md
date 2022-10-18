# #1977. **分割数字的方案数** / Number of Ways to Separate Numbers

> 难度：困难 · 标签：String、Dynamic Programming、Suffix Array · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-separate-numbers/)

---

## 题目（英文原版）

**Description**

You wrote down many positive integers in a string called num. However, you realized that you forgot to add commas to seperate the different numbers. You remember that the list of integers was non-decreasing and that no integer had leading zeros.
Return the number of possible lists of integers that you could have written down to get the string num. Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: num = "327"
Output: 2
Explanation: You could have written down the numbers:
3, 27
327
```

**Example 2:**

```
Input: num = "094"
Output: 0
Explanation: No numbers can have leading zeros and all numbers must be positive.
```

**Example 3:**

```
Input: num = "0"
Output: 0
Explanation: No numbers can have leading zeros and all numbers must be positive.
```

**Constraints**

- 1 <= num.length <= 3500
- num consists of digits '0' through '9'.

---

## 题目（中文翻译）

你在一个字符串 `num` 中写下了许多正整数。然而，你忘记在不同的数字之间添加逗号。你记得这些整数构成一个**非递减**（non‑decreasing）序列，并且没有整数包含前导零（leading zeros）。  
返回能够得到字符串 `num` 的整数列表的可能数量。由于答案可能很大，请返回 **10^9 + 7** 取模后的结果。

---

### 示例

**示例 1**  
**输入**: `num = "327"`  
**输出**: `2`  
**解释**: 你可能写下的数字序列有：  
- `3, 27`  
- `327`

**示例 2**  
**输入**: `num = "094"`  
**输出**: `0`  
**解释**: 任何数字都不能有前导零，且所有数字必须为正数。

**示例 3**  
**输入**: `num = "0"`  
**输出**: `0`  
**解释**: 任何数字都不能有前导零，且所有数字必须为正数。

---

### 约束

- `1 <= num.length <= 3500`
- `num` 仅由字符 `'0'` 到 `'9'` 组成

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把字符串 `num` 的每一种**切分**都枚举出来，然后检查这条切分是否满足  

1. 每个子串都不以 `'0'` 开头（因为没有前导零），且必须是正整数。  
2. 切分得到的整数序列是 **非递减** 的（后面的数 ≥ 前面的数）。

这就像把一根绳子随意打结：把每一个可能的打结位置（下标）全部列出来，形成所有可能的“段”。  
对每一种段的组合，我们再逐段比较大小，判断是否满足“后者 ≥ 前者”。  

如果全部满足，就算一种合法的写法；把所有合法写法计数即可。

**为什么能得到正确答案？**  
因为我们把**所有**可能的切分都遍历了一遍，符合条件的自然全部被统计，符合题意的解必然被包含。

**复杂度分析（大白话）**  

- 对长度为 `n` 的字符串，切分点有 `n‑1` 个，每个点要么切，要么不切，  
  所以总共有 `2^(n‑1)` 种切法。  
- 对每一种切法，我们还要把所有子串转成整数并比较大小，最坏情况是 `O(n)` 的工作。  

于是整体时间是 **指数级**的 `O(2^n)`，在 `n ≤ 3500` 时根本跑不完。  
空间上只需要保存递归栈或当前切分，最多 `O(n)`。

> **O(2^n) 的含义**：如果 `n` 增加 1，工作量会翻倍；当 `n=30` 时已经有超过 **10⁹** 次操作，完全不可接受。

#### 代码（Python）

```python
MOD = 10**9 + 7

def brute(num: str) -> int:
    n = len(num)
    ans = 0

    # dfs(pos, prev) 递归遍历从 pos 开始的剩余字符，
    # prev 为前一个已经确定的整数（用字符串表示，方便比较）
    def dfs(pos: int, prev: str) -> None:
        nonlocal ans
        if pos == n:                # 已经划到字符串末尾
            ans = (ans + 1) % MOD   # 找到一种合法写法
            return
        # 当前位置不能是 '0'，否则会出现前导零
        if num[pos] == '0':
            return
        # 试着把后面的字符取成不同长度的子串
        cur = ''
        for i in range(pos, n):
            cur += num[i]           # cur = num[pos:i+1]
            # 若已有前一个数，比较大小（字符串直接比较即可，因为同长度时字典序等价于数值大小）
            if prev != '' and (len(prev) < len(cur) or (len(prev) == len(cur) and prev > cur)):
                break               # 已经大于当前数，后面的更长只会更大，直接剪枝
            dfs(i + 1, cur)         # 递归处理剩余部分

    dfs(0, '')
    return ans
```

> 这段代码只用于说明「暴力」思路，**实际会超时**。

#### 复杂度  

- **时间复杂度**：`O(2^n)` —— 每个切分点都有“切/不切”两种选择，指数级增长。  
- **空间复杂度**：`O(n)` —— 递归深度最多 `n`，以及保存当前子串的临时字符串。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **枚举所有切分**。  
我们需要一种方法，**只在合法的切分上做累加**，而不是把不合法的全部遍历一遍。

#### 关键观察  

1. **子串的长度决定了大小的关系**  
   - 若前一个数的长度 **小于** 当前数的长度，则一定满足 `前 ≤ 后`（因为没有前导零，位数更少的数一定更小）。  
   - 若两者长度相等，则只能比较对应的字符大小。  

2. **子串比较可以在 O(1) 内完成**  
   - 预处理 **最长公共前缀（LCP）**：`lcp[i][j]` 表示从下标 `i` 和 `j` 开始的后缀有多少个相同的字符。  
   - 两个等长子串 `a = num[x:x+len]`、`b = num[y:y+len]`  
     - 若 `lcp[x][y] >= len`，则两子串完全相同。  
     - 否则第 `lcp[x][y]` 位不同，直接比较 `num[x+same]` 与 `num[y+same]` 即可。  

   这样我们只需要一次预处理 `O(n²)`，随后每次比较都是常数时间。

3. **动态规划（DP）**  
   - 设 `dp[i][len]` 为：**以第 `i` 个字符（不含）结尾，且最后一个数长度为 `len` 的合法切分数量**。  
     - `i` 为前缀长度，`0 ≤ i ≤ n`，`1 ≤ len ≤ i`。  
   - 初始状态：如果子串 `num[0:len]` 没有前导零，则 `dp[len][len] = 1`（只有一种切法——直接把前 `len` 位当作第一个数）。  
   - 转移：设当前子串为 `num[j:i]`，`j = i - len`（当前数的起始位置）。  
     - 若 `num[j] == '0'`，该子串非法，`dp[i][len] = 0`。  
     - 否则，需要把它接在 **前面** 已经合法的切分后面。前一个数以 `j` 为结尾，长度记作 `pre_len`。  
       - **如果 `pre_len < len`**，必然满足非递减，直接把所有 `dp[j][pre_len]` 加进来。  
       - **如果 `pre_len == len`**，只能在 `num[j‑len:j] ≤ num[j:i]` 时才合法。利用 LCP 进行 O(1) 判断。  

   为了快速求 “所有 `pre_len < len` 的和”，我们额外维护前缀和 `pref[i][k] = Σ_{t=1..k} dp[i][t]`。  

4. **答案**  
   - 所有以整个字符串结尾的切分，即 `Σ_{len=1..n} dp[n][len] = pref[n][n]`。  

#### 伪代码概览  

```
preprocess LCP matrix (n x n)

dp = [[0]*(n+1) for _ in range(n+1)]
pref = [[0]*(n+1) for _ in range(n+1)]

for i from 1 to n:
    for len from 1 to i:
        j = i - len                       # 当前数的起始位置
        if num[j] == '0': continue        # 前导零非法

        if j == 0:                         # 第一个数
            dp[i][len] = 1
        else:
            # 1) 前一个数长度更短的情况
            val = pref[j][len-1]           # Σ dp[j][pre_len] , pre_len < len

            # 2) 前一个数长度相等的情况
            if len <= j and num[j-len] != '0':
                if compare(j-len, j, len) <= 0:   # 前 ≤ 后
                    val = (val + dp[j][len]) % MOD

            dp[i][len] = val % MOD

        pref[i][len] = (pref[i][len-1] + dp[i][len]) % MOD
```

`compare(a, b, L)` 使用 LCP：

```
same = lcp[a][b]
if same >= L: return 0            # 完全相同
return -1 if num[a+same] < num[b+same] else 1
```

#### 代码（Python）

```python
MOD = 10**9 + 7

def numberOfWays(num: str) -> int:
    n = len(num)

    # ---------- 1. 预处理 LCP ----------
    # lcp[i][j] = longest common prefix length of suffixes starting at i and j
    lcp = [[0] * (n + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if num[i] == num[j]:
                lcp[i][j] = 1 + lcp[i + 1][j + 1]

    # ---------- 2. dp 与前缀和 ----------
    dp = [[0] * (n + 1) for _ in range(n + 1)]      # dp[i][len]
    pref = [[0] * (n + 1) for _ in range(n + 1)]    # pref[i][len] = Σ_{t≤len} dp[i][t]

    for i in range(1, n + 1):          # i 为前缀长度（不含第 i 位）
        for length in range(1, i + 1):
            start = i - length          # 当前数的起始下标
            if num[start] == '0':       # 前导零非法
                continue

            if start == 0:              # 第一个数，直接算一种
                dp[i][length] = 1
            else:
                # 1) 前一个数长度更短 —— 直接累加前缀和
                ways = pref[start][length - 1]

                # 2) 前一个数长度相等，需要比较大小
                if length <= start and num[start - length] != '0':
                    # 比较 num[start-length:start] 与 num[start:i]
                    same = lcp[start - length][start]
                    if same < length:   # 有不同字符
                        if num[start - length + same] < num[start + same]:
                            ways = (ways + dp[start][length]) % MOD
                    else:                # 完全相同，前 ≤ 后 成立
                        ways = (ways + dp[start][length]) % MOD

                dp[i][length] = ways % MOD

            # 更新前缀和
            pref[i][length] = (pref[i][length - 1] + dp[i][length]) % MOD

    # ---------- 3. 最终答案 ----------
    return pref[n][n] % MOD
```

> 代码中每一行都有中文注释，直接复制运行即可得到答案。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 预处理 LCP：`O(n²)`  
  - 双层循环填表：每个 `(i, length)` 只做常数次 O(1) 操作 → `O(n²)`  
  对于 `n = 3500`，约 `12 250 000` 次基本运算，轻松在一秒内完成。  

- **空间复杂度**：`O(n²)`  
  - LCP、dp、pref 三个 `n×n` 的整数矩阵。  
  - `3500² ≈ 12.25 × 10⁶`，每个整数 4 字节，总共约 150 MB（在多数在线评测平台可接受）。  
  - 若空间紧张，也可以把 `pref` 合并到 `dp` 中，只保留一行的前缀和，进一步压缩到 `O(n²)` → `O(n)` 的额外空间。

> 与暴力解的 `O(2ⁿ)` 相比，`O(n²)` 只随输入长度的平方增长，**能轻松处理 3500 长度的字符串**。

---

## 心得  

- **核心技巧**：**长度+前缀和 + 最长公共前缀（LCP）** 的组合，让我们在比较两个等长子串时只花 O(1) 时间，同时还能快速求 “所有更短长度的合法前缀” 的和。  
- **适用题型**：  
  1. “把字符串分割成满足某种单调性/大小关系的序列”——如 *Number of Ways to Separate Numbers*、*Number of Ways to Split a String*（单调递增）等。  
  2. “需要频繁比较子串大小且长度很大”的 DP——如 *Largest Number After Digit Swaps*（需要快速子串比较）等。  
- **一句话总结解题钥匙**：**把“比较大小”转化为“长度关系 + O(1) 字符比较”，再用前缀和把“所有更短的情况”一次性加进去**。

---

## 反思  

- **拿到题目第一反应**：直接回想“枚举所有切法”，写递归/回溯。  
- **最容易踩的坑**  
  1. **前导零**：忘记在每个子串开头检查 `'0'`，会导致错误计数。  
  2. **整数比较**：直接把子串转成 `int` 会超出 Python 整数范围（长度可达 3500），而且慢。必须用字符串比较或 LCP。  
  3. **边界条件**：`len == i`（即整个前缀是一个数）时需要单独处理，否则 `pref[start][len‑1]` 访问负下标。  
- **下次遇到同类题，第一步该想到**：  
  1. 用 **长度** 把“大小比较”先划分成“短必小、等长再比较”。  
  2. 预处理 **LCP**（或哈希）让等长比较 O(1)。  
  3. 用 **DP + 前缀和** 把“所有更短长度的合法前缀”一次性累计。  

这样就能把指数爆炸的暴力思路，压缩到多项式时间。祝学习愉快！