# #835. 图像重叠 / Image Overlap

> 难度：中等 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/image-overlap/)

---

## 题目（英文原版）

**Description**

You are given two images, img1 and img2, represented as binary, square matrices of size n x n. A binary matrix has only 0s and 1s as values.
We translate one image however we choose by sliding all the 1 bits left, right, up, and/or down any number of units. We then place it on top of the other image. We can then calculate the overlap by counting the number of positions that have a 1 in both images.
Note also that a translation does not include any kind of rotation. Any 1 bits that are translated outside of the matrix borders are erased.
Return the largest possible overlap.

**Examples**

**Example 1:**

```
Input: img1 = [[1,1,0],[0,1,0],[0,1,0]], img2 = [[0,0,0],[0,1,1],[0,0,1]]
Output: 3
Explanation: We translate img1 to right by 1 unit and down by 1 unit.

The number of positions that have a 1 in both images is 3 (shown in red).
```

**Example 2:**

```
Input: img1 = [[1]], img2 = [[1]]
Output: 1
```

**Example 3:**

```
Input: img1 = [[0]], img2 = [[0]]
Output: 0
```

**Constraints**

- n == img1.length == img1[i].length
- n == img2.length == img2[i].length
- 1 <= n <= 30
- img1[i][j] is either 0 or 1.
- img2[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定两个图像 `img1` 和 `img2`，它们都是大小为 `n × n` 的二进制（binary）方阵。二进制矩阵的取值只能是 `0` 或 `1`。  

我们可以对其中一幅图像进行平移（translation），即将所有的 `1` 向左、右、上、下任意移动任意步数。平移后将该图像覆盖在另一幅图像上。重叠度（overlap）定义为两个图像在相同位置上同时为 `1` 的格子数。  

注意：

- 平移不包括任何旋转（rotation）。  
- 被平移到矩阵边界之外的 `1` 会被擦除（即视为 `0`）。  

返回可能的最大重叠度。

## 示例

### 示例 1
**输入**  
`img1 = [[1,1,0],[0,1,0],[0,1,0]]`  
`img2 = [[0,0,0],[0,1,1],[0,0,1]]`

**输出**  
`3`

**解释**  
我们将 `img1` 向右平移 1 个单位并向下平移 1 个单位。两幅图像在同一位置上为 `1` 的格子数为 3（如红色标记所示）。

### 示例 2
**输入**  
`img1 = [[1]]`  
`img2 = [[1]]`

**输出**  
`1`

### 示例 3
**输入**  
`img1 = [[0]]`  
`img2 = [[0]]`

**输出**  
`0`

## 约束条件

- `n == img1.length == img1[i].length`
- `n == img2.length == img2[i].length`
- `1 ≤ n ≤ 30`
- `img1[i][j]` 只能是 `0` 或 `1`
- `img2[i][j]` 只能是 `0` 或 `1`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把 img1 按所有可能的平移方式（左/右/上/下）放在 img2 上，逐个位置比较 1 的个数，取最大的那个**。  
- **平移的范围**：因为矩阵是 n×n，最左可以往左平移 n‑1 步，最右可以往右平移 n‑1 步；上下同理。所以水平位移 `dx`、垂直位移 `dy` 都在 `[-(n-1), n-1]` 之间。  
- **遍历所有平移**：两层循环枚举 `dx`，两层循环枚举 `dy`，共 `(2n-1)²` 种平移方式。  
- **计算重叠**：对每一种平移，遍历矩阵的每个格子 `(i, j)`，如果平移后的位置仍在矩阵内部且 `img1[i][j] == 1 && img2[i+dx][j+dy] == 1`，则计数加一。  

> **类比**：把两张透明的网格纸（上面有黑点）对齐后，手动把其中一张向左、向右、向上或向下滑动，数一下有多少黑点恰好叠在一起。把所有可能的滑动方式都试一遍，就是暴力解。

这套方法一定能得到正确答案，因为我们穷举了**所有**合法的平移方式，并且在每种方式下精确统计了重叠的 1。

#### 代码（Python）

```python
def largestOverlap(img1, img2):
    n = len(img1)                         # 矩阵大小
    max_overlap = 0                       # 记录最大的重叠数

    # dx, dy 分别表示在行、列方向的平移量
    for dx in range(-(n - 1), n):          # 行平移，从 -n+1 到 n-1
        for dy in range(-(n - 1), n):      # 列平移，从 -n+1 到 n-1
            overlap = 0                    # 当前平移下的重叠计数

            # 遍历 img1 的每个格子
            for i in range(n):
                for j in range(n):
                    # 计算对应的 img2 坐标
                    x = i + dx
                    y = j + dy
                    # 判断坐标是否仍在矩阵内部
                    if 0 <= x < n and 0 <= y < n:
                        # 同时为 1，说明重叠
                        if img1[i][j] == 1 and img2[x][y] == 1:
                            overlap += 1

            # 更新全局最大值
            max_overlap = max(max_overlap, overlap)

    return max_overlap
```

#### 复杂度  

- **时间复杂度**：`O(n^4)`  
  - 解释：我们有 `O(n^2)` 种平移（`dx, dy` 各约 `2n`），每种平移要遍历 `n×n` 的格子，乘起来就是 `n^2 * n^2 = n^4`。  
  - 大白话：如果矩阵是 30×30，最坏情况下要做约 `30^4 ≈ 810,000` 次比较，虽然还能跑完，但已经不算高效了。  

- **空间复杂度**：`O(1)`  
  - 只用了几个常数级的变量，不会随输入规模增长而增加内存。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于：我们对每一种平移都要遍历整张矩阵，即使大部分格子是 0，也要检查一遍。  
观察题目可以发现：**只要记住每个 `1` 的坐标，平移的本质就是“把坐标整体加上同一个向量”。**  

**关键观察**  
- 若把 `img1` 中的一个 `1` 放到 `img2` 中某个 `1` 的位置上，它们之间的平移向量就是 `(dx, dy) = (x2 - x1, y2 - y1)`。  
- 当我们把 **所有** `img1` 的 `1` 用同一个向量平移后，与 `img2` 中的 `1` 重合的个数，正好等于**有多少对 `(img1的1, img2的1)` 产生了相同的向量**。  

于是可以把问题转化为：  
> 对每一对 `img1` 中的 `1` 和 `img2` 中的 `1`，计算它们的相对位移向量 `(dx, dy)`，统计出现次数最多的向量，次数即为最大重叠数。

**实现细节**  
1. 先把两张图片中所有 `1` 的坐标收集到两个列表 `ones1`、`ones2`（比如 `(row, col)`）。  
2. 用一个哈希表（Python 的 `dict`）记录每个向量出现的次数：`offset[(dx, dy)] += 1`。  
3. 哈希表的最大值即为答案。  

> **类比**：想象你有两套星星的坐标图，你把第一套星星整体向右上平移，想让尽可能多的星星正好落在第二套星星上。只要把每颗星星对应的“平移指令”记下来，找出最常被使用的指令，就是最优的平移方式。

这种做法只遍历 **实际出现的 1**，而不是整个 `n×n` 的矩阵，因而在多数情况下会快很多。

#### 代码（Python）

```python
from collections import defaultdict

def largestOverlap(img1, img2):
    n = len(img1)

    # 1. 收集两张图中所有 1 的坐标
    ones1 = [(i, j) for i in range(n) for j in range(n) if img1[i][j] == 1]
    ones2 = [(i, j) for i in range(n) for j in range(n) if img2[i][j] == 1]

    # 2. 哈希表统计每个平移向量出现的次数
    offset_cnt = defaultdict(int)          # key: (dx, dy), value: 出现次数

    for x1, y1 in ones1:                   # 遍历 img1 的每个 1
        for x2, y2 in ones2:               # 与 img2 的每个 1 配对
            dx = x2 - x1                    # 行方向的位移
            dy = y2 - y1                    # 列方向的位移
            offset_cnt[(dx, dy)] += 1       # 记录这个向量

    # 3. 找到出现次数最多的向量，即为最大重叠数
    # 如果两张图全是 0，offset_cnt 为空，此时返回 0
    return max(offset_cnt.values() or [0])
```

#### 复杂度  

- **时间复杂度**：`O(k1 * k2)`，其中 `k1`、`k2` 分别是两张图片中 `1` 的个数。  
  - 最坏情况下 `k1 = k2 = n²`，仍然是 `O(n⁴)`，但在实际数据（尤其是稀疏矩阵）中会大幅降低。  
  - 与暴力解对比：我们不再遍历所有格子，只遍历出现的 `1`，常数因子更小。  

- **空间复杂度**：`O(m)`，`m` 为不同平移向量的数量，最多不超过 `2n-1` × `2n-1 = O(n²)`。  
  - 这相当于在记录每种可能的平移方式出现了多少次，使用的额外内存仍然是可接受的（n ≤ 30）。

---

## 心得  

- **核心技巧**：把“平移”转化为“向量计数”。利用哈希表统计所有可能的位移向量出现次数，最高频即为答案。  
- **适用的题型**  
  1. **图片/矩阵的最大重叠**（本题）。  
  2. **二维点集合的最大平移匹配**（如 LeetCode 835. Image Overlap 的变体）。  
  3. **平面上两个点集的最大相同相对位移**（如求两组坐标的最大共线或相同相对位置）。  
- **一句话总结**：**“把每对 1 的相对位移记下来，最常出现的位移就是最佳平移”。**

---

## 反思  

- **第一反应**：直接把一张图滑动所有可能位置，用双层循环暴力比较。  
- **最容易踩的坑**  
  - **边界判断**：平移后坐标可能越界，需要仔细检查 `0 ≤ x < n`、`0 ≤ y < n`。  
  - **全 0 情况**：如果两张图里没有任何 1，哈希表会为空，返回默认值 0。  
  - **时间限制**：虽然 n ≤ 30 看似不大，但 O(n⁴) 仍可能在 Python 中接近极限，需考虑更高效的思路。  
- **下次遇到同类题**：第一步先把“有效元素”（这里是 1）抽出来，思考它们之间的**相对关系**（位移向量），再用计数/哈希手段寻找最常出现的关系。这样往往能把指数级的暴力直接压缩到只和实际元素数量相关的复杂度。