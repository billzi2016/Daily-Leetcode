# #3076. 最短不公共子串 / Shortest Uncommon Substring in an Array

> 难度：中等 · 标签：Array、Hash Table、String、Trie · [LeetCode 链接](https://leetcode.com/problems/shortest-uncommon-substring-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given an array arr of size n consisting of non-empty strings.
Find a string array answer of size n such that:
Return the array answer.

**Examples**

**Example 1:**

```
Input: arr = ["cab","ad","bad","c"]
Output: ["ab","","ba",""]
Explanation: We have the following:
- For the string "cab", the shortest substring that does not occur in any other string is either "ca" or "ab", we choose the lexicographically smaller substring, which is "ab".
- For the string "ad", there is no substring that does not occur in any other string.
- For the string "bad", the shortest substring that does not occur in any other string is "ba".
- For the string "c", there is no substring that does not occur in any other string.
```

**Example 2:**

```
Input: arr = ["abc","bcd","abcd"]
Output: ["","","abcd"]
Explanation: We have the following:
- For the string "abc", there is no substring that does not occur in any other string.
- For the string "bcd", there is no substring that does not occur in any other string.
- For the string "abcd", the shortest substring that does not occur in any other string is "abcd".
```

**Constraints**

- n == arr.length
- 2 <= n <= 100
- 1 <= arr[i].length <= 20
- arr[i] consists only of lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个大小为 `n` 的字符串数组 `arr`，其中每个字符串均非空。  
请构造一个大小为 `n` 的字符串数组 `answer`，满足对每个下标 `i`（`0 ≤ i < n`）：

- `answer[i]` 是 `arr[i]` 的 **最短子串**（shortest substring），且该子串 **不出现在** `arr` 中除 `arr[i]` 之外的任何其他字符串里。
- 若不存在满足条件的子串，则 `answer[i]` 设为空字符串 `""`。

返回数组 `answer`。

**示例 1**  
输入: `arr = ["cab","ad","bad","c"]`  
输出: `["ab","","ba",""]`  
解释:  
- 对字符串 `"cab"`，满足条件的最短子串有 `"ca"` 和 `"ab"`，两者等长，取字典序更小的 `"ab"`。  
- 对字符串 `"ad"`，不存在不在其他字符串中出现的子串，答案为 `""`。  
- 对字符串 `"bad"`，满足条件的最短子串为 `"ba"`（长度 2），因此答案为 `"ba"`。  
- 对字符串 `"c"`，同样不存在满足条件的子串，答案为 `""`。

**示例 2**  
输入: `arr = ["abc","bcd","abcd"]`  
输出: `["","","abcd"]`  
解释:  
- 对 `"abc"`，所有子串均在其他字符串中出现，答案为 `""`。  
- 对 `"bcd"`，同理，答案为 `""`。  
- 对 `"abcd"`，唯一满足条件的最短子串就是整个字符串本身 `"abcd"`，因此答案为 `"abcd"`。

**约束条件**  
- `n == arr.length`  
- `2 ≤ n ≤ 100`  
- `1 ≤ arr[i].length ≤ 20`  
- `arr[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个字符串的所有子串都列出来**，然后统计每个子串在整个数组中出现了多少次。  
- **子串**：在日常生活中可以把它想象成“一段连续的文字”。比如 `"cab"` 的子串有 `"c"、"a"、"b"、"ca"、"ab"、"cab"`。  
- **哈希表**（Python 中的 `dict`）就像一本**查字典**，`key` 是子串，`value` 是它出现的次数。我们遍历所有字符串，把它们的子串“登记”进去。如果某个子串只出现一次（`value == 1`），说明它只属于某一个原字符串——这正是我们要找的“独有子串”。  

找到所有只出现一次的子串后，对每个原字符串再挑选 **最短** 的那个；如果有多个最短的，选 **字典序最小** 的（即在字母表里排在前面的那个）。如果一个字符串没有任何独有子串，答案就是空串 `""`。

**为什么这个方法一定正确？**  
因为我们枚举了**所有可能的子串**，并且准确记录了每个子串出现的次数。只要一个子串只在某个字符串里出现，它必然是该字符串的候选答案。再从候选中挑最短、字典序最小，就满足题目要求。

**时间/空间复杂度的大白话**  
- 对每个字符串（最多 100 个），我们要列出它所有的子串。一个长度为 `L` 的字符串有 `L·(L+1)/2` 个子串，`L ≤ 20`，所以每个字符串最多 210 个子串。把所有字符串的子串都放进哈希表，最多约 `100 * 210 = 21000` 条记录，这在电脑里算是**很小的存储**（几 MB 量级）。
- 时间上，我们要遍历这些子串两遍（一次统计，一次挑选），所以是 **O(n·L²)**，在本题的约束下完全可以接受。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def shortest_uncommon_substring(arr: List[str]) -> List[str]:
    # 1️⃣ 统计所有子串出现的次数
    cnt = defaultdict(int)               # 哈希表：子串 -> 出现次数
    # 为了避免同一个字符串内部出现多次的子串被算成多次出现，
    # 这里先用 set 去重
    for s in arr:
        seen = set()                      # 本字符串已经出现过的子串集合
        L = len(s)
        for i in range(L):
            for j in range(i + 1, L + 1):
                sub = s[i:j]
                if sub not in seen:       # 只计一次
                    seen.add(sub)
                    cnt[sub] += 1

    # 2️⃣ 对每个原字符串寻找答案
    ans = []
    for s in arr:
        best = ""                         # 当前最短、字典序最小的独有子串
        L = len(s)
        # 按长度从小到大枚举，这样第一个找到的就是最短的
        for length in range(1, L + 1):
            candidates = []               # 本轮长度下所有独有子串
            for i in range(L - length + 1):
                sub = s[i:i + length]
                if cnt[sub] == 1:         # 只出现一次 → 独有
                    candidates.append(sub)
            if candidates:                # 找到至少一个独有子串
                best = min(candidates)    # 取字典序最小的
                break                     # 已经是最短的，结束搜索
        ans.append(best)                  # 若没有找到，best 仍是 "" 
    return ans
```

#### 复杂度

- **时间复杂度：** `O(n · L²)`  
  - `n` 为字符串个数（≤100），`L` 为最长字符串长度（≤20）。  
  - “O(n·L²)” 可以读作“时间随字符串个数线性增长，随每个字符串长度的平方增长”。在本题的数值范围内，这个量级大约是几万次循环，运行毫秒级。

- **空间复杂度：** `O(n·L²)`  
  - 用哈希表存所有子串，最坏情况每个子串都是唯一的，需要存 `n·L·(L+1)/2` 条记录。相当于“占用的内存随字符串个数线性增长，随每个字符串长度的平方增长”。同样在题目限制下非常小。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于我们对每个字符串的每个子串都做了两遍遍历：一次统计，一次再去找最短独有子串。虽然在本题里已经够快，但我们仍可以把这两步**合并**，一次遍历就把“出现次数”和“是否是唯一的”信息都记下来。

**核心技巧：Trie（字典树）**  
- 想象 Trie 是一棵 **字母组成的树**，每条边对应一个字符。沿着根到某个节点的路径拼起来，就是一个子串。  
- 在每个节点我们记录 **这个子串出现的不同原字符串数量**（记为 `occ`）。如果 `occ == 1`，说明该子串只属于唯一的那条字符串，正是我们要的候选。  

**构造过程**  
1. **把所有子串插入 Trie**  
   - 对每个原字符串 `s`，先把它所有子串（去重后）插入 Trie。  
   - 插入时，如果当前路径的节点第一次被访问（即该子串第一次出现），把 `occ` 设为 1；否则把 `occ` 加 1。  
   - 为了防止同一字符串内部的同一子串被计多次，使用 **本字符串的子串集合** 先去重。

2. **在原字符串内部寻找答案**  
   - 再次遍历每个字符串 `s`，**从左到右、从短到长**检查它的子串。  
   - 对每个子串，只需要沿着 Trie 走到对应节点，查看 `occ` 是否为 1。  
   - 因为我们是 **按长度递增** 的顺序检查，一旦找到 `occ == 1` 的子串，就是 **最短** 的；如果同长度有多个，记录字典序最小的即可。

**为什么 Trie 更好？**  
- Trie 把相同前缀的子串共享同一段路径，**省掉了大量重复存储**。在统计出现次数时，只需要在对应节点上加一，而不必每次都在哈希表里创建新的键。  
- 查找子串是否唯一只需要 **一次字符遍历**（O(length)），而不是每次都去哈希表查询（虽然哈希表查询是 O(1)，但构造哈希表时会产生大量键对象，内存开销更大）。

**类比**  
- 把 Trie 想成一本 **按字母顺序排好的字典**，每本书（原字符串）里出现的每个词（子串）都在字典里留下脚印（出现次数）。我们只需要找出只在一本书里出现的词。

#### 代码（Python）

```python
from typing import List, Dict

class TrieNode:
    __slots__ = ('children', 'occ')
    def __init__(self):
        self.children: Dict[str, TrieNode] = {}  # 子节点，键是字符
        self.occ: int = 0                         # 该子串出现的不同原字符串数

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str):
        """把一个子串插入 Trie，occ 加 1（代表它来自另一个原字符串）"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                node.children[ch] = TrieNode()
            node = node.children[ch]
        node.occ += 1

    def query_occ(self, word: str) -> int:
        """返回子串 word 对应节点的 occ；若不存在返回 0"""
        node = self.root
        for ch in word:
            if ch not in node.children:
                return 0
            node = node.children[ch]
        return node.occ

def shortest_uncommon_substring_opt(arr: List[str]) -> List[str]:
    trie = Trie()

    # 1️⃣ 把所有子串（去重）插入 Trie，统计出现次数
    for s in arr:
        seen = set()
        L = len(s)
        for i in range(L):
            cur = []
            for j in range(i, L):
                cur.append(s[j])
                sub = ''.join(cur)          # 直接构造子串，避免多次切片
                if sub not in seen:
                    seen.add(sub)
                    trie.insert(sub)

    # 2️⃣ 对每个原字符串寻找最短独有子串
    ans = []
    for s in arr:
        best = ""
        L = len(s)
        found = False
        # 按长度递增枚举
        for length in range(1, L + 1):
            candidates = []
            for i in range(L - length + 1):
                sub = s[i:i + length]
                if trie.query_occ(sub) == 1:   # 只出现一次 → 独有
                    candidates.append(sub)
            if candidates:
                best = min(candidates)          # 取字典序最小的
                found = True
                break                           # 已是最短，停止更长长度的搜索
        ans.append(best if found else "")
    return ans
```

**关键行中文注释**  
- `TrieNode.__slots__`：用来**节省内存**，因为我们会创建很多节点。  
- `insert`：遍历子串的每个字符，如果对应的子节点不存在就新建，最后把 `occ` 加 1。  
- `query_occ`：沿着字符路径走到底，如果路径缺失直接返回 0，表示子串根本不存在。  
- `seen`：在同一个原字符串内部去重，防止同一子串在同一字符串里多次计数。  
- 外层两层循环（`length`、`i`）实现**从短到长**的枚举，第一轮找到的就是最短答案。

#### 复杂度

- **时间复杂度：** `O(n · L²)`（与暴力解相同的数量级）  
  - 插入所有子串：每个字符串产生 `L·(L+1)/2` 个子串，插入 Trie 每个字符只走一次，整体仍是 `O(n·L²)`。  
  - 查询答案时，同样是按长度遍历子串，查询 Trie 也是线性字符数，故同样是 `O(n·L²)`。  
  - 虽然渐进式相同，但 **常数更小**：Trie 共享前缀，减少了 Python 对字典键的创建与哈希计算。

- **空间复杂度：** `O(n · L²)`（更紧凑）  
  - Trie 中的节点数最多等于所有不同子串的字符总数，最坏情况下仍是所有子串的总长度 `≈ n·L²`，但相比于暴力解的哈希表存储完整子串对象，Trie 只存单个字符和计数，内存占用更低。

---

## 心得

- **核心技巧**：使用 **Trie**（字典树）统计子串出现次数，并在同一结构上完成查询。  
- **适用的题型**  
  1. “所有子串/前缀出现次数” 类问题（如 LeetCode 1804 *Implement Trie II*）。  
  2. “寻找唯一/最少出现的子序列/子串” 类问题（如 1680 *Concatenated Words* 中的前缀判断）。  
- **解题钥匙**：**把所有子串放进同一棵共享前缀的树里，节点的计数直接告诉你它是否唯一**。

---

## 反思

- **第一反应**：直接枚举每个字符串的子串，用哈希表计数——最自然、最容易实现的暴力思路。  
- **最容易踩的坑**  
  - **同一字符串内部的重复子串**：如果不去重，会把同一个子串计成多次，导致真正唯一的子串被误判为出现多次。  
  - **字典序的比较**：在找到最短长度的候选子串后，需要再取最小的字典序，忘记这一步会得到错误答案。  
  - **空答案的处理**：没有任何独有子串时要返回空串 `""`，而不是 `None` 或者遗漏。  
- **下次类似题目**，第一步应该想到 **“把所有子串统一放进一个可以共享前缀的数据结构（Trie）或统一的计数表”**，这样既能快速统计出现次数，又能在查询时直接利用结构的层次信息找最短/唯一的子串。