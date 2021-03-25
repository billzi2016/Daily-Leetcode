# #1268. 搜索建议系统 / Search Suggestions System

> 难度：中等 · 标签：Array、String、Binary Search、Trie、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/search-suggestions-system/)

---

## 题目（英文原版）

**Description**

You are given an array of strings products and a string searchWord.
Design a system that suggests at most three product names from products after each character of searchWord is typed. Suggested products should have common prefix with searchWord. If there are more than three products with a common prefix return the three lexicographically minimums products.
Return a list of lists of the suggested products after each character of searchWord is typed.

**Examples**

**Example 1:**

```
Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
Explanation: products sorted lexicographically = ["mobile","moneypot","monitor","mouse","mousepad"].
After typing m and mo all products match and we show user ["mobile","moneypot","monitor"].
After typing mou, mous and mouse the system suggests ["mouse","mousepad"].
```

**Example 2:**

```
Input: products = ["havana"], searchWord = "havana"
Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
Explanation: The only word "havana" will be always suggested while typing the search word.
```

**Constraints**

- 1 <= products.length <= 1000
- 1 <= products[i].length <= 3000
- 1 <= sum(products[i].length) <= 2 * 104
- All the strings of products are unique.
- products[i] consists of lowercase English letters.
- 1 <= searchWord.length <= 1000
- searchWord consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串数组 **products** 和一个字符串 **searchWord**。  
设计一个系统，使得在用户输入 **searchWord** 的每个字符后，系统最多返回三个产品名称作为建议。  
建议的产品必须与 **searchWord** 具有公共前缀（common prefix）。如果拥有相同前缀的产品超过三个，则返回字典序（lexicographically）最小的三个产品。  
返回一个 **list of lists**，其中第 *i* 个子列表表示输入第 *i* 个字符后得到的建议产品集合。

**示例 1**

```text
Input: products = ["mobile","mouse","moneypot","monitor","mousepad"], searchWord = "mouse"
Output: [["mobile","moneypot","monitor"],["mobile","moneypot","monitor"],["mouse","mousepad"],["mouse","mousepad"],["mouse","mousepad"]]
```

**Explanation**: 将 `products` 按字典序排序得到 `["mobile","moneypot","monitor","mouse","mousepad"]`。  
在输入字符 `m` 和 `mo` 时，所有产品都匹配前缀，系统展示前三个词 `["mobile","moneypot","monitor"]`。  
随后输入 `mou`、`mous`、`mouse`，匹配的前缀仅剩 `["mouse","mousepad"]`，因此这两个词始终被返回。

**示例 2**

```text
Input: products = ["havana"], searchWord = "havana"
Output: [["havana"],["havana"],["havana"],["havana"],["havana"],["havana"]]
```

**Explanation**: 唯一的词 `"havana"` 在输入的每个字符阶段都会被建议。

**约束条件**

- `1 <= products.length <= 1000`
- `1 <= products[i].length <= 3000`
- `1 <= sum(products[i].length) <= 2 * 10^4`
- 所有 `products` 中的字符串互不相同
- `products[i]` 仅由小写英文字母组成
- `1 <= searchWord.length <= 1000`
- `searchWord` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**每输入一个字符，就遍历所有商品名称，找出以当前前缀开头的单词**，再把它们按字典序排好，取前 3 个返回。  

- **遍历所有商品**：相当于把 `products` 当成一大堆书名，手里拿着一本字典（搜索词），把每本书的标题一个个和字典的前缀比对。  
- **前缀匹配**：`word.startswith(prefix)` 就像检查一本书的标题是否以“莫”开头。  
- **排序**：把匹配到的标题按字典顺序排好（像把符合条件的书排成一本顺序的书架）。  
- **取前 3**：只取最前面的三本书返回。

这种方法一定能得到正确答案，因为我们把所有可能的商品都检查了一遍，只要满足前缀条件就一定会被考虑进去。

#### 代码（Python）

```python
from typing import List

def suggestedProducts_bruteforce(products: List[str], searchWord: str) -> List[List[str]]:
    # 先把所有商品按字典序排好，这样后面取前 3 时就已经是最小的三个了
    products.sort()                               # O(N log N)

    ans = []
    prefix = ""                                    # 当前已经输入的前缀
    for ch in searchWord:                          # 对每个字符逐个处理
        prefix += ch                               # 更新前缀
        matches = []                               # 用来收集本次匹配的商品

        # 暴力遍历所有商品，检查是否以当前前缀开头
        for prod in products:                     # O(N) 次遍历
            if prod.startswith(prefix):           # 前缀匹配
                matches.append(prod)              # 匹配成功就加入结果

        # 只取前 3 个（因为已经排好序，所以直接切片即可）
        ans.append(matches[:3])                   # O(1) 取切片

    return ans
```

#### 复杂度

- **时间复杂度**：  
  - 排序一次 `O(N log N)`（`N` 为商品数量）。  
  - 对每个字符（`M = len(searchWord)`）都遍历全部商品 `O(N)`，所以主体是 `O(M·N)`。  
  - 综合来看是 `O(N log N + M·N)`，在最坏情况下（`M≈1000, N≈1000`）约为 `10⁶` 次比较，仍在可接受范围。  
- **空间复杂度**：  
  - 只用了几个额外的列表，最多存放当前前缀匹配的商品，最坏是 `O(N)`（全部商品都匹配）。  
  - 除了输入外，额外空间是线性的 `O(N)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每输入一个字符都要遍历全部商品**，这会导致 `O(M·N)` 的时间。  
我们可以把商品列表 **先排好序**，然后利用 **二分查找** 快速定位“第一个可能匹配的商品”。之后只需要检查紧随其后的几个商品（最多 3+若干个）就能得到答案，避免全表扫描。

关键步骤：

1. **排序**  
   把 `products` 按字典序排好。排序一次 `O(N log N)`，后面所有的查找都基于这个有序数组。

2. **二分定位前缀的左边界**  
   对于每个前缀 `prefix`，我们在排好序的数组里找 **第一个** 不小于 `prefix` 的位置。  
   - 这相当于在字典里找“第一个不早于‘mo’的单词”。  
   - Python 的 `bisect_left` 能在 `O(log N)` 时间内完成。

3. **收集最多 3 条建议**  
   从找到的左边界向右检查最多 3 条商品，判断它们是否真的以 `prefix` 开头（因为二分只保证不小于前缀，可能出现不匹配的情况）。  
   - 检查的次数至多 3 次（每次 O(1)），所以总体仍是 `O(log N)`。

这样，每输入一个字符的时间从 `O(N)` 降到 `O(log N)`，整体时间复杂度变为 `O(N log N + M·log N)`，在最坏情况下约为 `10⁴` 次操作，远快于暴力解。

> **为什么二分能工作？**  
> 排好序后，所有以同一前缀开头的单词会 **连续** 出现在数组里。二分找到的左边界恰好是这段连续区间的起点，因此只要往后检查几条记录，就能得到全部（最多 3 条）匹配。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List

def suggestedProducts_optimal(products: List[str], searchWord: str) -> List[List[str]]:
    # 1. 先把商品排序，保证字典序连续性
    products.sort()                     # O(N log N)

    ans = []
    prefix = ""
    for ch in searchWord:               # 对每个字符依次处理
        prefix += ch                    # 当前前缀

        # 2. 二分查找第一个 >= prefix 的位置
        start = bisect_left(products, prefix)   # O(log N)

        # 3. 从 start 开始检查最多 3 条，收集真正匹配的商品
        suggestions = []
        for i in range(start, min(start + 3, len(products))):
            if products[i].startswith(prefix):   # 仍需确认前缀匹配
                suggestions.append(products[i])
        ans.append(suggestions)        # 记录本次建议

    return ans
```

#### 复杂度

- **时间复杂度**：  
  - 排序一次 `O(N log N)`。  
  - 对每个字符进行二分查找 `O(log N)`，再检查最多 3 条记录 `O(1)`。  
  - 总体 `O(N log N + M·log N)`。相较于暴力的 `O(M·N)`，大幅提升。  

- **空间复杂度**：  
  - 除了输入外，只使用了常数级别的额外空间（`prefix`、若干临时列表），所以是 `O(1)`（不计返回结果的空间）。  

> **与 Trie 的对比**：  
> 另一种常见的最优解是构建 **Trie（前缀树）**，在每个节点预先保存该前缀下字典序最小的 3 条商品。构建 Trie 需要 `O(total length of products)` 的时间和空间，查询每个字符只需 `O(1)`。这里我们采用二分法实现，因为实现更简洁且对 Python 来说常数更小。

---

## 心得

- **核心技巧**：先排序 + 二分定位前缀的左边界，再取最多 3 条匹配。  
- **适用的题型**：  
  1. **前缀搜索**（如 LeetCode 500. Keyboard Row）  
  2. **区间查询**（如 LeetCode 240. Search a 2D Matrix II）  
  3. **前缀自动完成**（如本题、LeetCode 642. Design Search Autocomplete）  
- **一句话总结**：**“把数据排好序，用二分快速定位，前缀匹配只检查极少几条”。**

## 反思

- **第一反应**：直接遍历所有商品进行前缀匹配（暴力），因为思路最直观。  
- **最容易踩的坑**：  
  - 忘记对 `products` 先排序，导致取出的 3 条不一定是字典序最小的。  
  - 二分后只检查 **恰好 3 条**，但需要先确认它们真的匹配前缀（否则会返回不相关的单词）。  
  - 边界条件：`searchWord` 长度可能大于所有商品的长度，或前缀在数组末尾找不到匹配，需要返回空列表。  
- **下次思路**：遇到“前缀 + 取前 K 条”这类需求时，先考虑 **排序 + 二分**（或 Trie）来把 “全表遍历” 的瓶颈消除。这样可以把时间复杂度从线性降到对数级。