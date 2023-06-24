# #2294. Partition Array Such That Maximum Difference Is K / Partition Array Such That Maximum Difference Is K

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/partition-array-such-that-maximum-difference-is-k/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k. You may partition nums into one or more subsequences such that each element in nums appears in exactly one of the subsequences.
Return the minimum number of subsequences needed such that the difference between the maximum and minimum values in each subsequence is at most k.
A subsequence is a sequence that can be derived from another sequence by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [3,6,1,2,5], k = 2
Output: 2
Explanation:
We can partition nums into the two subsequences [3,1,2] and [6,5].
The difference between the maximum and minimum value in the first subsequence is 3 - 1 = 2.
The difference between the maximum and minimum value in the second subsequence is 6 - 5 = 1.
Since two subsequences were created, we return 2. It can be shown that 2 is the minimum number of subsequences needed.
```

**Example 2:**

```
Input: nums = [1,2,3], k = 1
Output: 2
Explanation:
We can partition nums into the two subsequences [1,2] and [3].
The difference between the maximum and minimum value in the first subsequence is 2 - 1 = 1.
The difference between the maximum and minimum value in the second subsequence is 3 - 3 = 0.
Since two subsequences were created, we return 2. Note that another optimal solution is to partition nums into the two subsequences [1] and [2,3].
```

**Example 3:**

```
Input: nums = [2,2,4,5], k = 0
Output: 3
Explanation:
We can partition nums into the three subsequences [2,2], [4], and [5].
The difference between the maximum and minimum value in the first subsequences is 2 - 2 = 0.
The difference between the maximum and minimum value in the second subsequences is 4 - 4 = 0.
The difference between the maximum and minimum value in the third subsequences is 5 - 5 = 0.
Since three subsequences were created, we return 3. It can be shown that 3 is the minimum number of subsequences needed.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 105
- 0 <= k <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。你可以将 `nums` 划分为一个或多个子序列（subsequence），要求每个元素恰好出现在其中的一个子序列中。  
返回所需的最小子序列数量，使得每个子序列中的最大值与最小值之差不超过 `k`。  

**子序列（subsequence）** 是指可以通过删除原序列中的若干（也可以不删除）元素而得到的序列，删除过程不改变剩余元素的相对顺序。

### 示例

**示例 1**  
```
Input: nums = [3,6,1,2,5], k = 2
Output: 2
Explanation:
我们可以将 nums 划分为两个子序列 [3,1,2] 和 [6,5]。
第一个子序列的最大值与最小值之差为 3 - 1 = 2。
第二个子序列的最大值与最小值之差为 6 - 5 = 1。
因为产生了两个子序列，返回 2。可以证明 2 已经是最小可能的数量。
```

**示例 2**  
```
Input: nums = [1,2,3], k = 1
Output: 2
Explanation:
我们可以将 nums 划分为两个子序列 [1,2] 和 [3]。
第一个子序列的最大值与最小值之差为 2 - 1 = 1。
第二个子序列的最大值与最小值之差为 3 - 3 = 0。
因为产生了两个子序列，返回 2。另一个同样最优的划分方式是 [...]
```

**示例 3**  
```
Input: nums = [2,2,4,5], k = 0
Output: 3
Explanation:
我们可以将 nums 划分为三个子序列 [2,2]、[4] 和 [5]。
第一个子序列的最大值与最小值之差为 2 - 2 = 0。
第二个子序列的最大值与最小值之差为 4 - 4 = 0。
第三个子序列的最大值与最小值之差为 5 - 5 = 0。
因为产生了三个子序列，返回 3。
```

### 约束

- `1 <= nums.length <= 10^5`
- `0 <= nums[i] <= 10^5`
- `0 <= k <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的划分方式都枚举一遍**，然后找出满足「每个子序列的最大值和最小值之差 ≤ k」且子序列数量最少的那种。  
- **数据结构**：可以用 `list`（列表）保存当前的若干子序列，每个子序列本身也是 `list`。  
- **生活化类比**：把数组想成一堆装有不同重量的水果，k 就是「同一个篮子里最重和最轻水果重量差的上限」。暴力做法相当于把所有水果随意装进不同的篮子，尝试所有可能的装法，挑出篮子最少的方案。  

**为什么这个方法正确？**  
只要遍历了**所有**合法的划分方式，必然会包含最优解。只要在遍历过程中每次都检查「最大值‑最小值 ≤ k」这个条件，就能保证得到合法的划分。

**时间/空间复杂度**  
- **时间复杂度**：要遍历的划分数是指数级的（类似「把 n 个元素分成若干组」的 Bell 数），大约是 `O(2^n)`，对 n=10⁵ 完全不可接受。  
- **空间复杂度**：递归/回溯时需要保存当前的划分，最坏情况下需要 `O(n)` 的额外空间（保存所有子序列）。

> **大白话解释**：`O(2^n)` 就像把 20 本书每本都决定放进「左边」或「右边」两堆，可能的组合有 2 的 20 次方（约 100 万）种；而 n=10⁵ 时，这个数字会天文般大，根本算不完。

#### 代码（Python）

```python
from typing import List

def min_subseq_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    best = n  # 最坏情况每个元素单独成一段

    def backtrack(idx: int, groups: List[List[int]]) -> None:
        """尝试把 nums[idx:] 放进已有或新建的子序列"""
        nonlocal best
        if idx == n:                     # 所有元素都已经放置
            best = min(best, len(groups))
            return
        # 剪枝：已经超过当前最优解，就不必继续
        if len(groups) >= best:
            return

        x = nums[idx]
        # 1️⃣ 把 x 放进已有的每个子序列（只要合法）
        for g in groups:
            cur_max, cur_min = max(g), min(g)
            if max(cur_max, x) - min(cur_min, x) <= k:
                g.append(x)
                backtrack(idx + 1, groups)
                g.pop()                 # 恢复现场

        # 2️⃣ 新建一个子序列，只装 x
        groups.append([x])
        backtrack(idx + 1, groups)
        groups.pop()                    # 恢复现场

    backtrack(0, [])
    return best
```

> **注意**：上述代码仅用于说明思路，实际运行会在几百个元素左右就超时。

#### 复杂度

- **时间复杂度**：`O(2^n)` —— 需要尝试所有划分方式，指数级增长。  
- **空间复杂度**：`O(n)` —— 递归栈深度最多 n，外加保存当前划分的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **瓶颈在于枚举所有划分**，我们需要找到一种**直接决定划分方式** 的规则。观察题目提示：

> “在每个子序列里，只有最大值和最小值会影响是否满足 `max - min ≤ k`”。  
> “如果把一个子序列的最大值记为 Max，最小值记为 Min，那么把原数组中所有在 `[Min, Max]` 区间内的元素也放进同一个子序列是最优的”。

这意味着**子序列内部的元素可以不必保持原来的相对顺序**（因为我们只要求每个元素恰好出现一次，而不要求子序列是连续的）。于是我们可以**先把数组排序**，把相近的数放在一起，这样更容易满足「最大‑最小 ≤ k」的约束。

排序后，问题转化为：

> 在已排好序的数列中，**把相邻且差值 ≤ k 的元素尽可能放进同一个子序列**，一旦出现差值 > k，就必须开启一个新的子序列。

这正是**贪心**的典型场景：每次尽可能把当前元素并入当前子序列，只有在必须时才开新子序列。

**具体步骤**：

1. 对 `nums` 进行升序排序，得到 `sorted_nums`。  
2. 初始化 `cnt = 1`（至少需要一个子序列），以及 `start = sorted_nums[0]` 记录当前子序列的最小值。  
3. 从第二个元素开始遍历：  
   - 如果 `sorted_nums[i] - start > k`，说明当前元素与当前子序列的最小值差距超出 k，**必须开新子序列**，`cnt += 1`，并把 `start` 更新为该元素（新子序列的最小值）。  
   - 否则，当前元素可以安全加入当前子序列，**不需要做任何操作**（因为已经保证了最大‑最小 ≤ k）。  
4. 遍历结束后，`cnt` 即为最少子序列数。

> **为什么贪心是最优的？**  
> - 已排序后，若两个相邻元素的差值 ≤ k，它们一定可以放在同一个子序列而不破坏约束（因为子序列的最大值和最小值正好是这两个元素之间的范围）。  
> - 若差值 > k，则无论怎样把它们分配到不同的子序列，都不可能让这两个元素同在一个子序列，因为最大‑最小必然大于 k。于是**必须**在这里断开。  
> - 只要每次在“必须断开”的位置开新子序列，就不会产生不必要的额外子序列，从而得到最少的子序列数。

#### 代码（Python）

```python
from typing import List

def min_subseq_greedy(nums: List[int], k: int) -> int:
    """
    贪心 + 排序
    返回最少需要的子序列个数，使得每个子序列的 max - min <= k
    """
    if not nums:
        return 0

    # 1️⃣ 先把数组升序排列
    nums.sort()                       # 排序 O(n log n)

    # 2️⃣ 初始化第一个子序列
    cnt = 1                           # 至少有一个子序列
    start = nums[0]                   # 当前子序列的最小值（也是第一个元素）

    # 3️⃣ 从第二个元素开始遍历
    for x in nums[1:]:
        # 如果与当前子序列的最小值差距超过 k，就必须开新子序列
        if x - start > k:
            cnt += 1                  # 新增一个子序列
            start = x                 # 新子序列的最小值更新为当前元素
        # 否则 x 可以直接放进当前子序列，什么也不需要做

    return cnt
```

#### 复杂度

- **时间复杂度**：`O(n log n)` —— 主要耗时在数组排序，遍历本身是线性的 `O(n)`。  
  > 与暴力的指数级 `O(2^n)` 相比，`O(n log n)` 在 10⁵ 规模下毫秒级即可完成。  
- **空间复杂度**：`O(1)`（如果使用原地排序）或 `O(n)`（Python 的 `list.sort()` 需要额外的临时空间），但不随递归深度增长。

---

## 心得

- **核心技巧**：**先排序，再用贪心把相邻差值 ≤ k 的元素合并到同一个子序列**。  
- **适用场景**：  
  1. “把数组分成若干段，使每段内部满足某种范围约束” 类问题（如 LeetCode 435 `Non-overlapping Intervals` 的变形）。  
  2. “最小化分组数，使得每组内部元素差值不超过阈值” 的题目（例如 “Divide Array into Sets of K Consecutive Numbers”。）  
  3. “区间覆盖 / 区间分段” 的贪心模型（如 “Split Array Largest Sum”。）  
- **一句话总结解题钥匙**：**排序把“相近的数”搬到一起，只有在“相邻差值已经超过上限”时才必须开新组**。

## 反思

- **第一反应**：看到“最大值‑最小值 ≤ k”，自然会想到维护每个子序列的最大最小值，甚至尝试用哈希或滑动窗口。  
- **最容易踩的坑**：  
  - 忽略了子序列不要求保持原始顺序，导致尝试复杂的动态规划或双指针。  
  - 没有注意到 “在同一个子序列里，只要最大最小满足条件，其内部任意排列都是合法的”。  
  - 边界条件：`k = 0` 时只能把相同数放在一起，排序后相同数自然相邻，算法仍然正确。  
- **下次遇到同类题**：**先问自己“是否可以把元素重新排序”，如果可以，先排序再用贪心检查相邻差值**，这往往是最直接的最优思路。