# #595. 大国家 / Big Countries

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/big-countries/)

---

## 题目（英文原版）

**Description**

Table: World
A country is big if:
Write a solution to find the name, population, and area of the big countries.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| name        | varchar |
| continent   | varchar |
| area        | int     |
| population  | int     |
| gdp         | bigint  |
+-------------+---------+
name is the primary key (column with unique values) for this table.
Each row of this table gives information about the name of a country, the continent to which it belongs, its area, the population, and its GDP value.
```

**Example 2:**

```
Input: 
World table:
+-------------+-----------+---------+------------+--------------+
| name        | continent | area    | population | gdp          |
+-------------+-----------+---------+------------+--------------+
| Afghanistan | Asia      | 652230  | 25500100   | 20343000000  |
| Albania     | Europe    | 28748   | 2831741    | 12960000000  |
| Algeria     | Africa    | 2381741 | 37100000   | 188681000000 |
| Andorra     | Europe    | 468     | 78115      | 3712000000   |
| Angola      | Africa    | 1246700 | 20609294   | 100990000000 |
+-------------+-----------+---------+------------+--------------+
Output: 
+-------------+------------+---------+
| name        | population | area    |
+-------------+------------+---------+
| Afghanistan | 25500100   | 652230  |
| Algeria     | 37100000   | 2381741 |
+-------------+------------+---------+
```

---

## 题目（中文翻译）

**描述**  
表（table）：`World`  
`World` 表包含以下列（column）：

- `name`（varchar）  
- `continent`（varchar）  
- `area`（int）  
- `population`（int）  
- `gdp`（bigint）

其中 `name` 为主键（primary key），即每行的国家名称唯一。

如果一个国家满足以下任意条件，则称其为 **大国家**（big country）：

- `area` 大于 3000000（单位：平方公里）  
- `population` 大于 25000000（单位：人口）

请编写 SQL 语句，找出所有大国家的 `name`、`population` 和 `area`，并返回结果表（result table）。返回的行顺序任意。

**示例 1**  

```sql
World 表结构
+-------------+----------+------+------------+--------------+
| name        | continent| area | population | gdp          |
+-------------+----------+------+------------+--------------+
| Afghanistan | Asia     | 652230| 25500100  | 20343000000 |
| Albania     | Europe   | 28748 | 2831741   | 12960000000 |
| Algeria     | Africa   | 2381741| 37100000 | 188681000000|
| Andorra     | Europe   | 468   | 78115     | 3712000000  |
| Angola      | Africa   |1246700| 20609294  | 100990000000|
+-------------+----------+------+------------+--------------+
```

**输出**  

```sql
+-------------+------------+--------+
| name        | population | area   |
+-------------+------------+--------+
| Afghanistan | 25500100   | 652230 |
| Algeria     | 37100000   |2381741 |
+-------------+------------+--------+
```

**解释**  
`Afghanistan`（人口 25500100）和 `Algeria`（面积 2381741，人口 37100000）满足“大国家”的判定条件（面积 > 3000000 或人口 > 25000000），因此在结果中被返回。其他国家均不满足条件。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把 **World** 表的每一行都拿出来检查一次：  

1. 读取整张表（相当于把所有国家的信息装进一个大列表）。  
2. 对每一条记录，判断它的 `area`（面积）是否大于 **3 000 000**，或者 `population`（人口）是否大于 **25 000 000**。  
3. 满足条件的记录就把 `name、population、area` 三个字段保存下来，最后一次性返回。  

> **数据结构类比**：  
> - 表格里的每一行就像字典里的一个 **键值对**，键是列名，值是对应的数值。  
> - 把所有行装进列表，就像把一本电话簿全部翻开，准备逐条查找。  

> **为什么正确**：  
> 条件 “面积大于 3 000 000 **或** 人口大于 25 000 000” 是对每条记录的独立判定，只要遍历到这条记录，就能立刻知道它是否符合要求。遍历完所有记录后，所有符合条件的记录自然都被收集到了。

#### 代码（Python）  
下面用 `sqlite3`（Python 标准库自带的轻量级数据库）来演示完整的 **暴力** 实现。代码中每一行都加了中文注释，方便理解。

```python
import sqlite3
from typing import List, Tuple

# ---------- 1. 准备演示用的数据库 ----------
def init_db() -> sqlite3.Connection:
    """
    创建内存数据库并插入示例数据，返回连接对象。
    实际面试时，这一步已经有了现成的 World 表，这里仅作演示。
    """
    conn = sqlite3.connect(":memory:")          # 在内存里开一个临时数据库
    cur = conn.cursor()
    # 建表
    cur.execute("""
        CREATE TABLE World (
            name        TEXT PRIMARY KEY,
            continent   TEXT,
            area        INTEGER,
            population  INTEGER,
            gdp         BIGINT
        )
    """)
    # 插入示例数据（可以自行添加更多行以测试）
    sample = [
        ("Afghanistan", "Asia",   652230,   25500100, 20343000000),
        ("Albania",      "Europe", 28748,    2831741,  12960000000),
        ("Algeria",      "Africa", 2381741,  37100000, 188681000000),
        ("Andorra",      "Europe", 468,      78115,    3712000000),
        ("Angola",       "Africa", 1246700,  20609294, 100990000000),
    ]
    cur.executemany(
        "INSERT INTO World (name, continent, area, population, gdp) VALUES (?,?,?,?,?)",
        sample,
    )
    conn.commit()
    return conn


# ---------- 2. 暴力解 ----------
def big_countries_bruteforce(conn: sqlite3.Connection) -> List[Tuple[str, int, int]]:
    """
    逐行遍历 World 表，手动判断面积或人口是否满足“大国”条件。
    返回 (name, population, area) 的列表。
    """
    cur = conn.cursor()
    # 读取所有记录一次性放进 Python 列表（相当于把整本电话簿搬到桌面上）
    cur.execute("SELECT name, population, area FROM World")
    all_rows = cur.fetchall()                     # List[Tuple[str, int, int]]

    result = []                                   # 用来收集符合条件的国家
    for name, population, area in all_rows:       # 逐条检查
        # 条件：面积 > 3,000,000 或者 人口 > 25,000,000
        if area > 3_000_000 or population > 25_000_000:
            result.append((name, population, area))
    return result


# ---------- 3. 演示 ----------
if __name__ == "__main__":
    conn = init_db()
    ans = big_countries_bruteforce(conn)
    print("Big countries (brute force):")
    for row in ans:
        print(row)
```

> **运行结果**（对应示例数据）  
> ```
> Big countries (brute force):
> ('Afghanistan', 25500100, 652230)
> ('Algeria', 37100000, 2381741)
> ```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 这里的 `n` 是表中记录的条数。我们必须把每一行都看一遍，才能判断它是否“大”。  
  - 用大白话说，就是“遍历一次所有国家”，所以时间会随国家数量线性增长。  
- **空间复杂度**：`O(n)`（取决于实现）  
  - 代码里一次性把全部记录读进 Python 列表，需要额外的存储空间，最坏情况是和表的大小相同。  
  - 如果改成 **边读边判断**（使用 `cursor.fetchone()` 循环），就可以把空间降到 `O(1)`，即只保存常数个临时变量。

---

### 2. 最优解  

#### 思路  
从暴力解我们已经知道瓶颈只在 **遍历**，而遍历本身是不可避免的（必须检查每条记录）。  
真正的“优化”在于 **让数据库自己完成过滤**，而不是把所有数据搬到 Python 再手动筛选。  

- **慢点**：把所有行拉到 Python 再判断，等价于把电话簿全部抄在纸上，再用放大镜逐条检查，效率低。  
- **优化**：把筛选条件直接写进 SQL 的 `WHERE` 子句，让 SQLite 在内部完成过滤，只把符合条件的记录送回 Python。这样可以省掉大量无用的数据传输和 Python 循环。

核心技术就是 **SQL 的 SELECT + WHERE**。这里不需要额外的数据结构，只要把条件表达清楚即可。  

> **类比**：  
> 想象你在图书馆找一本特定主题的书，直接让图书管理员在系统里检索（相当于 SQL），比你自己把所有书都搬到桌子上再挑要快得多。

#### 代码（Python）  
下面的实现仍然使用 `sqlite3`，但所有过滤工作交给了 SQL。

```python
import sqlite3
from typing import List, Tuple

def big_countries_optimal(conn: sqlite3.Connection) -> List[Tuple[str, int, int]]:
    """
    直接在 SQL 中写过滤条件，只返回满足“大国”要求的记录。
    返回 (name, population, area) 的列表，顺序不固定。
    """
    cur = conn.cursor()
    # SELECT 只取需要的列，WHERE 把过滤条件交给数据库引擎
    query = """
        SELECT name, population, area
        FROM World
        WHERE area > 3000000        -- 面积大于 3,000,000
           OR population > 25000000 -- 人口大于 25,000,000
    """
    cur.execute(query)
    return cur.fetchall()   # 直接得到过滤后的结果列表


# ---------- 演示 ----------
if __name__ == "__main__":
    # 这里直接复用前面的初始化函数
    conn = init_db()
    ans = big_countries_optimal(conn)
    print("Big countries (optimal):")
    for row in ans:
        print(row)
```

> **运行结果**（与暴力解一致）  
> ```
> Big countries (optimal):
> ('Afghanistan', 25500100, 652230)
> ('Algeria', 37100000, 2381741)
> ```

#### 复杂度  
- **时间复杂度**：`O(k)`（其中 `k` 是满足条件的记录数）  
  - 数据库内部仍然需要遍历整张表，但它在 C 语言层面完成，且只把符合条件的 `k` 条记录返回给 Python。对 Python 来说，处理的工作量是 `k`，而不是 `n`。  
  - 用大白话说，就是“只把符合条件的国家送到你手里”。  
- **空间复杂度**：`O(k)`  
  - 只保存最终返回的符合条件的记录。相较于暴力解的 `O(n)`，在大表且符合条件少的情况下，显著节省内存。

---

## 心得  

- **核心技巧**：把过滤条件下推到数据库（SQL `WHERE`），让数据库引擎负责“大规模遍历”。  
- **适用题型**：  
  1. **过滤查询**：如 “查询工资大于 10 万的员工”。  
  2. **聚合前置过滤**：如 “统计人口超过 1 亿的国家的平均面积”。  
  3. **多表连接后过滤**：如 “找出订单金额大于 1000 的客户”。  
- **一句话总结**：**把“筛”交给数据库，程序只负责“收”。**

---

## 反思  

- **第一反应**：把所有数据读出来，用 Python 循环判断。  
- **最容易踩的坑**：  
  - 忘记在 `WHERE` 中使用 `OR`（导致只保留面积大的或只保留人口大的）。  
  - 忽视列名大小写或拼写错误，导致查询报错。  
  - 对返回顺序有误解：题目说明“任意顺序”即可，不必额外 `ORDER BY`。  
- **下次类似题目**：  
  1. **先想 SQL 能直接完成的过滤**，把条件写进 `WHERE`。  
  2. **确认只取需要的列**（`SELECT name, population, area`），避免不必要的数据传输。  
  3. **如果还有聚合或排序需求，再在 SQL 中继续完成**。