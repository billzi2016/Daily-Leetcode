# #596. 至少有5名学生的班级 / Classes With at Least 5 Students

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/classes-with-at-least-5-students/)

---

## 题目（英文原版）

**Description**

Table: Courses
Write a solution to find all the classes that have at least five students.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| student     | varchar |
| class       | varchar |
+-------------+---------+
(student, class) is the primary key (combination of columns with unique values) for this table.
Each row of this table indicates the name of a student and the class in which they are enrolled.
```

**Example 2:**

```
Input: 
Courses table:
+---------+----------+
| student | class    |
+---------+----------+
| A       | Math     |
| B       | English  |
| C       | Math     |
| D       | Biology  |
| E       | Math     |
| F       | Computer |
| G       | Math     |
| H       | Math     |
| I       | Math     |
+---------+----------+
Output: 
+---------+
| class   |
+---------+
| Math    |
+---------+
Explanation: 
- Math has 6 students, so we include it.
- English has 1 student, so we do not include it.
- Biology has 1 student, so we do not include it.
- Computer has 1 student, so we do not include it.
```

---

## 题目（中文翻译）

**描述**  
表（table）: **Courses**  

编写一个查询，找出所有学生人数不少于 5 人的班级（class）。返回结果表，顺序不限。结果格式参照下例。

**示例 1**  

| Column Name | Type    |
|-------------|---------|
| student     | varchar |
| class       | varchar |

(student, class) 是该表的主键（primary key），即由唯一值组成的列的组合。每一行记录表示一名学生的姓名以及其所属的班级。

**示例 2**  

**输入**  

Courses 表：

| student | class    |
|---------|----------|
| A       | Math     |
| B       | English  |
| C       | Math     |
| D       | Biology  |
| E       | Math     |
| F       | Computer |
| G       | Math     |
| H       | Math     |
| I       | Math     |

**输出**  

| class |
|-------|
| Math  |

**解释**  
- Math 班有 6 名学生，满足 “至少 5 名学生” 的条件，故被列出。  
- English、Biology、Computer 班各只有 1 名学生，不满足条件，未被列出。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历每一条记录，拿它的 `class` 去找整张表里所有同样 `class` 的记录，统计出现次数**。  
如果次数 ≥ 5，就把这个 `class` 加入答案。  

- **用到的数据结构**：  
  - `list`（把整张表当成一条条记录的列表）  
  - `set`（用来去重，防止同一个班级被重复加入答案）  

- **为什么正确**：  
  对每一个学生所在的班级，都完整地统计了该班级的学生数。只要统计结果满足题目要求（≥5），就一定是我们要的答案。  

- **时间/空间复杂度**：  
  - 外层循环遍历 `n` 条记录，内层再遍历一次整张表（也是 `n` 条），所以总共大约做了 `n × n = n²` 次比较，**时间复杂度是 O(n²)**。  
    - **大白话**：如果有 100 条记录，程序会进行大约 10 000 次“找同班同学”的操作。  
  - 只用了几个额外的集合保存答案，**空间复杂度是 O(k)**，其中 `k` 是符合条件的班级数（最坏情况下不超过 `n`，但通常很小）。

#### 代码（Python）

```python
from typing import List, Tuple

def classes_with_at_least_five_students_brute(courses: List[Tuple[str, str]]) -> List[str]:
    """
    暴力解法：对每一条记录都遍历整张表统计同班学生数
    参数 courses: List[(student, class)]，模拟数据库表
    返回值: 只包含符合条件的 class 名字的列表
    """
    result = set()                     # 用 set 去重，防止同一个班级多次加入
    n = len(courses)

    for i in range(n):
        _, cur_class = courses[i]      # 取出第 i 条记录的 class
        cnt = 0                        # 统计 cur_class 出现了多少次

        # 内层遍历整张表，统计同班同学数量
        for j in range(n):
            _, other_class = courses[j]
            if other_class == cur_class:
                cnt += 1

        # 如果人数达到 5，加入结果集合
        if cnt >= 5:
            result.add(cur_class)

    # 把集合转成列表返回（顺序不重要）
    return list(result)
```

#### 复杂度

- **时间复杂度**：O(n²) — 每条记录都要遍历整张表，类似“在 100 人里找 100 次”。
- **空间复杂度**：O(k) — 只额外用了一个保存答案的集合，k 是符合条件的班级数。

---

### 2. 最优解

#### 思路  

暴力解的慢点在于**重复统计同一个班级**。  
如果我们先把每个班级出现的次数全部算好，后面只需要一次遍历就能判断是否 ≥ 5。  

这一步可以用 **哈希表（字典）** 来实现：

1. **第一次遍历**：把每条记录的 `class` 作为键，出现一次就把对应的计数加 1。  
   - 哈希表就像一本“查字典”，我们把班级名字当作单词，字典里存的是这个单词出现了多少次（有多少学生）。
2. **第二次遍历**（或直接在第一遍结束后遍历字典）：把计数 ≥ 5 的键挑出来，就是答案。

- **核心算法**：**计数 + 哈希表**（在 Python 里用 `dict` 或 `collections.Counter`）。  
- **为什么快**：每条记录只被“看”一次，统计过程是 O(1) 的哈希查找/写入，总体是 **线性时间 O(n)**。  
- **类比**：想象你在超市排队结账，暴力解每次都重新数一遍排在你前面的顾客，而最优解是让收银员在每个人结账时直接记录人数，这样后面只需要看记录表就行了。

#### 代码（Python）

```python
from collections import Counter
from typing import List, Tuple

def classes_with_at_least_five_students_opt(courses: List[Tuple[str, str]]) -> List[str]:
    """
    最优解：一次遍历统计每个 class 的学生人数，再筛选 >= 5 的 class
    参数 courses: List[(student, class)]
    返回值: 只包含符合条件的 class 名字的列表
    """
    # 1. 统计每个 class 出现的次数（即学生人数）
    class_counter = Counter()
    for _, cls in courses:           # 只关心 class，student 本身不参与计数
        class_counter[cls] += 1

    # 2. 把人数 >= 5 的 class 取出来
    result = [cls for cls, cnt in class_counter.items() if cnt >= 5]

    return result
```

#### 复杂度

- **时间复杂度**：O(n) — 只遍历了一遍 `courses`（计数），再遍历哈希表的键（键的数量 ≤ n），整体是线性增长。  
  - 与暴力解相比，从“每 100 条记录要做 10 000 次比较”降到“只做 100 次计数”。
- **空间复杂度**：O(k) — 哈希表里存了每个不同班级的计数，k 为不同班级的数量，最坏不超过 `n`，但通常远小于 `n`。

---

## 心得

- **核心技巧**：使用哈希表（字典/计数器）一次遍历完成统计，再根据统计结果筛选。  
- **适用的题型**：  
  1. “出现次数不少于/不超过 X 次的元素” （如 LeetCode 统计出现次数的题目）。  
  2. “分组求和/求平均/求最大最小”等需要**先分组再聚合**的查询。  
  3. “找出出现频率最高的前 K 个元素” （利用计数 + 堆或排序）。  
- **一句话总结**：**把“遍历‑计数‑筛选”拆成两步，避免重复统计，时间自然线性**。

---

## 反思

- **第一反应**：看到“找出至少 5 人的班级”，我本能地想到“把每个班级的学生数算出来”，于是直接写了暴力的双层循环。  
- **最容易踩的坑**：  
  - **去重**：暴力解中如果不使用 `set`，同一个班级会被加入答案多次。  
  - **边界条件**：当表中根本没有任何班级达到 5 人时，需要返回空列表，而不是 `None` 或出错。  
  - **数据规模**：如果数据量很大（几万、几十万行），暴力 O(n²) 会超时，需要立刻想到哈希计数。  
- **下次第一步**：先在脑子里把 “分组计数” 用哈希表实现的模板跑一遍——“遍历一次，计数；遍历计数表，筛选”。只要出现 “多少个…的…”，几乎都可以套用这个思路。