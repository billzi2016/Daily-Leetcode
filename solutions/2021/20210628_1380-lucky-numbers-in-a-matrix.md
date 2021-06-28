# #1380. 矩阵中的幸运数字 / Lucky Numbers in a Matrix

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/lucky-numbers-in-a-matrix/)

---

## 题目（英文原版）

**Description**

Given an m x n matrix of distinct numbers, return all lucky numbers in the matrix in any order.
A lucky number is an element of the matrix such that it is the minimum element in its row and maximum in its column.

**Examples**

**Example 1:**

```
Input: matrix = [[3,7,8],[9,11,13],[15,16,17]]
Output: [15]
Explanation: 15 is the only lucky number since it is the minimum in its row and the maximum in its column.
```

**Example 2:**

```
Input: matrix = [[1,10,4,2],[9,3,8,7],[15,16,17,12]]
Output: [12]
Explanation: 12 is the only lucky number since it is the minimum in its row and the maximum in its column.
```

**Example 3:**

```
Input: matrix = [[7,8],[1,2]]
Output: [7]
Explanation: 7 is the only lucky number since it is the minimum in its row and the maximum in its column.
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= n, m <= 50
- 1 <= matrix[i][j] <= 105.
- All elements in the matrix are distinct.

---

## 题目（中文翻译）

给定一个 **m × n** 矩阵（matrix），其中所有数字互不相同，返回矩阵中所有的幸运数字（lucky numbers），顺序不限。  
如果一个元素同时是其所在行（row）的最小元素（minimum element）且是其所在列（column）的最大元素（maximum element），则称其为幸运数字。

**示例 1：**  
**示例 2：**  
**示例 3：**  

**约束条件**

- `m == mat.length`
- `n == mat[i].length`
- `1 <= n, m <= 50`
- `1 <= matrix[i][j] <= 10^5`
- 矩阵中的所有元素均互不相同。

**示例**

**示例 1:**  
```text
Input: matrix = [[3,7,8],[9,11,13],[15,16,17]]
Output: [15]
Explanation: 15 是唯一的幸运数字，因为它是所在行的最小元素且所在列的最大元素。
```

**示例 2:**  
```text
Input: matrix = [[1,10,4,2],[9,3,8,7],[15,16,17,12]]
Output: [12]
Explanation: 12 是唯一的幸运数字，因为它是所在行的最小元素且所在列的最大元素。
```

**示例 3:**  
```text
Input: matrix = [[7,8],[1,2]]
Output: [7]
Explanation: 7 是唯一的幸运数字，因为它是所在行的最小元素且所在列的最大元素。
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**逐个检查每个元素**，看它是不是“幸运数”。  
对矩阵中的每个位置 `(i, j)`，我们需要判断两个条件：

1. 它是所在行 `i` 的最小值。  
2. 它是所在列 `j` 的最大值。  

> **类比**：把矩阵想象成一张座位表，每一行是一排座位，每一列是一列座位。  
> - “行最小”就像在这一排里坐得最靠左（数值最小）。  
> - “列最大”就像在这一列里坐得最靠前（数值最大）。  

只要这两个条件同时满足，这个坐位上的人（数字）就是幸运数。

**为什么能得到正确答案**：  
因为题目定义的“幸运数”恰好是满足这两个条件的元素，逐个验证自然不会漏掉，也不会误判。

**时间/空间分析**（大白话版）：

- 对每个元素，我们都要**遍历整行**找最小、**遍历整列**找最大。  
  - 矩阵有 `m` 行、`n` 列，总共有 `m·n` 个元素。  
  - 每次检查要走 `n` 步（行）+ `m` 步（列），所以总步数约为 `m·n·(m+n)`。  
  - 这在大 O 表示法里记作 **O(m·n·(m+n))**，如果把 `m`、`n` 看成同级别的 `N`，就是 **O(N³)**，在最坏情况下会比较慢。  

- 额外使用的空间只有几个临时变量，**O(1)**（常数级）。


#### 代码（Python）

```python
from typing import List

def luckyNumbers_brute_force(matrix: List[List[int]]) -> List[int]:
    m, n = len(matrix), len(matrix[0])          # 行数、列数
    lucky = []                                   # 用来收集幸运数

    # 遍历矩阵中的每一个元素
    for i in range(m):
        for j in range(n):
            val = matrix[i][j]                  # 当前元素的值

            # 1️⃣ 检查它是否是所在行的最小值
            row_min = True
            for col in range(n):
                if matrix[i][col] < val:        # 只要发现更小的，就不是行最小
                    row_min = False
                    break

            # 2️⃣ 检查它是否是所在列的最大值
            col_max = True
            for row in range(m):
                if matrix[row][j] > val:        # 只要发现更大的，就不是列最大
                    col_max = False
                    break

            # 同时满足两个条件 → 幸运数
            if row_min and col_max:
                lucky.append(val)

    return lucky
```

#### 复杂度  

- **时间复杂度**：`O(m·n·(m+n))`  
  - 想象有 10 行 10 列，暴力解要检查 100 个元素，每个元素要再看 10+10=20 次，总共 2000 步。  
- **空间复杂度**：`O(1)`（不计返回列表的空间）  
  - 只用了几个计数器和布尔变量，和矩阵大小无关。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复遍历同一行或同一列**是主要的性能瓶颈。  
我们可以把每一行的最小值、每一列的最大值**提前算好**，保存到两个列表里，这样后面只需要一次 O(1) 的查表就能判断是否是幸运数。

具体步骤：

1. **遍历一次矩阵**，同时得到  
   - `row_mins[i]`：第 `i` 行的最小元素。  
   - `col_maxs[j]`：第 `j` 列的最大元素。  
   这一步只需要 O(m·n) 的时间，因为每个元素只会被看一次。

2. 再次遍历矩阵（或直接遍历 `row_mins`），检查每个元素 `matrix[i][j]` 是否同时等于 `row_mins[i]` **且** `col_maxs[j]`。  
   - 如果相等，就说明它既是所在行的最小，也是所在列的最大，直接加入答案。

> **类比**：想象我们先把每排座位里坐得最靠左的人（行最小）和每列座位里坐得最靠前的人（列最大）都记在笔记本上。以后要判断某个人是不是幸运数，只需要看看笔记本里有没有这两条记录，省去了再次找人的过程。

**为什么更快**：  
- 只遍历矩阵两遍，时间从 `O(m·n·(m+n))` 降到 `O(m·n)`，即 **线性** 时间。  
- 额外使用的空间只和行数、列数成正比，`O(m+n)`，仍然很小。

#### 代码（Python）

```python
from typing import List

def luckyNumbers_optimal(matrix: List[List[int]]) -> List[int]:
    m, n = len(matrix), len(matrix[0])

    # 1️⃣ 预处理：求每行最小值、每列最大值
    row_mins = [float('inf')] * m          # 初始化为正无穷，后面会被真正的最小值覆盖
    col_maxs = [float('-inf')] * n         # 初始化为负无穷，后面会被真正的最大值覆盖

    for i in range(m):
        for j in range(n):
            val = matrix[i][j]
            # 更新第 i 行的最小值
            if val < row_mins[i]:
                row_mins[i] = val
            # 更新第 j 列的最大值
            if val > col_maxs[j]:
                col_maxs[j] = val

    # 2️⃣ 再次遍历，找同时满足两个条件的元素
    lucky = []
    for i in range(m):
        for j in range(n):
            val = matrix[i][j]
            if val == row_mins[i] and val == col_maxs[j]:
                lucky.append(val)

    return lucky
```

#### 复杂度  

- **时间复杂度**：`O(m·n)`  
  - 只遍历了两遍矩阵，每个元素最多被看两次，和矩阵大小成正比。  
  - 对比暴力解的 `O(m·n·(m+n))`，明显更快，尤其当矩阵行列数都在 50 左右时，差距明显。

- **空间复杂度**：`O(m + n)`  
  - 需要保存 `row_mins`（长度 `m`）和 `col_maxs`（长度 `n`），这两个额外列表的大小随行列数线性增长。  
  - 对于本题的最大规模（50×50），最多只占用 100 个整数的空间，几乎可以忽略不计。

---

## 心得  

- **核心技巧**：**预处理（前缀/后缀/行/列信息） + 一次扫描**。  
  把重复的“遍历同一行/列”工作提前算好，后面只需要常数时间查询。  

- **适用的题型**（类似技巧）  
  1. **行最小列最大**（本题）。  
  2. **矩阵中的行最大列最小**（LeetCode 2401）。  
  3. **二维前缀和求子矩阵和**（需要提前计算每行每列的累计和）。  

- **一句话总结**：  
  “把每行/列的极值先记下来，检查元素时只要对号入座即可。”

---

## 反思  

- **第一反应**：直接对每个元素做两次遍历检查，写出暴力解。  
- **最容易踩的坑**  
  - 忘记矩阵元素是**互不相同**的，导致可能出现同一行/列出现多个极值的误判（虽然题目保证唯一，但代码仍需稳健）。  
  - 边界情况：只有 1 行或 1 列时，行最小和列最大恰好是同一个元素，需要代码能正确处理。  
- **下次遇到同类题**：第一步先**统计每行/列的关键信息**（最小、最大、和等），再用一次遍历完成判定。这样可以把时间从“指数级”或“三重循环”降到“一次线性扫描”。