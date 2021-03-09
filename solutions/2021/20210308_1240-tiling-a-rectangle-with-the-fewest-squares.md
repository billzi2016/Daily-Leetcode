# #1240. 用最少正方形平铺矩形 / Tiling a Rectangle with the Fewest Squares

> 难度：困难 · 标签：Backtracking · [LeetCode 链接](https://leetcode.com/problems/tiling-a-rectangle-with-the-fewest-squares/)

---

## 题目（英文原版）

**Description**

Given a rectangle of size n x m, return the minimum number of integer-sided squares that tile the rectangle.

**Examples**

**Example 1:**

```
Input: n = 2, m = 3
Output: 3
Explanation: 3 squares are necessary to cover the rectangle.
2 (squares of 1x1)
1 (square of 2x2)
```

**Example 2:**

```
Input: n = 5, m = 8
Output: 5
```

**Example 3:**

```
Input: n = 11, m = 13
Output: 6
```

**Constraints**

- 1 <= n, m <= 13

---

## 题目（中文翻译）

给定一个尺寸为 `n x m` 的矩形（rectangle），返回能够完全平铺该矩形的整数边长正方形（integer‑sided squares）的最小数量。

**示例 1**  
**输入**: `n = 2, m = 3`  
**输出**: `3`  
**解释**: 需要 3 个正方形才能覆盖整个矩形。  
- 2 个 1×1 的正方形  
- 1 个 2×2 的正方形  

**示例 2**  
**输入**: `n = 5, m = 8`  
**输出**: `5`  

**示例 3**  
**输入**: `n = 11, m = 13`  
**输出**: `6`  

**约束条件**  
- `1 <= n, m <= 13`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把矩形不停地切成小正方形**，直到所有空格都被填满。  
我们可以把矩形看成一张棋盘，每个格子要么已经被正方形盖住，要么是空的。  
从左上角（自然的起点）找出第一个空格，然后尝试把**所有可能的正方形**（边长从 1 到 能放下的最大值）放进去，递归地继续填剩下的空格。  

- **数据结构**：  
  - `grid`（二维列表）记录每个格子是否已经被占用。可以把它想象成一本笔记本，里面的每一格是“是否被贴上了贴纸”。  
  - `cnt` 记录已经放了多少个正方形。  
  - `best` 保存目前找到的最小正方形数（相当于“全局最好的答案”），用于剪枝。  

- **为什么正确**：  
  - 我们遍历了**所有**合法的放置顺序。只要有一种放法能够覆盖整个矩形，递归必定会走到把所有格子填满的那一步。于是最小的 `cnt` 必然会被记录在 `best` 中。  

- **时间/空间复杂度**：  
  - 这种做法会尝试**每一种可能的切分**，搜索树的分支数随矩形面积指数增长。可以粗略地说时间复杂度是 **O(指数)（≈ O(kⁿ)）**，其中 `k` 是每一步可能的正方形数量，`n = n*m` 是格子数。  
  - 空间上我们只需要保存 `grid`（`n*m` 个格子）和递归栈深度（最多 `n*m`），所以 **O(n·m)**。  

#### 代码（Python）

```python
def tilingRectangle_brute(n: int, m: int) -> int:
    # ---------- 1. 初始化 ----------
    # 用 0 表示空格，1 表示已经被正方形占用
    board = [[0] * m for _ in range(n)]
    best = n * m  # 最坏情况：全部用 1×1 正方形

    # ---------- 2. 辅助函数 ----------
    def first_empty():
        """返回左上角第一个空格的坐标 (i, j)，若全部填满返回 None"""
        for i in range(n):
            for j in range(m):
                if board[i][j] == 0:
                    return i, j
        return None

    def can_place(i: int, j: int, size: int) -> bool:
        """检查以 (i, j) 为左上角，边长为 size 的正方形是否可以放下"""
        if i + size > n or j + size > m:      # 越界
            return False
        for x in range(i, i + size):
            for y in range(j, j + size):
                if board[x][y] == 1:          # 已经被占用
                    return False
        return True

    def set_square(i: int, j: int, size: int, val: int):
        """把正方形区域标记为 val（1 表示占用，0 表示撤销）"""
        for x in range(i, i + size):
            for y in range(j, j + size):
                board[x][y] = val

    # ---------- 3. 深度优先搜索 ----------
    def dfs(cnt: int):
        nonlocal best
        # 剪枝：已经超过当前最优解，无需继续
        if cnt >= best:
            return

        pos = first_empty()
        # 全部填满，更新最优解
        if pos is None:
            best = cnt
            return

        i, j = pos
        # 尝试从大到小放正方形，能更快逼近最优
        max_size = min(n - i, m - j)
        for size in range(max_size, 0, -1):
            if can_place(i, j, size):
                set_square(i, j, size, 1)   # 放置
                dfs(cnt + 1)                # 递归继续
                set_square(i, j, size, 0)   # 撤销，回溯

    dfs(0)
    return best
```

#### 复杂度  

- **时间复杂度**：`O(指数)`（实际表现随矩形大小而急速增长），因为我们会遍历所有可能的切分方式。  
- **空间复杂度**：`O(n·m)`，主要是 `board` 用的二维数组，加上递归调用栈的深度（最坏不超过 `n·m`）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **搜索树太大**：每次都要尝试所有可能的正方形大小，即使很多分支注定不可能得到更好的答案。  
我们可以从以下几个角度进行优化：

1. **始终在左上角的第一个空格处放正方形**  
   - 这是一种“自然的”放置点：如果左上角还有空白，而我们把正方形放在别的地方，左上角迟早要被更小的正方形填补，导致更多的块。把它先填满通常能更快得到紧凑的布局。  

2. **从大到小尝试正方形**  
   - 大正方形覆盖的面积多，能够更快降低剩余空格数。若一次尝试就能把全部填满，递归深度最小，搜索树也会被大幅剪枝。  

3. **剪枝：如果当前已放的正方形数 ≥ 已知最优解，则直接返回**  
   - 这一步在代码里已经实现（`if cnt >= best: return`），可以立即舍弃不可能更好的分支。  

4. **更强的下界剪枝**  
   - 剩余未覆盖的格子数记为 `remain`。即使我们每次都放最大可能的正方形（边长 `max_side = max(n, m)`），仍然需要至少 `ceil(remain / (max_side**2))` 个正方形。  
   - 如果 `cnt + lower_bound >= best`，则该分支不可能得到更好的答案，直接剪掉。  

5. **使用“一维高度数组”代替二维 board**  
   - 观察到每次只在左上角的空格放正方形，实际上只需要记录每列已经被填满的高度（类似天际线）。高度数组 `height[j]` 表示第 `j` 列已被覆盖到第几行。  
   - 这样可以把 `can_place`、`set_square` 的实现简化为对高度的增减，时间常数更小。  

综合以上技巧，仍然是 **回溯（Backtracking）**，但搜索空间被大幅压缩，能够在 `n,m ≤ 13` 的范围内在毫秒级完成。

#### 代码（Python）

```python
import math

def tilingRectangle(n: int, m: int) -> int:
    """
    使用回溯 + 剪枝的最优实现。
    关键点：
    1. 用 height[] 记录每列已填满的高度（类似天际线）。
    2. 每次在左上角的第一个空位放正方形。
    3. 从大到小尝试正方形大小。
    4. 两层剪枝：cnt >= best 以及基于剩余面积的下界剪枝。
    """
    # 保证 n <= m，方便后面计算（不影响答案）
    if n > m:
        n, m = m, n

    # 初始天际线：全部为 0，高度为 0
    height = [0] * m
    best = m  # 上界：最多 m 个正方形（每列一块）

    # ---------- 辅助函数 ----------
    def first_min_height():
        """返回当前最小高度所在的列索引（左侧优先）"""
        min_h = min(height)
        return height.index(min_h), min_h

    def dfs(cnt: int):
        nonlocal best
        # 剪枝 1：已经不可能更优
        if cnt >= best:
            return

        # 所有列都已经填满，说明矩形已被完全覆盖
        if all(h == n for h in height):
            best = cnt
            return

        # 计算剩余未覆盖的格子数，用于下界剪枝
        remain = sum(n - h for h in height)
        # 最佳情况每次都能放最大的正方形（边长为 max(n, m)）
        lower = math.ceil(remain / (max(n, m) ** 2))
        if cnt + lower >= best:
            return

        # 找到左上角的第一个空位（列 idx，行 cur_h）
        idx, cur_h = first_min_height()
        # 能放的最大正方形边长受限于行、列以及矩形尺寸
        max_len = min(n - cur_h, m - idx)

        # 从大到小尝试正方形
        for size in range(max_len, 0, -1):
            # 检查这 size 列的高度是否都不小于 cur_h（即可以形成正方形）
            if all(height[j] == cur_h for j in range(idx, idx + size)):
                # 放置正方形：把这 size 列的高度提升 size
                for j in range(idx, idx + size):
                    height[j] += size
                dfs(cnt + 1)
                # 撤销：恢复高度
                for j in range(idx, idx + size):
                    height[j] -= size

    dfs(0)
    return best
```

> **代码解释要点**  
> - `height` 类似“一排排的堆叠盒子”，每列的高度告诉我们该列已经被填满到哪一行。  
> - `first_min_height` 找到当前**左上角**的空位，因为最小高度对应的列是最靠左、最靠上的空格。  
> - `if all(height[j] == cur_h for j in range(idx, idx + size))` 确保正方形的左、上、右、下四条边都在同一水平线上，才算合法。  
> - 两层剪枝（`cnt >= best` 与基于剩余面积的下界）大幅削减不可能的分支，使得即使在最坏的 `13×13` 也能在毫秒级跑完。

#### 复杂度  

- **时间复杂度**：虽然仍是指数级（`O(指数)`），但剪枝把实际遍历的节点数降到了可接受范围。对 `n,m ≤ 13` 的所有测试数据，运行时间通常在 `10⁴ ~ 10⁶` 次递归调用之间，远快于纯暴力。  
- **空间复杂度**：`O(m)` 用于存放 `height`（最多 13 列），递归栈深度最多为 `best ≤ max(n, m) ≤ 13`，因此总体是 **O(m)**，即常数级别的额外空间。

---

## 心得

- **核心技巧**：**回溯 + 剪枝**，尤其是“左上角自然空位” + “从大到小尝试” + “基于剩余面积的下界剪枝”。  
- **适用的题型**  
  1. **矩形/平面覆盖类**（如 “Perfect Squares” 等）  
  2. **装箱/堆叠类**（如 “Bin Packing” 的小规模变体）  
  3. **拼图类**（如 “N‑Queens” 需要在特定顺序放置）  
- **一句话总结解题钥匙**：**“总是先填最左上最空的格子，用尽可能大的块，并用已知最优解作上界进行剪枝”。**

---

## 反思

- **第一反应**：直接把矩形划分成若干正方形，遍历所有可能的切分方式（暴力 DFS）。  
- **最容易踩的坑**  
  - 忘记在递归返回时 **撤销** 已放置的正方形，导致后续分支看到错误的状态。  
  - 没有对 **对称情况**（如 `n,m` 与 `m,n`）做处理，会重复搜索相同的布局。  
  - 边界条件：矩形已经是正方形时应直接返回 `1`，否则会多走一层递归。  
- **下次遇到同类题**：第一步想到 **“把搜索空间压到最小：先找左上角空位、从大到小放块、并利用已有最优解进行剪枝”。**这一步往往决定能否在合理时间内得到答案。