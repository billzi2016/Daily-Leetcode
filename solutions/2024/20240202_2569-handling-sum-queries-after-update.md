# #2569. **处理更新后的求和查询** / Handling Sum Queries After Update

> 难度：困难 · 标签：Array、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/handling-sum-queries-after-update/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed arrays nums1 and nums2 and a 2D array queries of queries. There are three types of queries:
Return an array containing all the answers to the third type queries.

**Examples**

**Example 1:**

```
Input: nums1 = [1,0,1], nums2 = [0,0,0], queries = [[1,1,1],[2,1,0],[3,0,0]]
Output: [3]
Explanation: After the first query nums1 becomes [1,1,1]. After the second query, nums2 becomes [1,1,1], so the answer to the third query is 3. Thus, [3] is returned.
```

**Example 2:**

```
Input: nums1 = [1], nums2 = [5], queries = [[2,0,0],[3,0,0]]
Output: [5]
Explanation: After the first query, nums2 remains [5], so the answer to the second query is 5. Thus, [5] is returned.
```

**Constraints**

- 1 <= nums1.length,nums2.length <= 105
- nums1.length = nums2.length
- 1 <= queries.length <= 105
- queries[i].length = 3
- 0 <= l <= r <= nums1.length - 1
- 0 <= p <= 106
- 0 <= nums1[i] <= 1
- 0 <= nums2[i] <= 109

---

## 题目（中文翻译）

给定两个下标从 0 开始的数组 `nums1` 和 `nums2`，以及一个二维数组 `queries` 表示一系列查询。查询共有三种类型：

1. **类型 1**：`[1, l, r]`  
   将区间 `[l, r]`（含）内的所有 `nums1[i]` 设为 `1`。

2. **类型 2**：`[2, p, 0]`  
   对所有满足 `nums1[i] == 1` 的下标 `i`，把 `p` 加到对应的 `nums2[i]` 上。

3. **类型 3**：`[3, 0, 0]`  
   将当前 `nums2` 中所有元素的和（即 `sum(nums2)`）加入答案数组。

返回一个数组，包含所有类型 3 查询的答案，顺序与查询出现的顺序相同。

---

### 示例

**示例 1**

```text
Input: nums1 = [1,0,1], nums2 = [0,0,0], queries = [[1,1,1],[2,1,0],[3,0,0]]
Output: [3]
Explanation: 
- 第一次查询后，`nums1` 变为 [1,1,1]。  
- 第二次查询后，`nums2` 变为 [1,1,1]（因为所有 `nums1[i]` 均为 1，向每个对应的 `nums2[i]` 加 1）。  
- 第三次查询要求返回 `nums2` 的总和，结果为 3。于是返回 [3]。
```

**示例 2**

```text
Input: nums1 = [1], nums2 = [5], queries = [[2,0,0],[3,0,0]]
Output: [5]
Explanation: 
- 第一次查询是类型 2，`p = 0`，所以 `nums2` 保持不变仍为 [5]。  
- 第二次查询是类型 3，返回 `nums2` 的总和 5。于是返回 [5]。
```

---

### 约束条件

- `1 <= nums1.length, nums2.length <= 10^5`
- `nums1.length == nums2.length`
- `1 <= queries.length <= 10^5`
- `queries[i].length == 3`
- `0 <= l <= r <= nums1.length - 1`
- `0 <= p <= 10^6`
- `0 <= nums1[i] <= 1`
- `0 <= nums2[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的做法就是把每一次查询都完整地模拟一遍：

1. **类型 1**（`[1, l, r]`）  
   把 `nums1[l…r]` 区间全部置为 `1`。这相当于把一段路上的所有灯打开，遍历区间把每个元素改为 `1` 即可。  

2. **类型 2**（`[2, p, 0]`）  
   把 `nums2[i] += nums1[i] * p`（即如果 `nums1[i]==1`，就在 `nums2[i]` 上加 `p`）。这相当于“对所有打开的灯加上同样的电量”。遍历全部下标，检查 `nums1[i]` 是否为 `1`，如果是就更新 `nums2[i]`。  

3. **类型 3**（`[3, l, r]`）  
   直接求 `nums2[l…r]` 的和并记录答案。就像在一段路上数所有灯的电量总和。  

只要把三种操作顺序执行，就能得到所有第 3 种查询的答案。

> **为什么正确？**  
> 因为我们没有跳过任何一步，也没有对数据做近似，只是按照题目描述一步步改动数组，最后返回真实的区间和。只要实现没有错误，答案自然正确。

> **时间/空间分析（大白话版）**  
> - 对每一次查询我们都要遍历可能的整个数组（长度 `n ≤ 10⁵`），所以最坏情况下每次都是 `O(n)`。  
> - 总共有 `q ≤ 10⁵` 次查询，最坏的时间复杂度是 `O(n·q)`，在最极端的情况下约等于 `10⁵ × 10⁵ = 10¹⁰`，这在电脑里跑根本不可能。  
> - 只用了原来的两个数组 `nums1、nums2`，额外的空间几乎为 `O(1)`（常数级），所以空间消耗很小。

#### 代码（Python）

```python
from typing import List

def handle_query(nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
    n = len(nums1)
    ans = []                     # 用来存放第 3 类查询的答案

    for typ, x, y in queries:
        if typ == 1:                         # 把 nums1[l..r] 全部置为 1
            l, r = x, y
            for i in range(l, r + 1):
                nums1[i] = 1

        elif typ == 2:                       # 对每个 i，若 nums1[i]==1，则 nums2[i] += p
            p = x
            for i in range(n):
                if nums1[i] == 1:
                    nums2[i] += p

        else:                                # typ == 3，求 nums2[l..r] 的和
            l, r = x, y
            total = 0
            for i in range(l, r + 1):
                total += nums2[i]
            ans.append(total)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n · q)`  
  大白话：如果数组长度是 10 万，查询次数也是 10 万，最坏情况需要遍历 10 万 × 10 万 次，根本跑不完。

- **空间复杂度**：`O(1)`（不计答案列表）  
  只用了原来的两个数组，额外开销几乎为零。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次查询都要线性遍历数组**。我们需要把这些遍历“压缩”成对数级或常数级的操作。观察三种查询：

| 类型 | 操作 | 关键点 |
|------|------|--------|
| 1 | 把 `nums1[l..r]` 设为 `1` | 只改变 `nums1`，区间赋值 |
| 2 | 对所有 `i`，若 `nums1[i]==1` 则 `nums2[i] += p` | 实际上是 **把 `p` 加到所有 `nums1` 为 1 的位置** |
| 3 | 求 `nums2[l..r]` 的和 | 区间求和 |

> **核心观察**  
> - `nums1` 只会从 `0` 变成 `1`（永不回到 `0`），所以我们可以把它看作 **“标记位”**：哪些位置已经被“激活”。  
> - 第 2 类查询对 **所有已激活的位置** 加上同样的 `p`，这正好是 **区间加**（对整个数组的加法），但只在激活的位置生效。  
> - 第 3 类查询只关心 `nums2` 的区间和。  

因此我们把两个数组的状态合并到一棵 **线段树（Segment Tree）**，并在树上维护：

1. **`cnt`**：区间内 `nums1` 为 `1` 的个数。  
2. **`sum`**：区间内 `nums2` 的和。  

有了这两个信息，三类操作可以在 **`O(log n)`** 时间完成：

| 操作 | 线段树如何处理 |
|------|----------------|
| 1. `nums1[l..r] = 1` | 只要把对应区间的 `cnt` 设为区间长度（因为全变成 1），并把 `cnt` 的变化记录为 **懒标记** `lazy_set`。 |
| 2. `nums2[i] += p` 对所有 `nums1[i]==1` | 对整棵树的 **已激活** 部分统一加 `p`，即 `sum += cnt * p`。这可以通过 **懒加** `lazy_add` 完成：把 `p` 乘以该节点的 `cnt` 累加到 `sum`，并把 `p` 记录到子节点的 `lazy_add` 中。 |
| 3. 区间求和 `nums2[l..r]` | 直接返回对应节点的 `sum`，和普通线段树的查询一样。 |

> **为什么懒标记能工作？**  
> - **懒加**：在一次 “对已激活位置统一加 `p`” 时，我们不必立刻把 `p` 加到每个叶子节点，只在涉及的区间节点上记下 “以后要加 `p`”。当后续需要访问子节点时（例如进一步划分区间或查询），再把这笔加法“下推”。  
> - **懒设**（把 `nums1` 区间设为 1）：我们只需要把该区间的 `cnt` 直接设为区间长度，同时把之前的 `lazy_set` 覆盖掉。因为 `nums1` 只能从 0 变 1，这种覆盖是安全的。

> **类比**  
> 想象一条长长的走廊，每盏灯（`nums1[i]`）最开始可能是关的（0），也可能是开的（1）。我们在走廊的不同段落装了 **智能控制盒**（线段树节点），盒子里记着这段走廊有多少盏灯是开的（`cnt`）以及这段走廊灯泡的总电量（`sum`）。  
> - 把一段走廊的灯全部打开，只需要告诉对应的盒子 “这段里灯全开”，盒子内部会自动把 `cnt` 更新为段长。  
> - 给所有已经打开的灯统一加电量，只需要告诉根盒子 “每盏打开的灯加 `p`”，根盒子会把这笔加法记在自己的懒标记里，等到真正需要查看某段时再把加法分发下去。  
> - 查询某段电量，只需要让盒子把它记录的 `sum` 报给我们。

#### 代码（Python）

```python
from typing import List

class SegmentTree:
    """带懒标记的线段树，维护两个信息：
       cnt  -> 区间内 nums1 为 1 的个数
       sum  -> 区间内 nums2 的和
    """
    def __init__(self, nums1: List[int], nums2: List[int]):
        self.n = len(nums1)
        size = 4 * self.n                 # 足够大的数组存储树节点
        self.cnt = [0] * size              # 1 的个数
        self.sums = [0] * size             # nums2 的区间和
        self.lazy_add = [0] * size         # 对已激活位置的懒加
        self.lazy_set = [None] * size      # 对 nums1 的懒设（None 表示无操作）

        # 初始化：同时写入 cnt 与 sums
        def build(idx: int, l: int, r: int):
            if l == r:                     # 叶子节点
                self.cnt[idx] = nums1[l]
                self.sums[idx] = nums2[l]
                return
            mid = (l + r) // 2
            build(idx * 2, l, mid)
            build(idx * 2 + 1, mid + 1, r)
            self._pull(idx)                # 合并子节点信息

        build(1, 0, self.n - 1)

    # ----- 工具函数 -----
    def _pull(self, idx: int):
        """把左右子树的信息合并到父节点"""
        self.cnt[idx] = self.cnt[idx * 2] + self.cnt[idx * 2 + 1]
        self.sums[idx] = self.sums[idx * 2] + self.sums[idx * 2 + 1]

    def _apply_set(self, idx: int, l: int, r: int, val: int):
        """把区间 [l, r] 的 nums1 统一设为 val（只能是 1）"""
        self.cnt[idx] = (r - l + 1) * val          # 全部变成 val
        self.lazy_set[idx] = val                  # 记下懒设标记
        # 当设为 1 时，之前可能已经有懒加在这段上，需要把它算进 sum
        # 懒加的含义是：对已激活的（cnt）位置加 lazy_add
        # 这里 cnt 已经是全部位置，所以直接加上 cnt * lazy_add
        if self.lazy_add[idx]:
            self.sums[idx] += self.cnt[idx] * self.lazy_add[idx]

    def _apply_add(self, idx: int, add: int):
        """对已激活的位置统一加 add（只修改 sum，cnt 不变）"""
        self.sums[idx] += self.cnt[idx] * add
        if self.lazy_add[idx] is None:
            self.lazy_add[idx] = add
        else:
            self.lazy_add[idx] += add

    def _push(self, idx: int, l: int, r: int):
        """把懒标记下放到子节点"""
        if l == r:
            return  # 叶子无需下推
        mid = (l + r) // 2
        left, right = idx * 2, idx * 2 + 1

        # 先处理 lazy_set，因为它会覆盖子节点原来的 cnt
        if self.lazy_set[idx] is not None:
            self._apply_set(left, l, mid, self.lazy_set[idx])
            self._apply_set(right, mid + 1, r, self.lazy_set[idx])
            self.lazy_set[idx] = None

        # 再处理 lazy_add
        if self.lazy_add[idx]:
            self._apply_add(left, self.lazy_add[idx])
            self._apply_add(right, self.lazy_add[idx])
            self.lazy_add[idx] = 0

    # ----- 公开操作 -----
    def range_set_one(self, ql: int, qr: int):
        """把 nums1[ql..qr] 设为 1"""
        def _set(idx: int, l: int, r: int):
            if ql <= l and r <= qr:               # 完全覆盖
                self._apply_set(idx, l, r, 1)
                return
            self._push(idx, l, r)                  # 需要下放懒标记
            mid = (l + r) // 2
            if ql <= mid:
                _set(idx * 2, l, mid)
            if qr > mid:
                _set(idx * 2 + 1, mid + 1, r)
            self._pull(idx)                        # 更新父节点

        _set(1, 0, self.n - 1)

    def range_add_on_active(self, p: int):
        """对所有已激活（nums1 为 1）的下标，加上 p"""
        # 这实际上是对整棵树的懒加，因为只对 cnt>0 的位置生效
        def _add(idx: int, l: int, r: int):
            # 只要 cnt 为 0，直接返回（没有激活位置无需加）
            if self.cnt[idx] == 0:
                return
            if l == r:  # 叶子直接加
                self.sums[idx] += p
                return
            self._apply_add(idx, p)   # 在当前节点记录懒加
            # 不必立刻下推，等到后续查询/更新时再下推
        _add(1, 0, self.n - 1)

    def range_sum(self, ql: int, qr: int) -> int:
        """返回 nums2[ql..qr] 的和"""
        def _query(idx: int, l: int, r: int) -> int:
            if ql <= l and r <= qr:
                return self.sums[idx]
            self._push(idx, l, r)               # 确保子节点信息是最新的
            mid = (l + r) // 2
            res = 0
            if ql <= mid:
                res += _query(idx * 2, l, mid)
            if qr > mid:
                res += _query(idx * 2 + 1, mid + 1, r)
            return res
        return _query(1, 0, self.n - 1)


def handle_query(nums1: List[int], nums2: List[int], queries: List[List[int]]) -> List[int]:
    """
    主函数：使用懒惰线段树一次遍历所有查询，返回第 3 类查询的答案列表。
    """
    st = SegmentTree(nums1, nums2)
    ans = []

    for typ, x, y in queries:
        if typ == 1:                     # 把 nums1[l..r] 设为 1
            st.range_set_one(x, y)
        elif typ == 2:                   # 对所有已激活位置加 p
            st.range_add_on_active(x)    # y 总是 0，题目给的格式
        else:                            # typ == 3，区间求和
            ans.append(st.range_sum(x, y))

    return ans
```

#### 复杂度

- **时间复杂度**：`O((n + q) · log n)`  
  - 建树 `O(n)`（一次遍历构造），后面的每一次查询（不论是哪种类型）最多涉及 **`log n`** 层的递归或懒标记操作。  
  - 大白话：如果数组长 10⁵，`log₂10⁵ ≈ 17`，所以每次查询只需要大约 17 步就能完成，10⁵ 次查询也只要几百万步，完全可以在一秒左右跑完。

- **空间复杂度**：`O(n)`  
  - 线段树的数组大小约为 `4·n`，再加上几个懒标记数组，总体是线性空间。  
  - 与暴力解相比多用了几倍的内存，但仍然是可接受的（10⁵ 的数据只需要几 MB）。

---

## 心得

- **核心技巧**：**懒惰线段树**（Lazy Segment Tree）——在区间更新时不立刻把修改下放到每个叶子，而是记录在父节点的“懒标记”里，等到真正需要时再下推。  
- **适用的题型**  
  1. 区间赋值 + 区间求和（如本题的 `type 1` + `type 3`）  
  2. 区间加 + 区间最小值/最大值查询（经典 “区间加、区间最值”）  
  3. “区间翻转 + 区间计数”这类需要同时维护两种信息的题目  

> **一句话总结解题钥匙**：  
> 把“对整个数组的操作”转化为“对已激活位置的操作”，并用懒惰线段树把每一次区间更新压缩到 `O(log n)`。

---

## 反思

- **第一反应**：看到有区间赋值、区间加、区间求和三种混合，立刻想到 **线段树**，因为普通遍历太慢。  
- **最容易踩的坑**  
  1. **懒标记的覆盖顺序**：先处理 `set` 再处理 `add`，否则会把已经被设为 1 的位置错过加法。  
  2. **cnt 为 0 时的加法**：如果某节点的 `cnt` 为 0（全部未激活），对它执行加法是无意义的，若不判断会导致错误的 `sum` 更新。  
  3. **边界条件**：`queries` 中的 `type 2` 的第三个参数始终是 0，代码里要忽略它，否则可能误把它当成右端点。  

- **下次类似题的第一步**：  
  1. 明确每种操作对哪一个或哪几个属性（计数、和、最值）产生影响。  
  2. 判断是否可以用 **单一的数据结构** 同时维护这些属性（本题用线段树的两个字段）。  
  3. 再决定是否需要 **懒标记**（当有区间赋值或区间加时几乎必需）。