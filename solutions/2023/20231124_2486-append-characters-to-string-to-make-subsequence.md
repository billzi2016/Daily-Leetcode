# #2486. 向字符串末尾追加字符使其成为子序列 / Append Characters to String to Make Subsequence

> 难度：中等 · 标签：Two Pointers、String、Greedy · [LeetCode 链接](https://leetcode.com/problems/append-characters-to-string-to-make-subsequence/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t consisting of only lowercase English letters.
Return the minimum number of characters that need to be appended to the end of s so that t becomes a subsequence of s.
A subsequence is a string that can be derived from another string by deleting some or no characters without changing the order of the remaining characters.

**Examples**

**Example 1:**

```
Input: s = "coaching", t = "coding"
Output: 4
Explanation: Append the characters "ding" to the end of s so that s = "coachingding".
Now, t is a subsequence of s ("coachingding").
It can be shown that appending any 3 characters to the end of s will never make t a subsequence.
```

**Example 2:**

```
Input: s = "abcde", t = "a"
Output: 0
Explanation: t is already a subsequence of s ("abcde").
```

**Example 3:**

```
Input: s = "z", t = "abcde"
Output: 5
Explanation: Append the characters "abcde" to the end of s so that s = "zabcde".
Now, t is a subsequence of s ("zabcde").
It can be shown that appending any 4 characters to the end of s will never make t a subsequence.
```

**Constraints**

- 1 <= s.length, t.length <= 105
- s and t consist only of lowercase English letters.

---

## 题目（中文翻译）

给定两个仅由小写英文字母组成的字符串 `s` 和 `t`。返回需要在 `s` 的末尾追加的最少字符数，使得 `t` 成为 `s` 的子序列（subsequence）。

**子序列（subsequence）** 是指可以通过删除原字符串中的任意个（包括零个）字符而不改变其余字符相对顺序得到的字符串。

## 示例

### 示例 1
**输入**: `s = "coaching"`, `t = "coding"`  
**输出**: `4`  
**解释**: 在 `s` 的末尾追加字符 `"ding"`，得到 `s = "coachingding"`。此时 `t` 是 `s` 的子序列（"coachingding"）。可以证明，追加任意 3 个字符都无法使 `t` 成为子序列。

### 示例 2
**输入**: `s = "abcde"`, `t = "a"`  
**输出**: `0`  
**解释**: `t` 已经是 `s` 的子序列（"abcde"）。

### 示例 3
**输入**: `s = "z"`, `t = "abcde"`  
**输出**: `5`  
**解释**: 在 `s` 的末尾追加字符 `"abcde"`，得到 `s = "zabcde"`。此时 `t` 是 `s` 的子序列（"zabcde"）。可以证明，追加任意 4 个字符都无法使 `t` 成为子序列。

## 约束条件
- `1 <= s.length, t.length <= 10^5`
- `s` 和 `t` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的字符都加到 s 的末尾，然后检查 t 是否成为子序列**。  
具体步骤可以这样写：

1. 枚举要追加的字符数 `k`（从 0 开始递增）。  
2. 对每个 `k`，把所有可能的 `k` 长字符串（由 `'a'~'z'` 组成）拼在 `s` 后面，得到 `s'`。  
3. 检查 `t` 是否是 `s'` 的子序列：从左到右遍历 `s'`，遇到和 `t` 当前字符相同就向前走一步，最后看是否把 `t` 全部匹配完。  
4. 第一个能够匹配成功的 `k` 就是答案。

> **生活化类比**：  
> 想象你在一本书里找一段话（t），但书的后面缺页。暴力解相当于“把所有可能的后页都印出来”，再逐页检查能否找到完整的句子。显然，这种“把所有可能的后页都印出来”在实际中根本不可行，因为可能的组合天文数字。

#### 代码（Python）

```python
import itertools
import string

def is_subsequence(s: str, t: str) -> bool:
    """检查 t 是否是 s 的子序列（双指针实现）"""
    i = j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            j += 1          # 两个指针都向前走
        i += 1              # s 的指针总是向前走
    return j == len(t)      # j 走完说明匹配成功

def brute_force(s: str, t: str) -> int:
    """暴力搜索最小的追加字符数（不可行，仅作思路演示）"""
    alphabet = string.ascii_lowercase
    # 从 0 开始尝试追加字符数
    for k in range(len(t) + 1):
        # 产生所有长度为 k 的字符组合（这里用 product，实际会爆炸）
        for added in itertools.product(alphabet, repeat=k):
            new_s = s + ''.join(added)
            if is_subsequence(new_s, t):
                return k
    return len(t)   # 最坏情况，需要把整个 t 加进去
```

> **注意**：上述代码在 `len(t) = 10` 时已经不可运行，因为 `26^k` 的组合数会迅速爆炸。它仅用于说明“最笨的思路”。

#### 复杂度

- **时间复杂度**：`O( Σ_{k=0}^{|t|} 26^k * (|s|+k) )`  
  也就是 **指数级**（指数 = 26 的 k 次方），在最坏情况下相当于 `O(26^{|t|})`，远远超出题目限制。  
  大白话：想象每增加一个字符，就要把 26 种可能都尝试一次，几乎不可能在合理时间内算完。

- **空间复杂度**：`O(k)`（临时保存追加字符的字符串），同样是指数级的，因为需要存很多组合。

> 结论：暴力解虽然概念最直接，但在实际中根本不可用，需要寻找更聪明的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点不在于“到底要加什么”，而在于我们需要知道已经有多少字符可以直接匹配**。  
如果我们能找出 **t 的最长前缀**（从左到右的连续子串）已经是 **s 的子序列**，那么剩下的字符必然要追加到 s 的末尾。  

**关键观察**：

- 子序列的匹配顺序必须保持，但可以跳过 s 中不需要的字符。  
- 当我们从左到右遍历 `s` 与 `t` 时，只要字符相同，就可以把它们配对，两个指针都往前走；否则只能把 `s` 的指针往前走，等下一次机会。  
- 这个过程正好找到了 **t 在 s 中能够匹配的最长前缀**。  

**为什么这样最优**：

- 每个字符只遍历一次，时间是线性的 `O(|s| + |t|)`。  
- 只用了两个整数变量记录指针位置，空间是 `O(1)`（常数级）。  

**类比**：  
想象你在一条河里找石头（t 的字符），而河里漂着很多木头（s 的字符）。你只能顺着河流（从左到右）前进，遇到想要的石头就拿走，木头不需要的就直接划过去。你最终能拿到的石头序列，就是 t 能在 s 中匹配的最长前缀。

**实现步骤**：

1. 初始化两个指针 `i`（指向 s）和 `j`（指向 t），均从 0 开始。  
2. 当 `i < len(s)` 且 `j < len(t)` 时：  
   - 如果 `s[i] == t[j]`，说明这两个字符可以配对，`j += 1`（t 前进），`i += 1`（s 前进）。  
   - 否则，只把 `i += 1`（s 前进），继续寻找匹配机会。  
3. 循环结束后，`j` 的值就是 **已经匹配成功的字符数**，即 t 的最长前缀长度。  
4. 需要追加的字符数 = `len(t) - j`。

#### 代码（Python）

```python
def appendCharacters(s: str, t: str) -> int:
    """
    返回最少需要在 s 末尾追加的字符数，使 t 成为 s 的子序列。
    思路：双指针贪心，只遍历一次字符串。
    """
    i = j = 0                 # i 指向 s，j 指向 t
    while i < len(s) and j < len(t):
        if s[i] == t[j]:      # 匹配成功，两个指针都向前走
            j += 1
        i += 1                # s 的指针总是向前走
    # 循环结束时，j 已经是 t 中能够匹配的最长前缀长度
    return len(t) - j         # 剩下的字符必须全部追加
```

> **代码解读**  
> - 第 4 行 `i = j = 0`：一次性声明两个指针，都是从字符串开头开始。  
> - 第 6 行 `while i < len(s) and j < len(t)`: 同时保证两个指针没有越界。  
> - 第 7‑9 行：如果当前字符相等，说明找到了一个可以配对的字符，`j` 前进表示 t 的匹配进度增加；不管匹配不匹配，`i` 必须前进，因为我们已经检查过 s 的这个位置。  
> - 第 12 行：`len(t) - j` 正好是 t 剩余未匹配的字符数，这些字符只能直接追加到 s 的尾部。

#### 复杂度

- **时间复杂度**：`O(|s| + |t|)`  
  只遍历了两个字符串各一次。大白话：如果 s 长 100 万，t 长 10 万，最多走 110 万步，完全可以在一秒内完成。

- **空间复杂度**：`O(1)`  
  只用了几个整数变量，不随输入规模增长。

> 与暴力解相比，时间从 **指数级** 降到了 **线性级**，空间也从 **指数级** 降到 **常数级**，是可接受的最优解。

---

## 心得

- **核心技巧**：**双指针贪心**——一次遍历两个字符串，找出 t 能在 s 中匹配的最长前缀。  
- **适用题型**：  
  1. 判断一个字符串是否是另一个的子序列（LeetCode 392）。  
  2. 最长公共子序列的长度（可用双指针的变形实现，尤其在字符顺序固定时）。  
  3. “删除最少字符使两串相等” 类似的匹配问题。  
- **解题钥匙**：**只关心匹配进度**，不必真的去“构造”追加的字符，剩余未匹配的部分自然就是要追加的内容。

---

## 反思

- **第一反应**：看到“把字符追加到末尾”，本能想把所有可能的字符枚举——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忽略了“子序列”可以跳过字符，以为必须一次对应。  
  - 在实现双指针时忘记 `i` 必须始终前进，导致死循环。  
  - 边界条件：当 `t` 完全已经是 `s` 的子序列时，`j` 直接等于 `len(t)`，返回 0。  
- **下次遇到同类题**：第一步先**思考能否一次遍历完成匹配**，即“把两个指针放在各自字符串的开头，逐字符比较”。如果能，这类题通常可以用 **双指针/贪心** 在 `O(n)` 时间解决。