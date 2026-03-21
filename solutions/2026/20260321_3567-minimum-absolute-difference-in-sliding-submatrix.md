# #3567. 滑动子矩阵的最小绝对差 / Minimum Absolute Difference in Sliding Submatrix

> 难度：中等 · 标签：Array、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-absolute-difference-in-sliding-submatrix/)

---

## 题目（英文原版）

**Description**

You are given an m x n integer matrix grid and an integer k.
For every contiguous k x k submatrix of grid, compute the minimum absolute difference between any two distinct values within that submatrix.
Return a 2D array ans of size (m - k + 1) x (n - k + 1), where ans[i][j] is the minimum absolute difference in the submatrix whose top-left corner is (i, j) in grid.
Note: If all elements in the submatrix have the same value, the answer will be 0.

**Examples**

**Example 1:**

```
Input: grid = [[1,8],[3,-2]], k = 2
Output: [[2]]
Explanation:
```

**Example 2:**

```
Input: grid = [[3,-1]], k = 1
Output: [[0,0]]
Explanation:
```

**Example 3:**

```
Input: grid = [[1,-2,3],[2,3,5]], k = 2
Output: [[1,2]]
Explanation:
```

**Constraints**

- 1 <= m == grid.length <= 30
- 1 <= n == grid[i].length <= 30
- -105 <= grid[i][j] <= 105
- 1 <= k <= min(m, n)

---

## 题目（中文翻译）

给定一个 `m × n` 的整数矩阵 `grid` 和一个整数 `k`。  
对于矩阵中每一个连续的 `k × k` 子矩阵（submatrix），计算该子矩阵内任意两个不同元素的 **最小绝对差**（minimum absolute difference）。  
返回一个大小为 `(m - k + 1) × (n - k + 1)` 的二维数组 `ans`，其中 `ans[i][j]` 表示左上角坐标为 `(i, j)` 的子矩阵的最小绝对差。  
**注意**：如果子矩阵中的所有元素值相同，则答案为 `0`。

## 示例

### 示例 1
**输入**  
```text
grid = [[1,8],[3,-2]], k = 2
```
**输出**  
```text
[[2]]
```
**Explanation:**  

### 示例 2
**输入**  
```text
grid = [[3,-1]], k = 1
```
**输出**  
```text
[[0,0]]
```
**Explanation:**  

### 示例 3
**输入**  
```text
grid = [[1,-2,3],[2,3,5]], k = 2
```
**输出**  
```text
[[1,2]]
```
**Explanation:**  

## 约束条件
- `1 ≤ m == grid.length ≤ 30`
- `1 ≤ n == grid[i].length ≤ 30`
- `-10^5 ≤ grid[i][j] ≤ 10^5`
- `1 ≤ k ≤ min(m, n)`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是 **枚举每一个 k×k 的子矩阵**，把里面的所有元素取出来，找出两两之间的绝对差的最小值。

- **枚举子矩阵**：左上角坐标可以是 `(i, j)`，其中  
  `0 ≤ i ≤ m‑k`，`0 ≤ j ≤ n‑k`。  
- **取出子矩阵的元素**：把这 `k·k` 个数放进一个一维列表 `vals`。  
- **排序后相邻即最小**：把 `vals` 排序后，最小的绝对差一定出现在相邻两个数之间（因为排好序后，两个数之间的差已经是最小的可能了）。于是只需要遍历一次相邻差即可得到答案。  
- **全部相同的情况**：如果子矩阵里所有数都相同，排序后相邻差全为 0，答案自然是 0。

> **类比**：把子矩阵看成一本“小字典”。把所有单词（数值）排好序后，最相近的两个单词（相邻的两个数）之间的距离，就是我们要的最小差。

这个方法一定能得到正确答案，因为我们穷举了所有子矩阵，并且在每个子矩阵里找到了真正的最小差。

#### 代码（Python）

```python
from typing import List

def min_abs_diff_bruteforce(grid: List[List[int]], k: int) -> List[List[int]]:
    m, n = len(grid), len(grid[0])
    ans_rows = m - k + 1
    ans_cols = n - k + 1
    ans = [[0] * ans_cols for _ in range(ans_rows)]

    # 遍历每个左上角 (i, j)
    for i in range(ans_rows):
        for j in range(ans_cols):
            # 1. 收集子矩阵里的所有元素
            vals = []
            for r in range(i, i + k):
                for c in range(j, j + k):
                    vals.append(grid[r][c])

            # 2. 排序后只比较相邻元素的差
            vals.sort()
            min_diff = float('inf')
            for p in range(1, len(vals)):
                diff = vals[p] - vals[p - 1]          # 已经是绝对值，因为排序后后者≥前者
                if diff < min_diff:
                    min_diff = diff
                if min_diff == 0:                     # 已经是最小可能值，提前结束
                    break

            ans[i][j] = min_diff
    return ans
```

> **代码注释**  
> - 第 7‑9 行创建返回矩阵 `ans`，大小正好是所有可能的左上角位置。  
> - 第 12‑13 行遍历所有左上角坐标。  
> - 第 15‑18 行把当前子矩阵的 `k·k` 个数全部放进列表 `vals`。  
> - 第 21 行对 `vals` 排序，随后第 22‑28 行只比较相邻两个数的差，找到最小值。  
> - 如果在遍历过程中出现 `0`，说明已经找到了最小可能的差，直接 `break`。

#### 复杂度

- **时间复杂度**：`O((m‑k+1)·(n‑k+1)·k²·log(k²))`  
  - ` (m‑k+1)·(n‑k+1)` 是子矩阵的个数。  
  - 对每个子矩阵我们要收集 `k²` 个数并排序，排序的代价是 `k²·log(k²)`。  
  - 大白话：如果整个矩阵是 30×30，k=30，最多要排一次 900 个数，耗时仍在几千次操作范围内，完全能跑。

- **空间复杂度**：`O(k²)`（用于存放单个子矩阵的元素列表）  
  - 只在遍历每个子矩阵时临时申请这个列表，最多装下 `k·k` 个整数。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要重新收集并排序 `k²` 个数**。  
如果我们能够 **在子矩阵之间“滑动”时复用已有的元素**，就能省掉大量重复工作。

**核心想法**：使用一种可以**快速插入、删除并保持有序**的数据结构——**平衡二叉搜索树**（在 Python 中可以用 `bisect` 实现的 `SortedList`）。  
我们把每一列的 **垂直窗口**（长度为 k）先维护好，然后在水平方向上滑动窗口时，只需要把左侧一列的 k 个数删掉，把右侧新进来的列的 k 个数加入。这样每一步只涉及 `k` 次插入/删除，代价是 `O(log(k²))`，而不是重新排序 `k²` 个数。

**步骤概览**：

1. **准备列的有序容器**  
   对每一列 `c`，构造一个 `SortedList col_window[c]`，里面存放从第 `0` 行到第 `k‑1` 行的元素（即当前垂直窗口）。这一步 O(m·logk)。

2. **遍历每一行的起始位置**  
   - 对每一行 `top`（子矩阵上边界），我们先把 `col_window` 中对应的 k 行数据准备好。  
   - 接下来在同一行上 **水平滑动**：  
     - 把左侧列 `left = j‑1` 的 `k` 个元素全部从全局有序容器 `window` 中删除。  
     - 把右侧列 `right = j+k‑1` 的 `k` 个元素全部插入 `window`。  
     - `window` 始终保持当前 k×k 子矩阵的全部元素有序。

3. **从有序容器直接得到最小差**  
   有序容器里相邻两个数的差就是当前子矩阵的最小绝对差，只需要一次线性扫描 `O(k²)`，但我们可以在每次插入/删除时维护一个 **相邻差的最小值**，这样查询是 `O(1)`。为简化解释，这里仍然在每个窗口里遍历相邻元素得到最小差，整体仍然是 `O(m·n·log(k²))`。

> **类比**：把整个矩阵想象成一本书，每页是 1 行。我们先把连续的 k 页（列）摘出来装进一个 **有序抽屉**。往右翻页时，只把左边那页的内容扔掉，再把新进来的那页放进去，抽屉里始终保持所有文字按字母顺序排列。这样我们随时都能快速找到相邻两词的最小字距。

#### 代码（Python）

下面的实现使用 `bisect` 手写的 `SortedList`（避免额外安装库），保持代码可直接运行。

```python
from typing import List
import bisect

class SortedList:
    """简易版的有序列表，支持 O(log n) 的插入、删除和遍历"""
    def __init__(self):
        self.data = []

    def add(self, x: int) -> None:
        bisect.insort_left(self.data, x)          # 插入保持有序

    def discard(self, x: int) -> None:
        """删除一次出现的 x（若不存在则不做）"""
        i = bisect.bisect_left(self.data, x)
        if i < len(self.data) and self.data[i] == x:
            self.data.pop(i)

    def __len__(self) -> int:
        return len(self.data)

    def __iter__(self):
        return iter(self.data)

def min_abs_diff_optimal(grid: List[List[int]], k: int) -> List[List[int]]:
    m, n = len(grid), len(grid[0])
    ans_rows = m - k + 1
    ans_cols = n - k + 1
    ans = [[0] * ans_cols for _ in range(ans_rows)]

    # 1. 为每一列准备一个垂直窗口的有序容器
    col_windows = [SortedList() for _ in range(n)]
    for c in range(n):
        for r in range(k):                     # 前 k 行
            col_windows[c].add(grid[r][c])

    # 2. 逐行遍历子矩阵的上边界
    for top in range(ans_rows):
        # 为当前行的所有列构造一个整体的有序窗口
        window = SortedList()
        for c in range(k):                     # 前 k 列组成左上角子矩阵
            for val in col_windows[c].data:   # 把整列的 k 个数全部放进 window
                window.add(val)

        # 计算左上角子矩阵的答案
        ans[top][0] = _min_adjacent_diff(window)

        # 3. 水平滑动窗口
        for left in range(1, ans_cols):
            # 移除最左侧列的 k 个元素
            col_out = left - 1
            for val in col_windows[col_out].data:
                window.discard(val)

            # 添加新进入的最右侧列的 k 个元素
            col_in = left + k - 1
            for val in col_windows[col_in].data:
                window.add(val)

            # 当前窗口的最小差
            ans[top][left] = _min_adjacent_diff(window)

        # 4. 准备下一行的列窗口（向下滑动一行）
        if top + 1 < ans_rows:
            for c in range(n):
                # 删除离开的最上面那行元素
                out_val = grid[top][c]
                col_windows[c].discard(out_val)
                # 添加新进入的最下面那行元素
                in_val = grid[top + k][c]
                col_windows[c].add(in_val)

    return ans

def _min_adjacent_diff(sorted_list: SortedList) -> int:
    """在有序容器中求相邻两个数的最小差，时间 O(len)"""
    if len(sorted_list) <= 1:
        return 0
    prev = None
    best = float('inf')
    for cur in sorted_list:
        if prev is not None:
            diff = cur - prev
            if diff < best:
                best = diff
                if best == 0:          # 已经是最小可能值，直接返回
                    return 0
        prev = cur
    return best
```

> **关键行解释**  
> - 第 12‑16 行把每列的前 `k` 行装进 `col_windows[c]`，相当于“列的垂直滑窗”。  
> - 第 24‑28 行把左上角子矩阵的所有元素一次性放进全局 `window`，随后调用 `_min_adjacent_diff` 计算答案。  
> - 第 32‑39 行实现 **水平滑动**：把左侧列的全部 `k` 个数删掉 (`discard`)，把右侧列的全部 `k` 个数加入 (`add`)。  
> - 第 49‑55 行在遍历完当前行后，准备 **向下滑动**：对每列删除最上面一行的数，加入新出现的最下面一行的数。这样下一次循环的 `col_windows` 已经是对应的垂直窗口。

#### 复杂度

- **时间复杂度**：`O((m‑k+1)·(n‑k+1)·k·log(k²) + m·n·log k)`  
  - 水平滑动每一步插入/删除 `k` 次，每次 `O(log(k²))`。  
  - 竖直滑动（切换到下一行）同样是 `k` 次插入/删除。  
  - 相比暴力的 `k²·log(k²)`，我们把每一步的工作量从 **平方级** 降到了 **线性级**，在大矩阵或较大的 `k` 时会快很多。

- **空间复杂度**：`O(k·n)`  
  - `col_windows` 保存每列的 `k` 个数，总共 `k·n`。  
  - 额外的 `window` 保存当前子矩阵的 `k²` 个数，最大也是 `k·n`（因为 `k ≤ n`），整体仍在同一个数量级。

---

## 心得

- **核心技巧**：利用 **有序容器（平衡 BST）** 实现 **滑动窗口**，在二维矩阵上同时进行 **行滑动** 与 **列滑动**，从而复用已经排序好的元素，避免重复排序。  
- **适用的题型**  
  1. “子矩阵/子数组的第 k 小/第 k 大” 类问题（需要快速查询有序统计量）。  
  2. “滑动窗口内的最大/最小差值” 或 “窗口内的不同元素个数”。  
  3. “二维范围查询” 需要动态维护有序结构的情况。  
- **一句话总结解题钥匙**：**把子矩阵看成滑动窗口，使用能快速插入/删除且保持有序的数据结构，使得每次移动只改动边缘的少量元素**。

---

## 反思

- **第一反应**：直接暴力遍历每个子矩阵并排序，代码最容易写出来。  
- **最容易踩的坑**  
  - **边界**：`k = 1` 时子矩阵只有一个元素，答案应为 `0`（因为不存在两两比较），要在代码里处理。  
  - **负数**：绝对差在排序后直接用 `后 - 前` 即可，不需要再取 `abs`，否则会多余的计算。  
  - **删除/插入的正确性**：在滑动窗口时一定要确保把**整列的 k 个数**全部删除/加入，漏掉一个会导致窗口元素数量不对，进而得到错误的最小差。  
- **下次遇到同类题**：第一步先问自己 “是否可以把整体问题拆成滑动窗口？” 然后挑选合适的 **有序容器**（如 `SortedList`、平衡树或计数桶）来实现 **增删 + 快速查询**。这样往往能把原本的 `O(k²·log(k²))` 降到 `O(k·log k)`，显著提升效率。