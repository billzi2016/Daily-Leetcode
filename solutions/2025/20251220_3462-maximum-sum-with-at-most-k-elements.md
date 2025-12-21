# #3462. 最多 K 个元素的最大和 / Maximum Sum With at Most K Elements

> 难度：中等 · 标签：Array、Greedy、Sorting、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-with-at-most-k-elements/)

---

## 题目（英文原版）

**Description**

You are given a 2D integer matrix grid of size n x m, an integer array limits of length n, and an integer k. The task is to find the maximum sum of at most k elements from the matrix grid such that:
Return the maximum sum.

**Examples**

**Example 1:**

```
Input: grid = [[1,2],[3,4]], limits = [1,2], k = 2
Output: 7
Explanation:
```

**Example 2:**

```
Input: grid = [[5,3,7],[8,2,6]], limits = [2,2], k = 3
Output: 21
Explanation:
```

**Constraints**

- n == grid.length == limits.length
- m == grid[i].length
- 1 <= n, m <= 500
- 0 <= grid[i][j] <= 105
- 0 <= limits[i] <= m
- 0 <= k <= min(n * m, sum(limits))

---

## 题目（中文翻译）

给定一个大小为 `n × m` 的二维整数矩阵 `grid`、长度为 `n` 的整数数组 `limits`，以及一个整数 `k`。要求从矩阵 `grid` 中选取至多 `k` 个元素，使得满足题目条件（具体条件在原题中省略），返回能够得到的最大和。

**示例 1**  
**输入**: `grid = [[1,2],[3,4]]`, `limits = [1,2]`, `k = 2`  
**输出**: `7`  
**解释**:  

**示例 2**  
**输入**: `grid = [[5,3,7],[8,2,6]]`, `limits = [2,2]`, `k = 3`  
**输出**: `21`  
**解释**:  

**约束条件**  
- `n == grid.length == limits.length`  
- `m == grid[i].length`  
- `1 <= n, m <= 500`  
- `0 <= grid[i][j] <= 10^5`  
- `0 <= limits[i] <= m`  
- `0 <= k <= min(n * m, sum(limits))`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有合法的取法**，然后把每种取法的元素求和，取最大的那个。  
具体可以这样做：

1. 对第 `i` 行，我们可以取 `0 … limits[i]` 个元素。  
2. 对每一行的取法进行组合（类似“从每一行挑几个数”），把所有行的选择拼在一起，就得到一种**完整的取法**。  
3. 检查这次取法的总元素个数是否 ≤ k，若满足就把对应的数相加，更新最大和。

> **类比**：把每一行想象成一盒子，盒子里有若干颗糖果（数字），盒子上写着“本盒最多只能拿 `limits[i]` 颗”。暴力解就是把每个盒子里可能拿的糖果数全都试一遍，看看哪种组合的糖果总重量最大。

**为什么正确**  
因为我们把**所有**可能的合法取法都遍历了一遍，最大和一定会出现在这些遍历的结果里。

**时间/空间复杂度**  
- 对第 `i` 行有 `limits[i] + 1` 种取法，所有行的组合数是  
  \[
  \prod_{i=0}^{n-1} (limits[i] + 1)
  \]
  这在最坏情况下相当于 `O( (m+1)^n )`，指数级别，几乎不可能在 1 秒内跑完（即使 `n,m ≤ 5` 也会爆炸）。  
- 递归过程中需要保存当前已经选的元素，最多占用 `O(k)` 的额外空间。

> **大白话**：`O( (m+1)^n )` 就好比把 10 层楼的每层都装 10 种不同颜色的砖块，去尝试所有可能的配色——根本不可能在有限时间里完成。

#### 代码（Python）

```python
from typing import List

def brute_max_sum(grid: List[List[int]], limits: List[int], k: int) -> int:
    n, m = len(grid), len(grid[0])
    best = 0                                 # 保存全局最大和

    # 递归遍历每一行的取法
    def dfs(row: int, taken: int, cur_sum: int):
        nonlocal best
        # 剪枝：已经超过 k，就不必继续
        if taken > k:
            return
        # 到最后一行，更新答案
        if row == n:
            best = max(best, cur_sum)
            return

        # 先把当前行所有元素从大到小排好，方便后面选前 few 个
        sorted_row = sorted(grid[row], reverse=True)

        # 这行可以取 0~limits[row] 个元素
        for cnt in range(limits[row] + 1):
            # 计算取前 cnt 个元素的和
            add = sum(sorted_row[:cnt])
            dfs(row + 1, taken + cnt, cur_sum + add)

    dfs(0, 0, 0)
    return best
```

> 关键行解释  
> - `sorted_row = sorted(grid[row], reverse=True)`：把当前行从大到小排，就像把糖果按重量从重到轻排好，方便取前几颗。  
> - `for cnt in range(limits[row] + 1)`: 试遍所有合法的取数目（0、1、…、limits[i]）。  
> - `if taken > k: return`：一旦已经超过总上限 k，就不必继续递归（剪枝），否则递归树会更大。

#### 复杂度

- **时间复杂度**：`O( ∏ (limits[i] + 1) )`，指数级别，实际不可接受。  
- **空间复杂度**：`O(k + n)`，递归栈深度为 `n`，额外保存当前已取元素个数 `taken`（至多 `k`）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正耗时的地方在于“遍历所有组合”**。  
观察题目可以发现：

1. **每行只关心最大的 `limits[i]` 个数**，因为如果我们要从第 `i` 行取 `cnt ≤ limits[i]` 个元素，显然会选最大的 `cnt` 个，而不是随意挑。  
2. 把每行的前 `limits[i]` 大的数挑出来后，**全局只需要再挑出最大的 `k` 个数**（因为总体上我们只能取 `k` 个元素）。  
3. 这一步可以通过 **排序** 或 **最大堆（max‑heap）** 完成。

因此，最优解的整体流程是：

1. **对每一行**  
   - 把该行从大到小排序（`O(m log m)`）  
   - 取前 `limits[i]` 个，放进一个统一的“大桶” `candidates`。  
2. **从 `candidates` 中取最大的 `k` 个**  
   - 方法一：把 `candidates` 再整体排序，取前 `k`（`O(N log N)`，`N = sum(limits)`）。  
   - 方法二（更省空间/时间）：把所有候选数放进 **最大堆**，弹出 `k` 次得到最大的 `k` 个（`O(N + k log N)`）。  

> **类比**：先把每盒子里最贵的糖果挑出来装进一个大盘子，然后从大盘子里挑出最贵的 `k` 颗。挑最贵的过程可以用“排队（排序）”或“抢先（堆）”来实现。

下面给出 **使用最大堆** 的实现，因为它在 `k` 远小于 `N` 时更高效。

#### 代码（Python）

```python
import heapq
from typing import List

def max_sum_with_limits(grid: List[List[int]], limits: List[int], k: int) -> int:
    """
    返回在每行最多取 limits[i] 个、整体最多取 k 个元素时的最大可能和。
    思路：
    1. 每行降序排序，取前 limits[i] 个放进候选列表。
    2. 用最大堆一次弹出 k 次，累计和即为答案。
    """
    # 1️⃣ 把每行的前 limits[i] 大的数收集起来
    candidates = []                      # 所有行的候选数字
    for row, lim in zip(grid, limits):
        if lim == 0:          # 该行不能取任何数，直接跳过
            continue
        # 降序排列后只取前 lim 个
        row_sorted = sorted(row, reverse=True)
        candidates.extend(row_sorted[:lim])

    # 2️⃣ 用最大堆挑出最大的 k 个
    # Python 的 heapq 只实现最小堆，先把数字取负得到等价的最大堆
    max_heap = [-x for x in candidates]
    heapq.heapify(max_heap)              # O(N) 建堆

    ans = 0
    for _ in range(min(k, len(max_heap))):   # 防止 k 大于候选数总数
        largest = -heapq.heappop(max_heap)   # 弹出当前最大的数
        ans += largest

    return ans
```

> 关键行解释  
> - `row_sorted = sorted(row, reverse=True)`：把当前行从大到小排好，就像把糖果从重到轻排好。  
> - `candidates.extend(row_sorted[:lim])`：只把前 `lim` 颗最重的糖果放进大盘子。  
> - `max_heap = [-x for x in candidates]` + `heapq.heapify`：把普通列表变成最大堆（取负后使用最小堆实现）。  
> - `for _ in range(min(k, len(max_heap)))`：如果 `k` 超过了候选数的总量，只能弹出已有的全部。  

如果不想使用堆，也可以直接把 `candidates` 排序后取前 `k`：

```python
candidates.sort(reverse=True)
return sum(candidates[:k])
```

#### 复杂度

- **时间复杂度**  
  - 对每行排序：`O(n * m log m)`（`n ≤ 500, m ≤ 500`，在极限情况下约 `500 * 500 log 500`，仍然可接受）。  
  - 收集候选数：`O(N)`，其中 `N = sum(limits) ≤ n*m`。  
  - 建堆 `O(N)`，弹出 `k` 次 `O(k log N)`。  
  - **总计**：`O(n * m log m + N + k log N)`。  
    - 当 `k` 远小于 `N` 时，堆的优势尤为明显。  
- **空间复杂度**  
  - 候选数组 `candidates` 长度为 `N`，额外的堆也占 `O(N)`。  
  - 只要 `N ≤ n*m ≤ 250,000`，在普通机器上也很轻松。  

> 与暴力解对比：暴力解的时间是指数级的，最优解把问题压缩到 **排序 + 堆** 两步，时间从天文级降到了 **几百万次基本运算**，在 1 秒内轻松跑完。

---

## 心得

- **核心技巧**：先在每行内部**局部取最大**，再在全局**取前 k 大**。这是一种“**分治 + 合并**”的思路：先把每个子问题（每行）化简到最有价值的若干候选，再统一处理。
- **适用场景**  
  1. “每组最多取 X 个，总体最多取 Y 个” 类似限制（例如：**分组背包**的简化版）。  
  2. “从多个有序列表中取前 K 大元素”——如**合并 k 条有序链表的前 K 大**。  
  3. “每个类别只能选有限个，整体预算有限”——比如**商品促销的选品**问题。
- **一句话总结**：**先局部筛选，再全局挑选**，配合排序或堆即可高效求解。

---

## 反思

- **第一反应**：看到“每行有上限，整体有上限”，自然想到**枚举每行的取数**，于是想到了递归暴力。  
- **最容易踩的坑**  
  - 忽视 `limits[i]` 可能为 `0`，导致不必要的排序或切片。  
  - `k` 可能大于所有候选数的总和，需要在取前 `k` 时做 `min(k, len(candidates))` 防止弹空堆。  
  - 题目要求“最多 k 个”，而不是恰好 k 个，记得在 `k` 超出候选数时直接返回所有候选数的和。  
- **下次遇到同类题**：第一步想到 **“先在每个子集合中取前 limit 个最大值”**，再用 **排序/堆** 把全局的前 K 大挑出来。这样就能立刻把指数级的搜索压缩到对数/线性级别。