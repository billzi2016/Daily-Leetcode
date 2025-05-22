# #3196. **最大化交替子数组的总成本** / Maximize Total Cost of Alternating Subarrays

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/maximize-total-cost-of-alternating-subarrays/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums with length n.
The cost of a subarray nums[l..r], where 0 <= l <= r < n, is defined as:
cost(l, r) = nums[l] - nums[l + 1] + ... + nums[r] * (−1)r − l
Your task is to split nums into subarrays such that the total cost of the subarrays is maximized, ensuring each element belongs to exactly one subarray.
Formally, if nums is split into k subarrays, where k > 1, at indices i1, i2, ..., ik − 1, where 0 <= i1 < i2 < ... < ik - 1 < n - 1, then the total cost will be:
cost(0, i1) + cost(i1 + 1, i2) + ... + cost(ik − 1 + 1, n − 1)
Return an integer denoting the maximum total cost of the subarrays after splitting the array optimally.
Note: If nums is not split into subarrays, i.e. k = 1, the total cost is simply cost(0, n - 1).

**Examples**

**Example 1:**

```
Input: nums = [1,-2,3,4]
Output: 10
Explanation:
One way to maximize the total cost is by splitting [1, -2, 3, 4] into subarrays [1, -2, 3] and [4] . The total cost will be (1 + 2 + 3) + 4 = 10 .
```

**Example 2:**

```
Input: nums = [1,-1,1,-1]
Output: 4
Explanation:
One way to maximize the total cost is by splitting [1, -1, 1, -1] into subarrays [1, -1] and [1, -1] . The total cost will be (1 + 1) + (1 + 1) = 4 .
```

**Example 3:**

```
Input: nums = [0]
Output: 0
Explanation:
We cannot split the array further, so the answer is 0.
```

**Example 4:**

```
Input: nums = [1,-1]
Output: 2
Explanation:
Selecting the whole array gives a total cost of 1 + 1 = 2 , which is the maximum.
```

**Constraints**

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums`。  
子数组 `nums[l..r]`（其中 `0 ≤ l ≤ r < n`）的成本定义为：

```
cost(l, r) = nums[l] - nums[l + 1] + … + nums[r] * (−1)^{r−l}
```

你的任务是将 `nums` 划分成若干子数组，使得这些子数组的 **总成本**（即各子数组成本之和）最大化，且每个元素恰好属于一个子数组。  

形式化地，如果将 `nums` 划分为 `k` 个子数组（`k > 1`），划分点为 `i₁, i₂, …, i_{k−1}`，满足 `0 ≤ i₁ < i₂ < … < i_{k−1} < n−1`，则总成本为：

```
cost(0, i₁) + cost(i₁+1, i₂) + … + cost(i_{k−1}+1, n−1)
```

返回在最优划分下子数组总成本的最大可能值。  

> **提示**：若不进行任何划分（即 `k = 1`），总成本即为 `cost(0, n−1)`。

---

### 示例

#### 示例 1
```
Input: nums = [1,-2,3,4]
Output: 10
Explanation:
一种使总成本最大的划分方式是把 [1, -2, 3, 4] 分成子数组 [1, -2, 3] 和 [4]。  
总成本为 (1 + 2 + 3) + 4 = 10 。
```

#### 示例 2
```
Input: nums = [1,-1,1,-1]
Output: 4
Explanation:
一种使总成本最大的划分方式是把 [1, -1, 1, -1] 分成子数组 [1, -1] 和 [1, -1]。  
总成本为 (1 + 1) + (1 + 1) = 4 。
```

#### 示例 3
```
Input: nums = [0]
Output: 0
Explanation:
数组已不可再划分，答案为 0。
```

#### 示例 4
```
Input: nums = [1,-1]
Output: 2
Explanation:
直接取整个数组的成本为 1 + 1 = 2，已是最大值。
```

---

### 约束条件

- `1 ≤ nums.length ≤ 10⁵`
- `-10⁹ ≤ nums[i] ≤ 10⁹`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的切分方式都枚举一遍**，然后把每一种切分得到的子数组的交替求和算出来，取最大值。  
- **枚举切分**：长度为 `n` 的数组在 `n‑1` 个位置之间可以选择“切”或“不切”。把每一种“切/不切”组合看成一条二进制序列（0 表示不切，1 表示切），共 `2^(n‑1)` 种可能。  
- **计算子数组代价**：对于固定的切分，我们可以从左到右遍历数组，遇到切点就重新开始交替求和。子数组的代价 `cost(l, r)` 正好是 `nums[l] - nums[l+1] + nums[l+2] - …`，相当于 **“正负交替”** 的求和。  
- **取最大**：把每一种切分得到的总代价保存下来，最后返回最大的那个。

> **类比**：把切分想成在一串珠子之间插入或不插“分隔符”。暴力解就是把所有可能的插法全部列出来，逐个算分数。

这种方法一定能得到正确答案，因为我们把**所有合法的切分**都检查了一遍，最大值必然在其中。

#### 代码（Python）

```python
from itertools import product
from typing import List

def maxCost_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    if n == 0:
        return 0

    # 2^(n-1) 种切分方式，用二进制位表示是否在 i 位置切分（i 为 0..n-2）
    best = -10**18
    for cuts in product([0, 1], repeat=n-1):          # 每个位置 0/1
        total = 0
        sign = 1                                      # 当前子数组的符号，子数组总是以 + 开头
        for i, x in enumerate(nums):
            total += sign * x                         # 加入当前元素（正负交替）
            # 看看下一个位置是否要切分
            if i < n-1 and cuts[i] == 1:              # 需要切分
                sign = 1                               # 新子数组重新以 + 开头
            else:
                sign *= -1                             # 交替符号翻转
        best = max(best, total)
    return best
```

> **关键行注释**  
> - `product([0,1], repeat=n-1)` 产生所有切分方案。  
> - `sign` 用来记录当前元素是加还是减，子数组开始时 `sign = 1`（加），随后每走一步翻转一次 `sign *= -1`。  
> - 当当前位置后面有切分 (`cuts[i] == 1`) 时，`sign` 重置为 `1`，相当于开启了新的子数组。

#### 复杂度  

- **时间复杂度**：`O(2^{n})`（严格来说是 `O(2^{n-1})`），因为我们要遍历所有切分方案。可以把它想成“指数级增长”，当 `n` 增加 1，计算量几乎会翻倍。  
- **空间复杂度**：`O(1)`（不计入递归栈或生成器本身的常数空间），只用几个临时变量。

> 对于 `n` 甚至达到 10 时，这种方法已经不可接受，更别说题目要求 `n` 可达 `10^5` 了。下面我们来找更快的办法。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到：**每一次切分其实就是把后面的元素重新“从 + 开始”**。换一种角度思考：

- 在原始的交替求和中，**每个位置的符号取决于它在子数组里的相对位置**（奇偶性）。  
- 如果我们把整个数组看成 **只用一个交替序列**（从第 0 位开始的 `+ - + - …`），那么一次切分的作用等价于**把切点后面的符号全部重置为 +**。  
- 这正好可以描述为：**我们可以把某些元素的符号改成负号（即“翻转”），但有两个限制**  
  1. **第一个元素**（数组最左端或每个子数组的第一个） **不能翻转**，因为子数组总是以 + 开头。  
  2. **两个相邻的元素不能同时翻转**，因为一旦在位置 `i` 翻转（相当于在 `i‑1` 与 `i` 之间切分），下一个位置 `i+1` 必须重新以 + 开始，不能再保持负号。

于是问题转化为：

> 在数组 `nums` 上，选取若干**不相邻**的位置（第 0 位除外）把它们的符号取负，使得最终的 **总和** 最大。

这正是经典的**“不能相邻取数”** 动态规划（也叫“房屋抢劫”）的变形，只是这里我们是 **加上原始的符号**。

我们用两种状态来描述前缀 `[0..i]` 的最优结果：

| 状态 | 含义 |
|------|------|
| `dp0[i]` | 处理到第 `i` 位时，**第 i 位没有被翻转**（即它保持正号），得到的最大总和。 |
| `dp1[i]` | 处理到第 `i` 位时，**第 i 位被翻转**（即它取负），得到的最大总和。|

**状态转移**  

- 若第 `i` 位 **不翻转**，它一定是 **+nums[i]**（因为子数组一定以 + 开头），而前面的 `i‑1` 位可以是任意合法状态：  
  `dp0[i] = max(dp0[i‑1], dp1[i‑1]) + nums[i]`  

- 若第 `i` 位 **翻转**，它必须是 **‑nums[i]**，并且 **前一个位置不能翻转**（否则会出现相邻翻转），所以只能接在 `dp0[i‑1]` 上：  
  `dp1[i] = dp0[i‑1] - nums[i]`

**初始状态**  

- `i = 0`（第一个元素）**不能翻转**，所以  
  `dp0[0] = nums[0]`  
  `dp1[0] = -inf`（用一个很小的数表示不合法）

- 为了避免在实现时处理 `i‑1` 越界，可以直接在循环里把 `dp0, dp1` 用两个变量滚动更新。

**答案**  

遍历完全部元素后，最后一个位置可以是翻转也可以是不翻转，取两者的最大值：  
`answer = max(dp0_last, dp1_last)`

**空间优化**  

因为每一步只依赖 `i‑1` 的状态，**不需要保存整个数组**，只保留两个变量即可，空间从 `O(n)` 降到 `O(1)`。

> **类比**：想象一条路上有若干盏灯，每盏灯可以开（+）或关（‑），但**两盏相邻的灯不能同时关**，而且第一盏灯必须开。我们要在满足这些规则的前提下，让所有灯的亮度之和最大。DP 就是在一步步决定第 `i` 盏灯开还是关，同时记录到目前为止的最佳亮度。

#### 代码（Python）

```python
from typing import List

def maxCost(nums: List[int]) -> int:
    """
    动态规划 O(n) 时间、O(1) 空间
    dp0: 前缀结束在 i 且第 i 位不翻转的最大和
    dp1: 前缀结束在 i 且第 i 位翻转的最大和（只能在 i>0 时出现）
    """
    if not nums:                     # 空数组直接返回 0（虽然题目不会出现）
        return 0

    # 第 0 位只能是正的
    dp0 = nums[0]                     # 不翻转
    dp1 = float('-inf')               # 不合法状态，用负无穷表示

    # 从第 1 位开始遍历
    for i in range(1, len(nums)):
        x = nums[i]

        # 新的状态必须基于旧的状态计算，先保存旧值防止被覆盖
        prev_dp0, prev_dp1 = dp0, dp1

        # 第 i 位不翻转 → +x
        dp0 = max(prev_dp0, prev_dp1) + x

        # 第 i 位翻转 → -x，前一位必须不翻转
        dp1 = prev_dp0 - x

    # 最终答案是两种状态的最大值
    return max(dp0, dp1)
```

> **关键行注释**  
> - `dp0 = max(prev_dp0, prev_dp1) + x`：不翻转时，前面可以是任意合法状态。  
> - `dp1 = prev_dp0 - x`：翻转时必须接在“前一位不翻转”的情况上，保证不出现相邻翻转。  
> - 使用 `float('-inf')` 把“非法”状态排除，使 `max` 时不会误选。

#### 复杂度  

- **时间复杂度**：`O(n)`。我们只遍历一次数组，每一步做常数次算术和比较。对比暴力的指数级，这就像把“一座高山”变成了“一条直路”。  
- **空间复杂度**：`O(1)`。只用了几个整数变量，不随 `n` 增长。

> 与暴力解相比，时间从 **指数级** 降到 **线性**，空间也保持常数，能够轻松处理 `n = 10^5` 的大规模输入。

---

## 心得  

- **核心技巧**：把“切分子数组”转化为“在原数组上选择不相邻的负号”，进而使用 **二状态动态规划**（不翻转 / 翻转）求最大交替和。  
- **相似题型**（可以练习同样思路）：  
  1. *House Robber*（不能相邻抢劫）  
  2. *Maximum Sum of Non‑Adjacent Elements*（不相邻最大子序和）  
  3. *Maximum Alternating Subarray Sum*（交替求和的变形）  
- **一句话总结**：**把切分看成“在某些位置强制重置符号”，再用 DP 记住“上一个位置是否已经重置”，即可线性求解。**

---

## 反思  

- **第一反应**：直接枚举切分或尝试递归分治，结果很快发现不可行。  
- **最容易踩的坑**：  
  - 第一个元素 **不能翻转**（必须是正号），否则会多算一次负号。  
  - 两个相邻元素 **不能同时翻转**，否则等价于在同一个子数组内部出现了两次“重新开始”。  
  - 处理负数极大时，使用 `float('-inf')` 或足够小的整数防止溢出。  
- **下次类似题目**：第一步先**抽象出“状态限制”**（比如相邻不能同时取、首位必须正），然后**设定 DP 状态**（是否选/是否翻转），写出转移方程，再考虑**空间优化**。这样可以快速从暴力思路跳到最优解。