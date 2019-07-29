# #511. 游戏玩法分析 I / Game Play Analysis I

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/game-play-analysis-i/)

---

## 题目（英文原版）

**Description**

Table: Activity
Write a solution to find the first login date for each player.
Return the result table in any order.
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
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+
Output: 
+-----------+-------------+
| player_id | first_login |
+-----------+-------------+
| 1         | 2016-03-01  |
| 2         | 2017-06-25  |
| 3         | 2016-03-02  |
+-----------+-------------+
```

---

## 题目（中文翻译）

**描述**  
表：Activity  
编写一个查询，找出每个玩家的首次登录日期。返回结果表，顺序任意。结果格式请参照下面的示例。

+--------------+---------+
| Column Name  | Type    |
+--------------+---------+
| player_id    | int     |
| device_id    | int     |
| event_date   | date    |
| games_played | int     |
+--------------+---------+

(`player_id`, `event_date`) 为该表的主键（primary key），即由唯一值组成的列的组合。  
该表记录了若干游戏玩家的活动情况。每一行表示某玩家在某一天使用某设备登录后，玩了 `games_played` 场游戏（可能为 0），随后登出。

**示例**  

示例 1：  

输入：  
Activity 表：  
+-----------+-----------+------------+--------------+
| player_id | device_id | event_date | games_played |
+-----------+-----------+------------+--------------+
| 1         | 2         | 2016-03-01 | 5            |
| 1         | 2         | 2016-05-02 | 6            |
| 2         | 3         | 2017-06-25 | 1            |
| 3         | 1         | 2016-03-02 | 0            |
| 3         | 4         | 2018-07-03 | 5            |
+-----------+-----------+------------+--------------+

输出：  
+-----------+-------------+
| player_id | first_login |
+-----------+-------------+
| 1         | 2016-03-01  |
| 2         | 2017-06-25  |
| 3         | 2016-03-02  |
+-----------+-------------+

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**对每一个玩家，遍历整张表，找出他出现的最早 `event_date`**。  
- **数据结构**：把表格看成一个普通的 Python `list`，每条记录是一个 `dict`（或者元组）。  
  - `list` 就像一本电话簿，顺序记下所有通话记录。  
  - `dict` 的键（`player_id`、`event_date` …）就像字典里的词条，方便取值。  
- **为什么正确**：因为题目只要求每个玩家的第一次登录日期，遍历所有记录必能找到该玩家出现的所有日期，取最小的那个自然就是第一次登录。  
- **时间/空间复杂度**：  
  - 对每个玩家都要再遍历一次整张表，外层循环 `m`（玩家数），内层循环 `n`（总记录数），最坏情况 `m≈n`，所以时间是 **O(n²)**。  
  - 只使用了几个临时变量和一个存放答案的列表，额外空间是 **O(1)**（不计答案本身）。  

#### 代码（Python）  

```python
# 假设 activity 是一张表的全部记录，格式如下：
# activity = [
#     {"player_id": 1, "device_id": 2, "event_date": "2016-03-01", "games_played": 5},
#     {"player_id": 1, "device_id": 2, "event_date": "2016-05-02", "games_played": 6},
#     {"player_id": 2, "device_id": 3, "event_date": "2017-06-25", "games_played": 1},
#     {"player_id": 3, "device_id": 1, "event_date": "2016-03-02", "games_played": 0},
#     {"player_id": 3, "device_id": 4, "event_date": "2018-07-03", "games_played": 5},
# ]

def first_login_bruteforce(activity):
    # 先把所有不同的 player_id 收集起来
    players = set(row["player_id"] for row in activity)

    result = []  # 用来保存最终的 (player_id, first_login) 对
    for pid in players:                     # 对每个玩家
        earliest = None                     # 记录当前找到的最早日期
        for row in activity:                # 再遍历整张表
            if row["player_id"] == pid:     # 只关心同一个玩家的记录
                cur_date = row["event_date"]
                # 如果还没有记录，或者当前日期更早，就更新
                if earliest is None or cur_date < earliest:
                    earliest = cur_date
        # 循环结束后，earliest 就是该玩家的第一次登录日期
        result.append({"player_id": pid, "first_login": earliest})
    return result

# 运行示例
print(first_login_bruteforce(activity))
```

#### 复杂度  
- **时间复杂度**：`O(n²)`  
  - 想象你在一个大教室里，先找出所有学生的名字（一次 O(n)），再对每个学生再走遍全教室检查他们的到达时间，最坏情况下每个人都要检查 `n` 次。  
- **空间复杂度**：`O(1)`（不计输出列表）  
  - 只用了几个临时变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看到 **瓶颈在于“每个玩家都要再遍历一次整张表”**。  
如果在 **一次遍历** 中就把每个玩家的最早日期记下来，就能把时间降到线性。  

实现思路如下：  

1. **哈希表**（Python 的 `dict`）记录每个 `player_id` 已经看到的最早 `event_date`。  
   - 哈希表就像 **查字典**：把玩家的编号当作“词”，对应的最早日期当作“页码”。  
2. 从头到尾扫描 `activity`：  
   - 若玩家不在哈希表里，说明是第一次出现，直接把当前日期存进去。  
   - 若已经存在，比较当前日期与哈希表里保存的日期，保留更早的那个。  
3. 扫描结束后，哈希表里正好是每个玩家的第一次登录日期。  

这样只需要 **一次遍历**，时间降为 `O(n)`，空间用了一个 `dict`，即 `O(k)`（`k` 为玩家数量），这在最坏情况下也等于 `O(n)`。  

#### 代码（Python）  

```python
def first_login_optimal(activity):
    """
    一遍扫描完成所有玩家的第一次登录日期。
    使用字典（哈希表）把 player_id -> earliest_date 记录下来。
    """
    first_login = {}  # player_id -> earliest event_date

    for row in activity:                         # 只遍历一次
        pid = row["player_id"]
        cur_date = row["event_date"]
        if pid not in first_login:               # 第一次见到该玩家
            first_login[pid] = cur_date
        else:
            # 已经有记录，取更早的日期
            if cur_date < first_login[pid]:
                first_login[pid] = cur_date

    # 把字典转换成题目要求的列表形式
    result = [{"player_id": pid, "first_login": date}
              for pid, date in first_login.items()]
    return result

# 运行示例
print(first_login_optimal(activity))
```

#### 复杂度  
- **时间复杂度**：`O(n)` — 只需要一次线性扫描，想象把所有记录排成一条直线，只走一遍就能把每个玩家的最早日期记下来。  
- **空间复杂度**：`O(k)`（`k` 为玩家数量） — 用一个字典存每个玩家的日期，最坏情况下玩家数等于记录数，仍是线性空间。与暴力解的 `O(1)`（不计答案）相比，空间稍多，但换来了指数级的时间提升，通常是值得的。  

---  

## 心得  

- **核心技巧**：**哈希表（字典）一次遍历求最小值**。  
- **适用的题型**：  
  1. “每个用户的第一次/最后一次登录” 这类时间戳聚合问题。  
  2. “统计每种商品的最低/最高价格”。  
  3. “在一组数据中找每个键对应的最大/最小属性”。  
- **一句话总结解题钥匙**：**把“遍历找最小”转化为“在遍历过程中实时维护最小值”。**  

## 反思  

- **第一反应**：看到“每个玩家的第一次登录”，立刻想到“对每个玩家找最小日期”。  
- **最容易踩的坑**：  
  - **日期比较**：直接使用字符串比较在 `YYYY-MM-DD` 格式下是安全的，但如果日期格式变化，需要先转成 `datetime` 对象。  
  - **重复记录**：同一天可能有多条记录，只要取最小日期即可，不需要额外去重。  
  - **空表**：若输入为空，代码应返回空列表而不是报错。  
- **下次类似题的第一步**：先**确认聚合目标**（最小、最大、计数），再决定是否可以用 **哈希表一次遍历** 完成。这样可以快速判断是否需要优化。