# #2879. 显示前3行 / Display the First Three Rows

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/display-the-first-three-rows/)

---

## 题目（英文原版）

**Description**

Write a solution to display the first 3 rows of this DataFrame.

**Examples**

**Example 1:**

```
DataFrame: employees
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| employee_id | int    |
| name        | object |
| department  | object |
| salary      | int    |
+-------------+--------+
```

**Example 2:**

```
Input:
DataFrame employees
+-------------+-----------+-----------------------+--------+
| employee_id | name      | department            | salary |
+-------------+-----------+-----------------------+--------+
| 3           | Bob       | Operations            | 48675  |
| 90          | Alice     | Sales                 | 11096  |
| 9           | Tatiana   | Engineering           | 33805  |
| 60          | Annabelle | InformationTechnology | 37678  |
| 49          | Jonathan  | HumanResources        | 23793  |
| 43          | Khaled    | Administration        | 40454  |
+-------------+-----------+-----------------------+--------+
Output:
+-------------+---------+-------------+--------+
| employee_id | name    | department  | salary |
+-------------+---------+-------------+--------+
| 3           | Bob     | Operations  | 48675  |
| 90          | Alice   | Sales       | 11096  |
| 9           | Tatiana | Engineering | 33805  |
+-------------+---------+-------------+--------+
Explanation: 
Only the first 3 rows are displayed.
```

---

## 题目（中文翻译）

编写一个解决方案，显示此 DataFrame 的前 3 行。

**示例 1：**

DataFrame: employees  
+-------------+--------+  
| Column Name | Type   |  
+-------------+--------+  
| employee_id | int    |  
| name        | object |  
| department  | object |  
| salary      | int    |  
+-------------+--------+

**示例 2：**

Input:  
DataFrame employees  
+-------------+-----------+-----------------------+--------+  
| employee_id | name      | department            | salary |  
+-------------+-----------+-----------------------+--------+  
| 3           | Bob       | Operations            | 48675  |  
| 90          | Alice     | Sales                 | 11096  |  
| 9           | Tatiana   | Engineering           | 33805  |  
| 60   
... (已截断)

**约束条件：**  
无

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把 DataFrame 当成普通的二维表**，像 Excel 那样手动取出前面几行。  
在 Python 中，`pandas.DataFrame` 支持 **位置索引**（`iloc`），可以像列表切片一样写 `df.iloc[0:3]`，意思是“从第 0 行（第一行）开始，取到第 3 行（不含第 3 行）”。  

- **用到的数据结构**：`DataFrame` 本质上是**表格**，每一行对应一条记录。`iloc` 就像一本字典的“页码”，行号是页码，取哪一页就看页码是多少。  
- **为什么正确**：题目要求“显示前 3 行”，`iloc[0:3]` 正好取出第 0、1、2 行，恰好是前三条记录。  
- **时间/空间复杂度**：  
  - **时间复杂度**：我们遍历了 **3 条记录**，所以时间是 `O(3)`，在大 O 记号里常写成 `O(1)`（常数时间），因为不随 DataFrame 的整体大小变化。  
  - **空间复杂度**：返回了一个只包含 3 行的新 `DataFrame`，占用的空间也是常数级 `O(1)`（只和取出的行数有关）。  

> **大白话**：如果你把整个表看成一本厚厚的书，暴力解就是直接把前 3 页翻出来看，翻页的次数是固定的 3 次，和书的厚度（行数）无关。

#### 代码（Python）

```python
import pandas as pd

def first_three_rows_bruteforce(df: pd.DataFrame) -> pd.DataFrame:
    """
    暴力解：使用 iloc 进行切片，取出前 3 行
    """
    # iloc 是基于行号的定位器，0:3 表示取第 0、1、2 行（不含第 3 行）
    first_three = df.iloc[0:3]          # <-- 关键行：切片取前三行
    return first_three
```

#### 复杂度  

- **时间复杂度**：`O(1)` — 只取固定的 3 行，和总行数无关。  
- **空间复杂度**：`O(1)` — 新建的 DataFrame 只保存 3 行数据。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看出，**瓶颈并不在这里**，因为我们已经只操作了常数条记录。  
不过 `pandas` 为我们提供了一个更**语义化、更易读**的专用函数 `head()`，专门用来“取前几行”。  

- **核心函数**：`df.head(n)` 返回前 `n` 行（默认 `n=5`）。内部实现其实也是基于 `iloc`，但把意图表达得更明确。  
- **为什么更好**：代码更简洁，阅读时一眼就能看出“取前 3 行”。在实际项目里，这种“自解释”代码更易维护。  

#### 代码（Python）

```python
import pandas as pd

def first_three_rows_optimal(df: pd.DataFrame) -> pd.DataFrame:
    """
    最优解：直接使用 pandas 的 head() 方法取前 3 行
    """
    # head(3) 表示“取前 3 行”，语义最清晰
    return df.head(3)          # <-- 关键行：一行代码完成需求
```

#### 复杂度  

- **时间复杂度**：`O(1)` — 同样只取固定的 3 行。  
- **空间复杂度**：`O(1)` — 只创建一个包含 3 行的 DataFrame。  

> 与暴力解相比，**时间、空间都没有区别**，唯一的提升是代码可读性和表达意图的明确度。

---

## 心得  

- **核心技巧**：利用 `pandas` 提供的高阶 API（如 `head()`）来完成常见的表格操作。  
- **适用的题型**：  
  1. 取 DataFrame 前/后几行（`head()` / `tail()`）。  
  2. 按条件筛选前 N 条记录（`df.sort_values(...).head(N)`）。  
  3. 统计前 N 名（排行榜类题目）。  
- **一句话总结**：`head()` 就是“取前几页”的快捷键，记住它，很多“取前 N 条”都能一键搞定。

---

## 反思  

- **第一反应**：看到“显示前 3 行”，立刻想到切片 `df.iloc[:3]`，因为这和 Python 列表的切片非常相似。  
- **最容易踩的坑**：  
  - 忘记 `iloc` 的左闭右开区间特性，写成 `df.iloc[0:3]` 是对的，写成 `df.iloc[0:2]` 会少取一行。  
  - 如果 DataFrame 行数不足 3 行，`head(3)` 与 `iloc[:3]` 都会安全返回全部行，不会报错，这是需要记住的安全特性。  
- **下次思路**：遇到“取前/后/第几行”这种直接定位的需求时，先在脑中搜索 `head()` / `tail()` / `iloc`，选最语义化的函数实现。