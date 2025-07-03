# #3251. **Find the Count of Monotonic Pairs II** / Find the Count of Monotonic Pairs II

> 难度：困难 · 标签：Array、Math、Dynamic Programming、Combinatorics、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/find-the-count-of-monotonic-pairs-ii/)

---

## 题目（英文原版）

**Description**

You are given an array of positive integers nums of length n.
We call a pair of non-negative integer arrays (arr1, arr2) monotonic if:
Return the count of monotonic pairs.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums = [2,3,2]
Output: 4
Explanation:
The good pairs are:
```

**Example 2:**

```
Input: nums = [5,5,5,5]
Output: 126
```

**Constraints**

- 1 <= n == nums.length <= 2000
- 1 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个长度为 `n` 的正整数数组 `nums`。

我们称一对非负整数数组 `(arr1, arr2)` 为**单调的**（monotonic），如果满足以下条件：

（此处省略具体条件描述）

返回满足条件的单调对的数量。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

---

### 示例

#### 示例 1
**输入**  
``` 
nums = [2,3,2]
```  
**输出**  
```
4
```  
**解释**  
符合条件的配对有：

（此处省略具体配对列表）

#### 示例 2
**输入**  
``` 
nums = [5,5,5,5]
```  
**输出**  
```
126
```  
**解释**  
（此处省略具体解释）

---

### 约束条件

- `1 <= n == nums.length <= 2000`
- `1 <= nums[i] <= 1000`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求我们构造两条长度为 `n` 的非负整数数组 `arr1` 与 `arr2`，满足  

1. 对每一个下标 `i`，都有 `arr1[i] + arr2[i] = nums[i]`。  
2. `arr1` **单调不减**（后面的数不小于前面的数）。  
3. `arr2` **单调不增**（后面的数不大于前面的数）。  

> **类比**：  
> - 把 `arr1` 想成一本“升序词典”，词条只能往后变大或保持不变。  
> - 把 `arr2` 想成一本“降序词典”，词条只能往后变小或保持不变。  
> - 两本词典在同一页上相加得到 `nums[i]`。  

最直接的想法是：**枚举所有可能的 `(arr1[i], arr2[i])` 组合**，再检查单调性。  
对于每个 `i`，`arr1[i]` 可以是 `0 … nums[i]`（对应的 `arr2[i] = nums[i] - arr1[i]`），  
于是第 `i` 位有 `nums[i] + 1` 种取值。把所有位置的取值相乘，就得到所有“原始配对”的总数。  

然后，只要把每一种配对逐个验证 `arr1` 是否不减、`arr2` 是否不增，就能得到答案。  

> **为什么正确**：  
> - 我们遍历了 **所有** 满足 `arr1[i] + arr2[i] = nums[i]` 的配对，  
>   因此不可能漏掉任何合法解。  
> - 只要配对满足两条单调约束，就算是题目要求的“好配对”。  

> **复杂度**（大白话）：  
> - 每个位置最多有 `1000 + 1 = 1001` 种取值（因为 `nums[i] ≤ 1000`）。  
> - 如果直接把所有位置的取值枚举出来，时间复杂度是 `O(∏ (nums[i]+1))`，  
>   这在最坏情况下相当于 `O(1001^2000)`——根本不可计算。  
> - 空间上只需要存放当前枚举的配对，最多 `O(n)`。  

显然，暴力枚举根本跑不动，需要把 “单调约束” 融入到计数过程里，才能得到 **多项式时间** 的算法。

#### 代码（Python）

```python
MOD = 10**9 + 7

def brute(nums):
    n = len(nums)
    # 递归枚举所有 (a[i], b[i])，并在递归的过程中检查单调性
    ans = 0

    def dfs(i, prev_a, prev_b):
        """i：当前处理的位置，prev_a/prev_b：前一个位置的取值"""
        nonlocal ans
        if i == n:                     # 已经填完所有位置
            ans = (ans + 1) % MOD
            return

        for a in range(nums[i] + 1):   # a 可以是 0 … nums[i]
            b = nums[i] - a
            # 检查单调性：a 必须 >= prev_a，b 必须 <= prev_b
            if a >= prev_a and b <= prev_b:
                dfs(i + 1, a, b)

    # 第 0 位没有前驱，设前驱为最宽松的 -inf / +inf
    dfs(0, -float('inf'), float('inf'))
    return ans
```

> 代码里每一次递归都遍历 `0 … nums[i]`，所以时间随 `n` 指数增长，实际只能在 `n ≤ 5` 左右的小样例上跑通。

#### 复杂度  

- **时间复杂度**：`O(∏ (nums[i] + 1))`，相当于指数级别。  
  用大白话说，就是“每增加一个位置，就把可能的配对数乘以 1000 左右”，很快就爆炸。  
- **空间复杂度**：`O(n)`，递归栈的深度最多 `n`。

---

### 2. 最优解  

#### 思路  

从暴力解我们看到，**单调约束其实可以在计数时直接加入**，不必等到最后再去检验。  
关键是把 “`arr1` 不减、`arr2` 不增” 用等价的 **数值区间** 表达出来。

---

#### 2.1 把约束转化为对 `arr1` 的限制  

因为 `arr2[i] = nums[i] - arr1[i]`，  
`arr2` 单调不增 等价于：

```
nums[i] - arr1[i]   ≤   nums[i-1] - arr1[i-1]
⇔ arr1[i] - arr1[i-1]   ≥   nums[i] - nums[i-1]
```

于是对每个位置 `i (i ≥ 1)`，`arr1[i]` 必须满足两个条件  

1. **不小于前一个值**（`arr1` 不减）：`arr1[i] ≥ arr1[i-1]`  
2. **差值不少于 `nums` 的差**：`arr1[i] ≥ arr1[i-1] + max(0, nums[i] - nums[i-1])`

把它们合在一起：

```
let diff = max(0, nums[i] - nums[i-1])
arr1[i] ≥ arr1[i-1] + diff
```

同时，`arr1[i]` 不能超过 `nums[i]`（因为 `arr2[i]` 必须非负）：

```
0 ≤ arr1[i] ≤ nums[i]
```

> **直观解释**：  
> - 如果 `nums` 在当前位置升高了（比如从 3 变到 5），  
>   为了让 `arr2` 同时下降（保持 `arr1+arr2` 不变），  
>   `arr1` 必须 **至少** 跟着升高同样的幅度。  
> - 如果 `nums` 下降或不变，`arr1` 只要不降就行。

于是我们得到一个 **只和 `arr1` 相关的递推约束**：  
对每个 `i`，`arr1[i]` 必须在区间 `[L_i, R_i]` 中取值，其中  

```
R_i = nums[i]
L_i = arr1[i-1] + diff   (diff = max(0, nums[i] - nums[i-1]))
```

`L_i` 取决于前一个位置的取值 `arr1[i-1]`，这正好适合**动态规划**。

---

#### 2.2 动态规划设计  

**状态**  
`dp[i][v]`：考虑前 `i+1`（即下标 `0…i`）个位置，且 `arr1[i] = v` 时的合法配对数。

**初始状态**  
`i = 0` 时，`arr1[0]` 只要在 `0 … nums[0]` 之间即可（`arr2[0]` 自动满足），  
所以  

```
dp[0][v] = 1   for 0 ≤ v ≤ nums[0]
```

**转移**  

对于 `i ≥ 1`，设  

```
diff = max(0, nums[i] - nums[i-1])
```

要让 `arr1[i] = v` 合法，需要找所有可能的前驱 `u = arr1[i-1]`，满足  

```
u ≤ v - diff          (因为 v ≥ u + diff)
```

于是  

```
dp[i][v] = Σ_{u = 0}^{v-diff} dp[i-1][u]
```

这里的求和只和 `v` 和 `diff` 有关，可以用 **前缀和**把每一层的转移压到 `O(maxValue)`：

```
prefix[t] = Σ_{u = 0}^{t} dp[i-1][u]   （一次遍历得到）
dp[i][v] = prefix[v - diff]   （如果 v - diff < 0 则为 0）
```

**答案**  
最后一层 `i = n-1`，所有合法的 `arr1[n-1]`（即 `v`）都可以构成完整配对：

```
answer = Σ_{v = 0}^{nums[n-1]} dp[n-1][v]   (mod MOD)
```

---

#### 2.3 复杂度分析  

- `maxV = max(nums)` ≤ 1000。  
- 每一层我们遍历 `0 … maxV`，做一次前缀和，时间 `O(maxV)`。  
- 共 `n` 层，**总时间** `O(n * maxV)` ≤ `2000 * 1000 = 2·10⁶`，非常快。  

- 我们只保留上一层的 DP 表和当前层的 DP 表，**空间** `O(maxV)`。

> **大白话的时间解释**：  
> - 想象有 1000 格子（每格对应一种可能的 `arr1[i]` 的取值），  
>   对每一行（每个数组下标）我们只需要把上一行的累计和搬过去一次，  
>   所以整体工作量相当于“把 2000 张 1000 列的表格一次性填完”，  
>   这在电脑里只需要几毫秒。

---

#### 代码（Python）

```python
MOD = 10**9 + 7

def countMonotonicPairs(nums):
    """
    返回满足题目条件的 (arr1, arr2) 配对数，取模 1e9+7
    """
    n = len(nums)
    max_val = max(nums)                     # 最高可能的 arr1[i] 值

    # dp_prev[v] 表示上一行（i-1）时 arr1[i-1] = v 的方案数
    dp_prev = [0] * (max_val + 1)

    # 初始化 i = 0
    for v in range(nums[0] + 1):
        dp_prev[v] = 1

    # 逐行 DP
    for i in range(1, n):
        diff = max(0, nums[i] - nums[i - 1])   # 必须的最小增长量
        # 前缀和：pre[t] = Σ_{u=0}^{t} dp_prev[u]
        pre = [0] * (max_val + 1)
        running = 0
        for t in range(max_val + 1):
            running = (running + dp_prev[t]) % MOD
            pre[t] = running

        dp_cur = [0] * (max_val + 1)
        # 计算本行的 dp
        for v in range(nums[i] + 1):          # v 只能到 nums[i]
            limit = v - diff
            if limit >= 0:
                dp_cur[v] = pre[limit]        # 前缀和直接给出答案
            # else dp_cur[v] 保持 0

        dp_prev = dp_cur                       # 进入下一轮

    # 最后一行的所有 v 都是合法的终点
    ans = sum(dp_prev[:nums[-1] + 1]) % MOD
    return ans
```

> 关键行的中文注释已经写在代码里，直接复制运行即可得到正确答案。

#### 复杂度  

- **时间复杂度**：`O(n * max(nums))`  
  - 大白话：`n` 行，每行只遍历一次 0~1000 的格子，整个过程像是“把 2000 张 1000 列的表格一次性填完”。  
- **空间复杂度**：`O(max(nums))`  
  - 只保存两行 DP，类似只用两条绳子来搬运所有货物。

---

## 心得  

- **核心技巧**：把“两个数组分别单调不减/不增”转化为对单个数组 `arr1` 的 **区间约束**，随后使用 **一维动态规划 + 前缀和** 完成计数。  
- **此技巧适用的题型**：  
  1. “给定两条单调约束的数组，求满足和固定的配对数” （如本题）。  
  2. “在每一步只能向上或向下走一定步长，求路径数”——本质上也是把状态限制在区间内，用前缀和加速。  
  3. “数组分段限制 + 计数” 类的组合计数问题。  
- **一句话总结**：  
  **把双向单调条件合并成对单个数组的最小增长要求，然后用前缀和把“一层层累加”变成 O(1) 查询，即可在多项式时间内完成计数。**

---

## 反思  

- **第一反应**：看到 “单调不减 / 单调不增 + 和固定”，第一时间会想到直接枚举 `arr1[i]`，然后检查 `arr2`。这导致指数级暴力。  
- **最容易踩的坑**：  
  - 忽略 `arr2` 必须非负，导致 `arr1[i]` 上界写错。  
  - 在转移公式里忘记 `diff = max(0, nums[i] - nums[i-1])`，导致对下降的 `nums` 仍强制增长。  
  - 前缀和的下标越界（`v - diff` 可能为负）。  
- **下次类似题的第一步**：  
  **把所有约束写成对单个变量的上下界（区间），看能否用 DP + 前缀和/滑动窗口把区间求和加速**。这样往往可以把指数爆炸的暴力转化为线性或准线性复杂度的最优解。