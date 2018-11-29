# #185. **部门前三高薪资** / Department Top Three Salaries

> 难度：困难 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/department-top-three-salaries/)

---

## 题目（英文原版）

**Description**

Table: Employee
Table: Department
A company's executives are interested in seeing who earns the most money in each of the company's departments. A high earner in a department is an employee who has a salary in the top three unique salaries for that department.
Write a solution to find the employees who are high earners in each of the departments.
Return the result table in any order.
The result format is in the following example.

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
departmentId is a foreign key (reference column) of the ID from the Department table.
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
id is the primary key (column with unique values) for this table.
Each row of this table indicates the ID of a department and its name.
```

**Example 3:**

```
Input: 
Employee table:
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |
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
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
Explanation: 
In the IT department:
- Max earns the highest unique salary
- Both Randy and Joe earn the second-highest unique salary
- Will earns the third-highest unique salary

In the Sales department:
- Henry earns the highest salary
- Sam earns the second-highest salary
- There is no third-highest salary as there are only two employees
```

**Constraints**

- There are no employees with the exact same name, salary and department.

---

## 题目（中文翻译）

描述  
公司高层希望了解每个部门的最高收入员工。部门中的高收入者指在该部门 **薪资（salary）** 位列前三的唯一薪资的员工（即去重后的前三名）。  
请编写 SQL 查询，找出每个部门的高收入者。返回的结果表顺序不限，格式参见下方示例。

**表结构**

`Employee` 表：

| 列名 | 类型 |
|------|------|
| id | int |
| name | varchar |
| salary | int |
| departmentId | int |

- `id` 为主键（唯一值列）。  
- `departmentId` 为外键，引用 `Department` 表的 `id`。  
- 每行记录表示一名 **员工（Employee）** 的编号、姓名、薪资以及所在部门的编号。

`Department` 表：

| 列名 | 类型 |
|------|------|
| id | int |
| name | varchar |

- `id` 为主键。  
- 每行记录表示一个 **部门（Department）** 的编号和名称。

**示例**

输入  

`Employee` 表：

```
+----+-------+--------+--------------+
| id | name  | salary | departmentId |
+----+-------+--------+--------------+
| 1  | Joe   | 85000  | 1            |
| 2  | Henry | 80000  | 2            |
| 3  | Sam   | 60000  | 2            |
| 4  | Max   | 90000  | 1            |
| 5  | Janet | 69000  | 1            |
| 6  | Randy | 85000  | 1            |
| 7  | Will  | 70000  | 1            |
+----+-------+--------+--------------+
```

`Department` 表：

```
+----+-------+
| id | name  |
+----+-------+
| 1  | IT    |
| 2  | Sales |
+----+-------+
```

输出  

```
+------------+----------+--------+
| Department | Employee | Salary |
+------------+----------+--------+
| IT         | Max      | 90000  |
| IT         | Joe      | 85000  |
| IT         | Randy    | 85000  |
| IT         | Will     | 70000  |
| Sales      | Henry    | 80000  |
| Sales      | Sam      | 60000  |
+------------+----------+--------+
```

**解释**  
在 IT 部门：  
- Max 的薪资最高。  
- Randy 和 Joe 的薪资并列第二高。  
- Will 的薪资位列第三高。  

在 Sales 部门：  
- Henry 的薪资最高。  
- Sam 的薪资第二高。  
- 由于该部门仅有两名员工，不存在第三高的薪资。

**约束条件**  
- 不存在 **员工（Employee）** 的姓名、薪资和部门同时相同的记录。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每个部门** 的员工都挑出来，分别统计该部门的 **所有不同的工资**，把这些工资从高到低排个序，取前 3 个（如果不足 3 个就全取），再把工资在这 3 个之中的员工全部返回。

可以把它想象成：

* **部门** 像是不同的课堂，  
* **工资** 像是学生的成绩单，  
* 我们先把每个课堂的成绩单全部收集起来，去掉重复的成绩（因为题目要求“唯一的工资”），再把成绩单从高到低排好，选出前三名，最后把这些成绩对应的学生找出来。

**为什么这样一定对？**  
因为题目只要求“工资在该部门的前三个唯一工资之中”，只要我们正确得到每个部门的前三个唯一工资，然后把拥有这些工资的员工全部列出，就满足了要求。

**时间/空间复杂度**（大白话）  

* 暴力解要对每个部门都遍历所有员工，最坏情况下部门数是 `1`，于是我们会 **对每个员工都做一次完整的遍历**，这相当于 **`N`（员工数） × `N`**，也就是 **`O(N²)`**，可以想象成“把 `N` 本书每本都翻一遍”。  
* 为了记录每个部门的工资集合，需要额外的 **哈希表**（类似字典）来存放每个部门出现过的工资，最坏需要保存所有员工的工资，空间是 **`O(N)`**。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Dict, Tuple

# -------------------------------------------------
# 1. 暴力解：先收集每个部门的所有唯一工资，再筛选员工
# -------------------------------------------------
def high_earners_bruteforce(employees: List[Dict],
                            departments: List[Dict]) -> List[Tuple[str, str, int]]:
    """
    employees:   [{'id':1, 'name':'Joe',   'salary':85000, 'departmentId':1}, ...]
    departments: [{'id':1, 'name':'IT'}, {'id':2, 'name':'Sales'}]
    返回值:      [(部门名, 员工名, 工资), ...]
    """
    # 1）部门 id -> 部门名字（相当于查字典，key 是 id，value 是名字）
    dept_name = {d['id']: d['name'] for d in departments}

    # 2）收集每个部门出现过的所有工资（使用 set 去重，类似把工资写进“集合盒子”）
    salary_set = defaultdict(set)          # dept_id -> {salary1, salary2, ...}
    for emp in employees:
        salary_set[emp['departmentId']].add(emp['salary'])

    # 3）对每个部门的工资集合排序，取前三个（如果不足三就全取）
    top3_salary = {}                        # dept_id -> [最高, 第二高, 第三高]
    for dept_id, s_set in salary_set.items():
        # sorted(..., reverse=True) 把工资从大到小排好
        top3_salary[dept_id] = sorted(s_set, reverse=True)[:3]

    # 4）遍历员工，再判断其工资是否在对应部门的 top‑3 中
    res = []
    for emp in employees:
        dept_id = emp['departmentId']
        if emp['salary'] in top3_salary.get(dept_id, []):
            res.append((dept_name[dept_id], emp['name'], emp['salary']))

    return res
```

#### 复杂度

* **时间复杂度**：`O(N²)`  
  - 第 2 步遍历所有员工一次是 `O(N)`，  
  - 第 3 步对每个部门的工资集合排序，最坏情况所有员工都在同一个部门，排序要 `O(N log N)`，随后在第 4 步再次遍历所有员工检查 `in`（集合查找是 `O(1)`），但因为我们在每个部门里都要**重新遍历集合**（这里的实现方式导致了二次遍历），整体会退化到 `O(N²)`。  
  - 用大白话讲，就是“每个员工都要被检查很多次”，所以慢。

* **空间复杂度**：`O(N)`  
  - 需要存放每个部门的工资集合以及部门 id→名字的映射，最多保存所有员工的工资，随员工数线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对每个部门都重复遍历所有员工**，以及对工资集合进行多次排序。我们可以把这两件事合并为一次 **全局排序**，然后在一次线性扫描中直接得到每个部门的前 3 个唯一工资。

思路步骤：

1. **把所有员工按部门、工资降序一次性排好**。  
   - 想象把所有课堂的成绩单混在一起，然后先把它们按照“哪个课堂、成绩高低”一次性排好，就不需要每个课堂再单独排。

2. **遍历排好序的列表**，用一个字典记录**每个部门已经看到过多少个不同的工资**。  
   - 当我们看到一个新工资（不同于之前已经计数的工资）时，计数器 +1。  
   - 只要计数器 ≤ 3，就把当前员工加入答案；计数器 > 3 时直接跳过后面的同部门员工（因为它们的工资已经低于前 3 个）。

3. 由于我们在遍历时已经知道部门名字（通过 `departmentId → name` 的映射），可以直接把结果拼装好返回。

核心技巧：

* **一次排序**（`sorted`）把所有数据提前组织好，时间是 `O(N log N)`，这是最常见的“先排好序，再线性扫描”的套路。  
* **字典 + 集合** 记录每个部门已经出现的工资，字典的查找像查字典，`O(1)`，集合的 `add` 与 `in` 同样是 `O(1)`，所以遍历时几乎不花额外时间。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Dict, Tuple

# -------------------------------------------------
# 2. 最优解：一次全局排序 + 线性扫描
# -------------------------------------------------
def high_earners_optimal(employees: List[Dict],
                         departments: List[Dict]) -> List[Tuple[str, str, int]]:
    """
    与上面的函数功能相同，只是实现更快。
    """
    # 1）部门 id -> 部门名字（字典查找，O(1)）
    dept_name = {d['id']: d['name'] for d in departments}

    # 2）把所有员工一次性按照 (departmentId, -salary) 排序
    #    -salary 让工资从大到小排列
    sorted_emps = sorted(employees,
                         key=lambda e: (e['departmentId'], -e['salary']))

    # 3）遍历排序后的列表，记录每个部门已经出现的不同工资数量
    #    dept_id -> (已经出现的不同工资数, 上一次出现的工资值)
    cnt = defaultdict(lambda: (0, None))   # (count, last_salary)
    res = []

    for emp in sorted_emps:
        d_id = emp['departmentId']
        sal = emp['salary']
        cur_cnt, last_sal = cnt[d_id]

        # 如果当前工资和上一次记录的工资不同，说明是一个新的唯一工资
        if sal != last_sal:
            cur_cnt += 1               # 唯一工资数量 +1
            last_sal = sal
            cnt[d_id] = (cur_cnt, last_sal)

        # 只要这个唯一工资的排名不超过 3，就加入答案
        if cur_cnt <= 3:
            res.append((dept_name[d_id], emp['name'], sal))
        # 当 cur_cnt > 3 时，后面的同部门员工工资更低，直接跳过

    return res
```

#### 复杂度

* **时间复杂度**：`O(N log N)`  
  - 只进行一次排序，`log N` 是排序的必然开销。随后一次线性遍历 `O(N)`，整体是 `O(N log N)`。  
  - 与暴力解相比，**从二次遍历降到一次遍历**，速度提升显著。可以把它想成“先把所有书排好序，然后一次顺着书架走过去就能找到前三本书”，不需要每本书再回头翻。

* **空间复杂度**：`O(N)`  
  - 需要保存排序后的列表（相当于复制了一遍数据）以及部门计数的字典，最多和员工数成线性关系。  

---

## 心得

- **核心技巧**：**先全局排序，再用字典记录每个分组的前 k 个唯一值**。这是一种常见的“分组 Top‑k”思路，适用于很多需要“每个类别的前几名”类的问题。  
- **适用的类似题型**  
  1. “每个用户的最近 k 条订单”  
  2. “每个城市的前 3 高温记录”  
  3. “每个课程的前 5 高分学生”  
- **一句话总结解题钥匙**：**一次排序 + 线性扫描 + 按组计数**。

---

## 反思

- **第一反应**：直接把每个部门的工资集合收集出来、排序、取前 3 ，随后再筛选员工——这就是暴力思路。  
- **最容易踩的坑**  
  - **重复工资**：必须先去重，只算唯一的工资，否则会把相同工资算成不同名次。  
  - **部门员工不足 3 人**：要兼容“没有第三高工资”的情况，只取实际出现的工资数。  
  - **计数方式**：在遍历排序列表时，如果不判断“当前工资是否和上一次相同”，会把相同工资误算成多个不同名次。  
- **下次遇到同类题**：第一步想到 **“先把数据整体排序，然后在一次遍历中用哈希表记录每个组已出现的唯一值数量”**，这样即可高效得到每个组的 Top‑k。