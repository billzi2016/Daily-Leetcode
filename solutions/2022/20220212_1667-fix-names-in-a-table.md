# #1667. 修复表中的姓名 / Fix Names in a Table

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/fix-names-in-a-table/)

---

## 题目（英文原版）

**Description**

Table: Users
Write a solution to fix the names so that only the first character is uppercase and the rest are lowercase.
Return the result table ordered by user_id.
The result format is in the following example.

**Examples**

**Example 1:**

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| user_id        | int     |
| name           | varchar |
+----------------+---------+
user_id is the primary key (column with unique values) for this table.
This table contains the ID and the name of the user. The name consists of only lowercase and uppercase characters.
```

**Example 2:**

```
Input: 
Users table:
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | aLice |
| 2       | bOB   |
+---------+-------+
Output: 
+---------+-------+
| user_id | name  |
+---------+-------+
| 1       | Alice |
| 2       | Bob   |
+---------+-------+
```

---

## 题目（中文翻译）

Table: Users  

编写一个解决方案，使 `name` 字段的首字符为大写，其余字符为小写。返回按 `user_id` 排序的结果表。结果格式如下例所示。

**示例 1**  

| Column Name | Type    |
|-------------|---------|
| user_id     | int     |
| name        | varchar |

`user_id` 是该表的主键（primary key），也是唯一值的列（column with unique values）。该表包含用户的 ID 和姓名。姓名仅由大小写字母组成。

**示例 2**  

**输入**  
Users 表：

| user_id | name  |
|---------|-------|
| 1       | aLice |
| 2       | bOB   |

**输出**  

| user_id | name  |
|---------|-------|
| 1       | Alice |
| 2       | Bob   |

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法就是把表里的每一行都拿出来，**逐字符**检查并修改：  

1. 先把整个名字全部转成小写（相当于把所有字母都统一成“小写字典”里的词条）。  
2. 再把第 **1** 个字符转成大写（就像在字典里把第一个词的首字母抬高）。  

这样处理完所有行后，按 `user_id` 排序返回即可。  

> **为什么能得到正确答案？**  
> 题目要求“只有第一个字符是大写，其余全部小写”。我们先把所有字符都变成小写，确保了“其余全部小写”。随后只把第一个字符改为大写，恰好满足“第一个字符是大写”。两步操作顺序不影响结果，所以一定正确。  

> **时间/空间复杂度大白话**  
> - 假设表里有 `n` 条记录，每条名字的长度平均为 `m`。我们要遍历 **每一条记录**，并且对每条名字的每个字符都做一次大小写转换。于是总共要做 `n × m` 次基本操作，用大写的 **O(n·m)** 表示。  
> - 额外使用的空间只有几个临时变量（比如循环计数器、临时字符串），不随 `n` 增长，用 **O(1)** 表示。  

#### 代码（Python）  

```python
# 暴力版：手动遍历每个字符
def fix_names_brute(users):
    """
    :param users: List[Tuple[int, str]]  # [(user_id, name), ...]
    :return: List[Tuple[int, str]] 按 user_id 升序的结果
    """
    fixed = []
    for uid, name in users:
        # 1. 把整串变小写
        lower_name = name.lower()               # "aLice" -> "alice"
        # 2. 把第一个字符改为大写
        if lower_name:                           # 防止空字符串
            fixed_name = lower_name[0].upper() + lower_name[1:]
        else:
            fixed_name = ""                      # 空名字保持不变
        fixed.append((uid, fixed_name))

    # 3. 按 user_id 排序返回
    fixed.sort(key=lambda x: x[0])
    return fixed


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    # 模拟表数据
    users_table = [
        (1, "aLice"),
        (2, "bOB"),
        (3, "CHARLie"),
    ]
    print(fix_names_brute(users_table))
    # 输出: [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie')]
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  *n* 为记录数，*m* 为名字的平均长度。相当于“我们要把每个人的名字每个字母都看一遍”。  
- **空间复杂度**：`O(1)`（不计输出列表）  
  只用了常数个临时变量，和表的大小无关。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**遍历每条记录**是必须的（没有办法一次性改掉所有行），瓶颈不在遍历，而在**我们自己写的字符循环**。  
Python 已经为我们实现了高效且简洁的字符串大小写转换函数：  

| 方法 | 功能 | 为什么更好 |
|------|------|------------|
| `str.lower()` | 把整串转成小写 | 底层用 C 实现，速度快 |
| `str.capitalize()` | 把首字母大写、其余小写 | 一行搞定，避免手动切片拼接 |

因此**最优解**只需要两行代码就能完成每条记录的转换：  

```python
fixed_name = name.lower().capitalize()
```

或者直接使用 `title()`（对每个单词首字母大写）但这里名字只有一个单词，用 `capitalize()` 更合适。  

整体思路仍是：遍历表 → 对每行名字调用 `capitalize()` → 收集 → 按 `user_id` 排序返回。  

#### 代码（Python）  

```python
# 最优版：利用内置函数一次搞定
def fix_names_optimal(users):
    """
    :param users: List[Tuple[int, str]]
    :return: List[Tuple[int, str]] 按 user_id 升序
    """
    # 直接使用列表推导式和内置的 capitalize()
    fixed = [(uid, name.lower().capitalize()) for uid, name in users]

    # 排序
    fixed.sort(key=lambda x: x[0])
    return fixed


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    users_table = [
        (2, "bOB"),
        (1, "aLice"),
        (4, "david"),
        (3, "EVE"),
    ]
    print(fix_names_optimal(users_table))
    # 输出: [(1, 'Alice'), (2, 'Bob'), (3, 'Eve'), (4, 'David')]
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  仍然需要遍历每条记录并处理每个字符，但所有字符操作都是在 C 层完成的，常数因子更小。  
- **空间复杂度**：`O(1)`（不计输出）  
  与暴力版相同，只是代码更简洁，额外空间几乎没有增加。  

相较于暴力解，**核心提升在于把手动字符拼接交给了 Python 的内部实现**，运行更快、代码更易读。  

---  

## 心得  

- **核心技巧**：利用语言提供的 **字符串大小写函数**（`lower()`、`capitalize()`）一次性完成“首字母大写、其余小写”。  
- **适用的题型**  
  1. 把文本统一成特定大小写格式（如标题化、全大写）。  
  2. 处理 CSV/Excel 中的字段清洗（统一大小写后再去重）。  
  3. 类似 LeetCode “把句子里的每个单词首字母大写” 的题目（`title()`）。  
- **一句话总结解题钥匙**：**把“手动循环”交给标准库函数，一行代码搞定大小写转换**。  

---  

## 反思  

- **第一反应**：直接遍历每行，用 `lower()` 再手动拼接第一个字符的大写。  
- **最容易踩的坑**  
  - 名字为空字符串时直接取 `name[0]` 会报错，需要先判断。  
  - 名字中可能已经全部是大写或小写，直接 `capitalize()` 仍然能得到正确结果，无需额外判断。  
- **下次遇到同类题**：第一步想到 **“有没有现成的库函数可以一次性完成需求？”**，如果有就直接使用；如果没有，再考虑手动遍历实现。