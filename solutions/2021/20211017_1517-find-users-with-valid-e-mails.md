# #1517. **查找拥有有效电子邮件的用户** / Find Users With Valid E-Mails

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-users-with-valid-e-mails/)

---

## 题目（英文原版）

**Description**

Table: Users
Write a solution to find the users who have valid emails.
A valid e-mail has a prefix name and a domain where:
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| name          | varchar |
| mail          | varchar |
+---------------+---------+
user_id is the primary key (column with unique values) for this table.
This table contains information of the users signed up in a website. Some e-mails are invalid.
```

**Example 2:**

```
Input: 
Users table:
+---------+-----------+-------------------------+
| user_id | name      | mail                    |
+---------+-----------+-------------------------+
| 1       | Winston   | winston@leetcode.com    |
| 2       | Jonathan  | jonathanisgreat         |
| 3       | Annabelle | bella-@leetcode.com     |
| 4       | Sally     | sally.come@leetcode.com |
| 5       | Marwan    | quarz#2020@leetcode.com |
| 6       | David     | david69@gmail.com       |
| 7       | Shapiro   | .shapo@leetcode.com     |
+---------+-----------+-------------------------+
Output: 
+---------+-----------+-------------------------+
| user_id | name      | mail                    |
+---------+-----------+-------------------------+
| 1       | Winston   | winston@leetcode.com    |
| 3       | Annabelle | bella-@leetcode.com     |
| 4       | Sally     | sally.come@leetcode.com |
+---------+-----------+-------------------------+
Explanation: 
The mail of user 2 does not have a domain.
The mail of user 5 has the # sign which is not allowed.
The mail of user 6 does not have the leetcode domain.
The mail of user 7 starts with a period.
```

---

## 题目（中文翻译）

编写查询找出电子邮件地址有效的用户。  
有效的电子邮件（e-mail）由前缀（prefix）和域名（domain）组成，满足以下条件：

- 前缀只能包含小写字母或数字，且长度大于 0；  
- 域名由小写字母或数字组成的若干子段（subdomain）构成，各子段之间使用点号（`.`）分隔，且至少包含一个点号；  
- 整个地址中只能出现一个 `@` 符号，且 `@` 必须位于前缀与域名之间。

返回满足上述条件的用户记录，结果顺序任意。

**示例**

表结构：

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| name          | varchar |
| mail          | varchar |
+---------------+---------+
```

`user_id` 为主键（primary key），唯一标识每一行。该表记录了网站注册用户的信息，其中部分电子邮件无效。

**示例输入**

```
Users 表：
+---------+-----------+----------------------+
| user_id | name      | mail                 |
+---------+-----------+----------------------+
| 1       | Winston   | winston@leetcode.com |
| 2       | Jonathan  | jonathanisgreat      |
| 3       | Annabelle | bella-@leetcode.com  |
| 4       | Sally     | sally.come@leetcode.com |
| 5       | Marwan    | quarz                |
... (已截断)
```

**示例输出**

```
+---------+-----------+----------------------+
| user_id | name      | mail                 |
+---------+-----------+----------------------+
| 1       | Winston   | winston@leetcode.com |
| 4       | Sally     | sally.come@leetcode.com |
+---------+-----------+----------------------+
```

**解释**

- `winston@leetcode.com` 符合前缀和域名的规则，故被保留。  
- `jonathanisgreat` 缺少 `@` 符号，属于无效电子邮件。  
- `bella-@leetcode.com` 前缀包含非法字符 `-`，因此无效。  
- `sally.come@leetcode.com` 前缀 `sally.come` 只包含字母和点号，且点号在域名之前出现，仍然满足规则，被保留。  
- `quarz` 同样缺少 `@`，无效。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把每一行记录拿出来，手动检查它的邮箱是否符合规则**。  
可以把检查过程拆成几步：

1. **先找 “@”**：邮箱里必须恰好出现一次 `@`，它把前缀（用户名）和域名分开。  
   - 类比成一本字典，`@` 就像字典里唯一的章节标题，找不到或出现多次都不行。  
2. **检查前缀**：`@` 左边必须非空，且只能出现字母、数字、下划线（这里我们只要求非空即可，题目对字符没有更严格限制）。  
3. **检查域名**：`@` 右边必须包含 **至少一个 “.”**，并且点不能是第一个字符，也不能是最后一个字符。  

只要这三点都满足，就认为这条记录的 `mail` 是合法的。

**为什么这个方法一定正确？**  
因为我们把题目给出的合法邮箱的所有必要条件都逐条验证了，只有全部满足时才返回该用户。

**复杂度分析**（大白话版）：

- 假设表里有 `n` 条记录，每条记录的邮箱长度记作 `m`（一般几百字符以内）。  
- 我们要遍历所有记录 → **遍历 `n` 次**。  
- 对每条记录我们要遍历一次它的字符来找 `@`、点等 → **遍历 `m` 次**。  
- 所以总共的工作量是 `n × m`，记作 **O(n·m)**。  
- 只用了常数级别的额外空间（几个临时变量），记作 **O(1)**。

#### 代码（Python）

```python
from typing import List, Dict

def valid_email_brute(users: List[Dict]) -> List[int]:
    """
    暴力检查每条记录的 mail 是否符合 “前缀@域名” 规则。
    返回满足条件的 user_id 列表。
    """
    res = []
    for row in users:
        mail = row["mail"]
        # 1. 必须恰好出现一次 '@'
        if mail.count("@") != 1:
            continue

        prefix, domain = mail.split("@")
        # 2. 前缀非空
        if not prefix:
            continue

        # 3. 域名必须包含至少一个 '.'，且 '.' 不能在首位或末位
        if "." not in domain:
            continue
        if domain.startswith(".") or domain.endswith("."):
            continue

        # 所有条件都满足 → 记录该 user_id
        res.append(row["user_id"])
    return res

# ------------------- 示例 -------------------
sample = [
    {"user_id": 1, "name": "Winston",   "mail": "winston@leetcode.com"},
    {"user_id": 2, "name": "Jonathan",  "mail": "jonathanisgreat"},
    {"user_id": 3, "name": "Annabelle", "mail": "bella-@leetcode.com"},
    {"user_id": 4, "name": "Sally",     "mail": "sally.come@leetcode.com"},
    {"user_id": 5, "name": "Marwan",    "mail": "quarz"},
]
print(valid_email_brute(sample))   # 输出: [1, 3, 4]
```

#### 复杂度

- **时间复杂度**：`O(n·m)`  
  - `n` 是用户数量，`m` 是单个邮箱的字符数。  
  - 想象成“每个人都要检查一遍自己的邮箱”，所以花的时间随人数线性增长，且每次检查随邮箱长度线性增长。  
- **空间复杂度**：`O(1)`（不计输出列表）  
  - 只用了几个临时字符串变量，和输入规模无关。

---

### 2. 最优解

#### 思路  

在暴力实现里，**最大的瓶颈是我们自己写的逐字符检查**，代码比较冗长且容易遗漏细节。  
实际上，**正则表达式（Regex）** 能一次性把所有规则压缩成一个模式，**底层实现已经高度优化**，所以整体时间几乎是线性的 `O(n)`（每条记录只匹配一次）。

优化步骤：

1. **写出邮箱的正则模式**  
   - `^[^@]+@[^@]+\.[^@]+$`  
   - 解释：  
     - `^`、`$` 分别表示字符串的开始和结束，确保整条字符串都匹配。  
     - `[^@]+` 表示 “不是 @ 的字符，至少出现一次”，对应前缀。  
     - `@` 必须出现一次。  
     - `[^@]+\.[^@]+` 表示域名里必须有一个点，点前后都不能是 `@`，且各自至少有一个字符。  
2. **编译正则**（一次编译，多次使用），避免每条记录都重新解释模式。  
3. **遍历表格**，对每条记录的 `mail` 使用 `fullmatch` 判断是否完全匹配。  
4. **收集满足条件的 `user_id`**。

**为什么这个方法更好？**  
- 正则引擎内部使用 **有限状态机**，匹配过程是线性的，且实现语言层面已经做了大量的性能优化。  
- 代码更简洁、可读性更高，错误率低。

**复杂度分析**（通俗解释）：

- 仍然需要遍历 `n` 条记录 → **O(n)**。  
- 每条记录的匹配过程是 **O(m)**（`m` 为邮箱长度），但正则内部的常数因子更小。总体仍是线性。  
- 额外空间只用来存放编译好的正则对象 → **O(1)**。

#### 代码（Python）

```python
import re
from typing import List, Dict

# 预先编译一次正则，后面所有匹配都会直接使用这个对象
EMAIL_PATTERN = re.compile(r'^[^@]+@[^@]+\.[^@]+$')

def valid_email_regex(users: List[Dict]) -> List[int]:
    """
    使用正则表达式一次性检查邮箱合法性，返回合法的 user_id 列表。
    """
    res = []
    for row in users:
        mail = row["mail"]
        # fullmatch 要求整个字符串都匹配模式
        if EMAIL_PATTERN.fullmatch(mail):
            res.append(row["user_id"])
    return res

# ------------------- 示例 -------------------
print(valid_email_regex(sample))   # 输出: [1, 3, 4]
```

#### 复杂度

- **时间复杂度**：`O(n·m)` → 实际表现为 **线性 O(n)**，因为 `m`（邮箱长度）在实际数据中是常数级别。  
  - 与暴力解相比，省去了手写的多次 `count`、`split`、`startswith` 等操作，常数因子更小。  
- **空间复杂度**：`O(1)`（不计输出列表）  
  - 只多了一个编译好的正则对象，大小固定。

---

## 心得

- **核心技巧**：使用正则表达式一次性描述字符串的结构约束。  
- **适用的题型**  
  1. 检查手机号、身份证号、邮编等固定格式的字符串。  
  2. 过滤日志文件中符合特定模式的行。  
  3. 从文本中提取符合模式的子串（如 URL、日期等）。  
- **解题钥匙**：**把“多个规则”压缩成一个正则模式**，让底层实现帮你完成匹配。

## 反思

- **第一反应**：手动遍历字符、使用 `split`、`count` 检查。  
- **最容易踩的坑**  
  - 忘记检查 `@` 必须恰好出现一次，导致 `a@@b.com` 被误判。  
  - 域名中点的位置不合法（开头或结尾），需要额外判断。  
  - 对空字符串或仅包含 `@`、`.` 的情况忘记过滤。  
- **下次遇到同类题**：第一步先思考 **“能否用正则一次表达全部规则？”**，如果可以，直接写模式并编译；如果规则过于复杂再考虑手动检查。