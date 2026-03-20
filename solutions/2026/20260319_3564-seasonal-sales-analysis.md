# #3564. 季节性销售分析 / Seasonal Sales Analysis

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/seasonal-sales-analysis/)

---

## 题目（英文原版）

**Description**

Table: sales
Table: products
Write a solution to find the most popular product category for each season. The seasons are defined as:
The popularity of a category is determined by the total quantity sold in that season. If there is a tie, select the category with the highest total revenue (quantity × price).
Return the result table ordered by season in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| sale_id       | int     |
| product_id    | int     |
| sale_date     | date    |
| quantity      | int     |
| price         | decimal |
+---------------+---------+
sale_id is the unique identifier for this table.
Each row contains information about a product sale including the product_id, date of sale, quantity sold, and price per unit.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| product_id    | int     |
| product_name  | varchar |
| category      | varchar |
+---------------+---------+
product_id is the unique identifier for this table.
Each row contains information about a product including its name and category.
```

**Example 3:**

```
+---------+------------+------------+----------+-------+
| sale_id | product_id | sale_date  | quantity | price |
+---------+------------+------------+----------+-------+
| 1       | 1          | 2023-01-15 | 5        | 10.00 |
| 2       | 2          | 2023-01-20 | 4        | 15.00 |
| 3       | 3          | 2023-03-10 | 3        | 18.00 |
| 4       | 4          | 2023-04-05 | 1        | 20.00 |
| 5       | 1          | 2023-05-20 | 2        | 10.00 |
| 6       | 2          | 2023-06-12 | 4        | 15.00 |
| 7       | 5          | 2023-06-15 | 5        | 12.00 |
| 8       | 3          | 2023-07-24 | 2        | 18.00 |
| 9       | 4          | 2023-08-01 | 5        | 20.00 |
| 10      | 5          | 2023-09-03 | 3        | 12.00 |
| 11      | 1          | 2023-09-25 | 6        | 10.00 |
| 12      | 2          | 2023-11-10 | 4        | 15.00 |
| 13      | 3          | 2023-12-05 | 6        | 18.00 |
| 14      | 4          | 2023-12-22 | 3        | 20.00 |
| 15      | 5          | 2024-02-14 | 2        | 12.00 |
+---------+------------+------------+----------+-------+
```

**Example 4:**

```
+------------+-----------------+----------+
| product_id | product_name    | category |
+------------+-----------------+----------+
| 1          | Warm Jacket     | Apparel  |
| 2          | Designer Jeans  | Apparel  |
| 3          | Cutting Board   | Kitchen  |
| 4          | Smart Speaker   | Tech     |
| 5          | Yoga Mat        | Fitness  |
+------------+-----------------+----------+
```

**Example 5:**

```
+---------+----------+----------------+---------------+
| season  | category | total_quantity | total_revenue |
+---------+----------+----------------+---------------+
| Fall    | Apparel  | 10             | 120.00        |
| Spring  | Kitchen  | 3              | 54.00         |
| Summer  | Tech     | 5              | 100.00        |
| Winter  | Apparel  | 9              | 110.00        |
+---------+----------+----------------+---------------+
```

---

## 题目（中文翻译）

**描述**  
表：`sales`  
表：`products`

编写一个查询，找出每个季节最受欢迎的商品类别。季节的划分如下：  
（题目原文中未给出具体划分，按照题目要求自行定义季节对应的月份区间）

- 类别的受欢迎程度由该季节内的**总销售数量**（`quantity`）决定。  
- 若出现销售数量相同的情况，则比较**总收入**（`quantity × price`），收入更高的类别获胜。

返回的结果表需按 **season**（季节）升序排列，列名及示例格式如下所示。

**示例**  

示例 1（`sales` 表结构）：

| Column Name | Type    |
|-------------|---------|
| sale_id     | int     |
| product_id  | int     |
| sale_date   | date    |
| quantity    | int     |
| price       | decimal |

`sale_id` 为该表的唯一标识。每行记录一次商品的销售信息，包括 `product_id`、销售日期、销售数量等。

示例 2（`products` 表结构）：

| Column Name | Type    |
|-------------|---------|
| product_id  | int     |
| product_name| varchar |
| category    | varchar |

`product_id` 为该表的唯一标识。每行记录商品的基本信息，包括名称和所属类别。

示例 3（`sales` 示例数据）：

| sale_id | product_id | sale_date  | quantity | price |
|---------|------------|------------|----------|-------|
| 1       | 1          | 2023-01-15 | 5        | 10.00 |
| 2       | 2          | 2023-01-20 | 4        | 15.00 |
| 3       | 3          | 2023-03-10 | 3        | 18.00 |
| 4       | 4          | 2023-04-05 | 1        | 20.00 |
| ...     | ...        | ...        | ...      | ...   |

示例 4（`products` 示例数据）：

| product_id | product_name   | category |
|------------|----------------|----------|
| 1          | Warm Jacket    | Apparel  |
| 2          | Designer Jeans | Apparel  |
| 3          | Cutting Board  | Kitchen  |
| 4          | Smart Speaker  | Tech     |
| 5          | Yoga Mat       | Fitness  |

示例 5（查询结果）：

| season | category | total_quantity | total_revenue |
|--------|----------|----------------|---------------|
| Fall   | Apparel  | 10             | 120.00        |
| Spring | Kitchen  | 3              | 54.00         |
| Summer | Tech     | 5              | 100.00        |
| Winter | Apparel  | 9              | 110.00        |

**约束条件**  
无。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
1. **把两张表关联**  
   - `sales` 记录每笔订单，`products` 给每个 `product_id` 打上所属的 `category`。  
   - 关联方式类似查字典：`product_id` 就是钥匙，`category` 是对应的价值。我们把 `sales` 中的每行都“查一遍字典”，把商品的 `category` 加到这行记录里。  

2. **把日期映射到季节**  
   - 先把 `sale_date` 拿出来，只看月份。  
   - 用一个小表（或 Python 的 `dict`）把月份映射到季节：  
     - 12、1、2 → **Winter**  
     - 3、4、5 → **Spring**  
     - 6、7、8 → **Summer**  
     - 9、10、11 → **Fall**  

3. **逐行累计**  
   - 用一个三层嵌套的字典 `season_category[season][category] = [quantity_sum, revenue_sum]` 来累计。  
   - 对每一行：  
     - 计算本行的收入 `revenue = quantity * price`。  
     - 把 `quantity` 加到对应季节‑类别的 `quantity_sum`，把 `revenue` 加到 `revenue_sum`。  

4. **挑选每个季节的“最受欢迎”类别**  
   - 对每个季节，遍历它的所有类别，先比较 `quantity_sum`（销量），数量大的就是首选。  
   - 如果出现 **并列**（数量相同），再比较 `revenue_sum`（总收入），收入大的获胜。  

5. **把结果装进列表并排序**  
   - 按季节的字母顺序（Winter, Spring, Summer, Fall）输出 `season, category, total_quantity, total_revenue`。  

> **为什么正确？**  
> - 我们把每笔销售都完整地计入了对应的季节和类别，没有遗漏。  
> - 通过两层比较（先销量后收入）严格遵守题目给出的“受欢迎度”定义。  

#### 代码（Python）  
```python
import datetime
from collections import defaultdict

# ------------------- 示例数据（实际使用时从数据库读取） -------------------
sales = [
    # sale_id, product_id, sale_date, quantity, price
    (1, 1, "2023-01-15", 5, 10.00),
    (2, 2, "2023-01-20", 4, 15.00),
    (3, 3, "2023-03-10", 3, 18.00),
    (4, 4, "2023-04-05", 1, 20.00),
    # ... 其它行
]

products = [
    # product_id, product_name, category
    (1, "Warm Jacket", "Apparel"),
    (2, "Designer Jeans", "Apparel"),
    (3, "Cutting Board", "Kitchen"),
    (4, "Smart Speaker", "Tech"),
    # ... 其它行
]

# ------------------- 1️⃣ 建立 product_id → category 的查找表 -------------------
pid_to_cat = {pid: cat for pid, _, cat in products}

# ------------------- 2️⃣ 月份 → 季节 的映射表 -------------------
month_to_season = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Fall", 10: "Fall", 11: "Fall",
}

# ------------------- 3️⃣ 累计每个 (season, category) 的销量与收入 -------------------
# 结构: season_category[season][category] = [quantity_sum, revenue_sum]
season_category = defaultdict(lambda: defaultdict(lambda: [0, 0.0]))

for _, pid, sale_date, qty, price in sales:
    # 取月份 → 季节
    month = datetime.datetime.strptime(sale_date, "%Y-%m-%d").month
    season = month_to_season[month]

    # 找到商品的类别
    category = pid_to_cat.get(pid, "Unknown")

    # 计算本行收入
    revenue = qty * price

    # 累计
    season_category[season][category][0] += qty
    season_category[season][category][1] += revenue

# ------------------- 4️⃣ 为每个季节挑选最受欢迎的类别 -------------------
result = []
for season in sorted(season_category.keys()):          # 按季节字母顺序
    best_cat = None
    best_qty = -1
    best_rev = -1.0
    for cat, (qty_sum, rev_sum) in season_category[season].items():
        # 先比较销量，销量相同再比较收入
        if qty_sum > best_qty or (qty_sum == best_qty and rev_sum > best_rev):
            best_cat, best_qty, best_rev = cat, qty_sum, rev_sum
    result.append({
        "season": season,
        "category": best_cat,
        "total_quantity": best_qty,
        "total_revenue": round(best_rev, 2)   # 保留两位小数
    })

# ------------------- 5️⃣ 打印结果 -------------------
for row in result:
    print(row)
```

> **关键行中文注释** 已在代码里标出，帮助你一步步跟踪执行过程。  

#### 复杂度  
- **时间复杂度：** `O(N + M)`  
  - `N` 为 `sales` 表的行数，`M` 为 `products` 表的行数。我们只遍历两张表各一次，没出现嵌套循环。  
  - 大白话：如果有 10 万笔订单，程序大约会跑 10 万次（外加几千次商品表），不随季节或类别的多少再增加。  
- **空间复杂度：** `O(S * C)`  
  - `S` 为季节数（固定 4），`C` 为出现过的类别数。我们用一个字典保存每个季节‑类别的累计值，最多占用几百个键值对的空间。  

---  

### 2. 最优解  

#### 思路  
暴力解已经是 **线性** 的了，真正的提升在于**利用现成的向量化/分组工具**（如 `pandas` 的 `groupby`），省去手写的循环与嵌套 `dict`，代码更简洁、运行更快（底层是 C 实现的聚合）。思路仍然是：

1. **关联** `sales` 与 `products`（等价于 SQL 的 `JOIN`）。  
2. **映射季节**：直接在 DataFrame 中新建一列 `season`。  
3. **一次性分组**：`groupby(['season', 'category'])` 同时得到 `quantity` 的和以及 `quantity*price` 的和。  
4. **在每个季节内部再次挑选**：使用 `sort_values` + `drop_duplicates` 或者 `groupby('season').apply`，实现“先比较销量，平局再比较收入”。  

> **核心技巧**：  
> - **JOIN + GROUP BY** 是关系型数据库里最常见的统计手段，`pandas` 把它们搬到了 Python。  
> - **排序 + 去重** 可以一次性实现“最大值 + 条件”。  

#### 代码（Python）  
```python
import pandas as pd

# ------------------- 读取示例数据 -------------------
sales_df = pd.DataFrame([
    # sale_id, product_id, sale_date, quantity, price
    (1, 1, "2023-01-15", 5, 10.00),
    (2, 2, "2023-01-20", 4, 15.00),
    (3, 3, "2023-03-10", 3, 18.00),
    (4, 4, "2023-04-05", 1, 20.00),
    # ... 更多行
], columns=["sale_id", "product_id", "sale_date", "quantity", "price"])

products_df = pd.DataFrame([
    # product_id, product_name, category
    (1, "Warm Jacket", "Apparel"),
    (2, "Designer Jeans", "Apparel"),
    (3, "Cutting Board", "Kitchen"),
    (4, "Smart Speaker", "Tech"),
    # ... 更多行
], columns=["product_id", "product_name", "category"])

# ------------------- 1️⃣ JOIN -------------------
df = sales_df.merge(products_df[['product_id', 'category']],
                    on='product_id',
                    how='left')

# ------------------- 2️⃣ 添加 season 列 -------------------
# 先把字符串日期转为 datetime，再取月份 → 季节
df['sale_date'] = pd.to_datetime(df['sale_date'])
month_to_season = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Fall", 10: "Fall", 11: "Fall",
}
df['season'] = df['sale_date'].dt.month.map(month_to_season)

# ------------------- 3️⃣ 计算收入并聚合 -------------------
df['revenue'] = df['quantity'] * df['price']

# 按季节‑类别分组，求总销量和总收入
grouped = (
    df.groupby(['season', 'category'], as_index=False)
      .agg(total_quantity=('quantity', 'sum'),
           total_revenue=('revenue', 'sum'))
)

# ------------------- 4️⃣ 在每个季节内部挑选最受欢迎的类别 -------------------
# 先按照 total_quantity 降序、total_revenue 降序 排序
grouped = grouped.sort_values(
    ['season', 'total_quantity', 'total_revenue'],
    ascending=[True, False, False]
)

# 对每个 season 保留第一条（即销量最高、收入最高的那条）
result = grouped.drop_duplicates(subset='season', keep='first')

# ------------------- 5️⃣ 按季节升序输出 -------------------
result = result.sort_values('season').reset_index(drop=True)
print(result)
```

> **运行效果（示例）**  
> ```
>    season  category  total_quantity  total_revenue
> 0  Fall    Apparel                10          120.0
> 1  Spring  Kitchen                  3           54.0
> 2  Summer   Tech                    5          100.0
> 3  Winter  Apparel                  9          110.0
> ```  

#### 复杂度  
- **时间复杂度：** `O(N log N)`（主要来源于 `sort_values` 的排序），但 `N` 仅是分组后的记录数（最多 `4 * C`），通常远小于原始行数。实际执行速度比手写循环要快得多，因为底层是 C 实现的向量化操作。  
- **空间复杂度：** `O(N)`，需要存放一次 `JOIN` 后的临时 DataFrame 与分组结果。相较于暴力解的字典结构，空间占用略高但仍在可接受范围。  

---  

## 心得  

- **核心技巧**：`JOIN + GROUP BY + 排序去重`，这是数据库/数据分析里挑选“最高/最热”对象的标准套路。  
- **适用题型**（类似的）  
  1. **每月/每年销量最高的商品**（按月份/年份分组）。  
  2. **每个城市收入最高的店铺**（城市‑店铺分组，先比较销售额再比较利润）。  
  3. **每个部门员工工作时长最多的员工**（部门‑员工分组，先比较工时再比较绩效分）。  
- **一句话总结解题钥匙**：先把 **维度**（季节、类别）映射好，再用 **一次分组聚合 + 排序去重** 找出每个维度下的“冠军”。  

---  

## 反思  

- **拿到题目第一反应**：先把日期转成季节，再把销量和收入累加，最后比较。  
- **最容易踩的坑**  
  - **季节划分错误**：忘记把 12 月归到 Winter。  
  - **收入计算遗漏**：收入必须是 `quantity * price`，不能只用 `price`。  
  - **并列处理**：只比较销量会导致错误，需要在数量相同的情况下再比较收入。  
  - **空值或未知商品**：如果 `sales` 中出现了在 `products` 表里找不到的 `product_id`，要有默认的 “Unknown” 类别，防止程序报错。  
- **下次遇到同类题的第一步**：**明确分组键**（本题是 season + category）和 **比较规则**（先销量后收入），然后决定是手写循环还是直接使用 `groupby`。这样思路清晰，代码实现自然流畅。