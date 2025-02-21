# #3077. K 个不相交子数组的最大强度 / Maximum Strength of K Disjoint Subarrays

> 难度：困难 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-strength-of-k-disjoint-subarrays/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums with length n, and a positive odd integer k.
Select exactly k disjoint subarrays sub1, sub2, ..., subk from nums such that the last element of subi appears before the first element of sub{i+1} for all 1 <= i <= k-1. The goal is to maximize their combined strength.
The strength of the selected subarrays is defined as:
strength = k * sum(sub1)- (k - 1) * sum(sub2) + (k - 2) * sum(sub3) - ... - 2 * sum(sub{k-1}) + sum(subk)
where sum(subi) is the sum of the elements in the i-th subarray.
Return the maximum possible strength that can be obtained from selecting exactly k disjoint subarrays from nums.
Note that the chosen subarrays don't need to cover the entire array.
Input: nums = [1,2,3,-1,2], k = 3
Output: 22
Explanation:
The best possible way to select 3 subarrays is: nums[0..2], nums[3..3], and nums[4..4]. The strength is calculated as follows:
strength = 3 * (1 + 2 + 3) - 2 * (-1) + 2 = 22
Input: nums = [12,-2,-2,-2,-2], k = 5
Output: 64
Explanation:
The only possible way to select 5 disjoint subarrays is: nums[0..0], nums[1..1], nums[2..2], nums[3..3], and nums[4..4]. The strength is calculated as follows:
strength = 5 * 12 - 4 * (-2) + 3 * (-2) - 2 * (-2) + (-2) = 64
Input: nums = [-1,-2,-3], k = 1
Output: -1
Explanation:
The best possible way to select 1 subarray is: nums[0..0]. The strength is -1.

**Constraints**

- 1 <= n <= 104
- -109 <= nums[i] <= 109
- 1 <= k <= n
- 1 <= n * k <= 106
- k is odd.

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`，以及一个正奇数 `k`。  
从 `nums` 中选择恰好 `k` 个不相交的子数组（subarray）`sub1, sub2, ..., subk`，要求对于所有 `1 ≤ i ≤ k‑1`，`subi` 的最后一个元素出现在 `sub{i+1}` 的第一个元素之前。  
目标是使这些子数组的**综合强度**（strength）最大化。

选中的子数组的强度定义为：

```
strength = k   * sum(sub1)
          - (k‑1) * sum(sub2)
          + (k‑2) * sum(sub3)
          - ... 
          - 2   * sum(sub{k‑1})
          + 1   * sum(subk)
```

其中 `sum(subi)` 表示第 `i` 个子数组中所有元素的和。  

返回从 `nums` 中恰好选取 `k` 个不相交子数组所能得到的最大可能强度。  
注意，所选子数组不需要覆盖整个数组。

**示例 1**  
```
输入: nums = [1,2,3,-1,2], k = 3
输出: 22
解释:
选择的 3 个子数组为: nums[0..2], nums[3..3] 和 nums[4..4]。  
强度计算如下:
strength = 3 * (1 + 2 + 3) - 2 * (-1) + 1 * 2 = 22
```

**示例 2**  
```
输入: nums = [12,-2,-2,-2,-2], k = 5
输出: 64
解释:
唯一可能的选法是: nums[0..0], nums[1..1], nums[2..2], nums[3..3] 和 nums[4..4]。  
强度计算如下:
strength = 5 * 12 - 4 * (-2) + 3 * (-2) - 2 * (-2) + 1 * (-2) = 64
```

**示例 3**  
```
输入: nums = [-1,-2,-3], k = 1
输出: -1
解释:
最佳的选法是选取子数组 nums[0..0]。  
强度为 -1。
```

**约束条件**

- `1 ≤ n ≤ 10^4`
- `-10^9 ≤ nums[i] ≤ 10^9`
- `1 ≤ k ≤ n`
- `1 ≤ n * k ≤ 10^6`
- `k` 为奇数

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把所有可能的 k 条不相交子数组枚举出来，算出每一种的 “strength”，取最大**。  
我们可以这样做：

1. 先在数组里挑选第 1 条子数组的左端点 `l1`（0 ≤ l1 < n），再挑选右端点 `r1`（l1 ≤ r1 < n）。这就确定了第一条子数组 `nums[l1…r1]`。  
2. 接着在 `r1+1` 之后继续挑选第 2 条子数组的左、右端点 `l2、r2`，依此类推，直到挑出第 k 条。  
3. 每挑出一套 `k` 条子数组，就可以根据题目给出的系数 `k, -(k‑1), … , +1` 计算它们的 **strength**。  
4. 把所有可能的组合的 strength 取最大，就是答案。

> **类比**：想象你在一条直线的路灯下挑选 k 段不相交的路段，每段路段的长度对应子数组的和，系数就像不同颜色的涂料，交替涂在每段路上。要找出涂完后颜色最浓的方案，只能把所有可能的划分都列出来尝试。

这个方法之所以 **正确**，是因为我们穷举了**所有**合法的子数组集合，答案必然在其中。

**时间/空间分析**  

- 枚举一条子数组需要 `O(n²)`（左端点 × 右端点）。  
- 要挑出 k 条子数组，就要把这个过程套 `k` 层，时间复杂度是 `O(n^{2k})`（指数级别）。  
- 只需要保存当前递归路径上的子数组，空间是 `O(k)`（递归栈深度）。

> **大白话**：`O(n^{2k})` 就像把 `n` 颗糖果放进 `2k` 个盒子里，每种放法都要尝一遍，根本不可能在几秒钟内算完（尤其是 n=10⁴、k 可能上百时）。

#### 代码（Python）

```python
from typing import List

def max_strength_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)

    # 计算子数组和的帮助函数（前缀和可以把 O(1) 取到，这里直接算也行）
    def sub_sum(l: int, r: int) -> int:
        s = 0
        for i in range(l, r + 1):
            s += nums[i]
        return s

    # 系数序列：k, -(k-1), (k-2), … , +1（k 为奇数，最后一定是 +1）
    coeff = [k - i if i % 2 == 0 else -(k - i) for i in range(k)]

    best = -10**18  # 负无穷，保证即使全是负数也能更新

    # 递归枚举第 idx 条子数组，pos 为当前可以开始的最左位置
    def dfs(idx: int, pos: int, cur_strength: int):
        nonlocal best
        if idx == k:                     # 已经挑完 k 条
            best = max(best, cur_strength)
            return
        # 在剩余区间里任选左端点 l、右端点 r
        for l in range(pos, n):
            for r in range(l, n):
                s = sub_sum(l, r)        # 该子数组的和
                dfs(idx + 1, r + 1, cur_strength + coeff[idx] * s)

    dfs(0, 0, 0)
    return best
```

> **提示**：这段代码只能在 `n ≤ 10`、`k ≤ 3` 之类的极小数据上跑通，用来帮助理解思路，实际提交会 TLE（超时）。

#### 复杂度  

- **时间复杂度**：`O(n^{2k})` —— 每条子数组需要 `O(n²)`，套 `k` 层，呈指数增长。  
- **空间复杂度**：`O(k)` —— 递归栈最多保存 k 条子数组的信息。

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在 **“枚举所有子数组”** 这一步。  
观察公式：

```
strength = k·sum1 - (k-1)·sum2 + (k-2)·sum3 - … - 2·sum{k-1} + 1·sumk
```

可以把每个元素 **一次性** 贡献一个 **系数**（取决于它所在的是第几条子数组），而且系数只跟子数组的 **序号** 有关，与子数组的具体长度无关。  

> **关键观察**  
> 当我们从左到右遍历数组时，**是否把当前元素加入正在构造的子数组**，只会影响当前子数组的系数（`+j` 或 `-j`），而后面的子数组系数保持不变。  
> 这正好适合 **动态规划**：在遍历过程中记录“已经选了几条子数组”，以及“现在是否已经打开（正在选）一条子数组”。

---

#### 状态定义  

设 `dp0[i][j]` 为 **从下标 i 开始的后缀**（`nums[i…n-1]`）中，**已经选了 j 条子数组**，且 **当前不在任何子数组内部** 时能够得到的最大 strength。  

设 `dp1[i][j]` 为 **从下标 i 开始的后缀**，已经选了 j 条子数组，**当前正处于第 j 条子数组内部**（第 j 条子数组已经至少包含了 `nums[i]`）时的最大 strength。  

这里的 `j` **从 1 开始计数**（第 1 条子数组的系数是 `+k`，第 2 条是 `-(k-1)` …），当 `j = 0` 时只能处于 `dp0` 状态，`dp1` 没意义。

---

#### 系数函数  

第 `j` 条子数组的系数（即每加入一个元素要乘的数）为：

```
coeff(j) =  j   ,  if j is odd
          = -j   ,  if j is even
```

这恰好等价于题目给出的交替正负系数（因为 `k` 本身是奇数，`k, -(k-1), … , +1` 与 `coeff(1)…coeff(k)` 完全相同）。

---

#### 转移方程  

1. **把 `nums[i]` 加入正在进行的第 j 条子数组**  

   - 贡献：`nums[i] * coeff(j)`  
   - 之后有两种可能  
     * **结束子数组**：下一个位置 `i+1` 必须转到 “不在子数组内部”，而我们还需要再选 `j-1` 条子数组 → `dp0[i+1][j-1]`  
     * **继续延伸**：保持在 “内部” 状态，仍然是第 j 条子数组 → `dp1[i+1][j]`  

   因此  

   ```
   dp1[i][j] = nums[i] * coeff(j) + max( dp0[i+1][j-1] , dp1[i+1][j] )
   ```

   （当 `j = 0` 时该式子无意义，设为 -∞）

2. **当前不在子数组内部**  

   - 可以直接跳过 `nums[i]` → `dp0[i+1][j]`  
   - 也可以 **立刻把 `nums[i]` 当作第 j 条子数组的第一个元素**，这正是 `dp1[i][j]` 的值  

   所以  

   ```
   dp0[i][j] = max( dp0[i+1][j] , dp1[i][j] )
   ```

---

#### 初始条件  

- 当已经遍历到数组末尾 `i = n` 时，只能选 **0 条子数组**，且不在子数组内部：  

  ```
  dp0[n][0] = 0
  dp0[n][j>0] = -∞   (不可能选到更多子数组)
  dp1[n][*]   = -∞   (已经没有元素可以继续)
  ```

---

#### 结果  

我们从左到右遍历完所有位置后，答案就是 **从下标 0 开始、恰好选了 k 条子数组、且不在子数组内部** 的最大值：

```
answer = dp0[0][k]
```

---

#### 空间优化  

上面的转移只依赖 **第 i+1 行** 的数据，因此可以把二维表压缩成 **两行**（或直接用一维滚动数组）。  
记 `prev0[j] = dp0[i+1][j]`、`prev1[j] = dp1[i+1][j]`，遍历 `i` 从 `n-1` 到 `0` 时计算 `cur0、cur1`，随后把 `cur` 赋给 `prev`。  
这样空间降为 `O(k)`。

---

#### 代码（Python）

```python
from typing import List

def maxStrength(nums: List[int], k: int) -> int:
    n = len(nums)
    INF_NEG = -10**18          # 代表负无穷

    # 系数函数：第 j 条子数组的系数 (+j 或 -j)
    def coeff(j: int) -> int:
        return j if j % 2 == 1 else -j

    # dp0[j]  : 当前位置 i（从右往左）以后，已选 j 条子数组，且当前不在子数组内部的最大 strength
    # dp1[j]  : 当前位置 i 以后，已选 j 条子数组，且当前正处于第 j 条子数组内部的最大 strength
    dp0 = [INF_NEG] * (k + 1)
    dp1 = [INF_NEG] * (k + 1)

    # 初始条件：在数组末尾只能选 0 条子数组，且不在子数组内部
    dp0[0] = 0

    # 从右往左遍历每个元素
    for idx in range(n - 1, -1, -1):
        cur0 = [INF_NEG] * (k + 1)
        cur1 = [INF_NEG] * (k + 1)

        # 先计算 dp1（因为它需要使用上一轮的 dp0、dp1）
        for j in range(1, k + 1):            # j 为已经选了多少条子数组，j>=1 才能处于“内部”
            # 结束子数组后还需要选 j-1 条，或者继续延伸当前子数组
            end_then = dp0[j - 1]            # dp0[i+1][j-1]
            continue_then = dp1[j]           # dp1[i+1][j]
            best_next = max(end_then, continue_then)
            cur1[j] = nums[idx] * coeff(j) + best_next

        # 再计算 dp0
        for j in range(k + 1):
            # 不选当前元素，保持原状态；或者把当前元素当作第 j 条子数组的开始（即 dp1）
            cur0[j] = max(dp0[j], cur1[j])

        # 更新为本轮的结果，供左侧的元素使用
        dp0, dp1 = cur0, cur1

    return dp0[k]
```

**代码要点（中文注释）**  

- `coeff(j)` 用来返回第 `j` 条子数组的系数，奇数正、偶数负。  
- `dp0`、`dp1` 用 **一维数组** 保存当前右侧（已经遍历完的）区间的状态，空间 `O(k)`。  
- 循环 `for idx in range(n-1, -1, -1)` 实现 **从右往左** 的 DP，保证转移只依赖已经算好的 `i+1` 行。  
- `cur1[j]` 的公式正是上面推导的 `dp1[i][j]`。  
- `cur0[j] = max(dp0[j], cur1[j])` 实现 `dp0[i][j] = max(dp0[i+1][j], dp1[i][j])`。  
- 最终答案在 `dp0[k]`，因为我们必须恰好选完 `k` 条子数组，并且结束后不再“打开”子数组。

---

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - 每个位置 `i`（共 `n` 个）遍历 `j = 1 … k`，每次仅做常数次运算。  
  - 与暴力的指数级别相比，线性乘积在题目限制 `n·k ≤ 10⁶` 下完全可接受。  

- **空间复杂度**：`O(k)`  
  - 只保存两行 DP（`dp0`、`dp1`），不需要 `n × k` 的二维表。  

> 与暴力解相比，时间从 **天文数字** 降到 **几百万次**，空间也从 **递归栈** 降到 **几千个整数**，真正可以在 1 秒左右跑完。

---

## 心得  

- **核心技巧**：**状态机式的动态规划** —— 用 “是否在子数组内部” 这两个状态把原本的 **子数组划分** 问题转化为 **逐元素决策**。  
- **适用场景**：  
  1. **交替加权的子数组选择**（如本题、或 “正负交替系数的子序列最大和”）。  
  2. **需要在序列上划分若干段且每段都有不同权重**（例如 “分段收益最大化”）。  
  3. **带有“是否打开区间” 状态的 DP**（如 “最大子数组乘积” 的 DP 也有 “是否已选” 的状态）。  

- **一句话总结解题钥匙**：  
  > 把 “选哪几段子数组” 的全局组合问题，拆成 “遍历每个元素时，是继续当前段还是结束/不选” 的局部决策，并用 **两种状态**（在段内 / 不在段内）记录已选段数即可得到线性 DP。

---

## 反思  

- **第一反应**：看到 “k 条不相交子数组” 以及 **交替系数**，立刻想到 **枚举** 或 **前缀和 + 双指针**。但交替系数让普通的 “最大子数组和” 思路失效，因为每加入一个元素的贡献会随段序号改变。  
- **最容易踩的坑**  
  1. **系数方向错误**：`k` 为奇数时系数序列是 `+k, -(k-1), … , +1`，一定要用 `coeff(j) = j if j odd else -j`（而不是 `(-1)^{j}` 那种不考虑大小的符号）。  
  2. **边界条件**：`dp0[n][0] = 0`，其余全部设为负无穷；否则在 “结束子数组” 时会错误地把不存在的状态当成 0。  
  3. **下标越界**：在计算 `dp1[i][j]` 时使用 `dp0[i+1][j-1]`，需要确保 `j ≥ 1`。  
  4. **空间滚动写错顺序**：先算 `dp1`（依赖旧的 `dp0、dp1`），再算 `dp0`（依赖新产生的 `dp1`），否则会产生错误的转移。  

- **下次类似题的第一步**：  
  > 把 **“是否正在构造当前区间”** 抽象成一个二元状态，写出 **状态转移**（加入、结束、跳过），再检查系数/权重随状态的变化是否可以用一个简单函数表示。这样往往能把指数级枚举压缩到 `O(n·状态数)`。