# #2968. 通过操作最大化频率得分 / Apply Operations to Maximize Frequency Score

> 难度：困难 · 标签：Array、Binary Search、Sliding Window、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/apply-operations-to-maximize-frequency-score/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums and an integer k.
You can perform the following operation on the array at most k times:
The score of the final array is the frequency of the most frequent element in the array.
Return the maximum score you can achieve.
The frequency of an element is the number of occurences of that element in the array.

**Examples**

**Example 1:**

```
Input: nums = [1,2,6,4], k = 3
Output: 3
Explanation: We can do the following operations on the array:
- Choose i = 0, and increase the value of nums[0] by 1. The resulting array is [2,2,6,4].
- Choose i = 3, and decrease the value of nums[3] by 1. The resulting array is [2,2,6,3].
- Choose i = 3, and decrease the value of nums[3] by 1. The resulting array is [2,2,6,2].
The element 2 is the most frequent in the final array so our score is 3.
It can be shown that we cannot achieve a better score.
```

**Example 2:**

```
Input: nums = [1,4,4,2,4], k = 0
Output: 3
Explanation: We cannot apply any operations so our score will be the frequency of the most frequent element in the original array, which is 3.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 0 <= k <= 1014

---

## 题目（中文翻译）

给定一个下标从 **0** 开始的整数数组 **nums**（array）和一个整数 **k**。  
你可以对该数组至多执行 **k** 次以下 **操作**（operation）：

- 选择任意下标 **i**，将 **nums[i]** 增加 **1** 或减少 **1**。

最终数组的 **得分**（score）定义为数组中出现次数最多的 **元素**（element）的 **频率**（frequency），即该元素在数组中出现的次数。  
返回你能够得到的最大 **得分**（score）。

**频率**（frequency）指的是某个 **元素**（element）在数组中出现的次数。

---

## 示例

### 示例 1

**输入**  
```
nums = [1,2,6,4], k = 3
```

**输出**  
```
3
```

**解释**  
我们可以按如下方式对数组进行操作：

1. 选择 `i = 0`，将 `nums[0]` 增加 `1`，得到数组 `[2,2,6,4]`。  
2. 选择 `i = 3`，将 `nums[3]` 减少 `1`，得到数组 `[2,2,6,3]`。  
3. 再次选择 `i = 3`，将 `nums[3]` 再减 `1`，得到数组 `[2,2,6,2]`。

此时元素 `2` 的出现次数为 `3`，是所有元素中出现次数最多的，故 **得分** 为 `3`。

### 示例 2

**输入**  
```
nums = [1,4,4,2,4], k = 0
```

**输出**  
```
3
```

**解释**  
由于不能进行任何 **操作**（operation），数组保持不变。原数组中出现次数最多的元素是 `4`，其出现了 `3` 次，所以 **得分** 为 `3`。

---

## 约束条件

- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `0 <= k <= 10^14`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举**每一种可能的目标值 `target`（我们希望把若干个元素都变成 `target`），然后计算把哪些元素改成 `target` 所需的最少操作次数。如果这个次数 ≤ `k`，就说明可以得到 `target` 的频率。最后取所有可行的 `target` 中最大的频率即为答案。

- **用到的数据结构**：  
  - **数组**：存放原始的 `nums`。  
  - **遍历**：对每个 `target`（可以是数组中的任意一个数）都要遍历一次数组，统计把每个元素调到 `target` 所需的步数（如果元素比 `target` 大，就需要 **减**；比 `target` 小，就需要 **加**，每次加/减 1 计一次操作）。  
  - **哈希表（字典）**（可选）：把每个 `target` 对应的最大频率记下来，类似查字典：key 是目标值，value 是能够达到的最大频率。

- **为什么正确**：  
  我们把所有可能的目标值都尝试了一遍，并且对每个目标值都算出了最少的操作次数。如果这次数在预算 `k` 之内，就说明我们真的可以把这些元素都改成 `target`，于是 `target` 的出现次数就是一种合法的“频率”。取最大的合法频率，自然就是题目要求的最大得分。

- **时间/空间复杂度**（大白话解释）：  
  - 对每个可能的 `target`（最多 `n` 种），我们都要遍历整个数组（`n` 个元素），所以总共要做 `n × n` 次工作，也就是 **O(n²)**。如果 `n=10⁵`，这相当于 **一万亿** 次操作，根本跑不完。  
  - 只用了几个额外的变量或一个字典，空间上是 **O(n)**（字典最多存 `n` 条记录），相对来说不算大。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def maxFrequency_bruteforce(nums: List[int], k: int) -> int:
    n = len(nums)
    best = 0                     # 当前找到的最大频率
    # 把每个可能的目标值都遍历一遍
    for target in nums:
        cnt = 0                  # 统计能够变成 target 的元素个数
        cost = 0                 # 已经用了多少操作次数
        # 对每个元素，算把它调到 target 需要多少步
        for x in nums:
            diff = abs(x - target)   # 需要的操作次数（加或减）
            if cost + diff <= k:     # 预算够的话就把它算进去
                cost += diff
                cnt += 1
        best = max(best, cnt)        # 更新答案
    return best
```

> **注意**：上述代码仅作思路演示，实际运行会因为 **O(n²)** 的时间而超时。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 需要对每个可能的目标值遍历整个数组。可以把它想象成“把每个人的成绩都和每个人的目标成绩比较一次”，人数越多，比较次数呈平方增长。
- **空间复杂度**：`O(1)`（不计输入数组）—— 只用了常数个计数器和临时变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有目标值并逐个检查**是最慢的环节。我们需要一种方式，**一次遍历就能判断一段连续子数组是否可以在 ≤ k 步内统一成同一个数**。关键观察如下：

1. **排序后统一的目标值一定是子数组的最大元素**  
   把数组升序排列后，如果我们想把某段子数组里的所有数都变成相同的值，最省操作的做法是把它们都调到**这段子数组的最大值**（因为把小的调大只需要加，调小的反而要额外的减法，会浪费操作次数）。  
   > 类比：把一堆不同高度的杯子装满水，最省水的是把所有杯子都灌到最高的那只杯子容量。

2. **使用前缀和快速计算所需操作次数**  
   对排好序的数组 `arr`，设 `arr[l..r]` 为当前窗口。要把 `arr[l..r]` 全部变成 `arr[r]`（窗口最右端的值），需要的操作次数是：  
   ```
   ops = (arr[r] * (r - l + 1)) - (arr[l] + arr[l+1] + ... + arr[r])
   ```
   前面的 `(arr[r] * window_len)` 表示如果每个位置都已经是 `arr[r]`，总和应该是多少；后面的 `window_sum`（窗口内元素的实际和）是我们已经拥有的。两者差值正好是把所有元素提升到 `arr[r]` 所需的总增量。  
   只要我们能在 **O(1)** 时间得到窗口的元素和，就可以在 **O(1)** 判断窗口是否可行。这里用 **前缀和**（累加数组）来实现：`prefix[i] = arr[0] + ... + arr[i-1]`，于是 `window_sum = prefix[r+1] - prefix[l]`。

3. **滑动窗口（双指针）寻找最长合法子数组**  
   - 维护一个左指针 `l`，右指针 `r` 逐步向右扩张。  
   - 每次把 `arr[r]` 加入窗口后，计算 `ops`。  
   - 如果 `ops > k`，说明窗口太大，需要把左边界右移（`l += 1`），直到 `ops ≤ k`。  
   - 在每一步，记录窗口长度 `r - l + 1` 的最大值，即为可以在 ≤ k 步内统一的最大元素个数，也就是答案。  

   这一步的时间复杂度是 **O(n)**，因为每个指针最多只会遍历数组一次。

4. **为什么不需要二分搜索**  
   题目提示可以用二分搜索找最长子数组，但滑动窗口已经在一次遍历中完成了同样的工作，且实现更直观。二分搜索的思路是：对每个右端 `r`，二分查找最左的 `l` 使得 `ops ≤ k`；这本质上和滑动窗口的移动是一致的，只是写法不同。

> **核心技巧总结**：  
> - 先排序，使得“把一段变成同一个数”只需要考虑提升到段内最大值。  
> - 用前缀和把“提升总量”转化为常数时间的公式。  
> - 用滑动窗口把窗口长度最大化，同时保证所需操作 ≤ k。

#### 代码（Python）

```python
from typing import List

def maxFrequency(nums: List[int], k: int) -> int:
    # 1. 排序，便于统一为窗口最大值
    nums.sort()
    n = len(nums)

    # 2. 前缀和，prefix[i] = nums[0] + ... + nums[i-1]
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    max_len = 1          # 至少可以保留一个元素本身
    left = 0             # 窗口左端

    # 3. 右指针遍历整个数组
    for right in range(n):
        # 当前窗口长度
        window_len = right - left + 1
        # 需要的操作次数：把窗口内所有数提升到 nums[right]
        # ops = nums[right] * window_len - (sum of window)
        ops = nums[right] * window_len - (prefix[right + 1] - prefix[left])

        # 4. 若超出预算 k，左指针右移，缩小窗口
        while ops > k:
            left += 1
            window_len = right - left + 1
            ops = nums[right] * window_len - (prefix[right + 1] - prefix[left])

        # 5. 更新答案
        max_len = max(max_len, window_len)

    return max_len
```

> **代码要点注释**  
> - 第 2 步的 `prefix` 就像一本“累计账本”，随时可以算出任意区间的和。  
> - `ops` 的公式可以理解为“把每个小杯子装满到最高杯子的容量”，差值正是需要倒进去的水量（即操作次数）。  
> - `while ops > k` 循环是“窗口太大，左边的杯子太矮，需要把左边的杯子踢出去”，这样才能让总水量不超预算。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 排序需要 `O(n log n)`。  
  - 之后的滑动窗口遍历每个元素最多两次（右指针一次，左指针最多一次），是 `O(n)`，不影响整体的 `O(n log n)`。  
  - 与暴力解的 `O(n²)` 相比，`n` 增长到 10⁵ 时仍然可以在毫秒级完成。

- **空间复杂度**：`O(n)`  
  - 需要额外的前缀和数组 `prefix`（长度 `n+1`）和若干常数变量。  
  - 相比于只使用常数空间的解法，这里多用了线性空间，但在本题的约束下完全可以接受。

---

## 心得

- **核心技巧**：**排序 + 前缀和 + 滑动窗口**，把“把一段数字统一”转化为“把窗口内所有数字提升到窗口最大值”，并用前缀和快速求和，滑动窗口保证在 O(n) 内找到最长合法子数组。  
- **适用的题型**（类似思路）  
  1. *Frequency of the Most Frequent Element*（本题本身）。  
  2. *Longest Subarray with Sum at Most K*（利用前缀和 + 双指针）。  
  3. *Maximum Frequency Stack*（涉及把元素统一到某个值的贪心/滑动窗口思路）。  
- **一句话总结解题钥匙**：**先把数组排好序，让“统一”为“把小的提升到最大的”，再用前缀和算出提升代价，滑动窗口帮你在 O(n) 内找到最大可统一的子段。**

---

## 反思

- **第一反应**：看到“最多 k 次增减”，立刻想到“把若干个数变成相同的”，于是尝试枚举每个可能的目标值——这就是暴力思路。  
- **最容易踩的坑**  
  - 忽略排序后**只能提升**而不能同时降低的事实，导致错误地把差值取绝对值。  
  - 前缀和的下标容易写错（`prefix[right+1] - prefix[left]`），要确保窗口和对应正确的区间。  
  - 当 `k` 很大（如 10¹⁴）时，`ops` 可能超过 32 位整数范围，必须使用 Python 的大整数或在 C++/Java 中使用 `long long`。  
- **下次遇到同类题**：第一步想到 **“先排序，让统一目标变成窗口右端的值”，再用 **前缀和** 快速求窗口代价，最后用 **双指针/滑动窗口** 寻找最长满足条件的子数组**。这样可以把原本指数级的搜索压缩到线性或线性对数级别。