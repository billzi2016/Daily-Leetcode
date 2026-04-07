# #3586. 查找 COVID 康复患者 / Find COVID Recovery Patients

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-covid-recovery-patients/)

---

## 题目（英文原版）

**Description**

Table: patients
Table: covid_tests
Write a solution to find patients who have recovered from COVID - patients who tested positive but later tested negative.
Return the result table ordered by recovery_time in ascending order, then by patient_name in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| patient_id  | int     |
| patient_name| varchar |
| age         | int     |
+-------------+---------+
patient_id is the unique identifier for this table.
Each row contains information about a patient.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| test_id     | int     |
| patient_id  | int     |
| test_date   | date    |
| result      | varchar |
+-------------+---------+
test_id is the unique identifier for this table.
Each row represents a COVID test result. The result can be Positive, Negative, or Inconclusive.
```

**Example 3:**

```
+------------+--------------+-----+
| patient_id | patient_name | age |
+------------+--------------+-----+
| 1          | Alice Smith  | 28  |
| 2          | Bob Johnson  | 35  |
| 3          | Carol Davis  | 42  |
| 4          | David Wilson | 31  |
| 5          | Emma Brown   | 29  |
+------------+--------------+-----+
```

**Example 4:**

```
+---------+------------+------------+--------------+
| test_id | patient_id | test_date  | result       |
+---------+------------+------------+--------------+
| 1       | 1          | 2023-01-15 | Positive     |
| 2       | 1          | 2023-01-25 | Negative     |
| 3       | 2          | 2023-02-01 | Positive     |
| 4       | 2          | 2023-02-05 | Inconclusive |
| 5       | 2          | 2023-02-12 | Negative     |
| 6       | 3          | 2023-01-20 | Negative     |
| 7       | 3          | 2023-02-10 | Positive     |
| 8       | 3          | 2023-02-20 | Negative     |
| 9       | 4          | 2023-01-10 | Positive     |
| 10      | 4          | 2023-01-18 | Positive     |
| 11      | 5          | 2023-02-15 | Negative     |
| 12      | 5          | 2023-02-20 | Negative     |
+---------+------------+------------+--------------+
```

**Example 5:**

```
+------------+--------------+-----+---------------+
| patient_id | patient_name | age | recovery_time |
+------------+--------------+-----+---------------+
| 1          | Alice Smith  | 28  | 10            |
| 3          | Carol Davis  | 42  | 10            |
| 2          | Bob Johnson  | 35  | 11            |
+------------+--------------+-----+---------------+
```

---

## 题目（中文翻译）

编写 SQL 查询，找出已从 COVID 中恢复的患者——即先检测为 Positive（阳性），随后检测为 Negative（阴性）的患者。  
返回结果表按照 recovery_time（恢复天数）升序排列，若恢复天数相同则按 patient_name（患者姓名）升序排列。  
结果格式参照下面的示例。

**表结构**

**patients 表**

| Column Name | Type    |
|-------------|---------|
| patient_id  | int     |
| patient_name| varchar |
| age         | int     |

`patient_id` 是该表的唯一标识。每一行记录一位患者的信息。

**covid_tests 表**

| Column Name | Type    |
|-------------|---------|
| test_id     | int     |
| patient_id  | int     |
| test_date   | date    |
| result      | varchar |

`test_id` 是该表的唯一标识。每一行代表一次 COVID 检测结果，`result` 的取值可以是 Positive（阳性）、Negative（阴性）或 Inconclusive（不确定）。

**示例数据**

patients 表

| patient_id | patient_name | age |
|------------|--------------|-----|
| 1          | Alice Smith  | 28  |
| 2          | Bob Johnson  | 35  |
| 3          | Carol Davis  | 42  |
| 4          | David Wilson | 31  |
| 5          | Emma Brown   | 29  |

covid_tests 表

| test_id | patient_id | test_date  | result       |
|---------|------------|------------|--------------|
| 1       | 1          | 2023-01-15 | Positive     |
| 2       | 1          | 2023-01-25 | Negative     |
| 3       | 2          | 2023-02-01 | Positive     |
| 4       | 2          | 2023-02-05 | Inconclusive |
| 5       | 2          | 2023 … (已截断) |

**期望输出**

| patient_id | patient_name | age | recovery_time |
|------------|--------------|-----|---------------|
| 1          | Alice Smith  | 28  | 10            |
| 3          | Carol Davis  | 42  | 10            |
| 2          | Bob Johnson  | 35  | 11            |

**约束条件**

暂无。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把两张表想象成两本 **登记册**：  

* `patients` 记录每个人的基本信息，就像医院的患者档案。  
* `covid_tests` 记录每一次检测的结果，就像检测日志本。  

要找“先阳性后阴性”的患者，最直接的办法是 **把每个患者的所有检测记录都挑出来，逐一比较**：

1. 对每一个患者 `p`（遍历 `patients` 表），取出该患者在 `covid_tests` 表里的所有行。  
2. 在这些检测记录里，找出 **最早的 Positive**（第一次检测出阳性）。  
3. 再在 **Positive 之后的记录** 中找出 **最早的 Negative**（第一次检测转阴）。  
4. 两个日期相减得到 `recovery_time`（恢复天数），把患者信息连同 `recovery_time` 放进结果集合。  

> **类比**：把每个人的检测日志当成一本日记，先找到日记里第一次出现“发烧”，再往后找第一次出现“退烧”。  

这种做法一定能得到正确答案，因为我们把**所有可能的检测顺序**都检查了一遍，只要出现了“阳性 → 阴性”，就会被捕获。

#### 代码（Python）

```python
import datetime
from typing import List, Dict, Tuple

# ---------- 模拟的表数据 ----------
# patients 表：每条记录是 (patient_id, patient_name, age)
patients = [
    (1, "Alice Smith", 28),
    (2, "Bob Johnson", 35),
    (3, "Carol Davis", 42),
    (4, "David Wilson", 31),
    (5, "Emma Brown", 29),
]

# covid_tests 表：每条记录是 (test_id, patient_id, test_date, result)
covid_tests = [
    (1, 1, "2023-01-15", "Positive"),
    (2, 1, "2023-01-25", "Negative"),
    (3, 2, "2023-02-01", "Positive"),
    (4, 2, "2023-02-05", "Inconclusive"),
    (5, 2, "2023-02-12", "Negative"),
    (6, 3, "2023-03-01", "Positive"),
    (7, 3, "2023-03-11", "Negative"),
    # … 其它数据 …
]

def str_to_date(s: str) -> datetime.date:
    """把 'YYYY-MM-DD' 字符串转成 date 对象，方便相减"""
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()


# ---------- 暴力实现 ----------
def brute_force_recovery(patients: List[Tuple],
                         tests: List[Tuple]) -> List[Tuple]:
    """
    返回 (patient_id, patient_name, age, recovery_time) 的列表
    """
    result = []

    # 把所有检测记录按照 patient_id 分组，方便后面取子集
    tests_by_patient: Dict[int, List[Tuple]] = {}
    for t in tests:
        pid = t[1]
        tests_by_patient.setdefault(pid, []).append(t)

    # 对每个患者逐一检查
    for pid, name, age in patients:
        # 若该患者没有检测记录，直接跳过
        if pid not in tests_by_patient:
            continue

        # 把该患者的检测记录按日期升序排列（相当于日记的时间顺序）
        records = sorted(tests_by_patient[pid],
                         key=lambda x: str_to_date(x[2]))

        first_positive = None          # 第一次出现 Positive 的日期
        recovery_days = None           # 计算得到的恢复天数

        # 逐条遍历检测记录，模拟“日记本”翻页
        for _, _, date_str, result in records:
            cur_date = str_to_date(date_str)

            if first_positive is None:
                # 还没有找到 Positive，就看有没有 Positive
                if result == "Positive":
                    first_positive = cur_date
            else:
                # 已经找到 Positive，接下来找第一个 Negative
                if result == "Negative":
                    recovery_days = (cur_date - first_positive).days
                    break   # 找到第一组 Positive→Negative，结束循环

        # 如果找到了恢复天数，就把结果加入返回列表
        if recovery_days is not None:
            result.append((pid, name, age, recovery_days))

    # 最后按照题目要求排序
    result.sort(key=lambda x: (x[3], x[1]))   # recovery_time, patient_name
    return result


# 运行示例
for row in brute_force_recovery(patients, covid_tests):
    print(row)
```

**关键行解释**  

- `tests_by_patient`：把检测记录按患者分组，类似于把每个人的日记本分出来，查找时不需要遍历全表。  
- `sorted(..., key=...)`：把每本日记按日期从早到晚排好顺序，保证我们“先看到的就是最早的”。  
- `first_positive` 与 `recovery_days`：分别记录第一次阳性和随后第一次阴性，两个变量的出现顺序决定了“恢复”是否成立。  

#### 复杂度  

- **时间复杂度**：`O(P * T_log)`  
  - `P` 为患者数量（遍历 `patients` 表），  
  - 对每个患者我们要把对应的检测记录排序，设该患者有 `k` 条记录，则排序耗时 `O(k log k)`。  
  - 整体上相当于 **对所有检测记录做一次排序**（`O(N log N)`），再线性扫描一次（`O(N)`），所以总体是 `O(N log N)`。  
  - 用大白话说，就是“先把所有日志按日期排好序，这一步最耗时”。  

- **空间复杂度**：`O(N)`  
  - 需要额外的字典 `tests_by_patient` 把所有检测记录存一遍，和原始数据量同大小。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于对每个患者的检测记录进行排序**。如果原始 `covid_tests` 表已经是 **按 `patient_id`、`test_date` 排好序**（在真实数据库里我们可以直接在查询里 `ORDER BY`），我们就可以 **一次遍历** 把所有患者的恢复信息算出来，而不必为每个人单独排序。

**优化思路**：

1. **一次性把所有检测记录按 `patient_id`、`test_date` 排序**（一次全局排序代替多次局部排序）。  
2. 采用 **双指针/状态机** 的方式在同一次遍历中为每个患者记录：  
   - `first_positive_date`（首次阳性日期）  
   - 当出现阴性且已经记录了阳性时，立刻算出 `recovery_time`，并把患者加入结果。  
3. 为了在遍历结束后还能得到患者的基本信息（`patient_name`、`age`），我们把 `patients` 表先放进 **哈希表**（字典），相当于把患者档案装进一本“快速查询的电话簿”。  
4. 最后只需要一次排序（对结果按 `recovery_time`、`patient_name` 排序）即可返回。

> **类比**：想象把所有人的检测日志混在一起排好序，就像把所有人的日记按日期顺序合并成一本“大日志”。我们只要从头到尾顺着读，一看到“阳性”，就记下来；随后一旦出现对应人的“阴性”，立即算出两天的差值——不需要再回头找。

#### 代码（Python）

```python
import datetime
from typing import List, Tuple, Dict

# ---------- 仍然使用上面示例的表数据 ----------
# （这里不再重复定义，直接复用前面的 patients、covid_tests）

def str_to_date(s: str) -> datetime.date:
    return datetime.datetime.strptime(s, "%Y-%m-%d").date()


def optimal_recovery(patients: List[Tuple],
                     tests: List[Tuple]) -> List[Tuple]:
    """
    O(N log N) 时间、O(N) 空间的最优实现
    返回 (patient_id, patient_name, age, recovery_time) 的列表
    """
    # 1. 把患者信息放进字典，方便 O(1) 查询（相当于“电话簿”）
    patient_info: Dict[int, Tuple[str, int]] = {
        pid: (name, age) for pid, name, age in patients
    }

    # 2. 把所有检测记录一次性排序：先 patient_id 再 test_date
    #    这一步只做一次全局排序，代替了每个人的局部排序
    sorted_tests = sorted(tests,
                         key=lambda x: (x[1], str_to_date(x[2])))

    # 3. 用两个字典维护状态
    first_positive: Dict[int, datetime.date] = {}   # patient_id -> 第一次阳性日期
    recovered: List[Tuple[int, str, int, int]] = [] # 最终结果列表

    for _, pid, date_str, result in sorted_tests:
        # 若该患者根本不在 patients 表里（不可能，但防御性写法），直接跳过
        if pid not in patient_info:
            continue

        cur_date = str_to_date(date_str)

        if result == "Positive":
            # 只在还没有记录阳性时保存（只保留第一次阳性）
            if pid not in first_positive:
                first_positive[pid] = cur_date
        elif result == "Negative":
            # 只在已经出现阳性且还未恢复的情况下才计算恢复天数
            if pid in first_positive:
                # 计算恢复天数
                days = (cur_date - first_positive[pid]).days
                name, age = patient_info[pid]
                recovered.append((pid, name, age, days))
                # 恢复后就不再需要该患者的状态，防止后面的负面检测再次计入
                del first_positive[pid]

        # 其他结果（Inconclusive）直接忽略

    # 4. 按题目要求排序：恢复天数升序，若相同再按姓名升序
    recovered.sort(key=lambda x: (x[3], x[1]))
    return recovered


# 运行示例
for row in optimal_recovery(patients, covid_tests):
    print(row)
```

**关键行解释**  

- `sorted(tests, key=lambda x: (x[1], str_to_date(x[2])))`：一次性把所有检测记录按患者编号、检测日期排好序，等价于在 SQL 里 `ORDER BY patient_id, test_date`。  
- `first_positive`：记录每个患者**首次出现 Positive**的日期，一旦记录就不再覆盖（只保留最早的）。  
- 当遍历到 `Negative` 且已经有 `first_positive` 时，立刻算出恢复天数并加入 `recovered`，随后把该患者从 `first_positive` 中删除，保证每位患者只计入一次。  
- 最后一次 `sort` 只作用在结果集上，规模通常远小于原始检测记录。  

#### 复杂度  

- **时间复杂度**：`O(N log N)`  
  - `N` 为 `covid_tests` 表的记录数。唯一的 `log N` 来自 **一次全局排序**。随后一次线性遍历 `O(N)`，不再有额外的排序或嵌套循环。  
  - 与暴力解相比，**把多次小排序合并成一次大排序**，大幅降低常数因子。  

- **空间复杂度**：`O(N)`  
  - 需要保存排序后的检测记录（Python 的 `sorted` 会产生新列表）以及两个字典 `patient_info`、`first_positive`，总体线性于输入规模。  

---

## 心得  

- **核心技巧**：一次全局排序 + 状态机（记录首次阳性 → 首次阴性）  
- **适用的题型**  
  1. “首次出现 A 后的首次出现 B” 类的时间序列问题（如用户登录后首次下单）。  
  2. “在同一组数据中找满足先后关系的两条记录” （如员工调岗前后的工资变化）。  
  3. “在有序日志里提取事件间隔” （如系统故障恢复时间）。  
- **一句话总结解题钥匙**：**把所有日志按组+时间一次排好序，用一次遍历记录“第一次出现 A”，随后在同一次遍历里捕获对应的“第一次出现 B”。**  

---

## 反思  

- **第一反应**：把每个人的检测记录单独挑出来再排序，写两层循环；这看起来最直观，却会导致大量重复工作。  
- **最容易踩的坑**  
  1. **漏掉相同患者的多次阳性**：只需要记录第一次阳性，后面的阳性不影响恢复天数。  
  2. **阴性出现在阳性之前**：必须保证只在已经记录阳性的情况下才计算恢复时间。  
  3. **患者在 `patients` 表里但没有检测记录**：要安全地跳过。  
  4. **日期差值的正负**：使用 `datetime` 进行相减，避免手动计算导致错误。  
- **下次遇到类似题**：第一步先 **把原始日志统一排序**（或利用已有索引），再 **用状态机一次遍历** 完成需求，避免在每个分组内部重复排序或多次扫描。