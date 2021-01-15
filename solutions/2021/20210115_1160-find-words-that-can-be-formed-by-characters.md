# #1160. 可以由字符组成的单词 / Find Words That Can Be Formed by Characters

> 难度：简单 · 标签：Array、Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/find-words-that-can-be-formed-by-characters/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words and a string chars.
A string is good if it can be formed by characters from chars (each character can only be used once for each word in words).
Return the sum of lengths of all good strings in words.

**Examples**

**Example 1:**

```
Input: words = ["cat","bt","hat","tree"], chars = "atach"
Output: 6
Explanation: The strings that can be formed are "cat" and "hat" so the answer is 3 + 3 = 6.
```

**Example 2:**

```
Input: words = ["hello","world","leetcode"], chars = "welldonehoneyr"
Output: 10
Explanation: The strings that can be formed are "hello" and "world" so the answer is 5 + 5 = 10.
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length, chars.length <= 100
- words[i] and chars consist of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组（array of strings）`words` 和一个字符串（string）`chars`。  
如果一个字符串能够完全由 `chars` 中的字符组成（每个字符在构成该字符串时只能使用一次），则称该字符串为 **好字符串**（good）。  

返回 `words` 中所有好字符串的长度之和。  

**示例 1**  

```
Input: words = ["cat","bt","hat","tree"], chars = "atach"
Output: 6
Explanation: 可以构成的字符串是 "cat" 和 "hat"，因此答案为 3 + 3 = 6。
```

**示例 2**  

```
Input: words = ["hello","world","leetcode"], chars = "welldonehoneyr"
Output: 10
Explanation: 可以构成的字符串是 "hello" 和 "world"，因此答案为 5 + 5 = 10。
```

**约束条件**  

- `1 <= words.length <= 1000`  
- `1 <= words[i].length, chars.length <= 100`  
- `words[i]` 和 `chars` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个单词单独拿出来，和 `chars` 一对一比较**。  
可以把 `chars` 想象成一本字典，里面记录了每个字母出现了多少次（key 是字母，value 是页码——也就是“还有几张”）。  
对每个单词：

1. 把 `chars` 的字典 **复制** 一份（相当于再拿一本同样的字典），这样每个单词使用的字母互不影响。  
2. 按字母顺序遍历单词的每个字符，去查字典里有没有对应的字母且数量>0。  
   - 有的话，把数量减 1（相当于把这张页码“借走”）。  
   - 没有的话，说明这个单词 **不能** 用 `chars` 里的字母拼成，直接跳到下一个单词。  
3. 如果所有字符都顺利借到，则把该单词的长度累加到答案中。

> 为什么这样一定对？因为我们严格按照 `chars` 中每个字母的出现次数来“借”，只要出现次数足够，单词就一定能拼出来；否则就不行。

**复杂度分析（大白话）**  
- 对每个单词，我们都要遍历它的所有字符（最坏情况是 100 个字符），并且每次都在字典里做一次“查找/更新”。查找字典的时间可以看作是 **O(1)**（常数时间），所以单词的检查时间就是 **O(单词长度)**。  
- 设 `n = words.length`，`L` 为所有单词长度的上界（≤100），总时间就是 **O(n·L)**。  
- 但是我们每检查一个单词都要 **复制一次 `chars` 的字典**，复制的代价是 26（英文字母个数）次操作，算上去仍是常数级别。  
- 空间方面，我们需要额外的一个字典来存放 `chars` 的计数（大小固定为 26），以及每次复制时的临时字典，也都是常数大小，所以 **O(1)**（不随输入规模增长）。

#### 代码（Python）

```python
from collections import Counter

def count_characters_bruteforce(words, chars):
    # 把 chars 里每个字母出现的次数统计出来，像一本“字典”
    chars_counter = Counter(chars)          # {'a':2, 't':1, ...}
    total_len = 0

    for w in words:
        # 为当前单词准备一份独立的“字典”，防止相互影响
        remain = chars_counter.copy()       # 复制是 O(1)（只复制 26 项）
        can_form = True

        for ch in w:                         # 逐字符检查
            if remain[ch] > 0:               # 还有剩余的该字符吗？
                remain[ch] -= 1              # “借走”一张
            else:                            # 没有了，直接判定失败
                can_form = False
                break

        if can_form:                         # 单词可以拼出
            total_len += len(w)

    return total_len
```

#### 复杂度

- **时间复杂度**：`O(n·L)`  
  - `n` 为单词数量，`L` 为单词的最大长度。  
  - 大白话：如果有 1000 个单词，每个单词最多 100 个字母，最坏要检查 100 000 次字符。
- **空间复杂度**：`O(1)`  
  - 只用了固定大小的计数表（26 个字母），不随输入规模增长。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈** 在于每检查一个单词都要 **复制一份 `chars` 的计数表**。虽然复制本身是常数时间，但我们完全可以 **把这份计数表保存下来，只在需要时读取**，不必每次都复制。

关键观察：

- 判断一个单词能否由 `chars` 拼出，只需要比较 **每个字母的出现次数**，不需要真正“借走”。  
- 因此，只要 **`chars` 中每个字母的数量 ≥ 单词中该字母的数量**，单词就是 “good”。  

优化步骤：

1. **预处理**：一次性统计 `chars` 中每个字母的出现次数，放进长度为 26 的数组 `cnt_chars`（下标 0 对应 `'a'`，1 对应 `'b'` ……）。这一步只做一次，时间 `O(|chars|)`，空间 `O(26)`。  
2. 对每个单词，**再统计一次它自己的字母频率**，同样用长度为 26 的数组 `cnt_word`。  
3. 用一个小循环（遍历 26 次）比较两个数组对应位置的值：只要有一次 `cnt_word[i] > cnt_chars[i]`，说明该字母不够，用 `break` 提前结束比较。  
4. 若所有 26 次比较都通过，则把单词长度加入答案。

这样我们省掉了每次复制计数表的操作，只保留必要的比较，时间仍是 `O(n·L)`（因为每个单词仍要遍历一次字符），但常数更小，代码更简洁；空间仍是 `O(1)`（固定的 26 长度数组）。

> **为什么数组比 `Counter` 更快**  
> `Counter` 是基于哈希表的实现，需要做哈希运算并且存储键值对；而数组直接用下标访问，时间更确定、开销更低。对只包含小写字母的题目，这种“字母计数数组”是最自然的做法。

#### 代码（Python）

```python
def count_characters_optimal(words, chars):
    # 1️⃣ 统计 chars 中每个字母出现的次数，放进长度为 26 的数组
    cnt_chars = [0] * 26                     # 全部初始化为 0
    for ch in chars:
        cnt_chars[ord(ch) - ord('a')] += 1   # ord('a') = 97，计算下标

    total_len = 0

    # 2️⃣ 逐个检查单词
    for w in words:
        cnt_word = [0] * 26                  # 本单词的计数表
        for ch in w:
            idx = ord(ch) - ord('a')
            cnt_word[idx] += 1

        # 3️⃣ 比较两个计数表
        can_form = True
        for i in range(26):
            if cnt_word[i] > cnt_chars[i]:   # 只要有一种字母不够，就不行
                can_form = False
                break

        # 4️⃣ 若可以拼出，累加长度
        if can_form:
            total_len += len(w)

    return total_len
```

#### 复杂度

- **时间复杂度**：`O(n·L)`  
  - 与暴力解的数量级相同，但没有复制计数表的额外开销，实际运行更快。  
  - 大白话：仍然是“每个单词遍历一次字符”，再加上 26 次常数比较，几乎可以忽略不计。
- **空间复杂度**：`O(1)`  
  - 只用了两个固定长度为 26 的数组，空间不随 `words` 或 `chars` 长度增长。

---

## 心得

- **核心技巧**：**字符频率比较**（frequency counting）——把字符串转化为“每个字母出现了几次”的数组/哈希表，然后比较两者的对应值。  
- **适用的题型**（类似思路）  
  1. *Find and Replace Pattern*（比较模式的字符出现次数）  
  2. *Ransom Note*（判断能否用一段文字拼出另一段文字）  
  3. *Check If All A’s Appear Before All B’s*（也可以用计数或前缀和）  
- **一句话总结解题钥匙**：**把文字变成数字（频率表），用数字直接比较**。

---

## 反思

- **第一反应**：看到“每个字符只能用一次”，立刻想到“计数”。于是把 `chars` 当作字典，检查每个单词是否能在字典里“借到”足够的字符。  
- **最容易踩的坑**  
  - **忘记对每个单词独立计数**：`chars` 的计数不能在检查完第一个单词后直接复用，需要重新复制或重新比较。  
  - **忽视空字符或单词长度为 0 的情况**（本题约束里不出现，但在实际面试中要考虑）。  
  - **使用 `list.count()` 逐字符统计**会导致 **O(L²)**，因为 `count` 本身是遍历一次字符串。  
- **下次遇到同类题**，第一步应该想：**“我能把每个字符串抽象成一个‘字母频率表’吗？”** 如果答案是肯定的，那么后面的比较、验证往往可以在 **O(字母表大小)**（本题是 26）时间内完成。