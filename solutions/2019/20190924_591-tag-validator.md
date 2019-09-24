# #591. 标签验证器 / Tag Validator

> 难度：困难 · 标签：String、Stack · [LeetCode 链接](https://leetcode.com/problems/tag-validator/)

---

## 题目（英文原版）

**Description**

Given a string representing a code snippet, implement a tag validator to parse the code and return whether it is valid.
A code snippet is valid if all the following rules hold:

**Examples**

**Example 1:**

```
Input: code = "<DIV>This is the first line <![CDATA[<div>]]></DIV>"
Output: true
Explanation: 
The code is wrapped in a closed tag : <DIV> and </DIV>. 
The TAG_NAME is valid, the TAG_CONTENT consists of some characters and cdata. 
Although CDATA_CONTENT has an unmatched start tag with invalid TAG_NAME, it should be considered as plain text, not parsed as a tag.
So TAG_CONTENT is valid, and then the code is valid. Thus return true.
```

**Example 2:**

```
Input: code = "<DIV>>>  ![cdata[]] <![CDATA[<div>]>]]>]]>>]</DIV>"
Output: true
Explanation:
We first separate the code into : start_tag|tag_content|end_tag.
start_tag -> "<DIV>"
end_tag -> "</DIV>"
tag_content could also be separated into : text1|cdata|text2.
text1 -> ">>  ![cdata[]] "
cdata -> "<![CDATA[<div>]>]]>", where the CDATA_CONTENT is "<div>]>"
text2 -> "]]>>]"
The reason why start_tag is NOT "<DIV>>>" is because of the rule 6.
The reason why cdata is NOT "<![CDATA[<div>]>]]>]]>" is because of the rule 7.
```

**Example 3:**

```
Input: code = "<A>  <B> </A>   </B>"
Output: false
Explanation: Unbalanced. If "<A>" is closed, then "<B>" must be unmatched, and vice versa.
```

**Constraints**

- 1 <= code.length <= 500
- code consists of English letters, digits, '<', '>', '/', '!', '[', ']', '.', and ' '.

---

## 题目（中文翻译）

给定一个表示代码片段（code snippet）的字符串，实现一个标签验证器（tag validator）来解析该代码，并返回它是否有效。  
如果代码片段满足以下所有规则，则视为有效：

（原题目中未列出具体规则，这里保持原样）

## 示例

### 示例 1
**输入**  
``` 
code = "<DIV>This is the first line <![CDATA[<div>]]></DIV>"
```  
**输出**  
```
true
```  
**解释**  
代码被闭合标签 `<DIV>` 和 `</DIV>` 包裹。  
`TAG_NAME` 是合法的，`TAG_CONTENT` 由普通字符和 CDATA（`<![CDATA[...]]>`）组成。  
虽然 CDATA 内容中出现了一个未匹配的起始标签且其 `TAG_NAME` 无效，但它应被视为普通文本，不会被解析为标签。  
因此 `TAG_CONTENT` 合法，整个代码片段也合法，返回 `true`。

### 示例 2
**输入**  
``` 
code = "<DIV>>>  ![cdata[]] <![CDATA[<div>]>]]>]]>>]</DIV>"
```  
**输出**  
```
true
```  
**解释**  
我们先把代码拆分为：`start_tag|tag_content|end_tag`。  
- `start_tag` → `"<DIV>"`  
- `end_tag`   → `"</DIV>"`  

`tag_content` 还能进一步拆分为：`text1|cdata|text2`。  
- `text1` → `">>  ![cdata[]] "`  
- `cdata` → `<![CDATA[<div>]>]]>`，其中 `CDATA_CONTENT` 为 `"<div>]>"`  
- `text2` → `"]]>>>]"`  

之所以 `start_tag` 不是 `"<DIV>>>"`，是因为规则 6 的限制。  
之所以 `cdata` 不是 `<![CDATA[<div>]>]]>]]>`，是因为规则 7 的限制。

### 示例 3
**输入**  
``` 
code = "<A>  <B> </A>   </B>"
```  
**输出**  
```
false
```  
**解释**  
标签不平衡。若 `"<A>"` 被闭合，则 `"<B>"` 必须未匹配，反之亦然。

## 约束条件
- `1 <= code.length <= 500`
- `code` 只包含英文字母、数字、字符 `<`, `>`, `/`, `!`, `[`, `]`, `.`, 以及空格。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把整段代码 **从左到右** 扫一遍，每次遇到字符 `<` 就去找下一个 `>`，把两者之间的内容当作一个“标签”。如果找不到 `>`，说明格式不合法，直接返回 `False`。  

- **标签的种类**  
  - **开始标签**：形如 `<TAG_NAME>`，`TAG_NAME` 必须全部是大写字母，且长度在 1~9 之间。  
  - **结束标签**：形如 `</TAG_NAME>`，`TAG_NAME` 必须和最近的未匹配的开始标签相同。  
  - **CDATA**：形如 `<![CDATA[...]]>`，内部的内容 **不再解析**，直接视作普通字符。  

- **生活化类比**  
  - **栈**（这里的暴力实现不使用栈）就像一本 **“打开的书”**，每读进一个章节标题（开始标签）就把它放到书的左边；当读到章节结束（结束标签）时，就把对应的标题从左边拿走，检查是否匹配。  
  - **哈希表**（如果我们用字典记下已出现的标签）就像 **字典**，把单词当成键（key），解释放在页码（value）上。  

- **为什么这个方法能判断合法性**  
  只要我们能够 **完整地把每一个标签都切分出来**，并且严格检查它们是否符合规则（名字合法、配对正确、CDATA 正确闭合），那么整个字符串必然满足题目要求。  

- **时间/空间复杂度**  
  - 对每个字符 `i`，我们都要向后寻找最近的 `>`（最坏情况要遍历到字符串末尾），这相当于 **两层循环**，时间复杂度是 **O(n²)**，其中 `n` 为代码长度。  
  - 只使用常数级别的额外变量（比如 `i`、`j`、临时字符串），空间复杂度是 **O(1)**。  

> **大白话**：如果代码长 500，最坏情况下我们要检查 500×500≈25 万次字符，这在电脑眼里不算慢，但在算法课上我们总是追求更好的“线性”表现。

#### 代码（Python）  

```python
def isValid_bruteforce(code: str) -> bool:
    n = len(code)

    # 1️⃣ 必须以完整的开始标签开头，且只能有一个根标签
    if n == 0 or code[0] != '<':
        return False

    # 记录根标签的名字，后面出现的根标签必须匹配它
    root_tag = None
    i = 0

    while i < n:
        # -------------------------------------------------
        #   第一步：找下一个 '>'
        # -------------------------------------------------
        j = code.find('>', i + 1)          # O(n) 的线性查找
        if j == -1:                         # 没有匹配的 '>'
            return False

        token = code[i + 1:j]               # 两个尖括号之间的内容

        # -------------------------------------------------
        #   第二步：判断 token 是哪种标签
        # -------------------------------------------------
        #   1) CDATA
        if token.startswith('![CDATA['):
            # CDATA 必须以 "]]>" 结束
            end_cdata = code.find(']]>', j + 1)
            if end_cdata == -1:             # 没有闭合的 CDATA
                return False
            # CDATA 之间的内容直接跳过，不再解析
            i = end_cdata + 3
            continue

        #   2) 结束标签
        if token.startswith('/'):
            tag_name = token[1:]
            # 检查标签名是否合法
            if not (1 <= len(tag_name) <= 9) or not tag_name.isupper():
                return False
            # 必须已经出现过对应的开始标签
            if root_tag is None or tag_name != root_tag:
                return False
            # 结束标签必须是字符串的最后一个标签
            if j != n - 1:
                return False
            return True

        #   3) 开始标签
        tag_name = token
        if not (1 <= len(tag_name) <= 9) or not tag_name.isupper():
            return False
        # 第一次出现的开始标签视为根标签
        if root_tag is None:
            root_tag = tag_name
        # 其余开始标签在本暴力实现里不做嵌套检查
        i = j + 1
        # -------------------------------------------------
        #   第四步：继续向后扫描
        # -------------------------------------------------
        continue

    # 循环结束仍未匹配结束标签，非法
    return False
```

> 代码中每一行的注释都用中文写明了它的作用，直接复制运行即可。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - `code.find('>', i+1)` 每次最坏会遍历剩余的字符，形成两层循环。  
  - 对于长度 500 的字符串，大约需要 125 000 次字符比较。  

- **空间复杂度**：`O(1)`  
  - 只用了若干整数指针和临时字符串，不随输入规模增长而增长。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**主要的性能瓶颈** 在于每次都要从当前位置向后线性搜索 `>`，导致 **二次遍历**。  
如果我们在一次遍历的过程中，同时维护一个 **栈** 来记录尚未闭合的开始标签，就可以 **把所有的匹配工作合并到一次扫描**，时间降到线性 `O(n)`。

**关键点**  

1. **栈（stack）**  
   - 把每一次出现的合法开始标签压入栈。  
   - 遇到结束标签时，弹出栈顶并检查是否匹配。  
   - 栈为空且遍历完全部字符，说明所有标签都配对完毕。  

2. **CDATA 处理**  
   - 当检测到 `<![CDATA[` 时，直接寻找下一个 `]]>`（这也是一次线性搜索，但整个字符串只会被遍历一次）。  
   - CDATA 之间的内容不再解析，直接跳过。  

3. **根标签限制**  
   - 题目要求 **整个代码必须被唯一的根标签包裹**，即在整个字符串结束前，栈的深度只能为 1。  
   - 当栈为空时，后面不能再出现任何字符（除了可能的结束标签本身）。  

4. **合法字符检查**  
   - 标签名只能是 1~9 个大写字母。  
   - CDATA 必须完整闭合。  

**一步步推导**  

- **步骤 1**：遍历字符串 `code`，用指针 `i` 表示当前处理的位置。  
- **步骤 2**：如果 `code[i]` 不是 `'<'`，说明是普通字符，只能出现在已经打开的标签内部（栈不为空），否则非法。  
- **步骤 3**：若遇到 `'<'`，进一步判断三种可能：  
  - **CDATA**：`code[i:i+9] == "<![CDATA["` → 寻找最近的 `"]]>`"，若找不到返回 `False`，否则 `i` 跳到 `"]]>`" 之后。  
  - **结束标签**：`code[i+1] == '/'` → 读取标签名，检查是否合法并与栈顶匹配，弹栈。若弹后栈为空且 `i` 不是字符串末尾，返回 `False`（根标签已经闭合，后面不应再有字符）。  
  - **开始标签**：否则视为开始标签 → 读取标签名，检查合法性，压栈。若此时栈的大小为 1 且 `i` 不是 0，说明根标签不是最前面的字符，返回 `False`。  

- **步骤 4**：遍历结束后，检查栈是否为空，只有为空才是合法的代码。  

**类比**：  
把栈想象成 **“进出场的门票”**，进入时拿一张票（开始标签），离开时必须交回同样的票（结束标签）。如果有人在没有票的情况下离开，或者票的名字不匹配，系统就会报错。

#### 代码（Python）  

```python
def isValid(code: str) -> bool:
    n = len(code)
    stack = []               # 用来保存未闭合的开始标签
    i = 0

    while i < n:
        # -------------------------------------------------
        #   1) 必须以 '<' 开头才能继续解析
        # -------------------------------------------------
        if code[i] != '<':
            # 若栈为空，说明根标签尚未打开，普通字符非法
            if not stack:
                return False
            i += 1
            continue

        # -------------------------------------------------
        #   2) 判断是 CDATA / 结束标签 / 开始标签
        # -------------------------------------------------
        #   2.1 CDATA
        if i + 9 <= n and code[i:i+9] == "<![CDATA[":
            # 找到最近的 "]]>"
            j = code.find("]]>", i + 9)
            if j == -1:                # 没有闭合的 CDATA
                return False
            i = j + 3                  # 跳过 CDATA 内容
            continue

        #   2.2 结束标签 </TAG>
        if i + 2 <= n and code[i+1] == '/':
            j = code.find('>', i + 2)
            if j == -1:
                return False
            tag_name = code[i+2:j]     # 去掉 </ 和 >
            # 检查标签名是否合法
            if not (1 <= len(tag_name) <= 9) or not tag_name.isupper():
                return False
            # 必须与栈顶的开始标签匹配
            if not stack or stack[-1] != tag_name:
                return False
            stack.pop()                # 配对成功，弹栈

            # 若弹栈后栈为空，说明根标签已经闭合
            # 此时 i 必须正好是字符串的最后一个字符
            if not stack and j != n - 1:
                return False
            i = j + 1
            continue

        #   2.3 开始标签 <TAG>
        j = code.find('>', i + 1)
        if j == -1:
            return False
        tag_name = code[i+1:j]
        # 合法性检查
        if not (1 <= len(tag_name) <= 9) or not tag_name.isupper():
            return False
        # 根标签必须是最外层的第一个字符
        if not stack and i != 0:
            return False
        stack.append(tag_name)        # 入栈
        i = j + 1

    # 循环结束，所有标签必须全部匹配完毕
    return not stack
```

> **代码说明**  
- `stack` 用来保存尚未闭合的开始标签。  
- `code.find` 每次向后搜索一次 `>`（或 `]]>`），整个过程只遍历了字符串一次，**时间复杂度是线性**。  
- 每一次标签解析后，指针 `i` 都会直接跳到下一个未处理字符，避免了重复扫描。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只进行一次线性遍历，每个字符最多被访问常数次（一次普通字符检查、一次 `find`），所以整体是线性时间。  
  - 与暴力解的 `O(n²)` 相比，速度提升了数量级（500 长度时从约 25 万次下降到 500 次左右）。  

- **空间复杂度**：`O(m)`，其中 `m` 为同时打开的标签层数（栈的最大深度）。  
  - 最坏情况下全部是嵌套标签，`m` ≤ `n/2`，但在实际限制（500）下仍然是常数级别的额外空间。  

---  

## 心得  

- **核心技巧**：**栈**（stack）配合一次线性扫描，实现标签的配对与嵌套校验。  
- **适用的题型**  
  1. **括号匹配**（LeetCode 20）  
  2. **删除最外层括号**（LeetCode 1021）  
  3. **检查 HTML/XML 合法性**（类似本题）  
- **一句话总结解题钥匙**：  
  > 用栈把“进”与“出”配对，遇到 CDATA 时直接跳过，确保根标签唯一且完整闭合。  

---  

## 反思  

- **第一反应**：看到大量的 `<`、`>`、`CDATA`，立刻想到 “逐个匹配、用栈维护”。  
- **最容易踩的坑**  
  - **根标签位置**：根标签必须是字符串的第一个字符，且在根标签闭合前不能出现普通字符。  
  - **CDATA 的结束标记**：必须是 `]]>`，而不是单纯的 `]` 或 `>`，否则会误判。  
  - **标签名合法性**：只能是大写字母，长度 1~9，忘记检查长度会导致错误。  
  - **结束标签后不能有额外字符**：根标签闭合后，后面必须是字符串末尾。  
- **下次遇到同类题的第一步**：  
  - **先确定是否可以用“一次遍历 + 栈”** 来完成配对；若可以，就直接实现这种线性解法。  

祝你在算法的道路上越走越顺！ 🚀