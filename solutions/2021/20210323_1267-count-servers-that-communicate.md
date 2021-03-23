# #1267. 统计可以通信的服务器 / Count Servers that Communicate

> 难度：中等 · 标签：Array、Depth-First Search、Breadth-First Search、Union Find、Matrix、Counting · [LeetCode 链接](https://leetcode.com/problems/count-servers-that-communicate/)

---

## 题目（英文原版）

**Description**

You are given a map of a server center, represented as a m * n integer matrix grid, where 1 means that on that cell there is a server and 0 means that it is no server. Two servers are said to communicate if they are on the same row or on the same column.

Return the number of servers that communicate with any other server.

**Examples**

**Example 1:**

```
Input: grid = [[1,0],[0,1]]
Output: 0
Explanation: No servers can communicate with others.
```

**Example 2:**

```
Input: grid = [[1,0],[1,1]]
Output: 3
Explanation: All three servers can communicate with at least one other server.
```

**Example 3:**

```
Input: grid = [[1,1,0,0],[0,0,1,0],[0,0,1,0],[0,0,0,1]]
Output: 4
Explanation: The two servers in the first row can communicate with each other. The two servers in the third column can communicate with each other. The server at right bottom corner can't communicate with any other server.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m <= 250
- 1 <= n <= 250
- grid[i][j] == 0 or 1

---

## 题目（中文翻译）

给定一个服务器中心（server center）的地图，用一个 `m * n` 整数矩阵（matrix）`grid` 表示，其中 `1` 表示该单元格有服务器（server），`0` 表示没有服务器。两个服务器（server）如果在同一行（row）或同一列（column），则称它们能够通信（communicate）。

返回能够与 **任意其他** 服务器（server）通信的服务器数量。

## 示例

### 示例 1
**输入**  
```json
grid = [[1,0],[0,1]]
```
**输出**  
```
0
```
**解释**  
没有任何服务器能够与其他服务器通信。

### 示例 2
**输入**  
```json
grid = [[1,0],[1,1]]
```
**输出**  
```
3
```
**解释**  
所有三个服务器均至少可以与另一台服务器通信。

### 示例 3
**输入**  
```json
grid = [[1,1,0,0],
        [0,0,1,0],
        [0,0,1,0],
        [0,0,0,1]]
```
**输出**  
```
4
```
**解释**  
- 第一行的两台服务器可以相互通信。  
- 第三列的两台服务器可以相互通信。  
- 右下角的服务器无法与任何其他服务器通信。

## 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m <= 250`
- `1 <= n <= 250`
- `grid[i][j]` 为 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个服务器（即 `grid[i][j] == 1` 的位置），检查它所在的整行和整列，看看是否还有别的服务器**。  
- 如果在同一行或同一列里找到了另一台服务器，则这台服务器“可以通信”。  
- 如果整行、整列里都没有其他 `1`，说明它是孤立的，不能通信。

> **类比**：把矩阵想象成一张座位表，`1` 代表有小伙伴坐在那。要判断某个人能否和别的同学聊天，只需要看同一排（行）或同一列（列）里有没有其他人。

这种做法一定能得到正确答案，因为我们对每一台服务器都做了完整的检查，满足“同一行或同一列有另一台服务器”这一条件的必然会被计数。

#### 代码（Python）

```python
from typing import List

def countServers_bruteforce(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    ans = 0

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 0:          # 这里没有服务器，直接跳过
                continue

            # 检查同一行是否还有别的服务器
            row_has_other = any(grid[i][k] == 1 for k in range(n) if k != j)

            # 检查同一列是否还有别的服务器
            col_has_other = any(grid[k][j] == 1 for k in range(m) if k != i)

            if row_has_other or col_has_other:
                ans += 1                 # 这台服务器可以通信

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n * (m + n))`  
  对每个单元格（`m*n`）都要遍历它所在的整行（`n`）和整列（`m`），所以总体是行列长度的和乘以格子数。可以把它想象成“每检查一台服务器，要跑完整条跑道一次”。  
- **空间复杂度**：`O(1)`  
  只用了常数级的额外变量（计数器、循环变量），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历整行整列**，导致大量重复工作。  
实际上，我们只需要**统计每一行和每一列里有多少台服务器**，然后再一次性判断每台服务器是否“孤立”。  

**步骤拆解**：

1. **第一次遍历**整个矩阵，记录每一行的服务器数 `row_cnt[i]`，以及每一列的服务器数 `col_cnt[j]`。  
   - 这里使用两个一维数组（列表），类似于“行统计表”和“列统计表”。  
   - 这一步的时间是 `O(m*n)`，只遍历一次。

2. **第二次遍历**矩阵，对每个 `grid[i][j] == 1` 的位置检查：  
   - 如果 `row_cnt[i] > 1`（这一行有不止一台服务器） **或** `col_cnt[j] > 1`（这一列有不止一台服务器），说明这台服务器可以通信，计数+1。  
   - 否则它是孤立的，不计数。

> **类比**：想象有一个统计员先把每排和每列的人数记下来（第一遍），之后只要看某个人所在的排或列人数是否大于 1，就能立刻判断他是否能和别人聊天（第二遍），不必再去跑完整条跑道。

#### 代码（Python）

```python
from typing import List

def countServers(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    # 1. 统计每行、每列的服务器数量
    row_cnt = [0] * m          # row_cnt[i] = 第 i 行的服务器数
    col_cnt = [0] * n          # col_cnt[j] = 第 j 列的服务器数

    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1:
                row_cnt[i] += 1
                col_cnt[j] += 1

    # 2. 再遍历一次，判断每台服务器是否可以通信
    ans = 0
    for i in range(m):
        for j in range(n):
            if grid[i][j] == 1 and (row_cnt[i] > 1 or col_cnt[j] > 1):
                ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m * n)`  
  只遍历了矩阵两遍，每遍都是一次线性扫描。相比暴力的 `O(m*n*(m+n))`，大幅降低了时间消耗。可以把它想象成“只跑两次跑道”，而不是每台服务器都跑一次。

- **空间复杂度**：`O(m + n)`  
  需要两个额外的数组分别存放每行和每列的计数，大小与行数、列数成正比。对 250×250 的限制来说，这个额外空间是可以接受的。

---

## 心得

- **核心技巧**：先统计行/列出现次数，再利用统计结果一次判断。  
- **适用的题型**  
  1. “行/列出现次数决定答案” 类似题目，如 *Number of Corner Rectangles*（统计矩形）  
  2. “出现次数 > 1 即满足条件” 的计数题，如 *Lonely Pixel I*（孤立像素）  
  3. 需要**双向统计**（行 + 列）的矩阵题目，例如 *Maximum Number of Balloons*（行列限制）  

> **解题钥匙**：**先统计，再判定**——把重复的遍历工作压缩到一次预处理里。

---

## 反思

- **第一反应**：看到“同一行或同一列”，本能想到“遍历整行整列检查”。这就是暴力思路。  
- **最容易踩的坑**  
  1. **忘记排除自身**：在暴力解里检查同一行/列时，需要确保不是自己（`k != j`、`k != i`），否则会把自己算成“另一台”。  
  2. **边界情况**：全部为 `0` 或者只有一台服务器时，答案应为 `0`，统计数组要正确初始化。  
  3. **空间误用**：如果直接在原矩阵上做标记，可能会破坏后续统计，需要额外数组或两次遍历。  

- **下次类似题的第一步**：先问自己“是否可以通过一次遍历得到所有行/列的计数？”如果答案是“可以”，就把问题转化为**统计 + 一次判定**，往往能立刻得到最优解。