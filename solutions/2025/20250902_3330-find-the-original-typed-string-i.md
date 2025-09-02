# #3330. 寻找原始键入字符串 I / Find the Original Typed String I

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/find-the-original-typed-string-i/)

---

## 题目（英文原版）

**Description**

Alice is attempting to type a specific string on her computer. However, she tends to be clumsy and may press a key for too long, resulting in a character being typed multiple times.
Although Alice tried to focus on her typing, she is aware that she may still have done this at most once.
You are given a string word, which represents the final output displayed on Alice's screen.
Return the total number of possible original strings that Alice might have intended to type.

**Examples**

**Example 1:**

```
Input: word = "abbcccc"
Output: 5
Explanation:
The possible strings are: "abbcccc" , "abbccc" , "abbcc" , "abbc" , and "abcccc" .
```

**Example 2:**

```
Input: word = "abcd"
Output: 1
Explanation:
The only possible string is "abcd" .
```

**Example 3:**

```
Input: word = "aaaa"
Output: 4
```

**Constraints**

- 1 <= word.length <= 100
- word consists only of lowercase English letters.

---

## 题目（中文翻译）

Alice 正在尝试在电脑上键入一个特定的字符串。然而她有点笨拙，可能会把某个键按得太久，导致同一个字符（character）被输入多次。  
虽然 Alice 已经尽力集中注意力，但她知道最多只能出现 **一次** 这种情况。  

现在给定一个字符串 `word`，它表示 Alice 最终在屏幕上看到的输出。请返回 Alice 可能本意想要键入的原始字符串（original string）的数量。

---

### 示例

#### 示例 1  
**输入**  
```
word = "abbcccc"
```  
**输出**  
```
5
```  
**解释**  
可能的原始字符串有：`"abbcccc"`、`"abbccc"`、`"abbcc"`、`"abbc"`、以及 `"abcccc"`。

#### 示例 2  
**输入**  
```
word = "abcd"
```  
**输出**  
```
1
```  
**解释**  
唯一可能的原始字符串是 `"abcd"`。

#### 示例 3  
**输入**  
```
word = "aaaa"
```  
**输出**  
```
4
```  

---

### 约束条件
- `1 <= word.length <= 100`
- `word` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **每一段相同字符** 看成一个“候选”位置，尝试把它删掉若干个字符（至少保留一个），把所有可能的结果收集起来去重。

- **数据结构**：我们可以把最终出现的字符串 `word` 按照字符相同且相邻的块划分成若干段，例如 `"abbcccc"` → `["a", "bb", "cccc"]`。  
  这里的 **块** 就像一本字典的条目，条目名是字符本身，条目内容是这段字符出现的次数。
- **为什么正确**：题目说 Alice 最多只会在 **一段** 上多打了字符，所以我们只需要在 **一段**（或者不动）上进行“删减”。遍历所有段、遍历所有可能的删减长度，就能产生所有合法的原始字符串。
- **复杂度**：  
  - 对每一段的长度 `len`，我们要尝试 `len` 种删减方式（保留 1~len 个字符），因此最坏情况是对每段都这样做，整体时间大约是 `O(n²)`（因为每次生成新字符串都要遍历整段字符）。  
  - 需要一个 `set` 保存去重的字符串，空间同样是 `O(n²)`（最坏情况下会产生 `∑len = n` 条不同字符串，每条长度 `≈ n`）。

> **大白话**：`O(n²)` 可以想象成“如果你有 10 本书，每本书都要翻 10 次”，总操作次数是 100（10×10），随 `n` 增大，操作次数会像正方形一样快速增长。

#### 代码（Python）

```python
def possible_originals_bruteforce(word: str) -> int:
    """
    暴力枚举所有可能的原始字符串并去重，返回其数量。
    """
    n = len(word)
    # 先把 word 按照相同字符的连续块分割
    blocks = []          # 每个元素是 (字符, 块的长度)
    i = 0
    while i < n:
        j = i
        while j < n and word[j] == word[i]:
            j += 1
        blocks.append((word[i], j - i))
        i = j

    candidates = set()   # 用集合自动去重

    # ① 不进行任何删减的情况
    candidates.add(word)

    # ② 选取一段进行删减
    for idx, (ch, length) in enumerate(blocks):
        # 只能保留 1~length 个该字符
        for keep in range(1, length + 1):
            # 重新拼接字符串
            new_parts = []
            for k, (c, l) in enumerate(blocks):
                if k == idx:               # 选中的那段
                    new_parts.append(c * keep)
                else:
                    new_parts.append(c * l)   # 其他段保持不变
            candidates.add(''.join(new_parts))

    return len(candidates)
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：对每个块尝试 `len` 种删减方式，每次都要把所有块重新拼接一次，最坏情况相当于 `n` 次 `O(n)` 的拼接。

- **空间复杂度**：`O(n²)`  
  解释：可能产生 `≈ n` 条不同的字符串，每条长度 `≈ n`，所以整体占用的内存随 `n` 的平方增长。

---

### 2. 最优解

#### 思路  
从暴力解可以看到，**真正影响答案的只有每段的长度**，而不是具体的字符。我们只需要统计每段有多少字符，进而直接算出可以产生多少不同的原始字符串，而不必真的把它们全部列举出来。

1. **找出所有连续相同字符的块**，记录每块的长度 `len_i`。  
   这一步只需要一次线性扫描，类似于在路上走，遇到不同的颜色就记一次。

2. 对于长度为 `len_i` 的块，**如果 Alice 没有出错**，原始字符串就和最终字符串完全相同，算作一种可能。  
   如果 Alice 在这块上多敲了字符，那么原始字符串可以是该块的任意 **“保留 1~len_i 个字符”** 的情况。  
   - 长度为 1 的块删不掉（只能保留 1），所以不会产生新字符串。  
   - 长度为 `len_i > 1` 的块可以产生 `len_i - 1` 种 **比最终字符串更短** 的新字符串（因为保留 1、2、…、`len_i-1` 都是不同的）。

3. **把所有块的贡献相加**，再加上 “**全都不删**” 的那一种，即可得到答案：

\[
\text{answer} = 1 + \sum_{i \,:\, len_i > 1} (len_i - 1)
\]

这正是 **每块可以产生的新字符串数量**（不包括不删的情况）之和，再加上“一点也不删”的基准。

> **类比**：把每块看成一根绳子，绳子长度为 `len_i`。如果 Alice 没出错，就把所有绳子原封不动地摆好；如果在第 `i` 根绳子上多打了结，最多只能把这根绳子剪短到任意正整数长度（最短 1），而其他绳子保持原长。我们只需要统计每根绳子能剪多少种长度，然后把所有可能相加。

#### 代码（Python）

```python
def possible_originals(word: str) -> int:
    """
    O(n) 时间、O(1) 额外空间求解答案。
    """
    n = len(word)
    ans = 1          # “全都不删”的一种情况
    i = 0
    while i < n:
        j = i
        # 找到当前字符的连续块长度
        while j < n and word[j] == word[i]:
            j += 1
        block_len = j - i
        if block_len > 1:
            # 这块可以产生 (block_len - 1) 种更短的字符串
            ans += block_len - 1
        i = j
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只需要一次遍历字符串，`n` 是字符串长度。相当于“走一遍路就知道所有颜色的块”。

- **空间复杂度**：`O(1)`  
  只用常数个变量（计数器、指针），不随 `n` 增长。

> 与暴力解相比，时间从 “平方级” 降到了 “线性级”，空间也从 “平方级” 降到了 “常数级”。这在 `word.length ≤ 100` 时已经非常快，但更重要的是它展示了 **把问题抽象为统计而不是枚举** 的思路。

---

## 心得

- **核心技巧**：**把“最多一次的错误”转化为“只在一段上可以删减”，并用**块长度**直接计数**。**  
- **适用的题型**：  
  1. 只允许一次操作（如一次翻转、一次删除）的问题。  
  2. 需要统计不同结果数量而不是列举全部的题目（例如 “最多一次翻转得到多少不同的二进制字符串”）。  
  3. 连续相同元素分块统计的题目（如 “删除一次连续子数组后能得到多少不同数组”）。
- **一句话总结**：**把每段的“可删减次数”相加，再加上“不删”的基准，即是答案。**

---

## 反思

- **第一反应**：看到“最多一次”会想枚举所有可能的出错位置，然后把结果去重。  
- **最容易踩的坑**：  
  - 忘记 **“不删”** 本身也是一种合法情况，导致答案少 1。  
  - 对长度为 1 的块错误地算 `len-1 = 0` 仍算作一次删减，产生重复计数。  
  - 没考虑到 **“最多一次”**，而是把每段都当成可以删减，导致答案过大。
- **下次类似题**：第一步先 **把问题抽象成“块”或“区间”**，思考每个块能贡献多少不同的结果，再判断是否需要 **枚举** 或 **直接计数**。这样往往能直接得到 O(n) 的解法。