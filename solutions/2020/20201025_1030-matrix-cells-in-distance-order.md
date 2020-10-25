# #1030. 按距离排序的矩阵单元格 / Matrix Cells in Distance Order

> 难度：简单 · 标签：Array、Math、Geometry、Sorting、Matrix · [LeetCode 链接](https://leetcode.com/problems/matrix-cells-in-distance-order/)

---

## 题目（英文原版）

**Description**

You are given four integers row, cols, rCenter, and cCenter. There is a rows x cols matrix and you are on the cell with the coordinates (rCenter, cCenter).
Return the coordinates of all cells in the matrix, sorted by their distance from (rCenter, cCenter) from the smallest distance to the largest distance. You may return the answer in any order that satisfies this condition.
The distance between two cells (r1, c1) and (r2, c2) is |r1 - r2| + |c1 - c2|.

**Examples**

**Example 1:**

```
Input: rows = 1, cols = 2, rCenter = 0, cCenter = 0
Output: [[0,0],[0,1]]
Explanation: The distances from (0, 0) to other cells are: [0,1]
```

**Example 2:**

```
Input: rows = 2, cols = 2, rCenter = 0, cCenter = 1
Output: [[0,1],[0,0],[1,1],[1,0]]
Explanation: The distances from (0, 1) to other cells are: [0,1,1,2]
The answer [[0,1],[1,1],[0,0],[1,0]] would also be accepted as correct.
```

**Example 3:**

```
Input: rows = 2, cols = 3, rCenter = 1, cCenter = 2
Output: [[1,2],[0,2],[1,1],[0,1],[1,0],[0,0]]
Explanation: The distances from (1, 2) to other cells are: [0,1,1,2,2,3]
There are other answers that would also be accepted as correct, such as [[1,2],[1,1],[0,2],[1,0],[0,1],[0,0]].
```

**Constraints**

- 1 <= rows, cols <= 100
- 0 <= rCenter < rows
- 0 <= cCenter < cols

---

## 题目（中文翻译）

给定四个整数 `rows`、`cols`、`rCenter` 和 `cCenter`。存在一个 `rows × cols` 的矩阵，你位于坐标为 `(rCenter, cCenter)` 的单元格。

返回矩阵中所有单元格的坐标，按照它们与 `(rCenter, cCenter)` 的距离从小到大排序。只要满足此条件，返回的顺序可以是任意的。

两个单元格 `(r1, c1)` 与 `(r2, c2)` 之间的距离定义为 `|r1 - r2| + |c1 - c2|`（曼哈顿距离）。

## 示例

### 示例 1

**输入**: `rows = 1, cols = 2, rCenter = 0, cCenter = 0`  
**输出**: `[[0,0],[0,1]]`  
**解释**: 从 `(0, 0)` 到其他单元格的距离分别为: `[0,1]`

### 示例 2

**输入**: `rows = 2, cols = 2, rCenter = 0, cCenter = 1`  
**输出**: `[[0,1],[0,0],[1,1],[1,0]]`  
**解释**: 从 `(0, 1)` 到其他单元格的距离分别为: `[0,1,1,2]`  
答案 `[[0,1],[1,1],[0,0],[1,0]]` 也被视为正确。

### 示例 3

**输入**: `rows = 2, cols = 3, rCenter = 1, cCenter = 2`  
**输出**: `[[1,2],[0,2],[1,1],[0,1],[1,0],[0,0]]`  
**解释**: 从 `(1, 2)` 到其他单元格的距离分别为: `[0,1,1,2,2,3]`  
还有其他答案同样正确，例如 `[[1,2],[1,1],[0,2],[1,0],[0,1],[0,0]]`。

## 约束

- `1 ≤ rows, cols ≤ 100`
- `0 ≤ rCenter < rows`
- `0 ≤ cCenter < cols`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把矩阵里 **所有** 的坐标都列出来，然后按照题目给的距离公式  

\[
\text{distance} = |r - r_{\text{center}}| + |c - c_{\text{center}}|
\]

计算每个坐标到中心的距离，最后把它们 **排序**。  
这里用到的唯一数据结构是 **列表**（list），相当于我们把所有格子装进一个大盒子，盒子里每个元素都是 `[r, c]`。  
排序时，Python 的 `list.sort(key=…)` 会把盒子里的元素按照我们提供的“钥匙”——这里就是距离——从小到大排列。  

> **类比**：把所有格子想成一本电话簿，每一行记录一个格子的坐标。我们要把这本簿子按“离中心的远近”重新排页，就像把词条按拼音顺序重新排列一样，只是排序规则换成了曼哈顿距离。

**为什么这个方法一定对？**  
- 我们遍历了 **所有** 可能的坐标，保证不遗漏任何格子。  
- 对每个格子都计算了 **准确的** 曼哈顿距离。  
- 排序的定义恰好是“距离从小到大”，所以排序后的顺序必然满足题目要求。

#### 代码（Python）

```python
def all_cells_dist_order(rows: int, cols: int, rCenter: int, cCenter: int):
    cells = []                              # 用来装所有格子坐标的列表
    for r in range(rows):                   # 行遍历
        for c in range(cols):               # 列遍历
            # 计算曼哈顿距离
            dist = abs(r - rCenter) + abs(c - cCenter)
            cells.append((dist, [r, c]))    # 把距离和坐标一起放进列表，方便后面排序
    # 按距离的第 0 项升序排列
    cells.sort(key=lambda x: x[0])
    # 只需要返回坐标部分
    return [coord for _, coord in cells]
```

> **关键行解释**  
> - `abs(r - rCenter) + abs(c - cCenter)`：计算曼哈顿距离。  
> - `cells.sort(key=lambda x: x[0])`：把列表按照每个元组的第一个元素（距离）从小到大排序。  
> - 最后一行的列表推导式把“距离”这层包装去掉，只留下坐标。

#### 复杂度  

- **时间复杂度**：`O(rows * cols * log(rows * cols))`  
  - 我们遍历了 `rows * cols` 个格子，产生同样数量的元素。  
  - 然后对这 `n = rows*cols` 个元素进行排序，排序的代价是 `O(n log n)`，这就是 `log` 的含义：比线性增长慢一点，但仍然可接受（比如 100×100=10,000，`log₂10,000 ≈ 14`）。  

- **空间复杂度**：`O(rows * cols)`  
  - 需要额外的列表保存每个格子的坐标和距离，大小和矩阵本身一样。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于排序——`O(n log n)` 的 `log` 部分。  
观察题目约束：`rows, cols ≤ 100`，所以矩阵最多只有 10,000 个格子。更重要的是，**曼哈顿距离的取值范围是有限且很小的**。  
最大可能的距离等于从左上角到右下角的距离：

\[
\text{maxDist} = (rows-1 - rCenter) + (cols-1 - cCenter)
\]

再加上从右上到左下等情况，真正的最大距离不超过 `rows + cols - 2`（不超过 198）。  
这意味着距离只能是 `0, 1, 2, …, maxDist` 共 `maxDist+1` 种取值。

利用这个特性，我们可以 **桶排序**（Bucket Sort）：

1. 创建 `maxDist + 1` 个空桶（每个桶是一个列表），下标代表距离。  
2. 再次遍历所有格子，计算距离 `d`，把坐标放进下标为 `d` 的桶里。  
3. 最后顺序遍历桶，从距离小的桶到大的桶依次把坐标取出来，即得到按距离升序的答案。

这样我们只用了 **线性时间** `O(rows * cols)`，不需要 `log` 的排序开销。

> **类比**：想象有一排信箱，编号从 0 到 `maxDist`，每个信箱只收“距离恰好是该编号”的格子。我们先把所有格子投递到对应的信箱，最后依次打开信箱取出信件，顺序自然就是从近到远。

#### 代码（Python）

```python
def all_cells_dist_order(rows: int, cols: int, rCenter: int, cCenter: int):
    # 可能的最大距离
    max_dist = (rows - 1 - rCenter) + (cols - 1 - cCenter)
    max_dist = max(max_dist, rCenter + cCenter)          # 也可能从左上角到中心更远
    max_dist = max(max_dist, (rows - 1 - rCenter) + cCenter)
    max_dist = max(max_dist, rCenter + (cols - 1 - cCenter))

    # 桶：下标 = 距离，值 = 坐标列表
    buckets = [[] for _ in range(max_dist + 1)]

    # 把每个格子放进对应的桶
    for r in range(rows):
        for c in range(cols):
            d = abs(r - rCenter) + abs(c - cCenter)   # 计算距离
            buckets[d].append([r, c])                # 放进第 d 桶

    # 按桶的顺序收集结果
    ans = []
    for d in range(max_dist + 1):
        ans.extend(buckets[d])                       # 直接把整个桶的内容加进答案
    return ans
```

> **关键行解释**  
> - `max_dist` 的计算考虑了四个角到中心的距离，确保上界足够大。  
> - `buckets = [[] for _ in range(max_dist + 1)]`：创建一组空桶，数量等于最大可能距离 + 1。  
> - `buckets[d].append([r, c])`：把坐标放进对应距离的桶里。  
> - `ans.extend(buckets[d])`：把当前距离的所有坐标一次性加入答案，保持原有顺序即可。

#### 复杂度  

- **时间复杂度**：`O(rows * cols)`  
  - 两次遍历矩阵（一次放进桶，一次收集），每次都是线性操作，没有 `log`。  
  - 相比暴力解，**快了一个 `log` 量级**，在数据量更大时优势更明显。

- **空间复杂度**：`O(rows * cols + maxDist)`  
  - 仍然需要保存所有坐标（`rows*cols`），再加上 `maxDist+1` 个桶的指针数组，`maxDist` 最多 200，几乎可以忽略不计。

---

## 心得

- **核心技巧**：利用 **距离取值范围有限**，用 **桶排序** 把线性遍历转化为有序输出。  
- **适用场景**：  
  1. **计数/桶排序** 题目（例如 “按频率排序字符”）。  
  2. **距离或层次有限** 的 BFS/层序遍历（例如 “二维网格的层序遍历”）。  
  3. **值域小** 的数值排序（例如 “按年龄排序”）  
- **一句话总结**：把“距离相同的格子”先放进同一个小盒子，按盒子编号顺序取出，即可省掉排序的 `log`。

---

## 反思

- **第一反应**：直接把所有格子列出来，用 `sorted` 按距离排序。  
- **最容易踩的坑**：  
  - **距离上界**算错，导致桶的大小不够，从而出现 `IndexError`。  
  - 忘记 **包含中心格子**（距离 0）在内，导致答案缺失。  
  - 在极端情况下（`rows = cols = 100`），暴力排序仍能通过，但若约束更大，就会超时。  
- **下次遇到同类题**：第一步先思考“**取值范围是否有限**”。如果是，就立刻考虑**计数/桶**的思路，而不是直接排序。这样往往能把时间复杂度从 `O(n log n)` 降到 `O(n)`。