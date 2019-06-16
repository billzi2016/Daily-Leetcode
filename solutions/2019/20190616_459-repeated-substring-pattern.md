# #459. 重复子串模式 / Repeated Substring Pattern

> 难度：简单 · 标签：String、String Matching · [LeetCode 链接](https://leetcode.com/problems/repeated-substring-pattern/)

---

## 题目（英文原版）

**Description**

Given a string s, check if it can be constructed by taking a substring of it and appending multiple copies of the substring together.

**Examples**

**Example 1:**

```
Input: s = "abab"
Output: true
Explanation: It is the substring "ab" twice.
```

**Example 2:**

```
Input: s = "aba"
Output: false
```

**Example 3:**

```
Input: s = "abcabcabcabc"
Output: true
Explanation: It is the substring "abc" four times or the substring "abcabc" twice.
```

**Constraints**

- 1 <= s.length <= 104
- s consists of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，检查它是否能够通过取 `s` 的一个子串（substring）并将该子串复制多次后拼接而成。

**示例 1**  
**示例 2**  
**示例 3**  

**示例**  

**示例 1:**  
```
Input: s = "abab"
Output: true
Explanation: 它是子串 "ab" 重复两次得到的。
```

**示例 2:**  
```
Input: s = "aba"
Output: false
Explanation: 无法将其拆分为同一子串的多次拼接。
```

**示例 3:**  
```
Input: s = "abcabcabcabc"
Output: true
Explanation: 它可以是子串 "abc" 重复四次，或者子串 "abcabc" 重复两次得到的。
```

**约束条件**  
- `1 <= s.length <= 10^4`  
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把原字符串 `s` 的所有**可能的子串**都枚举一遍，只要子串的长度能整除 `len(s)`（也就是说，子串可以完整地“拼”成原字符串），就把它复制若干次，看是否和 `s` 完全相同。  

- **数据结构**：这里只需要用到 **字符串** 本身和 **整数**，不需要额外的数据结构。可以把子串想象成一本书的“章节”，只有章节长度能被整本书的页数整除时，才可能把章节重复拼成整本书。  
- **正确性**：如果 `s` 真的是由某个子串重复得到的，那么这个子串的长度一定是 `len(s)` 的约数。遍历所有约数并逐个验证，必然能找到答案。  
- **时间/空间复杂度**：  
  - 外层遍历所有可能的子串长度，最多是 `len(s)` 次；  
  - 对每个长度，都要把子串重复 `len(s)//len(sub)` 次并和 `s` 比较，这一步最坏情况要遍历整个字符串。  
  因此总体时间是 **O(n²)**（n 为字符串长度），可以想象成“每次都要把整本书重新读一遍”。  
  - 只用了常数级的额外空间 **O(1)**（只保存几个整数和临时的子串），不随 n 增长。

#### 代码（Python）
```python
def repeatedSubstringPattern_bruteforce(s: str) -> bool:
    n = len(s)
    # 枚举子串长度，从 1 到 n//2（超过一半就不可能再重复了）
    for l in range(1, n // 2 + 1):
        # 只有长度能整除 n 才可能拼成原串
        if n % l != 0:
            continue
        # 取前 l 个字符作为候选子串
        sub = s[:l]
        # 把子串重复 n//l 次
        rebuilt = sub * (n // l)
        # 与原串比较
        if rebuilt == s:
            return True
    return False
```

#### 复杂度
- **时间复杂度**：`O(n²)` — 想象成“对每一种可能的子串长度，都要重新遍历整条字符串”。  
- **空间复杂度**：`O(1)` — 只用了几个整数和临时字符串（Python 的 `*` 会生成新字符串，但长度不超过原串）。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于**每次都要完整地重新拼接并比较**，导致二次遍历。我们可以利用**字符串自身的特性**来一次性判断。

核心观察：如果 `s` 能被某个子串重复得到，那么把 `s` 拼成 `s+s`（即两倍），再去掉首字符和尾字符，得到的字符串仍然会包含原来的 `s`。  
- 直观解释：把 `s` 看成环形的绳子，剪开后再拼成两段。如果原来是“ab|ab|ab|ab”，把它连成两段后是 “abab|abab”。去掉最左边的一个字符和最右边的一个字符后，仍然可以在中间找到完整的 “abab”。  
- 反之，如果 `s` 不是由子串重复构成，那么 `s` 在 `(s+s)[1:-1]` 中出现的概率为 0。

因此，只需要一步操作：检查 `s` 是否是 `(s+s)[1:-1]` 的子串即可。

如果不想用这种“巧技”，另一种常见的最优思路是 **KMP（Knuth–Morris–Pratt）算法** 的前缀函数。前缀函数的最后一个值 `pi[-1]` 表示最长的**相等的前后缀**长度。如果 `len(s) % (len(s) - pi[-1]) == 0`，则说明可以由子串重复得到。这里我们用更易懂的字符串拼接技巧实现。

#### 代码（Python）
```python
def repeatedSubstringPattern_optimal(s: str) -> bool:
    """
    判断 s 是否可以由某个子串重复若干次构成。
    思路：把 s 拼成 s+s，去掉首尾各一个字符后检查是否仍然包含 s。
    """
    if not s:  # 空串直接返回 False，题目保证长度 >= 1，这里做防御性检查
        return False
    doubled = s + s               # 两倍长度的字符串
    trimmed = doubled[1:-1]        # 去掉首尾各一个字符
    # 检查原串是否仍然是子串（Python 的 in 已经做了高效的子串搜索）
    return s in trimmed
```

#### 复杂度
- **时间复杂度**：`O(n)` — 只需要一次线性扫描（`in` 操作在 CPython 中实现为 `O(n)` 的子串搜索），相当于“只读一遍绳子”。  
- **空间复杂度**：`O(n)` — 需要额外存放 `doubled`（长度 2n）和 `trimmed`（长度 2n‑2），但都是与输入规模线性相关的临时字符串。

---

## 心得

- **核心技巧**：利用字符串的**自相似**特性（`s+s` 去首尾）或**前缀函数**来一次性判断重复模式，避免枚举所有子串。  
- **适用题型**：  
  1. 判断字符串是否为另一个字符串的循环移位（如 “rotation” 问题）。  
  2. 找出字符串的最小周期长度（如 “periodic string”）。  
  3. KMP 前缀函数在寻找重复子模式时的应用。  
- **一句话总结**：**把字符串“翻两倍再裁剪”，如果原串还能在里面找到，就说明它是由子串循环重复而成**。

## 反思

- **第一反应**：直接枚举所有可能的子串长度并逐个验证——这就是暴力解。  
- **最容易踩的坑**：  
  - 忘记只枚举能够整除 `len(s)` 的长度，导致不必要的比较。  
  - 边界情况如长度为 1 的字符串，所有实现都要返回 `True`（因为它本身就是“子串”重复一次）。  
  - 在最优解中，如果直接使用 `s in (s+s)[1:-1]`，要确保 `s` 非空，否则会出现错误。  
- **下次第一步**：先思考**“是否可以把原字符串做某种变形后再做一次包含检查”**，这往往能把 O(n²) 的暴力转化为 O(n) 的巧妙判断。