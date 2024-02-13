# #2579. 统计着色单元格的总数 / Count Total Number of Colored Cells

> 难度：中等 · 标签：Math · [LeetCode 链接](https://leetcode.com/problems/count-total-number-of-colored-cells/)

---

## 题目（英文原版）

**Description**

There exists an infinitely large two-dimensional grid of uncolored unit cells. You are given a positive integer n, indicating that you must do the following routine for n minutes:
Below is a pictorial representation of the state of the grid after minutes 1, 2, and 3.
Return the number of colored cells at the end of n minutes.

**Examples**

**Example 1:**

```
Input: n = 1
Output: 1
Explanation: After 1 minute, there is only 1 blue cell, so we return 1.
```

**Example 2:**

```
Input: n = 2
Output: 5
Explanation: After 2 minutes, there are 4 colored cells on the boundary and 1 in the center, so we return 5.
```

**Constraints**

- 1 <= n <= 105

---

## 题目（中文翻译）

存在一个无限大的二维网格（grid），初始时所有单元格（cell）均未着色。给定一个正整数 `n`，表示需要按照下述规则进行 `n` 分钟的操作：

（具体的着色规则在原题中通过示意图给出，此处省略描述）

下面是第 1、2、3 分钟结束时网格状态的示意图。

返回在第 `n` 分钟结束时已着色的单元格数量。

### 示例

**示例 1**  
Input: `n = 1`  
Output: `1`  
Explanation: 经过 1 分钟后，只有 1 个蓝色单元格，所以返回 1。

**示例 2**  
Input: `n = 2`  
Output: `5`  
Explanation: 经过 2 分钟后，边界上有 4 个着色单元格，中心有 1 个，所以返回 5。

### 约束条件
- `1 <= n <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步一步地模拟题目描述的过程**：  
- 把格子看成一张无限大的纸，已染色的格子用 `(x, y)` 坐标记录在 `set` 中。  
- 第 1 分钟只染 `(0,0)` 一个格子。  
- 以后每分钟，把当前所有已染色格子的 **上下左右四个相邻格子** 加入集合（如果已经在集合里就不重复加入）。  

> **类比**：`set` 就像一本“查字典”。词（坐标）是 **key**，如果词已经在字典里（格子已经染色），查到后直接返回，不会再插入重复的记录。

为什么这种做法一定能得到正确答案？  
因为题目说“每分钟把所有已经染色格子的四个相邻格子也染色”，只要我们严格按照这个规则把新格子加入集合，最终集合的大小就是所有染色格子的数量。

#### 代码（Python）

```python
def colored_cells_bruteforce(n: int) -> int:
    # 已染色格子的集合，初始只含原点 (0, 0)
    colored = {(0, 0)}

    # 四个方向的向量，分别代表上、下、左、右
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    for _ in range(1, n):                     # 第 1 分钟已经完成，剩下 n-1 次循环
        new_cells = set()
        for x, y in colored:                  # 遍历当前所有已染色格子
            for dx, dy in dirs:               # 为每个格子尝试四个相邻位置
                nx, ny = x + dx, y + dy
                new_cells.add((nx, ny))       # 加入新格子（集合会自动去重）
        colored |= new_cells                  # 合并新格子到已染色集合
    return len(colored)                       # 集合大小即为染色格子总数
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  第 `i` 分钟会产生大约 `4·(i‑1)` 个新格子，累计大约 `1 + 4 + 8 + … + 4·(n‑1) = O(n²)` 次插入/查找操作。  
  用“大白话”说，就是随着分钟数增长，格子数量呈二次方增长，运算次数也随之二次方增长。

- **空间复杂度**：`O(n²)`  
  最后要存所有染色格子的坐标，数量本身就是 `O(n²)`，所以需要同等量的内存。

---

### 2. 最优解

#### 思路  

从暴力解我们可以观察到**染色的形状**：

- 第 1 分钟：只有原点 → 形状是一个点。  
- 第 2 分钟：在原点的上下左右各加一个格子 → 形成一个 **曼哈顿距离 ≤ 1** 的菱形。  
- 第 3 分钟：再向外扩展一层 → **曼哈顿距离 ≤ 2** 的菱形。  

可以把 **每分钟的扩展** 看成“把当前菱形的每一条边往外平移一格”。  
于是第 `n` 分钟结束时，所有被染色的格子恰好是 **曼哈顿距离 ≤ n‑1** 的格子集合。

> **曼哈顿距离**：从原点到格子 `(x, y)` 的距离是 `|x| + |y|`（走格子只能上下左右，走的格子数即为距离）。

所以我们只要 **统计** 满足 `|x| + |y| ≤ r`（其中 `r = n‑1`）的整数点有多少个即可。

**统计技巧**  
- 当距离恰好等于 `k`（`k ≥ 1`）时，满足 `|x| + |y| = k` 的点有 `4·k` 个（想象四条对称的直线，每条上有 `k` 个点）。  
- 把所有层叠加：  

```
总数 = 1（k=0） + Σ_{k=1}^{r} 4·k
     = 1 + 4·(1 + 2 + … + r)
     = 1 + 4· r·(r+1)/2
     = 1 + 2·r·(r+1)
```

把 `r = n‑1` 代入：

```
答案 = 1 + 2·(n‑1)·n
     = 2·n² – 2·n + 1
```

这就是 **闭式公式**，只需要 O(1) 时间、O(1) 空间就能算出答案。

#### 代码（Python）

```python
def colored_cells(n: int) -> int:
    """
    直接使用推导出的公式:
        ans = 2 * n * n - 2 * n + 1
    时间 O(1)，空间 O(1)
    """
    return 2 * n * n - 2 * n + 1
```

#### 复杂度

- **时间复杂度**：`O(1)` — 只做常数次算术运算。  
  与暴力解的二次方时间相比，快了 **几百倍甚至上千倍**（对 n=10⁵ 来说，暴力需要约 10¹⁰ 步，公式只要一步）。

- **空间复杂度**：`O(1)` — 不需要额外存储格子，只用几个整数变量。

---

## 心得

- **核心技巧**：把“每分钟向四周扩展”转化为 **曼哈顿距离 ≤ r 的格子计数**，再利用等差数列求和得到闭式公式。  
- **适用的题型**  
  1. “层层扩张”形成的菱形或正方形计数（如 LeetCode 1271 “Count Number of Good Subarrays” 的几何版）。  
  2. “以原点为中心的 Manhattan 球体格子数”类问题（例如 “Number of Lattice Points Inside a Circle” 的曼哈顿版）。  
- **一句话总结**：**把扩张过程抽象为距离层级，求和即得答案**。

---

## 反思

- **第一反应**：看到“每分钟在四个方向扩张”，本能想到 BFS/集合模拟——也就是暴力解。  
- **最容易踩的坑**  
  - 忽略 **无限大网格** 的概念，以为需要真的建一个大矩阵，导致内存爆炸。  
  - 没有注意到 **对称性**：每层新格子数是 `4·k`，如果直接遍历坐标会重复计数。  
  - 边界 `n = 1` 时公式仍然成立，需确认没有除零或负数错误。  
- **下次遇到同类题**：第一步先 **画几分钟的示意图**，观察形状是否是等距层的叠加；如果是，立刻尝试 **用距离或层数求和**，寻找闭式公式。