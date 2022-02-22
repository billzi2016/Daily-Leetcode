# #1678. **目标解析器（Goal Parser）解释** / Goal Parser Interpretation

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/goal-parser-interpretation/)

---

## 题目（英文原版）

**Description**

You own a Goal Parser that can interpret a string command. The command consists of an alphabet of "G", "()" and/or "(al)" in some order. The Goal Parser will interpret "G" as the string "G", "()" as the string "o", and "(al)" as the string "al". The interpreted strings are then concatenated in the original order.
Given the string command, return the Goal Parser's interpretation of command.

**Examples**

**Example 1:**

```
Input: command = "G()(al)"
Output: "Goal"
Explanation: The Goal Parser interprets the command as follows:
G -> G
() -> o
(al) -> al
The final concatenated result is "Goal".
```

**Example 2:**

```
Input: command = "G()()()()(al)"
Output: "Gooooal"
```

**Example 3:**

```
Input: command = "(al)G(al)()()G"
Output: "alGalooG"
```

**Constraints**

- 1 <= command.length <= 100
- command consists of "G", "()", and/or "(al)" in some order.

---

## 题目（中文翻译）

你拥有一个可以解释字符串指令的目标解析器。指令由字母 **"G"**、**"()"** 和/或 **"(al)"** 按任意顺序组成。目标解析器的解释规则如下：

- **"G"** 解释为字符串 **"G"**  
- **"()"** 解释为字符串 **"o"**  
- **"(al)"** 解释为字符串 **"al"**  

解释得到的各子串按照原始顺序拼接，即为最终结果。  
给定字符串 `command`，返回目标解析器对其的解释结果。

**示例**

```text
示例 1:
Input: command = "G()(al)"
Output: "Goal"
Explanation: 目标解析器按如下方式解释指令：
G   -> G
()  -> o
(al)-> al
最终拼接得到 "Goal"。
```

```text
示例 2:
Input: command = "G()()()()(al)"
Output: "Gooooal"
```

```text
示例 3:
Input: command = "(al)G(al)()()G"
Output: "alGalooG"
```

**约束条件**

- `1 <= command.length <= 100`
- `command` 仅由 **"G"**、**"()"** 和/或 **"(al)"** 组成，顺序任意。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把原始字符串一次又一次地 **整体替换** 成目标字符：

1. 把所有 "`(al)`" 替换成 "`al`"。  
2. 把所有 "`()`" 替换成 "`o`"。  
3. 把所有 "`G`" 替换成 "`G`"（其实不需要替换，保持原样即可）。  

这里用到的 “替换” 操作在 Python 中可以直接调用 `str.replace(old, new)`。  
可以把它想象成 **在一本书里用笔把所有的 “(al)” 划掉，再写上 “al”**，一次完成后再处理 “()”。  

为什么它是对的？  
- 题目保证字符串只由这三种子串组成，且不会出现交叉重叠的情况（比如 "`(a)l`" 这种非法形式）。  
- 按顺序把每种子串都换成对应的解释后，最终得到的就是题目要求的解释字符串。  

**时间/空间分析（大白话）**  
- `replace` 每调用一次都会遍历一次整个字符串，最坏情况会产生一个新的字符串（因为字符串是不可变的）。  
- 我们需要两次 `replace`（`(al)` → `al`，`() → o`），所以总共要 **遍历两遍**，时间大约是 `2 * n`，用大 O 表示就是 **O(n²)**（因为每次遍历都生成新字符串，整体的字符拷贝次数随长度呈二次增长）。  
- 需要额外的存放新字符串的空间，最坏情况是原字符串的两倍，记作 **O(n)**。

#### 代码（Python）  
```python
def interpret_brute(command: str) -> str:
    """
    暴力解：依次把 "(al)"、"()" 替换成对应的字符。
    这里的 replace 会返回一个新字符串，所以会产生额外的拷贝。
    """
    # 第一步：把所有 "(al)" 换成 "al"
    step1 = command.replace("(al)", "al")   # 生成新字符串
    # 第二步：把所有 "()" 换成 "o"
    result = step1.replace("()", "o")       # 再生成一次新字符串
    # "G" 本身不需要处理，直接保留
    return result
```

#### 复杂度  
- **时间复杂度**：O(n²) — 每次 `replace` 都会遍历整个字符串并生成新副本，做了两次遍历，整体拷贝次数随字符串长度的平方增长。  
- **空间复杂度**：O(n) — 需要额外存放两次生成的新字符串，最大占用约原长度的两倍（常数级别的额外空间）。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于每次替换都要重新遍历整个字符串**，而其实我们只需要一次线性扫描就能直接把每个子串翻译成对应字符。

优化思路如下：

1. 用一个指针 `i` 从左到右遍历 `command`。  
2. 看当前字符 `command[i]`：  
   - 如果是 `'G'` → 直接把 `'G'` 加入答案。  
   - 如果是 `'('`，则需要再看后面的字符来决定是 "`()`" 还是 "`(al)`"。  
     - 若 `command[i+1] == ')'` → 把 `'o'` 加入答案，`i` 前进 2 位（跳过 "`()`"）。  
     - 否则必然是 "`(al)``（因为题目保证合法） → 把 `'al'` 加入答案，`i` 前进 4 位（跳过 "`(al)`"）。  
3. 重复上述步骤直至遍历完整个字符串。

**核心概念——双指针**  
这里的 “指针” 其实就是整数下标 `i`，我们用它一次性读取字符并决定往后跳多少步。可以把它想象成 **在一条走廊里一步步前进，每次根据前方的标识决定跨几格**。

**为什么只需要一次遍历**  
- 每次我们都确定了当前子串的完整长度（1、2 或 4），于是可以直接把指针跳到下一个未处理的位置，**不再回头**。  
- 整个过程只看了一遍原始字符串，所以时间是线性的。

#### 代码（Python）  
```python
def interpret_optimal(command: str) -> str:
    """
    最优解：一次线性扫描，依据当前字符决定翻译结果并跳过已处理的子串。
    """
    i = 0                # 指针，指向当前要处理的字符下标
    n = len(command)     # 字符串长度，避免每次都调用 len()
    ans = []              # 用列表收集字符，最后一次性 join，效率更高

    while i < n:
        if command[i] == 'G':
            # 直接把 'G' 加入答案，指针只前进 1 位
            ans.append('G')
            i += 1
        else:  # 当前一定是 '('
            # 看下一个字符决定是 "()"" 还是 "(al)"
            if command[i + 1] == ')':
                # 遇到 "()"
                ans.append('o')
                i += 2      # 跳过 "()"
            else:
                # 遇到 "(al)"
                ans.append('a')
                ans.append('l')
                i += 4      # 跳过 "(al)"
    # 把列表拼成最终字符串返回
    return ''.join(ans)
```

#### 复杂度  
- **时间复杂度**：O(n) — 只遍历一次原始字符串，每个字符最多被检查一次。  
- **空间复杂度**：O(n) — 需要存放答案字符串（长度与输入相同），额外的指针变量是常数级别的。

---

## 心得  

- **核心技巧**：一次线性扫描 + 根据固定模式跳步的 “双指针” 思路。  
- **适用题型**：  
  1. 类似的「模式替换」题，如 LeetCode 1969 *数组元素的最小和*（需要一次遍历决定取值）。  
  2. 字符串解析类题目，例如 LeetCode 678 *有效的括号字符串*（一次遍历判断匹配）。  
  3. 需要「固定长度」或「固定模式」识别的题，如 LeetCode 443 *字符串压缩*。  
- **一句话总结**：**只要能一次确定当前子串的完整长度，就能用线性扫描一次搞定所有翻译。**

---

## 反思  

- **第一反应**：直接想到 `replace`，因为 Python 的字符串替换写起来最舒服。  
- **最容易踩的坑**：  
  - 忘记先处理 "`(al)`" 再处理 "`()`" 会导致 "`()`" 把 "`(al)`" 中的 "`(`" 当成独立模式，得到错误结果。  
  - 边界检查不严谨，例如在判断 `command[i+1]` 时要确保 `i+1` 不越界（这里题目保证合法，但写通用代码时仍需防止 IndexError）。  
- **下次遇到同类题**：第一步先 **画出模式的长度表**（`G:1, ():2, (al):4`），再 **决定用一次遍历并跳步** 的方式实现。这样可以避免多余的拷贝，直接得到最优解。