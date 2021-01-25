# #1174. 即时食品配送 II / Immediate Food Delivery II

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/immediate-food-delivery-ii/)

---

## 题目（英文原版）

**Description**

Table: Delivery
If the customer's preferred delivery date is the same as the order date, then the order is called immediate; otherwise, it is called scheduled.
The first order of a customer is the order with the earliest order date that the customer made. It is guaranteed that a customer has precisely one first order.
Write a solution to find the percentage of immediate orders in the first orders of all customers, rounded to 2 decimal places.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-----------------------------+---------+
| Column Name                 | Type    |
+-----------------------------+---------+
| delivery_id                 | int     |
| customer_id                 | int     |
| order_date                  | date    |
| customer_pref_delivery_date | date    |
+-----------------------------+---------+
delivery_id is the column of unique values of this table.
The table holds information about food delivery to customers that make orders at some date and specify a preferred delivery date (on the same order date or after it).
```

**Example 2:**

```
Input: 
Delivery table:
+-------------+-------------+------------+-----------------------------+
| delivery_id | customer_id | order_date | customer_pref_delivery_date |
+-------------+-------------+------------+-----------------------------+
| 1           | 1           | 2019-08-01 | 2019-08-02                  |
| 2           | 2           | 2019-08-02 | 2019-08-02                  |
| 3           | 1           | 2019-08-11 | 2019-08-12                  |
| 4           | 3           | 2019-08-24 | 2019-08-24                  |
| 5           | 3           | 2019-08-21 | 2019-08-22                  |
| 6           | 2           | 2019-08-11 | 2019-08-13                  |
| 7           | 4           | 2019-08-09 | 2019-08-09                  |
+-------------+-------------+------------+-----------------------------+
Output: 
+----------------------+
| immediate_percentage |
+----------------------+
| 50.00                |
+----------------------+
Explanation: 
The customer id 1 has a first order with delivery id 1 and it is scheduled.
The customer id 2 has a first order with delivery id 2 and it is immediate.
The customer id 3 has a first order with delivery id 5 and it is scheduled.
The customer id 4 has a first order with delivery id 7 and it is immediate.
Hence, half the customers have immediate first orders.
```

---

## 题目（中文翻译）

表：Delivery  

如果客户的首选送达日期（customer_pref_delivery_date）与下单日期（order_date）相同，则该订单称为即时（immediate）；否则称为预约（scheduled）。  

客户的第一笔订单是该客户下的最早的订单（order_date 最小的那一条记录），题目保证每位客户恰好有一笔第一订单。  

编写 SQL 查询，统计所有客户第一笔订单中即时订单的比例，结果保留两位小数。  

结果格式参照下面的示例。

示例 1  

```sql
Delivery 表结构:
+---------------------------+--------+
| Column Name               | Type   |
+---------------------------+--------+
| delivery_id               | int    |
| customer_id               | int    |
| order_date                | date   |
| customer_pref_delivery_date | date |
+---------------------------+--------+

delivery_id 是该表唯一值的列。
```

示例 2  

输入  
```sql
Delivery 表:
+-------------+-------------+------------+-----------------------------+
| delivery_id | customer_id | order_date | customer_pref_delivery_date |
+-------------+-------------+------------+-----------------------------+
| 1           | 1           | 2019-08-01 | 2019-08-02                  |
| 2           | 2           | 2019-08-02 | 2019-08-02                  |
| 3           | 1           | 2019-08-03 | 2019-08-03                  |
| 4           | 3           | 2019-08-04 | 2019-08-04                  |
| 5           | 3           | 2019-08-05 | 2019-08-06                  |
+-------------+-------------+------------+-----------------------------+
```

输出  
```sql
+--------------------------+
| percentage_immediate     |
+--------------------------+
| 66.67                    |
+--------------------------+
```

解释  
- 客户 1 的第一笔订单是 delivery_id = 1，order_date = 2019‑08‑01，首选送达日期为 2019‑08‑02，非即时。  
- 客户 2 的第一笔订单是 delivery_id = 2，order_date = 2019‑08‑02，首选送达日期同为 2019‑08‑02，为即时。  
- 客户 3 的第一笔订单是 delivery_id = 4，order_date = 2019‑08‑04，首选送达日期同为 2019‑08‑04，为即时。  

共有 3 位客户，其中 2 位的第一笔订单是即时订单，比例为 2 / 3 = 0.6667，保留两位小数后为 **66.67**%。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  

1. **把所有记录都读进来**，放到一个列表 `records` 中。  
2. **遍历每一个顾客**（`customer_id`），把该顾客的所有订单挑出来，找出 **order_date 最早** 的那条记录，这条记录就是该顾客的 “第一单”。  
3. 判断这条第一单的 `order_date` 是否等于 `customer_pref_delivery_date`，相等的话说明是 “立即送达”。  
4. 把所有顾客的第一单中 “立即送达” 的数量除以顾客总数，得到百分比并保留两位小数。  

> **类比**：  
> 把 `customer_id` 想成一本词典里的“词”，把所有订单想成这个词的所有解释。我们要找的就是每个词的**最早**解释（最早的 order_date），再看它是不是“立刻”送达。  

**为什么正确**：  
- 题目保证每个顾客恰好有一条第一单（即最早的 order_date 唯一），所以只要我们真的找到了每个顾客的最早订单，就一定找到了第一单。  
- 只要比较 `order_date` 与 `customer_pref_delivery_date` 是否相同，就能判断是否为立即订单。  

**时间/空间复杂度**（大白话版）：  
- **时间**：我们先遍历一次把所有记录放进列表（O(N)），随后对每个不同的顾客再次遍历一次所有记录去找最早的订单（最坏情况每个顾客都要看 N 条记录），这一步是 O(N·C)，其中 C 是顾客数。最坏情况下 C≈N，故整体是 **O(N²)**，也就是“平方级”，数据多了会非常慢。  
- **空间**：我们只用一个列表存所有记录和几个计数器，额外空间是 **O(N)**（和输入规模成正比）。  

#### 代码（Python）  

```python
from typing import List, Dict
from datetime import datetime

# 假设输入是一个列表，每条记录是一个字典
# 例如：
# records = [
#     {"delivery_id": 1, "customer_id": 1, "order_date": "2019-08-01", "customer_pref_delivery_date": "2019-08-02"},
#     {"delivery_id": 2, "customer_id": 2, "order_date": "2019-08-02", "customer_pref_delivery_date": "2019-08-02"},
#     ...
# ]

def immediate_percentage_bruteforce(records: List[Dict]) -> float:
    """暴力解：对每个顾客都遍历一次全部记录，找出第一单并统计立即单比例"""
    # 1️⃣ 把所有顾客的 id 收集起来（去重）
    customers = set(r["customer_id"] for r in records)

    immediate_cnt = 0  # 立即单的数量

    # 2️⃣ 对每个顾客单独搜索最早的订单
    for cid in customers:
        earliest = None          # 保存当前找到的最早记录
        earliest_date = None     # 对应的日期（datetime 对象，方便比较）

        for r in records:        # 暴力遍历所有记录
            if r["customer_id"] != cid:
                continue        # 只关心当前顾客的记录
            # 把字符串日期转成 datetime，方便比较大小
            cur_date = datetime.strptime(r["order_date"], "%Y-%m-%d")
            if earliest_date is None or cur_date < earliest_date:
                earliest = r
                earliest_date = cur_date

        # 3️⃣ 判断这条最早的记录是否为立即送达
        if earliest["order_date"] == earliest["customer_pref_delivery_date"]:
            immediate_cnt += 1

    # 4️⃣ 计算比例，保留两位小数
    total_customers = len(customers)
    if total_customers == 0:   # 防止除以 0
        return 0.0
    ratio = immediate_cnt / total_customers * 100
    return round(ratio, 2)


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    sample = [
        {"delivery_id": 1, "customer_id": 1, "order_date": "2019-08-01", "customer_pref_delivery_date": "2019-08-02"},
        {"delivery_id": 2, "customer_id": 2, "order_date": "2019-08-02", "customer_pref_delivery_date": "2019-08-02"},
        {"delivery_id": 3, "customer_id": 1, "order_date": "2019-08-03", "customer_pref_delivery_date": "2019-08-03"},
    ]
    print(immediate_percentage_bruteforce(sample))   # 输出 50.0
```

#### 复杂度  

- **时间复杂度**：**O(N²)**  
  - 第一次遍历收集顾客集合是 O(N)。  
  - 对每个顾客再次遍历全部记录找最早订单，最坏情况是 N 次遍历 N 条记录，即 N·N。  
- **空间复杂度**：**O(N)**  
  - 需要存放所有记录的列表（输入本身），再加一个 `set` 保存所有顾客 id。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**对每个顾客都要重新遍历所有记录**。我们可以把这一步“合并”到一次遍历里完成：  

1. **一次遍历**所有记录，同时维护一个哈希表（Python 中的 `dict`），键是 `customer_id`，值是该顾客目前已知的 **最早订单**（整个记录本身或只保存必要字段）。  
2. 当遍历到一条新记录时：  
   - 如果该顾客还没有出现过，直接把这条记录设为最早订单。  
   - 如果已经有最早订单，比较 `order_date` 的大小，只保留更早的那条。  
   - 这一步类似于“在字典里查词”，`customer_id` 就是词，字典里保存的最早订单相当于“词条”。  
3. 遍历结束后，字典里恰好存放了 **每个顾客的第一单**。  
4. 再遍历字典的值，统计 `order_date == customer_pref_delivery_date` 的数量，即为立即单数。  
5. 用公式 `立即单数 / 顾客总数 * 100`，并使用 `round(..., 2)` 保留两位小数。  

**核心数据结构**：**哈希表（字典）**。  
- 查找、插入、更新的时间都是 **O(1)**（常数时间），所以一次遍历就能把所有信息整理好。  

**类比**：想象你在整理一本“顾客-最早订单”手册。每读到一条新记录，就把手册里对应的顾客页翻开：  
- 没有这页？新建一页并写上这条记录。  
- 已有这页？比较日期，写下更早的那条。  
这样读完所有订单后，手册里每页正好是该顾客的第一单，后面再检查“是否立即”就非常快。  

#### 代码（Python）  

```python
from typing import List, Dict
from datetime import datetime

def immediate_percentage_optimal(records: List[Dict]) -> float:
    """
    最优解：只遍历一次记录，利用字典保存每个顾客的第一单。
    时间 O(N) ，空间 O(C)（C 为顾客数，最坏情况下等于 N）。
    """
    first_order: Dict[int, Dict] = {}   # key: customer_id, value: 记录字典（最早的那条）

    for r in records:
        cid = r["customer_id"]
        cur_date = datetime.strptime(r["order_date"], "%Y-%m-%d")

        if cid not in first_order:
            # 第一次看到这个顾客，直接保存
            first_order[cid] = {"record": r, "date": cur_date}
        else:
            # 已有记录，比较日期，只保留更早的
            if cur_date < first_order[cid]["date"]:
                first_order[cid] = {"record": r, "date": cur_date}

    # 统计立即单
    immediate_cnt = 0
    for info in first_order.values():
        rec = info["record"]
        if rec["order_date"] == rec["customer_pref_delivery_date"]:
            immediate_cnt += 1

    total_customers = len(first_order)
    if total_customers == 0:
        return 0.0
    ratio = immediate_cnt / total_customers * 100
    return round(ratio, 2)


# ------------------- 示例运行 -------------------
if __name__ == "__main__":
    sample = [
        {"delivery_id": 1, "customer_id": 1, "order_date": "2019-08-01", "customer_pref_delivery_date": "2019-08-02"},
        {"delivery_id": 2, "customer_id": 2, "order_date": "2019-08-02", "customer_pref_delivery_date": "2019-08-02"},
        {"delivery_id": 3, "customer_id": 1, "order_date": "2019-08-03", "customer_pref_delivery_date": "2019-08-03"},
    ]
    print(immediate_percentage_optimal(sample))   # 输出 50.0
```

#### 复杂度  

- **时间复杂度**：**O(N)**  
  - 只遍历一次所有记录，每次对字典的插入/查询/更新都是常数时间。  
- **空间复杂度**：**O(C)**（C 为顾客数）  
  - 只需要为每个顾客保存一条最早的记录，最坏情况下顾客数等于记录数 N。  

---  

## 心得  

- **核心技巧**：**一次遍历 + 哈希表**（字典）实现“分组后取极值”。  
- **适用场景**：  
  1. “每个用户的第一次登录时间” → 统计最早 `login_time`。  
  2. “每个商品的最低售价” → 在大批价格记录中取每个商品的最小 `price`。  
  3. “每个学生的最高成绩” → 类似的取最大值，只需把比较符号改成 `>`。  
- **一句话总结**：**把“找每组最早/最小/最大”这一步合并到一次遍历，用字典记住当前最佳值，就能把 O(N²) 降到 O(N)。**  

## 反思  

- **第一反应**：看到“每个顾客的第一单”会想到先把记录按照 `customer_id` 分组，再在每组里找最小 `order_date`。  
- **最容易踩的坑**：  
  - **日期比较**：直接比较字符串可能在跨月份时出错，最好统一转成 `datetime` 再比较。  
  - **顾客只有一条记录**：代码必须兼容只有一条订单的顾客（仍然是第一单）。  
  - **除以 0**：如果表为空，需要提前返回 0.0，避免除零异常。  
- **下次类似题的第一步**：**先考虑“只遍历一次，边读边维护每组的极值（最早/最小/最大）”，这通常是最高效的做法**。