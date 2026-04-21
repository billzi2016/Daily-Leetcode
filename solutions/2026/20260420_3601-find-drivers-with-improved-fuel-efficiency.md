# #3601. 查找燃油效率提升的司机 / Find Drivers with Improved Fuel Efficiency

> 难度：中等 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/find-drivers-with-improved-fuel-efficiency/)

---

## 题目（英文原版）

**Description**

Table: drivers
Table: trips
Write a solution to find drivers whose fuel efficiency has improved by comparing their average fuel efficiency in the first half of the year with the second half of the year.
Return the result table ordered by efficiency improvement in descending order, then by driver name in ascending order.
The result format is in the following example.
Example:

**Examples**

**Example 1:**

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| driver_id   | int     |
| driver_name | varchar |
+-------------+---------+
driver_id is the unique identifier for this table.
Each row contains information about a driver.
```

**Example 2:**

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| trip_id       | int     |
| driver_id     | int     |
| trip_date     | date    |
| distance_km   | decimal |
| fuel_consumed | decimal |
+---------------+---------+
trip_id is the unique identifier for this table.
Each row represents a trip made by a driver, including the distance traveled and fuel consumed for that trip.
```

**Example 3:**

```
+-----------+---------------+
| driver_id | driver_name   |
+-----------+---------------+
| 1         | Alice Johnson |
| 2         | Bob Smith     |
| 3         | Carol Davis   |
| 4         | David Wilson  |
| 5         | Emma Brown    |
+-----------+---------------+
```

**Example 4:**

```
+---------+-----------+------------+-------------+---------------+
| trip_id | driver_id | trip_date  | distance_km | fuel_consumed |
+---------+-----------+------------+-------------+---------------+
| 1       | 1         | 2023-02-15 | 120.5       | 10.2          |
| 2       | 1         | 2023-03-20 | 200.0       | 16.5          |
| 3       | 1         | 2023-08-10 | 150.0       | 11.0          |
| 4       | 1         | 2023-09-25 | 180.0       | 12.5          |
| 5       | 2         | 2023-01-10 | 100.0       | 9.0           |
| 6       | 2         | 2023-04-15 | 250.0       | 22.0          |
| 7       | 2         | 2023-10-05 | 200.0       | 15.0          |
| 8       | 3         | 2023-03-12 | 80.0        | 8.5           |
| 9       | 3         | 2023-05-18 | 90.0        | 9.2           |
| 10      | 4         | 2023-07-22 | 160.0       | 12.8          |
| 11      | 4         | 2023-11-30 | 140.0       | 11.0          |
| 12      | 5         | 2023-02-28 | 110.0       | 11.5          |
+---------+-----------+------------+-------------+---------------+
```

**Example 5:**

```
+-----------+---------------+------------------+-------------------+------------------------+
| driver_id | driver_name   | first_half_avg   | second_half_avg   | efficiency_improvement |
+-----------+---------------+------------------+-------------------+------------------------+
| 2         | Bob Smith     | 11.24            | 13.33             | 2.10                   |
| 1         | Alice Johnson | 11.97            | 14.02             | 2.05                   |
+-----------+---------------+------------------+-------------------+------------------------+
```

---

## 题目（中文翻译）

表：drivers  
表：trips  

编写一个查询，找出燃油效率（fuel efficiency）在一年前后期有所提升的司机。具体做法是比较该司机在上半年（first half of the year）和下半年（second half of the year）的 **平均燃油效率（average fuel efficiency）**。

返回的 **结果表（result table）** 按效率提升（efficiency improvement）降序排序，若提升相同则按司机姓名（driver name）升序排序。结果格式参考下列示例。

**示例 1**  

```
+-------------+---------+
| Column Name | Type    |
+-------------+---------+
| driver_id   | int     |
| driver_name | varchar |
+-------------+---------+
```
`driver_id` 为该表的唯一标识。每行记录一名司机的信息。

**示例 2**  

```
+---------------+---------+
| Column Name   | Type    |
+---------------+---------+
| trip_id       | int     |
| driver_id     | int     |
| trip_date     | date    |
| distance_km   | decimal |
| fuel_consumed | decimal |
+---------------+---------+
```
`trip_id` 为该表的唯一标识。每行记录一段行程，包括行驶距离和消耗燃油量等信息。

**示例 3**  

```
+-----------+---------------+
| driver_id | driver_name   |
+-----------+---------------+
| 1         | Alice Johnson |
| 2         | Bob Smith     |
| 3         | Carol Davis   |
| 4         | David Wilson  |
| 5         | Emma Brown    |
+-----------+---------------+
```

**示例 4**  

```
+---------+-----------+------------+-------------+---------------+
| trip_id | driver_id | trip_date  | distance_km | fuel_consumed |
+---------+-----------+------------+-------------+---------------+
| 1       | 1         | 2023-02-15 | 120.5       | 10.2          |
| 2       | 1         | 2023-03-20 | 200.0       | 16.5          |
| 3       | 1         | 2023-08-10 | 150.0       | 11.0          |
... (已截断)
```

**示例 5**  

```
+-----------+---------------+------------------+-------------------+------------------------+
| driver_id | driver_name   | first_half_avg   | second_half_avg   | efficiency_improvement |
+-----------+---------------+------------------+-------------------+------------------------+
| 2         | Bob Smith     | 11.24            | 13.33             | 2.10                   |
| 1         | Alice Johnson | ...              | ...               | ...                    |
... (已截断)
```

约束条件：  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **所有行**（即每一次出行记录）都遍历一遍，手动算出每位司机在上半年的平均油耗和下半年的平均油耗，再比较两者的大小。

- **数据结构**：  
  - 用 `defaultdict`（类似于查字典）把 `driver_id` 当作 **key**，对应的 **value** 保存两段时间的累计里程、累计燃油和次数。  
  - “字典”就像我们平时查 **词典**，键（key）是单词，值（value）是解释。这里键是司机的编号，值是用来算平均值的累加器。

- **为什么正确**：  
  - 对每条出行记录，我们只要判断它的日期落在 1~6 月还是 7~12 月，就把对应的里程和燃油加入相应的累计里程/燃油中。  
  - 最后用 `累计里程 / 累计燃油` 就得到该司机那半年的 **平均油耗（km / L）**，直接比较即可判断是否“提升”。

- **时间/空间复杂度**（大白话版）：  
  - `O(n)`：`n` 是出行记录的总数。我们只遍历一次，每条记录做常数次操作（判断月份、加法、计数），所以时间随记录数线性增长。  
  - `O(d)`：`d` 是司机的数量。我们为每位司机保存几条累计数据，空间随司机数增长。

#### 代码（Python）

```python
from collections import defaultdict
from datetime import datetime
from typing import List, Tuple

# 为演示，假设输入已经是 Python 列表形式
# drivers: List[Tuple[int, str]]               -> (driver_id, driver_name)
# trips:   List[Tuple[int, int, str, float, float]] 
#          -> (trip_id, driver_id, trip_date, distance_km, fuel_consumed)

def improved_drivers_bruteforce(drivers: List[Tuple[int, str]],
                                trips: List[Tuple[int, int, str, float, float]]
                               ) -> List[Tuple[int, str, float, float, float]]:
    """
    返回每位油耗提升的司机及其两段时间的平均油耗和提升幅度。
    结果按提升幅度降序、姓名升序排序。
    """
    # 1️⃣ 为每位司机准备累计器
    # value = [first_dist, first_fuel, first_cnt, second_dist, second_fuel, second_cnt]
    stats = defaultdict(lambda: [0.0, 0.0, 0, 0.0, 0.0, 0])

    # 2️⃣ 遍历所有出行记录，累加对应的半年的数据
    for _, driver_id, trip_date, distance, fuel in trips:
        month = datetime.strptime(trip_date, "%Y-%m-%d").month   # 取月份
        if month <= 6:   # 上半年
            stats[driver_id][0] += distance      # 累计里程
            stats[driver_id][1] += fuel          # 累计燃油
            stats[driver_id][2] += 1             # 计次数
        else:            # 下半年
            stats[driver_id][3] += distance
            stats[driver_id][4] += fuel
            stats[driver_id][5] += 1

    # 3️⃣ 计算平均油耗、筛选提升的司机
    result = []
    driver_name_map = {did: name for did, name in drivers}
    for driver_id, (fd, ff, fc, sd, sf, sc) in stats.items():
        # 必须两段都有记录才能比较
        if fc == 0 or sc == 0:
            continue
        first_avg = fd / ff          # 上半年平均油耗 (km / L)
        second_avg = sd / sf         # 下半年平均油耗
        if second_avg > first_avg:   # 有提升
            improvement = second_avg - first_avg
            result.append((driver_id,
                           driver_name_map[driver_id],
                           round(first_avg, 2),
                           round(second_avg, 2),
                           round(improvement, 2)))

    # 4️⃣ 排序：提升幅度大在前，名字字母序小在前
    result.sort(key=lambda x: (-x[4], x[1]))
    return result
```

#### 复杂度

- **时间复杂度**：`O(n + d log d)`  
  - `n` 为出行记录数（一次线性遍历）。  
  - 最后对 `d` 条符合条件的司机进行排序，排序的时间是 `d log d`，通常 `d` 远小于 `n`，所以整体仍然是线性主导。

- **空间复杂度**：`O(d)`  
  - 只保存每位司机的 6 个累计数字和名字映射，随司机数线性增长。

---

### 2. 最优解

#### 思路  

从暴力解来看，唯一的**瓶颈**是我们把所有记录都逐条判断、累计，然后再手动排序。  
如果使用 **SQL**（或类似的向量化工具）一次性完成“分组聚合”，可以省去显式的循环与字典维护，让代码更简洁、执行更快。

在 Python 中，**pandas** 正好提供了这种“一次性分组、聚合、筛选、排序”的能力。思路如下：

1. **把原始表装进 DataFrame**（类似 Excel 表格），每一列对应一个字段。  
2. **新增半年度标签**：`half = 'first' if month <= 6 else 'second'`。  
3. **一次 `groupby(['driver_id', 'half'])`，算出**  
   - `total_distance = sum(distance_km)`  
   - `total_fuel = sum(fuel_consumed)`  
   - `avg_efficiency = total_distance / total_fuel`（即平均油耗）  
4. **把上、下半年结果 pivot 成宽表**，每行只保留一个司机的两段平均油耗。  
5. **计算提升幅度**，筛选 `second > first` 的记录。  
6. **左连接司机表**得到姓名，最后 **按照提升幅度降序、姓名升序** 排序。

核心概念解释（零基础）：

- **DataFrame**：把它想象成一张带有标题行的电子表格，Python 里可以像操作表格一样快速统计。
- **groupby**：把表格按某几列“分组”，比如把所有同一个司机、同一个半年度的记录放到一起，然后对每组做求和、计数等操作。就像我们把同学按班级、性别分组后再算每组的平均成绩。
- **pivot**：把“长条形”数据（每行是 driver+half）转成“宽表”（每行是 driver，列里有 first_avg、second_avg），类似于把一张列表转成两列的对照表。

相比手写循环，pandas 利用了底层的 C 实现，速度更快，而且代码更易读。

#### 代码（Python）

```python
import pandas as pd
from typing import List, Tuple

def improved_drivers_optimal(drivers: List[Tuple[int, str]],
                             trips: List[Tuple[int, int, str, float, float]]
                            ) -> pd.DataFrame:
    """
    使用 pandas 完成同样的查询，返回 DataFrame，列名与题目示例保持一致。
    """
    # ---------- 1️⃣ 构造 DataFrame ----------
    df_driver = pd.DataFrame(drivers, columns=['driver_id', 'driver_name'])
    df_trip   = pd.DataFrame(trips,
                             columns=['trip_id', 'driver_id', 'trip_date',
                                      'distance_km', 'fuel_consumed'])
    # 将日期字符串转为 datetime，方便取月份
    df_trip['trip_date'] = pd.to_datetime(df_trip['trip_date'])

    # ---------- 2️⃣ 标记上/下半年 ----------
    df_trip['half'] = df_trip['trip_date'].dt.month.apply(
        lambda m: 'first' if m <= 6 else 'second')

    # ---------- 3️⃣ 分组聚合，计算每位司机每半年的平均油耗 ----------
    agg = (df_trip
           .groupby(['driver_id', 'half'], as_index=False)
           .agg(total_distance=('distance_km', 'sum'),
                total_fuel=('fuel_consumed', 'sum')))
    agg['avg_efficiency'] = agg['total_distance'] / agg['total_fuel']

    # ---------- 4️⃣ 将上、下半年展开成两列 ----------
    pivot = agg.pivot(index='driver_id',
                      columns='half',
                      values='avg_efficiency').reset_index()
    pivot.columns = ['driver_id', 'first_half_avg', 'second_half_avg']

    # ---------- 5️⃣ 计算提升幅度并筛选 ----------
    pivot['efficiency_improvement'] = pivot['second_half_avg'] - pivot['first_half_avg']
    improved = pivot[pivot['efficiency_improvement'] > 0].copy()

    # ---------- 6️⃣ 合并司机姓名 ----------
    result = improved.merge(df_driver, on='driver_id', how='left')

    # ---------- 7️⃣ 排序 ----------
    result = (result
              .sort_values(by=['efficiency_improvement', 'driver_name'],
                           ascending=[False, True])
              .reset_index(drop=True))

    # 调整列顺序，使输出与示例一致
    result = result[['driver_id', 'driver_name',
                     'first_half_avg', 'second_half_avg',
                     'efficiency_improvement']]

    # 为了美观，保留两位小数
    result[['first_half_avg', 'second_half_avg', 'efficiency_improvement']] = \
        result[['first_half_avg', 'second_half_avg', 'efficiency_improvement']].round(2)

    return result
```

#### 复杂度

- **时间复杂度**：`O(n)`（实际常数更小）  
  - `pandas` 在内部一次遍历完成分组、聚合等操作，整体仍是线性随记录数增长。  
  - 相比手写循环，省去了 Python 层面的显式循环，速度提升显著。

- **空间复杂度**：`O(n + d)`  
  - 需要在内存中保存原始表（`n` 条记录）以及聚合后的临时表。  
  - 与暴力解相比，多了一层 DataFrame 的开销，但仍然是线性级别。

---

## 心得

- **核心技巧**：**分组聚合（GROUP BY） + 条件筛选 + 排序**。在实际业务中，几乎所有“对同类对象求平均、总和、比较”类的问题都可以用这套思路解决。
- **适用的题型**（举例）  
  1. 统计每位员工每月的销售额并找出环比增长的员工。  
  2. 计算每个商品在不同季节的平均评分，找出评分提升的商品。  
  3. 按城市、年份统计人口增长率，筛选增长最快的城市。

- **一句话总结解题钥匙**：  
  “先把数据按要比较的维度（司机 + 半年）聚合成平均值，再一次性比较、过滤并排序。”

## 反思

- **第一反应**：看到“上半年、下半年”，立刻想到要把日期分段，然后对每段做平均值比较。  
- **最容易踩的坑**：  
  - **月份划分错误**：忘记把 6 月算进上半年或把 7 月算进下半年会导致结果偏差。  
  - **除零错误**：某段时间没有出行记录时，累计燃油为 0，直接除会报错，需要先检查次数或燃油是否为 0。  
  - **小数精度**：题目要求保留两位小数，直接打印浮点数可能出现 11.239999，需要 `round` 或格式化。  
- **下次第一步**：先把日期转成“上/下半年”标签（或其他时间段），再 **groupby** 做聚合，最后比较、筛选、排序。这样思路清晰，代码也能一步到位。