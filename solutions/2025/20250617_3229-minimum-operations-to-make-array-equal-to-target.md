# #3229. 使数组等于目标的最小操作次数 / Minimum Operations to Make Array Equal to Target

> 难度：困难 · 标签：Array、Dynamic Programming、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-array-equal-to-target/)

---

## 题目（英文原版）

**Description**

You are given two positive integer arrays nums and target, of the same length.
In a single operation, you can select any subarray of nums and increment each element within that subarray by 1 or decrement each element within that subarray by 1.
Return the minimum number of operations required to make nums equal to the array target.

**Examples**

**Example 1:**

```
Input: nums = [3,5,1,2], target = [4,6,2,4]
Output: 2
Explanation:
We will perform the following operations to make nums equal to target : - Increment nums[0..3] by 1, nums = [4,6,2,3] . - Increment nums[3..3] by 1, nums = [4,6,2,4] .
```

**Example 2:**

```
Input: nums = [1,3,2], target = [2,1,4]
Output: 5
Explanation:
We will perform the following operations to make nums equal to target : - Increment nums[0..0] by 1, nums = [2,3,2] . - Decrement nums[1..1] by 1, nums = [2,2,2] . - Decrement nums[1..1] by 1, nums = [2,1,2] . - Increment nums[2..2] by 1, nums = [2,1,3] . - Increment nums[2..2] by 1, nums = [2,1,4] .
```

**Constraints**

- 1 <= nums.length == target.length <= 105
- 1 <= nums[i], target[i] <= 108

---

## 题目（中文翻译）

给定两个长度相同的正整数数组 `nums` 和 `target`。  
在一次操作中，你可以选择 `nums` 的任意子数组（subarray），将该子数组中的每个元素全部加 1，或者全部减 1。  
返回使 `nums` 变为 `target` 所需的最小操作次数。

**示例 1**  
**输入**: `nums = [3,5,1,2]`, `target = [4,6,2,4]`  
**输出**: `2`  
**解释**:  
我们可以按以下操作将 `nums` 变为 `target`：  
- 将 `nums[0..3]` 增加 1，得到 `nums = [4,6,2,3]`。  
- 将 `nums[3..3]` 增加 1，得到 `nums = [4,6,2,4]`。

**示例 2**  
**输入**: `nums = [1,3,2]`, `target = [2,1,4]`  
**输出**: `5`  
**解释**:  
我们可以按以下操作将 `nums` 变为 `target`：  
- 将 `nums[0..0]` 增加 1，得到 `nums = [2,3,2]`。  
- 将 `nums[1..1]` 减少 1，得到 `nums = [2,2,2]`。  
- 再将 `nums[1..1]` 减少 1，得到 `nums = [2,1,2]`。  
- 将 `nums[2..2]` 增加 1，得到 `nums = [2,1,3]`。  
- 再将 `nums[2..2]` 增加 1，得到 `nums = [2,1,4]`。

**约束条件**  
- `1 <= nums.length == target.length <= 10^5`  
- `1 <= nums[i], target[i] <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **一步步把 `nums` 调整成 `target`**，每一次只对一个满足条件的子数组做 `+1` 或 `-1`。  
可以把数组想象成一排水槽，`nums[i]` 是第 i 个水槽里当前的水位，`target[i]` 是我们想要的水位。  
一次操作就像把一段连续的水槽里的水全部往上倒（`+1`）或往下倒（`-1`）。

暴力实现的思路：

1. 计算每个位置还差多少，记为 `diff[i] = target[i] - nums[i]`。  
   - 正数表示需要把该位置 **升高**（要加），负数表示需要 **降低**（要减）。
2. 从左到右遍历 `diff`，只要当前位置不为 0，就把它所在的最长连续段（同号）全部一次性 `+1` 或 `-1`，直到该段全部归零。  
3. 重复上述步骤，直到所有 `diff` 都变成 0。

> **为什么能得到正确答案？**  
> 每次我们都选取当前仍然不为 0 的最左边位置，并把它所在的同号连续段全部向正确方向移动 1 步。这样不会错过任何必须进行的操作，因为每个位置的差值只能通过一次次的 `+1`/`-1` 来消除。

> **时间/空间复杂度**  
> - 每一次完整的遍历最多把所有差值的绝对值 **各减 1**，所以最坏情况下要遍历 `max(|diff[i]|)` 次。  
> - 若数组长度为 `n`，最大差值记为 `M`（`M = max_i |diff[i]|`），则时间复杂度是 **O(n·M)**，在数据范围 `nums[i] ≤ 10^8` 时几乎不可接受。  
> - 只需要额外的 `diff` 数组，空间复杂度是 **O(n)**。

#### 代码（Python）

```python
def minOperations_bruteforce(nums, target):
    # 计算差值数组
    diff = [t - n for n, t in zip(nums, target)]
    ops = 0                       # 记录操作次数

    while any(d != 0 for d in diff):   # 只要还有非零的地方就继续
        i = 0
        while i < len(diff):
            if diff[i] == 0:          # 已经对齐，跳过
                i += 1
                continue

            # 确定本次操作的方向（+1 或 -1）
            step = 1 if diff[i] > 0 else -1

            # 找到同号的最长连续子数组
            j = i
            while j < len(diff) and diff[j] * step > 0:
                j += 1

            # 对子数组 [i, j-1] 做一次 +1 / -1
            for k in range(i, j):
                diff[k] -= step       # 因为 diff = target - nums，减去 step 相当于把 nums 加 step
            ops += 1
            i = j                      # 继续检查后面的元素

    return ops
```

#### 复杂度

- **时间复杂度**：`O(n·M)`，其中 `M = max_i |target[i] - nums[i]|`。  
  大白话：如果最大差距是 1000，数组长度是 10⁵，最坏要跑 10⁸ 步，太慢了。  
- **空间复杂度**：`O(n)`，只用了一个和原数组等长的差值数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**每一次我们都在把一段连续的差值统一向同一个方向移动 1 步**。  
如果把每一次的 “移动 1 步” 看成 **在差值数组上增加或减少 1**，其实我们只关心 **差值何时需要“向上”**（从更小的值变到更大的值），因为向下的过程已经在之前的向上操作里被“覆盖”了。

**关键观察**  

- 令 `a[i] = target[i] - nums[i]`（记作 **差值数组**）。  
- 设 `prev` 为左边已经处理好的“基准高度”。初始 `prev = 0`（相当于左边的虚拟位置  -1 的差值是 0）。  
- 当遍历到第 `i` 位时，如果 `a[i] > prev`，说明 **需要把高度从 `prev` 提升到 `a[i]`**，这必须额外进行 `a[i] - prev` 次子数组 `+1`（如果 `a[i]` 为负，则这一步是 **子数组 `-1`**）。  
- 如果 `a[i] <= prev`，只需要把基准降低到 `a[i]`，**不需要额外的操作**，因为之前提升的操作已经覆盖了这段区间。

于是答案就是 **所有“向上提升” 的幅度之和**：

\[
\text{ans} = \sum_{i=0}^{n-1} \max(0,\; a[i] - a[i-1]),\quad a[-1]=0
\]

> **为什么只算“向上提升”？**  
> 想象把差值画在坐标轴上，操作相当于在某段区间画一条水平线向上（`+1`）或向下（`-1`）。每一次向上画线都需要一次新的操作，向下的线可以直接在之前向上画的线的右端点“收回”，不产生额外计数。  

> **与暴力的区别**  
> 暴力每次只移动 **1 步**，需要重复 `M` 次；最优解一次性把同一段连续的提升全部算进去，只遍历一次数组，时间是 **O(n)**。

#### 代码（Python）

```python
def minOperations(nums, target):
    """
    返回把 nums 变成 target 所需的最少子数组 +1 / -1 操作次数
    思路：把差值数组 a[i] = target[i] - nums[i] 看作高度，
          只统计从左到右的“向上提升”幅度之和。
    """
    ans = 0          # 记录总操作数
    prev = 0         # 左侧已经达到的高度（虚拟的 a[-1]）

    for n, t in zip(nums, target):
        cur = t - n                     # 当前差值 a[i]
        if cur > prev:                  # 需要向上提升
            ans += cur - prev           # 计入提升的幅度
        prev = cur                      # 更新基准高度

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`，只遍历一次数组。  
  大白话：即使数组有 10⁵ 个元素，也只需要 10⁵ 步，瞬间搞定。  
- **空间复杂度**：`O(1)`，只用了几个整数变量，不随 `n` 增长。

---

## 心得

- **核心技巧**：把「区间增/减 1」转换为「高度变化」的问题，只统计从左到右的正向（向上）高度差。  
- **适用的题型**  
  1. **把数组变成全零**（如本题的差值化简）  
  2. **最小次数使数组单调递增/递减**（同样可以用正向高度差累加）  
  3. **区间操作转前缀和/差分**（如“最小加法次数”系列）  
- **一句话总结**：**把每一次子数组的 +1/-1 看成在差值图上的一次“向上画线”，答案就是所有向上段的长度之和。**

---

## 反思

- **第一反应**：直接模拟每一次子数组的增减，写个循环把差值一点点消掉。  
- **最容易踩的坑**  
  - 忽视 **负数差值**：`target[i] < nums[i]` 时需要用 “减 1”，但同样可以用 “向上提升” 的思路处理。  
  - **边界条件**：把 `prev` 初始化为 0（相当于在数组左侧虚拟一个高度为 0 的位置），否则会少算第一个元素的操作。  
- **下次遇到同类题**：第一步先 **把原问题转化为“让差值数组变成全零”**，再思考 **“从左到右，何时需要额外的操作”**，即统计正向高度差。这样即可直接得到线性时间解。