# #175. 合并两个表 / Combine Two Tables

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/combine-two-tables/)

---

## 题目（英文原版）

**Description**

Table: Person
Table: Address
Write a solution to report the first name, last name, city, and state of each person in the Person table. If the address of a personId is not present in the Address table, report null instead.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| personId    | int     |
| lastName    | varchar |
| firstName   | varchar |
+-------------+---------+
personId is the primary key (column with unique values) for this table.
This table contains information about the ID of some persons and their first and last names.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| addressId   | int     |
| personId    | int     |
| city        | varchar |
| state       | varchar |
+-------------+---------+
addressId is the primary key (column with unique values) for this table.
Each row of this table contains information about the city and state of one person with ID = PersonId.
```

**Example 3:**

```
Input: 
Person table:
+----------+----------+-----------+
| personId | lastName | firstName |
+----------+----------+-----------+
| 1        | Wang     | Allen     |
| 2        | Alice    | Bob       |
+----------+----------+-----------+
Address table:
+-----------+----------+---------------+------------+
| addressId | personId | city          | state      |
+-----------+----------+---------------+------------+
| 1         | 2        | New York City | New York   |
| 2         | 3        | Leetcode      | California |
+-----------+----------+---------------+------------+
Output: 
+-----------+----------+---------------+----------+
| firstName | lastName | city          | state    |
+-----------+----------+---------------+----------+
| Allen     | Wang     | Null          | Null     |
| Bob       | Alice    | New York City | New York |
+-----------+----------+---------------+----------+
Explanation: 
There is no address in the address table for the personId = 1 so we return null in their city and state.
addressId = 1 contains information about the address of personId = 2.
```

---

## 题目（中文翻译）

Table: Person  
Table: Address  

编写一个查询，报告 `Person` 表中每个人的 **first name**、**last name**、**city** 和 **state**。如果某个 `personId` 在 `Address` 表中没有对应的地址，则在 `city`、`state` 列返回 `null`。返回的结果表顺序任意。结果格式参见下例。

**示例 1**  

| Column Name | Type    |
|-------------|---------|
| personId    | int     |
| lastName    | varchar |
| firstName   | varchar |
  
`personId` 是该表的主键（primary key，唯一值的列）。该表存放一些人的 ID 以及他们的姓和名。

**示例 2**  

| Column Name | Type    |
|-------------|---------|
| addressId   | int     |
| personId    | int     |
| city        | varchar |
| state       | varchar |
  
`addressId` 是该表的主键（primary key，唯一值的列）。每行记录了对应 `personId` 的城市（city）和州（state）。

**示例 3**  

**Input**  

Person table:  

| personId | lastName | firstName |
|----------|----------|-----------|
| 1        | Wang     | Allen     |
| 2        | Alice    | Bob       |

Address table:  

| addressId | personId | city          | state      |
|-----------|----------|---------------|------------|
| 1         | 2        | New York City | New York   |
| 2         | 3        | Leetcode      | California |

**Output**  

| firstName | lastName | city          | state    |
|-----------|----------|---------------|----------|
| Allen     | Wang     | Null          | Null     |
| Bob       | Alice    | New York City | New York |

**解释**  
`personId = 1` 在 `Address` 表中没有对应的地址记录，因此其 `city`、`state` 返回 `null`。  
`addressId = 1` 包含了 `personId = 2` 的地址信息。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们有两张表：

| Person | 包含 `personId、lastName、firstName` |
|--------|---------------------------------------|
| Address| 包含 `addressId、personId、city、state` |

目标是把两张表按照 `personId` 合并，只保留 **Person** 表的所有行，若对应的地址不存在则在 `city、state` 位置填 `None`（SQL 中的 `NULL`）。

最直接的办法是 **双层循环**：

1. 取出 `Person` 表的每一行 `p`。  
2. 再遍历整个 `Address` 表，找出 `address.personId == p.personId` 的那一行（如果有的话）。  
3. 把找到的地址信息（或 `None`）和 `p` 合并成结果行。

> **类比**：想象你在两本电话簿里找对应的号码。第一本是“人名簿”，第二本是“地址簿”。暴力方法就是对每个人，顺着第二本从头到尾翻，直到找到匹配的名字——显然很慢。

**为什么正确**  
因为我们对每个 `personId` 都检查了 **所有** 的地址记录，只要有匹配的就会被取到，若没有匹配则保持 `None`，恰好满足题目要求。

**复杂度分析**  
- 外层遍历 `Person` 表有 `n` 行，内层遍历 `Address` 表有 `m` 行，最坏情况每次都要把内层遍历完，所以总操作数约为 `n * m`。  
  - 用大白话说，假如有 1000 个人和 1000 条地址记录，暴力解要做 **1,000,000 次**比较！  
- 额外空间只需要存放结果列表，和输入规模无关，记作 `O(1)`（不计结果本身）。

#### 代码（Python）

```python
# ---------- 暴力解 ----------
def combine_bruteforce(person, address):
    """
    person:  List[Dict]  每个 dict 包含 'personId','lastName','firstName'
    address: List[Dict]  每个 dict 包含 'addressId','personId','city','state'
    返回 List[Dict]，每个 dict 包含 'firstName','lastName','city','state'
    """
    result = []
    for p in person:                         # 遍历每个 person
        city, state = None, None              # 默认地址为空
        for a in address:                     # 在 address 表里逐个查找
            if a['personId'] == p['personId']:
                city, state = a['city'], a['state']
                break                         # 找到后直接退出内层循环
        # 把 person 信息和地址信息合并成一行
        result.append({
            'firstName': p['firstName'],
            'lastName' : p['lastName'],
            'city'     : city,
            'state'    : state
        })
    return result
```

#### 复杂度

- **时间复杂度**：`O(n * m)`  
  - `n` 为 Person 表行数，`m` 为 Address 表行数。  
  - 大白话：如果每个人都要检查所有地址，工作量会像“人数 × 地址数”这么大。
- **空间复杂度**：`O(1)`（不计返回结果的空间）  
  - 只用了常数个额外变量 `city、state`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **内层的线性搜索**：每次找地址都要遍历整个 `Address` 表。  
我们可以把地址表先整理成 **哈希表（字典）**，让 “根据 personId 快速找地址” 变成 **O(1)** 的操作。

步骤如下：

1. **预处理**：遍历一次 `Address` 表，构建 `addr_map`：  
   `addr_map[personId] = (city, state)`。  
   - 这里的字典就像“查字典”，`personId` 是词，`(city,state)` 是页码，查找速度极快。
2. 再遍历 `Person` 表，对每个 `p`：  
   - 用 `addr_map.get(p['personId'])` 直接得到对应的地址（若不存在返回 `None`）。  
   - 合并并放入结果。

这样我们只遍历两遍表，时间从 `O(n*m)` 降到 `O(n + m)`，空间多用了一个哈希表 `O(m)`。

#### 代码（Python）

```python
# ---------- 最优解 ----------
def combine_optimal(person, address):
    """
    使用哈希表把地址表索引化，随后 O(1) 查找每个 person 的地址。
    """
    # 1️⃣ 把 address 表变成 personId -> (city, state) 的映射
    addr_map = {}
    for a in address:
        # 假设同一个 personId 只会出现一次（题目主键保证）
        addr_map[a['personId']] = (a['city'], a['state'])

    # 2️⃣ 遍历 person 表，直接在哈希表里找对应的地址
    result = []
    for p in person:
        city_state = addr_map.get(p['personId'])   # O(1) 查找
        if city_state is None:                     # 没有对应地址
            city, state = None, None
        else:
            city, state = city_state

        result.append({
            'firstName': p['firstName'],
            'lastName' : p['lastName'],
            'city'     : city,
            'state'    : state
        })
    return result
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - 先遍历一次 `Address`（`m` 次），再遍历一次 `Person`（`n` 次），每次操作都是常数时间。  
  - 与暴力解相比，工作量从“人数 × 地址数”降到了“人数 + 地址数”，大幅提升。
- **空间复杂度**：`O(m)`  
  - 需要额外的哈希表来存放所有地址信息。  
  - 大白话：如果有 1000 条地址记录，我们会额外占用大约 1000 条“记事本”来记住它们。

---

## 心得

- **核心技巧**：**哈希表（字典）** 用来实现 **快速关联查询**，即把“一对多”或“多对一”的关联转化为常数时间查找。  
- **适用的题型**  
  1. 两张表的 **左连接 / 右连接**（如 “Employees & Departments”）。  
  2. “找出出现次数为 1 的元素”之类的 **计数/映射** 题目。  
  3. “根据 ID 合并信息” 的 **数据合并** 场景。  
- **一句话总结**：**先把“被查的那张表”建成字典，再遍历“主表”，把查询时间从线性降到常数。**

## 反思

- **第一反应**：直接写两个 `for` 循环——最自然的“逐个匹配”。  
- **最容易踩的坑**  
  - 忘记处理 **没有匹配的情况**（需要返回 `None/NULL`）。  
  - 若同一个 `personId` 在 `Address` 表出现多次（本题不会），需要决定取哪一条。  
  - 在 Python 中 `None` 会被打印为 `None`，而 SQL 中是 `NULL`，要注意题目要求的展示形式。  
- **下次类似题的第一步**：先思考 **“哪张表需要频繁被查询”**，把它做成哈希表，以实现 **O(1) 查询**。这样可以快速从暴力 O(N·M) 跳到线性 O(N+M)。