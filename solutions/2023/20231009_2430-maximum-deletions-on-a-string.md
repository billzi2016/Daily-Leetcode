# #2430. 字符串的最大删除次数 / Maximum Deletions on a String

> 难度：困难 · 标签：String、Dynamic Programming、Rolling Hash、String Matching、Hash Function · [LeetCode 链接](https://leetcode.com/problems/maximum-deletions-on-a-string/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of only lowercase English letters. In one operation, you can:
For example, if s = "ababc", then in one operation, you could delete the first two letters of s to get "abc", since the first two letters of s and the following two letters of s are both equal to "ab".
Return the maximum number of operations needed to delete all of s.

**Examples**

**Example 1:**

```
Input: s = "abcabcdabc"
Output: 2
Explanation:
- Delete the first 3 letters ("abc") since the next 3 letters are equal. Now, s = "abcdabc".
- Delete all the letters.
We used 2 operations so return 2. It can be proven that 2 is the maximum number of operations needed.
Note that in the second operation we cannot delete "abc" again because the next occurrence of "abc" does not happen in the next 3 letters.
```

**Example 2:**

```
Input: s = "aaabaab"
Output: 4
Explanation:
- Delete the first letter ("a") since the next letter is equal. Now, s = "aabaab".
- Delete the first 3 letters ("aab") since the next 3 letters are equal. Now, s = "aab".
- Delete the first letter ("a") since the next letter is equal. Now, s = "ab".
- Delete all the letters.
We used 4 operations so return 4. It can be proven that 4 is the maximum number of operations needed.
```

**Example 3:**

```
Input: s = "aaaaa"
Output: 5
Explanation: In each operation, we can delete the first letter of s.
```

**Constraints**

- 1 <= s.length <= 4000
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

**描述**  
给定一个仅由小写英文字母组成的字符串 `s`。在一次操作（operation）中，你可以：

> 例如，若 `s = "ababc"`，则在一次操作中，你可以删除 `s` 的前两个字符，得到 `"abc"`，因为 `s` 的前两个字符与紧随其后的两个字符均为 `"ab"`。

返回删除完所有字符所需的**最大**操作次数。

**示例 1**  
```
Input: s = "abcabcdabc"
Output: 2
Explanation:
- 删除前 3 个字符（"abc"），因为接下来的 3 个字符相同。此时 s = "abcdabc"。
- 删除剩余的所有字符。
共使用了 2 次操作，返回 2。可以证明 2 是所需的最大操作次数。
注意，在第二次操作中不能再删除 "abc"，因为紧随其后的 3 个字符并不等于 "abc"。
```

**示例 2**  
```
Input: s = "aaabaab"
Output: 4
Explanation:
- 删除第一个字符（"a"），因为下一个字符相同。此时 s = "aabaab"。
- 删除前 3 个字符（"aab"），因为接下来的 3 个字符相同。此时 s = "aab"。
- 删除第一个字符（"a"），因为下一个字符相同。此时 s = "ab"。
- 删除剩余的所有字符。
共使用了 4 次操作，返回 4。可以证明 4 是所需的最大操作次数。
```

**示例 3**  
```
Input: s = "aaaaa"
Output: 5
Explanation: 在每一次操作中，我们都可以删除字符串的第一个字符。
```

**约束条件**  
- `1 <= s.length <= 4000`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求把字符串 `s` 完全删掉，每一步只能删除 **前缀**，且删除的长度 `len` 必须满足：

- `s[0:len]` 与紧随其后的子串 `s[len:2*len]` 完全相同  
  （也就是说，前 `len` 个字符在后面紧接的 `len` 个字符里出现一次拷贝）

如果找不到这样长度的前缀，只能一次性把剩下的全部字符删掉。

**最直接的做法**就是：  
从左到右模拟删除过程。每次遍历所有可能的 `len`（从 1 到当前字符串长度的一半），检查 `s[:len] == s[len:2*len]` 是否成立。找到最小的合法 `len`（或者随意选一个合法 `len`），执行删除，然后继续对剩余的字符串重复同样的检查，直到字符串为空。

> **类比**：把字符串想成一排排相同的积木块。如果前面有一段积木恰好和紧跟在后面的那段积木一模一样，那么我们可以把前面那段积木一次性搬走。暴力做法就是把每一段可能的长度都试一遍，就像把手伸过去，一块块试能不能搬走。

**为什么这个方法一定能得到答案**  
因为我们在每一步都枚举了**所有**可能的合法删除长度，只要有办法删除，就一定会被找到。虽然我们不一定得到**最大**的操作次数（因为我们可能每次都选了最长的合法 `len`），但只要把每一步都执行完，最终一定会把字符串删光，得到一个合法的操作序列。

#### 代码（Python）

```python
def max_deletions_bruteforce(s: str) -> int:
    ops = 0                       # 已完成的操作次数
    while s:                      # 当字符串还有剩余时循环
        n = len(s)
        removed = False
        # 枚举可能的删除长度 len，最多只能到 n//2
        for l in range(1, n // 2 + 1):
            # 判断前缀 s[:l] 是否与后面的子串 s[l:2*l] 完全相同
            if s[:l] == s[l:2 * l]:
                s = s[l:]          # 删除前缀
                ops += 1
                removed = True
                break              # 找到一种合法删除后立刻跳出循环
        # 如果没有任何合法的前缀可以删除，就一次性把全部字符删掉
        if not removed:
            ops += 1
            break
    return ops
```

> 关键行解释  
> - `for l in range(1, n // 2 + 1)`: 只需要检查到一半长度，因为前缀要在后面还有对应的拷贝。  
> - `if s[:l] == s[l:2 * l]`: 直接用 Python 的切片比较，两段子串相等则可以删除。  
> - `s = s[l:]`: 把前缀“搬走”，保留下剩余的部分继续处理。

#### 复杂度

- **时间复杂度**：`O(n³)`（大白话：最坏情况下，每一次循环我们要遍历 `n/2` 种长度，每种长度比较两个子串需要 `O(n)`，而循环本身最坏会进行 `n` 次）  
- **空间复杂度**：`O(1)`（只用了常数个变量，字符串本身在原地切片，Python 会创建新对象但不随 `n` 成指数增长）

> 对于 `n ≤ 4000` 的约束，`O(n³)` 已经远远超出可接受范围，会在几秒甚至几分钟内超时。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要完整比较子串**，导致 `O(n³)`。我们需要两个改进：

1. **用 DP 记忆子问题**：  
   定义 `dp[i]` 为**删除前 `i+1` 个字符（即 `s[:i+1]`）**所能得到的最大操作次数。如果某段前缀根本不可删除，则 `dp[i] = -1` 表示“不可达”。这样我们把“大块”问题拆成“小块”问题，逐步递推。

2. **快速判断子串相等**：  
   使用 **滚动哈希（Rolling Hash）**（又叫 Rabin‑Karp 哈希）把每个子串映射成一个整数。比较两个子串是否相等，只需要比较它们的哈希值，时间从 `O(len)` 降到 `O(1)`（哈希冲突概率极低，实际可以视作不冲突）。

结合这两点，算法思路如下：

- 预处理：计算字符串的前缀哈希数组 `pref` 和幂数组 `pow_base`，这样任意子串 `[l, r]`（左闭右闭）的哈希可以在 `O(1)` 内得到。  
- DP 递推：遍历 `i` 从 `0` 到 `n-1`，尝试所有可能的删除长度 `len`（`1 ≤ len ≤ (i+1)//2`），检查是否满足 `s[i-len+1 : i+1]`（即当前前缀的最后 `len` 个字符） 与它前面的 `len` 个字符相等。  
  - 若相等且 `dp[i-len] != -1`，说明可以在已经得到的最佳方案 `dp[i-len]` 的基础上再加一次操作，更新 `dp[i] = max(dp[i], dp[i-len] + 1)`。  
- 额外的“直接删光”情况：如果 `dp[i]` 仍然是 `-1`，说明到这里为止没有合法的分割方式，那么我们可以一次性把 `s[:i+1]` 全部删掉，得到 `dp[i] = 1`（这对应暴力解里 “一次性删光” 的操作）。

最后答案是 `dp[n-1]`。

**滚动哈希细节**（零基础解释）  
- 把字母 `'a'~'z'` 映射成数字 `1~26`。  
- 选取一个大质数 `mod`（如 `10**9+7`）和一个基数 `base`（如 `91138233`）。  
- 前缀哈希 `pref[i]` 表示子串 `s[:i]` 的哈希值：`pref[i+1] = (pref[i] * base + val(s[i])) % mod`。  
- 任意子串 `[l, r]`（左闭右闭）的哈希为：  
  `hash(l, r) = (pref[r+1] - pref[l] * pow_base[r-l+1]) % mod`。  
  这就像把整条绳子（整个字符串）切成小段，直接算出每段的“指纹”。

> **为什么哈希能在 O(1) 比较？**  
> 把一段文字压缩成一个整数（指纹），相同的文字几乎一定得到相同的指纹。于是“这两段文字相等吗？”只要比较两个整数是否相同即可。

#### 代码（Python）

```python
def max_deletions(s: str) -> int:
    n = len(s)
    MOD = 10 ** 9 + 7          # 大质数，防止哈希冲突
    BASE = 91138233            # 随机选的基数，只要不是 1 且与 MOD 互质即可

    # ---------- 预处理：前缀哈希和幂数组 ----------
    pref = [0] * (n + 1)        # pref[i] = s[:i] 的哈希值
    pow_base = [1] * (n + 1)    # pow_base[i] = BASE^i % MOD

    for i, ch in enumerate(s):
        val = ord(ch) - ord('a') + 1          # a->1, b->2, ...
        pref[i + 1] = (pref[i] * BASE + val) % MOD
        pow_base[i + 1] = (pow_base[i] * BASE) % MOD

    # ---------- 辅助函数：取子串哈希 ----------
    def get_hash(l: int, r: int) -> int:
        """返回 s[l..r]（左闭右闭）的哈希值，时间 O(1)"""
        return (pref[r + 1] - pref[l] * pow_base[r - l + 1]) % MOD

    # ---------- DP ----------
    dp = [-1] * n                # dp[i] = 删除 s[:i+1] 的最大操作次数
    for i in range(n):
        # 尝试所有可能的删除长度 len（最多只能到 (i+1)//2）
        for length in range(1, (i + 1) // 2 + 1):
            # 前缀的后 half 与前 half 是否相等？
            # 前 half: s[i-2*length+1 : i-length+1]
            # 后 half: s[i-length+1 : i+1]
            if get_hash(i - 2 * length + 1, i - length) == get_hash(i - length + 1, i):
                # 若前面已经可以删到 i-length（即 dp[i-length] != -1）
                if dp[i - length] != -1:
                    dp[i] = max(dp[i], dp[i - length] + 1)

        # 如果仍然不可达，说明只能一次性把全部删掉
        if dp[i] == -1:
            dp[i] = 1   # 直接一次性删除 s[:i+1]

    return dp[-1]
```

> 关键行中文注释  
> - `pref[i + 1] = (pref[i] * BASE + val) % MOD`：把新字符加入哈希，就像把旧指纹左移并加上新字符的数值。  
> - `get_hash(l, r)`：利用前缀哈希的“减法”快速得到任意子串指纹。  
> - `if get_hash(...) == get_hash(...)`：只比较两个整数，判断两段子串是否相等。  
> - `dp[i] = max(dp[i], dp[i - length] + 1)`：把已经得到的最优方案再加一次合法删除。  
> - `if dp[i] == -1: dp[i] = 1`：没有任何合法切分，只能一次性删光。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `i`（0~n-1），内层最多遍历 `i//2` 种长度，二者相乘约等于 `n²/4`。  
  - 每一次比较子串相等只需 `O(1)` 哈希查询，所以整体是二次多项式。  
  - 对于 `n ≤ 4000`，`n² ≈ 1.6×10⁷`，在 Python 中仍能在毫秒级‑秒级完成。

- **空间复杂度**：`O(n)`  
  - 前缀哈希数组、幂数组以及 DP 数组各占 `n` 长度的整数列表。  
  - 与输入大小线性相关，符合题目限制。

> 与暴力解对比：我们把“每次比较子串”从 `O(len)` 降到了 `O(1)`，并且把“重复计算相同子问题”用 DP 记住，整体从 `O(n³)` 降到了 `O(n²)`，速度提升数百倍以上。

---

## 心得

- **核心技巧**：  
  1. **动态规划** 把全局最大操作次数拆解为子前缀的最优解。  
  2. **滚动哈希** 在 `O(1)` 时间内判断两个子串是否相等，避免 `O(len)` 的直接比较。

- **适用的题型**（相似思路可复用）：  
  - “删除子串后继续操作” 类的题，如 *Delete String*、*Remove Palindromic Substrings*。  
  - “判断子串相等/出现次数” 的题目，如 *Repeated Substring Pattern*、*Longest Repeated Substring*。  
  - 需要 **前缀划分** 并且子段相等的 DP 题目。

- **一句话总结解题钥匙**：  
  > 把“能否一次删除”抽象成“前缀与紧随其后的子串哈希相等”，再用 DP 把每一步的最佳次数累加即可。

---

## 反思

- **拿到题目第一反应**：  
  看到“前缀必须和后面的子串相同”立刻想到 **字符串匹配**（如 KMP、滚动哈希）来快速比较；同时因为要求“最大操作次数”，想到 **DP** 来记录每个位置的最优解。

- **最容易踩的坑**  
  1. **边界条件**：长度为 1 的字符串只能一次性删除，需要 `dp[i] = 1` 的默认处理。  
  2. **哈希取负**：`(a - b) % MOD` 在 Python 中可能为负数，需要再 `% MOD` 保证非负。  
  3. **长度计算错误**：在取子串哈希时要确保索引不越界，尤其 `i - 2*length + 1` 可能为负，只有在 `length ≤ (i+1)//2` 时才合法。  
  4. **冲突概率**：虽然单模数冲突概率极低，但在极端对手数据下可以使用双模数或直接比较子串（仍然是 O(1) 平均）。  

- **下次遇到同类题的第一步**：  
  > 先判断“是否可以在 O(1) 时间比较子串”。如果可以（哈希、前缀函数、Z‑函数等），就立刻用它来构造 DP/贪心的状态转移。这样既能保证正确性，又能把复杂度压到二次或更低。