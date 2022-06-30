# #1838. 最高频元素的出现次数 / Frequency of the Most Frequent Element

> 难度：中等 · 标签：Array、Binary Search、Greedy、Sliding Window、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/frequency-of-the-most-frequent-element/)

---

## 题目（英文原版）

**Description**

The frequency of an element is the number of times it occurs in an array.
You are given an integer array nums and an integer k. In one operation, you can choose an index of nums and increment the element at that index by 1.
Return the maximum possible frequency of an element after performing at most k operations.

**Examples**

**Example 1:**

```
Input: nums = [1,2,4], k = 5
Output: 3
Explanation: Increment the first element three times and the second element two times to make nums = [4,4,4].
4 has a frequency of 3.
```

**Example 2:**

```
Input: nums = [1,4,8,13], k = 5
Output: 2
Explanation: There are multiple optimal solutions:
- Increment the first element three times to make nums = [4,4,8,13]. 4 has a frequency of 2.
- Increment the second element four times to make nums = [1,8,8,13]. 8 has a frequency of 2.
- Increment the third element five times to make nums = [1,4,13,13]. 13 has a frequency of 2.
```

**Example 3:**

```
Input: nums = [3,9,6], k = 2
Output: 1
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105
- 1 <= k <= 105

---

## 题目（中文翻译）

数组中某个元素的出现次数称为该元素的频率（frequency）。  
给定一个整数数组 `nums` 和一个整数 `k`。在一次操作中，你可以选择 `nums` 的任意下标，并将该下标对应的元素增加 `1`。  
最多进行 `k` 次操作后，返回任意元素可能达到的最大频率。

**示例 1**  
**输入**: `nums = [1,2,4]`, `k = 5`  
**输出**: `3`  
**解释**: 将第一个元素增加三次，第二个元素增加两次，使得 `nums = [4,4,4]`。  
`4` 的频率为 `3`。

**示例 2**  
**输入**: `nums = [1,4,8,13]`, `k = 5`  
**输出**: `2`  
**解释**: 存在多种最优方案：  
- 将第一个元素增加三次得到 `nums = [4,4,8,13]`，`4` 的频率为 `2`。  
- 将第二个元素增加四次得到 `nums = [1,8,8,13]`，`8` 的频率为 `2`。  
- 将第三个元素增加五次得到 `nums = [1,4,13,13]`，`13` 的频率为 `2`。

**示例 3**  
**输入**: `nums = [3,9,6]`, `k = 2`  
**输出**: `1`

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^5`  
- `1 <= k <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是：**把每一个可能的目标值都枚举一遍**，看看把数组里哪些元素提升到这个目标值所需的总增量是否 ≤ k，能做到的最大“相同数量”就是答案。  

- **枚举目标值**：我们可以把数组中的每个元素当作“最终想让很多元素等于的数”。比如 `nums = [1,2,4]`，我们可以尝试让所有元素都变成 1、2、4 中的任意一个。  
- **统计需要的增量**：对每个目标值 `t`，遍历整个数组，计算 `max(0, t - nums[i])`（如果当前元素已经大于 `t`，就不需要增），把这些增量加起来。  
- **判断是否可行**：如果累计的增量 ≤ k，则说明在 k 次操作内可以把这些元素都提升到 `t`，此时 `t` 的出现次数就是我们可以得到的频率。  
- **取最大频率**：对所有目标值求最大可行频率即为答案。  

> **类比**：把 “哈希表” 想成字典，`key` 是数字，`value` 是它出现的次数。这里我们不需要哈希表，只是一次遍历把每个数字当作“字典里要查的词”，看能不能把其它词改成它。

**为什么正确**：因为我们枚举了所有可能的最终相等值，且对每个值都检查了是否在给定的操作次数内可以实现，所以一定能找到最优解。

**时间/空间复杂度**：  
- 外层遍历每个元素作为目标值，内层再次遍历整个数组求增量。若数组长度为 `n`，则时间复杂度是 `O(n²)`（两层循环）。  
- 只用了常数级别的额外变量（如计数器），空间复杂度是 `O(1)`。

> **大白话**：`O(n²)` 就像你在教室里让每个人都向前排一次，然后再让每个人都向前排一次……次数会爆炸，`n` 只要上万，这种方法根本跑不完。

#### 代码（Python）  

```python
def maxFrequency_bruteforce(nums, k):
    n = len(nums)
    ans = 1                     # 至少有一个元素本身的频率
    for i in range(n):          # 把 nums[i] 当作最终想要的值
        target = nums[i]
        need = 0                 # 累计把其它元素提升到 target 所需的增量
        for j in range(n):
            if nums[j] < target:        # 只对更小的元素计算增量
                need += target - nums[j]
        # 如果总增量不超过 k，说明可以让所有 ≤ target 的元素都变成 target
        if need <= k:
            # 统计有多少元素 ≤ target（这些都可以变成 target）
            freq = sum(1 for x in nums if x <= target)
            ans = max(ans, freq)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环，每层遍历 `n` 次。  
- **空间复杂度**：`O(1)` —— 只用了几个整数变量，和输入规模无关。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每次都要遍历整个数组** 来统计增量。我们需要一种方式，让“把一段连续的元素提升到同一个值”的计算变得 **快速**。  

关键观察：

1. **排序后，想让一段连续的元素都等于右端点的值最省操作**。  
   - 把数组从小到大排好序后，若我们决定把第 `r` 位的数 `nums[r]` 作为目标值，那么只可能把它左边（更小）的元素提升到 `nums[r]`，因为右边的已经不小于目标值，提升它们只会浪费操作。  
2. **滑动窗口**（Two‑Pointer）可以在 **O(n)** 时间内维护“一段连续子数组”需要的总增量。  
   - 设窗口左端点为 `l`，右端点为 `r`（`r` 正在向右扩展）。窗口内所有元素都要提升到 `nums[r]`。  
   - 所需的增量可以用 **前缀和** 或 **窗口内元素之和** 来快速算出：  
     ```
     need = (nums[r] * window_size) - sum(window)
     ```
     这里 `window_size = r - l + 1`，`sum(window)` 是窗口内所有元素的和。  
   - 当 `need > k` 时，说明当前窗口太大，无法在 k 次操作内完成，需要左移 `l` 缩小窗口，直到 `need ≤ k`。  
3. **贪心**：我们总是让窗口尽可能大（左端点尽量左移），因为更大的窗口意味着更高的频率。只要窗口合法（`need ≤ k`），就更新答案。  

**实现细节**  

- 先把 `nums` 排序。排序相当于把“不同大小的水果”按重量从轻到重排好，后面我们只会把左边更轻的水果加重到右边的重量。  
- 用两个指针 `l`、`r`，以及一个变量 `window_sum` 保存窗口内元素的总和，随 `r` 前进时把 `nums[r]` 加入 `window_sum`。  
- 每次计算 `need = nums[r] * (r - l + 1) - window_sum`。如果 `need > k`，就把 `nums[l]` 从窗口中移除（`window_sum -= nums[l]`），`l += 1`，再重新判断。  
- 当 `need ≤ k` 时，窗口合法，更新答案 `ans = max(ans, r - l + 1)`。  

> **类比**：想象你在搬箱子，箱子重量必须统一到最高的箱子重量。窗口就像一只手抓住一堆箱子，左手可以放下最轻的箱子（缩小窗口），右手不断抓更多箱子（扩大窗口），只要总共需要加的重量不超过你的力量 `k`，就可以一次性把它们搬走。

#### 代码（Python）  

```python
def maxFrequency(nums, k):
    """
    返回在至多 k 次“+1”操作后，数组中出现频率最高的元素的可能最大频率。
    """
    nums.sort()                     # 先排序，方便使用滑动窗口
    l = 0                           # 窗口左端
    window_sum = 0                  # 窗口内元素之和
    ans = 1                         # 至少有一个元素自己构成频率 1

    for r in range(len(nums)):      # 右端从左到右依次移动
        window_sum += nums[r]       # 把新元素加入窗口

        # 计算把窗口内所有数提升到 nums[r] 需要的增量
        #   nums[r] * window_size  = 目标值 * 窗口大小
        #   - window_sum            = 已经拥有的值，总和要减掉
        need = nums[r] * (r - l + 1) - window_sum

        # 如果需要的增量超过 k，左移窗口直至满足条件
        while need > k:
            window_sum -= nums[l]   # 移除左端元素
            l += 1                  # 左端右移
            need = nums[r] * (r - l + 1) - window_sum

        # 此时窗口合法，更新最大频率
        ans = max(ans, r - l + 1)

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n log n)` —— 首先排序耗 `O(n log n)`，随后左右指针各最多遍历一次，合计 `O(n)`，所以整体是 `O(n log n)`。  
  - 与暴力 `O(n²)` 相比，省去了大量重复计数，能轻松处理 `10⁵` 规模的数据。  
- **空间复杂度**：`O(1)`（不计排序本身的原地修改）—— 只用了几个整数变量，和数组长度无关。  

---

## 心得  

- **核心技巧**：先排序 + 滑动窗口（双指针） + 前缀和思想，利用“把左侧小元素提升到右端最大值” 的单调性，实现 **贪心 + O(n)** 的窗口扩张。  
- **适用的题型**：  
  1. “最长子数组，使其所有元素的和 ≤ k” （滑动窗口）  
  2. “最小操作次数使数组中所有元素相等” （类似思路）  
  3. “最长连续子序列，满足 max - min ≤ limit” （同样利用排序 + 双指针）  
- **一句话总结**：把数组排序后，用窗口维护“把左边全部提升到右边最大值所需的总增量”，让窗口尽可能大就是答案。  

---

## 反思  

- **第一反应**：看到“可以把任意元素 +1”，立刻想到“把所有想要的元素都加到同一个数”。于是想遍历每个可能的目标值，直接算需要多少次操作。  
- **最容易踩的坑**：  
  - 忘记先排序，直接在原数组上滑动窗口会导致窗口左侧可能出现比右端更大的数，增量公式不再成立。  
  - 计算增量时漏掉窗口大小乘以目标值的乘法，导致结果偏小。  
  - 边界情况：`k` 很大时，整个数组可以变成同一个数；`k` 为 0 时只能使用已有的最大频率。  
- **下次第一步**：先 **排序**，并思考 “如果把右端的数当作目标，左侧更小的数怎样最省操作”。这一步往往能把问题转化为滑动窗口或前缀和的形式，从而快速找到最优解。