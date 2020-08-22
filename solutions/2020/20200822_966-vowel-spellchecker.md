# #966. **元音拼写检查器** / Vowel Spellchecker

> 难度：中等 · 标签：Array、Hash Table、String · [LeetCode 链接](https://leetcode.com/problems/vowel-spellchecker/)

---

## 题目（英文原版）

**Description**

Given a wordlist, we want to implement a spellchecker that converts a query word into a correct word.
For a given query word, the spell checker handles two categories of spelling mistakes:
In addition, the spell checker operates under the following precedence rules:
Given some queries, return a list of words answer, where answer[i] is the correct word for query = queries[i].

**Examples**

**Example 1:**

```
Input: wordlist = ["KiTe","kite","hare","Hare"], queries = ["kite","Kite","KiTe","Hare","HARE","Hear","hear","keti","keet","keto"]
Output: ["kite","KiTe","KiTe","Hare","hare","","","KiTe","","KiTe"]
```

**Example 2:**

```
Input: wordlist = ["yellow"], queries = ["YellOw"]
Output: ["yellow"]
```

**Constraints**

- 1 <= wordlist.length, queries.length <= 5000
- 1 <= wordlist[i].length, queries[i].length <= 7
- wordlist[i] and queries[i] consist only of only English letters.

---

## 题目（中文翻译）

给定一个单词表（wordlist），实现一个拼写检查器（spellchecker），将查询单词（query）转换为正确的单词。  
对于每个查询单词，拼写检查器需要处理以下两类拼写错误：

1. **大小写错误**（case‑insensitive）：单词的字母大小写不匹配，但字母本身相同。  
2. **元音错误**（vowel error）：单词中所有元音字母 `a, e, i, o, u`（不区分大小写）都可以相互替换，例如 `"hello"` 与 `"hallo"` 视为相同。

拼写检查器按照如下优先级规则进行匹配：

1. **完全匹配**（exact match）：如果查询单词在单词表中出现，直接返回该单词。  
2. **大小写不敏感匹配**（case‑insensitive match）：如果在单词表中找不到完全匹配，但存在大小写不敏感的匹配，返回单词表中首次出现的该单词。  
3. **元音错误匹配**（vowel error match）：如果前两种匹配都不存在，但存在元音错误匹配，返回单词表中首次出现的该单词。  
4. 若上述所有匹配均不存在，则返回空字符串 `""`。

给定若干查询单词 `queries`，返回一个答案列表 `answer`，其中 `answer[i]` 为查询 `queries[i]` 对应的正确单词。

**示例 1**  

```text
Input: wordlist = ["KiTe","kite","hare","Hare"], queries = ["kite","Kite","KiTe","Hare","HARE","Hear","hear","keti","keet","keto"]
Output: ["kite","KiTe","KiTe","Hare","hare","","","KiTe","","KiTe"]
```

**示例 2**  

```text
Input: wordlist = ["yellow"], queries = ["YellOw"]
Output: ["yellow"]
```

**约束条件**

- `1 <= wordlist.length, queries.length <= 5000`
- `1 <= wordlist[i].length, queries[i].length <= 7`
- `wordlist[i]` 与 `queries[i]` 仅由英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法就是把每一个查询 `query` 与 `wordlist` 中的每个单词逐个比较，依次检查三条规则：

1. **完全匹配**（大小写完全相同）。  
2. **大小写不敏感匹配**：把 `query` 和 `wordlist` 中的单词都转成小写后比较。  
3. **元音错误匹配**：把单词中的所有元音（`a e i o u`）都统一换成同一个字符（比如 `*`），再比较。

如果在 `wordlist` 中找到了满足上述某一条的单词，就返回它；否则返回空串 `""`。

> **类比**：  
> - **哈希表**就像一本字典，`key` 是单词（或处理后的单词），`value` 是原始单词。我们只需要一次“查页码”就能得到答案。  
> - **把元音统一成 `*`**就像把颜色相近的几种笔统一成一种颜色，方便“只看形状不看颜色”。

虽然思路很清晰，但因为每一次查询都要遍历完整个 `wordlist`（最多 5000 条），所以会非常慢。

#### 代码（Python）

```python
from typing import List

VOWELS = set('aeiouAEIOU')

def mask_vowels(word: str) -> str:
    """把元音统一成 '*'，其它字符保持不变"""
    return ''.join('*' if ch in VOWELS else ch for ch in word.lower())

def spellchecker_bruteforce(wordlist: List[str], queries: List[str]) -> List[str]:
    ans = []
    for q in queries:
        # 1. 完全匹配
        if q in wordlist:
            ans.append(q)
            continue

        # 2. 大小写不敏感匹配
        q_low = q.lower()
        found = False
        for w in wordlist:
            if w.lower() == q_low:
                ans.append(w)      # 返回 wordlist 中第一次出现的原始单词
                found = True
                break
        if found:
            continue

        # 3. 元音错误匹配
        q_mask = mask_vowels(q)
        for w in wordlist:
            if mask_vowels(w) == q_mask:
                ans.append(w)
                found = True
                break
        if not found:
            ans.append("")          # 没有匹配到，返回空串
    return ans
```

> **关键行注释**  
> - `mask_vowels`：把所有元音字符换成 `*`，并统一转成小写，便于后面的比较。  
> - 第一次 `if q in wordlist`：直接利用 Python 列表的线性查找实现完全匹配。  
> - 第二层循环：遍历 `wordlist` 找到第一个大小写不敏感匹配的单词。  
> - 第三层循环：再遍历一次找元音错误匹配。

#### 复杂度  

- **时间复杂度**：`O(m * n * L)`  
  - `m = len(queries)`，`n = len(wordlist)`，`L` 为单词的最大长度（≤7）。  
  - 对每个查询我们最坏要遍历 `wordlist` 三遍，每遍都要比较长度为 `L` 的字符串。  
  - 用大白话说，就是 **“查询数 × 单词表大小 × 单词长度”**，在最坏情况下大约是 5000 × 5000 × 7 ≈ 1.75×10⁸ 次字符比较，明显会超时。

- **空间复杂度**：`O(1)`（不计输入输出本身）。只用了常数级别的临时变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每一次查询都要 **线性遍历** 整个 `wordlist`。如果我们能在 **常数时间**（或对数时间）内直接定位到可能的答案，就能把时间从 `O(m·n·L)` 降到 `O(m·L)`。

关键在于把 “查找” 的过程转化为 **哈希表（字典）查询**，因为字典的查找时间近似 `O(1)`。我们需要构造三张映射表，分别对应三条匹配规则：

| 规则 | 需要的映射 | 解释 |
|------|-----------|------|
| 完全匹配 | `exact_set`（`set`） | 把 `wordlist` 中的单词直接放进集合，判断 `query` 是否在集合里，等价于 “字典里有没有这页”。 |
| 大小写不敏感匹配 | `case_map: lower_word -> original_word` | 把 `wordlist` 中每个单词的小写形式作为键，原始单词（第一次出现的）作为值。查询时把 `query` 小写后直接查表。 |
| 元音错误匹配 | `vowel_map: masked_word -> original_word` | 把单词先 **统一转小写**，再把所有元音换成 `*`（称为 **“掩码”**），得到键。值仍然是第一次出现的原始单词。查询时对 `query` 做同样的掩码后查表。 |

构造映射时 **只保留第一次出现的原始单词**，因为题目要求返回 `wordlist` 中最早出现的匹配。

构造完这三张表后，对每个 `query` 按照优先级依次查表：

1. `query` 是否在 `exact_set` → 完全匹配。  
2. `query.lower()` 是否在 `case_map` → 大小写不敏感匹配。  
3. `mask_vowels(query)` 是否在 `vowel_map` → 元音错误匹配。  
4. 都不在 → 返回 `""`。

> **类比**：  
> - `exact_set` 像一本 **有序的目录**，直接定位页码。  
> - `case_map` 把所有大小写不同的写法都映射到同一页，类似 **忽略大小写的电话簿**。  
> - `vowel_map` 把所有元音“模糊化”，像 **把颜色相近的颜料混在一起**，只看形状不看颜色。

#### 代码（Python）

```python
from typing import List

VOWELS = set('aeiou')

def devowel(word: str) -> str:
    """
    将单词统一转小写后，把所有元音字符替换为 '*'
    例如 "KiTe" -> "k*t*"
    """
    return ''.join('*' if ch in VOWELS else ch for ch in word.lower())

def spellchecker(wordlist: List[str], queries: List[str]) -> List[str]:
    # 1. 完全匹配集合
    exact_set = set(wordlist)

    # 2. 大小写不敏感映射：小写形式 -> 第一次出现的原始单词
    case_map = {}
    for w in wordlist:
        low = w.lower()
        if low not in case_map:           # 只保留第一次出现的
            case_map[low] = w

    # 3. 元音错误映射：掩码形式 -> 第一次出现的原始单词
    vowel_map = {}
    for w in wordlist:
        masked = devowel(w)
        if masked not in vowel_map:
            vowel_map[masked] = w

    # 4. 对每个查询依次查表
    ans = []
    for q in queries:
        if q in exact_set:                # 完全匹配
            ans.append(q)
            continue

        low = q.lower()
        if low in case_map:               # 大小写不敏感匹配
            ans.append(case_map[low])
            continue

        masked = devowel(q)
        if masked in vowel_map:           # 元音错误匹配
            ans.append(vowel_map[masked])
            continue

        ans.append("")                    # 都没有匹配
    return ans
```

> **关键行注释**  
> - `exact_set = set(wordlist)`：把所有单词放进集合，查找是否完全相同只需要一次 “在不在集合里”。  
> - `case_map` 与 `vowel_map` 的 `if key not in map` 保证**返回最早出现的单词**。  
> - `devowel`：先把单词转成小写，再把元音换成 `*`，这样 `kite`、`kAtE`、`k*te` 都会得到同样的掩码 `k*te`。  
> - 查询时按优先级依次判断，符合题目要求的“先完全匹配 → 再大小写不敏感 → 再元音错误”。

#### 复杂度  

- **时间复杂度**：`O((n + m) * L)`  
  - 构造三张映射表遍历 `wordlist` 一遍，时间 `O(n * L)`（`L ≤ 7`）。  
  - 处理每个查询只做 **常数次** 字典查找和一次 `devowel`（`O(L)`），总计 `O(m * L)`。  
  - 用大白话说，就是 **“遍历一次单词表 + 对每个查询做一次线性（但很短）处理”**，远远快于暴力的 `O(m·n·L)`。

- **空间复杂度**：`O(n * L)`  
  - 需要额外存储三张映射表，最坏每个单词都占用一次键和值，键的长度为 `L`。  
  - 这相当于 **“复制一遍 wordlist”**，在本题的约束（最多 5000 条、每条最长 7）下完全可以接受。

---

## 心得

- **核心技巧**：使用 **哈希表**（字典）把“查找”操作从线性遍历提升到近乎常数时间。  
- **适用的题型**  
  1. **大小写不敏感匹配**（如 LeetCode 245. Shortest Word Distance III）。  
  2. **模糊匹配**（如把字符统一映射后比较），常见于 **电话号码键盘**、**单词拼写纠错**。  
  3. **多层次匹配规则**（先精确、后宽松），如 **搜索建议**、**路径匹配**等。  
- **一句话总结**：**“把每种匹配规则预先映射成哈希表，查询时按优先级直接查表”**。

---

## 反思

- **第一反应**：直接遍历 `wordlist`，对每个查询逐个比较。  
- **最容易踩的坑**  
  - **忽略出现顺序**：题目要求返回 `wordlist` 中最先出现的匹配，需要在构造映射表时只保留第一次出现的单词。  
  - **元音定义**：只考虑 `a e i o u`（不区分大小写），要先统一转小写再替换。  
  - **空字符串返回**：没有任何匹配时必须返回 `""` 而不是 `None`。  
- **下次类似题的第一步**：先思考 **“有没有办法把匹配过程转化为一次哈希查找”**，如果可以，就立即构造对应的映射表。这样往往能把时间复杂度从 `O(N·M)` 降到 `O(N+M)`。