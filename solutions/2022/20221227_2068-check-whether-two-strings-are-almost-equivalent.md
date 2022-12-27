# #2068. 检查两个字符串是否几乎等价 / Check Whether Two Strings are Almost Equivalent

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/check-whether-two-strings-are-almost-equivalent/)

---

## 题目（英文原版）

**Description**

Two strings word1 and word2 are considered almost equivalent if the differences between the frequencies of each letter from 'a' to 'z' between word1 and word2 is at most 3.
Given two strings word1 and word2, each of length n, return true if word1 and word2 are almost equivalent, or false otherwise.
The frequency of a letter x is the number of times it occurs in the string.

**Examples**

**Example 1:**

```
Input: word1 = "aaaa", word2 = "bccb"
Output: false
Explanation: There are 4 'a's in "aaaa" but 0 'a's in "bccb".
The difference is 4, which is more than the allowed 3.
```

**Example 2:**

```
Input: word1 = "abcdeef", word2 = "abaaacc"
Output: true
Explanation: The differences between the frequencies of each letter in word1 and word2 are at most 3:
- 'a' appears 1 time in word1 and 4 times in word2. The difference is 3.
- 'b' appears 1 time in word1 and 1 time in word2. The difference is 0.
- 'c' appears 1 time in word1 and 2 times in word2. The difference is 1.
- 'd' appears 1 time in word1 and 0 times in word2. The difference is 1.
- 'e' appears 2 times in word1 and 0 times in word2. The difference is 2.
- 'f' appears 1 time in word1 and 0 times in word2. The difference is 1.
```

**Example 3:**

```
Input: word1 = "cccddabba", word2 = "babababab"
Output: true
Explanation: The differences between the frequencies of each letter in word1 and word2 are at most 3:
- 'a' appears 2 times in word1 and 4 times in word2. The difference is 2.
- 'b' appears 2 times in word1 and 5 times in word2. The difference is 3.
- 'c' appears 3 times in word1 and 0 times in word2. The difference is 3.
- 'd' appears 2 times in word1 and 0 times in word2. The difference is 2.
```

**Constraints**

- n == word1.length == word2.length
- 1 <= n <= 100
- word1 and word2 consist only of lowercase English letters.

---

## 题目（中文翻译）

两个字符串 `word1` 和 `word2` 被认为**几乎等价**（almost equivalent），当且仅当它们在字母 `'a'` 到 `'z'` 的出现频率（frequency）之差的绝对值均不超过 `3`。  
给定两个长度均为 `n` 的字符串 `word1` 和 `word2`，如果它们几乎等价返回 `true`，否则返回 `false`。  

字符 `x` 的频率是它在字符串中出现的次数。

## 示例

### 示例 1
**输入**  
`word1 = "aaaa", word2 = "bccb"`  

**输出**  
`false`  

**解释**  
在 `"aaaa"` 中 `'a'` 出现了 `4` 次，而在 `"bccb"` 中 `'a'` 出现了 `0` 次。差值为 `4`，大于允许的 `3`，因此两字符串不几乎等价。

### 示例 2
**输入**  
`word1 = "abcdeef", word2 = "abaaacc"`  

**输出**  
`true`  

**解释**  
每个字母的频率差均不超过 `3`：  
- `'a'` 在 `word1` 中出现 `1` 次，在 `word2` 中出现 `4` 次，差值 `3`。  
- `'b'` 在两字符串中各出现 `1` 次，差值 `0`。  
- `'c'` 在 `word1` 中出现 `1` 次，在 `word2` 中出现 `2` 次，差值 `1`。  
- `'d'` 在 `word1` 中出现 `1` 次，在 `word2` 中出现 `0` 次，差值 `1`。  
- `'e'` 在 `word1` 中出现 `2` 次，在 `word2` 中出现 `0` 次，差值 `2`。  
- `'f'` 在 `word1` 中出现 `1` 次，在 `word2` 中出现 `0` 次，差值 `1`。  

所有差值均 ≤ `3`，所以返回 `true`。

### 示例 3
**输入**  
`word1 = "cccddabba", word2 = "babababab"`  

**输出**  
`true`  

**解释**  
每个字母的频率差均不超过 `3`：  
- `'a'` 在 `word1` 中出现 `2` 次，在 `word2` 中出现 `4` 次，差值 `2`。  
- `'b'` 在 `word1` 中出现 `2` 次，在 `word2` 中出现 `5` 次，差值 `3`。  
- `'c'` 在 `word1` 中出现 `3` 次，在 `word2` 中出现 `0` 次，差值 `3`。  
- `'d'` 在 `word1` 中出现 `2` 次，在 `word2` 中出现 `0` 次，差值 `2`。  

所有差值均 ≤ `3`，因此返回 `true`。

## 约束条件

- `n == word1.length == word2.length`
- `1 <= n <= 100`
- `word1` 和 `word2` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把两个字符串的每个字符出现的次数都统计出来，然后把对应字母的次数相减，看看差值是否都 ≤ 3。  

- **数据结构**：我们可以用「哈希表」来记每个字母出现了多少次。哈希表就像一本**词典**，键（key）是字母，值（value）是它在字符串里出现的次数。因为字母只有 26 个，用 Python 的 `dict` 完全够用。  
- **为什么正确**：题目要求比较 **每一个** 从 `'a'` 到 `'z'` 的字母频率差。只要我们把两边的频率都算出来，逐个比较差值，就能准确判断。  
- **时间/空间复杂度**：  
  - 统计一次 `word1` 需要遍历 `n` 次，统计 `word2` 也要遍历 `n` 次，总共 `2 × n` 次，写成 **O(n)**。  
  - 再遍历 26 个字母做比较，常数级别，仍然是 **O(n)**。  
  - 使用两个哈希表，各存 26 条记录，空间是 **O(1)**（因为 26 是常数，不随输入规模增长）。  

> 大白话解释：`O(n)` 就是「随字符串长度线性增长」，比如长度是 10，做 10 次事；长度是 100，做 100 次事。`O(1)` 则是「不管多大，都只占固定的几块空间」。

#### 代码（Python）

```python
def checkAlmostEquivalent_bruteforce(word1: str, word2: str) -> bool:
    # 1️⃣ 统计 word1 每个字母出现的次数
    cnt1 = {}                     # 哈希表：key 是字母，value 是出现次数
    for ch in word1:
        cnt1[ch] = cnt1.get(ch, 0) + 1   # 没出现过就当作 0，再加 1

    # 2️⃣ 统计 word2 每个字母出现的次数
    cnt2 = {}
    for ch in word2:
        cnt2[ch] = cnt2.get(ch, 0) + 1

    # 3️⃣ 对 26 个字母逐个比较差值
    for i in range(26):
        ch = chr(ord('a') + i)    # 把数字 i 转成对应的字符，例如 i=0 → 'a'
        diff = abs(cnt1.get(ch, 0) - cnt2.get(ch, 0))
        if diff > 3:              # 只要有一个字母差值大于 3，就不满足
            return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只要遍历两遍字符串（每遍 `n` 次），再遍历 26 次常数操作。  
- **空间复杂度**：`O(1)` —— 哈希表最多存 26 条记录，空间不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

暴力解已经是线性的时间、常数的空间，已经非常高效。  
不过我们可以把「两个哈希表」合并成 **一个长度为 26 的整数数组**，一次遍历同时完成「+1」和「-1」的计数，这样代码更简洁、常数更小。  

**瓶颈在哪？**  
- 两个哈希表的创建和查询都有一定的额外开销（哈希冲突、动态扩容等），虽然在本题不影响复杂度，却可以进一步省去。  

**优化步骤**  
1. 创建长度为 26 的列表 `diff = [0] * 26`，下标 0 对应 `'a'`，下标 1 对应 `'b'`，依此类推。  
2. 同时遍历 `word1` 与 `word2`（因为长度相同），对 `word1` 中的字符对应下标 `+1`，对 `word2` 中的字符对应下标 `-1`。遍历结束后，`diff[i]` 正好是两个字符串该字母出现次数的差值（可能是正也可能是负）。  
3. 再遍历一次 `diff`，只要出现绝对值大于 3 的，就返回 `False`；全部满足则返回 `True`。  

**核心概念：数组计数**  
- 把「哈希表」换成「固定大小的数组」是一种常见的「空间换时间」技巧。因为字母集合是已知且很小（26），我们可以直接用数组的下标来表示每个字母。  
- 类比：如果你有 26 把钥匙要放进抽屉，用「抽屉编号」代替「钥匙的名字」更快。

#### 代码（Python）

```python
def checkAlmostEquivalent(word1: str, word2: str) -> bool:
    # diff[i] 保存字母 chr(ord('a') + i) 在 word1 与 word2 中出现次数的差值
    diff = [0] * 26                     # 初始化为全 0

    # 同时遍历两个等长的字符串
    for ch1, ch2 in zip(word1, word2):
        diff[ord(ch1) - ord('a')] += 1   # word1 出现一次 → +1
        diff[ord(ch2) - ord('a')] -= 1   # word2 出现一次 → -1

    # 检查每个字母的差值绝对值是否 ≤ 3
    for d in diff:
        if abs(d) > 3:                   # 只要有一个超过 3，直接返回 False
            return False
    return True
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次字符串（`zip` 同时取两字符），再遍历 26 次常数操作。相比暴力解少了一次哈希表的遍历，常数更小。  
- **空间复杂度**：`O(1)` —— 只用了长度为 26 的固定数组。

---

## 心得  

- **核心技巧**：使用「固定大小的计数数组」一次遍历完成两边频率差的统计。  
- **适用的题型**：  
  1. 判断两个字符串是否是字母异位词（Anagram）。  
  2. 判断字符串中是否存在出现次数超过 K 次的字符。  
  3. 统计字符串中出现次数最多的字符（同样用计数数组）。  
- **解题钥匙**：**把「计数」和「比较」合并到一次遍历**，并用数组代替哈希表。

---

## 反思  

- **第一反应**：先把两个字符串的每个字母频率算出来，然后逐个比较。  
- **最容易踩的坑**：  
  - 忘记处理某个字母在其中一个字符串里根本不存在的情况（需要 `get(..., 0)` 或数组默认 0）。  
  - 直接比较两次遍历的结果而没有取绝对值，导致负数被误判。  
- **下次遇到同类题**：第一步先思考「字符集合是否固定且小」——如果是，就直接用长度为集合大小的数组计数，一遍遍历完成所有统计。