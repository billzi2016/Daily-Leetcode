# #3347. 执行操作后元素的最大频率 II / Maximum Frequency of an Element After Performing Operations II

> 难度：困难 · 标签：Array、Binary Search、Sliding Window、Sorting、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-frequency-of-an-element-after-performing-operations-ii/)

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
- 1 <= nums[i] <= 109
- 0 <= k <= 109
- 0 <= numOperations <= nums.length

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `nums`，以及两个整数 `k` 和 `numOperations`。  
你需要对 `nums` 执行恰好 `numOperations` 次操作，每一次操作的具体方式如下（此处原题描述不完整）：  

返回在完成所有操作后，`nums` 中任意元素可能达到的**最大频率**（即出现次数的最大值）。

**示例 1**  
```text
Input: nums = [1,4,5], k = 1, numOperations = 2
Output: 2
Explanation:
我们可以通过以下方式使某个元素的出现次数达到 2：
（此处原题解释未给出具体操作步骤）
```

**示例 2**  
```text
Input: nums = [5,11,20,20], k = 5, numOperations = 1
Output: 2
Explanation:
我们可以通过以下方式使某个元素的出现次数达到 2：
（此处原题解释未给出具体操作步骤）
```

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^9`  
- `0 <= k <= 10^9`  
- `0 <= numOperations <= nums.length`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一次操作** 当成“把一个数改成想要的值”。  
题目允许我们 **最多改动 `numOperations` 个元素**，且每次改动只能把一个数 **上下移动不超过 `k`**（即把 `x` 改成 `[x‑k, x+k]` 区间里的任意整数）。  

> **类比**：想象桌面上有很多不同颜色的弹珠，手里有几把刷子（`numOperations` 把），每把刷子只能把弹珠的颜色改成相邻的几种（距离不超过 `k` 的颜色）。我们想让某一种颜色的弹珠尽可能多。

暴力做法就是：

1. **枚举所有可能的目标值**。  
   直觉上，目标值只可能是原数组里某个数的 `-k、原值、+k`，因为把一个数往外拉太远会超出它的可改动范围。  
2. 对每个目标值，遍历整个数组，统计：
   - 已经等于目标值的元素个数（不需要动）。
   - 能在一次操作内改成目标值的元素个数（即 `|nums[i]‑target| ≤ k`）。
3. 把 “已经等于” + “可以改动的（但受 `numOperations` 限制）” 相加，得到该目标值的最大频率。  
4. 把所有目标值的答案取最大。

**为什么正确？**  
因为我们穷举了所有**可能出现的最优目标**（题目提示已说明），并且对每个目标都用了最宽松的策略——只要可以改动，就尽量改动，直到用完 `numOperations`。所以最终得到的就是全局最大。

**复杂度分析**（大白话版）  

- 我们要检查 `3·n`（每个数的 `-k、原值、+k`）个目标。  
- 对每个目标又要遍历一遍数组 `n` 次。  

于是总共要做大约 `3·n·n ≈ 3n²` 次基本操作。  
如果 `n = 10⁵`，`n²` 就是 **一万亿**，根本跑不完。  

- **时间复杂度**：`O(n²)`（平方级，意思是随数组长度的增长，耗时会像面积一样快速增长）。  
- **空间复杂度**：`O(1)`（只用了几个计数器，和数组大小无关）。

下面给出可以直接跑通的暴力实现，代码里每行都加了中文注释，帮助你一步步跟上思路。

#### 代码（Python）

```python
from typing import List

def maxFrequency_bruteforce(nums: List[int], k: int, numOperations: int) -> int:
    # 1. 生成所有可能的目标值：每个数的 -k、原值、+k
    candidates = set()
    for x in nums:
        candidates.add(x)          # 原值
        candidates.add(x - k)      # 往左最多 k
        candidates.add(x + k)      # 往右最多 k

    best = 0  # 记录全局最大频率

    # 2. 枚举每一个目标值
    for target in candidates:
        same = 0          # 已经等于 target 的个数
        convertible = 0   # 能在一次操作内改成 target 的个数（不包括已经相同的）

        # 3. 扫描整个数组，统计上面的两个数量
        for x in nums:
            if x == target:
                same += 1
            elif abs(x - target) <= k:   # 只要距离不超过 k，就能改动
                convertible += 1

        # 4. 用掉最多 numOperations 次改动，得到此 target 的最大频率
        #    已经相同的直接算，另外还能改动的最多是 min(convertible, numOperations)
        cur = same + min(convertible, numOperations)
        best = max(best, cur)

    return best
```

#### 复杂度

- **时间复杂度**：`O(n²)` —— 解释如上，遍历 `3·n` 个目标，每个目标又遍历 `n` 次。  
- **空间复杂度**：`O(n)`（存放 `candidates` 集合，最坏情况下有 `3n` 个不同的目标值）。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“每个目标都遍历一遍数组”**，这导致了二次方的时间。  
我们要把 **“遍历次数”** 降到 **一次**，也就是 **`O(n log n)`** 或 **`O(n)`**。

关键观察：

1. **目标值只会落在一个长度为 `2k` 的区间里**。  
   对于任意目标 `t`，只能把 **值在 `[t‑k, t+k]`** 范围内的数改成 `t`（一次操作）。  
   换句话说，所有可以被改成同一个目标的数，**它们的最大值与最小值之差 ≤ 2k**。

2. 把数组 **先排序**，相邻的数才可能一起进入同一个 `2k` 区间。  
   排序后，**滑动窗口**（双指针）可以一次遍历得到所有满足 `max‑min ≤ 2k` 的子数组（即所有合法区间）。

3. 在一个合法窗口 `[L, R]` 中，我们可以把窗口里的任意 `numOperations` 个元素改成 **同一个值**，  
   但把已经等于该值的元素算进去不需要操作。  
   因此 **最优的目标值** 必然是窗口里出现次数最多的那个数（因为它已经为我们省去了最多的操作次数）。

   > **类比**：一堆学生坐在一排，老师只能让 `numOperations` 位学生换座位到同一张桌子。  
   > 那么老师会先把已经坐在这张桌子旁的学生算进去，再把最多的 `numOperations` 位其他学生叫过去。

4. 所以，对于每个窗口我们只需要知道 **窗口大小**（总可改动的元素数）和 **窗口内出现最多的元素的频率**。  
   设 `win = R‑L+1`，`maxCnt = 窗口内出现次数最多的数的个数`，则该窗口能得到的最大频率为  

   ```
   cur = min( win , maxCnt + numOperations )
   ```

   - `maxCnt + numOperations`：把窗口里最多的那类数保留下来，再把最多 `numOperations` 其他数改成它。  
   - `win`：我们不可能让频率超过窗口里元素的总数。  
   - 取两者最小值就是实际能达到的上限。

5. 把所有窗口的 `cur` 取最大，即为答案。

**如何在 O(n) 内得到 `maxCnt`？**  
因为数组已经排好序，**相同的数是连续的**。我们可以在滑动窗口的过程中维护：

- `freq`：一个字典，记录当前窗口里每个数出现的次数。  
- `maxFreq`：窗口内的最大出现次数。  

当右指针向右移动时，`freq[nums[R]] += 1`，更新 `maxFreq`。  
当左指针向右收缩时，`freq[nums[L]] -= 1`，如果被减掉的数正好是 `maxFreq`，则需要 **重新遍历字典找出新的最大值**（这一步在最坏情况下会 O(窗口大小)，但整体仍保持线性，因为每个元素的计数只会增加和减少一次）。

**时间复杂度**：  
- 排序 `O(n log n)`。  
- 滑动窗口一次遍历 `O(n)`（每个元素最多进入、离开窗口各一次）。  
- 总体 `O(n log n)`，已经可以接受。

**空间复杂度**：  
- 额外的字典最多保存 `窗口内不同值的个数`，最坏 `O(n)`，但只比输入多一个同规模的映射，符合题目要求。

下面给出完整实现，代码里每一步都有中文解释，帮助你一步步跟上。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def maxFrequency(nums: List[int], k: int, numOperations: int) -> int:
    """
    返回在最多进行 numOperations 次「把一个数改成它上下 k 范围内任意值」的操作后，
    数组中出现频率最高的元素的最大可能出现次数。
    """
    # 1. 先把数组排序，方便后面用滑动窗口找所有满足 max-min <= 2k 的区间
    nums.sort()
    n = len(nums)

    left = 0                      # 窗口左端
    freq = defaultdict(int)      # 当前窗口里每个数的出现次数
    maxFreqInWindow = 0           # 窗口内出现次数最多的数的次数
    answer = 0

    # 2. 右指针一次遍历整个数组
    for right in range(n):
        # 把 nums[right] 加入窗口
        val = nums[right]
        freq[val] += 1
        # 更新窗口内的最大出现次数
        if freq[val] > maxFreqInWindow:
            maxFreqInWindow = freq[val]

        # 3. 若窗口不满足「最大值 - 最小值 <= 2k」就收缩左端
        #    因为数组已经排好序，窗口的最小值就是 nums[left]，最大值是 nums[right]
        while nums[right] - nums[left] > 2 * k:
            # 将左端的数移出窗口
            left_val = nums[left]
            freq[left_val] -= 1
            left += 1

            # 如果移出的是当前最大频数的那个数，需要重新计算 maxFreqInWindow
            if freq[left_val] + 1 == maxFreqInWindow:   # +1 因为刚才已经减 1
                # 重新遍历字典找出新的最大值（这一步整体仍是线性的）
                maxFreqInWindow = max(freq.values()) if freq else 0

        # 4. 此时窗口 [left, right] 合法，窗口大小
        window_size = right - left + 1

        # 5. 计算以窗口内出现次数最多的数为目标时能得到的最大频率
        #    - 已经出现 maxFreqInWindow 次的数不需要操作
        #    - 还能再把最多 numOperations 其他数改成它
        #    - 频率不可能超过窗口总大小
        cur = min(window_size, maxFreqInWindow + numOperations)

        # 6. 更新全局答案
        answer = max(answer, cur)

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - `sort` 需要 `O(n log n)`。  
  - 滑动窗口遍历一次 `O(n)`，每个元素进出窗口各一次。  
  - 重新计算 `maxFreqInWindow` 的最坏情况仍然是线性的累计，不会导致总体超过 `O(n)`。

- **空间复杂度**：`O(n)`  
  - 额外的哈希表 `freq` 最多保存窗口内所有不同值的计数，最坏 `O(n)`。  
  - 其它变量都是常数级。

---

## 心得  

- **核心技巧**：**滑动窗口 + 统计窗口内出现次数最多的元素**。  
  通过把“可改动的范围”转化为长度为 `2k` 的区间，我们只需在排序后用双指针一次遍历所有合法区间，再在每个区间里找出出现最多的数即可。

- **适用的题型**  
  1. “在给定的范围内，最多可以把多少元素变成同一个值”——如本题、LeetCode 1838 “Maximum Frequency of an Element After Operations”。  
  2. “找出满足某种窗口约束的最长子数组”——比如 “最长子数组的和不超过 K”。  
  3. “在窗口中维护某种统计信息（最大频率、最小值、不同元素个数）”——如 “最长子数组包含最多 K 种不同整数”。

- **一句话总结解题钥匙**：  
  **把所有能一次改动到同一个值的元素放进一个长度不超过 `2k` 的滑动窗口，窗口内出现次数最多的数就是最佳目标。**

---

## 反思  

- **第一反应**：看到 “`k`、`numOperations`、最大频率”就想到 **枚举目标值**，于是写出了暴力解。  
- **最容易踩的坑**  
  1. **忽视窗口宽度**：必须是 `max - min ≤ 2k`，而不是 `≤ k`。  
  2. **忘记已经相同的元素不需要消耗操作次数**，导致把 `numOperations` 用得太多。  
  3. **边界条件**：`numOperations` 可能为 `0`，此时答案只能是原数组中出现最多的元素的次数；`k` 为 `0` 时只能把相同的数合并。  
- **下次类似题的第一步**：  
  **先把可改动的范围转化为一个区间约束（长度 = 2·k），然后用排序 + 双指针枚举所有合法区间**。在此基础上，再考虑如何在区间内部挑选最佳目标（通常是出现次数最多的元素或最小/最大值）。