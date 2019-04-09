# #378. 排好序的矩阵中的第 k 小元素 / Kth Smallest Element in a Sorted Matrix

> 难度：中等 · 标签：Array、Binary Search、Sorting、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/)

---

## 题目（英文原版）

**Description**

Given an n x n matrix where each of the rows and columns is sorted in ascending order, return the kth smallest element in the matrix.
Note that it is the kth smallest element in the sorted order, not the kth distinct element.
You must find a solution with a memory complexity better than O(n2).
Follow up:

**Examples**

**Example 1:**

```
Input: matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8
Output: 13
Explanation: The elements in the matrix are [1,5,9,10,11,12,13,13,15], and the 8th smallest number is 13
```

**Example 2:**

```
Input: matrix = [[-5]], k = 1
Output: -5
```

**Constraints**

- n == matrix.length == matrix[i].length
- 1 <= n <= 300
- -109 <= matrix[i][j] <= 109
- All the rows and columns of matrix are guaranteed to be sorted in non-decreasing order.
- 1 <= k <= n2

---

## 题目（中文翻译）

给定一个 **n × n** 矩阵，其中每一行（row）和每一列（column）都按升序排列，返回矩阵中第 **k** 小的元素。  
注意这里指的是按照排序后的顺序的第 **k** 小元素，而不是第 **k** 个不同的元素。  
要求你设计的算法的空间复杂度（memory complexity）必须优于 **O(n²)**。

**示例 1**  
**输入**: `matrix = [[1,5,9],[10,11,13],[12,13,15]], k = 8`  
**输出**: `13`  
**解释**: 矩阵中的所有元素按升序排列后为 `[1,5,9,10,11,12,13,13,15]`，第 8 小的数是 **13**。

**示例 2**  
**输入**: `matrix = [[-5]], k = 1`  
**输出**: `-5`

**约束条件**  
- `n == matrix.length == matrix[i].length`  
- `1 <= n <= 300`  
- `-10^9 <= matrix[i][j] <= 10^9`  
- 矩阵的所有行和列均保证按非递减顺序排序。  
- `1 <= k <= n²`

**进阶**  
（题目原文未提供进阶要求，可自行探索更高效的解法，如利用最小堆或二分查找等。）

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把矩阵里所有元素都取出来，放进一个普通的 Python 列表里，然后**排序**，最后取第 `k` 小的那个数。  

- **使用的数据结构**：  
  - **列表（list）**：相当于把所有数字装进一个大盒子里，方便一次性拿出来。  
  - **排序**：就像把盒子里的卡片按照数字大小排好队，排好序后第 `k` 张卡片就是答案。  

- **为什么正确**：  
  只要把所有元素都完整地收集起来并按从小到大排好序，第 `k` 个位置上的元素必然是第 `k` 小的元素（题目要求的是整体排序后的第 `k` 小，而不是去重后的）。  

- **时间/空间复杂度**：  
  - 取出全部元素需要遍历 `n × n` 个格子，时间是 `O(n²)`。  
  - 对 `n²` 个数进行排序，普通的 Python 排序（Timsort）时间复杂度是 `O(n² log n²)`，约等于 `O(n² log n)`。  
  - 额外空间要存放这些数，也就是 `O(n²)`（相当于再开了一个和原矩阵同样大小的盒子）。  

> 大白话解释：如果矩阵是 300×300，`n²` 就是 90 000。把 90 000 个数字全部搬出来排队，虽然能做到，但搬运和排队的工作量都不小，而且会占用和原矩阵同样多的内存。

#### 代码（Python）

```python
def kthSmallest_brute(matrix, k):
    """
    暴力解法：把所有元素放进列表，排序后直接取第 k 小。
    """
    n = len(matrix)
    flat = []                         # 用来装所有元素的“盒子”
    for i in range(n):
        for j in range(n):
            flat.append(matrix[i][j])   # 把每个格子的数搬进盒子
    flat.sort()                       # 把盒子里的数从小到大排好队
    return flat[k - 1]                # Python 索引从 0 开始，第 k 小是第 k-1 位
```

#### 复杂度  

- **时间复杂度**：`O(n² log n)`  
  - 取出元素 `O(n²)`，排序 `O(n² log n)`，两者相加仍是 `O(n² log n)`。  
  - 这里的 `log n` 实际上是 `log(n²)` 的常数因子，和 `log n` 差不多。

- **空间复杂度**：`O(n²)`  
  - 需要额外的列表来存放全部 `n²` 个数，和原矩阵大小相同。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **全部搬运 + 排序**，这两步都用了 `O(n²)` 的额外空间，而且排序的 `log` 因子让时间更慢。  
我们可以利用矩阵本身的**行列有序**的特性，省掉搬运和完整排序的过程。

**核心想法**：把矩阵看成一个“有序的二维链表”。  
- 每一行都是从左到右递增的。  
- 每一列也是从上到下递增的。  

这正好适合 **最小堆（优先队列）**：每次弹出当前未访问元素中最小的那个，然后把它右边或下边的下一个候选加入堆。  

具体步骤：

1. **初始化**：把每一行的第一个元素（即每列的最上面的数）放进最小堆。  
   - 堆里保存 `(value, row, col)`，`value` 用来比较大小，`row`、`col` 记录位置。  
   - 这一步只需要 `n` 个元素，空间 `O(n)`，远小于 `O(n²)`。

2. **弹出 k‑1 次**：每弹出一次堆顶，就是当前未弹出元素中的最小值。  
   - 弹出后，如果该元素所在的列还有更下边的数（`col + 1 < n`），就把**同一行的下一个元素**加入堆。  
   - 这样保证堆里始终保持“每行的下一个未被访问的最小数”。

3. 第 `k` 次弹出的值就是第 `k` 小的元素。

**为什么正确**：  
- 堆始终维护了所有**可能成为下一个最小值**的候选。因为每行都是递增的，行内已经弹出的元素左边的数一定更小，右边的数才可能更大。  
- 每次弹出堆顶，都是当前候选中最小的，等价于在整体有序序列中向前移动一步。弹出 `k‑1` 次后，堆顶就是第 `k` 小的。

**类比**：想象有 `n` 条已经排好队的队伍（每行），我们只让每条队伍的**前面**一个人站到“候选池”。每次从候选池里挑最矮的（最小值），然后把他所在队伍的下一个人送进池子。第 `k` 次挑出来的，就是第 `k` 矮的人。

#### 代码（Python）

```python
import heapq

def kthSmallest(matrix, k):
    """
    最小堆解法：利用每行递增的特性，仅维护 O(n) 的额外空间。
    """
    n = len(matrix)
    # 堆中存 (值, 行号, 列号)
    min_heap = []
    
    # 只把每行的第一个元素放进堆，初始化候选池
    for row in range(n):
        heapq.heappush(min_heap, (matrix[row][0], row, 0))
        # heapq.heappush 相当于把元素放进“最小堆”，自动维护堆序

    # 弹出 k-1 次，最后一次弹出的就是第 k 小
    for _ in range(k - 1):
        val, r, c = heapq.heappop(min_heap)   # 取出当前最小的数
        if c + 1 < n:                         # 该行还有未访问的元素
            # 把同一行的下一个元素加入堆
            heapq.heappush(min_heap, (matrix[r][c + 1], r, c + 1))

    # 第 k 小的数就在堆顶
    kth_val, _, _ = heapq.heappop(min_heap)
    return kth_val
```

#### 复杂度  

- **时间复杂度**：`O(k log n)`  
  - 初始化堆需要 `n` 次 `heappush`，每次 `log n`。  
  - 主循环弹出 `k‑1` 次，每次弹出和（可能）再插入一次，均是 `log n`。  
  - 所以整体是 `O(k log n)`。在最坏情况下 `k = n²`，时间上界是 `O(n² log n)`，但实际 `k` 往往远小于 `n²`，而且空间只用了 `O(n)`。

- **空间复杂度**：`O(n)`  
  - 堆里最多保存 `n` 个元素（每行最多一个候选），远小于题目要求的 “比 `O(n²)` 更好”。

---

## 心得  

- **核心技巧**：利用**最小堆**（优先队列）把“每行的下一个未访问元素”作为候选，逐步弹出最小值。  
- **适用的题型**：  
  1. 合并 k 条有序链表（LeetCode 23）  
  2. 找到无序数组中第 k 小的元素（使用堆）  
  3. “有序矩阵中第 K 小”系列（本题、LeetCode 378）  
- **一句话总结**：**“把每行的最前面装进最小堆，弹出 k‑1 次后堆顶即为答案”。**

---

## 反思  

- **第一反应**：直接把矩阵展平成列表再排序，想到最直接的暴力解。  
- **最容易踩的坑**：  
  - 忘记 **只放每行的第一个元素** 初始化堆，导致堆大小变成 `O(n²)`，失去空间优势。  
  - 边界条件：当 `k = 1` 时，直接返回堆顶；当 `k = n²` 时，需要遍历完整个矩阵，堆的大小仍保持 `O(n)`。  
  - 处理负数和重复元素时仍然适用，因为堆只比较数值本身。  
- **下次类似题的第一步**：**先想能否利用已有的有序结构**（行/列递增、链表有序等），再考虑用堆或双指针等“只保留局部候选” 的方法，避免全局搬运。