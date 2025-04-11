# #3143. 正方形内的最大点数 / Maximum Points Inside the Square

> 难度：中等 · 标签：Array、Hash Table、String、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximum-points-inside-the-square/)

---

## 题目（英文原版）

**Description**

You are given a 2D array points and a string s where, points[i] represents the coordinates of point i, and s[i] represents the tag of point i.
A valid square is a square centered at the origin (0, 0), has edges parallel to the axes, and does not contain two points with the same tag.
Return the maximum number of points contained in a valid square.
Note:

**Examples**

**Example 1:**

```
Input: points = [[2,2],[-1,-2],[-4,4],[-3,1],[3,-3]], s = "abdca"
Output: 2
Explanation:
The square of side length 4 covers two points points[0] and points[1] .
```

**Example 2:**

```
Input: points = [[1,1],[-2,-2],[-2,2]], s = "abb"
Output: 1
Explanation:
The square of side length 2 covers one point, which is points[0] .
```

**Example 3:**

```
Input: points = [[1,1],[-1,-1],[2,-2]], s = "ccd"
Output: 0
Explanation:
It's impossible to make any valid squares centered at the origin such that it covers only one point among points[0] and points[1] .
```

**Constraints**

- 1 <= s.length, points.length <= 105
- points[i].length == 2
- -109 <= points[i][0], points[i][1] <= 109
- s.length == points.length
- points consists of distinct coordinates.
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个二维数组 `points` 和一个字符串 `s`，其中 `points[i]` 表示第 `i` 个点的坐标，`s[i]` 表示第 `i` 个点的标签（tag）。  
一个**合法正方形**（valid square）满足以下条件：

- 正方形的中心在原点 `(0, 0)`；
- 正方形的四条边平行于坐标轴；
- 正方形内部（包括边界）不包含标签相同的两个点。

返回能够放入合法正方形中的点的最大数量。

---

## 示例

### 示例 1  
**输入**  
```json
points = [[2,2],[-1,-2],[-4,4],[-3,1],[3,-3]], s = "abdca"
```  
**输出**  
```
2
```  
**解释**  
边长为 `4` 的正方形能够覆盖 `points[0]` 和 `points[1]` 两个点。

### 示例 2  
**输入**  
```json
points = [[1,1],[-2,-2],[-2,2]], s = "abb"
```  
**输出**  
```
1
```  
**解释**  
边长为 `2` 的正方形只能覆盖 `points[0]` 一个点。

### 示例 3  
**输入**  
```json
points = [[1,1],[-1,-1],[2,-2]], s = "ccd"
```  
**输出**  
```
0
```  
**解释**  
无法构造出以原点为中心且只包含 `points[0]` 与 `points[1]` 中任意一个点的合法正方形。

---

## 约束条件

- `1 <= s.length, points.length <= 10^5`
- `points[i].length == 2`
- `-10^9 <= points[i][0], points[i][1] <= 10^9`
- `s.length == points.length`
- 所有坐标互不相同
- `s` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个点都当成“必须要被正方形覆盖的点”，然后把正方形的边长定为刚好能把它包含进去的最小值**。  

- 对于点 `(x, y)`，正方形的中心在原点 `(0,0)`，边与坐标轴平行。  
- 为了让这个点落在正方形内部（包括边），正方形的半边长（即从中心到任意一条边的距离）必须不小于 `max(|x|, |y|)`。  
- 所以对应的**最小边长**是 `2 * max(|x|, |y|)`。  

暴力做法：

1. 把每个点的 `max(|x|,|y|)` 记下来，得到 `n` 种可能的半边长 `L`（`L = max(|x|,|y|)`）。  
2. 对每个 `L`，遍历全部 `n` 个点，统计 **满足 `max(|x|,|y|) ≤ L` 的点**。  
3. 再检查这些点的标签 `s[i]` 是否都有不同（相当于把标签放进一个哈希表，出现重复就不合法）。  
4. 合法的话更新答案为当前点的个数。  

> **类比**：把哈希表想象成一本字典，`key` 是标签，`value` 是页码。往字典里查一个标签，如果已经在里面，就说明这本字典里出现了重复的词，正方形就不合法了。

**为什么正确**：我们枚举了所有可能的正方形大小（每个点对应的最小正方形），并且对每种大小检查了所有被覆盖的点以及标签冲突，必然会覆盖所有合法的正方形。

**复杂度**：  
- 对每个 `L` 都要遍历全部 `n` 个点 → `n` 次 * `n` 次 = `O(n²)`。  
- 哈希表里最多放 `n` 个标签，空间 `O(n)`。

> **大白话解释**：`O(n²)` 就是“如果你有 10,000 个点，程序大概要跑 10,000 × 10,000 = 1 亿次”。在实际面试里，这会超时。

#### 代码（Python）

```python
from typing import List

def maxPointsInsideSquare_bruteforce(points: List[List[int]], s: str) -> int:
    n = len(points)
    # 预先算出每个点对应的半边长 L = max(|x|, |y|)
    half_lengths = [max(abs(x), abs(y)) for x, y in points]

    ans = 0
    # 枚举所有可能的 L（这里直接用每个点的 L）
    for L in half_lengths:
        seen = set()          # 用来检测标签是否重复
        cnt = 0               # 当前正方形覆盖的点数
        ok = True
        for i in range(n):
            # 判断点 i 是否在正方形内部（包括边界）
            if half_lengths[i] <= L:
                if s[i] in seen:      # 标签重复，非法
                    ok = False
                    break
                seen.add(s[i])
                cnt += 1
        if ok:
            ans = max(ans, cnt)        # 取最大的合法点数
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：外层循环 `n` 次，内层遍历所有 `n` 个点，最坏情况要做 `n × n` 次比较。
- **空间复杂度**：`O(n)`  
  - 解释：哈希表 `seen` 最多会存 `n` 个不同的标签。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**正方形的大小只和 `max(|x|,|y|)` 有关**。如果把所有点按这个值从小到大排好序，会得到一个**单调递增的序列**：

```
r_i = max(|x_i|, |y_i|)   (i 从 0 开始)
```

当我们把正方形的半边长设为 `L` 时，正方形会恰好覆盖 **所有 `r_i ≤ L` 的点**。换句话说，**随着 `L` 逐渐增大，覆盖的点集合只会不断往后“追加”，不会删掉已经在里面的点**。

因此，**只要在排序后从左到右依次加入点，检查标签是否已经出现过**：

- 如果当前点的标签 **没有出现过**，我们可以把它加入正方形，继续向右走。  
- 如果出现 **重复标签**，说明此时的正方形已经不合法了，因为正方形必须把 **所有** `r_i ≤ L` 的点都包含进去，无法把其中一个点挑出来不放。于是 **以当前点之前的点数** 为合法的最大答案，后面的点再也不能让正方形合法（因为半边长只能更大，导致重复标签仍然在里面）。

于是答案就是 **排序后最长的前缀，使得标签全部唯一**。

> **类比**：想象把所有点排成一条队伍，队伍前面的点都已经进了正方形。只要下一个人没有和前面的人同名，就可以让他进来；一旦出现同名的新人，正方形的门就要关闭，已经进来的人数就是最大值。

**核心数据结构**：**哈希集合（set）** 用来快速判断标签是否已经出现，时间 `O(1)`。

**步骤**：

1. 计算每个点的半边长 `r = max(|x|, |y|)`，并把 `(r, tag)` 组成的元组放进列表。  
2. 按 `r` 升序排序（`O(n log n)`）。  
3. 从左到右遍历排好序的列表，维护一个 `seen` 集合记录已经出现的标签。  
   - 若 `tag` 不在 `seen`，加入集合并继续。  
   - 若 `tag` 已在 `seen`，返回当前已经加入的点数（即索引 `i`），因为此时正方形已经不合法。  
4. 如果遍历完都没有冲突，答案就是 `n`（所有点标签互不相同）。

#### 代码（Python）

```python
from typing import List

def maxPointsInsideSquare(points: List[List[int]], s: str) -> int:
    """
    返回以原点为中心、边平行于坐标轴的合法正方形能够容纳的最多点数。
    思路：按 max(|x|,|y|) 排序，找最长的标签唯一前缀。
    """
    n = len(points)

    # 1. 计算每个点对应的半边长 r = max(|x|, |y|)
    #    同时把标签保存下来，组成 (r, tag) 的元组
    items = [(max(abs(x), abs(y)), s[i]) for i, (x, y) in enumerate(points)]

    # 2. 按 r 升序排序
    items.sort(key=lambda x: x[0])   # O(n log n)

    seen = set()      # 已经出现过的标签
    for idx, (_, tag) in enumerate(items):
        if tag in seen:          # 出现重复标签，正方形不合法
            return idx          # 前缀长度即为最大合法点数
        seen.add(tag)            # 记录新标签

    # 3. 全部遍历完都没有冲突，说明所有点都可以放进正方形
    return n
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 解释：排序是最耗时的步骤，需要 `n log n` 次比较；随后一次线性扫描 `O(n)`，不影响总体复杂度。相较于暴力的 `O(n²)`，这里的 “log” 相当于把时间降低了好几个数量级（比如 `10⁵` 的数据，`n log n` 只有几百万次操作，完全能跑完）。
- **空间复杂度**：`O(n)`  
  - 解释：存放排序后的 `(r, tag)` 列表需要 `n` 个元素，另外一个 `set` 最多保存 `n` 个不同的标签。

---

## 心得

- **核心技巧**：把几何约束（正方形必须包含所有半径 ≤ L 的点）转化为**单调序列的前缀唯一性**问题。  
- **适用场景**：  
  1. **按阈值逐步加入元素**，并要求某种“全局唯一性”或“无冲突”条件（如 **“最大不冲突子集”**）。  
  2. **二维几何中以原点为中心的 L∞ 球（正方形）**，需要按 `max(|x|,|y|)` 排序处理。  
  3. 类似的 **“以原点为中心的圆”**（使用 `sqrt(x²+y²)`）或 **“以某点为中心的矩形”**（使用 `max(dx, dy)`）的问题。  
- **一句话总结**：**把几何范围转化为单调的“半径”排序，答案就是标签唯一的最长前缀。**

---

## 反思

- **第一反应**：直接枚举每个点对应的正方形大小，暴力检查所有点——这会导致 `O(n²)`，不适合 `10⁵` 规模。  
- **最容易踩的坑**：  
  - 忽视正方形必须 **包含所有** `r ≤ L` 的点，误以为可以“挑选”点导致错误的子集判断。  
  - 没有考虑 **标签冲突的不可回溯性**：一旦出现重复，后续更大的正方形仍然会包含冲突点，答案只能是冲突前的前缀长度。  
  - 边界条件：所有标签互不相同时，答案应为 `n`；所有点都有相同标签时，答案只能是 `1`（第一个点的前缀）。  
- **下次类似题的第一步**：先思考“随着阈值（半径、边长、时间等）单调增大，集合会怎样变化”，并判断是否能用**排序 + 前缀/滑动窗口**来快速求解。这样往往能把暴力的 `O(n²)` 降到 `O(n log n)` 或 `O(n)`。