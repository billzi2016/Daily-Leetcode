# #1378. 用唯一标识替换员工 ID / Replace Employee ID With The Unique Identifier

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/replace-employee-id-with-the-unique-identifier/)

---

## 题目（英文原版）

**Description**

Table: Employees
Table: EmployeeUNI
Write a solution to show the unique ID of each user, If a user does not have a unique ID replace just show null.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| name          | varchar |
+---------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table contains the id and the name of an employee in a company.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| id            | int     |
| unique_id     | int     |
+---------------+---------+
(id, unique_id) is the primary key (combination of columns with unique values) for this table.
Each row of this table contains the id and the corresponding unique id of an employee in the company.
```

**Example 3:**

```
Input: 
Employees table:
+----+----------+
| id | name     |
+----+----------+
| 1  | Alice    |
| 7  | Bob      |
| 11 | Meir     |
| 90 | Winston  |
| 3  | Jonathan |
+----+----------+
EmployeeUNI table:
+----+-----------+
| id | unique_id |
+----+-----------+
| 3  | 1         |
| 11 | 2         |
| 90 | 3         |
+----+-----------+
Output: 
+-----------+----------+
| unique_id | name     |
+-----------+----------+
| null      | Alice    |
| null      | Bob      |
| 2         | Meir     |
| 3         | Winston  |
| 1         | Jonathan |
+-----------+----------+
Explanation: 
Alice and Bob do not have a unique ID, We will show null instead.
The unique ID of Meir is 2.
The unique ID of Winston is 3.
The unique ID of Jonathan is 1.
```

---

## 题目（中文翻译）

编写一个查询，展示每位员工对应的唯一标识（unique_id）。如果某位员工没有唯一标识，则在结果中显示 `null`。返回的结果表顺序不限，格式请参考下例。

**表结构**

**Employees 表**

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| name        | varchar |

`id` 为主键（primary key），即该列的值唯一。每行记录了公司中一名员工的 `id` 与 `name`。

**EmployeeUNI 表**

| Column Name | Type |
|-------------|------|
| id          | int  |
| unique_id   | int  |

`(id, unique_id)` 为复合主键（primary key），即两列组合后唯一。每行记录了员工的 `id` 与对应的唯一标识 `unique_id`。

**示例**

**输入**

Employees 表：

```
+----+----------+
| id | name     |
+----+----------+
| 1  | Alice    |
| 7  | Bob      |
| 11 | Meir     |
| 90 | Winston  |
| 3  | Jonathan |
+----+----------+
```

EmployeeUNI 表：

```
+----+-----------+
| id | unique_id |
+----+-----------+
| 3  | 1         |
| 11 | 2         |
| 90 | 3         |
+----+-----------+
```

**输出**

```
+-----------+----------+
| unique_id | name     |
+-----------+----------+
| null      | Alice    |
| null      | Bob      |
| 2         | Meir     |
| 3         | Winston  |
| 1         | Jonathan |
+-----------+----------+
```

**说明**

- 对于 `Employees` 表中存在但在 `EmployeeUNI` 表中没有对应记录的员工（如 `Alice`、`Bob`），结果中的 `unique_id` 显示为 `null`。  
- 其余员工则显示其对应的 `unique_id`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
这道题本质上是 **把两张表按 `id` 列做左连接**（LEFT JOIN），把 `EmployeeUNI` 中对应的 `unique_id` 拉出来；如果某个 `id` 在 `EmployeeUNI` 没有匹配，就返回 `null`。  

最直接、最笨的办法是：  

1. 先把 `Employees` 表全部读取到一个列表 `emp_list`，每条记录是 `(id, name)`。  
2. 再把 `EmployeeUNI` 表全部读取到另一个列表 `uni_list`，每条记录是 `(id, unique_id)`。  
3. 对 `emp_list` 中的每一条记录，遍历 `uni_list` 找到 **相同的 `id`**，如果找到就把 `unique_id` 记下来，否则记 `None`（相当于 SQL 里的 `NULL`）。  

> **类比**：把 `uni_list` 想成一本“员工唯一编号手册”，我们要为每个员工在手册里翻页找对应的编号。如果手册里找不到，就记“空白”。  

这个办法一定能得到正确答案，因为我们把每个员工都和手册里所有条目比较了一遍，必然不会漏掉匹配。  

#### 代码（Python）  

```python
# ---------- 暴力解 ----------
# 输入示例（实际使用时从数据库读取，这里用硬编码模拟）
employees = [
    (1, "Alice"),
    (7, "Bob"),
    (11, "Meir"),
    (90, "Winston"),
    (3, "Jonathan")
]

employee_uni = [
    (3, 1),
    (11, 2),
    (90, 3)
]

def brute_force(employees, employee_uni):
    """返回 [(unique_id or None, name), ...]"""
    result = []
    for emp_id, name in employees:               # 逐个遍历 Employees 表
        uniq = None                               # 默认是 None，表示没有匹配
        for uid, unique_id in employee_uni:       # 在 EmployeeUNI 表里逐条查找
            if uid == emp_id:                     # 找到相同的 id
                uniq = unique_id                  # 记录对应的 unique_id
                break                             # 已找到，跳出内层循环
        result.append((uniq, name))               # 把 (unique_id, name) 加入结果
    return result

# 运行并打印结果
for uid, name in brute_force(employees, employee_uni):
    print(uid, name)
```

> **关键行解释**  
> - `for emp_id, name in employees:`：遍历每个员工，就像把所有员工排成一列。  
> - `for uid, unique_id in employee_uni:`：对每个员工再把手册里所有条目逐一比对。  
> - `if uid == emp_id:`：找到相同 `id` 时，就是我们要的匹配。  

#### 复杂度  

- **时间复杂度**：`O(n * m)`，其中 `n` 是 `Employees` 表的行数，`m` 是 `EmployeeUNI` 表的行数。  
  - 用大白话说，就是“把每个员工都和手册里所有条目比较一次”，如果两张表各有 10 条记录，最坏情况下要比较 100 次。  
- **空间复杂度**：`O(1)`（不计输出列表），只用了几个临时变量，额外占用的内存几乎可以忽略不计。  

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **内层的线性查找**：每次都要遍历整个 `EmployeeUNI` 表。  
我们可以把 `EmployeeUNI` 表先组织成 **哈希表**（Python 的 `dict`），把 `id` 直接映射到 `unique_id`。这样查找就可以 **O(1)** 完成，整体时间降到 **O(n + m)**。  

> **类比**：把手册的内容先装进一本“快速检索的字典”，每次只需要看一眼（直接用 `id` 当关键词查），不必把整本手册翻遍。  

**关键步骤**  

1. **构建哈希表** `id → unique_id`：遍历 `EmployeeUNI`，把每条记录放进字典。  
2. **遍历 Employees**：对每个员工，直接在字典里查 `emp_id` 是否存在，若存在取出 `unique_id`，否则返回 `None`。  

这就是典型的 “左连接 + 哈希表” 思路，在实际 SQL 引擎里也会使用类似的 hash join 来提升性能。  

#### 代码（Python）  

```python
# ---------- 最优解 ----------
def optimal_solution(employees, employee_uni):
    """返回 [(unique_id or None, name), ...]，时间 O(n+m)"""
    # 1️⃣ 把 EmployeeUNI 表构造成哈希表：id -> unique_id
    id_to_unique = {uid: unique_id for uid, unique_id in employee_uni}
    # 2️⃣ 遍历 Employees，直接在哈希表里 O(1) 查找
    result = []
    for emp_id, name in employees:
        uniq = id_to_unique.get(emp_id)   # .get() 在找不到时返回 None
        result.append((uniq, name))
    return result

# 运行并打印结果
for uid, name in optimal_solution(employees, employee_uni):
    print(uid, name)
```

> **关键行解释**  
> - `{uid: unique_id for uid, unique_id in employee_uni}`：一次遍历把手册变成“查字典”。  
> - `id_to_unique.get(emp_id)`：在字典里直接取值，时间几乎是常数（不随表大小增长）。  

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - `m` 次遍历把 `EmployeeUNI` 放进哈希表，`n` 次遍历 `Employees` 并做 O(1) 查找。  
  - 与暴力解相比，**从 “乘法” 降到 “加法”**，当表很大时速度提升非常明显。  
- **空间复杂度**：`O(m)`  
  - 需要额外的哈希表来存储 `EmployeeUNI` 中的所有映射关系，大小正比于 `EmployeeUNI` 的行数。  

---  

## 心得  

- **核心技巧**：**哈希表（字典）实现左连接**。  
- **适用场景**：  
  1. 两张表需要根据某个键匹配，且其中一张表可以全部装入内存。  
  2. “把 A 表的每条记录映射到 B 表的属性” 类似的查询，如 `User → Profile`、`Product → Category` 等。  
- **一句话总结**：先把要频繁查找的表做成字典，查找就能做到 O(1)，整体就快了。  

## 反思  

- **第一反应**：看到 “把唯一编号显示出来，不存在则为 null”，立刻想到左连接（LEFT JOIN）。  
- **最容易踩的坑**：  
  - 忘记左连接的方向，导致把没有 `unique_id` 的员工直接过滤掉（相当于 INNER JOIN）。  
  - 在实现哈希表时，使用 `dict[emp_id]` 而不是 `dict.get(emp_id)`，当键不存在会抛异常。  
- **下次第一步**：先判断哪张表的行数更少，是否可以全部放进哈希表；如果可以，就立刻构造字典再遍历另一张表。