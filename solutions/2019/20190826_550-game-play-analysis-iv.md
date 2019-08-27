# #550. Game Play Analysis IV / Game Play Analysis IV

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/game-play-analysis-iv/)

---

## 题目（英文原版）

**Description**

Table: Activity
Write a solution to report the fraction of players that logged in again on the day after the day they first logged in, rounded to 2 decimal places. In other words, you need to determine the number of players who logged in on the day immediately following their initial login, and divide it by the number of total players.
The result format is in the following example.

**Examples**

**Example 1:**

```
+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+
(player_id, event_date) is the primary key (combination of columns with unique values) of this table.
This table shows the activity of players of some games.
Each row is a record of a player who logged in and played a number of games (possibly 0) before logging out on someday using some device.
```

**Example 2:**

```
Input: 
Activity table:
+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-03-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+
Output: 
+-----------+
| fraction  |
+-----------+
| 0.33      |
+-----------+
Explanation: 
Only the player with id 1 logged back in after the first day he had logged in so the answer is 1/3 = 0.33
```

---

## 题目（中文翻译）

**表：Activity**  

编写一个查询，报告在玩家首次登录的次日再次登录的比例，保留两位小数。换句话说，需要统计在首次登录后的第二天（即第一次登录的次日）仍然登录的玩家数量，并除以玩家总数。  

结果格式参照下面的示例。

**示例 1**  

| Column Name  | Type |
|--------------|------|
| player_id    | int  |
| device_id    | int  |
| event_date   | date |
| games_played | int  |

`(player_id, event_date)` 是该表的**主键**（primary key），即由唯一值组合而成的键。  

该表显示了一些游戏的玩家**活动**（activity）。  
每行记录了某个玩家在某一天使用某个设备登录后玩了若干游戏（可能为 0），随后登出。

**示例 2**  

**输入**  

Activity 表：

| player_id | device_id | event_date | games_played |
|-----------|-----------|------------|--------------|
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-03-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |

**输出**  

| fraction |
|----------|
| 0.33     |

**解释**  
只有玩家 ID 为 1 的玩家在首次登录后的次日再次登录，因此答案为 1/3 = 0.33。  

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每个玩家逐个检查**。  
1. 先把所有记录按照 `player_id` 分组。  
2. 对每个玩家，遍历他的所有登录日期，找出 **最早的那一天**（这就是 “first login”）。  
3. 再遍历一次该玩家的记录，看看是否有 **恰好是第一天的下一天**（`first_date + 1 天`）的登录记录。  
4. 把满足条件的玩家计数，最后除以玩家总数得到所求的比例。

这里用到的关键数据结构是 **列表 + 嵌套循环**，可以把它想象成 **“在一堆纸条里找同一个人的最早日期，再在另一堆纸条里找是否有紧随其后的那天”**。  

> 为什么正确  
> - 我们对每个玩家都找到了最早的登录日。  
> - 再检查是否存在恰好是这一天的次日的登录记录，符合题目 “在首次登录的第二天再次登录” 的定义。  
> - 最后把满足条件的玩家数除以所有玩家数，正是题目要求的分数。

> 时间/空间复杂度大白话  
> - **时间复杂度 O(n²)**：假设有 `n` 条记录，外层遍历每个玩家，内层又要遍历该玩家的所有记录来找最早日期和次日登录。最坏情况下每条记录都要被遍历多次，像是 **“两次循环”**，所以说是二次方。  
> - **空间复杂度 O(1)**（不计输入本身）：只用了几个计数器和临时变量，额外占用的空间几乎可以忽略不计。

#### 代码（Python）  

```python
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict

# -------------------------------------------------
# 这里的 activity_data 用列表模拟数据库表，每条记录是一个 dict
# -------------------------------------------------
def fraction_bruteforce(activity_data: List[Dict]) -> float:
    # 1️⃣ 按玩家分组，得到每个玩家的所有登录日期
    logs_by_player = defaultdict(list)          # player_id -> [date1, date2, ...]
    for row in activity_data:
        pid = row["player_id"]
        # 把字符串日期转成 datetime，方便后面比较和加一天
        logs_by_player[pid].append(datetime.strptime(row["event_date"], "%Y-%m-%d"))

    total_players = len(logs_by_player)          # 所有玩家数量
    players_next_day = 0                         # 符合“第二天登录”条件的玩家数量

    # 2️⃣ 对每个玩家做两层遍历（暴力）
    for pid, dates in logs_by_player.items():
        # 找出最早的登录日期
        first_day = min(dates)                   # O(k)  k 为该玩家的登录次数
        # 检查是否有恰好是 first_day 的次日的记录
        next_day = first_day + timedelta(days=1)
        # 这里再遍历一次 dates，等价于 O(k) 的第二层循环
        for d in dates:
            if d == next_day:
                players_next_day += 1
                break                           # 找到一次就可以退出本玩家的循环

    # 3️⃣ 计算比例，保留两位小数
    if total_players == 0:
        return 0.0
    return round(players_next_day / total_players, 2)


# ------------------- 示例 -------------------
if __name__ == "__main__":
    activity = [
        {"player_id": 1, "device_id": 2, "event_date": "2016-03-01", "games_played": 5},
        {"player_id": 1, "device_id": 2, "event_date": "2016-03-02", "games_played": 6},
        {"player_id": 2, "device_id": 3, "event_date": "2017-06-25", "games_played": 1},
        {"player_id": 3, "device_id": 1, "event_date": "2016-03-02", "games_played": 0},
        {"player_id": 3, "device_id": 4, "event_date": "2018-07-03", "games_played": 5},
    ]
    print(fraction_bruteforce(activity))   # 输出 0.33
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：`n` 为总记录数。对每个玩家都要遍历一次找最早日期，再遍历一次检查次日登录，最坏情况相当于两层循环，所需时间随记录数的平方增长。  
- **空间复杂度**：`O(1)`（不计输入）  
  - 解释：只用了几个计数器和临时变量，额外占用的内存基本不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于两次遍历同一个玩家的登录记录。我们可以把“是否出现次日登录”这一步 **提前准备好**，这样只需要一次遍历即可完成全部统计。  

关键思路：

1. **把每条记录的 (player_id, event_date) 记进一个集合**。  
   - 集合在 Python 中相当于 **哈希表**，就像查字典一样，`O(1)` 时间可以判断“某个玩家在某天是否登录”。  
2. **再遍历一次所有记录，求出每个玩家的首次登录日期**（只要保留最小的日期即可）。  
3. 对每个玩家的首次登录日 `first_day`，检查集合中是否存在 `(player_id, first_day + 1 天)`。如果存在，就说明该玩家在第二天又登录了。  

这样只需要 **两次线性扫描**，时间从 `O(n²)` 降到 `O(n)`，空间多用了一个集合 `O(n)` 来存储所有 (player, date) 对。

> 核心算法/数据结构解释  
> - **哈希表（字典 / set）**：像是 **“快速查字典”**，键是 `(player_id, date)`，查找是否存在只需要常数时间。  
> - **日期运算**：使用 `datetime` 把字符串转成日期对象，再加 `timedelta(days=1)` 得到次日。  

#### 代码（Python）  

```python
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict

def fraction_optimal(activity_data: List[Dict]) -> float:
    # 1️⃣ 把所有 (player_id, event_date) 放进集合，方便 O(1) 判断是否登录
    login_set = set()
    for row in activity_data:
        pid = row["player_id"]
        date_obj = datetime.strptime(row["event_date"], "%Y-%m-%d")
        login_set.add((pid, date_obj))

    # 2️⃣ 记录每个玩家的首次登录日期（取最小值）
    first_login = dict()          # player_id -> first_date
    for pid, date_obj in login_set:
        # 如果还没出现过，直接记录；否则取更早的日期
        if pid not in first_login or date_obj < first_login[pid]:
            first_login[pid] = date_obj

    total_players = len(first_login)
    players_next_day = 0

    # 3️⃣ 检查每个玩家的首次登录的次日是否也在集合里
    for pid, first_day in first_login.items():
        if (pid, first_day + timedelta(days=1)) in login_set:
            players_next_day += 1

    if total_players == 0:
        return 0.0
    return round(players_next_day / total_players, 2)


# ------------------- 示例 -------------------
if __name__ == "__main__":
    activity = [
        {"player_id": 1, "device_id": 2, "event_date": "2016-03-01", "games_played": 5},
        {"player_id": 1, "device_id": 2, "event_date": "2016-03-02", "games_played": 6},
        {"player_id": 2, "device_id": 3, "event_date": "2017-06-25", "games_played": 1},
        {"player_id": 3, "device_id": 1, "event_date": "2016-03-02", "games_played": 0},
        {"player_id": 3, "device_id": 4, "event_date": "2018-07-03", "games_played": 5},
    ]
    print(fraction_optimal(activity))   # 输出 0.33
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：我们只遍历了三遍（一次构建集合、一次找首次登录、一次检查次日登录），每遍都是线性时间，整体随记录数线性增长。相比暴力的二次方，这就像 **“跑直线”** 而不是 **“在正方形里来回跑”**。  
- **空间复杂度**：`O(n)`  
  - 解释：需要额外存放所有 `(player_id, date)` 对的集合以及每个玩家的首次登录日期，这些都和输入规模成正比。  

---

## 心得  

- **核心技巧**：利用 **哈希表（集合）** 实现 **快速存在性判断**，配合一次遍历找最小值。  
- **适用的题型**  
  1. “某用户的第一次/最后一次行为后，是否有特定的后续行为”——如 **“首次购买后是否再次购买”**。  
  2. “连续登录天数” 类问题，需要判断日期之间是否相差 1 天。  
  3. “某事件的相邻记录是否满足条件”，如 **“订单创建后第二天是否发货”**。  
- **一句话总结解题钥匙**：**先把所有可能的查询结果预先存进哈希表，再用 O(1) 的查表代替重复遍历**。

---

## 反思  

- **第一反应**：把数据按玩家分组，手动遍历每个玩家的日志寻找第一天和次日登录——这就是暴力思路。  
- **最容易踩的坑**  
  - **日期相加**：直接把字符串拼接会出错，需要把日期转成 `datetime` 再加 `timedelta`。  
  - **重复计数**：同一个玩家可能在次日登录多次，只计一次即可，记得 `break` 或者只判断是否存在。  
  - **除零错误**：如果表为空，玩家总数为 0，需要防止除以 0。  
- **下次类似题**：**先把“是否出现”这类查询抽象成集合/字典**，然后只遍历一次或两次即可得到答案。这样既能保证正确性，又能把时间复杂度降到线性。