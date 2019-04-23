# #394. 解码字符串 / Decode String

> 难度：中等 · 标签：String、Stack、Recursion · [LeetCode 链接](https://leetcode.com/problems/decode-string/)

---

## 题目（英文原版）

**Description**

Given an encoded string, return its decoded string.
The encoding rule is: k[encoded_string], where the encoded_string inside the square brackets is being repeated exactly k times. Note that k is guaranteed to be a positive integer.
You may assume that the input string is always valid; there are no extra white spaces, square brackets are well-formed, etc. Furthermore, you may assume that the original data does not contain any digits and that digits are only for those repeat numbers, k. For example, there will not be input like 3a or 2[4].
The test cases are generated so that the length of the output will never exceed 105.

**Examples**

**Example 1:**

```
Input: s = "3[a]2[bc]"
Output: "aaabcbc"
```

**Example 2:**

```
Input: s = "3[a2[c]]"
Output: "accaccacc"
```

**Example 3:**

```
Input: s = "2[abc]3[cd]ef"
Output: "abcabccdcdcdef"
```

**Constraints**

- 1 <= s.length <= 30
- s consists of lowercase English letters, digits, and square brackets '[]'.
- s is guaranteed to be a valid input.
- All the integers in s are in the range [1, 300].

---

## 题目（中文翻译）

给定一个编码字符串，返回其解码后的字符串。  
编码规则为：`k[encoded_string]`，其中方括号（square brackets）内的 `encoded_string` 将被重复恰好 `k` 次。注意，`k` 保证为正整数。  
你可以假设输入字符串始终有效——不存在多余的空格，方括号配对正确等。此外，原始数据不包含任何数字，数字仅用于表示重复次数 `k`。例如，不会出现 `3a` 或 `2[4]` 之类的输入。  
测试用例保证输出长度永不超过 `10^5`。

示例 1:  
Input: s = "3[a]2[bc]"  
Output: "aaabcbc"

示例 2:  
Input: s = "3[a2[c]]"  
Output: "accaccacc"

示例 3:  
Input: s = "2[abc]3[cd]ef"  
Output: "abcabccdcdcdef"

约束条件：  
- `1 <= s.length <= 30`  
- `s` 仅由小写英文字母、数字和方括号 `'[]'` 组成。  
- `s` 保证为合法输入。  
- `s` 中所有整数的取值范围为 `[1, 300]`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**从左到右逐字符读取**，遇到数字 `k` 时，记住它；随后一定会出现左方括号 `[`，表示接下来是一段需要重复 `k` 次的子串。我们可以：

1. **找到匹配的右方括号 `]`**（即当前左括号对应的结束位置）。  
2. 把方括号之间的内容直接取出来（这就是 `encoded_string`），**重复 `k` 次**，得到展开后的子串。  
3. 用得到的子串替换原来的 `k[encoded_string]`，再继续向后处理。

这相当于“把每个最内层的 `k[... ]` 直接算出来”，然后把算好的结果放回原字符串，直到没有方括号为止。

> 类比：把嵌套的文件夹压平。我们先打开最里面的文件夹（最内层的 `[`），把里面的文件复制 `k` 份，然后把这个文件夹删掉，继续处理外层文件夹。

**为什么正确**：题目保证输入合法，且所有的 `[` 都有对应的 `]`，所以每一次我们找的最内层 `k[encoded_string]` 必然是完整且独立的，直接展开后不会影响其它部分的结构。

**复杂度分析（大白话）**  
- 每展开一次，需要 **遍历一次子串** 来复制 `k` 次。  
- 最坏情况下，字符串长度每次都要 **从头到尾扫描** 去找匹配的 `]`，而展开的子串会让整体长度逐渐增大。  
- 如果把所有的展开操作累加起来，时间大概是 **`O(n²)`**（n 是最终输出长度），也就是“每次都要遍历一遍，遍历的次数随长度成平方增长”。  
- 我们只用了原字符串和临时的几个变量，额外空间是 **`O(n)`**（存放最终结果的字符串）。

#### 代码（Python）

```python
def decodeString_brute(s: str) -> str:
    # 只要字符串里还有 '['，就继续处理
    while '[' in s:
        i = 0
        # 先找到最左侧的 '['，因为它一定是最内层的左括号
        while s[i] != '[':
            i += 1
        # 向左找连续的数字，这就是重复次数 k
        j = i - 1
        while j >= 0 and s[j].isdigit():
            j -= 1
        k = int(s[j + 1:i])          # 取出 k

        # 再向右找对应的 ']'（因为当前的 '[' 已经是最内层，直接往后找第一个 ']' 即可）
        left = i                     # '[' 的位置
        right = left + 1
        cnt = 1                      # 用来匹配嵌套的括号，cnt 为 1 表示已经有一个 '['
        while cnt:
            if s[right] == '[':
                cnt += 1
            elif s[right] == ']':
                cnt -= 1
            right += 1
        right -= 1                   # right 指向匹配的 ']'

        # 取出方括号内部的子串
        sub = s[left + 1:right]

        # 用 sub 重复 k 次得到展开后的字符串
        expanded = sub * k

        # 用展开后的字符串替换掉原来的 "k[sub]"
        s = s[:j + 1] + expanded + s[right + 1:]

    return s
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  > 想象最终输出长度是 1000，暴力解每次都要从头扫描找到 `[`，再复制子串，整体工作量大约是 1000 × 1000 次字符操作。

- **空间复杂度**：`O(n)`  
  > 只保存了最终的结果字符串，额外的临时变量占用常数空间。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于**反复遍历整个字符串**，尤其是寻找匹配的 `]`。我们可以一次遍历字符串，同时利用**栈（Stack）**来记录**当前的重复次数**和**已经构建好的子串**，这样每个字符只处理一次。

**核心想法**：

1. **遍历字符** `s[i]`。  
2. 如果是 **数字**，说明后面会有一个 `[`，我们把这个数字（可能是多位数）压入 `count_stack`。  
3. 如果是 **左括号 `[`**，表示进入一个新的子层级，此时把当前已经拼好的字符串压入 `string_stack`，并把 `curr_str` 置空，准备收集新层级的字符。  
4. 如果是 **字母**，直接追加到 `curr_str`（当前层级的结果）。  
5. 如果是 **右括号 `]`**，说明当前层级结束：  
   - 从 `count_stack` 弹出对应的重复次数 `k`。  
   - 从 `string_stack` 弹出上一层级已经得到的字符串 `prev_str`。  
   - 把 `curr_str` 重复 `k` 次后，拼接到 `prev_str`，得到上一层级的新的 `curr_str`。  
6. 最终遍历结束时，`curr_str` 就是完整的解码结果。

> 类比：想象你在写信，遇到“把下面这段话重复 3 次”。你把这句话 **暂时放进抽屉**（栈），去写那段话，写完后再取出来重复粘贴，然后继续写信。抽屉（栈）保证了**后进先出**的顺序，正好对应括号的嵌套关系。

**为什么正确**：  
- 栈的 **后进先出** 正好对应 **括号的嵌套**（内层先结束，外层后结束）。  
- 每次遇到 `]`，我们一定已经完整收集了对应的 `encoded_string`，因此可以立刻完成一次展开，不需要再次遍历。

**复杂度分析**  
- 我们只 **遍历一次** 输入字符串，每个字符的处理都是 O(1)（压栈、弹栈、字符串拼接）。  
- 字符串拼接在 Python 中使用 `+=` 会产生新对象，但整体拼接的字符总数等于最终输出长度 `n`，因此总体时间仍是 **`O(n)`**。  
- 额外使用的栈最多保存 **嵌套层数**，最坏情况下每个字符都是 `[`，层数为 `len(s)`，所以 **空间是 `O(m)`**（`m` 为嵌套深度），加上输出字符串本身的空间 `O(n)`。

#### 代码（Python）

```python
def decodeString(s: str) -> str:
    count_stack = []   # 用来保存每一层的重复次数 k
    string_stack = []  # 用来保存每一层已经构建好的字符串
    curr_str = []      # 当前层级正在构建的字符列表（使用列表更高效）
    i = 0
    n = len(s)

    while i < n:
        if s[i].isdigit():
            # 读取完整的数字（可能是多位数），比如 "12["
            num = 0
            while i < n and s[i].isdigit():
                num = num * 10 + int(s[i])
                i += 1
            count_stack.append(num)   # 把 k 入栈
        elif s[i] == '[':
            # 进入新层级，先把当前已经得到的字符串入栈
            string_stack.append(''.join(curr_str))
            curr_str = []   # 重置，准备收集新层级的字符
            i += 1
        elif s[i] == ']':
            # 当前层结束，弹出对应的 k 与上一层的字符串
            k = count_stack.pop()
            prev = string_stack.pop()
            # 将当前层的内容重复 k 次，再拼接到上一层
            curr_str = list(prev + ''.join(curr_str) * k)
            i += 1
        else:
            # 普通字母，直接加入当前层
            curr_str.append(s[i])
            i += 1

    return ''.join(curr_str)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  > `n` 是最终输出的长度。我们只遍历一次原字符串，所有栈操作和拼接的工作量累计等于输出的字符数。

- **空间复杂度**：`O(m + n)`（其中 `m` 为最大括号嵌套深度）  
  > 额外的栈最多存 `m` 个整数和 `m` 段字符串，加上最终返回的结果 `n`。

---

## 心得

- 这道题考察的核心技巧是 **使用栈模拟嵌套结构**（或递归实现相同逻辑）。  
- 该技巧常见于：  
  1. **括号匹配**（Valid Parentheses）  
  2. **中缀表达式转后缀**（Infix to Postfix）  
  3. **字符串解析**（如 LeetCode 394：Decode String）  
- **一句话总结解题钥匙**：**“用栈把每一层的计数和已构建的子串保存下来，遇到右括号时弹栈完成一次展开”。**

## 反思

- **第一反应**：看到 `k[encoded]` 立刻想到递归或栈，因为它天然形成“先处理内部，再返回外部”的层次结构。  
- **最容易踩的坑**：  
  - 多位数的 `k`（如 `12[ab]`）不能只读取单个字符，需要循环累计。  
  - 字符串拼接若频繁使用 `+` 会导致 **O(n²)** 的隐式开销，推荐使用列表或 `''.join`。  
  - 需要确保在遇到 `[` 时把 **当前已收集的字符** 入栈，否则会丢失外层已经得到的部分。  
- **下次遇到同类题**，第一步应该想到：**“这是不是一个嵌套的、需要在结束时回溯的过程？”**如果答案是“是”，优先考虑 **栈**（或递归）来维护状态。