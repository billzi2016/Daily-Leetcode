# #2461. **长度为 K 的不重复子数组的最大和** / Maximum Sum of Distinct Subarrays With Length K

> 难度：中等 · 标签：Array、Hash Table、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and an integer k. Find the maximum subarray sum of all the subarrays of nums that meet the following conditions:
Return the maximum subarray sum of all the subarrays that meet the conditions. If no subarray meets the conditions, return 0.
A subarray is a contiguous non-empty sequence of elements within an array.

**Examples**

**Example 1:**

```
Input: nums = [1,5,4,2,9,9,9], k = 3
Output: 15
Explanation: The subarrays of nums with length 3 are:
- [1,5,4] which meets the requirements and has a sum of 10.
- [5,4,2] which meets the requirements and has a sum of 11.
- [4,2,9] which meets the requirements and has a sum of 15.
- [2,9,9] which does not meet the requirements because the element 9 is repeated.
- [9,9,9] which does not meet the requirements because the element 9 is repeated.
We return 15 because it is the maximum subarray sum of all the subarrays that meet the conditions
```

**Example 2:**

```
Input: nums = [4,4,4], k = 3
Output: 0
Explanation: The subarrays of nums with length 3 are:
- [4,4,4] which does not meet the requirements because the element 4 is repeated.
We return 0 because no subarrays meet the conditions.
```

**Constraints**

- 1 <= k <= nums.length <= 105
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `k`。请在所有满足以下条件的子数组（subarray）中，找到子数组和（subarray sum）的最大值并返回：

- 子数组的长度恰好为 `k`；
- 子数组内部的元素全部互不相同（即不存在重复元素）。

如果不存在满足条件的子数组，返回 `0`。

> **子数组** 是数组中连续且非空的元素序列。

### 示例

**示例 1**

```
输入: nums = [1,5,4,2,9,9,9], k = 3
输出: 15
解释: 长度为 3 的子数组如下：
- [1,5,4] 满足条件，和为 10
- [5,4,2] 满足条件，和为 11
- [4,2,9] 满足条件，和为 15
- [2,9,9] 不满足条件，因为元素 9 重复
- [9,9,9] 不满足条件，因为元素 9 重复
最大满足条件的子数组和为 15。
```

**示例 2**

```
输入: nums = [4,4,4], k = 3
输出: 0
解释: 唯一的长度为 3 的子数组是 [4,4,4]，但其中元素 4 重复，不满足条件。
因此返回 0。
```

### 约束

- `1 <= k <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有长度为 `k` 的子数组都枚举出来，逐个检查它们是否满足「所有元素互不相同」的条件，如果满足就把它们的和算出来，最后取最大值。  

- **枚举子数组**：遍历数组的每一个起始位置 `i`（`0 ≤ i ≤ len(nums)-k`），取出 `nums[i:i+k]` 这段连续的 `k` 个数。  
- **检查唯一性**：把这 `k` 个数放进一个集合（`set`），如果集合的大小恰好是 `k`，说明这段子数组里没有重复元素。集合可以类比成「字典」——把每个元素当成词，放进去后如果出现重复词，集合的大小就会小于原来的词数。  
- **计算子数组和**：把这 `k` 个数累加得到子数组的和，和当前记录的最大值比较，取更大的那个。

这个办法一定能得到正确答案，因为它把**所有**可能的子数组都检查了一遍，符合「穷举」的思想。

#### 代码（Python）

```python
def maximumSum(nums, k):
    n = len(nums)
    max_sum = 0                         # 记录满足条件的子数组的最大和，初始为 0
    for i in range(n - k + 1):          # 枚举所有长度为 k 的起始位置
        window = nums[i:i + k]          # 取出子数组
        if len(set(window)) == k:       # 用集合检查是否所有元素唯一
            cur_sum = sum(window)       # 计算子数组的和
            max_sum = max(max_sum, cur_sum)   # 更新最大值
    return max_sum
```

#### 复杂度

- **时间复杂度**：`O(n * k)`  
  - 外层遍历 `n‑k+1` 次，每次都要把 `k` 个元素复制到新列表、放进集合、再求和，都是 `O(k)` 的操作。  
  - 用大白话说，就是「数组有 `n` 个位置，每个位置都要检查 `k` 次」，所以整体会随 `n` 和 `k` 的乘积增长。  
- **空间复杂度**：`O(k)`  
  - 额外的集合和子数组列表最多存 `k` 个元素，和原数组无关，只跟窗口大小 `k` 有关系。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都重新遍历整个窗口**（复制、建集合、求和），导致时间复杂度是 `O(n·k)`。我们可以利用「滑动窗口」的思想，只在窗口移动时**增删少量元素**，从而把每一步的工作量降到 `O(1)`。

关键观察：

1. 当窗口从 `[i‑k+1 … i]` 移动到 `[i‑k+2 … i+1]` 时，**只会有两个元素变化**：  
   - 新加入的元素是 `nums[i+1]`（窗口右端）  
   - 移出的元素是 `nums[i‑k+1]`（窗口左端）  

2. 为了快速判断窗口内是否所有元素唯一，我们可以维护一个**哈希表（字典）**记录每个数在当前窗口出现的次数。哈希表就像「查字典」——键是数组中的数，值是它在窗口里出现的次数。

3. 同时维护一个**窗口的当前和** `window_sum`，当加入新元素时 `+=`，移出旧元素时 `-=`，这样不需要每次重新求和。

基于以上三点，算法步骤如下：

- 初始化：`left = 0`（窗口左端），`window_sum = 0`，`freq = {}`（空字典），`ans = 0`。  
- 依次把右端指针 `right` 向右移动，把 `nums[right]` 加入窗口：  
  - `window_sum += nums[right]`  
  - `freq[nums[right]] = freq.get(nums[right], 0) + 1`  
- 当窗口大小达到 `k` 时，检查 `freq` 中是否所有计数都是 `1`（即字典的键的数量等于 `k`）。如果是，则更新答案 `ans = max(ans, window_sum)`。  
- 无论是否满足唯一性，都要准备把左端元素踢出，使窗口继续保持大小 `k`：  
  - `left_elem = nums[left]`  
  - `window_sum -= left_elem`  
  - `freq[left_elem] -= 1`，如果计数降到 `0` 则把该键删掉，以免字典无限增长。  
  - `left += 1`  

这样每次右端指针只移动一次，左端指针也只移动一次，整个过程是 **线性** 的 `O(n)`。

#### 代码（Python）

```python
def maximumSum(nums, k):
    """
    使用滑动窗口 + 哈希表求解
    """
    n = len(nums)
    if k > n:               # 不可能出现长度为 k 的子数组
        return 0

    freq = {}               # 记录窗口内每个元素出现的次数，类似“查字典”
    window_sum = 0          # 当前窗口的元素和
    ans = 0
    left = 0                # 窗口左端指针

    for right in range(n):               # 右端指针依次右移
        # 1）把 nums[right] 加入窗口
        val = nums[right]
        window_sum += val
        freq[val] = freq.get(val, 0) + 1

        # 2）当窗口大小达到 k 时，检查唯一性并可能更新答案
        if right - left + 1 == k:
            # freq 中的键数量等于 k 说明所有元素均只出现一次
            if len(freq) == k:
                ans = max(ans, window_sum)

            # 3）窗口左移，准备下一次
            left_val = nums[left]
            window_sum -= left_val
            freq[left_val] -= 1
            if freq[left_val] == 0:       # 把计数为 0 的键删掉，防止字典膨胀
                del freq[left_val]
            left += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个元素恰好进入窗口一次、离开窗口一次，所有操作都是常数时间（字典的增删查均摊 `O(1)`），所以整体随数组长度线性增长。  
  - 用通俗的话说，就是「遍历一遍数组就完事」，不再像暴力那样每次都重新看 `k` 个数。

- **空间复杂度**：`O(k)`  
  - 哈希表里最多保存当前窗口的 `k` 个不同元素的计数，最多占用 `k` 条记录。  
  - 这比暴力解的 `O(k)` 额外空间更精细，因为我们不再存整段子数组，只保存计数。

---

## 心得

- **核心技巧**：**滑动窗口** + **哈希表（频率计数）**，用于在固定长度窗口内快速判断「所有元素唯一」并维护窗口和。  
- **适用的题型**  
  1. 「长度固定的子数组满足某种属性」——如「最长子数组且元素不重复」等。  
  2. 「子数组和/乘积满足条件」——如「最长子数组和 ≤ target」等。  
  3. 「窗口内出现次数满足限制」——如「最多出现 K 次的字符子串」等。  
- **一句话总结解题钥匙**：**把窗口视作一辆“移动的盒子”，只在进出时增减元素和计数，就能做到 O(n) 线性遍历**。

---

## 反思

- **第一反应**：直接枚举所有长度为 `k` 的子数组，然后逐个检查唯一性。  
- **最容易踩的坑**  
  - **忘记在左端移出元素时同步更新哈希表的计数**，导致判断唯一性时出现假阳性。  
  - **边界条件**：`k` 可能等于 `len(nums)`，此时只会检查唯一性一次；`k` 大于数组长度时直接返回 `0`。  
  - **字典键未删除**：如果只把计数减到 `0` 而不删键，`len(freq)` 会不准确，影响唯一性判断。  
- **下次类似题的第一步**：先问自己「窗口每次只会改变哪些元素？」并准备一个**频率哈希表**和**当前统计值（和/乘积等）**，这样就能直接套用滑动窗口的模板。