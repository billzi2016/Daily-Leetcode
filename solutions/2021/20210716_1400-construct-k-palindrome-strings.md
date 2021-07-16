# #1400. **构造 K 个回文字符串** / Construct K Palindrome Strings

> 难度：中等 · 标签：Hash Table、String、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/construct-k-palindrome-strings/)

---

## 题目（英文原版）

**Description**

Given a string s and an integer k, return true if you can use all the characters in s to construct non-empty k palindrome strings or false otherwise.

**Examples**

**Example 1:**

```
Input: s = "annabelle", k = 2
Output: true
Explanation: You can construct two palindromes using all characters in s.
Some possible constructions "anna" + "elble", "anbna" + "elle", "anellena" + "b"
```

**Example 2:**

```
Input: s = "leetcode", k = 3
Output: false
Explanation: It is impossible to construct 3 palindromes using all the characters of s.
```

**Example 3:**

```
Input: s = "true", k = 4
Output: true
Explanation: The only possible solution is to put each character in a separate string.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters.
- 1 <= k <= 105

---

## 题目（中文翻译）

给定一个字符串 `s` 和一个整数 `k`，如果可以使用 `s` 中的全部字符构造恰好 `k` 个非空回文字符串（palindrome strings），返回 `true`，否则返回 `false`。

**示例 1**  
**输入**: `s = "annabelle", k = 2`  
**输出**: `true`  
**解释**: 可以用 `s` 的所有字符构造两个回文字符串。可能的构造方式包括 `"anna" + "elble"`、`"anbna" + "elle"`、`"anellena" + "b"` 等。

**示例 2**  
**输入**: `s = "leetcode", k = 3`  
**输出**: `false`  
**解释**: 无法使用 `s` 的全部字符构造 3 个回文字符串。

**示例 3**  
**输入**: `s = "true", k = 4`  
**输出**: `true`  
**解释**: 唯一可行的方案是把每个字符单独放入一个字符串中。

**约束条件**

- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成。
- `1 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有字符全排列**，然后尝试把它们切分成 `k` 段，检查每一段是否是回文串。  
- **全排列**：把字符串 `s` 的字符排成所有可能的顺序，就像把一副牌的每张牌都换位置一样。  
- **切分**：把排好序的字符序列划分成 `k` 份，每份必须非空。可以把切分点想成在一根绳子上打 `k‑1` 个结。

如果找到了某种排列和切分方式，使得每一段都是回文，则答案为 `True`，否则为 `False`。

**为什么这个方法能得到正确答案？**  
因为它穷举了所有可能的字符排列和所有可能的划分方式，只要有一种可行的构造，就一定会在枚举过程中出现。

**为什么会超时？**  
- `s` 长度最多 `10^5`，全排列的数量是 `n!`（阶乘），即使 `n=10` 也已经是 3,628,800 种。`n=20` 更是天文数字，根本不可能在计算机上跑完。  
- 切分的组合数也是指数级的，`C(n‑1, k‑1)`，同样会爆炸。

所以暴力解只能用来说明思路，实际不能在限制范围内通过。

#### 代码（Python）

```python
import itertools

def can_construct_bruteforce(s: str, k: int) -> bool:
    """
    暴力穷举所有字符排列和切分方式（仅作思路演示，实际不可用）。
    """
    n = len(s)
    if k > n:                     # k 不能大于字符数
        return False

    # 1) 枚举所有字符的排列
    for perm in set(itertools.permutations(s)):
        # 2) 在 n-1 个可能的切分点里选出 k-1 个
        for cuts in itertools.combinations(range(1, n), k - 1):
            start = 0
            ok = True
            # 检查每一段是否为回文
            for cut in cuts + (n,):          # 最后一个切点是字符串末尾
                part = perm[start:cut]
                if part != part[::-1]:      # 不是回文
                    ok = False
                    break
                start = cut
            if ok:
                return True
    return False
```

> **注意**：上述代码只用于说明“暴力思路”，在 `len(s) > 10` 时会直接卡死。

#### 复杂度  

- 时间复杂度：`O(n! * C(n‑1, k‑1) * n)`  
  - `n!` 表示所有排列的数量，`C(n‑1, k‑1)` 表示切分方式的组合数，`n` 用来检查每段是否是回文。  
  - 用大白话说，就是“几乎不可能在合理时间内算完”，所以不适用于本题的规模。

- 空间复杂度：`O(n)`  
  - 主要是存放一次排列（长度 `n`）和递归栈/迭代器的开销。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到**枚举所有排列是没有必要的**，因为回文字符串对字符的要求非常简单：

- 回文的左半边和右半边必须是相同的字符对。  
- 只能有 **0 或 1 个字符出现奇数次**（放在回文的中间），其余字符出现次数必须是偶数。

这意味着**只要我们知道每个字符出现的次数**，就能判断是否可以把所有字符拆分成 `k` 个回文串。

下面一步步推导：

1. **字符计数**  
   用哈希表（Python 的 `collections.Counter`）统计每个字母出现的次数。  
   哈希表可以类比为**查字典**：键是字母，值是出现次数。

2. **奇数次数的字符有多少**  
   遍历计数表，统计出现次数为奇数的字母个数，记为 `odd_cnt`。  
   这些字符只能各自成为一个回文的“中心”，因为中心只能放单个字符。

3. **最少需要的回文串数**  
   - 每个奇数次数的字符至少占用 **一个** 回文串（作为中心）。  
   - 其余字符（出现偶数次）可以自由配对，**可以放进已有的回文串**，也可以一起组成新的回文串。  
   因此，**构造回文串的下限就是 `odd_cnt`**。

4. **与 `k` 的关系**  
   - 如果 `k` 小于 `odd_cnt`，说明我们想要的回文串数量不够，每个奇数字符都需要一个独立的回文，这时不可能。  
   - 另一方面，如果 `k` 大于字符串长度 `len(s)`，显然不可能，因为每个回文串至少要有一个字符。  

5. **其余情况必然可行**  
   当 `odd_cnt <= k <= len(s)` 时，构造方案如下（不必真的实现，只要能说明可行性）：
   - 先把每个奇数字符单独放进一个回文串，形成 `odd_cnt` 个回文（每个只含一个字符或再配对一些偶数字符）。
   - 剩下的 `k - odd_cnt` 个回文串可以从 **任意的偶数字符对** 中拿出两个字符组成长度为 2 的回文（如 `"aa"`），或者直接把一个剩余的字符单独成串（因为此时 `k` 不会超过字符总数）。
   - 由于偶数字符可以自由配对，必能填满所有 `k` 个回文串，使得所有字符都被使用。

所以判断条件归结为：

```
len(s) >= k  且  odd_cnt <= k
```

如果同时满足，答案为 `True`，否则为 `False`。

#### 代码（Python）

```python
from collections import Counter

def can_construct_k_palindromes(s: str, k: int) -> bool:
    """
    判断是否能把字符串 s 的全部字符拆分成恰好 k 个非空回文串。
    思路：只需要统计出现奇数次的字符个数 odd_cnt。
    条件：len(s) >= k 且 odd_cnt <= k
    """
    n = len(s)
    if k > n:                     # 不够字符凑成 k 个非空串
        return False

    # 统计每个字符出现的次数
    cnt = Counter(s)              # 哈希表：字符 -> 次数

    # 计算出现奇数次的字符有多少个
    odd_cnt = sum(1 for v in cnt.values() if v % 2 == 1)

    # 判断能否构造
    return odd_cnt <= k           # 同时满足 k <= n 已在前面判断
```

#### 复杂度  

- 时间复杂度：`O(n)`  
  - 只遍历一次字符串统计字符出现次数（`n = len(s)`），再遍历哈希表（最多 26 个小写字母）统计奇数个数。  
  - 用大白话说，就是“和字符串长度成正比”，在 10⁵ 规模下毫秒级完成。

- 空间复杂度：`O(1)`（常数空间）  
  - 哈希表最多存 26 条记录（英文字母），不随 `n` 增长而增长，算是常数级别的额外空间。

---

## 心得

- **核心技巧**：利用回文字符串的“奇数字符只能出现在中心”这一特性，转化为**计数奇数字符的个数**来判断可行性。  
- **适用的题型**  
  1. “能否把字符重新排列成回文” （如 LeetCode 409）  
  2. “拆分为若干回文子串的最少数量” （如 LeetCode 1278）  
  3. “把字符串分成若干段，使每段满足某种字符频率限制” 的贪心计数类问题。  
- **一句话总结解题钥匙**：**奇数字符的数量决定最少需要多少回文串，只要 `k` 不小于它且不超过字符总数，就一定能做到。**

---

## 反思

- **第一反应**：看到“回文”和“k 个字符串”，自然想到把字符全排列或递归划分，结果发现不切实际。  
- **最容易踩的坑**  
  - 忽略 `k > len(s)` 的直接否定情况。  
  - 只考虑奇数字符数量，却忘记奇数字符本身也可以分配到已有的回文串中（但这不会降低最小需要的回文数）。  
  - 边界：`k == len(s)` 时，每个字符单独成串，这种情况下即使所有字符都是相同也必须返回 `True`。  
- **下次遇到同类题的第一步**：先**抽象出字符出现次数的约束**（奇偶性、出现次数上限/下限），把问题转化为“计数 + 简单比较”，而不是直接尝试构造。