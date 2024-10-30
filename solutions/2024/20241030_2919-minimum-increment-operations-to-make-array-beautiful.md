# #2919. 使数组美观的最小增量操作次数 / Minimum Increment Operations to Make Array Beautiful

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-increment-operations-to-make-array-beautiful/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums having length n, and an integer k.
You can perform the following increment operation any number of times (including zero):
An array is considered beautiful if, for any subarray with a size of 3 or more, its maximum element is greater than or equal to k.
Return an integer denoting the minimum number of increment operations needed to make nums beautiful.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [2,3,0,0,2], k = 4
Output: 3
Explanation: We can perform the following increment operations to make nums beautiful:
Choose index i = 1 and increase nums[1] by 1 -> [2,4,0,0,2].
Choose index i = 4 and increase nums[4] by 1 -> [2,4,0,0,3].
Choose index i = 4 and increase nums[4] by 1 -> [2,4,0,0,4].
The subarrays with a size of 3 or more are: [2,4,0], [4,0,0], [0,0,4], [2,4,0,0], [4,0,0,4], [2,4,0,0,4].
In all the subarrays, the maximum element is equal to k = 4, so nums is now beautiful.
It can be shown that nums cannot be made beautiful with fewer than 3 increment operations.
Hence, the answer is 3.
```

**Example 2:**

```
Input: nums = [0,1,3,3], k = 5
Output: 2
Explanation: We can perform the following increment operations to make nums beautiful:
Choose index i = 2 and increase nums[2] by 1 -> [0,1,4,3].
Choose index i = 2 and increase nums[2] by 1 -> [0,1,5,3].
The subarrays with a size of 3 or more are: [0,1,5], [1,5,3], [0,1,5,3].
In all the subarrays, the maximum element is equal to k = 5, so nums is now beautiful.
It can be shown that nums cannot be made beautiful with fewer than 2 increment operations.
Hence, the answer is 2.
```

**Example 3:**

```
Input: nums = [1,1,2], k = 1
Output: 0
Explanation: The only subarray with a size of 3 or more in this example is [1,1,2].
The maximum element, 2, is already greater than k = 1, so we don't need any increment operation.
Hence, the answer is 0.
```

**Constraints**

- 3 <= n == nums.length <= 105
- 0 <= nums[i] <= 109
- 0 <= k <= 109

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的整数数组 `nums`（长度为 `n`）和一个整数 `k`。  
你可以任意次数（包括 0 次）执行以下增量操作（increment operation）：

> 选择任意下标 `i`，将 `nums[i]` 的值加 1。

如果对于任意长度不少于 3 的子数组（subarray），其最大元素 **大于等于** `k`，则称数组 `nums` 为**美观**（beautiful）。  
返回使 `nums` 变为美观所需的最少增量操作次数。

**子数组（subarray）** 是数组中连续且非空的元素序列。

---

### 示例

**示例 1**  
```
Input: nums = [2,3,0,0,2], k = 4
Output: 3
Explanation: 我们可以按以下方式进行增量操作，使数组美观：
- 选择下标 i = 1，将 nums[1] 加 1 → [2,4,0,0,2]。
- 选择下标 i = 4，将 nums[4] 加 1 → [2,4,0,0,3]。
- 再次选择下标 i = 4，将 nums[4] 加 1 → [2,4,0,0,4]。

此时所有长度 ≥ 3 的子数组的最大值均 ≥ k = 4。
```

**示例 2**  
```
Input: nums = [0,1,3,3], k = 5
Output: 2
Explanation: 我们可以按以下方式进行增量操作，使数组美观：
- 选择下标 i = 2，将 nums[2] 加 1 → [0,1,4,3]。
- 再次选择下标 i = 2，将 nums[2] 加 1 → [0,1,5,3]。

长度 ≥ 3 的子数组为 [0,1,5], [1,5,3], [0,1,5,3]，它们的最大元素均等于 k = 5，满足美观条件。
```

**示例 3**  
```
Input: nums = [1,1,2], k = 1
Output: 0
Explanation: 唯一的长度为 3 的子数组是 [1,1,2]，其最大元素 2 已经 > k = 1，故无需任何增量操作，答案为 0。
```

### 约束条件
- `3 <= n == nums.length <= 10^5`
- `0 <= nums[i] <= 10^9`
- `0 <= k <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一个元素都尝试加到 ≥ k**，然后检查所有长度 ≥ 3 的子数组，看看条件是否满足。  
如果不满足，就再把某些元素继续加，直到所有子数组的最大值都 ≥ k 为止。  

可以用递归或穷举的方式枚举“哪些位置需要被提升”，每种方案都计算所需的总增量，然后取最小值。  

- **数据结构**：我们只需要一个普通的 Python 列表 `nums`，以及一个整数 `k`。  
- **类比**：把数组想象成一排房子，房子里的人身高是 `nums[i]`。要让每 **3** 间相邻的房子里至少有 **一个** 人的身高 ≥ k，就得给某些人“穿上增高鞋”。暴力解相当于把每个人的鞋子尺码从 0 开始，一点点往上试，看看哪几个人必须穿增高鞋才能满足要求。  

**为什么这个方法一定能得到答案？**  
因为我们枚举了 **所有** 可能的提升方案，必然包含最优方案。只要我们对每一种方案正确计算增量并验证条件，就一定能得到最小的增量。

**时间/空间复杂度**  
- 枚举所有可能的提升集合的数量是 2ⁿ（每个位置要么提升要么不提升），所以时间复杂度是 **O(2ⁿ)**。  
  - 这里的 “O(2ⁿ)” 可以想象成：如果 n=20，可能的方案就有 1,048,576 种；n=30 时就要超过十亿，根本不可行。  
- 只用了常数级的额外空间（递归栈深度最多 n），所以空间复杂度是 **O(n)**（用于保存递归调用的栈）。

显然，这种暴力做法只能在 n 极小（比如 n ≤ 20）时才会跑得完。我们需要更聪明的办法。

---

#### 代码（Python）

```python
from itertools import product

def min_increment_bruteforce(nums, k):
    n = len(nums)
    best = float('inf')                     # 记录目前找到的最小增量

    # 对每一种“是否提升”方案进行遍历，0 表示不提升，1 表示提升到 k
    for mask in product([0, 1], repeat=n):
        cur = nums[:]                        # 复制一份原数组
        inc = 0                              # 本方案的总增量

        # 按照 mask 把需要提升的元素加到 k
        for i, need in enumerate(mask):
            if need:                         # 需要提升
                inc += max(0, k - cur[i])
                cur[i] = max(cur[i], k)

        # 检查所有长度 ≥3 的子数组是否都满足 max ≥ k
        ok = True
        for i in range(n):
            for j in range(i + 3, n + 1):    # 子数组左闭右开区间 [i, j)
                if max(cur[i:j]) < k:
                    ok = False
                    break
            if not ok:
                break

        if ok:
            best = min(best, inc)            # 更新最小值

    return best if best != float('inf') else 0
```

> **提示**：这段代码仅用于演示思路，实际运行在 n=10 以上就会非常慢。

---

#### 复杂度  

- **时间复杂度**：`O(2ⁿ * n³)`。  
  - `2ⁿ` 来自所有可能的提升组合；  
  - 对每个组合我们要检查 `O(n³)`（所有子数组）是否满足条件。  
  - 实际上即使把子数组检查优化到 `O(n²)`，整体仍然是指数级的，根本不可接受。  
- **空间复杂度**：`O(n)`（复制数组 `cur` 以及递归/迭代的临时变量）。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**关键是找出哪些位置必须被提升到 ≥ k**。  
观察条件：

> 任意长度 ≥ 3 的子数组的最大值 ≥ k  
> ⇔ **每三个相邻的元素中，至少有一个 ≥ k**。

因为如果某个长度 3 的窗口已经满足条件，那么更长的窗口里必然包含这个窗口，从而也满足条件。  
因此我们只需要保证 **“没有连续 3 个元素都 < k”**。

把 “把元素提升到 ≥ k” 看成 **在数组的若干位置放置“哨兵”**（即该位置已经 ≥ k）。  
这些哨兵的距离不能超过 2（否则会出现 3 个连续位置没有哨兵）。  
这正好是一个 **覆盖问题**：用最少的“代价”在数轴上放置点，使得任意相邻的 3 个位置里至少有一个点。

**动态规划** 可以帮助我们在 O(n) 时间内求最小代价。  

设  

- `need[i] = max(0, k - nums[i])`：把第 i 个元素提升到 k 所需的最小增量（如果已经 ≥ k，则为 0）。  
- `dp[i]`：**前缀** `nums[0..i]` 已经满足“每三个相邻元素至少有一个 ≥ k”，且 **第 i 位一定是被提升的（即 ≥ k）** 时的最小总增量。

为什么要让 `dp[i]` 的第 i 位一定被提升？  
因为这样可以递归地把问题拆成“前面已经处理好，且最后一个哨兵在位置 i”，从而只需要考虑前面最近的三个位置是否可以作为上一个哨兵。

**状态转移**  

- 对于前 0、1、2 个位置，它们本身就是窗口长度 ≤ 3，直接把它们提升即可：
  ```text
  dp[0] = need[0]
  dp[1] = need[1]
  dp[2] = need[2]
  ```
- 对于 i ≥ 3，若把第 i 位设为哨兵，则它前面最近的哨兵可以出现在 i‑1、i‑2、i‑3 任意位置（因为相邻哨兵之间的距离 ≤ 2）。于是：
  ```text
  dp[i] = need[i] + min(dp[i-1], dp[i-2], dp[i-3])
  ```

**答案**  
整个数组的最后一个窗口可能在 `n-1`、`n-2`、`n-3` 结束，因此我们可以让最后一个哨兵出现在这三个位置中的任意一个：
```text
answer = min(dp[n-1], dp[n-2], dp[n-3])
```
（当 n 正好等于 3 时，这三个值其实是同一个 `dp[2]`，仍然成立。）

**类比**：把每个位置想成一块地，需要花 `need[i]` 钱把它变成“高地”。我们要在地上铺设“信号塔”，相邻两座塔之间的距离不能超过 2。`dp[i]` 就是“在第 i 块地建塔且之前所有需求都满足时的最少花费”。每次我们只需要看前面最近的三块地的最小花费，加上当前这块地的建塔费用，就是新的最小花费。

#### 代码（Python）

```python
def min_increment_beautiful(nums, k):
    """
    返回把 nums 变成 beautiful 所需的最小增量次数。
    思路：动态规划，保证每三个相邻元素里至少有一个 >= k。
    """
    n = len(nums)
    if n < 3:
        # 题目保证 n >= 3，这里仅作安全防护
        return 0

    # 需要把每个位置提升到 k 的代价
    need = [max(0, k - x) for x in nums]

    # dp[i] 表示前缀 [0..i] 已满足条件，且第 i 位一定被提升到 >= k 时的最小代价
    dp = [0] * n
    dp[0] = need[0]
    dp[1] = need[1]
    dp[2] = need[2]

    for i in range(3, n):
        dp[i] = need[i] + min(dp[i-1], dp[i-2], dp[i-3])

    # 最后一个哨兵可以出现在 n-1、n-2、n-3 中的任意位置
    return min(dp[n-1], dp[n-2], dp[n-3])
```

**代码要点注释**  

- `need[i] = max(0, k - x)`：如果已经 ≥ k，`need[i]` 为 0，表示不需要额外操作。  
- `dp[i] = need[i] + min(dp[i-1], dp[i-2], dp[i-3])`：把第 i 位提升后，前面最近的哨兵可以在 i‑1、i‑2、i‑3 任意位置，取最小的前缀代价即可。  
- `min(dp[n-1], dp[n-2], dp[n-3])`：保证整个数组的最后一个长度‑3 窗口也被覆盖。

---

#### 复杂度  

- **时间复杂度**：`O(n)`。  
  - 我们只遍历一次数组，计算 `need` 与 `dp`，每一步的操作都是常数时间。  
  - 与暴力的指数级时间相比，这就像把“遍历所有可能”变成了“只走一条直路”。  
- **空间复杂度**：`O(n)`（存 `need` 与 `dp`），如果想进一步压缩空间，只保留最近三个 `dp` 值，空间可以降到 `O(1)`。

---

## 心得  

- **核心技巧**：把“每三个相邻元素至少有一个 ≥ k”转化为“在数轴上放置间距 ≤ 2 的哨兵”，然后用**动态规划**求最小覆盖代价。  
- **适用的题型**  
  1. “每 m 个连续元素中至少要满足某个条件” 类似的覆盖问题（如每 2 个连续位置至少有一个奇数）。  
  2. “在序列上放置最少的灯塔/监视器，使得每段长度 ≤ L 都被覆盖” 的最小费用 DP。  
- **一句话总结解题钥匙**：把全局约束化为“局部窗口必须被至少一个已提升元素覆盖”，再用 DP 只关注最近的几种状态即可得到线性时间最优解。

---

## 反思  

- **第一反应**：直接想要把所有元素都提升到 k，或者暴力枚举哪些位置需要提升。  
- **最容易踩的坑**  
  - 忽略了 **长度大于 3 的子数组** 其实只需要检查长度恰为 3 的窗口即可。  
  - 误把 `dp[i]` 定义为“前 i 个元素都已满足”而不强制 `i` 位置被提升，导致状态转移不完整。  
  - 边界条件：当 `n` 正好等于 3 时，答案应直接是 `need[0] + need[1] + need[2]` 中的最小值（即 `min(dp[0], dp[1], dp[2])`），实现时要防止索引越界。  
- **下次类似题的第一步**：  
  1. 把题目中的 “任意长度 ≥ m 的子数组满足 …” **等价转化** 为 “每长度恰为 m 的窗口必须满足 …”。  
  2. 观察窗口之间的**重叠关系**，思考是否可以用“覆盖”或“间距限制”来描述，然后尝试用 DP 或贪心在 **O(n)** 里求解。