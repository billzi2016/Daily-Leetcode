# #3617. 查找遵循学习螺旋模式的学生 / Find Students with Study Spiral Pattern

> 难度：困难 · 标签： · [LeetCode 链接](https://leetcode.com/problems/find-students-with-study-spiral-pattern/)

---

## 题目（英文原版）

**Description**

Table: students
Table: study_sessions
Write a solution to find students who follow the Study Spiral Pattern - students who consistently study multiple subjects in a rotating cycle.
Return the result table ordered by cycle length in descending order, then by total study hours in descending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| student_id   | int     |
| student_name | varchar |
| major        | varchar |
+--------------+---------+
student_id is the unique identifier for this table.
Each row contains information about a student and their academic major.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| session_id    | int     |
| student_id    | int     |
| subject       | varchar |
| session_date  | date    |
| hours_studied | decimal |
+---------------+---------+
session_id is the unique identifier for this table.
Each row represents a study session by a student for a specific subject.
```

**Example 3:**

```
+------------+--------------+------------------+
| student_id | student_name | major            |
+------------+--------------+------------------+
| 1          | Alice Chen   | Computer Science |
| 2          | Bob Johnson  | Mathematics      |
| 3          | Carol Davis  | Physics          |
| 4          | David Wilson | Chemistry        |
| 5          | Emma Brown   | Biology          |
+------------+--------------+------------------+
```

**Example 4:**

```
+------------+------------+------------+--------------+---------------+
| session_id | student_id | subject    | session_date | hours_studied |
+------------+------------+------------+--------------+---------------+
| 1          | 1          | Math       | 2023-10-01   | 2.5           |
| 2          | 1          | Physics    | 2023-10-02   | 3.0           |
| 3          | 1          | Chemistry  | 2023-10-03   | 2.0           |
| 4          | 1          | Math       | 2023-10-04   | 2.5           |
| 5          | 1          | Physics    | 2023-10-05   | 3.0           |
| 6          | 1          | Chemistry  | 2023-10-06   | 2.0           |
| 7          | 2          | Algebra    | 2023-10-01   | 4.0           |
| 8          | 2          | Calculus   | 2023-10-02   | 3.5           |
| 9          | 2          | Statistics | 2023-10-03   | 2.5           |
| 10         | 2          | Geometry   | 2023-10-04   | 3.0           |
| 11         | 2          | Algebra    | 2023-10-05   | 4.0           |
| 12         | 2          | Calculus   | 2023-10-06   | 3.5           |
| 13         | 2          | Statistics | 2023-10-07   | 2.5           |
| 14         | 2          | Geometry   | 2023-10-08   | 3.0           |
| 15         | 3          | Biology    | 2023-10-01   | 2.0           |
| 16         | 3          | Chemistry  | 2023-10-02   | 2.5           |
| 17         | 3          | Biology    | 2023-10-03   | 2.0           |
| 18         | 3          | Chemistry  | 2023-10-04   | 2.5           |
| 19         | 4          | Organic    | 2023-10-01   | 3.0           |
| 20         | 4          | Physical   | 2023-10-05   | 2.5           |
+------------+------------+------------+--------------+---------------+
```

**Example 5:**

```
+------------+--------------+------------------+--------------+-------------------+
| student_id | student_name | major            | cycle_length | total_study_hours |
+------------+--------------+------------------+--------------+-------------------+
| 2          | Bob Johnson  | Mathematics      | 4            | 26.0              |
| 1          | Alice Chen   | Computer Science | 3            | 15.0              |
+------------+--------------+------------------+--------------+-------------------+
```

---

## 题目（中文翻译）

**描述**  
表：`students`  
表：`study_sessions`  

编写查询找出遵循 **Study Spiral Pattern**（学习螺旋模式）的学生——即那些在多个科目之间按固定循环顺序持续学习的学生。  
返回的结果表需按 **cycle_length**（循环长度）降序排列，若循环长度相同，再按 **total_study_hours**（总学习时长）降序排列。  
结果格式参照下例。

**示例**  

示例 1:  

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| student_id   | int     |
| student_name | varchar |
| major        | varchar |
+--------------+---------+
```
`student_id` 为该表的唯一标识。每行记录包含学生的基本信息及其专业。

示例 2:  

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| session_id    | int     |
| student_id    | int     |
| subject       | varchar |
| session_date  | date    |
| hours_studied | decimal |
+---------------+---------+
```
`session_id` 为该表的唯一标识。每行记录代表某学生在某科目上的一次学习会话。

示例 3:  

```
+------------+--------------+----------------+
| student_id | student_name | major          |
+------------+--------------+----------------+
| 1          | Alice Chen   | Computer Science |
| 2          | Bob Johnson  | Mathematics      |
| 3          | Carol Davis  | Physics          |
| 4          | David Wilson | Chemistry        |
| 5          | Emma Brown   | Biology          |
+------------+--------------+----------------+
... (已截断)
```

示例 4:  

```
+------------+------------+------------+--------------+---------------+
| session_id | student_id | subject    | session_date | hours_studied |
+------------+------------+------------+--------------+---------------+
| 1          | 1          | Math       | 2023-10-01   | 2.5           |
| 2          | 1          | Physics    | 2023-10-02   | 3.0           |
| 3          | 1          | Chemistry  |
... (已截断)
```

示例 5（结果表）:  

```
+------------+--------------+----------------+--------------+-------------------+
| student_id | student_name | major          | cycle_length | total_study_hours |
+------------+--------------+----------------+--------------+-------------------+
| 2          | Bob Johnson  | Mathematics    | 4            | 26.0              |
| 1          | Alice Chen   | Computer Science| 3            |
... (已截断)
```

**约束条件**  
无。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **把两张表装进 Python**  
   - `students` 表可以用 `List[Dict]` 或者 `pandas.DataFrame` 表示，每行是一个学生的信息。  
   - `study_sessions` 表同理，记录每一次学习的科目、日期和时长。  

2. **按学生分组、按日期排序**  
   - 先把所有 `study_sessions` 按 `student_id` 分到不同的列表里，然后用日期从早到晚排好顺序。  
   - 这样我们得到每个学生的学习序列，例如 `["Math","Physics","Chemistry","Math","Physics","Chemistry"]`。  

3. **暴力枚举“旋转周期”**  
   - 把上面的序列记作 `S`，长度记为 `n`。  
   - 我们把可能的周期长度 `k` 从 `1` 到 `n//2`（因为周期至少要出现两次）逐个尝试。  
   - 对每个 `k`，检查 `S[i] == S[i%k]` 是否对所有 `i` 成立（即前 `k` 个科目不断循环）。  
   - 第一个满足条件的 `k` 就是该学生的 **循环长度**（如果没有任何 `k` 满足，则说明他没有形成螺旋模式）。  

4. **统计总学习时长**  
   - 只要学生有合法的循环长度，就把该学生所有 `hours_studied` 加总，得到 `total_study_hours`。  

5. **排序输出**  
   - 按 `cycle_length` 降序；如果相同，再按 `total_study_hours` 降序。  

> **类比**：  
> - 哈希表（`dict`）就像一本词典，单词是 **key**，对应的解释是 **value**。我们用它把 `student_id → [session...]` 这层映射存起来，查找时只要给出 `student_id`，立马能拿到该学生的所有记录。  

> **为什么正确**：  
> - 我们穷举了所有可能的周期长度，只要有一种长度能让整个序列完整地由一个小块循环得到，就一定是学生的“学习螺旋”。  
> - 统计总时长直接把所有记录相加，不会漏掉任何一次学习。  

#### 代码（Python）

```python
from collections import defaultdict
from datetime import datetime
from typing import List, Dict, Tuple

# ------------------- 模拟数据读取 -------------------
# students = [
#     {"student_id": 1, "student_name": "Alice Chen", "major": "Computer Science"},
#     {"student_id": 2, "student_name": "Bob Johnson", "major": "Mathematics"},
#     ...
# ]
# study_sessions = [
#     {"session_id": 1, "student_id": 1, "subject": "Math", "session_date": "2023-10-01", "hours_studied": 2.5},
#     {"session_id": 2, "student_id": 1, "subject": "Physics", "session_date": "2023-10-02", "hours_studied": 3.0},
#     ...
# ]

def find_spiral_bruteforce(students: List[Dict],
                           study_sessions: List[Dict]) -> List[Dict]:
    # 1️⃣ 按学生分组并按日期排序
    sessions_by_student = defaultdict(list)
    for s in study_sessions:
        # 把日期字符串转成 datetime，方便排序
        s["session_date"] = datetime.strptime(s["session_date"], "%Y-%m-%d")
        sessions_by_student[s["student_id"]].append(s)

    # 2️⃣ 计算每个学生的循环长度和总学习时长
    result = []
    for stu in students:
        sid = stu["student_id"]
        sess = sessions_by_student.get(sid, [])
        if not sess:                     # 没有学习记录直接跳过
            continue

        # 按日期升序排列
        sess.sort(key=lambda x: x["session_date"])
        subjects = [s["subject"] for s in sess]
        total_hours = sum(s["hours_studied"] for s in sess)

        n = len(subjects)
        cycle_len = None                 # 记录找到的最小合法周期

        # 暴力尝试所有可能的周期长度 k (1 ~ n//2)
        for k in range(1, n // 2 + 1):
            # 检查前 k 个科目是否能完整循环覆盖整个序列
            ok = True
            for i in range(n):
                if subjects[i] != subjects[i % k]:
                    ok = False
                    break
            if ok:                        # 找到第一个合法的 k
                cycle_len = k
                break

        if cycle_len:                     # 只有真的形成螺旋才加入结果
            result.append({
                "student_id": sid,
                "student_name": stu["student_name"],
                "major": stu["major"],
                "cycle_length": cycle_len,
                "total_study_hours": round(total_hours, 2)   # 保留两位小数
            })

    # 3️⃣ 排序：先按 cycle_length 降序，再按 total_study_hours 降序
    result.sort(key=lambda x: (-x["cycle_length"], -x["total_study_hours"]))
    return result

# ------------------- 调用示例 -------------------
# ans = find_spiral_bruteforce(students, study_sessions)
# for row in ans:
#     print(row)
```

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N` 为所有学习记录的总数（遍历一次把记录放进哈希表）。  
  - 对每个学生，我们最多会尝试 `L/2` 种周期长度（`L` 为该学生的记录条数），每次检查需要遍历 `L` 次。最坏情况下相当于 `L²/2`，但整体仍然是 `O(N * L)`，在数据量很大时会比较慢。  
  - 用大白话说，若一位学生有 100 条记录，暴力法要检查大约 5 000 次比较；学生越多，比较次数呈指数增长。

- **空间复杂度**：`O(N)`  
  - 需要把所有学习记录存进 `defaultdict`，相当于原始数据的副本。  
  - 额外的空间主要是几个临时列表，和输入规模同量级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有可能的周期长度并逐条比较**，这会导致二次遍历。  
我们可以把“找最小循环周期”这个子问题抽象为**字符串的最小周期**问题：  
- 把科目序列看成一个字符序列，例如 `["Math","Physics","Chemistry","Math","Physics","Chemistry"]` → `"Math|Physics|Chemistry|Math|Physics|Chemistry"`（用特殊分隔符防止科目名冲突）。  
- 对这个“字符串”求 **前缀函数**（KMP 算法中的 `lps`，即最长相等前后缀的长度），即可在 **线性时间 O(L)** 内得到最小周期。

**核心概念——前缀函数（prefix function）**  
- 对于序列 `S[0..L-1]`，`pi[i]` 表示 `S[0..i]` 的最长相等的前缀和后缀的长度（不包括完整的 `S[0..i]` 本身）。  
- 当 `L % (L - pi[L-1]) == 0` 时，`L - pi[L-1]` 就是最小的循环长度。  
- 这相当于把“找最小螺旋周期”变成“一遍扫描求最长公共前后缀”，避免了多次比较。

**步骤概览**  

| 步骤 | 说明 |
|------|------|
| 1️⃣ 数据准备 | 同暴力解：把记录按学生分组、按日期排序，得到每位学生的 `subjects` 列表和 `total_hours`。 |
| 2️⃣ 构造前缀函数 | 对 `subjects`（列表）直接跑 KMP 前缀函数（不需要转成字符串），时间 `O(L)`。 |
| 3️⃣ 判定是否形成螺旋 | 计算 `candidate = L - pi[-1]`；若 `L % candidate == 0` 且 `candidate < L`，则 `candidate` 为合法的循环长度。 |
| 4️⃣ 收集结果 & 排序 | 与暴力解相同，只是得到的 `cycle_length` 更快。 |

**为什么更快**  
- 每位学生只遍历一次 `subjects`（O(L)），不再枚举所有可能的 `k`。  
- 整体时间变为 **线性**：`O(N)`（遍历所有记录一次）+ `O(N)`（KMP 前缀函数），即 `O(N)`，相比暴力的 `O(N * L)` 大幅下降。

#### 代码（Python）

```python
from collections import defaultdict
from datetime import datetime
from typing import List, Dict

def _prefix_function(arr: List[str]) -> List[int]:
    """
    KMP 前缀函数（lps）实现，直接对字符串列表工作。
    pi[i] = 最长相等的前缀和后缀的长度（不含全串）。
    时间复杂度 O(len(arr))，空间复杂度 O(len(arr))。
    """
    n = len(arr)
    pi = [0] * n
    j = 0  # 当前匹配的长度

    for i in range(1, n):
        # 当不匹配时，回退到上一个可能的前缀长度
        while j > 0 and arr[i] != arr[j]:
            j = pi[j - 1]

        if arr[i] == arr[j]:
            j += 1
            pi[i] = j
        # else: pi[i] 仍为 0
    return pi


def find_spiral_optimal(students: List[Dict],
                        study_sessions: List[Dict]) -> List[Dict]:
    # 1️⃣ 按学生分组并排序（同暴力解）
    sessions_by_student = defaultdict(list)
    for s in study_sessions:
        s["session_date"] = datetime.strptime(s["session_date"], "%Y-%m-%d")
        sessions_by_student[s["student_id"]].append(s)

    result = []
    for stu in students:
        sid = stu["student_id"]
        sess = sessions_by_student.get(sid, [])
        if not sess:
            continue

        sess.sort(key=lambda x: x["session_date"])
        subjects = [s["subject"] for s in sess]
        total_hours = sum(s["hours_studied"] for s in sess)

        L = len(subjects)
        if L < 2:                     # 单条记录不可能形成循环
            continue

        # 2️⃣ 计算前缀函数
        pi = _prefix_function(subjects)
        candidate = L - pi[-1]        # 可能的最小周期长度

        # 3️⃣ 判定是否真的循环（必须完整覆盖且长度小于整体）
        if candidate < L and L % candidate == 0:
            # 说明 subjects = pattern * (L // candidate)
            result.append({
                "student_id": sid,
                "student_name": stu["student_name"],
                "major": stu["major"],
                "cycle_length": candidate,
                "total_study_hours": round(total_hours, 2)
            })

    # 4️⃣ 排序：cycle_length 降序 → total_study_hours 降序
    result.sort(key=lambda x: (-x["cycle_length"], -x["total_study_hours"]))
    return result

# ------------------- 示例调用 -------------------
# ans_opt = find_spiral_optimal(students, study_sessions)
# for row in ans_opt:
#     print(row)
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  - `N` 为所有学习记录的总数。  
  - 对每位学生我们只做一次线性遍历来生成 `subjects`，再一次线性遍历求前缀函数，合计 `2 * L`，相当于常数倍的 `O(L)`。所有学生的 `L` 之和正好是 `N`。  
  - 用大白话说，记录多少条就遍历多少条，一遍扫完就能得到答案，几乎不再“重复检查”。  

- **空间复杂度**：`O(N)`  
  - 与暴力解相同，需要保存分组后的记录。  
  - 前缀函数数组的额外空间是每位学生 `O(L)`，累计也是 `O(N)`。

---

## 心得

- **核心技巧**：利用 **KMP 前缀函数**（或称最长相等前后缀）在 **线性时间** 求出序列的最小循环周期。  
- **适用的题型**（类似的“找循环/重复模式”）  
  1. 判断字符串是否由一个子串循环构成（LeetCode 459 Repeated Substring Pattern）。  
  2. 计算数组的最小周期长度（常见的“数组轮转”或“音乐节拍”问题）。  
  3. 找出日志/行为序列的重复模式（如网站访问路径、机器指令循环）。  

- **一句话总结解题钥匙**：**把“找最小螺旋周期”转化为“最小周期字符串”问题，利用 KMP 前缀函数一次线性扫描即能得到答案**。

---

## 反思

- **第一反应**：看到“循环学习多个科目”，立刻想到把每个学生的学习顺序写成列表，然后逐个尝试可能的周期长度——这就是暴力思路。  
- **最容易踩的坑**  
  - **边界条件**：只有一条或两条记录时不可能形成完整循环，需要提前过滤。  
  - **科目名称冲突**：如果直接把科目拼接成字符串，`"MathPhysics"` 与 `"MathPhy"+"sics"` 可能产生误判。用列表直接跑 KMP 或者在字符串之间加上不可能出现的分隔符（如 `#`）可以避免。  
  - **日期排序**：忘记对 `session_date` 进行排序会导致错误的序列，从而误判循环。  
- **下次类似题的第一步**：先把数据整理成**有序的、仅包含核心信息的序列**（如只保留科目），然后思考“这是不是一个周期性序列”，再决定是暴力枚举还是使用 **前缀函数 / KMP / Z‑algorithm** 这类线性时间的周期检测工具。