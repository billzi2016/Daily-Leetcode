# #3165. 非相邻元素子序列的最大和 / Maximum Sum of Subsequence With Non-adjacent Elements

> 难度：困难 · 标签：Array、Divide and Conquer、Dynamic Programming、Segment Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-of-subsequence-with-non-adjacent-elements/)

---

## 题目（英文原版）

**Description**

You are given an array nums consisting of integers. You are also given a 2D array queries, where queries[i] = [posi, xi].
For query i, we first set nums[posi] equal to xi, then we calculate the answer to query i which is the maximum sum of a subsequence of nums where no two adjacent elements are selected.
Return the sum of the answers to all queries.
Since the final answer may be very large, return it modulo 109 + 7.
A subsequence is an array that can be derived from another array by deleting some or no elements without changing the order of the remaining elements.

**Examples**

**Example 1:**

```
Input: nums = [3,5,9], queries = [[1,-2],[0,-3]]
Output: 21
Explanation: After the 1 st query, nums = [3,-2,9] and the maximum sum of a subsequence with non-adjacent elements is 3 + 9 = 12 . After the 2 nd query, nums = [-3,-2,9] and the maximum sum of a subsequence with non-adjacent elements is 9.
```

**Example 2:**

```
Input: nums = [0,-1], queries = [[0,-5]]
Output: 0
Explanation: After the 1 st query, nums = [-5,-1] and the maximum sum of a subsequence with non-adjacent elements is 0 (choosing an empty subsequence).
```

**Constraints**

- 1 <= nums.length <= 5 * 104
- -105 <= nums[i] <= 105
- 1 <= queries.length <= 5 * 104
- queries[i] == [posi, xi]
- 0 <= posi <= nums.length - 1
- -105 <= xi <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`。同时给定一个二维数组 `queries`，其中 `queries[i] = [posi, xi]`。  
对于第 `i` 条查询，先把 `nums[posi]` 的值改为 `xi`，随后计算 **该查询的答案**——即在当前数组 `nums` 中，选取的元素没有相邻（non-adjacent）的子序列（subsequence）能够得到的最大和。  
返回所有查询答案之和。由于结果可能非常大，请返回 **模 10^9 + 7** 的值。

**子序列（subsequence）** 是指可以通过删除原数组中的若干（也可以不删除）元素而得到的数组，删除操作不会改变剩余元素的相对顺序。

---

### 示例

**示例 1**  
输入: `nums = [3,5,9]`, `queries = [[1,-2],[0,-3]]`  
输出: `21`  
解释:  
- 第 1 条查询后，`nums = [3,-2,9]`，满足非相邻元素的子序列最大和为 `3 + 9 = 12`。  
- 第 2 条查询后，`nums = [-3,-2,9]`，最大和为 `9`。  
所有查询答案之和为 `12 + 9 = 21`。

**示例 2**  
输入: `nums = [0,-1]`, `queries = [[0,-5]]`  
输出: `0`  
解释: 第 1 条查询后，`nums = [-5,-1]`，选择空子序列得到的和为 `0`（空子序列也是合法的），因此答案为 `0`。

---

### 约束条件

- `1 <= nums.length <= 5 * 10^4`
- `-10^5 <= nums[i] <= 10^5`
- `1 <= queries.length <= 5 * 10^4`
- `queries[i] == [posi, xi]`
- `0 <= posi <= nums.length - 1`
- `-10^5 <= xi <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次查询后把数组重新跑一遍**，求出「不选相邻元素」的最大子序和。  
这其实和经典的「打家劫舍」问题一模一样，常用的 DP 递推式是  

```
dp[i] = max(dp[i-1] , dp[i-2] + nums[i])
```

- `dp[i]` 表示只看前 `i+1` 个数（下标 `0..i`）时能够得到的最大和。  
- `dp[i-1]` → 不选第 `i` 个元素，答案直接沿用前面的最优。  
- `dp[i-2] + nums[i]` → 选第 `i` 个元素，那么第 `i-1` 必须不选，只能把第 `i` 加到 `dp[i-2]` 上。

这就像**挑选不相邻的水果**：要么不拿当前水果，要么把当前水果和前面「间隔一个」的最优组合装进篮子。

> **数据结构类比**：这里唯一需要的「容器」是两个整数 `prev`、`prev2`（相当于「前两层记忆」），不需要额外的哈希表或树。

为什么正确？  
递推式覆盖了所有合法的选择情况：每个位置只能「选」或「不选」，且「选」时强制前一个不选，递归地把问题规模缩小两步。

**时间/空间复杂度**  
- 对每一次查询，我们都要遍历完整个数组，时间是 `O(n)`，这里的 `O(n)` 可以理解为「把数组的每个元素都看一遍」。
- 只保存两个变量，空间是 `O(1)`，即「常数级」的内存。

#### 代码（Python）

```python
MOD = 10**9 + 7
INF_NEG = -10**18          # 用来表示「不可能」的极小值

def max_non_adjacent_sum(arr):
    """
    经典「打家劫舍」DP，返回不选相邻元素的最大子序和（空子序列算 0）。
    """
    n = len(arr)
    if n == 0:
        return 0
    # prev2 = dp[i-2] , prev = dp[i-1]
    prev2 = 0                # dp[-1] = 0
    prev = max(0, arr[0])    # dp[0] = max(0, arr[0])
    for i in range(1, n):
        cur = max(prev, prev2 + arr[i])   # dp[i] 的递推式
        prev2, prev = prev, cur           # 向前滑动窗口
    return prev

def solve_brutal(nums, queries):
    ans_sum = 0
    for pos, val in queries:
        nums[pos] = val                # 直接改动原数组
        cur = max_non_adjacent_sum(nums)
        ans_sum = (ans_sum + cur) % MOD
    return ans_sum
```

#### 复杂度

- **时间复杂度**：`O(q * n)`，每次查询遍历 `n` 个元素，`q` 次查询相当于「`q` 轮遍历」。
- **空间复杂度**：`O(1)`，只用到常数个整型变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次查询都要线性遍历整个数组**。  
`n` 和 `q` 都可以高达 `5·10⁴`，`O(q·n)` 最坏会达到 `2.5·10⁹` 次运算，远远超时。

要想快，就要 **利用「局部更新」的特性**：一次查询只改动 **一个位置**，其它位置的最优子结构保持不变。  
这正是 **线段树（Segment Tree）** 的强项：把数组划分成若干区间，每个区间保存「该区间内部的最优信息」，区间合并时只用 **O(1)** 的时间。

---

#### 2.1 需要在每个区间保存什么？

我们要在合并左右子区间时判断「左区间的最右元素」和「右区间的最左元素」是否同时被选中（那就相邻了，非法）。  
因此每个区间必须记住 **「区间最左/最右元素是否被选」** 的四种组合对应的最大和：

| 左端是否选 | 右端是否选 | 含义 |
|-----------|-----------|------|
| 0         | 0         | 区间两端都 **不** 选 |
| 0         | 1         | 左端不选，右端选 |
| 1         | 0         | 左端选，右端不选 |
| 1         | 1         | 两端都选（只在长度 ≥ 2 的区间可能） |

用一个 `2×2` 的矩阵 `dp` 表示，`dp[l][r]` = 该区间在满足「左端状态 = l、右端状态 = r」时的最大和。  
如果某种状态在该区间根本不可能出现，就记成 **负无穷**（`-inf`），在合并时自然会被抛弃。

> **类比**：把每个区间想象成「一本小词典」，词典的「入口」和「出口」分别是左端、右端是否被选，`dp` 就是记录「从入口到出口」的最佳「价值」。

---

#### 2.2 区间合并

设左子区间 `L`、右子区间 `R`，它们的 `dp` 分别是 `L[i][j]`、`R[p][q]`。  
合并后得到的新区间 `M`：

```
M[a][b] = max over (j, p) where NOT (j == 1 and p == 1)  ( L[a][j] + R[p][b] )
```

解释：

- `a` = 左端是否选（来源于左子区间的左端），`b` = 右端是否选（来源于右子区间的右端）。
- `j` 是左子区间的右端状态，`p` 是右子区间的左端状态。
- 关键约束：`j` 与 `p` 同时为 `1` 表示「左子区间的最右元素」和「右子区间的最左元素」都被选了，这会导致相邻，必须排除。

因为每个矩阵只有 4 个元素，枚举 `j`、`p` 的组合最多 4 次，合并的时间是 **常数** (`O(1)`)，不随区间长度增长。

---

#### 2.3 叶子节点的初始化

单个元素 `v` 的区间长度为 1：

- 不选它 → 两端都不选，`dp[0][0] = 0`。
- 选它 → 两端都选，`dp[1][1] = v`。
- 其它组合（左选右不选、左不选右选）在长度为 1 时不可能，记成 `-inf`。

---

#### 2.4 计算答案

根节点对应整个数组。  
答案是 **四种状态的最大值**（因为根节点的两端可以随意是选或不选）：

```
ans = max(root.dp[0][0], root.dp[0][1], root.dp[1][0], root.dp[1][1])
```

空子序列的和是 `0`，而 `dp[0][0]` 本身已经保证至少是 `0`，所以不需要额外处理。

每次查询：

1. 在树上 **点更新**（把位置 `pos` 的叶子节点重新设为新值 `xi`）。  
2. 向上 **重新合并**所有受影响的父节点。  
3. 读取根节点的最大值，加到答案累计和中。

整个过程的时间是 `O(log n)`，因为线段树的高度约为 `log₂ n`。

---

#### 2.5 复杂度对比

| 方法 | 单次查询时间 | 总时间 | 空间 |
|------|--------------|--------|------|
| 暴力 DP | `O(n)` | `O(q·n)` | `O(1)` |
| 线段树 | `O(log n)` | `O((n+q)·log n)` | `O(n)`（树的节点） |

对比可以看到，**把 `n` 从 5·10⁴ 降到 `log n ≈ 16`**，从而轻松通过所有测试。

---

#### 代码（Python）

```python
MOD = 10**9 + 7
INF_NEG = -10**18               # 负无穷的代替值

class Node:
    """线段树的节点，保存 2×2 矩阵 dp"""
    __slots__ = ('dp',)
    def __init__(self, val=None):
        # dp[i][j] 表示左端状态=i，右端状态=j 时的最大和
        self.dp = [[INF_NEG, INF_NEG],
                   [INF_NEG, INF_NEG]]
        if val is not None:          # 叶子节点的初始化
            self.dp[0][0] = 0        # 不选
            self.dp[1][1] = val      # 选

def merge(left: Node, right: Node) -> Node:
    """把两个相邻区间合并成更大的区间"""
    res = Node()
    for a in (0, 1):                # 左端状态来自 left
        for b in (0, 1):            # 右端状态来自 right
            best = INF_NEG
            for j in (0, 1):        # left 区间的右端状态
                for p in (0, 1):    # right 区间的左端状态
                    # 禁止相邻两端都被选
                    if j == 1 and p == 1:
                        continue
                    cand = left.dp[a][j] + right.dp[p][b]
                    if cand > best:
                        best = cand
            res.dp[a][b] = best
    return res

class SegTree:
    """支持点更新、整体最大查询的线段树"""
    def __init__(self, arr):
        self.n = len(arr)
        # 采用 1-indexed 完全二叉树的存储方式
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        self.tree = [Node() for _ in range(2 * self.size)]
        # 初始化叶子
        for i, v in enumerate(arr):
            self.tree[self.size + i] = Node(v)
        # 自底向上构建内部节点
        for i in range(self.size - 1, 0, -1):
            self.tree[i] = merge(self.tree[i << 1], self.tree[i << 1 | 1])

    def point_update(self, idx, value):
        """把位置 idx 的值改为 value"""
        pos = self.size + idx
        self.tree[pos] = Node(value)          # 重新创建叶子节点
        pos >>= 1
        while pos:
            self.tree[pos] = merge(self.tree[pos << 1],
                                   self.tree[pos << 1 | 1])
            pos >>= 1

    def total_max(self):
        """返回整棵树（即整个数组）的最大非相邻子序和"""
        root = self.tree[1]
        return max(root.dp[0][0], root.dp[0][1],
                   root.dp[1][0], root.dp[1][1])

def solve_optimal(nums, queries):
    seg = SegTree(nums)
    ans_sum = 0
    for pos, val in queries:
        seg.point_update(pos, val)          # O(log n)
        cur = seg.total_max()               # O(1)
        ans_sum = (ans_sum + cur) % MOD
    return ans_sum
```

> **注意**  
> - `INF_NEG` 必须足够小，保证 `a + INF_NEG` 仍然是「不可能」的极小值。这里取 `-10**18` 已经远小于可能的答案范围（`|nums[i]| ≤ 10⁵，n ≤ 5·10⁴`）。  
> - `total_max` 已经把「空子序列」的情况（`0`）包含进来，因为 `dp[0][0]` 至少是 `0`。

---

#### 复杂度

- **时间复杂度**：`O((n + q)·log n)`  
  - 构建树 `O(n)`（每个节点只合并一次），  
  - 每次查询 `O(log n)`（点更新沿树高向上合并），  
  - 读取答案是 `O(1)`。  
  与暴力的 `O(q·n)` 相比，`log n` 大约是 16，提升数百倍。

- **空间复杂度**：`O(n)`  
  - 线段树最多需要 `4·n` 个节点，每个节点保存 4 个整数，属于线性空间。

---

## 心得

- **核心技巧**：使用线段树在每个区间保存「左端/右端是否被选」的四种状态，从而在 **点更新** 时只需 `O(log n)` 就能重新得到全局最优解。  
- **适用题型**  
  1. 「区间 DP 合并」类问题，例如「区间最大子序和」需要左/右端信息。  
  2. 「带约束的子序列」如「不相邻取数」或「选或不选且相邻有冲突」的动态规划。  
  3. 「区间查询 + 点修改」的最大/最小/计数类问题（如「区间最大和」配合「不能相邻」的限制）。  
- **一句话总结**：**把「相邻冲突」抽象成左右端状态，用 2×2 DP 矩阵在段树里快速合并**。

---

## 反思

- **第一反应**：看到「每次查询后都要重新求最大不相邻子序和」立刻想到 `O(n)` 的 DP。  
- **最容易踩的坑**  
  - **负数情况**：如果所有数都是负的，空子序列的和应为 `0`，要在 DP/线段树里保证不把负数当成最优答案。  
  - **状态冲突**：合并时忘记排除「左区间右端选 && 右区间左端选」的组合，会导致相邻元素被错误地同时计入。  
  - **负无穷的设定**：若取值不够小，`-inf + 正数` 可能误判为合法解。  
- **下次遇到同类题**：先判断「是否可以把约束转化为左/右端状态」，然后考虑「用线段树/树状数组保存这些状态」来实现 **点更新 + 整体查询** 的 `O(log n)` 解法。