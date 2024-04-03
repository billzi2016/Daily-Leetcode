# #2639. 寻找网格列的宽度 / Find the Width of Columns of a Grid

> 难度：简单 · 标签：Array、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-the-width-of-columns-of-a-grid/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed m x n integer matrix grid. The width of a column is the maximum length of its integers.
Return an integer array ans of size n where ans[i] is the width of the ith column.
The length of an integer x with len digits is equal to len if x is non-negative, and len + 1 otherwise.

**Examples**

**Example 1:**

```
Input: grid = [[1],[22],[333]]
Output: [3]
Explanation: In the 0th column, 333 is of length 3.
```

**Example 2:**

```
Input: grid = [[-15,1,3],[15,7,12],[5,6,-2]]
Output: [3,1,2]
Explanation: 
In the 0th column, only -15 is of length 3.
In the 1st column, all integers are of length 1. 
In the 2nd column, both 12 and -2 are of length 2.
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 100
- -109 <= grid[r][c] <= 109

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的 `m x n` 整数矩阵（matrix）`grid`。一列的宽度（width）定义为该列中所有整数（integer）的 **长度（length）** 的最大值。  
整数 `x` 的长度计算方式如下：若 `x` 为非负数，则长度等于其十进制表示的位数 `len`；若 `x` 为负数，则长度等于 `len + 1`（多算一个负号）。  

返回一个大小为 `n` 的整数数组 `ans`，其中 `ans[i]` 为第 `i` 列的宽度。

**示例**  

示例 1:  
```
Input: grid = [[1],[22],[333]]
Output: [3]
Explanation: 在第 0 列，333 的长度为 3。
```

示例 2:  
```
Input: grid = [[-15,1,3],[15,7,12],[5,6,-2]]
Output: [3,1,2]
Explanation: 
- 第 0 列，只有 -15 的长度为 3。  
- 第 1 列，所有整数的长度均为 1。  
- 第 2 列，12 和 -2 的长度均为 2。
```

**约束条件**  
- `m == grid.length`  
- `n == grid[i].length`  
- `1 <= m, n <= 100`  
- `-10^9 <= grid[r][c] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把矩阵一列一列地扫过去**，每遇到一个元素，就算出它的「长度」——  
- 正数 123 的长度是 3（因为有 3 位数字）  
- 负数 -45 的长度是 3（因为还有一个符号位 ‘-’）  

算完长度后，用一个变量记录当前列出现过的最大长度，等整列扫完后把这个最大值放进答案数组 `ans` 的对应位置。

> **类比**：把每一列想象成一本书的章节，章节里有很多段落（矩阵中的数字）。我们要找出章节里**最长的段落**，于是把所有段落一个一个读出来，记下最长的那段。

为什么一定能得到正确答案？因为我们遍历了该列的**所有**元素，且每次都比较了「当前最大」和「本元素长度」，最终留下的必然是最大值。

#### 代码（Python）

```python
from typing import List

def findColumnWidths(grid: List[List[int]]) -> List[int]:
    # 行数 m，列数 n
    m, n = len(grid), len(grid[0])
    ans = [0] * n                     # 用来存放每列的最大长度

    # ---------- 暴力遍历每一列 ----------
    for col in range(n):              # 逐列
        max_len = 0
        for row in range(m):          # 逐行查看该列的每个元素
            num = grid[row][col]

            # ---------- 计算数字的长度 ----------
            # 先把负号算进去：如果是负数，长度要 +1
            cur_len = 1 if num < 0 else 0
            # 取绝对值后，除以 10 直到变成 0，除的次数就是位数
            x = abs(num)
            while x:
                cur_len += 1           # 每除一次，位数 +1
                x //= 10
            # 当 num 为 0 时，上面的 while 不会执行，但 0 的长度应为 1
            if num == 0:
                cur_len = 1

            # 更新当前列的最大长度
            if cur_len > max_len:
                max_len = cur_len
        ans[col] = max_len            # 把该列的答案写进结果数组
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(m * n * k)`，其中 `k` 是数字的位数（最多 10，因为 |num| ≤ 10⁹）。可以把 `k` 看成一个很小的常数，所以整体仍是 **线性** 的 `O(m·n)`。  
  大白话：我们把矩阵的每一个格子都看了一遍，格子越多，耗时越多。

- **空间复杂度：** `O(n)`，只用了一个长度为列数的答案数组 `ans`，其它变量都是常数级别的。  
  大白话：除了存答案的地方，几乎不占额外空间。

---

### 2. 最优解

#### 思路  

从暴力解来看，**最大的性能瓶颈**是**每次都用循环除以 10 来求位数**。虽然位数很小，但我们完全可以用更直接的方式得到长度：**把整数转成字符串**，字符串的长度天然就是我们要的值（负号会算进去），这一步在 Python 中是 `O(k)`，且实现更简洁。

另外，暴力解是**先把每列的最大值算完再放进答案**，其实我们可以在一次遍历矩阵的过程中**同步更新所有列的最大长度**，省去两层循环的嵌套感（虽然时间仍是 `O(m·n)`，但代码更紧凑）。

核心技巧：

1. **字符串长度**：`len(str(num))` 直接得到整数的「长度」。
2. **一次遍历同步更新**：遍历每一行的同时，遍历该行的每一列，使用 `ans[col] = max(ans[col], cur_len)` 即可。

> **类比**：想象我们在一次审阅所有章节的过程中，手里同时拿着每个章节的「最长段落长度」记录本。每读到一个段落，就立刻检查并更新对应章节的记录，而不是读完一章节后再去回顾。

#### 代码（Python）

```python
from typing import List

def findColumnWidths(grid: List[List[int]]) -> List[int]:
    m, n = len(grid), len(grid[0])
    ans = [0] * n                     # ans[i] 保存第 i 列的最大长度

    # ---------- 一次遍历同步更新 ----------
    for row in range(m):
        for col in range(n):
            num = grid[row][col]
            cur_len = len(str(num))   # 直接用字符串长度，负号会算进去
            # 更新第 col 列的最大长度
            if cur_len > ans[col]:
                ans[col] = cur_len
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(m·n)`（每个格子只处理一次）。把整数转成字符串的代价是常数级别的（因为数字最多 10 位），所以整体仍是线性。  
  与暴力解相比，**没有额外的除法循环**，实际运行更快。

- **空间复杂度：** `O(n)`，仅存放答案数组 `ans`。  
  与暴力解相同，但代码更简洁，额外的临时空间几乎为零。

---

## 心得

- **核心技巧**：利用字符串的 `len()` 直接求整数的位数；在一次遍历中同步维护每列的最大值。  
- **适用题型**：  
  1. **列/行统计类**（如求每列的最大/最小/和）  
  2. **矩阵转置或按列处理的题目**（如 “Find the Largest Positive Integer in Each Column”）  
  3. **需要对单个元素做 O(1) 转换的题目**（如 “Count Digits in Each Number”）  
- **一句话总结解题钥匙**：**一次遍历同步更新 + 用字符串直接得到整数长度**。

---

## 反思

- **第一反应**：看到“每列的最大长度”，立刻想到“逐列遍历、逐个比较”。  
- **最容易踩的坑**：  
  - **0 的长度**：`0` 转成字符串是 `"0"`，长度是 1，别忘了这点。  
  - **负数的符号**：如果手动算位数，需要额外加 1；使用 `str()` 时会自动包含符号，避免漏算。  
- **下次遇到同类题**：第一步先**确定遍历方向（行还是列）**，再**思考是否可以在一次遍历里把所有统计都完成**，如果需要对单个元素做额外处理，优先考虑**语言自带的快捷函数**（如 `len(str(x))`）。