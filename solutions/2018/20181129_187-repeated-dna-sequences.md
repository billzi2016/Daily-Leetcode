# #187. 重复的DNA序列 / Repeated DNA Sequences

> 难度：中等 · 标签：Hash Table、String、Bit Manipulation、Sliding Window、Rolling Hash、Hash Function · [LeetCode 链接](https://leetcode.com/problems/repeated-dna-sequences/)

---

## 题目（英文原版）

**Description**

The DNA sequence is composed of a series of nucleotides abbreviated as 'A', 'C', 'G', and 'T'.
When studying DNA, it is useful to identify repeated sequences within the DNA.
Given a string s that represents a DNA sequence, return all the 10-letter-long sequences (substrings) that occur more than once in a DNA molecule. You may return the answer in any order.

**Examples**

**Example 1:**

```
Input: s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
Output: ["AAAAACCCCC","CCCCCAAAAA"]
```

**Example 2:**

```
Input: s = "AAAAAAAAAAAAA"
Output: ["AAAAAAAAAA"]
```

**Constraints**

- 1 <= s.length <= 105
- s[i] is either 'A', 'C', 'G', or 'T'.

---

## 题目（中文翻译）

DNA 序列由四种核苷酸组成，分别用字符 `'A'`、`'C'`、`'G'`、`'T'` 表示。  
在研究 DNA 时，识别 DNA 中出现多次的序列是很有用的。  
给定一个字符串 `s` 表示 DNA 序列，返回所有出现次数超过一次的、长度为 **10** 的序列（子串）。返回结果的顺序可以任意。

### 示例

**示例 1**  
Input: `s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"`  
Output: `["AAAAACCCCC","CCCCC AAAAA"]`

**示例 2**  
Input: `s = "AAAAAAAAAAAAA"`  
Output: `["AAAAAAAAAA"]`

### 约束条件

- `1 <= s.length <= 10^5`
- `s[i]` 只能是 `'A'`、`'C'`、`'G'` 或 `'T'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把 DNA 串 `s` 中所有长度为 10 的子串都枚举出来，放进一个 **哈希表**（可以理解为一本词典，单词是子串，页码是出现次数）里统计出现次数，最后把出现次数大于 1 的子串挑出来返回。

- **数据结构**：  
  - `dict`（Python 的哈希表）——就像查字典一样，给定一个子串（key），我们能在 **常数时间** (`O(1)`) 内得到它已经出现了几次（value）。
- **为什么正确**：  
  - 题目要求找出所有出现 **超过一次** 的 10 长度子串。枚举所有可能的子串并统计次数，必然能够完整覆盖所有答案。  
- **时间/空间分析（大白话）**：  
  - 设字符串长度为 `n`，我们要检查的子串数量是 `n-9`（因为每个子串占 10 个字符）。  
  - 对每个子串我们都要做一次哈希插入/查询，假设哈希表的操作是 **常数时间**，整体时间就是 `O(n)` 次常数操作，也可以说 **线性时间**。  
  - 但每次我们都要 **切片**（`s[i:i+10]`），这在 Python 中会产生一个新的子串对象，长度固定为 10，复制的代价是 `O(10)`，常数可以忽略不计。  
  - 空间方面，需要把所有不同的 10 长度子串存进哈希表，最坏情况下每个子串都不重复，哈希表里会有 `n-9` 条记录，空间是 `O(n)`。

#### 代码（Python）

```python
def findRepeatedDnaSequences(s: str):
    """
    暴力枚举 + 哈希表统计出现次数
    """
    if len(s) < 10:               # 长度不足 10，直接返回空列表
        return []

    counter = {}                   # 用 dict 记录每个子串出现的次数
    for i in range(len(s) - 9):    # 遍历所有起始位置
        sub = s[i:i + 10]          # 取长度为 10 的子串
        # dict 的 get 方法如果 key 不存在返回 0
        counter[sub] = counter.get(sub, 0) + 1

    # 把出现次数 > 1 的子串挑出来
    result = [seq for seq, cnt in counter.items() if cnt > 1]
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`（线性时间）  
  - 这里的 `n` 是 DNA 序列的长度。我们只遍历一次字符串，虽然每次切片要复制 10 个字符，但这属于常数级别的开销。
- **空间复杂度**：`O(n)`（线性空间）  
  - 最坏情况下所有子串都不重复，需要存 `n-9` 条记录在哈希表中。

---

### 2. 最优解

#### 思路  
虽然上面的暴力解已经是 `O(n)` 时间，但它的空间用了 `O(n)`，在 `n` 达到 10⁵ 时仍然可以接受。不过我们可以进一步 **压缩空间**，利用 DNA 只包含 4 种字符的特性，把每个字符用 **2 位二进制** 表示，从而把一个长度为 10 的子串压缩成一个 **20 位整数**（即一个普通的 Python `int`），再用整数做哈希键。这样：

1. **把字符映射成数字**  
   - `'A' → 00`, `'C' → 01`, `'G' → 10`, `'T' → 11`。  
   - 这相当于把 DNA 当成 4 进制数，只是用二进制实现。
2. **滑动窗口 + 位运算**（滚动哈希）  
   - 维护一个 20 位的整数 `hash`，它始终表示当前窗口（长度 10）的子串。  
   - 当窗口向右移动一格时：  
     - 左侧最旧的字符要 **抛掉**（左移 2 位后再取低 20 位相当于把最左的 2 位清零）。  
     - 右侧新进的字符要 **加入**（把对应的 2 位放到最右边）。  
   - 只用几次位运算（`<<`, `&`, `|`）即可完成更新，时间仍是 `O(1)`。
3. **再次使用哈希表统计**  
   - 这次哈希表的键是整数，空间只和不同子串的数量成正比，仍是 `O(n)`，但每个键只占用 8~10 字节（相较于 10‑字符的字符串要小很多），实际内存占用更低。

> **关键点**：滑动窗口让我们不必每次都重新创建子串，而是“滚动”地更新一个整数，这就是 **滚动哈希**（Rolling Hash）的核心思想。

#### 代码（Python）

```python
def findRepeatedDnaSequences(s: str):
    """
    使用位运算 + 滑动窗口（滚动哈希）压缩空间
    """
    if len(s) < 10:
        return []

    # 1. 字符 → 2 位整数的映射表
    char_to_bits = {
        'A': 0b00,
        'C': 0b01,
        'G': 0b10,
        'T': 0b11,
    }

    mask = (1 << 20) - 1               # 只保留低 20 位，二进制 111...111（20 个 1）
    cur_hash = 0                       # 当前窗口对应的整数哈希值
    seen = {}                          # 哈希值 → 出现次数

    # 2. 先把前 10 个字符转成整数
    for i in range(10):
        cur_hash = (cur_hash << 2) | char_to_bits[s[i]]
    seen[cur_hash] = 1                 # 第一个窗口出现一次

    # 3. 滑动窗口：从第 11 个字符开始，每次左移 2 位后加入新字符
    for i in range(10, len(s)):
        # 左移 2 位相当于把窗口左侧的字符抛掉（随后用 mask 截断）
        cur_hash = ((cur_hash << 2) & mask) | char_to_bits[s[i]]
        seen[cur_hash] = seen.get(cur_hash, 0) + 1

    # 4. 把出现次数 > 1 的哈希值再转回字符串
    result = []
    # 为了把整数恢复成 DNA 子串，需要把 20 位每 2 位映射回字符
    bits_to_char = {v: k for k, v in char_to_bits.items()}

    for h, cnt in seen.items():
        if cnt > 1:
            # 取低 20 位，依次取出每两位对应的字符（从右往左），再反转顺序得到原串
            seq_chars = []
            temp = h
            for _ in range(10):
                two_bits = temp & 0b11          # 取最右边的 2 位
                seq_chars.append(bits_to_char[two_bits])
                temp >>= 2                      # 右移 2 位，准备取下一对
            result.append(''.join(reversed(seq_chars)))  # 反转得到正确顺序

    return result
```

> **代码要点注释**  
- `mask = (1 << 20) - 1`：保证哈希值始终保持 20 位，防止左移后产生多余高位。  
- `cur_hash = ((cur_hash << 2) & mask) | char_to_bits[s[i]]`：左移两位相当于窗口向右滑动，`& mask` 把最左的 2 位丢掉，`|` 把新字符的 2 位放进去。  
- 最后把整数恢复为字符串时，需要 **逆序** 读取，因为我们是从左到右不断把新字符放在最低位。

#### 复杂度

- **时间复杂度**：`O(n)`（线性时间）  
  - 每个字符只被处理一次，位运算和字典操作均为常数时间。相比暴力解，额外的整数恢复过程仍是常数倍的线性。
- **空间复杂度**：`O(n)`（线性空间）  
  - 只存储不同子串对应的整数哈希值，实际占用的内存比存完整字符串要小得多（约 4 倍压缩），在极端数据下仍是线性。

---

## 心得

- **核心技巧**：利用字符种类有限（只有 4 种）把子串压缩成固定长度的整数，再用 **滑动窗口 + 位运算（滚动哈希）** 高效更新哈希值。  
- **适用的题型**：  
  1. “长度固定的子串重复出现”——如 *Repeated DNA Sequences*、*Find All Anagrams in a String*（可改用计数数组）。  
  2. “大字符串中查找子串是否出现过”——如 *Substring of Size K With No Repeating Characters*。  
  3. “使用哈希或位运算做窗口判等”——如 *Maximum Average Subarray I*（滑动窗口求和）等。  
- **一句话总结**：**把有限字符映射成二进制，用滚动哈希在 O(1) 内更新窗口**，是处理固定长度子串重复问题的“钥匙”。

---

## 反思

- **第一反应**：直接遍历所有长度为 10 的子串，用字典计数——最直观、最不容易出错的办法。  
- **最容易踩的坑**：  
  - 忘记在滑动窗口时把左侧字符“抛掉”，导致哈希值不断增长，最终溢出（虽然 Python 整数不溢出，但会失去“固定窗口”意义）。  
  - 在恢复整数为字符串时顺序写反，得到的子串是倒序的。  
  - 边界条件：字符串长度小于 10 时直接返回空列表。  
- **下次类似题**：  
  1. **先判断窗口大小**（这里是 10），  
  2. **检查字符集合是否有限**（若是四种，可考虑二进制压缩），  
  3. **考虑滑动窗口+哈希**（或计数数组）是否能把每一步的更新压到 O(1)。  

这样一步步抽象出 “窗口 → 哈希 → 统计” 的通用框架，就能快速找到最优解。