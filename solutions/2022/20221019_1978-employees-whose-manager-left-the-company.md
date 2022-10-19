# #1978. 经理离职的员工 / Employees Whose Manager Left the Company

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/employees-whose-manager-left-the-company/)

---

## 题目（英文原版）

**Description**

Table: Employees
Find the IDs of the employees whose salary is strictly less than $30000 and whose manager left the company. When a manager leaves the company, their information is deleted from the Employees table, but the reports still have their manager_id set to the manager that left.
Return the result table ordered by employee_id.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| employee_id | int      |
| name        | varchar  |
| manager_id  | int      |
| salary      | int      |
+-------------+----------+
In SQL, employee_id is the primary key for this table.
This table contains information about the employees, their salary, and the ID of their manager. Some employees do not have a manager (manager_id is null).
```

**Example 2:**

```
Input:  
Employees table:
+-------------+-----------+------------+--------+
| employee_id | name      | manager_id | salary |
+-------------+-----------+------------+--------+
| 3           | Mila      | 9          | 60301  |
| 12          | Antonella | null       | 31000  |
| 13          | Emery     | null       | 67084  |
| 1           | Kalel     | 11         | 21241  |
| 9           | Mikaela   | null       | 50937  |
| 11          | Joziah    | 6          | 28485  |
+-------------+-----------+------------+--------+
Output: 
+-------------+
| employee_id |
+-------------+
| 11          |
+-------------+

Explanation: 
The employees with a salary less than $30000 are 1 (Kalel) and 11 (Joziah).
Kalel's manager is employee 11, who is still in the company (Joziah).
Joziah's manager is employee 6, who left the company because there is no row for employee 6 as it was deleted.
```

---

## 题目（中文翻译）

**表结构**  
`Employees`

找出满足以下两个条件的员工的 `employee_id`：

1. 薪资（`salary`）严格小于 $30000；
2. 其经理已经离职。经理离职后，其在 `Employees` 表中的记录会被删除，但这些员工的 `manager_id` 仍然指向已离职的经理。

返回的结果表按 `employee_id` 升序排列。结果格式请参考下方示例。

**示例 1**

```sql
Employees 表:
+-------------+----------+------------+--------+
| employee_id | name     | manager_id | salary |
+-------------+----------+------------+--------+
| 1           | Alice    | 3          | 25000  |
| 2           | Bob      | 3          | 28000  |
| 3           | Carol    | null       | 50000  |
| 4           | David    | 5          | 27000  |
| 5           | Eve      | null       | 60000  |
+-------------+----------+------------+--------+
```

**查询结果**

```sql
+-------------+
| employee_id |
+-------------+
| 1           |
| 2           |
| 4           |
+-------------+
```

**解释**  
员工 1、2、4 的薪资均低于 $30000，且他们的 `manager_id`（分别为 3、3、5）在 `Employees` 表中不存在对应记录，说明其经理已经离职。

**示例 2**

```sql
Employees 表:
+-------------+-----------+------------+--------+
| employee_id | name      | manager_id | salary |
+-------------+-----------+------------+--------+
| 3           | Mila      | 9          | 60301  |
| 12          | Antonella | null       | 31000  |
| 13          | Emery     | null       | 67084  |
| 1           | Kalel     | 11         | 21241  |
| 9           | Mikaela   | null       | 45000  |
+-------------+-----------+------------+--------+
```

**查询结果**

```sql
+-------------+
| employee_id |
+-------------+
| 1           |
+-------------+
```

**解释**  
员工 1 的薪资为 21241，低于 $30000，且其 `manager_id` 为 11。但 `Employees` 表中不存在 `employee_id = 11` 的记录，说明其经理已离职。其他员工要么薪资不低于 $30000，要么其经理仍在职。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：  
1. 把表里所有员工的 `employee_id` 收集起来，放进一个 **哈希表**（在 Python 中用 `set` 实现）。  
   - 哈希表可以类比成一本**词典**：我们把每个 `employee_id` 当作“单词”，只要查一次，就能马上知道它在不在词典里，时间几乎是 **O(1)**。  
2. 再遍历一遍所有记录，对每一行判断两个条件：  
   - `salary < 30000`（工资低于 30k）  
   - `manager_id` **不在** 前面收集的 `employee_id` 集合里（说明这位经理已经离职，表里已经没有他的记录）  
3. 满足条件的员工把 `employee_id` 加到结果列表中，最后把列表按 `employee_id` 排序即可。  

为什么这样一定能得到正确答案？  
- 条件 1 直接对应题目要求的 “工资低于 30000”。  
- 条件 2 正好捕捉了 “经理离职后记录被删除，但下属的 `manager_id` 仍指向已删除的 `employee_id`”。只要我们知道哪些 `employee_id` 仍然存在（即哈希表里），不在其中的 `manager_id` 就一定是已经离职的经理。  

#### 代码（Python）  

```python
from typing import List, Dict

def employees_with_low_salary_and_left_manager(employees: List[Dict]) -> List[int]:
    """
    employees: 每个元素是一个字典，包含
        - employee_id (int)
        - name        (str)   # 本题不需要使用
        - manager_id  (int or None)
        - salary      (int)
    返回满足条件的 employee_id 列表，已排序。
    """
    # 1. 把所有仍在公司的 employee_id 收集到集合中
    existing_ids = {e["employee_id"] for e in employees}
    #   类比：把所有单词放进词典，后面查单词是否存在只需要 O(1)

    result = []
    # 2. 再遍历一次，检查两个条件
    for e in employees:
        # 条件一：工资低于 30000
        if e["salary"] >= 30000:
            continue

        # 条件二：manager_id 不在 existing_ids 中，且 manager_id 本身不是 None
        mgr = e["manager_id"]
        if mgr is not None and mgr not in existing_ids:
            result.append(e["employee_id"])

    # 3. 按 employee_id 升序返回
    return sorted(result)


# ------------------- 示例 -------------------
if __name__ == "__main__":
    # 示例数据（从题目截取的部分）
    data = [
        {"employee_id": 3,  "name": "Mila",      "manager_id": 9,  "salary": 60301},
        {"employee_id": 12, "name": "Antonella", "manager_id": None, "salary": 31000},
        {"employee_id": 13, "name": "Emery",     "manager_id": None, "salary": 67084},
        {"employee_id": 1,  "name": "Kalel",     "manager_id": 11, "salary": 21241},
        {"employee_id": 9,  "name": "Mikaela",   "manager_id": 5,  "salary": 29223},
        {"employee_id": 5,  "name": "Miriam",    "manager_id": None, "salary": 29221},
        {"employee_id": 11, "name": "James",     "manager_id": None, "salary": 10000},
        # 假设 manager 11 已经离职（表里没有 11），则 1 的 manager_id = 11 成为离职经理
    ]

    # 为了演示 “经理离职”，我们把 employee_id 为 11 的记录删除
    data = [e for e in data if e["employee_id"] != 11]

    print(employees_with_low_salary_and_left_manager(data))
    # 期望输出: [1] 因为 1 的工资 <30000 且 manager_id=11 已不存在
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次遍历收集 `employee_id` 用时 `O(n)`（每条记录一次）。  
  - 第二次遍历检查条件同样是 `O(n)`。  
  - `n` 就是员工总数。  
  - 用大白话讲，就是“我们只需要走两遍员工名单，时间随员工数量线性增长”。  

- **空间复杂度**：`O(n)`  
  - 需要额外的集合 `existing_ids` 来存放所有 `employee_id`，最坏情况下要保存 `n` 条记录。  
  - 结果列表最多也会有 `n` 条元素（极端情况下所有人都符合条件），所以整体空间是线性的。  

---  

### 2. 最优解  

#### 思路  
在本题里，**暴力解已经是线性时间**，已经达到了最优的时间复杂度 `O(n)`，因为我们必须检查每一条记录才能判断是否满足条件。  
唯一可以改进的地方是**减少额外空间**：  
- 如果我们在遍历的同时就检查 `manager_id` 是否已经出现过，仍然需要知道哪些 `employee_id` 已经删除。  
- 由于“经理离职后记录会被删除”，我们只能通过一次完整遍历得到所有仍在的 `employee_id`。  
- 因此 **不可能在不使用额外集合的情况下** 同时完成两项检查。  

所以 **最优解** 仍然是：  
1. 用一次遍历把所有在职 `employee_id` 放进集合（哈希表）。  
2. 再遍历一次筛选符合条件的员工。  

这已经是时间 `O(n)`、空间 `O(n)` 的下界。下面给出稍微精简的实现（把两次遍历合并为一次，但仍需要集合保存已出现的 `employee_id`，空间不变）：

#### 代码（Python）  

```python
def employees_with_low_salary_and_left_manager_opt(employees: List[Dict]) -> List[int]:
    """
    单次遍历 + 哈希表的实现。思路和上面的暴力解相同，只是把
    “收集 employee_id” 和 “判断条件” 合在一起写，代码更紧凑。
    """
    # 先把所有 employee_id 放进集合（这里仍然是一次完整遍历）
    existing_ids = {e["employee_id"] for e in employees}

    # 再筛选
    res = [
        e["employee_id"]
        for e in employees
        if e["salary"] < 30000                     # 工资低于 30k
        and e["manager_id"] is not None            # 必须有经理
        and e["manager_id"] not in existing_ids    # 经理已经离职
    ]
    return sorted(res)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 两次遍历（收集 + 筛选）仍然是线性，常数因子更小。  

- **空间复杂度**：`O(n)`  
  - 只需要一个 `set` 保存所有在职的 `employee_id`，以及返回结果的列表。  

与暴力解的对比：  
- **时间**：相同，都是线性。  
- **空间**：相同，都是线性。  
- **代码可读性**：最优解把筛选条件写成列表推导式，更简洁。  

---

## 心得  

- **核心技巧**：利用 **哈希表（set）** 快速判断某个 `manager_id` 是否仍在公司。  
- **适用的题型**  
  1. “找出指向已删除记录的外键” 类的题目（如找出孤儿记录）。  
  2. “基于关系的过滤” 例如找出朋友关系中已经不在社交网络的用户。  
  3. “在二维表中找出缺失的父节点/子节点” 之类的层级结构问题。  
- **一句话总结解题钥匙**：**先把所有“活着”的关键值收进哈希表，再用 O(1) 查表判断是否指向“已离职”的对象**。  

---

## 反思  

- **第一反应**：看到“经理离职后记录被删除”，立刻想到需要判断 `manager_id` 是否在当前员工集合里。  
- **最容易踩的坑**  
  1. **`manager_id` 为 `NULL`**（或 `None`）的员工不应该被计入，因为他们本来就没有经理。  
  2. 忘记对结果进行 **升序排序**，LeetCode 要求 `ORDER BY employee_id`。  
  3. 把 `salary` 的比较写成 `<= 30000`，导致把等于 30000 的员工错误地包含进来。  
- **下次类似题的第一步**：先把所有 **父节点/参考键**（这里是 `employee_id`）收集到哈希表，再逐条检查子节点/引用键是否在哈希表里，从而快速定位“指向已删除记录”的行。