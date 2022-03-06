# #1693. 每日潜在客户和合作伙伴 / Daily Leads and Partners

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/daily-leads-and-partners/)

---

## 题目（英文原版）

**Description**

Table: DailySales
For each date_id and make_name, find the number of distinct lead_id's and distinct partner_id's.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| date_id     | date    |
| make_name   | varchar |
| lead_id     | int     |
| partner_id  | int     |
+-------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
This table contains the date and the name of the product sold and the IDs of the lead and partner it was sold to.
The name consists of only lowercase English letters.
```

**Example 2:**

```
Input: 
DailySales table:
+-----------+-----------+---------+------------+
| date_id   | make_name | lead_id | partner_id |
+-----------+-----------+---------+------------+
| 2020-12-8 | toyota    | 0       | 1          |
| 2020-12-8 | toyota    | 1       | 0          |
| 2020-12-8 | toyota    | 1       | 2          |
| 2020-12-7 | toyota    | 0       | 2          |
| 2020-12-7 | toyota    | 0       | 1          |
| 2020-12-8 | honda     | 1       | 2          |
| 2020-12-8 | honda     | 2       | 1          |
| 2020-12-7 | honda     | 0       | 1          |
| 2020-12-7 | honda     | 1       | 2          |
| 2020-12-7 | honda     | 2       | 1          |
+-----------+-----------+---------+------------+
Output: 
+-----------+-----------+--------------+-----------------+
| date_id   | make_name | unique_leads | unique_partners |
+-----------+-----------+--------------+-----------------+
| 2020-12-8 | toyota    | 2            | 3               |
| 2020-12-7 | toyota    | 1            | 2               |
| 2020-12-8 | honda     | 2            | 2               |
| 2020-12-7 | honda     | 3            | 2               |
+-----------+-----------+--------------+-----------------+
Explanation: 
For 2020-12-8, toyota gets leads = [0, 1] and partners = [0, 1, 2] while honda gets leads = [1, 2] and partners = [1, 2].
For 2020-12-7, toyota gets leads = [0] and partners = [1, 2] while honda gets leads = [0, 1, 2] and partners = [1, 2].
```

---

## 题目（中文翻译）

**描述**  
表：`DailySales`  
对于每一对 `date_id`（日期）和 `make_name`（产品名称），统计不同的 `lead_id`（潜在客户 ID）数量和不同的 `partner_id`（合作伙伴 ID）数量。  
返回结果表，行的顺序不限。结果格式参考下方示例。

**表结构**  

| Column Name | Type    |
|-------------|---------|
| date_id     | date    |
| make_name   | varchar |
| lead_id     | int     |
| partner_id  | int     |

该表没有主键（唯一值列），可能包含重复记录。每条记录记录了某一天某个产品的销售，以及对应的潜在客户 ID 和合作伙伴 ID。

**示例**  

输入：`DailySales` 表  

| date_id   | make_name | lead_id | partner_id |
|-----------|-----------|---------|------------|
| 2020-12-8 | toyota    | 0       | 1          |
| 2020-12-8 | toyota    | 1       | 0          |
| 2020-12-8 | toyota    | 1       | 2          |
| 2020-12-7 | toyota    | 0       | 2          |
| 2020-12-7 | toyota    | 0       | 1          |
| 2020-12-7 | toyota    | 1       | 1          |

输出  

| date_id   | make_name | lead_count | partner_count |
|-----------|-----------|------------|---------------|
| 2020-12-8 | toyota    | 2          | 3             |
| 2020-12-7 | toyota    | 2          | 2             |

**解释**  
- 对于 `2020-12-8` 的 `toyota`，`lead_id` 的不同取值为 {0, 1}，因此 `lead_count = 2`；`partner_id` 的不同取值为 {0, 1, 2}，因此 `partner_count = 3`。  
- 对于 `2020-12-7` 的 `toyota`，`lead_id` 的不同取值为 {0, 1}，`lead_count = 2`；`partner_id` 的不同取值为 {1, 2}，`partner_count = 2`。  

**约束条件**  
- 表中记录数不超过 10^5。  
- `date_id`、`make_name`、`lead_id`、`partner_id` 均可能出现重复。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一行都去和其它所有行比较**，看它们是否属于同一个 `(date_id, make_name)` 组合，如果是，就把对应的 `lead_id`、`partner_id` 放进一个集合（集合会自动去重）。  

- **数据结构**  
  - **集合（set）**：类似生活中的“收集卡片”。同一种卡片放进去一次，后面再放同样的卡片也不会增加数量。这里我们用它来实现“去重”。  
  - **列表（list）**：把所有记录按顺序存起来，方便遍历。  

- **为什么正确**  
  - 两行记录如果 `date_id` 与 `make_name` 完全相同，那么它们应该算在同一个分组里。把它们的 `lead_id`、`partner_id` 加进对应的集合后，集合的大小就恰好是该分组里 **不同** 的 `lead_id`（或 `partner_id`）数量。  

- **复杂度分析（大白话）**  
  - 对每一行我们都要遍历所有其它行来判断是否同组，这相当于“挑选伙伴”时要把每个人都跟其他所有人比较一次。  
  - 时间复杂度：**O(n²)**，这里的 `n` 是表的行数。比如有 10 000 行，就要做大约 1 亿 次比较，明显会慢。  
  - 空间复杂度：**O(k)**，`k` 是不同 `(date_id, make_name)` 组合的数量（每个组合都需要保存两个集合），一般远小于 `n`。  

#### 代码（Python）  

```python
# 暴力解：两层循环 + set 去重
def daily_sales_bruteforce(rows):
    """
    rows: List[Tuple[date_id, make_name, lead_id, partner_id]]
    返回 List[Tuple[date_id, make_name, lead_cnt, partner_cnt]]
    """
    result = []                         # 最终答案
    visited = set()                     # 用来避免对同一组重复统计

    for i in range(len(rows)):
        d_i, m_i, l_i, p_i = rows[i]

        # 如果这个组合已经算过了，直接跳过
        if (d_i, m_i) in visited:
            continue

        # 初始化两个空集合，用来收集不同的 lead_id / partner_id
        lead_set = set()
        partner_set = set()

        # 与所有行比较，找出同组的记录
        for j in range(len(rows)):
            d_j, m_j, l_j, p_j = rows[j]
            if d_i == d_j and m_i == m_j:       # 同一个 (date_id, make_name)
                lead_set.add(l_j)               # 集合会自动去重
                partner_set.add(p_j)

        # 把统计好的结果保存
        result.append((d_i, m_i, len(lead_set), len(partner_set)))
        visited.add((d_i, m_i))                 # 该组已统计，后面不必再算

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 想象成“每个人都要和所有人握手”，如果有 1000 个人，总共要握手 1 000 000 次。  
- **空间复杂度**：`O(k)`（`k` 为不同 `(date_id, make_name)` 的数量）  
  - 只需要为每个分组保存两个集合，集合的大小不会超过该组的记录数。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于两层循环的“全表比较”**。我们其实不需要两层循环，只要一次遍历就能把每行直接放进对应分组的集合里。  

**核心思路**：  
1. **哈希表（字典）**：把 `(date_id, make_name)` 当作键（key），对应的值（value）是一个包含两个集合的结构，分别存放该组出现过的 `lead_id` 和 `partner_id`。  
   - 类比：字典就像一本“地址簿”，键是地址（这里是日期+品牌），值是住在那儿的人的名单（这里是两套编号集合）。  
2. **一次遍历**：读取每一行时，直接把 `lead_id` 加进对应键的 `lead_set`，把 `partner_id` 加进 `partner_set`。这样每行只处理一次。  
3. **遍历结束后**，把字典里的每个键对应的集合大小取出来，就是答案。  

**为什么快**：  
- 只需要 **一次** 把所有行塞进哈希表，时间是 `O(n)`（线性），不再有“每个人和每个人握手”的额外比较。  
- 哈希表的查找/插入在平均情况下是 `O(1)`，所以每行的处理时间是常数。  

#### 代码（Python）  

```python
from collections import defaultdict

def daily_sales_optimal(rows):
    """
    rows: List[Tuple[date_id, make_name, lead_id, partner_id]]
    返回 List[Tuple[date_id, make_name, lead_cnt, partner_cnt]]
    """
    # defaultdict 可以自动为新键创建初始值，这里我们用 (set(), set())
    groups = defaultdict(lambda: (set(), set()))   # key -> (lead_set, partner_set)

    # 只遍历一次表
    for date_id, make_name, lead_id, partner_id in rows:
        lead_set, partner_set = groups[(date_id, make_name)]
        lead_set.add(lead_id)           # 集合自动去重
        partner_set.add(partner_id)

    # 把统计结果整理成列表返回
    result = []
    for (date_id, make_name), (lead_set, partner_set) in groups.items():
        result.append((date_id, make_name, len(lead_set), len(partner_set)))

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只需要遍历一次表，想象成“把所有人一次性送进对应的房间”，每个人只走一次路。  
- **空间复杂度**：`O(k + n)`（`k` 为不同组合数）  
  - 需要保存每个组合的两个集合，最坏情况下每条记录的 `lead_id`、`partner_id` 都不同，集合总共会占 `O(n)` 的空间。  

---

## 心得  

- **核心技巧**：**哈希表 + 集合**，用来实现“一遍遍历分组并去重”。  
- **适用的题型**  
  1. “按某些字段分组，统计不同值的数量”——如 *Customer Orders* 中统计每个用户的不同商品种类数。  
  2. “统计每个分组的唯一元素集合大小”——如 *Log Events* 中统计每个 IP 的独立访问页面数。  
- **解题钥匙**：**把“分组”转化为“字典的键”，把“去重”交给集合**，一次遍历搞定。

---

## 反思  

- **第一反应**：看到“每个 (date_id, make_name) 的不同 lead_id / partner_id”，自然想到 **分组 + 去重**。  
- **最容易踩的坑**  
  - **重复记录**：同一行可能出现多次，若直接计数会把重复算进去，必须使用集合去重。  
  - **空集合**：如果某个分组只有 `lead_id` 或 `partner_id` 为 `NULL`（这里示例里没有 NULL），集合仍会记录 `None`，要注意业务需求是否要排除。  
  - **键的构造**：键必须同时包含 `date_id` 与 `make_name`，否则会把不同日期或不同品牌的记录混在一起。  
- **下次第一步**：先 **思考能否用字典把分组信息直接存下来**，如果可以，就立刻转向 O(n) 的哈希表解法，而不是先写双层循环的暴力版。