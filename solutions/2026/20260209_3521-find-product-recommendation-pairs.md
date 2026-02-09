# #3521. 查找产品推荐配对 / Find Product Recommendation Pairs

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-product-recommendation-pairs/)

---

## 题目（英文原版）

**Description**

Table: ProductPurchases
Table: ProductInfo
Amazon wants to implement the Customers who bought this also bought... feature based on co-purchase patterns. Write a solution to :
A product pair is considered for recommendation if at least 3 different customers have purchased both products.
Return the result table ordered by customer_count in descending order, and in case of a tie, by product1_id in ascending order, and then by product2_id in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type | 
+-------------+------+
| user_id     | int  |
| product_id  | int  |
| quantity    | int  |
+-------------+------+
(user_id, product_id) is the unique key for this table.
Each row represents a purchase of a product by a user in a specific quantity.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    | 
+-------------+---------+
| product_id  | int     |
| category    | varchar |
| price       | decimal |
+-------------+---------+
product_id is the primary key for this table.
Each row assigns a category and price to a product.
```

**Example 3:**

```
+---------+------------+----------+
| user_id | product_id | quantity |
+---------+------------+----------+
| 1       | 101        | 2        |
| 1       | 102        | 1        |
| 1       | 103        | 3        |
| 2       | 101        | 1        |
| 2       | 102        | 5        |
| 2       | 104        | 1        |
| 3       | 101        | 2        |
| 3       | 103        | 1        |
| 3       | 105        | 4        |
| 4       | 101        | 1        |
| 4       | 102        | 1        |
| 4       | 103        | 2        |
| 4       | 104        | 3        |
| 5       | 102        | 2        |
| 5       | 104        | 1        |
+---------+------------+----------+
```

**Example 4:**

```
+------------+-------------+-------+
| product_id | category    | price |
+------------+-------------+-------+
| 101        | Electronics | 100   |
| 102        | Books       | 20    |
| 103        | Clothing    | 35    |
| 104        | Kitchen     | 50    |
| 105        | Sports      | 75    |
+------------+-------------+-------+
```

**Example 5:**

```
+-------------+-------------+-------------------+-------------------+----------------+
| product1_id | product2_id | product1_category | product2_category | customer_count |
+-------------+-------------+-------------------+-------------------+----------------+
| 101         | 102         | Electronics       | Books             | 3              |
| 101         | 103         | Electronics       | Clothing          | 3              |
| 102         | 104         | Books             | Kitchen           | 3              |
+-------------+-------------+-------------------+-------------------+----------------+
```

---

## 题目（中文翻译）

Amazon 希望基于共同购买（co‑purchase）模式实现 “购买了此商品的用户也购买了…” 功能。编写 SQL 查询满足以下要求：

- 若至少有 **3** 位不同的用户（customer）同时购买了两个商品，则这对商品可被视为推荐配对（product pair）。
- 返回结果表需包含 `product1_id`、`product2_id`、`product1_category`、`product2_category`、`customer_count`（同时购买这两个商品的用户数量）。
- 结果按照 `customer_count` 降序排列；若 `customer_count` 相同，则按 `product1_id` 升序排列；若仍相同，再按 `product2_id` 升序排列。

下面给出表结构示例以及示例数据。

**表结构**

```
Table: ProductPurchases
+-------------+------+
| Column Name | Type |
+-------------+------+
| user_id     | int  |
| product_id  | int  |
| quantity    | int  |
+-------------+------+
(user_id, product_id) 是此表的唯一键。
每行记录表示某用户以特定数量购买了一件商品。

Table: ProductInfo
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| product_id  | int     |
| category    | varchar |
| price       | decimal |
+-------------+---------+
product_id 是此表的主键。
每行记录为商品分配了类别（category）和价格（price）。
```

**示例数据**

```
+---------+------------+----------+
| user_id | product_id | quantity |
+---------+------------+----------+
| 1       | 101        | 2        |
| 1       | 102        | 1        |
| 1       | 103        | 3        |
| 2       | 101        | 1        |
| 2       | 102        | 5        |
| 2       | 104        | 1        |
| 3       | 101        | 2        |
| 3       | 103        | 1        |
| 3       | ... (已截断)
```

```
+------------+-------------+-------+
| product_id | category    | price |
+------------+-------------+-------+
| 101        | Electronics | 100   |
| 102        | Books       | 20    |
| 103        | Clothing    | 35    |
| 104        | Kitchen     | 50    |
| 105        | Sports      | 75    |
+------------+-------------+-------+
```

**期望输出示例**

```
+-------------+-------------+-------------------+-------------------+----------------+
| product1_id | product2_id | product1_category | product2_category | customer_count |
+-------------+-------------+-------------------+-------------------+----------------+
| 101         | 102         | Electronics       | Books             | 3              |
| 101         | 103         | Electronics       | Clothing          | ... (已截断)
```

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **把原始表想象成一本“购物账本”。**  
   - 每一行是一次购买记录：`user_id`（顾客）买了 `product_id`（商品），数量 `quantity`（这里数量不影响推荐，只要买过就算）。  
   - 我们只关心 **“同一个顾客买了哪些商品”**，所以先把账本按 `user_id` 分组，得到每个顾客的商品集合。  

2. **把每个顾客的商品集合看成一张“小卡片”。**  
   - 对于一张卡片（比如顾客 A 买了 {101, 102, 103}），我们可以枚举卡片上任意两张商品卡（组合 C(3,2)=3），每出现一次就把这对商品的 “共同购买次数” 加 1。  
   - 这一步就像在做 **“哈希表查字典”**：  
     - **key** = (较小的商品 id, 较大的商品 id) → 保证 (101,102) 与 (102,101) 视为同一对。  
     - **value** = 已经有多少不同顾客买过这对商品。  

3. **遍历完所有顾客后，筛选出出现次数 ≥ 3 的商品对**，再把商品的类别信息从 `ProductInfo` 表里找出来即可。  

> 为什么这个方法一定对？  
> - 每一次我们只统计 **“同一个顾客买了这两件商品”**，而不是跨顾客的随意组合。  
> - 把每个顾客的商品两两配对后，累计到同一哈希表中，最后统计的次数正好等于 “有多少不同顾客买过这对商品”。  

#### 代码（Python）

```python
from collections import defaultdict
from itertools import combinations
from typing import List, Tuple, Dict

# ---------- 模拟的输入 ----------
# purchases: List[Tuple[user_id, product_id, quantity]]
purchases: List[Tuple[int, int, int]] = [
    # (user_id, product_id, quantity) 示例数据
    (1, 101, 2), (1, 102, 1), (1, 103, 3),
    (2, 101, 1), (2, 102, 5), (2, 104, 1),
    (3, 101, 2), (3, 103, 1),
    (4, 101, 1), (4, 102, 2), (4, 103, 1),
    # … 这里可以继续添加更多数据
]

# product_info: Dict[product_id, category]
product_info: Dict[int, str] = {
    101: "Electronics",
    102: "Books",
    103: "Clothing",
    104: "Kitchen",
    105: "Sports",
    # …
}
# ----------------------------------

def brute_force(purchases: List[Tuple[int, int, int]],
                product_info: Dict[int, str]) -> List[Tuple[int, int, str, str, int]]:
    """
    暴力实现：逐用户枚举商品两两组合，累计出现次数。
    返回的每一行是
    (product1_id, product2_id, product1_category, product2_category, customer_count)
    """
    # 1️⃣ 按用户收集商品集合
    user_to_products: Dict[int, set] = defaultdict(set)
    for user_id, product_id, _ in purchases:
        user_to_products[user_id].add(product_id)

    # 2️⃣ 用哈希表统计每对商品被多少不同用户共同购买
    pair_cnt: Dict[Tuple[int, int], int] = defaultdict(int)
    for products in user_to_products.values():
        # 同一个用户购买的商品可能很多，用 combinations 产生两两配对
        for p1, p2 in combinations(sorted(products), 2):   # 先排序保证 p1 < p2
            pair_cnt[(p1, p2)] += 1

    # 3️⃣ 过滤出满足 “≥3 位不同用户” 的商品对，并补全类别信息
    result = []
    for (p1, p2), cnt in pair_cnt.items():
        if cnt >= 3:                     # 题目要求的阈值
            cat1 = product_info.get(p1, "UNKNOWN")
            cat2 = product_info.get(p2, "UNKNOWN")
            result.append((p1, p2, cat1, cat2, cnt))

    # 4️⃣ 按要求排序：customer_count 降序 → product1_id 升序 → product2_id 升序
    result.sort(key=lambda x: (-x[4], x[0], x[1]))
    return result


# 演示运行
if __name__ == "__main__":
    ans = brute_force(purchases, product_info)
    for row in ans:
        print(row)
```

> **关键注释说明**  
> - `defaultdict(set)` 把 “每个顾客买了哪些商品” 存成集合，类似字典里的 “查字典”。  
> - `combinations(sorted(products), 2)` 把集合里的商品两两配对，`sorted` 保证配对顺序统一（小的在前），避免把 (101,102) 和 (102,101) 当成两条不同记录。  
> - `pair_cnt[(p1, p2)] += 1` 就是把这对商品的共同购买次数累加。  

#### 复杂度  

- **时间复杂度**：`O( Σ_u k_u^2 )`  
  - 其中 `k_u` 是第 `u` 位用户购买的商品数量。  
  - “`k_u^2`” 表示对每个用户的商品集合做两两配对，最坏情况下如果每个用户买了 `K` 件商品，则时间会是 `O(U * K^2)`（U 为用户数）。  
  - 用大白话说：如果每个人买的东西很多，这一步会比较慢，因为要把每个人的商品两两组合一次。  

- **空间复杂度**：`O(P^2)`（最坏）  
  - `pair_cnt` 需要存放所有可能的商品对，商品总数记为 `P`，所以最多会有 `P*(P-1)/2` 种不同的配对。  
  - 另外还有 `user_to_products`（每个用户的商品集合），这部分空间和输入规模成正比。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于对每个用户的商品集合做两两组合**。如果某些商品非常热门（被很多用户买），它们会产生大量的配对，导致 `k_u^2` 过大。我们可以把视角换成 **“以商品为中心”**：

1. **先把每个商品对应的购买用户集合列出来**（商品 → 用户集合）。这一步只需要一次遍历，时间 `O(N)`（N 为购买记录条数）。  
2. **对所有商品对进行一次遍历**，直接求出它们的共同用户数。  
   - 设 `users_a`、`users_b` 为两个商品的购买用户集合，**共同用户数** = `|users_a ∩ users_b|`（集合交集的大小）。  
   - Python 中集合的交集运算 `len(set1 & set2)` 已经是 **线性时间**（取较小集合的大小），因此一次商品对的计算成本是 `O(min(|users_a|, |users_b|))`。  
3. **只保留交集大小 ≥ 3 的商品对**，再把类别信息补齐。  

这样做的好处是：

- 每条购买记录只会被放进两个集合（对应的商品），不再在用户层面产生二次组合。  
- 只要两个商品的购买用户集合都不大，交集运算就非常快。  
- 对于非常热门的商品，交集仍然是 `O(min(|A|,|B|))`，不会出现 `k_u^2` 那样的指数级增长。  

> **核心数据结构——哈希集合（set）**  
> - 类比查字典：`key` 是商品 id，`value` 是买过这件商品的所有用户 id（像一本“用户名单”）。  
> - `set` 天然支持快速的“是否在集合里”以及“交集”操作，底层实现是哈希表，查找、插入、删除的平均时间都是 **O(1)**。  

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Tuple, Dict

def optimal(purchases: List[Tuple[int, int, int]],
            product_info: Dict[int, str]) -> List[Tuple[int, int, str, str, int]]:
    """
    最优实现：以商品为中心，利用集合交集计算共同购买用户数。
    返回格式同上。
    """
    # 1️⃣ 建立商品 → 用户集合的映射
    product_to_users: Dict[int, set] = defaultdict(set)
    for user_id, product_id, _ in purchases:
        product_to_users[product_id].add(user_id)

    # 2️⃣ 获得所有商品 id 并排序（保证后面 pair 的顺序 p1 < p2）
    product_ids = sorted(product_to_users.keys())

    result = []
    # 3️⃣ 双层循环遍历所有商品对
    for i in range(len(product_ids)):
        p1 = product_ids[i]
        users1 = product_to_users[p1]
        for j in range(i + 1, len(product_ids)):
            p2 = product_ids[j]
            users2 = product_to_users[p2]

            # 交集大小 = 同时购买 p1 与 p2 的用户数
            common_cnt = len(users1 & users2)   # O(min(|users1|, |users2|))

            if common_cnt >= 3:
                cat1 = product_info.get(p1, "UNKNOWN")
                cat2 = product_info.get(p2, "UNKNOWN")
                result.append((p1, p2, cat1, cat2, common_cnt))

    # 4️⃣ 按题目要求排序
    result.sort(key=lambda x: (-x[4], x[0], x[1]))
    return result


# 演示运行（与上面相同的数据）
if __name__ == "__main__":
    ans_opt = optimal(purchases, product_info)
    for row in ans_opt:
        print(row)
```

> **关键点说明**  
> - `product_to_users` 的每个值都是 **集合**，所以 `users1 & users2` 直接得到交集。  
> - 双层循环只遍历 **商品对**（最多 `P*(P-1)/2` 次），而不是每个用户的商品组合。  
> - 交集运算的时间取决于两个集合的较小者，这在实际数据中往往远小于 `k_u^2` 的规模。  

#### 复杂度  

- **时间复杂度**：`O(P^2 * avg_min_user)`  
  - `P` 为商品总数。  
  - `avg_min_user` 是在所有商品对中较小集合的平均大小。  
  - 在大多数真实业务场景里，单个商品的购买用户数相对均衡，`avg_min_user` 远小于 `U`（用户总数），因此整体速度快于暴力解。  

- **空间复杂度**：`O(N + P^2)`（最坏）  
  - `product_to_users` 需要存放所有购买记录的映射，等价于原始数据大小 `O(N)`。  
  - `result` 只保存满足条件的商品对，最坏情况下可能是 `O(P^2)`（所有商品对都满足阈值），但这已经是输出本身的必然空间。  

> 与暴力解对比：  
> - 暴力解的时间与 **每个用户的商品数量平方** 成正比，容易在用户购买商品很多时爆炸。  
> - 最优解的时间与 **商品对的数量** 成正比，且每次检查只需要一次集合交集，通常更快且更易于扩展到大数据量。  

---

## 心得  

- **核心技巧**：把“共同购买”从“用户视角的配对”转化为“商品视角的集合交集”。  
- **适用场景**  
  1. “买了 X 的用户也买了 Y” 类的协同过滤（如电商推荐）。  
  2. “两个标签共同出现的次数” 统计（社交媒体 hashtag 关联分析）。  
  3. “两个课程被同一批学生选修的次数” （教育平台课程推荐）。  
- **一句话总结**：**把问题映射成集合交集，利用哈希集合的 O(1) 查找特性，往往能把“指数级”暴力降到 “平方级”。**  

---

## 反思  

- **第一反应**：看到“至少 3 位不同用户同时购买”立刻想到 **“把每个用户的商品两两配对并计数”**，这就是最直接的暴力思路。  
- **最容易踩的坑**  
  1. **重复计数**：如果不把商品对排序（确保 `p1 < p2`），同一对会被算成两条不同记录。  
  2. **忘记去重用户**：统计时必须基于 **不同用户**，而不是购买次数或数量。  
  3. **类别信息缺失**：最终输出要求商品类别，记得在结果阶段再去 `ProductInfo` 表里查。  
- **下次类似题的第一步**：先决定是 **“以用户为中心”** 还是 **“以商品/标签为中心”**，然后选用集合或哈希表做一次 “交集 / 计数” 操作，避免在原始维度上做 O(k²) 的暴力枚举。