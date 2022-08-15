# #1897. 重新分配字符使所有字符串相等 / Redistribute Characters to Make All Strings Equal

> 难度：简单 · 标签：Hash Table、String、Counting · [LeetCode 链接](https://leetcode.com/problems/redistribute-characters-to-make-all-strings-equal/)

---

## 题目（英文原版）

**Description**

You are given an array of strings words (0-indexed).
In one operation, pick two distinct indices i and j, where words[i] is a non-empty string, and move any character from words[i] to any position in words[j].
Return true if you can make every string in words equal using any number of operations, and false otherwise.

**Examples**

**Example 1:**

```
Input: words = ["abc","aabc","bc"]
Output: true
Explanation: Move the first 'a' in words[1] to the front of words[2],
to make words[1] = "abc" and words[2] = "abc".
All the strings are now equal to "abc", so return true.
```

**Example 2:**

```
Input: words = ["ab","a"]
Output: false
Explanation: It is impossible to make all the strings equal using the operation.
```

**Constraints**

- 1 <= words.length <= 100
- 1 <= words[i].length <= 100
- words[i] consists of lowercase English letters.

---

## 题目（中文翻译）

你得到一个字符串数组 `words`（下标从 0 开始）。

在一次操作中，选择两个不同的下标 `i` 和 `j`，其中 `words[i]` 为非空字符串（non‑empty string），并将 `words[i]` 中的任意字符移动到 `words[j]` 的任意位置。

如果可以通过任意次数的上述操作使 `words` 中的每个字符串都相等，则返回 `true`，否则返回 `false`。

### 示例

**示例 1**

```
Input: words = ["abc","aabc","bc"]
Output: true
Explanation: 将 `words[1]` 中的第一个 `'a'` 移动到 `words[2]` 的开头，使得
`words[1]` 变为 `"abc"`，`words[2]` 也变为 `"abc"`。
此时所有字符串均等于 `"abc"`，因此返回 `true`。
```

**示例 2**

```
Input: words = ["ab","a"]
Output: false
Explanation: 无法通过上述操作使所有字符串相等。
```

### 约束条件

- `1 <= words.length <= 100`
- `1 <= words[i].length <= 100`
- `words[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把所有字符都搬到一起，看看能不能平均分配**。  
- 把每个字符串里的每个字符都拿出来，放进一个“大篮子”。这一步可以想象成把所有单词的字母写在一张长纸上，顺序不重要，只在乎每个字母出现了多少次。
- 然后检查每种字母的总数能否被字符串的个数 `n = len(words)` 整除。因为最终每个字符串必须完全相同，假设最终的目标字符串是 `t`，那么 `t` 中每个字母的出现次数一定是 **总次数 ÷ n**。如果某个字母的总次数除不尽，就不可能把它平均分配到每个单词里，自然返回 `false`。
- 如果所有字母都可以整除，则一定可以把字符重新安排成相同的字符串（把每种字母均分到每个单词中即可），返回 `true`。

> **为什么这个方法一定对？**  
> 题目给的操作可以把任意字符从一个非空字符串移动到另一个字符串的任意位置，而**字符之间没有顺序约束**，只要每个字符的总量可以被 `n` 整除，就一定能把它们均匀地分配到每个单词里，使所有单词相同。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def makeEqual(words: List[str]) -> bool:
    """
    暴力思路：统计所有字符出现的总次数，检查能否被单词数整除。
    """
    n = len(words)                     # 单词总数
    total_counter = Counter()          # 用来统计所有字符的出现次数

    # 把每个单词的字符都加到 total_counter 中
    for w in words:
        total_counter.update(w)        # Counter.update 会把字符串里每个字符计数

    # 检查每种字符的总次数是否能被 n 整除
    for ch, cnt in total_counter.items():
        if cnt % n != 0:                # 余数不为 0，说明不能均分
            return False

    # 所有字符都能均分，必然可以构造相同的字符串
    return True
```

#### 复杂度

- **时间复杂度**：`O(L)`，其中 `L` 是所有单词字符总长度（`L ≤ 100 * 100 = 10⁴`）。我们只遍历一次所有字符并做计数，`O(L)` 就是实际运行时间的含义——线性随字符数量增长。
- **空间复杂度**：`O(1)`（常数空间），因为字符集固定为小写英文字母，计数表最多只有 26 项，不会随 `L` 增长。

---

### 2. 最优解

#### 思路  
从暴力解可以看出，**真正的瓶颈不在于遍历，而在于我们是否真的需要保存每个字符的出现顺序**。字符的顺序在题目中是无关紧要的，只要统计频率即可。于是可以直接使用长度为 26 的数组（或 `Counter`）来记录每个字母的出现次数，进一步简化实现细节。

优化步骤：

1. **使用固定大小的计数数组**  
   - 用 `cnt[0]` 表示 `'a'` 的出现次数，`cnt[1]` 表示 `'b'`，以此类推。这样不需要哈希表的额外开销，访问是 O(1) 的数组下标操作。
2. **一次遍历完成计数**  
   - 同时累计字符总数，最后只需要遍历 26 次检查是否能被 `n` 整除。
3. **提前返回**  
   - 在统计的过程中，如果发现某个字符已经出现次数超过 `n * max_per_string`（理论上不可能）可以提前返回 `False`，不过在本题约束下不必如此。

核心概念 **计数（Counting）**：把“有多少个”这类信息用数组或哈希表保存，是解决字符/数字出现次数问题的常用技巧，就像在超市里用电子秤称每种商品的数量。

#### 代码（Python）

```python
from typing import List

def makeEqual(words: List[str]) -> bool:
    """
    最优解：使用长度为 26 的数组统计字符频率，时间 O(L)，空间 O(1)。
    """
    n = len(words)               # 单词数
    cnt = [0] * 26               # 计数数组，cnt[i] 对应字母 chr(ord('a') + i)

    # 统计所有字符出现次数
    for w in words:
        for ch in w:
            idx = ord(ch) - ord('a')   # 将字符映射到 0~25 的下标
            cnt[idx] += 1

    # 检查每种字符是否能被 n 整除
    for i, c in enumerate(cnt):
        if c % n != 0:                 # 余数不为 0，无法均分
            return False

    return True
```

#### 复杂度

- **时间复杂度**：`O(L)`，仍然是遍历所有字符一次。相比之前的 `Counter`，常数因子更小（数组下标访问比哈希更快），在大数据下会更快。
- **空间复杂度**：`O(1)`，只使用 26 个整数的固定数组，和字符集大小无关。

---

## 心得

- **核心技巧**：**字符计数 + 能否整除**。只要把所有字符的出现次数统计出来，检查是否可以被单词数平均分配，就能得到答案。
- **适用题型**  
  1. *“重新排列字符串”* 类题目，如 **LeetCode 1650. Lowest Common Ancestor of a Binary Tree**（其实是计数类的）  
  2. *“判断能否组成某个目标”*，例如 **LeetCode 383. Ransom Note**（检查字符是否足够）  
  3. *“字符分配”*，如 **LeetCode 2265. Count Nodes Equal to Average of Subtree**（统计平均值）  
- **一句话总结**：只要字符的总频率能被字符串个数整除，就一定能把它们重新分配成相同的字符串。

---

## 反思

- **第一反应**：看到“移动字符到任意位置”，第一时间想到“字符的顺序不重要”，于是把注意力放在**字符的数量**上，而不是尝试模拟搬运过程。
- **最容易踩的坑**  
  - 忽视字符种类：必须对 **每一种** 字母都检查能否整除，单独检查一种会导致错误。  
  - 边界条件：当只有一个单词时，答案一定是 `True`（因为不需要移动），代码自然会覆盖，但要确认不因除零错误而崩溃。  
  - 大小写或非字母字符：题目限定为小写字母，若忽略这一点可能导致数组下标越界。
- **下次遇到同类题**：第一步先**统计所有关键元素的总量**（字符、数字、颜色等），再**看能否均匀分配**（整除或满足某个比例），这一步往往能快速得到结论。