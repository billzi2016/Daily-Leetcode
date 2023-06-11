# #2278. 字符串中字母的百分比 / Percentage of Letter in String

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/percentage-of-letter-in-string/)

---

## 题目（英文原版）

**Description**

Given a string s and a character letter, return the percentage of characters in s that equal letter rounded down to the nearest whole percent.

**Examples**

**Example 1:**

```
Input: s = "foobar", letter = "o"
Output: 33
Explanation:
The percentage of characters in s that equal the letter 'o' is 2 / 6 * 100% = 33% when rounded down, so we return 33.
```

**Example 2:**

```
Input: s = "jjjj", letter = "k"
Output: 0
Explanation:
The percentage of characters in s that equal the letter 'k' is 0%, so we return 0.
```

**Constraints**

- 1 <= s.length <= 100
- s consists of lowercase English letters.
- letter is a lowercase English letter.

---

## 题目（中文翻译）

给定一个字符串 **s**（string）和一个字符 **letter**（letter），返回 **s** 中等于 **letter** 的字符所占的百分比，结果向下取整为整数百分比。

## 示例

### 示例 1
**输入**  
`s = "foobar", letter = "o"`  

**输出**  
`33`  

**解释**  
`s` 中等于字母 `'o'` 的字符有 2 个，比例为 `2 / 6 * 100% = 33%`（向下取整），因此返回 `33`。

### 示例 2
**输入**  
`s = "jjjj", letter = "k"`  

**输出**  
`0`  

**解释**  
`s` 中没有等于字母 `'k'` 的字符，比例为 `0%`，因此返回 `0`。

## 约束条件

- `1 <= s.length <= 100`
- `s` 只包含小写英文字母。
- `letter` 是一个小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把字符串 `s` 从左到右全部遍历一遍，逐个检查每个字符是否和给定的 `letter` 相等。如果相等，就把计数器 `cnt` 加一。遍历结束后，`cnt` 就是 `letter` 在字符串中出现的次数。  
> **类比**：把字符串想象成一排排的信件，`letter` 就是我们要找的特定信封。我们把每封信打开来看，如果是目标信封就记下来，最后统计总数。

有了出现次数 `cnt`，再把它除以字符串的长度 `len(s)`，乘以 100，就得到百分比。题目要求**向下取整**，可以直接使用整数除法 `//`（Python 中 `//` 表示向下取整的除法），或者先算出浮点数再用 `int()` 截取整数部分。

这个方法一定正确，因为我们检查了 **每一个** 字符，漏掉的可能性为零。

#### 代码（Python）

```python
def percentageLetter(s: str, letter: str) -> int:
    # 1. 计数器，记录 letter 出现的次数
    cnt = 0
    # 2. 逐字符遍历 s
    for ch in s:
        if ch == letter:          # 如果当前字符等于目标字母
            cnt += 1              # 计数器加一
    # 3. 计算百分比并向下取整
    #    cnt / len(s) 是出现比例，乘 100 转成百分数，// 实现向下取整
    return (cnt * 100) // len(s)
```

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n = len(s)`。我们只遍历一次字符串，`n` 越大，花的时间就线性增长。  
- **空间复杂度**：`O(1)`，只用了几个整数变量，和字符串长度无关，属于常数级别。

---

### 2. 最优解  

#### 思路  

对这道题来说，**暴力遍历已经是最优**的做法，因为我们必须检查每个字符才能确定出现次数。没有办法跳过任何字符，否则就可能漏掉目标字母。  
唯一可以改进的地方是利用 Python 标准库提供的计数函数 `str.count()`，它内部同样是线性遍历，但代码更简洁。这里把它作为 “最优解” 来展示，思路仍然是：

1. 用 `s.count(letter)` 一行代码直接得到出现次数。  
2. 按同样的公式计算百分比并向下取整。

> **类比**：把 `s.count(letter)` 想象成一本已经装订好的字典，直接查询某个词出现的页码，而不需要我们自己一本一本翻。

#### 代码（Python）

```python
def percentageLetter(s: str, letter: str) -> int:
    # 直接使用 str.count 统计出现次数，内部实现仍是 O(n) 的遍历
    cnt = s.count(letter)        # 统计 letter 在 s 中出现了多少次
    # 同样的公式计算百分比并向下取整
    return (cnt * 100) // len(s)
```

#### 复杂度  

- **时间复杂度**：`O(n)`，`str.count` 仍然需要遍历整个字符串一次。相比手写循环，常数因子可能更小，但渐进复杂度不变。  
- **空间复杂度**：`O(1)`，只使用了几个整数变量。

---

## 心得

- **核心技巧**：统计字符出现次数 → 直接遍历或使用 `str.count`。  
- **适用场景**：  
  1. 统计字符串中某字符出现频率（如 LeetCode 1971. Find if Path Exists in Graph 里统计路径字符）。  
  2. 统计数组/列表中某元素出现次数（如 统计数组中 0 的个数）。  
  3. 需要计算比例或百分比的题目（如 统计投票中某候选人的得票率）。  
- **一句话总结**：**遍历一次即可得答案，别忘了用整数除法 `//` 实现向下取整**。

## 反思

- **第一反应**：直接想遍历字符串并计数，这几乎是唯一可行的思路。  
- **最容易踩的坑**：  
  - 忘记对结果向下取整，使用普通除法 `/` 会得到浮点数，需要再 `int()` 或 `//`。  
  - 当 `letter` 在 `s` 中不存在时，计数为 0，除法仍然合法，因为 `len(s) >= 1`（题目保证字符串非空），不会出现除以 0 的错误。  
- **下次类似题**：第一步先想 “**我需要多少次出现**”，于是自然想到计数 → 再考虑是否可以用语言自带的计数函数简化代码。