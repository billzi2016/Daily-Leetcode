# #2948. **通过交换元素使数组字典序最小** / Make Lexicographically Smallest Array by Swapping Elements

> 难度：中等 · 标签：Array、Union Find、Sorting · [LeetCode 链接](https://leetcode.com/problems/make-lexicographically-smallest-array-by-swapping-elements/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array of positive integers nums and a positive integer limit.
In one operation, you can choose any two indices i and j and swap nums[i] and nums[j] if |nums[i] - nums[j]| <= limit.
Return the lexicographically smallest array that can be obtained by performing the operation any number of times.
An array a is lexicographically smaller than an array b if in the first position where a and b differ, array a has an element that is less than the corresponding element in b. For example, the array [2,10,3] is lexicographically smaller than the array [10,2,3] because they differ at index 0 and 2 < 10.

**Examples**

**Example 1:**

```
Input: nums = [1,5,3,9,8], limit = 2
Output: [1,3,5,8,9]
Explanation: Apply the operation 2 times:
- Swap nums[1] with nums[2]. The array becomes [1,3,5,9,8]
- Swap nums[3] with nums[4]. The array becomes [1,3,5,8,9]
We cannot obtain a lexicographically smaller array by applying any more operations.
Note that it may be possible to get the same result by doing different operations.
```

**Example 2:**

```
Input: nums = [1,7,6,18,2,1], limit = 3
Output: [1,6,7,18,1,2]
Explanation: Apply the operation 3 times:
- Swap nums[1] with nums[2]. The array becomes [1,6,7,18,2,1]
- Swap nums[0] with nums[4]. The array becomes [2,6,7,18,1,1]
- Swap nums[0] with nums[5]. The array becomes [1,6,7,18,1,2]
We cannot obtain a lexicographically smaller array by applying any more operations.
```

**Example 3:**

```
Input: nums = [1,7,28,19,10], limit = 3
Output: [1,7,28,19,10]
Explanation: [1,7,28,19,10] is the lexicographically smallest array we can obtain because we cannot apply the operation on any two indices.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 1 <= limit <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的正整数数组 `nums` 和一个正整数 `limit`。  
一次操作中，你可以选择任意两个下标 `i` 和 `j`，如果满足 `|nums[i] - nums[j]| <= limit`，则交换 `nums[i] 和 nums[j]`。  
你可以执行任意次此操作，返回能够得到的字典序最小（lexicographically smallest）的数组。

如果在数组 `a` 与数组 `b` 第一个不同的位置上，`a` 的元素小于 `b` 的对应元素，则称 `a` 的字典序小于 `b`。例如数组 `[2,10,3]` 的字典序小于 `[10,2,3]`，因为它们在下标 0 处不同且 `2 < 10`。

---

### 示例

**示例 1**  
> **输入**: `nums = [1,5,3,9,8]`, `limit = 2`  
> **输出**: `[1,3,5,8,9]`  
> **解释**: 进行两次操作  
> - 交换 `nums[1]` 与 `nums[2]`，数组变为 `[1,3,5,9,8]`  
> - 交换 `nums[3]` 与 `nums[4]`，数组变为 `[1,3,5,8,9]`  
> 此后再进行任何合法交换都不能得到更小的字典序。  
> 注意，可能存在其他操作序列得到相同结果。

**示例 2**  
> **输入**: `nums = [1,7,6,18,2,1]`, `limit = 3`  
> **输出**: `[1,6,7,18,1,2]`  
> **解释**: 进行三次操作  
> - 交换 `nums[1]` 与 `nums[2]`，数组变为 `[1,6,7,18,2,1]`  
> - 交换 `nums[0]` 与 `nums[4]`，数组变为 `[2,6,7,18,1,1]`  
> - 交换 `nums[0]` 与 `nums[5]`，数组变为 `[1,6,7,18,1,2]`  
> 再做任何合法交换都无法得到更小的字典序。

**示例 3**  
> **输入**: `nums = [1,7,28,19,10]`, `limit = 3`  
> **输出**: `[1,7,28,19,10]`  
> **解释**: 由于任意两下标之间的差值均大于 `limit`，无法执行交换操作，原数组已是字典序最小。

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `1 <= limit <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每一次都把能够交换的两个人找出来，尝试所有可能的交换**，然后看能否得到更小的字典序。  
可以把数组想象成一排小朋友，只有身高差（即数值差）不超过 `limit` 的两个人才允许互相换位置。  

具体做法：

1. 从左到右遍历所有下标 `i`。  
2. 对每个 `i` 再遍历一次所有下标 `j>i`，如果 `|nums[i]-nums[j]| ≤ limit` 就把它们换一下。  
3. 换完以后继续从头检查，直到一次遍历都没有任何可以交换的地方——这时我们认为已经得到“最小”的数组了。

**为什么这个方法是正确的？**  
只要我们把所有合法的交换都尝试过，最终的状态就不再存在可以让字典序更小的交换了。因为字典序的比较是从左到右的，一旦左边的数已经是它所在连通块里最小的，后面的交换就不可能再影响更前面的位置。

**时间/空间复杂度**  
- 外层遍历 `n` 次，内层遍历最坏也要 `n` 次，交换检查是 `O(1)`，所以总体是 **`O(n²)`**。  
  大白话：如果数组有 10 000 个元素，暴力解大概要跑 10 000 × 10 000 = 1 亿次比较，明显太慢。  
- 只用到原数组本身和几个临时变量，**`O(1)`** 额外空间。

#### 代码（Python）

```python
def smallestArray_bruteforce(nums, limit):
    n = len(nums)
    changed = True                     # 是否在本轮出现了交换
    while changed:                     # 只要还能交换就一直循环
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                if abs(nums[i] - nums[j]) <= limit:
                    # 只在左边的数比右边的大时才换，才可能让字典序更小
                    if nums[i] > nums[j]:
                        nums[i], nums[j] = nums[j], nums[i]
                        changed = True
        # 若一次遍历都没有换位，changed 仍为 False，循环结束
    return nums
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历所有下标对。  
  对于 `n = 10⁵`（题目上限），这已经不可接受。
- **空间复杂度**：`O(1)` —— 只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历所有下标对**。实际上，如果两个元素可以直接或间接交换，它们就属于同一个**连通分量**（connected component），在同一个分量里任意两个位置都是可以相互换位的。  
我们只需要把每个连通分量内部的数**排序后重新放回原来的位置**，就能得到字典序最小的数组。

> **类比**：把数组的每个元素看成城市，若两座城市之间的高度差 ≤ `limit`，就修一条道路。只要城市之间有路（直接或间接），我们就可以随意调度车辆（元素）在这些城市之间搬来搬去。于是每个“连通的城市群”内部的车辆排成最小的顺序即可。

**如何快速得到连通分量？**  
- 任意两元素之间是否有边，只和它们的数值差有关，而不和下标关系。  
- 把数组 **按数值从小到大** 排序，同时记录原始下标。  
- 在排好序的序列里，只要相邻两个数的差 ≤ `limit`，它们必然相连（因为更远的数差只会更大），于是我们可以把它们**并入同一个集合**。  
- 这正好可以用 **并查集（Disjoint Set Union, DSU）** 实现：遍历排好序的数组，若 `sorted[i].value - sorted[i-1].value ≤ limit` 就 `union(i, i-1)`。

得到所有并查集的根之后，每个根对应一个连通分量。对每个分量：

1. 收集该分量所有**原始下标**和**对应的数值**。  
2. 把下标升序排列（因为我们要把最小的数放到最左边的下标），把数值也升序排列。  
3. 按顺序把排好序的数值写回对应的下标。

这样，左侧的下标必然拿到它所在连通块里最小的数，字典序自然最小。

**关键数据结构解释**  

- **并查集（Union‑Find）**：想象成一个“家族树”。每个元素最开始自己是一个家族（根指向自己），`find(x)` 能找到它的家族长（根），`union(a,b)` 把两个家族合并成一个。路径压缩让 `find` 极快（几乎是 O(1)），所以整体是线性时间。  
- **排序**：Python 的 `sorted` 使用 Timsort，时间复杂度 `O(n log n)`，足够快。

#### 代码（Python）

```python
from typing import List

class DSU:
    """并查集（Disjoint Set Union）"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点最初的父亲是自己
        self.rank = [0] * n            # 用于按秩合并，保持树的高度低

    def find(self, x: int) -> int:
        # 路径压缩：把查找路径上的所有节点直接挂到根上
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return                     # 已经在同一个集合
        # 按秩合并：高度低的挂到高度高的下面
        if self.rank[ra] < self.rank[rb]:
            self.parent[ra] = rb
        elif self.rank[ra] > self.rank[rb]:
            self.parent[rb] = ra
        else:
            self.parent[rb] = ra
            self.rank[ra] += 1

def smallestArray(nums: List[int], limit: int) -> List[int]:
    n = len(nums)
    # 1️⃣ 把数值和原下标一起保存，随后按数值排序
    indexed = [(val, idx) for idx, val in enumerate(nums)]
    indexed.sort(key=lambda x: x[0])          # 按数值升序

    dsu = DSU(n)

    # 2️⃣ 只看相邻的排好序的数，若差 ≤ limit 则合并它们所在的下标
    for i in range(1, n):
        if indexed[i][0] - indexed[i-1][0] <= limit:
            # 合并的是“原下标”，因为 DSU 的元素是位置而不是数值
            dsu.union(indexed[i][1], indexed[i-1][1])

    # 3️⃣ 收集每个连通分量的下标和对应的数值
    comp_to_indices = {}   # root -> [original indices]
    comp_to_values  = {}   # root -> [values]
    for idx, val in enumerate(nums):
        root = dsu.find(idx)
        comp_to_indices.setdefault(root, []).append(idx)
        comp_to_values.setdefault(root, []).append(val)

    # 4️⃣ 对每个分量内部分别排序，下标升序、数值升序，然后重新填回数组
    res = [0] * n
    for root in comp_to_indices:
        indices = comp_to_indices[root]
        values  = comp_to_values[root]

        indices.sort()          # 左边的下标先放最小的数
        values.sort()           # 该分量内部的数值从小到大

        for i, v in zip(indices, values):
            res[i] = v

    return res
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`（支配整体）  
  - DSU 合并遍历一次 `O(n α(n))`（α 为 Ackermann 函数的逆，几乎是常数）  
  - 再次遍历收集并排序每个分量的数值，总和仍不超过 `O(n log n)`。  
  与暴力的 `O(n²)` 相比，提升非常明显，即使 `n=10⁵` 也能轻松跑完。

- **空间复杂度**：`O(n)`  
  - 需要保存排序后的 `(value, index)` 列表、DSU 的 `parent`、`rank` 以及分量的下标/数值列表。  
  - 这都是线性额外空间，符合题目限制。

---

## 心得

- **核心技巧**：把可以相互交换的元素看成图的连通分量，用 **并查集（DSU）** 快速划分，再对每个分量内部排序实现字典序最小化。  
- **适用场景**：  
  1. “在满足某种局部条件时可以任意换位”，如 “差值 ≤ limit” 或 “值相同” 等。  
  2. “把数组分成若干可自由重排的块”，如 “相邻元素差 ≤ k” 或 “相同字符可以随意调换”。  
  3. “需要在连通块内部做最优排列”，如 “同一颜色的珠子可以随意重排”。  

- **一句话总结解题钥匙**：**把所有能互相换位的元素归为同一个集合，分别在每个集合内部排序即可得到全局字典序最小的数组。**

---

## 反思

- **第一反应**：直接模拟所有合法交换，写成两层循环的暴力实现。  
- **最容易踩的坑**  
  - 忽视了“间接可换位”的情况：`a` 能换 `b`，`b` 能换 `c`，则 `a` 也能换 `c`，必须考虑整个连通块。  
  - 在构造连通块时若直接遍历所有 `O(n²)` 对会超时，需要利用排序和相邻检查的技巧。  
  - 处理好 **下标** 与 **数值** 的对应关系：DSU 合并的是位置，而不是数值本身。  
- **下次类似题的第一步**：先思考“可交换的关系是否具备传递性”，如果是，就把元素抽象成图的节点，用 **并查集** 或 **DFS/BFS** 找连通分量，再在每个分量内部做最优排列。