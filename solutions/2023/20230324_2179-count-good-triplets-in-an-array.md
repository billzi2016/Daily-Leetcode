# #2179. 统计数组中的好三元组 / Count Good Triplets in an Array

> 难度：困难 · 标签：Array、Binary Search、Divide and Conquer、Binary Indexed Tree、Segment Tree、Merge Sort、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/count-good-triplets-in-an-array/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed arrays nums1 and nums2 of length n, both of which are permutations of [0, 1, ..., n - 1].
A good triplet is a set of 3 distinct values which are present in increasing order by position both in nums1 and nums2. In other words, if we consider pos1v as the index of the value v in nums1 and pos2v as the index of the value v in nums2, then a good triplet will be a set (x, y, z) where 0 <= x, y, z <= n - 1, such that pos1x < pos1y < pos1z and pos2x < pos2y < pos2z.
Return the total number of good triplets.

**Examples**

**Example 1:**

```
Input: nums1 = [2,0,1,3], nums2 = [0,1,2,3]
Output: 1
Explanation: 
There are 4 triplets (x,y,z) such that pos1x < pos1y < pos1z. They are (2,0,1), (2,0,3), (2,1,3), and (0,1,3). 
Out of those triplets, only the triplet (0,1,3) satisfies pos2x < pos2y < pos2z. Hence, there is only 1 good triplet.
```

**Example 2:**

```
Input: nums1 = [4,0,1,3,2], nums2 = [4,1,0,2,3]
Output: 4
Explanation: The 4 good triplets are (4,0,3), (4,0,2), (4,1,3), and (4,1,2).
```

**Constraints**

- n == nums1.length == nums2.length
- 3 <= n <= 105
- 0 <= nums1[i], nums2[i] <= n - 1
- nums1 and nums2 are permutations of [0, 1, ..., n - 1].

---

## 题目（中文翻译）

**描述**  
给定两个下标从 **0** 开始的数组 `nums1` 和 `nums2`，长度均为 `n`，且两者都是集合 `[0, 1, ..., n - 1]` 的全排列（permutation）。  
一个 **好三元组（good triplet）** 是指在 `nums1` 与 `nums2` 中，三个不同的数值按照下标递增的顺序出现。换言之，设 `pos1v` 为数值 `v` 在 `nums1` 中的下标，`pos2v` 为数值 `v` 在 `nums2` 中的下标，则三元组 `(x, y, z)`（其中 `0 ≤ x, y, z ≤ n - 1`）满足  
`pos1x < pos1y < pos1z` 且 `pos2x < pos2y < pos2z`。  
返回所有好三元组的数量。

**示例 1**  
**输入**: `nums1 = [2,0,1,3]`, `nums2 = [0,1,2,3]`  
**输出**: `1`  
**解释**:  
在 `nums1` 中满足 `pos1x < pos1y < pos1z` 的四个三元组为 `(2,0,1)`, `(2,0,3)`, `(2,1,3)`, `(0,1,3)`。  
其中仅 `(0,1,3)` 同时满足 `pos2x < pos2y < pos2z`，因此好三元组的数量为 **1**。

**示例 2**  
**输入**: `nums1 = [4,0,1,3,2]`, `nums2 = [4,1,0,2,3]`  
**输出**: `4`  
**解释**: 好三元组为 `(4,0,3)`, `(4,0,2)`, `(4,1,3)`, `(4,1,2)`，共计 **4** 个。

**约束条件**  
- `n == nums1.length == nums2.length`  
- `3 ≤ n ≤ 10^5`  
- `0 ≤ nums1[i], nums2[i] ≤ n - 1`  
- `nums1` 与 `nums2` 均为集合 `[0, 1, ..., n - 1]` 的全排列（permutation）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的三元组 `(x, y, z)` 都枚举一遍，检查它们在 `nums1` 与 `nums2` 中的位置关系是否同时满足  

```
pos1[x] < pos1[y] < pos1[z]   且   pos2[x] < pos2[y] < pos2[z]
```

> **数据结构类比**  
> - `pos1`、`pos2` 可以看成“字典”，把每个数映射到它在数组中的下标。就像查字典时，`key` 是单词，`value` 是页码。我们先把这两个字典都建好，后面只要 O(1) 就能得到任意数的下标。

枚举三元组的方式有两种：

1. **三层循环**：先遍历所有 `x`，再遍历所有 `y`，最后遍历所有 `z`。  
2. **先遍历 `y` 再枚举 `x`、`z`**：对每个可能的中间元素 `y`，把左侧的 `x` 与右侧的 `z` 分别枚举。

无论哪种写法，本质上都是 O(n³)（或者 O(n²) 乘以一次线性扫描），因为要检查 `n` 选 `3` 的组合数，数量级随 `n` 的立方增长。

> **为什么它是对的？**  
> 只要我们把所有合法的三元组全部遍历一遍，凡是满足题目条件的就计数，显然不会漏掉也不会多计。

> **时间/空间复杂度的大白话**  
> - **时间复杂度 O(n³)**：如果 `n = 1000`，算法大约要跑 `1000³ = 1,000,000,000` 次循环，电脑根本跑不完。  
> - **空间复杂度 O(n)**：我们只需要存两个字典（`pos1`、`pos2`），大小和数组长度成正比，几百 KB 左右，完全可以接受。

#### 代码（Python）

```python
def count_good_triplets_brute(nums1, nums2):
    n = len(nums1)

    # 把每个数映射到它在 nums1 / nums2 中的位置，像查字典一样 O(1) 取值
    pos1 = {v: i for i, v in enumerate(nums1)}
    pos2 = {v: i for i, v in enumerate(nums2)}

    ans = 0
    # 暴力枚举所有三元组 (x, y, z)
    for x in range(n):
        for y in range(n):
            if x == y:  # 需要三个**不同**的数
                continue
            for z in range(n):
                if z == x or z == y:
                    continue
                # 判断在两个数组中的顺序是否都递增
                if (pos1[x] < pos1[y] < pos1[z]) and (pos2[x] < pos2[y] < pos2[z]):
                    ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n³)` —— 三层循环，每层最多遍历 `n` 次。  
- **空间复杂度**：`O(n)` —— 只用了两个哈希表来存下标。

---

### 2. 最优解

#### 思路  

暴力解太慢的根本原因是**重复比较**：  
- 对每个 `y`，我们都要遍历所有左边的 `x` 再遍历所有右边的 `z`，导致大量不必要的工作。

**关键观察**  
对固定的中间元素 `y`，只要知道：

1. **左侧有多少个数 `x` 同时在 `nums1` 与 `nums2` 中都出现在 `y` 的左边**  
   → 记为 `left[y]`  
2. **右侧有多少个数 `z` 同时在 `nums1` 与 `nums2` 中都出现在 `y` 的右边**  
   → 记为 `right[y]`

那么以 `y` 为中间的好三元组数目就是 `left[y] * right[y]`（左边任选一个，右边任选一个，组合即可）。整个答案就是所有 `y` 的乘积之和。

**如何快速求 `left[y]`、`right[y]`？**  
把 `nums2` 中每个数的下标记下来，得到 `pos2[v]`。遍历 `nums1` 时，当前看到的数 `v` 实际上是“正在当作中间元素”。  

- `left[y]`：在遍历到 `y` 之前已经出现过的数中，有多少它们在 `nums2` 的下标也小于 `pos2[y]`。这相当于“在已经处理过的下标集合里，统计比 `pos2[y]` 更小的个数”。  
- `right[y]`：在遍历完所有元素后，剩余（还未处理）的数中，有多少它们在 `nums2` 的下标大于 `pos2[y]`。这可以在一次逆向遍历中同理求得。

**核心工具——树状数组（Binary Indexed Tree，简称 BIT）**  
- BIT 能在 **对数时间 O(log n)** 完成两类操作：  
  1. **add(i, 1)**：把位置 `i` 的计数加一（相当于把这个下标加入“已经出现的集合”）。  
  2. **query(i)**：求区间 `[0, i]` 的元素总数（即有多少已出现的下标 ≤ i）。  

把 `pos2` 看成坐标轴，`add` 把已遍历的元素标记在 BIT 上，`query(pos2[y]-1)` 就得到左侧符合条件的数量 `left[y]`。

**步骤概览**

1. **预处理**：建立 `pos2` 哈希表。  
2. **正向遍历 `nums1`**  
   - 用 BIT 统计已经出现的元素下标。  
   - `left[y] = bit.query(pos2[y] - 1)`（比 `pos2[y]` 小的已出现下标数）。  
   - 把 `pos2[y]` 加入 BIT（`bit.add(pos2[y], 1)`）。  
3. **逆向遍历 `nums1`**（或再建一个 BIT）  
   - 同理得到 `right[y] = suffix_bit.query(n-1) - suffix_bit.query(pos2[y])`（右侧比 `pos2[y]` 大的已出现下标数）。  
4. **累加答案**：`ans += left[y] * right[y]`。  

整个过程只用了两次线性遍历，每次内部的 BIT 操作是 `O(log n)`，因此总时间 `O(n log n)`，空间 `O(n)`（两个数组 + BIT）。

> **类比**  
> 想象你在排队买票，前面已经买好票的人会在一个“已买名单”里登记。现在你想知道在你前面有多少人比你更早到达（左侧符合条件），只要快速查询名单中比你早的人的数量即可。BIT 就是这种可以**快速计数**的名单。

#### 代码（Python）

```python
class BIT:
    """树状数组（Fenwick Tree），支持前缀和查询与单点增量"""
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)          # 1-indexed

    def add(self, idx: int, delta: int = 1):
        """把 idx 位置的计数加 delta（默认加 1）"""
        idx += 1                           # 转成 1-indexed
        while idx <= self.n:
            self.tree[idx] += delta
            idx += idx & -idx               # lowbit，向上跳

    def query(self, idx: int) -> int:
        """返回区间 [0, idx] 的元素总数（若 idx < 0 则返回 0）"""
        if idx < 0:
            return 0
        idx += 1
        s = 0
        while idx > 0:
            s += self.tree[idx]
            idx -= idx & -idx               # lowbit，向下跳
        return s


def count_good_triplets(nums1, nums2):
    n = len(nums1)

    # 1. 把每个数在 nums2 中的位置记下来，像查字典一样 O(1) 取值
    pos2 = {v: i for i, v in enumerate(nums2)}

    # 2. 正向遍历，计算 left[y]
    bit_left = BIT(n)
    left = [0] * n          # left[y] 对应的是值 y 而不是下标
    for v in nums1:         # 按 nums1 的顺序依次当作 “中间元素”
        p = pos2[v]          # v 在 nums2 中的下标
        left[v] = bit_left.query(p - 1)   # 已出现且下标更小的数量
        bit_left.add(p, 1)                # 把 v 加入已出现集合

    # 3. 逆向遍历，计算 right[y]
    bit_right = BIT(n)
    right = [0] * n
    for v in reversed(nums1):
        p = pos2[v]
        # 已出现且下标更大的数量 = 总已出现 - ≤ p 的已出现
        right[v] = bit_right.query(n - 1) - bit_right.query(p)
        bit_right.add(p, 1)

    # 4. 汇总答案
    ans = 0
    for v in range(n):          # v 即为可能的中间元素的值
        ans += left[v] * right[v]

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 两次遍历 `nums1`（正向 + 逆向），每次都做 `BIT` 的 `add` 与 `query`，每个操作 `O(log n)`。  
  - 与暴力解的 `O(n³)` 相比，`log n` 只在几百左右（`n=10⁵` 时约 17），速度提升数千倍。

- **空间复杂度**：`O(n)`  
  - 需要存 `pos2`（长度 `n`）以及两个 `BIT`（各 `n+1`）和 `left/right` 两个数组。总体线性空间，完全可以放进内存。

---

## 心得

- **核心技巧**：把“在两个排列中同时保持相对顺序”转化为“在第二个排列的下标上做区间计数”。利用 **树状数组**（或线段树）在遍历时实时维护已出现元素的下标分布，能够在 `O(log n)` 完成“左侧更小 / 右侧更大”的计数。
- **适用的题型**  
  1. **统计逆序对 / 交叉对**（LeetCode 493、327）  
  2. **在两个排列中找共同递增子序列的计数**（类似本题）  
  3. **二维坐标点的“左下/右上”计数**（如 “矩形中的点” 类问题）

> **解题钥匙**：把 “在两个序列里都排在前/后” 用 **下标的大小比较** 表示，再用 **可维护前缀计数的数据结构**（BIT / Segment Tree）实现快速统计。

---

## 反思

- **第一反应**：直接想枚举所有三元组，结果发现会超时。  
- **最容易踩的坑**  
  1. **下标越界**：`BIT.query(p-1)` 当 `p=0` 时要返回 `0`，否则会访问负数。  
  2. **值与下标的混淆**：`left/right` 数组的下标是“数的取值”，不是在 `nums1` 中的下标，记清楚两者的对应关系。  
  3. **计数乘积溢出**：答案可能达到 `C(n,3)`，在 Python 中整数不溢出，但如果用固定宽度整数语言要用 `long long`。  
- **下次遇到同类题**：  
  1. **先把两条序列映射成下标**（建立哈希表）。  
  2. **思考能否把“相对顺序”转化为“数值大小比较”。**  
  3. **选用 BIT / Segment Tree** 来维护已经遍历过的元素的分布，做到 `O(log n)` 计数。