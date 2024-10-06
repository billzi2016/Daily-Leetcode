# #2889. 重塑数据：透视 / Reshape Data: Pivot

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/reshape-data-pivot/)

---

## 题目（英文原版）

**Description**

Write a solution to pivot the data so that each row represents temperatures for a specific month, and each city is a separate column.
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame weather
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| city        | object |
| month       | object |
| temperature | int    |
+-------------+--------+
```

**Example 2:**

```
Example 1:
Input:
+--------------+----------+-------------+
| city         | month    | temperature |
+--------------+----------+-------------+
| Jacksonville | January  | 13          |
| Jacksonville | February | 23          |
| Jacksonville | March    | 38          |
| Jacksonville | April    | 5           |
| Jacksonville | May      | 34          |
| ElPaso       | January  | 20          |
| ElPaso       | February | 6           |
| ElPaso       | March    | 26          |
| ElPaso       | April    | 2           |
| ElPaso       | May      | 43          |
+--------------+----------+-------------+
Output:
+----------+--------+--------------+
| month    | ElPaso | Jacksonville |
+----------+--------+--------------+
| April    | 2      | 5            |
| February | 6      | 23           |
| January  | 20     | 13           |
| March    | 26     | 38           |
| May      | 43     | 34           |
+----------+--------+--------------+
Explanation:
The table is pivoted, each column represents a city, and each row represents a specific month.
```

---

## 题目（中文翻译）

编写一个解决方案，对数据进行透视（pivot），使每一行表示特定月份的温度，并且每个城市作为单独的列。结果格式参考下面的示例。

示例 1  
DataFrame `weather`

| Column Name | Type   |
|-------------|--------|
| city        | object |
| month       | object |
| temperature | int    |

示例 2  
Example 1:

**输入**

| city         | month    | temperature |
|--------------|----------|-------------|
| Jacksonville | January  | 13          |
| Jacksonville | February | 23          |
| Jacksonville | March    | 38          |
| Jacksonville | April    | 5           |
| Jacksonville | May      | 34          |
| ElPaso       | January  | 20          |
| … (已截断)   |          |             |

**约束条件**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是 **手动遍历** 原始的 `DataFrame`（其实可以把它想成一张普通的 Excel 表），把相同 **月份** 的记录聚在一起，再把不同 **城市** 的温度放到对应的列里。  
- **数据结构**：我们可以用一个 **字典**（类似查字典的工具书）来暂存结果。外层的键是 `month`，对应的值又是一个内部字典，内部字典的键是 `city`，值是 `temperature`。  
- **为什么正确**：遍历一遍原始表格，就把每条 `(city, month, temperature)` 信息放到了正确的“格子”里。遍历结束后，字典里自然就形成了“以 month 为行、city 为列”的二维结构。  
- **时间/空间复杂度**：  
  - **时间**：我们只需要 **一次** 遍历所有记录，设记录数为 `n`，则时间复杂度是 **O(n)**。这里的 `O(n)` 可以理解为“随着数据行数线性增长，耗时也线性增长”。  
  - **空间**：需要额外的字典保存结果，字典中会出现 `#unique_months × #unique_cities` 条目，记为 `m`。所以空间复杂度是 **O(m)**。  

#### 代码（Python）  

```python
import pandas as pd

def pivot_brute(df: pd.DataFrame) -> pd.DataFrame:
    """
    暴力实现 pivot：
    - 用 dict[month][city] = temperature 保存临时结果
    - 最后把 dict 转成 DataFrame
    """
    # 1. 建立两层字典，外层键是 month，内层键是 city
    data = {}                       # {month: {city: temperature, ...}, ...}
    for _, row in df.iterrows():    # 逐行遍历
        city = row['city']
        month = row['month']
        temp = row['temperature']

        if month not in data:        # 第一次遇到这个 month，先创建空 dict
            data[month] = {}
        data[month][city] = temp    # 把 temperature 放进对应的格子

    # 2. 把字典转成 DataFrame
    #   - 首先把外层键（month）变成一列
    #   - 再利用 pd.DataFrame.from_dict 将内层字典展开为列
    result = pd.DataFrame.from_dict(data, orient='index')
    result.index.name = 'month'          # 把索引命名为 month
    result.reset_index(inplace=True)    # 把 month 从索引变成普通列

    # 3. 为了保持列顺序（city 列按字母序），可自行排序
    city_cols = sorted([c for c in result.columns if c != 'month'])
    result = result[['month'] + city_cols]

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历一次所有行，行数多多少时间就多多少。  
- **空间复杂度**：`O(m)` — 需要额外存储 `month × city` 这张小表，和原始数据大小相比通常要小得多。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**遍历 + 手动填表** 是最慢的环节，尤其是当数据量大、列很多时，手动维护字典会增加代码复杂度和潜在错误。  
pandas 本身已经提供了 **`pivot` / `pivot_table`** 这类专门用于“旋转”数据的函数，内部实现已经高度优化（底层用 Cython），只需要一次调用即可完成同样的工作。  

**关键点**：  
1. **`pivot`** 要求每个 `(index, columns)` 组合唯一，否则会报错；本题每个城市在每个月只有一条温度记录，满足唯一性。  
2. **`pivot_table`** 更通用（可以处理重复值并指定聚合函数），如果不确定唯一性，使用它更安全。  

我们把 **`month`** 设为行索引（`index`），**`city`** 设为列标签（`columns`），**`temperature`** 作为填充的数值（`values`）。  

#### 代码（Python）  

```python
import pandas as pd

def pivot_optimal(df: pd.DataFrame) -> pd.DataFrame:
    """
    使用 pandas 自带的 pivot（或 pivot_table）实现快速旋转。
    - index   : month   -> 行标签
    - columns : city    -> 列标签
    - values  : temperature -> 填充的数值
    """
    # 直接调用 pivot，内部已经完成分组、重排、填充等操作
    result = df.pivot(index='month', columns='city', values='temperature')
    
    # pivot 会把 city 变成列索引（MultiIndex），我们把它恢复为普通列
    result = result.reset_index()               # 把 month 从索引变成普通列
    result.columns.name = None                  # 去掉列索引的名字（防止出现额外的层级名）

    # 为了让列顺序更直观（city 列按字母序），可以自行排序
    city_cols = sorted([c for c in result.columns if c != 'month'])
    result = result[['month'] + city_cols]

    return result
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 与暴力解相同的线性遍历，但底层实现是向量化的，常数因子更小，实际运行更快。  
- **空间复杂度**：`O(m)` — 仍然需要存储旋转后的表格，和结果大小成正比。  

相较于手写字典，**`pivot`** 省去了 Python 循环的开销，代码更简洁、可读性更高，也更不容易出错。

---  

## 心得  

- **核心技巧**：利用 pandas 的 `pivot` / `pivot_table` 进行数据透视（reshape）。  
- **适用的题型**：  
  1. 将长表（long format）转为宽表（wide format），如“销售额按地区/月份透视”。  
  2. 多维度聚合统计，如“学生成绩按科目、学期透视”。  
  3. 时间序列数据的“交叉表”展示，例如“网站访问量按国家、日期”。  
- **解题钥匙**：**“把要变成行的字段放在 `index`，要变成列的字段放在 `columns`，要填的数值放在 `values`”。**  

---  

## 反思  

- **第一反应**：看到“pivot”二字，立刻想到 pandas 的 `pivot`/`pivot_table`，因为这正是数据透视的专用函数。  
- **最容易踩的坑**：  
  - `pivot` 要求 `(index, columns)` 组合唯一，否则会报 `ValueError: Index contains duplicate entries, cannot reshape`。如果不确定唯一性，应改用 `pivot_table` 并指定聚合函数（如 `mean`）。  
  - 列索引名会残留 `city` 这种层级名，需要手动 `reset_index` 并清除 `columns.name`，否则输出会多出一行标题。  
  - 当某些城市在某个月没有记录时，会出现 `NaN`（缺失值），如果业务要求填默认值，可在 `pivot` 之后使用 `fillna`。  
- **下次遇到同类题**：第一步先检查 **是否可以直接使用 `pivot`/`pivot_table`**，把要变成行、列、值的字段分别列出来，再决定是否需要额外的聚合或缺失值处理。