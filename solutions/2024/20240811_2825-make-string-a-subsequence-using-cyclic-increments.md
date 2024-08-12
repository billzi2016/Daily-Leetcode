# #2825. **使用循环递增使字符串成为子序列** / Make String a Subsequence Using Cyclic Increments

> 难度：中等 · 标签：Two Pointers、String · [LeetCode 链接](https://leetcode.com/problems/make-string-a-subsequence-using-cyclic-increments/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed strings str1 and str2.
In an operation, you select a set of indices in str1, and for each index i in the set, increment str1[i] to the next character cyclically. That is 'a' becomes 'b', 'b' becomes 'c', and so on, and 'z' becomes 'a'.
Return true if it is possible to make str2 a subsequence of str1 by performing the operation at most once, and false otherwise.
Note: A subsequence of a string is a new string that is formed from the original string by deleting some (possibly none) of the characters without disturbing the relative positions of the remaining characters.

**Examples**

**Example 1:**

```
Input: str1 = "abc", str2 = "ad"
Output: true
Explanation: Select index 2 in str1.
Increment str1[2] to become 'd'. 
Hence, str1 becomes "abd" and str2 is now a subsequence. Therefore, true is returned.
```

**Example 2:**

```
Input: str1 = "zc", str2 = "ad"
Output: true
Explanation: Select indices 0 and 1 in str1. 
Increment str1[0] to become 'a'. 
Increment str1[1] to become 'd'. 
Hence, str1 becomes "ad" and str2 is now a subsequence. Therefore, true is returned.
```

**Example 3:**

```
Input: str1 = "ab", str2 = "d"
Output: false
Explanation: In this example, it can be shown that it is impossible to make str2 a subsequence of str1 using the operation at most once. 
Therefore, false is returned.
```

**Constraints**

- 1 <= str1.length <= 105
- 1 <= str2.length <= 105
- str1 and str2 consist of only lowercase English letters.

---

## 题目（中文翻译）

给定两个下标从 0 开始的字符串 `str1` 和 `str2`。  
一次操作中，你可以选择 `str1` 中的一组下标，对每个选中的下标 `i` 将 `str1[i]` 循环递增到下一个字符。即 `'a'` 变为 `'b'`，`'b'` 变为 `'c'`，依此类推，`'z'` 变为 `'a'`。  
如果至多执行一次该操作后能够使 `str2` 成为 `str1` 的子序列（subsequence），返回 `true`，否则返回 `false`。

> **注意**：字符串的子序列（subsequence）是指通过删除原字符串中的若干（也可能不删除）字符而得到的新字符串，要求剩余字符的相对顺序保持不变。

### 示例

#### 示例 1
```
Input: str1 = "abc", str2 = "ad"
Output: true
Explanation: 选中 `str1` 的下标 2。  
将 `str1[2]` 递增得到 `'d'`。  
于是 `str1` 变为 `"abd"`，此时 `str2` 已是其子序列，返回 true。
```

#### 示例 2
```
Input: str1 = "zc", str2 = "ad"
Output: true
Explanation: 同时选中下标 0 和 1。  
`str1[0]` 递增为 `'a'`，`str1[1]` 递增为 `'d'`。  
得到的 `str1` 为 `"ad"`，`str2` 成为其子序列，返回 true。
```

#### 示例 3
```
Input: str1 = "ab", str2 = "d"
Output: false
Explanation: 在至多一次操作的限制下，无法使 `str2` 成为 `str1` 的子序列，故返回 false。
```

### 约束条件
- $1 \leq \text{str1.length} \leq 10^5$
- $1 \leq \text{str2.length} \leq 10^5$
- `str1` 和 `str2` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **所有可能的增字符集合** 都枚举一遍，然后判断增完之后的 `str1` 能否包含 `str2` 作为子序列。

- **增字符集合**：把 `str1` 中的若干下标挑出来，分别把这些位置的字符向后循环一次（`a→b, …, z→a`），其余位置保持不变。  
  可以把它想象成“在字典里查找单词”，只不过这里的 **字典** 是所有 **2ⁿ** 种把字符“往后推一位”或“不动” 的组合（`n = len(str1)`），每一种组合对应一本“改造后”的书。

- **子序列检查**：把改造后的 `str1` 当成原始字符串，按照常规的双指针法检查 `str2` 是否是它的子序列。  

**为什么这个方法一定能得到正确答案**  
因为我们穷举了**所有**可能的增字符方式，只要有一种方式可以让 `str2` 成为子序列，就一定会在枚举过程中被发现。

**时间/空间复杂度**  
- 枚举所有子集需要 `2ⁿ` 种可能，`n` 最多 `10⁵`，所以时间复杂度是 **指数级**：`O(2^n)`，在实际中根本不可接受。  
- 每次枚举都要复制一遍 `str1`（长度 `n`），所以空间复杂度是 `O(n)`（用于存放临时改造后的字符串）。

> **大白话**：  
> `O(2^n)` 就好比“把所有可能的钥匙都试一遍”。当钥匙数量是 30 把时还能接受，钥匙是 100,000 把时就根本不可能。

#### 代码（Python）  

```python
from itertools import product

def brute_force(str1: str, str2: str) -> bool:
    n = len(str1)

    # 生成所有 0/1 组合，0 表示不增，1 表示增
    for mask in product([0, 1], repeat=n):
        # 根据 mask 生成改造后的字符串
        transformed = []
        for i, inc in enumerate(mask):
            ch = str1[i]
            if inc:                                   # 需要增字符
                # 循环增 1：'z' → 'a'
                ch = chr(((ord(ch) - ord('a') + 1) % 26) + ord('a'))
            transformed.append(ch)
        transformed = ''.join(transformed)

        # 检查 str2 是否是 transformed 的子序列（双指针）
        i = j = 0
        while i < len(transformed) and j < len(str2):
            if transformed[i] == str2[j]:
                j += 1
            i += 1
        if j == len(str2):          # 全部匹配完毕
            return True
    return False
```

> 这段代码只能在 **极小** 的测试数据上跑通，主要是用来说明最暴力的思路。

#### 复杂度  

- 时间复杂度：`O(2^n * n)` —— 每一种增字符组合都要遍历整个 `str1`（`n`），而组合数是 `2^n`。  
- 空间复杂度：`O(n)` —— 用于存放一次改造后的字符串。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正需要判断的只是每个字符是否可以“直接匹配”或“经过一次循环增后匹配”。**  
我们不必真的去枚举增哪些字符，只要在遍历 `str1` 的过程中，**看到一个字符能够满足这两种情况之一，就可以把它“用掉”匹配 `str2` 中的当前字符**。  

**瓶颈**  
暴力解的瓶颈在于 **枚举所有子集**，这一步根本不需要做。我们只关心匹配的可行性，而匹配本身是**单调递增**的：匹配 `str2` 的第 `j` 个字符必须使用 `str1` 中**更靠左**的下标。

**关键观察**  

- 对于 `str1[i]`，只有两种“可接受”的状态：  
  1. 与 `str2[j]` 完全相同 (`str1[i] == str2[j]`)  
  2. 经过一次循环增后相同 (`next(str1[i]) == str2[j]`)  

- 如果上述任意一种成立，就可以把 `str1[i]` 选入子序列（无论是增还是不增都只用一次），并让指针 `j` 前进到下一个字符。  
- 否则只能把 `str1[i]` 跳过，继续检查后面的字符。  

这正好对应 **双指针** 的经典子序列判定，只是匹配条件稍微宽松一点。

**算法步骤**  

1. 初始化两个指针 `i = 0`（遍历 `str1`）和 `j = 0`（遍历 `str2`）。  
2. 当 `i < len(str1)` 且 `j < len(str2)` 时：  
   - 计算 `next_char = chr(((ord(str1[i]) - 97 + 1) % 26) + 97)`（循环增 1）。  
   - 如果 `str1[i] == str2[j]` **或** `next_char == str2[j]`：  
     - 匹配成功，`j += 1`（`str2` 向前走一步）。  
   - `i += 1`（不论匹配成功与否，都把 `str1` 的指针右移）。  
3. 循环结束后，检查 `j` 是否已经等于 `len(str2)`：  
   - 若相等，说明所有字符都找到了匹配位置，返回 `True`。  
   - 否则返回 `False`。  

**为什么贪心一定对**  

- 我们总是把 **最左边** 能匹配的字符用掉。  
- 若把它跳过，后面的字符一定更靠右，**不可能帮助我们匹配更早的 `str2`**，因为子序列要求顺序不变。  
- 因此，**提前匹配**不会导致以后找不到匹配的情况，故贪心是最优的。

#### 代码（Python）  

```python
def can_make_subsequence(str1: str, str2: str) -> bool:
    """
    判断在至多一次“循环增 1”操作后，str2 是否可以成为 str1 的子序列。
    思路：双指针贪心匹配，每个字符只要本身或循环增后等于目标字符即可匹配。
    """
    i, j = 0, 0
    n, m = len(str1), len(str2)

    while i < n and j < m:
        # 循环增 1 的字符
        nxt = chr(((ord(str1[i]) - ord('a') + 1) % 26) + ord('a'))

        # 若当前字符本身或增后能匹配 str2[j]，则使用它匹配
        if str1[i] == str2[j] or nxt == str2[j]:
            j += 1               # str2 向前走一步
        # 不管匹配成功与否，str1 的指针都要右移
        i += 1

    # j 走到 str2 末尾说明全部匹配成功
    return j == m
```

> 代码里每一行都加了中文注释，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n + m)`，其中 `n = len(str1)`，`m = len(str2)`。  
  - 我们只遍历了一遍 `str1`（最多 `10⁵` 次），每次只做常数时间的字符比较。  
  - 与暴力解的 `O(2^n)` 相比，**快了指数级**。  
- **空间复杂度**：`O(1)`，只用了几个整数指针和一个临时字符变量，和输入规模无关。

---

## 心得  

- **核心技巧**：**宽松匹配的双指针** —— 在子序列判断的基础上，允许每个字符“自行增一次”。  
- **适用的题型**（类似思路）  
  1. “**可修改一次的子序列**” 例如：允许把一次字符替换为任意字符后再检查子序列。  
  2. “**循环增/减一次的匹配**” 如 LeetCode “Make Array Strictly Increasing”。  
  3. “**容错匹配**” 如允许最多 `k` 次错误（Edit distance ≤ k） 的子序列检查。  

- **一句话总结解题钥匙**：  
  “只要把**匹配条件**放宽到“原字符或一次循环增后字符”，就可以用**一次遍历的贪心**直接判断是否能成为子序列。”

---

## 反思  

- **第一反应**：枚举所有增字符的子集，然后逐个检查子序列——这是一种“全搜”的自然想法。  
- **最容易踩的坑**  
  - 忘记 **循环增** 的特殊情况：`'z'` 增后变成 `'a'`，需要用模 26 运算实现。  
  - 误以为可以“先增后匹配再回退”，其实每个字符只能增一次，不能在匹配后再改动。  
  - 边界条件：`str2` 长度大于 `str1` 时直接返回 `False`（遍历自然会得到）。  

- **下次遇到同类题**，第一步应该想到：  
  “**把匹配规则抽象成‘可以接受的字符集合’**（本字符 ∪ 增后字符），然后用**双指针**在原串上贪心寻找匹配”。这样就能立刻跳过指数级搜索，得到线性时间解。