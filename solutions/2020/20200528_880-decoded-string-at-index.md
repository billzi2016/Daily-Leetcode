# #880. **索引处的解码字符串** / Decoded String at Index

> 难度：中等 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/decoded-string-at-index/)

---

## 题目（英文原版）

**Description**

You are given an encoded string s. To decode the string to a tape, the encoded string is read one character at a time and the following steps are taken:
Given an integer k, return the kth letter (1-indexed) in the decoded string.

**Examples**

**Example 1:**

```
Input: s = "leet2code3", k = 10
Output: "o"
Explanation: The decoded string is "leetleetcodeleetleetcodeleetleetcode".
The 10th letter in the string is "o".
```

**Example 2:**

```
Input: s = "ha22", k = 5
Output: "h"
Explanation: The decoded string is "hahahaha".
The 5th letter is "h".
```

**Example 3:**

```
Input: s = "a2345678999999999999999", k = 1
Output: "a"
Explanation: The decoded string is "a" repeated 8301530446056247680 times.
The 1st letter is "a".
```

**Constraints**

- 2 <= s.length <= 100
- s consists of lowercase English letters and digits 2 through 9.
- s starts with a letter.
- 1 <= k <= 109
- It is guaranteed that k is less than or equal to the length of the decoded string.
- The decoded string is guaranteed to have less than 263 letters.

---

## 题目（中文翻译）

给定一个编码字符串 `s`。要将其解码为磁带（tape），需要一次读取一个字符并按以下步骤进行：

- 如果读取到的是字母，则将其直接写入磁带。
- 如果读取到的是数字 `d`（`2` 到 `9`），则把当前磁带的内容复制 `d‑1` 次，形成新的磁带。

给定整数 `k`，返回解码后字符串中第 `k` 个字母（**1‑indexed**，即从 1 开始计数）。

---

### 示例

**示例 1**

```
Input: s = "leet2code3", k = 10
Output: "o"
Explanation: 解码后的字符串为 "leetleetcodeleetleetcodeleetleetcode"。第 10 个字符是 "o"。
```

**示例 2**

```
Input: s = "ha22", k = 5
Output: "h"
Explanation: 解码后的字符串为 "hahahaha"。第 5 个字符是 "h"。
```

**示例 3**

```
Input: s = "a2345678999999999999999", k = 1
Output: "a"
Explanation: 解码后的字符串是字符 "a" 重复 8301530446056247680 次。第 1 个字符是 "a"。
```

---

### 约束条件

- `2 <= s.length <= 100`
- `s` 仅由小写英文字母和数字 `2` 到 `9` 组成。
- `s` 以字母开头。
- `1 <= k <= 10^9`
- 保证 `k` 小于等于解码后字符串的长度。
- 解码后字符串的长度保证小于 `2^63`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把整个解码过程完整地跑一遍**，得到完整的字符串后再取第 `k` 个字符。

- **用到的数据结构**：  
  - `list`（或者 `str`）来保存已经展开的字符序列。  
  - `int` 用来记录当前已经展开了多少字符。  

- **生活化类比**：  
  把编码字符串想象成一本**自助复印机**的说明书。  
  - 看到字母，就直接把这张纸放进复印机里，纸面内容保持不变。  
  - 看到数字 `d`，就把已经复印好的 **所有纸** 再复印 `d‑1` 份，放到后面。  
  最后我们把所有纸排成一条长长的卷轴，直接读第 `k` 张纸上的字符。

- **为什么正确**：  
  这种做法严格按照题目给出的“逐字符读取、遇字母直接写、遇数字重复前面内容”的规则来构造解码串，所以得到的字符串必然和题目要求的完全一致。

- **复杂度分析（大白话）**：  
  - **时间**：每次遇到数字都要把已经得到的全部字符复制 `d‑1` 次。假设最终解码串的长度是 `L`，我们实际上要把每个字符 **写进结果里一次**，所以时间是 **O(L)**。但题目允许的 `L` 可能非常大（上例 10^19），在现实机器上根本写不完。  
  - **空间**：我们要把完整的解码串存下来，需要 **O(L)** 的额外内存，同样在大输入下会爆内存。

> 简单来说，暴力解法在概念上最容易理解，但在数据量稍大时就会“卡死”，因为它真的把巨大的字符串全部生成了。

#### 代码（Python）

```python
def decodeAtIndex_bruteforce(s: str, k: int) -> str:
    # 用列表收集已经展开的字符，列表拼接速度比直接字符串好
    decoded = []                     # 相当于“纸卷”

    for ch in s:
        if ch.isdigit():             # 遇到数字，要把已经有的内容重复 d-1 次
            repeat = int(ch) - 1
            # 把已展开的部分复制 repeat 次并追加到末尾
            decoded.extend(decoded * repeat)
        else:                         # 遇到字母，直接加入
            decoded.append(ch)

        # 如果已经够长了，就可以直接返回第 k 个字符
        if len(decoded) >= k:
            return decoded[k - 1]    # 1-indexed → 0-indexed

    # 按题意这里一定能返回，不会走到下面
    raise ValueError("k 超出了解码后字符串的长度")
```

> **关键行中文注释** 已在代码中标出。

#### 复杂度

- **时间复杂度**：`O(L)`，其中 `L` 是解码后字符串的实际长度。  
  > 大白话：我们要把每个字符都写进去一次，字符越多，耗时越长。

- **空间复杂度**：`O(L)`，需要把完整的解码串存下来。  
  > 大白话：如果解码串有 1000 万个字符，就要占用大约 10 MB 的内存；如果有 10^12 个字符，普通电脑根本装不下。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“把整个解码串全部展开”**，这一步既耗时又耗内存。  
其实我们只需要 **第 k 个字符**，不需要完整的字符串。  

**关键观察**：

1. **正向遍历可以算出每一步的总长度**  
   - 维护一个变量 `size`，它表示遍历到当前位置时，解码后字符串的长度。  
   - 遇到字母 `c`，`size += 1`（长度加 1）。  
   - 遇到数字 `d`，`size *= d`（把已有的全部复制 `d` 份，长度乘以 `d`）。  

2. **从后往前倒着找**  
   - 当我们知道了最终的总长度 `size`（一定 ≥ k），可以从字符串的 **最后一个字符** 开始倒着思考：  
     - 如果当前字符是数字 `d`，说明在它之前的那段子串被 **重复了 d 次**。  
       - 实际上，第 `k` 位一定落在这段子串的 **某一次复制** 中。  
       - 把 `k` 映射回原始段的下标：`k = k % (size // d)`（取余），因为每 `size//d` 长度是一轮完整的原始段。  
       - 同时把 `size` 缩小回 `size // d`，继续向前看。  
     - 如果当前字符是字母 `c`，且 `k == size`（恰好指向这位），那答案就是 `c`。  
       - 否则把 `size -= 1`（相当于把这位字母“去掉”，继续向前找）。  

3. **不需要额外的栈**  
   - 只用两个整数 `size`、`k`，空间是 `O(1)`。

> **类比**：把解码过程想成一条不断伸长的绳子。我们先把绳子拉到最终长度，然后从绳子最右端往左“收回”。每次遇到“复制”节点，就把绳子折回原来的长度；每次遇到普通字符，就检查手指指的是否正好是这根绳子上的字母。

#### 代码（Python）

```python
def decodeAtIndex(s: str, k: int) -> str:
    size = 0                       # 当前已知的解码后长度

    # 1️⃣ 正向遍历，算出完整的长度（可能非常大，但仍在 64 位整数范围内）
    for ch in s:
        if ch.isdigit():
            size *= int(ch)       # 复制整段，长度乘以数字
        else:
            size += 1              # 加一个字母，长度加一

    # 2️⃣ 逆向遍历，寻找第 k 位对应的字符
    for ch in reversed(s):
        k %= size                   # 把 k 映射到当前长度范围内
        # 当 k 为 0 且当前字符是字母时，说明答案就在这里
        if k == 0 and ch.isalpha():
            return ch

        if ch.isdigit():
            size //= int(ch)       # “收回”复制的效果，长度恢复到复制前
        else:
            size -= 1               # 去掉这个字母的长度

    # 按题目保证一定能返回，不会走到这里
    raise ValueError("无法找到第 k 位字符")
```

> **关键行中文注释** 已在代码中标出。

#### 复杂度

- **时间复杂度**：`O(|s|)`，只遍历两遍字符串。  
  > 大白话：字符串长度只有 100，几乎瞬间完成。

- **空间复杂度**：`O(1)`，只用常数个整数变量。  
  > 大白话：不管解码后有多长，程序占用的内存几乎不变。

---

## 心得

- **核心技巧**：**从后往前逆向定位**。先算出整体长度，再利用取模把查询“压缩”回原始段落。  
- **适用的题型**：  
  1. “**重复字符串**”类问题（如 LeetCode 880. Decoded String at Index）。  
  2. “**压缩/展开**”的查询类问题（如“压缩字符串的第 k 位字符”）。  
  3. “**递归/迭代长度映射**”的题目（如“第 K 大的子序列”需要倒推）。  
- **一句话总结**：**先算长度，再倒着走，取模把位置映回最原始的字符**。

---

## 反思

- **第一反应**：把整个字符串全部解码出来，然后直接取第 `k` 位。  
- **最容易踩的坑**：  
  - **整数溢出**：解码后长度可能远超 32 位整数，需要使用 64 位（Python 整数自动大数）。  
  - **取模为 0 的情况**：`k % size == 0` 时要特别判断，因为此时实际对应的是当前段的最后一个字符。  
  - **忘记把 `size` 在遇到数字时恢复**（`size //= d`），会导致循环不收敛。  
- **下次遇到同类题**：**先把“总长度”算出来，再逆向用取模把目标位置一步步映射回原始字符**，这一步往往是突破口。