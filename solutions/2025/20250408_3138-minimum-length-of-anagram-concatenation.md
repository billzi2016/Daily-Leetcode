# #3138. 字母异位词拼接的最小长度 / Minimum Length of Anagram Concatenation

> 难度：中等 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-length-of-anagram-concatenation/)

---

## 题目（英文原版）

**Description**

You are given a string s, which is known to be a concatenation of anagrams of some string t.
Return the minimum possible length of the string t.
An anagram is formed by rearranging the letters of a string. For example, "aab", "aba", and, "baa" are anagrams of "aab".

**Examples**

**Example 1:**

```
Input: s = "abba"
Output: 2
Explanation:
One possible string t could be "ba" .
```

**Example 2:**

```
Input: s = "cdef"
Output: 4
Explanation:
One possible string t could be "cdef" , notice that t can be equal to s .
```

**Example 3:**

```
Input: s = "abcbcacabbaccba"
Output: 3
```

**Constraints**

- 1 <= s.length <= 105
- s consist only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，已知它是若干个字符串 `t` 的字母异位词（anagram）拼接而成。请返回字符串 `t` 可能的最小长度。

字母异位词是通过重新排列一个字符串的字符得到的。例如，`"aab"`、`"aba"`、`"baa"` 都是字符串 `"aab"` 的字母异位词。

### 示例

#### 示例 1
**输入**: `s = "abba"`  
**输出**: `2`  
**解释**:  
一种可能的 `t` 为 `"ba"` 。

#### 示例 2
**输入**: `s = "cdef"`  
**输出**: `4`  
**解释**:  
一种可能的 `t` 为 `"cdef"`，注意 `t` 可以等于 `s` 本身。

#### 示例 3
**输入**: `s = "abcbcacabbaccba"`  
**输出**: `3`

### 约束条件
- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的 t 长度都穷举一遍**，只要满足题目要求就返回最小的那一个。

1. 设 `n = len(s)`。显然 `t` 的长度 `d` 必须是 `n` 的因子（因为 `s` 是若干个等长的块拼起来的）。
2. 对每个因子 `d`（从小到大），把 `s` 按 `d` 切成 `k = n // d` 段。  
   - 取第一段的字符计数（比如 `{'a':2, 'b':1}`）作为候选的 `t` 的字符分布。  
   - 再遍历其余 `k-1` 段，逐段统计字符计数并和第一段比较。如果所有段的计数都相同，则说明这 `d` 可以作为 `t` 的长度。
3. 第一个满足条件的 `d` 就是答案。

> **类比**：把 `t` 想成一本字典，`s` 就是把这本字典的所有页（每页是 `t` 的一个排列）连在一起。我们只需要找到最短的“页”长度，使得每一页的字母分布都相同。

**为什么正确**：如果 `s` 真的是若干个 `t` 的全排列拼起来的，那么每一段的字符计数一定完全相同；反之，如果我们找到了一个 `d` 使得每段计数相同，就可以把这段计数当作 `t`，于是 `s` 就满足题意。

#### 代码（Python）

```python
from collections import Counter

def min_length_bruteforce(s: str) -> int:
    n = len(s)
    # 1~n 的所有可能长度（只保留能整除 n 的）
    for d in range(1, n + 1):
        if n % d != 0:          # 不是因子直接跳过
            continue
        k = n // d               # 需要的块数

        # 取第一块的字符计数作为参考
        first_block = Counter(s[:d])

        ok = True
        # 检查其余块是否和第一块计数相同
        for i in range(1, k):
            block = Counter(s[i * d:(i + 1) * d])
            if block != first_block:
                ok = False
                break

        if ok:                   # 第一个满足的 d 即为最小长度
            return d
    return n   # 理论上不会走到这里，因为 d = n 总是可行的
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层循环最多遍历 `n` 次（所有因子），内层对每个候选长度要遍历整串 `s`（`O(n)`），最坏情况是 `n` 接近 10⁵ 时会非常慢。  
  - 大白话：如果把 `s` 看成 10 万本书，暴力解要把每本书的每一页都重新检查一遍，工作量呈平方增长。

- **空间复杂度**：`O(1)`（不计计数器的常数大小）  
  - 只用了几个计数器，和字符串长度无关。

---

### 2. 最优解

#### 思路  

从暴力解我们可以发现**真正的瓶颈在于每次都要遍历整段字符计数**。其实我们根本不需要把 `s` 按块去检查，只要看**整体字符出现的次数**就可以判断哪些块长度是合法的。

关键观察：

- 设 `k` 为块数（`k = n / d`），`t` 的字符计数记作 `cnt_t`，`s` 的整体字符计数记作 `cnt_s`。  
- 因为 `s` 是 `k` 个 `t` 的全排列拼接，**每个字符在 `s` 中出现的次数一定是 `k` 的整数倍**，即 `cnt_s[c] = k * cnt_t[c]`。  
- 于是，只要 `cnt_s[c]` 能被 `k` 整除（对所有 26 个字母），我们就可以把 `cnt_t[c] = cnt_s[c] // k` 作为候选的 `t`。  

所以判断一个长度 `d` 是否可行，只需要：

1. 计算 `cnt_s`（一次遍历，得到每个字母出现的次数）。  
2. 对每个可能的块数 `k`（即 `n / d`），检查 `cnt_s[c] % k == 0` 是否对所有字母成立。  
3. 找到最小的 `d`（即最大的 `k`）即可。

因为 `d` 必须是 `n` 的因子，我们只需要枚举 **所有因子**，并且**从大到小枚举块数 `k`**（对应的 `d` 从小到大），这样一旦找到合法的 `k`，对应的 `d` 就是答案，后面就不必继续检查。

> **类比**：把 `cnt_s` 看成一大箱子装满了字母，每次我们想把它平分成 `k` 份（每份对应一个 `t`），只有当每种字母的数量都能被 `k` 整除时，才能做到“平分”。这就像把糖果平分给孩子，只有每种糖果的数量是孩子数的整数倍，才能每个孩子得到相同的糖果袋。

#### 代码（Python）

```python
import math
from collections import Counter

def min_length_optimal(s: str) -> int:
    n = len(s)
    total = Counter(s)                     # 整体字符计数，只遍历一次

    # 先把 n 的所有因子收集起来，按块数 k 从大到小遍历（即 d 从小到大）
    divisors = []
    for i in range(1, int(math.isqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)            # i 是因子
            if i != n // i:
                divisors.append(n // i)   # 对应的另一个因子

    # 按块数 k = n // d 从大到小排序（等价于 d 从小到大）
    divisors.sort(key=lambda d: n // d, reverse=True)

    for d in divisors:
        k = n // d                         # 需要的块数
        # 检查每个字母的总次数是否能被块数整除
        if all(cnt % k == 0 for cnt in total.values()):
            return d                       # 第一个满足的 d 即为最小长度
    return n                               # 安全返回，实际上不会到这里
```

#### 复杂度  

- **时间复杂度**：`O(n + 26 * √n)`  
  - `O(n)` 用于一次遍历统计 `cnt_s`。  
  - 枚举因子最多 `2 * √n` 个（因为每对因子对应一次循环），对每个因子检查 26 个字母的可整除性，常数非常小。整体上接近线性，远快于平方级的暴力解。  
  - 大白话：我们只需要把字符串扫一遍，然后再检查几百次（而不是上万次），所以速度几乎是“瞬间完成”。

- **空间复杂度**：`O(1)`（只存 26 个计数）  
  - `Counter` 只会保存 26 条记录，和字符串长度无关。

---

## 心得

- **核心技巧**：**利用整体字符计数与块数的整除关系**，把“逐块比较”转化为“全局计数能否平分”。  
- **适用的题型**  
  1. “字符串由若干个相同字符多重集的排列组成”——如 *Minimum Length of Anagram Concatenation*。  
  2. “把数组/字符串拆分成若干等价子块”——如 *Split Array into Equal Sum Subarrays*。  
  3. “求最小的基字符串长度”——如 *Find the Length of the Smallest Repeating Substring*。  
- **一句话总结解题钥匙**：**先算整体频次，再让块数去“整除”它们**。

---

## 反思

- **第一反应**：看到“拼接的字母异位词”，立刻想到把字符串分块、逐块比较——这就是暴力思路。  
- **最容易踩的坑**  
  - 忽视 **因子必须是整数**：直接遍历 `1..n` 会导致大量无效检查。  
  - 忽略 **空字符串或单字符** 的特殊情况（本题已限定长度 ≥1）。  
  - 在检查整除时忘记遍历 **所有 26 个字母**，导致错误的“通过”。  
- **下次遇到同类题**，第一步应该：**先统计全局信息（频次或前缀和），再用数学性质（整除、最大公约数等）快速筛选候选**。这样可以把 O(n²) 的暴力直接压到 O(n)。