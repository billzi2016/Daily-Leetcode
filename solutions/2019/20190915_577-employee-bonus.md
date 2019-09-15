# #577. 员工奖金 / Employee Bonus

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/employee-bonus/)

---

## 题目（英文原版）

**Description**

Table: Employee
Table: Bonus
Write a solution to report the name and bonus amount of each employee with a bonus less than 1000.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| empId       | int     |
| name        | varchar |
| supervisor  | int     |
| salary      | int     |
+-------------+---------+
empId is the column with unique values for this table.
Each row of this table indicates the name and the ID of an employee in addition to their salary and the id of their manager.
```

**Example 2:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| empId       | int  |
| bonus       | int  |
+-------------+------+
empId is the column of unique values for this table.
empId is a foreign key (reference column) to empId from the Employee table.
Each row of this table contains the id of an employee and their respective bonus.
```

**Example 3:**

```
Input: 
Employee table:
+-------+--------+------------+--------+
| empId | name   | supervisor | salary |
+-------+--------+------------+--------+
| 3     | Brad   | null       | 4000   |
| 1     | John   | 3          | 1000   |
| 2     | Dan    | 3          | 2000   |
| 4     | Thomas | 3          | 4000   |
+-------+--------+------------+--------+
Bonus table:
+-------+-------+
| empId | bonus |
+-------+-------+
| 2     | 500   |
| 4     | 2000  |
+-------+-------+
Output: 
+------+-------+
| name | bonus |
+------+-------+
| Brad | null  |
| John | null  |
| Dan  | 500   |
+------+-------+
```

---

## 题目（中文翻译）

描述：  
表 **Employee**  
表 **Bonus**  

编写一个查询，报告每位奖金（bonus）小于 1000 的员工的姓名（name）和奖金金额（bonus）。  
返回的结果表顺序任意。结果格式参见下方示例。

**示例 1**  

| Column Name | Type    |
|-------------|---------|
| empId       | int     |
| name        | varchar |
| supervisor  | int     |
| salary      | int     |

`empId` 为该表唯一标识列。每行记录表示员工的姓名、编号、工资以及其上级主管的编号。

**示例 2**  

| Column Name | Type |
|-------------|------|
| empId       | int  |
| bonus       | int  |

`empId` 为该表唯一标识列，并且是 **Employee** 表中 `empId` 的外键（reference column）。每行记录包含员工的编号及其对应的奖金。

**示例 3**  

输入  

Employee 表：

| empId | name   | supervisor | salary |
|-------|--------|------------|--------|
| 3     | Brad   | null       | 4000   |
| 1     | John   | 3          | 1000   |
| 2     | Dan    | 3          | 2000   |
| 4     | Thomas | 3          | 4000   |

Bonus 表：

| empId | bonus |
|-------|-------|
| 2     | 500   |
| 4     | 2000  |

输出  

| name | bonus |
|------|-------|
| Brad | null  |
| John | null  |
| Dan  | 500   |

约束条件：  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把两张表**逐行配对**，就像把两本通讯录的名字一个一个去比对是否是同一个人。  

- **数据结构**：  
  - `Employee` 表可以看成一个装有多条记录的**列表**，每条记录是一个 `dict`（键=列名，值=对应数据）。  
  - `Bonus` 表同理，也是一个列表。  
  - 为了找出同一个员工的 `empId` 是否相同，我们需要遍历**所有组合**——这就是**笛卡尔积**，相当于两本字典里每个词都去找另一本里有没有相同的词。  

- **正确性**：  
  - 对每个员工，我们把 `Bonus` 表里所有行都检查一遍，找到 `empId` 相等的那一行（如果有的话），取出对应的 `bonus`。  
  - 如果没有匹配的 `empId`，就认为该员工的 `bonus` 为 `None`（SQL 中的 `NULL`），而 `None` 按题目要求算作“小于 1000”。  
  - 最后只把 `bonus < 1000`（包括 `None`）的员工加入结果。  

- **时间/空间复杂度**：  
  - 时间上我们对每个员工都要遍历整个 `Bonus` 表，设员工数为 `n`，奖金记录数为 `m`，总共要做 `n × m` 次比较。  
    - 用大白话说，**O(n·m)** 就像“如果你有 10 本书，每本书要看 20 页”，总共要翻 200 页。  
  - 空间上我们只需要保存原始的两个列表和最终的答案，额外空间是 **O(1)**（不随 `n`、`m` 增长的常数）。  

#### 代码（Python）  

```python
# ---------- 暴力解 ---------- #
# 输入示例（实际使用时直接从数据库读取或传入函数参数即可）
employees = [
    {"empId": 3, "name": "Brad",   "supervisor": None, "salary": 4000},
    {"empId": 1, "name": "John",   "supervisor": 3,    "salary": 1000},
    {"empId": 2, "name": "Dan",    "supervisor": 3,    "salary": 2000},
    {"empId": 4, "name": "Thomas", "supervisor": 3,    "salary": 4000},
]

bonuses = [
    {"empId": 2, "bonus": 500},
    {"empId": 4, "bonus": 2000},
]

def employee_bonus_brute(employees, bonuses):
    """返回 name 与 bonus（bonus<1000 或 None）的列表，顺序不限"""
    result = []
    for emp in employees:                     # 遍历每个员工
        emp_bonus = None                      # 默认没有奖金 → None
        for b in bonuses:                     # 暴力遍历 Bonus 表
            if b["empId"] == emp["empId"]:    # 找到同一个 empId
                emp_bonus = b["bonus"]
                break                         # Bonus 表里每个 empId 只会出现一次，找到后可以退出内层循环
        # 根据题意，None 也算作小于 1000
        if emp_bonus is None or emp_bonus < 1000:
            result.append({"name": emp["name"], "bonus": emp_bonus})
    return result

# 运行示例
print(employee_bonus_brute(employees, bonuses))
```

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - `n` 为员工数量，`m` 为奖金记录数量。每个员工都要遍历所有奖金记录。  
- **空间复杂度**：`O(1)`（不计结果列表）  
  - 只用了常数级的额外变量 `emp_bonus`、循环计数器等。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 出在内层的线性搜索：每找一次 `empId` 都要遍历整个 `Bonus` 表。  
如果我们把 `Bonus` 表先整理成 **“键-值映射”**（即哈希表 / 字典），就可以在 **O(1)** 时间内直接拿到某个 `empId` 对应的奖金，省掉那层循环。  

- **核心数据结构：哈希表（Python 的 dict）**  
  - 想象一本“电话簿”，你只要把人的名字（这里是 `empId`）写在左边，电话号码（这里是 `bonus`）写在右边。  
  - 查找某个人的电话号码只需要一次“快速定位”，不需要遍历整本电话簿。  

- **步骤**  
  1. **预处理 Bonus 表**：遍历一次 `bonuses`，把每条记录放进字典 `bonus_map[empId] = bonus`。  
  2. **遍历 Employee 表**：对每个员工，直接用 `bonus_map.get(empId)` 取出对应奖金（如果不存在返回 `None`）。  
  3. **过滤**：只保留 `bonus` 为 `None` 或 `< 1000` 的记录。  

- **为什么 O(n+m) 是最优**  
  - 我们必须至少看一遍两张表（因为每条记录都可能影响答案），这已经是 **Ω(n+m)** 的下界。  
  - 使用哈希表恰好达到了这个下界，没有多余的遍历或嵌套循环。  

#### 代码（Python）  

```python
# ---------- 最优解（哈希表） ---------- #
def employee_bonus_optimal(employees, bonuses):
    """O(n+m) 时间完成，同样返回 name 与 bonus（bonus<1000 或 None）的列表"""
    # 1. 把 Bonus 表变成哈希表：empId -> bonus
    bonus_map = {b["empId"]: b["bonus"] for b in bonuses}
    # 2. 逐个员工查找对应的 bonus
    result = []
    for emp in employees:
        emp_bonus = bonus_map.get(emp["empId"])   # 若 empId 不在字典中返回 None
        if emp_bonus is None or emp_bonus < 1000:
            result.append({"name": emp["name"], "bonus": emp_bonus})
    return result

# 运行示例
print(employee_bonus_optimal(employees, bonuses))
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 第一次遍历 `bonuses`（`m` 次）构造哈希表，第二次遍历 `employees`（`n` 次）直接查询。  
  - 与暴力解的 `O(n·m)` 相比，提升巨大——比如 `n = 10^5`、`m = 10^5` 时，暴力解需要 10^10 次比较，而最优解只要 2×10^5 次。  

- **空间复杂度**：`O(m)`  
  - 需要额外存放 `bonus_map`，大小等同于 `bonuses` 表的记录数。  
  - 这相当于把“电话簿”装进内存，换取查询的高速。  

---  

## 心得  

- **核心技巧**：利用哈希表（字典）把 **一对多** 的关联查询转化为 **常数时间** 的键值查找。  
- **适用的题型**：  
  1. 两表关联后只需要 **判断是否存在** 或 **取出单个字段**（如 `Employee` & `Salary`、`Customer` & `Orders`）。  
  2. “统计类”问题：如统计每个单词出现次数、统计每个用户的登录次数等，都可以先把计数放在字典里。  
  3. “过滤类”问题：给定一组黑名单，快速判断某条记录是否在黑名单里。  
- **一句话总结**：**先把要频繁查找的表做成哈希表，后遍历主表即可实现线性时间的关联查询**。  

## 反思  

- **第一反应**：看到两张表要关联，直接想到 **JOIN**，于是想到用两层循环把每行配对——这就是暴力思路。  
- **最容易踩的坑**：  
  - **忘记处理左表中没有对应 Bonus 的情况**，导致 `None` 被误判为 `0` 或直接丢掉。  
  - **比较时的空值**：在 Python 中 `None < 1000` 会报错，必须先判断 `None` 再比较。  
- **下次遇到同类题**：第一步先问自己——“有没有可以一次遍历后直接查询的键？”如果有，就立刻构造哈希表；如果没有，再考虑更复杂的算法（如排序+双指针、前缀和等）。