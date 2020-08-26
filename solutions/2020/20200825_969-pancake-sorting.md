# #969. **煎饼排序** / Pancake Sorting

> 难度：中等 · 标签：Array、Two Pointers、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/pancake-sorting/)

---

## 题目（英文原版）

**Description**

Given an array of integers arr, sort the array by performing a series of pancake flips.
In one pancake flip we do the following steps:
For example, if arr = [3,2,1,4] and we performed a pancake flip choosing k = 3, we reverse the sub-array [3,2,1], so arr = [1,2,3,4] after the pancake flip at k = 3.
Return an array of the k-values corresponding to a sequence of pancake flips that sort arr. Any valid answer that sorts the array within 10 * arr.length flips will be judged as correct.

**Examples**

**Example 1:**

```
Input: arr = [3,2,4,1]
Output: [4,2,4,3]
Explanation: 
We perform 4 pancake flips, with k values 4, 2, 4, and 3.
Starting state: arr = [3, 2, 4, 1]
After 1st flip (k = 4): arr = [1, 4, 2, 3]
After 2nd flip (k = 2): arr = [4, 1, 2, 3]
After 3rd flip (k = 4): arr = [3, 2, 1, 4]
After 4th flip (k = 3): arr = [1, 2, 3, 4], which is sorted.
```

**Example 2:**

```
Input: arr = [1,2,3]
Output: []
Explanation: The input is already sorted, so there is no need to flip anything.
Note that other answers, such as [3, 3], would also be accepted.
```

**Constraints**

- 1 <= arr.length <= 100
- 1 <= arr[i] <= arr.length
- All integers in arr are unique (i.e. arr is a permutation of the integers from 1 to arr.length).

---

## 题目（中文翻译）

**描述**  
给定一个整数数组 `arr`，通过执行一系列煎饼翻转（pancake flip）来对数组进行排序。  
一次煎饼翻转的操作步骤如下：  
（原题目未给出具体步骤，此处保持原意）  

例如，若 `arr = [3,2,1,4]`，我们选择 `k = 3` 进行煎饼翻转，则会把子数组 `[3,2,1]` 反转，翻转后 `arr = [1,2,3,4]`。

返回一个整数数组，其中的每个元素 `k` 表示一次煎饼翻转的翻转位置，使得执行完这些翻转后 `arr` 为升序。任意在不超过 `10 * arr.length` 次翻转内完成排序的答案都视为正确。

**示例 1**

```text
Input: arr = [3,2,4,1]
Output: [4,2,4,3]
Explanation:
我们执行了 4 次煎饼翻转，翻转位置分别为 4、2、4、3。
初始状态: arr = [3, 2, 4, 1]
第一次翻转 (k = 4): arr = [1, 4, 2, 3]
第二次翻转 (k = 2): arr = [4, 1, 2, 3]
第三次翻转 (k = 4): arr = [3, 2, 1, 4]
第四次翻转 (k = 3): arr = [1, 2, 3, 4]，此时数组已排序。
```

**示例 2**

```text
Input: arr = [1,2,3]
Output: []
Explanation: 输入已经是升序，无需进行任何翻转。其他合法答案，例如 [3, 3]，也会被接受。
```

**约束条件**  
- `1 <= arr.length <= 100`  
- `1 <= arr[i] <= arr.length`  
- `arr` 中的所有整数互不相同（即 `arr` 是 `1` 到 `arr.length` 的一个排列）。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把最大值一次放到最右边**，然后再把次大值放到倒数第二个位置……如此循环，直到整个数组有序。  
实现时可以用两次“煎饼翻转”把目标元素搬到它该去的地方：

1. 在当前未排好序的前缀 `[0 … cur]`（`cur` 从数组最后向前移动）里找到最大的数 `max_val`，记它的下标为 `max_idx`。  
2. **第一次翻转**：把前缀 `[0 … max_idx]` 翻转，使 `max_val` 移到最左边（下标 0）。  
3. **第二次翻转**：把前缀 `[0 … cur]` 翻转，使 `max_val` 移到下标 `cur`（即它的最终位置）。  

把这两步重复 `n-1` 次，就能把所有元素排好序。  

> **类比**：把数组想象成一摞煎饼，最大的那块先翻到最上面（第一步），再把整摞翻一次，它就掉到了最底部（第二步）。  

为什么一定能排好序？因为每轮我们都把当前未排好序区间里最大的数放到该区间最右端，后面的元素已经固定，再继续处理更左边的区间，最终整个数组按从小到大排列。

时间复杂度：我们对每个 `cur`（最多 `n` 次）都要在前缀里找最大值，找最大值是 `O(cur)`，所以总共是 `O(n + (n‑1) + … + 1) = O(n²)`。  
空间复杂度：只用了常数个临时变量，`O(1)`。

#### 代码（Python）  

```python
from typing import List

def pancake_sort_brutal(arr: List[int]) -> List[int]:
    """
    暴力思路：每次把当前未排序区间的最大值搬到最右端
    返回所有翻转时使用的 k（1-indexed）
    """
    res: List[int] = []               # 记录每一步的 k
    n = len(arr)

    # cur 表示当前要放置最大数的目标下标，从右往左遍历
    for cur in range(n - 1, 0, -1):
        # 1️⃣ 在 [0 .. cur] 区间找最大值的下标
        max_idx = 0
        for i in range(1, cur + 1):
            if arr[i] > arr[max_idx]:
                max_idx = i

        # 已经在正确位置就不需要操作
        if max_idx == cur:
            continue

        # 2️⃣ 把最大值翻到最左边（如果它本来就在最左边则跳过这一步）
        if max_idx != 0:
            # 翻转前缀 [0 .. max_idx]
            arr[:max_idx + 1] = reversed(arr[:max_idx + 1])
            res.append(max_idx + 1)   # k 是长度，使用 1-indexed

        # 3️⃣ 把最大值翻到 cur 位置
        arr[:cur + 1] = reversed(arr[:cur + 1])
        res.append(cur + 1)           # 再记录一次翻转

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  > 这里的 `n²` 可以想象成“每个元素都要遍历剩下的所有元素一次”，如果 `n = 100`，最多要做约 10,000 次比较，仍然可以在毫秒级完成。  
- **空间复杂度**：`O(1)`（不计输出列表 `res` 的空间）  
  > 只用了几个整数变量来保存下标和循环计数，基本不占额外内存。

---  

### 2. 最优解  

#### 思路  

从上面的暴力思路可以看到，**瓶颈**在于每轮都要遍历前缀找最大值，这一步的复杂度是 `O(cur)`，导致整体 `O(n²)`。  
其实我们并不需要每次都完整遍历来找最大值，只要**一次遍历就能得到最大值的下标**，而且 **每轮最多只需要两次翻转**（有时甚至只需要一次或零次）。这已经是题目要求的最少翻转次数上限（不超过 `2·n`），因此可以称为“最优解”。  

关键点如下：

1. **一次线性扫描找最大值**：在当前未排好序的前缀 `[0 … cur]` 中，用一个变量记录当前最大值的下标，遍历一次即可得到 `max_idx`。  
2. **判断是否需要翻转**  
   - 如果 `max_idx == cur`，说明最大值已经在正确位置，直接进入下一轮。  
   - 如果 `max_idx != 0`，先把它翻到最左边（一次翻转）。  
   - 再把整个前缀 `[0 … cur]` 翻转，使最大值落到 `cur` 位置（第二次翻转）。  
3. **循环结束**：当 `cur` 递减到 `0` 时，数组已经有序。  

整个过程只用了 **两次翻转**（或更少）来定位每个元素，时间仍是 `O(n²)`（因为仍需对每个 `cur` 进行一次线性扫描），但**实际操作次数更少**，且实现更简洁。  

> **类比**：把每一块最大的煎饼先翻到盘子最上面，再一次把整个盘子翻过去，这样它就落到了最底部。只要每块煎饼都这么处理一次，所有煎饼就自然排好序了。

#### 代码（Python）  

```python
from typing import List

def pancake_sort(arr: List[int]) -> List[int]:
    """
    最优解：一次遍历找最大值，最多两次翻转把它放到正确位置。
    返回翻转时使用的 k（1-indexed）。
    """
    res: List[int] = []
    n = len(arr)

    # 从数组右端向左端处理，每轮把当前最大值放到位置 cur
    for cur in range(n - 1, 0, -1):
        # 只遍历一次找到最大值的下标
        max_idx = 0
        for i in range(1, cur + 1):
            if arr[i] > arr[max_idx]:
                max_idx = i

        # 已经在目标位置，无需任何翻转
        if max_idx == cur:
            continue

        # 若最大值不在最左边，先翻到最左边
        if max_idx != 0:
            arr[:max_idx + 1] = reversed(arr[:max_idx + 1])
            res.append(max_idx + 1)   # 记录翻转长度

        # 再把它翻到 cur 位置
        arr[:cur + 1] = reversed(arr[:cur + 1])
        res.append(cur + 1)

    return res
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  > 每次循环只做一次线性扫描（`O(cur)`），所以总体仍是 `n + (n‑1) + … + 1 = O(n²)`。不过常数因子比“完全暴力”小，实际运行更快。  
- **空间复杂度**：`O(1)`（不计输出列表）  
  > 只用了几个整数变量，额外内存几乎可以忽略不计。

---  

## 心得  

- **核心技巧**：**贪心 + 两次前缀翻转**（先把目标元素搬到最左，再搬到最终位置）。  
- **适用的题型**：  
  1. **前缀翻转类排序**（如 *Pancake Sorting*、*Reverse Subarray*）  
  2. **需要把某个元素放到指定位置的“一次定位两次移动”问题（如 *Sorting with Two Swaps*）  
  3. **使用前缀操作的数组变换**（如 *Maximum Subarray after One Reverse*）  
- **一句话总结**：**每次把当前区间最大（或最小）元素搬到它该去的边缘，只需要两次前缀翻转**。

## 反思  

- **第一反应**：把数组想成一堆煎饼，先把最大的一块翻到最上面，再一次翻整个堆，使它落到底部。于是自然想到“找最大 → 两次翻转”。  
- **最容易踩的坑**：  
  - **下标与 k 的对应**：题目要求的 `k` 是 **1‑indexed** 的长度，需要记得在代码里 `k = idx + 1`。  
  - **已经在正确位置的元素**：如果直接翻转会产生多余的操作，甚至导致错误的顺序，需要先判断 `max_idx == cur`。  
  - **空数组或已排好序的情况**：返回空列表 `[]`，否则会多余地输出不必要的翻转。  
- **下次类似题的第一步**：**确定目标元素（最大/最小）在当前未处理区间的下标**，然后思考“如何只用前缀操作把它搬到正确位置”。这一步往往能直接引出贪心的两次翻转方案。