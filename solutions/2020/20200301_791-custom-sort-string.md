# #791. 自定义排序字符串 / Custom Sort String

> 难度：中等 · 标签：Hash Table、String、Sorting · [LeetCode 链接](https://leetcode.com/problems/custom-sort-string/)

---

## 题目（英文原版）

**Description**

You are given two strings order and s. All the characters of order are unique and were sorted in some custom order previously.
Permute the characters of s so that they match the order that order was sorted. More specifically, if a character x occurs before a character y in order, then x should occur before y in the permuted string.
Return any permutation of s that satisfies this property.

**Examples**

**Example 1:**

```
Input: order = "cba", s = "abcd"
Output: "cbad"
Explanation: "a" , "b" , "c" appear in order, so the order of "a" , "b" , "c" should be "c" , "b" , and "a" .
Since "d" does not appear in order , it can be at any position in the returned string. "dcba" , "cdba" , "cbda" are also valid outputs.
```

**Example 2:**

```
Input: order = "bcafg", s = "abcd"
Output: "bcad"
Explanation: The characters "b" , "c" , and "a" from order dictate the order for the characters in s . The character "d" in s does not appear in order , so its position is flexible.
Following the order of appearance in order , "b" , "c" , and "a" from s should be arranged as "b" , "c" , "a" . "d" can be placed at any position since it's not in order. The output "bcad" correctly follows this rule. Other arrangements like "dbca" or "bcda" would also be valid, as long as "b" , "c" , "a" maintain their order.
```

**Constraints**

- 1 <= order.length <= 26
- 1 <= s.length <= 200
- order and s consist of lowercase English letters.
- All the characters of order are unique.

---

## 题目（中文翻译）

**题目描述**  
给定两个字符串 `order` 和 `s`。`order` 中的所有字符互不相同，并且已经按照某种自定义顺序排列。  
请重新排列（permutation）字符串 `s` 中的字符，使其遵循 `order` 中的排序规则。具体来说，如果字符 `x` 在 `order` 中出现在字符 `y` 之前，则在重新排列后的字符串中 `x` 也必须出现在 `y` 之前。  
返回任意满足该性质的 `s` 的排列。

**示例 1**  
```
Input: order = "cba", s = "abcd"
Output: "cbad"
Explanation: 字符 "a"、"b"、"c" 在 `order` 中出现，故它们在结果中的顺序应为 "c"、"b"、"a"。  
由于字符 "d" 未出现在 `order` 中，它可以出现在返回字符串的任意位置。比如 "dcba"、"cdba"、"cbda" 等都是合法答案。
```

**示例 2**  
```
Input: order = "bcafg", s = "abcd"
Output: "bcad"
Explanation: `order` 中的字符 "b"、"c"、"a" 决定了 `s` 中对应字符的相对顺序，应按照 "b"、"c"、"a" 排列。  
字符 "d" 未在 `order` 中出现，其位置不受限制。输出 "bcad" 符合该规则，其他如 "dbca"、"bcda" 只要保持 "b"、"c"、"a" 的相对顺序同样有效。
```

**约束条件**  
- `1 <= order.length <= 26`  
- `1 <= s.length <= 200`  
- `order` 和 `s` 仅由小写英文字母组成。  
- `order` 中的所有字符互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 `order` 里出现的字符一个一个地从 `s` 中挑出来**，按照 `order` 的顺序依次放进答案，然后把 `s` 中剩下的字符（即不在 `order` 里的字符）随意拼在后面。

- **使用的数据结构**：  
  - `list`（列表）用来保存答案字符，像装东西的篮子。  
  - 每次遍历 `s` 时，用 **线性扫描**（一次遍历）找出所有等于当前 `order` 中字符的字符，就像在一排排商品中找指定的商品。

- **为什么正确**：  
  - 题目要求：如果字符 `x` 在 `order` 中排在字符 `y` 前面，那么在最终字符串里 `x` 也必须出现在 `y` 前面。我们正是把 `order` 的字符按出现顺序全部取出来放进答案，这保证了相对顺序一定满足要求。  
  - 对于不在 `order` 里的字符，题目说它们的位置“随意”，所以直接把它们接在答案后面即可。

- **时间/空间复杂度**（大白话解释）  
  - 时间复杂度：外层遍历 `order`（最多 26 次），内层每次都要遍历完整的 `s`（最多 200 次），所以最坏情况下要做 26 × 200 ≈ **5200 次**字符比较，用 **O(|order|·|s|)** 表示，记作 **O(m·n)**（m 是 `order` 长度，n 是 `s` 长度），意思是“随两个字符串长度的乘积增长”。  
  - 空间复杂度：只用了一个额外的答案列表，长度等于 `s`，所以是 **O(n)**，即“和 `s` 长度成正比”。

#### 代码（Python）

```python
def customSortString_bruteforce(order: str, s: str) -> str:
    # 用来保存最终答案的字符列表
    ans = []

    # 依次处理 order 中的每个字符
    for ch in order:
        # 再遍历一遍 s，找出所有等于 ch 的字符
        for c in s:
            if c == ch:
                ans.append(c)          # 把它加入答案

    # 处理那些不在 order 中的字符
    for c in s:
        if c not in order:              # 只要不在 order 里，就直接加到末尾
            ans.append(c)

    # 把列表拼成字符串返回
    return ''.join(ans)
```

#### 复杂度

- **时间复杂度**：`O(|order|·|s|)` —— 需要把 `order` 的每个字符和 `s` 的每个字符都比较一次。  
- **空间复杂度**：`O(|s|)` —— 额外使用了一个与 `s` 等长的列表来存放结果。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历整个 `s`** 来找对应字符，这导致时间是 `|order|·|s|`。我们可以把 “`order` 中字符的优先级” **一次性记下来**，以后只需要 **O(1)** 的时间就能判断两个字符的相对顺序。

实现思路：

1. **构造哈希表**（Python 中的 `dict`），把 `order` 中每个字符映射到它的“出现顺序”。  
   - 类比：哈希表就像一本**字典**，`key` 是字符，`value` 是它在 `order` 中的下标（位置），相当于“页码”。查一次字典，立刻知道这个字符应该排第几位。

2. **对 `s` 进行排序**，排序时使用自定义比较键：  
   - 如果字符在 `order` 中，就返回它在哈希表里的下标。  
   - 如果字符不在 `order` 中，就返回一个很大的数（如 `len(order)`），保证它们排在所有有序字符的后面，且相对顺序保持原样（因为 Python 的 `sorted` 是稳定的）。

3. 返回排好序的字符串。

这样我们只需要一次遍历构造哈希表（`O(|order|)`），一次遍历 `s` 并排序（`O(|s| log |s|)`），总体时间是 `O(|s| log |s|)`，空间只需要哈希表和结果字符串，都是 `O(|order| + |s|)`。

#### 代码（Python）

```python
def customSortString(order: str, s: str) -> str:
    # 1️⃣ 把 order 中每个字符的出现顺序记在哈希表里
    #   例如 order = "cba" => {'c':0, 'b':1, 'a':2}
    rank = {ch: i for i, ch in enumerate(order)}

    # 2️⃣ 对 s 进行排序，排序键（key）就是字符的 rank
    #   - 如果字符在 order 中，就取对应的下标
    #   - 否则返回一个很大的数（这里用 len(order)），让它排在后面
    #   Python 的 sorted 是稳定的，意味着相同键的字符会保持原来的相对顺序
    sorted_chars = sorted(s, key=lambda ch: rank.get(ch, len(order)))

    # 3️⃣ 把排好序的字符列表拼成字符串返回
    return ''.join(sorted_chars)
```

#### 复杂度

- **时间复杂度**：`O(|s| log |s|)` —— 主要耗时在对 `s` 排序，排序的时间复杂度是 `n log n`（n = |s|）。相比暴力解的 `|order|·|s|`，当 `s` 长度比较大时，`log n` 增长得远比线性乘积慢。  
- **空间复杂度**：`O(|order| + |s|)` —— 需要存哈希表（大小至多 26）和排序产生的临时列表（长度等于 `s`），这两部分都是线性空间。

---

## 心得

- **核心技巧**：**哈希表 + 自定义排序键**，把字符的相对顺序提前记下来，后面只用一次排序就能完成。
- **适用的题型**  
  1. “自定义字母顺序” 类的字符串排序（如本题）。  
  2. 根据出现频率或优先级对元素重新排列（如“按出现频率排序字符”）。  
  3. 多维度排序时需要把某一维度映射为数值（如“按自定义等级排序任务”）。
- **一句话总结**：**先把顺序写进字典，再让排序“读懂”这个字典**。

---

## 反思

- **第一反应**：直接把 `order` 的字符一个一个在 `s` 里找，想到“遍历两遍”。  
- **最容易踩的坑**  
  - **忘记保持不在 `order` 中字符的相对顺序**：如果直接把它们全部追加到答案末尾，可能会打乱它们原来的顺序。使用 Python 稳定的 `sorted` 或者在暴力解里保持原序即可。  
  - **哈希表查不到的字符处理**：一定要给一个足够大的默认值，否则会把不在 `order` 中的字符排到前面。  
  - **字符全部不在 `order`**：此时排序键全是默认值，返回的仍然是原字符串（因为 `sorted` 稳定），要保证代码不会出错。  
- **下次类似题的第一步**：**把“优先级”先映射成数值（哈希表）**，再用这个数值去排序或计数。这样可以把“顺序判断”从每次比较的 O(1) 提升到整体 O(n log n) 或更好。