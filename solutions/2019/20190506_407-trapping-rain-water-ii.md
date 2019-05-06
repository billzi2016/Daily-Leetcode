# #407. **接雨水 II** / Trapping Rain Water II

> 难度：困难 · 标签：Array、Breadth-First Search、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/trapping-rain-water-ii/)

---

## 题目（英文原版）

**Description**

Given an m x n integer matrix heightMap representing the height of each unit cell in a 2D elevation map, return the volume of water it can trap after raining.

**Examples**

**Example 1:**

```
Input: heightMap = [[1,4,3,1,3,2],[3,2,1,3,2,4],[2,3,3,2,3,1]]
Output: 4
Explanation: After the rain, water is trapped between the blocks.
We have two small ponds 1 and 3 units trapped.
The total volume of water trapped is 4.
```

**Example 2:**

```
Input: heightMap = [[3,3,3,3,3],[3,2,2,2,3],[3,2,1,2,3],[3,2,2,2,3],[3,3,3,3,3]]
Output: 10
```

**Constraints**

- m == heightMap.length
- n == heightMap[i].length
- 1 <= m, n <= 200
- 0 <= heightMap[i][j] <= 2 * 104

---

## 题目（中文翻译）

给定一个 `m x n` 的整数矩阵 `heightMap`，它表示二维高程图中每个单元格的高度（height），请返回下雨后能够收集的水的体积。

**示例 1**

```
Input: heightMap = [[1,4,3,1,3,2],
                    [3,2,1,3,2,4],
                    [2,3,3,2,3,1]]
Output: 4
Explanation: 雨后，水被困在若干块之间。这里形成了两个小水塘，分别容纳 1 单位和 3 单位的水，总共收集了 4 单位的水。
```

**示例 2**

```
Input: heightMap = [[3,3,3,3,3],
                    [3,2,2,2,3],
                    [3,2,1,2,3],
                    [3,2,2,2,3],
                    [3,3,3,3,3]]
Output: 10
```

**约束条件**

- `m == heightMap.length`
- `n == heightMap[i].length`
- `1 <= m, n <= 200`
- `0 <= heightMap[i][j] <= 2 * 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个格子都检查它能盛多少水**。  
- 把每个格子看成一个小水桶，水只能从**四周的更低或相等的格子**流走。  
- 如果一个格子四周（上、下、左、右）都有比它高的墙，那么它上面就可以存水，存的高度等于四周最高墙的最小值减去它自己的高度。  

实现上可以这样：

1. 对每个内部格子（不是边界格子，因为边界永远会漏水），  
2. 以它为中心，向四个方向扩散，找到**能够“围住”它的最低墙**。  
3. 用 `min(highest_left, highest_right, highest_up, highest_down) - height[i][j]` 计算可以存的水量（若为负则视为 0）。  

> **类比**：想象你在一块平坦的地上挖了一个坑，四周有围墙。只有当四面围墙都比坑底高时，雨水才会在坑里积聚。我们要做的，就是把每个坑的四面墙的最高高度找出来，再和坑底比较。

这个方法一定能得到正确答案，因为我们对每个格子都做了最严格的“是否被完全包围”的检查。

#### 代码（Python）

```python
from typing import List

def trapRainWater_bruteforce(heightMap: List[List[int]]) -> int:
    if not heightMap or not heightMap[0]:
        return 0
    m, n = len(heightMap), len(heightMap[0])
    total = 0

    # 只需要检查内部格子，边界格子永远漏水
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            # 四个方向的最高墙
            max_left   = max(heightMap[i][k] for k in range(0, j))
            max_right  = max(heightMap[i][k] for k in range(j + 1, n))
            max_up     = max(heightMap[k][j] for k in range(0, i))
            max_down   = max(heightMap[k][j] for k in range(i + 1, m))

            # 能够存水的高度 = 四面最高墙的最小值 - 当前格子高度
            water_level = min(max_left, max_right, max_up, max_down)
            if water_level > heightMap[i][j]:
                total += water_level - heightMap[i][j]   # 累加水量
    return total
```

#### 复杂度  

- **时间复杂度**：`O(m * n * (m + n))`  
  - 外层遍历每个内部格子是 `m·n`，而求每个方向的最高墙需要遍历整行或整列，最坏情况是 `O(m + n)`，于是乘在一起。  
  - 大白话：如果矩阵是 200×200，最坏要做大约 200·200·400 ≈ 16 万次“遍历”，对电脑来说已经有点慢了。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量，跟矩阵大小无关。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次都要重新遍历整行整列去找最高墙，这会导致大量重复计算。  
观察雨水的流动规律可以得到一个更高效的模型：

1. **水一定从四周的最低墙向内渗透**。  
   想象把整个地图倒进一个大锅里，最先“沸腾”的是最低的那面墙，水会先从这里往里填。  
2. 这正好像**逐步扩大已知安全区域**的过程：  
   - 首先把所有**边界格子**放进一个**最小堆**（Priority Queue），堆顶始终是当前未处理格子中高度**最小**的那一个。  
   - 每次取出堆顶格子 `cell`，检查它的四个相邻格子 `nbr`（上下左右）。  
     - 如果 `nbr` 已经被访问过，就跳过。  
     - 否则，**如果 `nbr` 的高度低于 `cell` 的高度**，说明 `nbr` 能被 `cell` 那个更高的墙挡住，能够存水，存的体积是 `cell.height - nbr.height`。  
     - 然后把 `nbr` 加入堆中，**高度取 max(nbr.height, cell.height)**，因为水面已经上升到 `cell.height`，后续继续用这个更高的“墙”去比较。  

这个过程类似 **Dijkstra 最短路**：我们总是从当前**最小的“墙”**出发，保证每个格子第一次被确定的水位就是最小可能的水位，从而不会出现后续再降低的情况。

> **类比**：把每个格子想成一个装水的容器，边界的容器先放进一个“最小高度的水池”。我们每次把“最低的水池”倒出，看看它能向哪儿倒水（即向未处理的相邻格子），如果相邻格子比它低，就能装水；如果更高，就直接变成新的“墙”。这样一步步把整个地图的水位确定下来。

#### 代码（Python）

```python
import heapq
from typing import List, Tuple

def trapRainWater(heightMap: List[List[int]]) -> int:
    """
    使用最小堆 + BFS 的思路求二维雨水收集量。
    """
    if not heightMap or not heightMap[0]:
        return 0

    m, n = len(heightMap), len(heightMap[0])
    visited = [[False] * n for _ in range(m)]      # 标记是否已放入堆
    heap: List[Tuple[int, int, int]] = []          # (高度, 行, 列)

    # 1️⃣ 把所有边界格子加入堆，构成初始“围墙”
    for i in range(m):
        for j in (0, n - 1):                        # 左右两列
            heapq.heappush(heap, (heightMap[i][j], i, j))
            visited[i][j] = True
    for j in range(1, n - 1):
        for i in (0, m - 1):                        # 上下两行（去掉已经加入的四角）
            heapq.heappush(heap, (heightMap[i][j], i, j))
            visited[i][j] = True

    total_water = 0
    dirs = [(1,0), (-1,0), (0,1), (0,-1)]          # 四个方向

    # 2️⃣ 不断从堆中取出当前最低的墙，向四周扩散
    while heap:
        height, x, y = heapq.heappop(heap)         # 当前最小高度的格子
        # 检查四邻格子
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= m or ny < 0 or ny >= n or visited[nx][ny]:
                continue
            visited[nx][ny] = True
            neighbor_h = heightMap[nx][ny]

            # 如果邻格子比当前墙低，就能存水
            if neighbor_h < height:
                total_water += height - neighbor_h   # 累加水量

            # 将邻格子加入堆，实际高度取 max(原高度, 当前墙高度)
            heapq.heappush(heap, (max(neighbor_h, height), nx, ny))

    return total_water
```

#### 复杂度  

- **时间复杂度**：`O(m * n log(m * n))`  
  - 每个格子至多进入堆一次，堆的大小最多是 `m·n`，每次弹出或插入的代价是 `log(heap size)`，即 `log(m·n)`。  
  - 大白话：如果矩阵是 200×200（共 40 000 格），我们大约需要 40 000 次 `log` 计算，`log2(40000)≈15`，所以整体操作大约在 600 k 次左右，速度非常快。

- **空间复杂度**：`O(m * n)`  
  - 需要一个 `visited` 矩阵记录是否已经放入堆，以及堆本身最坏也会装下所有格子。  
  - 对于 200×200 的矩阵，这大约是 40 000 个布尔值和 40 000 个元组，完全可以接受。

---

## 心得

- **核心技巧**：**最小堆 + BFS**（或称为“海拔从外向内逐层灌水”）。  
- 该技巧常用于**“从边界向内部扩展、始终维护当前最小约束”**的题目，例如  
  1. **Trapping Rain Water II**（本题）  
  2. **Swim in Rising Water**（LeetCode 778）——在上升的水位中寻找最早能到达的路径  
  3. **Pacific Atlantic Water Flow**（LeetCode 417）——从两海岸逆向遍历判断能否流到海洋  

- **一句话总结**：  
  “把四周的最低墙当作起点，始终用最小堆保证每次只从当前最矮的墙向内扩张，就能一次遍历完全部格子并正确算出蓄水量。”

---

## 反思

- **第一反应**：看到二维矩阵，立刻想到对每个格子单独判断四周最高墙，这就是暴力思路。  
- **最容易踩的坑**：  
  - **边界格子永远不能存水**，一定要先把它们加入堆并标记已访问。  
  - **更新堆中格子的高度**时要取 `max(neighbor_h, current_wall_h)`，否则后续可能错误地把已经升高的水面当作更低的墙继续填水，导致重复计量。  
  - **重复访问**：忘记 `visited` 标记会导致同一个格子被多次加入堆，导致错误的水量计算和时间浪费。  

- **下次类似题的第一步**：  
  “先把所有**边界**（或所有已知的‘安全’/‘起始’）节点放进**最小堆**，然后用**BFS**逐层扩展，每次弹出最小的节点并更新邻居的约束”。这样就能把思路直接套用到多数“从外向内、最小约束”类问题上。