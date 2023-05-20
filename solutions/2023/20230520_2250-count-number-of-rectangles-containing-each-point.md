# #2250. 统计每个点被包含的矩形数量 / Count Number of Rectangles Containing Each Point

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Binary Indexed Tree、Sorting · [LeetCode 链接](https://leetcode.com/problems/count-number-of-rectangles-containing-each-point/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer array rectangles where rectangles[i] = [li, hi] indicates that ith rectangle has a length of li and a height of hi. You are also given a 2D integer array points where points[j] = [xj, yj] is a point with coordinates (xj, yj).
The ith rectangle has its bottom-left corner point at the coordinates (0, 0) and its top-right corner point at (li, hi).
Return an integer array count of length points.length where count[j] is the number of rectangles that contain the jth point.
The ith rectangle contains the jth point if 0 <= xj <= li and 0 <= yj <= hi. Note that points that lie on the edges of a rectangle are also considered to be contained by that rectangle.

**Examples**

**Example 1:**

```
Input: rectangles = [[1,2],[2,3],[2,5]], points = [[2,1],[1,4]]
Output: [2,1]
Explanation: 
The first rectangle contains no points.
The second rectangle contains only the point (2, 1).
The third rectangle contains the points (2, 1) and (1, 4).
The number of rectangles that contain the point (2, 1) is 2.
The number of rectangles that contain the point (1, 4) is 1.
Therefore, we return [2, 1].
```

**Example 2:**

```
Input: rectangles = [[1,1],[2,2],[3,3]], points = [[1,3],[1,1]]
Output: [1,3]
Explanation:
The first rectangle contains only the point (1, 1).
The second rectangle contains only the point (1, 1).
The third rectangle contains the points (1, 3) and (1, 1).
The number of rectangles that contain the point (1, 3) is 1.
The number of rectangles that contain the point (1, 1) is 3.
Therefore, we return [1, 3].
```

**Constraints**

- 1 <= rectangles.length, points.length <= 5 * 104
- rectangles[i].length == points[j].length == 2
- 1 <= li, xj <= 109
- 1 <= hi, yj <= 100
- All the rectangles are unique.
- All the points are unique.

---

## 题目（中文翻译）

**题目描述**  
给定一个二维整数数组 `rectangles`，其中 `rectangles[i] = [l_i, h_i]` 表示第 `i` 个矩形的长度为 `l_i`、高度为 `h_i`。同时给定一个二维整数数组 `points`，其中 `points[j] = [x_j, y_j]` 表示坐标为 `(x_j, y_j)` 的点。  

第 `i` 个矩形的左下角位于坐标 `(0, 0)`，右上角位于 `(l_i, h_i)`。  
返回一个长度为 `points.length` 的整数数组 `count`，其中 `count[j]` 表示包含第 `j` 个点的矩形数量。  

第 `i` 个矩形包含第 `j` 个点的条件是 `0 ≤ x_j ≤ l_i` 且 `0 ≤ y_j ≤ h_i`。位于矩形边界上的点也视为被包含。

**示例 1**  
```text
Input: rectangles = [[1,2],[2,3],[2,5]], points = [[2,1],[1,4]]
Output: [2,1]
Explanation: 
- 第一个矩形不包含任何点。
- 第二个矩形只包含点 (2, 1)。
- 第三个矩形包含点 (2, 1) 和 (1, 4)。
点 (2, 1) 被 2 个矩形包含，点 (1, 4) 被 1 个矩形包含。因此返回 [2, 1]。
```

**示例 2**  
```text
Input: rectangles = [[1,1],[2,2],[3,3]], points = [[1,3],[1,1]]
Output: [1,3]
Explanation:
- 第一个矩形只包含点 (1, 1)。
- 第二个矩形只包含点 (1, 1)。
- 第三个矩形包含点 (1, 3) 和 (1, 1)。
点 (1, 3) 被 1 个矩形包含，点 (1, 1) 被 3 个矩形包含。因此返回 [1,3]。
```

**约束条件**  
- `1 ≤ rectangles.length, points.length ≤ 5 * 10^4`
- `rectangles[i].length == points[j].length == 2`
- `1 ≤ l_i, x_j ≤ 10^9`
- `1 ≤ h_i, y_j ≤ 100`
- 所有矩形均唯一。
- 所有点均唯一。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个点和每个矩形都去比较一次：  

1. 取出第 `i` 个矩形的宽 `li`、高 `hi`（左下角固定在原点 (0,0)）。  
2. 取出第 `j` 个点的坐标 `(xj, yj)`。  
3. 检查 `0 ≤ xj ≤ li` 且 `0 ≤ yj ≤ hi` 是否同时成立。  
   - 这里的 “≤” 包含了点在矩形边界上的情况。  

如果成立，就把计数器 `count[j]` 加一。对所有矩形和所有点都如此遍历，最后得到每个点被多少矩形包含。

> **类比**：把矩形想成装有糖果的盒子，点是小朋友的手指。我们要检查每只手指能否伸进每个盒子里——最笨的办法就是每只手指都去每个盒子里试一次。

**正确性**：只要遍历了所有矩形‑点对并使用题目给出的包含条件，就一定不会漏掉任何合法的组合，也不会错误计数。

**复杂度分析**（大白话）：  
- 外层循环遍历 `points`（点的数量记为 `P`），里层遍历 `rectangles`（矩形的数量记为 `R`），两层相乘得到 **`P × R` 次比较**。  
- 每一次比较只做几次整数比较，时间几乎是常数。  
- 所以 **时间复杂度是 O(P·R)**。如果 `P` 和 `R` 都是 5 × 10⁴，最坏会有 2.5 × 10⁹ 次比较，跑不完。  
- 我们只用了几个整数数组和计数器，**空间复杂度是 O(P)**（存放答案的数组）。

#### 代码（Python）

```python
from typing import List

def countRectangles_bruteforce(rectangles: List[List[int]],
                               points: List[List[int]]) -> List[int]:
    """
    暴力解：对每个点遍历所有矩形，判断是否包含。
    """
    m = len(points)
    ans = [0] * m                     # 用来存每个点的答案

    for idx, (x, y) in enumerate(points):   # 枚举每个点
        cnt = 0
        for l, h in rectangles:            # 枚举每个矩形
            # 判断点是否在矩形内部（包括边界）
            if x <= l and y <= h:
                cnt += 1
        ans[idx] = cnt

    return ans
```

#### 复杂度

- **时间复杂度**：O(P·R)  
  > “P·R” 就是点的个数乘以矩形的个数，想象成“把每只手指都塞进每个盒子里”。  
- **空间复杂度**：O(P)  
  > 只用了一个和点数等长的答案数组，其他都是常数级的临时变量。

---

### 2. 最优解  

#### 思路  

暴力解太慢的根源在于 **每个点都要遍历所有矩形**。  
观察题目限制可以发现：

1. **y 坐标和矩形的高度 `hi` 都不超过 100**（常数上界）。  
2. 对于一个点 `(x, y)`，只有 **高度 ≥ y** 的矩形才可能包含它。  
3. 只要高度满足，**再检查宽度是否 ≥ x** 即可。

基于第 1 条，我们可以把矩形按 **高度** 分桶（高度 1~100 各自一个列表），每个桶里只存对应高度的宽度 `li`。  
对每个高度的宽度列表进行 **升序排序**，这样就可以用二分查找快速统计 “宽度 ≥ x 的矩形有多少”。  

处理单个点的步骤：

```
ans = 0
for h from y to 100:          # 只看足够高的高度
    list = bucket[h]          # 该高度所有矩形的宽度（已排序）
    if list 不为空:
        pos = bisect_left(list, x)   # 第一个 ≥ x 的位置
        ans += len(list) - pos       # 之后的全部满足宽度条件
```

因为高度最多只有 100，**每个点最多只做 100 次二分查找**，每次二分的代价是 `log(k)`（k 为该高度矩形数），远远小于遍历全部矩形。

> **类比**：把所有盒子按照高度分层摆放，每层的盒子已经按宽度排好序。小朋友只需要挑出自己手指所在的层以上，然后在每层里快速找出能放下手指的盒子——不需要一个个去试。

**关键数据结构**  

- **数组 bucket[101]**（下标 1~100），每个元素是一个 Python 列表，存放对应高度的宽度。  
- **二分查找**（`bisect_left`），相当于在排好序的书架上快速定位第一本满足条件的书。

**复杂度推导**  

- **预处理**：把 `R` 个矩形放进对应的桶里并排序。  
  - 放入是 O(R)。  
  - 对所有桶整体排序等价于对 `R` 个数整体排序，时间 `O(R log R)`（因为每个桶内部排序的总工作量不超过一次完整排序）。  
- **查询**：对每个点，最多遍历 100 个高度，每个高度一次二分 `O(log R_h)`。  
  - 最坏情况是 `100 * log R`，记作 `O(100·log R)`。  
  - `P` 个点合计 `O(P·100·log R)`，即 `O(P·log R)`（常数 100 可忽略）。  
- **空间**：保存所有宽度，总共 `R` 个整数，外加 101 个空列表的指针，故 `O(R)`。

综上，这种做法在 `R, P ≤ 5·10⁴` 的限制下完全可以在一秒左右跑完。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List

def countRectangles(rectangles: List[List[int]],
                    points: List[List[int]]) -> List[int]:
    """
    最优解：利用高度 ≤ 100 的特性分桶 + 二分统计宽度 ≥ x 的矩形个数。
    """
    MAX_H = 100                     # 题目给的高度上限
    # 1. 按高度分桶，bucket[h] 存放所有高度为 h 的矩形的宽度 l
    bucket: List[List[int]] = [[] for _ in range(MAX_H + 1)]
    for l, h in rectangles:
        bucket[h].append(l)

    # 2. 对每个高度的宽度列表进行升序排序，便于二分
    for h in range(1, MAX_H + 1):
        bucket[h].sort()

    # 3. 逐点查询
    ans: List[int] = []
    for x, y in points:
        cnt = 0
        # 只需要看高度 >= y 的桶
        for h in range(y, MAX_H + 1):
            arr = bucket[h]
            if not arr:                     # 该高度没有矩形，直接跳过
                continue
            # 二分找第一个宽度 >= x 的位置
            pos = bisect_left(arr, x)
            cnt += len(arr) - pos           # 位置之后的全部满足宽度条件
        ans.append(cnt)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(R log R + P·100·log R)` → 实际上可以写成 `O(R log R + P·log R)`，因为 100 是常数。  
  > 与暴力解的 `O(P·R)` 相比，**把 5·10⁴ × 5·10⁴ 的遍历降到了只需几百万次二分**，快了好几个数量级。  
- **空间复杂度**：`O(R + MAX_H)` → 主要是保存所有矩形宽度的 `bucket`，额外只用了 101 个小列表的指针。  

---

## 心得  

- **核心技巧**：利用「参数范围小」进行**分桶 + 二分**，把原本的二维约束转化为「高度固定，宽度二分」的单维查询。  
- **适用场景**：  
  1. 某一维度的取值范围极小（如 ≤ 100、≤ 1000），可以**离散化分桶**。  
  2. 需要对「≥ / ≤」这种区间计数进行大量查询，**排序 + 二分** 能把线性扫描变对数。  
  3. 类似题目：  
     - *Number of Flowers in Full Bloom*（按照时间段分桶）  
     - *Maximum Number of Points With Same X-Coordinate*（把 y 轴分桶）  
- **一句话总结解题钥匙**：**「把大问题拆成高度 ≤ 100 的小问题，每个小问题用二分快速统计宽度」**。

---

## 反思  

- **第一反应**：直接想到遍历所有矩形，忽略了约束里 “`hi, yj ≤ 100`” 这条黄金信息。  
- **最容易踩的坑**：  
  - 忘记把 **高度等于点的 y 坐标** 也算在内（条件是 `hi ≥ y`），导致答案偏小。  
  - 二分时使用 `bisect_left` 而不是 `bisect_right`，因为我们要找 **第一个 ≥ x** 的位置。  
  - 需要注意 **宽度和高度的取值范围不同**：宽度可达 1e9，不能直接做 BIT 或数组下标，需要用二分而不是直接索引。  
- **下次类似题目**：第一步先检查是否有 **“某个维度的取值上限很小”**，若有就考虑 **分桶**；随后在每个桶内部利用 **排序 + 二分** 或 **前缀和** 完成快速计数。