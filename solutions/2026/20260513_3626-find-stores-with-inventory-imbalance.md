# #3626. 查找库存失衡的商店 / Find Stores with Inventory Imbalance

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/find-stores-with-inventory-imbalance/)

---

## 题目（英文原版）

**Description**

Table: stores
Table: inventory
Write a solution to find stores that have inventory imbalance - stores where the most expensive product has lower stock than the cheapest product.
Return the result table ordered by imbalance ratio in descending order, then by store name in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| store_id    | int     |
| store_name  | varchar |
| location    | varchar |
+-------------+---------+
store_id is the unique identifier for this table.
Each row contains information about a store and its location.
```

**Example 2:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| inventory_id| int     |
| store_id    | int     |
| product_name| varchar |
| quantity    | int     |
| price       | decimal |
+-------------+---------+
inventory_id is the unique identifier for this table.
Each row represents the inventory of a specific product at a specific store.
```

**Example 3:**

```
+----------+----------------+-------------+
| store_id | store_name     | location    |
+----------+----------------+-------------+
| 1        | Downtown Tech  | New York    |
| 2        | Suburb Mall    | Chicago     |
| 3        | City Center    | Los Angeles |
| 4        | Corner Shop    | Miami       |
| 5        | Plaza Store    | Seattle     |
+----------+----------------+-------------+
```

**Example 4:**

```
+--------------+----------+--------------+----------+--------+
| inventory_id | store_id | product_name | quantity | price  |
+--------------+----------+--------------+----------+--------+
| 1            | 1        | Laptop       | 5        | 999.99 |
| 2            | 1        | Mouse        | 50       | 19.99  |
| 3            | 1        | Keyboard     | 25       | 79.99  |
| 4            | 1        | Monitor      | 15       | 299.99 |
| 5            | 2        | Phone        | 3        | 699.99 |
| 6            | 2        | Charger      | 100      | 25.99  |
| 7            | 2        | Case         | 75       | 15.99  |
| 8            | 2        | Headphones   | 20       | 149.99 |
| 9            | 3        | Tablet       | 2        | 499.99 |
| 10           | 3        | Stylus       | 80       | 29.99  |
| 11           | 3        | Cover        | 60       | 39.99  |
| 12           | 4        | Watch        | 10       | 299.99 |
| 13           | 4        | Band         | 25       | 49.99  |
| 14           | 5        | Camera       | 8        | 599.99 |
| 15           | 5        | Lens         | 12       | 199.99 |
+--------------+----------+--------------+----------+--------+
```

**Example 5:**

```
+----------+----------------+-------------+------------------+--------------------+------------------+
| store_id | store_name     | location    | most_exp_product | cheapest_product   | imbalance_ratio  |
+----------+----------------+-------------+------------------+--------------------+------------------+
| 3        | City Center    | Los Angeles | Tablet           | Stylus             | 40.00            |
| 1        | Downtown Tech  | New York    | Laptop           | Mouse              | 10.00            |
| 2        | Suburb Mall    | Chicago     | Phone            | Case               | 25.00            |
+----------+----------------+-------------+------------------+--------------------+------------------+
```

---

## 题目（中文翻译）

写一个查询，找出库存（inventory）失衡的商店——即该商店最贵的商品的库存量低于最便宜的商品的库存量的商店。返回的结果表需按失衡比例（imbalance ratio）降序排列，若失衡比例相同则按商店名称（store name）升序排列。结果格式参考下例。

**示例 1：**  

表（table）：stores  

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| store_id    | int     |
| store_name  | varchar |
| location    | varchar |
+-------------+---------+
```

- `store_id` 是该表的唯一标识符（unique identifier）。
- 每行记录一家商店及其所在位置。

**示例 2：**  

表（table）：inventory  

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| inventory_id| int     |
| store_id    | int     |
| product_name| varchar |
| quantity    | int     |
| price       | decimal |
+-------------+---------+
```

- `inventory_id` 是该表的唯一标识符（unique identifier）。
- 每行记录某家商店中一种具体商品的库存信息。

**示例 3：**  

```
+----------+----------------+-------------+
| store_id | store_name     | location    |
+----------+----------------+-------------+
| 1        | Downtown Tech  | New York    |
| 2        | Suburb Mall    | Chicago     |
| 3        | City Center    | Los Angeles |
| 4        | Corner Shop    | Miami       |
| 5        | Plaza Store    | Seattle     |
+----------+----------------+-------------+
```

**示例 4：**  

```
+--------------+----------+--------------+----------+--------+
| inventory_id | store_id | product_name | quantity | price  |
+--------------+----------+--------------+----------+--------+
| 1            | 1        | Laptop       | 5        | 999.99 |
| 2            | 1        | Mouse        | 50       | 19.99  |
| 3            | 1        | Keyboard     | 25       | 79.99  |
| 4            | 1        ... (已截断)
```

**示例 5（返回结果）：**  

```
+----------+----------------+-------------+------------------+-------------------+-----------------+
| store_id | store_name     | location    | most_exp_product | cheapest_product  | imbalance_ratio |
+----------+----------------+-------------+------------------+-------------------+-----------------+
| 3        | City Center    | Los Angeles | Tablet           | Stylus            | 40.00           ... (已截断)
```

**约束条件：**  
无

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

我们先把两张表想象成两本“登记册”。  
- **stores**：每一页记录一家店的 `store_id、store_name、location`。  
- **inventory**：每一页记录某家店里某件商品的 `store_id、product_name、quantity、price`。  

最直接的想法是：**把每一家店的所有商品挑出来，分别找出**  

1. **最贵的商品**（price 最高）对应的库存 `quantity_max`  
2. **最便宜的商品**（price 最低）对应的库存 `quantity_min`  

如果 `quantity_max < quantity_min`，说明这家店出现了 “库存失衡”。  
然后把失衡的店的信息连同最贵商品名、最便宜商品名以及失衡比例（这里我们把比例定义为 `quantity_min - quantity_max`，即差值）放进结果表。

> **为什么这种方法一定能得到正确答案？**  
> 因为我们对每一家店都完整遍历了它的全部商品，必然能找出价格最高和最低的那两件商品，并比较它们的库存。只要满足题目条件，就把它记录下来。

**复杂度的“大白话”**  
- 假设 `S` 是店的数量，`I` 是库存记录的总条数。  
- 对每一家店我们都要在 `inventory` 表里 **全表扫描** 一遍来挑出该店的商品 → `O(I)`。  
- 这样总共要做 `S` 次扫描 → **时间复杂度 `O(S·I)`**。如果 `S` 和 `I` 同量级，这相当于 `O(n²)`（把所有记录两两比较的意思）。  
- 我们只用了几个额外的变量（比如临时的最大/最小价格），**空间复杂度是 `O(1)`**（不随输入规模增长）。

#### 代码（Python）

```python
# 假设输入数据已经读取为 Python 列表（每条记录是 dict）：
# stores   = [{'store_id': 1, 'store_name': 'Downtown Tech', 'location': 'New York'}, ...]
# inventory = [{'inventory_id': 1, 'store_id': 1, 'product_name': 'Laptop',
#               'quantity': 5, 'price': 999.99}, ...]

def find_imbalance_bruteforce(stores, inventory):
    result = []

    # 对每一家店，逐个检查
    for store in stores:
        sid = store['store_id']

        # 过滤出该店所有商品
        items = [item for item in inventory if item['store_id'] == sid]

        # 如果这家店根本没有商品，直接跳过
        if not items:
            continue

        # 暴力遍历找最贵、最便宜的商品
        most_exp_item = items[0]   # 暂时把第一个当作最贵
        cheap_item    = items[0]   # 暂时把第一个当作最便宜

        for it in items:
            if it['price'] > most_exp_item['price']:
                most_exp_item = it
            if it['price'] < cheap_item['price']:
                cheap_item = it

        # 判断是否出现库存失衡
        if most_exp_item['quantity'] < cheap_item['quantity']:
            imbalance = cheap_item['quantity'] - most_exp_item['quantity']
            result.append({
                'store_id'          : sid,
                'store_name'        : store['store_name'],
                'location'          : store['location'],
                'most_exp_product'  : most_exp_item['product_name'],
                'cheapest_product'  : cheap_item['product_name'],
                'imbalance_ratio'   : float(imbalance)   # 这里用差值表示比例
            })

    # 按要求排序：先按比例降序，再按店名升序
    result.sort(key=lambda x: (-x['imbalance_ratio'], x['store_name']))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(S·I)`，即每家店都要遍历一次完整的库存表。  
  - 大白话：如果有 100 家店，每家店的库存记录平均 100 条，总共要做 10 000 次检查。  
- **空间复杂度**：`O(1)`（不计返回结果的空间），只用了常数个临时变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于对每一家店都要 **重复遍历** 整个 `inventory` 表。  
如果我们一次性把 `inventory` 表 **全部读进来**，并在 **同一次遍历** 完成以下两件事：

1. **为每一家店维护**  
   - 当前已见到的最高价格及对应的商品信息  
   - 当前已见到的最低价格及对应的商品信息  

2. 只要遍历结束，就已经得到每家店的“最贵/最便宜商品”。  

这相当于把 **“筛选 + 求极值”** 合并到一次 **线性扫描**（一次遍历）里，**把时间从 `O(S·I)` 降到 `O(I)`**。  

**核心数据结构：哈希表（字典）**  
- 把 `store_id` 当作 “钥匙”，对应的值是一个小字典，里面保存四个字段：  
  - `max_price`、`max_product`、`max_qty`  
  - `min_price`、`min_product`、`min_qty`  
- 类比：这就像一本“按店号分册的商品目录”，我们随手翻开对应的页码，就能在 O(1) 时间内更新该店的记录。

**一步步推导**  

1. 初始化一个空字典 `store_stats = {}`。  
2. 遍历 `inventory` 中的每条记录 `row`：  
   - 取出 `sid = row['store_id']`。  
   - 如果 `sid` 还没有在 `store_stats` 里出现，就创建一个记录并把当前商品设为既是最贵也是最便宜的（因为它是唯一的）。  
   - 否则，用 `row['price']` 与已有的 `max_price/min_price` 比较，必要时更新对应的商品名和数量。  
3. 遍历完 `inventory` 后，`store_stats` 已经保存了每家店的极值信息。  
4. 再遍历一次 `stores`（这一步只会遍历 `S` 条记录），把满足 **`max_qty < min_qty`** 的店挑出来并计算 `imbalance_ratio = min_qty - max_qty`。  
5. 最后按照题目要求排序并返回。

**复杂度的大白话**  
- **时间**：只遍历两遍表，第一遍是 `inventory`（`I` 条），第二遍是 `stores`（`S` 条），合在一起是 `O(I + S)`，基本上和记录总数成线性关系。  
- **空间**：我们为每一家店保存一个小字典，最多需要 `O(S)` 的额外空间（每家店占用常数大小的内存）。

#### 代码（Python）

```python
def find_imbalance_optimized(stores, inventory):
    """
    使用一次遍历统计每家店的最贵/最便宜商品信息，再一次遍历
    过滤出库存失衡的店并排序返回。
    """
    # ---------- 第一步：一次遍历 inventory，构建每家店的极值信息 ----------
    # store_stats[store_id] = {
    #     'max_price'   : float,
    #     'max_product' : str,
    #     'max_qty'     : int,
    #     'min_price'   : float,
    #     'min_product' : str,
    #     'min_qty'     : int
    # }
    store_stats = {}

    for row in inventory:
        sid = row['store_id']
        price = row['price']
        qty   = row['quantity']
        prod  = row['product_name']

        if sid not in store_stats:
            # 第一次看到这家店，用当前商品初始化
            store_stats[sid] = {
                'max_price'   : price,
                'max_product' : prod,
                'max_qty'     : qty,
                'min_price'   : price,
                'min_product' : prod,
                'min_qty'     : qty
            }
        else:
            stats = store_stats[sid]

            # 更新最高价商品
            if price > stats['max_price']:
                stats['max_price']   = price
                stats['max_product'] = prod
                stats['max_qty']     = qty

            # 更新最低价商品
            if price < stats['min_price']:
                stats['min_price']   = price
                stats['min_product'] = prod
                stats['min_qty']     = qty

    # ---------- 第二步：遍历 stores，挑出失衡的店 ----------
    result = []
    for store in stores:
        sid = store['store_id']
        # 这家店可能根本没有任何库存记录，直接跳过
        if sid not in store_stats:
            continue

        stats = store_stats[sid]
        # 判断“最贵商品的库存 < 最便宜商品的库存”
        if stats['max_qty'] < stats['min_qty']:
            imbalance = stats['min_qty'] - stats['max_qty']
            result.append({
                'store_id'         : sid,
                'store_name'       : store['store_name'],
                'location'         : store['location'],
                'most_exp_product' : stats['max_product'],
                'cheapest_product' : stats['min_product'],
                'imbalance_ratio'  : float(imbalance)   # 用差值表示比例
            })

    # ---------- 第三步：排序 ----------
    # 1）imbalance_ratio 降序 2）store_name 升序
    result.sort(key=lambda x: (-x['imbalance_ratio'], x['store_name']))
    return result
```

#### 复杂度  

- **时间复杂度**：`O(I + S)`  
  - 只需要一次线性遍历 `inventory`（`I` 条）和一次遍历 `stores`（`S` 条），没有嵌套循环。  
  - 与暴力解相比，省掉了每家店都要重复扫描 `inventory` 的那部分开销。  
- **空间复杂度**：`O(S)`  
  - 为每一家店保存一个固定大小的字典，随着店的数量线性增长。  
  - 这在实际业务中通常是可以接受的（店的数量远小于库存记录总数）。

---

## 心得  

- **核心技巧**：**一次遍历 + 哈希表（字典）聚合**。  
  - 先把需要的统计信息（最大/最小价格及对应库存）在遍历中直接累计，避免后续的重复扫描。  
- **适用的题型**（类似思路）  
  1. “找出每个用户的最近一次登录时间”。  
  2. “统计每个部门的最高工资和最低工资”。  
  3. “求每个类别的最早和最晚订单日期”。  
- **一句话总结解题钥匙**：**把所有要比较的“极值”在一次遍历中累计到以 `store_id` 为键的哈希表里，最后再统一过滤和排序。**

---

## 反思  

- **第一反应**：看到“最贵商品”和“最便宜商品”，立刻想到要对每家店分别做两次 `max/min` 查找，于是写出了暴力的双层循环。  
- **最容易踩的坑**  
  - **空店**：有的 `store_id` 可能在 `inventory` 中没有对应记录，直接访问会报错，需要提前判空。  
  - **同价商品**：如果同一家店里出现多件同价商品，题目只要求任意一件即可；代码中只保留第一次出现的商品信息，满足要求。  
  - **比例定义**：题目没有明确说明“imbalance_ratio”到底是差值还是相对比例，本文选择 **差值**（`cheapest_qty - most_exp_qty`），实际实现时请根据面试官/平台的具体说明作相应调整。  
- **下次遇到同类题**：**先思考能否一次遍历完成所有统计**，把“对每个分组求极值/聚合”抽象为 “使用哈希表在遍历中实时更新”。这样往往能直接从 O(n²) 降到 O(n)。