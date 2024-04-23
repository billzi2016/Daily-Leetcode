# #2661. 首次完全被涂色的行或列 / First Completely Painted Row or Column

> 难度：中等 · 标签：Array、Hash Table、Matrix · [LeetCode 链接](https://leetcode.com/problems/first-completely-painted-row-or-column/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array arr, and an m x n integer matrix mat. arr and mat both contain all the integers in the range [1, m * n].
Go through each index i in arr starting from index 0 and paint the cell in mat containing the integer arr[i].
Return the smallest index i at which either a row or a column will be completely painted in mat.

**Examples**

**Example 1:**

```
Input: arr = [1,3,4,2], mat = [[1,4],[2,3]]
Output: 2
Explanation: The moves are shown in order, and both the first row and second column of the matrix become fully painted at arr[2].
```

**Example 2:**

```
Input: arr = [2,8,7,4,1,3,5,6,9], mat = [[3,2,5],[1,4,6],[8,7,9]]
Output: 3
Explanation: The second column becomes fully painted at arr[3].
```

**Constraints**

- m == mat.length
- n = mat[i].length
- arr.length == m * n
- 1 <= m, n <= 105
- 1 <= m * n <= 105
- 1 <= arr[i], mat[r][c] <= m * n
- All the integers of arr are unique.
- All the integers of mat are unique.

---

## 题目（中文翻译）

**描述**  
给定一个 **0 索引** 的整数数组 `arr`，以及一个 `m × n` 的整数矩阵 `mat`。`arr` 和 `mat` 中均恰好包含区间 `[1, m·n]` 内的所有整数。  
从 `arr` 的下标 `0` 开始，依次遍历每个下标 `i`，将矩阵 `mat` 中对应整数 `arr[i]` 所在的单元格涂色。  
返回能够使矩阵 `mat` 的某一行（row）或某一列（column）首次全部被涂色的最小下标 `i`。

**示例**

**示例 1**  
```
Input: arr = [1,3,4,2], mat = [[1,4],[2,3]]
Output: 2
Explanation: 按顺序进行涂色后，矩阵的第一行和第二列在 arr[2] 时均已全部被涂色。
```

**示例 2**  
```
Input: arr = [2,8,7,4,1,3,5,6,9], mat = [[3,2,5],[1,4,6],[8,7,9]]
Output: 3
Explanation: 在 arr[3] 时，矩阵的第二列已全部被涂色。
```

**约束条件**
- `m == mat.length`
- `n = mat[i].length`
- `arr.length == m·n`
- `1 <= m, n <= 10^5`
- `1 <= m·n <= 10^5`
- `1 <= arr[i], mat[r][c] <= m·n`
- `arr` 中的所有整数互不相同。
- `mat` 中的所有整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**一步一步把 `arr` 里的数字对应到矩阵 `mat` 中的格子上**，每涂一次就检查一次所有行和所有列是否已经全部被涂满。

- **数据结构**  
  - `mat` 本身就是一个二维数组，像一张画布。  
  - 为了判断一行/一列是否全部被涂，我们可以用两个一维数组 `rowPainted`、`colPainted`，长度分别是行数 `m`、列数 `n`，记录每行/每列已经被涂了多少格子。  
  - 这里的“哈希表”可以类比成**查字典**：我们把每个数字当作“词”，它对应的坐标 `(r,c)` 当作“页码”。在暴力解里我们不提前建立这个词典，而是每次遍历矩阵去找数字所在的位置——这就像每次查字典都要把整本书翻一遍，显然很慢。

- **为什么正确**  
  - 每一次我们都把 `arr[i]` 对应的格子标记为已涂，并且检查所有行列的涂色数量。只要有一行的已涂格子数等于列数 `n`，或有一列的已涂格子数等于行数 `m`，说明该行或该列已经全部被涂满，返回当前索引 `i`。这与题目要求的“最早出现完整行/列”完全一致。

- **复杂度分析（大白话）**  
  - 对于每个 `arr[i]`，我们都要遍历整个矩阵 `mat`（最多 `m·n` 个格子）去找它所在的坐标，然后再遍历所有行和所有列去判断是否已完整。  
  - 所以总的时间大概是 `（m·n）` 次查找 × `（m·n）` 次检查 ≈ **O((m·n)²)**。如果 `m·n = 10⁵`，这相当于 10⁵ × 10⁵ = 10¹⁰ 次操作，根本跑不完。  
  - 空间上只用了两个长度分别为 `m`、`n` 的计数数组，**O(m + n)**，在本题约束下可以接受。

#### 代码（Python）

```python
def firstCompleteIndex_bruteforce(arr, mat):
    m, n = len(mat), len(mat[0])
    # 记录每行、每列已经被涂的格子数
    row_cnt = [0] * m
    col_cnt = [0] * n

    for i, val in enumerate(arr):
        # 暴力寻找 val 在矩阵中的位置
        found = False
        for r in range(m):
            for c in range(n):
                if mat[r][c] == val:          # 找到对应格子
                    row_cnt[r] += 1          # 该行涂了一格
                    col_cnt[c] += 1          # 该列涂了一格
                    found = True
                    break
            if found:
                break

        # 检查是否出现完整的行或列
        for r in range(m):
            if row_cnt[r] == n:               # 该行已经有 n 格被涂
                return i
        for c in range(n):
            if col_cnt[c] == m:               # 该列已经有 m 格被涂
                return i

    # 按题意一定会返回，下面仅为防止 IDE 报错
    return -1
```

#### 复杂度

- **时间复杂度**：`O((m·n)²)`  
  - “平方”意味着如果矩阵有 10⁴ 个格子，程序大约要跑 10⁸ 次循环；如果 10⁵ 个格子，就要跑 10¹⁰ 次，几乎不可能在一秒内完成。
- **空间复杂度**：`O(m + n)`  
  - 只用了两行计数数组，随矩阵大小线性增长，几乎可以忽略。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**两大瓶颈**：

1. **每次都要遍历整个矩阵去找数字的位置** → 实际上每个数字的坐标是固定的，只要提前记下来，就不必再遍历。
2. **每次检查所有行列是否已满** → 只要在涂格子时即时更新对应的行计数和列计数，并判断这两个计数是否已经达到上限，就可以立刻得出答案，不必再遍历。

**优化步骤**：

1. **预处理位置**  
   - 创建一个大小为 `m·n + 1` 的数组 `pos`（也可以用字典），下标是数字，值是 `(row, col)` 坐标。  
   - 遍历一次矩阵 `mat`，把每个数的坐标存进去。  
   - 这一步相当于把“查字典”变成**一次性建好索引**，后面查询时只需要 `O(1)` 时间。

2. **实时计数**  
   - 再准备两个计数数组 `row_cnt[m]`、`col_cnt[n]`，初始为 0。  
   - 按顺序遍历 `arr`，取出当前数字 `x`，用 `pos[x]` 直接得到它所在的 `(r, c)`。  
   - `row_cnt[r] += 1`，`col_cnt[c] += 1`，随后检查 `row_cnt[r] == n` 或 `col_cnt[c] == m`。  
   - 一旦任意一个条件成立，说明第 `r` 行或第 `c` 列已经全部被涂满，返回当前索引 `i`。

3. **为什么 O(m·n) 就能完成**  
   - 预处理遍历矩阵一次：`O(m·n)`。  
   - 主循环遍历 `arr` 一次：同样是 `O(m·n)`（因为 `arr` 长度正好等于矩阵格子数）。  
   - 两步加起来仍是线性时间 **O(m·n)**，在 10⁵ 规模下完全可以跑在毫秒级。  
   - 额外空间主要是 `pos`（大小 `m·n + 1`）以及两个计数数组，都是 **O(m·n)**，仍在题目限制内。

> **类比**：把矩阵想成一座城市的地图，每栋楼都有唯一的门牌号（`mat` 中的数字）。我们先把所有门牌号对应的坐标登记在“地址簿”里（`pos`），以后有人来找某栋楼，只要翻开地址簿查一眼，就能立刻定位，不必在城市里跑来跑去。

#### 代码（Python）

```python
def firstCompleteIndex(arr, mat):
    """
    返回最早出现完整行或完整列的 arr 索引
    """
    m, n = len(mat), len(mat[0])

    # 1️⃣ 预处理：把每个数字的坐标存进 pos 数组
    # pos[x] = (row, col) ，下标从 1 到 m*n
    pos = [None] * (m * n + 1)          # 大小恰好容纳所有数字
    for r in range(m):
        for c in range(n):
            val = mat[r][c]
            pos[val] = (r, c)          # O(1) 存入

    # 2️⃣ 计数数组，记录每行、每列已经被涂的格子数
    row_cnt = [0] * m
    col_cnt = [0] * n

    # 3️⃣ 按顺序遍历 arr
    for i, x in enumerate(arr):
        r, c = pos[x]                    # O(1) 直接得到坐标
        row_cnt[r] += 1                  # 该行多涂了一格
        col_cnt[c] += 1                  # 该列多涂了一格

        # 检查是否已经完整
        if row_cnt[r] == n or col_cnt[c] == m:
            return i                     # 找到答案，直接返回

    # 按题意一定会在循环中返回，这里仅为防止 IDE 警告
    return -1
```

#### 复杂度

- **时间复杂度**：`O(m·n)`  
  - 只遍历矩阵一次（建坐标表）+ 遍历 `arr` 一次（实时计数），每一步都是常数时间操作。相较于暴力解的平方级别，这就像把“跑十公里”变成了“走十分钟”。  
- **空间复杂度**：`O(m·n)`  
  - 需要存放每个数字的坐标 (`pos`) 以及行/列计数数组。虽然看起来是 `m·n` 级别，但上限仅为 10⁵，占用的内存大约几百 KB，完全可以接受。

---

## 心得

- **核心技巧**：**预处理映射 + 计数数组**（类似“一次遍历 + 哈希表”）。  
- **适用的题型**  
  1. “逐步激活格子后，第一次出现某行/列全满” 类似本题。  
  2. “给定一系列操作，何时第一次使某个集合的元素全部出现” —— 如 LeetCode 1482 *“将数组划分成若干子数组，使每个子数组的最小值相同”*。  
  3. “从序列中逐个标记元素，求第一次满足某个计数阈值的下标” —— 如 1732 *“找到最近的有相同颜色的柱子”*（使用哈希表记录位置）。  
- **一句话总结**：**先把“每个数字在矩阵中的位置”记下来，随后在遍历 `arr` 时即时更新行/列计数并检查阈值**，这样就能在 O(总格子数) 的时间内得到答案。

---

## 反思

- **第一反应**：看到“每次涂格子后检查所有行列”，自然会想到直接遍历检查——也就是暴力解。  
- **最容易踩的坑**  
  1. **忘记提前记录坐标**，导致每次查找 O(m·n)。  
  2. **计数阈值写反**：行满的阈值是列数 `n`，列满的阈值是行数 `m`，容易把二者搞混。  
  3. **边界条件**：`m` 或 `n` 为 1 时，第一步就可能直接满足，需要确保代码在 `row_cnt[r] == n` 或 `col_cnt[c] == m` 时立即返回。  
- **下次遇到同类题的第一步**：**先思考“是否可以把每个元素的关键信息（位置、所属集合等）预先映射到 O(1) 的查询结构”。** 有了这一步，后面的增量更新往往就能在一次遍历内完成。