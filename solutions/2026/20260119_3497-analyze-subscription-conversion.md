# #3497. 分析订阅转化 / Analyze Subscription Conversion 

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/analyze-subscription-conversion/)

---

## 题目（英文原版）

**Description**

Table: UserActivity
A subscription service wants to analyze user behavior patterns. The company offers a 7-day free trial, after which users can subscribe to a paid plan or cancel. Write a solution to:
Return the result table ordered by user_id in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+------------------+---------+
| Column Name      | Type    | 
+------------------+---------+
| user_id          | int     |
| activity_date    | date    |
| activity_type    | varchar |
| activity_duration| int     |
+------------------+---------+
(user_id, activity_date, activity_type) is the unique key for this table.
activity_type is one of ('free_trial', 'paid', 'cancelled').
activity_duration is the number of minutes the user spent on the platform that day.
Each row represents a user's activity on a specific date.
```

**Example 2:**

```
+---------+---------------+---------------+-------------------+
| user_id | activity_date | activity_type | activity_duration |
+---------+---------------+---------------+-------------------+
| 1       | 2023-01-01    | free_trial    | 45                |
| 1       | 2023-01-02    | free_trial    | 30                |
| 1       | 2023-01-05    | free_trial    | 60                |
| 1       | 2023-01-10    | paid          | 75                |
| 1       | 2023-01-12    | paid          | 90                |
| 1       | 2023-01-15    | paid          | 65                |
| 2       | 2023-02-01    | free_trial    | 55                |
| 2       | 2023-02-03    | free_trial    | 25                |
| 2       | 2023-02-07    | free_trial    | 50                |
| 2       | 2023-02-10    | cancelled     | 0                 |
| 3       | 2023-03-05    | free_trial    | 70                |
| 3       | 2023-03-06    | free_trial    | 60                |
| 3       | 2023-03-08    | free_trial    | 80                |
| 3       | 2023-03-12    | paid          | 50                |
| 3       | 2023-03-15    | paid          | 55                |
| 3       | 2023-03-20    | paid          | 85                |
| 4       | 2023-04-01    | free_trial    | 40                |
| 4       | 2023-04-03    | free_trial    | 35                |
| 4       | 2023-04-05    | paid          | 45                |
| 4       | 2023-04-07    | cancelled     | 0                 |
+---------+---------------+---------------+-------------------+
```

**Example 3:**

```
+---------+--------------------+-------------------+
| user_id | trial_avg_duration | paid_avg_duration |
+---------+--------------------+-------------------+
| 1       | 45.00              | 76.67             |
| 3       | 70.00              | 63.33             |
| 4       | 37.50              | 45.00             |
+---------+--------------------+-------------------+
```

---

## 题目（中文翻译）

**描述**  
表：`UserActivity`  

一家订阅服务希望分析用户行为模式。公司提供 7 天免费试用（free trial），试用期结束后用户可以订阅付费计划（paid）或取消（cancelled）。请编写查询，返回每个用户在免费试用期间的平均活动时长（`trial_avg_duration`）以及在付费期间的平均活动时长（`paid_avg_duration`），结果按 `user_id` 升序排列。返回结果的格式请参考下例。

**表结构**  

```sql
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| user_id      | int     |
| activity_date| date    |
| activity_type| varchar |
| activity_duration| int |
+--------------+---------+
```

- `(user_id, activity_date, activity_type)` 为该表的唯一键。  
- `activity_type` 取值为 `'free_trial'`（免费试用）、`'paid'`（付费）或 `'cancelled'`（取消）。  
- `activity_duration` 表示该活动的时长（单位：分钟）。

**示例**  

*示例 1（表结构）*  
```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| user_id      | int     |
| activity_date| date    |
| activity_type| varchar |
| activity_duration| int |
+--------------+---------+
(user_id, activity_date, activity_type) 是此表的唯一键。
activity_type 为 ('free_trial', 'paid', 'cancelled') 之一。
```

*示例 2（原始数据）*  

```
+---------+--------------+--------------+-----------------+
| user_id | activity_date| activity_type| activity_duration|
+---------+--------------+--------------+-----------------+
| 1       | 2023-01-01   | free_trial   | 45              |
| 1       | 2023-01-02   | free_trial   | 30              |
| 1       | 2023-01-05   | free_trial   | 60              |
| 1       | 2023-01-08   | paid         | 80              |
| 1       | 2023-01-09   | paid         | 70              |
| 1       | 2023-01-10   | paid         | 80              |
| 2       | 2023-01-03   | free_trial   | 50              |
| 2       | 2023-01-04   | cancelled    | 0               |
| 3       | 2023-01-02   | free_trial   | 70              |
| 3       | 2023-01-03   | paid         | 60              |
| 3       | 2023-01-04   | paid         | 65              |
| 3       | 2023-01-05   | paid         | 65              |
| 4       | 2023-01-01   | free_trial   | 35              |
| 4       | 2023-01-02   | free_trial   | 40              |
| 4       | 2023-01-03   | paid         | 45              |
| 4       | 2023-01-04   | paid         | 45              |
+---------+--------------+--------------+-----------------+
```

*示例 3（查询结果）*  

```
+---------+-------------------+-------------------+
| user_id | trial_avg_duration| paid_avg_duration |
+---------+-------------------+-------------------+
| 1       | 45.00             | 76.67             |
| 3       | 70.00             | 63.33             |
| 4       | 37.50             | 45.00             |
+---------+-------------------+-------------------+
```

**约束条件**  
暂无。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把表里的每一行都拿出来，和其它所有行进行比较，找出同一个 `user_id` 且 `activity_type` 为 **free_trial** 或 **paid** 的记录，然后把它们的 `activity_duration` 加在一起，最后除以出现的次数得到平均值。

- **数据结构**：这里用到的最基本的数据结构是 **列表**（把整张表当成一个列表的每个元素）和 **嵌套循环**。可以把列表想象成一摞纸条，每张纸条记录了某用户某天的行为。我们要把每张纸条和其余所有纸条逐一比对，就像在找同学的作业时，一个人去检查所有人的答案。
- **正确性**：因为我们把每一行都和所有可能匹配的行比较了一遍，所有属于同一用户、同一活动类型的时长都会被累计进去，除以计数后自然得到真实的平均时长。
- **时间/空间复杂度**：  
  - 时间复杂度是 **O(n²)**，因为外层循环遍历 `n` 行，内层循环对每一行又要遍历 `n` 行。  
    - **大白话**：如果有 10 条记录，就要检查 10 × 10 = 100 次；如果有 1000 条记录，就要检查 1 000 000 次，明显会慢。  
  - 空间复杂度是 **O(1)**（不计输入本身），因为我们只用了几个计数器和累加器，额外占用的内存几乎不随 `n` 增长。

#### 代码（Python）

```python
from typing import List, Tuple

def brute_average(records: List[Tuple[int, str, str, int]]) -> List[Tuple[int, float, float]]:
    """
    records: [(user_id, activity_date, activity_type, activity_duration), ...]
    返回 [(user_id, trial_avg, paid_avg), ...]，只保留同时出现 trial 与 paid 的用户
    """
    result = []
    # 先把所有 user_id 收集起来，方便后面遍历
    user_ids = sorted({r[0] for r in records})

    for uid in user_ids:
        trial_sum = trial_cnt = 0
        paid_sum  = paid_cnt  = 0

        # 暴力遍历所有行，找出属于当前 uid 的记录
        for r in records:
            if r[0] != uid:          # 不是同一个用户，直接跳过
                continue
            if r[2] == 'free_trial':
                trial_sum += r[3]
                trial_cnt += 1
            elif r[2] == 'paid':
                paid_sum += r[3]
                paid_cnt += 1

        # 只保留 trial 与 paid 都出现过的用户
        if trial_cnt > 0 and paid_cnt > 0:
            trial_avg = round(trial_sum / trial_cnt, 2)
            paid_avg  = round(paid_sum  / paid_cnt , 2)
            result.append((uid, trial_avg, paid_avg))

    return result
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环，每层都要遍历全部记录。  
  - 实际意义：记录数翻倍，运行时间会变成原来的四倍，规模稍大就会卡死。
- **空间复杂度**：`O(1)` —— 只用了若干计数器和累加变量，额外内存几乎不随 `n` 增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于每次处理一个用户时，都要把整张表重新遍历一遍。实际上，我们只需要 **一次遍历** 把每条记录归类到对应的用户与活动类型上，就能得到所有的累计时长和出现次数。

这正好可以使用 **哈希表（字典）** 来实现：

1. **一次遍历**：对每条记录  
   - 以 `user_id` 为键，在字典中建立或取出该用户的统计信息。  
   - 再根据 `activity_type`（`free_trial` 或 `paid`）把 `activity_duration` 加到对应的累计和，并把计数器 +1。  
   - 这里的字典就像一本“用户小账本”，键是用户编号，值是 `[free_sum, free_cnt, paid_sum, paid_cnt]`。
2. **遍历完后**，对字典的每个条目检查是否同时出现了 trial 与 paid（计数都大于 0），如果是就计算平均值（`sum / cnt`），并保留两位小数。  
3. **排序**：把结果按照 `user_id` 升序排列即可。

> **哈希表的类比**：想象你在图书馆查字典，字典的“词条”就是 `user_id`，而“页码”对应我们记录的累计时长和计数。查找、插入的速度都很快（常数时间），所以一次遍历就能完成所有统计。

#### 代码（Python）

```python
from typing import List, Tuple

def optimal_average(records: List[Tuple[int, str, str, int]]) -> List[Tuple[int, float, float]]:
    """
    使用哈希表一次遍历完成统计，时间 O(n)，空间 O(u)（u 为不同用户数）。
    """
    # user_stats[user_id] = [free_sum, free_cnt, paid_sum, paid_cnt]
    user_stats = {}

    for uid, _date, typ, dur in records:
        if uid not in user_stats:
            user_stats[uid] = [0, 0, 0, 0]          # 初始化四个计数器

        if typ == 'free_trial':
            user_stats[uid][0] += dur               # free_sum
            user_stats[uid][1] += 1                 # free_cnt
        elif typ == 'paid':
            user_stats[uid][2] += dur               # paid_sum
            user_stats[uid][3] += 1                 # paid_cnt
        # 'cancelled' 类型直接忽略，因为题目只要求 trial 与 paid 的平均时长

    # 生成结果列表
    result = []
    for uid in sorted(user_stats):                 # 按照 user_id 升序遍历
        free_sum, free_cnt, paid_sum, paid_cnt = user_stats[uid]
        if free_cnt > 0 and paid_cnt > 0:          # 必须两种活动都出现过
            trial_avg = round(free_sum / free_cnt, 2)
            paid_avg  = round(paid_sum / paid_cnt, 2)
            result.append((uid, trial_avg, paid_avg))

    return result
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次记录表，哈希表的插入/查询都是常数时间。  
  - 与暴力解相比，记录数翻倍只会让运行时间翻倍，而不是指数级增长，效率提升巨大。
- **空间复杂度**：`O(u)` —— 需要为每个不同的 `user_id` 保存四个整数（累计和和计数），`u` 为用户总数。  
  - 如果用户很多，空间会随之增长，但仍远小于 `O(n²)` 的时间开销。

---

## 心得

- **核心技巧**：利用哈希表（字典）一次遍历完成分组统计（求和、计数），再在遍历结束后统一计算平均值。  
- **适用的题型**  
  1. “按类别求平均/总和”——如 `Sales` 表中不同地区的销售额平均值。  
  2. “分组计数”——如统计每个产品的购买次数。  
  3. “分组聚合 + 条件筛选”——如只保留出现次数大于等于 2 的用户。  
- **一句话总结**：**“把同类数据先收进同一个小抽屉（哈希表），一次扫完再统一算”。**

---

## 反思

- **第一反应**：看到 “average … per user” 立刻想到 **GROUP BY**，于是想用字典来模拟分组。  
- **最容易踩的坑**  
  - **遗漏 `cancelled`**：题目只要求 `free_trial` 与 `paid`，如果不在遍历时过滤 `cancelled`，会把它们计入平均值，导致错误。  
  - **除零错误**：有的用户可能只有 trial 没有 paid，或只有 paid 没有 trial，计算平均前必须检查计数是否为 0。  
  - **小数位数**：输出要求保留两位小数，直接使用 `round(..., 2)` 即可，别忘了这一步。  
- **下次思路**：看到 “对每个用户做聚合” 时，第一步就先在脑中画出 **“哈希表 + 单遍扫描”** 的框架，再判断是否需要额外的过滤或排序。这样可以避免不必要的多次遍历。