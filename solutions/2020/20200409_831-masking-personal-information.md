# #831. 隐藏个人信息 / Masking Personal Information

> 难度：中等 · 标签：String · [LeetCode 链接](https://leetcode.com/problems/masking-personal-information/)

---

## 题目（英文原版）

**Description**

You are given a personal information string s, representing either an email address or a phone number. Return the masked personal information using the below rules.
Email address:
An email address is:
To mask an email:
Phone number:
A phone number is formatted as follows:
To mask a phone number:

**Examples**

**Example 1:**

```
Input: s = "LeetCode@LeetCode.com"
Output: "l*****e@leetcode.com"
Explanation: s is an email address.
The name and domain are converted to lowercase, and the middle of the name is replaced by 5 asterisks.
```

**Example 2:**

```
Input: s = "AB@qq.com"
Output: "a*****b@qq.com"
Explanation: s is an email address.
The name and domain are converted to lowercase, and the middle of the name is replaced by 5 asterisks.
Note that even though "ab" is 2 characters, it still must have 5 asterisks in the middle.
```

**Example 3:**

```
Input: s = "1(234)567-890"
Output: "***-***-7890"
Explanation: s is a phone number.
There are 10 digits, so the local number is 10 digits and the country code is 0 digits.
Thus, the resulting masked number is "***-***-7890".
```

**Constraints**

- s is either a valid email or a phone number.
- If s is an email:
	
8 <= s.length <= 40
s consists of uppercase and lowercase English letters and exactly one '@' symbol and '.' symbol.
- 8 <= s.length <= 40
- s consists of uppercase and lowercase English letters and exactly one '@' symbol and '.' symbol.
- If s is a phone number:
	
10 <= s.length <= 20
s consists of digits, spaces, and the symbols '(', ')', '-', and '+'.
- 10 <= s.length <= 20
- s consists of digits, spaces, and the symbols '(', ')', '-', and '+'.

---

## 题目（中文翻译）

**描述**  
给定一个个人信息字符串 `s`，它表示一个电子邮件地址（email）或一个电话号码（phone number）。请按照下列规则返回经过掩码处理后的个人信息。

### 电子邮件地址（email）  
- 电子邮件的格式为 `name@domain`，其中 `name` 为用户名，`domain` 为域名。  
- 掩码规则：
  1. 将 `name` 和 `domain` 都转换为小写字母。  
  2. 将 `name` 的首字母保留为小写，末尾字母也保留为小写，其余字符全部替换为 **5 个星号（asterisk）** `*`。  
  3. 最终格式为 `first*5*last@domain`，例如 `LeetCode@LeetCode.com` → `l*****e@leetcode.com`。

### 电话号码（phone number）  
- 电话号码的原始字符串可能包含数字、空格、以及符号 `'('`、`')'`、`'-'`、`'+'`。  
- 首先去除所有非数字字符，仅保留数字字符。记保留下来的数字总数为 `n`。  
- 最后 10 位数字构成 **本地号码（local number）**，前面的 `n‑10` 位构成 **国家码（country code）**（若 `n = 10` 则没有国家码）。  
- 掩码规则：  
  1. 本地号码的前 6 位全部用 `***-***-` 形式的星号掩码表示，只保留最后 4 位数字。  
  2. 若存在国家码，则在最前面加上 `+`，随后跟随与国家码位数相同数量的星号，再加一个 `-`。  
  3. 最终格式为  
     - 无国家码：`***-***-XXXX`  
     - 有国家码：`+***...-***-***-XXXX`（`*` 的数量与国家码位数相同）  

### 示例

**示例 1**  
``` 
Input: s = "LeetCode@LeetCode.com"
Output: "l*****e@leetcode.com"
Explanation: s 是一个电子邮件地址。用户名和域名均被转为小写，用户名中间的字符被 5 个星号替换。
```

**示例 2**  
``` 
Input: s = "AB@qq.com"
Output: "a*****b@qq.com"
Explanation: s 是一个电子邮件地址。用户名和域名均被转为小写，尽管用户名只有 2 个字符，仍然需要在中间放置 5 个星号。
```

**示例 3**  
``` 
Input: s = "1(234)567-890"
Output: "***-***-7890"
Explanation: s 是一个电话号码。去除非数字字符后得到 10 位数字，所以没有国家码，掩码结果为 "***-***-7890"。
```

### 约束条件
- `s` 要么是合法的电子邮件地址，要么是合法的电话号码。  
- 若 `s` 为电子邮件地址：  
  - `8 <= s.length <= 40`  
  - `s` 只包含大小写英文字母，且恰好包含一个 `'@'` 符号和一个 `'.'` 符号。  
- 若 `s` 为电话号码：  
  - `10 <= s.length <= 20`  
  - `s` 只包含数字、空格以及符号 `'('`、`')'`、`'-'`、`'+'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
这道题的核心其实是 **把字符串按照两种不同的格式分别处理**，没有需要遍历多次或递归的复杂操作。  
- 首先判断输入 `s` 是邮箱还是手机号。**判断方式**：如果字符串里出现 `'@'`，必然是邮箱；否则就是手机号。  
- **邮箱的处理**  
  1. 把整个字符串全部转成小写（相当于把所有字母都查字典，统一成同一本词典的页码）。  
  2. 找到 `'@'` 前面的名字部分 `name`，记住它的第一个字符 `first` 和最后一个字符 `last`。  
  3. 用 5 个星号 `*****` 把中间的字符全部遮盖，然后拼接 `first + "*****" + last + domain`。  
- **手机号的处理**  
  1. 把所有非数字字符（空格、括号、`-`、`+`）全部剔除，只留下数字序列 `digits`。这一步就像把一堆杂乱的信件只挑出邮政编码那几位数字。  
  2. 根据数字总数判断是否有国家码：  
     - 10 位 → 没有国家码。  
     - >10 位 → 前面的 `len(digits) - 10` 位是国家码。  
  3. 按照要求拼接掩码：  
     - 前面 3 位和中间 3 位始终显示为 `***-***-`。  
     - 最后 4 位直接保留。  
     - 如果有国家码，需要在最前面加上 `+` 再跟对应数量的 `*`（如 `+**-***-***-xxxx`）。  

> 为什么这样做一定对？  
> - 题目已经明确了两类输入的格式，只要我们严格按照规则把对应位置的字符替换成 `*`（或保留），就一定满足要求。  
> - 只要遍历一次字符串就能得到所有数字或找到 `'@'`，不需要额外的搜索或排序。

#### 代码（Python）

```python
def maskPII(s: str) -> str:
    # 如果出现 '@'，说明是邮箱
    if '@' in s:
        # 统一转小写
        s = s.lower()
        # 分割出名字和域名
        name, domain = s.split('@')
        # 只保留首尾字符，其他全部用 5 个星号代替
        masked_name = name[0] + "*****" + name[-1]
        return masked_name + '@' + domain

    # 否则是手机号
    # 只保留数字，其他符号全部丢掉
    digits = [ch for ch in s if ch.isdigit()]
    digits = ''.join(digits)            # 把列表拼成字符串

    # 最后四位直接保留
    local = digits[-4:]

    # 判断是否有国家码
    if len(digits) == 10:               # 没有国家码
        return f"***-***-{local}"
    else:                               # 有国家码，需要在最前面加上 '+' 和对应数量的 '*'
        country_len = len(digits) - 10
        country_mask = '+' + '*' * country_len + '-'
        return f"{country_mask}***-***-{local}"
```

#### 复杂度  

- **时间复杂度：O(n)** — 这里的 `n` 是字符串 `s` 的长度。我们只遍历了一遍（或者两遍：一次找 `@`，一次收集数字），每一步都是常数时间操作。  
  > 大白话：不管 `s` 有多长，我们的程序跑的步数和字符数是成正比的，最多走一次全长的路。

- **空间复杂度：O(1)（不计输出）** — 只用了常数个额外变量（如 `name`、`domain`、`digits` 列表）。如果把最终返回的字符串算进来，就是 O(n)，因为要把结果写出来。  
  > 大白话：除了存放答案之外，我们几乎没有占用额外的“盒子”。

---

### 2. 最优解

#### 思路  
在本题中，“最优”其实就是 **一次遍历完成所有工作**，避免重复的字符串切片或不必要的列表创建。  
- **统一遍历**：在一次循环里同时判断字符是否是 `'@'`，并且把数字收集起来。这样可以在 **O(n)** 时间内得到：
  - 是否为邮箱（出现 `@` 的位置）  
  - 所有数字（用于手机号掩码）  
- **后续处理**：根据是否找到 `@` 决定后面的拼接方式。  
  - 对于邮箱，只需要记录 `@` 前后第一个和最后一个字符的下标，直接在原字符串上切片，不需要额外的 `split`。  
  - 对于手机号，已经在遍历时得到纯数字序列，直接按照长度拼接即可。

> 核心技巧：**一次遍历 + 条件分支**，这在很多需要“先判断类型再处理”的字符串题目中非常常见。把所有信息一次性收集完，再统一决策，能够最大限度地减少不必要的遍历次数和临时对象。

#### 代码（Python）

```python
def maskPII(s: str) -> str:
    # 记录是否出现 '@'，以及它的下标
    at_idx = -1
    # 用列表收集所有数字字符（手机号需要）
    digits = []

    # 单次遍历整个字符串
    for i, ch in enumerate(s):
        if ch == '@':
            at_idx = i                     # 记住 '@' 的位置
        if ch.isdigit():
            digits.append(ch)              # 把数字保存下来

    # ------------------- 处理邮箱 -------------------
    if at_idx != -1:                       # 出现了 '@'，必是邮箱
        # 直接在原字符串上取首尾字符，省去 split 的开销
        first = s[0].lower()
        last = s[at_idx - 1].lower()       # '@' 前的最后一个字符
        domain = s[at_idx + 1:].lower()    # '@' 之后的全部（包括 '.'）
        return f"{first}*****{last}@{domain}"

    # ------------------- 处理手机号 -------------------
    # 把数字列表拼成字符串
    num = ''.join(digits)

    # 最后四位
    local = num[-4:]

    if len(num) == 10:                     # 没有国家码
        return f"***-***-{local}"
    else:                                  # 有国家码
        country_len = len(num) - 10
        # 前面的国家码用 + 和对应数量的 * 表示
        return f"+{'*' * country_len}-***-***-{local}"
```

#### 复杂度  

- **时间复杂度：O(n)**  
  - 只遍历一次字符串，所有判断、收集、记录都在同一次循环里完成。  
  - 相比直觉解的两次遍历（一次判断一次 `split`），这里省去了额外的线性遍历，常数因子更小。

- **空间复杂度：O(n)**（仅限于存放数字的列表）  
  - 需要额外的 `digits` 列表保存所有数字，最坏情况下和原字符串等长。  
  - 其它变量都是常数空间。  

> 与暴力解对比：时间复杂度相同都是 O(n)，但最优解的常数更小，实际运行更快，且代码思路更统一，易于扩展。

---

## 心得

- **核心技巧**：一次遍历收集信息 + 条件分支决定后续处理。  
- **适用的题型**  
  1. 判别并处理不同格式的字符串（如邮箱/手机号、URL/路径等）。  
  2. 需要在同一次扫描中提取特定字符集合（如只要数字、只要字母）。  
  3. “掩码”类题目：对敏感信息进行统一格式化输出。  
- **解题钥匙**：**先把所有必须的信息一次性拿到手，再统一决定怎么拼接**。

---

## 反思

- **第一反应**：看到 `'@'` 就想到邮箱，看到数字、`+`、`-`、`(`、`)` 就想到手机号，直接按照题目描述去替换。  
- **最容易踩的坑**  
  - 忘记把邮箱的 **整个**字符串转成小写，只转了名字或域名。  
  - 对手机号没有正确去掉所有非数字字符，导致数字计数错误。  
  - 国家码长度为 0 时仍错误地在最前面加上 `+`。  
- **下次遇到同类题**：第一步先 **遍历一次**，在遍历中记录“类型标志”和“关键子串（如数字）”，再根据标志统一输出。这样可以避免多余的遍历和临时对象，代码更简洁、效率更高。