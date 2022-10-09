# #1965. Employees With Missing Information / Employees With Missing Information

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/employees-with-missing-information/)

---

## 题目（英文原版）

**Description**

Table: Employees
Table: Salaries
Write a solution to report the IDs of all the employees with missing information. The information of an employee is missing if:
Return the result table ordered by employee_id in ascending order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| employee_id | int     |
| name        | varchar |
+-------------+---------+
employee_id is the column with unique values for this table.
Each row of this table indicates the name of the employee whose ID is employee_id.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| employee_id | int     |
| salary      | int     |
+-------------+---------+
employee_id is the column with unique values for this table.
Each row of this table indicates the salary of the employee whose ID is employee_id.
```

**Example 3:**

```
Input: 
Employees table:
+-------------+----------+
| employee_id | name     |
+-------------+----------+
| 2           | Crew     |
| 4           | Haven    |
| 5           | Kristian |
+-------------+----------+
Salaries table:
+-------------+--------+
| employee_id | salary |
+-------------+--------+
| 5           | 76071  |
| 1           | 22517  |
| 4           | 63539  |
+-------------+--------+
Output: 
+-------------+
| employee_id |
+-------------+
| 1           |
| 2           |
+-------------+
Explanation: 
Employees 1, 2, 4, and 5 are working at this company.
The name of employee 1 is missing.
The salary of employee 2 is missing.
```

---

## 题目（中文翻译）

**题目描述**  
表 **Employees**  
| 列名 | 类型 |
|------|------|
| employee_id | int |
| name | varchar |

`employee_id` 为唯一键，每行记录对应 `employee_id` 的员工姓名。

表 **Salaries**  
| 列名 | 类型 |
|------|------|
| employee_id | int |
| salary | int |

`employee_id` 为唯一键，每行记录对应 `employee_id` 的员工薪资。

编写 SQL 查询，返回所有 **信息缺失** 员工的 `employee_id`。当满足以下任意一种情况时，视为信息缺失：

- 员工在 **Employees** 表中出现，但在 **Salaries** 表中没有对应记录（缺少薪资）。
- 员工在 **Salaries** 表中出现，但在 **Employees** 表中没有对应记录（缺少姓名）。
- 员工在两张表中都不存在（既没有姓名也没有薪资）。

返回结果按 `employee_id` **升序** 排列。

**示例**  

输入  

Employees 表：

| employee_id | name     |
|------------|----------|
| 2          | Crew     |
| 4          | Haven    |
| 5          | Kristian |

Salaries 表：

| employee_id | salary |
|------------|--------|
| 5          | 76071  |
| 1          | 22517  |
| 4          | 63539  |

输出  

| employee_id |
|------------|
| 1          |
| 2          |
| 3          |

**解释**  
- `employee_id = 1` 在 **Salaries** 中有记录，但在 **Employees** 中没有对应的姓名，信息缺失。  
- `employee_id = 2` 在 **Employees** 中有记录，但在 **Salaries** 中没有对应的薪资，信息缺失。  
- `employee_id = 3` 在两张表中都没有出现，信息同样缺失。  

**约束条件**  
- 表中 `employee_id` 为唯一值。  
- 两张表的行数均不超过 10⁵。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把两张表 `Employees` 和 `Salaries` 的所有 `employee_id` 都拿出来，逐个比较，看看哪个 `employee_id` 只出现在其中一张表而不在另一张表。  

- **数据结构**：这里我们可以把每张表的 `employee_id` 看成一本“名单”。  
  - 把 `Employees` 表的 `employee_id` 当成 **学生名单**，把 `Salaries` 表的 `employee_id` 当成 **成绩册**。  
  - 要找“信息缺失的员工”，相当于找既不在学生名单里，又在成绩册里，或者反过来，只在名单里不在成绩册里的人。  
- **为什么正确**：如果一个员工的 `employee_id` 同时出现在两张表，说明他的姓名和工资信息都完整；只要缺少其中任意一条记录，就算信息不全。  
- **暴力实现**：对 `Employees` 表的每一行，遍历 `Salaries` 表的每一行去检查是否有相同的 `employee_id`；同理再把 `Salaries` 表的每一行遍历 `Employees` 表。只要在另一张表里找不到对应的 `employee_id`，就把它加入答案。  

> **时间/空间复杂度**  
> - 时间复杂度：每张表都要和另一张表的每一行比较一次，假设 `Employees` 有 `n` 行，`Salaries` 有 `m` 行，时间复杂度是 **O(n·m)**。可以把 `n·m` 想象成“把两张表的行数相乘”，如果两张表都有 10 万行，运算次数就会达到 1 亿元，显然不够高效。  
> - 空间复杂度：只用了几个临时变量，和输入规模无关，**O(1)**（不计返回结果的空间）。

#### 代码（Python）  

```python
# ------------------- 暴力解 -------------------
# 为了演示，这里用 Python 的 list[dict] 来模拟两张表
employees = [
    {"employee_id": 2, "name": "Crew"},
    {"employee_id": 4, "name": "Haven"},
    {"employee_id": 5, "name": "Kristian"},
]

salaries = [
    {"employee_id": 5, "salary": 76071},
    {"employee_id": 1, "salary": 22517},
    {"employee_id": 4, "salary": 63539},
]

def missing_info_bruteforce(employees, salaries):
    """返回信息缺失的 employee_id 列表（升序）"""
    missing = set()                     # 用集合去重
    # 只在 Employees 表里出现，却不在 Salaries 表里的 id
    for e in employees:                 # 外层遍历 Employees
        found = False
        for s in salaries:              # 内层遍历 Salaries
            if e["employee_id"] == s["employee_id"]:
                found = True
                break
        if not found:                   # 没找到对应的 salary
            missing.add(e["employee_id"])

    # 只在 Salaries 表里出现，却不在 Employees 表里的 id
    for s in salaries:                  # 外层遍历 Salaries
        found = False
        for e in employees:             # 内层遍历 Employees
            if s["employee_id"] == e["employee_id"]:
                found = True
                break
        if not found:                   # 没找到对应的 name
            missing.add(s["employee_id"])

    return sorted(missing)              # 按升序返回

print(missing_info_bruteforce(employees, salaries))
# 输出: [1, 2]
```

#### 复杂度  

- **时间复杂度**：`O(n·m)` —— 需要把每一行和另一张表的所有行比较一次。  
- **空间复杂度**：`O(1)`（不计返回结果的空间）—— 只用了常数个变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，瓶颈在于 **“逐行遍历比较”**。其实我们只关心 **是否出现过**，不需要一次次去找对应行。  

- **把每张表的 `employee_id` 收集成集合**（`set`），集合的特性是“查找是否存在的时间是 O(1)”。  
- 当我们把两个集合记为 `E`（Employees 表的 id）和 `S`（Salaries 表的 id）时，缺失信息的员工就是 **只出现在其中一个集合的 id**。这正是集合的 **对称差**（symmetric difference）操作：`E ^ S`。  
- 对称差直接返回所有只在 `E` 或只在 `S` 中出现的元素，正好符合题意。  

> **核心概念解释**  
> - **集合（Set）**：想象成一堆不重复的卡片，每张卡片上写一个员工编号。放进集合后，同一个编号只能出现一次。  
> - **对称差**：把两堆卡片放在一起，拿走所有既在第一堆也在第二堆的卡片，剩下的就是只在一堆里出现的卡片。  

#### 代码（Python）  

```python
# ------------------- 最优解 -------------------
def missing_info_optimal(employees, salaries):
    """利用集合的对称差，O(n+m) 时间完成"""
    # 把每张表的 employee_id 收集到集合中
    emp_ids = {e["employee_id"] for e in employees}   # {2,4,5}
    sal_ids = {s["employee_id"] for s in salaries}    # {1,4,5}

    # 对称差：只在其中一张表出现的 id
    missing = emp_ids ^ sal_ids   # 等价于 (emp_ids - sal_ids) | (sal_ids - emp_ids)

    return sorted(missing)        # 按升序返回

print(missing_info_optimal(employees, salaries))
# 输出: [1, 2]
```

#### 复杂度  

- **时间复杂度**：`O(n + m)` —— 只遍历两张表一次，把 `employee_id` 放进集合，集合的查找/插入都是常数时间。相比暴力的 `O(n·m)`，速度提升了几个数量级。  
- **空间复杂度**：`O(n + m)` —— 需要额外存放两个集合，大小正好等于两张表的行数之和。  

---

## 心得  

- **核心技巧**：利用 **集合（Set）** 的 **对称差** 快速找出只出现一次的元素。  
- **适用的题型**  
  1. “找出两个表中不匹配的记录”——例如 *Missing Numbers*、*Find the Difference of Two Arrays*。  
  2. “判断两个集合是否相等或包含关系”——如 *Intersection of Two Arrays*、*Check If Two Strings Are Anagrams*。  
- **一句话总结解题钥匙**：**把“是否出现”抽象成集合的“成员关系”，用集合的运算一次性得到答案**。

---

## 反思  

- **第一反应**：看到 “两张表，找出缺失信息”，自然想到逐行比对（暴力）。  
- **最容易踩的坑**  
  - 忘记 **去重**：如果同一个 `employee_id` 在某张表里出现多次（虽然本题保证唯一），直接遍历会产生重复的答案。集合天然去重，避免了这个问题。  
  - **返回顺序**：题目要求按 `employee_id` 升序输出，记得在最后 `sorted()` 一下。  
- **下次遇到类似题**：第一步先问自己 “我只需要知道某个值是否出现过吗？” 若答案是，立刻考虑 **集合** 或 **哈希表**，把线性遍历的比较转化为常数时间的查找。