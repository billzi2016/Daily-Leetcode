# #2841. 几乎唯一子数组的最大和 / Maximum Sum of Almost Unique Subarray

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-of-almost-unique-subarray/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two positive integers m and k.
Return the maximum sum out of all almost unique subarrays of length k of nums. If no such subarray exists, return 0.
A subarray of nums is almost unique if it contains at least m distinct elements.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [2,6,7,3,1,7], m = 3, k = 4
Output: 18
Explanation: There are 3 almost unique subarrays of size k = 4. These subarrays are [2, 6, 7, 3], [6, 7, 3, 1], and [7, 3, 1, 7]. Among these subarrays, the one with the maximum sum is [2, 6, 7, 3] which has a sum of 18.
```

**Example 2:**

```
Input: nums = [5,9,9,2,4,5,4], m = 1, k = 3
Output: 23
Explanation: There are 5 almost unique subarrays of size k. These subarrays are [5, 9, 9], [9, 9, 2], [9, 2, 4], [2, 4, 5], and [4, 5, 4]. Among these subarrays, the one with the maximum sum is [5, 9, 9] which has a sum of 23.
```

**Example 3:**

```
Input: nums = [1,2,1,2,1,2,1], m = 3, k = 3
Output: 0
Explanation: There are no subarrays of size k = 3 that contain at least m = 3 distinct elements in the given array [1,2,1,2,1,2,1]. Therefore, no almost unique subarrays exist, and the maximum sum is 0.
```

**Constraints**

- 1 <= nums.length <= 2 * 104
- 1 <= m <= k <= nums.length
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

**题目描述**

给定一个整数数组 `nums`，以及两个正整数 `m` 和 `k`。  
返回 `nums` 中所有长度为 `k` 的**几乎唯一子数组（almost unique subarray）**的最大和。如果不存在满足条件的子数组，返回 `0`。

- **子数组（subarray）**是数组中连续的、非空的元素序列。
- 当一个子数组至少包含 `m` 个不同的元素时，称其为**几乎唯一子数组**。

**示例**

示例 1  
输入: `nums = [2,6,7,3,1,7]`, `m = 3`, `k = 4`  
输出: `18`  
解释: 长度为 `k = 4` 的几乎唯一子数组共有 3 个，分别是 `[2, 6, 7, 3]`、`[6, 7, 3, 1]` 和 `[7, 3, 1, 7]`。其中和最大的子数组是 `[2, 6, 7, 3]`，其和为 `18`。

示例 2  
输入: `nums = [5,9,9,2,4,5,4]`, `m = 1`, `k = 3`  
输出: `23`  
解释: 长度为 `k = 3` 的几乎唯一子数组共有 5 个，分别是 `[5, 9, 9]`、`[9, 9, 2]`、`[9, 2, 4]`、`[2, 4, 5]` 和 `[4, 5, 4]`。其中和最大的子数组是 `[5, 9, 9]`，其和为 `23`。

示例 3  
输入: `nums = [1,2,1,2,1,2,1]`, `m = 3`, `k = 3`  
输出: `0`  
解释: 在数组 `[1,2,1,2,1,2,1]` 中，没有长度为 `k = 3` 且至少包含 `m = 3` 个不同元素的子数组。因此不存在几乎唯一子数组，最大和为 `0`。

**约束条件**

- `1 <= nums.length <= 2 * 10^4`
- `1 <= m <= k <= nums.length`
- `1 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是「把所有长度为 `k` 的连续子数组枚举出来」，逐个检查它们是否满足「至少有 `m` 个不同的元素」，满足的话再计算它们的和，记录最大值。

- **枚举子数组**：可以用两层循环，外层 `i` 表示子数组的左端点，`i` 从 `0` 遍历到 `len(nums)-k`，内层把 `i … i+k-1` 的元素逐个取出来。
- **统计不同元素的个数**：可以把子数组的元素放进一个 **哈希表（字典）**，键是元素的值，值是出现次数。哈希表就像一本「词典」，我们把每个数字当成「单词」，出现的次数相当于「页码」——只要字典里有多少条目，就说明有多少种不同的数字。
- **判断**：字典的键数（`len(dict)`）≥ `m` 即为「almost unique」。
- **求和**：把子数组的 `k` 个数相加，更新全局最大和。

这种做法一定能得到正确答案，因为我们没有遗漏任何合法子数组。

#### 代码（Python）

```python
def max_sum_bruteforce(nums, m, k):
    n = len(nums)
    max_sum = 0                     # 记录符合条件的最大和，初始为 0

    # i 为子数组的左端点
    for i in range(n - k + 1):
        freq = {}                    # 哈希表，统计子数组里每个数出现的次数
        cur_sum = 0                  # 当前子数组的和

        # 遍历长度为 k 的窗口
        for j in range(i, i + k):
            x = nums[j]
            cur_sum += x
            freq[x] = freq.get(x, 0) + 1   # 更新出现次数

        # 检查不同元素的个数是否 ≥ m
        if len(freq) >= m:
            max_sum = max(max_sum, cur_sum)

    return max_sum
```

#### 复杂度

- **时间复杂度**：`O(n * k)`  
  外层遍历约 `n` 次，内层每次要遍历 `k` 个元素。用大白话说，就是「如果数组有 10000 个数，窗口大小是 500，那最差情况下要做 10000×500 = 5,000,000 次基本操作」。
- **空间复杂度**：`O(k)`  
  哈希表最多装下窗口里的 `k` 个不同元素（最坏全部不相同），所以额外空间随窗口大小线性增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都重新遍历整个窗口**，这导致 `O(n·k)` 的时间。我们可以利用「滑动窗口」的思想，让窗口在数组上 **一次移动一步**，并 **增量地** 更新窗口内部的信息（和、不同元素个数），从而把时间降到 `O(n)`。

关键点如下：

1. **窗口大小固定为 `k`**  
   - 当窗口向右移动时，左端点的元素会离开窗口，右端点会加入一个新元素。我们只需要把离开的元素从哈希表里减去计数（如果计数降到 0，就删掉对应的键），把新来的元素计数加 1。
2. **维护窗口的总和**  
   - 同样地，离开的元素从总和中减去，加入的元素加进去，整个窗口的和可以在 `O(1)` 时间内更新。
3. **维护不同元素的个数**  
   - 哈希表的键数 `len(cnt)` 正好等于窗口里不同元素的个数。增删计数时，只要键从 0 变成 1（出现新种类）或从 1 变成 0（种类消失），就相应地增减 `distinct_cnt`。
4. **判断并记录答案**  
   - 每当窗口的大小恰好为 `k` 时，检查 `distinct_cnt >= m`，如果满足，就用当前窗口和更新最大和。

这样，**每个元素只进出窗口各一次**，整体线性遍历即可。

下面用类比帮助理解：

- 想象你在走廊里推一个装满 4 本书的手推车（窗口大小 `k=4`）。每走一步，最左边的书掉出来（离开窗口），最右边的新书放进去（进入窗口）。你只需要记住手推车里总共多少钱（总和）以及有多少种不同的书（不同元素），不必重新数一遍手推车里的所有书。

#### 代码（Python）

```python
def max_sum_sliding_window(nums, m, k):
    """
    使用滑动窗口 + 哈希表求解
    时间 O(n)，空间 O(k)（哈希表最多存 k 个不同元素）
    """
    n = len(nums)
    if n < k:                     # 题目保证不会出现，但防御性写法
        return 0

    cnt = {}                      # 哈希表：元素 -> 出现次数
    distinct = 0                  # 当前窗口不同元素的个数
    cur_sum = 0                   # 当前窗口的元素和
    max_sum = 0                   # 记录符合条件的最大和

    left = 0                      # 窗口左端点
    for right in range(n):        # 窗口右端点依次向右扩展
        x = nums[right]

        # 加入新元素
        cur_sum += x
        cnt[x] = cnt.get(x, 0) + 1
        if cnt[x] == 1:           # 之前没有出现过，种类数加 1
            distinct += 1

        # 当窗口长度超过 k 时，收缩左端点
        if right - left + 1 > k:
            y = nums[left]
            cur_sum -= y
            cnt[y] -= 1
            if cnt[y] == 0:       # 该种类完全离开窗口
                distinct -= 1
                del cnt[y]        # 删除键，保持哈希表干净
            left += 1

        # 此时窗口恰好长度为 k
        if right - left + 1 == k:
            if distinct >= m:      # 满足“almost unique”
                max_sum = max(max_sum, cur_sum)

    return max_sum
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个元素至多进入窗口一次、离开窗口一次，所有操作都是 `O(1)`，所以整体随数组长度线性增长。相比暴力的 `O(n·k)`，速度提升显著——比如 `n=20000, k=5000` 时，暴力需要约 `1e8` 次操作，而滑动窗口只要 `2e4` 次。
- **空间复杂度**：`O(k)`（最坏 `O(n)`）  
  哈希表最多保存当前窗口里不同的元素。窗口大小上限是 `k`，因此空间随 `k` 线性增长。若所有元素都不相同且 `k=n`，则会占用 `O(n)` 空间。

---

## 心得

- **核心技巧**：**滑动窗口 + 哈希表** 用来在固定长度子数组上实时维护「和」和「不同元素个数」。
- **适用题型**：
  1. “长度固定的子数组满足某种计数条件”——如 *Maximum Sum of Subarray with At Most K Distinct Elements*。
  2. “最长/最短子数组满足条件”——如 *Longest Substring Without Repeating Characters*（使用可变窗口）。
  3. “子数组和满足区间”——如 *Subarray Sum Equals K*（配合前缀和或哈希表）。
- **一句话总结**：把窗口当成“会动的盒子”，只在盒子进出元素时增减计数，整个过程不需要重复遍历。

---

## 反思

- **第一反应**：直接想到枚举所有长度为 `k` 的子数组并逐个检查——这就是暴力解。
- **最容易踩的坑**：
  1. **边界条件**：窗口刚好达到 `k` 时才开始比较，否则会误判长度不足的子数组。
  2. **计数正确性**：离开窗口的元素计数降到 0 时必须把对应键删掉，否则 `len(cnt)` 会把已经不存在的元素算进去。
  3. **大数相加**：`nums[i]` 可能到 `1e9`，累加时要使用 Python 的大整数即可，无需担心溢出，但在其他语言要注意 64 位整数。
- **下次类似题**：第一步先确认「窗口大小是否固定」；若固定，就立刻考虑 **固定大小滑动窗口**，并准备好 **哈希表/计数器** 来增量维护窗口内部的统计信息。这样可以把时间从平方级降到线性级。