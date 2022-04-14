# #1741. 统计每位员工的总在岗时间 / Find Total Time Spent by Each Employee

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-total-time-spent-by-each-employee/)

---

## 题目（英文原版）

**Description**

Table: Employees
Write a solution to calculate the total time in minutes spent by each employee on each day at the office. Note that within one day, an employee can enter and leave more than once. The time spent in the office for a single entry is out_time - in_time.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| emp_id      | int  |
| event_day   | date |
| in_time     | int  |
| out_time    | int  |
+-------------+------+
(emp_id, event_day, in_time) is the primary key (combinations of columns with unique values) of this table.
The table shows the employees' entries and exits in an office.
event_day is the day at which this event happened, in_time is the minute at which the employee entered the office, and out_time is the minute at which they left the office.
in_time and out_time are between 1 and 1440.
It is guaranteed that no two events on the same day intersect in time, and in_time < out_time.
```

**Example 2:**

```
Input: 
Employees table:
+--------+------------+---------+----------+
| emp_id | event_day  | in_time | out_time |
+--------+------------+---------+----------+
| 1      | 2020-11-28 | 4       | 32       |
| 1      | 2020-11-28 | 55      | 200      |
| 1      | 2020-12-03 | 1       | 42       |
| 2      | 2020-11-28 | 3       | 33       |
| 2      | 2020-12-09 | 47      | 74       |
+--------+------------+---------+----------+
Output: 
+------------+--------+------------+
| day        | emp_id | total_time |
+------------+--------+------------+
| 2020-11-28 | 1      | 173        |
| 2020-11-28 | 2      | 30         |
| 2020-12-03 | 1      | 41         |
| 2020-12-09 | 2      | 27         |
+------------+--------+------------+
Explanation: 
Employee 1 has three events: two on day 2020-11-28 with a total of (32 - 4) + (200 - 55) = 173, and one on day 2020-12-03 with a total of (42 - 1) = 41.
Employee 2 has two events: one on day 2020-11-28 with a total of (33 - 3) = 30, and one on day 2020-12-09 with a total of (74 - 47) = 27.
```

---

## 题目（中文翻译）

**描述**  
表（Table）`Employees`  
请编写 SQL 查询，计算每位员工在每一天的总在办公室时间（单位：分钟）。注意，同一天内同一员工可能会有多次进出记录。一次进出所花费的时间等于 `out_time - in_time`。  
返回的结果表可以按任意顺序排列，格式参考示例。

**表结构**  

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| emp_id      | int  |
| event_day   | date |
| in_time     | int  |
| out_time    | int  |
+-------------+------+
```

- `(emp_id, event_day, in_time)` 为主键（primary key），即该组合的值唯一。  
- `event_day` 表示事件发生的日期。  
- 该表记录了员工在办公室的进出时间。

**示例 1**

```
Employees table:
+--------+------------+----------+----------+
| emp_id | event_day  | in_time  | out_time |
+--------+------------+----------+----------+
| 1      | 2020-11-28 | 4        | 32       |
| 1      | 2020-11-28 | 55       | 200      |
| 1      | 2020-12-03 | 1        | 42       |
| 2      | 2020-11-28 | 3        | 33       |
| 2      | 2020-12-09 | 47       | 74       |
+--------+------------+----------+----------+
```

**输出**

```
+--------+------------+------------+
| emp_id | event_day  | total_time |
+--------+------------+------------+
| 1      | 2020-11-28 | 173        |
| 1      | 2020-12-03 | 41         |
| 2      | 2020-11-28 | 30         |
| 2      | 2020-12-09 | 27         |
+--------+------------+------------+
```

**解释**  
- 对于员工 1 在 2020‑11‑28：`(32 - 4) + (200 - 55) = 28 + 145 = 173` 分钟。  
- 对于员工 1 在 2020‑12‑03：`42 - 1 = 41` 分钟。  
- 对于员工 2 在 2020‑11‑28：`33 - 3 = 30` 分钟。  
- 对于员工 2 在 2020‑12‑09：`74 - 47 = 27` 分钟。

**约束条件**  
- 本题无额外约束。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题本质上是 **把同一个员工、同一天的多条记录累加**，每条记录的贡献是 `out_time - in_time`（离开时间减去进入时间）。  
最直接的做法就是：

1. 把表中的每一行都读取出来。  
2. 按照 `emp_id`（员工编号）和 `event_day`（日期）这两个字段分组。  
3. 对同一组内的所有记录，逐条计算 `out_time - in_time`，累加得到该员工当天的总在岗时间。

可以把 “分组” 想象成 **把相同名字的书放进同一个抽屉**，抽屉的钥匙就是 `(emp_id, event_day)`。然后把抽屉里每本书的页数（这里是 `out_time - in_time`）加起来，就是这本抽屉（这位员工这一天）的总页数（总时长）。

**为什么正确**：  
- 每条记录都只对应一次 `out_time - in_time`，没有遗漏也没有重复。  
- 同一员工同一天的所有记录都会被放进同一个抽屉并全部相加，正好符合题目“在一天内可能会进出多次”的要求。  

**复杂度分析（大白话）**：

- **时间复杂度**：我们遍历一次表（记作 `n` 行），每遍历一行就做常数次的加减和一次哈希表的查找/更新。整体是 **O(n)**，意思是“随着数据行数线性增长，耗时也线性增长”。  
- **空间复杂度**：我们需要一个哈希表（Python 的 `dict`）来保存每个 `(emp_id, event_day)` 对应的累计时长。最坏情况下，每一行的组合都是唯一的，需要保存 `n` 条记录，所以是 **O(n)** 的额外空间。

#### 代码（Python）

```python
from typing import List, Tuple
import collections

# ------------------------------------------------------------------
# 这里我们用一个函数来模拟 LeetCode 的 SQL 环境。
# 参数 employees: List[Tuple[int, str, int, int]]
#   每条记录的格式为 (emp_id, event_day, in_time, out_time)
# 返回值: List[Tuple[int, str, int]]
#   每条记录的格式为 (emp_id, event_day, total_time)
# ------------------------------------------------------------------
def total_time_brute(employees: List[Tuple[int, str, int, int]]) -> List[Tuple[int, str, int]]:
    # 用 defaultdict 自动初始化累计时长为 0
    total = collections.defaultdict(int)   # key -> (emp_id, event_day)

    # 逐行遍历表
    for emp_id, event_day, in_time, out_time in employees:
        # 计算单次进出的时长
        duration = out_time - in_time      # 这里的减法就是题目要求的 out_time - in_time
        # 把时长加到对应的 (emp_id, event_day) 上
        total[(emp_id, event_day)] += duration

    # 把哈希表转换成题目要求的列表形式
    result = [(emp, day, total[(emp, day)]) for (emp, day) in total]
    return result


# ------------------- 示例 -------------------
if __name__ == "__main__":
    # 示例数据（对应题目示例 2）
    data = [
        (1, "2020-11-28", 4, 32),
        (1, "2020-11-28", 55, 200),
        (1, "2020-12-03", 1, 42),
        (2, "2020-11-28", 3, 33),
        (2, "2020-12-09", 47, 74),
    ]

    ans = total_time_brute(data)
    for row in ans:
        print(row)
# 运行后会输出类似：
# (1, '2020-11-28', 173)
# (1, '2020-12-03', 41)
# (2, '2020-11-28', 30)
# (2, '2020-12-09', 27)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们只遍历一次所有记录，`n` 越大，耗时大约会线性增长。

- **空间复杂度**：`O(k)`（`k` 为不同 `(emp_id, event_day)` 的数量，最坏 `k = n`）  
  解释：需要额外存储每个员工每一天的累计时长，最多和输入行数一样多。

---

### 2. 最优解

#### 思路  

在本题中，**暴力解已经是线性时间**，已经达到了最优的时间下界：我们必须看完所有记录才能知道每个人每一天的总时长。因此不存在更快的算法。  
不过，我们可以把实现方式写得更「数据库友好」——把思路直接映射到 **SQL 的 `GROUP BY`**，这样在真实的面试或在线评测里只需要一条语句即可完成。

下面的 Python 实现使用 **`pandas`**（如果你熟悉数据分析库）来演示“一行代码完成分组求和”，思路仍然是“先把相同的键放进同一个抽屉，再把抽屉里的数字加起来”。`pandas` 在内部已经对分组做了高度优化，代码更简洁。

> **提示**：如果不想依赖外部库，直接使用 `defaultdict`（上面的暴力解）已经是最优的。这里展示 `pandas` 只是为了让大家看到「SQL 思路」在 Python 里的对应写法。

#### 代码（Python）

```python
import pandas as pd
from typing import List, Tuple

def total_time_opt(employees: List[Tuple[int, str, int, int]]) -> List[Tuple[int, str, int]]:
    # 把原始列表转成 DataFrame，列名对应表结构
    df = pd.DataFrame(employees, columns=["emp_id", "event_day", "in_time", "out_time"])

    # 计算每条记录的在岗时长，新增一列 duration
    df["duration"] = df["out_time"] - df["in_time"]

    # 按 emp_id、event_day 分组后求和 duration
    grouped = df.groupby(["emp_id", "event_day"], as_index=False)["duration"].sum()

    # 转换成题目要求的 List[Tuple[int, str, int]] 格式
    result = list(grouped.itertuples(index=False, name=None))
    return result


# ------------------- 示例 -------------------
if __name__ == "__main__":
    data = [
        (1, "2020-11-28", 4, 32),
        (1, "2020-11-28", 55, 200),
        (1, "2020-12-03", 1, 42),
        (2, "2020-11-28", 3, 33),
        (2, "2020-12-09", 47, 74),
    ]

    ans = total_time_opt(data)
    for row in ans:
        print(row)
# 输出同上例
```

#### 复杂度

- **时间复杂度**：`O(n)`（实际常数因 `pandas` 内部实现略有不同，但仍是线性）  
  与暴力解相比，没有本质上的提升，只是把「手动分组」的工作交给了库。

- **空间复杂度**：`O(n)`  
  需要存放原始数据以及中间的 `duration` 列和分组结果，整体仍是线性空间。

---

## 心得

- **核心技巧**：**分组求和**（Group‑By + Sum）。把相同键的多条记录聚合在一起，然后对感兴趣的列做累加。  
- **适用的题型**：  
  1. “统计每个用户每天的活跃时长”  
  2. “求每个商品每月的销售额”  
  3. “计算每位学生每门课的总分”  
- **一句话总结**：**把相同的 (员工, 日期) 放进同一个抽屉，抽屉里所有离开时间减去进入时间的和，就是答案。**

## 反思

- **第一反应**：看到 “每一天可能会进出多次”，立刻想到 “要把同一天同一个人的多条记录累加”。  
- **最容易踩的坑**：  
  - 忘记 `out_time` 与 `in_time` 的顺序导致负数（一定是 `out - in`）。  
  - 忽略日期是 `date` 类型，直接把日期当作整数处理会出错。  
  - 对于没有任何记录的员工，题目不要求输出，这点要注意不要自行补零。  
- **下次第一步**：先把“相同的键”抽出来（`emp_id` + `event_day`），确认要对哪一列做 **求和**，然后决定用 `defaultdict` 手动实现还是直接写一条 `GROUP BY` SQL。