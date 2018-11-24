# #181. Employees Earning More Than Their Managers / Employees Earning More Than Their Managers

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/employees-earning-more-than-their-managers/)

---

## 题目（英文原版）

**Description**

Table: Employee
Write a solution to find the employees who earn more than their managers.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| salary      | int     |
| managerId   | int     |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the ID of an employee, their name, salary, and the ID of their manager.
```

**Example 2:**

```
Input: 
Employee table:
+----+-------+--------+-----------+
| id | name  | salary | managerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | Null      |
| 4  | Max   | 90000  | Null      |
+----+-------+--------+-----------+
Output: 
+----------+
| Employee |
+----------+
| Joe      |
+----------+
Explanation: Joe is the only employee who earns more than his manager.
```

---

## 题目（中文翻译）

**描述**  
表：Employee  
编写一个查询，找出收入（salary）高于其直属经理（manager）的员工。  
返回的结果表顺序任意。结果格式参见下方示例。

**表结构**  

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| name        | varchar |
| salary      | int     |
| managerId   | int     |
+-------------+---------+
```

- `id` 为主键（primary key），即唯一标识每行记录的列。  
- 每条记录表示员工的 ID、姓名、薪资以及其经理的 ID（`managerId`）。  
- `managerId` 为 `NULL` 时，表示该员工没有上级经理。

**示例**  

输入：

```
Employee 表:
+----+-------+--------+-----------+
| id | name  | salary | managerId |
+----+-------+--------+-----------+
| 1  | Joe   | 70000  | 3         |
| 2  | Henry | 80000  | 4         |
| 3  | Sam   | 60000  | Null      |
| 4  | Max   | 90000  | Null      |
+----+-------+--------+-----------+
```

输出：

```
+----------+
| Employee |
+----------+
| Joe      |
+----------+
```

**解释**：只有 Joe 的薪资（70000）高于其经理 Sam（60000），因此结果中只包含 Joe。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
这道题本质上是 **“把每个员工的工资和他的直接上级的工资做比较”**。  
最直接的想法是：

1. 把表 `Employee` 中的每一行（每个员工）拿出来，记作 `e`。  
2. 再遍历一次整张表，找出 **managerId 等于 `e.id` 的那一行**，这行就是 `e` 的经理 `m`。  
3. 比较 `e.salary` 与 `m.salary`，如果前者更大，就把 `e.name` 加入答案。

这里用到的唯一数据结构是 **列表**（存放所有员工记录）和 **字典**（把每行数据当成键值对，便于取字段）。  
可以把 **“遍历表找经理”** 想象成在图书馆里 **“把一本书放在桌子上，然后再把整个书架从头到尾翻一遍找那本对应的参考书”**——很费时间，但最直观。

**为什么这个方法一定能得到正确答案？**  
- 每个员工只有唯一的 `managerId`（如果有的话），遍历整张表一定能找到对应的那位经理（若 `managerId` 为 `NULL`，说明没有经理，直接跳过）。  
- 只要比较一次工资，就能判断是否满足 “员工工资 > 经理工资”。  

#### 代码（Python）

```python
from typing import List, Dict

def employees_earning_more_bruteforce(employees: List[Dict]) -> List[str]:
    """
    暴力解：两层循环逐个比较员工与其经理的工资
    :param employees: 每个元素是 {"id": int, "name": str, "salary": int, "managerId": int|None}
    :return: 符合条件的员工姓名列表
    """
    result = []                         # 用来保存符合条件的员工姓名
    for e in employees:                # 外层循环：遍历每个员工 e
        manager_id = e["managerId"]
        if manager_id is None:         # 没有经理，直接跳过
            continue

        # 内层循环：在所有记录中寻找 id == manager_id 的那位经理 m
        for m in employees:
            if m["id"] == manager_id:  # 找到对应的经理
                # 比较工资
                if e["salary"] > m["salary"]:
                    result.append(e["name"])
                break                 # 找到后即可结束内层循环
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  解释：如果有 `n` 条记录，外层遍历一次是 `n`，每一次都要在全部 `n` 条记录里找经理，最坏情况是 `n × n`，即 `n²`。可以把它想成“把 `n` 本书每本都和所有 `n` 本书比较一次”，显然会花很多时间。  

- **空间复杂度**：`O(1)`（不计输出列表）  
  解释：只用了几个临时变量（`result`、`e`、`m`），占用的额外空间和 `n` 无关，几乎是常数级别。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**瓶颈在于每次都要遍历整张表去找经理**。如果我们能**一次性把 “id → 员工信息” 的对应关系记下来**，后面查经理就可以直接定位，而不必再遍历。

这正是 **哈希表（Python 中的 dict）** 的用武之地：  
- 把每条记录的 `id` 当作 **key**，整条记录（或只需要的字段）当作 **value**，就像“查字典”一样，给出词（id）立刻得到解释（员工信息）。  
- 查找的时间是 **O(1)**，即常数时间，不随数据规模增长。

具体步骤：

1. **第一遍遍历**，把所有员工放进一个字典 `id_to_emp`，键是 `id`，值是对应的记录。  
2. **第二遍遍历**，对每个员工 `e`：  
   - 若 `e.managerId` 为 `None`，说明没有上级，直接跳过。  
   - 否则直接用 `id_to_emp[e.managerId]` 取到经理 `m`（一次哈希查找）。  
   - 比较工资，若 `e.salary > m.salary`，把 `e.name` 加入答案。  

整个过程只需要 **两次线性遍历**，时间降到了 `O(n)`，空间用了一个额外的字典 `O(n)`。

#### 代码（Python）

```python
from typing import List, Dict

def employees_earning_more_optimal(employees: List[Dict]) -> List[str]:
    """
    最优解：利用哈希表把 id → 员工信息的映射提前建立，后续查经理是 O(1)。
    :param employees: 与上面相同的结构列表
    :return: 符合条件的员工姓名列表
    """
    # 第一步：构建 id → 员工记录的映射（相当于建立“查字典”）
    id_to_emp = {e["id"]: e for e in employees}
    # 解释：{键: 值 for ...} 是列表推导式的字典版，遍历一次就把所有记录装进字典

    result = []                     # 用来保存满足条件的员工姓名
    for e in employees:            # 再遍历一次所有员工
        manager_id = e["managerId"]
        if manager_id is None:     # 没有经理，跳过
            continue

        manager = id_to_emp.get(manager_id)   # O(1) 查找经理记录
        # 防御性检查：如果数据不完整，可能找不到经理，这里安全起见加一个判断
        if manager and e["salary"] > manager["salary"]:
            result.append(e["name"])

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：第一次遍历把所有记录放进字典是 `n` 次操作；第二次遍历每个员工只做常数次的哈希查找和比较，同样是 `n` 次。总共是 `2n`，用大 O 表示就是 `O(n)`，即“随员工人数线性增长”。  

- **空间复杂度**：`O(n)`  
  解释：额外用了一个字典保存 `n` 条映射关系，空间随输入规模线性增长。可以把它想成“把所有员工的名片贴在桌面上，随时可以抽取”。  

---  

## 心得  

- **核心技巧**：利用哈希表把 “id → 记录” 的映射提前建立，实现 **常数时间的关联查询**。  
- **适用的题型**：  
  1. **员工/学生/商品等层级关系查询**（如“找出比上司工资高的员工”）。  
  2. **根据某个唯一键快速定位对应记录**（如“两个表的关联查询”“找出相同城市的用户”等）。  
  3. **一对一映射问题**（如“把学生 ID 映射到成绩”）。  
- **一句话总结解题钥匙**：**把需要频繁查找的东西提前放进哈希表，查询就能做到 O(1)。**  

---  

## 反思  

- **第一反应**：看到 “员工”和 “经理” 两个实体，需要两层遍历去比较，想到先写暴力版。  
- **最容易踩的坑**：  
  - `managerId` 为 `NULL`（或 Python 中的 `None`）时，必须跳过，否则会在哈希表里找不到对应键导致错误。  
  - 数据不完整时可能出现 “员工的 managerId 在表中不存在” 的情况，使用 `dict.get` 并加判断可以防止 `KeyError`。  
- **下次遇到同类题**：第一步就问自己 “有没有可以一次性建立的映射（如 id → 信息）”，如果有，就立刻构造哈希表，再进行后续比较或计算。