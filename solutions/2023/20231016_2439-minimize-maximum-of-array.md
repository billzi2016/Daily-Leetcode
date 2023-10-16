# #2439. 最小化数组的最大值 / Minimize Maximum of Array

> 难度：中等 · 标签：Array、Binary Search、Dynamic Programming、Greedy、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimize-maximum-of-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums comprising of n non-negative integers.
In one operation, you must:
Return the minimum possible value of the maximum integer of nums after performing any number of operations.

**Examples**

**Example 1:**

```
Input: nums = [3,7,1,6]
Output: 5
Explanation:
One set of optimal operations is as follows:
1. Choose i = 1, and nums becomes [4,6,1,6].
2. Choose i = 3, and nums becomes [4,6,2,5].
3. Choose i = 1, and nums becomes [5,5,2,5].
The maximum integer of nums is 5. It can be shown that the maximum number cannot be less than 5.
Therefore, we return 5.
```

**Example 2:**

```
Input: nums = [10,1]
Output: 10
Explanation:
It is optimal to leave nums as is, and since 10 is the maximum value, we return 10.
```

**Constraints**

- n == nums.length
- 2 <= n <= 105
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个下标从 **0** 开始的整数数组 `nums`，其中包含 `n` 个非负整数。

在一次 **操作（operation）** 中，你必须选择一个满足 `1 ≤ i < n` 的下标 `i`，并执行以下变更：

- 将 `nums[i - 1]` 增加 `1`；
- 将 `nums[i]` 减少 `1`。

你可以对数组执行任意次数的上述操作（包括零次）。返回在所有可能的操作序列执行完毕后，数组中最大整数的最小可能取值。

**示例 1：**  
输入：`nums = [3,7,1,6]`  
输出：`5`  
解释：  
一种最优的操作序列如下：  
1. 选择 `i = 1`，数组变为 `[4,6,1,6]`。  
2. 选择 `i = 3`，数组变为 `[4,6,2,5]`。  
3. 选择 `i = 1`，数组变为 `[5,5,2,5]`。  
此时数组的最大值为 `5`，且可以证明最大值不可能小于 `5`，因此返回 `5`。

**示例 2：**  
输入：`nums = [10,1]`  
输出：`10`  
解释：  
保持原数组不变即可，此时最大值为 `10`，返回 `10`。

**约束条件：**  

- `n == nums.length`
- `2 ≤ n ≤ 10^5`
- `0 ≤ nums[i] ≤ 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把每一次可以进行的转移操作都枚举**，尝试所有可能的转移顺序，最后记录下得到的数组的最大值的最小情况。  

- **数据结构**：我们只需要原始的 `list nums`，在递归或循环里把它原地改动（把第 `i` 位的 1 移到 `i‑1` 位），相当于在“搬砖”。可以把数组想象成一排水槽，操作就是把水往左边的水槽倒一滴。  
- **为什么正确**：只要把所有合法的搬砖序列都遍历一遍，就一定能找到最优的那个序列——这就是“穷举”。  
- **复杂度分析**：  
  - 每一次操作都有 `n‑1` 种可能的选择（任选一个 `i>0`），而操作次数本身没有上限（只要还能让某个位置的数减小就可以继续）。所以搜索树的深度和分支都会非常大，最坏情况下的时间是 **指数级**（类似 `O( (n‑1)^k )`，`k` 是操作次数），根本不可接受。  
  - 空间上，只需要保存递归栈或临时数组，最多 `O(n)`。  

> **大白话**：如果把每一步都写成“把第 i 个盒子里的球往左边的盒子倒一个”，暴力解相当于把所有可能的倒球顺序都列出来检查，这就像把所有可能的排队方式都尝试一遍，人数多了根本排不完。

#### 代码（Python）

```python
def brute_force(nums):
    """
    暴力搜索所有可能的转移序列（仅作概念演示，实际会超时）。
    """
    n = len(nums)
    best = max(nums)                     # 当前找到的最小的最大值

    def dfs(arr):
        nonlocal best
        cur_max = max(arr)
        # 已经比已知的更差，剪枝
        if cur_max >= best:
            return
        # 记录当前状态的最大值
        best = min(best, cur_max)

        # 尝试把每个 i>0 的 1 向左搬一次
        for i in range(1, n):
            if arr[i] == 0:               # 没有可以搬的了
                continue
            arr[i] -= 1
            arr[i - 1] += 1
            dfs(arr)                       # 继续搜索
            # 恢复现场
            arr[i] += 1
            arr[i - 1] -= 1

    dfs(nums[:])                          # 使用副本防止修改原数组
    return best
```

> 这段代码只能在 `n` 很小（比如 `n ≤ 6`）时跑得完，主要用来帮助我们理解“最原始的想法”。

#### 复杂度  

- **时间复杂度**：`O(exponential)`（指数级），因为每一步都有 `n‑1` 种选择，且没有明确的深度上限。  
- **空间复杂度**：`O(n)`，递归栈最多保存 `n` 层。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**不停地模拟每一次搬砖**，而实际上我们只关心**是否可以让所有位置的数都不超过某个阈值 `M`**。只要能判断 “给定的 `M` 能否实现”，就可以用 **二分搜索** 找到最小的可行 `M`。

**关键观察**  

1. **只能往左搬**，所以左边的元素永远只能收到右边的“水”，不会失去自己的值。  
2. 对于前缀 `[0 … i]`，所有右边元素向左搬的水最终都会汇聚到这段前缀里。于是**这段前缀的总和**在任何时刻都是不变的：`prefix_sum = sum(nums[0..i])`。  
3. 如果我们要求每个位置的值都 ≤ `M`，那么这段前缀里最多只能放 `M` 这么大 * `i+1`（长度）* 的水。换句话说：  

   \[
   \text{prefix\_sum} \le M \times (i+1)
   \]

   只要有一个前缀不满足，上面的不等式，就说明 **`M` 太小，无法实现**。  
4. 因此，判断 `M` 可行只需要一次线性遍历，检查所有前缀是否满足上述不等式。  

**二分搜索**  

- **搜索区间**：最小可能的最大值显然不低于 `0`，上界可以取原数组的最大值 `max(nums)`（因为不进行任何操作时的最大值就是上界）。  
- **判定函数** `can(M)`：遍历数组，累加前缀和 `s`，若出现 `s > M * (i+1)`，立刻返回 `False`；遍历结束都没冲突则返回 `True`。  
- **二分过程**：  
  - `low = 0`，`high = max(nums)`  
  - 当 `low < high` 时，取 `mid = (low + high) // 2`  
  - 若 `can(mid)` 为真，说明 `mid` 已经可行，尝试更小的值 `high = mid`；否则 `low = mid + 1`。  
- 循环结束时 `low`（或 `high`）即为答案。  

**类比**：把每个前缀想象成一只容器，容器容量是 `M * 长度`，而水的总量是前缀和。只要每个容器都能装下它对应的水，就说明我们能把所有水往左搬，使每个格子的水不超过 `M`。

#### 代码（Python）

```python
from typing import List

def minimizeArrayValue(nums: List[int]) -> int:
    """
    二分搜索答案 + 前缀和判定
    时间复杂度 O(n log Max) ，空间复杂度 O(1)
    """
    n = len(nums)

    # ---------- 判定函数 ----------
    def can(limit: int) -> bool:
        """
        判断是否可以让数组的最大值 <= limit
        思路：遍历前缀，确保前缀和不超过 limit * (i+1)
        """
        prefix = 0
        for i, v in enumerate(nums):
            prefix += v                # 当前前缀和
            # 如果前缀和已经大于容量，说明 limit 太小
            if prefix > limit * (i + 1):
                return False
        return True

    # ---------- 二分搜索 ----------
    low, high = 0, max(nums)          # 答案一定在这个闭区间内
    while low < high:
        mid = (low + high) // 2
        if can(mid):                  # mid 可行，尝试更小
            high = mid
        else:                         # mid 不行，需要更大
            low = mid + 1
    return low
```

#### 复杂度  

- **时间复杂度**：`O(n log Max)`  
  - `n` 是数组长度（最多 `10⁵`），`Max` 是数组中最大元素（≤ `10⁹`）。  
  - 二分搜索的迭代次数大约是 `log₂(Max) ≈ 30`，每次遍历一次数组。  
  - 与暴力解相比，**把指数级的搜索压缩成了线性乘以常数 30**，快得多。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量（前缀和、指针），没有额外的数组或递归栈。  

---

## 心得  

- **核心技巧**：利用**前缀和 + 单调约束**把“能否实现”转化为**每个前缀的平均值 ≤ M**，再配合**二分搜索**找到最小可行的 `M`。  
- **适用场景**：  
  1. “只能往左/右搬运” 的数组问题（如 LeetCode 2079 “Minimize Maximum of Array”）。  
  2. 需要在**单调约束**下求最小/最大可行值的题目，例如“分配糖果”“最小化最大子数组和”。  
  3. 任何可以用**前缀和上界**判定的优化类问题。  
- **一句话总结**：**把“最大值 ≤ M”转化为“每个前缀的平均 ≤ M”，二分搜索最小的 M**。

---

## 反思  

- **第一反应**：看到“只能把右边的数往左搬”，自然想到**模拟搬砖**，但立刻会感觉到搜索空间爆炸。  
- **最容易踩的坑**：  
  - 忘记 **前缀长度** (`i+1`) 乘上 `M`，导致判定条件写成 `prefix > M`（明显错误）。  
  - 二分的边界写错：如果把 `low` 初始设为 `max(nums)`，会直接返回错误答案。  
  - 需要使用 **整数乘法** 防止浮点误差，直接比较 `prefix > limit * (i+1)`。  
- **下次思路**：遇到“只能单向搬移/合并” 的问题，第一步先思考 **“整体量不变，局部约束如何表达？”**，尝试用 **前缀和 + 单调不等式** 构造判定函数，然后再决定是否使用二分或贪心。