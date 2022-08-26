# #1910. 移除子串的所有出现 / Remove All Occurrences of a Substring

> 难度：中等 · 标签：String、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/remove-all-occurrences-of-a-substring/)

---

## 题目（英文原版）

**Description**

Given two strings s and part, perform the following operation on s until all occurrences of the substring part are removed:
Return s after removing all occurrences of part.
A substring is a contiguous sequence of characters in a string.

**Examples**

**Example 1:**

```
Input: s = "daabcbaabcbc", part = "abc"
Output: "dab"
Explanation: The following operations are done:
- s = "daabcbaabcbc", remove "abc" starting at index 2, so s = "dabaabcbc".
- s = "dabaabcbc", remove "abc" starting at index 4, so s = "dababc".
- s = "dababc", remove "abc" starting at index 3, so s = "dab".
Now s has no occurrences of "abc".
```

**Example 2:**

```
Input: s = "axxxxyyyyb", part = "xy"
Output: "ab"
Explanation: The following operations are done:
- s = "axxxxyyyyb", remove "xy" starting at index 4 so s = "axxxyyyb".
- s = "axxxyyyb", remove "xy" starting at index 3 so s = "axxyyb".
- s = "axxyyb", remove "xy" starting at index 2 so s = "axyb".
- s = "axyb", remove "xy" starting at index 1 so s = "ab".
Now s has no occurrences of "xy".
```

**Constraints**

- 1 <= s.length <= 1000
- 1 <= part.length <= 1000
- s​​​​​​ and part consists of lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `part`，对 `s` 重复执行以下操作，直至所有 `part` 的出现（occurrences）全部被移除：
- 在 `s` 中找到 `part` 的一次出现，将其删除。

返回删除所有 `part` 后的字符串 `s`。

子串（substring）是字符串中连续的字符序列。

**示例 1**

```text
Input: s = "daabcbaabcbc", part = "abc"
Output: "dab"
Explanation: 依次进行如下操作：
- s = "daabcbaabcbc"，在下标 2 处删除 "abc"，得到 s = "dabaabcbc"。
- s = "dabaabcbc"，在下标 4 处删除 "abc"，得到 s = "dababc"。
- s = "dababc"，在下标 3 处删除 "abc"，得到 s = "dab"。
此时 s 中已不再出现 "abc"。
```

**示例 2**

```text
Input: s = "axxxxyyyyb", part = "xy"
Output: "ab"
Explanation: 依次进行如下操作：
- s = "axxxxyyyyb"，在下标 4 处删除 "xy"，得到 s = "axxxyyyb"。
- s = "axxxyyyb"，在下标 3 处删除 "xy"，得到 s = "axxyyb"。
- s = "axxyyb"，在下标 2 处删除 "xy"，得到 s = "axyb"。
- s = "axyb"，在下标 1 处删除 "xy"，得到 s = "ab"。
此时 s 中已不再出现 "xy"。
```

**约束条件**

- `1 <= s.length <= 1000`
- `1 <= part.length <= 1000`
- `s` 和 `part` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是：**一次遍历字符串 `s`，每找到一次子串 `part` 就把它删掉，然后从头再检查一次**。  
可以把这个过程想象成 **在一段文字里找“关键词”，找到后把这几个字划掉**，划掉以后，前后相邻的文字会重新连在一起，可能会出现新的关键词，于是再继续找。

实现细节：

1. 使用 Python 的 `str.find(sub)` 能一次性返回 `sub` 在当前字符串中的最左出现位置（若不存在返回 `-1`）。  
2. 如果找到了，就把 `s` 切成三段：左边、被删掉的 `part`、右边，拼接左边和右边得到新的 `s`。  
3. 循环上述步骤，直到 `find` 返回 `-1`，说明已经没有 `part` 了。

> **为什么正确**  
> 每一次我们都把 `s` 中出现的 **最左** 的 `part` 删除，题目要求“把所有出现的 `part` 删除”，而删除后可能出现新的 `part`，我们会在下一轮继续检查。只要循环到找不到为止，就一定把所有可能出现的 `part` 都删光了。

> **复杂度分析（大白话）**  
> - **时间**：每次 `find` 最坏要遍历整个字符串 O(n)，删除后字符串长度会变短，但最坏情况下每次只删掉 `len(part)` 个字符，循环次数可能是 `n / len(part)` 次，综合下来大约是 O(n²)。可以把它想象成“把一堆积木一次只搬走几块，搬来搬去要搬很多次”。  
> - **空间**：我们只使用了几个临时变量保存字符串本身，额外空间是 O(1)。

#### 代码（Python）

```python
def remove_substring_brute(s: str, part: str) -> str:
    """
    暴力解法：循环查找并删除 part，直到找不到为止
    """
    while True:
        idx = s.find(part)          # 找到 part 最左出现的位置，-1 表示不存在
        if idx == -1:               # 没找到，结束循环
            break
        # 把左边 + 右边拼接起来，等价于把 idx~idx+len(part)-1 这段删掉
        s = s[:idx] + s[idx + len(part):]
    return s
```

#### 复杂度

- **时间复杂度**：O(n²)  
  > n 为原始字符串长度。每次 `find` 都要遍历整段字符串，最坏会进行约 n / |part| 次循环。
- **空间复杂度**：O(1)  
  > 只用了常数个额外变量，原字符串本身在原地被重新拼接。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次删除都要重新生成整个字符串**，导致大量的拷贝。我们可以把“删除”操作改成 **在遍历过程中直接把字符弹出**，这样只需要一次遍历。

**核心技巧：栈（Stack）**  
- 把字符串看成一串积木，从左到右依次放进栈里。  
- 每放进去一个字符，就检查栈顶最近的 `len(part)` 个字符是否正好组成 `part`。  
- 如果相同，就把这 `len(part)` 个字符一次性弹出（相当于把这段子串删掉）。  
- 继续往后放字符，直到遍历完所有字符。栈中剩下的字符顺序就是答案。

> **为什么正确**  
> 栈的特性是 **后进先出**，恰好对应我们要检查的“最近的若干字符”。当我们把字符压入栈时，所有已经确定不可能再和后面的字符组合成 `part` 的字符就会永久留在栈底。只要在每一步都检查栈顶是否形成 `part`，就能即时删除所有出现的子串，包括因为前一次删除而产生的新子串。

> **类比**  
> 想象你在纸上写字，每写完一个字就检查最近写的几个字是否拼成了 “abc”。如果拼成了，就把这几笔橡皮擦掉，继续往后写。这样只需要一次从左到右的书写过程。

> **实现细节**  
> 1. 用列表 `stack` 当作字符栈，`stack.append(ch)` 把字符压入。  
> 2. 每次压入后，若栈的长度 ≥ `len(part)`，取栈顶的 `len(part)` 个字符（`stack[-len(part):]`）与 `part` 比较。  
> 3. 相等则执行 `del stack[-len(part):]`，一次性弹出。  
> 4. 最终 `''.join(stack)` 即为结果。

> **复杂度分析（大白话）**  
> - **时间**：我们只遍历一次 `s`，每个字符最多进栈一次、出栈一次，整体是 O(n)。  
> - **空间**：栈里最多保存全部字符，最坏是 O(n) 的额外空间。

#### 代码（Python）

```python
def remove_substring_opt(s: str, part: str) -> str:
    """
    最优解：使用栈一次遍历完成所有删除
    """
    stack = []                     # 用列表当栈，存放已经遍历过的字符
    m = len(part)                  # part 的长度，后面会多次使用

    for ch in s:                   # 从左到右遍历原字符串
        stack.append(ch)           # 把当前字符压入栈
        # 只有栈的长度足够长时才可能形成 part
        if len(stack) >= m and ''.join(stack[-m:]) == part:
            # 栈顶的最近 m 个字符正好是 part，全部弹出
            del stack[-m:]         # 删除相当于 "pop" m 次

    # 栈中剩下的字符顺序即为最终字符串
    return ''.join(stack)
```

> **代码要点说明**  
> - `stack[-m:]` 取的是栈顶最近 `m` 个字符，等价于 “查看最近写的几笔”。  
> - `del stack[-m:]` 一次性删除这几笔，比循环 `pop` 更简洁。  
> - `''.join(stack)` 把列表转回字符串，时间复杂度仍然是线性的。

#### 复杂度

- **时间复杂度**：O(n)  
  > n 为 `s` 的长度。每个字符最多进栈一次、出栈一次，整体线性遍历。
- **空间复杂度**：O(n)  
  > 需要额外的栈来保存已经遍历的字符，最坏情况下保存全部字符。

---

## 心得

- **核心技巧**：**栈 + 滑动窗口**（检查栈顶最近 `len(part)` 个字符），可以在一次遍历中完成“出现即删除”的需求。  
- **适用题型**  
  1. **移除子串**（本题）  
  2. **字符串消消乐**：比如 LeetCode 1003 “检查替换后的词是否为回文” 中的 “消除相邻相同字符” 也可以用栈实现。  
  3. **括号匹配**：判断合法括号序列时，同样利用栈检查最近的左括号是否匹配。  
- **一句话总结**：**“把字符压栈，遇到完整的目标子串就弹出——一次遍历搞定所有删除”。**

---

## 反思

- **第一反应**：直接用 `str.replace` 循环或 `find` 删除，想到的是暴力实现。  
- **最容易踩的坑**  
  1. **新出现的子串**：删除一次后，前后字符会重新相连，可能形成新的 `part`，必须继续检查。  
  2. **边界条件**：`part` 长度为 1 时，栈的检查仍然适用；若 `part` 与 `s` 完全相同，要返回空串。  
  3. **重复删除**：如果使用 `replace` 一次性全部替换，可能错过因删除产生的新子串。  
- **下次类似题的第一步**：先问自己 “删除后会不会出现新的目标模式？” 如果答案是 **会**，就考虑 **栈**（或双指针）实现 “出现即删” 的一次遍历方案。