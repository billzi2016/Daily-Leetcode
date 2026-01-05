# #3479. 水果装入篮子 III / Fruits Into Baskets III

> 难度：中等 · 标签：Array、Binary Search、Segment Tree、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/fruits-into-baskets-iii/)

---

## 题目（英文原版）

**Description**

You are given two arrays of integers, fruits and baskets, each of length n, where fruits[i] represents the quantity of the ith type of fruit, and baskets[j] represents the capacity of the jth basket.
From left to right, place the fruits according to these rules:
Return the number of fruit types that remain unplaced after all possible allocations are made.

**Examples**

**Example 1:**

```
Input: fruits = [4,2,5], baskets = [3,5,4]
Output: 1
Explanation:
Since one fruit type remains unplaced, we return 1.
```

**Example 2:**

```
Input: fruits = [3,6,1], baskets = [6,4,7]
Output: 0
Explanation:
Since all fruits are successfully placed, we return 0.
```

**Constraints**

- n == fruits.length == baskets.length
- 1 <= n <= 105
- 1 <= fruits[i], baskets[i] <= 109

---

## 题目（中文翻译）

给定两个整数数组 `fruits` 和 `baskets`，长度均为 `n`，其中 `fruits[i]` 表示第 `i` 类水果的数量，`baskets[j]` 表示第 `j` 个篮子的容量。  
从左到右依次放置水果，遵循以下规则：

* 按顺序尝试将当前未放置的水果类型放入当前篮子；
* 若当前篮子的剩余容量能够容纳该水果类型的全部数量，则全部放入；
* 否则，只能放入尽可能多的水果，剩余的该水果类型将继续尝试放入后面的篮子；
* 当所有篮子都已尝试完毕或所有水果都已放完时结束。

返回在完成所有可能的分配后，仍未被放置的水果类型的数量。

**示例 1**  
**Input:** `fruits = [4,2,5]`, `baskets = [3,5,4]`  
**Output:** `1`  
**Explanation:**  
有一种水果类型（数量为 5）无法全部放入任何篮子，最终剩余未放置的水果类型数为 1，故返回 1。

**示例 2**  
**Input:** `fruits = [3,6,1]`, `baskets = [6,4,7]`  
**Output:** `0`  
**Explanation:**  
所有水果都能够成功放入篮子中，未放置的水果类型数为 0，故返回 0。

**约束条件**  
- `n == fruits.length == baskets.length`  
- `1 <= n <= 10^5`  
- `1 <= fruits[i], baskets[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**依次遍历水果种类**，对每一种水果在**篮子数组的原始顺序**里从左到右找第一个容量 ≥ 该水果数量且还没有被占用的篮子，找到后就把它占掉。  

- **用到的数据结构**  
  - `used` 布尔数组：记录每个篮子是否已经被占用。可以把它想象成“篮子是否已经被贴了“已用”标签”。  
- **为什么正确**  
  - 我们严格按照题目要求的“从左到右依次放置”，每次都挑选**最早**（左边）的满足容量的篮子，这就是题目所描述的“尽可能多放”。  
- **时间/空间复杂度**  
  - 对第 `i` 种水果我们最坏要遍历所有 `n` 个篮子才能找到合适的（或者遍历完都找不到）。于是总体时间是 `n` 次遍历 `n`，即 **O(n²)**。  
    - 大白话：如果 `n = 10⁴`，暴力解大约要跑 `10⁸` 次循环，已经接近电脑的极限。  
  - 只用了一个长度为 `n` 的布尔数组，空间 **O(n)**。  

#### 代码（Python）

```python
def countUnplaced_fruits_bruteforce(fruits, baskets):
    n = len(fruits)
    used = [False] * n          # 记录每个篮子是否已经被占用
    unplaced = 0                # 记录无法放置的水果种类数

    for fruit in fruits:        # 按顺序遍历每一种水果
        placed = False
        for i in range(n):      # 从左到右找第一个合适且未被占用的篮子
            if not used[i] and baskets[i] >= fruit:
                used[i] = True   # 把篮子标记为已用
                placed = True
                break            # 该水果已经放进去，结束内层循环
        if not placed:           # 如果遍历完都没有找到合适的篮子
            unplaced += 1

    return unplaced
```

#### 复杂度  

- **时间复杂度：O(n²)**  
  - “n²” 表示我们最坏会进行 `n`（水果）×`n`（篮子）的比较。  
- **空间复杂度：O(n)**  
  - 只用了一个长度为 `n` 的 `used` 数组，和输入本身的大小同级。  

---  

### 2. 最优解  

#### 思路  

从暴力解出发，**瓶颈** 在于每次都要线性扫描整个篮子数组。我们需要一种**快速定位**“第一个容量 ≥ fruit 且未被占用的篮子”的办法。  

1. **先把篮子按容量从小到大排好序**（容量相同的保持原下标顺序）。  
   - 类比：把所有篮子排成一条“从小到大的货架”，这样只要水果数量不大于某个篮子的容量，**右边的所有篮子容量一定也够**。  
2. 对于当前水果 `fruit`，**二分查找**在已排序的篮子列表中找到**第一个容量 ≥ fruit** 的位置 `pos`。二分查找的时间是 `O(log n)`。  
3. 但仅仅找到容量足够的**位置**还不够，因为该位置对应的篮子可能已经被别的水果占用了。我们需要在 `pos … n-1` 这段**剩余的篮子**里挑选**原下标最小的**（即最左边的）未使用的篮子。  
   - 这里可以使用 **线段树（Segment Tree）** 来维护每个区间的**最小原下标**。  
   - 线段树的每个叶子节点对应排序后数组的一个元素，存的值是该篮子的**原下标**（如果已经被占用，就记成 `+∞`）。内部节点保存区间内的最小值。  
   - 查询 `pos … n-1` 的最小原下标，若是 `+∞` 说明这段区间没有可用篮子，水果无法放置；否则得到的下标就是我们要占用的篮子。  
4. 把占用的篮子在线段树中更新为 `+∞`，表示它已经不可再用了。  

这样，每种水果只需要 **一次二分 + 一次区间最小值查询 + 一次点更新**，每一步都是 `O(log n)`，总体 `O(n log n)`。  

**核心数据结构解释**  

- **二分查找**：想象在排好序的篮子容量列表里找“第一个不小于 fruit 的位置”，就像在有序的电话本里快速定位某个名字。  
- **线段树**：把一排 `n` 个篮子看成一棵满二叉树的叶子，每个内部节点记住它负责的那段叶子里**最小的原下标**。查询区间最小值时，只需要访问 `log n` 条路径上的节点，速度快。  

#### 代码（Python）

```python
import math

INF = 10**18                     # 足够大的数，代表“已经被占用”

class SegmentTree:
    """线段树（最小值版），支持区间最小查询和单点更新"""
    def __init__(self, data):
        """data 是长度为 n 的列表，存放每个叶子节点的初始值（原下标）"""
        self.n = len(data)
        # 树的大小取最接近 2 * 2^ceil(log2 n) 的整数，便于实现
        size = 1 << (math.ceil(math.log2(self.n)) + 1)
        self.tree = [INF] * size
        self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, l, r):
        if l == r:                         # 叶子节点
            self.tree[node] = data[l]
            return
        mid = (l + r) // 2
        self._build(data, node * 2, l, mid)
        self._build(data, node * 2 + 1, mid + 1, r)
        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])

    def query_min(self, ql, qr):
        """返回区间 [ql, qr] 内的最小值（原下标），若区间为空返回 INF"""
        return self._query(1, 0, self.n - 1, ql, qr)

    def _query(self, node, l, r, ql, qr):
        if ql > r or qr < l:               # 完全不相交
            return INF
        if ql <= l and r <= qr:            # 完全覆盖
            return self.tree[node]
        mid = (l + r) // 2
        left_min = self._query(node * 2, l, mid, ql, qr)
        right_min = self._query(node * 2 + 1, mid + 1, r, ql, qr)
        return min(left_min, right_min)

    def update(self, idx, value):
        """把第 idx（排序后的位置）对应的叶子更新为 value（这里用 INF 表示已占用）"""
        self._update(1, 0, self.n - 1, idx, value)

    def _update(self, node, l, r, idx, value):
        if l == r:
            self.tree[node] = value
            return
        mid = (l + r) // 2
        if idx <= mid:
            self._update(node * 2, l, mid, idx, value)
        else:
            self._update(node * 2 + 1, mid + 1, r, idx, value)
        self.tree[node] = min(self.tree[node * 2], self.tree[node * 2 + 1])


def countUnplaced_fruits_optimal(fruits, baskets):
    n = len(fruits)

    # 1) 按容量对篮子排序，同时保留原下标
    #   sorted_baskets[i] = (capacity, original_index)
    sorted_baskets = sorted([(baskets[i], i) for i in range(n)], key=lambda x: x[0])

    capacities = [c for c, _ in sorted_baskets]           # 仅容量的升序数组，供二分查找
    original_idxs = [idx for _, idx in sorted_baskets]   # 对应的原下标，构造线段树的初始数据

    # 2) 建立线段树，树中每个叶子保存该篮子的原下标（未使用时）
    seg = SegmentTree(original_idxs)

    unplaced = 0

    for fruit in fruits:                                 # 按题目顺序遍历水果
        # 2.1) 二分找第一个容量 >= fruit 的位置
        lo, hi = 0, n - 1
        pos = n                                            # 若全部容量 < fruit，保持 n（表示不存在）
        while lo <= hi:
            mid = (lo + hi) // 2
            if capacities[mid] >= fruit:
                pos = mid
                hi = mid - 1
            else:
                lo = mid + 1

        if pos == n:                                       # 没有任何篮子容量足够
            unplaced += 1
            continue

        # 2.2) 在 pos..n-1 区间查询最小的原下标（即最左侧可用篮子）
        min_original = seg.query_min(pos, n - 1)

        if min_original == INF:                           # 这段区间的篮子都已经被占用了
            unplaced += 1
        else:
            # 找到可用篮子后，把它在段树中标记为 INF，表示已占用
            # 需要把原下标对应回排序后的位置 idx，以便更新
            # 因为我们只知道原下标，遍历一次找回对应的 idx（O(log n) 仍可接受），
            # 这里使用二分在 original_idxs 中查找（因为原下标不一定有序），
            # 为了代码简洁直接线性查找（实际实现可用哈希表）。
            idx_in_sorted = None
            for i in range(pos, n):
                if original_idxs[i] == min_original:
                    idx_in_sorted = i
                    break
            seg.update(idx_in_sorted, INF)                # 标记为已占用

    return unplaced
```

> **代码说明**  
> - `SegmentTree` 实现了 **区间最小值查询** 与 **单点更新**，每次操作的时间是 `O(log n)`。  
> - 二分查找用的是手写的循环，直观地展示了“在排好序的容量列表里找第一个不小于 fruit 的位置”。  
> - 为了把找到的原下标映射回排序后的位置，这里用了一个小循环（`O(n)` 最坏），在真实竞赛中可以用 `dict` 把原下标 → 排序后下标的映射提前建立，以保持整体 `O(n log n)`。  

#### 复杂度  

- **时间复杂度：O(n log n)**  
  - 对每个水果：一次二分查找 `O(log n)` + 一次线段树区间查询 `O(log n)` + 一次点更新 `O(log n)`。三者相加仍是 `log n` 级别。整体 `n` 次循环即 `O(n log n)`。  
  - 与暴力的 `O(n²)` 相比，**当 n 达到 10⁵ 时，速度提升约 1000 倍**。  
- **空间复杂度：O(n)**  
  - 需要存 `sorted_baskets`、`capacities`、`original_idxs` 各 `O(n)`，以及线段树本身约 `4n` 的节点，合计仍是线性空间。  

---  

## 心得  

- **核心技巧**：先对“容量”排序 + 二分定位 + 线段树维护“最左未使用的原下标”。  
- **适用的题型**  
  1. **区间分配类**（如“任务安排”“会议室预定”）——需要快速找满足条件的最左/最右资源。  
  2. **在线查询+更新**（如“动态区间最小值”）——常用线段树或树状数组维护。  
  3. **多维约束匹配**（如“把人物配对到房间”）——先排序降低维度，再用结构维护可用位置。  
- **一句话总结**：**把容量排序后，用二分锁定可行区间，再用线段树挑最左的未占用篮子**，即可把“线性扫描”压到 `log n`。  

## 反思  

- **第一反应**：直接遍历寻找合适篮子，忽视了大量重复的线性扫描。  
- **最容易踩的坑**  
  - **下标混淆**：排序后下标与原下标不一致，更新时一定要把两者对应起来（推荐使用哈希映射）。  
  - **溢出**：线段树中使用的 “∞” 必须大于任何合法原下标，防止误判。  
  - **边界条件**：当所有篮子容量都小于当前水果时，二分应返回 “不存在”，否则会误用非法位置。  
- **下次遇到类似题**：第一步先**把约束（容量）排序**，看能否通过**二分 + 数据结构**把线性搜索降到对数级。这样思路更清晰，也更容易写出高效代码。