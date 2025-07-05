# #3254. **找到大小为 K 的子数组的 Power I** / Find the Power of K-Size Subarrays I

> 难度：中等 · 标签：Array、Sliding Window · [LeetCode 链接](https://leetcode.com/problems/find-the-power-of-k-size-subarrays-i/)

---

## 题目（英文原版）

**Description**

You are given an array of integers nums of length n and a positive integer k.
The power of an array is defined as:
You need to find the power of all subarrays of nums of size k.
Return an integer array results of size n - k + 1, where results[i] is the power of nums[i..(i + k - 1)].

**Examples**

**Example 1:**

```
Input: nums = [1,2,3,4,3,2,5], k = 3
Output: [3,4,-1,-1,-1]
Explanation:
There are 5 subarrays of nums of size 3:
```

**Example 2:**

```
Input: nums = [2,2,2,2,2], k = 4
Output: [-1,-1]
```

**Example 3:**

```
Input: nums = [3,2,3,2,3,2], k = 2
Output: [-1,3,-1,3,-1]
```

**Constraints**

- 1 <= n == nums.length <= 500
- 1 <= nums[i] <= 105
- 1 <= k <= n

---

## 题目（中文翻译）

给定一个长度为 `n` 的整数数组 `nums` 和一个正整数 `k`。  
数组的 **power** 定义为：  

你需要计算 `nums` 中所有大小为 `k` 的子数组（subarray）的 power。  
返回一个长度为 `n - k + 1` 的整数数组 `results`，其中 `results[i]` 为子数组 `nums[i .. (i + k - 1)]` 的 power。

**示例 1**  
```text
Input: nums = [1,2,3,4,3,2,5], k = 3
Output: [3,4,-1,-1,-1]
Explanation:
共有 5 个大小为 3 的子数组：
```

**示例 2**  
```text
Input: nums = [2,2,2,2,2], k = 4
Output: [-1,-1]
Explanation:
```

**示例 3**  
```text
Input: nums = [3,2,3,2,3,2], k = 2
Output: [-1,3,-1,3,-1]
Explanation:
```

**约束条件**
- `1 <= n == nums.length <= 500`
- `1 <= nums[i] <= 10^5`
- `1 <= k <= n`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的做法就是把每一个长度为 `k` 的子数组单独拿出来，统计它内部每个数字出现了几次，然后找出 **出现恰好一次的数字的最大值**。  
- **数据结构**：我们用 Python 的 `dict`（哈希表）来记录子数组中每个数的出现次数。哈希表可以类比成一本字典，**key** 就是单词（这里是数组中的数字），**value** 是对应的页码（这里是出现次数）。查找、插入、更新的时间都非常快，几乎是 **O(1)**。  
- **为什么正确**：题目要求的“子数组的 power”正好是“在该子数组中出现恰好一次的最大数字”。只要我们把每个子数组的所有数字出现次数算出来，再从中挑出符合条件的最大值，就一定得到正确答案。  

#### 代码（Python）  

```python
from typing import List

def get_power_bruteforce(nums: List[int], k: int) -> List[int]:
    n = len(nums)
    res = []

    # 枚举每一个长度为 k 的窗口
    for i in range(n - k + 1):
        freq = {}                     # 哈希表：记录窗口内每个数的出现次数
        # 统计窗口 [i, i+k) 内的频次
        for j in range(i, i + k):
            x = nums[j]
            freq[x] = freq.get(x, 0) + 1   # freq[x] += 1，若 x 不在表中则默认 0

        # 在 freq 中找出出现一次的数的最大值
        power = -1                     # -1 表示没有满足条件的数
        for num, cnt in freq.items():
            if cnt == 1 and num > power:
                power = num
        res.append(power)

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - 外层遍历每个窗口 `n‑k+1` 次，内层要遍历窗口内部的 `k` 个元素，所以总共大约是 `n·k` 次操作。  
  - 大白话：如果数组长 1000，窗口长 100，最坏情况下要做 100 000 次计数工作。  

- **空间复杂度**：`O(k)`  
  - 每个窗口最多记录 `k` 个不同的数字（哈希表的大小），其余空间都是常数级别的。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每次都要重新统计窗口内的频次**，这导致了 `O(n·k)` 的时间。  
其实，窗口在向右滑动时，只会 **失去左边的一个元素**，并 **新增右边的一个元素**。如果我们能够在滑动的过程中“增量更新”频次，就不必每次重新遍历整个窗口。  

下面一步步推导优化思路：  

1. **维护一个全局频次表** `freq`（仍然是哈希表），它始终保存当前窗口里每个数的出现次数。  
2. **维护一个只包含出现一次的数的集合** `unique_set`（在实现中使用最大堆 + 懒删除）。  
   - 当某个数的出现次数从 `0 → 1` 时，把它加入 `unique_set`。  
   - 当出现次数从 `1 → 2` 时，说明它不再是“只出现一次”，需要从 `unique_set` 移除。直接删除堆里元素代价高，于是采用 **懒删除**：仍然把它留在堆里，只在取堆顶时检查堆顶对应的频次是否仍为 1，若不是就弹出。  
3. **获取当前窗口的 power**：堆顶（即最大值）就是当前窗口中出现一次的最大数；如果堆为空，则答案为 `-1`。  

> **核心算法**：滑动窗口 + 哈希表（计数） + 最大堆（快速获取最大唯一数）  
> - **滑动窗口**：只在窗口左右各移动一步，时间是 `O(1)`。  
> - **哈希表**：增删改都是 `O(1)`。  
> - **堆**：插入和弹出都是 `O(log k)`，整个过程最多执行 `2n` 次堆操作，整体是 `O(n log k)`。  

#### 代码（Python）  

```python
import heapq
from collections import defaultdict
from typing import List

def get_power_opt(nums: List[int], k: int) -> List[int]:
    """
    滑动窗口 + 频次哈希表 + 最大堆（懒删除）
    返回所有长度为 k 的子数组的 power
    """
    n = len(nums)
    if k == 0:
        return []

    freq = defaultdict(int)          # 当前窗口内每个数的出现次数
    max_heap = []                     # Python 的 heapq 是最小堆，取负数实现最大堆
    res = []

    # ---------- 初始化前 k 个元素 ----------
    for i in range(k):
        x = nums[i]
        freq[x] += 1
        if freq[x] == 1:              # 第一次出现，加入堆
            heapq.heappush(max_heap, -x)

    # ---------- 计算第一个窗口的答案 ----------
    while max_heap and freq[-max_heap[0]] != 1:   # 懒删除：堆顶不再唯一则弹出
        heapq.heappop(max_heap)
    res.append(-max_heap[0] if max_heap else -1)

    # ---------- 窗口右移 ----------
    for i in range(k, n):
        # 1) 移出左侧元素
        left = nums[i - k]
        freq[left] -= 1
        if freq[left] == 1:           # 原来出现两次，现在只剩一次，重新加入堆
            heapq.heappush(max_heap, -left)
        # 若 freq[left] == 0，说明左侧元素已经完全离开窗口，堆里仍可能残留，需要在取堆顶时清理

        # 2) 加入新元素
        right = nums[i]
        freq[right] += 1
        if freq[right] == 1:          # 新元素首次出现，加入堆
            heapq.heappush(max_heap, -right)

        # 3) 取当前窗口的 power（堆顶即为最大唯一数）
        while max_heap and freq[-max_heap[0]] != 1:
            heapq.heappop(max_heap)   # 弹出不再唯一的元素
        res.append(-max_heap[0] if max_heap else -1)

    return res
```

> **代码要点注释**  
> - `defaultdict(int)` 自动把不存在的键初始化为 `0`，省去 `if key in dict` 的判断。  
> - 堆中存的是 **负数**，因为 `heapq` 只能实现最小堆，用负数即可模拟最大堆。  
> - “懒删除”指的是 **不在元素失去唯一性时立刻把它从堆里删**，而是等到下次取堆顶时才检查并弹出。这样可以把堆的删除操作保持在 `O(log k)`（弹出）而不是 `O(k)`（遍历寻找并删除）。  

#### 复杂度  

- **时间复杂度**：`O(n log k)`  
  - 每次窗口滑动只做常数次哈希表更新 `O(1)`，以及最多两次堆的 `push/pop`，每次 `O(log k)`。整体随 `n` 线性增长。  
  - 与暴力解的 `O(n·k)` 相比，尤其当 `k` 接近 `n` 时，提升非常明显。  

- **空间复杂度**：`O(k)`  
  - 频次表最多存放当前窗口的 `k` 种不同数字，堆里同样至多 `k` 条记录（即使有已失效的旧记录，也不会超过 `2k`，仍是线性于 `k`）。  

---

## 心得  

- **核心技巧**：**滑动窗口 + 哈希计数 + 最大堆（或平衡树）**，实现“在滑动过程中快速获取出现一次的最大元素”。  
- **适用场景**：  
  1. “在每个长度为 `k` 的子数组中统计满足某种频次条件的最大/最小值”。  
  2. “滑动窗口下的动态集合查询”，例如 LeetCode 239 **滑动窗口最大值**（使用最大堆或单调队列），以及 220 **包含重复元素的 K 个连续出现的子数组**（使用哈希表计数）。  
- **一句话总结**：把 **“每次重新统计”** 换成 **“增量维护”**，配合合适的辅助结构（堆/平衡树）即可在 `O(log k)` 内得到窗口答案。  

---

## 反思  

- **第一反应**：直接套用两层循环，先把窗口里的数字全部计数，再找最大唯一数。  
- **最容易踩的坑**：  
  - **边界条件**：`k = 1` 时每个子数组只有一个元素，答案就是该元素本身（因为它必然只出现一次）。  
  - **堆的懒删除**：如果忘记在取堆顶前清理已失效的元素，会得到错误的 power（因为堆里可能残留已出现两次的数）。  
  - **整数范围**：题目保证 `nums[i]` 为正整数，使用负数存入最大堆不会产生冲突。  
- **下次类似题**：遇到“窗口内要快速查询满足特定频次的最大/最小值”时，第一步就应该想到 **“维护一个窗口频次表 + 能快速返回 extremum 的数据结构（堆/平衡树/单调队列）”**，然后在窗口滑动时增删这两个结构。这样可以把时间从 `O(n·k)` 降到 `O(n log k)`（甚至 `O(n)`，如果使用单调队列）。