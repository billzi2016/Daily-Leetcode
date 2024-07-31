# #2808. **最小秒数使循环数组相等** / Minimum Seconds to Equalize a Circular Array

> 难度：中等 · 标签：Array、Hash Table · [LeetCode 链接](https://leetcode.com/problems/minimum-seconds-to-equalize-a-circular-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums containing n integers.
At each second, you perform the following operation on the array:
Note that all the elements get replaced simultaneously.
Return the minimum number of seconds needed to make all elements in the array nums equal.

**Examples**

**Example 1:**

```
Input: nums = [1,2,1,2]
Output: 1
Explanation: We can equalize the array in 1 second in the following way:
- At 1st second, replace values at each index with [nums[3],nums[1],nums[3],nums[3]]. After replacement, nums = [2,2,2,2].
It can be proven that 1 second is the minimum amount of seconds needed for equalizing the array.
```

**Example 2:**

```
Input: nums = [2,1,3,3,2]
Output: 2
Explanation: We can equalize the array in 2 seconds in the following way:
- At 1st second, replace values at each index with [nums[0],nums[2],nums[2],nums[2],nums[3]]. After replacement, nums = [2,3,3,3,3].
- At 2nd second, replace values at each index with [nums[1],nums[1],nums[2],nums[3],nums[4]]. After replacement, nums = [3,3,3,3,3].
It can be proven that 2 seconds is the minimum amount of seconds needed for equalizing the array.
```

**Example 3:**

```
Input: nums = [5,5,5,5]
Output: 0
Explanation: We don't need to perform any operations as all elements in the initial array are the same.
```

**Constraints**

- 1 <= n == nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

你得到一个下标从 0 开始的数组 `nums`，长度为 `n`。

每秒，你可以对数组执行一次如下操作（所有元素同时替换）：

- 对于每个下标 `i`（`0 ≤ i < n`），你可以将 `nums[i]` 替换为  
  `nums[i]` 本身、左邻居 `nums[(i‑1+n) % n]`，或右邻居 `nums[(i+1) % n]` 中的任意一个值。

返回使数组 `nums` 中所有元素相等所需的最小秒数。

---

### 示例

#### 示例 1
> **输入** `nums = [1,2,1,2]`  
> **输出** `1`  
> **解释**  
> 第 1 秒，将每个位置的值分别替换为 `[nums[3], nums[1], nums[3], nums[3]]`，得到 `nums = [2,2,2,2]`。  
> 可以证明，1 秒是使数组相等的最少时间。

#### 示例 2
> **输入** `nums = [2,1,3,3,2]`  
> **输出** `2`  
> **解释**  
> 第 1 秒，将每个位置的值分别替换为 `[nums[0], nums[2], nums[2], nums[2], nums[3]]`，得到 `nums = [2,3,3,3,3]`。  
> 第 2 秒，将每个位置的值分别替换为 `[nums[1], nums[1], nums[2], nums[3], nums[4]]`，得到 `nums = [3,3,3,3,3]`。  
> 可以证明，2 秒是使数组相等的最少时间。

#### 示例 3
> **输入** `nums = [5,5,5,5]`  
> **输出** `0`  
> **解释** 初始数组所有元素已相等，无需进行任何操作。

---

### 约束条件
- `1 ≤ n = nums.length ≤ 10^5`
- `1 ≤ nums[i] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的最终值** `x`（即数组中出现过的数），然后**模拟**每一秒的替换过程，直到所有位置都变成 `x`，记录所需的秒数，最后取最小值。

- **使用的数据结构**：  
  - **哈希表**（Python 的 `dict`）可以把每个数 `x` 和它出现的下标列表对应起来。哈希表就像一本字典，`key` 是单词（这里是数组的数），`value` 是对应的解释（这里是下标列表）。  
  - **队列**或**集合**可以在每一秒保存“已经是 `x` 的位置”，因为每秒的更新是**同步**的——所有位置同时根据上一次的状态决定新值。

- **为什么正确**：  
  - 我们穷举了所有可能的目标值 `x`，只要有一种 `x` 能在 `t` 秒内让数组全部相同，就一定会在枚举中被找到。  
  - 通过一步步模拟，每一次都严格遵守题目“每秒所有元素同时被左邻或右邻的值替换”的规则，所以得到的秒数是真实需要的时间。

- **时间/空间复杂度**（大白话）  
  - 对每个不同的数 `x`，我们都要 **遍历整个数组** 去模拟，最坏情况下数组里每个数都不相同，**要模拟 `n` 次**，每次又要遍历 `n` 个位置 ⇒ **时间复杂度是 O(n²)**。  
  - 这里的 `O(n²)` 可以想象成“把一张 1000×1000 的方格纸全部填满”，随着 `n` 增大，工作量会 **呈平方级增长**，很快就不可接受。  
  - 需要保存每次模拟的状态（数组副本）和哈希表，**空间复杂度是 O(n)**，即只要能存下原数组大小的几倍就行。

#### 代码（Python）

```python
from collections import defaultdict, deque
import copy

def min_seconds_bruteforce(nums):
    n = len(nums)
    # 统计所有出现过的数
    distinct = set(nums)
    ans = float('inf')

    for target in distinct:                     # 枚举最终要统一成的数 target
        cur = nums[:]                           # cur 是每秒的当前状态（复制一份）
        seconds = 0

        # 用集合记录已经是 target 的下标，便于同步更新
        have = {i for i, v in enumerate(cur) if v == target}

        while len(have) < n:                    # 只要还有位置不是 target，就继续
            seconds += 1
            nxt = cur[:]                        # nxt 用来存放“下一秒”的结果，所有位置同步更新
            for i in range(n):
                if cur[i] != target:            # 只有不是 target 的位置需要考虑
                    # 左邻居下标（环形数组）
                    left = (i - 1) % n
                    # 右邻居下标
                    right = (i + 1) % n
                    # 如果左或右邻居已经是 target，就可以在这一秒变成 target
                    if cur[left] == target or cur[right] == target:
                        nxt[i] = target
            cur = nxt
            have = {i for i, v in enumerate(cur) if v == target}
        ans = min(ans, seconds)

    return ans
```

> **注意**：这段代码只用于说明最直观的思路，实际运行在 `n = 10⁵` 时会超时。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 对每个不同的数都要遍历整个数组一次。  
- **空间复杂度**：`O(n)` —— 需要保存当前数组的副本以及一些辅助集合。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**真正的瓶颈在于对每个可能的目标值 `x` 都要完整遍历一次**。  
实际上我们不需要模拟每一秒的过程，只要**直接算出**把所有元素变成 `x` 需要的秒数即可。

**关键观察**  

1. **传播速度**  
   - 在一次操作中，所有已经是 `x` 的位置会把它的左邻或右邻“感染”成 `x`。  
   - 因此，`x` 的连续块每秒可以向左、向右各扩展 **恰好 1 步**。  
   - 设两个相邻的 `x` 出现位置是 `i` 与 `j`（环形数组，`j > i`），它们之间的非 `x` 区间长度为 `len = j - i - 1`。  
   - 每秒两端同时向中间收缩 1，**需要的秒数等于 `⌊(j - i) / 2⌋`**（即 `len // 2 + 1 // 2`，简化后就是 ` (j-i)//2`）。  
   - 这正是题目提示给出的公式。

2. **最慢的那段决定总时间**  
   - 对于同一个目标值 `x`，数组里可能出现多段非 `x` 区间。  
   - 因为所有区间是**并行**进行的，整体完成的时间等于**最长区间**需要的时间。  
   - 所以，只要找出 `x` 在数组中出现的**相邻位置之间的最大间距** `max_gap`（环形考虑最后一个与第一个的距离），答案就是 `max_gap // 2`。

3. **只遍历一次就能得到所有 `max_gap`**  
   - 在一次线性扫描中，记录每个数最近一次出现的位置 `last[value]`，以及它第一次出现的位置 `first[value]`。  
   - 当再次看到同一个数时，计算当前间距 `i - last[value]`，更新该数的 `max_gap`，再把 `last[value] = i`。  
   - 扫描结束后，别忘了处理**环形间距**：`first[value] + n - last[value]`。  
   - 这样我们只用了 **一次 O(n) 的遍历**，就得到了所有数对应的 `max_gap`，进而得到最小的秒数。

**核心算法**：一次哈希表统计 + 取最大间距 / 2 → **线性时间**。

#### 代码（Python）

```python
def minimum_seconds(nums):
    """
    返回使环形数组所有元素相等所需的最少秒数。
    思路：对每个不同的数 x，记录它出现的下标间的最大间距 gap，
          需要的秒数 = gap // 2。答案是所有 x 中的最小值。
    """
    n = len(nums)
    # first[v] 记录 v 第一次出现的下标
    # last[v]  记录 v 最近一次出现的下标（在遍历过程中会更新）
    # max_gap[v] 记录 v 的相邻出现位置之间的最大间距
    first = {}
    last = {}
    max_gap = {}

    for i, v in enumerate(nums):
        if v not in first:               # 第一次看到 v
            first[v] = i
            last[v] = i
            max_gap[v] = 0               # 初始化最大间距为 0
        else:
            gap = i - last[v]            # 当前出现位置与上一次出现位置的距离
            if gap > max_gap[v]:
                max_gap[v] = gap
            last[v] = i                  # 更新最近一次出现的位置

    # 处理环形的间距：最后一次出现到第一次出现要跨过数组末尾
    for v in first:
        circular_gap = first[v] + n - last[v]
        if circular_gap > max_gap[v]:
            max_gap[v] = circular_gap

    # 对每个数计算需要的秒数，并取最小值
    answer = float('inf')
    for v in max_gap:
        seconds = max_gap[v] // 2       # floor((j-i)/2)
        if seconds < answer:
            answer = seconds

    return answer
```

**代码要点注释**  

- `first`, `last`, `max_gap` 都是 **哈希表**（字典），相当于“查字典”一样快速定位每个数的相关信息。  
- `gap = i - last[v]` 就是 **相邻出现位置的距离**，相当于“两个相同颜色的灯泡之间的格子数”。  
- `circular_gap` 把环形的 “尾巴连头” 也算进去，保证没有遗漏最远的那段。  
- `seconds = max_gap[v] // 2` 正是 **最长间距除以 2 向下取整**，对应题目提示的公式。

#### 复杂度

- **时间复杂度**：`O(n)` —— 只遍历一次数组，哈希表的增删查都是常数时间。  
  - 与暴力解的 `O(n²)` 相比，工作量从“平方级”降到“线性级”，即使 `n=10⁵` 也能轻松跑完。

- **空间复杂度**：`O(k)`，其中 `k` 为不同数的种类数（`k ≤ n`）。  
  - 只需要保存每个数的三个整数（第一次出现、最近一次出现、最大间距），相当于“多了一本小字典”，占用的内存与数组长度同阶。

---

## 心得

- **核心技巧**：把“每秒向左右各扩展一步”的传播过程转化为“相邻出现位置的最大间距 / 2”。  
- **适用的题型**  
  1. **环形传播类**：如 “Minimum Number of Days to Make All Flowers Bloom”。  
  2. **最大间距/最小覆盖类**：如 “Maximum Distance Between Two Same Elements”。  
  3. **同步更新的模拟类**：如 “Minimum Number of Operations to Make Array Equal”。  
- **一句话总结解题钥匙**：**只要找出目标值在数组中出现的最远相邻距离，答案就是这段距离除以二的向下取整**。

---

## 反思

- **第一反应**：看到“每秒所有元素同时被左邻或右邻的值替换”，立刻想到要**逐秒模拟**，于是写出了暴力解。  
- **最容易踩的坑**  
  - **环形处理遗漏**：忘记把最后一次出现与第一次出现之间的距离算进去，会导致答案偏小。  
  - **整数除法的取整方式**：题目要求 `⌊(j-i)/2⌋`，使用 `//`（向下取整）而不是普通除法。  
  - **只出现一次的数**：此时最大间距是整个数组长度，需要特殊考虑（公式仍然适用，但要记得把 `first` 与 `last` 的环形间距加入）。  
- **下次类似题的第一步**：**先把传播/扩散的规则抽象为“距离”或“间隔”，看看是否可以用一次遍历统计最大/最小间距**，而不是直接模拟过程。这样往往能把复杂度从平方级降到线性级。