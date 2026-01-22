# #3500. 最小划分数组子数组的代价 / Minimum Cost to Divide Array Into Subarrays

> 难度：困难 · 标签：Array、Dynamic Programming、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-divide-array-into-subarrays/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays, nums and cost, of the same size, and an integer k.
You can divide nums into subarrays. The cost of the ith subarray consisting of elements nums[l..r] is:
Note that i represents the order of the subarray: 1 for the first subarray, 2 for the second, and so on.
Return the minimum total cost possible from any valid division.

**Examples**

**Example 1:**

```
Input: nums = [3,1,4], cost = [4,6,6], k = 1
Output: 110
Explanation:
```

**Example 2:**

```
Input: nums = [4,8,5,1,14,2,2,12,1], cost = [7,2,8,4,2,2,1,1,2], k = 7
Output: 985
Explanation:
```

**Constraints**

- 1 <= nums.length <= 1000
- cost.length == nums.length
- 1 <= nums[i], cost[i] <= 1000
- 1 <= k <= 1000

---

## 题目（中文翻译）

你得到两个整数数组 `nums` 与 `cost`，它们的长度相同，还有一个整数 `k`。  
你可以将 `nums` 划分成若干子数组（subarray）。第 `i` 个子数组包含元素 `nums[l..r]`（下标从 `l` 到 `r`），其代价为：

> **注**：`i` 表示子数组的顺序，第一段子数组的 `i = 1`，第二段子数组的 `i = 2`，依此类推。

返回所有合法划分方式中能够得到的最小总代价。

**示例 1**  
```
Input: nums = [3,1,4], cost = [4,6,6], k = 1
Output: 110
Explanation:
```

**示例 2**  
```
Input: nums = [4,8,5,1,14,2,2,12,1], cost = [7,2,8,4,2,2,1,1,2], k = 7
Output: 985
Explanation:
```

**约束条件**  

- `1 <= nums.length <= 1000`  
- `cost.length == nums.length`  
- `1 <= nums[i], cost[i] <= 1000`  
- `1 <= k <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把数组 **从左到右** 逐段划分，每一次划分都要把「当前子数组」的费用算出来，然后把「剩下」的部分再继续划分。  
最直白的做法就是：

1. **枚举** 第一个子数组的右端点 `r`（`r` 可以是 `0 … n‑1`）。  
2. 计算子数组 `nums[0 … r]` 的费用 `costSub(0, r)`（题目已经给出了费用公式，这里只需要把对应的前缀和带进去）。  
3. **递归** 或者 **动态规划** 求解「从 `r+1` 开始」的最小费用。  

> **类比**：把数组想成一条路，路上有若干个「服务站」——每停一次就要交一次费用。暴力解相当于把每一种可能的「停站方案」都列出来，挑最便宜的那条。

因为我们每次都要遍历所有可能的右端点，整体的时间会是 **二次方**（`O(n²)`），空间只需要保存一个一维 DP 表（`O(n)`）。

#### 代码（Python）

```python
def minimumCost(nums, cost, k):
    n = len(nums)

    # ---------- 预处理前缀和 ----------
    # 前缀和可以在 O(1) 时间内算出任意子数组的 sum
    pre_num = [0] * (n + 1)   # pre_num[i] = nums[0] + … + nums[i-1]
    pre_cost = [0] * (n + 1)  # pre_cost[i] = cost[0] + … + cost[i-1]
    for i in range(n):
        pre_num[i + 1] = pre_num[i] + nums[i]
        pre_cost[i + 1] = pre_cost[i] + cost[i]

    # ---------- 子数组费用 ----------
    # 题目给出的费用公式是：
    #   subCost(l, r) = (pre_num[r+1] - pre_num[l]) * (pre_cost[r+1] - pre_cost[l]) + k * (pre_cost[r+1] - pre_cost[l])
    # 这里把「子数组的总和」和「子数组的 cost 总和」分别取出来再代入公式。
    def sub_cost(l, r):
        sum_num = pre_num[r + 1] - pre_num[l]
        sum_cost = pre_cost[r + 1] - pre_cost[l]
        return sum_num * sum_cost + k * sum_cost

    # ---------- 动态规划 ----------
    # dp[i] 表示「从位置 i 开始」的最小总费用（即 suffix [i … n-1]）
    dp = [0] * (n + 1)          # dp[n] = 0，空后缀不需要费用
    for i in range(n - 1, -1, -1):          # 从右往左填表
        best = float('inf')
        # 枚举当前子数组的右端点 r
        for r in range(i, n):
            cur = sub_cost(i, r) + dp[r + 1]
            if cur < best:
                best = cur
        dp[i] = best

    return dp[0]                # 整个数组的最小费用
```

> **代码要点**  
> 1. `pre_num`、`pre_cost` 是「前缀和」，相当于一本「累计账本」，可以让我们在 `O(1)` 时间内算出任意区间的总和。  
> 2. `sub_cost(i, r)` 把题目给出的费用公式「翻译」成代码。这里的「乘法」和「加法」完全遵照题目描述。  
> 3. `dp[i]` 从右往左递推，保证在算 `dp[i]` 时，`dp[r+1]` 已经算好。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：外层循环遍历 `n` 个起点，内层循环遍历每个起点对应的所有右端点，最坏情况下是 `1 + 2 + … + n = n·(n+1)/2 ≈ n²/2`，所以是二次方级别。  
- **空间复杂度**：`O(n)`  
  解释：我们只用了 `pre_num、pre_cost、dp` 三个长度为 `n+1` 的数组，和常数级的临时变量，整体线性空间。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于「枚举所有右端点」的那层循环。  
观察费用公式：

```
subCost(l, r) = (sumNum[l…r]) * (sumCost[l…r]) + k * (sumCost[l…r])
```

把 `sumNum`、`sumCost` 用前缀和写成：

```
sumNum[l…r]  = pre_num[r+1] - pre_num[l]
sumCost[l…r] = pre_cost[r+1] - pre_cost[l]
```

把它代入 `dp` 的转移式：

```
dp[l] = min_{r ≥ l}  ( (pre_num[r+1] - pre_num[l]) * (pre_cost[r+1] - pre_cost[l])
                     + k * (pre_cost[r+1] - pre_cost[l])
                     + dp[r+1] )
```

把 `pre_num[l]`、`pre_cost[l]` 看成 **常数**（因为在算 `dp[l]` 时，这两个值已经固定），
我们可以把整个表达式重新整理成 **关于 r 的一次函数**：

```
dp[l] =  ( -pre_num[l] * pre_cost[l] - k * pre_cost[l] )          // 与 r 无关的常数
        +  min_{r ≥ l} ( pre_num[r+1] * pre_cost[r+1] + dp[r+1]
                         - pre_num[l] * pre_cost[r+1]
                         - k * pre_cost[r+1] )
```

令  

```
X_r = pre_cost[r+1]                     # 斜率（随 r 递增）
Y_r = pre_num[r+1] * pre_cost[r+1] + dp[r+1]   # 截距
```

则内部最小值可以写成：

```
min_{r ≥ l} ( Y_r - pre_num[l] * X_r - k * X_r )
        = min_{r ≥ l} ( (Y_r - k * X_r) - pre_num[l] * X_r )
```

这正是 **「在 X 轴上取斜率为 X_r，截距为 (Y_r - k*X_r) 的直线」**，  
我们需要求 **「在 x = pre_num[l]」处的最小值**。  
这正是**动态规划 + 凸包（Convex Hull Trick）** 可以在 **`O(log n)`** 或 **`O(1)`**（单调斜率）时间内完成的情形。

**关键观察**：

- `pre_cost`（即 `X_r`）是 **单调递增** 的，因为 `cost[i] ≥ 1`。  
- 当斜率单调时，维护下凸包（或者说“单调队列”）可以在 **摊销 O(1)** 时间完成插入与查询。

**步骤**：

1. **从右往左** 计算 `dp`（因为 `dp[l]` 依赖 `dp[r+1]`，而 `r+1 > l`）。  
2. 维护一个 **单调斜率的队列**，队列中每个元素对应一个候选 `r`，保存 `(X_r, Y_r - k*X_r)`。  
3. 对于当前 `l`，在队列中找 **使 `(Y - k*X) - pre_num[l] * X` 最小** 的直线。由于 `X` 单调递增，只需要比较队首的两条直线的值即可，弹出不再最优的那条。  
4. 计算 `dp[l]`，随后把对应的 `r = l-1`（即把 `l` 作为新的右端点）加入队列，保证斜率仍然单调。

这样，整个 DP 只需要 **一次遍历**，每个元素最多进出队列一次，时间 **`O(n)`**，空间 **`O(n)`**（存前缀和与 DP）。

#### 代码（Python）

```python
from collections import deque

def minimumCost(nums, cost, k):
    n = len(nums)

    # ---------- 前缀和 ----------
    pre_num = [0] * (n + 1)
    pre_cost = [0] * (n + 1)
    for i in range(n):
        pre_num[i + 1] = pre_num[i] + nums[i]
        pre_cost[i + 1] = pre_cost[i] + cost[i]

    # ---------- DP ----------
    dp = [0] * (n + 1)          # dp[n] = 0
    # 单调队列，存 (X, B)   其中 X = pre_cost[r+1]，B = pre_num[r+1]*pre_cost[r+1] + dp[r+1] - k*X
    hull = deque()

    # 初始时，r = n-1（即空后缀），对应的 X = pre_cost[n]，B = pre_num[n]*pre_cost[n] + dp[n] - k*X
    X_n = pre_cost[n]
    B_n = pre_num[n] * pre_cost[n] + dp[n] - k * X_n
    hull.append((X_n, B_n))

    # 辅助函数：两条直线 (X1,B1) 与 (X2,B2) 在 x 处的值
    def value(line, x):
        X, B = line
        return B - x * X          # 这里的公式是 (B) - x * (X)

    # 辅助函数：判断第 2 条线是否在第 3 条线之前就已经不可能成为最优
    # 使用交点比较，避免浮点数，直接用分式比较
    def is_bad(l1, l2, l3):
        # (B2 - B1) / (X2 - X1) >= (B3 - B2) / (X3 - X2)
        # 为避免除法，交叉相乘
        X1, B1 = l1
        X2, B2 = l2
        X3, B3 = l3
        return (B2 - B1) * (X3 - X2) >= (B3 - B2) * (X2 - X1)

    # 从右往左遍历 l
    for l in range(n - 1, -1, -1):
        x = pre_num[l]                     # 查询点

        # ① 在队首找最小值（单调查询）
        while len(hull) >= 2 and value(hull[0], x) >= value(hull[1], x):
            hull.popleft()                 # 舍弃已经不可能最优的直线

        best = value(hull[0], x)           # 这就是 min_{r≥l} (B - x*X)

        # ② 加上题目中与 l 本身有关的常数部分
        const = -pre_num[l] * pre_cost[l] - k * pre_cost[l]
        dp[l] = const + best

        # ③ 把以 r = l-1 为右端点的直线加入 hull
        #    对应的 X = pre_cost[l], B = pre_num[l]*pre_cost[l] + dp[l] - k*X
        X_new = pre_cost[l]
        B_new = pre_num[l] * pre_cost[l] + dp[l] - k * X_new
        new_line = (X_new, B_new)

        #   维护斜率单调（X_new 递减，因为我们从右往左插入），
        #   同时弹掉“坏”直线
        while len(hull) >= 2 and is_bad(hull[-2], hull[-1], new_line):
            hull.pop()
        hull.append(new_line)

    return dp[0]
```

> **代码要点**  
> 1. **前缀和** 与暴力解相同，用来快速求子数组的 `sumNum` 与 `sumCost`。  
> 2. **凸包（Convex Hull Trick）**：把每一个「右端点 `r`」对应的费用表达成一条直线 `y = B - x*X`，查询时只需要在当前 `x = pre_num[l]` 处取最小值。  
> 3. **单调队列**：因为 `X = pre_cost[r+1]` 随 `r` 单调递增（我们是逆序插入，所以在队列里是递减），可以用 `deque` 维护上凸包，做到摊销 `O(1)` 的插入和查询。  
> 4. `is_bad` 用交叉相乘避免浮点数，确保在整数范围内比较两条直线的交点位置。

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：每个位置 `l` 只做常数次队首/队尾操作，整体遍历一次即可。相比暴力的二次方，这就是 **线性** 的提升。  
- **空间复杂度**：`O(n)`  
  解释：需要保存前缀和、DP 表以及最多 `n` 条直线的队列，都是线性空间。

---

## 心得

- **核心技巧**：把「子数组费用」写成「斜率 × 变量 + 截距」的线性函数，利用 **单调斜率 + 凸包（Convex Hull Trick）** 把二次循环压到一次循环。  
- **适用场景**：  
  1. 动态规划转移式中出现 `dp[i] = min_{j>i} (A[j] * B[i] + C[j])`，且 `A[j]` 随 `j` 单调。  
  2. 「分段计费」类题目，例如「分割数组的最小代价」(`minimumCost`)、 「划分数组使每段代价为最大值」等。  
  3. 需要在「点的横坐标」上快速查询「最小/最大斜率线」的场景。  
- **一句话总结**：**把费用转化为「直线」并在单调斜率上维护上凸包，就能把 O(n²) 的 DP 变成 O(n)。**

---

## 反思

- **第一反应**：看到「划分子数组」立刻想到「区间 DP」——枚举左端点、右端点、递归求解后缀。于是写出暴力的 `O(n²)` 版。  
- **最容易踩的坑**：  
  1. **前缀和的下标**容易写错（`pre[i]` 表示前 `i` 个元素的和，取区间时要记得 `pre[r+1] - pre[l]`）。  
  2. **费用公式的展开**如果漏掉常数项 `-k*pre_cost[l]`，会导致答案整体偏大。  
  3. **凸包维护**时交点比较要用整数交叉相乘，否则会出现精度或除零错误。  
- **下次类似题**：第一步先 **写出费用的代数形式**，检查是否可以拆成「斜率 × 变量 + 截距」的线性函数；如果可以且斜率随索引单调，就立刻想到 **Convex Hull Trick**，把二次循环压到一次遍历。