# #1574. 删除最短子数组使数组有序 / Shortest Subarray to be Removed to Make Array Sorted

> 难度：中等 · 标签：Array、Two Pointers、Binary Search、Stack、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/shortest-subarray-to-be-removed-to-make-array-sorted/)

---

## 题目（英文原版）

**Description**

Given an integer array arr, remove a subarray (can be empty) from arr such that the remaining elements in arr are non-decreasing.
Return the length of the shortest subarray to remove.
A subarray is a contiguous subsequence of the array.

**Examples**

**Example 1:**

```
Input: arr = [1,2,3,10,4,2,3,5]
Output: 3
Explanation: The shortest subarray we can remove is [10,4,2] of length 3. The remaining elements after that will be [1,2,3,3,5] which are sorted.
Another correct solution is to remove the subarray [3,10,4].
```

**Example 2:**

```
Input: arr = [5,4,3,2,1]
Output: 4
Explanation: Since the array is strictly decreasing, we can only keep a single element. Therefore we need to remove a subarray of length 4, either [5,4,3,2] or [4,3,2,1].
```

**Example 3:**

```
Input: arr = [1,2,3]
Output: 0
Explanation: The array is already non-decreasing. We do not need to remove any elements.
```

**Constraints**

- 1 <= arr.length <= 105
- 0 <= arr[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `arr`，从中删除一个子数组（可以为空），使得剩余的元素呈非递减（non-decreasing）顺序。返回需要删除的最短子数组的长度。

子数组是数组的一个连续子序列（contiguous subsequence）。

**示例 1**  
**输入**: `arr = [1,2,3,10,4,2,3,5]`  
**输出**: `3`  
**解释**: 最短的可删除子数组是 `[10,4,2]`，长度为 3。删除后剩余的元素为 `[1,2,3,3,5]`，已经有序。另一种正确的做法是删除子数组 `[3,10,4]`。

**示例 2**  
**输入**: `arr = [5,4,3,2,1]`  
**输出**: `4`  
**解释**: 由于数组严格递减，只能保留单个元素。因此需要删除长度为 4 的子数组，可以是 `[5,4,3,2]` 或者 `[4,3,2,1]`。

**示例 3**  
**输入**: `arr = [1,2,3]`  
**输出**: `0`  
**解释**: 数组已经是非递减的，无需删除任何元素。

**约束条件**  
- `1 <= arr.length <= 10^5`  
- `0 <= arr[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**要删除的子数组的左右端点 `i、j`（`0 ≤ i ≤ j < n`），把 `arr[i…j]` 删除后，把剩下的两段拼在一起，检查拼接后的序列是否是 **非递减**（即每个数都不比左边的数小）。  

- **数据结构**：我们只需要 **列表** 本身和几个整数变量。  
  - “列表”就像一串珠子，`i`、`j` 分别指向要摘掉的那段珠子两端。  
  - 检查是否有序可以类比为 **看书**：从左到右逐页翻，看每页的编号是否不比前一页小。  

- **为什么正确**：因为我们把所有可能的删除区间都尝试了一遍，只要有一种能让剩余序列有序，就会在枚举过程中被发现。  

- **时间/空间复杂度**：  
  - 枚举 `i、j` 两层循环，最坏情况下是 `n·n/2 ≈ O(n²)` 次。  
  - 对每一对 `(i,j)` 再遍历一次数组来判断有序，需要 `O(n)`，于是总时间是 `O(n³)`。  
  - 其实我们可以在枚举时直接在 **O(1)** 时间内判断有序（利用前缀最大/后缀最小），把时间降到 `O(n²)`，这里先把最笨的 `O(n³)` 说清楚，后面再优化。  
  - 只用常数级别的额外变量，**空间**是 `O(1)`。

> **大白话**：  
> `O(n²)` 就是“如果数组有 10 000 个元素，你大概要跑 1 亿 次”。`O(n³)` 更糟，像是“要跑 1 万 亿 次”。这在 10⁵ 规模的输入下根本跑不完。

#### 代码（Python）

```python
def findLengthOfShortestSubarray_bruteforce(arr):
    n = len(arr)
    # 最差情况下需要删除整个数组，长度为 n
    best = n

    # 枚举所有可能的子数组左右端点 (i, j)
    for i in range(n):
        for j in range(i, n):
            # 把 arr[i..j] 删除后，检查剩余序列是否有序
            prev = None          # 前一个保留下来的数
            ok = True
            # 先遍历左侧保留下来的部分
            for k in range(0, i):
                if prev is not None and arr[k] < prev:
                    ok = False
                    break
                prev = arr[k]
            # 再遍历右侧保留下来的部分
            if ok:
                for k in range(j + 1, n):
                    if prev is not None and arr[k] < prev:
                        ok = False
                        break
                    prev = arr[k]

            # 如果有序，更新最短长度
            if ok:
                best = min(best, j - i + 1)

    return best
```

#### 复杂度  

- **时间复杂度**：`O(n³)`（三层循环：`i`、`j`、遍历检查）  
  - 含义：如果数组长度翻倍，运行时间大约会增加 **8 倍**（因为 2³ = 8）。  
- **空间复杂度**：`O(1)`（只用常数个额外变量）  

---

### 2. 最优解  

#### 思路  

暴力解慢的根源在于**反复检查同样的前缀/后缀**。  
观察题目：  
- 删除一个子数组后，剩下的序列其实是 **“一个有序前缀 + 一个有序后缀”** 的拼接。  
- 前缀必须从数组最左边开始，后缀必须一直到最右边结束。  

因此我们可以先把 **最长的非递减前缀** 和 **最长的非递减后缀** 找出来：

```
arr = [1,2,3,10,4,2,3,5]
      ^^^^^           前缀 (0~2)  是递增的
                ^^^^^^   后缀 (5~7)  是递增的
```

如果把中间的 `10,4,2` 删掉，前缀的最后一个 `3` ≤ 后缀的第一个 `3`，拼接后仍然有序。  

**关键点**：只要前缀的最后一个元素 **不大于** 后缀的第一个元素，就可以把它们直接拼在一起，而不需要检查中间的元素。

接下来要做的事情是 **在前缀和后缀之间寻找最小的删除长度**。有两种实现方式：

1. **双指针（Two Pointers）**  
   - 设 `i` 为前缀的结束位置（从左到右遍历），`j` 为后缀的开始位置（从左到右遍历后缀）。  
   - 初始时 `i` 在前缀的最右端，`j` 在后缀的最左端。  
   - 若 `arr[i] ≤ arr[j]`，说明可以把 `[0..i]` 与 `[j..n-1]` 合并，删除长度为 `j-i-1`。尝试把 `i` 再往左移动（缩短前缀）看是否还能满足条件，从而得到更小的删除区间。  
   - 若不满足 `arr[i] ≤ arr[j]`，说明前缀太大，需要把 `j` 向右移动（把后缀的起点往后挪）让后缀的第一个元素更大。  

   这种过程只遍历数组一次，**时间 O(n)**，**空间 O(1)**。

2. **二分搜索（Binary Search）**（可选）  
   - 对每个前缀位置 `i`，在后缀中二分找到最左的 `j` 使得 `arr[i] ≤ arr[j]`。  
   - 由于后缀本身是有序的，二分是 `O(log n)`，整体 `O(n log n)`。  
   - 这里我们采用更直观的 **双指针** 实现。

下面用 **双指针** 详细解释每一步：

1. **找最长的递增前缀**  
   - 从左往右走，直到出现 `arr[k] > arr[k+1]` 为止。记下前缀的最后下标 `left_end`。  
   - 若整个数组已经递增，则答案是 `0`（不需要删除）。

2. **找最长的递增后缀**  
   - 从右往左走，直到出现 `arr[k-1] > arr[k]` 为止。记下后缀的起始下标 `right_start`。  

3. **初始答案**  
   - 可以只删前缀后面的全部（即保留后缀），长度为 `right_start`；  
   - 也可以只删后缀前面的全部（即保留前缀），长度为 `n-1-left_end`。  
   - 两者取最小，作为答案的初始值。

4. **双指针合并**  
   - `i` 从 `0` 遍历到 `left_end`（包括）。  
   - `j` 从 `right_start` 开始向右移动，只要 `arr[i] > arr[j]` 就把 `j` 向右推。  
   - 当 `arr[i] ≤ arr[j]` 时，`[0..i]` 与 `[j..n-1]` 可以拼接，删除长度为 `j-i-1`。更新最小答案。  
   - 继续把 `i` 往右走，重复上述过程。  

这样我们只用 **一次线性扫描** 就找到了最短的需要删除的子数组。

#### 代码（Python）

```python
def findLengthOfShortestSubarray(arr):
    n = len(arr)
    if n <= 1:
        return 0

    # 1️⃣ 找最长的非递减前缀
    left_end = 0
    while left_end + 1 < n and arr[left_end] <= arr[left_end + 1]:
        left_end += 1
    # 整个数组已经递增
    if left_end == n - 1:
        return 0

    # 2️⃣ 找最长的非递减后缀
    right_start = n - 1
    while right_start - 1 >= 0 and arr[right_start - 1] <= arr[right_start]:
        right_start -= 1

    # 3️⃣ 初始答案：只保留前缀或只保留后缀
    ans = min(n - left_end - 1,      # 删除左端的后半段
              right_start)           # 删除右端的前半段

    # 4️⃣ 双指针尝试把前缀 + 后缀拼起来
    i = 0
    j = right_start
    while i <= left_end and j < n:
        if arr[i] <= arr[j]:
            # 前缀 [0..i] 与后缀 [j..n-1] 能拼接
            ans = min(ans, j - i - 1)   # 删除区间长度
            i += 1                      # 继续尝试更长的前缀
        else:
            # 前缀太大，后缀需要向右移动
            j += 1

    return ans
```

> **代码注释**（每行中文解释）  
> - `left_end`：前缀的最右下标，就像从左边一直走到“坡道的尽头”。  
> - `right_start`：后缀的最左下标，等价于从右边一直走到“坡道的起点”。  
> - `ans`：当前找到的最短删除长度。先把“只保留左边”或“只保留右边”两种极端情况算进去。  
> - 双指针循环：`i` 代表我们挑选的前缀长度，`j` 代表我们挑选的后缀起点。只要前缀最后一个数不大于后缀第一个数，就可以把它们拼在一起，更新答案。否则让后缀右移，直到条件满足。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历数组几遍（一次找前缀，一次找后缀，最后一次双指针），即使 `n` 翻倍，运行时间也只会 **大约翻倍**（线性关系）。  
- **空间复杂度**：`O(1)`  
  - 只用了常数个整数变量，没有额外的数组或递归栈。

---

## 心得  

- **核心技巧**：把“删除子数组后剩余有序”转化为“**有序前缀 + 有序后缀** 且前缀最后一个 ≤ 后缀第一个”。  
- **适用的题型**（类似思路）  
  1. “最短子数组使整体有序”系列（如 LeetCode 1746 — 删除子数组使数组递增）。  
  2. “合并两个有序区间”类问题（比如在已排序数组中插入新元素后保持有序）。  
  3. “数组分割成两个单调子序列”之类的划分问题。  
- **一句话总结解题钥匙**：**先找最长的有序前缀/后缀，再用双指针让它们尽可能贴合，删掉中间的最小区间**。

---

## 反思  

- **第一反应**：看到“删除子数组”，立刻想到“枚举所有区间”。这虽然直观，却忽略了题目给出的 **有序** 约束。  
- **最容易踩的坑**  
  1. **边界条件**：数组本身已经有序时应返回 `0`，而不是 `n-1`。  
  2. **前缀/后缀交叉**：当 `left_end` 与 `right_start` 重叠时，需要保证双指针循环仍然有效，否则会产生负的删除长度。  
  3. **相等情况**：题目要求 **非递减**（≤），不能误写成严格递增（<），否则会错判 `arr[i] == arr[j]` 的可拼接性。  
- **下次遇到同类题**：第一步先**定位已有的有序段**（前缀、后缀），再思考**如何用最少的操作把它们拼接**，而不是直接暴力枚举。这样常能把时间复杂度从 `O(n²)`/`O(n³)` 降到 `O(n)`。