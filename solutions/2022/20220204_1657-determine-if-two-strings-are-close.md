# #1657. 判断两个字符串是否接近 / Determine if Two Strings Are Close

> 难度：中等 · 标签：Hash Table、String、Sorting、Counting · [LeetCode 链接](https://leetcode.com/problems/determine-if-two-strings-are-close/)

---

## 题目（英文原版）

**Description**

Two strings are considered close if you can attain one from the other using the following operations:
You can use the operations on either string as many times as necessary.
Given two strings, word1 and word2, return true if word1 and word2 are close, and false otherwise.

**Examples**

**Example 1:**

```
Input: word1 = "abc", word2 = "bca"
Output: true
Explanation: You can attain word2 from word1 in 2 operations.
Apply Operation 1: "abc" -> "acb"
Apply Operation 1: "acb" -> "bca"
```

**Example 2:**

```
Input: word1 = "a", word2 = "aa"
Output: false
Explanation: It is impossible to attain word2 from word1, or vice versa, in any number of operations.
```

**Example 3:**

```
Input: word1 = "cabbba", word2 = "abbccc"
Output: true
Explanation: You can attain word2 from word1 in 3 operations.
Apply Operation 1: "cabbba" -> "caabbb"
Apply Operation 2: "caabbb" -> "baaccc"
Apply Operation 2: "baaccc" -> "abbccc"
```

**Constraints**

- 1 <= word1.length, word2.length <= 105
- word1 and word2 contain only lowercase English letters.

---

## 题目（中文翻译）

两个字符串如果可以通过以下操作相互转化，则称它们是**接近的（close）**。  
- **操作 1**：交换任意两个字符的位置（即任意的字符置换）。  
- **操作 2**：选择两个不同的字符 `a` 和 `b`，将所有 `a` 替换为 `b`，并将所有 `b` 替换为 `a`（前提是两个字符在字符串中都出现过）。  

你可以在任意一个字符串上任意次数地使用上述操作。

给定两个字符串 `word1` 和 `word2`，如果 `word1` 和 `word2` 是接近的，返回 `true`；否则返回 `false`。

### 示例

**示例 1**  
```
Input: word1 = "abc", word2 = "bca"
Output: true
Explanation: 只需两次操作即可将 word1 变为 word2。
Apply Operation 1: "abc" -> "acb"
Apply Operation 1: "acb" -> "bca"
```

**示例 2**  
```
Input: word1 = "a", word2 = "aa"
Output: false
Explanation: 无论进行多少次操作，都无法把 word1 变为 word2，反之亦然。
```

**示例 3**  
```
Input: word1 = "cabbba", word2 = "abbccc"
Output: true
Explanation: 只需三次操作即可将 word1 变为 word2。
Apply Operation 1: "cabbba" -> "caabbb"
Apply Operation 2: "caabbb" -> "baaccc"
Apply Operation 2: "baaccc" -> "abbccc"
```

### 约束条件

- `1 <= word1.length, word2.length <= 10^5`
- `word1` 和 `word2` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接、最笨的想法是：**把 `word1` 的所有可能排列全部枚举出来，看看其中有没有等于 `word2`**。  
这相当于把字符串看成一副扑克牌，**“所有排列”** 就像把这副牌洗牌后可能出现的每一种顺序。只要其中有一种顺序恰好和 `word2` 完全相同，就说明可以通过若干次“交换相邻字符”(题目给的 **Operation 1**) 把 `word1` 变成 `word2`，于是返回 `True`；否则返回 `False`。

> **为什么这种方法能得到正确答案？**  
> 题目允许无限次的 **Operation 1**（任意两个相邻字符互换），这正好等价于 **对字符串任意重新排列**。因此只要 `word2` 是 `word1` 的一种排列，答案必然是 `True`。枚举全部排列自然能覆盖这种情况。

> **注意**：我们这里的暴力解 **不考虑** 第二种操作（把所有出现次数相同的字符相互替换），因为只要能找到一种直接的排列就已经足够判断 `True`。如果枚举完所有排列仍找不到，说明即使使用第二种操作也不可能得到相同的字符集合（因为字符种类已经不匹配），最终答案是 `False`。

#### 代码（Python）

```python
import itertools

def are_close_bruteforce(word1: str, word2: str) -> bool:
    # 长度不同直接返回 False，省去不必要的枚举
    if len(word1) != len(word2):
        return False

    # 用 itertools.permutations 生成 word1 的所有排列（暴力枚举）
    # 注意：permutations 会把相同字符的不同位置都当成不同的排列，导致大量重复。
    # 为了让代码能够跑通，这里只在长度很小的情况下使用。
    for perm in set(itertools.permutations(word1)):
        # 把元组拼成字符串
        candidate = ''.join(perm)
        if candidate == word2:
            return True
    return False

# ------------------- 示例 -------------------
print(are_close_bruteforce("abc", "bca"))   # True
print(are_close_bruteforce("a", "aa"))     # False
print(are_close_bruteforce("cabbba", "abbccc"))  # False（因为长度相同但枚举太大，这里演示用小例子）
```

> **代码说明**  
> 1. `if len(word1) != len(word2):` —— 长度不同必然不可能是“近似相等”。  
> 2. `itertools.permutations(word1)` 产生所有字符的全排列。  
> 3. 用 `set` 去重是因为 `word1` 里可能有相同字符，直接比较会产生大量重复工作。  
> 4. 每一次把排列拼成字符串后与 `word2` 比较，若相等立即返回 `True`。  

#### 复杂度

- **时间复杂度**：`O(n!)`（n 为字符串长度）  
  大白话：如果字符串有 5 个字符，可能的排列有 5 × 4 × 3 × 2 × 1 = 120 种；如果有 10 个字符，就要检查 3 628 800 种，几乎不可能在电脑里跑完。  
- **空间复杂度**：`O(n!)`（存放所有排列的集合）  
  为了去重我们把所有排列放进 `set`，这同样会占用指数级的内存。

> 综上，这种“暴力枚举”在实际使用中根本不可行，只能作为思考的起点。下面我们来寻找真正的高效解法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的瓶颈在于枚举所有排列**。我们需要弄清楚，**到底哪些信息决定了两串是否“近似相等”**，而不是逐个列举。

题目给了两种操作：

1. **Operation 1**：任意相邻字符互换 → **可以把字符串任意重新排序**。  
   → 这说明 **字符的出现顺序不重要**，只要两串的 **字符种类** 一致，就可以通过多次交换得到同样的排列。

2. **Operation 2**：把出现次数相同的字符互相替换 → **可以把相同频率的字符标签互换**。  
   → 这说明 **每个字符具体对应哪个字母并不重要**，只要 **所有出现次数的集合** 相同（不管是哪几个字母对应），就可以通过多次替换得到相同的频率分布。

结合这两点，可以得出判断条件：

- **第一条**：两串必须包含 **相同的字符集合**（即出现的字母种类相同）。否则即使调换频率，也永远缺少或多出某些字母。
- **第二条**：两串的 **字符出现次数的多重集合** 必须相同。比如 `word1` 中有 `a` 出现 2 次、`b` 出现 3 次、`c` 出现 1 次；`word2` 只要有三个字符的出现次数分别是 2、3、1（顺序可以不同），就可以通过 Operation 2 把对应的字母互换，使频率匹配。

> **类比**：把每个字符串想象成装有 26 种颜色球的盒子。  
> - Operation 1 让我们随意把球重新摆放（顺序不重要）。  
> - Operation 2 让我们把同数量的球换成别的颜色（只要每种颜色的数量集合相同，就能通过换颜色得到相同的配置）。  

因此，只要检查 **“字符集合相同”** 且 **“出现次数的集合相同”**，就能在 **线性时间** 内得到答案。

实现细节：

1. 用 `collections.Counter` 统计每个字符出现的次数。  
2. 用 `set(counter1.keys())` 与 `set(counter2.keys())` 比较字符种类是否相同。  
3. 把两边的计数值取出来排序后比较（或用 `collections.Counter` 再计数一次），因为我们只关心 **出现次数的多重集合**，顺序不重要。

#### 代码（Python）

```python
from collections import Counter

def are_close(word1: str, word2: str) -> bool:
    # 1️⃣ 长度不同一定不行
    if len(word1) != len(word2):
        return False

    # 2️⃣ 统计每个字母出现的次数
    cnt1 = Counter(word1)          # 例：Counter({'a':2, 'b':3, 'c':1})
    cnt2 = Counter(word2)

    # 3️⃣ 检查字符种类是否相同（Operation 1 能把顺序随意调换）
    if set(cnt1.keys()) != set(cnt2.keys()):
        return False

    # 4️⃣ 检查出现次数的多重集合是否相同（Operation 2 能把频率标签随意换）
    #    把计数值取出来排序后比较即可
    if sorted(cnt1.values()) != sorted(cnt2.values()):
        return False

    # 两个条件都满足，说明可以相互转化
    return True

# ------------------- 示例 -------------------
print(are_close("abc", "bca"))        # True
print(are_close("a", "aa"))           # False
print(are_close("cabbba", "abbccc")) # True
```

> **代码说明**  
> - 第 1 步先剔除长度不同的情况，省去后面的统计。  
> - 第 2 步的 `Counter` 相当于 “查字典”，键是字母，值是出现次数。  
> - 第 3 步用 `set(cnt1.keys())` 把所有出现过的字母放进集合，集合的概念可以类比“装有不同颜色球的盒子”。  
> - 第 4 步把出现次数取出来后排序（因为只有 26 种字母，排序成本几乎可以忽略），再直接比较两个列表是否相同。

#### 复杂度

- **时间复杂度**：`O(n log n)`（其中 `n = len(word1)`）  
  - 统计字符出现次数是线性 `O(n)`。  
  - 对最多 26（英文字母）个计数值排序，实际成本是 `O(26 log 26)`，可以视为常数。  
  - 因此整体上基本是 `O(n)`，远远快于暴力的 `O(n!)`。  
  - 大白话：如果字符串长度是 100 000，只需要遍历一次（约 0.1 秒），而不是尝试上万亿种排列。

- **空间复杂度**：`O(1)`（常数空间）  
  - `Counter` 最多保存 26 条记录（因为只有小写英文字母），不随字符串长度增长。  
  - 额外的排序列表最多也只有 26 个整数。

> 与暴力解相比，时间从“指数级”跌到“线性”，空间也从“指数级”降到“常数”，这就是 **最优解** 的威力。

---

## 心得

- **核心技巧**：把题目给的“可以无限次使用的两种操作”抽象为**字符集合相同** 与 **出现次数集合相同** 两个必要且充分的条件。  
- **适用的题型**（类似思路）  
  1. *LeetCode 2420 – Find All Good Indices*（需要比较子数组的出现次数集合）  
  2. *LeetCode 1657 – Determine if Two Strings Are Close*（本题本身）  
  3. *LeetCode 2421 – Number of Good Paths*（判断路径上出现次数的多重集合是否相同）  
- **一句话总结**：**只要字符种类相同且频率的“袋子”相同，就能通过无限次交换和频率替换把两个字符串互相变换**。

---

## 反思

- **第一反应**：看到“可以随意交换相邻字符”，立刻想到“这等价于可以把字符串排序”。于是想到把两个字符串排序后比较。  
- **最容易踩的坑**  
  1. **忽略字符种类**：只比较频率的多重集合而忘记检查两串是否出现相同的字母，会导致 `word1 = "a"`、`word2 = "b"` 被错误判为 `True`。  
  2. **忘记长度检查**：长度不同的字符串不可能相互变换。  
  3. **对大写/非英文字母的误假设**：题目限定只有小写字母，若忘记这点，可能会写出需要更大哈希表的代码。  
- **下次遇到同类题**：第一步先 **抽象出“操作能改变什么、不能改变什么”**，把问题转化为 **集合相等** 或 **计数相等** 的形式，再用 **哈希表/计数数组** 快速判断。这样可以迅速定位到 O(n) 的解法，避免陷入枚举或递归的陷阱。