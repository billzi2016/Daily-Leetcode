# #3421. 找出成绩提升的学生 / Find Students Who Improved

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-students-who-improved/)

---

## 题目（英文原版）

**Description**

Table: Scores
Write a solution to find the students who have shown improvement. A student is considered to have shown improvement if they meet both of these conditions:
Return the result table ordered by student_id, subject in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| student_id  | int     |
| subject     | varchar |
| score       | int     |
| exam_date   | varchar |
+-------------+---------+
(student_id, subject, exam_date) is the primary key for this table.
Each row contains information about a student's score in a specific subject on a particular exam date. score is between 0 and 100 (inclusive).
```

**Example 2:**

```
+------------+----------+-------+------------+
| student_id | subject  | score | exam_date  |
+------------+----------+-------+------------+
| 101        | Math     | 70    | 2023-01-15 |
| 101        | Math     | 85    | 2023-02-15 |
| 101        | Physics  | 65    | 2023-01-15 |
| 101        | Physics  | 60    | 2023-02-15 |
| 102        | Math     | 80    | 2023-01-15 |
| 102        | Math     | 85    | 2023-02-15 |
| 103        | Math     | 90    | 2023-01-15 |
| 104        | Physics  | 75    | 2023-01-15 |
| 104        | Physics  | 85    | 2023-02-15 |
+------------+----------+-------+------------+
```

**Example 3:**

```
+------------+----------+-------------+--------------+
| student_id | subject  | first_score | latest_score |
+------------+----------+-------------+--------------+
| 101        | Math     | 70          | 85           |
| 102        | Math     | 80          | 85           |
| 104        | Physics  | 75          | 85           |
+------------+----------+-------------+--------------+
```

---

## 题目（中文翻译）

**表 (Table)：Scores**

编写 SQL 查询，找出成绩有提升的学生。若学生满足以下两个条件，则认为其成绩有提升：

1. 对同一科目（subject），存在多次考试记录（exam_date）。
2. 同一科目中，后一次考试的分数（score）大于第一次考试的分数。

返回的结果表需按 `student_id`、`subject` 升序排列。结果格式参见示例。

**示例 1：**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| student_id  | int     |
| subject     | varchar |
| score       | int     |
| exam_date   | varchar |
+-------------+---------+
(student_id, subject, exam_date) 是该表的主键 (primary key)。
每行记录了学生在某科目某次考试的分数，score 的取值范围为 0~100。
...
```

**示例 2：**

```
+------------+----------+-------+------------+
| student_id | subject  | score | exam_date  |
+------------+----------+-------+------------+
| 101        | Math     | 70    | 2023-01-15 |
| 101        | Math     | 85    | 2023-02-15 |
| 101        | Physics  | 65    | 2023-01-15 |
| 101        | Physics  | 60    | 2023-02-15 |
| 102        | Math     | 80    | 2023-01-15 |
| 102        | Math     
...
```

**示例 3（查询结果）：**

```
+------------+----------+-------------+--------------+
| student_id | subject  | first_score | latest_score |
+------------+----------+-------------+--------------+
| 101        | Math     | 70          | 85           |
| 102        | Math     | 80          | 85           |
| 104        | Physics  | 75          | 85           |
+------------+----------+-------------+--------------+
```

**约束条件：**

- 无。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 把表 `Scores` 中的所有记录全部拿出来，遍历每一行。  
2. 对每一条记录，找出 **同一个学生、同一门学科** 的 **所有** 考试日期对应的分数。  
3. 取其中最早（`exam_date` 最小）的分数 `first_score`，以及最近（`exam_date` 最大）的分数 `latest_score`。  
4. 若 `latest_score > first_score`，说明这位学生在这门课上有提升，就把 `(student_id, subject, first_score, latest_score)` 加入答案。

> **类比**：把所有记录想象成一本学生成绩簿。我们要为每本子簿（同一个学生‑同一门课）翻遍所有页（所有考试），找出第一页的成绩和最后一页的成绩，然后比较大小。  
> 这里用到的“字典”相当于 **哈希表**，它就像一本“查字典”，`key` 是 `(student_id, subject)`，`value` 是该学生‑该科目的所有成绩列表。通过 `key` 我们可以快速定位到对应的成绩集合。

**为什么正确**  
- 我们遍历了 **所有** 记录，保证不会漏掉任何学生或科目。  
- 对每个学生‑科目组合，分别取最早和最晚的成绩，正是题目要求的“first_score”和“latest_score”。  
- 最后只保留 `latest_score > first_score` 的组合，完全符合“有提升”的定义。

#### 代码（Python）

```python
from typing import List, Tuple
from collections import defaultdict

# ---------- 输入 ----------
# 每条记录用 (student_id, subject, score, exam_date) 表示
# exam_date 用字符串 'YYYY-MM-DD'，在比较时直接按字典序即可
scores: List[Tuple[int, str, int, str]] = [
    (101, "Math",    70, "2023-01-15"),
    (101, "Math",    85, "2023-02-15"),
    (101, "Physics", 65, "2023-01-15"),
    (101, "Physics", 60, "2023-02-15"),
    (102, "Math",    80, "2023-01-15"),
    (102, "Math",    85, "2023-02-15"),
    (104, "Physics", 75, "2023-01-10"),
    (104, "Physics", 85, "2023-02-20"),
    # … 这里可以继续添加更多测试数据
]

def brute_force(scores: List[Tuple[int, str, int, str]]) -> List[Tuple[int, str, int, int]]:
    """
    暴力解法：逐个学生‑科目找出最早和最晚的成绩，再比较。
    返回值的每一项为 (student_id, subject, first_score, latest_score)。
    """
    # 1. 用哈希表把同一学生‑科目的所有记录收集起来
    #    key -> (student_id, subject)
    #    value -> [(score, exam_date), ...]
    groups = defaultdict(list)
    for stu, sub, sc, date in scores:
        groups[(stu, sub)].append((sc, date))

    result = []
    # 2. 对每个学生‑科目，遍历它的所有成绩，找出最早/最晚的分数
    for (stu, sub), records in groups.items():
        # 初始化为第一个记录的值，后面再逐个比较
        first_score, latest_score = records[0][0], records[0][0]
        first_date, latest_date = records[0][1], records[0][1]

        for sc, date in records:
            # 找最早的日期对应的分数
            if date < first_date:
                first_date = date
                first_score = sc
            # 找最晚的日期对应的分数
            if date > latest_date:
                latest_date = date
                latest_score = sc

        # 3. 只保留提升的情况
        if latest_score > first_score:
            result.append((stu, sub, first_score, latest_score))

    # 4. 按题目要求排序：先 student_id 再 subject（均升序）
    result.sort(key=lambda x: (x[0], x[1]))
    return result

# ---------- 运行 ----------
for row in brute_force(scores):
    print(row)
```

**关键注释**  
- `defaultdict(list)`：相当于“查字典”，`key` 是学生‑科目，`value` 是该组合的所有成绩。  
- `date < first_date` 与 `date > latest_date`：因为日期是 `YYYY-MM-DD` 形式的字符串，直接比较字典序就能得到时间前后关系。  
- `result.sort(...)`：把最终答案按 **学生编号 → 科目** 的顺序排列，符合输出要求。

#### 复杂度

- **时间复杂度**：`O(N + G·M)`，其中 `N` 为表中记录总数，`G` 为不同的学生‑科目组合数，`M` 为每个组合的记录数。最坏情况下 `G≈N`、`M≈1`，所以整体仍是 `O(N)`。  
  > 大白话：我们只遍历了一遍原始数据，再对每个学生‑科目遍历它们自己的小集合，整个过程的工作量和记录的总数是同一个量级的。

- **空间复杂度**：`O(N)`，因为需要把所有记录按学生‑科目分组存下来（哈希表）。  
  > 大白话：相当于我们把成绩簿全部复制了一遍，放进了一个“字典”里，所占的空间和原始数据差不多。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们需要为每个学生‑科目单独遍历一次它的所有记录来找最早/最晚分数。其实如果我们在遍历原始表时 **就把记录按时间顺序排好**，那么只需要一次线性扫描就能得到答案——不必再对每个组合做二次遍历。

**优化步骤**  

1. **一次排序**  
   - 按 `(student_id, subject, exam_date)` 进行升序排序。  
   - 排好序后，同一个学生‑科目的记录会 **紧挨在一起**，且 **最早的记录在最前，最新的记录在最后**。  
   - 类比：把成绩簿先按“学生 → 科目 → 日期”排好顺序，就像把所有同一本子簿的页面排成一本完整的书。

2. **一次线性扫描**  
   - 只要遍历一次排好序的列表，维护当前正在处理的 `(student_id, subject)`。  
   - 当遇到新组合时，把上一个组合的 **首分**（第一次出现的 `score`）和 **末分**（上一次出现的 `score`）进行比较，决定是否加入答案。  
   - 这样每条记录只会被看一次，时间上是 `O(N log N)`（排序）+ `O(N)`（扫描）≈ `O(N log N)`。

3. **输出排序**  
   - 因为我们已经是按 `student_id → subject → exam_date` 排好序的，直接把符合条件的记录按出现顺序加入答案即可，无需再次排序。

**核心技巧**：**排序 + 一次遍历**（也叫 “扫描合并”）。排序把同类数据集中，遍历把每类数据的“首尾”信息一次性抽取出来。

#### 代码（Python）

```python
from typing import List, Tuple

def optimal(scores: List[Tuple[int, str, int, str]]) -> List[Tuple[int, str, int, int]]:
    """
    最优解：先按 (student_id, subject, exam_date) 排序，再一次遍历找出首分和末分。
    返回 (student_id, subject, first_score, latest_score)。
    """
    # 1. 按 student_id、subject、exam_date 排序
    #    这里的 lambda 返回一个三元组，Python 会按顺序比较每个元素
    scores_sorted = sorted(scores, key=lambda x: (x[0], x[1], x[3]))

    result = []
    # 2. 维护当前组合的首分和末分
    cur_student = cur_subject = None
    first_score = latest_score = None

    for stu, sub, sc, date in scores_sorted:
        # 当遇到新的 (student_id, subject) 时，结束上一个组合的比较
        if (stu, sub) != (cur_student, cur_subject):
            # 不是第一次遍历（即上一个组合已经收集完毕）
            if cur_student is not None and latest_score > first_score:
                result.append((cur_student, cur_subject, first_score, latest_score))

            # 重置为新组合的信息
            cur_student, cur_subject = stu, sub
            first_score = sc          # 第一次出现的分数，就是最早的分数
            latest_score = sc         # 同时初始化为当前分数，后面会被更新
        else:
            # 同一组合的后续记录，只需要更新 latest_score
            latest_score = sc

    # 处理最后一个组合（循环结束后它还没有被写入结果）
    if cur_student is not None and latest_score > first_score:
        result.append((cur_student, cur_subject, first_score, latest_score))

    # 3. 因为已经是按 (student_id, subject) 的顺序，直接返回
    return result

# ---------- 运行 ----------
for row in optimal(scores):
    print(row)
```

**关键注释**  
- `sorted(..., key=lambda x: (x[0], x[1], x[3]))`：一次把所有记录排好顺序，等价于把“成绩簿”先按学生、科目、日期排好。  
- `if (stu, sub) != (cur_student, cur_subject):`：检测是否换到了新的学生‑科目组合。  
- `first_score` 只在首次出现时设定，`latest_score` 在遍历过程中不断被最新的 `score` 覆盖。  
- 循环结束后别忘了把 **最后一个** 组合的结果写入 `result`。

#### 复杂度

- **时间复杂度**：`O(N log N)`  
  - 排序需要 `N log N`（`N` 为记录数）。  
  - 排序后只做一次线性扫描 `O(N)`，相较于暴力解的多次遍历，整体更快。  
  - 大白话：想象把一本乱序的成绩簿先整理好顺序（花点时间），以后查找只需要一次快速翻页。

- **空间复杂度**：`O(N)`（用于存放排序后的列表和结果）。  
  - 这和暴力解的空间需求相同，只是额外占用了一个排好序的副本。

---

## 心得

- **核心技巧**：**排序 + 一次线性扫描**（也叫 “扫描合并”），它能够在只遍历一次数据的前提下，快速获得每组的“首”和“尾”。  
- **适用场景**：  
  1. **找每组的最早/最晚、最大/最小**（如“每个用户的首次登录时间”“每个商品的最高售价”）。  
  2. **区间合并类问题**（如“合并重叠会议”“统计连续天数的最大值”）。  
  3. **分组后需要顺序信息的统计**（如“每位学生每科的成绩进步情况”）。  
- **一句话总结**：**先把同类数据排好顺序，再一次遍历即可轻松得到首尾比较结果**。

---

## 反思

- **第一反应**：看到“first_score”和“latest_score”，立刻想到要对每个学生‑科目找出最早和最晚的记录，于是想到 **分组** + **遍历**。  
- **最容易踩的坑**  
  1. **日期比较**：如果日期是字符串，必须保证格式统一为 `YYYY-MM-DD`，才能直接用 `<`、`>` 比较。  
  2. **忘记处理最后一组**：一次遍历时，循环结束后最后一个组合的结果往往忘记写入答案。  
  3. **排序顺序**：忘记把 `exam_date` 也加入排序键，导致同一学生‑科目的记录仍然是乱序的，进而得到错误的 `first_score`/`latest_score`。  
- **下次遇到同类题的第一步**：**先思考是否可以通过一次排序把同类数据聚在一起**；如果可以，后续就只需要一次线性扫描即可完成统计。