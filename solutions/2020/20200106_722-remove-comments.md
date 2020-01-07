# #722. 去除注释 / Remove Comments

> 难度：中等 · 标签：Array、String · [LeetCode 链接](https://leetcode.com/problems/remove-comments/)

---

## 题目（英文原版）

**Description**

Given a C++ program, remove comments from it. The program source is an array of strings source where source[i] is the ith line of the source code. This represents the result of splitting the original source code string by the newline character '\n'.
In C++, there are two types of comments, line comments, and block comments.
The first effective comment takes precedence over others.
If a certain line of code is empty after removing comments, you must not output that line: each string in the answer list will be non-empty.
There will be no control characters, single quote, or double quote characters.
Also, nothing else such as defines or macros will interfere with the comments.
It is guaranteed that every open block comment will eventually be closed, so "/*" outside of a line or block comment always starts a new comment.
Finally, implicit newline characters can be deleted by block comments. Please see the examples below for details.
After removing the comments from the source code, return the source code in the same format.

**Examples**

**Example 1:**

```
Input: source = ["/*Test program */", "int main()", "{ ", "  // variable declaration ", "int a, b, c;", "/* This is a test", "   multiline  ", "   comment for ", "   testing */", "a = b + c;", "}"]
Output: ["int main()","{ ","  ","int a, b, c;","a = b + c;","}"]
Explanation: The line by line code is visualized as below:
/*Test program */
int main()
{ 
  // variable declaration 
int a, b, c;
/* This is a test
   multiline  
   comment for 
   testing */
a = b + c;
}
The string /* denotes a block comment, including line 1 and lines 6-9. The string // denotes line 4 as comments.
The line by line output code is visualized as below:
int main()
{ 
  
int a, b, c;
a = b + c;
}
```

**Example 2:**

```
Input: source = ["a/*comment", "line", "more_comment*/b"]
Output: ["ab"]
Explanation: The original source string is "a/*comment\nline\nmore_comment*/b", where we have bolded the newline characters.  After deletion, the implicit newline characters are deleted, leaving the string "ab", which when delimited by newline characters becomes ["ab"].
```

**Constraints**

- 1 <= source.length <= 100
- 0 <= source[i].length <= 80
- source[i] consists of printable ASCII characters.
- Every open block comment is eventually closed.
- There are no single-quote or double-quote in the input.

---

## 题目（中文翻译）

**描述**  
给定一个 C++ 程序，去除其中的注释。程序源码以字符串数组 `source` 的形式给出，其中 `source[i]` 是第 `i` 行源码。这相当于把原始源码字符串按换行符 `'\n'` 拆分后的结果。

在 C++ 中，有两种注释：行注释（line comments）和块注释（block comments）。  
- 行注释以 `//` 开始，直到行尾结束。  
- 块注释以 `/*` 开始，以 `*/` 结束，期间可以跨多行。

**规则**  
1. 当多种注释形式重叠时，先出现的有效注释拥有最高优先级。  
2. 删除注释后，如果某一行变为空行，则该行不应出现在返回结果中，即答案列表中的每个字符串均为非空。  
3. 输入中不会出现控制字符、单引号或双引号，也不会有 `#define`、宏等会干扰注释的情况。  
4. 每一个打开的块注释必定会被闭合，因此出现于普通代码或行注释之外的 `/*` 总是标志着新块注释的开始。  
5. 块注释可以删除隐含的换行符（即跨行的块注释会把其中的换行符一起移除），详见下方示例。

完成所有注释的删除后，以与输入相同的格式返回处理后的源码数组。

**示例 1**  

```text
Input: source = ["/*Test program */", "int main()", "{ ", "  // variable declaration ", "int a, b, c;", "/* This is a test", "   multiline  ", "   comment for ", "   testing */", "a = b + c;", "}"]
Output: ["int main()","{ ","  ","int a, b, c;","a = b + c;","}"]
Explanation: 代码按行可视化如下：
/*Test program */
int main()
{ 
  // variable declaration 
int a, b, c;
/* This is a test
   multiline  
   comment for 
   testing */
a = b + c;
}
字符串 `/*` 表示块注释，覆盖第 1 行以及第 6~9 行；字符串 `//` 表示第 4 行的行注释。  
去除注释后，代码按行可视化为：
int main()
{ 
  
int a, b, c;
a = b + c;
}
```

**示例 2**  

```text
Input: source = ["a/*comment", "line", "more_comment*/b"]
Output: ["ab"]
Explanation: 原始源码字符串为 `"a/*comment\nline\nmore_comment*/b"`，其中加粗的部分为换行符。删除注释后，隐含的换行符也被一起删除，得到 `"ab"`，再按换行符切分后得到 `["ab"]`。
```

**约束条件**  

- `1 <= source.length <= 100`  
- `0 <= source[i].length <= 80`  
- `source[i]` 仅包含可打印的 ASCII 字符。  
- 每个打开的块注释必定会被闭合。  
- 输入中不存在单引号或双引号。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把每一行代码都拆成字符，逐个检查**，一旦发现 `//` 或 `/*` 就把后面的内容直接丢掉。  

- **数据结构**：  
  - `list`（列表）就像装有多本笔记本的抽屉，`source[i]` 是第 `i` 本笔记本的内容。  
  - `string`（字符串）可以看成一串珠子，一颗珠子对应一个字符。我们把字符串拆成字符列表，就像把珠子一个一个拎出来检查。  
  - “注释块” 用一个 **布尔变量 `in_block`** 表示当前是否身处 `/* … */` 之间，类似于在阅读一本书时是否打开了“隐藏页”。  

- **为什么正确**：  
  - 对每个字符都做了 **“我在块注释里吗？”** 的判断。  
  - 若在块注释里，直接跳过字符；若遇到块注释的结束标记 `*/`，就把 `in_block` 设为 `False`。  
  - 若不在块注释里，遇到 `//` 就把本行剩余字符全部忽略（因为行注释一直到行尾）。  
  - 其余字符全部保留下来，最后把每行保留下来的字符拼成新行。  

- **时间/空间复杂度**（大白话版）：  
  - **时间**：我们把所有字符都走了一遍，最坏情况每行都有 80 个字符，最多 100 行，总共最多 8 000 个字符 → **O(N)**（N 为字符总数）。  
  - **空间**：除了保存结果之外，只用到了一个 `in_block` 标记和若干临时字符串 → **O(1)**（不随输入大小增长的常数空间），结果本身必须返回，算在输出空间里。  

> 这里的 “暴力” 其实已经是线性遍历的思路，只是没有把状态机写得太精炼。对初学者来说，把每一步写得非常直白、每个判断都单独写一行，会更易于理解。

#### 代码（Python）

```python
def removeComments(source):
    """
    :type source: List[str]
    :rtype: List[str]
    """
    res = []                # 最终返回的代码行
    in_block = False        # 当前是否在块注释 /* ... */ 之中

    # 逐行遍历
    for line in source:
        i = 0               # 当前字符的索引
        if not in_block:
            cur = []        # 本行保留下来的字符（列表，最后 join 成字符串）

        while i < len(line):
            # ---------- 块注释结束 ----------
            if in_block and line[i:i+2] == '*/':
                in_block = False
                i += 2       # 跳过 '*/'
                continue

            # ---------- 仍在块注释中 ----------
            if in_block:
                i += 1       # 直接丢掉这个字符
                continue

            # ---------- 行注释 ----------
            if line[i:i+2] == '//':
                # 行注释后面的全部字符都不需要了，直接结束本行的处理
                break

            # ---------- 块注释开始 ----------
            if line[i:i+2] == '/*':
                in_block = True
                i += 2       # 跳过 '/*'
                continue

            # ---------- 普通字符 ----------
            cur.append(line[i])
            i += 1

        # 行结束后，如果不在块注释里且本行有内容，就加入答案
        if not in_block and cur:
            res.append(''.join(cur))

    return res
```

#### 复杂度  

- **时间复杂度**：`O(N)`，N 为所有字符的总数。我们只遍历了一遍，没有嵌套循环。  
- **空间复杂度**：`O(1)`（不计输出）。只用了常数个额外变量 `in_block`、`i`、`cur`（`cur` 最多存一行的字符，长度受单行长度限制）。  

---  

### 2. 最优解  

#### 思路  

从上面的暴力实现来看，**真正的瓶颈** 并不在时间（已经是线性），而在代码的可读性与实现的“状态管理”。  
我们可以把整个过程抽象成 **一个有限状态机**（Finite State Machine），只用两种状态：

| 状态 | 含义 | 进入/退出的触发字符 |
|------|------|--------------------|
| **普通代码** (`NORMAL`) | 正常代码，字符要保留 | `/*` → 进入 `BLOCK`；`//` → 进入 `LINE_END`（直接跳到行尾） |
| **块注释** (`BLOCK`) | 在 `/* … */` 之间，所有字符都丢弃 | `*/` → 返回 `NORMAL` |

实现时只需要一个布尔 `in_block` 来记录当前是否在 `BLOCK` 状态，**不需要额外的栈或递归**，因为题目保证块注释一定能成对闭合，且不出现嵌套（`/*` 在块注释内部不再起作用）。  

核心步骤如下：

1. **逐行遍历**：外层 `for line in source`。  
2. **逐字符扫描**：使用 `while i < len(line)`，在 `NORMAL` 状态下检查两字符组合 (`line[i:i+2]`) 是否是注释起始或结束标记。  
3. **状态转移**：  
   - `NORMAL` + `/*` → `in_block = True`，`i += 2`。  
   - `NORMAL` + `//` → `break`（本行结束）。  
   - `BLOCK` + `*/` → `in_block = False`，`i += 2`。  
   - 其他字符：若 `in_block` 为 `False`，则保存到本行结果。  
4. **行结束处理**：如果当前不在块注释且本行结果非空，加入 `res`。  

> **为什么叫“最优”**：  
> - 时间已经是最小的 O(N)。  
> - 只用了常数额外空间，代码结构清晰，易于调试。  
> - 与“暴力”实现的区别在于：把所有的判断统一放进 **状态机** 的框架里，避免了重复检查 `in_block` 的逻辑，使代码更简洁。

#### 代码（Python）

```python
def removeComments(source):
    """
    使用有限状态机（NORMAL / BLOCK）一次遍历完成去注释。
    """
    res = []          # 最终返回的代码行
    in_block = False  # 当前是否处于块注释状态

    for line in source:
        i = 0
        # 只在普通代码状态时需要构建本行结果
        cur = [] if not in_block else None

        while i < len(line):
            # ---- 块注释结束 ----
            if in_block and line[i:i+2] == '*/':
                in_block = False
                i += 2
                continue

            # ---- 仍在块注释中，直接跳过当前字符 ----
            if in_block:
                i += 1
                continue

            # ---- 行注释，直接结束本行扫描 ----
            if line[i:i+2] == '//':
                break

            # ---- 块注释开始 ----
            if line[i:i+2] == '/*':
                in_block = True
                i += 2
                continue

            # ---- 普通字符，加入本行结果 ----
            cur.append(line[i])
            i += 1

        # 行结束后，如果不在块注释且本行有内容，保存
        if not in_block and cur:
            res.append(''.join(cur))

    return res
```

#### 复杂度  

- **时间复杂度**：`O(N)`，每个字符只检查一次，没有任何额外的循环。相较于暴力实现，**速度相同**，但代码更简洁。  
- **空间复杂度**：`O(1)`（不计输出），只使用了 `in_block`、`i`、`cur` 三个额外变量。  

---  

## 心得  

- **核心技巧**：**有限状态机**（State Machine）+ **一次遍历**。  
- **适用的题型**（类似思路）：  
  1. **字符串解析**（如 LeetCode 212. Word Search II 中的 Trie 状态转移）。  
  2. **括号匹配**（如 LeetCode 20. Valid Parentheses，使用栈模拟状态）。  
  3. **标记语言解析**（如 XML/HTML 标签匹配、Markdown 渲染）。  
- **一句话总结**：**把“在注释里 / 不在注释里”抽象成两种状态，用一个布尔变量切换，线性扫描即可完成去注释。**  

## 反思  

- **第一反应**：看到 `/* … */` 与 `//`，立刻想到逐字符遍历并手动跳过注释内容。  
- **最容易踩的坑**：  
  - **块注释跨行**：忘记在跨行的情况下保持 `in_block` 状态，导致后面的代码被错误保留。  
  - **`/*` 与 `*/` 重叠**：如 `/**/`，必须先识别结束再恢复普通状态，否则会漏掉后面的字符。  
  - **空行**：删除注释后可能得到空字符串，题目要求不输出空行，需要在加入结果前检查 `cur` 是否非空。  
- **下次类似题目第一步**：**先明确所有可能的“状态”，把每种状态下的转移规则写下来，再用一次遍历实现。**这样可以避免遗漏边界条件，代码结构也更清晰。