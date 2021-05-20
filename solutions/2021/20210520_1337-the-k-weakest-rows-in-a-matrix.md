# #1337. 矩阵中最弱的 K 行 / The K Weakest Rows in a Matrix

> 难度：简单 · 标签：Array、Binary Search、Sorting、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/the-k-weakest-rows-in-a-matrix/)

---

## 题目（英文原版）

**Description**

You are given an m x n binary matrix mat of 1's (representing soldiers) and 0's (representing civilians). The soldiers are positioned in front of the civilians. That is, all the 1's will appear to the left of all the 0's in each row.
A row i is weaker than a row j if one of the following is true:
Return the indices of the k weakest rows in the matrix ordered from weakest to strongest.

**Examples**

**Example 1:**

```
Input: mat = 
[[1,1,0,0,0],
 [1,1,1,1,0],
 [1,0,0,0,0],
 [1,1,0,0,0],
 [1,1,1,1,1]], 
k = 3
Output: [2,0,3]
Explanation: 
The number of soldiers in each row is: 
- Row 0: 2 
- Row 1: 4 
- Row 2: 1 
- Row 3: 2 
- Row 4: 5 
The rows ordered from weakest to strongest are [2,0,3,1,4].
```

**Example 2:**

```
Input: mat = 
[[1,0,0,0],
 [1,1,1,1],
 [1,0,0,0],
 [1,0,0,0]], 
k = 2
Output: [0,2]
Explanation: 
The number of soldiers in each row is: 
- Row 0: 1 
- Row 1: 4 
- Row 2: 1 
- Row 3: 1 
The rows ordered from weakest to strongest are [0,2,3,1].
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 2 <= n, m <= 100
- 1 <= k <= m
- matrix[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 `m × n` 的二进制矩阵（binary matrix）`mat`，其中 `1` 代表士兵（soldier），`0` 代表平民（civilian）。在每一行中，所有的士兵都站在平民的前面，也就是说每行的 `1` 必然出现在 `0` 的左侧。

如果满足以下任意一种情况，则第 `i` 行比第 `j` 行更弱（weaker）：

1. 第 `i` 行的士兵数量少于第 `j` 行的士兵数量；
2. 两行的士兵数量相同，但 `i < j`（即行索引更小的行视为更弱）。

返回矩阵中 **最弱的 `k` 行的索引**，按照从弱到强的顺序排列。

## 示例

### 示例 1
**输入**  
```text
mat = 
[[1,1,0,0,0],
 [1,1,1,1,0],
 [1,0,0,0,0],
 [1,1,0,0,0],
 [1,1,1,1,1]],
k = 3
```
**输出**  
```text
[2,0,3]
```
**解释**  
各行的士兵数量为：  
- 第 0 行：2  
- 第 1 行：4  
- 第 2 行：1  
- 第 3 行：2  
- 第 4 行：5  

按照从弱到强排序后得到的行索引顺序为 `[2,0,3,1,4]`，其中前 `k = 3` 个索引即为答案 `[2,0,3]`。

### 示例 2
**输入**  
```text
mat = 
[[1,0,0,0],
 [1,1,1,1],
 [1,0,0,0],
 [1,0,0,0]],
k = 2
```
**输出**  
```text
[0,2]
```
**解释**  
各行的士兵数量为：  
- 第 0 行：1  
- 第 1 行：4  
- 第 2 行：1  
- 第 3 行：1  

按照从弱到强排序后得到的行索引顺序为 `[0,2,3,1]`，前 `k = 2` 个索引即为答案 `[0,2]`。

## 约束条件
- `m == mat.length`
- `n == mat[i].length`
- `2 <= n, m <= 100`
- `1 <= k <= m`
- `mat[i][j]` 只能是 `0` 或 `1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把每一行的士兵（`1`）全部数一遍，得到 **“这行有多少兵”** 的统计值。  
统计完所有行后，我们把 **“行号 + 兵的数量”** 这对信息放进一个列表里，按照下面的规则排序：

1. 兵的数量少的排在前面（兵少的行更弱）。  
2. 兵的数量相同的情况下，行号小的排在前面（题目要求的 tie‑break）。

排序好以后，直接取前 `k` 个行号即可。

> **类比**：把每行看成一本书，`1` 是书的正文，`0` 是空白页。我们先把每本书的正文页数数出来（相当于统计 1 的个数），再把所有书按照页数从少到多排队，前 `k` 本就是最“薄”的书。

这个方法一定能得到正确答案，因为我们完整地比较了所有行的兵数，并且按照题目给出的顺序进行了排序。

#### 代码（Python）
```python
from typing import List

def kWeakestRows(mat: List[List[int]], k: int) -> List[int]:
    m = len(mat)                     # 行数
    # step1：统计每行的兵的数量
    soldier_counts = []              # 用来存放 (兵的数量, 行号)
    for i in range(m):
        cnt = 0
        for val in mat[i]:           # 线性遍历该行的每个元素
            if val == 1:
                cnt += 1
            else:                    # 一旦出现 0，后面全是 0，直接停止计数
                break
        soldier_counts.append((cnt, i))

    # step2：先按兵的数量升序，再按行号升序排序
    soldier_counts.sort()            # Python 的元组比较会先比较第一个元素，再比较第二个

    # step3：取前 k 行的行号
    return [idx for _, idx in soldier_counts[:k]]
```

#### 复杂度
- **时间复杂度**：`O(m·n + m·log m)`  
  - `m·n`：遍历整个矩阵，最坏情况每行都要看完所有 `n` 列。  
  - `m·log m`：对 `m` 条记录进行排序，排序的代价是 `log m` 级别的比较次数。  
  用大白话说，就是“先把所有数字看一遍（线性），再把它们排队（排序）”。
- **空间复杂度**：`O(m)`  
  只需要额外存放 `m` 条 `(兵的数量, 行号)` 记录，和输入矩阵本身无关。

---

### 2. 最优解

#### 思路  
暴力解的 **瓶颈** 在于两点：

1. **统计每行兵的数量时用了线性扫描**，即使我们已经知道每行的 `1` 都在左边，仍然从左到右逐个检查。  
2. **对全部 `m` 行都排序**，即使我们只需要最小的 `k` 行（`k` 可能远小于 `m`）。

我们可以分别对这两点做优化：

1. **二分查找**  
   因为每行的 `1` 必然在左侧、`0` 在右侧，整个行是一个**非递减序列** `111...000`。  
   要找第一个 `0` 的位置，只需要在该行上做二分查找，时间从 `O(n)` 降到 `O(log n)`。  
   这一步相当于在一本排好序的书里，快速定位“正文结束的页码”。

2. **堆（优先队列）取前 `k` 小**  
   Python 的 `heapq.nsmallest(k, iterable)` 能在 `O(m·log k)` 的时间内找出最小的 `k` 项，而不必对全部 `m` 项完整排序。  
   这里我们仍然把 **“兵的数量 + 行号”** 当作一个元组放进堆中，堆会自动保持“最弱的在前”。  
   当 `k` 远小于 `m` 时，这一步能显著省时。

综合起来的流程：

1. 对每一行用二分查找得到兵的数量 `cnt`（`O(log n)`）。  
2. 把 `(cnt, row_index)` 放进一个最小堆，使用 `heapq.nsmallest` 直接得到 `k` 条最弱的记录（`O(m·log k)`）。  
3. 取出这 `k` 条记录的行号，按 `cnt`、`row_index` 的顺序已经是从弱到强的，直接返回即可。

#### 代码（Python）
```python
import heapq
from typing import List

def kWeakestRows(mat: List[List[int]], k: int) -> List[int]:
    m, n = len(mat), len(mat[0])

    def count_soldiers(row: List[int]) -> int:
        """在已排序的 1...1 0...0 行上二分查找第一个 0 的下标，即为 1 的个数"""
        left, right = 0, n
        while left < right:
            mid = (left + right) // 2
            if row[mid] == 1:          # 仍在 1 的区间，往右找
                left = mid + 1
            else:                       # 已经进入 0 的区间，往左收敛
                right = mid
        return left                     # left == 第一个 0 的位置，也就是 1 的数量

    # step1：收集每行的 (兵的数量, 行号)
    pairs = []
    for i in range(m):
        cnt = count_soldiers(mat[i])    # O(log n)
        pairs.append((cnt, i))

    # step2：直接取最小的 k 条记录，heapq.nsmallest 用堆实现，复杂度约为 O(m·log k)
    weakest = heapq.nsmallest(k, pairs)

    # step3：返回行号（已经按弱到强排好序）
    return [idx for _, idx in weakest]
```

#### 复杂度
- **时间复杂度**：`O(m·log n + m·log k)`  
  - `m·log n`：对每行做二分查找，找到兵的数量。  
  - `m·log k`：使用堆取最小的 `k` 条记录。  
  与暴力解相比，**把 `n`（列数）从线性降到了对数**，并且**只保留 `k` 条记录**，在 `k << m` 时会更快。

- **空间复杂度**：`O(m)`（如果使用 `heapq.nsmallest`，内部仍会创建一个大小为 `m` 的列表）  
  若改为手动维护大小为 `k` 的最大堆，则可降至 `O(k)`，但实现稍微复杂。这里为了代码简洁，仍是 `O(m)`。

---

## 心得

- **核心技巧**：利用行内部的有序特性（所有 `1` 在左）做二分查找；使用堆（或 `heapq.nsmallest`）高效获取前 `k` 小元素。  
- **适用场景**：  
  1. “在每行/每列都有单调序列时，统计前缀或寻找临界点”。  
  2. “需要从大量数据中挑出最小（或最大）`k` 项”。  
  3. “矩阵每行都是 `0/1` 排序的特殊情形，如 LeetCode 1347、1090 等”。  
- **一句话总结**：**先用二分快速算出每行的兵数，再用堆取最小的 `k` 行**，这就是解题钥匙。

---

## 反思

- **第一反应**：看到“每行的 1 都在左边”，自然想到“数每行的 1”。于是直接写了两层循环，得到 O(m·n)。  
- **最容易踩的坑**：  
  1. **行内 1 与 0 的顺序**：如果忘记了 1 必在左，可能会误用普通计数导致不必要的遍历。  
  2. **排序的 tie‑break**：兵数相同的行必须按行号升序输出，忘记这一点会导致答案不符合题目要求。  
  3. **`k` 可能等于 `m`**：直接返回全部行时，堆的实现要能处理 `k == m` 的情况。  
- **下次类似题的第一步**：先检查**是否有内部有序结构**（如 0/1、递增序列），如果有，就考虑**二分**或**滑动窗口**等对数级别的算法；随后思考**是否只需要前 `k` 个**，若是则使用**堆/优先队列**来避免完整排序。