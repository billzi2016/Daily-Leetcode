# #3472. 最长回文子序列（Longest Palindromic Subsequence）在至多 K 次操作后的最大长度 / Longest Palindromic Subsequence After at Most K Operations

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/longest-palindromic-subsequence-after-at-most-k-operations/)

---

## 题目（英文原版）

**Description**

You are given a string s and an integer k.
In one operation, you can replace the character at any position with the next or previous letter in the alphabet (wrapping around so that 'a' is after 'z'). For example, replacing 'a' with the next letter results in 'b', and replacing 'a' with the previous letter results in 'z'. Similarly, replacing 'z' with the next letter results in 'a', and replacing 'z' with the previous letter results in 'y'.
Return the length of the longest palindromic subsequence of s that can be obtained after performing at most k operations.

**Examples**

**Example 1:**

```
Input: s = "abced", k = 2
Output: 3
Explanation:
The subsequence "ccc" forms a palindrome of length 3, which is the maximum.
```

**Example 2:**

```
Input: s = " aaazzz ", k = 4
Output: 6
Explanation:
The entire string forms a palindrome of length 6.
```

**Constraints**

- 1 <= s.length <= 200
- 1 <= k <= 200
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`。  
一次操作中，你可以将任意位置的字符替换为字母表中的下一个或上一个字母（循环取模，`'a'` 的前一个字母是 `'z'`，`'z'` 的后一个字母是 `'a'`）。例如，将 `'a'` 替换为下一个字母得到 `'b'`，将 `'a'` 替换为上一个字母得到 `'z'`；同理，将 `'z'` 替换为下一个字母得到 `'a'`，将 `'z'` 替换为上一个字母得到 `'y'`。  

返回在至多 `k` 次操作后，能够得到的最长回文子序列（palindromic subsequence）的长度。

---

### 示例

**示例 1**

```
Input: s = "abced", k = 2
Output: 3
Explanation:
子序列 "ccc" 构成长度为 3 的回文，这是可以达到的最大长度。
```

**示例 2**

```
Input: s = "aaazzz", k = 4
Output: 6
Explanation:
整个字符串在经过最多 4 次操作后可以变成回文，长度为 6。
```

---

### 约束

- `1 <= s.length <= 200`
- `1 <= k <= 200`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的子序列都枚举出来**，然后看每个子序列能不能在不超过 `k` 次操作的情况下变成回文，记录最长的长度。

- **子序列**就像从一串珠子里挑出若干颗，挑的顺序必须保持原来的先后关系。  
- **操作**把字符往前或往后移动一步（循环），相当于在字母表里“走一步”。  
- 对每个子序列，我们需要计算把两端对应字符配成相同所需的最小步数（即**循环距离**），把所有配对的步数加起来，判断是否 ≤ `k`。

> **为什么会对**  
> 因为遍历了**全部**合法的子序列，肯定不会错过最优解。

> **时间/空间分析**  
> - 长度为 `n` 的字符串有 `2^n` 个子序列（每个字符选或不选），枚举它们的时间是指数级的，记作 `O(2^n)`。  
> - 额外的空间只需要存放当前子序列，最多 `O(n)`。  

> **大白话**：  
> `O(2^n)` 就像把所有可能的钥匙都尝一遍，钥匙数量随字符数指数增长，几分钟就会变成几千年。

#### 代码（Python）

```python
from itertools import combinations

def dist(a: str, b: str) -> int:
    """循环距离，返回把 a 变成 b 最少需要的步数"""
    d = abs(ord(a) - ord(b))
    return min(d, 26 - d)          # 前进或后退，取较小的

def longest_pal_subseq_bruteforce(s: str, k: int) -> int:
    n = len(s)
    best = 0

    # 枚举子序列的长度，从大到小可以提前剪枝
    for length in range(n, 0, -1):
        # 产生所有下标组合，例如 (0,2,4) 表示选 s[0],s[2],s[4]
        for idx in combinations(range(n), length):
            seq = [s[i] for i in idx]          # 取出子序列字符
            # 计算配对的总操作数（两端配对）
            cost = 0
            i, j = 0, len(seq) - 1
            while i < j:
                cost += dist(seq[i], seq[j])
                i += 1
                j -= 1
                if cost > k:        # 超出上限，直接放弃
                    break
            if cost <= k:           # 合法且是回文（因为已经配对完）
                best = max(best, len(seq))
                # 已经找到当前长度的合法解，可直接返回
                return best
    return best
```

> **注意**：这段代码仅用于说明思路，实际运行会在 `n≈20` 以后就超时。

#### 复杂度

- **时间复杂度**：`O(2^n)` —— 随着字符串长度指数增长，几乎不可接受。  
- **空间复杂度**：`O(n)` —— 只保存当前枚举的子序列。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举子序列**，这一步把时间推到了指数级。  
我们注意到：

1. 子序列的相对顺序不变，只关心**区间 `[i…j]`** 内的字符如何配对。  
2. 配对时只需要知道两端字符的**循环距离** `dist(s[i], s[j])`，这是一笔固定的代价。  
3. 当我们决定是否把 `s[i]` 与 `s[j]` 配成一对时，**剩余的子问题**正好是区间 `[i+1 … j-1]`，且可用的操作次数会相应减少。

这正好符合**动态规划**的递推结构：把大问题拆成小问题，记录子问题的最优解，避免重复计算。

---

#### 关键状态

`dp[i][j][c]` = 在子串 `s[i..j]`（左闭右闭）里，**使用不超过 `c` 次操作**时，能够得到的最长回文子序列长度。

- `i`、`j`：子串的左右边界，`0 ≤ i ≤ j < n`。  
- `c`：剩余的操作次数，`0 ≤ c ≤ k`。

> **类比**：把 `dp` 想象成一本 **“字典”**（哈希表），键是 `(i,j,c)`，值是对应的最长长度。查询一次即可得到答案，避免再次遍历子序列。

---

#### 递推公式

对任意 `i < j`，我们有三种选择：

1. **不使用两端字符**，只考虑左边或右边的子串  
   - `dp[i+1][j][c]`（丢掉左端）  
   - `dp[i][j-1][c]`（丢掉右端）

2. **把两端字符配成一对**  
   - 需要的操作数 `d = dist(s[i], s[j])`。  
   - 前提是 `c ≥ d`（还有足够的操作次数）。  
   - 配对后再处理内部子串 `[i+1 … j-1]`，可用的操作次数剩 `c-d`，再加上这对字符本身贡献的长度 `+2`。  
   - 公式：`dp[i+1][j-1][c-d] + 2`

取上述三者的最大值：

```
dp[i][j][c] = max(
    dp[i+1][j][c],
    dp[i][j-1][c],
    dp[i+1][j-1][c-d] + 2   (if c >= d)
)
```

#### 初始条件

- 空子串 `i > j`：长度 `0`（不可能选任何字符）。  
- 单字符子串 `i == j`：无论剩余多少操作，最长回文子序列长度都是 `1`（单个字符本身就是回文）。

#### 计算顺序

我们从 **短子串** 往 **长子串** 扩展，保证在计算 `dp[i][j][*]` 时，所依赖的 `dp[i+1][j][*]、dp[i][j-1][*]、dp[i+1][j-1][*]` 已经算好。

- 外层循环遍历子串长度 `len = 1 … n`。  
- 再遍历左端 `i`，右端 `j = i + len - 1`。  
- 最内层遍历可用操作次数 `c = 0 … k`。

#### 结果

答案是 `max_{c ≤ k} dp[0][n-1][c]`，即整个字符串区间内，使用不超过 `k` 次操作时的最长回文子序列长度。

---

#### 代码（Python）

```python
def cyclic_dist(a: str, b: str) -> int:
    """返回把字符 a 变成字符 b 所需的最小循环步数"""
    diff = abs(ord(a) - ord(b))
    return min(diff, 26 - diff)   # 前进或后退，取较小的

def longest_pal_subseq(s: str, K: int) -> int:
    n = len(s)
    # dp[i][j][c] 初始化为 0
    dp = [[[0] * (K + 1) for _ in range(n)] for _ in range(n)]

    # 单字符子串：长度为 1
    for i in range(n):
        for c in range(K + 1):
            dp[i][i][c] = 1

    # 按子串长度递增计算
    for length in range(2, n + 1):               # 子串长度 2 … n
        for i in range(n - length + 1):
            j = i + length - 1
            for c in range(K + 1):
                # 1) 丢掉左端或右端
                best = max(dp[i + 1][j][c], dp[i][j - 1][c])

                # 2) 配对两端字符
                d = cyclic_dist(s[i], s[j])
                if c >= d:                      # 有足够的操作次数
                    inner = dp[i + 1][j - 1][c - d] if i + 1 <= j - 1 else 0
                    best = max(best, inner + 2)

                dp[i][j][c] = best

    # 整体区间，找操作次数 ≤ K 时的最大值
    return max(dp[0][n - 1][c] for c in range(K + 1))
```

**代码要点注释**

- `cyclic_dist`：把字母表想象成一个圆环，向左或向右走最少步数。  
- `dp` 三维数组：`dp[i][j][c]` 对应子串 `[i..j]`、剩余操作次数 `c`。  
- `inner = dp[i+1][j-1][c-d] if i+1 <= j-1 else 0`：处理子串长度为 2 时内部区间为空的情况。  
- 最外层 `max(dp[0][n-1][c] ...)`：即使还有剩余操作次数，也可以不使用，故取不超过 `K` 的最大值。

#### 复杂度

- **时间复杂度**：`O(n² * K)`  
  - `n`（最长 200）遍历左端，`n`遍历右端，`K`（最多 200）遍历操作次数。  
  - 大约 `8·10⁶` 次基本操作，在 Python 中毫秒级即可完成。  
  - 与暴力的指数级 `2^n` 相比，**线性**增长，真正可用。

- **空间复杂度**：`O(n² * K)`  
  - 需要保存每个区间、每个剩余操作次数的最优值。  
  - 约 `8·10⁶` 个整数，约 64 MB，符合题目限制。  
  - 若想进一步压缩，可使用滚动数组把 `i` 维度压到两层，空间降到 `O(n * K)`，但对本题不是必须的。

---

## 心得

- **核心技巧**：**区间动态规划 + 费用（操作次数）维度**。  
- **适用题型**  
  1. “在限定代价内求最长回文子序列”——本题。  
  2. “限定编辑次数求最长公共子序列”——类似的三维 DP。  
  3. “在限定次数内把字符串变成回文”——可直接复用相同状态转移。  
- **解题钥匙**：**把“操作次数”当成 DP 的第三维度，像处理背包问题一样累计费用**。

---

## 反思

- **第一反应**：先想“枚举所有子序列”，因为回文子序列的定义直观。  
- **最容易踩的坑**  
  - **循环距离的计算**：忘记取最小的前进/后退步数，会导致代价过大。  
  - **边界条件**：子串长度为 2 时，内部区间为空，需要特殊处理（返回 0）。  
  - **操作次数的“至多”**：DP 中要保存“≤ c”的最优值，而不是恰好等于 `c`，否则会错失未用完操作的情况。  
- **下次思路**：看到“在限定代价下求最优结构”时，第一步就考虑**把代价作为 DP 的维度**，并检查是否可以把子问题划分为**左/右子区间**或**前缀/后缀**的递推形式。这样往往能直接写出 `O(n²·K)` 级别的解法。