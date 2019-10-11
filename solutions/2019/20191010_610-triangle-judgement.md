# #610. 三角形判定 / Triangle Judgement

> 难度：简单 · 标签：Database · [LeetCode 链接](https://leetcode.com/problems/triangle-judgement/)

---

## 题目（英文原版）

**Description**

Table: Triangle
Report for every three line segments whether they can form a triangle.
Return the result table in any order.
The result format is in the following example.

**Examples**

**Example 1:**

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| x           | int  |
| y           | int  |
| z           | int  |
+-------------+------+
In SQL, (x, y, z) is the primary key column for this table.
Each row of this table contains the lengths of three line segments.
```

**Example 2:**

```
Input: 
Triangle table:
+----+----+----+
| x  | y  | z  |
+----+----+----+
| 13 | 15 | 30 |
| 10 | 20 | 15 |
+----+----+----+
Output: 
+----+----+----+----------+
| x  | y  | z  | triangle |
+----+----+----+----------+
| 13 | 15 | 30 | No       |
| 10 | 20 | 15 | Yes      |
+----+----+----+----------+
```

---

## 题目（中文翻译）

**表结构**  
`Triangle` 表记录每组三条线段的长度。

**描述**  
请针对表中的每一行，判断这三条线段是否能够构成三角形（triangle）。  
返回包含原始长度以及判断结果的结果表（result table），结果的行序可以任意。

**结果格式** 参考下例。

**示例 1：表结构**  

```
+-------------+------+
| Column Name | Type |
+-------------+------+
| x           | int  |
| y           | int  |
| z           | int  |
+-------------+------+
```

在 SQL 中，`(x, y, z)` 为该表的主键（primary key）列。  
每一行存放三条线段（line segment）的长度。

**示例 2：**  

```
Input: 
Triangle table:
+----+----+----+
| x  | y  | z  |
+----+----+----+
| 13 | 15 | 30 |
| 10 | 20 | 15 |
+----+----+----+

Output: 
+----+----+----+----------+
| x  | y  | z  | triangle |
+----+----+----+----------+
| 13 | 15 | 30 | No       |
| 10 | 20 | 15 | Yes      |
+----+----+----+----------+
```

**约束条件**  
无

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们手里有一张“Triangle”表，每一行记录了三根线段的长度 `x、y、z`。  
要判断这三根线段能否组成三角形，只需要满足 **三条不等式**：

1. `x + y > z`
2. `x + z > y`
3. `y + z > x`

如果这三条都成立，就可以拼出三角形；否则不行。  
这就是最直接、最“笨”的办法——对每一行 **逐条** 检查这三个条件。  

> **类比**：把每根线段想成三块木板，只有当任意两块的长度之和比第三块长时，才能把它们围成一个闭合的三角形。

为什么这个方法一定对？  
- 三角形的 **三边不等式** 是几何学的基本定理，任何能组成三角形的三条边必然满足上面的三个不等式，反之亦然。  
- 我们对每一行都完整检查了这三条不等式，所以结果必然正确。

#### 代码（Python）

```python
from typing import List, Tuple

def triangle_bruteforce(rows: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int, str]]:
    """
    暴力解：对每一行逐条检查三条不等式
    参数 rows：[(x, y, z), ...]  每个元组代表一行数据
    返回值：在每行后面加上 "Yes"/"No" 表示能否组成三角形
    """
    result = []
    for x, y, z in rows:
        # 检查三条不等式
        if x + y > z and x + z > y and y + z > x:
            triangle = "Yes"          # 能组成三角形
        else:
            triangle = "No"           # 不能组成三角形
        # 把结果存进列表，保持原来的顺序
        result.append((x, y, z, triangle))
    return result

# ---------- 示例运行 ----------
if __name__ == "__main__":
    data = [(13, 15, 30), (10, 20, 15)]
    for row in triangle_bruteforce(data):
        print(row)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  解释：我们遍历了 `n` 行，每行只做了 **常数次**（3 次加法、3 次比较）操作，所以总时间正比于行数 `n`。  
- **空间复杂度**：`O(n)`（返回结果需要存 `n` 条记录）  
  若只考虑额外的临时空间（不算返回值），则是 `O(1)`，因为每次只用到几个整数变量。

---

### 2. 最优解

#### 思路  

暴力解已经是线性的，已经很快了。但我们可以把判断过程写得更**简洁**，并且把“三条不等式”合并成 **一条** 判断：

> 把三根线段从小到大排好序，记为 `a ≤ b ≤ c`。  
> 只要最短的两根之和 `a + b` 大于最长的那根 `c`，其余两条不等式自然成立。

**为什么？**  
- 已知 `a ≤ b ≤ c`，则 `a + c > b` 与 `b + c > a` 必然成立，因为 `c` 本身已经是最大的数，`a + c`、`b + c` 肯定比 `b`、`a` 大。  
- 因此只需要比较一次 `a + b > c` 即可。

实现时我们可以把每行的 `(x, y, z)` 放进一个长度为 3 的列表，调用 Python 内置的 `sorted()`（时间复杂度是 `O(3 log 3)`，常数极小），得到 `[a, b, c]`，再做一次加法比较。

#### 代码（Python）

```python
from typing import List, Tuple

def triangle_optimal(rows: List[Tuple[int, int, int]]) -> List[Tuple[int, int, int, str]]:
    """
    最优解：先把每行的三条边排序，只比较最短两条之和是否大于最长的那条
    """
    result = []
    for x, y, z in rows:
        a, b, c = sorted([x, y, z])   # a <= b <= c
        if a + b > c:
            triangle = "Yes"
        else:
            triangle = "No"
        result.append((x, y, z, triangle))
    return result

# ---------- 示例运行 ----------
if __name__ == "__main__":
    data = [(13, 15, 30), (10, 20, 15)]
    for row in triangle_optimal(data):
        print(row)
```

#### 复杂度  

- **时间复杂度**：`O(n)`（同样是遍历 `n` 行）  
  虽然每行多了一次排序，但排序的规模只有 3，等价于常数时间，整体仍然是线性的。相比暴力解，它把 **三次比较** 合并成 **一次比较**，代码更简洁。  
- **空间复杂度**：`O(n)`（返回结果）  
  临时空间只用到一个长度为 3 的列表 `sorted([x, y, z])`，即 `O(1)`。

---

## 心得

- **核心技巧**：**三边不等式** → **排序后只比较最短两边之和**。  
- 这种“把多个条件合并成一个” 的思路在很多几何或数值判断题里都很有用。  
- **类似题目**  
  1. 判断四条边能否组成矩形（两两相等即可）。  
  2. 判断若干整数能否组成等差数列（检查公差是否相等）。  
  3. 判断一组点能否构成凸多边形（利用极角排序 + 叉积符号）。  

> **一句话总结**：只要把三条边从小到大排好序，检查“最短两根之和 > 最长那根”即可快速判断是否能组成三角形。

## 反思

- **第一反应**：看到“三根线段”，立刻想到几何学里的“三边不等式”，于是写出三个独立的比较。  
- **最容易踩的坑**  
  - 忽略了**等于**的情况：`a + b == c` 时只能拼成一条直线，**不是**三角形。必须使用严格的大于 `>`。  
  - 输入可能包含 **负数或零**（虽然实际生活中长度不可能为负），如果出现，需要先判断 `>0` 再比较。  
- **下次遇到同类题**，第一步应先**把所有数排序**，看能否把多个约束合并成“最小/最大”之间的单一比较，这往往能让代码更简洁、思路更清晰。