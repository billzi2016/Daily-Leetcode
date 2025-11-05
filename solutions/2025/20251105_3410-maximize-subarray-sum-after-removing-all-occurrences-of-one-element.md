# #3410. 删除一种元素的所有出现后，最大化子数组和 / Maximize Subarray Sum After Removing All Occurrences of One Element

> 难度：困难 · 标签：Array、Dynamic Programming、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/maximize-subarray-sum-after-removing-all-occurrences-of-one-element/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums.
You can do the following operation on the array at most once:
Return the maximum subarray sum across all possible resulting arrays.

**Examples**

**Example 1:**

```
Input: nums = [-3,2,-2,-1,3,-2,3]
Output: 7
Explanation:
We can have the following arrays after at most one operation:
The output is max(4, 4, 7, 4, 2) = 7 .
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 10
Explanation:
It is optimal to not perform any operations.
```

**Constraints**

- 1 <= nums.length <= 105
- -106 <= nums[i] <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums`。  
你可以至多执行一次以下操作：选择数组中**某个**元素的取值，并删除该取值在数组中的所有出现位置。  

返回在所有可能得到的数组中，子数组（subarray）和的最大值。  

示例 1  
输入: `nums = [-3,2,-2,-1,3,-2,3]`  
输出: `7`  
解释:  
我们至多进行一次操作后，可以得到以下几种数组（分别对应删除 `-3`、`2`、`-2`、`-1`、`3` 中的某一种）：  
- 删除 `-3` 后的数组子数组最大和为 4  
- 删除 `2` 后的数组子数组最大和为 4  
- 删除 `-2` 后的数组子数组最大和为 7  
- 删除 `-1` 后的数组子数组最大和为 4  
- 删除 `3` 后的数组子数组最大和为 2  

最终答案为 `max(4, 4, 7, 4, 2) = 7`。  

示例 2  
输入: `nums = [1,2,3,4]`  
输出: `10`  
解释:  
此时最佳做法是不进行任何操作，整个数组本身即为最大子数组和。  

约束条件  
- `1 <= nums.length <= 10^5`  
- `-10^6 <= nums[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举要删除的元素的取值**，对每一种取值，把数组里所有等于它的数全部去掉（相当于把它们当作 “不存在”），然后在剩下的数组上求最大子数组和。  
这一步求最大子数组和可以用 **Kadane 算法**（一次遍历，维护当前子数组的最大和）完成。

> **类比**：把数组想成一串珠子，珠子上可能写着不同的数字。我们先挑一种数字（比如 “-2”），把所有写着 “-2” 的珠子摘掉，剩下的珠子重新连在一起，再找出连续珠子和最大的那段。把所有可能的数字都试一遍，最大的和就是答案。

为什么这能得到正确答案？因为题目只允许 **至多一次** 的全局删除操作，枚举所有可能的被删除数字就覆盖了所有合法的操作（包括“不删除”——相当于把“删除的数字”设为一个根本不存在的值）。

**时间复杂度**  
- 枚举不同的数字最多有 `m` 种（`m ≤ n`，因为数组长度为 `n`），每种情况下都要遍历一次完整数组求 Kadane，时间是 `O(n)`。  
- 所以总时间是 `O(m·n)`，最坏情况下 `m = n`，即 `O(n²)`。  
> 大白话：如果数组有 10⁵ 个数，暴力解相当于要跑 10⁵ 次 10⁵ 长度的遍历，几乎不可能在合理时间内完成。

**空间复杂度**  
- 只用了常数级的额外空间（几个变量），所以是 `O(1)`。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def max_subarray_sum(arr: List[int]) -> int:
    """Kadane 算法：一次遍历求最大子数组和"""
    cur = best = arr[0]
    for x in arr[1:]:
        # 如果把当前子数组丢掉，重新从 x 开始会更好，就这么做
        cur = max(x, cur + x)
        best = max(best, cur)
    return best

def max_sum_after_removing_one(nums: List[int]) -> int:
    # 记录每个数出现的位置，方便后面构造删除后的数组
    pos = defaultdict(list)
    for i, v in enumerate(nums):
        pos[v].append(i)

    # 最佳答案，先把“什么也不删”的情况算进去
    answer = max_subarray_sum(nums)

    # 枚举所有可能被删除的数值
    for val, indices in pos.items():
        # 把所有等于 val 的位置设为 0（相当于删除后相邻）
        tmp = nums[:]                     # 复制一份原数组
        for i in indices:
            tmp[i] = 0                    # 删除等价于变成 0，后面 Kadane 会自动跳过
        answer = max(answer, max_subarray_sum(tmp))

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)`（最坏情况下每个不同的数都要遍历一次数组）。
- **空间复杂度**：`O(n)`（复制数组 `tmp` 时需要额外的 `n` 长度空间，若在原数组上原地修改再恢复，可降到 `O(1)`）。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次枚举一个值都要重新遍历整个数组。  
实际上，**数组的结构并没有改变**，我们只是在不同的时刻把若干位置的数“暂时变成 0”。如果能够 **快速地把若干位置的数改为 0 并立刻得到当前数组的最大子数组和**，就不需要每次都重新跑 Kadane。

这正是 **线段树**（Segment Tree）擅长的事情：  
- 对数组的一个区间维护一些信息（这里是四个：总和、最大前缀和、最大后缀和、最大子数组和）。  
- 支持 **点更新**（把某个位置的值改为 0）和 **整体查询**（根节点即为整段数组的最大子数组和），时间都是 `O(log n)`。

**核心概念——四元组**（每个线段树节点保存）  
| 名称 | 含义 | 类比 |
|------|------|------|
| `sum` | 区间所有元素的和 | 把所有珠子加在一起的总重量 |
| `pref` | 区间内**以左端点开始**的最大子数组和 | 从左边第一颗珠子开始，往右抓，能抓到的最大重量 |
| `suff` | 区间内**以右端点结束**的最大子数组和 | 从右边第一颗珠子开始，往左抓，能抓到的最大重量 |
| `ans` | 区间内的**最大子数组和**（不要求包含端点） | 任意连续珠子中，重量最大的那段 |

**合并两个子区间**  
设左子区间为 `L`，右子区间为 `R`，则父节点的四元组可以这样算：

```
sum  = L.sum + R.sum
pref = max(L.pref, L.sum + R.pref)
suff = max(R.suff, R.sum + L.suff)
ans  = max(L.ans, R.ans, L.suff + R.pref)
```

- `pref`：要么只在左边，就取 `L.pref`；要么跨过左边全部再进入右边的前缀，得到 `L.sum + R.pref`。  
- `suff` 同理。  
- `ans`：最大子数组要么完全在左边、完全在右边，或者跨越中间，这时左边的最大后缀加右边的最大前缀即为跨越的和。

**整体算法**  

1. **预处理**  
   - 建立线段树，初始值即为原数组 `nums`。  
   - 同时记录每个不同数值出现的所有下标（`value → [indices]`），因为我们要一次性把同一个数的所有位置改成 0。

2. **遍历所有可能被删除的数值**（包括 “不删”）  
   - 对当前值 `v`，把 `pos[v]` 中的所有位置 **点更新为 0**（每次 `O(log n)`）。  
   - 查询根节点的 `ans`，即是“把所有 `v` 删除后”的最大子数组和。  
   - 用一个全局变量 `best` 记录最大值。  
   - **注意**：因为每个位置只会在它对应的数值被处理时被改成 0，一旦改了就不需要恢复——后面的数值已经不需要它原来的值了。这样每个位置只更新一次，总共 `n` 次更新。

3. 返回 `best`。

**复杂度分析**  
- **时间**：  
  - 构建线段树 `O(n)`。  
  - 对每个不同的数值，遍历它出现的下标并做点更新，每次 `O(log n)`。所有下标共 `n` 个，所以更新总共 `O(n log n)`。  
  - 每次查询根节点 `O(1)`，共 `m ≤ n` 次，忽略不计。  
  - 故总体时间 `O(n log n)`，远快于暴力的 `O(n²)`。  
- **空间**：线段树需要约 `4·n` 个节点，每个节点保存四个整数，故 `O(n)`。

> **直观理解**：想象你在一条长河上搭桥，每座桥可以一次性承受一定的重量（对应区间信息）。当你把河里某些石头（等于被删除的数）搬走（改成 0），只需要在石头所在的位置重新检查桥的承重（点更新），而不必重新测量整条河的所有桥。这样就能快速得到当前河段能够承受的最大重量（最大子数组和）。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

class Node:
    """线段树的节点，保存四元组信息"""
    __slots__ = ('sum', 'pref', 'suff', 'ans')
    def __init__(self, s=0, p=0, su=0, a=0):
        self.sum = s      # 区间总和
        self.pref = p     # 区间最大前缀和
        self.suff = su    # 区间最大后缀和
        self.ans = a      # 区间最大子数组和

def combine(left: Node, right: Node) -> Node:
    """合并两个子区间，得到父区间的四元组"""
    res = Node()
    res.sum  = left.sum + right.sum
    res.pref = max(left.pref, left.sum + right.pref)
    res.suff = max(right.suff, right.sum + left.suff)
    res.ans  = max(left.ans, right.ans, left.suff + right.pref)
    return res

class SegTree:
    """支持点更新和整体最大子数组和查询的线段树"""
    def __init__(self, data: List[int]):
        self.n = len(data)
        # 为了简化实现，使用 1-indexed 的完全二叉树数组
        self.tree = [Node() for _ in range(4 * self.n)]
        self._build(1, 0, self.n - 1, data)

    def _build(self, idx: int, l: int, r: int, data: List[int]):
        if l == r:
            v = data[l]
            self.tree[idx] = Node(v, max(v, 0), max(v, 0), max(v, 0))
            return
        mid = (l + r) // 2
        self._build(idx * 2, l, mid, data)
        self._build(idx * 2 + 1, mid + 1, r, data)
        self.tree[idx] = combine(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def point_update(self, pos: int, new_val: int):
        """把位置 pos 的值改为 new_val（这里 new_val 为 0）"""
        self._update(1, 0, self.n - 1, pos, new_val)

    def _update(self, idx: int, l: int, r: int, pos: int, val: int):
        if l == r:
            # 叶子节点直接写入新值
            self.tree[idx] = Node(val, max(val, 0), max(val, 0), max(val, 0))
            return
        mid = (l + r) // 2
        if pos <= mid:
            self._update(idx * 2, l, mid, pos, val)
        else:
            self._update(idx * 2 + 1, mid + 1, r, pos, val)
        self.tree[idx] = combine(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def max_subarray_sum(self) -> int:
        """根节点保存的 ans 即为整段数组的最大子数组和"""
        return self.tree[1].ans

def max_sum_after_removing_one(nums: List[int]) -> int:
    n = len(nums)
    # 1. 记录每个数值出现的下标
    pos = defaultdict(list)
    for i, v in enumerate(nums):
        pos[v].append(i)

    # 2. 建立线段树（初始时没有任何删除）
    seg = SegTree(nums)

    # 3. 初始答案：不进行任何删除
    best = seg.max_subarray_sum()

    # 4. 按数值遍历，依次把该数值的所有位置改成 0，查询答案
    for val, indices in pos.items():
        for idx in indices:
            seg.point_update(idx, 0)          # 把该位置的元素“删除”
        best = max(best, seg.max_subarray_sum())

    return best
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 建树 `O(n)`，每个位置更新一次 `O(log n)`，共 `n` 次更新 → `O(n log n)`。  
  - 与暴力 `O(n²)` 相比，速度提升了几个数量级（例如 `n=10⁵` 时，`n log n ≈ 1.7·10⁶`，完全可接受）。

- **空间复杂度**：`O(n)`  
  - 线段树需要约 `4n` 个节点，每个节点存四个整数。

---

## 心得

- **核心技巧**：利用线段树维护 “最大子数组和” 四元组，配合点更新实现“把同一个数全部变为 0” 的快速查询。  
- **适用场景**：  
  1. **区间最大子数组和**（如 LeetCode 53、动态维护子数组和的题目）。  
  2. **数组元素动态修改后仍需快速求最大子段**（如“单点修改，区间查询最大子段和”）。  
  3. **需要一次性“屏蔽”若干位置再求全局最优**（本题的“删除所有相同元素”）。  
- **一句话总结**：把“把同一数字全部删掉”转化为“把这些位置的值改为 0”，再用线段树一次性维护最大子数组和，即可在 `O(n log n)` 内求出最优答案。

---

## 反思

- **第一反应**：直接枚举所有可能删除的数字，配合 Kadane 计算——想到的就是暴力。  
- **最容易踩的坑**：  
  - **负数的处理**：删除负数后，子数组可能跨过原来的负数位置。若把被删元素设为 `-inf`（负无穷）会把跨段截断，答案会出错。正确做法是设为 `0`（相当于把它们从数组中“抽走”）。  
  - **全负数组**：如果所有数都是负的，最大子数组和应该是最大的单个元素（即使不删也可能是负数）。线段树的 `pref/suff/ans` 必须用 `max(val, 0)` 初始化，否则会出现错误的 0。  
  - **重复更新**：必须保证每个位置只更新一次，否则会把已经删掉的 0 再改回原值，导致错误。利用“每个数只遍历一次”的思路即可避免。  
- **下次类似题的第一步**：  
  1. **把全局一次性操作抽象为点/区间的值修改**（如设为 0、设为 INF）。  
  2. **找能快速维护目标属性的数据结构**（线段树、树状数组、单调栈等）。  
  3. **确定每个元素的更新次数**，保证整体复杂度在 `O(n log n)` 以内。