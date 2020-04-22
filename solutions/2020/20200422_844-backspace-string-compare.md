# #844. 退格字符串比较 / Backspace String Compare

> 难度：简单 · 标签：Two Pointers、String、Stack、Simulation · [LeetCode 链接](https://leetcode.com/problems/backspace-string-compare/)

---

## 题目（英文原版）

**Description**

Given two strings s and t, return true if they are equal when both are typed into empty text editors. '#' means a backspace character.
Note that after backspacing an empty text, the text will continue empty.
Follow up: Can you solve it in O(n) time and O(1) space?

**Examples**

**Example 1:**

```
Input: s = "ab#c", t = "ad#c"
Output: true
Explanation: Both s and t become "ac".
```

**Example 2:**

```
Input: s = "ab##", t = "c#d#"
Output: true
Explanation: Both s and t become "".
```

**Example 3:**

```
Input: s = "a#c", t = "b"
Output: false
Explanation: s becomes "c" while t becomes "b".
```

**Constraints**

- 1 <= s.length, t.length <= 200
- s and t only contain lowercase letters and '#' characters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`，当它们分别在空的文本编辑器（text editor）中输入时，如果最终得到的字符串相同则返回 `true`。字符 `'#'` 表示退格键（backspace character）。  
注意，对空文本执行退格操作后，文本仍保持为空。

**示例 1:**  
**示例 2:**  
**示例 3:**  

**约束条件：**  
- 1 ≤ s.length, t.length ≤ 200  
- `s` 和 `t` 仅由小写字母和 `'#'` 组成  

**进阶要求：** 能否在 O(n) 时间复杂度和 O(1) 额外空间复杂度下完成？

**示例**

**示例 1:**  
```
Input: s = "ab#c", t = "ad#c"
Output: true
Explanation: 两个字符串在处理退格后都变成 "ac"。
```

**示例 2:**  
```
Input: s = "ab##", t = "c#d#"
Output: true
Explanation: 两个字符串在处理退格后都变成 ""（空串）。
```

**示例 3:**  
```
Input: s = "a#c", t = "b"
Output: false
Explanation: `s` 处理后变成 "c"，而 `t` 处理后仍为 "b"。
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把每个字符依次“敲进”一个空的文本编辑器里。  
- 当遇到普通字母时，就把它放进去。  
- 当遇到 `#`（退格键）时，就把已经放进去的最后一个字符删掉（如果文本已经空了，就什么也不做）。  

要实现“放进去”和“删掉最后一个字符”，**栈**（stack）是最合适的数据结构。  
栈可以想象成一叠盘子，**压进去**相当于 `push`，**弹出来**相当于 `pop`，正好对应“后进先出”。  

我们对两个字符串 `s` 和 `t` 各自维护一个栈，遍历完后把栈里的字符拼成最终的字符串，再直接比较是否相等即可。  

> 为什么这个方法一定正确？  
> 因为我们模拟了真实的键盘操作：每读一个字符，就立刻把它对编辑器产生的效果执行一次，最终的栈内容就是编辑器里剩下的文字。

**时间/空间复杂度大白话**  
- 时间复杂度 `O(n + m)`：我们要把两个字符串各遍历一遍，`n` 是 `s` 长度，`m` 是 `t` 长度。遍历一次就算一次操作，和“走路的步数”成正比。  
- 空间复杂度 `O(n + m)`：最坏情况下字符串里没有 `#`，我们要把所有字符都放进栈里，栈的大小会和字符串长度一样大。  

#### 代码（Python）  

```python
def build(s: str) -> str:
    """把字符串 s 按照退格规则转成最终的文字，使用栈模拟"""
    stack = []                     # 用列表当栈，push 用 append，pop 用 pop()
    for ch in s:                   # 逐字符遍历
        if ch != '#':              # 普通字母，直接放进栈
            stack.append(ch)       
        elif stack:                # ch 是 '#', 且栈不为空时弹出栈顶
            stack.pop()           
        # 若 stack 为空且遇到 '#', 什么也不做，保持空状态
    return ''.join(stack)          # 把栈里的字符拼成最终字符串

def backspaceCompare(s: str, t: str) -> bool:
    return build(s) == build(t)    # 两个最终字符串相等即为 true
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 这里的 `n`、`m` 分别是 `s`、`t` 的长度。我们对每个字符只做一次「放进」或「弹出」的操作，像是走了 `n+m` 步。  
- **空间复杂度**：`O(n + m)`  
  - 最坏情况下两个栈都要存下所有字符，相当于用了和输入等长的额外空间。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **空间**：我们用了额外的栈来存所有字符。  
其实我们只需要比较两个字符串在 **退格后** 的每一个有效字符是否相同，而不必把全部字符全部保留下来。  

**关键观察**  
- 从右往左遍历字符串更容易判断“当前字符到底有没有被后面的 `#` 抹掉”。  
- 当我们在某个位置看到 `#` 时，意味着接下来要 **跳过** 一个普通字符（因为它会被退格删除），并且 `#` 本身也不计入最终结果。  

基于此，我们可以使用 **双指针**（two‑pointers）技巧：  
- `i` 指向 `s` 的末尾，`j` 指向 `t` 的末尾。  
- 每次循环先让 `i`、`j` 向左移动到 **下一个实际有效的字符**（即跳过被 `#` 删除的字符）。  
- 然后比较这两个字符是否相同。若不同直接返回 `False`。  
- 两个指针都走到字符串左边界（`-1`）时，说明所有字符都匹配，返回 `True`。  

**如何实现“跳过被删除的字符”**  
- 维护一个 **skip 计数**：当看到 `#` 时 `skip++`，表示以后要跳过多少个普通字符。  
- 当看到普通字符时，如果 `skip > 0`，说明它应该被之前的 `#` 删除，`skip--` 并继续向左走。  
- 当 `skip == 0` 时，这个普通字符就是 **当前有效字符**。  

这种做法只用了常数级的额外变量（指针和 skip 计数），不需要额外的栈，空间复杂度降到 `O(1)`。  

**类比**：可以把指针想象成两个人在两条绳子上从右往左走，每走一步都要检查自己前面有多少“绊脚石”（`#`），遇到绊脚石就往后退一步（跳过一个字符），直到两个人都站在同一块“干净的地板”上，才说他们的路径相同。  

#### 代码（Python）  

```python
def next_valid_char_index(s: str, idx: int) -> int:
    """
    给定字符串 s 和当前下标 idx（从右往左），返回下一个
    未被退格删除的字符所在的下标。如果所有字符都被删除则返回 -1。
    """
    skip = 0                     # 需要跳过的字符数量
    while idx >= 0:
        if s[idx] == '#':        # 碰到退格，要求再跳过一个字符
            skip += 1
            idx -= 1
        elif skip > 0:           # 当前是普通字符，但被前面的 # 要删除
            skip -= 1
            idx -= 1
        else:                    # 找到一个真正有效的字符
            break
    return idx                    # 可能是 -1，表示已经没有字符了

def backspaceCompare(s: str, t: str) -> bool:
    i, j = len(s) - 1, len(t) - 1   # 两指针从各自字符串的末尾开始

    while i >= 0 or j >= 0:        # 只要任意一个还有字符未处理，就继续
        i = next_valid_char_index(s, i)   # 移动到 s 的下一个有效字符
        j = next_valid_char_index(t, j)   # 移动到 t 的下一个有效字符

        # 两边都已经遍历完，说明完全匹配
        if i < 0 and j < 0:
            return True
        # 只剩一边还有字符，或者字符不相等，都不匹配
        if i < 0 or j < 0 or s[i] != t[j]:
            return False

        # 当前字符相等，继续向左检查下一个字符
        i -= 1
        j -= 1

    return True    # 循环结束后自然相等
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 每个指针最多遍历各自字符串一次，虽然在遇到 `#` 时会多走几步“跳过”，但整体仍然是线性比例，就像走了 `n+m` 步路。  
- **空间复杂度**：`O(1)`  
  - 只用了若干整数变量（指针、skip 计数），不随输入长度增长，像是只带了一个小背包。相比暴力解省掉了栈的空间。  

---  

## 心得  

- **核心技巧**：**双指针逆序遍历 + 跳过计数**，把“退格”操作转化为“在遍历时直接忽略”。  
- **适用的题型**：  
  1. **字符串逆向匹配**（如 “Valid Palindrome III” 需要跳过特定字符）。  
  2. **带有删除/撤销操作的比较**（如 “Compare Version Numbers” 中的前导零处理）。  
  3. **需要 O(1) 额外空间的双序列对齐**（如 “Merge Sorted Array” 中的逆向归并）。  
- **一句话总结**：**把“先做完所有操作再比较”改成“边走边比较”，省掉所有临时存储**。  

---  

## 反思  

- **第一反应**：直接用栈把每个字符串“跑通”一次，再比较结果。  
- **最容易踩的坑**：  
  - 忘记处理 **连续的 `#`**（比如 `"###a"`），导致跳过计数不准确。  
  - 边界情况：字符串全是 `#`，或者长度为 1 时的处理，需要确保指针可以安全降到 `-1`。  
  - 在双指针实现里，忘记在 `i`、`j` 同时为 `-1` 时直接返回 `True`，会出现错误的 `False`。  
- **下次类似题目**的第一步：**先思考“能不能在遍历的过程中直接决定哪些字符是有效的”，把“后处理”改成“实时过滤”。**