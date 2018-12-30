# #218. 天际线问题 / The Skyline Problem

> 难度：困难 · 标签：Array、Divide and Conquer、Binary Indexed Tree、Segment Tree、Line Sweep、Heap (Priority Queue)、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/the-skyline-problem/)

---

## 题目（英文原版）

**Description**

A city's skyline is the outer contour of the silhouette formed by all the buildings in that city when viewed from a distance. Given the locations and heights of all the buildings, return the skyline formed by these buildings collectively.
The geometric information of each building is given in the array buildings where buildings[i] = [lefti, righti, heighti]:
You may assume all buildings are perfect rectangles grounded on an absolutely flat surface at height 0.
The skyline should be represented as a list of "key points" sorted by their x-coordinate in the form [[x1,y1],[x2,y2],...]. Each key point is the left endpoint of some horizontal segment in the skyline except the last point in the list, which always has a y-coordinate 0 and is used to mark the skyline's termination where the rightmost building ends. Any ground between the leftmost and rightmost buildings should be part of the skyline's contour.
Note: There must be no consecutive horizontal lines of equal height in the output skyline. For instance, [...,[2 3],[4 5],[7 5],[11 5],[12 7],...] is not acceptable; the three lines of height 5 should be merged into one in the final output as such: [...,[2 3],[4 5],[12 7],...]

**Examples**

**Example 1:**

```
Input: buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
Output: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
Explanation:
Figure A shows the buildings of the input.
Figure B shows the skyline formed by those buildings. The red points in figure B represent the key points in the output list.
```

**Example 2:**

```
Input: buildings = [[0,2,3],[2,5,3]]
Output: [[0,3],[5,0]]
```

**Constraints**

- 1 <= buildings.length <= 104
- 0 <= lefti < righti <= 231 - 1
- 1 <= heighti <= 231 - 1
- buildings is sorted by lefti in non-decreasing order.

---

## 题目（中文翻译）

一个城市的天际线是从远处观察时，所有建筑形成的轮廓的外部轮廓线。给定所有建筑的位置和高度，返回这些建筑共同形成的天际线。

每栋建筑的几何信息存放在数组 `buildings` 中，其中 `buildings[i] = [left_i, right_i, height_i]`：
- `left_i` 为建筑左侧的 x 坐标  
- `right_i` 为建筑右侧的 x 坐标  
- `height_i` 为建筑的高度  

可以假设所有建筑都是坐落在高度为 0 的完全平坦地面上的完美矩形。

天际线应当表示为一系列“关键点”（key points），按 x 坐标递增排序，形式为 `[[x1,y1],[x2,y2],...]`。每个关键点都是天际线中某条水平线段的左端点，除了列表中的最后一个点——它的 y 坐标必为 0，用来标记最右侧建筑结束处的天际线终点。左侧最远建筑和右侧最远建筑之间的地面也应视为天际线的一部分。

**注意**：输出的天际线中不能出现高度相同且相邻的水平线。例如 `[..., [2,3], [4,5], [7,5], [11,5], [12,7], ...]` 是不合法的；高度为 5 的三段水平线应合并为一段，最终形式应为 `[..., [2,3], [4,5], [12,7], ...]`。

---

### 示例

#### 示例 1
```text
Input: buildings = [[2,9,10],[3,7,15],[5,12,12],[15,20,10],[19,24,8]]
Output: [[2,10],[3,15],[7,12],[12,0],[15,10],[20,8],[24,0]]
```
**解释**：  
图 A 显示了输入中的建筑。  
图 B 显示了这些建筑形成的天际线。图 B 中的红色点即为输出列表中的关键点。

#### 示例 2
```text
Input: buildings = [[0,2,3],[2,5,3]]
Output: [[0,3],[5,0]]
```

---

### 约束条件
- `1 <= buildings.length <= 10^4`
- `0 <= left_i < right_i <= 2^31 - 1`
- `1 <= height_i <= 2^31 - 1`
- `buildings` 按 `left_i` 的非递减顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把**所有可能出现的 x 坐标**都枚举出来，然后在每个 x 上算出当前最高的建筑高度，最后把相邻高度相同的点合并成一个关键点。

- **枚举 x 坐标**：把每栋建筑的左端点 `left` 和右端点 `right` 收集起来，去重并排序，得到一条离散的 “横坐标轴”。这一步可以类比成把城市地图上的所有街道拐点标记出来，只有在拐点处高度可能会改变。
- **求当前最高高度**：遍历所有建筑，如果建筑的 `left ≤ x < right`（即该建筑覆盖了这个 x），就把它的 `height` 加入候选；取最大值即为此 x 处的 skyline 高度。这里的“遍历所有建筑”就像在字典里查单词——把每个建筑当作字典的 `key`，`value` 是它的高度，只是这里我们要遍历所有 `key`。
- **合并相邻相同高度**：如果相邻两个 x 的高度相同，则它们之间是一条水平直线，不需要在结果里出现两个关键点，只保留左侧的那个。

**为什么这个方法一定能得到正确答案？**  
因为 skyline 的每个拐点必定出现在某栋建筑的左端或右端（题目已经保证）。我们把所有左、右端点都列出来并逐一计算高度，必然能够捕捉到所有拐点。只要在最后把相同高度的相邻点合并，就得到符合要求的关键点序列。

#### 代码（Python）

```python
from typing import List

def getSkyline_brute(buildings: List[List[int]]) -> List[List[int]]:
    # 1. 收集所有左端点和右端点
    xs = sorted({x for b in buildings for x in (b[0], b[2])})   # b[2] 是 right，写错了应为 b[1]
    # 正确写法：
    xs = sorted({x for b in buildings for x in (b[0], b[1])})
    
    res = []                # 最终的关键点列表
    prev_height = 0         # 前一个 x 位置的高度，方便合并相同高度

    # 2. 对每个离散的 x，求最高建筑的高度
    for x in xs:
        cur_height = 0
        for left, right, h in buildings:
            if left <= x < right:      # 建筑覆盖当前 x
                cur_height = max(cur_height, h)
        # 3. 如果高度变化了，就产生一个关键点
        if cur_height != prev_height:
            res.append([x, cur_height])
            prev_height = cur_height

    # 4. 最后加上终点 (最右侧建筑的右端, 0)
    # xs 已经包含所有右端点，最后一个右端点一定在列表里
    if res and res[-1][1] != 0:  # 防止已经是 0 的情况重复添加
        res.append([xs[-1], 0])
    return res
```

> **代码要点说明**  
> - 第 1 步使用集合 `{}` 去重，然后 `sorted` 排序，得到所有可能的拐点。  
> - 第 2 步的两层循环是暴力核心：外层遍历所有 x，内层遍历所有建筑，时间上是“**每个 x 检查每栋楼**”。  
> - 第 3 步只在高度真正改变时才记录关键点，这一步负责把连续相同高度的点合并。  

#### 复杂度

- **时间复杂度：** `O(m * n)`，其中 `n` 为建筑数量，`m` 为不同的端点数量（最多是 `2n`）。直观理解就是“每个拐点检查所有建筑”。在最坏情况下 `m≈2n`，所以大约是 `O(n²)`。  
- **空间复杂度：** `O(m)` 用于保存端点集合和排序后的列表，最多 `2n`，即 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **“每个 x 都要遍历所有建筑”**，导致二次循环。我们需要一种方式，让 **在 x 轴上前进时，能够快速知道当前最高建筑的高度**，而不是每次都全遍历。

**核心思路 → “扫描线 + 最大堆”**  

1. **把所有事件（左端点、右端点）统一放到一条时间线（x 轴）上**，并按 x 坐标从左到右排序。  
   - 左端点视为 “**加入一座建筑**”。  
   - 右端点视为 “**移除一座建筑**”。  

2. **维护一个最大堆（Priority Queue）**，堆里存的是当前“活跃”建筑的高度。  
   - 当扫描到左端点时，把这座建筑的高度 `h` **推入堆**。  
   - 当扫描到右端点时，需要把对应的建筑从堆中删除。直接删除堆里任意元素在普通堆里很难，于是我们采用 **延迟删除** 的技巧：把要删除的高度标记在一个哈希表 `to_remove` 中，等堆顶出现时再真正弹出。  

3. **每处理完一个 x 坐标的所有事件后，查看堆顶**（即当前最高建筑的高度）。如果和上一次记录的高度不同，就产生一个关键点 `[x, cur_max]`。  

4. **合并相同高度**：因为我们只在高度变化时才记录点，天然完成了合并。  

**为什么堆能快速得到最高高度？**  
堆是一种特殊的完全二叉树，根节点（堆顶）永远是最大（或最小）元素，读取它的时间是 `O(1)`，插入和删除（弹出）是 `O(log k)`，其中 `k` 是当前堆的大小。相比暴力的 `O(n)`，这是巨大的提升。

**延迟删除的类比**  
想象你在一个“高楼排行榜”里记录所有在视野内的楼的高度。当一座楼离开视野时，你并不立刻在排行榜里找它并删除（因为找起来很慢），而是把它的高度记在“待删除”名单上。等到排行榜的最高楼恰好是待删除名单里的，那你再把它真正弹出。这样整体操作仍然保持高效。

#### 代码（Python）

```python
import heapq
from typing import List

def getSkyline(buildings: List[List[int]]) -> List[List[int]]:
    """
    扫描线 + 最大堆（延迟删除）实现
    """
    # 1. 把所有事件放到一个列表中
    #   (x, -height, right)  表示左端点，height 取负号是为了让 heapq 当成最大堆使用
    #   (x, 0, 0)            表示右端点，height 为 0 表示不加入堆，只触发删除检查
    events = []
    for left, right, h in buildings:
        events.append((left, -h, right))   # 加入建筑
        events.append((right, 0, 0))       # 移除建筑的标记

    # 2. 按 x 坐标排序；如果 x 相同，左端点 (-h) 要先于右端点 (0) 处理
    events.sort()
    
    # 3. 最大堆 + 延迟删除字典
    heap = [(0, float('inf'))]   # 初始高度 0，右端点设为正无穷，永不弹出
    to_remove = {}               # height -> 需要删除的次数
    result = []
    prev_max = 0

    for x, neg_h, right in events:
        if neg_h < 0:   # 左端点，加入堆
            heapq.heappush(heap, (neg_h, right))
        else:           # 右端点，标记要删除的建筑高度
            # 因为我们不知道它在堆里的具体位置，只能记录待删除
            # 这里的 height 正好是 -neg_h = 0，实际需要删除的是对应的左端点
            # 为了统一处理，我们在后面统一弹出堆顶时检查
            # 将对应的 (height, right) 标记为待删除
            # 这里我们利用 right = 0 这个信息，直接把所有右端点对应的建筑标记删除
            # 实际上我们只需要在弹出堆顶时检查其 right 是否已经小于等于当前 x
            # 所以这里不必额外操作
            pass

        # 4. 清理堆顶：弹出已经结束（right <= x）的建筑
        while heap and heap[0][1] <= x:
            heapq.heappop(heap)

        cur_max = -heap[0][0]   # 取负号恢复真实高度
        if cur_max != prev_max:
            result.append([x, cur_max])
            prev_max = cur_max

    return result
```

> **代码要点说明**  
> 1. **事件列表**：每个左端点产生 `(left, -height, right)`，负号是为了让 Python 默认的最小堆 `heapq` 充当最大堆。右端点只需要触发一次 “检查堆顶是否已经失效”。  
> 2. **排序规则**：先按照 `x` 升序；若 `x` 相同，左端点的 `-height`（更负）会排在前面，保证在同一坐标先加入再删除。  
> 3. **堆的内容**：`(neg_height, right)`，`right` 用来判断这座建筑何时离开视野。  
> 4. **弹出失效建筑**：只要堆顶的 `right ≤ 当前 x`，说明这座建筑已经结束，弹出即可。因为堆中可能还有更高的建筑仍在视野内，所以只弹出堆顶即可。  
> 5. **产生关键点**：当当前最高高度 `cur_max` 与上一次记录的 `prev_max` 不同，就把 `[x, cur_max]` 加入结果。  

> **为什么不需要显式的“延迟删除哈希表”？**  
> 这里我们利用 `right` 信息直接在遍历时清理堆顶。因为所有右端点都会在以后出现，且堆里只关心最高的那座建筑，所以只要堆顶已经超出当前 `x`，就把它弹出。这样实现更简洁，仍然是 **延迟删除** 的一种变形。

#### 复杂度

- **时间复杂度：** `O(n log n)`  
  - 构造事件列表并排序需要 `O(n log n)`（`n` 为建筑数量，事件数是 `2n`）。  
  - 主循环中每个事件至多一次 `heapq.heappush`（`O(log n)`）和一次 `heapq.heappop`（`O(log n)`），总体也是 `O(n log n)`。  
  与暴力的二次循环相比，这大幅提升了效率。  

- **空间复杂度：** `O(n)`  
  - 事件列表占 `2n`，堆里最多保存所有仍在视野中的建筑，最坏情况下也是 `O(n)`。  

---

## 心得

- **核心技巧**：**扫描线 + 最大堆**（或平衡二叉搜索树）能够在 “左→右” 的顺序里实时维护当前最高建筑，避免重复遍历。  
- **适用的类似题型**  
  1. **“接雨水” (Trapping Rain Water)** – 需要快速知道左侧或右侧的最大高度。  
  2. **“柱状图中最大的矩形” (Largest Rectangle in Histogram)** – 同样使用单调栈维护高度的递增序列。  
  3. **“区间合并” (Merge Intervals) / “会议室计数” (Meeting Rooms II)** – 也可以用扫描线 + 最小堆求并发数。  

- **一句话总结解题钥匙**：  
  **把所有“高度变化点”排成时间线，边扫边用堆维护当前最高高度，变化即是关键点。**

---

## 反思

- **第一反应**：直接想到枚举所有端点并逐个求最高，结果是 `O(n²)`，实现简单但太慢。  
- **最容易踩的坑**  
  1. **同一 x 坐标有多个事件**：左端点必须先于右端点处理，否则会误把正在结束的建筑提前弹出。  
  2. **堆中残留已经结束的建筑**：必须在每次查询前清理 `right ≤ x` 的建筑，否则最高高度会被已经不存在的建筑“欺骗”。  
  3. **结果中出现连续相同高度的点**：一定要在高度变化时才加入关键点，否则会出现题目禁止的重复水平线。  
- **下次遇到同类题的第一步**：**先把所有“状态改变的时刻”(左端点、右端点)抽出来，排序成时间线**，然后思考用什么数据结构能在每个时刻快速得到我们需要的“当前状态”(最大高度、最小结束时间等)。这样就能从暴力直接跳到最优的扫描线方案。