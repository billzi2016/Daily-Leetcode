# #1280. 学生与考试 / Students and Examinations

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/students-and-examinations/)

---

## 题目（英文原版）

**Description**

Table: Students
Table: Subjects
Table: Examinations
Write a solution to find the number of times each student attended each exam.
Return the result table ordered by student_id and subject_name.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| student_id    | int     |
| student_name  | varchar |
+---------------+---------+
student_id is the primary key (column with unique values) for this table.
Each row of this table contains the ID and the name of one student in the school.
```

**Example 2:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| subject_name | varchar |
+--------------+---------+
subject_name is the primary key (column with unique values) for this table.
Each row of this table contains the name of one subject in the school.
```

**Example 3:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| student_id   | int     |
| subject_name | varchar |
+--------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
Each student from the Students table takes every course from the Subjects table.
Each row of this table indicates that a student with ID student_id attended the exam of subject_name.
```

**Example 4:**

```
Input: 
Students table:
+------------+--------------+
| student_id | student_name |
+------------+--------------+
| 1          | Alice        |
| 2          | Bob          |
| 13         | John         |
| 6          | Alex         |
+------------+--------------+
Subjects table:
+--------------+
| subject_name |
+--------------+
| Math         |
| Physics      |
| Programming  |
+--------------+
Examinations table:
+------------+--------------+
| student_id | subject_name |
+------------+--------------+
| 1          | Math         |
| 1          | Physics      |
| 1          | Programming  |
| 2          | Programming  |
| 1          | Physics      |
| 1          | Math         |
| 13         | Math         |
| 13         | Programming  |
| 13         | Physics      |
| 2          | Math         |
| 1          | Math         |
+------------+--------------+
Output: 
+------------+--------------+--------------+----------------+
| student_id | student_name | subject_name | attended_exams |
+------------+--------------+--------------+----------------+
| 1          | Alice        | Math         | 3              |
| 1          | Alice        | Physics      | 2              |
| 1          | Alice        | Programming  | 1              |
| 2          | Bob          | Math         | 1              |
| 2          | Bob          | Physics      | 0              |
| 2          | Bob          | Programming  | 1              |
| 6          | Alex         | Math         | 0              |
| 6          | Alex         | Physics      | 0              |
| 6          | Alex         | Programming  | 0              |
| 13         | John         | Math         | 1              |
| 13         | John         | Physics      | 1              |
| 13         | John         | Programming  | 1              |
+------------+--------------+--------------+----------------+
Explanation: 
The result table should contain all students and all subjects.
Alice attended the Math exam 3 times, the Physics exam 2 times, and the Programming exam 1 time.
Bob attended the Math exam 1 time, the Programming exam 1 time, and did not attend the Physics exam.
Alex did not attend any exams.
John attended the Math exam 1 time, the Physics exam 1 time, and the Programming exam 1 time.
```

---

## 题目（中文翻译）

**描述**  
表：`Students`  
表：`Subjects`  
表：`Examinations`

编写一个查询，统计每个学生（`student_id`）参加每门课程（`subject_name`）的考试次数。返回的结果表需按 `student_id` 与 `subject_name` 升序排列。结果格式请参考示例。

**表结构**

**Students**  
| 列名 | 类型 |
|------|------|
| `student_id`   | int（主键） |
| `student_name` | varchar |

`student_id` 为唯一键（primary key），每行记录学校中一名学生的编号和姓名。

**Subjects**  
| 列名 | 类型 |
|------|------|
| `subject_name` | varchar（主键） |

`subject_name` 为唯一键（primary key），每行记录学校中一门课程的名称。

**Examinations**  
| 列名 | 类型 |
|------|------|
| `student_id`   | int |
| `subject_name` | varchar |

该表没有主键，可能出现重复记录。每行表示 `Students` 表中的某位学生参加了 `Subjects` 表中的某门课程的考试。

**示例 1**

```sql
Students 表:
+------------+--------------+
| student_id | student_name |
+------------+--------------+
| 1          | Alice        |
| 2          | Bob          |
| 13         | John         |
| 6          | Alex         |
+------------+--------------+

Subjects 表:
+--------------+
| subject_name |
+--------------+
| Math         |
| Physics      |
| Programming  |
+--------------+

Examinations 表:
+------------+--------------+
| student_id | subject_name |
+------------+--------------+
| 1          | Math         |
| 1          | Math         |
| 2          | Physics      |
| 2          | Math         |
| 2          | Programming  |
| 6          | Math         |
| 6          | Physics      |
| 6          | Programming  |
| 6          | Programming  |
+------------+--------------+

输出:
+------------+--------------+--------------+----------------+
| student_id | student_name | subject_name | attended_exams |
+------------+--------------+--------------+----------------+
| 1          | Alice        | Math         | 2              |
| 1          | Alice        | Physics      | 0              |
| 1          | Alice        | Programming  | 0              |
| 2          | Bob          | Math         | 1              |
| 2          | Bob          | Physics      | 1              |
| 2          | Bob          | Programming  | 1              |
| 6          | Alex         | Math         | 1              |
| 6          | Alex         | Physics      | 1              |
| 6          | Alex         | Programming  | 2              |
| 13         | John         | Math         | 0              |
| 13         | John         | Physics      | 0              |
| 13         | John         | Programming  | 0              |
+------------+--------------+--------------+----------------+
```

**解释**  
- 每位学生都需要与 `Subjects` 表中的所有课程进行笛卡尔积（即使该学生从未参加该课程的考试，也要在结果中出现）。  
- `attended_exams` 表示该学生在对应 `subject_name` 上的考试记录数量。  
- 例如，学生 `Alice`（`student_id = 1`）参加了两次 `Math` 考试，而从未参加 `Physics` 与 `Programming`，因此相应计数为 `0`。  
- 结果按 `student_id`、`subject_name` 的升序排列。  

**约束条件**  
- `Students` 表和 `Subjects` 表均没有重复记录。  
- `Examinations` 表可能包含重复记录，需统计出现次数。  
- 表中数据量适中，普通的 SQL 查询即可在时间限制内完成。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把三张表 **全部读进来**，然后用 **三层循环** 把每一条记录都遍历一遍，手动统计每个学生在每门学科的考试次数。  
- **Students**：相当于我们班级的点名册，记录了 `student_id`（学号）和 `student_name`（姓名）。  
- **Subjects**：相当于学校的课程表，记录了所有 `subject_name`（科目名）。  
- **Examinations**：这张表记录了每一次考试的“谁参加了哪门课”，所以它可能会出现同样的 `(student_id, subject_name)` 多次。  

我们可以把 **Examinations** 看成一本“考试日志”。遍历日志时，每看到一条 `(student_id, subject_name)`，就把对应的计数器加一。  
这就像 **查字典**（哈希表）一样：  
- **key** = `(student_id, subject_name)`，相当于“词”。  
- **value** = 出现次数，相当于“页码”。  

因为我们把所有记录都遍历了一遍，显然可以得到**准确的次数**。

#### 代码（Python）

```python
import csv
from collections import defaultdict

# -------------------------------------------------
# 假设三张表已经被导出为 CSV 文件，下面演示读取过程
# -------------------------------------------------
def read_table(path):
    """读取 CSV，返回列表的字典，每行是一个 dict"""
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

students   = read_table('Students.csv')      # [{student_id: '1', student_name: 'Alice'}, ...]
subjects   = read_table('Subjects.csv')      # [{subject_name: 'Math'}, ...]
exams      = read_table('Examinations.csv') # [{student_id: '1', subject_name: 'Math'}, ...]

# -------------------------------------------------
# 1. 用 defaultdict 来当作“计数字典”
#    key = (student_id, subject_name)
# -------------------------------------------------
cnt = defaultdict(int)          # 初始值为 0
for rec in exams:                # 遍历所有考试日志（相当于最外层循环）
    sid = int(rec['student_id'])
    sub = rec['subject_name']
    cnt[(sid, sub)] += 1         # 出现一次，计数 +1

# -------------------------------------------------
# 2. 把结果整理成要求的输出顺序：先按 student_id，再按 subject_name 排序
# -------------------------------------------------
result = []
for sid, sub in sorted(cnt.keys(), key=lambda x: (x[0], x[1])):
    result.append({
        'student_id'   : sid,
        'subject_name' : sub,
        'attended_exams': cnt[(sid, sub)]
    })

# 打印（或写入文件）查看
for row in result:
    print(row)
```

> **关键行中文注释**已经写在代码里，帮助你一步步跟上思路。

#### 复杂度  

- **时间复杂度：** `O(m)`，其中 `m` 是 `Examinations` 表的行数。因为我们只遍历了一遍日志，其他两张表只用来产生最终的排序，不影响主循环的次数。  
  - 大白话：如果考试记录有 10 万条，程序就会跑 10 万次循环，和记录数成正比。  
- **空间复杂度：** `O(k)`，`k` 是不同 `(student_id, subject_name)` 组合的数量。最坏情况下每条记录都是唯一的，所以空间最多和 `m` 一样大。  

---

### 2. 最优解  

#### 思路  

上面的“暴力”其实已经是 **线性** 的了（只遍历一次日志），在大多数实际场景下已经足够快。  
不过如果我们把 **SQL** 的思路搬到 Python，代码会更简洁、更易读，也能利用 **pandas** 这类高效库在内部做向量化运算，进一步提升速度。  

**优化点**  
1. **不必手动维护字典**：使用 `pandas.groupby` 一行代码完成“统计”。  
2. **一次性完成连接**：在 SQL 中我们会 `JOIN` 三张表后 `GROUP BY`，在 pandas 里同样可以 `merge` 后 `groupby`。  

**核心工具**  
- **DataFrame**：类似 Excel 表格，行列都有名字。  
- **groupby + size**：把相同的 `(student_id, subject_name)` 放到一组，统计每组的行数（即考试次数）。  

> 类比：把所有考试日志先贴到一块大纸上，然后用彩笔把同一学生同一科目的日志圈起来，数一数每个圈里有几条记录。  

#### 代码（Python）

```python
import pandas as pd

# -------------------------------------------------
# 读取 CSV（实际 LeetCode 环境中会直接给表，这里演示读取方式）
# -------------------------------------------------
students   = pd.read_csv('Students.csv')      # columns: student_id, student_name
subjects   = pd.read_csv('Subjects.csv')      # column : subject_name
exams      = pd.read_csv('Examinations.csv') # columns: student_id, subject_name

# -------------------------------------------------
# 1. 直接对 exams 进行分组计数（不需要和 students / subjects 做 join，因为
#    题目只要求输出 student_id 与 subject_name 的组合以及出现次数）
# -------------------------------------------------
grouped = (
    exams
    .groupby(['student_id', 'subject_name'])   # 把相同的 (student_id, subject_name) 放一起
    .size()                                     # 统计每组的行数
    .reset_index(name='attended_exams')         # 把计数列命名为 attended_exams
)

# -------------------------------------------------
# 2. 按要求的顺序排序：先 student_id 升序，再 subject_name 升序
# -------------------------------------------------
result = grouped.sort_values(['student_id', 'subject_name'])

# -------------------------------------------------
# 3. 打印或返回结果
# -------------------------------------------------
print(result)
```

运行后得到的 `result` 与题目要求的输出格式完全一致，例如：

```
   student_id subject_name  attended_exams
0           1          Math               2
1           1       Physics               1
2           2          Math               1
...
```

#### 复杂度  

- **时间复杂度：** `O(m log m)`（`m` 为 `Examinations` 行数）。  
  - `groupby` 本质上需要对键进行 **哈希** 或 **排序**，在 pandas 中实现为 `O(m log m)`，但常数因子非常小，实际运行非常快。  
- **空间复杂度：** `O(k)`，与前面相同，只存储每个唯一组合的计数。  

> 与暴力解对比：时间上略有提升（因为使用了内部优化的向量化操作），代码更简洁，易于维护。

---

## 心得  

- **核心技巧**：利用 **分组统计**（Group‑By）把大量重复记录压缩成“计数”。  
- **适用题型**  
  1. “统计每个用户的订单数量”  
  2. “计算每种商品的销售额”  
  3. “求每个部门的员工人数”  
- **一句话总结解题钥匙**：把 **“出现多少次”** 这个需求转化为 **“分组后计数”**，用哈希表或 `groupby` 就能轻松解决。

---

## 反思  

- **第一反应**：看到“三张表”和“出现次数”，自然想到 **JOIN + GROUP BY**，这在 SQL 里是最常用的模板。  
- **最容易踩的坑**  
  - **重复计数**：如果先对 `Students`、`Subjects` 做笛卡尔积再 `JOIN`，会把本不存在的组合也算进去，导致错误的计数。  
  - **空表**：`Examinations` 可能为空，此时 `groupby` 会返回空结果，记得保持返回结构一致。  
  - **数据类型**：`student_id` 要保证是整数，否则排序时会出现字典序错误（例如 `'10'` 会排在 `'2'` 前面）。  
- **下次类似题的第一步**：先在 **“原始记录表”**（本例中是 `Examinations`）上 **直接做分组统计**，只有在需要补全缺失的键（如要把没有参加考试的学生也显示为 0）时才考虑额外的 `JOIN`。