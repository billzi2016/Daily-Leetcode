# #1962. 移除石子使总数最小化 / Remove Stones to Minimize the Total

> 难度：中等 · 标签：Array、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/remove-stones-to-minimize-the-total/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array piles, where piles[i] represents the number of stones in the ith pile, and an integer k. You should apply the following operation exactly k times:
Notice that you can apply the operation on the same pile more than once.
Return the minimum possible total number of stones remaining after applying the k operations.
floor(x) is the largest integer that is smaller than or equal to x (i.e., rounds x down).

**Examples**

**Example 1:**

```
Input: piles = [5,4,9], k = 2
Output: 12
Explanation: Steps of a possible scenario are:
- Apply the operation on pile 2. The resulting piles are [5,4,5].
- Apply the operation on pile 0. The resulting piles are [3,4,5].
The total number of stones in [3,4,5] is 12.
```

**Example 2:**

```
Input: piles = [4,3,6,7], k = 3
Output: 12
Explanation: Steps of a possible scenario are:
- Apply the operation on pile 2. The resulting piles are [4,3,3,7].
- Apply the operation on pile 3. The resulting piles are [4,3,3,4].
- Apply the operation on pile 0. The resulting piles are [2,3,3,4].
The total number of stones in [2,3,3,4] is 12.
```

**Constraints**

- 1 <= piles.length <= 105
- 1 <= piles[i] <= 104
- 1 <= k <= 105

---

## 题目（中文翻译）

**题目描述**  
给定一个下标从 0 开始的整数数组 `piles`，其中 `piles[i]` 表示第 `i` 堆石子的数量，以及一个整数 `k`。你需要恰好执行 `k` 次以下操作：

- 选择任意一堆石子，将该堆的石子数替换为 `floor(piles[i] / 2)`（即对 `piles[i] / 2` 向下取整）。

注意，同一堆可以被多次选择并执行操作。

返回在执行完 `k` 次操作后，石子总数的最小可能值。

`floor(x)` 表示不大于 `x` 的最大整数（即向下取整）。

**示例**

*示例 1*  
输入：`piles = [5,4,9]`, `k = 2`  
输出：`12`  
解释：可能的操作步骤如下：
- 对第 2 堆执行操作，得到的堆为 `[5,4,5]`。
- 对第 0 堆执行操作，得到的堆为 `[3,4,5]`。  
此时石子总数为 `3 + 4 + 5 = 12`。

*示例 2*  
输入：`piles = [4,3,6,7]`, `k = 3`  
输出：`12`  
解释：可能的操作步骤如下：
- 对第 2 堆执行操作，得到的堆为 `[4,3,3,7]`。
- 对第 3 堆执行操作，得到的堆为 `[4,3,3,4]`。
- 对第 0 堆执行操作，得到的堆为 `[2,3,3,4]`。  
此时石子总数为 `2 + 3 + 3 + 4 = 12`。

**约束条件**
- `1 <= piles.length <= 10^5`
- `1 <= piles[i] <= 10^4`
- `1 <= k <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

题目让我们 **恰好** 做 `k` 次操作，每次可以任选一堆石子，把这堆石子 **减半并向上取整**（即 `ceil(x/2)`），等价于 **去掉** `floor(x/2)` 块石子。  
最直观的想法是：

1. 每次遍历整个数组，找到当前最大的那堆石子（因为把最大堆减半对总和的影响最大）。  
2. 把它替换成 `ceil(max/2)`，继续下一次操作。  

这里的“最大堆”可以类比为 **字典里查最大的单词**：我们每次都要把最大的那一个挑出来处理。  

这种做法一定能得到 **最小的总石子数**，因为每一步我们都把“当前最贵”的那堆石子减半，后面的步骤再也不会出现更大的堆可以再被减半。

#### 代码（Python）  

```python
import math
from typing import List

def minStoneSum_bruteforce(piles: List[int], k: int) -> int:
    """
    暴力实现：每次都遍历整个列表找最大值
    时间复杂度高，但思路最直接
    """
    for _ in range(k):
        # 找到当前最大的那堆（线性扫描）
        max_idx = 0
        for i in range(1, len(piles)):
            if piles[i] > piles[max_idx]:
                max_idx = i

        # 把它减半并向上取整
        # ceil(x/2) = (x + 1) // 2   // Python 整除
        piles[max_idx] = (piles[max_idx] + 1) // 2

    # 所有操作结束后，求总和
    return sum(piles)
```

#### 复杂度  

- **时间复杂度**：`O(k * n)`  
  - `k` 次操作，每次都要遍历 `n = len(piles)` 找最大值。  
  - 用大白话讲，就是如果 `k = 1000`、`n = 1000`，最坏要做 **100 万次比较**，会慢。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量（索引、计数器），不随输入规模增长。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次寻找最大堆的线性扫描**。如果我们能把“找最大堆”这一步改成 **对数时间**，整体就会快很多。  

Python 标准库提供了 **堆（Priority Queue）**，它是一棵满足“父节点 ≥ 子节点”（最大堆）或 “父节点 ≤ 子节点”（最小堆） 的二叉树。  
- 对 **最大堆**，`pop`（弹出）操作可以在 `O(log n)` 时间内得到当前最大的元素。  
- `push`（插入）同样是 `O(log n)`。

实现思路：

1. 把所有 `piles` 放进 **最大堆**。Python 的 `heapq` 只实现 **最小堆**，所以我们把每个数取负数（负数越小，实际数越大），相当于构造最大堆。  
2. 重复 `k` 次：  
   - `pop` 出堆顶（即当前最大堆），记为 `x`（记得把负号恢复）。  
   - 计算 `new = ceil(x / 2) = (x + 1) // 2`。  
   - 把 `-new` 再 `push` 回堆。  
3. 最后把堆里所有负数恢复正数并求和。

整个过程只用了 **堆的 `push/pop`**，每次操作都是 `O(log n)`，所以总体是 `O((n + k) log n)`。

#### 代码（Python）  

```python
import heapq
from typing import List

def minStoneSum(piles: List[int], k: int) -> int:
    """
    最优解：使用最大堆（借助 Python 的最小堆 + 负数技巧）
    时间复杂度 O((n + k) log n)，空间复杂度 O(n)
    """
    # 1. 把所有 piles 变成负数，构造最大堆
    max_heap = [-x for x in piles]      # 负数越小，实际数越大
    heapq.heapify(max_heap)             # O(n) 建堆

    # 2. 进行 k 次操作
    for _ in range(k):
        # 取出当前最大的堆（负数最小）
        largest = -heapq.heappop(max_heap)   # 恢复正数
        # 计算减半后向上取整的结果
        reduced = (largest + 1) // 2
        # 把新值再放回堆中（仍然用负数保存）
        heapq.heappush(max_heap, -reduced)

    # 3. 所有操作结束后，求总和（把负数恢复正数）
    total = -sum(max_heap)   # sum 里都是负数，取相反数即为正和
    return total
```

#### 复杂度  

- **时间复杂度**：`O((n + k) log n)`  
  - 建堆一次 `O(n)`，随后 `k` 次 `pop`+`push`，每次 `O(log n)`。  
  - 与暴力解的 `O(k·n)` 相比，尤其当 `k`、`n` 都很大（如 10⁵）时，速度提升数百倍。  
- **空间复杂度**：`O(n)`  
  - 堆里保存了 `n` 个负数，需要与输入规模相同的额外空间。

---

## 心得  

- **核心技巧**：**贪心 + 最大堆**。每一步都选当前最大的堆进行减半，这是全局最优的贪心策略。  
- **适用的题型**：  
  1. “把最大元素减半/减去一定比例” 类的最小化问题（如 LeetCode 1962）。  
  2. “每次挑选最大/最小元素进行处理” 的调度或资源分配问题（如 “把数组中最大数减半 k 次”）。  
  3. “需要频繁获取当前最大值/最小值”的动态数据流问题（如 合并最小/最大文件大小）。  
- **一句话总结**：**每一步都把最大堆减半，利用堆让“找最大”变得快如闪电**。

---

## 反思  

- **第一反应**：看到“每次都要对最大堆做相同的操作”，立刻想到 **贪心**——把最大值先处理。  
- **最容易踩的坑**：  
  - **整数除法**：`ceil(x/2)` 必须写成 `(x + 1) // 2`，否则会得到向下取整的错误结果。  
  - **堆的方向**：Python 只提供最小堆，需要用负数技巧模拟最大堆，忘记取负会导致选到最小堆。  
  - **边界条件**：`k` 可能大于 `n`，但堆始终保持 `n` 个元素，仍然可以继续弹出/插入。  
- **下次遇到同类题**：第一步先 **判断是否可以用贪心**（是否每一步的局部最优能保证全局最优），随后 **寻找能快速获取局部最优的结构**（堆、单调队列、前缀和等）。