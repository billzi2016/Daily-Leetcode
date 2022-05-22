# #1789. **员工的主要部门** / Primary Department for Each Employee

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/primary-department-for-each-employee/)

---

## 题目（英文原版）

**Description**

Table: Employee
Employees can belong to multiple departments. When the employee joins other departments, they need to decide which department is their primary department. Note that when an employee belongs to only one department, their primary column is 'N'.
Write a solution to report all the employees with their primary department. For employees who belong to one department, report their only department.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   |  Type   |
+---------------+---------+
| employee_id   | int     |
| department_id | int     |
| primary_flag  | varchar |
+---------------+---------+
(employee_id, department_id) is the primary key (combination of columns with unique values) for this table.
employee_id is the id of the employee.
department_id is the id of the department to which the employee belongs.
primary_flag is an ENUM (category) of type ('Y', 'N'). If the flag is 'Y', the department is the primary department for the employee. If the flag is 'N', the department is not the primary.
```

**Example 2:**

```
Input: 
Employee table:
+-------------+---------------+--------------+
| employee_id | department_id | primary_flag |
+-------------+---------------+--------------+
| 1           | 1             | N            |
| 2           | 1             | Y            |
| 2           | 2             | N            |
| 3           | 3             | N            |
| 4           | 2             | N            |
| 4           | 3             | Y            |
| 4           | 4             | N            |
+-------------+---------------+--------------+
Output: 
+-------------+---------------+
| employee_id | department_id |
+-------------+---------------+
| 1           | 1             |
| 2           | 1             |
| 3           | 3             |
| 4           | 3             |
+-------------+---------------+
Explanation: 
- The Primary department for employee 1 is 1.
- The Primary department for employee 2 is 1.
- The Primary department for employee 3 is 3.
- The Primary department for employee 4 is 3.
```

---

## 题目（中文翻译）

Employees 可以同时属于多个部门。当员工加入多个部门时，需要决定哪个部门是其主要部门。注意：如果员工只属于一个部门，则该记录的 `primary_flag` 为 `'N'`，但该唯一的部门即视为其主要部门。  
请编写查询，返回每位员工对应的主要部门（即 `primary_flag` 为 `'Y'` 的部门；若不存在 `'Y'`，则返回唯一的部门）。结果可以任意顺序返回。

**表结构**

```text
Employee Table
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| employee_id   | int     |
| department_id | int     |
| primary_flag  | varchar |
+---------------+---------+
(employee_id, department_id) 为主键 (primary key)。
employee_id   为员工编号。
department_id 为部门编号。
primary_flag  为该部门是否为主要部门的标记，取值为 'Y'（是）或 'N'（否）。
```

**示例**

**示例 1**

```sql
Input:
Employee table:
+-------------+---------------+--------------+
| employee_id | department_id | primary_flag |
+-------------+---------------+--------------+
| 1           | 1             | N            |
| 2           | 1             | Y            |
| 2           | 2             | N            |
| 3           | 3             | N            |
| 4           | 2             | N            |
+-------------+---------------+--------------+

Output:
+-------------+---------------+
| employee_id | department_id |
+-------------+---------------+
| 1           | 1             |
| 2           | 1             |
| 3           | 3             |
| 4           | 2             |
+-------------+---------------+

Explanation:
- 员工 1 只属于部门 1，虽然 `primary_flag` 为 'N'，但该部门即为其主要部门。
- 员工 2 同时属于部门 1 与部门 2，其中部门 1 的 `primary_flag` 为 'Y'，因此部门 1 为其主要部门。
- 员工 3 只属于部门 3，故部门 3 为主要部门。
- 员工 4 只属于部门 2，故部门 2 为主要部门。
```

**约束条件**

- `1 <= employee_id, department_id <= 10^5`
- `primary_flag` 只会出现 `'Y'` 或 `'N'`  
- 表中数据行数不超过 `10^5`  

请返回上述格式的查询结果即可。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目本质是：**把同一个 `employee_id` 的多条记录合并，只保留该员工的“主部门”。**  
最直接的想法是：

1. **遍历所有记录**，把同一个员工的所有部门收集到一个列表里（相当于把字典里每个 key 对应的 value 当成一个装东西的箱子）。  
2. 再**遍历每个员工的列表**，找出 `primary_flag = 'Y'` 的那条记录。  
   - 如果找到了，就把它的 `department_id` 当作该员工的主部门。  
   - 如果没有找到（说明该员工只有一条记录，`primary_flag` 为 `'N'`），直接把唯一的 `department_id` 当作主部门。  

> **类比**：把 `employee_id` 当成学生的学号，`department_id` 当成他选的课程，`primary_flag` 当成“必修/选修”。我们要找每个学生的必修课；如果只有一门课，那它自然就是必修课。

**正确性**：因为我们把每个员工的所有记录都完整收集起来，随后严格按照题目要求（优先 Y，其次唯一 N）挑选，必然得到符合要求的主部门。

**时间/空间复杂度**（大白话）：

- **时间复杂度**：我们先遍历一次所有记录（`n` 条），再遍历每个员工的记录（总共仍是 `n` 条），所以是 **O(n)**。  
- **空间复杂度**：需要一个字典把所有记录按员工分组，最坏情况下每条记录都要存一次，空间是 **O(n)**。

> 这里的 **O(n)** 可以想象成“和记录数量成正比”。如果有 100 条记录，执行的基本操作大约是 100 次左右。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Dict, Tuple

def primary_department_brute(employee: List[Tuple[int, int, str]]) -> List[Tuple[int, int]]:
    """
    暴力解法：先把同一员工的记录全部收集，再挑选主部门。
    参数 employee 为 [(employee_id, department_id, primary_flag), ...]。
    返回 [(employee_id, primary_department_id), ...]。
    """
    # 1. 按 employee_id 分组，收集所有 (department_id, primary_flag)
    groups: Dict[int, List[Tuple[int, str]]] = defaultdict(list)
    for emp_id, dept_id, flag in employee:
        groups[emp_id].append((dept_id, flag))   # 把这条记录放进对应员工的箱子里

    # 2. 为每个员工挑选主部门
    result: List[Tuple[int, int]] = []
    for emp_id, records in groups.items():
        primary = None          # 用来存主部门的 id
        # 先找 flag 为 'Y' 的记录
        for dept_id, flag in records:
            if flag == 'Y':
                primary = dept_id
                break          # 找到就可以结束循环了
        # 如果没有 Y，说明只有一条 N 记录，直接取它
        if primary is None:
            primary = records[0][0]   # 唯一的 department_id
        result.append((emp_id, primary))

    return result
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历了两遍记录，和记录总数成线性关系。  
- **空间复杂度**：`O(n)` — 用字典把所有记录都保存了一遍。

---

### 2. 最优解

#### 思路  

从暴力解出发，**瓶颈**在于我们用了两层循环：先收集全部记录，再遍历每个员工的记录列表。其实我们不需要把所有记录都保存下来，只要在遍历一次原始表时**立刻确定**每个员工的主部门即可。

**关键点**：

1. **一次遍历**：遍历表的每一行，维护一个字典 `primary`，键是 `employee_id`，值是当前已知的主部门 `department_id`。  
2. **更新规则**  
   - 如果当前行的 `primary_flag == 'Y'`，直接把它的 `department_id` 记为主部门（因为 Y 必定是主部门）。  
   - 如果字典里还没有该员工的记录（即第一次出现），且 `primary_flag == 'N'`，先把这条 N 记录保存下来。后面如果出现 Y 再覆盖即可。  
3. **遍历结束**，字典里就已经是每个员工的主部门了，无需再做第二轮处理。

> **类比**：想象你在收集学生的必修课信息。每当你看到一条记录，如果标记是必修（Y），就直接写下来；如果是选修（N），且之前还没有任何信息，就先记下来，等以后再遇到必修时再改写。这样只需一次“走访”就能完成。

**正确性**：  
- 对于只有一条 N 记录的员工，第一次出现时会被记入字典，后面再无其他记录，最终保留下来。  
- 对于有 Y 记录的员工，无论 Y 出现在哪一次，都会覆盖之前的 N（如果有的话），确保最终结果是 Y 对应的部门。  

**时间/空间复杂度**：

- **时间复杂度**：只遍历一次表，**O(n)**。  
- **空间复杂度**：只保存每个员工的主部门，最多 `m` 条记录（`m` 为不同员工数），**O(m)** ≤ **O(n)**。

#### 代码（Python）

```python
from typing import List, Tuple, Dict

def primary_department_opt(employee: List[Tuple[int, int, str]]) -> List[Tuple[int, int]]:
    """
    最优解：一次遍历即可确定每个员工的主部门。
    参数 employee 为 [(employee_id, department_id, primary_flag), ...]。
    返回 [(employee_id, primary_department_id), ...]。
    """
    # primary[emp_id] = department_id of the current known primary department
    primary: Dict[int, int] = {}

    for emp_id, dept_id, flag in employee:
        if flag == 'Y':
            # 一旦出现 Y，就一定是主部门，直接覆盖
            primary[emp_id] = dept_id
        else:  # flag == 'N'
            # 只在第一次遇到该员工时记下来（因为可能后面会有 Y 覆盖）
            if emp_id not in primary:
                primary[emp_id] = dept_id

    # 把字典转换成题目要求的列表形式
    result = [(emp_id, dept_id) for emp_id, dept_id in primary.items()]
    return result
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历一次原始表，和记录数成正比。相比暴力解省掉了第二轮遍历。  
- **空间复杂度**：`O(m)` — 只保存每个员工的一个部门（`m` 为不同员工数），在最坏情况下等同于 `O(n)`，但通常会更小。

---

## 心得

- **核心技巧**：一次遍历 + 哈希表（字典）实现“先记后覆盖”。  
- **适用的题型**：  
  1. “每组数据的最新/最高/唯一标记” 类题（如：找每个订单的最新状态、每个用户的最新登录时间）。  
  2. “分组后取满足特定条件的唯一记录” 类题（如：每个学生的最高分、每个商品的主图片）。  
- **一句话总结**：**遍历一次，用字典保存并在需要时覆盖，就是最快的分组取唯一解法。**

---

## 反思

- **第一反应**：先把数据按员工分组，再在每组里挑选，这是一种最自然的思路。  
- **最容易踩的坑**：  
  - 忽略了“只有一条 N 记录时也要返回该部门”的情况，导致返回空或错误。  
  - 没有考虑同一个员工可能出现多次 Y（虽然题目暗示不会，但防御性代码要能覆盖）。  
- **下次类似题的第一步**：**问自己：是否可以在一次遍历时直接确定答案？如果可以，使用哈希表记录并在出现更合适的值时覆盖。**这样往往能直接得到最优解。