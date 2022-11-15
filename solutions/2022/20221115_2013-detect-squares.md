# #2013. 检测正方形 / Detect Squares

> 难度：中等 · 标签：Array、Hash Table、Design、Counting · [LeetCode 链接](https://leetcode.com/problems/detect-squares/)

---

## 题目（英文原版）

**Description**

You are given a stream of points on the X-Y plane. Design an algorithm that:
An axis-aligned square is a square whose edges are all the same length and are either parallel or perpendicular to the x-axis and y-axis.
Implement the DetectSquares class:

**Examples**

**Example 1:**

```
Input
["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
[[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]
Output
[null, null, null, null, 1, 0, null, 2]

Explanation
DetectSquares detectSquares = new DetectSquares();
detectSquares.add([3, 10]);
detectSquares.add([11, 2]);
detectSquares.add([3, 2]);
detectSquares.count([11, 10]); // return 1. You can choose:
                               //   - The first, second, and third points
detectSquares.count([14, 8]);  // return 0. The query point cannot form a square with any points in the data structure.
detectSquares.add([11, 2]);    // Adding duplicate points is allowed.
detectSquares.count([11, 10]); // return 2. You can choose:
                               //   - The first, second, and third points
                               //   - The first, third, and fourth points
```

**Constraints**

- point.length == 2
- 0 <= x, y <= 1000
- At most 3000 calls in total will be made to add and count.

---

## 题目（中文翻译）

你将会接收到一个位于 **X‑Y 平面** 上的点的连续数据流（stream）。请设计一种算法，使得能够：

- **add(point)**：向数据流中加入一个点 `point = [x, y]`。  
- **count(point)**：统计并返回当前数据流中，以 `point` 为一个顶点且能形成 **轴对齐正方形（axis-aligned square）** 的所有可能正方形的数量。  

**轴对齐正方形（axis-aligned square）** 是指其四条边长度相等，且每条边要么平行于 x 轴，要么垂直于 x 轴（同理相对于 y 轴）。

实现 `DetectSquares` 类，使其支持上述两种操作。

---

### 示例

```text
输入
["DetectSquares", "add", "add", "add", "count", "count", "add", "count"]
[[], [[3, 10]], [[11, 2]], [[3, 2]], [[11, 10]], [[14, 8]], [[11, 2]], [[11, 10]]]

输出
[null, null, null, null, 1, 0, null, 2]

解释
DetectSquares detectSquares = new DetectSquares();
detectSquares.add([3, 10]);          // 添加点 (3, 10)
detectSquares.add([11, 2]);          // 添加点 (11, 2)
detectSquares.add([3, 2]);           // 添加点 (3, 2)
detectSquares.count([11, 10]);       // 返回 1，唯一的轴对齐正方形顶点为 (3,2), (3,10), (11,2), (11,10)
detectSquares.count([14, 8]);        // 返回 0，没有形成正方形的组合
detectSquares.add([11, 2]);          // 再次添加点 (11, 2)，此时该点出现两次
detectSquares.count([11, 10]);       // 返回 2，考虑到 (11,2) 出现两次，形成两种不同的正方形组合
```

---

### 约束条件

- `point.length == 2`
- `0 <= x, y <= 1000`
- `add` 和 `count` 方法的调用总次数不超过 **3000** 次。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

把所有出现过的点都存进一个 **列表**（就像把每次看到的坐标写在纸上）。  
当要查询 `count(point)` 时，我们把纸上的每一个点 `(x1, y1)` 当作可能的**左上角**或**左下角**，尝试和查询点 `(x, y)` 组成一个轴对齐的正方形：

1. 先算出水平距离 `d = |x - x1|`。如果 `d == 0`，说明两点在同一竖线上，根本不可能形成正方形，直接跳过。  
2. 正方形的另一条水平边必须在 `y ± d`（即上方或下方）的位置。于是我们得到两个候选点  
   - `(x, y ± d)`   （和查询点在同一列）  
   - `(x1, y ± d)`  （和左侧点在同一列）  
3. 检查这两个候选点是否已经出现过（在列表里出现过多少次，就算多少种组合）。

因为 **列表** 只能线性查找，所以每次查询都要遍历所有已有点，时间会很慢。  

> **类比**：把列表想象成一本电话簿，想找某个名字对应的电话号码只能从头到尾翻，效率自然不高。

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

class DetectSquares:
    def __init__(self):
        # 用一个列表记录所有加入的点，可能会有重复点
        self.points: List[List[int]] = []
        # 另建一个哈希表统计每个点出现的次数，后面计数时会用到
        self.cnt = defaultdict(int)   # key: (x, y) -> 出现次数

    def add(self, point: List[int]) -> None:
        """把新点加入数据结构"""
        x, y = point
        self.points.append(point)
        self.cnt[(x, y)] += 1          # 出现次数 +1

    def count(self, point: List[int]) -> int:
        """返回以 point 为一个顶点，能够组成的轴对齐正方形的个数"""
        x, y = point
        ans = 0

        # 暴力遍历所有已经出现过的点，尝试把它当作同一水平线上的另一个顶点
        for (x1, y1) in self.points:
            # 必须在同一水平线上，且水平距离不为 0
            if y1 != y or x1 == x:
                continue
            d = abs(x1 - x)            # 正方形的边长

            # 两种可能的垂直方向：上方或下方
            for ny in (y + d, y - d):
                # 检查另外两个角是否存在
                cnt1 = self.cnt.get((x, ny), 0)   # (x, ny) 的出现次数
                cnt2 = self.cnt.get((x1, ny), 0)  # (x1, ny) 的出现次数
                ans += cnt1 * cnt2                # 组合数相乘
        return ans
```

> **关键行解释**  
> - `self.cnt[(x, y)] += 1`：把点的出现次数记下来，后面查询时可以一次 O(1) 得到。  
> - `if y1 != y or x1 == x: continue`：只保留与查询点在同一水平线且不重合的点。  
> - `ans += cnt1 * cnt2`：如果 `(x, ny)` 出现了 `a` 次，`(x1, ny)` 出现了 `b` 次，则这两点可以和前面的两点组合出 `a*b` 种正方形。

#### 复杂度  

- **时间复杂度**：`O(N)`，其中 `N` 为已经加入的点的总数。因为每次 `count` 都要遍历整个列表。  
  - 大白话：如果已经加入了 1000 个点，查询一次就要看 1000 次，像是每次都要把全部纸条重新翻一遍。  
- **空间复杂度**：`O(N)`，存储所有点以及它们的计数。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **遍历所有点**。其实我们只需要关心 **与查询点同一水平线的点**，而不是全部点。  
如果我们把点按照 **x 坐标** 分组保存（即 `x -> {y: count}`），那么：

1. 给定查询点 `(x, y)`，只取出所有 **在同一水平线上** 的点，即 `x'` 与 `x` 不同但 `y' == y`。这些点可以直接从 `x` → `y` 的哈希表里拿到，复杂度是 `O(k)`，`k` 为同一水平线上点的数量。  
2. 对每个这样的点 `(x1, y)`，设水平距离 `d = |x1 - x|`。正方形的另外两条垂直边必须在 `y ± d`。我们只需要检查这两个坐标是否出现过，并乘上它们的出现次数即可。  
3. 计数时仍然使用之前保存的 **点出现次数**，所以每种组合都能正确统计。

> **类比**：把所有点按照列（x 坐标）放进抽屉，每个抽屉里再按行（y 坐标）放小格子。要找同一水平线的点，只需要打开对应的抽屉，直接查看里面的格子，省去了翻遍所有抽屉的时间。

实现细节：

- 用 `defaultdict(lambda: defaultdict(int))` 构建二维哈希表 `cnt[x][y]`，表示坐标 `(x, y)` 出现的次数。  
- `add` 只需要 `cnt[x][y] += 1`，时间 O(1)。  
- `count`：遍历 `cnt[x1]`（即所有 **列** 为 `x1` 的点），挑选出 `y == query_y` 的那些点，随后做上面的检查。整体时间 `O(k)`，最坏情况下 `k ≤ 1000`（因为坐标范围 0~1000），远小于 `N`（最多 3000 次调用）。

#### 代码（Python）  

```python
from collections import defaultdict
from typing import List

class DetectSquares:
    def __init__(self):
        # 二维哈希表：cnt[x][y] = 该坐标出现的次数
        self.cnt = defaultdict(lambda: defaultdict(int))

    def add(self, point: List[int]) -> None:
        """向数据结构中加入一个点"""
        x, y = point
        self.cnt[x][y] += 1          # 计数 +1

    def count(self, point: List[int]) -> int:
        """返回以 point 为一个顶点，能够组成的轴对齐正方形的个数"""
        x, y = point
        ans = 0

        # 遍历所有可能的“同一水平线上的另一个点”
        # 只需要看所有不同的列 x1（即 cnt 中的键），并检查该列在 y 这一行是否有点
        for x1, col in self.cnt.items():
            if x1 == x:                # 同一列不可能构成水平边
                continue
            if y not in col:           # 该列在查询行没有点，直接跳过
                continue

            d = abs(x1 - x)            # 正方形的边长
            # 两个可能的垂直方向（上方或下方）
            for ny in (y + d, y - d):
                cnt1 = self.cnt[x].get(ny, 0)   # (x, ny) 的出现次数
                cnt2 = self.cnt[x1].get(ny, 0)  # (x1, ny) 的出现次数
                # 组合数：左上/左下角出现 cnt1 次，右上/右下角出现 cnt2 次
                ans += cnt1 * cnt2
        return ans
```

> **关键行解释**  
> - `self.cnt = defaultdict(lambda: defaultdict(int))`：外层键是 `x`，内层键是 `y`，两层哈希表像是 **坐标矩阵**，查询任意点的出现次数都是 O(1)。  
> - `if y not in col: continue`：只关注在同一水平线（相同 `y`）的点，省掉大量不相关的列。  
> - `cnt1 * cnt2`：如果 `(x, ny)` 出现了 2 次，`(x1, ny)` 出现了 3 次，则这两个位置可以和前面的两个点组合出 `2 * 3 = 6` 种正方形。

#### 复杂度  

- **时间复杂度**：`O(k)`，其中 `k` 为与查询点同一水平线上不同 `x` 的点数。  
  - 在最坏情况下（所有点都在同一行），`k ≤ 1000`（因为 `x` 范围是 0~1000），仍然远小于暴力解的 `O(N)`。  
- **空间复杂度**：`O(N)`，存储所有出现过的点及其计数。  

与暴力解对比：  
- 暴力解每次查询要遍历 **所有** 点，最坏 `O(N)`（N 最高可达 3000）。  
- 最优解只遍历 **同一行** 的点，实际运行更快，且代码结构更清晰。  

---

## 心得  

- **核心技巧**：利用哈希表把点按照坐标分层存储，实现**按行/列快速定位**。  
- **适用场景**：  
  1. **检测轴对齐矩形/正方形**（如 LeetCode 750 `Number Of Corner Rectangles`）。  
  2. **求同一纵横线上的点对**（如 “点对点” 统计题目）。  
  3. **二维频次统计**（如 “查询矩形内点的数量” 类题）。  
- **一句话总结**：把二维平面拆成“列 → 行”两层哈希表，查询时只看同一行的点，时间从全局 O(N) 降到局部 O(k)。  

---

## 反思  

- **第一反应**：直接把所有点保存在列表里，遍历求解。  
- **最容易踩的坑**：  
  - **重复点**：同一个坐标可能被 `add` 多次，需要计数而不是只判断是否存在。  
  - **边界**：`d = 0` 时不构成正方形，必须排除。  
  - **坐标范围**：虽然坐标上限是 1000，但仍然要用哈希表而不是固定大小的二维数组，以免浪费空间。  
- **下次遇到类似题**：第一步先思考 **“我需要哪些点的关系？”**，如果是“同一行/列”，就立即考虑 **按行/列分组的哈希表**；如果是“同一斜率”，则考虑 **按对角线哈希**。这样可以快速定位相关点，避免全局遍历。