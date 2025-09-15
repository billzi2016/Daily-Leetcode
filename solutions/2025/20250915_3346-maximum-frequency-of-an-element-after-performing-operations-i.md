# #3346. 元素操作后的最大出现频率 I / Maximum Frequency of an Element After Performing Operations I

> 难度：中等 · 标签：Array、Binary Search、Sliding Window、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-i/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums and two integers k and numOperations.
You must perform an operation numOperations times on nums, where in each operation you:
Return the maximum possible frequency of any element in nums after performing the operations.

**Examples**

**Example 1:**

```
Input: nums = [1,4,5], k = 1, numOperations = 2
Output: 2
Explanation:
We can achieve a maximum frequency of two by:
```

**Example 2:**

```
Input: nums = [5,11,20,20], k = 5, numOperations = 1
Output: 2
Explanation:
We can achieve a maximum frequency of two by:
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 105
- 0 <= k <= 105
- 0 <= numOperations <= nums.length

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `nums`，以及两个整数 `k` 和 `numOperations`。  
你必须对 `nums` 执行 `numOperations` 次操作，每一次操作的具体内容如下（题目原文未给出，这里保持原样）：  

返回在完成所有操作后，`nums` 中任意元素可能达到的最大出现频率（frequency）。

---

**示例 1**  
**输入**: `nums = [1,4,5]`, `k = 1`, `numOperations = 2`  
**输出**: `2`  
**解释**:  
我们可以通过以下方式实现出现频率为 **2**：

（此处省略具体操作步骤，保持原题格式）

---

**示例 2**  
**输入**: `nums = [5,11,20,20]`, `k = 5`, `numOperations = 1`  
**输出**: `2`  
**解释**:  
我们可以通过以下方式实现出现频率为 **2**：

（此处省略具体操作步骤，保持原题格式）

---

**约束条件**  

- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^5`  
- `0 <= k <= 10^5`  
- `0 <= numOperations <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的目标值**，看把哪些元素“改造成”这个目标值后，出现次数最多能是多少。  

- **把数组排好序**，这样相同目标值的候选元素会集中在一起，方便统计。  
- 对于每一个候选目标 `t`（即数组中的某个数），我们遍历整个数组，统计把哪些元素提升到 `t` 需要的操作次数。  
- 只要累计的操作次数不超过 `k * numOperations`（每次操作可以把一个数增加 `k`，一共可以操作 `numOperations` 次），就可以把这些元素都变成 `t`，于是 `t` 的出现频率就是这些元素的数量。  

> **类比**：把 `k` 想成一本字典里每页能写的字数，`numOperations` 是你手里有的笔。每次用笔在某页上写 `k` 个字，最多写 `numOperations` 次。要让几个词的解释都在同一页（相同数值），就要算总共需要写多少字，不能超过笔的总容量。

- **为什么正确**：我们把所有可能的目标值都尝试了一遍，只要有一种方式可以在预算内把 `freq` 个数变成同一个值，就会在对应的目标 `t` 那里被记录下来。最终取最大 `freq`，自然就是答案。

- **时间/空间复杂度**：  
  - 对每个目标值我们要遍历整个数组，数组长度记作 `n`，所以时间是 `O(n²)`（两层循环）。  
  - 只用了常数级别的额外变量，空间是 `O(1)`。

> **大白话解释 O(n²)**：如果数组有 1000 个数，暴力解要做大约 1000 × 1000 = 1 000 000 次“检查”。当 `n` 再大一点（比如 10⁵），次数会变成 10⁵ × 10⁵ = 10¹⁰，根本跑不完。

#### 代码（Python）

```python
from typing import List

def maxFrequency_bruteforce(nums: List[int], k: int, numOperations: int) -> int:
    # 总的可用“增量” = 每次可以加 k，最多可以做 numOperations 次
    budget = k * numOperations

    nums.sort()                     # 先排好序，方便后面枚举目标值
    n = len(nums)
    best = 1                        # 至少每个数自己就是频率 1

    for i in range(n):              # 以 nums[i] 为目标值 t
        t = nums[i]
        ops_used = 0                 # 已经用了多少增量
        cnt = 0                      # 已经可以变成 t 的元素个数

        for j in range(n):          # 逐个检查每个元素能否提升到 t
            if nums[j] > t:          # 已经比目标大，后面的更大，直接跳出
                break
            need = t - nums[j]       # 把 nums[j] 提升到 t 需要多少增量
            if ops_used + need > budget:   # 超预算就不能再加入
                break
            ops_used += need
            cnt += 1

        best = max(best, cnt)       # 更新全局最大频率

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n²)` —— 两层循环，外层遍历每个可能的目标值，内层遍历数组统计所需增量。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量（排序除外，原地排序不计额外空间）。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次都要重新遍历整个数组**，导致二次方的时间。  
观察一下：  

1. **数组排序后**，如果我们把窗口 `[l, r]`（左闭右闭）里的所有数都提升到窗口最右端的数 `nums[r]`，  
   那么需要的增量是  

   ```
   needed = nums[r] * (r - l + 1) - sum(nums[l..r])
   ```

   这正是“把窗口里的所有数变成同一个最大值”所消耗的资源。  

2. **窗口向右滑动**时，`nums[r]` 只会增大，`needed` 只会**单调不减**。  
   当 `needed` 超过我们拥有的预算 `budget = k * numOperations` 时，说明窗口太宽了，左边界 `l` 必须右移，缩小窗口，直到 `needed` 再次不超预算。  

这就是典型的 **滑动窗口（双指针）** 思路：  

- 先把数组升序排列。  
- 用两个指针 `l`、`r` 维护一个合法窗口，使得窗口内所有数提升到 `nums[r]` 所需的总增量 ≤ `budget`。  
- 每次把右指针右移一次，更新窗口的元素和 `window_sum`，再检查 `needed` 是否超预算；若超，则左指针右移，缩小窗口并相应减去左端元素的值。  
- 窗口长度 `r - l + 1` 就是把这段数变成同一个值的最大频率，遍历过程中取最大值即可。

> **核心概念——前缀和**：我们用 `window_sum` 保存当前窗口元素的和，`needed` 的公式只需要 `window_sum`，不必每次重新遍历窗口。  

> **类比**：把窗口想成一段装满水的管子，`budget` 是管子能承受的最大水量。往右扩张管子会让水位（`needed`）升高；如果水位超过管子承受的上限，就必须把左边的水倒掉（左指针右移），保持水位不超限。

#### 代码（Python）

```python
from typing import List

def maxFrequency(nums: List[int], k: int, numOperations: int) -> int:
    """
    返回在至多 numOperations 次、每次最多增加 k 的操作后，
    任意元素出现的最大频率。
    """
    budget = k * numOperations          # 总的增量上限
    nums.sort()                         # 先排序，方便滑动窗口
    n = len(nums)

    left = 0                            # 窗口左端
    window_sum = 0                      # 窗口内元素之和
    best = 1                            # 至少每个数自己是频率 1

    for right in range(n):              # 右端一次右移
        window_sum += nums[right]       # 加入新元素
        # 计算把窗口所有数提升到 nums[right] 所需的增量
        # needed = nums[right] * window_len - window_sum
        while nums[right] * (right - left + 1) - window_sum > budget:
            # 超预算，左端收缩
            window_sum -= nums[left]
            left += 1

        # 此时窗口合法，更新答案
        best = max(best, right - left + 1)

    return best
```

> **关键行解释**  
> - `budget = k * numOperations`：把“每次最多加 k，最多可以做 numOperations 次”合并成一次性总预算。  
> - `while nums[right] * (right - left + 1) - window_sum > budget:`：判断当前窗口是否还能在预算内把所有数提升到右端的最大值。  
> - `window_sum -= nums[left]` 与 `left += 1`：左指针右移时，要同步把离开窗口的数从 `window_sum` 中减掉，保持和的正确性。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序 `O(n log n)`；滑动窗口遍历每个元素最多进出一次，`O(n)`。  
  - 与暴力的 `O(n²)` 相比，数量级下降了很多，即使 `n = 10⁵` 也能轻松跑完。  

- **空间复杂度**：`O(1)`（不计排序的原地改动）  
  - 只用了几个整型变量 `left、right、window_sum、best`，不随输入规模增长。

---

## 心得  

- **核心技巧**：**滑动窗口 + 前缀和**（窗口内元素和）在处理“在预算内把子数组统一成同一个值”这类问题时非常高效。  
- **适用的相似题型**  
  1. *LeetCode 1838 – Frequency of the Most Frequent Element*（仅有 `k`，没有 `numOperations`）  
  2. *LeetCode 1004 – Max Consecutive Ones III*（在最多翻转 `k` 个 0 的前提下求最长连续 1）  
  3. *LeetCode 424 – Longest Repeating Character Replacement*（在最多替换 `k` 次字符的前提下求最长重复子串）  

- **一句话总结解题钥匙**：  
  > 把“把一段数都提升到同一个最大值”转化为 **窗口长度 × 最大值 – 窗口和 ≤ 总预算**，用双指针保持该不等式即可。

---

## 反思  

- **拿到题目第一反应**：先想“把每个数都直接改成目标值”，于是想到枚举目标并逐个统计，需要 O(n²)。  
- **最容易踩的坑**  
  1. **预算的计算**：别忘了 `k` 是每次操作能增加的量，`numOperations` 是次数，两者要相乘得到总可用增量。  
  2. **窗口左移时的和更新**：忘记从 `window_sum` 中减去左端元素会导致 `needed` 计算错误，进而产生无限循环。  
  3. **边界情况**：当 `budget = 0`（即 `k = 0` 或 `numOperations = 0`）时，答案只能是原数组中出现次数最多的元素，此时窗口永远只能保持长度 1。  

- **下次遇到同类题，第一步该想到**：  
  **把“预算限制 + 统一值”转化为“窗口内元素和的线性不等式”，随后使用滑动窗口维护最宽合法区间**。这样可以在 O(n log n)（排序）或 O(n)（已排序）时间内得到答案。