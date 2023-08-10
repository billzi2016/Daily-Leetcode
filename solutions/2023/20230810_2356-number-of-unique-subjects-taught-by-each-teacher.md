# #2356. 每位教师教授的唯一科目数量 / Number of Unique Subjects Taught by Each Teacher

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/number-of-unique-subjects-taught-by-each-teacher/)

---

## 题目（英文原版）

**Description**

Table: Teacher
Write a solution to calculate the number of unique subjects each teacher teaches in the university.
Return the result table in any order.
The result format is shown in the following example.

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| teacher_id  | int  |
| subject_id  | int  |
| dept_id     | int  |
+-------------+------+
(subject_id, dept_id) is the primary key (combinations of columns with unique values) of this table.
Each row in this table indicates that the teacher with teacher_id teaches the subject subject_id in the department dept_id.
```

**Example 2:**

```
Input: 
Teacher table:
+------------+------------+---------+
| teacher_id | subject_id | dept_id |
+------------+------------+---------+
| 1          | 2          | 3       |
| 1          | 2          | 4       |
| 1          | 3          | 3       |
| 2          | 1          | 1       |
| 2          | 2          | 1       |
| 2          | 3          | 1       |
| 2          | 4          | 1       |
+------------+------------+---------+
Output:  
+------------+-----+
| teacher_id | cnt |
+------------+-----+
| 1          | 2   |
| 2          | 4   |
+------------+-----+
Explanation: 
Teacher 1:
  - They teach subject 2 in departments 3 and 4.
  - They teach subject 3 in department 3.
Teacher 2:
  - They teach subject 1 in department 1.
  - They teach subject 2 in department 1.
  - They teach subject 3 in department 1.
  - They teach subject 4 in department 1.
```

---

## 题目（中文翻译）

编写一个 SQL 查询，计算大学中每位教师教授的唯一科目（subject）的数量。  
返回的结果表可以任意排序。结果格式参见下面示例。

**示例 1**

表结构：

```sql
+-------------+------+
| Column Name | Type |
+-------------+------+
| teacher_id  | int  |
| subject_id  | int  |
| dept_id     | int  |
+-------------+------+
```

`(subject_id, dept_id)` 为主键（primary key），即该表中每行的组合值唯一。  
每一行表示 `teacher_id` 对应的教师在 `dept_id` 所在的系教授 `subject_id` 这门科目。

**示例 2**

输入：

Teacher 表：

```sql
+------------+------------+---------+
| teacher_id | subject_id | dept_id |
+------------+------------+---------+
| 1          | 2          | 3       |
| 1          | 2          | 4       |
| 1          | 3          | 3       |
| 2          | 1          | 1       |
| 2          | 2          | 1       |
| 2          | 3          | 1       |
| 2          | 4          | 1       |
... (已截断)
```

约束条件：  
无

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把表里的每一行都拿出来，逐个检查老师教了哪些科目**。  

- **数据结构**：把 `Teacher` 表读取成一个 `list`，每个元素是 `(teacher_id, subject_id, dept_id)` 的元组。  
- 为了统计每位老师的科目数量，我们可以用一个 **字典** `teacher_subjects`，键是 `teacher_id`，值是 **列表**，把该老师出现的所有 `subject_id` 都放进去。  
- 最后遍历这个字典，用 `set()` 把列表去重（`set` 就像一本“词典”，相同的词只会出现一次），得到每位老师真正教的不同科目数。

> **类比**：把老师看成“学生”，把科目看成“图书”。把所有老师借的书记录下来后，用“图书馆的去重功能”（`set`）把重复的书过滤掉，剩下的就是每位老师实际借的不同书的数量。

**为什么正确**：  
- 每一行都被完整遍历一次，所有老师对应的所有科目都会被记录下来。  
- `set` 能够保证相同的 `subject_id` 只算一次，正好满足“唯一科目”的要求。

#### 代码（Python）

```python
# 暴力解：逐行收集，再去重
def unique_subjects_brute(teacher_table):
    """
    teacher_table: List[Tuple[int, int, int]]
        每个元组分别是 (teacher_id, subject_id, dept_id)
    返回值: List[Tuple[int, int]]  -> (teacher_id, unique_subject_count)
    """
    # 1️⃣ 用字典把每位老师的所有科目都收集起来（可能会有重复）
    teacher_subjects = {}                     # {teacher_id: [subject_id, ...]}
    for teacher_id, subject_id, _ in teacher_table:
        if teacher_id not in teacher_subjects:
            teacher_subjects[teacher_id] = []  # 第一次出现，先建空列表
        teacher_subjects[teacher_id].append(subject_id)   # 把科目加入列表

    # 2️⃣ 把列表去重并计数
    result = []
    for teacher_id, subjects in teacher_subjects.items():
        unique_cnt = len(set(subjects))       # set() 自动去掉重复的 subject_id
        result.append((teacher_id, unique_cnt))

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次表格（`n` 行），每行做 O(1) 的字典操作。  
  - 再遍历字典的键（老师的数量 `k ≤ n`），对每位老师的科目列表调用 `set()`，总元素仍然是 `n`，所以整体仍是线性时间。  
  - 大白话：如果表里有 1000 条记录，程序大约会跑 1000 次循环，算是“一次遍历完”。

- **空间复杂度**：`O(n)`  
  - 需要存放所有老师对应的科目列表，最坏情况下每条记录都要保存一次。  
  - 大白话：如果有 1000 条记录，就要用大约 1000 个格子来暂存它们。

---

### 2. 最优解  

#### 思路  

从暴力解来看，**真正的瓶颈**并不是时间，而是**不必要的列表保存**：我们在第一次遍历时就已经可以直接把“唯一科目”计数好，而不必先把所有科目收集进列表再去重。

**优化思路**：

1. **使用集合（set）直接记录**每位老师已经出现过的科目。  
2. 当遍历到一条记录时，尝试把 `subject_id` 加入该老师的集合。  
   - 如果该科目已经在集合里，`add` 操作不产生变化（相当于已经计数过了）。  
   - 如果是新科目，集合的大小会自动加 1。  
3. 最后只要把每个老师集合的大小取出来即可。

**核心数据结构**：**字典 + 集合**（`defaultdict(set)`）  
- `defaultdict` 可以省去“键不存在时手动创建空集合”的判断。  
- `set` 本身就能保证唯一性，省去了后续的 `set()` 去重步骤。

> **类比**：把老师的“科目卡片盒”想象成一个“抽屉”。每次老师教新科目，就往抽屉里放一张卡片；如果已经有相同卡片，抽屉不会再多出一张。抽屉里卡片的数量，就是老师教的不同科目数。

#### 代码（Python）

```python
from collections import defaultdict

def unique_subjects_optimal(teacher_table):
    """
    只遍历一次表格，直接用 set 记录每位老师的唯一科目。
    """
    # 1️⃣ 用 defaultdict 自动创建空 set，键是 teacher_id，值是该老师的 subject_id 集合
    teacher_to_subjects = defaultdict(set)   # {teacher_id: {subject_id, ...}}

    # 2️⃣ 逐行加入集合，集合会自行去重
    for teacher_id, subject_id, _ in teacher_table:
        teacher_to_subjects[teacher_id].add(subject_id)   # add 重复时不影响集合

    # 3️⃣ 把每位老师的集合大小取出来
    result = [(tid, len(subjs)) for tid, subjs in teacher_to_subjects.items()]
    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只进行一次遍历，每条记录的 `add` 操作在集合中均摊为 O(1)。  
  - 与暴力解相比，省去了第二次遍历（去重），但整体仍是线性时间。  
  - 大白话：表里有多少条记录，就跑多少次循环，没别的额外开销。

- **空间复杂度**：`O(k)`，其中 `k` 为 **不同的 (teacher_id, subject_id) 对数**。  
  - 每个唯一的老师‑科目组合只会在集合中保存一次。  
  - 相比暴力解的 `O(n)`，在最坏情况下两者相同，但在很多实际数据里，`k` 会明显小于 `n`（因为同一老师可能教同一科目多次），所以更省空间。

---

## 心得  

- **核心技巧**：利用 **集合去重** 的特性，配合 **字典/默认字典** 把“老师 → 科目集合”映射起来。  
- **适用的题型**：  
  1. “统计每个用户/客户/学生的唯一行为/商品/科目数”  
  2. “求每个部门/类别的不同元素数量”  
  3. “找出每个键对应的不同值集合大小”  
- **解题钥匙**：**一次遍历 + 集合自动去重**。

---

## 反思  

- **第一反应**：看到“每位老师的唯一科目数”，立刻想到 “把老师分组，然后去重计数”。  
- **最容易踩的坑**：  
  - 忘记去掉 `dept_id`，误把 `(teacher_id, subject_id, dept_id)` 当作唯一键，导致同一科目在不同系被误算为不同科目。  
  - 处理空表或只有一种老师时的边界情况，需要确保返回空列表或正确的计数。  
- **下次第一步**：先想 **“要用什么数据结构能天然去重？”**——答案往往是 `set`，配合 `dict` 完成分组。这样可以直接写出最简洁、最优的解法。