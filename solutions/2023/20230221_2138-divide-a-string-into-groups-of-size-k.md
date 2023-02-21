# #2138. 将字符串划分为大小为 k 的组 / Divide a String Into Groups of Size k

> 难度：简单 · 标签：String、Simulation · [LeetCode 链接](https://leetcode.com/problems/divide-a-string-into-groups-of-size-k/)

---

## 题目（英文原版）

**Description**

A string s can be partitioned into groups of size k using the following procedure:
Note that the partition is done so that after removing the fill character from the last group (if it exists) and concatenating all the groups in order, the resultant string should be s.
Given the string s, the size of each group k and the character fill, return a string array denoting the composition of every group s has been divided into, using the above procedure.

**Examples**

**Example 1:**

```
Input: s = "abcdefghi", k = 3, fill = "x"
Output: ["abc","def","ghi"]
Explanation:
The first 3 characters "abc" form the first group.
The next 3 characters "def" form the second group.
The last 3 characters "ghi" form the third group.
Since all groups can be completely filled by characters from the string, we do not need to use fill.
Thus, the groups formed are "abc", "def", and "ghi".
```

**Example 2:**

```
Input: s = "abcdefghij", k = 3, fill = "x"
Output: ["abc","def","ghi","jxx"]
Explanation:
Similar to the previous example, we are forming the first three groups "abc", "def", and "ghi".
For the last group, we can only use the character 'j' from the string. To complete this group, we add 'x' twice.
Thus, the 4 groups formed are "abc", "def", "ghi", and "jxx".
```

**Constraints**

- 1 <= s.length <= 100
- s consists of lowercase English letters only.
- 1 <= k <= 100
- fill is a lowercase English letter.

---

## 题目（中文翻译）

**描述**  
可以使用如下过程将字符串 `s` 划分为大小为 `k` 的组：  
从 `s` 的起始位置依次取 `k` 个字符构成一个组，直至字符串结束。若最后一个组不足 `k` 个字符，则使用填充字符 `fill`（fill character）补齐至 `k` 个字符。需要注意的是，划分后去掉最后一组的填充字符（如果存在），再按顺序拼接所有组，得到的结果应当与原字符串 `s` 完全相同。

给定字符串 `s`、每组的大小 `k` 与填充字符 `fill`，返回一个字符串数组，表示按照上述过程划分得到的所有组。

**示例 1**  
**输入**: `s = "abcdefghi"`, `k = 3`, `fill = "x"`  
**输出**: `["abc","def","ghi"]`  
**解释**:  
- 前 3 个字符 `"abc"` 组成第一组。  
- 接下来的 3 个字符 `"def"` 组成第二组。  
- 最后的 3 个字符 `"ghi"` 组成第三组。  
由于所有组都能被字符串中的字符完整填满，不需要使用填充字符 `fill`。因此得到的组为 `"abc"、"def"、"ghi"`。

**示例 2**  
**输入**: `s = "abcdefghij"`, `k = 3`, `fill = "x"`  
**输出**: `["abc","def","ghi","jxx"]`  
**解释**:  
- 前三组同前例分别为 `"abc"`、`"def"`、`"ghi"`。  
- 对于最后一组，只能从字符串中取到字符 `'j'`，不足 `k` 个字符。于是使用填充字符 `fill`（即 `'x'`）两次将其补齐，得到 `"jxx"`。  
- 最终得到的四组为 `"abc"`、`"def"`、`"ghi"`、`"jxx"`。

**约束条件**  
- `1 <= s.length <= 100`  
- `s` 仅由小写英文字母组成。  
- `1 <= k <= 100`  
- `fill` 为小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把原字符串从左到右每 k 个字符取出来**，形成一个子串（即一组）。如果最后剩下的字符不足 k 个，就在后面补上 `fill` 这个字符，使它恰好变成 k 长。  

- **用到的数据结构**：  
  - **列表（list）**：可以把每一次得到的子串存进去，最后一次性返回。列表就像我们平时用的“装盒子”的盒子，往里塞东西很方便。  
  - **字符串切片**：Python 的切片 `s[i:j]` 相当于在书里取第 `i` 页到第 `j-1` 页的内容，简单直观。  

- **为什么正确**：  
  - 我们严格按照题目要求的“每 k 个字符一组”来划分，除非最后一组不够 k。  
  - 对于最后一组，题目说要用 `fill` 把它补齐到 k 长，而我们正好在长度不足时追加相同数量的 `fill`。  

- **时间/空间复杂度**（大白话解释）：  
  - **时间复杂度**：我们要遍历一遍字符串的每个字符，最多 `len(s)` 次。每次取子串的操作在 Python 里是 **O(k)**（因为要复制 k 个字符），所以总的时间是 `O(len(s))`，对初学者可以把它想成“和字符串长度成正比”。  
  - **空间复杂度**：我们要把所有分好的子串保存下来，最终会占用和原字符串差不多的空间，也就是 `O(len(s))`，相当于“需要和原来一样多的盒子来装”。  

#### 代码（Python）

```python
def divideString(s: str, k: int, fill: str) -> list[str]:
    """
    暴力直觉解：逐段切片并在最后不足时填充 fill
    """
    res = []                       # 用列表保存每一组
    n = len(s)
    # step 1: 按照每 k 个字符切一次
    for i in range(0, n, k):       # i 依次是 0, k, 2k, ...
        group = s[i:i + k]         # 取出长度最多为 k 的子串
        # step 2: 如果这一组不足 k，就用 fill 补齐
        if len(group) < k:
            group += fill * (k - len(group))
        res.append(group)          # 把完整的组放进结果列表
    return res
```

#### 复杂度

- **时间复杂度**：`O(len(s))` — 需要看一遍字符串的每个字符，字符越多花的时间越多。  
- **空间复杂度**：`O(len(s))` — 结果列表里保存的所有子串加起来和原字符串差不多长，需要同等大小的空间。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的“瓶颈”并不在循环本身——我们已经只遍历了一遍字符串。  
所谓“最优”，在这里指的是 **写得更简洁、少写几行代码**，而时间/空间本质上已经是线性的，已经达到了最好的数量级。

优化思路：

1. **一次性算出需要多少组**  
   - 设 `n = len(s)`，每组 `k` 个字符。  
   - 需要的组数 = `ceil(n / k)`，即如果 `n` 不是 `k` 的整数倍，还要多一组来装剩余字符。  
   - 用整数运算 `groups = (n + k - 1) // k` 可以直接得到（把除法向上取整的技巧记住，类似把 `n` 补齐到最近的 `k` 的倍数）。

2. **先把字符串补齐到恰好 `groups * k` 长**  
   - 计算缺少的字符数 `missing = groups * k - n`。  
   - 把 `fill` 重复 `missing` 次拼到原字符串后面，得到一个 **长度恰好是 k 的倍数** 的新字符串 `t`。

3. **直接切片**  
   - 现在 `t` 的长度是 `k` 的整数倍，只要把它每 `k` 个字符切一次，就能得到所有组。  
   - 用列表推导式（list comprehension）一次性生成结果，代码更紧凑。

> **核心技巧解释**  
> - **向上取整**：`(a + b - 1) // b` 的含义是“把 `a` 除以 `b`，如果有余数就再加一个 `b`”。想象把 `a` 块糖果装进容量为 `b` 的盒子，哪怕最后一个盒子只装了几块，也要算一个完整的盒子。  
> - **列表推导式**：把“循环+收集”合在一行写完，就像在厨房一次性把所有切好的菜装进盘子。

#### 代码（Python）

```python
def divideString(s: str, k: int, fill: str) -> list[str]:
    """
    最优解：先补齐再一次性切片
    """
    n = len(s)
    # 计算需要的组数（向上取整）
    groups = (n + k - 1) // k          # 例：n=10,k=3 => groups=4
    # 需要补多少个 fill 才能恰好凑成 groups*k
    missing = groups * k - n
    # 把缺少的 fill 拼到字符串后面
    t = s + fill * missing
    # 一次性切出所有长度为 k 的子串
    return [t[i:i + k] for i in range(0, len(t), k)]
```

#### 复杂度

- **时间复杂度**：`O(len(s))` — 只遍历一次字符串（加上少量的乘法/除法），和暴力解一样快，但写法更简洁。  
- **空间复杂度**：`O(len(s))` — 需要存放补齐后的新字符串 `t`（长度最多比原来多 `k-1`），以及返回的列表，仍然和原字符串同阶。

---

## 心得

- **核心技巧**：向上取整求组数 + 先补齐再一次性切片。  
- **适用的题型**：  
  1. “把数组/字符串划分成固定长度的块” 类问题（如 LeetCode 1013 `Partition Array Into Three Parts With Minimum Cost` 的分块思路）。  
  2. “需要对不足的最后一段进行填充” 的场景（如二进制数据的块填充、网络协议的帧填充）。  
- **一句话总结解题钥匙**：先把长度补齐到整数倍，再统一切割。

---

## 反思

- **第一反应**：看到“每 k 个字符一组”，立刻想到用循环 `for i in range(0, len(s), k)`，然后处理最后一组不够的情况。  
- **最容易踩的坑**：  
  - 忘记在最后一组不足时补 `fill`，导致返回的最后一个子串长度不对。  
  - 直接用 `len(s) // k` 计算组数会把剩余的字符直接丢掉，需要向上取整。  
- **下次遇到同类题的第一步**：先算出“需要多少完整的块”，看是否需要补齐；如果需要，先补齐再统一切分，这样可以一次性完成所有块的生成。