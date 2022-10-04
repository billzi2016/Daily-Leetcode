# #1959. K 次调整大小操作下的最小总空间浪费 / Minimum Total Space Wasted With K Resizing Operations

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-total-space-wasted-with-k-resizing-operations/)

---

## 题目（英文原版）

**Description**

You are currently designing a dynamic array. You are given a 0-indexed integer array nums, where nums[i] is the number of elements that will be in the array at time i. In addition, you are given an integer k, the maximum number of times you can resize the array (to any size).
The size of the array at time t, sizet, must be at least nums[t] because there needs to be enough space in the array to hold all the elements. The space wasted at time t is defined as sizet - nums[t], and the total space wasted is the sum of the space wasted across every time t where 0 <= t < nums.length.
Return the minimum total space wasted if you can resize the array at most k times.
Note: The array can have any size at the start and does not count towards the number of resizing operations.

**Examples**

**Example 1:**

```
Input: nums = [10,20], k = 0
Output: 10
Explanation: size = [20,20].
We can set the initial size to be 20.
The total wasted space is (20 - 10) + (20 - 20) = 10.
```

**Example 2:**

```
Input: nums = [10,20,30], k = 1
Output: 10
Explanation: size = [20,20,30].
We can set the initial size to be 20 and resize to 30 at time 2. 
The total wasted space is (20 - 10) + (20 - 20) + (30 - 30) = 10.
```

**Example 3:**

```
Input: nums = [10,20,15,30,20], k = 2
Output: 15
Explanation: size = [10,20,20,30,30].
We can set the initial size to 10, resize to 20 at time 1, and resize to 30 at time 3.
The total wasted space is (10 - 10) + (20 - 20) + (20 - 15) + (30 - 30) + (30 - 20) = 15.
```

**Constraints**

- 1 <= nums.length <= 200
- 1 <= nums[i] <= 106
- 0 <= k <= nums.length - 1

---

## 题目（中文翻译）

你正在设计一个动态数组。给定一个下标从 0 开始的整数数组 `nums`，其中 `nums[i]` 表示第 `i` 时刻数组中将会出现的元素个数。此外，还给定一个整数 `k`，表示你最多可以对数组进行 `k` 次调整大小（可以调整为任意大小）。

数组在时刻 `t` 的大小 `size_t` 必须不少于 `nums[t]`，因为需要足够的空间容纳所有元素。时刻 `t` 的空间浪费定义为 `size_t - nums[t]`，总空间浪费是所有 `0 ≤ t < nums.length` 时的空间浪费之和。

返回在至多进行 `k` 次调整大小的情况下能够达到的最小总空间浪费。

**注意**：数组初始时可以任意大小，该初始大小不计入调整次数。

## 示例

### 示例 1
**输入**  
`nums = [10,20], k = 0`  

**输出**  
`10`  

**解释**  
`size = [20,20]`。我们可以把初始大小设为 20。  
总空间浪费为 `(20 - 10) + (20 - 20) = 10`。

### 示例 2
**输入**  
`nums = [10,20,30], k = 1`  

**输出**  
`10`  

**解释**  
`size = [20,20,30]`。我们可以把初始大小设为 20，并在时刻 2 将大小调整为 30。  
总空间浪费为 `(20 - 10) + (20 - 20) + (30 - 30) = 10`。

### 示例 3
**输入**  
`nums = [10,20,15,30,20], k = 2`  

**输出**  
`15`  

**解释**  
`size = [10,20,20,30,30]`。我们可以把初始大小设为 10，在时刻 1 调整为 20，时刻 3 再调整为 30。  
总空间浪费为 `(10 - 10) + (20 - 20) + (20 - 15) + (30 - 30) + (30 - 20) = 15`。

## 约束

- `1 <= nums.length <= 200`
- `1 <= nums[i] <= 10^6`
- `0 <= k <= nums.length - 1`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每一次“重新分配大小”看成一次分段**。  
- 如果我们最多可以 `k` 次重新分配（resize），那么整个时间轴会被划分成 **`k+1` 段**。  
- 在同一段里，数组的容量保持不变，必须足够大以容纳该段所有时刻的元素数 `nums[t]`。  
- 为了浪费最少，我们会把这段的容量设成该段里最大值 `max(nums[l…r])`。  
- 这段的浪费 = `段长 × 最大值 - 这段所有元素之和`。  

于是问题就变成：**把数组划分成至多 `k+1` 段，使得每段的浪费之和最小**。

暴力解法就是**枚举所有可能的划分方式**，逐个计算总浪费，取最小值。  

> 类比：把一根绳子切成几段，每段要装进一个盒子，盒子的大小必须大于等于这段绳子的最长长度，盒子里空余的空间就是浪费。我们要把绳子切得合适，使得所有盒子的空余空间最小。

为什么正确？  
- 每一种合法的划分对应唯一的一套 “什么时候 resize、resize 成多大”。  
- 计算每段的最优容量（最大值）必然是该段浪费的下界。  
- 因此遍历所有划分必然能得到全局最优。

**时间/空间复杂度**  
- 枚举划分等价于在 `n-1` 条“切割线”里选 `k` 条（或者更少），组合数是 `C(n-1, k)`，在最坏情况下（`k≈n/2`）指数级增长，约为 `O(n^k)`，对 `n≤200` 完全不可接受。  
- 计算每段浪费时需要遍历该段，最坏 `O(n)`，所以整体时间更高。  
- 只用常数级的额外空间 `O(1)`（不计递归栈）。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def minWastedSpace_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    # 预先算好前缀和，后面快速求段和
    pref = [0]
    for x in nums:
        pref.append(pref[-1] + x)   # pref[i] = nums[0] + ... + nums[i-1]

    # 计算段 [l, r]（含两端）的浪费
    def waste(l: int, r: int) -> int:
        seg_max = max(nums[l:r+1])          # 段内最大值
        seg_sum = pref[r+1] - pref[l]       # 段和
        return (r - l + 1) * seg_max - seg_sum

    best = float('inf')
    # 选取 0~n-2 之间的切点，切点数量 ≤ k
    cuts_positions = list(range(n-1))
    for cut_cnt in range(k+1):                     # 可以少于 k 次 resize
        for cuts in combinations(cuts_positions, cut_cnt):
            # 把切点转成实际的段区间
            prev = 0
            total = 0
            for c in cuts + (n-1,):               # 最后一个“切点”是数组末尾
                total += waste(prev, c)
                prev = c + 1
            best = min(best, total)
    return best
```

> 关键行注释已写在代码里。该实现只能在非常小的 `n`（如 `n≤15`）下跑通，用来帮助大家理解除“枚举所有划分”到底长什么样。

#### 复杂度  

- 时间复杂度：`O( C(n-1,0)+C(n-1,1)+…+C(n-1,k) * n )`，在最坏情况下接近指数级 `≈ O(n^k)`，不可接受。  
- 空间复杂度：`O(1)`（不计递归或 `itertools` 产生的迭代器），仅用了常数级额外变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于枚举所有划分**。  
我们注意到：

1. **每段的浪费只和段的左端点、右端点有关**（只需要段内最大值和段和）。  
2. 当我们已经决定了前 `i` 个时间点的最优划分，并且知道用了多少次 resize，**后面的选择只和当前位置 `i` 以及剩余的 resize 次数有关**。

这正好符合**动态规划**（Dynamic Programming）的特点：把大问题拆成子问题，子问题的解可以复用。

##### 状态定义  

- `dp[t][i]` = 前 `i+1`（即下标 `0…i`）个时间点，**恰好使用了 `t` 次 resize**（即 `t+1` 段）时的最小总浪费。  
  - `t` 的取值范围 `0 … k`。  
  - `i` 的取值范围 `0 … n-1`。

##### 初始状态  

- 当 `t = 0`（不进行任何 resize）时，整个前缀必须使用同一个容量，即 **只划分成一段**。  
  - `dp[0][i] = waste(0, i)`，直接用第 0 段到第 `i` 的浪费。

##### 转移方程  

假设我们在位置 `i` 结束第 `t` 次 resize（也就是说第 `t` 段的右端点是 `i`），  
则第 `t` 段的左端点一定是某个 `p+1`（`p < i`），而前 `p` 个位置已经用了 `t-1` 次 resize。  

\[
dp[t][i] = \min_{0 \le p < i} \big( dp[t-1][p] + waste(p+1, i) \big)
\]

- `dp[t-1][p]`：前 `p+1` 个位置的最优解（用了 `t-1` 次 resize）。  
- `waste(p+1, i)`：第 `t` 段（从 `p+1` 到 `i`）的浪费。

##### 结果  

我们可以最多使用 `k` 次 resize，所以答案是 `min_{t=0..k} dp[t][n-1]`。  
但因为 `dp[t][i]` 随着 `t` 增大只能不增（多一次 resize 只会让浪费更少或相等），直接取 `dp[k][n-1]` 即可。

##### 预处理 `waste(l, r)`  

直接在转移时每次遍历 `[l, r]` 计算最大值和和会导致 `O(k n^3)`。  
我们可以 **提前算好所有区间的浪费**：

1. 用前缀和 `pref` 快速得到任意区间和。  
2. 对每个左端点 `l`，向右扩展时维护当前最大值 `cur_max`，这样在 `O(1)` 时间内得到 `waste(l, r)`。  
   - 时间复杂度 `O(n^2)`，空间 `O(n^2)`（`n ≤ 200`，完全可以接受）。

##### 复杂度对比  

- 暴力解：指数级时间。  
- 动态规划：`O(k * n^2)` 时间，`O(k * n)` 或 `O(n^2)` 空间。  
  - 对于本题最大 `n = 200`、`k ≤ 199`，最多约 `200 * 200^2 = 8,000,000` 次基本操作，毫秒级可跑完。

#### 代码（Python）

```python
from typing import List

def minWastedSpace(nums: List[int], k: int) -> int:
    n = len(nums)

    # ---------- 1. 预处理：区间和 ----------
    pref = [0] * (n + 1)                 # pref[i] = nums[0] + ... + nums[i-1]
    for i in range(n):
        pref[i + 1] = pref[i] + nums[i]

    # ---------- 2. 预处理：区间浪费 waste[l][r] ----------
    # waste[l][r] = (r-l+1) * max(nums[l..r]) - sum(nums[l..r])
    waste = [[0] * n for _ in range(n)]
    for l in range(n):
        cur_max = 0
        for r in range(l, n):
            cur_max = max(cur_max, nums[r])          # 维护区间最大值
            seg_sum = pref[r + 1] - pref[l]          # 区间和（O(1)）
            waste[l][r] = (r - l + 1) * cur_max - seg_sum

    # ---------- 3. 动态规划 ----------
    # dp[t][i] = 前 i+1 个元素，恰好用了 t 次 resize（t+1 段）的最小浪费
    INF = 10 ** 18
    dp = [[INF] * n for _ in range(k + 1)]

    # base: t = 0 (不做任何 resize)
    for i in range(n):
        dp[0][i] = waste[0][i]

    # 逐步增加可用的 resize 次数
    for t in range(1, k + 1):
        for i in range(n):
            # 第 t 段的右端点是 i，左端点可以是任意 p+1 (p < i)
            # 需要遍历所有可能的分割点 p
            best = INF
            for p in range(t - 1, i):   # p 必须至少有 t-1 个元素来容纳前 t-1 段
                cand = dp[t - 1][p] + waste[p + 1][i]
                if cand < best:
                    best = cand
            dp[t][i] = best

    # 结果：最多 k 次 resize，即使用 k 次或更少
    return dp[k][n - 1]
```

**代码要点解释**  

- `pref` 用来 **瞬间求区间和**，相当于查字典的“页码”。  
- `waste[l][r]` 的预计算把 “找最大值” 与 “求和” 合并到一次双层循环中，时间是 `O(n^2)`，空间也是 `O(n^2)`。  
- DP 中的 `for p in range(t-1, i)`：  
  - `t-1` 是最小可能的左端点位置，保证前面已经划分出 `t` 段（每段至少一个元素）。  
- `INF` 是一个足够大的数，防止未初始化的状态参与最小值比较。

#### 复杂度  

- 时间复杂度：`O(k * n^2)`  
  - 预处理 `waste`：`O(n^2)`  
  - DP 双层循环：`k` 次外层，`n` 次内层，再遍历 `p`（最坏 `n`），合计 `O(k n^2)`。  
  - 对于 `n ≤ 200`、`k ≤ 199`，约 8 × 10⁶ 次基本运算，运行毫秒级。  
- 空间复杂度：`O(n^2 + k n)`  
  - `waste` 矩阵 `O(n^2)`（≈ 40 KB）  
  - DP 表 `O(k n)`，在本题同样在几百 KB 量级，完全可接受。

---

## 心得  

- **核心技巧**：把“最多 K 次重新分配”转化为“把序列划分成最多 K+1 段”，然后用 **区间预处理 + 动态规划** 求最小代价。  
- **适用的题型**  
  1. “分割数组使代价最小”系列，如 LeetCode 1470（**重新排列数组**）  
  2. “划分为若干段，每段代价由区间特征决定” 如 “分割数组的最大和” 题目  
  3. “有限次操作（重置、切换）导致的最小损失” 类似 “Minimum Cost to Split Array”。  
- **一句话总结解题钥匙**：**把每一次 resize 看成一次切割点，预先算好所有区间的代价，再用 DP 按切割点递推最小总浪费**。

---

## 反思  

- **第一反应**：直接模拟所有可能的切割组合（暴力），但很快意识到组合数会爆炸。  
- **最容易踩的坑**  
  - **边界条件**：`t` 次 resize 对应 `t+1` 段，DP 初始化时必须把 `dp[0][i]` 设为整段的浪费。  
  - **分割点合法性**：在第 `t` 次 resize 时，左边至少已经形成 `t` 段，故 `p` 的起始下标要是 `t-1`，否则会出现空段。  
  - **整数溢出**：`nums[i] ≤ 10⁶，n ≤ 200`，最大浪费约 `200 * 10⁶ = 2·10⁸`，使用 Python 的 `int` 完全安全，但在其他语言需要使用 64 位整数。  
- **下次类似题目第一步**：**先问自己：可以把问题抽象成“把序列划分为若干段，每段有固定代价”，再考虑是否可以预处理代价并使用 DP**。这样可以迅速定位到区间预处理 + DP 的解法框架。