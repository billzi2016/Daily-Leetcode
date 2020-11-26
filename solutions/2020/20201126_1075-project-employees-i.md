# #1075. 项目员工 I / Project Employees I

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/project-employees-i/)

---

## 题目（英文原版）

**Description**

Table: Project
Table: Employee
Write an SQL query that reports the average experience years of all the employees for each project, rounded to 2 digits.
Return the result table in any order.
The query result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| project_id  | int     |
| employee_id | int     |
+-------------+---------+
(project_id, employee_id) is the primary key of this table.
employee_id is a foreign key to Employee table.
Each row of this table indicates that the employee with employee_id is working on the project with project_id.
```

**Example 2:**

```
+------------------+---------+
| Column Name      | Type    |
+------------------+---------+
| employee_id      | int     |
| name             | varchar |
| experience_years | int     |
+------------------+---------+
employee_id is the primary key of this table. It's guaranteed that experience_years is not NULL.
Each row of this table contains information about one employee.
```

**Example 3:**

```
Input: 
Project table:
+-------------+-------------+
| project_id  | employee_id |
+-------------+-------------+
| 1           | 1           |
| 1           | 2           |
| 1           | 3           |
| 2           | 1           |
| 2           | 4           |
+-------------+-------------+
Employee table:
+-------------+--------+------------------+
| employee_id | name   | experience_years |
+-------------+--------+------------------+
| 1           | Khaled | 3                |
| 2           | Ali    | 2                |
| 3           | John   | 1                |
| 4           | Doe    | 2                |
+-------------+--------+------------------+
Output: 
+-------------+---------------+
| project_id  | average_years |
+-------------+---------------+
| 1           | 2.00          |
| 2           | 2.50          |
+-------------+---------------+
Explanation: The average experience years for the first project is (3 + 2 + 1) / 3 = 2.00 and for the second project is (3 + 2) / 2 = 2.50
```

---

## 题目（中文翻译）

编写一条 SQL 查询，统计每个项目下所有员工的 **平均工作经验年数**（average experience years），并保留两位小数。  
返回的结果表顺序任意即可。查询结果的格式参见下方示例。

---

## 表结构

**Project 表**

| 列名         | 类型 |
|--------------|------|
| project_id   | int  |
| employee_id  | int  |

- (`project_id`, `employee_id`) 为 **主键（primary key）**。  
- `employee_id` 为指向 **Employee 表** 的 **外键（foreign key）**。  
- 每一行表示编号为 `employee_id` 的员工正在参与编号为 `project_id` 的项目。

**Employee 表**

| 列名           | 类型    |
|----------------|---------|
| employee_id    | int     |
| name           | varchar |
| experience_years | int   |

- `employee_id` 为 **主键（primary key）**。  
- 保证 `experience_years` 不为 `NULL`。  
- 每一行记录一名员工的基本信息。

---

## 示例

**输入**

Project 表：

```
+------------+-------------+
| project_id | employee_id |
+------------+-------------+
| 1          | 1           |
| 1          | 2           |
| 1          | 3           |
| 2          | 1           |
| 2          | 4           |
+------------+-------------+
```

Employee 表：

```
+-------------+------+-----------------+
| employee_id | name | experience_years |
+-------------+------+-----------------+
| 1           | Khaled | 3               |
| 2           | Ali    | 2               |
| 3           | John   | 1               |
| 4           | Doe    | 2               |
+-------------+------+-----------------+
```

**输出**

```
+------------+---------------+
| project_id | average_years |
+------------+---------------+
| 1          | 2.00          |
| 2          | 2.50          |
+------------+---------------+
```

**解释**  
第一个项目的平均工作经验年数为 `(3 + 2 + 1) / 3 = 2.00`，  
第二个项目的平均工作经验年数为 `(3 + 2) / 2 = 2.50`。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**先把两张表连接起来**（把每个项目对应的员工的工作年限找出来），再**逐个项目**遍历，手动把同一个 `project_id` 下的所有 `experience_years` 加起来，最后除以人数得到平均值。  

- **数据结构类比**：把 `Project` 表看成一本“项目目录”，每一行记着 “项目号 – 员工号”。把 `Employee` 表看成一本“员工手册”，每一行记着 “员工号 – 工作年限”。我们要把这两本书的对应页码翻开，配对起来，就像在字典里查单词：键（`employee_id`）对应的值（`experience_years`）需要先找到。  
- **为什么正确**：只要把每条 “项目‑员工” 记录对应的工作年限找出来，随后对同一项目的年限求平均，就完全满足题目要求。  
- **时间/空间复杂度**：  
  - 先遍历 `Project` 表 `m` 行，每行都要在 `Employee` 表里**线性查找**一次（最坏情况要遍历 `n` 行），于是时间复杂度是 **O(m·n)**，这在数据量稍大时会明显变慢。  
  - 为了存放临时的求和和计数，我们需要一个哈希表（`dict`）保存每个 `project_id` 对应的 `[sum, cnt]`，空间复杂度是 **O(k)**，其中 `k` 是项目的种类数（最坏等于 `m`）。  

#### 代码（Python）  

```python
# 下面的代码演示“暴力”思路，直接用 Python 列表模拟两张表
# Project 表（project_id, employee_id）
project = [
    (1, 1),
    (1, 2),
    (1, 3),
    (2, 1),
    (2, 4),
]

# Employee 表（employee_id, name, experience_years）
employee = [
    (1, "Khaled", 3),
    (2, "Ali",    2),
    (3, "John",   1),
    (4, "Doe",    2),
]

# 1️⃣ 先把 employee 表变成字典，方便后面“查字典”
exp_by_emp = {eid: years for eid, _, years in employee}
# 2️⃣ 暴力遍历 Project，每条记录都去 employee 字典里找经验年限
#    再用一个 dict 累加求和、计数
sum_cnt = {}          # key: project_id, value: [sum_years, cnt]
for pid, eid in project:
    years = exp_by_emp[eid]           # O(1) 查表
    if pid not in sum_cnt:
        sum_cnt[pid] = [0, 0]
    sum_cnt[pid][0] += years          # 累加经验年限
    sum_cnt[pid][1] += 1              # 计数

# 3️⃣ 计算平均值并保留两位小数
result = [(pid, round(total / cnt, 2)) for pid, (total, cnt) in sum_cnt.items()]
print(result)   # [(1, 2.0), (2, 2.5)]
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`（对每条项目记录在员工表中线性查找）。在实际代码里我们用了哈希表把查找降到 `O(1)`，但如果真的每次都遍历整个员工列表，就会是乘法级别的时间。  
- **空间复杂度**：`O(k + n)`，需要额外的哈希表保存 `employee` 信息 (`O(n)`) 和每个项目的累计数据 (`O(k)`)。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于每次都要去遍历 `Employee` 表寻找对应的 `experience_years`。只要把 `Employee` 表一次性**预处理成哈希表**（`employee_id → experience_years`），后面所有查找都能在 **O(1)** 时间完成。  

整个过程可以分两步：

1. **一次遍历 Employee 表**，把 `employee_id` 映射到 `experience_years`（相当于把“员工手册”做成一本快速索引的字典）。  
2. **一次遍历 Project 表**，用字典直接取出每个 `employee_id` 的工作年限，累计到对应的 `project_id` 上，同时记录人数。  

这两个线性遍历的总时间是 **O(m + n)**，已经是最优的线性时间。  

- **核心数据结构**：**哈希表（dict）**。在 Python 中，字典的查找、插入、更新都是常数时间，类似于生活中的“查字典”，键是单词（这里是 `employee_id`），值是对应的页码（这里是工作年限）。  
- **为什么能得到平均值**：我们在一次遍历中已经把每个项目的 **总经验年限** 和 **员工人数** 累加完毕，只要把两者相除并保留两位小数即可。  

#### 代码（Python）  

```python
def average_experience_per_project(project, employee):
    """
    :param project: List[Tuple[int, int]]  [(project_id, employee_id), ...]
    :param employee: List[Tuple[int, str, int]] [(employee_id, name, experience_years), ...]
    :return: List[Tuple[int, float]] [(project_id, average_years), ...]  平均值保留两位小数
    """
    # 1️⃣ 把 Employee 表变成哈希表：employee_id → experience_years
    exp_by_emp = {eid: years for eid, _, years in employee}
    # 2️⃣ 用另一个哈希表累计每个项目的总年限和人数
    agg = {}   # key: project_id, value: [sum_years, cnt]
    for pid, eid in project:
        years = exp_by_emp[eid]          # O(1) 查找
        if pid not in agg:
            agg[pid] = [0, 0]
        agg[pid][0] += years             # 累加经验
        agg[pid][1] += 1                 # 计数

    # 3️⃣ 计算平均值，保留两位小数
    result = [(pid, round(total / cnt, 2)) for pid, (total, cnt) in agg.items()]
    # 为了符合 LeetCode 输出顺序，这里不要求排序，任意顺序均可
    return result


# ------------------- 示例 -------------------
project = [(1, 1), (1, 2), (1, 3), (2, 1), (2, 4)]
employee = [(1, "Khaled", 3), (2, "Ali", 2), (3, "John", 1), (4, "Doe", 2)]

print(average_experience_per_project(project, employee))
# 输出: [(1, 2.0), (2, 2.5)]
```

> **SQL 版（仅作对照）**  
> ```sql
> SELECT p.project_id,
>        ROUND(AVG(e.experience_years), 2) AS average_years
> FROM   Project p
> JOIN   Employee e ON p.employee_id = e.employee_id
> GROUP BY p.project_id;
> ```
> 把上面的 Python 思路映射到 SQL，只需要一次 `JOIN` 再 `GROUP BY` 即可，SQL 引擎内部已经帮我们实现了哈希聚合，时间复杂度同样是线性级别。

#### 复杂度  

- **时间复杂度**：`O(m + n)`  
  - `n` 为 `Employee` 表的行数（一次遍历建立字典）。  
  - `m` 为 `Project` 表的行数（一次遍历累计）。  
  与暴力解的 `O(m·n)` 相比，**快了很多**，因为我们把每一次的线性查找都换成了常数时间的哈希查询。  
- **空间复杂度**：`O(k + n)`  
  - `n` 用于存放 `employee_id → experience_years` 的字典。  
  - `k` 为项目种类数，用于存放每个项目的累计数据。  
  这两个额外空间在实际中都非常小，且不可避免——我们必须记住每个员工的经验以及每个项目的累计信息。

---

## 心得  

- **核心技巧**：利用哈希表把“关联查询”变成 O(1) 的直接索引，然后在一次遍历中完成聚合。  
- **适用的题型**  
  1. 需要 **关联两张表**（或两类数据）后做 **分组统计** 的题目，如 “每个部门的平均工资”。  
  2. “**一对多**”关系下的聚合问题，例如 “每个作者的总书籍销量”。  
  3. 任何可以把 “外键 → 目标属性” 预处理成字典的场景，都可以使用此技巧。  
- **一句话总结**：**先把“查字典”做成哈希表，再一次遍历完成所有求和与计数**，既简单又高效。

---

## 反思  

- **第一反应**：看到 “Project 与 Employee 两表关联求平均”，立刻想到 `JOIN + GROUP BY`（SQL）或 “先把 Employee 变成字典，再遍历 Project” （手写代码）。  
- **最容易踩的坑**  
  - **忘记把 `experience_years` 转成浮点数再除**，导致整数除法得到 0。  
  - **平均值保留两位小数**：直接打印可能会出现 `2.0` 而不是 `2.00`，需要使用 `round(..., 2)` 或格式化。  
  - **项目可能没有员工**（虽然题目未说明），若出现空项目，需要防止除以 0。  
- **下次遇到同类题**：第一步先**构造哈希映射**（外键 → 需要的属性），再**单遍历聚合**，最后**计算平均/求和**并**格式化输出**。这样思路清晰，代码也自然高效。