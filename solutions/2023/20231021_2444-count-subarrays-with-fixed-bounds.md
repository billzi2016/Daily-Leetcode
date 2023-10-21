# #2444. 计数固定边界子数组 / Count Subarrays With Fixed Bounds

> 难度：困难 · 标签：Array、Queue、Sliding Window、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/count-subarrays-with-fixed-bounds/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers minK and maxK.
A fixed-bound subarray of nums is a subarray that satisfies the following conditions:
Return the number of fixed-bound subarrays.
A subarray is a contiguous part of an array.

**Examples**

**Example 1:**

```
Input: nums = [1,3,5,2,7,5], minK = 1, maxK = 5
Output: 2
Explanation: The fixed-bound subarrays are [1,3,5] and [1,3,5,2].
```

**Example 2:**

```
Input: nums = [1,1,1,1], minK = 1, maxK = 1
Output: 10
Explanation: Every subarray of nums is a fixed-bound subarray. There are 10 possible subarrays.
```

**Constraints**

- 2 <= nums.length <= 105
- 1 <= nums[i], minK, maxK <= 106

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和两个整数 `minK`、`maxK`。  
**固定边界子数组（fixed‑bound subarray）** 是指满足以下所有条件的子数组（subarray）：

1. 子数组中的最小值等于 `minK`。  
2. 子数组中的最大值等于 `maxK`。  
3. 子数组中的所有元素都在 `[minK, maxK]` 区间内（即 `minK ≤ nums[i] ≤ maxK`）。

返回满足上述条件的子数组的数量。

> 子数组是数组中连续的一段。

### 示例

#### 示例 1
```text
Input: nums = [1,3,5,2,7,5], minK = 1, maxK = 5
Output: 2
Explanation: 符合条件的固定边界子数组为 [1,3,5] 和 [1,3,5,2]。
```

#### 示例 2
```text
Input: nums = [1,1,1,1], minK = 1, maxK = 1
Output: 10
Explanation: nums 的每个子数组都是固定边界子数组，共有 10 种可能的子数组。
```

### 约束条件
- `2 ≤ nums.length ≤ 10^5`
- `1 ≤ nums[i], minK, maxK ≤ 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **枚举所有子数组**，逐个检查它们是否满足题目要求。  
- **枚举子数组**：用两层循环，外层固定子数组的左端点 `left`，内层把右端点 `right` 从 `left` 向右推进。  
- **检查子数组**：在遍历的过程中维护当前子数组的最小值 `cur_min` 和最大值 `cur_max`。  
  - 当 `cur_min == minK` 并且 `cur_max == maxK` 时，这个子数组就是“固定界限子数组”。  
- **类比**：把数组想象成一排书，左手指向子数组的左边，右手不断往右翻页，每翻一页就检查一次这本书的最薄和最厚的章节（最小值、最大值）是否正好是我们想要的两本特定的书（`minK`、`maxK`）。

**为什么正确**  
只要把所有可能的左端点、右端点组合都遍历一遍，就没有遗漏的子数组；每次判断的逻辑恰好对应题目对“最小值 = minK 且最大值 = maxK 且所有元素都在 `[minK, maxK]` 范围内”的定义，所以计数一定是准确的。

**时间/空间复杂度**  
- **时间**：两层循环最多会产生 `n*(n+1)/2` 种子数组，最坏情况每次都要更新最小/最大值，整体是 **O(n²)**。  
  - 大白话：如果数组有 10,000 个元素，暴力解大约要检查 10,000²/2 ≈ 5,000 万次，这在实际运行时会非常慢。  
- **空间**：只使用常数个额外变量（`cur_min`、`cur_max`、计数器等），所以是 **O(1)**。

#### 代码（Python）

```python
def count_subarrays_bruteforce(nums, minK, maxK):
    n = len(nums)
    ans = 0                       # 统计答案
    for left in range(n):         # 枚举左端点
        cur_min = float('inf')    # 当前子数组的最小值，初始为正无穷
        cur_max = float('-inf')   # 当前子数组的最大值，初始为负无穷
        for right in range(left, n):   # 枚举右端点
            cur_min = min(cur_min, nums[right])   # 更新最小值
            cur_max = max(cur_max, nums[right])   # 更新最大值
            # 判断是否满足「最小值 = minK 且最大值 = maxK」且所有元素都在区间内
            if cur_min == minK and cur_max == maxK:
                # 只要出现 minK、maxK，且中间没有越界的数，说明一定满足所有元素都在 [minK, maxK]。
                # 这里不需要额外检查，因为只要 minK、maxK 出现，其他数必然在区间内（否则 min/max 会被破坏）。
                ans += 1
            # 如果出现了比 maxK 更大或比 minK 更小的数，后面的子数组就不可能再满足条件
            if nums[right] < minK or nums[right] > maxK:
                break               # 提前结束内层循环，省点时间
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` — 两层循环遍历所有子数组，最坏情况会检查约 `n²/2` 次。  
- **空间复杂度**：`O(1)` — 只用了常数个临时变量。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **重复遍历**：每次左端点移动时，都重新扫描右侧的元素，导致大量冗余计算。  
我们需要 **一次遍历** 就把所有合法子数组计数完。下面一步步推导思路：

1. **划分合法区间**  
   - 只要子数组里出现了 **不在 `[minK, maxK]` 区间** 的元素，那么以它为左端点或右端点的任何子数组都不合法。  
   - 因此可以把原数组切成若干段，每段内部的所有数都满足 `minK ≤ num ≤ maxK`。  
   - 在每段内部，我们只需要关心 `minK` 与 `maxK` 出现的位置。

2. **滑动窗口 + 记录最新位置**  
   - 用 **单指针** `i` 从左到右遍历数组。  
   - 维护三个下标：  
     - `last_invalid`：最近一次出现 **非法数**（`< minK` 或 `> maxK`）的位置。  
     - `last_minK`：最近一次出现 **等于 `minK`** 的位置。  
     - `last_maxK`：最近一次出现 **等于 `maxK`** 的位置。  
   - 对于当前位置 `i`（假设 `nums[i]` 合法），以 `i` 为右端点的所有子数组的左端点只能在 `(last_invalid, i]` 之间。  
   - 要让子数组同时包含 `minK` 与 `maxK`，左端点必须 **不晚于** 两者中更靠左的那个位置，即 `min(last_minK, last_maxK)`。  
   - 因此，以 `i` 为右端点的合法子数组数量 = `max(0, min(last_minK, last_maxK) - last_invalid)`。  
   - 把这个数累加到答案中，继续向右移动指针。

3. **为什么一次遍历就够了**  
   - 每个元素只会更新一次 `last_invalid` / `last_minK` / `last_maxK`，计算公式只用了 O(1) 的算术操作。  
   - 所有合法子数组都被“右端点”唯一对应一次，计数不重复也不遗漏。

**类比**：把数组想成一条河流，`last_invalid` 是河岸上的大石头（不让船过去），`last_minK`、`last_maxK` 是两座灯塔（必须经过的标记）。要让船从左岸出发、右岸停靠，左岸的起点只能在最近的大石头右边，而且必须先经过两座灯塔中更靠左的那座。每走一步，就能立刻算出有多少条路径满足条件。

#### 代码（Python）

```python
def count_subarrays(nums, minK, maxK):
    """
    一次遍历 O(n) 统计满足:
        - 子数组的最小值恰好是 minK
        - 子数组的最大值恰好是 maxK
        - 所有元素均在 [minK, maxK] 区间
    """
    ans = 0                     # 最终答案
    last_invalid = -1           # 最近一次出现非法数的下标，初始化为 -1 表示“左边界外”
    last_minK = -1              # 最近一次出现 minK 的下标
    last_maxK = -1              # 最近一次出现 maxK 的下标

    for i, x in enumerate(nums):
        # 1️⃣ 检查当前元素是否合法
        if x < minK or x > maxK:
            # 非法数会把以后所有以它为左端点的子数组都砍掉
            last_invalid = i
            # 同时把 minK / maxK 的记录也清空，防止误计数
            last_minK = -1
            last_maxK = -1
            continue

        # 2️⃣ 更新 minK / maxK 的最新位置（如果出现的话）
        if x == minK:
            last_minK = i
        if x == maxK:
            last_maxK = i

        # 3️⃣ 计算以 i 为右端点的合法子数组数目
        # 必须同时出现 minK 与 maxK，且左端点要在 last_invalid 右侧
        left_bound = min(last_minK, last_maxK)   # 两者中更靠左的那个位置
        if left_bound > last_invalid:           # 说明已经出现了两者且没有被非法数“挡住”
            ans += left_bound - last_invalid    # 右端点固定时，可选的左端点有这么多种

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只遍历一次数组，所有操作都是常数时间。与暴力解的 `O(n²)` 相比，提升了数量级（比如 `n=10⁵` 时，只有 10⁵ 次循环，几乎是瞬间完成）。  
- **空间复杂度**：`O(1)` — 只用了几个人变量来记录下标，没有额外的数组或栈。

---

## 心得  

- **核心技巧**：**滑动窗口 + 位置记录**（也可以视作一种 “单调队列” 思路的简化）。  
- **适用的题型**  
  1. “子数组的最值必须等于给定的两个数”——比如 *Number of Subarrays with Bounded Maximum*。  
  2. “子数组中不出现非法元素，且必须包含若干关键元素”——例如 *Subarrays with K Different Integers*（需要记录关键元素出现次数）。  
  3. “求满足某种区间约束的子数组数量”——如 *Count Number of Nice Subarrays*。  
- **一句话总结解题钥匙**：**把所有不合法的元素当作“墙”，把必出现的关键元素当作“灯塔”，用最近位置的差值直接算出每个右端点对应的合法左端点数目**。

---

## 反思  

- **第一反应**：直接想到双层循环枚举子数组，随后意识到会超时。  
- **最容易踩的坑**  
  - 忽略了 “所有元素必须在 `[minK, maxK]` 区间” 这条约束，导致计数时把含有非法数的子数组也算进去了。  
  - 在实现最优解时，忘记在遇到非法数时把 `last_minK`、`last_maxK` 重置，容易产生负数计数。  
- **下次类似题的第一步**：先 **定位非法元素**（把数组切成合法块），再 **记录关键元素的最新位置**，最后用 “最近关键位置 - 最近非法位置” 这一步公式直接统计。这样思路既清晰又能保证 O(n) 的效率。