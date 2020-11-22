# #1070. 产品销售分析 III / Product Sales Analysis III

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/product-sales-analysis-iii/)

---

## 题目（英文原版）

**Description**

Table: Sales
Write a solution to find all sales that occurred in the first year each product was sold.
Return a table with the following columns: product_id, first_year, quantity, and price.
Return the result in any order.

**Examples**

**Example 1:**

```
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
(sale_id, year) is the primary key (combination of columns with unique values) of this table.
product_id is a foreign key (reference column) to Product table.
Each row records a sale of a product in a given year.
A product may have multiple sales entries in the same year.
Note that the per-unit price.
```

**Example 2:**

```
Input: 
Sales table:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+ 
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+

Output: 
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+ 
| 100        | 2008       | 10       | 5000  |
| 200        | 2011       | 15       | 9000  |
+------------+------------+----------+-------+
```

---

## 题目（中文翻译）

编写一个查询，找出每种产品首次出现销售的那一年对应的所有销售记录。  
返回的结果表包含以下列：`product_id`、`first_year`、`quantity` 和 `price`。  
结果顺序不限。

**表结构**  

```
Table: Sales
+-------------+-------+
| Column Name | Type  |
+-------------+-------+
| sale_id     | int   |
| product_id  | int   |
| year        | int   |
| quantity    | int   |
| price       | int   |
+-------------+-------+
```

- `(sale_id, year)` 是该表的主键（primary key），即唯一标识每行记录的列组合。  
- `product_id` 是指向 `Product` 表的外键（foreign key），用于关联产品信息。  
- 每行记录了某产品在特定年份的销售情况。  
- 同一产品在同一年可能有多条销售记录。  
- 注意每单位的价格（price）是以整数形式存储的。

**示例 1**

```
Input:
Sales 表:
+---------+------------+------+----------+-------+
| sale_id | product_id | year | quantity | price |
+---------+------------+------+----------+-------+
| 1       | 100        | 2008 | 10       | 5000  |
| 2       | 100        | 2009 | 12       | 5000  |
| 7       | 200        | 2011 | 15       | 9000  |
+---------+------------+------+----------+-------+

Output:
+------------+------------+----------+-------+
| product_id | first_year | quantity | price |
+------------+------------+----------+-------+
| 100        | 2008       | 10       | 5000  |
| 200        | 2011       | 15       | 9000  |
+------------+------------+----------+-------+
```

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：  

1. 对每一条销售记录 `r`，找出 **同一商品**（`product_id` 相同）的所有记录。  
2. 在这些记录里找到最小的 `year`，这就是该商品的 **first_year**。  
3. 再把 `r` 的 `year` 与它对应的 **first_year** 比较，若相等就把这条记录加入答案。  

> **数据结构类比**  
> - 把整张表想成一本《销售日志》，每一行是一本日志的页码。  
> - 想找某本商品的第一年，就像在一本字典里查找某个词的首字母页码，需要把所有页码都翻一遍才能确定最小的页码。  

这种做法一定能得到正确答案，因为我们把每个商品所有的年份都检查了一遍，必然能找到最早的那一年。  

#### 代码（Python）  

```python
# 假设 sales 是一个列表，每个元素是字典，表示一条记录
# 示例：sales = [{'sale_id': 1, 'product_id': 100, 'year': 2008,
#                'quantity': 10, 'price': 5000}, ... ]

def brute_force(sales):
    """暴力解：O(n²) 时间，O(1) 额外空间"""
    ans = []                         # 用来存放最终结果
    n = len(sales)

    for i in range(n):               # 遍历每一条记录 r_i
        cur = sales[i]
        pid = cur['product_id']

        # 1️⃣ 找到同一商品的所有记录，计算最小年份
        min_year = cur['year']       # 先把自己当成最小值
        for j in range(n):           # 再遍历整张表寻找更小的年份
            if sales[j]['product_id'] == pid:
                min_year = min(min_year, sales[j]['year'])

        # 2️⃣ 若当前记录的年份就是该商品的 first_year，就加入答案
        if cur['year'] == min_year:
            ans.append({
                'product_id': pid,
                'first_year': min_year,
                'quantity'  : cur['quantity'],
                'price'     : cur['price']
            })
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环遍历 `n` 条记录，内层又要遍历全部 `n` 条记录去找最小年份，`n × n` 就是 `n²`。  
  - 用大白话说，就是“每条记录都要和所有记录比较一次”，如果有 10,000 条数据，就要比较 100,000,000 次，明显慢。  

- **空间复杂度**：`O(1)`（不计返回结果的空间）  
  - 只用了几个临时变量，和输入规模无关。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈**在于每次都要遍历整张表去找同一商品的最小年份。  
其实我们只需要 **一次遍历** 就能把每个商品的最早年份记下来：  

1. 用一个字典 `first_year_map`，键是 `product_id`，值是该商品目前已知的最小 `year`。  
   - 第一次看到某个商品时，直接把它的 `year` 放进去。  
   - 再次看到同商品时，用 `min` 与字典里保存的年份比较，更新为更小的那一个。  
   - 这一步相当于“在字典里查词条的页码”，查找和更新都是 **O(1)**，所以整体是 **O(n)**。  

2. 第一次遍历结束后，`first_year_map` 已经完整地保存了每个商品的 **first_year**。  

3. 再遍历一次原表，把 `year == first_year_map[product_id]` 的记录挑出来，即为答案。  

> **核心数据结构：哈希表（字典）**  
> - 哈希表就像一本“随身词典”，把商品编号当作“单词”，把对应的最早年份当作“页码”。  
> - 查找或插入一个单词，只需要“一下子”定位到对应的页码，时间是常数级 `O(1)`。  

#### 代码（Python）  

```python
def optimal(sales):
    """最优解：O(n) 时间，O(k) 空间（k 为不同商品的数量）"""
    # 1️⃣ 第一次遍历：收集每个商品的最小年份
    first_year_map = {}                     # product_id -> first_year
    for rec in sales:
        pid = rec['product_id']
        yr  = rec['year']
        # 如果之前没有出现过，直接记下来；否则取更小的年份
        if pid not in first_year_map:
            first_year_map[pid] = yr
        else:
            # min 是取两个数中较小的那个
            first_year_map[pid] = min(first_year_map[pid], yr)

    # 2️⃣ 第二次遍历：挑选出 first_year 对应的记录
    ans = []
    for rec in sales:
        pid = rec['product_id']
        if rec['year'] == first_year_map[pid]:   # 正好是该商品的第一年
            ans.append({
                'product_id': pid,
                'first_year': first_year_map[pid],
                'quantity'  : rec['quantity'],
                'price'     : rec['price']
            })
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 解释：我们只做了两次线性扫描，遍历的次数是 `n + n = 2n`，在“大 O”记号里常数 2 被忽略，剩下 `O(n)`。  
  - 与暴力解相比，省掉了 “每条记录都要和所有记录比较一次” 的那一步，速度提升明显。  

- **空间复杂度**：`O(k)`，其中 `k` 为不同 `product_id` 的数量  
  - 解释：我们额外用了一个字典来存每个商品的最早年份，字典的大小正好等于商品种类数。  
  - 如果商品种类和记录数差不多，这相当于 `O(n)`，但一般商品种类远小于总记录数，空间占用可接受。  

---  

## 心得  

- **核心技巧**：**哈希表（字典）一次遍历求最小值**，再利用该映射过滤数据。  
- **适用的题型**  
  1. “每个用户的首次登录时间” → 先记录每个用户的最早 timestamp。  
  2. “每种商品的最高评分” → 用字典维护每种商品的最大 rating。  
  3. “每个部门的最早入职员工” → 类似思路，只是存放员工 ID 或姓名。  

> **一句话总结**：先用哈希表把“每类对象的极值”算出来，再一次遍历即可得到对应的完整记录。  

---  

## 反思  

- **第一反应**：看到“每个商品的第一年”，本能想到“对每个商品找最小的 year”。于是直接写了两层循环的暴力实现。  
- **最容易踩的坑**  
  1. **同一年有多条记录**：题目说明同一商品同一年可能有多条销售，需要把**所有**这些记录都返回，而不是只挑一条。  
  2. **字典的初始化**：忘记在第一次遇到商品时写入字典，会导致后续 `min` 操作报错。  
  3. **返回列的顺序**：答案要求列名是 `product_id, first_year, quantity, price`，代码里一定要保持这个顺序，否则在实际提交时会因列名不匹配而错误。  

- **下次遇到类似题目**，第一步应该先**思考如何用一次遍历把“极值信息”收集起来**（比如最小/最大/出现次数），再利用这个信息进行过滤或统计，而不是直接套用双层循环。这样既能保证正确性，也能大幅提升效率。