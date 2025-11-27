# #3436. 查找有效的电子邮件 / Find Valid Emails

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-valid-emails/)

---

## 题目（英文原版）

**Description**

Table: Users
Write a solution to find all the valid email addresses. A valid email address meets the following criteria:
Return the result table ordered by user_id in ascending order.
Example:

**Examples**

**Example 1:**

```
+-----------------+---------+
| Column Name     | Type    |
+-----------------+---------+
| user_id         | int     |
| email           | varchar |
+-----------------+---------+
(user_id) is the unique key for this table.
Each row contains a user's unique ID and email address.
```

**Example 2:**

```
+---------+---------------------+
| user_id | email               |
+---------+---------------------+
| 1       | alice@example.com   |
| 2       | bob_at_example.com  |
| 3       | charlie@example.net |
| 4       | david@domain.com    |
| 5       | eve@invalid         |
+---------+---------------------+
```

**Example 3:**

```
+---------+-------------------+
| user_id | email             |
+---------+-------------------+
| 1       | alice@example.com |
| 4       | david@domain.com  |
+---------+-------------------+
```

---

## 题目（中文翻译）

编写一个解决方案，找出所有符合条件的有效电子邮件地址。有效的电子邮件地址满足下列标准：

返回的结果表需按 **user_id** 升序排序。

**示例 1**  
+-----------------+---------+  
| Column Name     | Type    |  
+-----------------+---------+  
| user_id         | int     |  
| email           | varchar |  
+-----------------+---------+  
`(user_id)` 为该表的唯一键。每行记录包含用户的唯一 ID 和电子邮件地址。

**示例 2**  
+---------+-------------------+  
| user_id | email             |  
+---------+-------------------+  
| 1       | alice@example.com |  
| 2       | bob_at_example.com|  
| 3       | charlie@example.net|  
| 4       | david@domain.com  |  
| 5       | eve@invalid       |  
+---------+-------------------+

**示例 3**  
+---------+-------------------+  
| user_id | email             |  
+---------+-------------------+  
| 1       | alice@example.com |  
| 4       | david@domain.com  |  
+---------+-------------------+

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把表里的每一行都拿出来，逐条检查 `email` 是否符合“合法邮箱”的规则。  
这里我们把规则简化为：

1. 必须恰好出现一次字符 `@`（相当于“字典”里必须只有一个词条）。  
2. `@` 右侧必须至少出现一次 `.`（相当于“字典”里必须还有子目录）。  
3. `@` 左侧、右侧都不能出现空格或其他非法字符（相当于词条必须是完整的单词）。  

实现时只需要：

- 用 `str.count('@')` 判断 `@` 的个数。  
- 用 `str.find('@')` 找到 `@` 的位置，再在它右边检查是否有 `.`。  
- 用 `in` 检查是否出现空格等非法字符。

只要全部条件满足，就把该行的 `user_id` 与 `email` 加入结果列表。

> **类比**：把每封邮件想象成一本书的目录页码，`@` 像章节号，`.` 像小节号，只有章节号唯一且后面还有小节号，目录才算是合法的。

#### 代码（Python）

```python
# 假设数据已经以列表字典的形式读取进来
users = [
    {"user_id": 1, "email": "alice@example.com"},
    {"user_id": 2, "email": "bob_at_example.com"},
    {"user_id": 3, "email": "charlie@example.net"},
    {"user_id": 4, "email": "david@domain.com"},
    {"user_id": 5, "email": "eve@invalid"},
]

def is_valid_email(email: str) -> bool:
    """暴力检查邮箱是否合法"""
    # 1️⃣ 必须恰好有一个 '@'
    if email.count('@') != 1:
        return False

    at_pos = email.find('@')          # 找到 '@' 的下标
    # 2️⃣ '@' 前后都不能有空格
    if ' ' in email[:at_pos] or ' ' in email[at_pos+1:]:
        return False

    # 3️⃣ '@' 右侧必须至少有一个 '.'（且 '.' 必须在 '@' 之后）
    domain_part = email[at_pos+1:]    # 取出域名部分
    if '.' not in domain_part:
        return False

    # 通过所有检查，返回 True
    return True

def find_valid_emails_bruteforce(users):
    """暴力遍历所有记录，筛选合法邮箱"""
    valid = []
    for row in users:
        if is_valid_email(row["email"]):
            valid.append(row)               # 记录合法行
    # 按 user_id 升序返回
    return sorted(valid, key=lambda x: x["user_id"])

# 运行示例
result = find_valid_emails_bruteforce(users)
print(result)   # [{'user_id': 1, 'email': 'alice@example.com'}, {'user_id': 4, 'email': 'david@domain.com'}]
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`  
  - `n` 为用户总数，`m` 为单个邮箱的长度。因为我们对每条记录都要遍历一次字符（`count`、`find`、`in` 都是线性扫描），所以整体是 **线性乘以字符串长度**，可以把它想成“检查每封信需要花的时间”。  
- **空间复杂度**：`O(k)`  
  - 只用了常数级的额外空间（`valid` 列表最多保存合法记录，最坏情况是全部合法，这里记作 `k`），不随单个字符串长度增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每次都要对同一个字符串做多次线性扫描（`count`、`find`、`in`、`'.' in domain_part`）。  
如果把这些检查合并成一次扫描，甚至直接利用正则表达式一次匹配，就能把常数因子降到最低。

**核心技巧：正则表达式（Regular Expression）**  
正则像一本“万能搜索手册”，一次就能判断字符串是否符合复杂模式。  
我们把合法邮箱的规则写成正则：

```
^[^@\s]+@[^@\s]+\.[^@\s]+$
```

解释：

- `^`、`$`：匹配字符串的开始与结束，保证整条记录都符合规则。  
- `[^@\s]+`：`[]` 表示“字符集合”，`^` 在里面表示“除……之外的任意字符”。这里要求 **不包含 `@` 与空格** 的至少一个字符。  
- `@`：必须出现一次 `@`。  
- `[^@\s]+\.`：`@` 后面先是一段不含 `@` 与空格的字符（域名），随后必须紧跟一个 `.`。  
- `[^@\s]+`：`.` 之后再来一段不含 `@` 与空格的字符（顶级域名），结束。

只要一次 `re.fullmatch` 成功，就说明邮箱合法。  
正则本身在底层已经做了 **一次** 线性扫描，省去了我们手写的多次 `count`、`find` 等操作。

#### 代码（Python）

```python
import re

# 预编译正则，编译一次即可复用，等价于“把规则写在字典里一次性查找”
EMAIL_PATTERN = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')

def is_valid_email_regex(email: str) -> bool:
    """使用正则一次匹配判断邮箱是否合法"""
    return EMAIL_PATTERN.fullmatch(email) is not None

def find_valid_emails_optimal(users):
    """一次遍历 + 正则匹配，筛选合法邮箱"""
    valid = [row for row in users if is_valid_email_regex(row["email"])]
    # 按 user_id 升序返回
    return sorted(valid, key=lambda x: x["user_id"])

# 运行示例
result_opt = find_valid_emails_optimal(users)
print(result_opt)   # 与暴力解的输出相同
```

#### 复杂度  

- **时间复杂度**：`O(n * m)`（同样是线性），但常数更小。  
  - 正则在底层一次遍历完成所有检查，等价于“只检查一次信件”。相比暴力解的多次扫描，实际运行更快。  
- **空间复杂度**：`O(k)`（同上），额外只多了正则对象的常数空间。

> 与暴力解对比：时间阶层没有变化（都是线性），但 **实际运行速度更快**，代码更简洁、更易维护。

---

## 心得

- **核心技巧**：正则表达式一次性匹配复杂模式，能够把多次遍历合并为一次。  
- **适用题型**：  
  1. 验证手机号、身份证号等固定格式字符串。  
  2. 从日志中抽取符合特定模式的行（如 IP 地址、URL）。  
  3. 判断密码强度（必须同时包含字母、数字、特殊字符）。  
- **一句话总结**：**“把所有规则写进正则，一次匹配搞定”。**

---

## 反思

- **第一反应**：直接遍历每条记录，用字符串方法手动检查 `@`、`.`、空格等。  
- **最容易踩的坑**：  
  - 忽略了 `@` 或 `.` 前后出现空格的情况。  
  - 只检查是否有 `.`，却没保证 `.` 出现在 `@` 之后。  
  - 没考虑多个 `@` 的情况（`a@@b.com` 也会被误判为合法）。  
- **下次思路**：一看到“格式校验”类的题目，首先在脑中构造正则模式，判断是否能一次匹配；若正则太复杂，再考虑逐步手写检查。