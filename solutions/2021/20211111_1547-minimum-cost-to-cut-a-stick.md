# #1547. **切木棍的最小费用** / Minimum Cost to Cut a Stick

> 难度：困难 · 标签：Array、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-cut-a-stick/)

---

## 题目（英文原版）

**Description**

Given a wooden stick of length n units. The stick is labelled from 0 to n. For example, a stick of length 6 is labelled as follows:
Given an integer array cuts where cuts[i] denotes a position you should perform a cut at.
You should perform the cuts in order, you can change the order of the cuts as you wish.
The cost of one cut is the length of the stick to be cut, the total cost is the sum of costs of all cuts. When you cut a stick, it will be split into two smaller sticks (i.e. the sum of their lengths is the length of the stick before the cut). Please refer to the first example for a better explanation.
Return the minimum total cost of the cuts.

**Examples**

**Example 1:**

```
Input: n = 7, cuts = [1,3,4,5]
Output: 16
Explanation: Using cuts order = [1, 3, 4, 5] as in the input leads to the following scenario:

The first cut is done to a rod of length 7 so the cost is 7. The second cut is done to a rod of length 6 (i.e. the second part of the first cut), the third is done to a rod of length 4 and the last cut is to a rod of length 3. The total cost is 7 + 6 + 4 + 3 = 20.
Rearranging the cuts to be [3, 5, 1, 4] for example will lead to a scenario with total cost = 16 (as shown in the example photo 7 + 4 + 3 + 2 = 16).
```

**Example 2:**

```
Input: n = 9, cuts = [5,6,1,4,2]
Output: 22
Explanation: If you try the given cuts ordering the cost will be 25.
There are much ordering with total cost <= 25, for example, the order [4, 6, 5, 2, 1] has total cost = 22 which is the minimum possible.
```

**Constraints**

- 2 <= n <= 106
- 1 <= cuts.length <= min(n - 1, 100)
- 1 <= cuts[i] <= n - 1
- All the integers in cuts array are distinct.

---

## 题目（中文翻译）

给定一根长度为 `n` 单位的木棍，木棍的坐标从 `0` 到 `n` 标记。例如，长度为 `6` 的木棍标记如下：

```
0 ---- 1 ---- 2 ---- 3 ---- 4 ---- 5 ---- 6
```

给定一个整数数组 `cuts`，其中 `cuts[i]` 表示需要在该位置进行一次切割。你可以自行决定切割的顺序，而不是必须按数组顺序进行。

一次切割的费用等于被切割木棍的长度，所有切割的费用之和即为总费用。每次切割会把一根木棍分成两根更短的木棍（即两根木棍长度之和等于切割前的长度），请参考第一个示例获得更直观的理解。

返回能够完成所有切割的 **最小总费用**。

---

### 示例

**示例 1**

> **输入**: `n = 7`, `cuts = [1,3,4,5]`  
> **输出**: `16`  
> **解释**: 按照切割顺序 `[1, 3, 4, 5]`（即输入顺序）进行时，情况如下：

- 第一次切割在长度为 `7` 的木棍上，费用为 `7`。  
- 第二次切割在长度为 `6` 的木棍上（即第一次切割后得到的第二段），费用为 `6`。  
- 第三次切割在长度为 `4` 的木棍上，费用为 `4`。  
- 最后一次切割在长度为 `3` 的木棍上，费用为 `3`。  

总费用为 `7 + 6 + 4 + 3 = 20`。通过重新安排切割顺序可以将总费用降低到 `16`，这就是最小可能费用。

---

**示例 2**

> **输入**: `n = 9`, `cuts = [5,6,1,4,2]`  
> **输出**: `22`  
> **解释**: 若按照给定的切割顺序进行，费用为 `25`。存在多种切割顺序的总费用不超过 `25`，例如顺序 `[4, 6, 5, 2, 1]` 的总费用为 `22`，这就是可以达到的最小费用。

---

### 约束条件

- `2 <= n <= 10^6`
- `1 <= cuts.length <= min(n - 1, 100)`
- `1 <= cuts[i] <= n - 1`
- `cuts` 数组中的所有整数互不相同。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把所有切割的顺序都枚举一遍**，把每一种顺序对应的花费算出来，最后取最小值。  

- **数据结构**：  
  - `cuts` 本身是一个整数列表，存放所有要切的位置。  
  - 为了遍历所有顺序，我们可以使用 Python 的 `itertools.permutations`，它会把列表的元素全部排成不同的排列，就像把一副扑克牌的顺序全都洗出来一样。  

- **为什么能得到正确答案**：  
  - 题目只要求“可以随意改变切割顺序”，因此**每一种合法的顺序都是可能的**。只要我们把所有顺序的费用算完，最小的那个必然就是答案。  

- **时间/空间复杂度的大白话**：  
  - 假设要切的点有 `m` 个（`m = len(cuts)`），把它们全部排成不同的顺序相当于把 `m` 本不同的书排成一排，有 `m!`（m 的阶乘）种可能。  
  - 对每一种顺序，我们需要模拟一次切割，最多遍历 `m` 次来累计费用。  
  - 所以 **时间复杂度是 O(m! × m)**，这在 `m = 6` 时已经是 720 × 6 ≈ 4000 步，但当 `m = 10` 时就会变成 3.6 million × 10，完全不可接受。  
  - **空间复杂度**只用到常数级的临时变量（比如当前费用），所以是 **O(1)**。  

#### 代码（Python）  

```python
import itertools
from typing import List

def minCost_bruteforce(n: int, cuts: List[int]) -> int:
    """
    暴力枚举所有切割顺序，返回最小总费用。
    """
    best = float('inf')                     # 记录目前找到的最小费用
    for order in itertools.permutations(cuts):
        cost = 0
        segments = [(0, n)]                 # 初始只有一根完整的木棍，用 (左端点, 右端点) 表示
        for cut in order:                   # 按当前排列的顺序依次切割
            # 找到 cut 落在哪根当前的木棍上
            for i, (l, r) in enumerate(segments):
                if l < cut < r:             # cut 必须在两端点之间
                    cost += r - l           # 本次切割费用 = 当前木棍长度
                    # 把这根木棍拆成两段，替换掉原来的
                    segments[i] = (l, cut)
                    segments.insert(i + 1, (cut, r))
                    break
        best = min(best, cost)              # 更新最小费用
    return best
```

> **代码说明**  
> - `segments` 用来保存当前所有未切完的木棍，每根木棍用左、右端点表示。  
> - 对每个 `cut`，我们线性遍历 `segments` 找到它所在的那根木棍，然后把这根木棍分成两段并累计费用。  
> - 最后取所有排列中的最小费用返回。

#### 复杂度  

- **时间复杂度**：`O(m! × m)`  
  - “`m!`” 表示所有排列的数量，`m` 表示每次遍历当前木棍列表的代价。对初学者来说，可以把它想象成“先把所有可能的排队顺序列出来（很多很多），再对每个顺序逐个检查”。  
- **空间复杂度**：`O(1)`（不计输入和输出）  
  - 只用到几个临时变量和一个最多长 `m` 的 `segments` 列表，大小不随递归或额外数据结构增长。

---

### 2. 最优解  

#### 思路  

从暴力解我们看到 **瓶颈在于枚举所有顺序**，而实际上**切割的顺序只决定了每一次切割时所在的“区间长度”**。如果我们能把“在某个区间内完成所有切割的最小费用”记下来，就可以把大问题拆成小问题，避免枚举。

**核心思想：区间动态规划（Interval DP）**  
- 把木棍看成一条数轴，切点把它划分成若干区间。  
- 对任意两个相邻的切点（或端点 0、n）之间的区间 `[i, j]`，我们记 `dp[i][j]` 为**在这段区间内完成所有内部切点的最小费用**。  
- 当我们在区间 `[i, j]` 内挑选一个切点 `k`（`i < k < j`）先切时，当前这一次切割的费用是整个区间的长度 `cuts[j] - cuts[i]`（因为此时这根木棍还没有被分开）。切完以后，区间被分成左半段 `[i, k]` 和右半段 `[k, j]`，它们各自的最小费用已经在 `dp[i][k]`、`dp[k][j]` 中记录。  

于是递推公式为  

```
dp[i][j] = min( dp[i][k] + dp[k][j] ) + (cuts[j] - cuts[i])
           for all k where i < k < j
```

**为什么要先排序？**  
切点的位置在数轴上是有顺序的。若不排序，`dp` 的下标就无法对应“左边界”和“右边界”。我们把所有切点先排好序，再在两端加上 0 与 n，得到一个有序的列表 `pos`（长度为 `m+2`），这样 `pos[i]` 永远是左端点，`pos[j]` 永远是右端点，递推才合法。

**实现细节**  
1. 将 `cuts` 排序并在前后分别加入 0 与 n，记为 `pos`。  
2. 创建大小为 `(m+2) × (m+2)` 的二维数组 `dp`，初始化为 0（因为长度为 0 或 1 的区间不需要切割）。  
3. 按 **区间长度** 从小到大遍历：先算长度为 2 的区间（恰好只包含两个端点），再算长度为 3 的区间……最终得到 `dp[0][m+1]`，即整个木棍的最小费用。  

**类比**：  
把 `dp[i][j]` 想成“在两座城镇之间铺路的最小花费”，如果中途要建一个加油站（切点），我们可以先决定在哪建，然后分别解决左边和右边的路。这样递归地把大路拆成小路，最后把所有花费加起来，就是最小的总花费。

#### 代码（Python）  

```python
from typing import List

def minCost_dp(n: int, cuts: List[int]) -> int:
    """
    区间动态规划（Interval DP）求最小切割费用。
    时间复杂度 O(m^3)，空间复杂度 O(m^2)，其中 m = len(cuts)。
    """
    # 1. 排序并加上两端点 0 与 n
    cuts.sort()
    pos = [0] + cuts + [n]          # pos[i] 表示第 i 个端点的位置
    m = len(cuts)                   # 实际切点数量

    # 2. 初始化 DP 表，dp[i][j] 表示在 pos[i] 与 pos[j] 之间的最小费用
    dp = [[0] * (m + 2) for _ in range(m + 2)]

    # 3. 按区间长度从小到大计算
    # length 表示区间端点之间相隔多少个位置（至少要相隔 2 才可能有内部切点）
    for length in range(2, m + 2):          # length = 2 -> 区间只包含两个端点，费用为 0
        for i in range(m + 2 - length):
            j = i + length                 # 区间右端点下标
            best = float('inf')
            # 在 (i, j) 之间挑选一个切点 k 作为本次最先切割的位置
            for k in range(i + 1, j):
                cost = dp[i][k] + dp[k][j] + (pos[j] - pos[i])
                if cost < best:
                    best = cost
            dp[i][j] = best if best != float('inf') else 0

    # 4. 整根木棍的最小费用位于 dp[0][m+1]
    return dp[0][m + 1]
```

> **代码说明**  
> - `pos` 把所有关键点（0、所有切点、n）排成一条有序的数轴。  
> - 外层循环 `length` 按区间的端点间距递增，保证在计算 `dp[i][j]` 时，子区间 `dp[i][k]`、`dp[k][j]` 已经算好。  
> - 内层循环遍历所有可能的第一刀 `k`，取费用最小的那一种。  
> - 最终答案就是 `dp[0][m+1]`，即从左端点 0 到右端点 n 的整个区间。

#### 复杂度  

- **时间复杂度**：`O(m³)`  
  - `m = len(cuts) ≤ 100`（题目限制），所以最多是 `100³ = 1,000,000` 次基本运算，完全可以在毫秒级跑完。  
  - 与暴力的 `m!` 相比，`m³` 就像“把所有排列压缩成只需要检查每对端点的组合”，数量大幅下降。  

- **空间复杂度**：`O(m²)`  
  - 需要保存一个 `(m+2) × (m+2)` 的二维表，大约 `10⁴` 个整数，内存占用只有几百 KB。  

---

## 心得  

- **核心技巧**：区间动态规划（Interval DP）——把“大区间的最优解”拆成“左子区间 + 右子区间 + 本次切割的固定费用”。  
- **适用的题型**：  
  1. **戳气球（Burst Balloons）** – 在区间内依次戳气球，费用与相邻气球值有关。  
  2. **矩阵链乘法（Matrix Chain Multiplication）** – 计算最小乘法次数，同样是把链分成两段递归。  
  3. **石子合并（Stone Merging）** – 合并相邻石子，费用为合并后总重量。  
- **一句话总结解题钥匙**：**“先把所有关键位置排好序，然后用 DP 记录每段区间的最小花费，递推时把区间再划分成左右两段”。**  

---

## 反思  

- **第一反应**：看到“可以随意改变切割顺序”，自然想到枚举所有排列（暴力），但立刻意识到 `cuts` 最多 100，`100!` 完全不可行。  
- **最容易踩的坑**：  
  - **忘记在 `cuts` 前后加入 0 与 n**，导致区间长度计算错误。  
  - **边界处理**：区间长度为 2（只有两个端点）时费用应为 0，不能误加 `pos[j] - pos[i]`。  
  - **DP 的遍历顺序**：必须保证子区间已经算好（即从小区间到大区间），否则会使用未初始化的值。  
- **下次类似题目第一步**：先**把所有“分割点”或“关键位置”排好序并加上两端点**，确认问题可以转化为“区间之间的最优子结构”，再决定是否使用区间 DP。