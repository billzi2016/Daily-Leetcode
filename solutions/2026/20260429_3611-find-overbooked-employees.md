# #3611. 查找会议超负荷的员工 / Find Overbooked Employees

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-overbooked-employees/)

---

## 题目（英文原版）

**Description**

Table: employees
Table: meetings
Write a solution to find employees who are meeting-heavy - employees who spend more than 50% of their working time in meetings during any given week.
Return the result table ordered by the number of meeting-heavy weeks in descending order, then by employee name in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| employee_id   | int     |
| employee_name | varchar |
| department    | varchar |
+---------------+---------+
employee_id is the unique identifier for this table.
Each row contains information about an employee and their department.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| meeting_id    | int     |
| employee_id   | int     |
| meeting_date  | date    |
| meeting_type  | varchar |
| duration_hours| decimal |
+---------------+---------+
meeting_id is the unique identifier for this table.
Each row represents a meeting attended by an employee. meeting_type can be 'Team', 'Client', or 'Training'.
```

**Example 3:**

```
+-------------+----------------+-------------+
| employee_id | employee_name  | department  |
+-------------+----------------+-------------+
| 1           | Alice Johnson  | Engineering |
| 2           | Bob Smith      | Marketing   |
| 3           | Carol Davis    | Sales       |
| 4           | David Wilson   | Engineering |
| 5           | Emma Brown     | HR          |
+-------------+----------------+-------------+
```

**Example 4:**

```
+------------+-------------+--------------+--------------+----------------+
| meeting_id | employee_id | meeting_date | meeting_type | duration_hours |
+------------+-------------+--------------+--------------+----------------+
| 1          | 1           | 2023-06-05   | Team         | 8.0            |
| 2          | 1           | 2023-06-06   | Client       | 6.0            |
| 3          | 1           | 2023-06-07   | Training     | 7.0            |
| 4          | 1           | 2023-06-12   | Team         | 12.0           |
| 5          | 1           | 2023-06-13   | Client       | 9.0            |
| 6          | 2           | 2023-06-05   | Team         | 15.0           |
| 7          | 2           | 2023-06-06   | Client       | 8.0            |
| 8          | 2           | 2023-06-12   | Training     | 10.0           |
| 9          | 3           | 2023-06-05   | Team         | 4.0            |
| 10         | 3           | 2023-06-06   | Client       | 3.0            |
| 11         | 4           | 2023-06-05   | Team         | 25.0           |
| 12         | 4           | 2023-06-19   | Client       | 22.0           |
| 13         | 5           | 2023-06-05   | Training     | 2.0            |
+------------+-------------+--------------+--------------+----------------+
```

**Example 5:**

```
+-------------+----------------+-------------+---------------------+
| employee_id | employee_name  | department  | meeting_heavy_weeks |
+-------------+----------------+-------------+---------------------+
| 1           | Alice Johnson  | Engineering | 2                   |
| 4           | David Wilson   | Engineering | 2                   |
+-------------+----------------+-------------+---------------------+
```

---

## 题目（中文翻译）

Table: employees  
Table: meetings  

编写一个查询，找出 **会议密集的员工**——即在任意给定的一周内，员工的会议时间 **超过 50%**（> 50%）的工作时间。  

返回结果表，**先按会议密集周数（meeting-heavy weeks）降序排列**，若相同则 **按员工姓名升序排列**。结果格式参考下例。

示例：

示例 1:
```text
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| employee_id   | int     |
| employee_name | varchar |
| department    | varchar |
+---------------+---------+
```
`employee_id` 为该表的唯一标识。每行记录一名员工及其所在部门。

示例 2:
```text
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| meeting_id    | int     |
| employee_id   | int     |
| meeting_date  | date    |
| meeting_type  | varchar |
| duration_hours| decimal |
+---------------+---------+
```
`meeting_id` 为该表的唯一标识。每行记录一次员工参加的会议。`meeting_type` 可以是 `'Team'`、`'Client'` 或其他类型。

示例 3:
```text
+-------------+----------------+-------------+
| employee_id | employee_name  | department  |
+-------------+----------------+-------------+
| 1           | Alice Johnson  | Engineering |
| 2           | Bob Smith      | Marketing   |
| 3           | Carol Davis    | Sales       |
| 4           | David Wilson   | Engineering |
| 5           | Emma Brown     | HR          |
+-------------+----------------+-------------+
```

示例 4:
```text
+------------+-------------+--------------+--------------+----------------+
| meeting_id | employee_id | meeting_date | meeting_type | duration_hours |
+------------+-------------+--------------+--------------+----------------+
| 1          | 1           | 2023-06-05   | Team         | 8.0            |
| 2          | 1           | 2023-06-06   | Client       | 6.0            |
| 3          | 1           | ...          | ...          | ...            |
+------------+-------------+--------------+--------------+----------------+
```

示例 5（返回结果）:
```text
+-------------+----------------+-------------+-----------------------+
| employee_id | employee_name  | department  | meeting_heavy_weeks  |
+-------------+----------------+-------------+-----------------------+
| 1           | Alice Johnson  | Engineering | 2                     |
| 4           | David Wilson   | Engineering | 2                     |
+-------------+----------------+-------------+-----------------------+
```

约束条件：  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有数据全部展开**，逐行检查每条会议记录，把它们累加到对应员工、对应周的“会议时长”上。  
这一步可以想象成：

- **员工表**：像一本电话簿，`employee_id` 就是每个人的唯一电话号码。  
- **会议表**：像一本日记，每一行记录了某个员工在某天参加了多久的会议。  

我们把每条会议记录 “放进” 一个 **哈希表**（在 Python 中可以用 `dict`），键是 `(employee_id, week_number)`，值是该员工在该周累计的会议时长。  
哈希表就像 **查字典**：  
- **key**（键）是“词”，这里是 `(employee_id, week_number)`。  
- **value**（值）是“页码”，这里是累计的会议时长。

遍历完所有会议后，我们再遍历这个哈希表：

- 如果某个 `(employee_id, week_number)` 的累计时长 > 20（因为一周工作 40 小时，超过 50% 就是 >20 小时），说明该周是 “meeting‑heavy”。  
- 对每个员工统计满足条件的周数，即得到 `meeting_heavy_weeks`。

最后把结果按照 **meeting_heavy_weeks 降序 → employee_name 升序** 排序即可。

> 这种做法之所以 **一定正确**，是因为我们没有遗漏任何会议记录，也没有对数据进行任何近似或抽样，直接统计了所有可能的“员工‑周”。  

#### 代码（Python）

```python
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

# ------------------- 这里是“暴力”实现 -------------------
def find_meeting_heavy_employees_bruteforce(
    employees: List[Dict[str, Any]],
    meetings: List[Dict[str, Any]],
    work_hours_per_week: float = 40.0,
) -> List[Dict[str, Any]]:
    """
    暴力解：逐条累加会议时长 → 判断是否超过 50% → 统计符合条件的周数
    参数
    ----
    employees: 员工信息列表，每个元素包含 employee_id、employee_name、department
    meetings: 会议记录列表，每个元素包含 meeting_id、employee_id、meeting_date、duration_hours
    work_hours_per_week: 每周标准工作时长，默认 40 小时
    返回值
    ----
    按要求排序的结果列表，每行包含 employee_id、employee_name、department、meeting_heavy_weeks
    """

    # 1. 用 defaultdict 自动创建“0” 初始值，key = (employee_id, week_number)
    week_meeting_time = defaultdict(float)

    # 2. 遍历每条会议记录，累加到对应的 (employee_id, week_number) 上
    for m in meetings:
        emp_id = m["employee_id"]
        # 把字符串日期转成 datetime，方便取 ISO 周数
        date_obj = datetime.strptime(m["meeting_date"], "%Y-%m-%d")
        # iso_week = (year, week_number) 这里我们只关心 week_number
        week_number = date_obj.isocalendar()[1]  # 1~53
        # 累加会议时长
        week_meeting_time[(emp_id, week_number)] += float(m["duration_hours"])

    # 3. 统计每位员工“meeting‑heavy”周的数量
    heavy_week_cnt = defaultdict(int)   # key = employee_id, value = heavy weeks
    threshold = work_hours_per_week / 2  # 50% 的阈值 = 20 小时

    for (emp_id, wk), total in week_meeting_time.items():
        if total > threshold:               # 超过阈值即为 meeting‑heavy
            heavy_week_cnt[emp_id] += 1

    # 4. 把统计结果和员工信息拼装在一起
    result = []
    for emp in employees:
        emp_id = emp["employee_id"]
        cnt = heavy_week_cnt.get(emp_id, 0)   # 没有 meeting‑heavy 周则为 0
        if cnt > 0:                           # 只返回至少有一次 meeting‑heavy 的员工
            result.append({
                "employee_id": emp_id,
                "employee_name": emp["employee_name"],
                "department": emp["department"],
                "meeting_heavy_weeks": cnt,
            })

    # 5. 按 meeting_heavy_weeks 降序、employee_name 升序排序
    result.sort(key=lambda x: (-x["meeting_heavy_weeks"], x["employee_name"]))
    return result
```

#### 复杂度

- **时间复杂度**：`O(M + N)`  
  - `M` 是会议记录条数，遍历一次累计时长。  
  - `N` 是员工数量，遍历一次把统计结果拼装输出。  
  - 用大白话说，就是“会议多多少次就花多少时间”，不会出现平方级的增长（不像 `O(N²)` 那样会变得非常慢）。

- **空间复杂度**：`O(K)`  
  - `K` 为不同的 `(employee_id, week_number)` 组合数，最坏情况下每条会议都在不同的员工‑周上。  
  - 这相当于我们需要保存一张“小表”，记录每个员工每周的累计时长。  

---

### 2. 最优解

#### 思路  

暴力解已经是 **线性** 的 (`O(M+N)`) ，已经非常高效，几乎已经达到了最优。  
但我们仍可以在 **实现细节** 上进一步“精简”，让代码更易读、占用更少临时空间：

1. **一次遍历完成所有工作**  
   - 在遍历会议记录时直接把 “是否超过 50%” 的判断搬进去。  
   - 只需要保存每个员工每周的累计时长，**不需要再额外遍历哈希表**。

2. **使用 `defaultdict(set)` 记录已经算过的 meeting‑heavy 周**  
   - 当累计时长第一次超过阈值时，就把该周计入员工的 “heavy weeks” 集合。  
   - 这样避免了后续再次检查同一周是否已计数。

3. **利用 `itertools.groupby`（或 pandas）做分组**  
   - 如果数据量非常大且已经按照 `employee_id`、`meeting_date` 排序，使用 `groupby` 可以一次遍历完成聚合，进一步降低 **常数因子**。

下面给出 **最优实现**（仍然是 `O(M+N)`，但只遍历一次，空间仅为 `O(K)`，且代码更简洁）。

#### 代码（Python）

```python
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Any

def find_meeting_heavy_employees_optimal(
    employees: List[Dict[str, Any]],
    meetings: List[Dict[str, Any]],
    work_hours_per_week: float = 40.0,
) -> List[Dict[str, Any]]:
    """
    最优解：一次遍历完成累计、阈值判断和统计
    """
    threshold = work_hours_per_week / 2          # 20 小时
    # 记录每位员工每周累计时长
    week_acc = defaultdict(float)                # key = (emp_id, week_no)
    # 记录每位员工已经被算作 heavy 的周集合（避免重复计数）
    heavy_weeks = defaultdict(set)               # key = emp_id, value = set of week_no

    for m in meetings:
        emp_id = m["employee_id"]
        date_obj = datetime.strptime(m["meeting_date"], "%Y-%m-%d")
        week_no = date_obj.isocalendar()[1]

        # 累加时长
        week_key = (emp_id, week_no)
        week_acc[week_key] += float(m["duration_hours"])

        # 第一次超过阈值，就记一次 heavy week
        if week_acc[week_key] > threshold and week_no not in heavy_weeks[emp_id]:
            heavy_weeks[emp_id].add(week_no)

    # 把统计结果和员工信息拼装
    result = []
    for emp in employees:
        emp_id = emp["employee_id"]
        cnt = len(heavy_weeks.get(emp_id, []))
        if cnt:  # 只返回有 heavy week 的员工
            result.append({
                "employee_id": emp_id,
                "employee_name": emp["employee_name"],
                "department": emp["department"],
                "meeting_heavy_weeks": cnt,
            })

    # 排序：heavy weeks 降序 → name 升序
    result.sort(key=lambda x: (-x["meeting_heavy_weeks"], x["employee_name"]))
    return result
```

#### 复杂度

- **时间复杂度**：`O(M + N)`（一次遍历所有会议 + 一次遍历所有员工）  
  - 与暴力解相同，但 **只遍历一次哈希表**，常数因子更小。

- **空间复杂度**：`O(K)`（只保存每个员工‑周的累计时长以及已计数的周集合）  
  - 与暴力解相同的量级，但 `heavy_weeks` 用 `set` 直接记录已经算过的周，省去后续遍历的额外空间。

---

## 心得

- **核心技巧**：**按周聚合 + 阈值判断**。本题把“每周工作时间 40 小时”转化为 “阈值 20 小时”，只要累计超过阈值就算 `meeting‑heavy`。  
- **相似题型**  
  1. **统计每月/每季度的销售额是否超过目标**（按时间窗口聚合）  
  2. **判断用户每日活跃时长是否超过一定比例**（用户‑天聚合）  
  3. **计算每位司机每周的行驶里程是否超过上限**（司机‑周聚合）  
- **一句话总结**：把“时间窗口 + 阈值”看成“一把尺子”，只要累计值超过尺子，就算合格；把每个对象的所有窗口结果统计出来，再排序即可。

---

## 反思

- **第一反应**：把会议表直接按 `employee_id`、`meeting_date` 分组，算每周总时长，然后比较 20 小时。  
- **最容易踩的坑**  
  - **周的划分**：不同年份、跨年时要使用 ISO 周号 (`isocalendar`) 而不是直接 `date // 7`。  
  - **时长精度**：`duration_hours` 可能是小数，需要用 `float` 累加，防止整数除法误差。  
  - **员工没有会议**：要确保即使某员工在所有周都不 meeting‑heavy，也不要误把 `0` 当作有效记录返回。  
- **下次类似题**：**先确定聚合维度（周、月、天） → 计算累计 → 与阈值比较 → 统计符合条件的次数**，这一步骤几乎可以直接搬套。