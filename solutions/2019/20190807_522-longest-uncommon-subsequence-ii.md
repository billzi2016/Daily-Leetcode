# #522. 最长不常见子序列 II / Longest Uncommon Subsequence II

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/longest-uncommon-subsequence-ii/)

---

## 题目（英文原版）

**Description**

Given an array of strings strs, return the length of the longest uncommon subsequence between them. If the longest uncommon subsequence does not exist, return -1.
An uncommon subsequence between an array of strings is a string that is a subsequence of one string but not the others.
A subsequence of a string s is a string that can be obtained after deleting any number of characters from s.

**Examples**

**Example 1:**

```
Input: strs = ["aba","cdc","eae"]
Output: 3
```

**Example 2:**

```
Input: strs = ["aaa","aaa","aa"]
Output: -1
```

**Constraints**

- 2 <= strs.length <= 50
- 1 <= strs[i].length <= 10
- strs[i] consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 `strs`，返回它们之间**最长不常见子序列**（longest uncommon subsequence）的长度。如果不存在这样的子序列，返回 `-1`。

**不常见子序列**（uncommon subsequence）指的是：该字符串是某一个字符串的**子序列**（subsequence），但不是其他所有字符串的子序列。  
**子序列**（subsequence）是指可以通过从原字符串中删除任意数量的字符（包括零个）得到的字符串。

#### 示例

**示例 1**

```text
Input: strs = ["aba","cdc","eae"]
Output: 3
```

**示例 2**

```text
Input: strs = ["aaa","aaa","aa"]
Output: -1
```

#### 约束条件

- `2 <= strs.length <= 50`
- `1 <= strs[i].length <= 10`
- `strs[i]` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要我们找 **最长的** “不常见子序列”。  
不常见子序列的定义是：

* 它是某个字符串的子序列（可以删掉任意字符得到），  
* 同时 **不是** 其它所有字符串的子序列。

最直接的想法是把每个字符串都当作候选答案，逐个验证：

1. 对数组中的每个字符串 `s`：  
   检查 `s` 是否是 **其他** 任意字符串的子序列。  
   - 只要找到一条“`s` 是别的字符串的子序列”，`s` 就不合格，直接进入下一个候选。  
   - 如果遍历完都没有发现 `s` 被包含，则 `s` 合格，记录下它的长度。  
2. 最后返回所有合格字符串的最大长度；若没有合格的，返回 `-1`。

> **数据结构类比**：  
> 检查“是否是子序列”就像在一本书里找某句话。我们用 **双指针**（两个手指）从左到右同步阅读：一本书的指针走得快点，另一句的指针只在匹配到相同字符时才前进一步。全部匹配完后，说明这句话（子序列）真的能在书里找到。

> **为什么正确**：  
> 只要遍历了所有字符串，并且每次都严格按照“不被其它任何字符串包含”来判断，那么最终得到的最长长度必然是题目要求的答案。

#### 代码（Python）

```python
from typing import List

def is_subsequence(short: str, long: str) -> bool:
    """
    双指针检查 short 是否是 long 的子序列
    """
    i = j = 0
    while i < len(short) and j < len(long):
        if short[i] == long[j]:
            i += 1          # 匹配成功，短串指针前进
        j += 1              # 长串指针始终前进
    return i == len(short)  # 全部匹配完毕说明是子序列

def findLUSlength_bruteforce(strs: List[str]) -> int:
    n = len(strs)
    max_len = -1

    for i in range(n):
        candidate = strs[i]
        # 检查 candidate 是否是其它任何字符串的子序列
        uncommon = True
        for j in range(n):
            if i == j:
                continue
            if is_subsequence(candidate, strs[j]):
                uncommon = False
                break   # 已经被别的字符串包含，直接放弃
        if uncommon:
            max_len = max(max_len, len(candidate))

    return max_len
```

#### 复杂度

- **时间复杂度**：`O(n² · L)`  
  - `n` 是字符串个数（最多 50），  
  - `L` 是单个字符串的最长长度（最多 10）。  
  解释：我们要对每一对字符串 (`n²` 次) 调用一次子序列检查，而每次检查最多遍历 `L` 个字符。

- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量（指针、布尔值），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解已经能在题目限制下跑完，但仍有两个可以利用的“加速点”：

1. **长度排序 + 早停**  
   - 题目要求最长的不常见子序列。  
   - 把所有字符串按长度从大到小排序，先检查长的。  
   - 当我们找到第一个合格的字符串时，它的长度必然是最大值，后面更短的字符串就不必再检查了。  
   - 这相当于“先挑大块”，可以大幅减少不必要的比较。

2. **去重**  
   - 如果同一个字符串出现了两次或更多次，那么它不可能是答案，因为它已经是其它字符串的子序列（相同的字符串本身就是子序列）。  
   - 因此可以先统计出现次数，只对出现一次的字符串做子序列检查。

核心算法仍然是 **双指针** 判断子序列，但通过排序+去重让我们只在最有希望的候选上浪费时间。

> **类比**：  
> 想象你在挑选最高的山峰。先把所有山峰按高度从高到低排好队，最高的先检查。如果最高的山峰是“独一无二的”，你直接返回它的高度；如果不是，就继续检查第二高的，依此类推。这样你永远不会去检查比答案低得多的山。

#### 代码（Python）

```python
from typing import List
from collections import Counter

def is_subsequence(short: str, long: str) -> bool:
    """双指针实现，详见暴力解中的说明"""
    i = j = 0
    while i < len(short) and j < len(long):
        if short[i] == long[j]:
            i += 1
        j += 1
    return i == len(short)

def findLUSlength_optimal(strs: List[str]) -> int:
    # 1️⃣ 统计出现次数，出现 >1 次的直接剔除
    cnt = Counter(strs)

    # 2️⃣ 按长度降序排列，长度相同的可以随意顺序
    strs_sorted = sorted(strs, key=len, reverse=True)

    for i, cand in enumerate(strs_sorted):
        # 只考虑唯一出现的字符串
        if cnt[cand] > 1:
            continue

        # 检查 cand 是否是其它任何字符串的子序列
        uncommon = True
        for j, other in enumerate(strs_sorted):
            if i == j:          # 同一个位置，不比较
                continue
            if len(other) < len(cand):
                # 由于已经按长度从大到小排序，后面的字符串更短
                # 短串不可能包含更长的 cand，直接跳出循环
                break
            if is_subsequence(cand, other):
                uncommon = False
                break

        if uncommon:
            return len(cand)   # 第一个满足条件的，就是最长的

    return -1                 # 没有符合条件的字符串
```

#### 复杂度

- **时间复杂度**：`O(n² · L)`（最坏情况仍然如此）  
  - 通过排序 `O(n log n)` 和去重 `O(n)` 的额外开销可以忽略不计。  
  - 与暴力解的差别在于 **早停**：一旦找到答案立即返回，平均情况下会检查 far fewer pairs。  

- **空间复杂度**：`O(n)`  
  - 需要额外的计数器 `Counter`（存 `n` 条记录）以及排序产生的临时列表。  

相比暴力解，**最优解在实际运行时往往更快**，尤其当数组里有很多短字符串或大量重复时，提前返回可以显著减少比较次数。

---

## 心得

- **核心技巧**：  
  - 使用 **双指针** 判断一个字符串是否是另一个的子序列。  
  - **排序 + 早停**：先处理更有可能成为答案的长字符串。  
  - **去重**：出现多次的字符串必然不符合“不常见”要求。

- **适用的题型**（类似思路）  
  1. *Longest Uncommon Subsequence I*（只涉及两个字符串的情况）。  
  2. *Maximum Length of Pair Chain*（先排序再贪心）。  
  3. *Find the Duplicate Number*（利用计数/去重的思路）。

- **一句话总结**：  
  “先把最长、唯一的字符串挑出来，用双指针快速检查是否被别的字符串覆盖，找到的第一条就是答案。”

---

## 反思

- **第一反应**：  
  “遍历每个字符串，逐一判断它是不是别的字符串的子序列”，这就是暴力思路。

- **最容易踩的坑**  
  1. **重复字符串**：忘记去重会导致错误返回，因为相同的字符串本身就是彼此的子序列。  
  2. **子序列判断的细节**：双指针的循环条件必须同时检查两个指针，防止越界。  
  3. **提前结束的时机**：排序后要记得在遍历到更短的字符串时直接 break，避免不必要的比较。

- **下次遇到同类题的第一步**：  
  “把输入按关键属性（这里是长度）排序，并过滤掉显然不可能的候选（重复），再用最基础的判定工具（双指针）逐个验证”。这样可以把搜索空间快速压缩到最小。