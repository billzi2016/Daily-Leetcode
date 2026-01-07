# #3482. 分析组织层级 / Analyze Organization Hierarchy

> 难度：困难 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/analyze-organization-hierarchy/)

---

## 题目（英文原版）

**Description**

Table: Employees
Write a solution to analyze the organizational hierarchy and answer the following:
Return the result table ordered by the result ordered by level in ascending order, then by budget in descending order, and finally by employee_name in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+----------------+---------+
| Column Name    | Type    | 
+----------------+---------+
| employee_id    | int     |
| employee_name  | varchar |
| manager_id     | int     |
| salary         | int     |
| department     | varchar |
+----------------+----------+
employee_id is the unique key for this table.
Each row contains information about an employee, including their ID, name, their manager's ID, salary, and department.
manager_id is null for the top-level manager (CEO).
```

**Example 2:**

```
+-------------+---------------+------------+--------+-------------+
| employee_id | employee_name | manager_id | salary | department  |
+-------------+---------------+------------+--------+-------------+
| 1           | Alice         | null       | 12000  | Executive   |
| 2           | Bob           | 1          | 10000  | Sales       |
| 3           | Charlie       | 1          | 10000  | Engineering |
| 4           | David         | 2          | 7500   | Sales       |
| 5           | Eva           | 2          | 7500   | Sales       |
| 6           | Frank         | 3          | 9000   | Engineering |
| 7           | Grace         | 3          | 8500   | Engineering |
| 8           | Hank          | 4          | 6000   | Sales       |
| 9           | Ivy           | 6          | 7000   | Engineering |
| 10          | Judy          | 6          | 7000   | Engineering |
+-------------+---------------+------------+--------+-------------+
```

**Example 3:**

```
+-------------+---------------+-------+-----------+--------+
| employee_id | employee_name | level | team_size | budget |
+-------------+---------------+-------+-----------+--------+
| 1           | Alice         | 1     | 9         | 84500  |
| 3           | Charlie       | 2     | 4         | 41500  |
| 2           | Bob           | 2     | 3         | 31000  |
| 6           | Frank         | 3     | 2         | 23000  |
| 4           | David         | 3     | 1         | 13500  |
| 7           | Grace         | 3     | 0         | 8500   |
| 5           | Eva           | 3     | 0         | 7500   |
| 9           | Ivy           | 4     | 0         | 7000   |
| 10          | Judy          | 4     | 0         | 7000   |
| 8           | Hank          | 4     | 0         | 6000   |
+-------------+---------------+-------+-----------+--------+
```

---

## 题目（中文翻译）

**表结构**：`Employees`

编写一个解决方案来分析组织层级并回答以下要求：

- 返回的结果表需按 **层级（level）** 升序排序，若层级相同则按 **预算（budget）** 降序排序，再者按 **员工姓名（employee_name）** 升序排序。
- 结果格式请参考下面的示例。

**示例 1**  

```
+----------------+---------+
| Column Name    | Type    |
+----------------+---------+
| employee_id    | int     |
| employee_name  | varchar |
| manager_id     | int     |
| salary         | int     |
| department     | varchar |
+----------------+----------+
```

`employee_id` 为该表的唯一键。  
每一行记录一名员工的信息，包括其 ID、姓名、直接上级的 `manager_id`、薪资 `salary` 以及所在部门 `department`。

**示例 2**  

```
+-------------+---------------+------------+--------+------------+
| employee_id | employee_name | manager_id | salary | department |
+-------------+---------------+------------+--------+------------+
| 1           | Alice         | null       | 12000  | Executive  |
| 2           | Bob           | 1          | 10000  | Sales      |
| 3           | Charlie       | 1          | 10000  | Engineering|
| ... (已截断)
```

**示例 3（返回结果）**  

```
+-------------+---------------+-------+-----------+--------+
| employee_id | employee_name | level | team_size | budget |
+-------------+---------------+-------+-----------+--------+
| 1           | Alice         | 1     | 9         | 84500  |
| 3           | Charlie       | 2     | 4         | 41500  |
| 2           | Bob           | 2     | 3         | 31000  |
| 6           | Frank         | 3     | ...       | ...    |
| ... (已截断)
```

**约束条件**  
无。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题要求把一张员工表 **Employees** 里每个人的层级（level）、团队规模（team_size）以及团队预算（budget）算出来，然后按照层级升序、预算降序、姓名升序输出。  

最直接的做法是**对每一行都单独遍历整张表**：

1. **层级（level）**  
   - 从当前员工的 `manager_id` 向上找，直到 `manager_id` 为 `None`（即公司最高层）。找了几次就等于该员工的层级。  
   - 这一步类似“追溯家谱”，每次都要在整张表里找对应的上级，最坏要找 `n-1` 次。

2. **团队规模（team_size）**  
   - 团队规模指的是 **包括自己在内的所有下属**（直接的 + 间接的）。  
   - 暴力做法是：遍历整张表，判断每个其它员工是否是当前员工的**直接或间接**下属。判断是否为下属同样需要沿着 `manager_id` 链向上查找，直到根或找到目标上级。

3. **团队预算（budget）**  
   - 与团队规模类似，只是把找到的所有下属（包括自己）的 `salary` 加起来。

> **类比**：  
> - `manager_id` 就像字典里的 “父键”。查找上级相当于在字典里 **查字典**：给出一个词（员工），一直往上翻页（找上级），直到看到封面（`None`）。  
> - 团队规模/预算的判断类似“在一棵树里找所有子树的节点”。我们每次都要把整棵树遍历一遍，效率很低。

只要把这三件事都写出来，就能得到正确答案——因为我们把 **每个员工的所有信息都完整算出来** 了。

#### 代码（Python）

```python
# ------------------- 暴力解 -------------------
# 输入：employees 为列表，每个元素是 (employee_id, employee_name, manager_id, salary, department)
# 输出：列表，每行 (employee_id, employee_name, level, team_size, budget)

def brute_force(employees):
    # 为了快速根据 id 找员工信息，先建立一个 id -> 记录 的映射（类似字典查找）
    emp_map = {e[0]: e for e in employees}

    # ----------------- 计算层级 -----------------
    def get_level(emp_id):
        """沿着 manager_id 向上走，走几步就是层级"""
        level = 1
        cur = emp_map[emp_id]
        while cur[2] is not None:          # manager_id 不为 None
            level += 1
            cur = emp_map[cur[2]]          # 跳到上级
        return level

    # ----------------- 判断下属关系 -----------------
    def is_subordinate(sub_id, sup_id):
        """判断 sub_id 是否是 sup_id 的直接或间接下属"""
        cur = emp_map[sub_id]
        while cur[2] is not None:          # 向上遍历
            if cur[2] == sup_id:
                return True
            cur = emp_map[cur[2]]
        return False

    result = []
    for emp in employees:
        emp_id, name = emp[0], emp[1]

        # 1. 层级
        level = get_level(emp_id)

        # 2. 团队规模 & 3. 预算
        team_size = 0
        budget = 0
        for other in employees:
            if other[0] == emp_id or is_subordinate(other[0], emp_id):
                team_size += 1
                budget += other[3]       # salary

        result.append((emp_id, name, level, team_size, budget))

    # 按题目要求排序：level 升序、budget 降序、employee_name 升序
    result.sort(key=lambda x: (x[2], -x[4], x[1]))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个员工都要遍历整张表（`n` 次），而在遍历过程中还可能再向上追溯链条（最坏 `O(n)`），整体仍是 `n × n` 的量级。  
  - 用大白话说，就是 **如果有 10 000 名员工，代码会做大约 1 亿 次“查上级”或“判断下属”的操作**，会比较慢。

- **空间复杂度**：`O(n)`  
  - 只用了一个 `emp_map`（字典）保存所有记录，以及结果列表。额外的递归栈或临时变量都和 `n` 成线性关系。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **重复遍历**：  
- 计算层级时，每个员工都要从自己一直往上爬到根。  
- 计算团队规模/预算时，又要对每对员工检查上下级关系。

如果把所有员工的上下级关系一次性组织好，就可以 **只遍历一次** 就把层级、子树规模、子树工资全部算出来。

**核心技巧**：把 `manager_id` → `employee_id` 的关系视作一棵（或多棵）**有向树**（根是 `manager_id = NULL` 的员工）。  
- **层级**：在树的深度优先遍历（DFS）或广度优先遍历（BFS）时，自根向下传递当前深度即可。  
- **团队规模 & 预算**：在 **后序遍历**（即先处理子节点，再处理父节点）时，父节点可以把子节点返回的 `team_size` 与 `budget` 累加到自己身上。

实现步骤：

1. **构建邻接表** `children`：键是 manager_id，值是直接下属的列表。相当于 “一个部门的所有成员”。这一步只遍历一次 `O(n)`。
2. **找到根节点**（`manager_id is None`），可能有多个根（多个独立公司）。
3. **深度优先搜索**（递归或显式栈）  
   - 进入节点时记录 `level = parent_level + 1`。  
   - 递归遍历所有子节点，得到它们的 `team_size`、`budget`。  
   - 当前节点的 `team_size = 1 + sum(child.team_size)`（加上自己），`budget = salary + sum(child.budget)`。  
   - 将结果保存到全局列表中。

这样每个员工只被访问 **一次**，所有信息在一次遍历中完成，时间复杂度降到线性。

> **类比**：  
> - 把公司结构想象成一棵“家谱树”。先把每个人的子女（直接下属）放进盒子里（邻接表），再从祖先（CEO）往下走，记录每层的代数（level），把每个人的子孙的数量和财富累计上来。一次走完，所有信息一次性得到。

#### 代码（Python）

```python
# ------------------- 最优解（DFS） -------------------
# 输入输出同上

from collections import defaultdict

def optimal(employees):
    # 1️⃣ 建立 id -> 记录 的映射，方便随时取 salary、name 等信息
    emp_map = {e[0]: {'name': e[1], 'manager': e[2], 'salary': e[3]} for e in employees}

    # 2️⃣ 构造邻接表 children[parent_id] = [child_id, ...]
    children = defaultdict(list)
    roots = []                     # manager_id 为 None 的员工
    for emp_id, info in emp_map.items():
        mgr = info['manager']
        if mgr is None:
            roots.append(emp_id)
        else:
            children[mgr].append(emp_id)

    # 结果列表
    result = []

    # 3️⃣ 深度优先遍历（后序）计算 level、team_size、budget
    def dfs(node_id, level):
        """返回 (team_size, budget)"""
        name   = emp_map[node_id]['name']
        salary = emp_map[node_id]['salary']

        total_size = 1          # 包含自己
        total_budget = salary   # 包含自己的工资

        # 先递归子节点，累加子树信息
        for child in children.get(node_id, []):
            child_size, child_budget = dfs(child, level + 1)
            total_size   += child_size
            total_budget += child_budget

        # 把当前员工的信息加入结果
        result.append((node_id, name, level, total_size, total_budget))
        return total_size, total_budget

    # 可能有多个根，逐个遍历
    for r in roots:
        dfs(r, 1)                # 根节点的层级是 1

    # 4️⃣ 按题目要求排序
    result.sort(key=lambda x: (x[2], -x[4], x[1]))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个员工只进入一次 `dfs`，在函数内部只做常数次操作（遍历自己的直接下属列表）。因此整体随员工数量线性增长。  
  - 与暴力解的 `O(n²)` 相比，人数翻倍只会把运行时间翻倍，而不是平方级的爆炸。

- **空间复杂度**：`O(n)`  
  - `emp_map`、`children`、`result` 都是线性大小。  
  - 递归调用栈最坏深度等于树的高度，最坏情况下（链式结构）也是 `O(n)`，但仍是线性级别。

---

## 心得

- **核心技巧**：把“上下级关系”抽象成 **树结构**，用 **深度优先遍历（后序）** 一次性计算层级、子树规模、子树和。  
- **适用场景**  
  1. 组织结构、部门树等需要统计子树信息的题目（例如 LeetCode 1527 “Patients With a Certain Condition”）。  
  2. 文件系统、目录树的空间占用统计。  
  3. 计算二叉树每个节点的子树节点数或子树和（经典 DP on Tree）。  
- **一句话总结**：**把层级关系建成树，后序遍历一次搞定所有子树聚合**。

---

## 反思

- **第一反应**：看到 `manager_id` 这种自指字段，立刻想到“树”。但最开始往往会走向“遍历每个人、每次都向上追溯”，导致暴力 `O(n²)` 的实现。  
- **最容易踩的坑**  
  - **根节点不止一个**（有多个 `manager_id = NULL`），必须把所有根都遍历。  
  - **递归深度**：极端链式结构可能导致递归层数很深，实际 Python 需要注意递归深度上限（可改为显式栈）。  
  - **排序细节**：层级升序、预算降序、姓名升序的三重键必须写对，容易写成预算升序导致结果不符。  
- **下次类似题**：先 **画出树的结构**，确认是否可以一次遍历完成所有聚合；如果可以，就直接使用 **DFS/BFS + DP on Tree**，避免重复遍历。