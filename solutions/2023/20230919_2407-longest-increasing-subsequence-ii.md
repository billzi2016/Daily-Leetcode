# #2407. 最长递增子序列 II / Longest Increasing Subsequence II

> 难度：困难 · 标签：Array、Divide and Conquer、Dynamic Programming、Binary Indexed Tree、Segment Tree、Queue、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/longest-increasing-subsequence-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
Find the longest subsequence of nums that meets the following requirements:
Return the length of the longest subsequence that meets the requirements.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [4,2,1,4,3,4,5,8,15], k = 3
Output: 5
Explanation:
The longest subsequence that meets the requirements is [1,3,4,5,8].
The subsequence has a length of 5, so we return 5.
Note that the subsequence [1,3,4,5,8,15] does not meet the requirements because 15 - 8 = 7 is larger than 3.
```

**Example 2:**

```
Input: nums = [7,4,5,1,8,12,4,7], k = 5
Output: 4
Explanation:
The longest subsequence that meets the requirements is [4,5,8,12].
The subsequence has a length of 4, so we return 4.
```

**Example 3:**

```
Input: nums = [1,5], k = 1
Output: 1
Explanation:
The longest subsequence that meets the requirements is [1].
The subsequence has a length of 1, so we return 1.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i], k <= 105

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个整数（integer）`k`。  
找到满足以下要求的 `nums` 的最长子序列（subsequence）：

1. 子序列中的元素严格递增；  
2. 相邻元素之间的差值不超过 `k`（即对于相邻的 `a、b`，有 `b - a ≤ k`）。

返回满足上述要求的最长子序列的长度。

子序列（subsequence）是指通过删除原数组（array）中的若干（或不删除）元素而得到的数组，删除过程不改变剩余元素的相对顺序。

**示例 1**  
输入: `nums = [4,2,1,4,3,4,5,8,15], k = 3`  
输出: `5`  
解释:  
满足要求的最长子序列为 `[1,3,4,5,8]`。该子序列长度为 5，故返回 5。需要注意，子序列 `[1,3,4,5,8,15]` 不符合要求，因为 `15 - 8 = 7` 大于 `k=3`。

**示例 2**  
输入: `nums = [7,4,5,1,8,12,4,7], k = 5`  
输出: `4`  
解释:  
满足要求的最长子序列为 `[4,5,8,12]`。该子序列长度为 4，故返回 4。

**示例 3**  
输入: `nums = [1,5], k = 1`  
输出: `1`  
解释:  
满足要求的最长子序列为 `[1]`。该子序列长度为 1，故返回 1。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i], k <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
- 对每一个位置 `i`，把它当成子序列的 **最后一个元素**。  
- 再把它前面的所有位置 `j (j < i)` 挨个检查，看看能否把 `nums[j]` 接在 `nums[i]` 前面。  
- 只要满足两个条件：  

  1. `nums[j] < nums[i]`（必须递增）  
  2. `nums[i] - nums[j] ≤ k`（相邻两个数的差不能超过 `k`）  

  那么 `dp[i] = max(dp[i], dp[j] + 1)`。  
- 最后答案就是所有 `dp[i]` 的最大值。

这里的 `dp[i]` 表示“以 `nums[i]` 为结尾的合法子序列的最长长度”。  

> **类比**：想象每个数字是一本书的章节编号，`dp[i]` 就是把第 `i` 章放在书尾时，能够得到的最长合法章节序列。我们把前面的每一本书（`j`）都翻一遍，看看能不能接在第 `i` 章后面——这就是暴力的“逐本翻查”。

#### 代码（Python）

```python
from typing import List

def length_of_lis_with_k(nums: List[int], k: int) -> int:
    n = len(nums)
    # dp[i] 表示以 nums[i] 结尾的合法子序列的最长长度，最少是 1（自己本身）
    dp = [1] * n

    # 暴力遍历所有前面的元素
    for i in range(n):
        for j in range(i):
            # 必须递增且相邻差不超过 k
            if nums[j] < nums[i] and nums[i] - nums[j] <= k:
                # 把 j 位置的子序列接到 i 位置后面，长度加 1
                dp[i] = max(dp[i], dp[j] + 1)

    # 整个数组的最长合法子序列长度
    return max(dp)
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - “两层循环”每次都要检查前面所有元素。  
  - 若 `n = 10⁵`，则约 `10¹⁰` 次操作，明显会超时。  
  - **大白话**：如果把每个人都要跟前面所有人握手，人数多了手会握到手软，速度会慢到不行。  

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的 `dp` 数组来保存每个位置的结果。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历所有前面的 `j`**，其实我们只关心满足条件的 `j` 中 **`dp[j]` 的最大值**。如果能在 **“值的区间”** `[nums[i] - k, nums[i] - 1]` 内快速得到最大的 `dp`，就不必逐个检查。

**关键点**：

1. `dp[i]` 只和前面已经处理好的 `dp` 有关（因为我们按顺序遍历 `i`），所以可以把所有已经计算好的 `dp` 按 **“数字的大小”** 存到一个结构里。  
2. 对于当前的 `nums[i]`，我们要查询的范围是 **“所有已经出现过的、数值在 `[nums[i]-k, nums[i]-1]` 之间的 `dp` 最大值”**。  
3. 这正好是**区间最大值查询**（Range Maximum Query）的问题，常用的数据结构有**线段树**或**树状数组（Fenwick Tree）**。这里用**线段树**实现，因为它天然支持 **区间查询 + 单点更新**。

**步骤**：

- 设 `MAXV = max(nums) ≤ 10⁵`（题目限制）。我们在 `[1, MAXV]` 上建立一棵线段树，树叶节点保存对应数值的 **当前最大 `dp`**（如果该数值还未出现，默认 0）。  
- 按数组顺序遍历 `i = 0 … n-1`：  
  1. 计算查询左、右边界 `L = max(1, nums[i] - k)`，`R = nums[i] - 1`。  
  2. 在区间 `[L, R]` 上做 **最大值查询**，得到 `best = max dp`。如果区间为空（`L > R`），`best = 0`。  
  3. 当前 `dp_i = best + 1`（自己本身算 1，外加前面能接的最长长度）。  
  4. 把 `dp_i` **更新**到线段树的叶子 `pos = nums[i]`，取最大值（因为同一个数值可能出现多次，保留最长的）。  
- 遍历结束后，所有 `dp_i` 中的最大值即为答案。

> **类比**：把每个数字想象成一本书的“章节号”。我们在一本巨大的“目录”（线段树）里记录每个章节号对应的最长合法章节序列长度。当要写新章节 `x` 时，只需要在目录里快速找出 **“最近的、编号在 `[x-k, x-1]` 范围内的章节”** 的最长序列，然后在它的基础上加一即可。目录的查询是 `log(MAXV)` 级别，极快。

#### 代码（Python）

```python
from typing import List

class SegmentTree:
    """线段树（区间最大值 + 单点取最大）"""
    def __init__(self, size: int):
        # 树的大小取 4 * size，足够容纳完整二叉树
        self.N = size
        self.tree = [0] * (4 * size)

    def _update(self, idx: int, l: int, r: int, pos: int, val: int):
        """把位置 pos 的值更新为 max(old, val)"""
        if l == r:                     # 到达叶子节点
            self.tree[idx] = max(self.tree[idx], val)
            return
        mid = (l + r) // 2
        if pos <= mid:
            self._update(idx * 2, l, mid, pos, val)
        else:
            self._update(idx * 2 + 1, mid + 1, r, pos, val)
        # 父节点维护左右子区间的最大值
        self.tree[idx] = max(self.tree[idx * 2], self.tree[idx * 2 + 1])

    def update(self, pos: int, val: int):
        self._update(1, 1, self.N, pos, val)

    def _query(self, idx: int, l: int, r: int, ql: int, qr: int) -> int:
        """返回区间 [ql, qr] 的最大值"""
        if ql > r or qr < l:           # 完全不相交
            return 0
        if ql <= l and r <= qr:       # 完全覆盖
            return self.tree[idx]
        mid = (l + r) // 2
        left_max = self._query(idx * 2, l, mid, ql, qr)
        right_max = self._query(idx * 2 + 1, mid + 1, r, ql, qr)
        return max(left_max, right_max)

    def query(self, l: int, r: int) -> int:
        if l > r:                      # 区间为空时返回 0
            return 0
        return self._query(1, 1, self.N, l, r)


def length_of_lis_with_k(nums: List[int], k: int) -> int:
    if not nums:
        return 0
    max_val = max(nums)               # 确定线段树的大小
    seg = SegmentTree(max_val)

    ans = 0
    for x in nums:
        # 要查询的前驱数值区间 [x-k, x-1]
        left = max(1, x - k)
        right = x - 1
        best = seg.query(left, right)   # 区间最大 dp
        cur = best + 1                   # 以 x 结尾的最长合法子序列长度
        seg.update(x, cur)               # 把 cur 写回到位置 x
        ans = max(ans, cur)              # 维护全局最大

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log C)`，其中 `C = max(nums) ≤ 10⁵`。  
  - 对每个元素我们做一次 **区间查询** + **单点更新**，每次操作在 **树高 `log C`**（约 17）层完成。  
  - 与暴力的 `O(n²)` 相比，`log C` 只是一把“加速的杠杆”，即使 `n = 10⁵` 也能在毫秒级完成。  

- **空间复杂度**：`O(C)`（线段树数组大小），约 `4 * 10⁵` 的整数，完全在内存限制内。  
  - 只额外用了 `dp` 变量 `ans`，不需要保存整个 `dp` 数组，进一步节约空间。  

---

## 心得  

- **核心技巧**：把 “以某个数值结尾的最长合法子序列长度” 按数值映射到线段树（或 Fenwick 树），利用**区间最大值查询**实现 `O(log C)` 的状态转移。  
- **适用的题型**：  
  1. **带约束的最长递增子序列**（如本题、`LIS with limited difference`）。  
  2. **区间 DP + 值域约束**（如“最长上升子序列 II”或“带阈值的最大子数组和”）。  
  3. **在数值范围上做最大/最小查询的动态规划**（如“最大子序列和，元素差 ≤ k”等）。  
- **一句话总结解题钥匙**：  
  > **“把 DP 状态映射到值域，使用线段树（或树状数组）在 `log` 时间内完成区间最大查询”。**  

---

## 反思  

- **第一反应**：看到“最长子序列”“相邻差 ≤ k”，自然想到 **动态规划**，但最开始会写成 `O(n²)` 的双循环。  
- **最容易踩的坑**：  
  - **边界**：查询区间可能为空（`x - k` 小于 1 或 `x-1` 小于 `x-k`），必须返回 0 而不是错误。  
  - **重复数值**：同一个数值可能出现多次，更新时要取 **最大**，否则后面的出现会把之前更好的结果覆盖掉。  
  - **数值范围**：`nums[i]` 最大到 `10⁵`，如果直接把下标当作 `dp` 数组大小会导致 `O(n²)`，一定要利用数值上限构建线段树。  
- **下次遇到同类题**，第一步应想到：  
  1. 用 DP 表示 “以当前元素结尾的最优解”。  
  2. 看转移式里需要 **“在某个数值区间内的最优值”**，于是选用 **区间查询数据结构**（线段树 / 树状数组）来加速。