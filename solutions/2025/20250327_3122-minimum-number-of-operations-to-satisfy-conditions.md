# #3122. 满足条件的最小操作次数 / Minimum Number of Operations to Satisfy Conditions

> 难度：中等 · 标签：Array、Dynamic Programming、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-operations-to-satisfy-conditions/)

---

## 题目（英文原版）

**Description**

You are given a 2D matrix grid of size m x n. In one operation, you can change the value of any cell to any non-negative number. You need to perform some operations such that each cell grid[i][j] is:
Return the minimum number of operations needed.

**Examples**

**Example 1:**

```
Input: grid = [[1,0,2],[1,0,2]]
Output: 0
Explanation:

All the cells in the matrix already satisfy the properties.
```

**Example 2:**

```
Input: grid = [[1,1,1],[0,0,0]]
Output: 3
Explanation:

The matrix becomes [[1,0,1],[1,0,1]] which satisfies the properties, by doing these 3 operations:
```

**Example 3:**

```
Input: grid = [[1],[2],[3]]
Output: 2
Explanation:

There is a single column. We can change the value to 1 in each cell using 2 operations.
```

**Constraints**

- 1 <= n, m <= 1000
- 0 <= grid[i][j] <= 9

---

## 题目（中文翻译）

你得到一个大小为 `m x n` 的二维矩阵 `grid`。一次操作中，你可以把任意单元格的值改成任意非负整数。需要通过若干次操作，使得每个单元格 `grid[i][j]` 满足题目要求的条件。返回所需的最少操作次数。

**示例 1**  
**输入**: `grid = [[1,0,2],[1,0,2]]`  
**输出**: `0`  
**解释**:  
矩阵中的所有单元格已经满足属性，故不需要任何操作。

**示例 2**  
**输入**: `grid = [[1,1,1],[0,0,0]]`  
**输出**: `3`  
**解释**:  
通过 3 次操作后矩阵变为 `[[1,0,1],[1,0,1]]`，此时满足属性。

**示例 3**  
**输入**: `grid = [[1],[2],[3]]`  
**输出**: `2`  
**解释**:  
只有一列。可以把每个单元格的值改成 `1`，共需 2 次操作。

**约束条件**  
- `1 <= n, m <= 1000`  
- `0 <= grid[i][j] <= 9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

先把题目用生活化的语言说清楚：

- **矩阵**想象成一排排的**柜子**，每个柜子有 `m` 层（行），`n` 个柜子排成一列（列）。  
- **一次操作**就是把任意格子里的数字改成任意非负整数，就像把某层的商品换成别的商品。  
- **要求**有两条：
  1. 同一列的所有格子必须是相同的商品（即每列的数字全部相等）。  
  2. 相邻两列的商品必须不同（相邻列的数字不能相同）。

> **哈希表**可以帮助我们统计每一列里出现了哪些商品以及出现的次数。把哈希表想成“商品目录”，`key` 是商品种类（数字 0~9），`value` 是该商品在这一列出现的次数。

**暴力做法**：

1. **枚举每一列**，尝试把它改成 **所有可能的数字**（0~9），计算需要改动的格子数。  
2. 对每列的每个候选数字，**检查所有相邻列的候选数字**，确保相邻列的数字不相同。  
3. 把所有合法的组合的改动次数加起来，取最小值。

这个想法一定能得到答案，因为我们把**所有可能的改法**都遍历了一遍。  

> **为什么一定对？**  
> 只要我们遍历了每一列的每一个可能取值，并且在组合时遵守了“相邻列不同”的规则，最终的组合就一定是题目要求的合法解。最小的改动次数必然出现在这些组合之中。

**复杂度分析（大白话）**：

- 对每列我们要尝试 10 种数字（0~9），共 `n` 列 → 10 × n 次。  
- 对每一种选择，还要和前一列的 10 种选择比较，判断是否相同 → 再乘以 10。  
- 总的时间大概是 `10 × 10 × n = 100n`，再加上统计每列频率的 `m × n`，总体是 **O(m·n + 100·n)**，即 **O(m·n)**。  
- 空间上只需要保存每列的频率表（10 个计数）和 DP 表（每列 10 个状态），所以 **O(10·n) ≈ O(n)**。

虽然时间已经能接受（`m,n ≤ 1000`），但我们可以把 **“枚举所有组合”** 的思路写得更清晰、更易实现——这就是下面的 **最优解**。

#### 代码（Python）

```python
from itertools import product

def min_operations_bruteforce(grid):
    m, n = len(grid), len(grid[0])
    # 统计每列里每个数字出现的次数，freq[col][digit]
    freq = [[0] * 10 for _ in range(n)]
    for i in range(m):
        for j in range(n):
            val = grid[i][j]
            freq[j][val] += 1

    # 对每列的每个可能取值计算改动次数（cost = 行数 - 相同数字的行数）
    cost = [[m - freq[col][d] for d in range(10)] for col in range(n)]

    # 暴力遍历所有列的取值组合（10^n 种，实际只在 n 很小的情况下可用）
    ans = float('inf')
    for combo in product(range(10), repeat=n):
        # 检查相邻列是否不同
        if any(combo[i] == combo[i + 1] for i in range(n - 1)):
            continue
        # 计算总改动次数
        total = sum(cost[col][combo[col]] for col in range(n))
        ans = min(ans, total)

    return ans
```

> 这段代码只用于说明思路，`product(range(10), repeat=n)` 在 `n` 较大时会爆炸，实际使用请参考下面的 DP 优化。

#### 复杂度

- **时间复杂度**：`O(10^n)`（指数级）——因为我们枚举了每列的所有可能取值组合。  
  > 大白话：如果矩阵有 20 列，可能的组合就是 10 的 20 次方，根本算不完。
- **空间复杂度**：`O(m·n + n·10)` 用来存频率和代价表，基本可以忽略。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于“枚举所有列的取值组合”。我们其实不需要一次性把所有列的取值都列出来，只要在 **前面已经决定的列** 基础上，**逐列决定** 当前列的取值，并记住最小的改动次数，就能得到全局最优。  
这正是 **动态规划（Dynamic Programming，DP）** 的典型场景：

1. **状态**  
   `dp[j][v]` = 处理到第 `j` 列（0‑based）时，第 `j` 列被改成数字 `v`（0~9）所需的最少操作次数。

2. **初始状态**  
   第 0 列没有左邻居，直接用改成 `v` 的代价：  
   `dp[0][v] = cost_0(v) = m - freq_0[v]`。

3. **状态转移**  
   对第 `j` 列的每个可能数字 `v`，它必须和第 `j‑1` 列的数字 **不同**。所以：
   ```
   dp[j][v] = cost_j(v) + min{ dp[j-1][u] | u != v }
   ```
   这里的 `cost_j(v)` 同样是把第 `j` 列改成 `v` 所需的改动次数。

4. **答案**  
   最后一列可以是任意数字，取最小值：  
   `answer = min_v dp[n-1][v]`。

5. **如何快速求 `min{dp[j-1][u] | u != v}`**  
   对每一列我们只要找出 **最小值** 与 **次小值** 两个数及其对应的数字。  
   - 若当前 `v` 不是最小值对应的数字，则直接使用全局最小值。  
   - 否则使用次小值。  
   这样每列的转移只需要 `O(10)` 而不是 `O(10·10)`，但即使不做这个优化，`10·10·n = 100n` 也足够快（`n ≤ 1000`），所以这里直接用 **两层循环** 更易懂。

6. **核心数据结构**  
   - **频率数组**（哈希表的简化版）：`freq[col][digit]` 记录每列里每个数字出现的次数。  
   - **DP 数组**：只保留前一列的 10 个状态，使用滚动数组即可把空间降到 `O(10)`。

> **类比**：把每列看成一层楼的房间，`dp[j][v]` 就是“到第 `j` 层并且第 `j` 层的房间颜色是 `v` 时，最少需要刷多少层”。我们每次只关心上一层的颜色，而不必记住更早的层。

#### 代码（Python）

```python
def min_operations(grid):
    """
    返回把矩阵变成“每列相同且相邻列不同”所需的最少操作次数。
    """
    m, n = len(grid), len(grid[0])

    # 1️⃣ 统计每列里每个数字的出现次数（0~9）
    freq = [[0] * 10 for _ in range(n)]
    for i in range(m):
        for j in range(n):
            val = grid[i][j]
            freq[j][val] += 1

    # 2️⃣ 预计算把第 col 列改成 digit 的代价
    #    cost[col][digit] = 需要改动的格子数 = 行数 - 同数字的行数
    cost = [[m - freq[col][d] for d in range(10)] for col in range(n)]

    # 3️⃣ DP - 只保留上一列的 10 个状态（滚动数组）
    prev = cost[0][:]          # dp for column 0
    # prev[d] 已经是把第0列改成 d 所需的最少次数

    for col in range(1, n):
        cur = [0] * 10        # dp for current column
        for v in range(10):   # 当前列选 v
            # 在上一列中找一个与 v 不同的最小值
            best = float('inf')
            for u in range(10):
                if u == v:
                    continue
                if prev[u] < best:
                    best = prev[u]
            cur[v] = cost[col][v] + best
        prev = cur             # 向后滚动

    # 4️⃣ 最终答案是最后一列的最小值
    return min(prev)
```

> **代码要点注释**（每行中文解释已写在代码里）  
> - `freq` 用来统计每列里每个数字出现了多少次，类似“商品目录”。  
> - `cost` 直接把“要把整列改成某个数字，需要改动多少格子”算出来。  
> - DP 部分 `prev` 保存上一列的最优代价，`cur` 计算当前列的代价。  
> - 内层的两层循环（`v`、`u`）实现 “前一列的数字不能和当前列相同”。  
> - 最后 `min(prev)` 就是把所有列都处理完后最少的操作次数。

#### 复杂度

- **时间复杂度**：  
  - 统计频率：`O(m·n)`（遍历矩阵一次）。  
  - DP 转移：`O(n·10·10) = O(100·n)`，在本题约等于 `O(n)`。  
  - 合计：**O(m·n)**。  
  > 大白话：我们只需要把矩阵扫两遍，一遍统计，一遍 DP，算的格子数跟矩阵本身一样多，快得像闪电。

- **空间复杂度**：  
  - 频率表 `freq`：`n·10`，即 **O(n)**。  
  - DP 只用两行 10 长的数组：**O(1)**（常数级）。  
  - 合计：**O(n)**，在最坏情况下是 1000 × 10 = 10 000 个整数，完全可以接受。

---

## 心得

- **核心技巧**：把“每列统一且相邻列不同”转化为 **列‑>数字** 的状态，利用 **动态规划** 在每一步只考虑前一列的约束，从而避免指数级枚举。  
- **适用场景**：  
  1. **矩阵/数组的相邻约束**（如“相邻元素不能相同”“相邻行/列满足特定关系”）。  
  2. **每个位置可以选择多种颜色/数值，且相邻位置颜色需不同**（典型的涂色 DP）。  
  3. **行/列的统一约束 + 相邻不同**（如本题、LeetCode “Minimum Number of Operations to Make the Array Alternating”）。  
- **一句话总结**：  
  “把每列的取值当作状态，用 DP 记住‘到当前列为止的最小改动’，只要保证与前一列不同，就能一次遍历得到全局最优。”

---

## 反思

- **第一反应**：看到“每列相同、相邻列不同”，立刻想到 **枚举每列所有可能的数字**，随后检查相邻列是否冲突。  
- **最容易踩的坑**：  
  - **忘记统计每列的频率**，直接把每个格子都改成新数字，导致操作次数远高于最优。  
  - **相邻列相同的约束**在 DP 转移时漏掉，导致得到非法解。  
  - **边界情况**：只有一列时，只需要把该列统一即可，DP 中的 “相邻列” 检查要能够自然跳过。  
- **下次类似题的第一步**：  
  “先把每个位置的 **最小改动代价**（依据局部约束）算出来，然后思考**相邻位置的关系**，看能否用 DP 或贪心把全局最优拼起来。”