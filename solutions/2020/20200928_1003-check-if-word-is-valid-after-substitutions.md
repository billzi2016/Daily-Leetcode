# #1003. 检查单词在替换后是否有效 / Check If Word Is Valid After Substitutions

> 难度：中等 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/check-if-word-is-valid-after-substitutions/)

---

## 题目（英文原版）

**Description**

Given a string s, determine if it is valid.
A string s is valid if, starting with an empty string t = "", you can transform t into s after performing the following operation any number of times:
Return true if s is a valid string, otherwise, return false.

**Examples**

**Example 1:**

```
Input: s = "aabcbc"
Output: true
Explanation:
"" -> "abc" -> "aabcbc"
Thus, "aabcbc" is valid.
```

**Example 2:**

```
Input: s = "abcabcababcc"
Output: true
Explanation:
"" -> "abc" -> "abcabc" -> "abcabcabc" -> "abcabcababcc"
Thus, "abcabcababcc" is valid.
```

**Example 3:**

```
Input: s = "abccba"
Output: false
Explanation: It is impossible to get "abccba" using the operation.
```

**Constraints**

- 1 <= s.length <= 2 * 104
- s consists of letters 'a', 'b', and 'c'

---

## 题目（中文翻译）

给定一个字符串 `s`，判断它是否为 **有效** 字符串。  
如果从空字符串 `t = ""` 开始，经过任意次数以下操作后能够将 `t` 转换为 `s`，则 `s` 为有效字符串。  

返回 `true` 表示 `s` 是有效的，否则返回 `false`。

---

## 示例

### 示例 1
**输入**: `s = "aabcbc"`  
**输出**: `true`  
**解释**:  
`"" -> "abc" -> "aabcbc"`  
因此 `"aabcbc"` 是有效的。

### 示例 2
**输入**: `s = "abcabcababcc"`  
**输出**: `true`  
**解释**:  
`"" -> "abc" -> "abcabc" -> "abcabcabc" -> "abcabcababcc"`  
因此 `"abcabcababcc"` 是有效的。

### 示例 3
**输入**: `s = "abccba"`  
**输出**: `false`  
**解释**:  
无法通过上述操作得到 `"abccba"`。

---

## 约束条件

- `1 <= s.length <= 2 * 10^4`
- `s` 仅由字母 `'a'`, `'b'`, `'c'` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把题目描述的“从空串通过若干次插入 “abc” 得到 s” 翻过来想：  
**如果我们可以把 s 中出现的 “abc” 删除掉，最后把所有字符都删光，那么 s 就是合法的。**  

这相当于把 “插入” 变成了 “删除”。  
我们可以遍历字符串，把每个字符依次放进一个列表（这里把列表当作**栈**来用），每放进来一次，就检查栈顶最近的三个字符是否恰好是 `a、b、c`，如果是，就把这三个字符弹出（相当于把一个 “abc” 删除掉）。  

- **栈**：可以把它想象成一本随时只能在最上面翻页的笔记本，`push` 相当于在最上面写新字符，`pop` 相当于把最上面的字符擦掉。  
- **为什么正确**：每一次我们删除的 “abc” 必定是一次合法的插入的逆操作。只要所有字符都能被这样成对消除，说明整个过程可以逆向回到空串，即原始的插入过程是可能的。  

#### 代码（Python）  

```python
def isValid(s: str) -> bool:
    stack = []                     # 用列表模拟栈
    for ch in s:                   # 依次读取每个字符
        stack.append(ch)           # 把字符压入栈顶
        # 检查栈顶最近的三个字符是否是 "abc"
        if len(stack) >= 3 and stack[-3:] == ['a', 'b', 'c']:
            # 弹出这三个字符，相当于把一个 "abc" 删除
            stack.pop()
            stack.pop()
            stack.pop()
    # 最后栈空说明所有字符都被成功消除
    return not stack
```

#### 复杂度  

- **时间复杂度**：`O(n)`，只遍历一次字符串，每个字符最多被压入栈一次、弹出一次。  
  - 大白话：如果字符串长 10 万，算法大约要跑 10 万步左右，跟字符串长度成正比。  
- **空间复杂度**：`O(n)`，最坏情况下栈里可能会保存所有字符（比如全是 `a`），需要和输入等长的额外空间。  

---  

### 2. 最优解  

#### 思路  
暴力解已经是线性时间、线性空间的方案，在本题已经是最优的时间复杂度了。  
如果要进一步**降低空间**，可以利用**指针**直接在原字符串上模拟栈的行为，做到 **原地**（in‑place）操作，只使用 `O(1)` 额外空间。  

实现思路：  
1. 用一个整数 `top` 表示“栈顶”在原字符串中的位置（即已经确认有效的字符的最右边索引）。初始 `top = -1`（空栈）。  
2. 依次遍历 `s` 的每个字符 `c`，把它写到 `s[top+1]` 的位置，然后 `top += 1`（相当于 `push`）。  
3. 每次写入后检查最近的三个字符 `s[top-2]、s[top-1]、s[top]` 是否为 `a、b、c`。如果是，就把 `top` 向左移动三格（相当于 `pop` 三次）。  
4. 最后如果 `top == -1`，说明所有字符都被消除，返回 `True`；否则返回 `False`。  

这种做法只用常数级的额外变量（`top`），不需要额外的列表或栈，空间降到了 **O(1)**。  

#### 代码（Python）  

```python
def isValid(s: str) -> bool:
    # 将字符串转成列表，方便原地修改（字符串不可变）
    chars = list(s)
    top = -1                     # 栈顶指针，-1 表示空栈

    for ch in chars:            # 逐个字符处理
        top += 1                # 相当于 push，移动栈顶
        chars[top] = ch        # 把当前字符写到栈顶位置

        # 栈中至少有 3 个字符时检查最近的三个是否为 "abc"
        if top >= 2 and chars[top-2] == 'a' and chars[top-1] == 'b' and chars[top] == 'c':
            top -= 3            # 弹出这三个字符，相当于删除一个 "abc"

    # top 为 -1 说明栈已经全部清空，字符串合法
    return top == -1
```

#### 复杂度  

- **时间复杂度**：`O(n)`，同样只遍历一次字符，每个字符最多被写入一次、被“弹出”一次。  
- **空间复杂度**：`O(1)`（不计入输入字符串本身的存储），只使用了几个整数变量。  
  - 与暴力解对比：时间相同，但空间从 `O(n)` 降到了常数级，适合对内存有严格要求的场景。  

---  

## 心得  

- **核心技巧**：利用栈（或等价的指针）把“插入”问题转化为“删除”问题，逐步消除 “abc”。  
- **适用的题型**：  
  1. “删除指定子串后判断是否为空”——如 *Valid Parentheses*（括号匹配）  
  2. “在字符串中消除相邻相同字符”——如 *Remove All Adjacent Duplicates in String*  
  3. “利用单调栈求区间最值”——思路相似，都是在遍历中维护一个栈来记录状态。  
- **一句话总结**：**把“能插入 abc”逆向为“能删掉 abc”，用栈把每一次匹配的 abc 及时弹出，即可判定合法性。**  

## 反思  

- **第一反应**：看到 “插入 abc” 立刻想到逆向思考——把插入当成删除，更容易实现。  
- **最容易踩的坑**：  
  - 忘记在每次压栈后都要检查最近的三个字符（如果只在遍历结束后检查会漏掉中间的匹配）。  
  - 边界情况：字符串长度不是 3 的倍数，或者出现不完整的 “ab”、 “bc” 等残余，需要确保最终栈为空才算合法。  
- **下次类似题目第一步**：**先把操作逆向**（插入 → 删除 / 加 → 减），再寻找可以在线性时间内完成的“消除”策略（栈、双指针、前缀和等）。