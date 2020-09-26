# #1000. 合并石子的最小成本 / Minimum Cost to Merge Stones

> 难度：困难 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-merge-stones/)

---

## 题目（英文原版）

**Description**

There are n piles of stones arranged in a row. The ith pile has stones[i] stones.
A move consists of merging exactly k consecutive piles into one pile, and the cost of this move is equal to the total number of stones in these k piles.
Return the minimum cost to merge all piles of stones into one pile. If it is impossible, return -1.

**Examples**

**Example 1:**

```
Input: stones = [3,2,4,1], k = 2
Output: 20
Explanation: We start with [3, 2, 4, 1].
We merge [3, 2] for a cost of 5, and we are left with [5, 4, 1].
We merge [4, 1] for a cost of 5, and we are left with [5, 5].
We merge [5, 5] for a cost of 10, and we are left with [10].
The total cost was 20, and this is the minimum possible.
```

**Example 2:**

```
Input: stones = [3,2,4,1], k = 3
Output: -1
Explanation: After any merge operation, there are 2 piles left, and we can't merge anymore.  So the task is impossible.
```

**Example 3:**

```
Input: stones = [3,5,1,2,6], k = 3
Output: 25
Explanation: We start with [3, 5, 1, 2, 6].
We merge [5, 1, 2] for a cost of 8, and we are left with [3, 8, 6].
We merge [3, 8, 6] for a cost of 17, and we are left with [17].
The total cost was 25, and this is the minimum possible.
```

**Constraints**

- n == stones.length
- 1 <= n <= 30
- 1 <= stones[i] <= 100
- 2 <= k <= 30

---

## 题目（中文翻译）

有 n 堆石子排成一行，第 i 堆的石子数为 `stones[i]`。  
一次**合并操作（move）**需要将恰好 k 个相邻的石子堆合并成一堆，合并的代价等于这 k 堆石子数之和。  

返回将所有石子堆合并成一堆的最小代价。如果无法完成合并，则返回 `-1`。

## 示例

### 示例 1
**输入**  
```text
stones = [3,2,4,1], k = 2
```
**输出**  
```text
20
```
**解释**  
我们从 `[3, 2, 4, 1]` 开始。  
- 合并 `[3, 2]`，代价为 `5`，得到 `[5, 4, 1]`。  
- 合并 `[4, 1]`，代价为 `5`，得到 `[5, 5]`。  
- 合并 `[5, 5]`，代价为 `10`，得到 `[10]`。  

总代价为 `20`，这是可能的最小代价。

### 示例 2
**输入**  
```text
stones = [3,2,4,1], k = 3
```
**输出**  
```text
-1
```
**解释**  
任意一次合并后，剩余的堆数为 `2`，无法再进行一次恰好合并 `k=3` 堆的操作。因此任务不可完成，返回 `-1`。

### 示例 3
**输入**  
```text
stones = [3,5,1,2,6], k = 3
```
**输出**  
```text
25
```
**解释**  
我们从 `[3, 5, 1, 2, 6]` 开始。  
- 合并 `[5, 1, 2]`，代价为 `8`，得到 `[3, 8, 6]`。  
- 合并 `[3, 8, 6]`，代价为 `17`，得到 `[17]`。  

总代价为 `25`，这是可能的最小代价。

## 约束条件
- `n == stones.length`
- `1 <= n <= 30`
- `1 <= stones[i] <= 100`
- `2 <= k <= 30`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的合并顺序** 都枚举一遍，算出每一种顺序的总代价，最后取最小值。  
可以把每一次合并看成一次递归：

1. 当前有 `stones[l…r]` 这几堆石子。  
2. 挑选任意相邻的 `k` 堆（即在区间 `[l, r]` 中选择一个起点 `i`，合并 `stones[i] … stones[i+k-1]`）。  
3. 产生新的石堆列表，递归继续合并，直到只剩一堆。  

> **类比**：把每一堆石子想象成一本书的章节，合并 `k` 堆就像把相邻的 `k` 章节装订成一本新书，装订费就是这几章节的页数之和。我们要找出把所有章节装订成一本书的最省钱方式。

**为什么正确**  
只要我们遍历了 *所有* 合并的可能序列，就一定能找到代价最小的那一种。递归本身完整地描述了题目的每一步操作，所以只要不遗漏任何合法的合并，就一定能得到正确答案。

**时间/空间复杂度**  
- 每一步都要在 `O(length)`（区间长度）个位置挑选 `k` 堆合并，递归深度大约是 `(n-1)/(k-1)`（每合并一次，堆数减少 `k-1`）。  
- 这相当于在 **指数级** 的搜索树上遍历：`O( (n)^( (n-1)/(k-1) ) )`。  
- 空间上除了保存递归栈外，只需要 `O(n)` 的临时数组。

> **大白话**：如果把 `O(n²)` 想象成“把 100 本书两两配对”，`O(2ⁿ)` 就像“把 30 本书的每一种可能排成一行”。指数级的时间在 n=30 时已经会让程序跑到天荒地老。

#### 代码（Python）

```python
from functools import lru_cache
from itertools import accumulate

def merge_bruteforce(stones, k):
    n = len(stones)
    # 前缀和，方便快速求任意区间的石子总数
    prefix = [0] + list(accumulate(stones))

    # 区间和函数
    def interval_sum(l, r):
        return prefix[r + 1] - prefix[l]

    @lru_cache(None)               # 记忆化，防止重复计算（仍然是指数级）
    def dfs(arr):
        """返回把 arr（tuple）全部合并成一堆的最小代价，若不可合并返回 INF"""
        m = len(arr)
        if m == 1:                 # 已经只剩一堆，费用为 0
            return 0
        if m < k:                  # 不够 k 堆，无法继续合并
            return float('inf')

        best = float('inf')
        # 枚举所有可能的合并位置
        for i in range(m - k + 1):
            # 合并 i~i+k-1 这 k 堆
            merged = sum(arr[i:i + k])
            new_arr = arr[:i] + (merged,) + arr[i + k:]
            cost = dfs(new_arr)
            if cost != float('inf'):
                best = min(best, cost + merged)   # 本次合并费用 + 之后的最小费用
        return best

    ans = dfs(tuple(stones))
    return -1 if ans == float('inf') else ans
```

> 代码里用了 `lru_cache` 做记忆化，虽然仍然很慢，但可以让我们在调试小样例时不至于卡死。

#### 复杂度

- **时间复杂度**：指数级 `O(k^{(n-1)/(k-1)})`（每一步都有 `≈ n` 种选择，递归深度约为 `(n-1)/(k-1)`），远远超过题目限制。  
- **空间复杂度**：`O(n)`（递归栈深度）+ 记忆化表的大小（最多存 `n!` 种不同的子序列），在最坏情况下也是指数级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复计算**：很多不同的合并顺序会得到相同的子区间，然而我们每次都重新算一遍。  
我们需要把“子区间的最小代价” **存起来**，以后直接查表，而不是重新递归。  
这正是 **动态规划（Dynamic Programming, DP）** 的核心思想：把大问题拆成小子问题，子问题只算一次。

---

#### 关键观察 1：堆数的可达性  

每一次合并会把堆数 **减少 `k‑1`**（因为 `k` 堆变成 1 堆）。  
设初始堆数为 `n`，要最终只剩 1 堆，需要进行 `t = (n-1)/(k-1)` 次合并。  
因此 **只有当 `(n-1) % (k-1) == 0` 时才可能完成**，否则直接返回 `-1`。

---

#### 关键观察 2：区间 DP + 前缀和  

我们把石子数组看成一条直线，任意合并只会在 **相邻** `k` 堆之间发生。  
于是可以把问题限定在 **区间** `[i, j]`（`0 ≤ i ≤ j < n`）上：

- `dp[i][j]` 表示把区间 `stones[i…j]` 合并成 ****`p` 堆**（`p` 为该区间最终剩余的堆数）** 的最小代价。  
- 为了统一表示，我们记 `dp[i][j][m]` 为把区间合并成恰好 **`m` 堆** 的最小费用（`1 ≤ m ≤ k`）。  

**但我们可以把状态压缩**：  
因为最终我们只关心 **是否能合并成 1 堆**，而在合并成 1 堆之前，需要先把区间合并成 **`k` 堆** 再一次合并。  
于是采用两层 DP：

1. `cost[i][j]`：把 `stones[i…j]` 合并成 ****1 堆** 的最小费用（前提是可行）。  
2. `dp[i][j]`：把 `stones[i…j]` 合并成 ****任意合法堆数** 的最小费用，**这里的“合法”指的是** ` (j-i) % (k-1) == 0` **（即可以继续合并成更少的堆）**。

---

#### 递推公式  

设 `sum(i, j)` 为区间 `[i, j]` 的石子总数（利用前缀和 O(1) 求得）。

1. **先把区间合并成 `k` 堆**（因为只有 `k` 堆才能一次合并成 1 堆）  
   ```text
   dp[i][j] = min_{i ≤ m < j, (m-i+1) % (k-1) == 0}
              dp[i][m] + dp[m+1][j]
   ```
   解释：把 `[i, j]` 切成两段，使左段恰好可以合并成若干堆（满足 `(len-1) % (k-1) == 0`），右段同理。两段各自的最小费用相加，即得到把整段合并成 **`k` 堆** 的费用。

2. **再把 `k` 堆合并成 1 堆**（这一步需要付一次合并费用，即区间总石子数）  
   ```text
   if (j - i) % (k - 1) == 0:      # 整个区间最终能变成 1 堆
       cost[i][j] = dp[i][j] + sum(i, j)
   else:
       cost[i][j] = dp[i][j]       # 只能停留在 “k 堆” 的状态
   ```

   注意：当 `i == j` 时，`dp[i][i] = cost[i][i] = 0`（单个石堆不需要合并）。

---

#### 实现细节  

- **前缀和**：`prefix[t] = stones[0] + … + stones[t-1]`，则 `sum(i, j) = prefix[j+1] - prefix[i]`。  
- **循环顺序**：区间长度从小到大枚举，保证子区间的 DP 已经算好。  
- **状态表**：`dp` 与 `cost` 都是 `n × n` 的二维数组，空间 `O(n²)`（`n ≤ 30`，非常小）。  
- **时间复杂度**：外层遍历所有 `O(n²)` 区间；内层在每个区间里尝试所有合法的切分点，最多 `O(n)` 次 → **总体 `O(n³)`**。对 `n = 30` 来说完全可接受。

---

#### 代码（Python）

```python
from itertools import accumulate
from math import inf

def mergeStones(stones, k):
    n = len(stones)
    # 1. 先判断是否可能合并成一堆
    if (n - 1) % (k - 1) != 0:      # 只能在满足此式时完成全部合并
        return -1

    # 2. 前缀和，帮助 O(1) 计算任意区间的石子总数
    prefix = [0] + list(accumulate(stones))

    def interval_sum(l, r):
        """返回 stones[l..r] 的总和"""
        return prefix[r + 1] - prefix[l]

    # 3. dp[i][j] 表示把区间 [i, j] 合并成「合法」堆数（即可以继续合并）的最小费用
    dp = [[0] * n for _ in range(n)]

    # 4. 按区间长度从小到大枚举
    for length in range(k, n + 1):           # 长度小于 k 时不可能再合并
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = inf
            # 4.1 先把区间拆成两段，使左段、右段各自都是「合法」的堆数
            # 只在切分点 m 使左段长度满足 (m-i) % (k-1) == 0 才是合法的
            for m in range(i, j, k - 1):
                # m 为左段的结束位置，右段从 m+1 开始
                dp[i][j] = min(dp[i][j], dp[i][m] + dp[m + 1][j])

            # 4.2 如果当前区间长度可以最终合并成 1 堆，额外加上一次合并的费用
            if (length - 1) % (k - 1) == 0:   # 能变成 1 堆
                dp[i][j] += interval_sum(i, j)

    # 5. 整个数组的答案就在 dp[0][n-1] 中
    return dp[0][n - 1]
```

**代码要点解释**

| 行号 | 关键代码 | 中文注释 |
|------|----------|----------|
| 5‑6 | `if (n - 1) % (k - 1) != 0: return -1` | 先判断是否有解的必要条件 |
| 9‑11 | `prefix = [0] + list(accumulate(stones))` | 前缀和数组，后面求区间和只需 O(1) |
| 14‑16 | `def interval_sum(l, r): return prefix[r+1] - prefix[l]` | 区间求和函数 |
| 20‑21 | `dp = [[0] * n for _ in range(n)]` | 初始化 DP 表，默认 0（单个石堆） |
| 23‑30 | `for length in range(k, n+1): …` | 按区间长度递增枚举，保证子问题已算好 |
| 26‑29 | `for m in range(i, j, k-1): dp[i][j] = min(dp[i][j], dp[i][m] + dp[m+1][j])` | 只在合法切分点（间隔 `k-1`）上尝试，合并左右子区间的最小费用 |
| 31‑33 | `if (length-1) % (k-1) == 0: dp[i][j] += interval_sum(i, j)` | 当区间可以最终合并成 1 堆时，加上这一次合并的费用（区间总石子数） |
| 38 | `return dp[0][n-1]` | 整体答案 |

---

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 外层两层遍历所有区间 `O(n²)`，内层遍历合法切分点至多 `O(n)`。  
  - 对 `n ≤ 30` 来说，大约几千次运算，毫秒级完成。相比暴力的指数级，快得多。

- **空间复杂度**：`O(n²)`  
  - 只用了一个 `n × n` 的二维数组来存 DP，`n=30` 时占用约 900 个整数，几乎可以忽略。

---

## 心得

- **核心技巧**：**区间动态规划 + 前缀和**，配合 “堆数可达性” 的数学判断。  
- **适用的题型**  
  1. “合并石子”“合并数组” 系列（如 LeetCode 1000+ 题目）。  
  2. “矩阵分割”“最小代价划分” 类的区间 DP（如 “Burst Balloons”）。  
  3. “分割数组求最小代价” 的前缀和 + DP（如 “Stone Game II” 的变形）。  

> **一句话总结解题钥匙**：  
> “把大问题拆成可以递归合并的**合法子区间**，用 DP 把子区间的最优代价记下来，最后在合并成 1 堆时再加一次区间总和。”

---

## 反思

- **第一反应**：看到“每次只能合并 k 堆”，立刻想到“递归遍历所有合并顺序”。这是一条通向暴力解的直觉路径。  
- **最容易踩的坑**  
  1. **可行性判断遗漏**：忘记检查 `(n-1) % (k-1) == 0`，导致在不可能的输入上仍继续计算，最终返回错误的数值。  
  2. **切分点的步长错误**：在 DP 中遍历切分点时必须跳 `k-1`，否则会产生非法的子区间，使状态转移不满足题目限制。  
  3. **前缀和写错**：区间求和的下标容易越界，记得 `prefix` 长度要比 `stones` 多 1。  
- **下次遇到同类题**，第一步应该先**写出可行性公式**（堆数变化规律），再**构造区间 DP**，并利用**前缀和**把“合并费用”计算降到 O(1)。这样就能快速定位最优子结构，避免盲目枚举。