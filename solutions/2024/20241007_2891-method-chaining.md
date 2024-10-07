# #2891. 方法链 / Method Chaining

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/method-chaining/)

---

## 题目（英文原版）

**Description**

Write a solution to list the names of animals that weigh strictly more than 100 kilograms.
Return the animals sorted by weight in descending order.
The result format is in the following example.
In Pandas, method chaining enables us to perform operations on a DataFrame without breaking up each operation into a separate line or creating multiple temporary variables.
Can you complete this task in just one line of code using method chaining?

**Examples**

**Example 1:**

```
DataFrame animals
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| name        | object |
| species     | object |
| age         | int    |
| weight      | int    |
+-------------+--------+
```

**Example 2:**

```
Input: 
DataFrame animals:
+----------+---------+-----+--------+
| name     | species | age | weight |
+----------+---------+-----+--------+
| Tatiana  | Snake   | 98  | 464    |
| Khaled   | Giraffe | 50  | 41     |
| Alex     | Leopard | 6   | 328    |
| Jonathan | Monkey  | 45  | 463    |
| Stefan   | Bear    | 100 | 50     |
| Tommy    | Panda   | 26  | 349    |
+----------+---------+-----+--------+
Output: 
+----------+
| name     |
+----------+
| Tatiana  |
| Jonathan |
| Tommy    |
| Alex     |
+----------+
Explanation: 
All animals weighing more than 100 should be included in the results table.
Tatiana's weight is 464, Jonathan's weight is 463, Tommy's weight is 349, and Alex's weight is 328.
The results should be sorted in descending order of weight.
```

---

## 题目（中文翻译）

编写一个解决方案，列出体重严格大于 **100 千克** 的动物的名称。  
返回的动物需按体重 **降序** 排序。结果格式参见下方示例。

**示例 1:**  
在 Pandas 中，**方法链（method chaining）** 使我们能够在 **数据框（DataFrame）** 上执行操作，而无需将每一步拆成单独的代码行或创建多个临时变量。  
你能仅用一行代码并利用 **方法链** 完成此任务吗？

### 示例

#### 示例 1:
DataFrame animals  
+-------------+--------+  
| Column Name | Type   |  
+-------------+--------+  
| name        | object |  
| species     | object |  
| age         | int    |  
| weight      | int    |  
+-------------+--------+

#### 示例 2:
Input:  
DataFrame animals:  
+----------+---------+-----+--------+  
| name     | species | age | weight |  
+----------+---------+-----+--------+  
| Tatiana  | Snake   | 98  | 464    |  
| Khaled   | Giraffe | 50  | 41     |  
| Alex     | Leopard | 6   | 328    |  
| Jonathan | Monkey  | 45  | 463    |  
| Stefan   | Bear    | 100 | 50     |  
| Tommy    | Panda   | 26  | 349    |  
+----------+---------+-----+--------+  
... (已截断)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把任务拆成几步来完成：

1. **筛选**：把体重 `weight` 大于 100 kg 的行挑出来。  
   - 这里用到的结构是 **DataFrame**，可以把它想象成一张 Excel 表格，每一列对应一种属性（名字、种类、年龄、体重），每一行对应一只动物。  
   - 筛选相当于在表格里用过滤器，只留下符合条件的行，就像在超市里挑出所有价格超过 100 元的商品。

2. **排序**：把筛选后的结果按照体重从大到小排序。  
   - 排序就像把挑出来的商品按重量从重到轻排成一列，方便我们快速找出最重的。

3. **取名字**：只保留 `name` 这一列，并把它转换成 Python 列表。  
   - 把列想象成一本书的章节，只取章节标题（名字）即可。

把这三步写成代码，虽然每一步都很清晰，但需要创建多个临时变量，看起来有点“繁琐”。  

#### 代码（Python）

```python
import pandas as pd

# 假设已有 DataFrame animals
# 1. 过滤体重 > 100
filtered = animals[animals['weight'] > 100]

# 2. 按体重降序排列
sorted_df = filtered.sort_values(by='weight', ascending=False)

# 3. 取名字列并转成列表
result = sorted_df['name'].tolist()

print(result)  # 示例输出: ['Tatiana', 'Jonathan', 'Alex', ...]
```

#### 复杂度  

- **时间复杂度**：  
  - 过滤遍历一次表格，时间是 `O(n)`（`n` 为动物数量）。  
  - 排序需要 `O(m log m)`，`m` 是筛选后留下的动物数（最坏情况 `m = n`）。  
  - 取列和转列表各是 `O(m)`。  
  - 综合起来是 `O(n + m log m)`，在最坏情况下约等于 `O(n log n)`。  
  - 大白话：如果有 1000 只动物，排序大约需要 1000 × log₂1000 ≈ 10 000 次比较。

- **空间复杂度**：  
  - 过滤后会产生一个新的 DataFrame，最多需要 `O(m)` 的额外空间。  
  - 再排序会再产生一个临时对象，空间同样是 `O(m)`。  
  - 最终返回的列表是 `O(m)`。  
  - 所以整体是 `O(m)`，即和筛选后动物的数量成正比。

---

### 2. 最优解

#### 思路  

在 **pandas** 中，**method chaining**（方法链）可以让我们把多个操作“串在一起”，不必显式创建中间变量。  

从暴力解可以看到，瓶颈不在时间上（排序本身就是必须的），而在 **代码的可读性与简洁性** 上。  
只要把“过滤 → 排序 → 取列 → 转列表”这四个步骤连成一条链，就能在 **一行代码** 内完成全部工作。

核心技巧：

- `df[condition]`：**布尔索引**，把满足条件的行挑出来。把它想成在表格里画了一个只显示符合要求的窗口。
- `.sort_values(by='col', ascending=False)`：**排序**，把窗口里的数据按指定列倒序排列。
- `['col']`：**列选择**，相当于在窗口里只打开某一列的视图。
- `.tolist()`：把 pandas 的 **Series**（单列数据）转成普通的 Python 列表，方便后续使用。

把它们依次写在同一行，用 `.` 把每一步连起来，就是 **method chaining**。

#### 代码（Python）

```python
import pandas as pd

# 一行代码完成所有需求
result = (animals[animals['weight'] > 100]               # 过滤体重 > 100
                .sort_values(by='weight', ascending=False)  # 按体重降序
                ['name']                                   # 只保留名字列
                .tolist())                                 # 转成 Python 列表

print(result)  # 示例输出: ['Tatiana', 'Jonathan', 'Alex', ...]
```

> **关键行中文注释**  
> - `animals['weight'] > 100` → “把体重大于 100 的动物挑出来”。  
> - `.sort_values(..., ascending=False)` → “把挑出来的动物按体重从大到小排”。  
> - `['name']` → “只看名字这列”。  
> - `.tolist()` → “把 pandas 的列转成普通列表”。

#### 复杂度  

- **时间复杂度**：与暴力解相同，仍是 `O(n log n)`（主要耗时在排序）。  
  - 只不过我们没有额外的拷贝步骤，所有操作在 pandas 内部链式完成，常数因子更小。

- **空间复杂度**：仍是 `O(m)`，因为 pandas 在链式调用时会复用中间对象，额外占用的空间基本不变。  
  - 与暴力解相比，**不需要显式保存临时变量**，代码更紧凑，内存占用略有优化。

---

## 心得

- **核心技巧**：`DataFrame` 的布尔索引 + `sort_values` + 列选择 + `tolist()` 的 method chaining。  
- **适用场景**：  
  1. 对表格数据进行多步过滤、排序、聚合后直接输出结果（如 “找出所有收入超过 10 万的员工并按收入降序列出姓名”。）  
  2. 数据清洗流程中需要连续执行多步转换（如 “去掉缺失值 → 计算新列 → 按某列分组 → 统计”。）  
  3. 在竞赛或面试中要求“一行代码”实现特定数据处理任务。  
- **解题钥匙**：把每一步的 **DataFrame 操作** 看成一块积木，用 `.` 把它们拼起来即可。

## 反思

- **第一反应**：先把任务拆成若干独立步骤，用临时变量一步步实现。  
- **最容易踩的坑**：  
  - 忘记在布尔索引后加括号导致语法错误。  
  - `sort_values` 默认是升序，需要显式 `ascending=False` 才能得到降序。  
  - 最后忘记 `.tolist()`，返回的是 pandas 的 Series 而不是普通列表。  
- **下次类似题**：第一步先在脑中构造 **过滤 → 排序 → 取列 → 转换** 的链式流程，确认每一步对应的 pandas 方法，然后直接写成一行代码。