# #1844. 将所有数字替换为字符 / Replace All Digits with Characters

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/replace-all-digits-with-characters/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed string s that has lowercase English letters in its even indices and digits in its odd indices.
You must perform an operation shift(c, x), where c is a character and x is a digit, that returns the xth character after c.
For every odd index i, you want to replace the digit s[i] with the result of the shift(s[i-1], s[i]) operation.
Return s after replacing all digits. It is guaranteed that shift(s[i-1], s[i]) will never exceed 'z'.
Note that shift(c, x) is not a preloaded function, but an operation to be implemented as part of the solution.

**Examples**

**Example 1:**

```
Input: s = "a1c1e1"
Output: "abcdef"
Explanation: The digits are replaced as follows:
- s[1] -> shift('a',1) = 'b'
- s[3] -> shift('c',1) = 'd'
- s[5] -> shift('e',1) = 'f'
```

**Example 2:**

```
Input: s = "a1b2c3d4e"
Output: "abbdcfdhe"
Explanation: The digits are replaced as follows:
- s[1] -> shift('a',1) = 'b'
- s[3] -> shift('b',2) = 'd'
- s[5] -> shift('c',3) = 'f'
- s[7] -> shift('d',4) = 'h'
```

**Constraints**

- 1 <= s.length <= 100
- s consists only of lowercase English letters and digits.
- shift(s[i-1], s[i]) <= 'z' for all odd indices i.

---

## 题目（中文翻译）

你得到一个 **0 索引** 的字符串 `s`，其中偶数下标位置的字符都是小写英文字母，奇数下标位置的字符都是数字。  
你需要实现一个操作 `shift(c, x)`，其中 `c` 是字符，`x` 是数字，返回字母表中 `c` 往后第 `x` 个字符。  

对于每个奇数下标 `i`，用 `shift(s[i‑1], s[i])` 的结果替换掉 `s[i]` 所对应的数字。  
返回替换所有数字后的字符串 `s`。题目保证 `shift(s[i‑1], s[i])` 的结果永远不会超过 `'z'`。  
注意，`shift(c, x)` 并不是预定义函数，而是需要你在解法中实现的操作。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**  
**示例 1:**  
```
Input: s = "a1c1e1"
Output: "abcdef"
Explanation: 数字的替换过程如下：
- s[1] -> shift('a',1) = 'b'
- s[3] -> shift('c',1) = 'd'
- s[5] -> shift('e',1) = 'f'
```

**示例 2:**  
```
Input: s = "a1b2c3d4e"
Output: "abbdcfdhe"
Explanation: 数字的替换过程如下：
- s[1] -> shift('a',1) = 'b'
- s[3] -> shift('b',2) = 'd'
- s[5] -> shift('c',3) = 'f'
- s[7] -> shift('d',4) = 'h'
```

**约束条件**  
- `1 <= s.length <= 100`  
- `s` 仅由小写英文字母和数字组成。  
- 对所有奇数下标 `i`，都有 `shift(s[i‑1], s[i]) <= 'z'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目把字符串 `s` 看成交替出现的「字母‑数字」序列，要求把每个奇数下标的数字 `s[i]` 用 **shift** 运算的结果替换掉。  
`shift(c, x)` 的意义是：从字符 `c` 往后数 `x` 位得到的新字符。  
> **类比**：把字母表想成一本字典，`c` 是某一页的标题，`x` 是要翻多少页，得到的页码对应的字母就是结果。

实现思路非常直接：

1. 从左到右遍历字符串，遇到奇数下标 `i`（即是数字）时：
   - 取前一个字符 `c = s[i-1]`（一定是小写字母）。
   - 把 `c` 转成对应的字母序号（`ord(c) - ord('a')`），再加上数字 `x = int(s[i])`。
   - 把得到的序号再转回字符，即 `chr(ord('a') + new_index)`，放回原位置。
2. 其它位置（偶数下标）保持不动。

**为什么正确**：  
- 题目保证奇数下标必是数字，偶数下标必是字母，且 `shift` 结果不超过 `'z'`，所以上述计算一定落在 `'a'~'z'` 范围内。
- 我们对每个数字都按题意做了相同的「往后数」操作，最终得到的字符串正是题目要求的。

**复杂度分析（大白话）**：

- **时间**：我们只遍历一次字符串，长度记作 `n`，每一步都是 O(1) 的算数运算，所以总共需要大约 `n` 次操作，用数学符号写作 **O(n)**。这就像排队买饭，排多少人就花多少时间，人数翻倍时间也会翻倍。
- **空间**：我们直接在原字符串上改写（Python 用列表临时存），只用了常数级别的额外变量，和字符串长度无关，用 **O(1)** 表示。相当于只在桌子上放了几把勺子，跟排队人数没关系。

#### 代码（Python）

```python
def replaceDigits(s: str) -> str:
    # 把字符串转成列表，方便原地修改
    chars = list(s)

    # 从左到右遍历，步长为 2，只看奇数下标（数字所在位置）
    for i in range(1, len(chars), 2):
        prev_char = chars[i - 1]          # 前一个字母
        shift_amount = int(chars[i])      # 当前的数字，转成整数

        # 计算 shift 后的字母：
        #   ord('a') 是字母表的起始编号，减去它得到 0~25 的索引
        #   加上 shift_amount 再转回字符
        new_char = chr(ord('a') + (ord(prev_char) - ord('a') + shift_amount))
        chars[i] = new_char                # 替换原来的数字

    # 把列表再拼成字符串返回
    return ''.join(chars)
```

#### 复杂度

- **时间复杂度**：**O(n)** — 只遍历一次字符串，`n` 越大，时间大致线性增长。
- **空间复杂度**：**O(1)** — 只用了常数个临时变量（Python 为了可变修改用了 `list`，但不算额外的随 `n` 增长的空间）。

---

### 2. 最优解

#### 思路  

在本题中，**暴力解已经是最优**，因为每个字符只能检查一次，无法再做进一步的“跳过”。  
不过我们仍然可以从「慢在哪里」的角度说明：

- 如果把每个数字都当作「要在整段字符串里找下一个字母」的搜索，那时间会是 **O(n²)**（每次都从头遍历），这就是不好的做法。
- 正确的做法是利用题目已经给出的「相邻」关系：数字只需要看它左边的那个字母，**不需要再遍历其它位置**。这一步把时间从二次降到线性。

核心技巧就是**利用相邻结构**（相邻字符必分别是字母和数字），直接用 **ASCII 码**（`ord`/`chr`）完成「向后移动」的计算。没有额外的数据结构，仅靠常数级别的算数运算即可。

> **类比**：把字母表想成一条直线，`c` 在某个位置，`x` 是要往右走的步数，直接算出新位置，而不是一步一步走。

#### 代码（Python）

```python
def replaceDigits(s: str) -> str:
    # 直接使用列表改写，保持 O(1) 额外空间
    res = list(s)

    for i in range(1, len(res), 2):          # 只遍历奇数下标
        # 前一个字母的 ASCII 编码减去 'a' 的编码得到 0~25 的索引
        base = ord(res[i - 1]) - ord('a')
        shift = int(res[i])                  # 当前数字
        # 新字母的索引 = 基础索引 + 移动步数，然后再转回字符
        res[i] = chr(ord('a') + base + shift)

    return ''.join(res)
```

#### 复杂度

- **时间复杂度**：**O(n)** — 与暴力解相同，因为已经是最简的线性遍历。相比「每次遍历寻找」的 O(n²) 版本快了很多。
- **空间复杂度**：**O(1)** — 只用了常数个临时变量（列表本身是对输入的改写，不算额外空间）。

---

## 心得

- **核心技巧**：利用相邻字符的固定模式（字母‑数字），把「向后移动」转化为简单的 ASCII 加减运算。
- **适用的题型**  
  1. “相邻字符有特定关系，需要一次遍历完成转换”的题目，如 LeetCode 1544 *Make The String Great*。  
  2. 只需根据前一个元素计算当前元素的题目，例如「前缀和」或「滑动窗口」中的累计更新。  
  3. 需要把数字映射成字符的题目，如「数字转字母」(Phone Number to Letter)。
- **一句话总结解题钥匙**：**只看左边的字母，直接算出偏移后的字符**。

---

## 反思

- **第一反应**：看到“字母‑数字交替”就想到遍历奇数位，用 `ord`/`chr` 做偏移。
- **最容易踩的坑**  
  - 把数字当成字符直接相加（`'a' + '1'`），会得到错误的 Unicode 码。必须先把数字转成整数。  
  - 忽视题目保证的 “不会超过 `'z'`”，如果自行在代码里加模 26 可能导致错误。  
  - 边界条件：字符串长度为 1 时（只有字母），循环不会执行，直接返回即可。
- **下次遇到同类题的第一步**：**先确认相邻元素之间的固定关系，再决定只遍历一次或需要额外的数据结构**。这样可以立刻排除 O(n²) 的暴力搜索思路，直接进入线性解。