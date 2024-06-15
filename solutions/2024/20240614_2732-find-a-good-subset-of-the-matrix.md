# #2732. 寻找矩阵的良好子集 / Find a Good Subset of the Matrix

> 难度：困难 · 标签：Array、Hash Table、Bit Manipulation、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-a-good-subset-of-the-matrix/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n binary matrix grid.
Let us call a non-empty subset of rows good if the sum of each column of the subset is at most half of the length of the subset.
More formally, if the length of the chosen subset of rows is k, then the sum of each column should be at most floor(k / 2).
Return an integer array that contains row indices of a good subset sorted in ascending order.
If there are multiple good subsets, you can return any of them. If there are no good subsets, return an empty array.
A subset of rows of the matrix grid is any matrix that can be obtained by deleting some (possibly none or all) rows from grid.

**Examples**

**Example 1:**

```
Input: grid = [[0,1,1,0],[0,0,0,1],[1,1,1,1]]
Output: [0,1]
Explanation: We can choose the 0th and 1st rows to create a good subset of rows.
The length of the chosen subset is 2.
- The sum of the 0th column is 0 + 0 = 0, which is at most half of the length of the subset.
- The sum of the 1st column is 1 + 0 = 1, which is at most half of the length of the subset.
- The sum of the 2nd column is 1 + 0 = 1, which is at most half of the length of the subset.
- The sum of the 3rd column is 0 + 1 = 1, which is at most half of the length of the subset.
```

**Example 2:**

```
Input: grid = [[0]]
Output: [0]
Explanation: We can choose the 0th row to create a good subset of rows.
The length of the chosen subset is 1.
- The sum of the 0th column is 0, which is at most half of the length of the subset.
```

**Example 3:**

```
Input: grid = [[1,1,1],[1,1,1]]
Output: []
Explanation: It is impossible to choose any subset of rows to create a good subset.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m <= 104
- 1 <= n <= 5
- grid[i][j] is either 0 or 1.

---

## 题目（中文翻译）

给定一个下标从 0 开始的 **m × n** 二进制矩阵（binary matrix）`grid`。

我们将 **非空子集（subset）** 的若干行称为**良好**，如果该子集中每一列的和不超过子集长度的一半。  
更形式化地说，若选取的行子集长度为 **k**，则每一列的和必须不大于 `floor(k / 2)`（向下取整）。

返回一个整数数组，包含构成良好子集的行下标，且按升序排序。  
- 若存在多个良好子集，返回任意一个即可。  
- 若不存在良好子集，返回空数组。

矩阵 `grid` 的行子集指的是通过删除（可能不删除或全部删除）若干行后得到的矩阵。

## 示例

### 示例 1
**输入**  
```json
grid = [[0,1,1,0],
        [0,0,0,1],
        [1,1,1,1]]
```
**输出**  
```
[0,1]
```
**解释**  
我们可以选择第 0 行和第 1 行构成一个良好子集。  
子集长度为 2。  
- 第 0 列的和为 `0 + 0 = 0`，不超过子集长度的一半。  
- 第 1 列的和为 `1 + 0 = 1`，不超过子集长度的一半。  
- 第 2 列的和为 `1 + 0 = 1`，不超过子集长度的一半。  
- 第 3 列的和为 `0 + 1 = 1`，不超过子集长度的一半。

### 示例 2
**输入**  
```json
grid = [[0]]
```
**输出**  
```
[0]
```
**解释**  
选择第 0 行即可得到一个良好子集。  
子集长度为 1。  
- 第 0 列的和为 `0`，不超过子集长度的一半。

### 示例 3
**输入**  
```json
grid = [[1,1,1],
        [1,1,1]]
```
**输出**  
```
[]
```
**解释**  
不存在任何行子集能够满足良好子集的条件。

## 约束条件
- `m == grid.length`
- `n == grid[i].length`
- `1 <= m <= 10^4`
- `1 <= n <= 5`
- `grid[i][j]` 只能是 `0` 或 `1`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的行子集都枚举一遍**，然后检查每个子集是否满足题目条件。  

- **子集**：把矩阵的行看成一堆卡片，随意挑出几张（至少一张）组成一个新矩阵。  
- **检查**：设挑出的行数为 `k`，对每一列统计 1 的个数 `cnt`，如果 `cnt ≤ floor(k/2)`，则这列合格；所有列都合格则整个子集合格。  

> **类比**：把每列的 1 当成“投票”。如果挑了 `k` 行，那么每列最多只能有 `k/2` 票赞成（向下取整），否则这列“超标”。  

这种方法一定能找出答案（如果有的话），因为我们把**所有**可能的子集都检查了一遍。

#### 代码（Python）

```python
from itertools import combinations
from math import floor
from typing import List

def goodSubset_bruteforce(grid: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])
    # 逐个子集大小遍历，最小的满足条件的直接返回
    for k in range(1, m + 1):                     # 子集的行数从 1 到 m
        for rows in combinations(range(m), k):   # 选出 k 行的所有组合
            ok = True
            # 检查每一列是否满足 “1 的数量 ≤ floor(k/2)”
            for col in range(n):
                cnt = sum(grid[r][col] for r in rows)   # 统计该列的 1 的个数
                if cnt > floor(k / 2):                  # 超过上限，子集不合格
                    ok = False
                    break
            if ok:                                       # 找到第一个合格子集
                return list(rows)                        # 已经是升序的
    return []                                            # 没有合格子集
```

> 关键行解释  
> - `combinations(range(m), k)`：相当于把 `m` 张卡片中挑 `k` 张的所有方式。  
> - `sum(grid[r][col] for r in rows)`：把挑出来的行在同一列的 1 加起来，就是该列的“投票数”。  

#### 复杂度  

- **时间复杂度**：`O( Σ_{k=1}^{m} C(m, k) * k * n )`  
  - `C(m, k)` 是组合数，表示挑 `k` 行的方式数。  
  - 对每个子集我们要遍历 `k` 行、`n` 列来统计 1 的个数。  
  - 简单说就是**指数级**，在最坏情况下会遍历 `2^m` 个子集，`m` 可达 10⁴ 时根本不可行。  

- **空间复杂度**：`O(k)`（递归/迭代过程中保存当前子集的行号），最多 `O(m)`。  

> 大白话：  
> - 时间复杂度的 `2^m` 意味着如果把每行想成一个开关（开=选，关=不选），所有可能的开关组合数量会随行数指数增长，行数稍大就会“爆炸”。  
> - 空间主要是存放当前检查的行编号，和输入规模同量级。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到，真正的瓶颈是**枚举所有子集**。  
提示里已经给出关键事实：

> **如果存在合格子集，那么一定可以找到大小为 1 或 2 的合格子集。**

这意味着我们只需要检查两种情况：

1. **单行子集**（size = 1）  
   - 条件是：该行所有元素都是 `0`，因为 `k = 1` 时 `floor(k/2) = 0`，每列的 1 的数量必须 ≤ 0。  
   - 检查方式：遍历每行，若全为 `0`，直接返回该行索引。

2. **两行子集**（size = 2）  
   - 此时 `k = 2`，`floor(k/2) = 1`，每列的 1 的数量只能是 `0` 或 `1`。  
   - 换句话说，两行 **不能在同一列同时出现 1**。如果把每行看成一个二进制掩码（`0/1` 序列对应整数），则两行掩码的 **按位与** 必须为 `0`。  

   由于 `n ≤ 5`，每行的二进制掩码最多只有 `2⁵ = 32` 种可能。我们可以：

   - 把每行转成整数 `mask`（例如 `[0,1,1,0] → 0b0110 = 6`）。  
   - 用一个字典 `mask → 行索引列表` 记录出现过的掩码。  
   - **遍历所有可能的掩码组合** `(mask1, mask2)`，只要 `mask1 & mask2 == 0`（按位与为 0），并且这两个掩码在矩阵中都有出现，就得到一组合格的两行。  

   由于掩码种类最多 32，遍历所有组合的时间是 `O(32²) = O(1)`，与 `m` 大小无关。

> **类比**：  
> - 把每行看成一把钥匙，钥匙的每个齿（位）要么是凹（0）要么是凸（1）。两把钥匙一起使用时，任何位置不能出现两个凸齿（两个 1），否则“卡住”。这正是 `mask1 & mask2 == 0` 的含义。  

#### 代码（Python）

```python
from typing import List, Dict

def goodSubset_optimal(grid: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])

    # ---------- 1. 检查单行 ----------
    for i, row in enumerate(grid):
        if all(v == 0 for v in row):          # 行全为 0
            return [i]                        # 直接返回该行索引

    # ---------- 2. 把每行转成二进制掩码 ----------
    mask_to_idx: Dict[int, List[int]] = {}    # 同一个掩码可能对应多行
    for i, row in enumerate(grid):
        mask = 0
        for j, v in enumerate(row):
            if v == 1:
                mask |= 1 << j               # 第 j 列为 1 时，把第 j 位设为 1
        mask_to_idx.setdefault(mask, []).append(i)

    # ---------- 3. 枚举两行 ----------
    masks = list(mask_to_idx.keys())
    for i, m1 in enumerate(masks):
        for m2 in masks[i:]:                  # 只需要遍历一次组合，包含 m1==m2 的情况
            if m1 & m2:                       # 按位与不为 0，说明有列同时为 1，不合格
                continue
            # 至少各自出现一次即可
            idx1 = mask_to_idx[m1][0]         # 任取一行
            if m1 == m2:
                # 同一个掩码但需要两行，必须保证该掩码出现了至少两次
                if len(mask_to_idx[m1]) < 2:
                    continue
                idx2 = mask_to_idx[m1][1]     # 取第二行
            else:
                idx2 = mask_to_idx[m2][0]     # 不同掩码，直接取各自的任意一行
            return sorted([idx1, idx2])      # 按升序返回

    # ---------- 4. 没有合格子集 ----------
    return []
```

> 关键行中文注释  
> - `all(v == 0 for v in row)`：检查一行是否全是 `0`，对应子集大小 1 的条件。  
> - `mask |= 1 << j`：把第 `j` 列的 `1` 放到二进制的第 `j` 位上。  
> - `if m1 & m2:`：按位与不为 `0` 表示这两行在某列都有 `1`，不满足 “每列最多 1 个 1”。  
> - `mask_to_idx.setdefault(mask, []).append(i)`：把同样的掩码收集到一起，方便后面取行号。  

#### 复杂度  

- **时间复杂度**：`O(m * n + 32²)`  
  - 将每行转成掩码需要遍历 `m` 行、`n` 列，`n ≤ 5`，所以是 `O(m)`。  
  - 掩码组合的遍历最多 `32 * 32` 次，常数级，记作 `O(1)`。  
  - 与暴力解的指数级相比，几乎是线性时间。  

- **空间复杂度**：`O(m)`  
  - 需要保存每行对应的掩码以及行号列表，最坏情况每行都有唯一掩码，存 `m` 条记录。  

> 与暴力解对比：  
> - 暴力解是 `O(2^m)`，几乎不可能在 `m = 10⁴` 时跑完。  
> - 最优解只需一次线性遍历，加上一小段常数时间的组合检查，轻松通过所有测试。  

---

## 心得  

- **核心技巧**：利用题目给出的 **“若有解，则必有大小为 1 或 2 的解”**，把原本指数级的子集搜索压缩到常数级的检查。  
- **适用场景**：  
  1. **行/列约束的子集问题**，当约束可以用位运算或“至多 k 个 1”描述时。  
  2. **小维度（n ≤ 5）+ 大行数** 的矩阵或集合问题，常用 **位掩码 + 哈希表** 进行去重和快速匹配。  
  3. **“是否存在满足条件的子集”**，而不是求最优值的情况，常可利用 **结构性证明**（如本题的大小上界）直接降维。  

> **一句话总结**：  
> 只要先把每行压成二进制掩码，再利用“两个掩码按位与为 0”这个简单判定，就能在 O(m) 时间内找出满足条件的行子集。  

---

## 反思  

- **第一反应**：直接想到枚举所有子集，结果发现时间爆炸。  
- **最容易踩的坑**：  
  - 忘记 `k = 1` 时的阈值是 `0`，导致误判包含有 `1` 的单行。  
  - 在两行检查时，忽略了同一掩码出现两次的情况（比如两行完全相同且全为 `0`），会错误返回只有一行的索引。  
  - 处理返回的行索引时要保证升序，否则不符合输出要求。  

- **下次遇到类似题目**：第一步先思考**是否可以用位掩码或哈希表把高维信息压缩**，再利用**题目给出的结构性结论**（如子集大小上界）把搜索空间直接削减到常数级。这样就能把“看似困难的组合搜索”变成“一次线性扫描”。