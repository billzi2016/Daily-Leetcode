# #262. **行程与用户** / Trips and Users

> 难度：困难 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/trips-and-users/)

---

## 题目（英文原版）

**Description**

Table: Trips
Table: Users
The cancellation rate is computed by dividing the number of canceled (by client or driver) requests with unbanned users by the total number of requests with unbanned users on that day.
Write a solution to find the cancellation rate of requests with unbanned users (both client and driver must not be banned) each day between "2013-10-01" and "2013-10-03" with at least one trip. Round Cancellation Rate to two decimal points.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| id          | int      |
| client_id   | int      |
| driver_id   | int      |
| city_id     | int      |
| status      | enum     |
| request_at  | varchar  |     
+-------------+----------+
id is the primary key (column with unique values) for this table.
The table holds all taxi trips. Each trip has a unique id, while client_id and driver_id are foreign keys to the users_id at the Users table.
Status is an ENUM (category) type of ('completed', 'cancelled_by_driver', 'cancelled_by_client').
```

**Example 2:**

```
+-------------+----------+
| Column Name | Type     |
+-------------+----------+
| users_id    | int      |
| banned      | enum     |
| role        | enum     |
+-------------+----------+
users_id is the primary key (column with unique values) for this table.
The table holds all users. Each user has a unique users_id, and role is an ENUM type of ('client', 'driver', 'partner').
banned is an ENUM (category) type of ('Yes', 'No').
```

**Example 3:**

```
Input: 
Trips table:
+----+-----------+-----------+---------+---------------------+------------+
| id | client_id | driver_id | city_id | status              | request_at |
+----+-----------+-----------+---------+---------------------+------------+
| 1  | 1         | 10        | 1       | completed           | 2013-10-01 |
| 2  | 2         | 11        | 1       | cancelled_by_driver | 2013-10-01 |
| 3  | 3         | 12        | 6       | completed           | 2013-10-01 |
| 4  | 4         | 13        | 6       | cancelled_by_client | 2013-10-01 |
| 5  | 1         | 10        | 1       | completed           | 2013-10-02 |
| 6  | 2         | 11        | 6       | completed           | 2013-10-02 |
| 7  | 3         | 12        | 6       | completed           | 2013-10-02 |
| 8  | 2         | 12        | 12      | completed           | 2013-10-03 |
| 9  | 3         | 10        | 12      | completed           | 2013-10-03 |
| 10 | 4         | 13        | 12      | cancelled_by_driver | 2013-10-03 |
+----+-----------+-----------+---------+---------------------+------------+
Users table:
+----------+--------+--------+
| users_id | banned | role   |
+----------+--------+--------+
| 1        | No     | client |
| 2        | Yes    | client |
| 3        | No     | client |
| 4        | No     | client |
| 10       | No     | driver |
| 11       | No     | driver |
| 12       | No     | driver |
| 13       | No     | driver |
+----------+--------+--------+
Output: 
+------------+-------------------+
| Day        | Cancellation Rate |
+------------+-------------------+
| 2013-10-01 | 0.33              |
| 2013-10-02 | 0.00              |
| 2013-10-03 | 0.50              |
+------------+-------------------+
Explanation: 
On 2013-10-01:
  - There were 4 requests in total, 2 of which were canceled.
  - However, the request with Id=2 was made by a banned client (User_Id=2), so it is ignored in the calculation.
  - Hence there are 3 unbanned requests in total, 1 of which was canceled.
  - The Cancellation Rate is (1 / 3) = 0.33
On 2013-10-02:
  - There were 3 requests in total, 0 of which were canceled.
  - The request with Id=6 was made by a banned client, so it is ignored.
  - Hence there are 2 unbanned requests in total, 0 of which were canceled.
  - The Cancellation Rate is (0 / 2) = 0.00
On 2013-10-03:
  - There were 3 requests in total, 1 of which was canceled.
  - The request with Id=8 was made by a banned client, so it is ignored.
  - Hence there are 2 unbanned request in total, 1 of which were canceled.
  - The Cancellation Rate is (1 / 2) = 0.50
```

---

## 题目（中文翻译）

表结构  
**Trips**  

| 列名 | 类型 |
|------|------|
| id | int |
| client_id | int |
| driver_id | int |
| city_id | int |
| status | enum |
| request_at | varchar |

- `id` 为 **主键 (primary key)**，保证唯一。  
- `client_id` 与 `driver_id` 为 **外键 (foreign key)**，分别关联 **Users** 表中的 `users_id`。  
- `status` 为 **枚举 (enum)** 类型，取值为 `('completed', 'cancelled_by_driver', 'cancelled_by_client')`。  

**Users**  

| 列名 | 类型 |
|------|------|
| users_id | int |
| banned | enum |
| role | enum |

- `users_id` 为 **主键 (primary key)**。  
- `role` 为 **枚举 (enum)**，取值为 `('client', 'driver', 'partner')`。  
- `banned` 为 **枚举 (enum)**，取值为 `('Yes', 'No')`，表示用户是否被 **禁用 (banned)**。  

**题目描述**  
取消率 (cancellation rate) 的计算方式为：在同一天内，**未被禁用的用户**（即乘客和司机均未被禁用）的所有 **请求 (request)** 中，被 **取消 (cancelled)**（包括司机取消 `cancelled_by_driver` 或乘客取消 `cancelled_by_client`）的请求数量除以该天所有未被禁用的请求总数。

请计算 **2013-10-01** 至 **2013-10-03**（包含）之间，每天至少有一次行程的 **未被禁用用户的请求** 的取消率，并将取消率保留两位小数。结果可以任意顺序返回。

**示例**  

输入  

Trips 表：

| id | client_id | driver_id | city_id | status              | request_at |
|----|-----------|-----------|---------|---------------------|------------|
| 1  | 1         | 10        | 1       | completed           | 2013-10-01 |
| 2  | 2         | 11        | 1       | cancelled_by_driver | 2013-10-01 |
| 3  | 3         | 12        | 6       | completed           | 2013-10-01 |
| 4  | 4         | 13        | 6       | cancelled_by_client | 2013-10-01 |
| 5  | 1         | 10        | 1       | completed           | 2013-10-02 |
| 6  | 2         | 11        | 6       | completed           | 2013-10-02 |
| 7  | 3         | 12        | 6       | completed           | 2013-10-02 |
| 8  | 2         | 12        | 12      | completed           | 2013-10-03 |
| 9  | 3         | 10        | 12      | completed           | 2013-10-03 |
| 10 | 4         | 13        | 12      | cancelled_by_driver | 2013-10-03 |

Users 表：

| users_id | banned | role   |
|----------|--------|--------|
| 1        | No     | client |
| 2        | Yes    | client |
| 3        | No     | client |
| 4        | No     | client |
| 10       | No     | driver |
| 11       | No     | driver |
| 12       | No     | driver |
| 13       | No     | driver |

输出  

| Day        | Cancellation Rate |
|------------|--------------------|
| 2013-10-01 | 0.33               |
| 2013-10-02 | 0.00               |
| 2013-10-03 | 0.50               |

**解释**  

- **2013-10-01**：共有 4 条请求，其中 2 条被取消。但 Id=2 的请求的乘客 (client) 被禁用 (banned)，因此不计入。未被禁用的请求总数为 3 条，取消 1 条，取消率为 `1 / 3 = 0.33`。  
- **2013-10-02**：共有 3 条请求，全部完成。Id=6 的请求的乘客被禁用，故排除。未被禁用的请求为 2 条，取消为 0，取消率为 `0 / 2 = 0.00`。  
- **2013-10-03**：共有 3 条请求，1 条被取消。Id=8 的请求的乘客被禁用，排除。未被禁用的请求为 2 条，取消 1 条，取消率为 `1 / 2 = 0.50`。  

**约束条件**  
无。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的办法就是把 **Trips** 表和 **Users** 表全部读进来，逐条遍历每一条行程记录：  

1. 根据 `client_id` 在 **Users** 表里找出对应的用户记录，判断 `banned` 是否为 `'No'`。  
2. 同理，再根据 `driver_id` 找出司机记录，判断 `banned` 是否为 `'No'`。  
3. 只有当**客户端和司机都未被封禁**时，这条请求才算进“未封禁请求”。  
4. 再看 `status` 是否是 `'cancelled_by_driver'` 或 `'cancelled_by_client'`，如果是就算作**取消**。  
5. 用一个字典 `day → [total, cancelled]` 累计每一天的请求总数和取消数。  
6. 最后遍历字典，算出 `cancellation_rate = cancelled / total`（保留两位小数），只保留日期在 **2013‑10‑01~2013‑10‑03** 且 `total > 0` 的记录。  

> **类比**：  
> - **哈希表**（Python 的 `dict`）就像一本电话簿，`key` 是日期，`value` 是这天的计数。  
> - **遍历** 每一条记录相当于在街上逐家逐户检查，慢但最容易理解。  

这个办法之所以 **正确**，是因为我们没有遗漏任何一条符合条件的记录：所有的过滤、计数都在代码里一步步实现，和题目描述的计算过程一模一样。  

#### 代码（Python）  

```python
import pandas as pd
from typing import List, Tuple

def cancellation_rate_bruteforce(trips: pd.DataFrame,
                                 users: pd.DataFrame) -> pd.DataFrame:
    """
    暴力实现：逐行遍历 Trips，手动关联 Users，统计每天的取消率。
    参数
    ----
    trips: 包含 id, client_id, driver_id, status, request_at 的 DataFrame
    users: 包含 users_id, banned, role 的 DataFrame
    返回
    ----
    DataFrame，列为 Day、Cancellation Rate（保留两位小数）
    """
    # 先把 Users 按 id 建成字典，查找 O(1)
    user_banned = dict(zip(users['users_id'], users['banned']))   # {id: 'Yes'/'No'}

    # 用字典记录每天的[总请求数, 取消数]
    day_stats = {}   # type: dict[str, List[int]]

    for _, row in trips.iterrows():
        day = row['request_at']
        # 只关注 2013-10-01 ~ 2013-10-03
        if day < '2013-10-01' or day > '2013-10-03':
            continue

        client_id = row['client_id']
        driver_id = row['driver_id']

        # 若客户端或司机在 Users 表里找不到，直接跳过（数据不完整的情况）
        if client_id not in user_banned or driver_id not in user_banned:
            continue

        # 两者必须都未被封禁
        if user_banned[client_id] != 'No' or user_banned[driver_id] != 'No':
            continue

        # 记录这一天的总请求数
        if day not in day_stats:
            day_stats[day] = [0, 0]   # [total, cancelled]
        day_stats[day][0] += 1

        # 判断是否为取消请求
        if row['status'] in ('cancelled_by_driver', 'cancelled_by_client'):
            day_stats[day][1] += 1

    # 把统计结果转成 DataFrame，保留两位小数
    result_rows = []
    for day, (total, cancelled) in sorted(day_stats.items()):
        if total == 0:   # 题目要求“至少有一次行程”的天才保留
            continue
        rate = round(cancelled / total + 1e-9, 2)   # +1e-9 防止 0.335... 四舍五入误差
        result_rows.append({'Day': day, 'Cancellation Rate': f"{rate:.2f}"})

    return pd.DataFrame(result_rows)

# ----------------------------------------------------------------------
# 以下是示例数据的构造（可以直接运行验证）
if __name__ == "__main__":
    trips_data = [
        [1, 1, 10, 1, 'completed', '2013-10-01'],
        [2, 2, 11, 1, 'cancelled_by_driver', '2013-10-01'],
        [3, 3, 12, 6, 'completed', '2013-10-01'],
        [4, 4, 13, 6, 'cancelled_by_client', '2013-10-01'],
        [5, 1, 10, 1, 'completed', '2013-10-02'],
        [6, 2, 11, 6, 'completed', '2013-10-02'],
        [7, 3, 12, 6, 'completed', '2013-10-02'],
        [8, 2, 12, 12, 'completed', '2013-10-03'],
        [9, 3, 10, 12, 'completed', '2013-10-03'],
        [10, 4, 13, 12, 'cancelled_by_driver', '2013-10-03'],
    ]
    users_data = [
        [1, 'No', 'client'],
        [2, 'Yes', 'client'],
        [3, 'No', 'client'],
        [4, 'No', 'client'],
        [10, 'No', 'driver'],
        [11, 'No', 'driver'],
        [12, 'No', 'driver'],
        [13, 'No', 'driver'],
    ]
    trips_df = pd.DataFrame(trips_data,
                            columns=['id', 'client_id', 'driver_id', 'city_id',
                                     'status', 'request_at'])
    users_df = pd.DataFrame(users_data,
                            columns=['users_id', 'banned', 'role'])

    print(cancellation_rate_bruteforce(trips_df, users_df))
```

#### 复杂度  

- **时间复杂度**：`O(T + U)`  
  - `T` 为 Trips 表的行数，`U` 为 Users 表的行数。我们遍历一次 Trips（每条记录做 O(1) 的字典查找），再遍历一次 Users 建字典。  
  - 用大白话说，就是 **“跟表的大小成正比”**，如果表有 10 万行，就需要大约 10 万次操作。  

- **空间复杂度**：`O(U + D)`  
  - `U` 用来存放用户的 `id → banned` 哈希表。  
  - `D` 为我们统计的天数（本题最多 3 天），几乎可以忽略不计。  

---

### 2. 最优解  

#### 思路  

在 **SQL** 场景下，直接让数据库帮我们完成“关联、过滤、分组、聚合”是最高效的做法。  
把暴力解的 **瓶颈** 拆开来看：

| 步骤 | 暴力解的做法 | 瓶颈所在 |
|------|--------------|----------|
| 关联用户 | 手动在 Python 中一次一次 `dict` 查找 | 仍然是 O(T) 但代码层面要自己写循环 |
| 过滤封禁 | 在遍历时每条判断 | 与关联一起，仍然是线性遍历 |
| 按日期统计 | 用 `dict` 手动累计 | 需要自行维护键值对 |
| 计算比例 | Python 中再算一次 | 额外的遍历 |

如果把 **关联、过滤、分组** 的工作交给数据库，它会一次性在磁盘/内存上完成 **“JOIN + WHERE + GROUP BY”**，只需要一次扫描（内部可能使用哈希连接或排序合并），时间上通常快几个数量级。

**核心算法**：  
1. **INNER JOIN** 把 Trips 与 Users（两次，一次对应 client，一次对应 driver）连接起来，只保留 `banned = 'No'` 的记录。  
2. 用 **WHERE** 把日期限定在 `'2013-10-01'` ~ `'2013-10-03'`。  
3. 用 **GROUP BY request_at** 把同一天的记录聚合。  
4. 使用 **SUM(CASE …)** 统计当天的 **总请求数** 与 **取消请求数**。  
5. 最后算 `cancelled / total`，并用 `ROUND(..., 2)` 保留两位小数。  

> **类比**：  
> - 把 **JOIN** 想成把两本电话簿摞在一起，只保留同时出现的号码（未封禁的用户）。  
> - **GROUP BY** 像是把同一天的订单排成一行，交给统计员一次性算总数和取消数。  

下面给出 **Python** 代码（利用 `pandas`）来模拟“一条 SQL 语句”，因为 `pandas` 在内部已经实现了高效的向量化 Join 与 GroupBy，和数据库的执行计划思路相同。

#### 代码（Python）  

```python
import pandas as pd

def cancellation_rate_optimal(trips: pd.DataFrame,
                              users: pd.DataFrame) -> pd.DataFrame:
    """
    最优实现：一次性完成 JOIN、过滤、分组、聚合。
    思路与 SQL 完全等价，只是用 pandas 表达。
    """
    # 1️⃣ 把 Users 按角色分别取出，方便后面关联
    clients = users[users['role'] == 'client'][['users_id', 'banned']]
    drivers = users[users['role'] == 'driver'][['users_id', 'banned']]

    # 2️⃣ 关联 client
    merged = trips.merge(clients,
                         left_on='client_id',
                         right_on='users_id',
                         how='inner',
                         suffixes=('', '_client'))
    merged.drop(columns='users_id', inplace=True)   # 删除多余列

    # 3️⃣ 再关联 driver
    merged = merged.merge(drivers,
                          left_on='driver_id',
                          right_on='users_id',
                          how='inner',
                          suffixes=('', '_driver'))
    merged.drop(columns='users_id', inplace=True)

    # 4️⃣ 只保留两边都未被封禁的记录
    merged = merged[(merged['banned'] == 'No') & (merged['banned_driver'] == 'No')]

    # 5️⃣ 限定日期范围
    merged = merged[(merged['request_at'] >= '2013-10-01') &
                    (merged['request_at'] <= '2013-10-03')]

    # 6️⃣ 计算当天的总请求数和取消请求数
    agg = merged.groupby('request_at').apply(
        lambda df: pd.Series({
            'total': len(df),
            'cancelled': (df['status'].isin(
                ['cancelled_by_driver', 'cancelled_by_client'])).sum()
        })
    ).reset_index()

    # 7️⃣ 计算取消率，保留两位小数（字符串形式便于展示）
    agg['Cancellation Rate'] = (
        agg['cancelled'] / agg['total']
    ).apply(lambda x: f"{round(x + 1e-9, 2):.2f}")

    # 8️⃣ 按要求返回列名
    result = agg.rename(columns={'request_at': 'Day'})[['Day', 'Cancellation Rate']]
    return result

# ----------------------------------------------------------------------
# 示例运行（与上面暴力实现使用相同的示例数据）
if __name__ == "__main__":
    # 与前面相同的示例数据
    trips_df = pd.DataFrame([
        [1, 1, 10, 1, 'completed', '2013-10-01'],
        [2, 2, 11, 1, 'cancelled_by_driver', '2013-10-01'],
        [3, 3, 12, 6, 'completed', '2013-10-01'],
        [4, 4, 13, 6, 'cancelled_by_client', '2013-10-01'],
        [5, 1, 10, 1, 'completed', '2013-10-02'],
        [6, 2, 11, 6, 'completed', '2013-10-02'],
        [7, 3, 12, 6, 'completed', '2013-10-02'],
        [8, 2, 12, 12, 'completed', '2013-10-03'],
        [9, 3, 10, 12, 'completed', '2013-10-03'],
        [10, 4, 13, 12, 'cancelled_by_driver', '2013-10-03'],
    ], columns=['id', 'client_id', 'driver_id', 'city_id',
                'status', 'request_at'])
    users_df = pd.DataFrame([
        [1, 'No', 'client'],
        [2, 'Yes', 'client'],
        [3, 'No', 'client'],
        [4, 'No', 'client'],
        [10, 'No', 'driver'],
        [11, 'No', 'driver'],
        [12, 'No', 'driver'],
        [13, 'No', 'driver'],
    ], columns=['users_id', 'banned', 'role'])

    print(cancellation_rate_optimal(trips_df, users_df))
```

#### 复杂度  

- **时间复杂度**：`O(T log T + U log U)`（在最坏情况下，`pandas` 的 `merge` 需要对两个表进行排序或构建哈希表）。  
  - 实际上对等值 `JOIN`，`pandas` 会使用 **哈希连接**，时间近似 **线性** `O(T + U)`，和数据库的执行计划相同。  
  - 用大白话讲，就是 **“只要把两张表各扫描一次”**，比手动逐条判断要快很多。  

- **空间复杂度**：`O(T + U)`  
  - 需要额外的临时表来保存 `JOIN` 后的结果以及 `GROUP BY` 的聚合中间数据。  

相较于暴力解，**时间上只需要一次大规模的向量化操作**，而不是在 Python 循环里一次一次判断，速度提升显著。  

---

## 心得  

- **核心技巧**：利用 **JOIN + 条件过滤 + GROUP BY + CASE 聚合** 一次性完成多表关联、筛选以及分组统计。  
- **适用场景**  
  1. 需要在两张（或多张）表之间根据外键关联并只保留满足某些属性的记录。  
  2. 统计某个时间维度（天、月、年）上的比例、均值、计数等聚合指标。  
  3. 类似题目：  
     - “每日活跃用户数（DAU）”  
     - “每月订单取消率”  
- **一句话总结**：**把所有过滤、关联、聚合一次性交给数据库/向量化库，别在代码里写层层循环**。  

---

## 反思  

- **第一反应**：看到“取消率 = 取消数 / 未封禁请求数”，第一步就想到 **把 Trips 与 Users 关联**，然后 **按日期分组统计**。  
- **最容易踩的坑**  
  1. **双向封禁检查**：既要检查客户端也要检查司机是否被封禁，漏掉任意一方都会导致统计错误。  
  2. **日期范围**：必须严格限定在 `'2013-10-01'` 到 `'2013-10-03'`，否则会出现多余的行。  
  3. **除零错误**：如果某天全部请求都被过滤掉（总数为 0），不能直接除以 0，题目要求只保留“至少有一次行程”的天。  
  4. **四舍五入**：`ROUND(..., 2)` 在某些语言里会出现 0.335 → 0.33 的细微误差，需要加上极小的偏移或使用 Decimal。  
- **下次遇到同类题**：第一步先 **画出关联图**（Trip ↔ Client、Trip ↔ Driver），明确 **过滤条件**（both not banned），再 **决定使用一次性聚合**（SQL / pandas）还是逐行遍历（仅在数据极小或不允许使用 SQL 时）。  

祝你在数据库题目中玩得开心，逐步掌握“把计算交给机器”的思路！