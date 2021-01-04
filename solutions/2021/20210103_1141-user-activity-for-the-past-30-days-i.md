# #1141. **过去 30 天的用户活跃度 I** / User Activity for the Past 30 Days I

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/user-activity-for-the-past-30-days-i/)

---

## 题目（英文原版）

**Description**

Table: Activity
Write a solution to find the daily active user count for a period of 30 days ending 2019-07-27 inclusively. A user was active on someday if they made at least one activity on that day.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| session_id    | int     |
| activity_date | date    |
| activity_type | enum    |
+---------------+---------+
This table may have duplicate rows.
The activity_type column is an ENUM (category) of type ('open_session', 'end_session', 'scroll_down', 'send_message').
The table shows the user activities for a social media website. 
Note that each session belongs to exactly one user.
```

**Example 2:**

```
Input: 
Activity table:
+---------+------------+---------------+---------------+
| user_id | session_id | activity_date | activity_type |
+---------+------------+---------------+---------------+
| 1       | 1          | 2019-07-20    | open_session  |
| 1       | 1          | 2019-07-20    | scroll_down   |
| 1       | 1          | 2019-07-20    | end_session   |
| 2       | 4          | 2019-07-20    | open_session  |
| 2       | 4          | 2019-07-21    | send_message  |
| 2       | 4          | 2019-07-21    | end_session   |
| 3       | 2          | 2019-07-21    | open_session  |
| 3       | 2          | 2019-07-21    | send_message  |
| 3       | 2          | 2019-07-21    | end_session   |
| 4       | 3          | 2019-06-25    | open_session  |
| 4       | 3          | 2019-06-25    | end_session   |
+---------+------------+---------------+---------------+
Output: 
+------------+--------------+ 
| day        | active_users |
+------------+--------------+ 
| 2019-07-20 | 2            |
| 2019-07-21 | 2            |
+------------+--------------+ 
Explanation: Note that we do not care about days with zero active users.
```

---

## 题目（中文翻译）

编写一个 SQL 查询，统计截至 **2019‑07‑27**（含）过去 30 天内，每一天的活跃用户数。若用户在某天至少有一次活动（activity），则视为该天活跃。

返回结果表，顺序不限。结果格式参考下例：

```
+--------------+-------------------+
| activity_date| active_user_count |
+--------------+-------------------+
| 2019-07-27   | 3                 |
| 2019-07-26   | 5                 |
| ...          | ...               |
+--------------+-------------------+
```

**表结构**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| user_id       | int     |
| session_id    | int     |
| activity_date | date    |
| activity_type | enum    |
+---------------+---------+
```

- 表中可能出现重复行。  
- `activity_type` 列是枚举（enum），取值为 `('open_session', 'end_session', 'scroll_down', 'send_message')`。  

**示例 1**

```
Activity 表:
+---------+------------+---------------+---------------+
| user_id | session_id | activity_date | activity_type |
+---------+------------+---------------+---------------+
| 1       | 1          | 2019-07-20    | open_session  |
| 1       | 1          | 2019-07-20    | scroll_down   |
| 1       | 1          | 2019-07-20    | end_session   |
| 2       | 4          | 2019-07-20    | open_session  |
| 2       | 4          | 2019-07-20    | send_message  |
| 2       | 4          | 2019-07-20    | end_session   |
| 2       | 5          | 2019-07-21    | open_session  |
| 2       | 5          | 2019-07-21    | scroll_down   |
| 2       | 5          | 2019-07-21    | end_session   |
| 3       | 6          | 2019-07-20    | open_session  |
| 3       | 6          | 2019-07-20    | scroll_down   |
| 3       | 6          | 2019-07-20    | end_session   |
+---------+------------+---------------+---------------+
```

**输出**

```
+--------------+-------------------+
| activity_date| active_user_count |
+--------------+-------------------+
| 2019-07-20   | 3                 |
| 2019-07-21   | 1                 |
+--------------+-------------------+
```

**示例 2**

```
Input:
Activity 表:
+---------+------------+---------------+---------------+
| user_id | session_id | activity_date | activity_type |
+---------+------------+---------------+---------------+
| 1       | 1          | 2019-07-20    | open_session  |
| 1       | 1          | 2019-07-20    | scroll_down   |
| 1       | 1          | 2019-07-20    | end_session   |
| 2       | 4          | 2019-07-20    | open_session  |
| 2       | 4          | 2019-07-20    | send_message  |
| 2       | 4          | 2019-07-20    | end_session   |
| 2       | 5          | 2019-07-21    | open_session  |
| 2       | 5          | 2019-07-21    | scroll_down   |
| 2       | 5          | 2019-07-21    | end_session   |
| 3       | 6          | 2019-07-20    | open_session  |
| 3       | 6          | 2019-07-20    | scroll_down   |
| 3       | 6          | 2019-07-20    | end_session   |
+---------+------------+---------------+---------------+

Output:
+--------------+-------------------+
| activity_date| active_user_count |
+--------------+-------------------+
| 2019-07-20   | 3                 |
| 2019-07-21   | 1                 |
+--------------+-------------------+
```

**约束条件**

- 无其他限制。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把每一天都单独检查一遍**，看这一天有没有用户产生记录。具体步骤如下：

1. **准备日期列表**：从 `2019‑07‑27` 往前数 30 天，得到 30 个日期（比如 `2019‑07‑27`, `2019‑07‑26`, …, `2019‑07‑‑‑`）。  
2. **逐日遍历**：对列表里的每个日期 `d`，遍历整张 `Activity` 表的所有行，找出 `activity_date == d` 的记录。  
3. **收集用户**：把这些记录里出现的 `user_id` 放进一个集合（集合像是“装不重复的盒子”，类似把字典里的单词放进抽屉，每个抽屉只能放一种单词）。集合的大小就是当天的活跃用户数。  
4. 把 `(d, count)` 加入结果列表，最后返回。

> **为什么正确**  
> 只要我们遍历了所有行并且只统计了 `activity_date` 正好是目标日期的 `user_id`，就不可能漏掉任何活跃用户，也不会把不在该日期的用户算进去。

> **复杂度直观解释**  
> - `O(N)` 表示“和记录数成正比”。如果表里有 1000 条记录，`O(N)` 大约是 1000 步。  
> - `O(N·D)` 表示“记录数乘以天数”。这里 `D = 30`，所以如果有 1000 条记录，暴力解大约要跑 30 000 步。

#### 代码（Python）

```python
from datetime import datetime, timedelta
from typing import List, Tuple, Dict

# ---------- 模拟输入 ----------
# 每条记录是一个元组 (user_id, session_id, activity_date, activity_type)
Activity = [
    # 示例数据，实际使用时请把所有行放进这个列表
    (1, 1, "2019-07-20", "open_session"),
    (1, 1, "2019-07-20", "scroll_down"),
    (2, 4, "2019-07-25", "send_message"),
    # ...
]

def brute_force(activity: List[Tuple[int, int, str, str]]) -> List[Tuple[str, int]]:
    """暴力解：对每一天都遍历整个表，统计活跃用户数"""
    # 1️⃣ 生成最近 30 天的日期字符串列表（包含结束日 2019-07-27）
    end_day = datetime.strptime("2019-07-27", "%Y-%m-%d")
    days = [(end_day - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    result = []  # 用来保存 (date, active_user_count)

    # 2️⃣ 对每一天进行一次全表扫描
    for d in days:
        users = set()                     # 集合：自动去重的“装用户的盒子”
        for row in activity:
            # row[2] 是 activity_date
            if row[2] == d:               # 只关心当天的记录
                users.add(row[0])         # row[0] 是 user_id
        result.append((d, len(users)))    # 当天活跃用户数 = 集合大小

    return result
```

#### 复杂度

- **时间复杂度**：`O(N·D)`，其中 `N` 为表中记录条数，`D = 30` 为天数。实际意义是：如果记录翻倍，运行时间也会大致翻倍，因为我们要把每条记录看 `30` 次。
- **空间复杂度**：`O(U)`，`U` 为单天最多的活跃用户数（集合里最多装多少用户）。因为我们只在每一次循环里保存当天的用户集合，额外空间与天数无关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“对每一天都全表扫描”**——同一条记录被检查了 30 次，显得很浪费。我们可以把 **“把记录按日期分组”** 这件事提前做一次，只遍历一次表，就能得到每一天的所有活跃用户。具体步骤：

1. **一次遍历收集**  
   - 用一个字典 `date_to_users`，键是日期字符串，值是一个集合（装该日期所有出现过的 `user_id`）。  
   - 对每条记录，只要把 `user_id` 加进对应日期的集合即可。相当于把“同学们排队进教室”这件事一次性完成，而不是每次都重新排队。  
2. **生成最近 30 天**：同样准备 `2019‑07‑27` 往前的 30 天列表。  
3. **取结果**：遍历这 30 天的日期列表，从 `date_to_users` 中取出对应集合的大小（如果某天根本没有记录，则默认 0）。

> **核心数据结构——字典 + 集合**  
> - **字典** 像是“装有标签的抽屉”，我们把每个日期当作标签，快速找到对应的抽屉。查找时间是 `O(1)`，也就是说不管字典里有多少天，找某一天的抽屉几乎不花时间。  
> - **集合** 像是“只能放不重复东西的盒子”，自动帮我们去掉同一天内同一个用户的多次活动。

> **时间空间直观解释**  
> - 只遍历一次表，时间随记录数线性增长（`O(N)`），不再乘以天数。  
> - 需要额外的空间来保存每一天的用户集合，最坏情况是所有用户在所有天都有活动，空间是 `O(N)`（因为每条记录只会被放进一个集合）。

#### 代码（Python）

```python
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Set

def optimal(activity: List[Tuple[int, int, str, str]]) -> List[Tuple[str, int]]:
    """最优解：一次遍历把记录按日期归类，再统计最近 30 天的活跃用户数"""
    # 1️⃣ 用字典把每一天的活跃用户收集到集合里
    date_to_users: Dict[str, Set[int]] = {}   # key: 日期, value: 当天出现过的用户集合
    for user_id, _, activity_date, _ in activity:
        if activity_date not in date_to_users:
            date_to_users[activity_date] = set()
        date_to_users[activity_date].add(user_id)   # 集合会自动去重

    # 2️⃣ 生成最近 30 天的日期列表（包括结束日 2019-07-27）
    end_day = datetime.strptime("2019-07-27", "%Y-%m-%d")
    days = [(end_day - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(30)]

    # 3️⃣ 取出每一天的活跃用户数，若当天没有记录则计为 0
    result = []
    for d in days:
        count = len(date_to_users.get(d, set()))  # .get(d, set())：若 d 不在字典里返回空集合
        result.append((d, count))

    return result
```

#### 复杂度

- **时间复杂度**：`O(N + D)`  
  - `O(N)` 用于一次遍历所有记录并放进对应集合。  
  - `O(D)`（`D = 30`）用于遍历日期列表并取集合大小。总体上随记录数线性增长，天数是常数级别的开销。  
  - 与暴力解相比，省掉了每条记录被检查 `30` 次的额外工作。

- **空间复杂度**：`O(N)`（最坏情况）  
  - 需要保存每条记录所属日期的集合。若每条记录的 `user_id` 都不同，集合里会存下所有 `N` 条记录的用户 ID。  
  - 这比暴力解的额外空间要多一些（因为暴力解只在一次循环里保存一个集合），但换来了显著的时间提升。

---

## 心得

- **核心技巧**：**一次遍历 + 按键分组（字典+集合）**。把所有需要的统计信息提前聚合，后面只做常数时间的查询。  
- **适用的类似题型**  
  1. “最近 7 天的登录用户数”  
  2. “每个月的订单用户去重计数”  
  3. “每个商品最近 N 天的购买人数”  
- **一句话总结**：**把“按日期分桶”做在遍历表的第一步，后面查询只要 O(1) 即可**。

---

## 反思

- **拿到题目第一反应**：先想“遍历 30 天，每天再遍历表”。这看起来最直接，却容易忽视重复工作。  
- **最容易踩的坑**  
  - **日期范围的边界**：结束日期必须 **包含** `2019-07-27`，而不是只到 `2019-07-26`。  
  - **重复记录**：同一用户在同一天可能出现多次，需要去重（使用集合）。  
  - **没有记录的日期**：字典里可能找不到某天，需要默认返回 0，防止 `KeyError`。  
- **下次类似题的第一步**：**先把数据按需求的维度（这里是日期）分组**，再在分组结果上做统计，这样可以一次遍历完成全部信息的收集。