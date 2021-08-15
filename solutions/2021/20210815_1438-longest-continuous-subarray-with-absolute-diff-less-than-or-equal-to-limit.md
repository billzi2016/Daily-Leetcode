# #1438. 最长连续子数组，使绝对差不超过限制 / Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit

> 难度：中等 · 标签：Array、Queue、Sliding Window、Heap (Priority Queue)、Ordered Set、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/)

---

## 题目（英文原版）

**Description**

Given an array of integers nums and an integer limit, return the size of the longest non-empty subarray such that the absolute difference between any two elements of this subarray is less than or equal to limit.

**Examples**

**Example 1:**

```
Input: nums = [8,2,4,7], limit = 4
Output: 2 
Explanation: All subarrays are: 
[8] with maximum absolute diff |8-8| = 0 <= 4.
[8,2] with maximum absolute diff |8-2| = 6 > 4. 
[8,2,4] with maximum absolute diff |8-2| = 6 > 4.
[8,2,4,7] with maximum absolute diff |8-2| = 6 > 4.
[2] with maximum absolute diff |2-2| = 0 <= 4.
[2,4] with maximum absolute diff |2-4| = 2 <= 4.
[2,4,7] with maximum absolute diff |2-7| = 5 > 4.
[4] with maximum absolute diff |4-4| = 0 <= 4.
[4,7] with maximum absolute diff |4-7| = 3 <= 4.
[7] with maximum absolute diff |7-7| = 0 <= 4. 
Therefore, the size of the longest subarray is 2.
```

**Example 2:**

```
Input: nums = [10,1,2,4,7,2], limit = 5
Output: 4 
Explanation: The subarray [2,4,7,2] is the longest since the maximum absolute diff is |2-7| = 5 <= 5.
```

**Example 3:**

```
Input: nums = [4,2,2,2,4,4,2,2], limit = 0
Output: 3
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109
- 0 <= limit <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums` 和一个整数 `limit`，返回满足以下条件的最长非空子数组（subarray）的长度：该子数组中任意两个元素的绝对差（absolute difference）不超过 `limit`。

## 示例

### 示例 1
**输入**  
```
nums = [8,2,4,7], limit = 4
```
**输出**  
```
2
```
**解释**  
所有子数组如下：
- `[8]`，最大绝对差 `|8-8| = 0 ≤ 4`。  
- `[8,2]`，最大绝对差 `|8-2| = 6 > 4`。  
- `[8,2,4]`，最大绝对差 `|8-2| = 6 > 4`。  
- `[8,2,4,7]`，最大绝对差 `|8-2| = 6 > 4`。  
- `[2]`，最大绝对差 `|2-2| = 0 ≤ 4`。  
- `[2,4]`，最大绝对差 `|2-4| = 2 ≤ 4`。  
- `[2,4,7]`，最大绝对差 `|2-7| = 5 > 4`。  
- `[4]`，最大绝对差 `|4-4| = 0 ≤ 4`。  
- `[4,7]`，最大绝对差 `|4-7| = 3 ≤ 4`。  
- `[7]`，最大绝对差 `|7-7| = 0 ≤ 4`。  

最长满足条件的子数组长度为 `2`（如 `[2,4]` 或 `[4,7]`）。

### 示例 2
**输入**  
```
nums = [10,1,2,4,7,2], limit = 5
```
**输出**  
```
4
```
**解释**  
子数组 `[2,4,7,2]` 是最长的合法子数组，因为其最大绝对差 `|2-7| = 5 ≤ 5`。

### 示例 3
**输入**  
```
nums = [4,2,2,2,4,4,2,2], limit = 0
```
**输出**  
```
3
```
**解释**  
在 `limit = 0` 的情况下，合法子数组只能包含相同的元素。最长的此类子数组长度为 `3`（如 `[2,2,2]`）。

## 约束条件
- `1 <= nums.length <= 10^5`
- `1 <= nums[i] <= 10^9`
- `0 <= limit <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举所有可能的子数组**，检查每个子数组的最大值和最小值之差是否 ≤ `limit`，如果满足，就更新答案的最大长度。

- **枚举子数组**：可以用两层循环，外层固定左端点 `i`，内层把右端点 `j` 从 `i` 往后移动。每次扩展子数组时，实时维护当前子数组的最大值和最小值。
- **数据结构**：这里不需要额外的数据结构，只用两个整数 `cur_max`、`cur_min` 保存当前子数组的最大、最小元素。想象它们像是“查字典”——我们随时把看到的数字记下来，随时可以得到当前的最大/最小。
- **正确性**：因为我们把 **所有** 子数组都检查了一遍，必然能找到满足条件的最长那一个。

#### 代码（Python）

```python
from typing import List

def longest_subarray_brute(nums: List[int], limit: int) -> int:
    n = len(nums)
    ans = 0                         # 记录目前找到的最长长度
    for i in range(n):              # 左端点
        cur_max = cur_min = nums[i] # 子数组只有一个元素时，最大最小相等
        for j in range(i, n):       # 右端点
            # 更新当前子数组的最大、最小值
            cur_max = max(cur_max, nums[j])
            cur_min = min(cur_min, nums[j])
            # 判断是否满足限制
            if cur_max - cur_min <= limit:
                ans = max(ans, j - i + 1)   # 记录更大的长度
            else:
                # 已经不满足，继续往右扩展也不会恢复，因为最大值只会更大或最小值只会更小
                # 可以提前结束内层循环，省点时间
                break
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环分别遍历 `n` 次，最坏情况下每次都要检查 `n` 个右端点。用大白话说，就是 **“每个元素都要和后面的每个元素比较一次”**，所以会慢到 10⁵ 的数据会超时。
- **空间复杂度**：`O(1)`  
  只用了常数个额外变量来保存最大、最小值和答案。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次左端点移动时都要重新遍历右端点**，导致大量重复计算。我们需要一种方式，让左端点和右端点只各自 **向右走一次**，并且能够 **快速得到当前窗口的最大值和最小值**。

这正好可以用 **滑动窗口 + 单调队列（Monotonic Queue）** 来实现。

1. **滑动窗口**  
   - 用两个指针 `left`、`right` 表示当前子数组 `[left, right]`（两端都包含）。  
   - `right` 每次向右移动一步，把新元素加入窗口。  
   - 当窗口不合法（即窗口内最大值 - 最小值 > limit）时，**收缩窗口**：`left` 向右移动，直到窗口重新合法。

2. **如何在 O(1) 时间得到窗口的最大值和最小值？**  
   - 维护两个 **单调递减**（存最大值）和 **单调递增**（存最小值）的双端队列 `max_q`、`min_q`。  
   - 队列里存的是 **元素的下标**，这样可以判断该元素是否已经不在窗口内（下标 < left 时弹出）。  
   - 插入新元素 `nums[right]` 时：
     - 对 `max_q`：从队尾弹出所有 **小于等于** `nums[right]` 的下标，然后把 `right` 加入队尾。这样队首永远是窗口内的最大值下标。  
     - 对 `min_q`：从队尾弹出所有 **大于等于** `nums[right]` 的下标，然后把 `right` 加入队尾。队首就是最小值下标。  
   - 这两个队列的维护过程类似 “把高低不符合顺序的元素赶走”，可以想象成 **“排队买票，只保留排在最前面的最高/最低票价”**。

3. **窗口是否合法**  
   - 当 `nums[max_q[0]] - nums[min_q[0]] > limit` 时，窗口不合法，需要把 `left` 向右移动。移动时，如果 `left` 正好等于 `max_q[0]`（或 `min_q[0]`），就把对应的队首弹出，因为它已经离开窗口。

4. **更新答案**  
   - 每次右指针移动后，只要窗口合法，就用 `right - left + 1` 更新最大长度。

这样每个元素只会被 **加入一次、弹出一次**，整体时间是线性的。

#### 代码（Python）

```python
from collections import deque
from typing import List

def longest_subarray(nums: List[int], limit: int) -> int:
    """
    滑动窗口 + 单调队列
    """
    max_q = deque()   # 存下标，队首是窗口内的最大值下标，递减队列
    min_q = deque()   # 存下标，队首是窗口内的最小值下标，递增队列
    left = 0           # 窗口左边界
    ans = 0

    for right, value in enumerate(nums):
        # 维护 max_q：删除所有 <= 当前值的下标
        while max_q and nums[max_q[-1]] <= value:
            max_q.pop()
        max_q.append(right)

        # 维护 min_q：删除所有 >= 当前值的下标
        while min_q and nums[min_q[-1]] >= value:
            min_q.pop()
        min_q.append(right)

        # 如果当前窗口不合法，左指针收缩
        while nums[max_q[0]] - nums[min_q[0]] > limit:
            left += 1                         # 左边界右移一格
            # 弹出已经离开窗口的下标
            if max_q[0] < left:
                max_q.popleft()
            if min_q[0] < left:
                min_q.popleft()

        # 窗口合法，更新答案
        ans = max(ans, right - left + 1)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个元素至多进入一次队列，又至多弹出一次。用大白话说，就是 **“所有的进出都只算一次”**，所以即使 `n = 10⁵` 也能在毫秒级完成。
- **空间复杂度**：`O(n)`（最坏情况）  
  队列里最多保存当前窗口内的所有下标。若窗口恰好是整个数组，空间就是 `n`。不过一般情况下会远小于 `n`，且只用了两个整数队列。

---

## 心得

- **核心技巧**：**滑动窗口 + 单调队列**。滑动窗口帮助我们把“左、右指针只走一次”做到；单调队列帮助我们在 **O(1)** 时间内得到窗口的最大值和最小值。
- **适用的题型**  
  1. 「最长子数组」且要求**窗口内的极值差**满足某个条件（本题）。  
  2. 「子数组的最大/最小值」统计，如「滑动窗口最大值」(LeetCode 239)。  
  3. 「满足某种单调性」的窗口，如「最长连续子数组，使得所有元素的和 ≤ K」可以用单调队列或前缀和+二分。
- **一句话总结**：**“把窗口里最大/最小值的维护交给单调队列，让窗口滑动本身负责合法性检查”。**

---

## 反思

- **第一反应**：看到“子数组的最大值和最小值差 ≤ limit”，立刻想到**滑动窗口**，因为它天然适合“连续区间”的约束。
- **最容易踩的坑**  
  1. **队列失效**：左指针移动时忘记把已经离开的下标从队首弹出，导致 `max_q[0]`、`min_q[0]` 指向已不在窗口的元素，进而产生错误的差值判断。  
  2. **边界条件**：当 `limit = 0` 时，只能接受全部相等的子数组，必须保证 `while` 循环能够收缩到只剩相同元素。  
  3. **整数溢出**：在 Python 中不必担心，但在其他语言（如 C++）要注意 `max - min` 可能超出 32 位整数范围。
- **下次类似题的第一步**：**先确认“窗口合法性只依赖于窗口内部的极值（最大/最小）或累计值”，然后决定是否需要单调队列、堆或前缀和来快速维护这些信息**。这样就能迅速锁定最优解的方向。