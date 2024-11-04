# #2926. **最大平衡子序列和** / Maximum Balanced Subsequence Sum

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Binary Indexed Tree、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-balanced-subsequence-sum/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums.
A subsequence of nums having length k and consisting of indices i0 < i1 < ... < ik-1 is balanced if the following holds:
A subsequence of nums having length 1 is considered balanced.
Return an integer denoting the maximum possible sum of elements in a balanced subsequence of nums.
A subsequence of an array is a new non-empty array that is formed from the original array by deleting some (possibly none) of the elements without disturbing the relative positions of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [3,3,5,6]
Output: 14
Explanation: In this example, the subsequence [3,5,6] consisting of indices 0, 2, and 3 can be selected.
nums[2] - nums[0] >= 2 - 0.
nums[3] - nums[2] >= 3 - 2.
Hence, it is a balanced subsequence, and its sum is the maximum among the balanced subsequences of nums.
The subsequence consisting of indices 1, 2, and 3 is also valid.
It can be shown that it is not possible to get a balanced subsequence with a sum greater than 14.
```

**Example 2:**

```
Input: nums = [5,-1,-3,8]
Output: 13
Explanation: In this example, the subsequence [5,8] consisting of indices 0 and 3 can be selected.
nums[3] - nums[0] >= 3 - 0.
Hence, it is a balanced subsequence, and its sum is the maximum among the balanced subsequences of nums.
It can be shown that it is not possible to get a balanced subsequence with a sum greater than 13.
```

**Example 3:**

```
Input: nums = [-2,-1]
Output: -1
Explanation: In this example, the subsequence [-1] can be selected.
It is a balanced subsequence, and its sum is the maximum among the balanced subsequences of nums.
```

**Constraints**

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 `nums`。  
若一个长度为 `k` 的子序列（subsequence）由下标 `i₀ < i₁ < ... < i_{k‑1}` 组成，且满足以下条件，则称该子序列为 **平衡**（balanced）：

- 当 `k = 1` 时，任意单个元素的子序列默认平衡。
- 当 `k > 1` 时，对于任意相邻的下标 `i_j` 与 `i_{j+1}`（`0 ≤ j < k‑1`），必须有  
  `nums[i_{j+1}] - nums[i_j] ≥ i_{j+1} - i_j`。

返回能够构成平衡子序列的元素和的 **最大可能值**。

> **子序列**（subsequence）是指在保持剩余元素相对位置不变的前提下，从原数组中删除若干（也可能不删除）元素后得到的非空数组。

---

### 示例

#### 示例 1
```text
Input: nums = [3,3,5,6]
Output: 14
Explanation:
在本例中，可以选择下标为 0、2、3 的子序列 [3,5,6]。
- nums[2] - nums[0] = 5 - 3 ≥ 2 - 0
- nums[3] - nums[2] = 6 - 5 ≥ 3 - 2
因此它是一个平衡子序列，且其元素和为所有平衡子序列中最大的。
下标为 1、2、3 的子序列同样满足平衡条件。
可以证明不存在和大于 14 的平衡子序列。
```

#### 示例 2
```text
Input: nums = [5,-1,-3,8]
Output: 13
Explanation:
可以选择下标为 0、3 的子序列 [5,8]。
- nums[3] - nums[0] = 8 - 5 ≥ 3 - 0
它是平衡的，且其和是所有平衡子序列中最大的。  
可以证明无法得到和超过 13 的平衡子序列。
```

#### 示例 3
```text
Input: nums = [-2,-1]
Output: -1
Explanation:
可以选择子序列 [-1]（下标为 1）。它是平衡的，且其和是所有平衡子序列中最大的。
```

---

### 约束条件
- `1 ≤ nums.length ≤ 10⁵`
- `-10⁹ ≤ nums[i] ≤ 10⁹`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求我们从数组 `nums` 中挑选若干个元素（下标保持递增），形成一个 **平衡子序列**。  
平衡的条件可以写成  

```
nums[i_j] - nums[i_{j-1}]  >=  i_j - i_{j-1}
```

直观的想法是：**枚举所有可能的子序列**，检查它们是否满足上面的不等式，然后记录最大和。  

- **枚举子序列**：可以用递归或回溯，每次决定“把当前元素加入子序列还是不加入”。  
- **检查平衡**：只要把新加入的元素下标 `x` 与前一个已选元素下标 `y` 做一次比较 `nums[x] - nums[y] >= x - y`，如果不满足就剪枝。  

这种做法就像在超市里挑选商品：我们把每件商品都当成“要不要买”的选项，尝遍所有可能的购物清单，最后挑出价值最高且满足“预算约束”的那份。

**为什么会对**：只要遍历了 **所有** 合法的子序列，就一定能找到最大和。  

**时间/空间复杂度**：  
- 子序列的数量是 `2^n`（每个位置有“选”或“不选”两种决定），所以最坏情况下我们要检查指数级别的组合，时间复杂度是 **O(2ⁿ)**，对 `n ≤ 10⁵` 完全不可接受。  
- 递归栈深度最多 `n`，空间复杂度是 **O(n)**。

> **大白话**：`O(2ⁿ)` 就像让你把 30 本书全部排成所有可能的堆叠方式，根本不可能在一分钟内算完。

#### 代码（Python）

```python
def maxBalancedSubseq_bruteforce(nums):
    n = len(nums)
    best = float('-inf')

    def dfs(idx, last_idx, cur_sum):
        """在位置 idx 开始尝试，last_idx 是上一个被选元素的下标"""
        nonlocal best
        if idx == n:                     # 到达数组末尾，结束当前分支
            best = max(best, cur_sum)   # 更新全局最大和
            return

        # 1) 不选 idx，直接跳到下一个位置
        dfs(idx + 1, last_idx, cur_sum)

        # 2) 选 idx（需要满足平衡条件）
        if last_idx == -1 or nums[idx] - nums[last_idx] >= idx - last_idx:
            dfs(idx + 1, idx, cur_sum + nums[idx])

    dfs(0, -1, 0)        # -1 表示还没有选任何元素
    return best
```

> 这段代码仅作演示，实际运行会在 `n` 超过 20 时直接超时。

#### 复杂度

- **时间复杂度**：`O(2ⁿ)` —— 需要尝遍所有子序列，随 `n` 指数增长。  
- **空间复杂度**：`O(n)` —— 递归栈最深 `n` 层。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **重复计算**：每次我们都从头遍历所有已经选过的下标去判断能否接上当前元素。  
要想快，就要把“把前面所有合法前驱的最大 dp 值”这件事 **提前准备好**，让查询变成 **O(log n)** 或 **O(1)**。

---

##### 2.1 把不等式改写成单调关系  

原始条件  

```
nums[i_j] - nums[i_{j-1}] >= i_j - i_{j-1}
```

两边同时减去下标，得到  

```
(nums[i_j] - i_j) >= (nums[i_{j-1}] - i_{j-1})
```

**关键点**：只要我们把每个位置 `x` 的 “价值” 定义为  

```
key[x] = nums[x] - x
```

则平衡条件等价于 **key 是非递减的**。换句话说，若我们把所有位置按 `key` 从小到大排序，那么在这条顺序上，后面的元素都可以接在前面任何 `key` 不更大的位置后面。

---

##### 2.2 动态规划的状态  

设  

```
dp[x] = 以位置 x 结尾的平衡子序列的最大和
```

- 如果只选 `x` 本身，和为 `nums[x]`。  
- 如果要在 `x` 前面接一个合法的前驱 `y`（`y < x` 且 `key[y] <= key[x]`），则  

```
dp[x] = nums[x] + max{ dp[y] | y < x, key[y] <= key[x] }
```

于是我们只需要 **快速得到** “在 `key ≤ key[x]` 且下标在左边的 dp 最大值”。这正好可以用 **树状数组（Fenwick Tree）** 或 **线段树** 来维护前缀最大值。

---

##### 2.3 坐标压缩  

`key[x] = nums[x] - x` 的取值范围可以很大（`-10⁹ - 10⁵`），直接在树上建立这么多节点会浪费空间。  
**坐标压缩** 的思路是：

1. 把所有 `key` 收集到一个列表，排序并去重。  
2. 用 `dict[key] = 在压缩后数组中的下标（从 1 开始）` 来映射。  

这样我们只需要 `O(n)` 个树节点。

---

##### 2.4 具体步骤  

| 步骤 | 说明 |
|------|------|
|1️⃣ 收集 `key = nums[i] - i` 并压缩 | 得到 `compress[key]`（1~m） |
|2️⃣ 初始化 Fenwick 树，默认值为 `-inf`（因为我们要取最大）| |
|3️⃣ 按原数组顺序遍历 i = 0 … n‑1 | 对每个 i：|
| a. 通过 `compress[key[i]]` 在树上查询 `[1, idx]` 的最大 dp（即所有 `key ≤ key[i]` 的前缀最大）| `best = query(idx)` |
| b. 计算 `dp[i] = max(nums[i], nums[i] + best)`| 只选自己或接在前面的最佳子序列后面 |
| c. 用 `update(idx, dp[i])` 把当前位置的 dp 写回树（若更大则覆盖）| 保证后面的查询能看到它 |
|4️⃣ 最后答案是所有 `dp[i]` 的最大值| 也可以在遍历时维护一个全局最大 |

> **类比**：把树状数组想成一本“记分册”，每一行对应一种 `key`（比如不同的学生成绩段），我们可以**快速查询** “截至某行的最高分”，并且**随时更新** 某行的最高分。

---

##### 2.5 为什么是最优  

- 每个位置只做一次查询和一次更新，均为 `O(log n)`（树状数组的特性）。  
- 所有 `n` 个位置合计 `O(n log n)`，在 `n ≤ 10⁵` 的限制下轻松通过。  
- 空间只用 `O(n)`（压缩数组 + 树），没有额外的二维 DP 表。

---

#### 代码（Python）

```python
from typing import List
import bisect

class Fenwick:
    """Fenwick（树状数组）用于维护前缀最大值，1-indexed"""
    def __init__(self, n: int):
        self.n = n
        self.bit = [-10**30] * (n + 1)          # 用极小值初始化，方便取 max

    def update(self, idx: int, val: int) -> None:
        """在位置 idx 处写入更大的值（若 val 更大）"""
        while idx <= self.n:
            if val > self.bit[idx]:
                self.bit[idx] = val
            idx += idx & -idx                 # lowbit，向上遍历

    def query(self, idx: int) -> int:
        """返回区间 [1, idx] 的最大值"""
        res = -10**30
        while idx > 0:
            if self.bit[idx] > res:
                res = self.bit[idx]
            idx -= idx & -idx                 # lowbit，向下遍历
        return res


def maximumBalancedSubsequenceSum(nums: List[int]) -> int:
    n = len(nums)

    # 1️⃣ 计算 key = nums[i] - i 并坐标压缩
    keys = [num - i for i, num in enumerate(nums)]
    sorted_unique = sorted(set(keys))
    # mapping: key -> 1-indexed position in Fenwick
    def get_idx(val: int) -> int:
        # bisect_left 返回在 sorted_unique 中第一次出现的位置（0-base），+1 变成 1-base
        return bisect.bisect_left(sorted_unique, val) + 1

    m = len(sorted_unique)
    ft = Fenwick(m)

    ans = -10**30
    for i, num in enumerate(nums):
        key = keys[i]
        idx = get_idx(key)

        # 2️⃣ 查询所有 key' <= key 的最大 dp
        best_pre = ft.query(idx)          # 若没有合法前驱，返回极小值

        # 3️⃣ 计算 dp[i]
        # 只选自己或接在前面最佳子序列后面
        dp_i = max(num, num + best_pre)

        # 4️⃣ 更新 Fenwick，使得以相同 key 的位置能够得到更大的 dp
        ft.update(idx, dp_i)

        # 5️⃣ 维护全局答案
        if dp_i > ans:
            ans = dp_i

    return ans
```

**代码要点注释**  

- `keys = nums[i] - i` 把平衡条件变成 “key 不下降”。  
- `sorted_unique` 与 `bisect` 实现 **坐标压缩**，把可能的巨大 `key` 映射到 `[1, m]`。  
- `Fenwick` 的 `query` 返回 **前缀最大**，恰好对应 “所有 `key ≤ current_key` 的前驱的最大 dp”。  
- `dp_i = max(num, num + best_pre)`：如果前面没有合法前驱（`best_pre` 极小），`num + best_pre` 会比 `num` 小，自动退化为只选自己。  
- `update` 只在新 dp 更大的情况下写入，保证树中每个位置保存的始终是 **该 key 的历史最大 dp**。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `O(n log n)` 来自两次 `log n` 操作（查询、更新）在每个元素上。相较于暴力的 `O(2ⁿ)`，速度提升了指数级。  
- **空间复杂度**：`O(n)`  
  - 需要存储 `keys`、压缩映射以及 Fenwick 树，均为线性空间。

---

## 心得

- **核心技巧**：把原始不等式转化为 **单调性**（`nums[i] - i`），再用 **动态规划 + 前缀最大查询**（Fenwick / Segment Tree）求最优子结构。  
- **适用场景**：  
  1. 需要在“某种单调条件”下寻找前缀最优值的 DP（如 “数组中出现的值不小于前一个”）。  
  2. “区间最大/最小查询 + 动态更新” 的经典问题，如 “最长递增子序列的最大和”。  
  3. 需要**坐标压缩**的离散化场景，例如 “区间覆盖、线段相交计数”。  
- **一句话总结**：把平衡条件抽象为 `key` 的非递减，用前缀最大维护 `dp`，查询/更新用 Fenwick，时间从指数降到对数。

---

## 反思

- **第一反应**：直接枚举子序列，写递归或位运算，结果很快就超时。  
- **最容易踩的坑**：  
  - 忘记把 `key` 进行坐标压缩，导致 Fenwick 大小爆炸。  
  - 在查询前缀最大时忘记处理“没有合法前驱”的情况（需要用极小值或判断 `best_pre` 是否有效）。  
  - `dp` 可能是负数，初始化 Fenwick 为 `0` 会错误地把“不选任何元素”当作合法前缀，导致答案比实际大。  
- **下次类似题**：  
  1. **先把约束写成单调形式**（如 `a[i] - i`、`a[i] + i`）。  
  2. **确定状态转移**，看是否只依赖于“左侧满足某单调条件的最大 dp”。  
  3. **选合适的数据结构**（Fenwick / Segment Tree）来实现“前缀最值查询 + 动态更新”。  

祝你在算法的道路上越走越顺 🚀！