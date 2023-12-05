# #2500. 删除每行的最大值 / Delete Greatest Value in Each Row

> 难度：简单 · 标签：Array、Sorting、Heap (Priority Queue)、Matrix、Simulation · [LeetCode 链接](https://leetcode.com/problems/delete-greatest-value-in-each-row/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix grid consisting of positive integers.
Perform the following operation until grid becomes empty:
Note that the number of columns decreases by one after each operation.
Return the answer after performing the operations described above.

**Examples**

**Example 1:**

```
Input: grid = [[1,2,4],[3,3,1]]
Output: 8
Explanation: The diagram above shows the removed values in each step.
- In the first operation, we remove 4 from the first row and 3 from the second row (notice that, there are two cells with value 3 and we can remove any of them). We add 4 to the answer.
- In the second operation, we remove 2 from the first row and 3 from the second row. We add 3 to the answer.
- In the third operation, we remove 1 from the first row and 1 from the second row. We add 1 to the answer.
The final answer = 4 + 3 + 1 = 8.
```

**Example 2:**

```
Input: grid = [[10]]
Output: 10
Explanation: The diagram above shows the removed values in each step.
- In the first operation, we remove 10 from the first row. We add 10 to the answer.
The final answer = 10.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 50
- 1 <= grid[i][j] <= 100

---

## 题目（中文翻译）

给定一个由正整数构成的 **m × n** 矩阵（matrix）`grid`。  
重复执行以下 **操作（operation）** 直至 `grid` 为空（即所有列都被删除）：

1. 对每一行（row），找出并删除该行中的最大值（若有多个相同的最大值，可任意删除其中一个）。  
2. 将本次删除得到的所有值中的最大值加入答案（answer）中。

注意：每执行一次操作后，矩阵的列数会减少 1（因为每行都少了一个元素）。

返回完成上述所有操作后得到的答案。

**示例 1**  
**输入**  
``` 
grid = [[1,2,4],[3,3,1]]
```  
**输出**  
```
8
```  
**解释**  
上图展示了每一步删除的值。  
- 第一次操作，删除第一行的 `4` 与第二行的 `3`（第二行有两个 `3`，任选其一），将 `4` 加入答案。  
- 第二次操作，删除第一行的 `2` 与第二行的 `3`，将 `3` 加入答案。  
- 第三次操作，删除第一行的 `1` 与第二行的 `1`，将 `1` 加入答案。  
最终答案为 `4 + 3 + 1 = 8`。

**示例 2**  
**输入**  
``` 
grid = [[10]]
```  
**输出**  
```
10
```  
**解释**  
- 第一次操作，删除唯一的 `10` 并将其加入答案。  
最终答案为 `10`。

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 <= m, n <= 50`  
- `1 <= grid[i][j] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把题目描述 **原原本本** 按顺序模拟一遍：

1. **遍历每一行**，在该行还未被删除的格子里找出最大的数，这一步相当于“在一行里找最高的山”。  
2. 把这行找到的最大值**标记为已删除**（可以把它设成 `-inf`，相当于在字典里把这个词划掉）。  
3. 把本轮所有行的最大值取**整体最大**，加入答案。  

把上面 1~3 的过程重复 `n` 次（因为每次都会把每行的一个格子删掉，列数会慢慢变成 0），最后得到的累加和就是答案。

> **类比**：  
> - 哈希表（字典）就像查字典，`key` 是单词，`value` 是页码。这里我们用 `grid[i][j] = -inf` 把“已经删掉的格子”标记为“这页已经不存在”。  
> - 找每行的最大值就像在每条街道上找最高的楼，最高楼的高度再和其它街道的最高楼比较，取最高的那一栋加入总费用。

**为什么正确**：  
每一次操作题目都要求 **先在每行删除最大的数**，再 **把本轮被删除的最大数加到答案**。我们完全按照这个顺序去做，没有漏掉任何一步，也没有提前做不该做的事，所以最终答案必然和题目要求一致。

**时间/空间分析（大白话）**：  
- 每轮我们要遍历 `m` 行，每行再遍历 `n` 列找最大，时间是 `m × n`。  
- 需要做 `n` 轮（因为每轮删掉一列），于是总时间是 `n × (m × n) = m·n²`。  
  - 用大 O 表示就是 **O(m·n²)**，可以想象成“把每个格子看了 n 次”。  
- 只用了原矩阵本身再加几个临时变量，**额外空间是 O(1)**，即“几张纸”。

#### 代码（Python）

```python
from typing import List

def delete_greatest_value_bruteforce(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])
    ans = 0                       # 最终答案

    # 重复 n 次，每次相当于“删掉一列”
    for _ in range(n):
        row_maxes = []            # 本轮每行删除的最大值

        # 1️⃣ 在每行找最大（未被删除的）
        for i in range(m):
            max_val = -1
            max_j = -1
            for j in range(n):
                if grid[i][j] > max_val:   # 找到更大的数
                    max_val = grid[i][j]
                    max_j = j
            # 2️⃣ 标记为已删除（设成负无穷，后面不会再被选到）
            grid[i][max_j] = -float('inf')
            row_maxes.append(max_val)

        # 3️⃣ 本轮的最大值加入答案
        ans += max(row_maxes)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n²)` — 每轮遍历 `m·n`，共 `n` 轮，等价于“把每个格子看了 n 次”。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量，矩阵本身就地改动。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **瓶颈** 出在每轮都要 **遍历整行** 去找最大，这导致了 `n` 次的重复扫描。  
如果我们在一开始就把每行的元素 **从大到小排好序**，那么第 1 轮我们直接取每行的第 1 个元素，第 2 轮取第 2 个，第 `k` 轮取第 `k` 个——**不需要再遍历找最大**，因为排序已经把最大的排在前面了。

具体步骤：

1. **对每一行做降序排序**。这一步相当于把每条街道的楼按高度从高到低排好队。  
2. 排序后，第 `j` 列（`j` 从 0 开始）对应的是每行第 `j` 大的数。我们只要把第 `j` 列所有行的数取 **最大值**，累加到答案。  
   - 这一步可以看成 “每轮把排好队的第 `j` 个人的身高取最大”。  
3. 对所有列 `j = 0 … n-1` 重复第 2 步，得到最终答案。

**为什么正确**：  
- 第 `j` 轮操作要求 “在每行删除当前剩余的最大数”。排序后，第 `j` 大的数正好是第 `j` 轮被删除的数。  
- 题目再要求 “把本轮被删除的最大数加入答案”。第 `j` 列的最大值正是本轮被删除的最大数。  
- 因此 **按列取最大并求和** 与题目原始描述等价。

**核心算法/数据结构**：

- **排序**（Python 的 `list.sort(reverse=True)`）：把每行的元素从大到小排好。排序的时间复杂度是 `O(n log n)`，这里的 `n` 是每行的列数。  
- **遍历二维矩阵**：一次遍历所有列，取每列最大值，时间 `O(m·n)`。

**类比/图示**（文字版）：

```
原矩阵（每行未排序）          排序后（每行降序）          取列最大并累加
[1, 2, 4]          →          [4, 2, 1]          →   col0 max = 4
[3, 3, 1]          →          [3, 3, 1]          →   col1 max = 3
                                             →   col2 max = 1
答案 = 4 + 3 + 1 = 8
```

#### 代码（Python）

```python
from typing import List

def delete_greatest_value_optimal(grid: List[List[int]]) -> int:
    m, n = len(grid), len(grid[0])

    # 1️⃣ 每行降序排序（把每条街道的楼从高到低排好队）
    for row in grid:
        row.sort(reverse=True)

    ans = 0
    # 2️⃣ 按列遍历，取每列的最大值并累加
    for col in range(n):
        col_max = max(grid[row][col] for row in range(m))
        ans += col_max

    return ans
```

#### 复杂度

- **时间复杂度**：`O(m·n log n)`  
  - 每行排序 `O(n log n)`，共 `m` 行 → `O(m·n log n)`。  
  - 再遍历一次矩阵取列最大 `O(m·n)`，与前者同阶或更小，整体仍是 `O(m·n log n)`。  
  - 与暴力解的 `O(m·n²)` 相比，**把 `n` 从乘法降到了对数**，在 `n` 较大时快很多。

- **空间复杂度**：`O(1)`（如果可以在原矩阵上就地排序）  
  - 只用了常数级的临时变量；排序本身是原地的，不需要额外数组。

---

## 心得

- **核心技巧**：先对每行降序排序，再按列取最大并求和。  
- **适用的题型**：  
  1. 需要“每轮在每行取最大”并累计最大值的矩阵题（如本题）。  
  2. “对每行/列做排序后再聚合”的问题（如 “Maximum Row Sum After Column Sort”）。  
  3. “分层取最大/最小” 的多轮删除类题目（如 “Delete Columns to Make Sorted II” 的思路）。  
- **一句话总结**：**先把每行排好序，后面每一轮直接取对应位置的最大值即可**。

---

## 反思

- **第一反应**：看到“每轮在每行删最大”，立刻想到**逐行扫描**，于是写出了暴力模拟。  
- **最容易踩的坑**：  
  - **边界条件**：`m`、`n` 都可能为 1，需要确保循环不会越界。  
  - **删除标记**：如果直接把删掉的元素设为 `0`，会误导后面的最大值判断（因为 0 仍然是正数范围内的合法值）。使用 `-inf` 更安全。  
  - **排序改变原矩阵**：如果后续还有其他操作，记得拷贝一份再排序。  
- **下次遇到同类题**：第一步先思考**“能否把重复的搜索变成一次性预处理（如排序、前缀和）”**，如果可以，就立刻把预处理写进去，再在此基础上做一次遍历求解。