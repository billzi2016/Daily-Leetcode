# #1284. 将二进制矩阵转换为全零矩阵的最少翻转次数 / Minimum Number of Flips to Convert Binary Matrix to Zero Matrix

> 难度：困难 · 标签：Array、Hash Table、Bit Manipulation、Breadth-First Search、Matrix · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-flips-to-convert-binary-matrix-to-zero-matrix/)

---

## 题目（英文原版）

**Description**

Given a m x n binary matrix mat. In one step, you can choose one cell and flip it and all the four neighbors of it if they exist (Flip is changing 1 to 0 and 0 to 1). A pair of cells are called neighbors if they share one edge.
Return the minimum number of steps required to convert mat to a zero matrix or -1 if you cannot.
A binary matrix is a matrix with all cells equal to 0 or 1 only.
A zero matrix is a matrix with all cells equal to 0.

**Examples**

**Example 1:**

```
Input: mat = [[0,0],[0,1]]
Output: 3
Explanation: One possible solution is to flip (1, 0) then (0, 1) and finally (1, 1) as shown.
```

**Example 2:**

```
Input: mat = [[0]]
Output: 0
Explanation: Given matrix is a zero matrix. We do not need to change it.
```

**Example 3:**

```
Input: mat = [[1,0,0],[1,0,0]]
Output: -1
Explanation: Given matrix cannot be a zero matrix.
```

**Constraints**

- m == mat.length
- n == mat[i].length
- 1 <= m, n <= 3
- mat[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个 `m x n` 的二进制矩阵（binary matrix） `mat`。在一次操作中，你可以选择任意一个单元格并**翻转**（flip）该单元格以及它的四个相邻单元格（如果相邻单元格存在）。相邻单元格指的是共享一条边的单元格。

返回将 `mat` 转换为全零矩阵（zero matrix）所需的最少操作次数；如果无法转换，则返回 `-1`。

**定义**  
- 二进制矩阵：矩阵中所有单元格的取值仅为 `0` 或 `1`。  
- 全零矩阵：矩阵中所有单元格的取值均为 `0`。  

---

## 示例

### 示例 1
**输入**  
``` 
mat = [[0,0],[0,1]]
```
**输出**  
```
3
```
**解释**  
一种可能的操作序列是先翻转位置 `(1, 0)`，再翻转 `(0, 1)`，最后翻转 `(1, 1)`，如图所示即可得到全零矩阵。

### 示例 2
**输入**  
``` 
mat = [[0]]
```
**输出**  
```
0
```
**解释**  
给定的矩阵已经是全零矩阵，无需进行任何操作。

### 示例 3
**输入**  
``` 
mat = [[1,0,0],[1,0,0]]
```
**输出**  
```
-1
```
**解释**  
无论如何翻转，都无法将该矩阵变为全零矩阵。

---

## 约束条件

- `m == mat.length`
- `n == mat[i].length`
- `1 <= m, n <= 3`
- `mat[i][j]` 只能是 `0` 或 `1`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求把一个 **m×n**（`1 ≤ m,n ≤ 3`）的二进制矩阵全部翻成 `0`。  
每一次操作我们可以选中一个格子，把它本身以及上下左右四个相邻格子（如果存在）全部 **取反**（`1↔0`）。  

因为矩阵很小，最多只有 `3×3 = 9` 个格子。  
**关键观察**：对同一个格子翻两次等价于一次也不翻，因为 `1→0→1`、`0→1→0`，最终状态不变。  
所以每个格子 **最多翻一次**，翻零次或一次都可以。  
这就把问题转化为：**在 9（或更少）个格子中挑选一个子集，依次执行对应的翻转操作，最终能否得到全 0 矩阵？**  

我们可以把每一种子集看作一个 **二进制掩码**（bitmask），位 `1` 表示对应格子要翻一次，位 `0` 表示不翻。  
所有可能的子集数量是 `2^(m·n)`，即最多 `2^9 = 512` 种，完全可以枚举。

**步骤**：

1. 把原矩阵压成一个整数 `start`（每个格子对应一位），便于位运算。  
2. 枚举 `mask` 从 `0` 到 `2^(m·n)-1`：  
   - 把 `start` 复制一份 `cur`。  
   - 对每个格子 `i`（对应 `mask` 的第 `i` 位），如果该位为 `1`，就在 `cur` 上执行一次“翻转自身和四邻居”的操作。  
3. 枚举完后检查 `cur` 是否全为 `0`（即整数 `0`），若是则记录下翻的次数 `popcount(mask)`（二进制里 `1` 的个数），取最小值。  
4. 若所有 `mask` 都不能得到全 `0`，返回 `-1`。

> **类比**：把矩阵想成一本字典，每个格子是一页。翻一次相当于把该页和相邻几页的内容全部倒过来（正→反，反→正）。我们要找一种“翻页组合”，让整本书最后全是空白页（全 `0`）。

#### 代码（Python）

```python
from itertools import product

def min_flips_bruteforce(mat):
    m, n = len(mat), len(mat[0])
    total = m * n                       # 格子总数，最多 9

    # -------- 把矩阵压成整数 0~2^(m*n)-1 ----------
    start = 0
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 1:
                # 第 (i*n + j) 位设为 1
                start |= 1 << (i * n + j)

    # -------- 预先算好每个格子翻转会影响的位 ----------
    # flip_mask[k] 表示如果翻第 k 个格子，哪些位会被取反
    flip_mask = []
    for i in range(m):
        for j in range(n):
            mask = 0
            for di, dj in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    mask |= 1 << (ni * n + nj)
            flip_mask.append(mask)

    ans = float('inf')                  # 用来记录最小翻转次数

    # -------- 枚举所有子集（mask） ----------
    for mask in range(1 << total):      # 0 ~ 2^total-1
        cur = start
        # 对每个格子检查 mask 第 i 位是否为 1，若是就翻一次
        for k in range(total):
            if (mask >> k) & 1:         # 第 k 位是 1
                cur ^= flip_mask[k]    # 取反对应的位（异或）
        if cur == 0:                    # 全部变成 0
            flips = bin(mask).count('1')   # 统计翻了多少格子
            ans = min(ans, flips)

    return -1 if ans == float('inf') else ans
```

> 关键行解释  
> - `start |= 1 << (i * n + j)`：把矩阵的 `(i,j)` 格子对应的位设为 1（如果原来是 1）。  
> - `mask >> k & 1`：检查子集 `mask` 中第 `k` 位是否为 1，决定是否对第 `k` 个格子翻转。  
> - `cur ^= flip_mask[k]`：**异或**（XOR）相当于“取反”，只会改变 `flip_mask[k]` 中标记的位。  

#### 复杂度  

- **时间复杂度**：`O( 2^{m·n} · (m·n) )`  
  - 解释：我们遍历 `2^{m·n}`（最多 512）种子集；每种子集要遍历所有格子 `m·n`（最多 9）来检查是否翻转并执行异或操作。  
  - 用大白话说，就是**指数级**的遍历，但因为矩阵只有 9 格子，实际运行很快（几千次运算）。
- **空间复杂度**：`O( m·n )`  
  - 只用了常数个整数和一个长度为 `m·n` 的 `flip_mask` 列表，最多 9 个元素，属于**线性**空间。

---

### 2. 最优解  

#### 思路  

暴力解已经可以在常数时间内跑完（因为搜索空间极小），但它没有利用**搜索顺序**来直接得到最少步数。  
如果把每一种状态（即矩阵的当前配置）看成图中的一个节点，**一次翻转**就是从一个节点到另一个节点的**有向边**。  
我们要找的是 **从起始节点到全零节点的最短路径长度**，这正是 **Breadth‑First Search（BFS）** 的典型应用。

**为什么 BFS 能直接得到最小步数？**  
- BFS 按层展开：先访问所有距离起点 1 步的状态，再访问距离 2 步的状态…  
- 第一次碰到全零状态时，必然是最少翻转次数，因为 BFS 保证了“层序”遍历。

**核心技巧**：

1. **状态压缩**：同样把矩阵压成一个整数（位图），这样每个状态只占一个 `int`，便于哈希查重。  
2. **队列**：保存待扩展的状态以及已经走了多少步。  
3. **访问集合**：用 `set`（或 Python 的 `dict`）记录已经出现过的状态，防止重复搜索。  
4. **邻居生成**：对当前状态的每一个格子尝试一次翻转（即 `cur ^ flip_mask[k]`），得到下一个状态。  

因为矩阵大小至多 `3×3`，状态总数仍是 `2^{9}=512`，BFS 最多遍历这么多节点，时间和空间都是 `O(2^{m·n})`，但它比枚举所有子集更**直接**得到最小步数，且思路在更大规模的类似问题（如 `m,n ≤ 5`）时同样适用。

#### 代码（Python）

```python
from collections import deque

def min_flips_bfs(mat):
    m, n = len(mat), len(mat[0])
    total = m * n

    # ---------- 把矩阵压成整数 ----------
    start = 0
    for i in range(m):
        for j in range(n):
            if mat[i][j] == 1:
                start |= 1 << (i * n + j)

    if start == 0:          # 已经是全零矩阵
        return 0

    # ---------- 预计算每个格子翻转的位掩码 ----------
    flip_mask = []
    for i in range(m):
        for j in range(n):
            mask = 0
            for di, dj in [(0,0), (1,0), (-1,0), (0,1), (0,-1)]:
                ni, nj = i + di, j + dj
                if 0 <= ni < m and 0 <= nj < n:
                    mask |= 1 << (ni * n + nj)
            flip_mask.append(mask)

    # ---------- BFS ----------
    q = deque()
    q.append((start, 0))          # (当前状态, 已经翻的次数)
    visited = {start}

    while q:
        cur, steps = q.popleft()
        # 对每个格子尝试一次翻转，生成邻居状态
        for k in range(total):
            nxt = cur ^ flip_mask[k]   # 翻第 k 格子
            if nxt == 0:               # 找到全零矩阵
                return steps + 1
            if nxt not in visited:
                visited.add(nxt)
                q.append((nxt, steps + 1))

    # BFS 结束仍未找到，说明不可达
    return -1
```

> 关键行解释  
> - `q.append((start, 0))`：把起始状态连同已经用了 0 步放进队列。  
> - `nxt = cur ^ flip_mask[k]`：一次翻转对应的状态转移，使用 **异或** 把对应位取反。  
> - `if nxt == 0:`：一旦出现全零状态，直接返回当前步数 `steps+1`（因为这一步刚刚完成）。  

#### 复杂度  

- **时间复杂度**：`O( 2^{m·n} · (m·n) )`  
  - BFS 最多遍历所有可能的状态（`2^{m·n}`），每个状态要尝试 `m·n` 次翻转来生成邻居。  
  - 与暴力枚举的复杂度相同数量级，但 BFS 在找到答案的那一层就会提前结束，实际运行往往更快。  
- **空间复杂度**：`O( 2^{m·n} )`  
  - 需要保存已访问的状态集合和队列，最坏情况下会把所有状态都放进去（最多 512 个整数），仍然是线性空间。

---

## 心得  

- **核心技巧**：**状态压缩 + BFS**（或全枚举）  
  把矩阵用位图压成一个整数，使得“翻转”操作可以用 **异或** 快速实现；随后在状态图上做最短路搜索。  
- **适用的题型**  
  1. **灯泡开关类**（如 LeetCode 995 `Minimum Number of Steps to Make All Elements Equal`、LC 1284 `Minimum Number of Flips to Convert Binary Matrix to Zero Matrix`）  
  2. **棋盘/格子翻转**（如 LC 752 `Open the Lock`、LC 773 `Sliding Puzzle`）  
  3. **位运算状态搜索**（如 LC 1345 `Jump Game IV` 中的 BFS + 位图）  
- **一句话总结解题钥匙**：  
  “把矩阵压成二进制整数，用异或模拟一次翻转，在所有状态的图上用 BFS 找最短路径”。  

---

## 反思  

- **第一反应**：看到“翻自身和四邻居”，想到**每个格子只能翻一次**，于是直接想到**枚举所有子集**。  
- **最容易踩的坑**  
  1. **边界格子**没有完整的四个邻居，必须在计算翻转掩码时判断坐标是否合法。  
  2. **重复状态**：在 BFS 中若不记录已访问的状态，会出现无限循环（同一个状态被反复加入队列）。  
  3. **位序映射错误**：把 `(i,j)` 映射到第几位时，务必统一使用 `i * n + j`（行主序），否则翻转会对应错位。  
- **下次遇到同类题**：第一步先**把状态压成整数或字符串**，再决定是**全枚举**还是**BFS**，并**提前写出每个格子翻转的位掩码**，这样后面的搜索就可以“一键”完成。