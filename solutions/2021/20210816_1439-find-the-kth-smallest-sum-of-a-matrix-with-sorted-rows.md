# #1439. 矩阵行已排序时的第 K 小和 / Find the Kth Smallest Sum of a Matrix With Sorted Rows

> 难度：困难 · 标签：Array、Binary Search、Heap (Priority Queue)、Matrix · [LeetCode 链接](https://leetcode.com/problems/find-the-kth-smallest-sum-of-a-matrix-with-sorted-rows/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix mat that has its rows sorted in non-decreasing order and an integer k.
You are allowed to choose exactly one element from each row to form an array.
Return the kth smallest array sum among all possible arrays.

**Examples**

**Example 1:**

```
Input: mat = [[1,3,11],[2,4,6]], k = 5
Output: 7
Explanation: Choosing one element from each row, the first k smallest sum are:
[1,2], [1,4], [3,2], [3,4], [1,6]. Where the 5th sum is 7.
```

**Example 2:**

```
Input: mat = [[1,3,11],[2,4,6]], k = 9
Output: 17
```

**Example 3:**

```
Input: mat = [[1,10,10],[1,4,5],[2,3,6]], k = 7
Output: 9
Explanation: Choosing one element from each row, the first k smallest sum are:
[1,1,2], [1,1,3], [1,4,2], [1,4,3], [1,1,6], [1,5,2], [1,5,3]. Where the 7th sum is 9.
```

**Constraints**

- m == mat.length
- n == mat.length[i]
- 1 <= m, n <= 40
- 1 <= mat[i][j] <= 5000
- 1 <= k <= min(200, nm)
- mat[i] is a non-decreasing array.

---

## 题目（中文翻译）

给定一个 `m × n` 矩阵 `mat`，其每行均按非递减顺序排序，并给定一个整数 `k`。  
你需要从每一行恰好选取一个元素，组成一个数组（array）。  
返回所有可能数组的第 `k` 小的数组和（array sum）。

**示例 1**  
输入: `mat = [[1,3,11],[2,4,6]], k = 5`  
输出: `7`  
说明: 从每行各选一个元素，前 `k` 小的和依次为:  
`[1,2] (sum=3)`, `[1,4] (5)`, `[3,2] (5)`, `[3,4] (7)`, `[1,6] (7)`。第 5 小的和为 `7`。

**示例 2**  
输入: `mat = [[1,3,11],[2,4,6]], k = 9`  
输出: `17`

**示例 3**  
输入: `mat = [[1,10,10],[1,4,5],[2,3,6]], k = 7`  
输出: `9`  
说明: 从每行各选一个元素，前 `k` 小的和依次为:  
`[1,1,2] (4)`, `[1,1,3] (5)`, `[1,4,2] (7)`, `[1,4,3] (8)`, `[1,1,6] (8)`, `[1,5,2] (8)`, `[1,5,3] (9)`。第 7 小的和为 `9`。

**约束条件**  
- `m == mat.length`  
- `n == mat[i].length`  
- `1 ≤ m, n ≤ 40`  
- `1 ≤ mat[i][j] ≤ 5000`  
- `1 ≤ k ≤ min(200, m·n)`  
- `mat[i]` 为非递减数组。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一行的每个元素都拿出来尝试**，把所有可能的「选一行一个元素」的组合列举完整，然后把得到的总和排个序，直接取第 k 小的那个。  

- **数据结构**：我们可以把每一种选法看成一个长度为 `m` 的数组（`m` 为行数），把所有数组的和放进一个普通的 Python `list`，最后 `list.sort()`。  
- **生活化类比**：把每一行想象成一副牌，牌面是递增排好的数字。暴力解就是把每副牌的每张牌都抽出来，尝试所有可能的「一副牌抽一张」的组合，就像把所有可能的手牌都摆在桌面上，然后把手牌的点数从小到大排好序。  
- **为什么正确**：因为我们把 **所有** 合法的组合都列举出来了，排好序后第 k 小的必然是答案。  

> **注意**：这一步在理论上是对的，但实际会因为组合数量爆炸而不可行。  
> 对于 `m` 行、每行 `n` 个元素，组合数是 `n^m`（指数级），即使 `m = n = 10` 也已经是 `10^10` 种可能，根本跑不完。

#### 代码（Python）

```python
import itertools
from typing import List

def kth_smallest_brute(mat: List[List[int]], k: int) -> int:
    """
    暴力枚举所有组合，返回第 k 小的和
    仅作思路展示，实际会超时/内存爆炸
    """
    # itertools.product 会把每行的元素做笛卡尔积，产生所有可能的选法
    all_sums = []
    for combo in itertools.product(*mat):      # combo 是一个长度为 m 的元组
        s = sum(combo)                         # 计算该组合的总和
        all_sums.append(s)

    all_sums.sort()                            # 从小到大排好序
    return all_sums[k - 1]                     # 第 k 小（k 从 1 开始计数）
```

#### 复杂度  

- **时间复杂度**：`O(n^m * m)`  
  - `n^m` 是组合的总数（指数级），每个组合要遍历 `m` 行求和。  
  - 用大白话说，就是「如果你把每行的每个数都当成一个选择，所有选择的组合数会像滚雪球一样越来越大，最后根本等不完」。
- **空间复杂度**：`O(n^m)` 用来存所有和的列表。  

显然，这种「最直接」的办法只能帮助我们理清问题本身，真正要解题必须做 **优化**。

---  

### 2. 最优解  

#### 思路  

暴力解慢的根本原因是 **一次性把所有组合都列出来**，而题目只要求第 k 小的和，`k ≤ 200`，远远小于所有组合的数量。我们可以 **只关注最小的那几千个**，把搜索范围大幅缩小。  

下面的思路分两层：

1. **把两行合并成 “k 小和”**  
   - 已知两行都是递增的（题目保证每行已排序），我们可以利用 **最小堆（priority queue）** 找出这两行所有可能和中最小的 `k` 个。  
   - 类比：把两副排好序的牌放在一起，每次从堆里取出当前最小的点数，然后把「把较大那张牌换成下一张」的新的组合放回堆中。这样只会产生 `k` 次弹出，堆里最多保存 `k` 条记录，时间是 `O(k log k)`。

2. **把多行逐步合并**  
   - 先把第 1 行当成「当前的 k 小和集合」——其实就是第 1 行本身（因为只选一行，和就是元素本身）。  
   - 然后把第 2 行和「当前集合」合并，得到新的「前 k 小和」集合。  
   - 接着把第 3 行再和这个集合合并，如此循环，直到所有 `m` 行都被处理完。  
   - 每一次合并的代价都是 `O(k log k)`，总共 `m‑1` 次合并，整体时间 `O(m·k·log k)`。  
   - 因为 `k ≤ 200`，`m ≤ 40`，这在实际运行中非常快。

> **核心数据结构：最小堆（priority queue）**  
> - 堆就像一个「随时能拿出最小元素」的盒子。Python 的 `heapq` 实现了最小堆。  
> - 每个堆元素我们记录两件事：**当前的和**、**在当前行里用了哪个下标**。这样弹出后可以“向右走一步”生成新的候选和。

#### 关键细节  

- **只保留 k 条记录**：合并时我们只需要前 `k` 小的和，所以在产生新候选时，一旦堆里已经有 `k` 条且新产生的和大于堆顶（第 k 小），可以直接丢弃。  
- **去重**：不同的路径可能产生相同的和，为了防止重复弹出，需要用一个 `visited` 集合记住已经放进堆的 `(row_index, col_index)`（或者更一般的 “状态”）组合。  
- **初始堆**：合并第一行和第二行时，先把 `first_row[i] + second_row[0]`（即第二行最左边的元素）全部放进去，随后每次弹出 `(i, j)` 时把 `(i, j+1)` 加入堆。

#### 代码（Python）

```python
import heapq
from typing import List, Tuple, Set

def kth_smallest(mat: List[List[int]], k: int) -> int:
    """
    使用逐行合并 + 最小堆，求第 k 小的数组和
    复杂度：O(m * k * log k) 时间，O(k) 空间
    """
    # ---------- 第一步：把第一行视为当前的 “k 小和集合” ----------
    cur = mat[0][:k]                 # 只保留前 k 小的，因为后面的肯定更大
    # ---------- 逐行合并 ----------
    for row in mat[1:]:
        # 对当前行和已有的 cur 合并，得到新的前 k 小和
        cur = merge_two_rows(cur, row, k)
    # 最后 cur 已经是所有行的前 k 小和，直接返回第 k 小（下标 k-1）
    return cur[k - 1]

def merge_two_rows(a: List[int], b: List[int], k: int) -> List[int]:
    """
    已知 a 已经是递增的前 k 小和，b 是递增的行，
    求 a 与 b 所有可能和的前 k 小（仍然递增返回）。
    """
    heap: List[Tuple[int, int, int]] = []   # (和, a_idx, b_idx)
    visited: Set[Tuple[int, int]] = set()   # 防止重复入堆

    # 初始把 a 中每个元素和 b[0] 配对，放进堆
    for i, av in enumerate(a):
        s = av + b[0]
        heapq.heappush(heap, (s, i, 0))
        visited.add((i, 0))

    result: List[int] = []          # 保存合并后的前 k 小和
    while heap and len(result) < k:
        s, i, j = heapq.heappop(heap)   # 取当前最小的和
        result.append(s)

        # 把同一个 a[i] 与 b 的下一个元素配对（如果还有的话）放入堆
        if j + 1 < len(b):
            nxt = (i, j + 1)
            if nxt not in visited:      # 防止同一状态多次入堆
                heapq.heappush(heap, (a[i] + b[j + 1], i, j + 1))
                visited.add(nxt)

    return result
```

**代码说明（每行中文注释已写在代码里）**  

- `kth_smallest`：主函数。先把第一行的前 `k` 小元素直接取出来（因为后面的已经不可能进入前 `k`），随后对每一后续行调用 `merge_two_rows`。  
- `merge_two_rows`：核心合并函数。  
  - 堆里保存三元组 `(sum, i, j)`，表示 `a[i] + b[j]` 的和以及对应的下标。  
  - 初始把所有 `a[i] + b[0]` 放进堆，保证堆的大小不超过 `len(a)`（≤ k）。  
  - 每弹出一次最小和 `s`，就把 **同一个 `a[i]`** 与 **下一个 `b` 元素** 配对 (`b[j+1]`) 放进堆，这相当于「把指针在第二行向右移动一步」。  
  - 用 `visited` 集合避免把同一对 `(i, j)` 多次放进堆，防止重复弹出相同的和。  
  - 循环直到收集到 `k` 个最小和或堆耗尽（理论上不会耗尽，因为 `k ≤ n·m`）。

#### 复杂度  

- **时间复杂度**：`O(m * k * log k)`  
  - 每一行合并都要维护一个大小至多为 `k` 的堆，弹出 `k` 次，每次弹出/插入的代价是 `log k`。  
  - 用大白话说：我们只在「最有希望」的 `k` 条路上跑步，每跑一步（弹出）都只需要把「最近的几条路」重新排个序，整个过程只要几千次操作，几乎瞬间完成。  
  - 与暴力解的 `O(n^m)`（指数级）相比，快了 **指数级** 的差距。

- **空间复杂度**：`O(k)`  
  - 主要是堆和 `visited` 集合的大小，都不会超过 `k`（因为我们只会把每行的前 `k` 条候选放进去）。  
  - 用大白话说：我们只需要记住「前 k 小的和」以及它们对应的状态，不需要保存所有可能的组合。

---

## 心得  

- **核心技巧**：**逐行合并 + 最小堆（k-way 合并）**。  
  - 把每一行看成一条递增的「数列」，把多条数列的前 `k` 小和逐步合并，就能在 `O(m·k·log k)` 时间内得到答案。  
- **适用的题型**  
  1. **两个已排序数组的前 k 小和**（LeetCode 373. Find K Pairs with Smallest Sums）。  
  2. **多行/多列的前 k 小元素**（如 “Kth Smallest Element in a Sorted Matrix”）。  
  3. **合并多路有序流的前 k 条记录**（常见于外部排序、流式处理）。  
- **一句话总结解题钥匙**：**只保留最小的 k 条候选，用堆把“向右走一步”的新候选快速加入**。

---

## 反思  

- **第一反应**：看到“每行已排序”，立刻想到“二分查找”或“堆”。但直接二分计数实现比较复杂，先想到的其实是 **把行两两合并**，因为合并两行的最小和可以用堆解决。  
- **最容易踩的坑**  
  1. **去重**：不同路径可能产生相同的 `(i, j)`，若不记录 `visited`，堆里会出现重复元素，导致结果里出现相同的和，最终第 k 小可能不对。  
  2. **只取前 k 小**：在每一步合并时一定要截断到 `k`，否则堆会膨胀到 `k·n`，导致时间和空间失控。  
  3. **边界条件**：`k` 可能比某一步的组合数还小，需要在 `while` 循环里判断 `len(result) < k`，防止弹出多余的元素。  
- **下次遇到同类题**：第一步先思考 **“只需要前 k 条”**，把搜索空间限制在最小的几条上；第二步考虑 **“把问题逐层拆分”，每层只保留前 k 条，使用最小堆进行合并**。这样往往能把指数级的暴力搜索压缩到线性（或 `k·log k`）的规模。