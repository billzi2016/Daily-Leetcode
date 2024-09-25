# #2878. 获取 DataFrame 的大小 / Get the Size of a DataFrame

> 难度：简单 · 标签： · [LeetCode 链接](https://leetcode.com/problems/get-the-size-of-a-dataframe/)

---

## 题目（英文原版）

**Description**

Write a solution to calculate and display the number of rows and columns of players.
Return the result as an array:
[number of rows, number of columns]
The result format is in the following example.

**Examples**

**Example 1:**

```
DataFrame players:
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| player_id   | int    |
| name        | object |
| age         | int    |
| position    | object |
| ...         | ...    |
+-------------+--------+
```

**Example 2:**

```
Input:
+-----------+----------+-----+-------------+--------------------+
| player_id | name     | age | position    | team               |
+-----------+----------+-----+-------------+--------------------+
| 846       | Mason    | 21  | Forward     | RealMadrid         |
| 749       | Riley    | 30  | Winger      | Barcelona          |
| 155       | Bob      | 28  | Striker     | ManchesterUnited   |
| 583       | Isabella | 32  | Goalkeeper  | Liverpool          |
| 388       | Zachary  | 24  | Midfielder  | BayernMunich       |
| 883       | Ava      | 23  | Defender    | Chelsea            |
| 355       | Violet   | 18  | Striker     | Juventus           |
| 247       | Thomas   | 27  | Striker     | ParisSaint-Germain |
| 761       | Jack     | 33  | Midfielder  | ManchesterCity     |
| 642       | Charlie  | 36  | Center-back | Arsenal            |
+-----------+----------+-----+-------------+--------------------+
Output:
[10, 5]
Explanation:
This DataFrame contains 10 rows and 5 columns.
```

---

## 题目（中文翻译）

编写一个解决方案，计算并输出 **players** 数据框（DataFrame）的行数和列数。  
返回结果为一个数组（array）：  

```
[number of rows, number of columns]
```

结果的展示方式请参照下面的示例。

**示例 1**

DataFrame players:
```
+-------------+--------+
| Column Name | Type   |
+-------------+--------+
| player_id   | int    |
| name        | object |
| age         | int    |
| position    | object |
| ...         | ...    |
+-------------+--------+
```

**示例 2**

输入:
```
+-----------+----------+-----+-------------+-----------------+
| player_id | name     | age | position    | team            |
+-----------+----------+-----+-------------+-----------------+
| 846       | Mason    | 21  | Forward     | RealMadrid      |
| 749       | Riley    | 30  | Winger      | Barcelona       |
| 155       | Bob      | 28  | Striker     | ManchesterUnited
... (已截断)
```

**约束条件**

无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **手动数**。  
- **行数**：把 DataFrame 当成一张表格，一行一行往下走，计数器加一。相当于我们在纸上数“有多少行”。在代码里可以把 DataFrame 当成一个可迭代对象（`for row in df.itertuples()`），每遍历一次计数器 `row_cnt += 1`。  
- **列数**：把每一列的名字（列标签）拿出来，一个一个数。列名就像字典的“键”，我们可以把它们装进列表 `list(df.columns)`，再用 `len()` 得到长度。

> **类比**：  
> - **哈希表**（字典）就像一本查字典，`key` 是词，`value` 是对应的页码。这里的 `df.columns` 类似“词表”，我们只需要知道有多少个词（列）即可。  
> - **遍历行**就像走访每一位住户，统计总人数。

这种做法一定能得到正确答案，因为我们把表格的每一行、每一列都看了一遍。

#### 代码（Python）

```python
import pandas as pd

def size_bruteforce(df: pd.DataFrame) -> list:
    """
    暴力统计 DataFrame 的行数和列数
    返回 [行数, 列数]
    """
    # 统计行数 —— 手动遍历每一行
    row_cnt = 0
    for _ in df.itertuples(index=False):   # itertuples 能一次返回一行的所有字段
        row_cnt += 1                         # 行计数器加一

    # 统计列数 —— 把列标签收集到列表后求长度
    col_cnt = 0
    for _ in df.columns:                     # df.columns 本身是一个 Index，可直接遍历
        col_cnt += 1

    return [row_cnt, col_cnt]

# ------------------- 示例 -------------------
if __name__ == "__main__":
    # 构造一个小表格作演示
    data = {
        "player_id": [846, 749, 155],
        "name": ["Mason", "Riley", "Bob"],
        "age": [21, 30, 28],
        "position": ["Forward", "Winger", "Striker"],
        "team": ["RealMadrid", "Barcelona", "ManchesterUnited"]
    }
    players = pd.DataFrame(data)
    print(size_bruteforce(players))   # 输出: [3, 5]
```

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - `n` 为行数，遍历一次需要 `O(n)`。  
  - `m` 为列数，遍历一次需要 `O(m)`。  
  - 合起来就是 `O(n + m)`，也可以写成 `O(N)`（N 为总元素数），但对初学者来说把行列分开说更直观。  
- **空间复杂度**：`O(1)`  
  - 只用了几个计数器 (`row_cnt`, `col_cnt`) 和循环变量，没有额外的随输入规模增长的存储。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **遍历** 是瓶颈：我们逐行、逐列地走一遍，只是为了得到两个数字。  
实际上，**pandas 已经帮我们把行列的数量预先算好了**，存放在 `DataFrame.shape` 属性里。  

- `df.shape` 返回一个二元组 `(行数, 列数)`，内部实现是直接读取 DataFrame 的元信息，时间几乎为常数。  
- 类比：如果我们把表格装进了一个文件柜，`shape` 就像柜子外面贴的标签，告诉我们一眼就能知道有多少抽屉（行）和每抽屉里有多少格子（列），根本不需要打开柜子去数。

因此最优解只需要一行代码取出 `shape`，再转换成题目要求的列表格式。

#### 代码（Python）

```python
import pandas as pd

def size_optimal(df: pd.DataFrame) -> list:
    """
    使用 pandas 内置属性 shape 直接获取 DataFrame 的尺寸
    返回 [行数, 列数]
    """
    # df.shape -> (rows, cols)   O(1) 时间获取
    rows, cols = df.shape
    return [rows, cols]

# ------------------- 示例 -------------------
if __name__ == "__main__":
    data = {
        "player_id": [846, 749, 155],
        "name": ["Mason", "Riley", "Bob"],
        "age": [21, 30, 28],
        "position": ["Forward", "Winger", "Striker"],
        "team": ["RealMadrid", "Barcelona", "ManchesterUnited"]
    }
    players = pd.DataFrame(data)
    print(size_optimal(players))   # 输出: [3, 5]
```

#### 复杂度

- **时间复杂度**：`O(1)` — 常数时间。我们不需要遍历任何元素，只是读取已经存在的元信息。相比暴力解的 `O(n+m)`，快了几个数量级，尤其当表格很大时优势明显。  
- **空间复杂度**：`O(1)` — 只用了两个整数变量 `rows`、`cols`，不随输入规模增长。

---

## 心得

- **核心技巧**：善于利用库函数/属性（这里是 `DataFrame.shape`），把“手动计数”交给底层实现。  
- **适用的题型**  
  1. “求数组/列表的长度” → `len()`；  
  2. “获取字符串的字符数” → `len(s)`；  
  3. “获取 NumPy 数组的维度” → `array.shape`。  
- **解题钥匙**：**先想想有没有现成的“一行代码”能直接得到答案**，再考虑自己实现。

## 反思

- **第一反应**：看到“行数、列数”，马上想到遍历统计——这就是暴力解。  
- **最容易踩的坑**  
  - 忘记 `df.shape` 返回的是 **元组**，直接返回会得到 `(rows, cols)`，而题目要求的是列表 `[rows, cols]`。  
  - 如果使用 `len(df)` 只能得到行数，容易忽略列数。  
- **下次遇到同类题**：第一步先在官方文档或 IDE 的自动补全里查找 **对应的数据结构的属性或函数**（如 `shape`、`size`、`len`），确认是否已有 O(1) 的获取方式，再决定是否真的需要手写遍历。