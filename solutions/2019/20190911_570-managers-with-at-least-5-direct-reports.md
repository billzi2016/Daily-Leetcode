# #570. 直接下属不少于5人的经理 / Managers with at Least 5 Direct Reports

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/managers-with-at-least-5-direct-reports/)

---

## 题目（英文原版）

**Description**

Table: Employee
Write a solution to find managers with at least five direct reports.
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
| department  | varchar |
| managerId   | int     |
+-------------+---------+
id is the primary key (column with unique values) for this table.
Each row of this table indicates the name of an employee, their department, and the id of their manager.
If managerId is null, then the employee does not have a manager.
No employee will be the manager of themself.
```

**Example 2:**

```
Input: 
Employee table:
+-----+-------+------------+-----------+
| id  | name  | department | managerId |
+-----+-------+------------+-----------+
| 101 | John  | A          | null      |
| 102 | Dan   | A          | 101       |
| 103 | James | A          | 101       |
| 104 | Amy   | A          | 101       |
| 105 | Anne  | A          | 101       |
| 106 | Ron   | B          | 101       |
+-----+-------+------------+-----------+
Output: 
+------+
| name |
+------+
| John |
+------+
```

---

## 题目（中文翻译）

表：Employee  

编写一个查询，找出拥有至少 **5** 名直接下属（direct reports）的经理（manager）。返回结果表，顺序任意。结果格式参见下例。

**示例 1**  

| Column Name | Type    |
|-------------|---------|
| id          | int     |
| name        | varchar |
| department  | varchar |
| managerId   | int     |

- `id` 是此表的主键（primary key），即唯一标识每一行记录的列。  
- 每行记录表示员工的姓名、所属部门以及其经理的 `id`。  
- 若 `managerId` 为 `null`，则该员工没有上级。  
- 不会出现员工自己是自己的经理的情况。

**示例 2**  

**输入**  
Employee 表：

| id  | name  | department | managerId |
|-----|-------|------------|-----------|
| 101 | John  | A          | null      |
| 102 | Dan   | A          | 101       |
| 103 | James | A          | 101       |
| 104 | Amy   | A          | 101       |
| 105 | Anne  | A          | 101       |
| 106 | Ron   | B          | 101       |

**输出**

| name |
|------|
| John |

约束条件：  
无

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**对每一位员工都去遍历整个表，统计有多少人把他当成 `managerId`**。  
这相当于在现实生活中让每个人都去检查“我到底有多少下属”，就像在一个班级里让每个同学都去数一遍全班同学的座位号，看有多少人坐在他前面——显然非常费时。

- **使用的数据结构**：  
  - `list`（存放所有员工记录），每条记录可以是 `dict` 或自定义 `Employee` 类。  
  - 只需要遍历，不需要额外的数据结构。  

- **为什么正确**：  
  - 对每个员工我们都完整地检查了一遍所有记录，确保没有漏掉任何直接下属。只要计数大于等于 5，就把该员工的名字加入答案。  

- **时间/空间复杂度**：  
  - **时间**：外层遍历 `n` 次，内层遍历同样 `n` 次，总共大约 `n × n = n²` 次比较。  
    - 大白话：如果公司有 1000 个人，这种方法要检查 1,000,000 次；人数翻倍，检查次数会变成 4 倍。  
  - **空间**：只用了常数级别的额外变量（计数器、结果列表），所以是 **O(1)**。

#### 代码（Python）

```python
# 假设 employee_table 是一个列表，每个元素是形如
# {"id": 101, "name": "John", "department": "A", "managerId": None}
# 的字典

def managers_brute_force(employee_table):
    result = []                     # 用来保存满足条件的经理名字
    for emp in employee_table:      # 外层遍历每一位员工（可能是经理）
        manager_id = emp["id"]
        count = 0                   # 统计直接下属的数量

        # 内层遍历整个表，找出所有 managerId == manager_id 的记录
        for other in employee_table:
            if other["managerId"] == manager_id:
                count += 1

        # 如果直接下属不少于 5 人，就把名字加入答案
        if count >= 5:
            result.append(emp["name"])

    return result
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环，每层遍历 `n` 条记录。  
- **空间复杂度**：`O(1)` —— 只用了几个计数器和结果列表（结果列表的大小最多是 `n`，不算额外空间）。

---

### 2. 最优解

#### 思路  
从暴力解可以看到 **瓶颈在于每次都要遍历整个表**。  
我们可以把 “统计每个 manager 有多少直接下属” 这件事 **一次性完成**，再根据统计结果挑选满足条件的经理。

优化步骤：

1. **一次遍历收集计数**  
   - 用一个 **哈希表（Python 的 dict）** 把 `managerId` → 直接下属数量 记录下来。  
   - 类比：这就像在课堂上让每位同学把自己的座位号写在一张纸上，然后老师一次性把所有纸收集起来，统计每个座位号出现了多少次。

2. **再一次遍历把 `id` → `name` 的映射建立起来**  
   - 这一步同样是 O(n)，但只需要保存每个员工的姓名，方便后面根据 `id` 找到经理的名字。

3. **筛选**  
   - 遍历计数表，找出计数 ≥ 5 的 `managerId`，再从 `id → name` 的映射中取出对应的姓名。

整个过程只需要 **两次线性遍历**，时间降到了 `O(n)`，空间使用了两个字典，都是 `O(n)`。

#### 代码（Python）

```python
def managers_optimized(employee_table):
    """
    返回所有直接下属数量 >= 5 的经理姓名（顺序不定）。
    """
    # 1. 统计每个 managerId 的直接下属数量
    report_cnt = {}                 # managerId -> 下属计数
    for emp in employee_table:
        mgr = emp["managerId"]
        if mgr is not None:         # 只有真正有上级的员工才计数
            report_cnt[mgr] = report_cnt.get(mgr, 0) + 1

    # 2. 建立 id -> name 的映射，方便后面查找经理姓名
    id_to_name = {emp["id"]: emp["name"] for emp in employee_table}

    # 3. 选出满足条件的经理姓名
    result = [id_to_name[mid] for mid, cnt in report_cnt.items() if cnt >= 5]

    return result
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历两遍表，`n` 为员工总数。  
  - 与暴力解相比，从 `n²` 降到了 `n`，如果员工有 10,000 人，原始解要检查 1 亿次，而最优解只检查约 20,000 次，速度提升数百倍。

- **空间复杂度**：`O(n)` —— 两个字典分别存放计数和 `id→name` 映射，最坏情况下每个员工都会占用一个键值对。

---

## 心得

- **核心技巧**：利用哈希表（字典）一次遍历完成计数，避免嵌套循环。  
- **适用的题型**  
  1. “统计出现次数”类问题，如 **找出出现超过 K 次的元素**。  
  2. “父子关系统计”类，如 **部门经理下属人数、社交网络中朋友数**。  
  3. **分组聚合**（Group By）在 SQL 中的等价实现。  
- **一句话总结**：**把“对每个人都全表扫描”改成“先全表收集信息，再一次性筛选”，就是从 O(n²) 到 O(n) 的关键**。

---

## 反思

- **第一反应**：直接想到双层循环，逐个比较，最安全但最慢。  
- **最容易踩的坑**  
  - 忘记排除 `managerId` 为 `null` 的情况，会把 `None` 也计入统计，导致错误结果。  
  - 对于同一个 `managerId` 出现多次计数时，必须使用 `dict.get(...,0)+1`，否则会覆盖之前的计数。  
- **下次遇到同类题**：第一步先思考 **“有没有办法一次遍历把所有需要的统计信息收集起来？”**，若能，用哈希表或数组完成聚合；若不能，再考虑更复杂的数据结构（如并查集、线段树等）。