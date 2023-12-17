# #2514. 计数变位词 / Count Anagrams

> 难度：困难 · 标签：Hash Table、Math、String、Combinatorics、Counting · [LeetCode 链接](https://leetcode.com/problems/count-anagrams/)

---

## 题目（英文原版）

**Description**

You are given a string s containing one or more words. Every consecutive pair of words is separated by a single space ' '.
A string t is an anagram of string s if the ith word of t is a permutation of the ith word of s.
Return the number of distinct anagrams of s. Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "too hot"
Output: 18
Explanation: Some of the anagrams of the given string are "too hot", "oot hot", "oto toh", "too toh", and "too oht".
```

**Example 2:**

```
Input: s = "aa"
Output: 1
Explanation: There is only one anagram possible for the given string.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of lowercase English letters and spaces ' '.
- There is single space between consecutive words.

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `s`，其中包含一个或多个单词。相邻的单词之间仅由一个空格 `' '` 分隔。  
如果字符串 `t` 的第 `i` 个单词是字符串 `s` 的第 `i` 个单词的一个排列（permutation），则称 `t` 为 `s` 的一个变位词（anagram）。  
返回 `s` 的不同变位词的数量。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

**示例**  

*示例 1*  
```
Input: s = "too hot"
Output: 18
Explanation: 给定字符串的一些变位词包括 "too hot"、"oot hot"、"oto toh"、"too toh"、"too oht" 等。
```

*示例 2*  
```
Input: s = "aa"
Output: 1
Explanation: 对于该字符串仅有一种可能的变位词。
```

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母和空格 `' '` 构成。  
- 相邻单词之间恰好有一个空格。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每个单词的所有字符全排列**，然后把每个单词的排列组合起来得到整句话的所有可能。  

- **数据结构**：把字符串先用 `split(' ')` 分成单词列表，随后对每个单词使用 Python 的 `itertools.permutations` 生成所有排列。`itertools.permutations` 类似于把字典的每一页都翻一遍，列出所有可能的词序。  
- **正确性**：因为题目要求第 *i* 个单词必须是原来第 *i* 个单词的一个排列，只要我们把每个单词的所有排列枚举出来，再把第 0、1、2… 个单词的排列两两组合，就一定能得到**所有合法的 anagram**。  
- **时间/空间复杂度**：  
  - 对一个长度为 `k` 的单词，所有排列的数量是 `k!`（k 的阶乘），这在 `k` 稍大时会爆炸。  
  - 假设句子里有 `m` 个单词，长度分别为 `k1, k2, …, km`，则总的排列数是 `k1! * k2! * … * km!`。即使只计算一次，这也会远远超过机器的运算能力。  
  - 用大白话说，`O(k!)` 就像“从 1 到 k 按顺序排队的方式有多少种”，比如 `k=10` 就已经是 3,628,800 种，`k=20` 更是 2.4×10¹⁸ 种，根本不可能在几秒钟内枚举完。  

#### 代码（Python）  

```python
import itertools

def count_anagrams_brute(s: str) -> int:
    words = s.split(' ')               # 把句子拆成单词列表
    # 对每个单词生成所有排列（每个排列是一个元组）
    perms_per_word = [list(itertools.permutations(w)) for w in words]

    # 计算所有单词排列的笛卡尔积，即所有可能的整句组合
    total = 0
    for combo in itertools.product(*perms_per_word):
        # 把每个单词的元组重新拼成字符串
        anagram = ' '.join(''.join(p) for p in combo)
        total += 1                       # 每出现一次就计数一次
    return total
```

> **注意**：这段代码只能在极小的测试用例（比如每个单词长度 ≤ 5）下跑通，真实的 `s.length ≤ 10⁵` 完全不可行。  

#### 复杂度  

- **时间复杂度**：`O(k1! * k2! * … * km!)`，指数级爆炸，实际不可接受。  
- **空间复杂度**：同样是 `O(k1! + k2! + … + km!)`，因为要把所有排列都存下来。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于枚举每个单词的全部排列。实际上，我们根本不需要把每一种排列都列出来，只要知道每个单词有多少种不同的排列数，就可以把这些数量相乘得到答案。  

**关键点**：  
1. **排列数的公式**  
   对于一个长度为 `k`、字符出现次数分别为 `c1, c2, …, ct`（`c1 + c2 + … + ct = k`）的单词，**不同排列的数量**是  

   \[
   \frac{k!}{c_1! \times c_2! \times \dots \times c_t!}
   \]

   这叫**多重集合排列公式**。  
   - 分子 `k!` 表示如果所有字符都不相同，排列方式有多少种（全排列）。  
   - 分母把因为相同字符导致的“重复计数”全部除掉。  

2. **模运算**  
   题目要求对 `10^9+7` 取模（记作 `MOD`），所以所有乘法和除法都要在模空间里完成。除法可以转化为乘以**模逆元**（在素数模下使用费马小定理）。  
   - `a^{-1} ≡ a^{MOD-2} (mod MOD)`，这就是**模逆**的计算方法。  

3. **预处理阶乘和逆阶乘**  
   为了在 O(1) 时间内得到任意 `k!`、`c!` 的值，我们在程序开始时一次性**预计算**到最大可能的 `k`（即整个字符串最长单词的长度，最多 `10⁵`）。  
   - `fact[i] = i! % MOD`  
   - `inv_fact[i] = (i!)^{-1} % MOD`（用快速幂求 `fact[i]^{MOD-2}`）  

4. **整体答案**  
   对每个单词计算上面的排列数 `cnt_i`，最终答案是  

   \[
   ans = \prod_{i=1}^{m} cnt_i \pmod{MOD}
   \]

   只需要一次遍历所有单词即可。  

#### 代码（Python）  

```python
MOD = 10**9 + 7

def mod_pow(a: int, e: int) -> int:
    """快速幂：计算 a^e % MOD，时间 O(log e)"""
    res = 1
    a %= MOD
    while e:
        if e & 1:
            res = res * a % MOD
        a = a * a % MOD
        e >>= 1
    return res

def prepare_factorials(n: int):
    """预计算 0..n 的阶乘和逆阶乘，返回两个列表"""
    fact = [1] * (n + 1)          # fact[i] = i! % MOD
    for i in range(1, n + 1):
        fact[i] = fact[i - 1] * i % MOD

    inv_fact = [1] * (n + 1)      # inv_fact[i] = (i!)^{-1} % MOD
    inv_fact[n] = mod_pow(fact[n], MOD - 2)   # 先算出 n! 的逆元
    for i in range(n, 0, -1):
        # 由 (i-1)! = i! / i 可得逆元的递推关系
        inv_fact[i - 1] = inv_fact[i] * i % MOD
    return fact, inv_fact

def count_anagrams(s: str) -> int:
    words = s.split(' ')
    # 统计所有单词中出现的最大长度，作为阶乘上限
    max_len = max(len(w) for w in words)

    fact, inv_fact = prepare_factorials(max_len)

    ans = 1
    for w in words:
        k = len(w)                     # 单词总字符数
        # 统计每个字符出现次数
        freq = {}
        for ch in w:
            freq[ch] = freq.get(ch, 0) + 1

        # 先把 k! 放进去
        cnt = fact[k]
        # 再除以每个字符的 ci!（使用模逆元相乘）
        for c in freq.values():
            cnt = cnt * inv_fact[c] % MOD

        ans = ans * cnt % MOD          # 把不同单词的排列数相乘
    return ans
```

**代码要点解释**  

| 行号 | 中文注释 |
|------|----------|
| 1    | 常量 `MOD` 为题目给出的 10⁹+7（素数），后面所有运算都在它之下取模 |
| 4‑12 | `mod_pow` 实现 **快速幂**，把指数拆成二进制，时间是 `O(log e)`，用于求模逆 |
| 14‑24| `prepare_factorials` 预先算出所有 `i!` 与 `(i!)^{-1}`，只遍历一次，整体是 `O(max_len)` |
| 28‑30| 把输入字符串按空格拆成单词列表 |
| 32‑33| 找出最长单词的长度，决定需要的阶乘上限（最多 10⁵） |
| 35‑36| 调用预处理，得到 `fact`、`inv_fact` 两个数组 |
| 38‑48| 对每个单词：<br>① 统计字符频次；<br>② 用公式 `k! / (c1! * c2! …)` 计算该单词的不同排列数 `cnt`，除法转成乘以逆元；<br>③ 把 `cnt` 累乘到全局答案 `ans` 中 |
| 49   | 返回最终答案（已经对 `MOD` 取模） |

#### 复杂度  

- **时间复杂度**：  
  - 预处理阶乘 `O(max_len)`，`max_len ≤ 10⁵`。  
  - 主循环遍历所有字符一次，即 `O(|s|)`。  
  - 整体是 **O(|s| + max_len)**，在本题的约束下即 **O(n)**（线性）。  

- **空间复杂度**：  
  - 两个长度为 `max_len+1` 的数组各占 `O(max_len)`。  
  - 其它额外空间（如频率字典）最多是单词长度的大小，整体是 **O(max_len)**，即 **O(n)**。  

相比暴力解，时间从指数级 `k!` 降到了线性 `n`，空间也从爆炸式下降到可接受的几百 KB。  

---

## 心得  

- **核心技巧**：利用**多重集合排列公式**结合**模逆**求解字符出现重复时的排列数，再把各单词的结果相乘。  
- **适用的题型**：  
  1. “统计不同排列数” 类的计数题（如 “Number of Ways to Rearrange a String”）。  
  2. “组合计数 + 重复元素” 的问题（如 “Unique Letter String” 中的计数思路）。  
  3. 需要对大数取模的排列/组合题（如 “Count Good Substrings” 中的组合计数）。  
- **一句话总结解题钥匙**：**先算出每个单词的“去重后全排列数”，再把它们相乘**。  

---

## 反思  

- **第一反应**：直接想把每个单词的所有排列枚举出来，然后拼接成句子，结果马上发现不可行。  
- **最容易踩的坑**：  
  - **重复字符导致的过计数**：忘记除以每个字符的阶乘会把相同排列算成不同的。  
  - **模逆的实现**：直接使用除法会出错，需要把除法转成乘以 `a^{MOD-2}`。  
  - **预处理上限**：若只预处理到 `26`（字母数），会在长单词（长度 > 26）时数组越界。  
- **下次类似题的第一步**：先**写出计数公式**（全排列 / 组合），判断是否有“重复元素”，再考虑**模运算**和**预处理**，最后实现。