# #2047. 句子中有效单词的数目 / Number of Valid Words in a Sentence

> 难度：简单 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/number-of-valid-words-in-a-sentence/)

---

## 题目（英文原版）

**Description**

A sentence consists of lowercase letters ('a' to 'z'), digits ('0' to '9'), hyphens ('-'), punctuation marks ('!', '.', and ','), and spaces (' ') only. Each sentence can be broken down into one or more tokens separated by one or more spaces ' '.
A token is a valid word if all three of the following are true:
Examples of valid words include "a-b.", "afad", "ba-c", "a!", and "!".
Given a string sentence, return the number of valid words in sentence.

**Examples**

**Example 1:**

```
Input: sentence = "cat and  dog"
Output: 3
Explanation: The valid words in the sentence are "cat", "and", and "dog".
```

**Example 2:**

```
Input: sentence = "!this  1-s b8d!"
Output: 0
Explanation: There are no valid words in the sentence.
"!this" is invalid because it starts with a punctuation mark.
"1-s" and "b8d" are invalid because they contain digits.
```

**Example 3:**

```
Input: sentence = "alice and  bob are playing stone-game10"
Output: 5
Explanation: The valid words in the sentence are "alice", "and", "bob", "are", and "playing".
"stone-game10" is invalid because it contains digits.
```

**Constraints**

- 1 <= sentence.length <= 1000
- sentence only contains lowercase English letters, digits, ' ', '-', '!', '.', and ','.
- There will be at least 1 token.

---

## 题目（中文翻译）

**题目描述**

一个句子（sentence）仅由小写字母（'a' 到 'z'）、数字（'0' 到 '9'）、连字符（'-'）、标点符号（'!'、'.'、','）以及空格（' '）组成。每个句子可以被拆分成一个或多个由一个或多个空格分隔的 token（子串）。

若一个 token 同时满足以下全部三条条件，则它是一个有效单词（valid word）：

1. 只能包含小写字母、连字符和/或标点符号，**不能** 包含数字。
2. 最多只能出现一次连字符（'-'），且该连字符必须位于两个小写字母之间（即不能是首字符或尾字符，且前后字符必须都是字母）。
3. 最多只能出现一次标点符号（'!'、'.'、','），若出现，则该标点符号必须是 token 的最后一个字符。

符合条件的有效单词示例包括 `"a-b."`、`"afad"`、`"ba-c"`、`"a!"` 和 `"!"`。

给定字符串 `sentence`，返回句子中有效单词的数量。

**示例**

*示例 1*  
输入：`sentence = "cat and  dog"`  
输出：`3`  
解释：句子中的有效单词是 `"cat"`、`"and"` 和 `"dog"`。

*示例 2*  
输入：`sentence = "!this  1-s b8d!"`  
输出：`0`  
解释：句子中没有有效单词。  
- `"!this"` 无效，因为它以标点符号开头。  
- `"1-s"` 和 `"b8d"` 无效，因为它们包含数字。

*示例 3*  
输入：`sentence = "alice and  bob are playing stone-game10"`  
输出：`5`  
解释：句子中的有效单词是 `"alice"`、`"and"`、`"bob"`、`"are"` 和 `"playing"`。  
`"stone-game10"` 无效，因为它包含数字。

**约束条件**

- `1 <= sentence.length <= 1000`
- `sentence` 只包含小写英文字母、数字、空格 `' '`、连字符 `'-'`、以及标点符号 `'!'`、`'.'`、`','`。
- 至少存在一个 token。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **先把句子切成 token**  
   句子里的单词之间用空格 `' '` 隔开，连续的空格算作分隔符。把整个字符串 `sentence.split(' ')`，再把空串过滤掉，就得到所有「词块」(`token`)。

2. **逐个 token 按规则检查**  
   - **字母**：`a`~`z`，只要出现就算合法（不需要计数，只要不是非法字符就行）。  
   - **数字**：只要 token 中出现数字，就直接判为 **非法**。  
   - **连字符 `-`**：  
     - 只能出现 **一次**；  
     - 不能在开头或结尾；  
     - 必须左、右两边都是字母（相当于「-」两边都要是单词的组成部分）。  
   - **标点符号 `! . ,`**：  
     - 只能出现 **一次**；  
     - 必须在 token 的 **最后**，不能出现在中间。  

   这里的「检查」可以用 **三次遍历** 完成：  
   - 第一次遍历统计数字出现次数；  
   - 第二次遍历统计连字符出现次数并检查它的左右字符；  
   - 第三次遍历统计标点出现次数并检查它是否在末尾。  

   只要有一次检查不通过，就把这个 token 标记为非法。所有合法的 token 数目即为答案。

> **类比**：把每个 token 想象成一本小册子，  
> - 检查数字就像在册子里找“数字页码”，一出现就直接说这本册子不合格；  
> - 检查连字符就像找唯一的“插页”，它必须正好在两页文字之间；  
> - 检查标点符号就像找唯一的“封底标记”，只能在最后一页出现。

#### 代码（Python）

```python
def countValidWords(sentence: str) -> int:
    # 1. 按空格切割，过滤掉空串
    tokens = [t for t in sentence.split(' ') if t]   # 过滤连续空格产生的空 token
    valid_cnt = 0

    for token in tokens:
        # --------- 1. 检查是否包含数字 ----------
        has_digit = any(ch.isdigit() for ch in token)
        if has_digit:
            continue                # 有数字直接不是合法单词

        # --------- 2. 检查连字符 ----------
        hyphen_pos = -1               # 记录连字符出现的位置
        hyphen_cnt = 0
        for i, ch in enumerate(token):
            if ch == '-':
                hyphen_cnt += 1
                hyphen_pos = i
        # 连字符出现次数 >1，或出现在首尾，或左右不是字母，都不合法
        if hyphen_cnt > 1:
            continue
        if hyphen_cnt == 1:
            if hyphen_pos == 0 or hyphen_pos == len(token) - 1:
                continue
            if not (token[hyphen_pos - 1].isalpha() and token[hyphen_pos + 1].isalpha()):
                continue

        # --------- 3. 检查标点 ----------
        punct_cnt = sum(ch in "!., " for ch in token)  # 注意空格已经不在 token 中
        if punct_cnt > 1:
            continue
        if punct_cnt == 1 and token[-1] not in "!.,":   # 标点必须在末尾
            continue

        # 通过所有检查，计数加一
        valid_cnt += 1

    return valid_cnt
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`  
  - `n` 为 token 的数量，`m` 为每个 token 的长度。  
  - 因为我们对每个 token 做了三次遍历（数字、连字符、标点），最坏情况是 `3 * m`，常数可以忽略，整体是 **线性** 的 `O(total_characters)`。  
  - 用大白话讲，就是「看一遍句子里的每个字符」——不管句子有多长，时间都随字符数等比例增长。

- **空间复杂度**：`O(k)`  
  - `k` 为 token 列表的数量（最坏情况下等于句子长度），主要是存放切分后的子串。  
  - 额外的变量都是常数级别的，故整体是 **线性** 的 `O(n)`，但如果把切分的结果视为输入的一部分，也可以说是 **O(1)** 额外空间。

---

### 2. 最优解

#### 思路  

上面的「暴力」解已经是 **线性** 的，只要遍历一次字符就能完成所有检查。  
可以把 **三次遍历** 合并成 **一次遍历**，在遍历 token 时同步记录：

- 是否出现过数字  
- 连字符出现次数以及它左、右是否为字母  
- 标点出现次数以及它是否在末尾  

一次遍历的好处是 **只看一次字符**，更省时间，代码也更简洁。  
下面的实现把所有规则压缩到一个 `for` 循环里，用几个布尔变量和计数器维护状态。

> **类比**：把 token 当成一条生产线，  
> - 每经过一个字符，就让「质量检查员」同时检查「数字、连字符、标点」三项。  
> - 只要有任意一项不合格，立刻把这条产品标记为「不合格」并停止检查。

#### 代码（Python）

```python
def countValidWords(sentence: str) -> int:
    # 1. 按空格切割，过滤掉空串
    tokens = [t for t in sentence.split(' ') if t]
    ans = 0

    for token in tokens:
        # 初始化状态
        has_digit = False          # 是否出现数字
        hyphen_cnt = 0             # 连字符出现次数
        punct_cnt = 0              # 标点出现次数
        valid = True               # 当前 token 是否仍可能合法

        for i, ch in enumerate(token):
            if ch.isdigit():
                has_digit = True
                valid = False
                break               # 出现数字直接结束本 token 检查

            if ch == '-':
                hyphen_cnt += 1
                # 连字符规则检查
                if hyphen_cnt > 1 or i == 0 or i == len(token) - 1:
                    valid = False
                    break
                if not (token[i - 1].isalpha() and token[i + 1].isalpha()):
                    valid = False
                    break

            if ch in "!.,":          # 标点符号
                punct_cnt += 1
                # 标点只能出现一次且必须在末尾
                if punct_cnt > 1 or i != len(token) - 1:
                    valid = False
                    break

        # 循环结束后，如果仍然合法则计数
        if valid:
            ans += 1

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(total_characters)`  
  - 每个字符只遍历一次，所有规则在同一次循环里完成。  
  - 与暴力解相比，省去了额外的遍历，常数因子更小，实际运行更快。

- **空间复杂度**：`O(k)`（存放 token 列表）或 **O(1)** 额外空间  
  - 只使用了几个计数器和布尔变量，额外占用的内存不随输入规模增长。

---

## 心得

- **核心技巧**：一次遍历 + 状态机（用变量记录是否出现非法字符）。  
- **适用场景**：  
  1. **字符串合法性检查**（如邮箱、电话号码验证）。  
  2. **路径合法性判定**（如文件路径、URL 规范校验）。  
  3. **自定义语法解析**（如简易编程语言的 token 检验）。  
- **一句话总结**：把所有规则压缩到一次遍历，用几个「开关」记录状态，就能高效判断字符串是否合法。

---

## 反思

- **第一反应**：看到「只含字母、数字、连字符、标点、空格」就想到「先切词，再逐词检查」。
- **最容易踩的坑**：  
  - 连字符两边必须是字母，忘记检查左侧或右侧会导致误判。  
  - 标点只能出现在末尾，若只判断出现次数而不判断位置，同样会错误。  
  - 连续空格会产生空串，需要在切词后过滤掉。  
- **下次遇到同类题**：  
  1. **先明确每条规则的「局部」限制**（出现次数、位置、相邻字符）。  
  2. **思考能否在一次遍历中同时维护这些限制**，把检查过程做成「状态机」。  
  3. **实现时注意边界条件**（首字符、尾字符、空 token 等）。