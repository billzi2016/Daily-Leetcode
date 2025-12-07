# #3446. 按对角线排序矩阵 / Sort Matrix by Diagonals

> 难度：中等 · 标签：Array、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/sort-matrix-by-diagonals/)

---

## 题目（英文原版）

**Description**

You are given an n x n square matrix of integers grid. Return the matrix such that:

**Examples**

**Example 1:**

```
Input: grid = [[1,7,3],[9,8,2],[4,5,6]]
Output: [[8,2,3],[9,6,7],[4,5,1]]
Explanation:

The diagonals with a black arrow (bottom-left triangle) should be sorted in non-increasing order:
The diagonals with a blue arrow (top-right triangle) should be sorted in non-decreasing order:
```

**Example 2:**

```
Input: grid = [[0,1],[1,2]]
Output: [[2,1],[1,0]]
Explanation:

The diagonals with a black arrow must be non-increasing, so [0, 2] is changed to [2, 0] . The other diagonals are already in the correct order.
```

**Example 3:**

```
Input: grid = [[1]]
Output: [[1]]
Explanation:
Diagonals with exactly one element are already in order, so no changes are needed.
```

**Constraints**

- grid.length == grid[i].length == n
- 1 <= n <= 10
- -105 <= grid[i][j] <= 105

---

## 题目（中文翻译）

**描述**  
给定一个 `n × n` 的方阵（square matrix）`grid`，返回按以下规则重新排列后的矩阵：

- 位于左下三角（包括主对角线）的每条对角线（diagonal）必须按 **非递增**（non‑increasing）顺序排序。  
- 位于右上三角的每条对角线必须按 **非递减**（non‑decreasing）顺序排序。

---

**示例 1**  
**输入**  
```json
grid = [[1,7,3],
        [9,8,2],
        [4,5,6]]
```  
**输出**  
```json
[[8,2,3],
 [9,6,7],
 [4,5,1]]
```  
**解释**  
左下三角的对角线（黑色箭头）需按非递增排序；右上三角的对角线（蓝色箭头）需按非递减排序。

---

**示例 2**  
**输入**  
```json
grid = [[0,1],
        [1,2]]
```  
**输出**  
```json
[[2,1],
 [1,0]]
```  
**解释**  
黑色箭头指向的对角线必须为非递增顺序，因此 `[0, 2]` 被改为 `[2, 0]`。其余对角线已经符合要求。

---

**示例 3**  
**输入**  
```json
grid = [[1]]
```  
**输出**  
```json
[[1]]
```  
**解释**  
只有一个元素的对角线本身已经有序，不需要做任何修改。

---

**约束条件**  

- `grid.length == grid[i].length == n`  
- `1 ≤ n ≤ 10`  
- `-10^5 ≤ grid[i][j] ≤ 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

1. **把同一条对角线的元素挑出来**  
   - 矩阵里有两种对角线需要分别处理：  
     - **左下 ↘ 右上**（从左下角往右上角走），它们的下标满足 `i + j` 相同。可以把 `i + j` 当作这条对角线的“身份证”。  
     - **左上 ↘ 右下**（从左上角往右下角走），它们的下标满足 `i - j` 相同。把 `i - j` 当作这条对角线的“身份证”。  
   - 用 Python 的 **字典（hash table）** 来收集每条对角线的所有数字。字典就像一本查字典的工具书，`key` 是对角线的身份证（`i+j` 或 `i-j`），`value` 是一个列表，装着这条对角线上的所有数。

2. **对每条对角线进行排序**  
   - 左下 ↘ 右上方向的对角线要求 **降序**（大到小），所以把对应列表 `reverse=True` 排序。  
   - 左上 ↘ 右下方向的对角线要求 **升序**（小到大），直接使用默认的升序排序。

3. **把排好序的数放回矩阵**  
   - 再遍历一次矩阵，用同样的 `i+j` / `i-j` 作为钥匙，从字典里弹出（`pop`）已经排好序的数，依次填回原位置。  

> **为什么这个方法一定对？**  
> 对角线的定义是唯一的：同一条对角线上的所有元素的 `i+j`（或 `i-j`）值必然相同。我们先把这些元素全部收集起来，排序后再原路放回，保证了每条对角线内部的顺序满足题目要求，而不影响其他对角线。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def sort_diagonally(grid: List[List[int]]) -> List[List[int]]:
    n = len(grid)

    # 1️⃣ 用两个字典分别存放两种对角线的元素
    #   key = i + j  -> 需要降序
    #   key = i - j  -> 需要升序
    diag_down = defaultdict(list)   # 左下↘右上 (i+j)
    diag_up   = defaultdict(list)   # 左上↘右下 (i-j)

    # 收集所有元素
    for i in range(n):
        for j in range(n):
            diag_down[i + j].append(grid[i][j])
            diag_up[i - j].append(grid[i][j])

    # 2️⃣ 对每条对角线排序
    for k in diag_down:
        diag_down[k].sort(reverse=True)   # 降序
    for k in diag_up:
        diag_up[k].sort()                 # 升序

    # 3️⃣ 把排好序的数放回矩阵
    for i in range(n):
        for j in range(n):
            # 先处理左下↘右上方向（因为它们已经是降序，pop() 取最后一个正好是最小的）
            grid[i][j] = diag_down[i + j].pop()
            # 再处理左上↘右下方向（升序，同样 pop() 取最后一个是最大的，正好覆盖前面的值）
            # 这里直接覆盖即可，因为题目只要求每条对角线分别满足各自的顺序
            grid[i][j] = diag_up[i - j].pop()

    return grid
```

> **关键行中文注释**  
> - `defaultdict(list)`：如果字典里没有这个键，自动创建一个空列表，省去手动 `if key not in dict` 的判断。  
> - `sort(reverse=True)`：把列表从大到小排好，等会 `pop()` 时弹出的就是最小的元素，正好对应降序需求。  
> - `pop()`：弹出并返回列表最后一个元素，时间复杂度是 O(1)，非常高效。

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - 我们遍历矩阵两次，都是 `O(n²)`。  
  - 对每条对角线排序，最坏情况下每条对角线长度为 `n`，而对角线总数也是 `O(n)`，所以整体排序的时间是 `O(n * n log n) = O(n² log n)`。  
  - 大白话：如果矩阵是 10×10，最多要排 10 条 10 长度的序列，排序每条大约要花 `10·log10` 的时间，总体仍然在几百次操作之内。

- **空间复杂度**：`O(n²)`  
  - 我们把矩阵里的所有元素都存进了字典里（两个字典各自保存一次），相当于又复制了一遍矩阵。  
  - 对于 10×10 的矩阵，最多再占用 100 个整数的空间。

---

### 2. 最优解  

#### 思路  

暴力解已经是 **最直观**、**最易实现** 的方案。  
从性能角度看，真正的“瓶颈”是 **排序**——对每条对角线做 `O(k log k)` 的排序（`k` 为对角线长度）。  
在本题的约束下（`n ≤ 10`），即使全部排序也只会产生几百次比较，已经足够快。  

不过，如果想在 **更大规模**（比如 `n = 10⁴`）时仍保持线性或接近线性的表现，可以：

1. **利用计数排序**（Counting Sort）  
   - 题目给出的数值范围是 `[-10⁵, 10⁵]`，共 `2·10⁵+1` 种可能。对每条对角线使用计数排序，时间可以降到 `O(k + V)`，其中 `V` 为数值范围。  
   - 由于 `V`（约 200k）远大于对角线长度 `k ≤ n`，在本题规模下计数排序反而不划算，但在 `n` 很大的情况下会更快。

2. **使用堆（优先队列）**  
   - 对每条对角线维护一个 **最小堆**（升序）或 **最大堆**（降序），在遍历矩阵的同时直接把元素弹出放回。  
   - 这样只需要一次遍历矩阵，堆的插入/弹出都是 `O(log k)`，整体仍是 `O(n² log n)`，但省去了先收集再排序的两遍遍历。

下面给出 **使用堆** 的实现，它在代码结构上更贴近“一次遍历完成” 的思路，也方便读者以后在更大数据规模时做改动。

#### 代码（Python）

```python
import heapq
from collections import defaultdict
from typing import List

def sort_diagonally_opt(grid: List[List[int]]) -> List[List[int]]:
    n = len(grid)

    # 1️⃣ 用两个字典分别存放两种对角线的堆
    #   对左下↘右上方向，用最大堆（通过负数实现） => 降序
    #   对左上↘右下方向，用最小堆 => 升序
    down_heap = defaultdict(list)   # i + j : 最大堆（负数）
    up_heap   = defaultdict(list)   # i - j : 最小堆

    # 把所有元素放进对应的堆里（一次遍历完成收集）
    for i in range(n):
        for j in range(n):
            heapq.heappush(down_heap[i + j], -grid[i][j])   # 负号实现最大堆
            heapq.heappush(up_heap[i - j], grid[i][j])      # 默认是最小堆

    # 2️⃣ 再遍历一次矩阵，把堆顶弹出放回
    for i in range(n):
        for j in range(n):
            # 先处理左下↘右上（降序），弹出最大值（负数取反）
            grid[i][j] = -heapq.heappop(down_heap[i + j])
            # 再处理左上↘右下（升序），弹出最小值
            grid[i][j] = heapq.heappop(up_heap[i - j])

    return grid
```

> **代码要点解释**  
> - `heapq` 是 Python 标准库里的 **最小堆** 实现。要让它变成最大堆，只需要把要比较的数取负（`-x`），负数越大，原数越小。弹出时再取相反数恢复。  
> - 两个堆分别对应两种对角线的排序方向，所有操作都在 `O(log k)` 时间内完成。  
> - 只遍历矩阵两次（一次收集，一次写回），没有额外的排序步骤。

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - 每个元素在加入堆和弹出堆时各一次，堆的高度不超过该对角线的长度 `k ≤ n`，所以每次操作是 `O(log n)`。  
  - 总共 `2·n²` 次堆操作 → `O(n² log n)`。  
  - 与暴力解的时间复杂度相同，只是 **常数因子更小**（省去一次完整的排序遍历），在大矩阵上会更快。

- **空间复杂度**：`O(n²)`  
  - 两个堆一起存放了矩阵的全部元素，仍然是原矩阵大小的两倍。

---

## 心得  

- **核心技巧**：利用下标的**线性关系**（`i+j`、`i-j`）把矩阵的对角线映射到“一维”容器（字典、堆），再分别进行**升序/降序**处理。  
- **适用的题型**  
  1. “对角线遍历”类题目，例如 *“对角线遍历矩阵”*（LeetCode 498）  
  2. “对角线上的操作”类题目，如 *“对角线最大和”*（LeetCode 1977）  
  3. 任意需要把 **同一属性的元素聚合**（如同一行、同一列、同一斜线）后排序的题目。  
- **一句话总结**：**把对角线映射到唯一键，利用堆或排序一次性完成升/降序**。

---

## 反思  

- **第一反应**：看到“对角线”和“排序”，立刻想到把每条对角线的元素收集到列表里再排序。  
- **最容易踩的坑**  
  - **键的选取错误**：左下↘右上用 `i+j`，左上↘右下用 `i-j`，弄混会导致元素归到错误的对角线。  
  - **升序/降序搞反**：题目对两种方向的要求不一样，忘记在对应的容器里加 `reverse=True` 或使用最大堆。  
  - **覆盖顺序**：在把排序好的数写回矩阵时，如果先写了升序再写降序，会把前一次写的结果覆盖掉，需要分两次写回或使用不同的容器。  
- **下次遇到同类题**：第一步先 **确定对角线的唯一标识公式**（`i+j` 或 `i-j`），然后决定 **使用列表+排序** 还是 **堆**，根据数据规模选择最合适的实现。