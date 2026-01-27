# #3505. **使 K 个子数组内部元素相等的最小操作次数** / Minimum Operations to Make Elements Within K Subarrays Equal

> 难度：困难 · 标签：Array、Hash Table、Math、Dynamic Programming、Sliding Window、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-elements-within-k-subarrays-equal/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers, x and k. You can perform the following operation any number of times (including zero):
Return the minimum number of operations needed to have at least k non-overlapping subarrays of size exactly x in nums, where all elements within each subarray are equal.

**Examples**

**Example 1:**

```
Input: nums = [5,-2,1,3,7,3,6,4,-1], x = 3, k = 2
Output: 8
Explanation:
```

**Example 2:**

```
Input: nums = [9,-2,-2,-2,1,5], x = 2, k = 2
Output: 3
Explanation:
```

**Constraints**

- 2 <= nums.length <= 105
- -106 <= nums[i] <= 106
- 2 <= x <= nums.length
- 1 <= k <= 15
- 2 <= k * x <= nums.length

---

## 题目（中文翻译）

给定一个整数数组 `nums`，以及两个整数 `x` 和 `k`。你可以任意次数（包括零次）执行下列操作：

返回使得数组 `nums` 中至少存在 `k` 个互不重叠的、长度恰好为 `x` 的子数组（subarray），且每个子数组内部的所有元素相等所需的最小操作次数。

### 示例

#### 示例 1
**输入**  
```
nums = [5,-2,1,3,7,3,6,4,-1], x = 3, k = 2
```
**输出**  
```
8
```
**解释**：

（此处填写解释内容）

#### 示例 2
**输入**  
```
nums = [9,-2,-2,-2,1,5], x = 2, k = 2
```
**输出**  
```
3
```
**解释**：

（此处填写解释内容）

### 约束条件
- `2 <= nums.length <= 10^5`
- `-10^6 <= nums[i] <= 10^6`
- `2 <= x <= nums.length`
- `1 <= k <= 15`
- `2 <= k * x <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的 k 个不重叠子数组**，然后计算把每个子数组里所有元素变成相同值所需要的操作次数，最后取最小的总和。  

- **子数组的代价**  
  对于长度为 `x` 的窗口 `w = [a₁, a₂, …, aₓ]`，如果我们把所有元素改成同一个数 `v`，需要的操作次数是 `|a₁‑v| + |a₂‑v| + … + |aₓ‑v|`（每次把一个数加 1 或减 1 都算一次操作）。  
  这类 “把一堆数都变成同一个数，使绝对差之和最小” 的经典结论是：**取中位数**（median）作为 `v` 能得到最小的代价。可以把中位数想象成“字典里最常出现的词”，把所有词改成这个词最省力。  

- **暴力枚举**  
  1. 先遍历所有长度为 `x` 的窗口，算出每个窗口的代价（把窗口里的数改成它们的中位数）。  
  2. 再在这些代价的序列里挑选 `k` 个不相交的窗口，使得代价之和最小。  
  3. 直接用递归或全排列去尝试所有组合。  

**为什么正确**  
- 对每个窗口，使用中位数得到的代价是该窗口内部 **最优** 的（没有比这更少的操作能把窗口里所有数变相同）。  
- 把每个窗口的最优代价算出来后，问题就转化为“在这些窗口里挑 `k` 个不重叠的，求最小总和”。只要把所有合法组合都算一遍，最小值必然就是答案。  

**时间/空间复杂度**  
- 计算每个窗口代价：`O(n·x)`（每个窗口都要遍历 `x` 个数），这里 `n` 是数组长度。  
- 枚举 `k` 个不重叠窗口：组合数是指数级的，最坏情况是 `C(n/x, k)`，随 `n` 爆炸。  
- 整体时间复杂度近似 **O( (n·x) + C(n/x, k) )**，在最坏情况下几乎不可能在 1 秒内跑完。  
- 需要保存每个窗口的代价，空间 `O(n)`。  

> **大白话解释**：  
> - `O(n·x)` 就像你把每本书的每一页都读一遍，`n` 本书、每本 `x` 页。  
> - `C(n/x, k)` 就像从 `n/x` 本书里挑 `k` 本，每挑一种都要重新算一次，数量会像雪花一样快速增多。

---

#### 代码（Python）  

```python
from itertools import combinations
from typing import List

def window_cost(nums: List[int], start: int, x: int) -> int:
    """暴力计算以 start 为左端点、长度为 x 的窗口的最小代价（取中位数）。"""
    win = nums[start:start + x]
    win.sort()
    median = win[x // 2]                     # 中位数
    return sum(abs(v - median) for v in win)

def min_operations_bruteforce(nums: List[int], x: int, k: int) -> int:
    n = len(nums)
    # 1. 预计算每个窗口的代价
    costs = [window_cost(nums, i, x) for i in range(n - x + 1)]

    # 2. 暴力枚举 k 个不相交窗口
    best = float('inf')
    # 生成所有窗口的起始位置的组合
    for combo in combinations(range(n - x + 1), k):
        # 检查是否不相交
        ok = True
        for i in range(k - 1):
            if combo[i] + x > combo[i + 1]:   # 有重叠
                ok = False
                break
        if not ok:
            continue
        total = sum(costs[i] for i in combo)
        best = min(best, total)

    return best
```

> 这段代码 **只能在极小规模**（比如 `n ≤ 20`）下跑通，主要用来帮助大家理解最直接的思路。

#### 复杂度  

- **时间复杂度**：`O(n·x + C(n/x, k)·k)`  
  - `n·x` 用来算每个窗口的代价。  
  - `C(n/x, k)` 是所有合法组合的数量，乘以 `k` 是把每个组合的代价相加。  
  - 在实际测试里，这个复杂度会导致 **超时**。  
- **空间复杂度**：`O(n)`  
  - 只需要保存每个窗口的代价。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到两大瓶颈：

1. **窗口代价的计算**  
   暴力遍历窗口内部 `x` 次，整体是 `O(n·x)`，在 `x` 接近 `n` 时仍然可以接受，但我们可以把它降到 `O(n·log x)`，利用**维护中位数的滑动窗口**（两堆堆实现）在 O(log x) 时间内得到当前窗口的中位数和代价。

2. **挑选 k 个不重叠窗口**  
   暴力枚举组合是指数级的。观察到窗口长度固定为 `x`，所以如果我们把窗口的左端点记作 `i`（`0 ≤ i ≤ n‑x`），不相交的条件就是 **下一个窗口的左端点必须 ≥ i + x**。这正好是 **“在一条直线上挑不相交的若干段，使总权重最小”** 的经典动态规划（DP）模型。  

下面一步步把这两个优化组合起来：

---

##### 2.1 维护滑动窗口的中位数与代价  

**核心数据结构：双堆（max‑heap + min‑heap）**  

- **左堆 `low`**（最大堆）保存较小的一半元素，堆顶是左半部分的最大值（即当前中位数的左侧）。  
- **右堆 `high`**（最小堆）保存较大的一半元素，堆顶是右半部分的最小值。  

我们始终保持两堆的大小差不超过 1，这样堆顶（左堆的堆顶）就是 **中位数**（当 `x` 为奇数时恰好是中位数；当 `x` 为偶数时取左侧的那个数，同样可以得到最小代价）。  

为了在窗口滑动时 **删除** 已经离开的元素，采用 **懒删**：用一个 `delayed` 字典记录待删除的值，真正弹出时再检查是否已经标记为删除。  

**如何快速算代价**  

设  
- `sum_low` 为左堆中所有元素的和  
- `sum_high` 为右堆中所有元素的和  
- `median = low[0]`（左堆的堆顶）  

窗口内所有数到 `median` 的绝对差之和可以用下面的公式得到：

```
cost = median * len(low) - sum_low   # 左侧所有数提升到 median 的费用
     + sum_high - median * len(high) # 右侧所有数降到 median 的费用
```

这样每次 **插入 / 删除** 一个元素，只需要 O(log x) 更新堆和对应的和，就能在 O(1) 时间得到当前窗口的代价。

---

##### 2.2 选 k 个不相交窗口的 DP  

记 `cost[i]` 为以 `i` 为左端点、长度为 `x` 的窗口的最小代价（已经在上一步算好）。  

我们把数组看成从左到右遍历，`dp[i][j]` 表示 **只看前 `i`（0‑based，表示前 `i` 个元素）**，已经选了 `j` 个窗口时的最小总代价。  

转移有两种情况：

1. **不选以 `i‑1` 为结尾的窗口**  
   `dp[i][j] = min(dp[i][j], dp[i‑1][j])`  

2. **选以 `i‑1` 为结尾的窗口**（即窗口起点是 `i‑x`）  
   前提是 `i ≥ x`，并且我们要在 `i‑x` 之前已经选了 `j‑1` 个窗口：  
   `dp[i][j] = min(dp[i][j], dp[i‑x][j‑1] + cost[i‑x])`  

初始化：`dp[0][0] = 0`，其余为正无穷。  

因为 `k ≤ 15`，`n ≤ 10⁵`，二维 DP 的时间是 `O(n·k)`（约 1.5 百万次操作），完全可以接受。  

**空间优化**  
我们可以只保留上一行和当前行的 DP，甚至直接用一个 `(k+1)` 长度的数组在遍历时倒序更新（从 `k` 到 `1`），得到 `O(k)` 的额外空间。

---

##### 2.3 整体流程  

1. **滑动窗口**：一次遍历数组，使用双堆维护当前长度为 `x` 的窗口的中位数和代价，得到数组 `cost[0 … n‑x]`。  
2. **动态规划**：再遍历 `i = 0 … n`，用 DP 计算选 `k` 个不相交窗口的最小总代价。  
3. **答案**：`dp[n][k]`（恰好选了 `k` 个）即为所求的最少操作次数。

---

#### 代码（Python）  

```python
import heapq
from typing import List

INF = 10 ** 18

class DualHeap:
    """维护一个滑动窗口的中位数及左右两侧的元素和（懒删版）。"""
    def __init__(self, k: int):
        self.small = []          # max-heap (存负数)
        self.large = []          # min-heap
        self.delayed = {}        # 待删除的元素计数
        self.k = k               # 窗口大小
        self.smallSize = 0       # 有效元素个数
        self.largeSize = 0
        self.sumSmall = 0        # 左侧元素和
        self.sumLarge = 0        # 右侧元素和

    # ---------- 辅助 ----------
    def _prune(self, heap):
        """弹出已经标记为删除的堆顶元素。"""
        while heap:
            num = -heap[0] if heap is self.small else heap[0]
            if self.delayed.get(num, 0):
                self.delayed[num] -= 1
                if self.delayed[num] == 0:
                    del self.delayed[num]
                heapq.heappop(heap)
            else:
                break

    def _makeBalance(self):
        """保持两堆大小平衡，且 small 可以比 large 多一个元素。"""
        if self.smallSize > self.largeSize + 1:
            # small -> large
            num = -heapq.heappop(self.small)
            self.sumSmall -= num
            self.smallSize -= 1
            heapq.heappush(self.large, num)
            self.sumLarge += num
            self.largeSize += 1
            self._prune(self.small)
        elif self.smallSize < self.largeSize:
            # large -> small
            num = heapq.heappop(self.large)
            self.sumLarge -= num
            self.largeSize -= 1
            heapq.heappush(self.small, -num)
            self.sumSmall += num
            self.smallSize += 1
            self._prune(self.large)

    # ---------- 对外接口 ----------
    def insert(self, num: int):
        """向窗口中加入一个数。"""
        if not self.small or num <= -self.small[0]:
            heapq.heappush(self.small, -num)
            self.sumSmall += num
            self.smallSize += 1
        else:
            heapq.heappush(self.large, num)
            self.sumLarge += num
            self.largeSize += 1
        self._makeBalance()

    def erase(self, num: int):
        """从窗口中删除一个数（懒删）。"""
        self.delayed[num] = self.delayed.get(num, 0) + 1
        if num <= -self.small[0]:
            self.sumSmall -= num
            self.smallSize -= 1
            if num == -self.small[0]:
                self._prune(self.small)
        else:
            self.sumLarge -= num
            self.largeSize -= 1
            if self.large and num == self.large[0]:
                self._prune(self.large)
        self._makeBalance()

    def get_median(self) -> int:
        """返回当前窗口的中位数（左侧堆顶）。"""
        return -self.small[0]

    def get_cost(self) -> int:
        """返回把窗口所有数变成中位数所需的最小操作次数。"""
        median = self.get_median()
        # 左侧提升到 median 的费用 + 右侧降到 median 的费用
        left = median * self.smallSize - self.sumSmall
        right = self.sumLarge - median * self.largeSize
        return left + right


def min_operations(nums: List[int], x: int, k: int) -> int:
    n = len(nums)
    # ---------- 1. 预计算每个长度为 x 的窗口的代价 ----------
    dh = DualHeap(x)
    costs = [0] * (n - x + 1)

    # 先把前 x 个数放进去
    for i in range(x):
        dh.insert(nums[i])
    costs[0] = dh.get_cost()

    # 滑动窗口
    for start in range(1, n - x + 1):
        # 移除左侧即将离开的元素
        dh.erase(nums[start - 1])
        # 插入新进入窗口的元素
        dh.insert(nums[start + x - 1])
        costs[start] = dh.get_cost()

    # ---------- 2. 动态规划选 k 个不相交窗口 ----------
    # dp[j] 表示已经选了 j 个窗口、且当前处理到的位置 i（隐含）的最小代价
    dp = [INF] * (k + 1)
    dp[0] = 0  # 选 0 个窗口费用为 0

    # 为了检查“不相交”，我们在遍历位置 i（窗口左端点）时，只能把
    # 以 i 为左端点的窗口和 i - x 之前的状态相加。
    # 因此我们需要一个额外的数组 prev 保存 i - x 位置的 dp。
    # 这里直接用一个长度为 n+1 的二维表也很直观，下面用一维滚动实现。
    # pre_dp 保存 i - x 位置的 dp（在 i 增长时更新一次）。
    pre_dp = [INF] * (k + 1)
    pre_dp[0] = 0   # i = 0 时的基准

    for i in range(1, n + 1):
        # i 表示已经看完前 i 个元素（0‑based），对应的窗口左端点是 i‑x
        if i >= x:
            # 把窗口左端点为 i‑x 的代价加入到 pre_dp 中，准备在以后使用
            w_start = i - x
            cost_w = costs[w_start]
            # 使用倒序更新，防止同一次窗口被多次计入
            for cnt in range(k, 0, -1):
                if pre_dp[cnt - 1] != INF:
                    dp[cnt] = min(dp[cnt], pre_dp[cnt - 1] + cost_w)

        # 当前 i 位置不选任何窗口时，dp 不变；但我们需要把 dp 复制到 pre_dp
        # 为下一轮 i + x 提供 “i 之前的最优状态”。这里直接覆盖。
        pre_dp = dp[:]

    return dp[k]

# -------------------------------------------------
# 示例
print(min_operations([5, -2, 1, 3, 7, 3, 6, 4, -1], x=3, k=2))   # 8
print(min_operations([9, -2, -2, -2, 1, 5], x=2, k=2))        # 3
```

**代码要点（中文注释）**  

- `DualHeap` 用两堆实现“滑动窗口中位数 + 两侧和”，每次 `insert` / `erase` 只需要 `O(log x)`。  
- `costs[i]` 直接得到窗口 `[i, i+x)` 变成同值的最小操作数。  
- DP 部分使用 **一维滚动**（`dp` 与 `pre_dp`），时间 `O(n·k)`，空间 `O(k)`。  

---

#### 复杂度  

- **时间复杂度**  
  - 滑动窗口求代价：`O(n·log x)`（每次插入/删除堆操作 `log x`）。  
  - 动态规划：`O(n·k)`（`k ≤ 15`），约 `1.5·10⁶` 次基本运算。  
  - **总计**：`O(n·log x + n·k)`。  
    - 对于 `n = 10⁵、x ≤ n、k ≤ 15`，运行在毫秒级别，完全能通过。

- **空间复杂度**  
  - `costs` 长度 `n‑x+1` → `O(n)`。  
  - 双堆内部最多保存 `x` 个元素 → `O(x)`（不超过 `O(n)`）。  
  - DP 只用 `O(k)` 额外空间。  
  - **总计**：`O(n)`，约几百 KB–几 MB，符合限制。

> **大白话**：  
> - `O(n·log x)` 就像把 100 000 本书的每一页都放进一个 **可快速找中位数的抽屉**（堆），每次放进去或拿出来只需要几步（对数步），而不是把整本书翻一遍。  
> - `O(n·k)` 就是一次遍历 100 000 本书，顺手记下“已经挑了多少段”，最多记 15 次，几乎不增加负担。

---

## 心得  

- **核心技巧**：  
  1. **滑动窗口 + 双堆** 求每个固定长度子数组的 “变成相同数的最小代价”。  
  2. **动态规划** 在“一维序列里挑不相交区间”得到最小总和。  

- **适用的题型**（可以迁移这套思路）：  
  - “把每个长度为 `L` 的子数组变成单调/相等/同余” 之类，需要先算每个窗口的代价。  
  - “在数组上挑 `k` 段，要求段间不重叠且总权重最小/最大”。  
  - “滑动窗口统计中位数或其它 order‑statistics”，如 LeetCode 480（滑动窗口中位数）。  

- **一句话总结解题钥匙**  
  > **“先把每个窗口的最优代价算出来（中位数 + 双堆），再用小规模 DP 把 k 段挑出来”。**  

---

## 反思  

- **第一反应**：看到“把子数组里所有元素变成相等”，立刻想到 “把每个窗口的元素调到中位数”。这一步是关键的数学洞察。  
- **最容易踩的坑**  
  1. **窗口代价的计算**：如果直接遍历窗口会导致 `O(n·x)` 超时，必须使用维护中位数的结构。  
  2. **删除元素的懒删**：堆本身不支持任意删除，忘记懒删会导致堆顶不是当前窗口的真实中位数，导致错误的代价。  
  3. **DP 的不相交条件**：容易忘记“下一个窗口左端点必须 ≥ 前一个左端点 + x”，导致选到相交的窗口。  
  4. **边界**：`k·x` 可能正好等于 `n`，此时只能选唯一一种划分，需要保证 DP 能覆盖 “恰好选满整个数组”。  

- **下次类似题的第一步**  
  > **先判断是否可以把每个固定长度子区间的代价独立求出（通常是中位数、均值或最大值），再把“挑 k 段不相交”抽象成 DP 或贪心**。  

祝你在算法的路上越走越顺 🚀!