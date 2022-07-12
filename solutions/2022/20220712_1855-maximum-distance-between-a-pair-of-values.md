# #1855. 最大值对之间的最大距离 / Maximum Distance Between a Pair of Values

> 难度：中等 · 标签：Array、Two Pointers、Binary Search · [LeetCode 链接](https://leetcode.com/problems/maximum-distance-between-a-pair-of-values/)

---

## 题目（英文原版）

**Description**

You are given two non-increasing 0-indexed integer arrays nums1​​​​​​ and nums2​​​​​​.
A pair of indices (i, j), where 0 <= i < nums1.length and 0 <= j < nums2.length, is valid if both i <= j and nums1[i] <= nums2[j]. The distance of the pair is j - i​​​​.
Return the maximum distance of any valid pair (i, j). If there are no valid pairs, return 0.
An array arr is non-increasing if arr[i-1] >= arr[i] for every 1 <= i < arr.length.

**Examples**

**Example 1:**

```
Input: nums1 = [55,30,5,4,2], nums2 = [100,20,10,10,5]
Output: 2
Explanation: The valid pairs are (0,0), (2,2), (2,3), (2,4), (3,3), (3,4), and (4,4).
The maximum distance is 2 with pair (2,4).
```

**Example 2:**

```
Input: nums1 = [2,2,2], nums2 = [10,10,1]
Output: 1
Explanation: The valid pairs are (0,0), (0,1), and (1,1).
The maximum distance is 1 with pair (0,1).
```

**Example 3:**

```
Input: nums1 = [30,29,19,5], nums2 = [25,25,25,25,25]
Output: 2
Explanation: The valid pairs are (2,2), (2,3), (2,4), (3,3), and (3,4).
The maximum distance is 2 with pair (2,4).
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 105
- 1 <= nums1[i], nums2[j] <= 105
- Both nums1 and nums2 are non-increasing.

---

## 题目（中文翻译）

给定两个 **非递增（non‑increasing）**、下标从 0 开始的整数数组 `nums1` 和 `nums2`。  
若下标对 `(i, j)` 满足 `0 ≤ i < nums1.length`、`0 ≤ j < nums2.length`，且同时满足 `i ≤ j` 且 `nums1[i] ≤ nums2[j]`，则该下标对是**有效的（valid）**。该下标对的**距离（distance）**定义为 `j - i`。  

返回所有有效下标对中可能的**最大距离（maximum distance）**。如果不存在任何有效下标对，返回 `0`。  

**数组（array）** `arr` 为**非递增（non‑increasing）**的定义为：对所有 `1 ≤ i < arr.length`，都有 `arr[i‑1] ≥ arr[i]`。  

## 示例

### 示例 1
**输入**  
```text
nums1 = [55,30,5,4,2], nums2 = [100,20,10,10,5]
```
**输出**  
```text
2
```
**解释**  
有效的下标对有 `(0,0)`, `(2,2)`, `(2,3)`, `(2,4)`, `(3,3)`, `(3,4)`, `(4,4)`。  
最大距离为 `2`，对应下标对 `(2,4)`。

### 示例 2
**输入**  
```text
nums1 = [2,2,2], nums2 = [10,10,1]
```
**输出**  
```text
1
```
**解释**  
有效的下标对有 `(0,0)`, `(0,1)`, `(1,1)`。  
最大距离为 `1`，对应下标对 `(0,1)`。

### 示例 3
**输入**  
```text
nums1 = [30,29,19,5], nums2 = [25,25,25,25,25]
```
**输出**  
```text
2
```
**解释**  
有效的下标对有 `(2,2)`, `(2,3)`, `(2,4)`, `(3,3)`, `(3,4)`。  
最大距离为 `2`，对应下标对 `(2,4)`。

## 约束条件
- `1 ≤ nums1.length, nums2.length ≤ 10^5`
- `1 ≤ nums1[i], nums2[j] ≤ 10^5`
- `nums1` 与 `nums2` 均为**非递增（non‑increasing）**数组。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的下标对 `(i, j)` 都枚举一遍，检查它们是否满足题目的两个条件：

1. `i ≤ j`（左边的下标不能超过右边的下标）  
2. `nums1[i] ≤ nums2[j]`（左边的数要不大于右边的数）

如果这两个条件都成立，就算出这对的距离 `j - i`，在所有合法的距离里取最大值。

> **类比**：想象你有两排排好序的书（从大到小），要找一本左边书不比右边书厚的最远组合。暴力做法就是把每本左边的书和每本右边的书一一比对，像是把每本书都拿去对照一次。

只要遍历完所有组合，就一定能得到正确答案，因为我们没有漏掉任何可能的配对。

#### 代码（Python）

```python
from typing import List

def max_distance_bruteforce(nums1: List[int], nums2: List[int]) -> int:
    n1, n2 = len(nums1), len(nums2)
    ans = 0                                 # 用来记录最大距离
    # 双层循环枚举所有 (i, j)
    for i in range(n1):
        for j in range(i, n2):              # 必须保证 i <= j
            if nums1[i] <= nums2[j]:        # 检查数值大小关系
                ans = max(ans, j - i)       # 更新最大距离
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n1 * n2)`。  
  这里的 `n1`、`n2` 分别是两数组的长度。想象成“你得把左边的每本书和右边的每本书都比一次”，最坏情况下要做 `n1 × n2` 次比较。  
  当数组长度都达到 10⁵ 时，`n1 * n2` 可能是 10¹⁰，显然不可接受。

- **空间复杂度**：`O(1)`。只用了常数级别的额外变量 `ans`，不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **大量的重复比较**。  
因为两个数组都是 **非递增**（从大到小）排好的，我们可以利用这一点把搜索过程“跳过”很多不必要的比较。

> **关键观察**  
> - 对于固定的 `i`（左数组的下标），如果我们找到了满足 `nums1[i] ≤ nums2[j]` 的最远 `j`，那么对更小的 `i`（即左边的数更大或相等），它对应的最远 `j` **不会比** 前一个 `j` 更左。因为左边的数更大，想要满足 `≤` 的条件，需要右边的数也不小，右边的数组已经是从左到右递减的，能够满足的最远位置只能向右移动或保持不变。  

基于这点，有两种常见的实现方式：

1. **二分搜索**（对每个 `i` 在 `nums2` 中找最右侧满足条件的 `j`）  
2. **双指针**（一次遍历同时移动两个指针）

这里我们重点讲 **双指针**，因为它的实现最简洁、时间常数更小。

**双指针步骤**  

1. 初始化两个指针 `i = 0`（遍历 `nums1`）和 `j = 0`（遍历 `nums2`），以及答案 `ans = 0`。  
2. 对于每个 `i`，我们尝试把 `j` 向右移动（`j++`），只要仍满足 `j < len(nums2)` 且 `nums1[i] ≤ nums2[j]`。  
3. 当条件不再满足或 `j` 已经到达数组末尾时，当前 `j-1`（上一次满足条件的位置）就是以 `i` 为左端的最远合法右端。此时更新 `ans = max(ans, (j-1) - i)`。  
4. 然后把 `i` 往右走一步（`i++`），**不要把 `j` 往左回退**，因为如上观察，最远合法 `j` 只会不小于上一次的值。继续第 2 步。  
5. 当 `i` 走完 `nums1` 或者 `j` 已经到达 `nums2` 末尾时结束。

> **类比**：想象两个人站在两条排好序的队伍前面，左边的人只能往右走，右边的人也只能往右走。左边的人每前进一步，右边的人会尽量向前走到还能“看得见”左边人的位置。因为队伍是从高到低排的，左边的人越往后（数值更小），右边的人就越容易保持在更远的前面。

#### 代码（Python）

```python
from typing import List

def max_distance_two_pointers(nums1: List[int], nums2: List[int]) -> int:
    n1, n2 = len(nums1), len(nums2)
    i = j = 0          # i 遍历 nums1，j 遍历 nums2
    ans = 0

    while i < n1 and j < n2:
        # 只要右指针还能往右走且满足 nums1[i] <= nums2[j]，就继续移动 j
        while j < n2 and nums1[i] <= nums2[j]:
            # 更新答案：当前合法对的距离是 j - i
            ans = max(ans, j - i)
            j += 1      # 右指针继续向右尝试更远的距离
        # 当前 j 已经不满足条件（或者已经到数组末尾），左指针往右走一步
        i += 1
        # 为了保证 i <= j，必要时把 j 拉到 i 的位置
        if j < i:
            j = i
    return ans
```

> **代码要点解释**  
> - `while j < n2 and nums1[i] <= nums2[j]`：只要右边的数足够大（不小于左边的数），我们就可以把右指针继续往右推。  
> - `ans = max(ans, j - i)`：每一次右指针成功停留在合法位置，都可能产生更大的距离，立刻更新答案。  
> - `if j < i: j = i`：当左指针追上右指针时（因为 `i` 递增），必须把右指针重新拉到不小于 `i` 的位置，保持 `i ≤ j` 的约束。

#### 复杂度  

- **时间复杂度**：`O(n1 + n2)`。  
  两个指针只会各自向右走一次，最多遍历两数组的总长度。相当于“你只需要一次扫视，两个人一起向前走”，没有重复回头比较。  
  对比暴力的 `O(n1·n2)`，这是指数级的提升。

- **空间复杂度**：`O(1)`。只用了几个整型变量，不随输入规模增长。

---

## 心得

- **核心技巧**：利用数组的单调性（非递增）配合 **双指针**（或二分搜索）把“找最远合法位置”从线性搜索降到对数或一次遍历。  
- **适用的题型**  
  1. 两个有序数组之间的 “最大距离 / 最长子序列” 类问题（如 LeetCode 1060、1061）。  
  2. “在单调数组中寻找满足条件的最右/最左位置”——典型的二分搜索或滑动窗口思路（如 4. 寻找左边最近的更小元素）。  
- **一句话总结**：**把“往右找最远”交给指针一次完成，单调性保证指针永不回头**。

---

## 反思

- **第一反应**：看到 “两个非递增数组”，立刻想到可以用二分搜索，因为排序让搜索更快。随后又想到“双指针”可能更直观。  
- **最容易踩的坑**  
  - 忘记 `i ≤ j` 的约束，导致左指针跑到右指针左边，计算出负的距离。  
  - 当 `j` 已经到达数组末尾仍继续比较，会出现索引越界。  
  - 对于全不合法的情况（如所有 `nums1` 都大于 `nums2`），答案应该是 `0`，而不是未初始化的负数。  
- **下次类似题的第一步**：检查数组是否有单调性或其他结构化信息，如果有，立刻考虑“二分搜索”或“双指针”来把搜索范围压缩，而不是盲目枚举。