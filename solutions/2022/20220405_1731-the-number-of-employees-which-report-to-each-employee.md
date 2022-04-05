# #1731. 每位员工的直接下属人数 / The Number of Employees Which Report to Each Employee

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/the-number-of-employees-which-report-to-each-employee/)

---

## 题目（英文原版）

**Description**

Table: Employees
For this problem, we will consider a manager an employee who has at least 1 other employee reporting to them.
Write a solution to report the ids and the names of all managers, the number of employees who report directly to them, and the average age of the reports rounded to the nearest integer.
Return the result table ordered by employee_id.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| employee_id | int      |
| name        | varchar  |
| reports_to  | int      |
| age         | int      |
+-------------+----------+
employee_id is the column with unique values for this table.
This table contains information about the employees and the id of the manager they report to. Some employees do not report to anyone (reports_to is null).
```

**Example 2:**

```
Input: 
Employees table:
+-------------+---------+------------+-----+
| employee_id | name    | reports_to | age |
+-------------+---------+------------+-----+
| 9           | Hercy   | null       | 43  |
| 6           | Alice   | 9          | 41  |
| 4           | Bob     | 9          | 36  |
| 2           | Winston | null       | 37  |
+-------------+---------+------------+-----+
Output: 
+-------------+-------+---------------+-------------+
| employee_id | name  | reports_count | average_age |
+-------------+-------+---------------+-------------+
| 9           | Hercy | 2             | 39          |
+-------------+-------+---------------+-------------+
Explanation: Hercy has 2 people report directly to him, Alice and Bob. Their average age is (41+36)/2 = 38.5, which is 39 after rounding it to the nearest integer.
```

**Example 3:**

```
Input: 
Employees table:
+-------------+---------+------------+-----+ 
| employee_id | name    | reports_to | age |
|-------------|---------|------------|-----|
| 1           | Michael | null       | 45  |
| 2           | Alice   | 1          | 38  |
| 3           | Bob     | 1          | 42  |
| 4           | Charlie | 2          | 34  |
| 5           | David   | 2          | 40  |
| 6           | Eve     | 3          | 37  |
| 7           | Frank   | null       | 50  |
| 8           | Grace   | null       | 48  |
+-------------+---------+------------+-----+ 
Output: 
+-------------+---------+---------------+-------------+
| employee_id | name    | reports_count | average_age |
| ----------- | ------- | ------------- | ----------- |
| 1           | Michael | 2             | 40          |
| 2           | Alice   | 2             | 37          |
| 3           | Bob     | 1             | 37          |
+-------------+---------+---------------+-------------+
```

---

## 题目（中文翻译）

**表结构**  
`Employees`

在本题中，**经理（manager）** 指至少有 1 名其他员工向其汇报的员工。

请编写查询，返回所有经理的 `employee_id`、`name`、直接向其汇报的员工数量，以及这些下属的平均年龄（四舍五入到最近的整数）。  
结果表需按 `employee_id` 升序排序。  
结果格式参考下方示例。

---

## 示例

### 示例 1  

**输入**  

```sql
Employees table:
+-------------+----------+------------+-----+
| employee_id | name     | reports_to | age |
+-------------+----------+------------+-----+
| 1           | Joe      | null       | 30  |
| 2           | Henry    | 1          | 25  |
| 3           | Sam      | 1          | 28  |
| 4           | Max      | 2          | 22  |
| 5           | Linda    | 2          | 24  |
| 6           | Jane     | 3          | 27  |
+-------------+----------+------------+-----+
```

**输出**  

```sql
+-------------+-------+-------------------+-------------------+
| employee_id | name  | reports_count     | average_age       |
+-------------+-------+-------------------+-------------------+
| 1           | Joe   | 2                 | 26                |
| 2           | Henry | 2                 | 23                |
| 3           | Sam   | 1                 | 27                |
+-------------+-------+-------------------+-------------------+
```

**解释**  
- 经理 `Joe`（employee_id = 1）直接有 2 名下属（`Henry`、`Sam`），下属年龄平均值为 (25+28)/2 = 26.5，四舍五入后为 26。  
- 经理 `Henry`（employee_id = 2）直接有 2 名下属（`Max`、`Linda`），平均年龄为 (22+24)/2 = 23。  
- 经理 `Sam`（employee_id = 3）直接有 1 名下属（`Jane`），平均年龄为 27。

---

### 示例 2  

**输入**  

```sql
Employees table:
+-------------+--------+------------+-----+
| employee_id | name   | reports_to | age |
+-------------+--------+------------+-----+
| 9           | Hercy  | null       | 43  |
| 6           | Alice  | 9          | 41  |
| 4           | Bob    | 9          | 36  |
| 2           | Winston| null       | 37  |
+-------------+--------+------------+-----+
```

**输出**  

```sql
+-------------+------+--------------+--------------+
| employee_id | name | reports_count| average_age  |
+-------------+------+--------------+--------------+
| 9           | Hercy| 2            | 39           |
+-------------+------+--------------+--------------+
```

**解释**  
- 只有 `Hercy`（employee_id = 9）是经理，拥有 2 名直接下属（`Alice`、`Bob`），平均年龄为 (41+36)/2 = 38.5，四舍五入后为 39。

---

### 示例 3  

**输入**  

```sql
Employees table:
+-------------+----------+------------+-----+
| employee_id | name     | reports_to | age |
+-------------+----------+------------+-----+
| 1           | Michael  | null       | 45  |
| 2           | Alice    | 1          | 38  |
| 3           | Bob      | 1          | 42  |
| 4           | Charlie  | 2          | 34  |
| 5           | David    | 2          | 40  |
| 6           | Eva      | 3          | 29  |
+-------------+----------+------------+-----+
```

**输出**  

```sql
+-------------+----------+--------------+--------------+
| employee_id | name     | reports_count| average_age  |
+-------------+----------+--------------+--------------+
| 1           | Michael  | 2            | 40           |
| 2           | Alice    | 2            | 37           |
| 3           | Bob      | 1            | 29           |
+-------------+----------+--------------+--------------+
```

**解释**  
- `Michael`（employee_id = 1）直接有 2 名下属（`Alice`、`Bob`），平均年龄为 (38+42)/2 = 40。  
- `Alice`（employee_id = 2）直接有 2 名下属（`Charlie`、`David`），平均年龄为 (34+40)/2 = 37。  
- `Bob`（employee_id = 3）直接有 1 名下属（`Eva`），平均年龄为 29。

---

**约束条件**  
- 无

---

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

我们手里只有一张 `Employees` 表，里面每一行记录了：

| employee_id | name | reports_to | age |
|-------------|------|------------|-----|

- `employee_id` 是唯一标识（相当于每个人的身份证号）。  
- `reports_to` 表示这名员工直接向哪位员工汇报。如果是 `null`，说明他没有直接上级（可能是公司最高层）。  

**目标**：找出所有**经理**（即至少有一个下属的员工），并输出：

1. 经理的 `employee_id`  
2. 经理的 `name`  
3. 直接下属的数量  
4. 直接下属的平均年龄（四舍五入到最近的整数）  

最直接的做法是：

1. **遍历整张表**，把每个人的 `reports_to` 记下来。可以把 `reports_to` 当作 **字典的键**，把它对应的下属（`employee_id`）放进 **列表**，这一步相当于“把每个人的名字写进字典，key 是经理的 id，value 是所有直接汇报给他的员工”。  
2. 再遍历一次 **字典**，把每个经理的下属列表长度算出来（即直接下属数量），把下属的年龄加起来再除以人数得到平均值，最后用 `round()` 四舍五入。  

这里把 **字典** 类比成 **查字典**：  
- **key** = 经理的 id（像单词）  
- **value** = 这位经理所有直接下属的年龄列表（像页码上对应的解释）  

这样我们就能得到每位经理需要的统计信息。  

**为什么这个方法一定正确？**  
- 每一行只会把自己的 `reports_to` 加到对应经理的列表里，**不会漏**也**不会重复**（因为每个人只会有唯一的直接上级）。  
- 统计下属数量和平均年龄时，直接使用已经收集好的列表，确保统计的是**直接**下属而不是间接下属。  

#### 代码（Python）

> 下面的实现使用标准库 `collections.defaultdict`，可以直接在本地运行。  
> 为了模拟 LeetCode 的数据库表，这里把数据放进了一个列表 `employees`，每条记录是一个字典。

```python
from collections import defaultdict
from typing import List, Dict, Any

# ------------------- 模拟输入 -------------------
# 每条记录对应表中的一行
employees: List[Dict[str, Any]] = [
    {"employee_id": 9, "name": "Hercy",   "reports_to": None, "age": 43},
    {"employee_id": 6, "name": "Alice",   "reports_to": 9,    "age": 41},
    {"employee_id": 4, "name": "Bob",     "reports_to": 9,    "age": 36},
    {"employee_id": 2, "name": "Winston", "reports_to": None, "age": 37},
    # 这里可以继续添加更多测试数据……
]

# ------------------- 暴力实现 -------------------
def managers_bruteforce(employees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    返回每位经理的统计信息（暴力解）。
    结果的每个元素是一个字典，键分别为:
        employee_id, name, reports_count, average_age
    """
    # 1. 建立 manager_id -> 直接下属年龄列表 的映射
    reports_map: defaultdict[int, List[int]] = defaultdict(list)
    # 同时保存 manager_id -> name 的对应关系（后面需要打印名字）
    id_to_name: Dict[int, str] = {}

    for emp in employees:
        emp_id = emp["employee_id"]
        manager_id = emp["reports_to"]
        age = emp["age"]
        name = emp["name"]

        # 记录每个人的名字，方便后面查找
        id_to_name[emp_id] = name

        # 如果这条记录有上级，就把自己的年龄放进上级的列表
        if manager_id is not None:
            reports_map[manager_id].append(age)

    # 2. 依据映射生成结果
    result: List[Dict[str, Any]] = []
    for manager_id, ages in reports_map.items():
        # 只要有下属，就算是经理
        reports_count = len(ages)                # 直接下属数量
        average_age = round(sum(ages) / reports_count)  # 四舍五入的平均年龄
        result.append({
            "employee_id": manager_id,
            "name": id_to_name[manager_id],
            "reports_count": reports_count,
            "average_age": average_age,
        })

    # 3. 按 employee_id 升序返回（LeetCode 要求的顺序）
    result.sort(key=lambda x: x["employee_id"])
    return result

# ------------------- 运行示例 -------------------
if __name__ == "__main__":
    out = managers_bruteforce(employees)
    for row in out:
        print(row)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 第一次遍历把每个人的信息放进字典，需要 `n` 次操作。  
  - 第二次遍历只遍历了有下属的经理，最多也是 `n` 次（因为每个人最多只能是别人的下属一次）。  
  - 所以整体是线性时间，`O(n)`。这里的 `n` 就是表中员工的行数，意思是“随着员工数量增长，程序的运行时间几乎成正比”。  

- **空间复杂度**：`O(m)`  
  - `reports_map` 最多存 `m` 条记录，`m` 为 **经理的数量**（每位经理对应一个列表）。最坏情况下每个人都是别人的下属，即 `m ≈ n`，所以空间复杂度也是线性 `O(n)`。  
  - 这里的空间指的是程序在运行期间占用的额外内存，而不是原始输入表本身。  

---  

### 2. 最优解  

#### 思路  

从暴力解来看，**瓶颈**其实并不在时间上（已经是 `O(n)`），而是在 **代码的可读性与一次遍历的完整性**。  
我们可以把「收集下属」和「统计结果」这两步合并到 **同一次遍历** 中完成，思路如下：

1. **一次遍历**：  
   - 用 `defaultdict` 同时记录两件事：  
     - `cnt[manager_id]`：直接下属的计数  
     - `sum_age[manager_id]`：直接下属年龄的累计和  
   - 同时维护 `id_to_name`（经理 id → 姓名），因为我们仍需要输出名字。  

2. **遍历结束后**：  
   - 只需要遍历 `cnt`（或 `sum_age`）一次，直接算出平均年龄 `round(sum_age / cnt)`，并组装结果。  

这样做的好处：

- **只遍历一次表**，代码更紧凑，常数因子更小。  
- 不需要存放每位经理所有下属的完整年龄列表（节约了一点内存），只保留 **计数** 和 **年龄总和** 两个数字即可。  

**核心数据结构**：  
- `defaultdict(int)`（相当于「自动把不存在的键初始化为 0」的字典），用来做计数和求和。可以把它想象成 **自动补零的记事本**，每写一次就自动加一或加上年龄。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Dict, Any

# ------------------- 模拟输入（同上） -------------------
employees: List[Dict[str, Any]] = [
    {"employee_id": 9, "name": "Hercy",   "reports_to": None, "age": 43},
    {"employee_id": 6, "name": "Alice",   "reports_to": 9,    "age": 41},
    {"employee_id": 4, "name": "Bob",     "reports_to": 9,    "age": 36},
    {"employee_id": 2, "name": "Winston", "reports_to": None, "age": 37},
    # 可自行添加更多数据进行测试
]

# ------------------- 最优实现 -------------------
def managers_optimal(employees: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    O(n) 时间、O(m) 空间（仅保存计数和年龄和），一次遍历完成统计。
    """
    # 统计每位经理的直接下属数量和年龄总和
    cnt: defaultdict[int, int] = defaultdict(int)      # manager_id -> 直接下属数
    sum_age: defaultdict[int, int] = defaultdict(int)  # manager_id -> 年龄累计和
    id_to_name: Dict[int, str] = {}                     # manager_id -> 姓名

    for emp in employees:
        emp_id = emp["employee_id"]
        manager_id = emp["reports_to"]
        age = emp["age"]
        name = emp["name"]

        # 记录每个人的姓名，后面需要用到（即使他是普通员工也要保存，以防成为经理）
        id_to_name[emp_id] = name

        # 如果有直接上级，则更新该上级的计数和年龄和
        if manager_id is not None:
            cnt[manager_id] += 1
            sum_age[manager_id] += age

    # 组装结果，只保留有下属的 manager（cnt 非 0 即为经理）
    result: List[Dict[str, Any]] = []
    for manager_id, report_cnt in cnt.items():
        avg_age = round(sum_age[manager_id] / report_cnt)  # 四舍五入
        result.append({
            "employee_id": manager_id,
            "name": id_to_name[manager_id],
            "reports_count": report_cnt,
            "average_age": avg_age,
        })

    # 按 employee_id 升序返回
    result.sort(key=lambda x: x["employee_id"])
    return result

# ------------------- 运行示例 -------------------
if __name__ == "__main__":
    out = managers_optimal(employees)
    for row in out:
        print(row)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次 `employees` 表，进行常数时间的字典操作（计数 + 累加），随后遍历 `cnt`（经理数量最多 `n`），整体仍是线性。  
  - 与暴力解的时间复杂度相同，但**常数因子更小**，实际运行更快。  

- **空间复杂度**：`O(m)`  
  - 只保存两个整数（计数、年龄和）以及名字映射，**不再保存每位经理所有下属的年龄列表**，因此相比暴力解省了一点内存。  
  - `m` 为经理数量，最坏情况下 `m ≤ n`，仍是线性空间。  

---

## 心得  

- **核心技巧**：**分组聚合**（group‑by）——把同一个经理的所有直接下属聚合到一起，再求计数和平均值。  
- **适用的题型**（类似思路）  
  1. “Department Salary Statistics”：统计每个部门的员工人数、总薪资、平均薪资。  
  2. “Product Sales Summary”：统计每个商品的销量、总收入、平均单价。  
- **一句话总结解题钥匙**：**先把下属归到对应的经理，再在每个组里做计数和求和**。  

---

## 反思  

- **拿到题目第一反应**：先把 `reports_to` 当作外键，找出所有出现过的 `reports_to` 值，它们就是经理的候选集合。  
- **最容易踩的坑**  
  1. **遗漏没有下属的员工**：题目只要求输出**有下属**的经理，别把所有 `reports_to` 为 `null` 的人也算进去。  
  2. **平均年龄的四舍五入**：直接使用整数除法会丢失小数，需要先转成浮点数再 `round()`。  
  3. **空下属列表**：如果某位经理的下属列表为空（理论上不该出现），除以 0 会报错，需要确保只对计数 > 0 的经理进行平均值计算。  
- **下次遇到同类题**：第一步想到“**把上级 id 作为键，建立聚合统计（计数、求和）**”，然后再在聚合结果上计算所需的衍生指标（平均值、最大/最小等）。这样思路清晰、实现也简洁。