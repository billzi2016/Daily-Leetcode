# #2134. 最少交换次数使所有 1 聚集在一起 II / Minimum Swaps to Group All 1's Together II

> 难度：中等 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/minimum-swaps-to-group-all-1s-together-ii/)

---

## 题目（英文原版）

**Description**

A swap is defined as taking two distinct positions in an array and swapping the values in them.
A circular array is defined as an array where we consider the first element and the last element to be adjacent.
Given a binary circular array nums, return the minimum number of swaps required to group all 1's present in the array together at any location.

**Examples**

**Example 1:**

```
Input: nums = [0,1,0,1,1,0,0]
Output: 1
Explanation: Here are a few of the ways to group all the 1's together:
[0,0,1,1,1,0,0] using 1 swap.
[0,1,1,1,0,0,0] using 1 swap.
[1,1,0,0,0,0,1] using 2 swaps (using the circular property of the array).
There is no way to group all 1's together with 0 swaps.
Thus, the minimum number of swaps required is 1.
```

**Example 2:**

```
Input: nums = [0,1,1,1,0,0,1,1,0]
Output: 2
Explanation: Here are a few of the ways to group all the 1's together:
[1,1,1,0,0,0,0,1,1] using 2 swaps (using the circular property of the array).
[1,1,1,1,1,0,0,0,0] using 2 swaps.
There is no way to group all 1's together with 0 or 1 swaps.
Thus, the minimum number of swaps required is 2.
```

**Example 3:**

```
Input: nums = [1,1,0,0,1]
Output: 0
Explanation: All the 1's are already grouped together due to the circular property of the array.
Thus, the minimum number of swaps required is 0.
```

**Constraints**

- 1 <= nums.length <= 105
- nums[i] is either 0 or 1.

---

## 题目（中文翻译）

**交换（swap）** 的定义是：选取数组中的两个不同位置并交换它们的值。  
**循环数组（circular array）** 是指我们把数组的首元素与末元素视为相邻的数组。  

给定一个二进制循环数组 `nums`，返回将数组中所有 `1` 聚集到任意位置所需的最少交换次数。

---

### 示例

#### 示例 1  
**输入**：`nums = [0,1,0,1,1,0,0]`  
**输出**：`1`  
**解释**：以下是几种将所有 `1` 聚集在一起的方式：  
- `[0,0,1,1,1,0,0]`，使用 **1 次交换**。  
- `[0,1,1,1,0,0,0]`，使用 **1 次交换**。  
- `[1,1,0,0,0,0,1]`，使用 **2 次交换**（利用数组的循环属性）。  

没有办法在 **0 次交换** 内把所有 `1` 聚在一起。  
因此，所需的最少交换次数为 **1**。

#### 示例 2  
**输入**：`nums = [0,1,1,1,0,0,1,1,0]`  
**输出**：`2`  
**解释**：以下是几种将所有 `1` 聚集在一起的方式：  
- `[1,1,1,0,0,0,0,1,1]`，使用 **2 次交换**（利用循环属性）。  
- `[1,1,1,1,1,0,0,0,0]`，使用 **2 次交换**。  

没有办法在 **0 次或 1 次交换** 内把所有 `1` 聚在一起。  
因此，所需的最少交换次数为 **2**。

#### 示例 3  
**输入**：`nums = [1,1,0,0,1]`  
**输出**：`0`  
**解释**：由于循环属性，所有 `1` 已经聚集在一起。  
因此，所需的最少交换次数为 **0**。

---

### 约束条件

- `1 <= nums.length <= 10^5`
- `nums[i]` 只能是 `0` 或 `1`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有 1 的位置列出来，然后把它们搬到一起**。  
具体做法可以是：

1. 先统计数组中一共有多少个 `1`，记为 `total`。这一步相当于先算出“要聚在一起的东西有多少”。  
2. 由于数组是环形的，我们可以把数组复制一遍拼接在后面，得到 `nums + nums`，这样就可以把“跨过数组头尾”的窗口也变成普通的连续子数组。把它想象成把一条环形跑道拉直，跑道两端再接上一段相同的跑道，跑步时就不需要“跳过去”。  
3. 然后在这条拉直后的数组里，枚举所有长度为 `total` 的子数组，统计子数组里有多少个 `0`。因为子数组里本来应该全是 `1`，所以每出现一个 `0` 就需要一次交换才能把它换成 `1`。  
4. 最小的 `0` 数量即为答案。

> **为什么正确？**  
> - 要把所有 `1` 放进同一个窗口，窗口的大小只能是 `total`（因为 `1` 的总数不变）。  
> - 只要窗口里已经是 `1`，就不需要动；窗口里是 `0`，一定要把它和窗口外的某个 `1` 交换，恰好一次交换可以把一个 `0` 换走。于是窗口内的 `0` 数目就是需要的最少交换次数。  

> **时间/空间复杂度**  
> - 我们要遍历 **所有** 长度为 `total` 的窗口。窗口的起始位置有 `n`（原数组长度）个，统计每个窗口里 `0` 的个数需要遍历 `total` 次，所以时间是 `O(n * total)`。在最坏情况下（比如 `total ≈ n/2`），这相当于 `O(n²)`，即“平方级别”，会随数组长度的增长而快速变慢。  
> - 额外的空间只用了一个复制的数组，长度是 `2n`，所以空间是 `O(n)`。

#### 代码（Python）

```python
def minSwaps_bruteforce(nums):
    n = len(nums)
    total = sum(nums)                 # 1 的总个数
    if total <= 1:                    # 0 或 1 个 1 已经是“聚在一起”
        return 0

    # 为了处理环形，把数组拼接一次
    extended = nums + nums

    min_swaps = float('inf')
    # 枚举所有长度为 total 的子数组
    for start in range(n):            # 只需要遍历前 n 个起点
        zeros = 0
        for i in range(start, start + total):
            if extended[i] == 0:
                zeros += 1           # 统计窗口里的 0
        min_swaps = min(min_swaps, zeros)

    return min_swaps
```

#### 复杂度

- **时间复杂度**：`O(n * total)`，在最坏情况下约为 `O(n²)`。  
  > “O(n²)” 可以理解为：如果数组长度是 10⁴，算法大约要做 10⁸ 次基本操作，显然太慢。

- **空间复杂度**：`O(n)`，因为我们额外创建了一个长度为 `2n` 的数组来模拟环形。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于每次窗口都要重新统计 `0` 的个数**。  
如果我们能够在窗口滑动时 **复用上一次的统计结果**，就能把时间降到线性 `O(n)`。这正是 **滑动窗口（Sliding Window）** 的核心思想。

滑动窗口的基本思想：

1. 先把窗口固定在数组的最左边，统计窗口内 `0` 的个数 `zero_cnt`。  
2. 然后把窗口向右移动一格：左边界离开窗口的元素如果是 `0`，`zero_cnt` 减 1；右边界进入窗口的元素如果是 `0`，`zero_cnt` 加 1。这样只用常数时间就完成了窗口的“更新”。  
3. 在每个位置记录 `zero_cnt` 的最小值，最小值即为所求的最少交换次数。

因为数组是环形的，同样采用 “把数组复制一遍” 的技巧，使得所有可能的窗口都可以在 **一次线性遍历** 中被覆盖。

**关键点解释**：

- **为什么窗口大小是 `total`**  
  我们必须把所有 `1` 放进同一个连续段，而 `1` 的总数是固定的 `total`，所以窗口的长度只能是 `total`。想象把 `total` 块砖头（代表 1）放进一个长条形的盒子里，盒子太短放不下，太长会留下空位，最合适的正好是盒子长度等于砖块数量。

- **为什么只统计 `0` 的个数**  
  在目标窗口里应该全是 `1`，每一个 `0` 必须被换成 `1`，一次交换只能把一个 `0` 换走（与窗口外的 `1` 交换），所以窗口里的 `0` 数量就是需要的最少交换次数。

- **环形如何处理**  
  把原数组复制一遍，形成 `extended = nums + nums`。这样从位置 `0` 开始的窗口一直滑到位置 `n-1`，即覆盖了所有“环形”可能的起点。复制的部分只用来让窗口跨越边界，不会影响答案，因为我们只关注窗口长度为 `total`，而 `total ≤ n`。

#### 代码（Python）

```python
def minSwaps(nums):
    n = len(nums)
    total = sum(nums)                 # 1 的总数
    if total <= 1:                    # 0 或 1 个 1 已经满足要求
        return 0

    # 把数组复制一次，方便处理环形窗口
    extended = nums + nums

    # 先统计第一个窗口（下标 0 ~ total-1）里 0 的个数
    zero_cnt = 0
    for i in range(total):
        if extended[i] == 0:
            zero_cnt += 1

    min_swaps = zero_cnt               # 当前窗口的交换次数

    # 窗口右移，左边界 i，右边界 i+total
    for i in range(1, n):              # 只需要移动 n-1 次，遍历所有起点
        # 移出窗口的元素
        if extended[i - 1] == 0:
            zero_cnt -= 1
        # 新进入窗口的元素
        if extended[i + total - 1] == 0:
            zero_cnt += 1

        # 更新最小值
        if zero_cnt < min_swaps:
            min_swaps = zero_cnt

    return min_swaps
```

**代码关键行解释**：

- `extended = nums + nums`：把环形拉直，像把一条环形跑道拼成直路。  
- 初始 `for i in range(total)`：统计第一个窗口里有多少 `0`，相当于先把窗口“装好”。  
- `for i in range(1, n)`：窗口左移一步。左边离开的元素是 `extended[i-1]`，右边进入的元素是 `extended[i+total-1]`。只要检查这两个位置是不是 `0`，就能在 **O(1)** 时间内更新 `zero_cnt`。  
- `min_swaps = min(min_swaps, zero_cnt)`：记录遍历过程中出现的最小 `0` 数量，即最少交换次数。

#### 复杂度

- **时间复杂度**：`O(n)`。  
  - 我们只遍历了 `extended` 的前 `n + total`（其实是 `2n`）个元素一次，每次窗口移动只做常数次操作。  
  - 与暴力解的 `O(n²)` 相比，线性时间在 `n = 10⁵` 时也能轻松跑完。

- **空间复杂度**：`O(n)`（用于存放 `extended`）。如果不想额外复制数组，也可以在原数组上用取模运算模拟环形，但复制更直观，空间仍然是线性级别。

---

## 心得

- **核心技巧**：**滑动窗口 + 环形数组的复制**。  
  这道题的关键在于把“窗口内的 0 个数”视作代价，并用滑动窗口在 **O(1)** 时间内更新这个代价，从而把整体复杂度降到线性。

- **适用的题型**  
  1. “最少交换/翻转使子数组满足某种条件”——如 *Minimum Swaps to Group All 1's Together*（非环形版）。  
  2. “环形数组的最长/最短满足条件子段”——如 *Maximum Size Subarray Sum Equals K*（环形版）或 *Longest Subarray With At Most K Distinct Elements*（环形）。  
  3. “固定长度窗口内统计某种元素”——如 *Maximum Number of Ones After K Flips*、*Maximum Sum of Subarray of Size K*。

- **一句话总结**：  
  **把“所有 1 必须落在同一个固定长度窗口”转化为“窗口内的 0 越少越好”，再用滑动窗口一次遍历求最小 0 数即可。**

---

## 反思

- **第一反应**：看到“环形数组”和“把所有 1 放在一起”，自然会想到先统计 1 的总数，然后枚举所有可能的连续段。这直接导向了暴力的 O(n²) 思路。  

- **最容易踩的坑**  
  1. **忘记环形的处理**：直接在原数组上滑动会遗漏跨越数组首尾的窗口，需要把数组复制或使用取模。  
  2. **边界条件**：当 `total` 为 0 或 1 时，答案应直接返回 0，避免后续除零或窗口大小为 0 的错误。  
  3. **窗口大小等于 n**：如果所有元素都是 1，`total == n`，窗口恰好覆盖整个数组，仍然应该返回 0。  

- **下次类似题的第一步**：  
  **先把“要聚在一起的元素个数”算出来，确定窗口大小，然后想办法在 O(n) 内遍历所有固定长度的窗口（常用技巧：复制数组或取模 + 滑动窗口）。**