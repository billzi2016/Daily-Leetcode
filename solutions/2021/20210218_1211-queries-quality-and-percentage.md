# #1211. 查询质量与比例 / Queries Quality and Percentage

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/queries-quality-and-percentage/)

---

## 题目（英文原版）

**Description**

Table: Queries
We define query quality as:
We also define poor query percentage as:
Write a solution to find each query_name, the quality and poor_query_percentage.
Both quality and poor_query_percentage should be rounded to 2 decimal places.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| query_name  | varchar |
| result      | varchar |
| position    | int     |
| rating      | int     |
+-------------+---------+
This table may have duplicate rows.
This table contains information collected from some queries on a database.
The position column has a value from 1 to 500.
The rating column has a value from 1 to 5. Query with rating less than 3 is a poor query.
```

**Example 2:**

```
Input: 
Queries table:
+------------+-------------------+----------+--------+
| query_name | result            | position | rating |
+------------+-------------------+----------+--------+
| Dog        | Golden Retriever  | 1        | 5      |
| Dog        | German Shepherd   | 2        | 5      |
| Dog        | Mule              | 200      | 1      |
| Cat        | Shirazi           | 5        | 2      |
| Cat        | Siamese           | 3        | 3      |
| Cat        | Sphynx            | 7        | 4      |
+------------+-------------------+----------+--------+
Output: 
+------------+---------+-----------------------+
| query_name | quality | poor_query_percentage |
+------------+---------+-----------------------+
| Dog        | 2.50    | 33.33                 |
| Cat        | 0.66    | 33.33                 |
+------------+---------+-----------------------+
Explanation: 
Dog queries quality is ((5 / 1) + (5 / 2) + (1 / 200)) / 3 = 2.50
Dog queries poor_ query_percentage is (1 / 3) * 100 = 33.33

Cat queries quality equals ((2 / 5) + (3 / 3) + (4 / 7)) / 3 = 0.66
Cat queries poor_ query_percentage is (1 / 3) * 100 = 33.33
```

---

## 题目（中文翻译）

表：Queries  
我们定义查询质量（query quality）为：  
（此处给出公式）  

我们也定义低质量查询比例（poor query percentage）为：  
（此处给出公式）  

编写一个查询，找出每个 `query_name` 对应的质量（quality）和低质量查询比例（poor_query_percentage）。  
`quality` 和 `poor_query_percentage` 均需四舍五入保留两位小数。  
返回结果表，顺序任意。结果格式参照下面示例。

**示例 1**

```sql
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| query_name  | varchar |
| result      | varchar |
| position    | int     |
| rating      | int     |
+-------------+---------+
```

- 该表可能存在重复行。  
- 该表记录了若干对数据库的查询信息。  
- `position` 列的取值范围为 1 到 500。  
- `rating` 列的取值范围为 …（题目中给出的取值范围）。

**示例 2**

输入：

```
Queries 表：
+------------+-------------------+----------+--------+
| query_name | result            | position | rating |
+------------+-------------------+----------+--------+
| Dog        | Golden Retriever  | 1        | 5      |
| Dog        | German Shepherd   | 2        | 5      |
| Dog        | Mule              | 200      | 1      |
| Cat        | Shirazi           | 5        | 2      |
...
```

（后续数据省略）

**约束条件**

- 无

**返回结果示例**

（示例输出保持原样，只翻译说明部分）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求 **对每一种 `query_name`** 计算两件事：

1. **quality**：所有记录的 `rating` 的平均值。  
2. **poor_query_percentage**：`rating` 小于等于 2 的记录占该 `query_name` 总记录数的比例（乘以 100%），并保留两位小数。

最直接的做法是：

- 先把表里的所有行读取进一个 Python 列表 `rows`（每行可以是一个元组或字典）。  
- 对于列表中的每一种 `query_name`，**逐行遍历**，把属于该 `query_name` 的记录挑出来，手动累加 `rating`、计数、以及 “差查询” 的计数。  
- 计算完后再除以总数得到平均值和比例，使用 `round(..., 2)` 保留两位小数。

这就像在超市里 **一次只挑一种商品**，把所有货架上该商品的价格一个个记下来，再算平均价和差评比例。  

> **为什么这样一定能得到正确答案**  
> 因为我们没有遗漏任何一行，也没有对数据做任何近似，直接按照题目定义的公式算，必然和官方答案一致。

**时间/空间复杂度的大白话解释**  

- **时间复杂度**：假设表里有 `N` 行，`M` 种不同的 `query_name`。对每一种 `query_name` 我们都要遍历一次完整的表，所以总共要跑 `M × N` 次检查。最坏情况下每种名字几乎都不相同，`M` 接近 `N`，于是时间复杂度约为 **O(N²)**。可以把它想象成“把一张纸上的每个字都和每行都比一遍”，显然会很慢。  
- **空间复杂度**：我们只用到了原始的 `rows` 列表（题目已经给出），再加上几个计数器和结果列表，和 `N` 成正比，所以是 **O(N)**，即占用的额外空间与数据量线性相关。

#### 代码（Python）

```python
# ---------- 暴力解 ----------
# 假设已经把 Queries 表读取为下面的列表，每个元素是一个字典
# rows = [
#     {"query_name": "Dog", "result": "Golden Retriever", "position": 1, "rating": 5},
#     {"query_name": "Dog", "result": "German Shepherd",  "position": 2, "rating": 5},
#     {"query_name": "Dog", "result": "Mule",            "position": 200, "rating": 1},
#     {"query_name": "Cat", "result": "Shirazi",        "position": 5, "rating": 2},
#     ...
# ]

def brute_force(rows):
    # 先收集所有出现过的 query_name
    names = set(row["query_name"] for row in rows)

    result = []                     # 最终要返回的列表
    for name in names:              # 对每一种 query_name 做一次完整遍历
        total_rating = 0            # rating 的累计和
        total_cnt = 0               # 该 query_name 的记录总数
        poor_cnt = 0                # rating <= 2 的记录数

        for row in rows:            # 暴力遍历整张表
            if row["query_name"] == name:   # 只处理当前名字的行
                total_rating += row["rating"]
                total_cnt += 1
                if row["rating"] <= 2:      # “差查询”的判定
                    poor_cnt += 1

        # 计算平均质量和差查询百分比，保留两位小数
        quality = round(total_rating / total_cnt, 2)
        poor_percentage = round(100.0 * poor_cnt / total_cnt, 2)

        result.append({
            "query_name": name,
            "quality": quality,
            "poor_query_percentage": poor_percentage
        })
    return result
```

#### 复杂度

- **时间复杂度**：O(N²) —— 对每一种 `query_name` 都要遍历一遍完整的表。  
- **空间复杂度**：O(N) —— 只额外存放了一个结果列表，和输入规模线性相关。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 出在「每次都遍历整张表」。  
如果我们在 **一次遍历** 中就把所有需要的统计信息收集好，后面再一次性算出平均值和比例，就可以把时间降到线性。

这正好可以使用 **哈希表（Python 的 dict）** 来累计每个 `query_name` 的信息：

- 键（key）是 `query_name`。  
- 值（value）是一个小列表/元组，保存三个累计量：  
  1. `sum_rating`（rating 总和）  
  2. `total_cnt`（总记录数）  
  3. `poor_cnt`（rating ≤ 2 的记录数）

遍历一次 `rows`，对每行：

1. 取出它的 `query_name`，在 dict 中若不存在就创建初始值 `[0,0,0]`。  
2. 把 `rating` 加到 `sum_rating`，`total_cnt` 加 1。  
3. 如果 `rating ≤ 2`，`poor_cnt` 再加 1。

遍历结束后，dict 已经包含了所有所需的累计信息。我们再遍历 dict 的键值对，**一次性算出**：

- `quality = round(sum_rating / total_cnt, 2)`  
- `poor_query_percentage = round(100.0 * poor_cnt / total_cnt, 2)`

这样只用了 **一次遍历**（O(N)）的时间，空间只需要保存每个不同 `query_name` 的三个整数（O(M)，M ≤ N）。

> **哈希表的类比**  
> 想象我们在整理图书馆的书籍时，拿出一本登记簿（字典），每遇到一本新书，就在册子里写下它的标题（key）以及累计的页数、数量、破损本数等信息（value）。这样我们不需要每本书都去翻遍整个书架，只要把信息写进册子里，最后再算平均页数即可。

#### 代码（Python）

```python
# ---------- 最优解 ----------
def optimal_solution(rows):
    """
    使用一次遍历 + 哈希表统计，时间 O(N)，空间 O(M)（M 为不同的 query_name 数目）
    """
    # 第一步：收集统计信息
    stats = {}   # key: query_name, value: [sum_rating, total_cnt, poor_cnt]

    for row in rows:
        name = row["query_name"]
        rating = row["rating"]

        # 若是第一次出现该 query_name，初始化累计数组
        if name not in stats:
            stats[name] = [0, 0, 0]   # [sum_rating, total_cnt, poor_cnt]

        # 累计 rating 总和和记录数
        stats[name][0] += rating          # sum_rating
        stats[name][1] += 1               # total_cnt

        # 统计 rating <= 2 的“差查询”数量
        if rating <= 2:
            stats[name][2] += 1           # poor_cnt

    # 第二步：根据累计信息计算最终结果
    result = []
    for name, (sum_rating, total_cnt, poor_cnt) in stats.items():
        quality = round(sum_rating / total_cnt, 2)               # 平均 rating
        poor_percentage = round(100.0 * poor_cnt / total_cnt, 2) # 差查询占比
        result.append({
            "query_name": name,
            "quality": quality,
            "poor_query_percentage": poor_percentage
        })
    return result
```

#### 复杂度

- **时间复杂度**：O(N) —— 只遍历一次原始数据表。  
  与暴力解的 O(N²) 相比，**快了 N 倍**，即使数据量上万行也能毫秒级完成。  
- **空间复杂度**：O(M) —— 只保存每个不同 `query_name` 的三个计数器。  
  M 最多等于 N（每行都是唯一名字），但通常会远小于 N，属于线性空间。

---

## 心得

- **核心技巧**：一次遍历 + 哈希表累计（也叫“分组聚合”）。  
- **适用场景**：  
  1. **求每组的平均值、总和、计数**（如 LeetCode “Employee Bonus”）。  
  2. **统计每组的特定条件比例**（如 “User Activity Percent”）。  
  3. **分组求最大/最小值**（如 “Highest Salary per Department”）。  
- **一句话总结**：**把“把相同名字的行放进同一个抽屉”这件事在遍历时一次性完成，抽屉里记下累计信息，最后再算平均和比例**。

---

## 反思

- **第一反应**：看到 “每个 query_name 的质量和差查询百分比”，立刻想到 **SQL 中的 GROUP BY**，于是先把思路转成 Python 的分组聚合。  
- **最容易踩的坑**  
  1. **除零错误**：如果某个 `query_name` 的记录数为 0（理论上不可能，但在手写测试时要防御），要先检查 `total_cnt > 0`。  
  2. **小数位数**：`round(..., 2)` 会四舍五入到两位小数，但要确保 **先乘以 100 再除**，否则会得到 0~1 之间的小数而不是百分比。  
  3. **数据类型**：`rating` 是整数，除法会得到浮点数，记得使用 `100.0` 强制浮点除法，防止 Python 2（已不常用）出现整数除法。  
- **下次遇到同类题**：**第一步先决定用哈希表“一次遍历统计”，再根据题目要求在统计完后进行计算**。这样可以直接把时间复杂度从 O(N²) 降到 O(N)。