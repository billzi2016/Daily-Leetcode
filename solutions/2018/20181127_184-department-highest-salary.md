# #184. 部门最高工资 / Department Highest Salary

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/department-highest-salary/)

---

## 题目（英文原版）

**Description**

Table: Employee
Table: Department
Write a solution to find employees who have the highest salary in each of the departments.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
id is the primary key (column with unique values) for this table.
departmentId is a foreign key (reference columns) of the ID from the Department table.
Each row of this table indicates the ID, name, and salary of an employee. It also contains the ID of their department.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
id is the primary key (column with unique values) for this table. It is guaranteed that department name is not NULL.
Each row of this table indicates the ID of a department and its name.
```

**Example 3:**

```
Input: 
Employee table:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Jim   | 90000  | 1            |
| 3  | Henry | 80000  | 2            |
| 4  | Sam   | 60000  | 2            |
| 5  | Max   | 90000  | 1            |
+----+-------+--------+--------------+
Department table:
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
Output: 
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Jim      | 90000  |
| Sales      | Henry    | 80000  |
| IT         | Max      | 90000  |
+------------+----------+--------+
Explanation: Max and Jim both have the highest salary in the IT department and Henry has the highest salary in the Sales department.
```

---

## 题目（中文翻译）

描述  
表（Table）：Employee  
表（Table）：Department  

编写一个查询，找出每个部门中工资最高的员工。返回结果表，顺序不限。结果格式参考下面的示例。

**示例 1**

```text
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| id           | int     |
| name         | varchar |
| salary       | int     |
| departmentId | int     |
+--------------+---------+
```

- `id` 为主键（primary key），即唯一值列。  
- `departmentId` 为外键（foreign key），引用 Department 表中的 `id`。  
- 每行记录员工的 `id`、`name`、`salary`，以及所属部门的 `departmentId`。

```text
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
+-------------+---------+
```

- `id` 为主键（primary key），保证唯一。  
- `name` 不会为 `NULL`，表示部门名称。  
- 每行记录部门的 `id` 与 `name`。

**示例 3**

输入  

Employee 表：

```text
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 70000  | 1            |
| 2  | Jim   | 90000  | 1            |
| 3  | Henry | 80000  | 2            |
| 4  | Sam   | 60000  | 2            |
| 5  | Max   | 90000  | 1            |
+----+-------+--------+--------------+
```

Department 表：

```text
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
```

输出  

```text
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Jim      | 90000  |
| Sales      | Henry    | 80000  |
| IT         | Max      | 90000  |
+------------+----------+--------+
```

解释：在 IT 部门，Jim 和 Max 的工资均为最高（90000），因此都出现在结果中；在 Sales 部门，Henry 的工资最高（80000），因此仅有他一条记录。  

约束条件  
无

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是 **“先找每个部门的最高工资，然后再把对应的员工挑出来”**。  
我们可以把 `Employee` 表想象成一本员工通讯录，用 **列表** 存每一行记录；`Department` 表则像一本部门字典，用 **列表** 存部门信息。  

实现步骤：

1. 先遍历 `Department` 列表，拿到每个部门的 `id`（相当于字典的关键字）。  
2. 对于当前部门，再遍历一遍 `Employee` 列表，找出属于该部门且工资最大的员工（就像在一堆人里挑最高的）。  
3. 再遍历一次 `Employee`，把所有工资等于该最高值的员工全部收集进去（因为可能有多人并列最高）。  

> **为什么正确？**  
> - 第 2 步保证我们找到了该部门的最高工资 `max_salary`。  
> - 第 3 步把所有工资等于 `max_salary` 的员工都加入结果，正好满足“最高工资的所有员工”。  

> **时间/空间复杂度的大白话**  
> - 假设有 `n` 条员工记录，`m` 条部门记录。  
> - 第 2 步对每个部门都要遍历所有员工 → `m × n` 次比较。  
> - 第 3 步再遍历一次所有员工 → 再加 `n` 次比较。  
> - 所以总体是 **O(m·n)**，在最坏情况下（比如每个部门都有员工）可以近似看成 **O(n²)**（因为 `m` 与 `n` 同阶）。  
> - 空间上我们只用了几个临时变量和结果列表，和输入规模无关 → **O(1)**（不计输出）。

#### 代码（Python）  

```python
# ------------------- 暴力解 -------------------
# 假设输入是两张表的列表形式：
# employees = [{'id':1, 'name':'Joe',   'salary':70000, 'departmentId':1},
#              {'id':2, 'name':'Jim',   'salary':90000, 'departmentId':1},
#              ...]
# departments = [{'id':1, 'name':'IT'},
#                {'id':2, 'name':'Sales'}]

def highest_salary_brute(employees, departments):
    """返回每个部门工资最高的员工信息"""
    res = []                     # 最终结果列表
    # 1️⃣遍历所有部门
    for dept in departments:
        dept_id = dept['id']
        dept_name = dept['name']
        # 2️⃣找该部门的最高工资（遍历所有员工）
        max_salary = float('-inf')   # 初始设为负无穷，保证任何工资都会更大
        for emp in employees:
            if emp['departmentId'] == dept_id:      # 只看同部门的员工
                if emp['salary'] > max_salary:
                    max_salary = emp['salary']
        # 3️⃣把所有工资等于 max_salary 的员工加入结果
        for emp in employees:
            if (emp['departmentId'] == dept_id and
                emp['salary'] == max_salary):
                res.append({
                    'Department': dept_name,
                    'Employee':   emp['name'],
                    'Salary':     emp['salary']
                })
    return res
```

#### 复杂度  

- **时间复杂度：O(m·n)**  
  直白地说：如果部门有 1000 个，员工有 1000 条，就要做 1,000,000 次比较。  
- **空间复杂度：O(1)**（不计输出列表）  
  只用了几个整数和临时变量，和数据规模无关。

---

### 2. 最优解  

#### 思路  
从暴力解可以看到 **瓶颈** 出现在“对每个部门都要遍历所有员工”。  
我们可以把这一步 **合并** 到一次遍历里完成：  

1. **一次遍历** `Employee` 表，使用 **字典**（类似查字典的工具，key 是部门 id，value 是该部门目前看到的最高工资）记录每个部门的最高工资。  
   - 这里的字典相当于 **“部门 → 最高工资”** 的映射表。  
2. 再遍历一次 `Employee`，把工资等于该部门最高工资的员工挑出来。  
   - 因为我们已经在字典里知道每个部门的最高工资，所以只需要一次比较即可。  

> **核心数据结构解释**  
> - **字典（dict）**：把部门 id 当作“钥匙”，对应的最高工资当作“页码”。查找、插入、更新的时间都很快，几乎是 **O(1)**，相当于在一本超大字典里瞬间定位到想要的页。  

> **为什么更快？**  
> - 第一次遍历把 **所有部门的最高工资一次性算完**，只用了 `n` 次比较。  
> - 第二次遍历只需要检查每条员工记录是否等于它所在部门的最高工资，同样是 `n` 次比较。  
> - 整体 **O(n)**，相比暴力的 `O(m·n)`（甚至 `O(n²)`）快了很多。  

> **类比**：想象你要在一座城市里找每条街道的最高楼。暴力解相当于每次找街道都去全城跑一遍；最优解则是先走遍全城一次，记录每条街道的最高楼，然后再把这些信息一次性展示出来。

#### 代码（Python）  

```python
# ------------------- 最优解 -------------------
def highest_salary_optimal(employees, departments):
    """一次遍历求最高工资 + 再一次遍历挑选员工"""
    # 1️⃣ 建立部门 id → 部门名 的映射（方便后面查）
    dept_id_to_name = {d['id']: d['name'] for d in departments}
    
    # 2️⃣ 第一次遍历：求每个部门的最高工资
    max_salary_by_dept = {}                     # dept_id -> max salary
    for emp in employees:
        dept_id = emp['departmentId']
        salary = emp['salary']
        # 如果还没有记录或当前工资更高，就更新
        if dept_id not in max_salary_by_dept or salary > max_salary_by_dept[dept_id]:
            max_salary_by_dept[dept_id] = salary
    
    # 3️⃣ 第二次遍历：挑出工资等于最高工资的员工
    res = []
    for emp in employees:
        dept_id = emp['departmentId']
        if emp['salary'] == max_salary_by_dept[dept_id]:
            res.append({
                'Department': dept_id_to_name[dept_id],
                'Employee':   emp['name'],
                'Salary':     emp['salary']
            })
    return res
```

#### 复杂度  

- **时间复杂度：O(n)**  
  只遍历了两遍员工表，总共做了约 `2n` 次比较。即使部门数很多，也不影响时间，因为我们不再对部门做外层循环。  
- **空间复杂度：O(m)**  
  需要额外的字典存每个部门的最高工资和部门名，大小和部门数量 `m` 成正比。对大多数实际数据来说，这是一块很小的额外空间。

---

## 心得  

- **核心技巧**：**一次遍历统计 + 哈希表（字典）做分组**。  
- **适用场景**：  
  1. “每组的最大 / 最小 / 总和” 类问题，例如“每个学校最高分的学生”。  
  2. “找出每个类别出现次数最多的元素”，如“每种商品的最畅销款”。  
  3. “在日志中找出每个用户的最近一次登录”，需要用字典维护最新时间。  
- **一句话总结**：先用字典把每个部门的最高工资算出来，再一次筛选即可——**“先统计，再过滤”。**

## 反思  

- **第一反应**：直接对每个部门循环遍历所有员工，写出最直观的暴力代码。  
- **最容易踩的坑**：  
  - 忽略了 **并列最高工资** 的情况，只返回了一个员工。  
  - 在统计最高工资时忘记初始化为负无穷，导致所有工资都比默认值大。  
  - 未处理部门表可能出现的 **空部门**（虽然本题保证有对应员工）。  
- **下次思路**：一看到“每组的最大/最小”这类描述，立刻想到 **哈希表分组 + 单次遍历**，先把每组的极值记录下来，再一次筛选。这样既能避免多层循环，又能保证正确处理并列情况。