# #1915. 美妙子串的数量 / Number of Wonderful Substrings

> 难度：中等 · 标签：Hash Table、String、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/number-of-wonderful-substrings/)

---

## 题目（英文原版）

**Description**

A wonderful string is a string where at most one letter appears an odd number of times.
Given a string word that consists of the first ten lowercase English letters ('a' through 'j'), return the number of wonderful non-empty substrings in word. If the same substring appears multiple times in word, then count each occurrence separately.
A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: word = "aba"
Output: 4
Explanation: The four wonderful substrings are underlined below:
- "aba" -> "a"
- "aba" -> "b"
- "aba" -> "a"
- "aba" -> "aba"
```

**Example 2:**

```
Input: word = "aabb"
Output: 9
Explanation: The nine wonderful substrings are underlined below:
- "aabb" -> "a"
- "aabb" -> "aa"
- "aabb" -> "aab"
- "aabb" -> "aabb"
- "aabb" -> "a"
- "aabb" -> "abb"
- "aabb" -> "b"
- "aabb" -> "bb"
- "aabb" -> "b"
```

**Example 3:**

```
Input: word = "he"
Output: 2
Explanation: The two wonderful substrings are underlined below:
- "he" -> "h"
- "he" -> "e"
```

**Constraints**

- 1 <= word.length <= 105
- word consists of lowercase English letters from 'a' to 'j'.

---

## 题目（中文翻译）

一个美妙字符串（wonderful string）是指至多有一个字母出现奇数次的字符串。  
给定只包含前十个小写英文字母（'a' 到 'j'）的字符串 `word`，返回 `word` 中所有 **非空** 美妙子串（wonderful substring）的数量。如果同一个子串在 `word` 中出现多次，则每次出现都要单独计数。  

子串（substring）是字符串中连续的一段字符序列。

## 示例

### 示例 1
**输入**  
```text
word = "aba"
```
**输出**  
```text
4
```
**解释**  
下面划线的四个子串都是美妙的：
- `"aba"` → `"a"`
- `"aba"` → `"b"`
- `"aba"` → `"a"`
- `"aba"` → `"aba"`

### 示例 2
**输入**  
```text
word = "aabb"
```
**输出**  
```text
9
```
**解释**  
下面划线的九个子串都是美妙的：
- `"aabb"` → `"a"`
- `"aabb"` → `"aa"`
- `"aabb"` → `"aab"`
- `"aabb"` → `"aabb"`
- `"aabb"` → `"a"`
- `"aabb"` → `"abb"`
- `"aabb"` → `"b"`
- `"aabb"` → `"bb"`
- `"aabb"` → `"b"`

### 示例 3
**输入**  
```text
word = "he"
```
**输出**  
```text
2
```
**解释**  
下面划线的两个子串都是美妙的：
- `"he"` → `"h"`
- `"he"` → `"e"`

## 约束条件
- `1 <= word.length <= 10^5`
- `word` 只由 `'a'` 到 `'j'` 的小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是枚举所有子串，统计每个子串里每个字符出现的次数，然后判断是否满足「至多只有一个字符出现奇数次」的条件。  

- **枚举子串**：用两个循环 `i`（子串左端）和 `j`（子串右端）遍历所有 `i ≤ j` 的区间。  
- **统计字符**：因为题目只涉及前 10 个小写字母（`a~j`），我们可以用长度为 10 的整数数组 `cnt[10]` 来记录子串中每个字母出现的次数。  
- **判断奇数个数**：遍历 `cnt`，统计出现奇数次的字母有多少个，只要 ≤ 1 就算是「wonderful」子串。

**生活化类比**：  
把字符串看成一本书，子串就是书中连续的若干页。我们逐页翻阅（遍历 `i`），每翻到一页就把这页的字母加入「字典」（`cnt`），相当于在查字典时把每个单词的出现次数记下来。最后检查字典里「奇数次出现的单词」是否不超过一个。

**为什么正确**：  
暴力遍历会检查每一种可能的子串，且对每个子串都完整统计了字符出现次数，完全符合题目定义，所以一定不会漏掉任何合法子串。

#### 代码（Python）

```python
def wonderfulSubstrings_brute(word: str) -> int:
    n = len(word)
    ans = 0

    # i 为子串左端
    for i in range(n):
        cnt = [0] * 10                 # 记录 a~j 的出现次数
        # j 为子串右端，逐渐扩展子串
        for j in range(i, n):
            idx = ord(word[j]) - ord('a')
            cnt[idx] += 1              # 加入新字符

            # 统计奇数次数的字母个数
            odd = 0
            for c in cnt:
                if c % 2 == 1:         # 出现奇数次
                    odd += 1
                if odd > 1:           # 已经超过 1 个，直接退出
                    break

            if odd <= 1:               # 符合“至多一个奇数”条件
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n² * 10)` → 简写为 `O(n²)`。  
  解释：外层两层循环形成 `n·(n+1)/2` ≈ `n²/2` 种子串，每次统计奇数次数需要遍历长度为 10 的数组，常数 10 可以忽略不计。  
- **空间复杂度**：`O(10)` → 简写为 `O(1)`。  
  只用了固定大小的计数数组 `cnt`，与字符串长度无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复统计**：相邻子串只差一个字符，却要重新遍历 10 次计数数组。我们可以把「每个前缀的字符奇偶性」抽象成一个 **位掩码**（bitmask），这样子串的奇偶信息就可以通过**前缀异或**快速得到。

**关键观察**  
- 对任意前缀 `word[0..i]`，用 10 位的二进制数表示每个字符出现次数的奇偶性：第 `k` 位为 `1` 表示字符 `'a'+k` 出现了奇数次，为 `0` 表示出现偶数次。  
- 子串 `word[l..r]` 的奇偶性等价于 **前缀 `r` 的掩码 XOR 前缀 `l-1` 的掩码**。因为相同的字符出现次数会相互抵消（偶数 ↔ 0），只留下两端不同的奇偶信息。  
- 题目要求子串「至多一个字符出现奇数次」 ⇔ `mask_substring` 的 **1 的个数 ≤ 1**。  
  因此我们只需要找 **前缀掩码** 与 **当前掩码** 差别在 0 位或 1 位的情况。

**如何快速计数**  
遍历字符串，一边维护当前前缀掩码 `cur`，一边在哈希表 `cnt` 中记录「已经出现过的每种掩码」出现的次数。对当前位置：

1. **完全相同**：若之前出现过相同的掩码 `cur`，则对应的子串奇偶掩码为全 0，符合条件。把 `cnt[cur]` 加到答案中。  
2. **只差一位**：尝试把 `cur` 的每一位 `k` 翻转（`cur ^ (1 << k)`），若该掩码在 `cnt` 中出现过，也说明有子串只剩下字符 `k` 出现奇数次，同样计入答案。  
3. 最后把当前掩码加入哈希表 `cnt[cur] += 1`，为后面的子串提供参考。

**类比**：  
想象每个前缀是一本账本，账本里用 10 个格子记录每种字母的「欠/多」情况（奇数视为欠 1，偶数视为清零）。当我们想知道从某天到今天的「欠」是多少时，只要把今天的账本和过去某天的账本做「相减」(异或) 就得到答案。我们只关心「欠 0」或「欠 1 种字母」的情况，于是把所有历史账本存进字典，遇到新账本时只要快速检查「相同」或「只差一格」的历史账本有多少即可。

#### 代码（Python）

```python
from collections import defaultdict

def wonderfulSubstrings(word: str) -> int:
    # 哈希表：key 为出现过的掩码，value 为该掩码出现的次数
    cnt = defaultdict(int)
    cnt[0] = 1               # 空前缀的掩码为 0，出现一次

    cur = 0                  # 当前前缀的掩码
    ans = 0

    for ch in word:
        # 更新当前掩码：对应字符的奇偶性取反
        bit = ord(ch) - ord('a')
        cur ^= 1 << bit      # 异或翻转第 bit 位

        # 1）掩码完全相同的情况
        ans += cnt[cur]

        # 2）掩码只差一位的情况，遍历 0~9 共十个字符
        for k in range(10):
            mask = cur ^ (1 << k)   # 翻转第 k 位
            ans += cnt[mask]

        # 3）把当前掩码计入哈希表，供后续使用
        cnt[cur] += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * 10)` → 简写为 `O(n)`。  
  解释：遍历字符串一次（`n` 次），每一步内部循环固定 10 次（因为只有 10 种字母），常数可以忽略。相比暴力的 `n²`，速度提升了好几个数量级。  
- **空间复杂度**：`O(2^10)` → 简写为 `O(1)`。  
  解释：掩码只占 10 位，总共有 `2^10 = 1024` 种可能，哈希表最多存这么多键，空间大小与 `n` 无关，视作常量。

---

## 心得

- **核心技巧**：利用**位掩码 + 前缀异或 + 哈希计数**，把「字符出现奇偶」压缩到 10 位整数中，从而在 O(1) 时间内判断子串是否合法。  
- **适用题型**：  
  1. 「字母出现次数的奇偶」类问题（如 LeetCode 1371. 同时拥有 0 和 1 的子数组）。  
  2. 「至多 K 个奇数」的子串计数（可将 K 扩展为 2、3，只需枚举更多位的组合）。  
  3. 「回文可 rearrange」的子串计数（同样用奇偶位掩码）。  
- **一句话总结**：  
  **把「出现次数的奇偶」映射成位掩码，前缀异或让子串信息瞬间得到，哈希表把「相同或相差一位」的计数变为 O(1)。**

---

## 反思

- **第一反应**：直接想到枚举子串并统计，忽视了题目只涉及 10 种字母这一重要限制。  
- **最容易踩的坑**：  
  - **忘记计入空前缀**：若不把 `cnt[0]=1` 放在初始化，第一段子串会少算一次。  
  - **位运算错误**：`cur ^= 1 << bit` 必须是异或而不是或或与，否则奇偶翻转不正确。  
  - **统计重复**：在遍历 `k` 时要确保不把 `cur` 本身再次算进（虽然 `cnt[cur]` 已在第一步计入，单独再加会导致重复）。  
- **下次思路**：遇到「奇偶次数」或「至多 K 种不同」的限制时，第一步就把字符状态压缩成位掩码；随后考虑前缀/后缀配合哈希计数，避免 O(n²) 的暴力。