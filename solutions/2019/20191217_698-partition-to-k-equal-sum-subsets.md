# #698. **分割成 K 个相等和的子集** / Partition to K Equal Sum Subsets

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Memoization、Bitmask · [LeetCode 链接](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/)

---

## 题目（英文原版）

**Description**

Given an integer array nums and an integer k, return true if it is possible to divide this array into k non-empty subsets whose sums are all equal.

**Examples**

**Example 1:**

```
Input: nums = [4,3,2,3,5,2,1], k = 4
Output: true
Explanation: It is possible to divide it into 4 subsets (5), (1, 4), (2,3), (2,3) with equal sums.
```

**Example 2:**

```
Input: nums = [1,2,3,4], k = 3
Output: false
```

**Constraints**

- 1 <= k <= nums.length <= 16
- 1 <= nums[i] <= 104
- The frequency of each element is in the range [1, 4].

---

## 题目（中文翻译）

给定一个整数数组（integer array）`nums` 和一个整数 `k`，如果可以将该数组划分为 `k` 个非空子集（subset），且每个子集的元素和都相等，则返回 `true`。

**示例 1**

```text
Input: nums = [4,3,2,3,5,2,1], k = 4
Output: true
Explanation: 可以将数组划分为 4 个子集 (5), (1, 4), (2, 3), (2, 3)，它们的和相等。
```

**示例 2**

```text
Input: nums = [1,2,3,4], k = 3
Output: false
```

**约束条件**

- `1 <= k <= nums.length <= 16`
- `1 <= nums[i] <= 10^4`
- 每个元素的出现次数在 `[1, 4]` 范围内。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个数字都尝试放进 k 个子集中的任意一个**，把所有可能的放法枚举完后，检查每个子集的和是否相等。

- **数据结构**  
  - `subset_sums`：长度为 `k` 的列表，`subset_sums[i]` 记录第 `i` 个子集目前的总和。可以把它想象成 **k 个装水的水桶**，我们每次往某个水桶里倒一个数字。  
  - `nums` 本身是一条**装满石子的链**，我们要把每块石子放进任意一个水桶。

- **为什么正确**  
  - 只要遍历了所有可能的放置方式，就一定能覆盖“是否可以恰好把所有石子分成 k 组且每组和相同”的答案。只要在递归结束时（所有数字都已经放完）检查 `subset_sums` 是否全部相等即可。

- **时间/空间复杂度**  
  - 对每个数字都有 `k` 种选择，递归深度为 `n = len(nums)`，所以**最坏情况**会产生 `k^n` 种放法。  
  - 用大白话说，`k^n` 就像 **把 n 把钥匙放进 k 把锁里，每把钥匙都有 k 种可能的锁**，组合数会非常大。  
  - 空间上只需要保存 `subset_sums`（`k` 个整数）和递归栈（最多 `n` 层），所以是 `O(k + n)`。

#### 代码（Python）

```python
def can_partition_bruteforce(nums, k):
    # 先算出每个子集应该达到的目标和
    total = sum(nums)
    if total % k != 0:               # 总和不能被 k 整除，肯定不行
        return False
    target = total // k

    # 递归搜索：把 idx 位置的数字放进任意一个子集
    def dfs(idx, subset_sums):
        if idx == len(nums):          # 所有数字都放完了
            # 检查每个子集的和是否都等于 target
            return all(s == target for s in subset_sums)

        cur = nums[idx]
        for i in range(k):
            # 如果放进第 i 个子集会超过目标和，直接跳过（剪枝）
            if subset_sums[i] + cur > target:
                continue
            subset_sums[i] += cur      # 把数字放进子集 i
            if dfs(idx + 1, subset_sums):
                return True
            subset_sums[i] -= cur      # 回溯，撤销选择

            # 如果子集 i 目前是空的（和为 0），后面的空子集也不会产生新解，
            # 可以直接剪枝，避免对称的重复搜索
            if subset_sums[i] == 0:
                break
        return False

    # 为了加速，先把大数放前面（大数更容易导致提前剪枝）
    nums.sort(reverse=True)
    return dfs(0, [0] * k)
```

#### 复杂度  

- **时间复杂度**：`O(k^n)`  
  - 解释：每个数字都有 `k` 种放法，所有组合数是指数级的。  
- **空间复杂度**：`O(k + n)`  
  - `k` 个子集的和 + 最深递归层数 `n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量的重复搜索**。我们可以从以下几个方向来削减搜索空间：

1. **目标和已知**  
   `target = sum(nums) / k`。只要每个子集的累计和不超过 `target`，就不必继续往里放。

2. **排序 + 大数优先**  
   把数组从大到小排序后先放大数。大数更容易触碰 `target`，能更早触发剪枝。

3. **使用“已使用”标记**  
   用一个布尔数组 `used[i]`（或位掩码）记录第 `i` 个数字是否已经放进某个子集，避免重复放置。

4. **递归的层次**  
   与其在每一步决定“把当前数字放进哪一个子集”，不如在每一次**尝试填满一个子集**。  
   - 当一个子集已经凑满 `target` 时，递归去填下一个子集。  
   - 这样只需要在 **当前子集内部** 做选择，搜索树更窄。

5. **对称性剪枝**  
   - 如果在填当前子集时，第一个空子集（和为 0）尝试失败，那么把相同的数字放进其他空子集也一定失败，直接返回 `False`。

6. **位掩码 DP（可选）**  
   对于 `len(nums) ≤ 16`，可以把“哪些数字已经被使用”压缩成一个 **16 位的整数**（位掩码）。  
   - `dp[mask]` 表示**已使用的数字集合 mask**对应的**当前子集的累计和**（模 `target`），即 `dp[mask] = cur_sum % target`。  
   - 当 `dp[mask] == 0` 且 `mask` 已经包含所有数字时，说明所有子集都恰好凑满。

下面给出两种实现：**回溯 + 剪枝**（更直观）和 **位掩码 DP**（更快）。

---

#### 代码（Python）——回溯+剪枝

```python
def can_partition(nums, k):
    total = sum(nums)
    if total % k != 0:          # 总和不能整除，直接返回 False
        return False
    target = total // k

    nums.sort(reverse=True)    # 大数在前，帮助提前剪枝
    if nums[0] > target:        # 最大的数已经大于目标和，必不可能
        return False

    used = [False] * len(nums)  # 记录每个数字是否已经被放进子集

    # 递归尝试填满第 cur_idx 个子集
    def backtrack(start_index, cur_sum, cur_idx):
        # 当前子集已经凑满 target，转向下一个子集
        if cur_sum == target:
            # 如果已经是第 k-1 个子集，说明前 k-1 个子集都凑满了，
            # 剩下的数字必然也能凑满最后一个子集
            return cur_idx == k - 1 or backtrack(0, 0, cur_idx + 1)

        # 在 nums[start_index:] 范围内尝试放入下一个数字
        for i in range(start_index, len(nums)):
            if used[i]:
                continue
            # 若放入后会超过目标和，直接跳过（剪枝）
            if cur_sum + nums[i] > target:
                continue

            used[i] = True
            if backtrack(i + 1, cur_sum + nums[i], cur_idx):
                return True
            used[i] = False   # 回溯

            # 关键剪枝：如果当前子集是空的（cur_sum == 0），
            # 第一次尝试放入的数字失败后，后面的数字即使换位也不会成功
            if cur_sum == 0:
                break
            # 如果放入后恰好等于 target，但仍然失败，说明后面的组合也不行
            if cur_sum + nums[i] == target:
                break
        return False

    return backtrack(0, 0, 0)
```

> **关键注释**  
> - `used[i]` 就像 **一本记事本**，记录第 `i` 本书是否已经被借走。  
> - `backtrack(0, 0, cur_idx + 1)` 表示“当前子集已经装满，换下一个空的背包”。  
> - `if cur_sum == 0: break` 是**对称性剪枝**，防止把相同的数字放进不同的空子集而产生重复搜索。

#### 代码（Python）——位掩码 DP（适用于 n ≤ 16）

```python
def can_partition_bitmask(nums, k):
    total = sum(nums)
    if total % k != 0:
        return False
    target = total // k
    n = len(nums)

    # 预处理：如果有元素本身大于 target，直接返回 False
    if max(nums) > target:
        return False

    # dp[mask] = 当前子集的累计和 % target，-1 表示不可达
    dp = [-1] * (1 << n)
    dp[0] = 0  # 空集合的累计和为 0

    for mask in range(1 << n):
        if dp[mask] == -1:          # 这个状态不可达，跳过
            continue
        for i in range(n):
            # 如果第 i 位已经被使用，跳过
            if mask & (1 << i):
                continue
            # 如果把 nums[i] 加进去会超过 target，跳过
            if dp[mask] + nums[i] > target:
                continue
            nxt = mask | (1 << i)   # 把第 i 个数字标记为已使用
            dp[nxt] = (dp[mask] + nums[i]) % target
    # 所有数字都被使用且 dp[full_mask] == 0，说明恰好分成 k 份
    return dp[(1 << n) - 1] == 0
```

> **位掩码解释**  
> - 把每个数字想象成 **一盏灯**，用 0/1 表示灯是否亮着。`mask` 就是一串二进制数字，记录哪些灯（数字）已经被点亮（使用）。  
> - `dp[mask]` 保存的是“当前子集已经装了多少”，但只保留 `target` 以内的余数，这样可以在加入新数字时快速判断是否会溢出。

#### 复杂度  

- **回溯+剪枝**  
  - 时间复杂度：最坏情况仍然是指数级，但剪枝大幅降低实际搜索次数。一般记作 `O(k * 2^{n})`，因为每个数字只会被尝试放进有限的子集。  
  - 空间复杂度：`O(n)`（递归栈）+ `O(n)`（used 数组）≈ `O(n)`。

- **位掩码 DP**  
  - 时间复杂度：`O(n * 2^{n})`（遍历所有子集状态，每个状态尝试加入最多 `n` 个数字）。  
    - 与暴力的 `k^{n}` 相比，`2^{n}` 对 `n ≤ 16` 来说是可接受的。  
  - 空间复杂度：`O(2^{n})` 用来保存 `dp` 表。  
  - 相比回溯，位掩码 DP 更“确定”，不会出现递归深度过深的情况。

---

## 心得

- **核心技巧**：**回溯 + 剪枝**（排序、大数优先、对称性剪枝）以及 **位掩码 DP**（把“已使用的数字集合”压缩成整数）。
- **适用题型**  
  1. “把数组划分成若干子集，使每个子集满足同一约束”——如 *Partition to K Equal Sum Subsets*、*Partition to K Subsets with Same Average*。  
  2. “在有限元素中选出若干组合满足目标和”——如 *Target Sum*、*Subset Sum*、*Matchsticks to Square*。  
  3. “元素数量不多（≤20），需要枚举子集状态”——如 *Maximum Sum of Two Non-Overlapping Subarrays*（位掩码版）等。
- **一句话总结解题钥匙**：**先算出目标值，排序后大数先放，用“已使用”标记和对称性剪枝把搜索树压到最小**。

---

## 反思

- **第一反应**：看到“把数组分成 k 组，和相等”，立刻想到**先算目标和**，然后**枚举每个数放进哪个组**（暴力）。
- **最容易踩的坑**  
  1. **总和不能被 k 整除**——这是最先可以判断的失败条件，忘记会导致不必要的搜索。  
  2. **最大元素 > target**——如果单个数字已经超过目标和，直接返回 `False`。  
  3. **对称性搜索**——没有剪枝会出现大量相同状态的重复遍历，导致超时。  
  4. **递归深度**——在 Python 中递归层数超过默认限制会报错，实际 `n ≤ 16` 不会触发，但仍需注意。  
- **下次遇到同类题的第一步**：  
  1. 计算并检查**可行性条件**（总和能否整除、最大值是否超限）。  
  2. **把数组降序**，准备好“先放大数”。  
  3. 决定使用**回溯 + 剪枝**还是**位掩码 DP**（看 `n` 的大小），再开始递归/状态转移。