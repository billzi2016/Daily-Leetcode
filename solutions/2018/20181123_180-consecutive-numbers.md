# #180. 连续数字 / Consecutive Numbers

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/consecutive-numbers/)

---

## 题目（英文原版）

**Description**

Table: Logs
Find all numbers that appear at least three times consecutively.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+
In SQL, id is the primary key for this table.
id is an autoincrement column starting from 1.
```

**Example 2:**

```
Input: 
Logs table:
+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+
Output: 
+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+
Explanation: 1 is the only number that appears consecutively for at least three times.
```

---

## 题目（中文翻译）

**描述：**  
表（Table）：`Logs`  
找出所有在 `Logs` 表中出现次数不少于 **三次且连续** 的数字（`num`），并返回这些数字构成的结果表（result table），顺序不限。结果表的格式参见下面的示例。

**示例：**  

+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| id          | int     |
| num         | varchar |
+-------------+---------+

在 SQL 中，`id` 为该表的主键，且为自增列，起始值为 1。

**示例 1：**

输入（Logs 表）：

+----+-----+
| id | num |
+----+-----+
| 1  | 1   |
| 2  | 1   |
| 3  | 1   |
| 4  | 2   |
| 5  | 1   |
| 6  | 2   |
| 7  | 2   |
+----+-----+

输出（Result 表）：

+-----------------+
| ConsecutiveNums |
+-----------------+
| 1               |
+-----------------+

**解释：**  
`1` 是唯一一个出现次数不少于三次且连续的数字。

**约束条件：**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：把表 `Logs` 按照 `id` 排序（因为 `id` 是自增的，顺序本身就代表了时间顺序），然后**从头到尾一次遍历**，记录当前数字连续出现的次数。  

- **数据结构**：我们只需要一个普通的 Python 列表 `logs` 来存放 `(id, num)`，以及几个临时变量（`prev`、`cnt`、`ans`）。  
  - `prev`：上一条记录的 `num`，相当于“前一页的词”。  
  - `cnt`：当前 `num` 连续出现的次数。  
  - `ans`：满足条件的数字集合，用 `set`（相当于“不重复的词典”）来保存，避免重复计入。  

**为什么正确**：  
遍历时每看到一个新 `num`，就和前一个 `num` 比较：  
- 相同 → 连续计数 `cnt += 1`。  
- 不同 → 把之前的计数清零，重新从 1 开始计数。  
只要计数达到 **3**，说明这段连续出现的长度已经满足题意，把对应的数字加入结果集合即可。遍历结束后，集合里的数字就是所有出现 **至少三次** 连续的数。

**时间/空间复杂度**（大白话）：  
- **时间**：我们只遍历一次表，表里有 `n` 条记录，所以时间是 `O(n)`，也就是“和记录数成正比”。  
- **空间**：除了保存输入数据本身（LeetCode 已经给出），我们只用了常数个变量和一个结果集合，最多存放所有不同的数字，最坏情况是 `O(k)`（`k` 为不同数字的个数），在大多数情况下可以视作 `O(1)`（常数级别）。

#### 代码（Python）  

```python
from typing import List, Tuple

def consecutive_nums_brute(logs: List[Tuple[int, str]]) -> List[str]:
    """
    暴力（直觉）解法
    logs : List[(id, num)]，已按 id 升序排列
    返回所有出现至少三次连续的 num（去重后顺序不要求）
    """
    if not logs:
        return []

    # 用 set 去重，最后直接转成 list 返回
    result = set()

    # 第一次遍历的基准
    prev_num = logs[0][1]   # 前一条记录的 num
    cnt = 1                 # 当前连续出现的次数

    # 从第二条记录开始遍历
    for _, cur_num in logs[1:]:
        if cur_num == prev_num:          # 与前一条相同 → 连续
            cnt += 1
        else:                            # 不同 → 重新计数
            cnt = 1
            prev_num = cur_num

        # 一旦连续次数 >= 3，就把这个数字记下来
        if cnt >= 3:
            result.add(cur_num)

    # 把 set 转成 list（LeetCode 要求返回表格，这里用 list 表示）
    return list(result)


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    # (id, num) 按 id 从小到大给出
    sample_logs = [
        (1, "1"),
        (2, "1"),
        (3, "1"),
        (4, "2"),
        (5, "1"),
        (6, "2"),
        (7, "2"),
    ]
    print(consecutive_nums_brute(sample_logs))   # 输出: ['1']
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次，`n` 为表中记录数。  
- **空间复杂度**：`O(k)` —— `k` 为不同数字的个数（最坏 `k = n`），但一般可以看作 `O(1)`，因为只用了几个计数变量和一个结果集合。

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到，**唯一的瓶颈**其实已经是 `O(n)`，因为我们必须查看每一条记录才能判断是否连续。  
所以“最优”并不是把时间进一步降到 `O(log n)`（那是不可能的），而是**写出更简洁、更易读且不需要手动维护计数的实现**。  

思路如下：

1. **利用 `itertools.groupby`** 把相邻相同的 `num` 分成一组。  
   - `groupby` 会把连续相同的元素聚合在一起，返回 `(num, iterator_of_rows)`。  
   - 这一步相当于“把连续相同的词放进同一本书的同一章节”。  

2. 对每一组检查它的长度（即这段连续出现的次数）。  
   - 长度 `>= 3` 的 `num` 就满足要求，加入答案集合。  

这样我们仍然是一次线性扫描，但把“计数”这件事交给了 Python 标准库，让代码更简洁。

**核心工具——`groupby`** 的类比：  
想象你在排队买咖啡，大家的咖啡种类相同就会站成一小段队。`groupby` 就像是排队的工作人员，把相同种类的顾客划分到同一个小队，方便我们一次性统计每个小队的人数。

**时间/空间复杂度**：  
- 时间仍是 `O(n)`，因为 `groupby` 只会遍历一次输入。  
- 空间仍是 `O(k)`（存放结果集合），额外的临时空间几乎可以忽略。

#### 代码（Python）  

```python
from itertools import groupby
from typing import List, Tuple

def consecutive_nums_opt(logs: List[Tuple[int, str]]) -> List[str]:
    """
    最优（简洁）解法：利用 itertools.groupby 把相邻相同的 num 分组
    """
    if not logs:
        return []

    # 只关心 num，id 已经保证顺序，所以直接对 num 进行 groupby
    result = set()

    # groupby 会把相邻相同的 num 合在一起
    for num, group in groupby(num for _, num in logs):
        length = sum(1 for _ in group)   # 统计该组的大小
        if length >= 3:
            result.add(num)

    return list(result)


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    sample_logs = [
        (1, "1"),
        (2, "1"),
        (3, "1"),
        (4, "2"),
        (5, "1"),
        (6, "2"),
        (7, "2"),
    ]
    print(consecutive_nums_opt(sample_logs))   # 输出: ['1']
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次表格，`groupby` 本身是线性算法。  
- **空间复杂度**：`O(k)` —— 只存放满足条件的不同数字集合。

与暴力解对比：两者时间上没有差距，最优解在**代码可读性**和**实现简洁度**上更好，适合在实际项目中直接使用。

---  

## 心得  

- **核心技巧**：一次遍历 + 连续计数（或 `groupby` 分组）  
- **适用题型**：  
  1. “连续出现 N 次” 类的题目（如找出连续出现 2 次、4 次的字符）。  
  2. “相邻相同元素归并” 的场景（如压缩字符串、日志去重）。  
  3. 需要判断子序列是否满足长度阈值的滑动窗口问题。  
- **一句话总结**：只要能一次遍历把“相邻相同”聚在一起，就能在 `O(n)` 时间内找出所有满足“连续出现 ≥ k 次”的元素。

---  

## 反思  

- **第一反应**：看到“连续三次”，马上想到“遍历计数”。  
- **最容易踩的坑**：  
  - 忽略 `id` 的顺序，导致把非相邻的相同数字误认为连续。  
  - 只记录第一次出现的 3 次，忘记把后面再出现的同一数字继续加入结果（使用 `set` 可以避免重复）。  
  - 空表或只有少于 3 条记录的情况需要提前返回空列表。  
- **下次类似题的第一步**：确认**顺序**（通常是主键或时间戳），然后决定是手动计数还是直接用 `groupby`/滑动窗口把相邻相同的元素聚合起来。