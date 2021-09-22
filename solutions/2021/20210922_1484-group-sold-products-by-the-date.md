# #1484. 按日期分组已售产品 / Group Sold Products By The Date

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/group-sold-products-by-the-date/)

---

## 题目（英文原版）

**Description**

Table Activities:
Write a solution to find for each date the number of different products sold and their names.
The sold products names for each date should be sorted lexicographically.
Return the result table ordered by sell_date.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| sell_date   | date    |
| product     | varchar |
+-------------+---------+
There is no primary key (column with unique values) for this table. It may contain duplicates.
Each row of this table contains the product name and the date it was sold in a market.
```

**Example 2:**

```
Input: 
Activities table:
+------------+------------+
| sell_date  | product     |
+------------+------------+
| 2020-05-30 | Headphone  |
| 2020-06-01 | Pencil     |
| 2020-06-02 | Mask       |
| 2020-05-30 | Basketball |
| 2020-06-01 | Bible      |
| 2020-06-02 | Mask       |
| 2020-05-30 | T-Shirt    |
+------------+------------+
Output: 
+------------+----------+------------------------------+
| sell_date  | num_sold | products                     |
+------------+----------+------------------------------+
| 2020-05-30 | 3        | Basketball,Headphone,T-shirt |
| 2020-06-01 | 2        | Bible,Pencil                 |
| 2020-06-02 | 1        | Mask                         |
+------------+----------+------------------------------+
Explanation: 
For 2020-05-30, Sold items were (Headphone, Basketball, T-shirt), we sort them lexicographically and separate them by a comma.
For 2020-06-01, Sold items were (Pencil, Bible), we sort them lexicographically and separate them by a comma.
For 2020-06-02, the Sold item is (Mask), we just return it.
```

---

## 题目（中文翻译）

**描述**  
给定表 **Activities**，编写一个查询，找出每个日期（`sell_date`）对应的不同产品（`product`）的数量以及这些产品的名称。  
每个日期的产品名称需要按字典序（lexicographically）排序。  
返回的结果表按 `sell_date` 升序排列。  
结果格式参考下方示例。

**示例 1**  

| Column Name | Type    |
|-------------|---------|
| sell_date   | date    |
| product     | varchar |

该表没有主键（primary key，列值唯一），可能包含重复记录。  
表中的每一行记录了某个产品的名称及其在市场上售出的日期。

**示例 2**  

**输入**  

Activities 表：

| sell_date  | product   |
|------------|-----------|
| 2020-05-30 | Headphone |
| 2020-06-01 | Pencil    |
| 2020-06-02 | Mask      |
| 2020-05-30 | Basketball|
| 2020-06-01 | Bible     |
| 2020-06-02 | Mask      |
| 2020-05-30 | T-Shirt   |

**输出**  

| sell_date  | product_count | products                     |
|------------|----------------|------------------------------|
| 2020-05-30 | 3              | Basketball,Headphone,T-Shirt |
| 2020-06-01 | 2              | Bible,Pencil                 |
| 2020-06-02 | 1              | Mask                         |

**解释**  
- 2020‑05‑30 共售出 3 种不同的产品，分别是 `Basketball`、`Headphone`、`T-Shirt`，按字典序排列后输出。  
- 2020‑06‑01 共售出 2 种不同的产品，分别是 `Bible`、`Pencil`。  
- 2020‑06‑02 虽然出现了两条 `Mask` 记录，但只算作一种产品。  

**约束条件**  
- 表中可能包含重复行。  
- `sell_date` 为 `date` 类型，`product` 为 `varchar` 类型。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. **遍历所有日期**，把出现过的日期全部挑出来（可以用一个列表存所有日期，再 `set` 去重）。  
2. 对于每一个日期，再 **遍历整张表**，把这一天出现的商品全部收集起来。  
3. 用 `set` 去掉重复的商品名称（因为同一天可能卖了同一种商品多次），随后把商品名称 **排序**（字典序），最后统计商品种类数。

> 类比：把整张表想成一本日记本，第一遍把所有出现的日期记下来（相当于先做目录），第二遍再翻回去，针对每个目录项（日期）把对应的商品写在一起。

这种做法一定能得到正确答案，因为我们没有遗漏任何行，也没有漏掉任何日期。

#### 代码（Python）

```python
from typing import List, Tuple

def group_sold_products_bruteforce(activities: List[Tuple[str, str]]) -> List[Tuple[str, int, str]]:
    """
    暴力解法
    :param activities: List[(sell_date, product)]，模拟表中的每一行
    :return: List[(sell_date, product_cnt, product_names)]，按题目要求返回
    """
    # 1. 收集所有出现的日期
    dates = [row[0] for row in activities]          # 把所有日期拿出来
    unique_dates = sorted(set(dates))               # 去重并排序，保证最终结果按日期升序

    result = []
    for d in unique_dates:                          # 对每一个日期做一次全表扫描
        products_of_day = []                         # 用来暂存该日期的所有商品
        for row in activities:                       # 再遍历一次整张表
            if row[0] == d:                          # 找到同一天的记录
                products_of_day.append(row[1])      # 收集商品名

        # 去重、排序
        unique_products = sorted(set(products_of_day))   # set 去重，sorted 按字典序排序
        product_cnt = len(unique_products)                # 商品种类数
        product_names = ','.join(unique_products)         # 按要求拼成字符串

        result.append((d, product_cnt, product_names))

    return result
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层遍历每个唯一日期（最坏情况下有 `n` 个不同日期），内层又要遍历整张表 `n` 行，所以总共要做大约 `n × n` 次比较。  
- **空间复杂度**：`O(n)`  
  解释：我们需要保存所有唯一日期（最多 `n` 个）以及临时的商品集合，都是和输入规模线性相关的。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“对每个日期都要再遍历一次整张表”**，这会导致二次扫描。  
我们可以在 **一次遍历** 中把信息全部收集好，再统一处理：

1. **一次遍历** 把每一行的 `(date, product)` 放进一个字典 `date → set(product)` 中。  
   - 这里的字典相当于 “日期 → 商品集合”。  
   - `set` 自动去重，就像把每一天的商品放进一个不允许重复的背包里。  
2. 遍历完后，**对字典的键（日期）进行排序**，因为返回结果要求按日期升序。  
3. 对每个日期对应的商品集合，先 **排序**（字典序），再统计数量并拼接成字符串。

这样只需要 **一次线性扫描**（`O(n)`），随后对每个日期的商品集合进行排序。若每一天的商品数目总体上仍是 `n`，则总的排序成本为 `O(n log n)`（因为所有商品最终会被排序一次），整体复杂度是 `O(n log n)`。

> 类比：把所有商品先“装进不同抽屉（日期）”，每个抽屉里只能放不同的商品（用 `set`），等所有东西都放好后，再把抽屉排好顺序，打开抽屉把商品排好顺序摆出来。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Tuple

def group_sold_products_optimal(activities: List[Tuple[str, str]]) -> List[Tuple[str, int, str]]:
    """
    最优解：一次遍历 + 哈希表（字典） + 集合去重
    :param activities: List[(sell_date, product)]
    :return: List[(sell_date, product_cnt, product_names)]
    """
    # 1. 用 defaultdict(set) 建立 “日期 → 商品集合” 的映射
    date_to_products = defaultdict(set)   # 第一次出现某个日期时自动创建空集合

    for sell_date, product in activities:   # 只遍历一次
        date_to_products[sell_date].add(product)   # 自动去重

    # 2. 按日期升序遍历字典的键
    result = []
    for d in sorted(date_to_products.keys()):   # sorted 对键进行字典序/日期顺序排序
        products = sorted(date_to_products[d])  # 对该日期的商品集合再排序
        product_cnt = len(products)
        product_names = ','.join(products)
        result.append((d, product_cnt, product_names))

    return result
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `O(n)` 用于一次遍历把数据放进字典。  
  - `sorted(date_to_products.keys())` 需要对所有不同日期排序，最多 `n` 个，时间 `O(k log k)`（`k` 为不同日期数）。  
  - 对每个日期的商品集合进行 `sorted`，所有商品总体仍是 `n` 条记录，所以总体排序成本为 `O(n log n)`。  
  与暴力解的 `O(n²)` 相比，规模稍大的数据集会快很多。

- **空间复杂度**：`O(n)`  
  - 字典里保存了每条记录对应的商品（去重后），最坏情况每条记录都是唯一的，仍然需要 `O(n)` 空间。

---

## 心得

- **核心技巧**：利用哈希表（字典）把“相同键的记录聚合”起来，再配合集合去重和排序。  
- **适用的题型**  
  1. “按某列分组统计不同值” 类题，例如 **Group Customers By Country**。  
  2. “按日期聚合事件并去重” 类题，例如 **User Visits Per Day**。  
  3. “把相同键的字符串合并并排序” 类题，例如 **Concat Names By Department**。  
- **一句话总结解题钥匙**：**一次遍历把数据聚合进字典/集合，最后统一排序输出**。

---

## 反思

- **第一反应**：直接把每个日期的商品全部列出来，然后手动去重、排序——这就是暴力思路。  
- **最容易踩的坑**  
  - **重复记录**：同一天同一种商品可能出现多次，必须用 `set` 去重，否则统计会出错。  
  - **排序要求**：商品名称要按字典序排序，忘记排序会导致答案不匹配。  
  - **返回顺序**：结果表必须按 `sell_date` 升序排列，忘记对日期排序会导致 WA。  
- **下次遇到同类题**：第一步立刻想到 “用字典把相同键的行聚合”，然后决定是否需要集合去重或列表排序。这样就能避免二次遍历的低效写法。