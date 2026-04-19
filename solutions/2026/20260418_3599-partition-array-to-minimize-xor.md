# #3599. 划分数组以最小化异或 / Partition Array to Minimize XOR

> 难度：中等 · 标签：Array、Dynamic Programming、Bit Manipulation、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/partition-array-to-minimize-xor/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k.
Your task is to partition nums into k non-empty subarrays. For each subarray, compute the bitwise XOR of all its elements.
Return the minimum possible value of the maximum XOR among these k subarrays.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], k = 2
Output: 1
Explanation:
The optimal partition is [1] and [2, 3] .
The maximum XOR among the subarrays is 1, which is the minimum possible.
```

**Example 2:**

```
Input: nums = [2,3,3,2], k = 3
Output: 2
Explanation:
The optimal partition is [2] , [3, 3] , and [2] .
The maximum XOR among the subarrays is 2, which is the minimum possible.
```

**Example 3:**

```
Input: nums = [1,1,2,3,1], k = 2
Output: 0
Explanation:
The optimal partition is [1, 1] and [2, 3, 1] .
The maximum XOR among the subarrays is 0, which is the minimum possible.
```

**Constraints**

- 1 <= nums.length <= 250
- 1 <= nums[i] <= 109
- 1 <= k <= n

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。  
你的任务是将 `nums` 划分为 `k` 个非空子数组（subarray）。对于每个子数组，计算其所有元素的按位异或（bitwise XOR）。  
返回在这 `k` 个子数组中 **最大** XOR 的最小可能取值。

### 示例

#### 示例 1
**输入**: `nums = [1,2,3]`, `k = 2`  
**输出**: `1`  
**解释**:  
最优的划分方式是 `[1]` 和 `[2, 3]`。  
子数组的 XOR 分别为 `1` 与 `1`，其中的最大值为 `1`，这是可以达到的最小值。

#### 示例 2
**输入**: `nums = [2,3,3,2]`, `k = 3`  
**输出**: `2`  
**解释**:  
最优的划分方式是 `[2]`、`[3, 3]` 和 `[2]`。  
子数组的 XOR 分别为 `2`、`0`、`2`，最大值为 `2`，这是最小可能的最大 XOR。

#### 示例 3
**输入**: `nums = [1,1,2,3,1]`, `k = 2`  
**输出**: `0`  
**解释**:  
最优的划分方式是 `[1, 1]` 和 `[2, 3, 1]`。  
子数组的 XOR 分别为 `0` 与 `0`，最大值为 `0`，即最小可能的最大 XOR。

### 约束条件
- `1 <= nums.length <= 250`
- `1 <= nums[i] <= 10^9`
- `1 <= k <= n`（其中 `n` 为 `nums` 的长度）

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的切分方式都枚举一遍**，然后计算每一种切分下每段的 XOR，取其中的最大值，最后在所有切分的最大值里找最小的那个。  

- **数据结构**：我们只需要一个普通的数组 `nums`，以及一个临时的列表来保存当前的切分点。  
- **生活化类比**：把数组想象成一根绳子，上面有若干个结（元素）。我们要在这根绳子上打 `k‑1` 把“剪刀”，把绳子剪成 `k` 段。暴力解就是把**每一种可能的剪刀位置**都尝试一遍，就像把所有可能的剪法都列出来，然后挑最好的那一种。  
- **为什么一定能得到答案**：因为我们穷举了 **所有** 合法的切分方式，答案必然出现在枚举的集合里。  

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def min_max_xor_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    # 预先算好前缀异或，方便快速求子数组异或
    # pre[i] = nums[0] ^ … ^ nums[i-1]，pre[0] = 0
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] ^ nums[i]

    # 所有可能的切点组合，切点是位置索引（左闭右开），共 k-1 个切点
    # 例如 n=5, k=3 -> 需要在 1..4 之间选两个切点
    best = float('inf')
    for cuts in combinations(range(1, n), k - 1):
        # 把切点放进列表，首尾各加一个哨兵，方便遍历子段
        pts = (0, ) + cuts + (n, )
        cur_max = 0
        # 逐段计算 XOR
        for i in range(1, len(pts)):
            l, r = pts[i - 1], pts[i]          # 子数组是 nums[l:r]
            seg_xor = pre[r] ^ pre[l]          # 利用前缀异或求子数组 XOR
            cur_max = max(cur_max, seg_xor)    # 记录当前切分的最大 XOR
        best = min(best, cur_max)              # 在所有切分里取最小的最大值
    return best
```

> **关键点注释**  
> - `pre[i] ^ pre[l]` 就是子数组 `[l, i)` 的 XOR，和手算“一段一段累加再取异或”是一样的，只是更快。  
> - `combinations(range(1, n), k-1)` 会枚举所有合法的切点位置，`range(1, n)` 表示切点不能在最左端或最右端（否则会出现空段）。  

#### 复杂度  

- **时间复杂度**：`O(C(n-1, k-1) * n)`  
  - `C(n-1, k-1)` 是从 `n-1` 个可能位置中挑 `k-1` 个切点的组合数。  
  - 对每一种组合我们要遍历 `k` 段（最多 `n` 段），所以乘以 `n`。  
  - 用大白话说，就是**“组合数乘以线性遍历”**，当 `n` 稍大、`k` 不是特别小的时候，这个数字会爆炸，根本跑不完。  

- **空间复杂度**：`O(n)`  
  - 主要是前缀异或数组 `pre` 用了 `n+1` 的空间，其他变量都是常数级。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有切点**，组合数随 `n` 指数增长。我们需要一种 **动态规划**（DP）的思路，把“大块枚举”变成“小块递推”。  

1. **前缀异或**  
   先算好 `pre[i] = nums[0] ^ … ^ nums[i‑1]`（`pre[0] = 0`），这样任意子数组 `[l, r)` 的 XOR 能在 **O(1)** 时间内得到：`xor(l, r) = pre[r] ^ pre[l]`。这一步和暴力解一样，但在 DP 中会被频繁使用。  

2. **状态定义**  
   - `dp[i][j]`：把前 `i`（即下标 `0..i-1`）个元素划分成 `j` 段后，**所有段的 XOR 最大值的最小可能值**。  
   - 目标是求 `dp[n][k]`（`n = len(nums)`）。  

3. **状态转移**  
   考虑最后一段的起点 `t`（`0 ≤ t < i`），则第 `j` 段是 `[t, i)`，它的 XOR 为 `pre[i] ^ pre[t]`。前面的 `j-1` 段已经由 `dp[t][j-1]` 表示。  
   对于这个切法，整体的最大 XOR 是 `max(dp[t][j-1], pre[i] ^ pre[t])`。我们想让这个最大值尽可能小，于是对所有合法的 `t` 取 **最小值**：

   ```
   dp[i][j] = min_{0 ≤ t < i}  max( dp[t][j-1] , pre[i] ^ pre[t] )
   ```

   这就是典型的 “划分 DP”。  

4. **初始化**  
   - `dp[0][0] = 0`（空数组划分成 0 段，最大 XOR 为 0）。  
   - 其它 `dp[0][j]`（`j>0`）和 `dp[i][0]`（`i>0`）是无效状态，用一个很大的数（如 `inf`）填充，防止误用。  

5. **实现细节**  
   - `n ≤ 250`，`k ≤ n`，所以二维 DP 表的大小是 `251 × 251`，完全可以放在内存里。  
   - 三重循环：外层遍历 `i`（1..n），中层遍历 `j`（1..k），内层遍历所有可能的 `t`（0..i-1）。整体时间是 `O(n²·k)`，在最坏情况下约 `250³ ≈ 1.6×10⁷`，在 Python 中可以接受。  

6. **类比帮助理解**  
   把 DP 想象成 **层层搭积木**：  
   - 第 1 层（`j=1`）只需要把前 `i` 个数整体算一次 XOR，答案就是 `pre[i]` 本身。  
   - 第 2 层（`j=2`）在第 1 层的基础上再找一个切点，让两段的最大 XOR 最小。  
   - 依次往上，每加一层就多一次“切”。  

#### 代码（Python）

```python
from typing import List

def min_max_xor_dp(nums: List[int], k: int) -> int:
    n = len(nums)
    INF = 10 ** 18          # 足够大的数，充当“无解”

    # 1. 前缀异或
    pre = [0] * (n + 1)
    for i in range(n):
        pre[i + 1] = pre[i] ^ nums[i]

    # 2. DP 表，dp[i][j] 表示前 i 个元素划分成 j 段的最小“最大 XOR”
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    dp[0][0] = 0            # 空数组、0 段的基准

    # 3. 逐步填表
    for i in range(1, n + 1):          # 考虑前 i 个元素
        for j in range(1, min(k, i) + 1):   # 至少需要 j ≤ i
            # 枚举最后一段的起点 t
            best = INF
            for t in range(j - 1, i):       # t 必须至少保留 j-1 段在左侧
                # 前 j-1 段的最优最大 XOR
                left = dp[t][j - 1]
                # 当前第 j 段的 XOR = pre[i] ^ pre[t]
                cur = pre[i] ^ pre[t]
                # 整体的最大值
                cur_max = max(left, cur)
                # 取所有切法的最小值
                if cur_max < best:
                    best = cur_max
            dp[i][j] = best

    return dp[n][k]
```

> **关键行注释**  
> - `for t in range(j - 1, i):`：切点 `t` 必须保证左侧至少有 `j‑1` 段（每段非空），所以 `t` 不能小于 `j‑1`。  
> - `cur = pre[i] ^ pre[t]`：利用前缀异或，瞬间得到第 `j` 段的 XOR。  
> - `cur_max = max(left, cur)`：整体的最大 XOR 必须是左侧最大和右侧 XOR 两者的较大者。  

#### 复杂度  

- **时间复杂度**：`O(n²·k)`  
  - 外层遍历 `i`（`n` 次），中层遍历 `j`（至多 `k` 次），内层遍历所有可能的切点 `t`（最多 `i` 次），相乘得到 `n·k·n = n²·k`。  
  - 用大白话说就是“把数组的每一段都尝试一次”，但因为我们把“子数组 XOR”算成了 **O(1)**，所以整体仍然在几千万次左右，能够在 1 秒左右跑完。  

- **空间复杂度**：`O(n·k)`  
  - DP 表占用了 ` (n+1) × (k+1) ` 的二维数组，最多约 `251 × 251 ≈ 6.3万` 个整数，完全在内存里。  
  - 额外的前缀异或数组是 `O(n)`，与 DP 表同级别。  

---

## 心得  

- **核心技巧**：**划分动态规划 + 前缀异或**。  
- **该技巧适用的题型**：  
  1. “把数组分成 k 段，使每段的某种代价（和、最大值、异或等）满足最小化/最大化”——如 *Partition Array for Maximum Sum*、*Divide Array in Sets of K Consecutive Numbers*（思路类似）。  
  2. 需要快速求子数组某种聚合值（和、异或、位与）的题目，往往先预处理前缀数组。  
- **一句话总结解题钥匙**：**把“最大值的最小化”转化为 DP 中的“取最小的最大”，配合前缀异或把子段代价降到 O(1)。**  

---

## 反思  

- **第一反应**：看到“划分成 k 段，求每段 XOR 的最大值最小”，立刻想到**二分答案 + 检查可行性**（类似划分子数组使每段和 ≤ X），但因为 XOR 没有单调性，这条路走不通。于是转向**划分 DP**。  
- **最容易踩的坑**：  
  1. **切点合法性**：`dp[t][j‑1]` 必须在左侧已经划分好 `j‑1` 段，`t` 不能太小，否则会出现空段。  
  2. **初始化**：忘记把不可达的状态设成 `INF`，导致后续 `max` 计算出现错误。  
  3. **前缀异或的定义**：`pre[i]` 包含前 `i` 个元素（不含下标 `i`），如果写成 `pre[i] = pre[i‑1] ^ nums[i]` 会导致索引偏移错误。  
- **下次遇到同类题**：第一步先**判断是否可以用前缀技巧把子段代价降到 O(1)**，再**写出划分 DP 的状态转移**，最后检查切点合法性和初始化。这样思路会更清晰、实现更顺畅。