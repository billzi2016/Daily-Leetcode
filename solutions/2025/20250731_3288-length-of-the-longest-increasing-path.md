# #3288. 最长递增路径的长度 / Length of the Longest Increasing Path

> 难度：困难 · 标签：Array、Binary Search、Sorting · [LeetCode 链接](https://leetcode.com/problems/length-of-the-longest-increasing-path/)

---

## 题目（英文原版）

**Description**

You are given a 2D array of integers coordinates of length n and an integer k, where 0 <= k < n.
coordinates[i] = [xi, yi] indicates the point (xi, yi) in a 2D plane.
An increasing path of length m is defined as a list of points (x1, y1), (x2, y2), (x3, y3), ..., (xm, ym) such that:
Return the maximum length of an increasing path that contains coordinates[k].

**Examples**

**Example 1:**

```
Input: coordinates = [[3,1],[2,2],[4,1],[0,0],[5,3]], k = 1
Output: 3
Explanation:
(0, 0) , (2, 2) , (5, 3) is the longest increasing path that contains (2, 2) .
```

**Example 2:**

```
Input: coordinates = [[2,1],[7,0],[5,6]], k = 2
Output: 2
Explanation:
(2, 1) , (5, 6) is the longest increasing path that contains (5, 6) .
```

**Constraints**

- 1 <= n == coordinates.length <= 105
- coordinates[i].length == 2
- 0 <= coordinates[i][0], coordinates[i][1] <= 109
- All elements in coordinates are distinct.
- 0 <= k <= n - 1

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数二维数组 `coordinates`（坐标）和一个整数 `k`，满足 `0 <= k < n`。  
`coordinates[i] = [xi, yi]` 表示平面上的点 `(xi, yi)`。

**递增路径（increasing path）** 长度为 `m` 定义为一系列点  
`(x1, y1), (x2, y2), (x3, y3), ..., (xm, ym)`，满足（此处省略具体递增条件的描述）。

返回包含 `coordinates[k]` 的递增路径的最大可能长度。

---

## 示例

### 示例 1
**输入**  
```
coordinates = [[3,1],[2,2],[4,1],[0,0],[5,3]], k = 1
```
**输出**  
```
3
```
**解释**  
`(0, 0) , (2, 2) , (5, 3)` 是包含点 `(2, 2)` 的最长递增路径。

### 示例 2
**输入**  
```
coordinates = [[2,1],[7,0],[5,6]], k = 2
```
**输出**  
```
2
```
**解释**  
`(2, 1) , (5, 6)` 是包含点 `(5, 6)` 的最长递增路径。

---

## 约束条件
- `1 <= n == coordinates.length <= 10^5`
- `coordinates[i].length == 2`
- `0 <= coordinates[i][0], coordinates[i][1] <= 10^9`
- `coordinates` 中的所有元素均唯一。
- `0 <= k <= n - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求 **在所有坐标点中找到一条严格递增的路径**（即后一个点的 `x` 与 `y` 均比前一个点大），且这条路径必须经过下标为 `k` 的点 `P = coordinates[k]`。  
最直接的想法是：

1. **枚举所有点的排列**（或者所有子集的排列），检查它是否满足“坐标递增”。  
2. 若满足，就看这条序列里是否包含点 `P`，记录长度的最大值。

> **类比**：把所有点想成一副扑克牌，每张牌上写着两个数字 `(x, y)`。我们想把牌按“左手牌的两个数字都更小” 的规则排成一条最长的顺子，并且这副顺子里一定要有第 `k` 张牌。

因为点的个数 `n` 可以达到 `10⁵`，所有排列的数量是 `n!`，根本不可能在电脑里穷举。  
即使只枚举 **子集**（不考虑顺序），也要检查 `2ⁿ` 种可能，仍然不可行。

> **正确性**：只要遍历了所有可能的序列，肯定会找到最长的那条。  
> **为什么慢**：遍历的组合数随 `n` 指数级增长，几乎不可能在 1 秒内跑完。

#### 代码（Python）

```python
import itertools

def longest_path_bruteforce(coordinates, k):
    target = tuple(coordinates[k])               # 把目标点变成不可变的元组，方便比较
    best = 0

    # 生成所有可能的排列（这里仅作演示，n 超过 8 就会超时）
    for perm in itertools.permutations(coordinates):
        # 只保留包含目标点的排列
        if target not in perm:
            continue

        ok = True
        # 检查是否严格递增
        for (x1, y1), (x2, y2) in zip(perm, perm[1:]):
            if not (x1 < x2 and y1 < y2):
                ok = False
                break
        if ok:
            best = max(best, len(perm))

    return best
```

> **提示**：上面的实现只适合 `n ≤ 8` 左右的玩具数据，真正的测试数据会让它直接超时。

#### 复杂度  

- **时间复杂度**：`O(n! * n)`（遍历所有排列，每条排列检查 `n` 次），在实际中等价于 **指数级**，即使把 `n!` 记作 `O(cⁿ)`，也远远大于线性或多项式。
- **空间复杂度**：`O(n)`（递归栈或排列生成器需要保存当前排列），相对来说不算大，但时间已经不可接受。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**真正的难点在于快速找到满足坐标递增的最长序列**。  
观察题目提示，我们可以把问题拆成两部分：

1. **左侧点**：所有同时满足 `x < x_k` 且 `y < y_k` 的点，这些点只能出现在 `P` 之前。  
2. **右侧点**：所有同时满足 `x > x_k` 且 `y > y_k` 的点，这些点只能出现在 `P` 之后。

对每一侧，只要把点按照 `x` 的顺序排好，再在 `y` 上做 **最长递增子序列（LIS）**，就能得到“从左到 `P`”或“从 `P` 到右”的最长长度。

> **为什么可以只看 `y`**  
> 当 `x` 已经严格递增（我们已经排好顺序），只要保证 `y` 也严格递增，整个点对 `(x, y)` 就一定递增。  
> 但是如果有相同的 `x`，我们不能让 `y` 递增，因为 `x` 必须严格增大。于是 **在 `x` 相同的情况下把 `y` 按** **降序** 排序**，这样在做 LIS 时不会误把同 `x` 的点接在一起**。

对左侧点：

- 只保留 `x < x_k` 且 `y < y_k` 的点（包括 `P` 本身）。
- 按 `x` 升序、`y` 降序排序。
- 对排序后的序列，求 **每个点的 LIS 长度（以该点结尾）**。这一步可以用 **树状数组（Fenwick）** 或 **线段树**在 `y` 维度上做 “前缀最大值” 查询，时间 `O(log N)`。

对右侧点：

- 同理，只保留 `x > x_k` 且 `y > y_k` 的点（包括 `P`）。
- 为了让 “从 `P` 往右” 仍然是 “递增 → LIS”，我们把坐标 **翻转**：把 `x`、`y` 都取负数或直接把序列倒序。这里我们把 `x` 按 **降序**、`y` 按 **升序** 排序，然后再在 `y` 上做 LIS（仍然是递增）。  
- 同样用 Fenwick 求每个点的 LIS 长度（**以该点为起点**），这相当于在倒序后求 “以该点结尾”的 LIS。

最后：

- `left_len[i]` = 最长递增序列 **以** `coordinates[i]` **结尾** 的长度（只看左侧点）。
- `right_len[i]` = 最长递增序列 **以** `coordinates[i]` **开头** 的长度（只看右侧点）。
- 对目标点 `k`，答案 = `left_len[k] + right_len[k] - 1`（`k` 本身被算了两次，需要减 1）。

> **核心数据结构：树状数组（Fenwick）**  
> - 类比：像一本“查字典”，我们要快速得到“所有小于等于某个 y 的最大 LIS 长度”。Fenwick 能在 `O(log N)` 时间内完成“前缀最大”查询和“单点更新”。

#### 代码（Python）

```python
from typing import List
import bisect

class Fenwick:
    """支持前缀最大值的树状数组（1-indexed）"""
    def __init__(self, size: int):
        self.n = size
        self.tree = [0] * (size + 1)

    def update(self, idx: int, value: int):
        """把位置 idx 的值提升为 max(old, value)"""
        while idx <= self.n:
            if value > self.tree[idx]:
                self.tree[idx] = value
            idx += idx & -idx

    def query(self, idx: int) -> int:
        """返回区间 [1, idx] 的最大值"""
        res = 0
        while idx > 0:
            if self.tree[idx] > res:
                res = self.tree[idx]
            idx -= idx & -idx
        return res


def longestIncreasingPath(coordinates: List[List[int]], k: int) -> int:
    n = len(coordinates)
    target = coordinates[k]
    tx, ty = target

    # ---------- 1. 处理左侧（小于 target） ----------
    left_points = []
    for i, (x, y) in enumerate(coordinates):
        if x < tx and y < ty:          # 同时更小的点
            left_points.append((x, y, i))
    # 把 target 本身也放进去，方便后面得到 left_len[k]
    left_points.append((tx, ty, k))

    # 按 x 升序、x 相同则 y 降序 排序
    left_points.sort(key=lambda p: (p[0], -p[1]))

    # 对 y 做离散化（坐标压缩），因为 y 可能高达 1e9
    all_y = sorted({y for _, y, _ in left_points})
    y_to_idx = {y: i + 1 for i, y in enumerate(all_y)}   # Fenwick 1-indexed

    fenwick = Fenwick(len(all_y))
    left_len = [0] * n        # 只会在左侧点上被填充

    for x, y, idx in left_points:
        pos = y_to_idx[y]
        best = fenwick.query(pos - 1) + 1   # 前缀最大 + 自己
        left_len[idx] = best
        fenwick.update(pos, best)           # 把以当前点结尾的 LIS 长度写进去

    # ---------- 2. 处理右侧（大于 target） ----------
    right_points = []
    for i, (x, y) in enumerate(coordinates):
        if x > tx and y > ty:          # 同时更大的点
            right_points.append((x, y, i))
    # 同样把 target 加进来
    right_points.append((tx, ty, k))

    # 为了让 “从 target 往右” 仍然是递增序列，
    # 把 x 按降序、x 相同则 y 升序 排序（相当于把坐标翻转）
    right_points.sort(key=lambda p: (-p[0], p[1]))

    # 再次离散化 y（可以复用上面的映射，也可以重新建）
    all_y_r = sorted({y for _, y, _ in right_points})
    y_to_idx_r = {y: i + 1 for i, y in enumerate(all_y_r)}

    fenwick = Fenwick(len(all_y_r))
    right_len = [0] * n

    for x, y, idx in right_points:
        pos = y_to_idx_r[y]
        best = fenwick.query(pos - 1) + 1
        right_len[idx] = best
        fenwick.update(pos, best)

    # ---------- 3. 合并 ----------
    # left_len[k] 为以 k 结尾的最长左侧长度（包括 k 本身）
    # right_len[k] 为以 k 开头的最长右侧长度（包括 k 本身）
    return left_len[k] + right_len[k] - 1


# -------------------------------------------------
# 下面是一个简单的自测
if __name__ == "__main__":
    print(longestIncreasingPath([[3,1],[2,2],[4,1],[0,0],[5,3]], 1))   # 3
    print(longestIncreasingPath([[2,1],[7,0],[5,6]], 2))               # 2
```

**代码要点解释**

| 行号 | 关键代码 | 中文注释 |
|------|----------|----------|
| 9‑13 | `class Fenwick` | 实现支持“前缀最大”的树状数组，类似查字典时找“最靠前的最大页码”。 |
| 27‑31| `if x < tx and y < ty` | 只保留左侧严格小于目标点的坐标。 |
| 34   | `left_points.sort(key=lambda p: (p[0], -p[1]))` | 先按 `x` 升序，`x` 相同的情况下把 `y` 降序，防止同 `x` 的点被误接。 |
| 38‑40| `y_to_idx = {y: i + 1 for i, y in enumerate(all_y)}` | 把可能巨大的 `y` 值压缩成 `[1 … m]`，方便 Fenwick 使用。 |
| 44‑48| `best = fenwick.query(pos - 1) + 1` | 查询所有 **更小的 y** 对应的最长长度，再加上当前点本身。 |
| 58‑66| 右侧处理（`x > tx` 且 `y > ty`）| 把 `x` 降序、`y` 升序排序，相当于把坐标翻转，使“递增”仍然对应 “LIS”。 |
| 78   | `return left_len[k] + right_len[k] - 1` | 两侧长度相加，减去重复计数的目标点。 |

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 每侧点的排序 `O(m log m)`（`m ≤ n`），  
  - 坐标压缩 `O(m log m)`（排序），  
  - Fenwick 查询/更新每次 `O(log m)`，共 `m` 次。两侧相加仍是 `O(n log n)`。  
  与暴力解的指数级相比，`log n` 只是一点点开销，几乎可以在 1 秒内处理 `10⁵` 条数据。

- **空间复杂度**：`O(n)`  
  - 存储点的列表、离散化映射、Fenwick 树各占 `O(n)`。  
  - 相比暴力的递归栈，这里只需要线性额外空间。

---

## 心得

- **核心技巧**：把二维严格递增的约束转化为“一维 LIS”，配合坐标排序和 **Fenwick 树（前缀最大）** 完成 `O(n log n)` 求解。  
- **适用题型**：  
  1. “最长递增子序列”在二维或多维坐标下的变形（如 “Maximum Length of Pair Chain”）。  
  2. “点集合的最大链”或 “最大矩形嵌套” 类问题。  
  3. 需要在平面上“左下 → 右上”路径的 DP/贪心题目。  
- **一句话总结**：**先把点按 x 排序，再在 y 上做 LIS，利用树状数组把查询/更新压到 `log n`**。

---

## 反思

- **第一反应**：直接想枚举所有排列/子集，忽略了 `n` 这么大的限制。  
- **最容易踩的坑**  
  - **相同 x 的点**：如果不把 `y` 降序排，LIS 可能会把同 `x` 的点接在一起，违反“x 必须严格增大”。  
  - **坐标压缩**：`y` 的范围可达 `10⁹`，直接把它当作 Fenwick 索引会导致数组太大，需要离散化。  
  - **左侧/右侧的边界**：一定要严格 `<` / `>`，否则会把不合法的点算进路径。  
- **下次思路**：遇到 “二维递增链” 这类题目，第一步就 **把一个维度排序、把另一个维度转成 LIS**，再选合适的数据结构（Fenwick / Segment Tree）提升到 `O(n log n)`。这样可以迅速从暴力思路跳到可接受的复杂度。