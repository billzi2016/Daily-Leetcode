# #1941. 检查所有字符出现次数是否相等 / Check if All Characters Have Equal Number of Occurrences

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/check-if-all-characters-have-equal-number-of-occurrences/)

---

## 题目（英文原版）

**Description**

Given a string s, return true if s is a good string, or false otherwise.
A string s is good if all the characters that appear in s have the same number of occurrences (i.e., the same frequency).

**Examples**

**Example 1:**

```
Input: s = "abacbc"
Output: true
Explanation: The characters that appear in s are 'a', 'b', and 'c'. All characters occur 2 times in s.
```

**Example 2:**

```
Input: s = "aaabb"
Output: false
Explanation: The characters that appear in s are 'a' and 'b'.
'a' occurs 3 times while 'b' occurs 2 times, which is not the same number of times.
```

**Constraints**

- 1 <= s.length <= 1000
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，如果 `s` 是 **好字符串**（good string），则返回 `true`；否则返回 `false`。  
**好字符串** 的定义是：在 `s` 中出现的所有字符的出现次数（即 **频率**（frequency））都相同。

## 示例

### 示例 1
**输入**  
```text
s = "abacbc"
```
**输出**  
```text
true
```
**解释**  
`s` 中出现的字符为 `'a'`、`'b'` 和 `'c'`，每个字符均出现了 2 次。

### 示例 2
**输入**  
```text
s = "aaabb"
```
**输出**  
```text
false
```
**解释**  
`s` 中出现的字符为 `'a'` 和 `'b'`。`'a'` 出现了 3 次，而 `'b'` 只出现了 2 次，出现次数不相等。

## 约束条件
- `1 <= s.length <= 1000`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个字符，都去整条字符串里数一遍它出现了多少次**。  
这跟我们在纸上手动统计字母频率的过程一样：

1. 从左到右遍历字符串，取出第一个字符 `c`。  
2. 再遍历一遍整个字符串，统计 `c` 出现了几次，记为 `cnt`。  
3. 把 `cnt` 保存下来（比如放进一个列表），然后继续处理下一个字符。  
4. 当所有字符都统计完后，只要列表里所有的数字都相等，答案就是 `True`，否则 `False`。

> **类比**：把哈希表想成一本“字典”。在暴力解里我们没有直接去查字典，而是每次都手动翻遍整本书去找对应的词条，这显然很慢。

**为什么这个方法一定能得到正确答案**  
因为我们对每个出现的字符都完整统计了它的出现次数，得到的频率肯定是准确的。只要比较这些频率是否全等，就能判断题目要求的“好字符串”。

#### 代码（Python）

```python
def areOccurrencesEqual_bruteforce(s: str) -> bool:
    # 保存每个字符的出现次数
    freq_list = []

    # 对字符串里的每个字符都单独统计一次
    for i in range(len(s)):
        ch = s[i]

        # 已经统计过的字符不需要再算，直接跳过
        if ch in s[:i]:          # 这里相当于“这本字典里已经有这页了”
            continue

        cnt = 0                  # 计数器，统计 ch 出现了几次
        for j in range(len(s)):
            if s[j] == ch:       # 再遍历一遍整条字符串
                cnt += 1

        freq_list.append(cnt)    # 把统计结果放进列表

    # 检查列表里所有数字是否相同
    # 把列表转换成集合，集合里只有唯一的元素；若集合大小为 1，说明全部相等
    return len(set(freq_list)) == 1
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层循环遍历 `n` 次，内层再遍历 `n` 次来计数，最坏情况下相当于 `n × n` 次操作。  
  对于长度 1000 的字符串来说，最多要做约 `10⁶` 次比较，虽然还能跑通，但已经不是最省时的办法了。

- **空间复杂度**：`O(n)`  
  解释：我们用了 `freq_list` 来保存每个字符的计数，最坏情况下每个字符都不同，需要存 `n` 个数字。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于每次都要遍历整条字符串去计数**。  
我们可以把“遍历一次统计所有字符的次数”这件事一次性完成，这正是 **哈希表（字典）** 的强项：

1. **一次遍历**：从左到右扫描字符串，遇到字符 `c` 就把 `c` 作为键（key）放进字典，值（value）加 1。  
   - 这相当于把“查字典”变成了“直接在字典里记页码”。  
2. 遍历结束后，字典的所有值就是每个字符的出现次数。  
3. 把这些值放进集合（`set`），如果集合的大小是 1，说明所有频率相同，返回 `True`；否则返回 `False`。

> **核心数据结构**：`dict`（哈希表）  
> - **查找/插入** 都是 `O(1)`（常数时间），所以只需要一次线性遍历就能得到所有频率。  
> - **集合 `set`** 用来快速判断所有频率是否相同：把所有频率去重后，只要剩下一个元素就说明全部相等。

#### 代码（Python）

```python
def areOccurrencesEqual(s: str) -> bool:
    # 第一步：统计每个字符出现的次数，使用字典（哈希表）
    freq = {}                     # 空字典，键是字符，值是出现次数
    for ch in s:                  # 只遍历一次字符串
        if ch in freq:            # 已经出现过，计数加一
            freq[ch] += 1
        else:                     # 第一次出现，计数初始化为 1
            freq[ch] = 1

    # 第二步：检查所有计数是否相同
    # 把字典的所有值取出来放进集合，集合会自动去重
    unique_counts = set(freq.values())

    # 如果集合里只有一个元素，说明所有字符出现次数相同
    return len(unique_counts) == 1
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们只遍历了一遍字符串（`n` 次），每次对字典的增删改查都是常数时间，所以整体是线性时间。相比暴力的 `O(n²)`，快了很多。

- **空间复杂度**：`O(k)`，`k` 为不同字符的种类数（最多 26，因为只有小写英文字母）。  
  解释：字典里只存每种字符出现的次数，最多 26 条记录，算是常数空间。

---

## 心得

- **核心技巧**：使用哈希表（字典）一次遍历统计字符频率，再利用集合去重判断是否全部相等。  
- **适用的题型**  
  1. 判断两个字符串是否是字母异位词（是否拥有相同字符计数）。  
  2. 找出出现次数最多的字符或前 K 高频字符。  
  3. 判断数组中是否所有元素出现次数相同（同理可用哈希表统计）。
- **一句话总结**：把“每个字符都遍历计数”变成“一遍遍历直接记在字典里”，再用集合快速检测统一性，就是本题的解题钥匙。

---

## 反思

- **拿到题目第一反应**：先想“把每个字母出现的次数都写下来”，于是想到最直接的双层循环统计。  
- **最容易踩的坑**  
  - 忘记只统计出现过的字符，导致对不存在的字符也计数（会把 `0` 也算进去）。  
  - 对空字符串或只有一种字符的情况没有特别处理，其实这两种都应该返回 `True`。  
- **下次遇到同类题的第一步**：立刻想到 “**用哈希表一次遍历收集频率**”，因为这几乎是所有涉及“出现次数比较”问题的通用模板。