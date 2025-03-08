# #3097. OR 至少为 K 的最短子数组 II / Shortest Subarray With OR at Least K II

> 难度：中等 · 标签：Array、Bit Manipulation、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/shortest-subarray-with-or-at-least-k-ii/)

---

## 题目（英文原版）

**Description**

You are given an array nums of non-negative integers and an integer k.
An array is called special if the bitwise OR of all of its elements is at least k.
Return the length of the shortest special non-empty subarray of nums, or return -1 if no special subarray exists.

**Examples**

**Example 1:**

```
Input: nums = [1,2,3], k = 2
Output: 1
Explanation:
The subarray [3] has OR value of 3 . Hence, we return 1 .
```

**Example 2:**

```
Input: nums = [2,1,8], k = 10
Output: 3
Explanation:
The subarray [2,1,8] has OR value of 11 . Hence, we return 3 .
```

**Example 3:**

```
Input: nums = [1,2], k = 0
Output: 1
Explanation:
The subarray [1] has OR value of 1 . Hence, we return 1 .
```

**Constraints**

- 1 <= nums.length <= 2 * 105
- 0 <= nums[i] <= 109
- 0 <= k <= 109

---

## 题目（中文翻译）

给定一个由非负整数构成的数组 `nums` 和一个整数 `k`。若一个数组的所有元素的按位或（bitwise OR）结果不少于 `k`，则称该数组为 **特殊数组**。返回 `nums` 中最短的、非空的、满足上述条件的特殊子数组（subarray）的长度；如果不存在任何特殊子数组，返回 `-1`。

## 示例

### 示例 1
**输入**  
```text
nums = [1,2,3], k = 2
```
**输出**  
```text
1
```
**解释**  
子数组 `[3]` 的 OR 值为 `3`，满足不少于 `k`，因此返回长度 `1`。

### 示例 2
**输入**  
```text
nums = [2,1,8], k = 10
```
**输出**  
```text
3
```
**解释**  
子数组 `[2,1,8]` 的 OR 值为 `11`，满足条件，最短长度为 `3`。

### 示例 3
**输入**  
```text
nums = [1,2], k = 0
```
**输出**  
```text
1
```
**解释**  
子数组 `[1]` 的 OR 值为 `1`，已经不小于 `k`，返回长度 `1`。

## 约束条件
- `1 <= nums.length <= 2 * 10^5`
- `0 <= nums[i] <= 10^9`
- `0 <= k <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把所有可能的子数组都枚举一遍，算出它们的 **按位或（OR）**，看看是否≥`k`，如果满足就把长度记下来，最后取最小值。

- **枚举子数组**：外层循环固定子数组的左端点 `l`，内层循环把右端点 `r` 从 `l` 推向数组末尾。  
- **计算 OR**：在固定左端点的情况下，随着右端点向右移动，只要把新加入的元素和当前的 OR 做一次 `|` 运算，就得到新的子数组 OR。  
- **生活化类比**：把数组想成一排灯泡，每个灯泡的亮度用二进制位表示。把子数组的 OR 看作把这些灯泡的亮光“合并”在一起，只要有一盏灯亮起的位就会被点亮。我们要找的就是“点亮的亮光≥k”且灯泡最少的那段连续灯泡。

这种做法一定能得到正确答案，因为我们把 **所有** 子数组都检查了一遍，漏掉的情况不存在。

#### 代码（Python）

```python
def shortestSubarray(nums, k):
    n = len(nums)
    ans = float('inf')                     # 用无穷大表示暂未找到答案

    for left in range(n):                  # 枚举左端点
        cur_or = 0                         # 当前子数组的 OR
        for right in range(left, n):       # 向右扩展右端点
            cur_or |= nums[right]          # 加入新元素，更新 OR
            if cur_or >= k:                # 满足要求
                ans = min(ans, right-left+1)   # 记录更短的长度
                break                      # 已经是以 left 为左端点的最短了，直接跳出

    return -1 if ans == float('inf') else ans
```

> 关键行解释  
> - `cur_or |= nums[right]`：把新加入的元素的二进制位“打开”，相当于把灯泡的亮光并到一起。  
> - `if cur_or >= k:`：只要合并后的亮光强度不小于 `k`，说明找到了一个合法子数组。  
> - `break`：因为右端点已经尽可能靠左了，继续往右只会让子数组更长，长度不可能再更小。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 想象一下 `n=10⁵` 时，需要检查 10⁹ 次子数组，这在实际运行中会超时。这里的 “²” 表示 **平方**，也就是随着数组长度 `n` 的增长，耗时会以 `n` 的二次方速度增长，增长得非常快。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`cur_or、ans、left、right`），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历很多右端点**。如果我们能够在遍历一次数组的过程中，同时维护当前窗口（子数组）的 OR，并在满足条件时尽可能把左端点往右收缩，就能把时间降到线性级别。

**关键观察**  

- 按位或的特性：  
  - **只会把 0 变成 1，永远不会把 1 变回 0**。  
  - 因此，当我们把左端点向右移动（即“删掉”一个元素）时，窗口的 OR **可能会下降**，但只能因为某个位的出现次数从 ≥1 变成了 0。  

- **记录每一位出现的次数**：  
  - 用一个长度为 31（因为 `nums[i] ≤ 10⁹ < 2³⁰`）的数组 `cnt[bit]`，`cnt[b]` 表示当前窗口中第 `b` 位为 1 的元素个数。  
  - 窗口的 OR 可以随时通过 `cnt` 计算出来：只要 `cnt[b] > 0`，第 `b` 位就在 OR 里是 1。  

- **滑动窗口（双指针）**：  
  1. 右指针 `r` 从左向右遍历数组，把 `nums[r]` 加入窗口，同时更新 `cnt`。  
  2. 检查窗口的 OR 是否已经 **≥ k**。如果是，就尝试把左指针 `l` 往右移动，**缩小窗口**，同时更新 `cnt`，直到再移动会导致 OR < k。每一次满足条件时，记录窗口长度 `r-l+1`，取最小值。  
  3. 重复步骤 1~2，直至右指针走完。

这样每个元素最多会被左指针和右指针各访问一次，整体时间是 `O(n * B)`，`B` 为位数（这里是 31），相当于线性 `O(n)`。

**类比**：把数组想成一条河流，`r` 是不断往下游放水的闸门，`l` 是往上游收回水的闸门。我们希望在河段里保持“水位”（OR）足够高（≥k），同时让这段河尽可能短。

#### 代码（Python）

```python
def shortestSubarray(nums, k):
    n = len(nums)
    # cnt[b] 表示窗口内第 b 位为 1 的元素个数，b = 0~30
    cnt = [0] * 31

    def window_or() -> int:
        """根据 cnt 计算当前窗口的 OR 值"""
        val = 0
        for b in range(31):
            if cnt[b]:
                val |= (1 << b)
        return val

    ans = float('inf')
    left = 0

    for right in range(n):
        # 把 nums[right] 加入窗口，更新每一位的计数
        x = nums[right]
        for b in range(31):
            if x >> b & 1:
                cnt[b] += 1

        # 当窗口的 OR 已经满足 >= k 时，尝试收缩左端点
        while left <= right and window_or() >= k:
            ans = min(ans, right - left + 1)   # 记录更短的长度
            # 把 nums[left] 移出窗口，更新计数
            y = nums[left]
            for b in range(31):
                if y >> b & 1:
                    cnt[b] -= 1
            left += 1

    return -1 if ans == float('inf') else ans
```

> 关键行解释  
> - `for b in range(31): if x >> b & 1: cnt[b] += 1`：把新加入的数的每一位“打开”，对应的计数加一。  
> - `while ... window_or() >= k:`：只要窗口的 OR 仍然够大，就继续把左端点往右收，尝试让窗口更短。  
> - `cnt[b] -= 1`：左端点离开窗口时，把它贡献的位计数减一，如果某个位的计数降到 0，说明窗口里已经没有该位为 1 的元素了，后面 `window_or()` 会把这位设为 0。  

**进一步优化**（可选）  
因为 `window_or()` 每次都要遍历 31 位，整体仍是 `O(31·n)`，但 31 是常数，实际运行非常快。若想省去每次遍历，可在维护计数的同时维护一个整数 `cur_or`，在加入元素时 `cur_or |= nums[right]`，在移出元素时如果某个位的计数降到 0，就把该位从 `cur_or` 中清除 `cur_or &= ~(1 << b)`。思路相同，这里为了代码易读保留了 `window_or()`。

#### 复杂度  

- **时间复杂度**：`O(n * 31) ≈ O(n)`  
  - 每个元素最多进入窗口一次、离开窗口一次，位数 31 是常数，所以整体线性。相比暴力的 `n²`，速度提升了好几个数量级。  
- **空间复杂度**：`O(31) = O(1)`  
  - 只用了 31 个计数器和若干常数变量，和输入规模无关。

---

## 心得

- **核心技巧**：利用 **位计数 + 双指针（滑动窗口）** 来维护动态的按位或。  
- **适用的题型**  
  1. “最短/最长子数组满足按位或/按位与/按位异或的阈值” 类似题目。  
  2. “子数组的所有元素满足某种单调位特性” 如“子数组的最大值 ≤ K”。  
  3. “需要在 O(n) 内维护窗口中每一位出现次数的统计” 的题目。  
- **一句话总结**：**“把每一位当作独立的资源，用计数追踪窗口是否拥有足够的资源，就能用滑动窗口高效求最短子数组”。**

---

## 反思

- **第一反应**：先想到了枚举所有子数组（暴力），因为这能确保不遗漏任何可能。  
- **最容易踩的坑**  
  - **位数范围**：忘记考虑 `nums[i]` 最大到 `10⁹`，需要 30 位而不是 32 位（Python 整数是无限长，但我们只需关心到最高位）。  
  - **左指针移动时的位清除**：如果只减计数而不在计数为 0 时把对应位从 OR 中清除，`window_or()` 仍会错误地把该位算作 1。  
  - **k=0 的特殊情况**：只要数组非空，答案一定是 1，需要在代码里自然覆盖（上述实现已经兼容）。  
- **下次第一步**：先判断“**是否可以用滑动窗口**”。检查目标函数（这里是 OR）是否具有 **单调性**（只会增加不下降），如果是，就立刻尝试双指针；否则考虑前缀和、DP 或其他技巧。