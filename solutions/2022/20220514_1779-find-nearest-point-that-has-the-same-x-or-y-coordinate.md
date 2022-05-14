# #1779. 寻找与当前点具有相同 X 或 Y 坐标的最近点 / Find Nearest Point That Has the Same X or Y Coordinate

> 难度：简单 · 标签：Array · [LeetCode 链接](https://leetcode.com/problems/find-nearest-point-that-has-the-same-x-or-y-coordinate/)

---

## 题目（英文原版）

**Description**

You are given two integers, x and y, which represent your current location on a Cartesian grid: (x, y). You are also given an array points where each points[i] = [ai, bi] represents that a point exists at (ai, bi). A point is valid if it shares the same x-coordinate or the same y-coordinate as your location.
Return the index (0-indexed) of the valid point with the smallest Manhattan distance from your current location. If there are multiple, return the valid point with the smallest index. If there are no valid points, return -1.
The Manhattan distance between two points (x1, y1) and (x2, y2) is abs(x1 - x2) + abs(y1 - y2).

**Examples**

**Example 1:**

```
Input: x = 3, y = 4, points = [[1,2],[3,1],[2,4],[2,3],[4,4]]
Output: 2
Explanation: Of all the points, only [3,1], [2,4] and [4,4] are valid. Of the valid points, [2,4] and [4,4] have the smallest Manhattan distance from your current location, with a distance of 1. [2,4] has the smallest index, so return 2.
```

**Example 2:**

```
Input: x = 3, y = 4, points = [[3,4]]
Output: 0
Explanation: The answer is allowed to be on the same location as your current location.
```

**Example 3:**

```
Input: x = 3, y = 4, points = [[2,3]]
Output: -1
Explanation: There are no valid points.
```

**Constraints**

- 1 <= points.length <= 104
- points[i].length == 2
- 1 <= x, y, ai, bi <= 104

---

## 题目（中文翻译）

给定两个整数 `x` 和 `y`，它们表示你在笛卡尔坐标系（Cartesian grid）中的当前位置 `(x, y)`。同时给定一个数组 `points`，其中 `points[i] = [ai, bi]` 表示在坐标 `(ai, bi)` 处存在一个点。若一个点的 **x 坐标** 或 **y 坐标** 与你的当前位置相同，则该点是有效的。

返回满足条件的有效点在 `points` 中的下标（0 起始），且该点到你当前位置的曼哈顿距离（Manhattan distance）最小。如果有多个满足最小距离的点，返回下标最小的那个。如果不存在任何有效点，返回 `-1`。

两点 `(x1, y1)` 与 `(x2, y2)` 的曼哈顿距离定义为 `abs(x1 - x2) + abs(y1 - y2)`。

---

### 示例

**示例 1**  
```text
Input: x = 3, y = 4, points = [[1,2],[3,1],[2,4],[2,3],[4,4]]
Output: 2
```
**解释**：在所有点中，只有 `[3,1]`、`[2,4]` 和 `[4,4]` 是有效点。  
在这些有效点中，`[2,4]` 与 `[4,4]` 与当前位置的曼哈顿距离均为 `1`，是最小的。  
`[2,4]` 的下标最小，所以返回 `2`。

**示例 2**  
```text
Input: x = 3, y = 4, points = [[3,4]]
Output: 0
```
**解释**：答案可以与当前位置相同，即点 `[3,4]` 本身也是有效点。

**示例 3**  
```text
Input: x = 3, y = 4, points = [[2,3]]
Output: -1
```
**解释**：不存在满足条件的有效点。

---

### 约束条件

- `1 <= points.length <= 10^4`
- `points[i].length == 2`
- `1 <= x, y, ai, bi <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有点都检查一遍**，找出满足“横坐标相同或纵坐标相同”的点，然后在这些合法点里挑出曼哈顿距离最小的那个。  

- **数据结构**：只需要用一个普通的列表 `points`（题目已经给出）以及几个整数变量来记录当前最小距离和对应的下标。  
  - 可以把“哈希表”想成一本词典，`key` 是单词，`value` 是页码。这里我们不需要查找“键”，只需要顺序遍历，所以直接用列表就够了。  
- **正确性**：因为我们把**所有**点都检查了一遍，凡是满足“同 x 或同 y”的点一定会被考虑；在这些点中我们挑了距离最小的，所以返回的下标必然是题目要求的答案。  
- **时间/空间复杂度**：  
  - 我们遍历一次 `points`，每次只做常数时间的比较和加法，整体是 **O(n)**，其中 `n = len(points)`。  
    - “O(n)” 可以理解为“随着点的数量线性增长”，比如 1000 个点大约要做 1000 次检查。  
  - 只用了几个额外的整数变量，空间是 **O(1)**（常数级），即不随 `n` 增长而增长。  

#### 代码（Python）

```python
from typing import List

class Solution:
    def nearestValidPoint(self, x: int, y: int, points: List[List[int]]) -> int:
        """
        暴力遍历所有点，找出满足同 x 或同 y 且曼哈顿距离最小的点下标。
        """
        min_dist = float('inf')   # 当前找到的最小距离，初始为正无穷大
        ans_idx = -1              # 结果下标，默认 -1 表示不存在合法点

        for idx, (px, py) in enumerate(points):
            # 只考虑横坐标相同或纵坐标相同的点
            if px == x or py == y:
                # 曼哈顿距离 = |x - px| + |y - py|
                dist = abs(x - px) + abs(y - py)
                # 若距离更小，或者距离相同但下标更靠前，则更新答案
                if dist < min_dist:
                    min_dist = dist
                    ans_idx = idx
        return ans_idx
```

#### 复杂度

- **时间复杂度**：`O(n)` — 随着点的数量线性增长，需要检查每一个点一次。  
- **空间复杂度**：`O(1)` — 只用了常数个额外变量（`min_dist`、`ans_idx`），不随输入规模变化。

---

### 2. 最优解

#### 思路  

对于本题，**遍历一次已经是最优的**，因为我们必须检查每个点才能确认它是否满足“同 x 或同 y”。没有办法在不看某个点的情况下判断它是否是合法的、更近的候选者。  
所以最优解仍然是一次线性扫描，只是可以在遍历过程中做一点小优化：

1. **提前结束**：如果在遍历时发现距离为 `0`（即点恰好在 `(x, y)`），这已经是最小可能距离，后面再也不可能出现更小的距离，可以直接返回当前下标。  
2. 代码结构保持简洁，避免不必要的函数调用或额外数据结构。  

这两点并不会改变大 O 记号（仍是 `O(n)`），但在实际运行时会略微提升速度，尤其是当合法点恰好就在起点时。

#### 代码（Python）

```python
from typing import List

class Solution:
    def nearestValidPoint(self, x: int, y: int, points: List[List[int]]) -> int:
        """
        同样是一次线性扫描，但在发现距离为 0 时立即返回，省去后续无意义的检查。
        """
        best_dist = float('inf')
        best_idx = -1

        for i, (px, py) in enumerate(points):
            # 必须满足横坐标相同或纵坐标相同
            if px != x and py != y:
                continue  # 直接跳过不合法的点

            dist = abs(x - px) + abs(y - py)

            # 已经是最小可能距离 0，直接返回当前下标
            if dist == 0:
                return i

            if dist < best_dist:
                best_dist = dist
                best_idx = i

        return best_idx
```

#### 复杂度

- **时间复杂度**：`O(n)` — 仍然需要遍历所有点，最坏情况下仍是线性时间。若提前遇到距离为 0，则可能提前结束，实际运行更快。  
- **空间复杂度**：`O(1)` — 只用了常数个临时变量。

---

## 心得

- **核心技巧**：**一次线性扫描 + 条件过滤**。通过遍历并即时比较，能够在 `O(n)` 时间内找到满足特定约束的最优解。  
- **适用的题型**：  
  1. “在数组/列表中寻找满足某种条件的最小/最大值”  
  2. “找出最近的满足条件的点/元素”（如最近的相同颜色、最近的相同数值等）  
  3. “在一维或二维坐标系中，根据曼哈顿距离或欧氏距离进行筛选”  
- **一句话总结**：**只要把所有候选者遍历一遍并实时维护最优解，就能在一次线性扫描中解决这类“最近/最小”问题。**

---

## 反思

- **第一反应**：看到“相同 x 或相同 y”，立刻想到“遍历检查每个点”。这是一种直觉的**筛选+比较**思路。  
- **最容易踩的坑**：  
  - 忘记同时检查 **横坐标相同** **或** **纵坐标相同**（写成 `and` 会漏掉合法点）。  
  - 忽视 **返回最小下标** 的要求：当出现相同最小距离的多个点时，必须保留第一次出现的下标。  
  - 边界情况：只有一个点且恰好在 `(x, y)`，或根本没有合法点，需要返回 `-1`。  
- **下次遇到同类题**，第一步应该想到：**“能否一次遍历全部元素，并在遍历过程中维护当前最优解？”** 如果可以，那通常就是最优解的方向。