# #2124. 检查所有 a 是否出现在所有 b 之前 / Check if All A's Appears Before All B's

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/check-if-all-as-appears-before-all-bs/)

---

## 题目（英文原版）

**Description**

Given a string s consisting of only the characters 'a' and 'b', return true if every 'a' appears before every 'b' in the string. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: s = "aaabbb"
Output: true
Explanation:
The 'a's are at indices 0, 1, and 2, while the 'b's are at indices 3, 4, and 5.
Hence, every 'a' appears before every 'b' and we return true.
```

**Example 2:**

```
Input: s = "abab"
Output: false
Explanation:
There is an 'a' at index 2 and a 'b' at index 1.
Hence, not every 'a' appears before every 'b' and we return false.
```

**Example 3:**

```
Input: s = "bbb"
Output: true
Explanation:
There are no 'a's, hence, every 'a' appears before every 'b' and we return true.
```

**Constraints**

- 1 <= s.length <= 100
- s[i] is either 'a' or 'b'.

---

## 题目（中文翻译）

给定一个仅由字符 `'a'` 和 `'b'` 组成的字符串 `s`，如果字符串中每个 `'a'` 都出现在每个 `'b'` 之前，则返回 `true`；否则返回 `false`。

**示例 1**  
**输入**: `s = "aaabbb"`  
**输出**: `true`  
**解释**:  
`'a'` 出现在索引 `0、1、2`，`'b'` 出现在索引 `3、4、5`。因此所有 `'a'` 都在所有 `'b'` 之前，返回 `true`。

**示例 2**  
**输入**: `s = "abab"`  
**输出**: `false`  
**解释**:  
在索引 `2` 处有 `'a'`，而在索引 `1` 处有 `'b'`。因此并非所有 `'a'` 都在所有 `'b'` 之前，返回 `false`。

**示例 3**  
**输入**: `s = "bbb"`  
**输出**: `true`  
**解释**:  
字符串中没有 `'a'`，所以条件自然成立，返回 `true`。

**约束条件**  
- `1 <= s.length <= 100`  
- `s[i]` 只能是 `'a'` 或 `'b'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有字符两两比较**，只要出现了 `'b'` 在 `'a'` 前面的情况（即子串 `"ba"`），就说明不满足 “所有 `a` 必须出现在所有 `b` 前面”。  
- **用到的数据结构**：只需要原始的字符串 `s`，不需要额外的数据结构。可以把它想象成一排小盒子，每个盒子里只能放 `'a'` 或 `'b'`，我们要检查盒子里是否出现了 “先放 `b` 再放 `a`” 的顺序。
- **为什么正确**：如果在任意位置出现了 `"ba"`，必然有一个 `a` 位于一个 `b` 的右侧，这正好违背了题意。反之，若遍历完所有相邻字符都没有 `"ba"`，说明所有 `a` 都在 `b` 前面（或者根本没有 `a`），返回 `True`。
- **时间/空间复杂度**：我们会检查每一对相邻字符，最多检查 `len(s)-1` 次。时间复杂度是 **O(n)**（`n` 为字符串长度），空间只用了常数个变量，空间复杂度是 **O(1)**。  
> 大白话：如果 `n` 是 100，最多检查 99 次，几乎不花时间；`O(1)` 就是说无论 `n` 多大，额外占用的内存几乎不变。

#### 代码（Python）

```python
def checkString_bruteforce(s: str) -> bool:
    """
    暴力检查相邻字符是否出现 "ba"
    """
    # 遍历下标 0 ~ len(s)-2，比较 s[i] 和 s[i+1]
    for i in range(len(s) - 1):
        if s[i] == 'b' and s[i + 1] == 'a':   # 发现 "ba" 子串
            return False                     # 立刻返回 False
    return True                              # 循环结束，说明没有 "ba"
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 需要遍历一次字符串，`n` 越大，检查次数线性增长。  
- **空间复杂度**：`O(1)` —— 只用了常数个临时变量（`i`、`s` 本身不算额外空间）。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道：**只要出现 `"ba"` 就不合法**。  
- **慢在哪里**：暴力解已经是线性扫描，已经很快；这里的“最优”指的是**代码更简洁、思路更直接**。我们可以不必手动比较每对字符，而是直接利用 Python 的字符串查找功能 `in`，判断 `"ba"` 是否是 `s` 的子串。  
- **一步步推导**  
  1. 题目等价于 “字符串中是否包含子串 `ba`”。  
  2. Python 中 `sub in s` 会在 **O(n)** 时间内完成子串检查（内部实现同样是一次遍历）。  
  3. 只要 ` "ba" not in s ` 为真，就返回 `True`，否则返回 `False`。  
- **核心概念**：**子串查找**（substring search）。可以把它想象成在一段文字里找一本特定的词语，找到一次就说明出现了。这里我们找的是 `"ba"`，如果找不到，就说明所有 `a` 都在 `b` 前面。  
- **为什么是最优**：时间仍是 `O(n)`，但代码只用一行表达，阅读和维护更容易。

#### 代码（Python）

```python
def checkString_optimal(s: str) -> bool:
    """
    直接判断字符串中是否出现子串 "ba"
    """
    # 如果 "ba" 没出现，说明所有 a 都在 b 前面（或根本没有 a）
    return "ba" not in s
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 仍然需要检查整个字符串一次，`n` 越大检查时间线性增长。  
- **空间复杂度**：`O(1)` —— 只使用了常数级的临时变量（实际上这里没有额外变量）。

> 与暴力解对比：两者时间相同，但最优解更简洁、可读性更高。

---

## 心得

- **核心技巧**：检查是否出现特定的“坏子串”（这里是 `"ba"`），常用 `in` 或遍历相邻字符的方式。  
- **适用的题型**  
  1. 判断字符串是否满足 “所有 X 必须出现在所有 Y 前面” （如 `Check if All 0's Appear Before All 1's`）。  
  2. 判断字符串是否符合某种 **模式**（如 “没有连续相同字符”），可以通过搜索特定子串实现。  
  3. 判断是否为 **合法的括号序列**，思路类似：寻找 “非法子串” 如 `")("`。  
- **一句话总结**：**找出违背规则的最小“坏片段”，只要它不存在，整体就符合要求**。

---

## 反思

- **第一反应**：看到只有 `'a'`、`'b'` 两种字符，立刻想到遍历一次检查相邻位置是否出现 `"ba"`。  
- **最容易踩的坑**  
  - 忽略了空字符串或全是 `'b'`、全是 `'a'` 的情况。其实这些都应该返回 `True`，因为没有违背规则的对。  
  - 把判断写成 “是否所有 `a` 的下标都小于所有 `b` 的下标”，实现时容易忘记处理没有 `a` 或没有 `b` 的情况。  
- **下次类似题目第一步**：先**确定一种“非法模式”**（如 `"ba"`），然后检查该模式是否出现。这样可以把复杂的比较转化为简单的子串查找或一次线性扫描。