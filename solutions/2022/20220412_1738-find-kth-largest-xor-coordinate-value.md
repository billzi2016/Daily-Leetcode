# #1738. 第 K 大 XOR 坐标值 / Find Kth Largest XOR Coordinate Value

> 难度：中等 · 标签：Array、Divide and Conquer、Bit Manipulation、Sorting、Heap (Priority Queue)、Matrix、Prefix Sum、Quickselect · [LeetCode 链接](https://leetcode.com/problems/find-kth-largest-xor-coordinate-value/)

---

## 题目（英文原版）

**Description**

You are given a 2D matrix of size m x n, consisting of non-negative integers. You are also given an integer k.
The value of coordinate (a, b) of the matrix is the XOR of all matrix[i][j] where 0 <= i <= a < m and 0 <= j <= b < n (0-indexed).
Find the kth largest value (1-indexed) of all the coordinates of matrix.

**Examples**

**Example 1:**

```
Input: matrix = [[5,2],[1,6]], k = 1
Output: 7
Explanation: The value of coordinate (0,1) is 5 XOR 2 = 7, which is the largest value.
```

**Example 2:**

```
Input: matrix = [[5,2],[1,6]], k = 2
Output: 5
Explanation: The value of coordinate (0,0) is 5 = 5, which is the 2nd largest value.
```

**Example 3:**

```
Input: matrix = [[5,2],[1,6]], k = 3
Output: 4
Explanation: The value of coordinate (1,0) is 5 XOR 1 = 4, which is the 3rd largest value.
```

**Constraints**

- m == matrix.length
- n == matrix[i].length
- 1 <= m, n <= 1000
- 0 <= matrix[i][j] <= 106
- 1 <= k <= m * n

---

## 题目（中文翻译）

**题目描述**  
给定一个大小为 `m × n` 的二维矩阵 `matrix`，其中元素均为非负整数。同时给定一个整数 `k`。  
矩阵中坐标 `(a, b)`（0‑索引）的 **值** 定义为所有满足 `0 ≤ i ≤ a < m` 且 `0 ≤ j ≤ b < n` 的 `matrix[i][j]` 的 **异或（XOR）** 结果。  
请找出矩阵所有坐标值中的第 `k` 大（1‑索引）值。

**示例**  

示例 1  
```
Input: matrix = [[5,2],[1,6]], k = 1
Output: 7
Explanation: 坐标 (0,1) 的值为 5 XOR 2 = 7，它是最大的值。
```

示例 2  
```
Input: matrix = [[5,2],[1,6]], k = 2
Output: 5
Explanation: 坐标 (0,0) 的值为 5 = 5，它是第二大的值。
```

示例 3  
```
Input: matrix = [[5,2],[1,6]], k = 3
Output: 4
Explanation: 坐标 (1,0) 的值为 5 XOR 1 = 4，它是第三大的值。
```

**约束条件**  
- `m == matrix.length`  
- `n == matrix[i].length`  
- `1 ≤ m, n ≤ 1000`  
- `0 ≤ matrix[i][j] ≤ 10^6`  
- `1 ≤ k ≤ m * n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每一个坐标 (a, b) 都把左上角的所有元素全部 XOR 一遍**，把得到的值存下来，最后把所有值从大到小排序，取第 `k` 个。  

- **使用的数据结构**：  
  - 一个普通的二维列表 `matrix`（题目已经给出），我们把它当作“厨房里的食材”。  
  - 另外再准备一个一维列表 `vals`，用来装每个坐标的 XOR 结果，类似于“把每道菜的味道分数记下来”。  

- **为什么这个方法一定能得到正确答案**：  
  题目要求的坐标值正好是“左上子矩阵的所有元素异或”。只要我们真的把对应的子矩阵的元素全部遍历并异或，得到的就是坐标的真实值。遍历完所有坐标后，`vals` 中就包含了 **全部** `m·n` 个坐标的值，排序后第 `k` 大自然就是答案。  

- **时间/空间复杂度的大白话解释**：  
  - 对每个坐标 `(a,b)`，我们要遍历 `0..a` 行、`0..b` 列，总共 ` (a+1)*(b+1) ` 个元素。最坏情况下 `(a,b)` 可以是右下角 `(m-1,n-1)`，那就是遍历整个矩阵 `m·n` 次。  
  - 于是总体的遍历次数是  
    \[
    \sum_{a=0}^{m-1}\sum_{b=0}^{n-1}(a+1)(b+1)=O(m^2n^2)
    \]  
    用大白话说，就是 **矩阵的行数和列数各自都要平方**，如果矩阵是 1000×1000，运算次数会达到 **10^12**，根本跑不完。  
  - 额外的空间只用来存放 `m·n` 个结果，大小是 `O(mn)`，这在本题是可以接受的。  

#### 代码（Python）  

```python
def kthLargestValue_bruteforce(matrix, k):
    """
    暴力解法：对每个坐标重新遍历左上子矩阵求 XOR
    时间复杂度 O(m^2 * n^2) ，空间复杂度 O(mn)
    """
    m, n = len(matrix), len(matrix[0])
    vals = []                       # 用来收集所有坐标的 XOR 值

    # 遍历每个坐标 (a, b)
    for a in range(m):
        for b in range(n):
            cur = 0                  # 当前坐标的 XOR 结果，初始为 0（XOR 的中性元）
            # 遍历左上子矩阵的所有元素
            for i in range(a + 1):
                for j in range(b + 1):
                    cur ^= matrix[i][j]   # 异或运算
            vals.append(cur)        # 把结果放进列表

    # 从大到小排序后取第 k 个（k 为 1-indexed）
    vals.sort(reverse=True)
    return vals[k - 1]
```

#### 复杂度  

- **时间复杂度**：`O(m²·n²)`  
  - 这里的 `O` 符号可以想象成“把行数和列数各自都乘了两次”。如果矩阵是 10×10，运算大约是 10⁴ 次；如果是 1000×1000，就会是 10¹² 次，显然不可接受。  
- **空间复杂度**：`O(m·n)`  
  - 只需要一个长度为 `m·n` 的数组来存放所有坐标的值，和原矩阵大小同级别。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复遍历左上子矩阵是最大的性能瓶颈**。我们需要一种方式，让每个坐标的 XOR 结果在 **常数时间** 内得到。  

**关键技巧：二维前缀异或（Prefix XOR）**  

- 对一维数组，前缀和 `pre[i] = a[0] ⊕ a[1] ⊕ … ⊕ a[i]` 能让区间 `[l, r]` 的和用 `pre[r] ⊕ pre[l‑1]` 计算。  
- 同理，二维情况下也可以定义 **前缀异或矩阵** `px[i][j]`，表示从左上角 `(0,0)` 到 `(i,j)`（包括两端）的所有元素的 XOR。递推式为  

  ```
  px[i][j] = matrix[i][j] 
           ^ px[i-1][j] 
           ^ px[i][j-1] 
           ^ px[i-1][j-1]
  ```

  这里的 `^` 就是 Python 中的异或运算符。这个式子可以类比为“把新加入的格子、上面的前缀、左边的前缀以及左上角的前缀都合并”。  

- **得到坐标值**：一旦前缀矩阵 `px` 构造完成，**每个坐标的值恰好就是 `px[i][j]` 本身**（因为它已经是左上子矩阵的 XOR）。于是我们只需要一次遍历把所有 `px[i][j]` 收集起来。  

- **如何取第 k 大**：  
  - 方法 1：把所有值放进列表，整体排序，时间 `O(mn log(mn))`。  
  - 方法 2（更省时）：维护一个大小为 `k` 的 **小根堆**（最小优先队列）。遍历时把每个值推入堆；如果堆的大小超过 `k`，就弹出堆顶（当前第 `k` 小的），这样堆里始终保留最大的 `k` 个元素。遍历结束后，堆顶就是第 `k` 大的值。  
  - 这里我们采用 **堆** 的实现，时间 `O(mn log k)`，空间 `O(k)`，在 `k` 远小于 `mn` 时非常快。  

- **类比帮助理解**：  
  - 前缀异或矩阵就像 **一本查字典**，字典的“页码”是 `px[i][j]`，只要我们一次性把所有页码写下来，就不需要每次再去翻整本字典。  
  - 小根堆则像 **一个装满了最大 k 个分数的盒子**，盒子里最小的那个分数始终在最前面，等所有分数都放进去后，盒子前面的分数就是第 `k` 大的。  

#### 代码（Python）  

```python
import heapq
from typing import List

def kthLargestValue(matrix: List[List[int]], k: int) -> int:
    """
    最优解：利用二维前缀异或 + 小根堆（size = k）
    时间复杂度 O(m * n * log k) ，空间复杂度 O(k)
    """
    m, n = len(matrix), len(matrix[0])

    # 1) 建立前缀异或矩阵，直接在原地覆盖，省空间
    #    为避免越界，额外多开一行一列 0，方便写公式
    prefix = [[0] * (n + 1) for _ in range(m + 1)]

    #    计算每个 px[i][j]（对应原矩阵的 (i-1, j-1)）
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            prefix[i][j] = (
                matrix[i - 1][j - 1] ^
                prefix[i - 1][j] ^
                prefix[i][j - 1] ^
                prefix[i - 1][j - 1]
            )

    # 2) 用小根堆维护最大的 k 个值
    min_heap = []                     # Python 的 heapq 默认是最小堆

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            val = prefix[i][j]        # 这就是坐标 (i-1, j-1) 的 XOR 值
            if len(min_heap) < k:
                heapq.heappush(min_heap, val)   # 直接加入
            else:
                # 堆里已经有 k 个，只有比堆顶更大的才有资格进入
                if val > min_heap[0]:
                    heapq.heapreplace(min_heap, val)  # pop+push 合二为一

    # 堆顶即第 k 大的值
    return min_heap[0]
```

#### 复杂度  

- **时间复杂度**：`O(m * n * log k)`  
  - 前缀矩阵的构造只需要一次遍历，`O(mn)`。  
  - 对每个坐标的值进行堆操作，堆的大小始终不超过 `k`，每次 `push`/`replace` 的代价是 `log k`。整体是 `mn * log k`。  
  - 用大白话说，就是“先把矩阵的每个格子扫一遍（线性），再在一个装了最多 `k` 件小东西的盒子里插入或替换，插入一次要花 `log k` 步”。  

- **空间复杂度**：`O(k)`（堆的大小） + `O(mn)`（前缀矩阵）  
  - 如果想进一步省掉前缀矩阵的额外空间，可以在原矩阵上就地修改，空间可降到 `O(k)`。这里为了代码可读性保留了 `O(mn)` 的前缀矩阵。  

---  

## 心得  

- **核心技巧**：**二维前缀异或** + **维护 top‑k 的小根堆**。  
- **该技巧适用的题型**：  
  1. “子矩阵求和 / 求异或” 类问题（如 LeetCode 1314 “Matrix Block Sum”）。  
  2. “找第 k 大/小的子数组/子矩阵值” 这类需要频繁查询区间结果的题目（如 1738 “Find Kth Largest XOR Coordinate Value”、 1802 “Maximum Value at a Given Index in a Bounded Array”）。  
- **一句话总结解题钥匙**：**把重复的子矩阵计算一次性预处理好，再用堆把最大的 k 个结果挑出来**。  

---  

## 反思  

- **第一反应**：看到“左上子矩阵的 XOR”，立刻想到“遍历每个坐标的子矩阵”，于是写出了暴力解。  
- **最容易踩的坑**：  
  - **前缀异或公式写错**：`px[i][j]` 必须把左上角的 `px[i‑1][j‑1]` 再异或一次，忘记会导致结果翻倍。  
  - **边界处理**：在使用额外的第 0 行/0 列时，务必把它们初始化为 0，否则会出现索引错误或错误的 XOR。  
  - **堆的大小**：若直接把所有 `mn` 个值放进堆再弹出，会退化成 `O(mn log(mn))`，失去优势。记得始终限制堆的最大容量为 `k`。  
- **下次遇到同类题**：第一步先问自己——**“有没有办法把每个子区间的结果用一次预处理得到？”**，如果答案是“有”，就立刻写前缀/后缀/差分等结构；随后再考虑 **“需要全排序还是只要前 k 大？”**，决定是否使用堆或快速选择。