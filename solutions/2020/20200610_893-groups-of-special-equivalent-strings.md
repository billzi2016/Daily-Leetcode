# #893. 特殊等价字符串的分组 / Groups of Special-Equivalent Strings

> 难度：中等 · 标签：Array、Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/groups-of-special-equivalent-strings/)

---

## 题目（英文原版）

**Description**

You are given an array of strings of the same length words.
In one move, you can swap any two even indexed characters or any two odd indexed characters of a string words[i].
Two strings words[i] and words[j] are special-equivalent if after any number of moves, words[i] == words[j].
A group of special-equivalent strings from words is a non-empty subset of words such that:
Return the number of groups of special-equivalent strings from words.

**Examples**

**Example 1:**

```
Input: words = ["abcd","cdab","cbad","xyzz","zzxy","zzyx"]
Output: 3
Explanation: 
One group is ["abcd", "cdab", "cbad"], since they are all pairwise special equivalent, and none of the other strings is all pairwise special equivalent to these.
The other two groups are ["xyzz", "zzxy"] and ["zzyx"].
Note that in particular, "zzxy" is not special equivalent to "zzyx".
```

**Example 2:**

```
Input: words = ["abc","acb","bac","bca","cab","cba"]
Output: 3
```

**Constraints**

- 1 <= words.length <= 1000
- 1 <= words[i].length <= 20
- words[i] consist of lowercase English letters.
- All the strings are of the same length.

---

## 题目（中文翻译）

给定一个字符串数组 `words`，其中所有字符串长度相同。  

在一次操作中，你可以交换同一字符串 `words[i]` 中任意两个 **偶数下标字符**（even indexed characters）或任意两个 **奇数下标字符**（odd indexed characters）。  

如果经过任意次数的操作后，`words[i]` 能够变成 `words[j]`，则称这两个字符串 **特殊等价**（special‑equivalent）。  

`words` 的一个 **特殊等价字符串组**（group of special‑equivalent strings）是 `words` 的一个非空子集，使得子集内任意两字符串彼此特殊等价。  

求 `words` 中不同的特殊等价字符串组的数量并返回。

### 示例

#### 示例 1
```text
Input: words = ["abcd","cdab","cbad","xyzz","zzxy","zzyx"]
Output: 3
Explanation:
第一组是 ["abcd","cdab","cbad"]，因为它们两两之间都是特殊等价的，且没有其他字符串能够同时与这三者两两特殊等价。
其余两组分别是 ["xyzz","zzxy"] 和 ["zzyx"]。
需要注意的是，"zzxy" 与 "zzyx" 并非特殊等价。
```

#### 示例 2
```text
Input: words = ["abc","acb","bac","bca","cab","cba"]
Output: 3
```

### 约束条件
- `1 <= words.length <= 1000`
- `1 <= words[i].length <= 20`
- `words[i]` 只包含小写英文字母
- 所有字符串的长度相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**两两比较** `words[i]` 和 `words[j]` 能否通过合法的交换变成相同的字符串。  
因为题目允许：

* 任意两个 **偶数下标**（0、2、4…）的字符可以互相交换  
* 任意两个 **奇数下标**（1、3、5…）的字符可以互相交换  

这相当于把偶数位的字符视为一个“小盒子”，奇数位的字符视为另一个“小盒子”。只要两个字符串在这两个盒子里拥有 **完全相同的字符 multiset**（即相同的字符出现次数），它们就可以通过若干次交换变成相同的顺序。

暴力实现的步骤：

1. 对每一对 `(i, j)`（`i < j`）  
   - 统计 `words[i]` 偶数位字符的出现次数（可以用字典或数组），奇数位同理。  
   - 统计 `words[j]` 的偶数位、奇数位字符出现次数。  
   - 如果两者的偶数位统计相等且奇数位统计相等，则这两个字符串是 **special‑equivalent**。  
2. 用并查集（Union‑Find）把互相等价的下标合并，最后统计并查集的根节点数量即为答案。

> **类比**：把哈希表想象成一本字典，**key** 是字母，**value** 是这本字典里该字母出现了多少页（次数）。只要两本字典的页码完全相同，就说明这两本字典描述的是同一套内容。

**为什么正确**：  
如果两个字符串的偶数位字符集合相同，奇数位字符集合也相同，那么我们可以先把所有偶数位字符排成任意顺序（因为任意交换），再把奇数位字符排成任意顺序，最终就能得到完全相同的字符串。反之，如果某个字符在偶数位出现次数不同，就不可能仅通过偶数位内部的交换来补齐，等价关系必然不成立。

**时间/空间复杂度**  
- 外层有 `n`（`words` 长度）个字符串，内层两两比较，需要 `C(n,2) = n·(n-1)/2` 次比较 → **O(n²)**。  
- 对每一次比较，需要遍历字符串长度 `k`（`k ≤ 20`）统计字符出现次数 → **O(k)**。  
- 综合起来是 **O(n²·k)**，在最坏情况下 `n=1000, k=20` 仍然可以跑，但不是最优。  
- 需要额外的并查集数组（大小 `n`）以及两个长度为 26 的计数数组 → **O(n + 26)**，即 **O(n)** 的空间。

#### 代码（Python）

```python
from typing import List

class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点先是自己的父亲
        self.rank = [0] * n            # 用于按秩合并，降低树高

    def find(self, x: int) -> int:
        # 路径压缩：把查找路径上的所有节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:                    # 已经在同一个集合
            return
        # 按秩合并，秩小的挂到秩大的下面
        if self.rank[rx] < self.rank[ry]:
            self.parent[rx] = ry
        elif self.rank[rx] > self.rank[ry]:
            self.parent[ry] = rx
        else:
            self.parent[ry] = rx
            self.rank[rx] += 1


def numSpecialEquivGroups_bruteforce(words: List[str]) -> int:
    n = len(words)
    uf = UnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):
            if _equiv(words[i], words[j]):      # 两字符串是否等价
                uf.union(i, j)                 # 合并它们的集合

    # 统计不同的根节点数量，即为不同的等价组数
    roots = {uf.find(i) for i in range(n)}
    return len(roots)


def _equiv(a: str, b: str) -> bool:
    """判断两个字符串是否 special‑equivalent"""
    # 计数数组：26 个字母对应的出现次数
    even_a = [0] * 26
    odd_a = [0] * 26
    even_b = [0] * 26
    odd_b = [0] * 26

    for idx, ch in enumerate(a):
        if idx % 2 == 0:
            even_a[ord(ch) - ord('a')] += 1
        else:
            odd_a[ord(ch) - ord('a')] += 1

    for idx, ch in enumerate(b):
        if idx % 2 == 0:
            even_b[ord(ch) - ord('a')] += 1
        else:
            odd_b[ord(ch) - ord('a')] += 1

    # 两个计数数组完全相同即等价
    return even_a == even_b and odd_a == odd_b
```

#### 复杂度

- **时间复杂度**：`O(n²·k)`  
  - `n²` 来自两两比较，`k` 是字符串长度（每次比较要遍历一次字符串）。  
  - 大白话：如果有 1000 条字符串，每条 20 个字符，最坏要比较约 500,000 次，每次看 20 个字符，总共约 10 000 000 次字符检查，仍能在一秒左右跑完，但随着 `n` 增大就会显得慢。

- **空间复杂度**：`O(n)`  
  - 主要是并查集的 `parent`、`rank` 数组，另外每次比较临时的计数数组大小固定（26），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解我们已经发现：**只要偶数位字符集合相同且奇数位字符集合相同，两字符串就等价**。  
这意味着我们不必两两比较，只要把每个字符串**规范化**（归一化）成一种唯一的“代表形”，相同代表形的字符串自然属于同一组。

**规范化的办法**：

1. 把字符串的偶数下标字符提取出来，放进列表 `even`。  
2. 把奇数下标字符提取出来，放进列表 `odd`。  
3. 分别对 `even`、`odd` 排序（因为字符的出现顺序在等价判断中不重要），得到有序列表 `even_sorted`、`odd_sorted`。  
4. 把两段有序字符拼接成一个新字符串 `key = ''.join(even_sorted) + ''.join(odd_sorted)`。  

只要两个原始字符串的 `key` 完全相同，它们必然是 special‑equivalent。于是：

- 遍历 `words`，为每个单词算出 `key`，把 `key` 放进 **集合**（hash set）中。  
- 最终集合的大小就是不同等价组的数量。

> **类比**：把每个单词的“偶数盒子”和“奇数盒子”里的字母都排好序，就像把字典里的词条先按照字母表顺序排好，然后再把两个词条的排好序的“偶数段+奇数段”拼在一起，形成唯一的“指纹”。指纹相同的单词就是“同一族”。

**为什么更快**：

- 只需要 **一次**遍历每个字符串（`O(k)`），再做一次 **排序**（`O(k log k)`）。  
- 整体时间是 `O(n·k log k)`，远小于 `O(n²·k)`。  
- 空间只需要保存每个字符串的 `key`，即 `O(n·k)`，加上集合的哈希开销，仍然是线性空间。

#### 代码（Python）

```python
from typing import List

def numSpecialEquivGroups(words: List[str]) -> int:
    """
    返回 special-equivalent 字符串的组数
    思路：把每个字符串的偶数位字符和奇数位字符分别排序后拼接，得到唯一标识。
    将所有标识放进集合，集合大小即为答案。
    """
    groups = set()                       # 用来存放不同的标识（哈希表）

    for w in words:
        even_chars = []                  # 偶数位字符列表
        odd_chars = []                   # 奇数位字符列表

        for idx, ch in enumerate(w):
            if idx % 2 == 0:
                even_chars.append(ch)
            else:
                odd_chars.append(ch)

        # 对两段字符各自排序，使相同字符集合得到相同顺序
        even_chars.sort()
        odd_chars.sort()

        # 生成唯一的“指纹”
        key = ''.join(even_chars) + ''.join(odd_chars)
        groups.add(key)                  # 自动去重

    return len(groups)                   # 集合大小即为不同组数
```

#### 复杂度

- **时间复杂度**：`O(n·k log k)`  
  - 对每个字符串：提取字符 `O(k)`，排序 `O(k log k)`，拼接 `O(k)`。  
  - `n` 条字符串累计即 `O(n·k log k)`。  
  - 大白话：如果有 1000 条字符串、每条 20 个字符，排序每条只要 20·log₂20 ≈ 86 次比较，总共约 86,000 次操作，远快于暴力的几百万次。

- **空间复杂度**：`O(n·k)`  
  - 每条字符串生成的 `key` 长度为 `k`（偶数+奇数），存入集合需要线性空间。  
  - 额外的临时列表 `even_chars`、`odd_chars` 大小均 ≤ `k`，不随 `n` 增长。

---

## 心得

- **核心技巧**：把“可自由交换的下标集合”内部的字符视为**无序多集合**，只需对其**排序**或**计数**得到唯一表示。
- **适用的题型**  
  1. *字符串分组*（如 LeetCode 890 `Find and Replace Pattern`）  
  2. *字符集合等价*（如 LeetCode 839 `Similar String Groups`）  
  3. *数组/链表的可交换位置等价*（如 “相同奇偶位置可交换的数组分组”）
- **一句话总结**：把能随意交换的下标位置的字符**排序后拼接**，得到的“指纹”就是等价类的钥匙。

---

## 反思

- **第一反应**：直接两两比较，写出判等函数，然后用并查集合并。  
- **最容易踩的坑**  
  - 忘记把 **偶数位**和 **奇数位** 分开统计，导致错误地把跨位字符混在一起。  
  - 处理字符串长度为奇数时，偶数位会比奇数位多一个，需要保证两段分别排序后再拼接。  
  - 集合去重时要使用 **不可变** 类型（如字符串），如果误用列表会报错。  
- **下次类似题的第一步**：先思考“哪些位置的字符是可以互相自由交换的”，把这些位置的字符视作**一个袋子**，然后寻找**把袋子内容唯一化**（排序或计数）的方式。这样往往能立刻把 O(n²) 的暴力思路压缩到 O(n·log k)。