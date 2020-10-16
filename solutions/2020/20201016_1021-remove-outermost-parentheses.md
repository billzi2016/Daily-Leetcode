# #1021. 去除最外层括号 / Remove Outermost Parentheses

> 难度：简单 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/remove-outermost-parentheses/)

---

## 题目（英文原版）

**Description**

A valid parentheses string is either empty "", "(" + A + ")", or A + B, where A and B are valid parentheses strings, and + represents string concatenation.
A valid parentheses string s is primitive if it is nonempty, and there does not exist a way to split it into s = A + B, with A and B nonempty valid parentheses strings.
Given a valid parentheses string s, consider its primitive decomposition: s = P1 + P2 + ... + Pk, where Pi are primitive valid parentheses strings.
Return s after removing the outermost parentheses of every primitive string in the primitive decomposition of s.

**Examples**

**Example 1:**

```
Input: s = "(()())(())"
Output: "()()()"
Explanation: 
The input string is "(()())(())", with primitive decomposition "(()())" + "(())".
After removing outer parentheses of each part, this is "()()" + "()" = "()()()".
```

**Example 2:**

```
Input: s = "(()())(())(()(()))"
Output: "()()()()(())"
Explanation: 
The input string is "(()())(())(()(()))", with primitive decomposition "(()())" + "(())" + "(()(()))".
After removing outer parentheses of each part, this is "()()" + "()" + "()(())" = "()()()()(())".
```

**Example 3:**

```
Input: s = "()()"
Output: ""
Explanation: 
The input string is "()()", with primitive decomposition "()" + "()".
After removing outer parentheses of each part, this is "" + "" = "".
```

**Constraints**

- 1 <= s.length <= 105
- s[i] is either '(' or ')'.
- s is a valid parentheses string.

---

## 题目（中文翻译）

有效括号字符串（valid parentheses string）要么为空串 `""`，要么是 `"(" + A + ")"`，要么是 `A + B`，其中 `A` 和 `B` 也是有效括号字符串，`+` 表示字符串拼接。

如果一个有效括号字符串 `s` **非空**，并且不存在把它拆分为 `s = A + B`（其中 `A`、`B` 均为非空的有效括号字符串）的方式，则称 `s` 为**原始**（primitive）。

给定一个有效括号字符串 `s`，考虑它的原始分解：  
`s = P₁ + P₂ + … + P_k`，其中每个 `P_i` 均为原始的有效括号字符串。

返回对上述原始分解中的每个原始字符串去除最外层括号后的结果字符串。

## 示例

### 示例 1
**输入**
``` 
s = "(()())(())"
```  
**输出**
``` 
"()()()"
```  
**解释**  
输入字符串为 `"(()())(())"`，其原始分解为 `"(()())"` + `"(())"`。  
去掉每一部分的最外层括号后得到 `"()()"` + `"()"` = `"()()()"`。

### 示例 2
**输入**
``` 
s = "(()())(())(()(()))"
```  
**输出**
``` 
"()()()()(())"
```  
**解释**  
输入字符串为 `"(()())(())(()(()))"`，其原始分解为 `"(()())"` + `"(())"` + `"(()(()))"`。  
去掉每一部分的最外层括号后得到 `"()()"` + `"()"` + `"()(())"` = `"()()()()(())"`。

### 示例 3
**输入**
``` 
s = "()()"
```  
**输出**
``` 
""
```  
**解释**  
输入字符串为 `"()()"`，其原始分解为 `"()"` + `"()"`。  
去掉每一部分的最外层括号后得到 `""` + `""` = `""`。

## 约束条件
- `1 <= s.length <= 10⁵`
- `s[i]` 只能是 `'('` 或 `')'`
- `s` 是一个有效括号字符串（valid parentheses string）

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把字符串 `s` 按照每一种可能的切分方式全部枚举**，检查每一段是否是“原始”（primitive）的合法括号串。  
- **合法括号串**：可以用栈（想象成“装东西的盒子”）来判断。遍历字符，遇到左括号 `(` 就往栈里放一个东西，遇到右括号 `)` 就把栈顶的东西取出来。如果遍历完后栈为空，说明这段字符串是合法的。  
- **原始串**：在合法的前提下，这段子串内部不能再再分成两个非空的合法子串。换句话说，从左到右遍历时，**第一次出现栈为空的时刻**就是一个原始串的结束位置。  

暴力解的步骤如下：  

1. 枚举所有可能的起点 `i`（0 ≤ i < n）。  
2. 从 `i` 开始向后扩展终点 `j`（i ≤ j < n），实时维护一个栈计数 `cnt`（`cnt` 相当于栈的大小，只需要一个整数）。  
3. 当 `cnt` 恰好回到 0 时，说明 `s[i..j]` 是一个合法的括号串。  
   - 再检查这段子串内部是否出现过 `cnt` 为 0（除去首尾），如果出现，则说明它可以再拆分，**不是原始**。  
   - 如果没有出现过，则这就是一个原始串，直接把去掉首尾的部分（`s[i+1..j-1]`）加入答案。  
4. 继续枚举下一个起点，直到遍历完整个字符串。  

**为什么这个方法能得到正确答案**：  
- 每一次 `cnt` 回到 0 必然对应一个合法的括号子串（因为左括号数等于右括号数，且中途没有出现负数）。  
- 只保留那些在内部**没有再次出现 `cnt==0`** 的子串，正好符合“原始”的定义。  

**时间/空间复杂度**：  
- 外层遍历 `i` 有 `n` 次，内层最坏情况下会把 `j` 推到字符串末尾，导致 **O(n²)** 的时间。  
- 只用到一个整数 `cnt`，空间是 **O(1)**（不计输入输出本身的存储）。  

> **大白话解释**：  
> - `O(n²)` 就好比你要检查一条长度为 `n` 的绳子上每一段可能的子绳子，需要遍历 `n` 条子绳子，每条子绳子又要从头走到尾，最坏会走 `n + (n‑1) + … + 1 ≈ n²/2` 步。  
> - `O(1)` 的空间意味着我们只需要一只手指记数，不需要额外的“大盒子”来存放数据。  

#### 代码（Python）  

```python
def removeOuterParentheses_bruteforce(s: str) -> str:
    n = len(s)
    ans = []                     # 用来收集去掉外层后的字符
    i = 0
    while i < n:                 # 枚举每一个可能的起点
        cnt = 0                   # 相当于栈的大小，只是一个计数器
        inner_zero = False       # 标记在当前子串内部是否出现过 cnt == 0
        for j in range(i, n):    # 向右扩展终点
            if s[j] == '(':
                cnt += 1
            else:                # s[j] == ')'
                cnt -= 1

            # 当 cnt 为 0 时，子串 s[i..j] 已经是合法括号串
            if cnt == 0:
                # 若在 i+1..j-1 之间出现过 cnt == 0，则不是原始串
                if not inner_zero:
                    # 把去掉首尾的部分加入答案
                    ans.append(s[i+1:j])   # i+1 到 j-1
                # 结束本次子串的搜索，下一轮从 j+1 开始
                i = j + 1
                break

            # 只要 cnt 重新回到 0，就说明内部已经出现了可以拆分的点
            if cnt == 0:
                inner_zero = True
        else:
            # 理论上不会走到这里，因为输入保证是合法的括号串
            i = n

    return ''.join(ans)
```

> **关键行中文注释** 已经写在代码里，帮助你快速定位每一步的作用。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 这里的 `n` 是字符串长度。最坏情况下每个起点都要遍历到字符串末尾，导致二次方级别的操作。  
- **空间复杂度**：`O(1)`（不计答案字符串本身）  
  - 只使用了常数个整数变量 `cnt、i、j、inner_zero`。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于重复遍历同一段字符**。事实上，**只要一次线性扫描就能直接得到每个原始串的边界**，因为原始串的定义恰好对应“**从左到右计数器第一次回到 0**”。  

**核心观察**：  
- 用一个计数器 `balance` 表示当前已经看到的左括号 `(` 与右括号 `)` 的差值。  
- 当遍历到某个字符时，`balance` 增加（遇到 `(`）或减少（遇到 `)`）。  
- **当 `balance` 从 1 变成 0 的那一刻**，说明我们刚刚走完了一个原始串（因为它的最外层左括号刚好在本轮被抵消）。  
- 同理，**当 `balance` 从 0 变成 1 的那一刻**，我们正进入一个新的原始串的最外层左括号，这个左括号需要被 **丢弃**。  

于是我们只需要在遍历时：  

1. 读取字符 `c`。  
2. 若 `c` 为 `(`：  
   - 若 `balance > 0`，说明它不是最外层的左括号，**保留**到答案中。  
   - `balance += 1`。  
3. 若 `c` 为 `)`：  
   - `balance -= 1`（先把计数器减），因为我们要先判断这是不是最外层的右括号。  
   - 若 `balance > 0`，说明它不是最外层的右括号，**保留**到答案中。  

整个过程只走一遍字符串，时间 `O(n)`，空间只需要存答案 `O(n)`（输出本身的大小）。  

**类比**：把 `balance` 想成“水位”。左括号是往水池里加水，右括号是放水。当水位刚好回到零时，水池被清空，这对应一个完整的原始括号块。我们只把“中间的水”（非最外层的括号）倒出来。  

#### 代码（Python）  

```python
def removeOuterParentheses(s: str) -> str:
    """
    一次遍历，利用 balance 计数器直接找到每个原始串的内部字符。
    """
    balance = 0          # 当前左括号减去右括号的数量
    res = []              # 用列表收集结果，最后 join 成字符串

    for ch in s:
        if ch == '(':
            # 只有当已经在某个原始串内部（balance > 0）时，才保留 '('
            if balance > 0:
                res.append(ch)
            balance += 1          # 计数器先加，表示进入更深层
        else:  # ch == ')'
            balance -= 1          # 先减，看看这是不是最外层的 ')'
            if balance > 0:
                res.append(ch)   # 仍然在内部，保留 ')'

    return ''.join(res)
```

> **关键行中文注释** 已经写在代码里，帮助你一步步跟上思路。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次字符串，`n` 为字符串长度。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(n)`（输出本身的大小）  
  - 只用了一个计数器 `balance` 以及存放答案的列表。  

---  

## 心得  

- **核心技巧**：使用计数器（相当于简化版的栈）一次遍历即可定位原始括号块的边界。  
- **适用场景**：  
  1. “删除最外层括号” 这类原始串分解的问题（本题）。  
  2. “判断字符串是否为有效的括号序列”——同样可以用计数器判断是否在任何时刻出现负数。  
  3. “最长有效括号子串”——虽然需要更复杂的技巧，但计数器是基础。  
- **一句话总结解题钥匙**：**“balance 从 0→1 时丢掉左括号，从 1→0 时丢掉右括号，其余的都是内部字符”。**  

## 反思  

- **第一反应**：看到“原始分解”几个字，立刻想到“把字符串划分成若干块，每块内部平衡”。于是想到了栈或计数器。  
- **最容易踩的坑**：  
  - **忘记先更新 `balance` 再判断**：右括号时必须先 `balance -= 1`，否则会把本应该删除的最外层 `)` 错误保留下来。  
  - **边界条件**：全是 `()` 的情况会返回空字符串，代码必须能处理 `balance` 直接回到 0 的瞬间。  
- **下次类似题的第一步**：先想 **“能否用一个计数器把层次信息压缩？”**，如果能，就尝试一次遍历解决；如果不行，再考虑真正的栈或 DP。