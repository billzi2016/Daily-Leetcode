# #581. 最短无序连续子数组 / Shortest Unsorted Continuous Subarray

> 难度：中等 · 标签：Array、Two Pointers、Stack、Greedy、Sorting、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/shortest-unsorted-continuous-subarray/)

---

## 题目（英文原版）

**Description**

Given an integer array nums, you need to find one continuous subarray such that if you only sort this subarray in non-decreasing order, then the whole array will be sorted in non-decreasing order.
Return the shortest such subarray and output its length.

**Examples**

**Example 1:**

```
Input: nums = [2,6,4,8,10,9,15]
Output: 5
Explanation: You need to sort [6, 4, 8, 10, 9] in ascending order to make the whole array sorted in ascending order.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 0
```

**Example 3:**

```
Input: nums = [1]
Output: 0
```

**Constraints**

- 1 <= nums.length <= 104
- -105 <= nums[i] <= 105

---

## 题目（中文翻译）

给定一个整数数组 `nums`，需要找出一个 **连续子数组**（continuous subarray），使得如果仅对该子数组进行 **非递减**（non‑decreasing）排序，整个数组即可变为非递减有序。返回满足条件的最短子数组的长度。

## 示例

**示例 1**  
输入：`nums = [2,6,4,8,10,9,15]`  
输出：`5`  
解释：需要对 `[6, 4, 8, 10, 9]` 进行升序（ascending）排序，使得整个数组变为升序有序。

**示例 2**  
输入：`nums = [1,2,3,4]`  
输出：`0`

**示例 3**  
输入：`nums = [1]`  
输出：`0`

## 约束条件

- `1 <= nums.length <= 10^4`
- `-10^5 <= nums[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一种可能的连续子数组都枚举一遍**，检查把它排序以后整个数组是否有序。  

- **枚举子数组**：用两个下标 `i`、`j`（`i ≤ j`）表示子数组 `nums[i..j]`，一共有 `n·(n+1)/2` 种可能。  
- **检查有序**：把 `nums[i..j]` 复制出来，排序（Python 的 `sorted`），再把它放回原位，最后遍历一次数组判断是否为非递减序列。  

> **哈希表类比**：如果把「是否已经排好序」想象成一本字典的查词过程，暴力解相当于把每一本可能的章节都拆下来重新排版，然后再把整本书重新检查一次。显然非常费时。

为什么能得到正确答案？因为我们把 **所有** 合法的子数组都尝试了一遍，只要有一个子数组满足「排序后整体有序」，我们就会记录它的长度，最终取最小值即可。

#### 代码（Python）

```python
from typing import List

def findUnsortedSubarray_bruteforce(nums: List[int]) -> int:
    n = len(nums)
    # 最坏情况下返回整个数组长度
    ans = n  

    # i 为子数组左端点，j 为右端点（包含）
    for i in range(n):
        for j in range(i, n):
            # 复制并排序子数组
            sorted_part = sorted(nums[i:j+1])
            # 把排序好的子数组拼回原数组（不改变原 nums）
            candidate = nums[:i] + sorted_part + nums[j+1:]

            # 检查 candidate 是否已经是非递减的
            ok = True
            for k in range(1, n):
                if candidate[k] < candidate[k-1]:
                    ok = False
                    break
            if ok:
                ans = min(ans, j - i + 1)   # 更新最小长度

    # 如果原数组本身就是有序的，ans 会被更新为 0
    return 0 if ans == n else ans
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 两层循环枚举子数组是 `O(n²)`，每次需要 `sorted`（`O(m log m)`，最坏 `O(n log n)`）再遍历检查有序性 `O(n)`，整体约为 `O(n³)`。  
  - 大白话：如果数组长度是 1000，暴力解大概要进行 **十亿次**的基本操作，显然不现实。

- **空间复杂度**：`O(n)`  
  - 为了拼接 `candidate` 需要额外的 `O(n)` 列表空间，其他变量都是常数级。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复检查同样的元素**。我们其实只需要找出最左侧和最右侧两个「界限」，把这两个界限之间的子数组全部排序即可使整个数组有序。  
关键是确定这两个界限：

1. **从左到右**，记录当前遍历到的位置的**最大值** `max_sofar`。  
   - 若出现 `nums[i] < max_sofar`，说明 `nums[i]` 比左边已经出现的最大值小，意味着它应该被放到左边的某个位置，故 `i` 必须被包含在待排序区间内。  
   - 记下所有满足此条件的最右位置 `right`。

2. **从右到左**，记录当前遍历到的位置的**最小值** `min_sofar`。  
   - 若出现 `nums[i] > min_sofar`，说明 `nums[i]` 比右边已经出现的最小值大，意味着它应该被放到右边的某个位置，故 `i` 必须被包含在待排序区间内。  
   - 记下所有满足此条件的最左位置 `left`。

最终答案就是 `right - left + 1`（若 `right <= left`，说明数组本身已经有序，返回 0）。

> **单调栈类比**：如果把数组看成一条河流，左→右遍历时我们在记录「最高水位」`max_sofar`，右→左遍历时记录「最低水位」`min_sofar`。只要出现水位倒退（即当前值低于最高或高于最低），就说明这里有「暗流」需要清理——这些位置正好构成我们要排序的子区间。

下面给出两种实现方式，**单调栈**与**双指针**思路相同，只是写法不同。这里采用双指针（两遍扫描）实现，代码最简洁。

#### 代码（Python）

```python
from typing import List

def findUnsortedSubarray(nums: List[int]) -> int:
    n = len(nums)
    # 1. 从左到右找右边界
    max_sofar = nums[0]
    right = -1                     # -1 表示暂时还没有发现需要排序的区间
    for i in range(1, n):
        if nums[i] >= max_sofar:
            max_sofar = nums[i]    # 更新左侧的最大值
        else:
            right = i               # 当前 i 必须被包含进来

    # 如果 right 仍为 -1，说明整个数组已经有序
    if right == -1:
        return 0

    # 2. 从右到左找左边界
    min_sofar = nums[-1]
    left = 0
    for i in range(n-2, -1, -1):
        if nums[i] <= min_sofar:
            min_sofar = nums[i]    # 更新右侧的最小值
        else:
            left = i                # 当前 i 必须被包含进来

    # 子数组长度即为右边界 - 左边界 + 1
    return right - left + 1
```

> **关键行中文注释**  
> - `max_sofar` / `min_sofar`：分别记录左遍历的最大值、右遍历的最小值。  
> - `right = i`、`left = i`：只要出现「逆序」就把当前位置记下来，最终的 `right`、`left` 分别是最靠右、最靠左的逆序位置。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历了数组两遍，每次都是常数时间操作。  
  - 与暴力解的 `O(n³)` 相比，长度为 10⁴ 的数组只需要几万次操作，完全在 1 ms 量级。

- **空间复杂度**：`O(1)`  
  - 只用了若干个整型变量，没有额外的数组或栈，常数级空间。

---

## 心得

- **核心技巧**：利用**单调性**（从左的最大值、从右的最小值）一次遍历找出最左/最右的「需要排序」位置。  
- **适用的题型**  
  1. **寻找最小覆盖区间**（如「找到最短连续子数组使其和 ≥ target」的双指针技巧）。  
  2. **数组的局部逆序检测**（如「判断数组是否已经局部有序」）。  
  3. **单调栈/单调队列**相关的「最近更大/更小」问题（如「每日温度」）。  
- **一句话总结**：**只要记录左侧的最高点和右侧的最低点，逆序出现的最左、最右位置就是答案**。

---

## 反思

- **第一反应**：直接想到「把所有子数组都排序后验证」——这就是暴力思路。  
- **最容易踩的坑**  
  1. **边界条件**：全局有序时 `right` 会保持初始值，需要单独返回 `0`。  
  2. **负数、重复元素**：比较时使用 `>=` / `<=` 而不是 `>` / `<`，否则会误判已经有序的相等元素。  
  3. **数组长度为 1**：同样应返回 `0`，代码里 `right == -1` 的判断自然覆盖。  
- **下次遇到同类题**：第一步先思考「是否可以通过一次或两次扫描记录全局极值来定位需要处理的区间」，而不是立刻去枚举子区间。这样往往能把时间复杂度降到线性。