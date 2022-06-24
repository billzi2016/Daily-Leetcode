# #1830. **使字符串有序的最少操作次数** / Minimum Number of Operations to Make String Sorted

> 难度：困难 · 标签：Math、String、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-make-string-sorted/)

---

## 题目（英文原版）

**Description**

You are given a string s (0-indexed)​​​​​​. You are asked to perform the following operation on s​​​​​​ until you get a sorted string:
Return the number of operations needed to make the string sorted. Since the answer can be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "cba"
Output: 5
Explanation: The simulation goes as follows:
Operation 1: i=2, j=2. Swap s[1] and s[2] to get s="cab", then reverse the suffix starting at 2. Now, s="cab".
Operation 2: i=1, j=2. Swap s[0] and s[2] to get s="bac", then reverse the suffix starting at 1. Now, s="bca".
Operation 3: i=2, j=2. Swap s[1] and s[2] to get s="bac", then reverse the suffix starting at 2. Now, s="bac".
Operation 4: i=1, j=1. Swap s[0] and s[1] to get s="abc", then reverse the suffix starting at 1. Now, s="acb".
Operation 5: i=2, j=2. Swap s[1] and s[2] to get s="abc", then reverse the suffix starting at 2. Now, s="abc".
```

**Example 2:**

```
Input: s = "aabaa"
Output: 2
Explanation: The simulation goes as follows:
Operation 1: i=3, j=4. Swap s[2] and s[4] to get s="aaaab", then reverse the substring starting at 3. Now, s="aaaba".
Operation 2: i=4, j=4. Swap s[3] and s[4] to get s="aaaab", then reverse the substring starting at 4. Now, s="aaaab".
```

**Constraints**

- 1 <= s.length <= 3000
- s​​​​​​ consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个下标从 0 开始的字符串 `s`。你需要对 `s` 反复执行下述操作，直至得到一个按字典序升序排列的字符串（即 **sorted string**）：

> **操作**：  
> 1. 任选两个下标 `i`、`j`（`0 ≤ i ≤ j < s.length`），交换 `s[i]` 与 `s[j]`；  
> 2. 将下标 `j` 起始的后缀（即 `s[j…]`）翻转（**reverse**）。

返回使字符串有序所需的最少操作次数。由于答案可能非常大，返回其对 `10^9 + 7` 取模后的结果。

---

### 示例

#### 示例 1
```text
Input: s = "cba"
Output: 5
Explanation:
操作过程如下：
- 第 1 次操作：i=2, j=2。交换 s[1] 与 s[2] 得到 s="cab"，随后翻转下标 2 开始的后缀。此时 s="cab"。
- 第 2 次操作：i=1, j=2。交换 s[0] 与 s[2] 得到 s="bac"，随后翻转下标 1 开始的后缀。此时 s="bca"。
- 第 3 次操作：i=2, j=2。交换 s[1] 与 s[2] 得到 s="bac"，随后翻转下标 2 开始的后缀。此时 s="b...
（后续过程略）```

#### 示例 2
```text
Input: s = "aabaa"
Output: 2
Explanation:
操作过程如下：
- 第 1 次操作：i=3, j=4。交换 s[2] 与 s[4] 得到 s="aaaab"，随后翻转下标 3 开始的子串。此时 s="aaaba"。
- 第 2 次操作：i=4, j=4。交换 s[3] 与 s[4] 得到 s="aaaab"，随后翻转下标 4 开始的子串。此时 s="aaaab"。
```

---

### 约束

- `1 <= s.length <= 3000`
- `s` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把题目给的操作真的一次一次地模拟下去**，直到字符串变成按字典序递增（即 `"aa…zz"` 那种）为止。  

具体步骤如下：

1. 从左到右找第一个满足 `s[i‑1] > s[i]` 的位置 `i`（如果找不到，说明已经是最小的排列，结束）。  
2. 在 `i` 之后（包括 `i`）找最右边的字符 `s[j]`，满足 `s[j] < s[i‑1]`。  
3. 交换 `s[i‑1]` 与 `s[j]`。  
4. 把从 `i` 开始的后缀全部 **翻转**（相当于把这段字符重新排成递增）。  

这套流程正是 “**求前一个排列**” 的标准算法。  
只要不断执行它，我们就会一步步走向最小的排列，计数器每加一次就表示完成了一次操作。

> **为什么它一定能得到有序字符串？**  
> 前一个排列的定义就是：在所有字典序比当前排列小的排列里，**字典序最大的** 那一个。换句话说，前一个排列比当前排列更“靠左”，而最小的排列（全局有序）没有前一个了，所以必然会最终到达。

> **时间/空间复杂度大概是怎样的？**  
> 假设我们需要执行 `k` 次操作，每一次都要遍历字符串寻找 `i`、`j`，时间是 `O(k·n)`（`n` 是字符串长度）。  
> `k` 其实等于 **比当前排列大的所有不同排列的数量**，在最坏情况下（所有字符都不相同）`k` 可以达到 `n! - 1`，也就是“阶乘”。  
> - `O(k·n)` 在 `n = 10` 时已经是 `10! ≈ 3.6M` 步，`n = 12` 就超过 400M，根本跑不完。  
> - 空间只需要存放原字符串，`O(1)`。

所以暴力模拟只能用来 **验证思路**，在实际测试里会超时。

#### 代码（Python）

```python
def prev_permutation(s: list) -> bool:
    """把列表 s 原地改成前一个排列，返回是否成功（是否还有前一个）"""
    n = len(s)
    # 1️⃣ 找到最右侧的 i 使得 s[i-1] > s[i]
    i = n - 1
    while i > 0 and s[i - 1] <= s[i]:
        i -= 1
    if i == 0:                 # 已经是最小排列
        return False

    # 2️⃣ 找到最右侧的 j ≥ i，使得 s[j] < s[i-1]
    j = n - 1
    while s[j] >= s[i - 1]:
        j -= 1

    # 3️⃣ 交换
    s[i - 1], s[j] = s[j], s[i - 1]

    # 4️⃣ 翻转后缀，使其递增
    s[i:] = reversed(s[i:])
    return True


def brute_force_ops(s: str) -> int:
    """暴力模拟，返回需要的操作次数（仅用于小规模验证）"""
    arr = list(s)
    ops = 0
    while prev_permutation(arr):
        ops += 1
    return ops
```

> **关键行中文注释** 已经写在代码里，帮助你一步步跟踪每个操作的意义。

#### 复杂度  

- **时间复杂度**：`O(k·n)`，其中 `k` 是比原字符串大的排列数。  
  - 当 `n` 较大时，`k` 接近 `n!`，这意味着时间会呈“阶乘”增长，几乎不可接受。  
- **空间复杂度**：`O(1)`（只用了常数级别的额外变量）。

---

### 2. 最优解  

#### 思路  

从暴力解我们已经知道：**每一次操作都把当前排列往字典序更小的方向走一步**，最终要走的步数等于“比当前排列大的排列有多少”。  
于是我们把 “一步一步模拟” 换成 **一次性计数**——直接算出有多少合法的排列排在当前字符串的右边（字典序更大）。

> **核心问题**  
> 给定一个含有重复字符的多重集合（即字符串的字符计数），求 **所有不同排列** 中，**字典序比 s 大** 的个数。

这正是**排列计数 + 前缀求和**的问题。我们把字符串从左到右扫描，逐位考虑如果把当前位置换成一个更小的字符，会产生多少种完整的排列。把这些可能数累加起来，就是 **当前排列在升序排列列表中的排名（0‑基）**。  

- **总排列数**（所有不同排列的数量）  
  \[
  \text{total} = \frac{n!}{\prod_{c} cnt_c!}
  \]
  其中 `cnt_c` 是字符 `c` 出现的次数。  

- **排名（rank）**  
  扫描到第 `i` 位时，已使用掉前 `i` 个字符，剩下的字符计数记作 `rem`.  
  对于所有 **比 s[i] 小且仍有剩余的字符** `ch`，我们把 `ch` 放在第 `i` 位，然后把剩下的字符随意排列。  
  这一步的排列数是  
  \[
  \frac{(n-i-1)!}{\prod_{c} (rem_c')!}
  \]
  其中 `rem_c'` 是把 `ch` 的计数减 1 后的剩余量。  
  把所有 `ch` 的贡献加起来，就是 `rank` 在第 `i` 位的增量。  

- **答案**  
  \[
  \text{ans} = (\text{total} - \text{rank}) \bmod M
  \]
  `M = 10^9 + 7`（题目要求的模数）。

> **为什么只需要 O(n·Alphabet) 的时间？**  
> - 字符集只有小写英文字母（26 个），所以在每个位置只需要遍历至多 26 次。  
> - 计算阶乘和逆元只需预处理一次，之后每次求 “剩余排列数” 可以 **用已知的全局阶乘除以对应字符计数的阶乘**，这一步是 O(1)。  

> **关键数学工具——模逆元**  
> 在模 `M` 下除法等价于乘以 **逆元**（即 `a^{-1} ≡ a^{M-2} (mod M)`，因为 `M` 是质数）。我们预先算出所有 `1! … n!` 的逆元，随后就可以 O(1) 完成 `total / something` 的计算。

#### 代码（Python）

```python
MOD = 10**9 + 7
MAXN = 3000            # 题目上限

# ---------- 预处理阶乘和逆元 ----------
fact = [1] * (MAXN + 1)          # fact[i] = i! % MOD
inv_fact = [1] * (MAXN + 1)      # (i!)^{-1} % MOD

for i in range(1, MAXN + 1):
    fact[i] = fact[i - 1] * i % MOD

# 费马小定理求逆元：a^{-1} ≡ a^{MOD-2} (mod MOD)
inv_fact[MAXN] = pow(fact[MAXN], MOD - 2, MOD)
for i in range(MAXN, 0, -1):
    inv_fact[i - 1] = inv_fact[i] * i % MOD   # (i-1)! = i! / i

# ---------- 主函数 ----------
def makeStringSorted(s: str) -> int:
    n = len(s)
    # 统计每个字符的出现次数
    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    # 计算所有不同排列的总数
    total = fact[n]
    for c in cnt:
        total = total * inv_fact[c] % MOD   # 除以 cnt[c]!

    rank = 0                # s 在升序排列列表中的 0‑基排名
    # 逐位处理
    for i, ch in enumerate(s):
        idx = ord(ch) - ord('a')
        # 对所有比当前字符更小且还有剩余的字符，尝试放到当前位置
        for smaller in range(0, idx):
            if cnt[smaller] == 0:
                continue
            # 把 smaller 放在第 i 位后，剩余字符的排列数
            cnt[smaller] -= 1                     # 暂时使用一个
            perm = fact[n - i - 1]                # (剩余长度)!
            for c in cnt:
                perm = perm * inv_fact[c] % MOD   # 除以各自的阶乘
            rank = (rank + perm) % MOD
            cnt[smaller] += 1                     # 恢复计数

        # 把真实的字符 s[i] 消耗掉，继续处理后缀
        cnt[idx] -= 1
        if cnt[idx] < 0:        # 防御性检查，理论上不会触发
            break

    # 需要的操作数 = total - rank（模 MOD）
    ans = (total - rank) % MOD
    return ans
```

> **代码要点解释**  
> - `fact` / `inv_fact`：分别是阶乘和阶乘的模逆元，帮助我们在 O(1) 时间内完成“除以 cnt! ”的操作。  
> - `total`：先算出所有不同排列的数量。  
> - 外层循环遍历字符串的每个位置 `i`，内层循环遍历比当前字符更小的 26 种可能。  
> - `perm` 计算的是 “把某个更小字符放在这里，其余字符随意排列”的方案数。  
> - `rank` 累加这些方案数，最终得到 `s` 在升序排列列表中的排名。  
> - 最终答案 `total - rank` 正好是 “比 s 更大的排列数”，也就是题目要求的操作次数。

#### 复杂度  

- **时间复杂度**：`O(n * ΣAlphabet)`，这里 `Alphabet = 26`，所以实际是 `O(26·n) ≈ O(n)`。  
  - 每个位置最多遍历 26 次，内部的乘法/取模都是 O(1)。  
- **空间复杂度**：`O(n)` 用于存放阶乘数组（长度 3000）以及字符计数数组，都是常数级别的额外空间。

相较于暴力解的阶乘级时间，最优解在 3000 长度的极限下也能轻松跑完。

---

## 心得  

- **核心技巧**：把“连续的前一个排列操作”转化为 **排列的字典序排名**，利用组合数学（阶乘、逆元）一次性计数。  
- **相似题型**（可以练习同类思路）：  
  1. **LeetCode 2585 – Number of Ways to Earn Points**（排列计数与模运算）  
  2. **LeetCode 1155 – Number of Dice Rolls With Target Sum**（动态规划 + 计数）  
  3. **LeetCode 1715 – Count Appearances of a Substring in a String**（组合计数）  
- **一句话总结解题钥匙**：**把“逐步走向最小排列”换算成“有多少排列在它右边”，用阶乘/逆元快速求出这一步数**。

---

## 反思  

- **第一反应**：看到“不断做前一个排列直到有序”，本能想到直接模拟。  
- **最容易踩的坑**：  
  - **重复字符**导致的除法需要使用模逆元，否则会出现除不尽的情况。  
  - **大数取模**：`total - rank` 可能为负，记得加上模数再取模。  
  - **预处理范围**：`n` 上限是 3000，必须把阶乘预处理到至少 `3000`，否则会越界。  
- **下次遇到同类题**：第一步先**思考是否可以把“逐步操作”转化为“全局计数”，尤其是涉及排列、组合或字典序的题目时，往往可以用**排名/逆序数**的思路一次性算出答案。