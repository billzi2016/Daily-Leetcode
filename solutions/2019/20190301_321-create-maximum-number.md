# #321. 创建最大数 / Create Maximum Number

> 难度：困难 · 标签：Array、Two Pointers、Stack、Greedy、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/create-maximum-number/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2 of lengths m and n respectively. nums1 and nums2 represent the digits of two numbers. You are also given an integer k.
Create the maximum number of length k <= m + n from digits of the two numbers. The relative order of the digits from the same array must be preserved.
Return an array of the k digits representing the answer.

**Examples**

**Example 1:**

```
Input: nums1 = [3,4,6,5], nums2 = [9,1,2,5,8,3], k = 5
Output: [9,8,6,5,3]
```

**Example 2:**

```
Input: nums1 = [6,7], nums2 = [6,0,4], k = 5
Output: [6,7,6,0,4]
```

**Example 3:**

```
Input: nums1 = [3,9], nums2 = [8,9], k = 3
Output: [9,8,9]
```

**Constraints**

- m == nums1.length
- n == nums2.length
- 1 <= m, n <= 500
- 0 <= nums1[i], nums2[i] <= 9
- 1 <= k <= m + n
- nums1 and nums2 do not have leading zeros.

---

## 题目（中文翻译）

给定两个整数数组（integer arrays）`nums1` 和 `nums2`，它们的长度分别为 `m` 和 `n`。`nums1` 和 `nums2` 表示两个数字的各位数字。还给定一个整数 `k`。  

请从这两个数字的数字中挑选，组成长度为 `k`（且 `k ≤ m + n`）的最大数字。来自同一数组的数字在挑选后仍需保持相对顺序（relative order）。  

返回一个长度为 `k` 的数组，表示答案的各位数字。

## 示例

### 示例 1
**输入:** `nums1 = [3,4,6,5]`, `nums2 = [9,1,2,5,8,3]`, `k = 5`  
**输出:** `[9,8,6,5,3]`

### 示例 2
**输入:** `nums1 = [6,7]`, `nums2 = [6,0,4]`, `k = 5`  
**输出:** `[6,7,6,0,4]`

### 示例 3
**输入:** `nums1 = [3,9]`, `nums2 = [8,9]`, `k = 3`  
**输出:** `[9,8,9]`

## 约束条件
- `m == nums1.length`
- `n == nums2.length`
- `1 ≤ m, n ≤ 500`
- `0 ≤ nums1[i], nums2[i] ≤ 9`
- `1 ≤ k ≤ m + n`
- `nums1` 和 `nums2` 中不含前导零。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把两条数组的所有子序列（保持原来顺序）枚举出来，然后从中挑出长度为 `k`、字典序最大的那一个**。  
- **子序列**：想象我们有两串珠子（`nums1`、`nums2`），每次可以挑选若干颗珠子，挑的顺序必须跟原来的顺序一致。  
- **字典序最大**：就像比较两个单词，先比较第一个字符，谁大就谁更大；如果相同再比较第二个，以此类推。  

实现时可以把两条数组的所有可能取法分别存到列表里（比如 `choose(nums1, i)` 表示从 `nums1` 里挑 `i` 个保持顺序的子序列），再把两边挑好的子序列拼接、截取前 `k` 位，挑出最大的。

> **为什么这个方法一定能得到答案？**  
> 因为我们把所有合法的取法都穷举了，答案必然在其中。只要我们能正确比较字典序，最大者就是答案。

#### 代码（Python）

```python
from itertools import combinations

def all_subsequences(arr, t):
    """返回 arr 中保持顺序、长度恰好为 t 的所有子序列（列表）。"""
    # 用 combinations 直接挑出下标组合，保持顺序
    res = []
    for idxs in combinations(range(len(arr)), t):
        subseq = [arr[i] for i in idxs]      # 按下标取对应的数字
        res.append(subseq)
    return res

def merge(a, b, k):
    """把两个序列 a、b 合并成长度为 k 的最大序列，保持各自内部顺序。"""
    i = j = 0
    merged = []
    while len(merged) < k:
        # 若 a 剩余的字典序大于等于 b，就取 a 的当前元素
        if a[i:] > b[j:]:
            merged.append(a[i])
            i += 1
        else:
            merged.append(b[j])
            j += 1
    return merged

def maxNumber_bruteforce(nums1, nums2, k):
    m, n = len(nums1), len(nums2)
    best = [0] * k                     # 记录当前找到的最大序列
    # 枚举从 nums1 取 i 个、从 nums2 取 k-i 个的所有可能
    for i in range(max(0, k - n), min(k, m) + 1):
        seq1_list = all_subsequences(nums1, i)
        seq2_list = all_subsequences(nums2, k - i)
        for s1 in seq1_list:
            for s2 in seq2_list:
                cand = merge(s1, s2, k)   # 合并成长度 k
                if cand > best:           # Python 的列表比较就是字典序比较
                    best = cand
    return best
```

> 关键点中文注释已经写在代码里。  
> `all_subsequences` 用到了 Python 标准库的 `itertools.combinations`，它会把所有下标组合枚举出来，天然保持顺序。

#### 复杂度

- **时间复杂度**：  
  - 枚举子序列的个数是组合数 `C(m, i)`、`C(n, k-i)`，总共要遍历所有 `i`。组合数在最坏情况下指数级（约 `O(2^m)`），因此整体时间是 **指数级**，对 `m,n ≤ 500` 完全不可行。  
  - 大白话：这相当于让你把所有可能的挑选方式都写下来，再一个个比较，根本做不到。

- **空间复杂度**：  
  - 需要存放所有子序列，最坏情况下也是指数级 `O(2^m + 2^n)`。  
  - 大白话：记忆体会被子序列的“海洋”淹没。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有子序列**。实际上我们只需要**每条数组中挑出恰好 `i` 个的最大子序列**（保持顺序），再把两条最大子序列合并成长度 `k` 的最大序列。  
因此整个思路可以拆成三步：

1. **在单个数组里选出最大子序列**  
   - 这一步是经典的 **单调栈（Monotonic Stack）** 题型。  
   - 把数组看成一排珠子，要求挑出 `t` 颗珠子，使得挑出的序列字典序最大。  
   - 过程：从左到右遍历，每遇到一个数字 `x`，只要栈顶数字小于 `x` 并且后面还有足够的数字可以补齐 `t`（即还能“丢掉”栈顶），就把栈顶弹出。最后栈的前 `t` 个元素就是答案。  
   - 类比：把栈想成一条“递减的河流”，遇到更大的石头就把前面的“小石头”冲走，保证剩下的石头尽可能大。

2. **合并两条子序列得到最大序列**  
   - 合并时仍要保持字典序最大。  
   - 用 **双指针** 同时指向两条序列的当前位置，比较剩余部分的字典序（`a[i:]` 与 `b[j:]`），把字典序更大的那个元素放入结果。  
   - 这一步类似“合并两个有序队列”，但比较的不是数值大小，而是**后面剩余序列的整体大小**。

3. **遍历所有合法的分配 i**  
   - `i` 表示从 `nums1` 取 `i` 个，`k-i` 从 `nums2` 取。  
   - `i` 必须满足 `0 ≤ i ≤ len(nums1)` 且 `k-i ≤ len(nums2)`。  
   - 对每一种合法的 `i`，分别求出两条数组的最大子序列，然后合并，挑出字典序最大的那一个。

> **为什么这一步能保证全局最优？**  
> - 对每条数组我们已经找到了“在该数组内部保持顺序的最优挑选”。  
> - 合并时我们总是把“剩余字典序更大的那一边”先取，这保证了合并后的序列在每一步都是局部最优的，从而整体最优（贪心策略的标准证明）。  
> - 由于我们遍历了所有可能的 `i`，必然覆盖了答案所在的取法。

#### 代码（Python）

```python
def max_subsequence(nums, t):
    """
    在 nums 中挑出保持相对顺序、长度恰好为 t 的字典序最大的子序列。
    使用单调栈实现，时间 O(len(nums))，空间 O(t)。
    """
    drop = len(nums) - t               # 需要“丢弃”的元素个数
    stack = []
    for x in nums:
        # 当栈顶小于当前元素且还有机会再补足 t 个时，弹出栈顶
        while drop and stack and stack[-1] < x:
            stack.pop()
            drop -= 1
        stack.append(x)
    # 可能还有多余的元素，截取前 t 个即为答案
    return stack[:t]

def merge(seq1, seq2):
    """
    把两个序列合并成字典序最大的序列，保持各自内部顺序。
    采用双指针比较剩余子序列大小，时间 O(len(seq1)+len(seq2))。
    """
    i = j = 0
    merged = []
    while i < len(seq1) or j < len(seq2):
        # 若 seq1 从 i 开始的子序列字典序更大（或相等），取 seq1[i]
        if seq1[i:] > seq2[j:]:
            merged.append(seq1[i])
            i += 1
        else:
            merged.append(seq2[j])
            j += 1
    return merged

def maxNumber(nums1, nums2, k):
    """
    主函数：返回长度为 k 的最大数字序列。
    复杂度：时间 O(k * (m+n))，空间 O(k)。
    """
    m, n = len(nums1), len(nums2)
    best = [0] * k                     # 当前找到的最优序列
    # i 为从 nums1 取的个数，遍历所有合法分配
    for i in range(max(0, k - n), min(k, m) + 1):
        # 1) 分别求出两条数组的最大子序列
        subseq1 = max_subsequence(nums1, i)
        subseq2 = max_subsequence(nums2, k - i)
        # 2) 合并成长度 k 的候选序列
        candidate = merge(subseq1, subseq2)
        # 3) 更新全局最优
        if candidate > best:
            best = candidate
    return best
```

> **关键行中文注释**  
> - `drop = len(nums) - t`：需要丢掉的元素数目。  
> - `while drop and stack and stack[-1] < x:`：只要还能丢、栈不空且栈顶小于当前元素，就把栈顶弹掉。  
> - `if seq1[i:] > seq2[j:]:`：比较两个序列剩余部分的字典序，决定取哪一个。

#### 复杂度

- **时间复杂度**：  
  - `max_subsequence` 对每条数组线性扫描一次，`O(m)` / `O(n)`。  
  - `merge` 同样是线性合并，`O(k)`（因为最多取 `k` 个元素）。  
  - 外层循环遍历所有合法的 `i`，最多 `k+1` 次。  
  - 综合：**`O(k * (m + n))`**。  
  - 大白话：我们最多会执行 `k` 次“挑子序列 + 合并” 操作，每次的工作量是遍历两条原数组一次，整体是线性可接受的。

- **空间复杂度**：  
  - `max_subsequence` 需要保存最多 `t` 个元素的栈，`t ≤ k`。  
  - `merge` 产生的合并序列长度为 `k`。  
  - 因此整体额外空间是 **`O(k)`**，只和答案长度有关，远小于原数组长度。

---

## 心得

- **核心技巧**：  
  1. **单调栈** 用来在保持相对顺序的前提下，挑出字典序最大的子序列。  
  2. **贪心合并**（双指针比较剩余子序列）保证两个子序列拼接后仍是全局最大。  
  3. **枚举分配** 把问题拆成“从每条数组各挑多少” 的子问题，保证不遗漏答案。

- **该技巧适用的题型**（可类比）  
  - *LeetCode 402. Remove K Digits*（单调栈求最小数）  
  - *LeetCode 321. Create Maximum Number*（本题）  
  - *LeetCode 179. Largest Number*（把数字排列成最大数，涉及比较剩余子序列）

- **一句话总结解题钥匙**：  
  “先在每条数组内部用单调栈挑出最优子序列，再用贪心合并比较剩余字典序，遍历所有取数分配即可得到全局最大”。

## 反思

- **拿到题目第一反应**：  
  “这看起来像‘从两个序列中挑数字，保持顺序，拼成最大的数’，是不是直接把两条数组拼起来再挑最大子序列？”  
  → 立刻想到要保持每条数组内部的相对顺序，不能随意打乱。

- **最容易踩的坑**  
  1. **子序列长度合法性**：`i` 必须满足 `0 ≤ i ≤ len(nums1)` 且 `k-i ≤ len(nums2)`，否则会出现越界。  
  2. **比较剩余子序列时的切片**：`seq1[i:] > seq2[j:]` 在 Python 中是字典序比较，但切片会产生新列表，若在循环里频繁创建会导致额外的时间开销（但对本题仍在接受范围）。  
  3. **单调栈的“丢弃次数”**：`drop` 必须准确等于 `len(nums) - t`，否则可能会把太多或太少的元素弹出，导致结果长度错误。

- **下次遇到同类题，第一步该想到什么**  
  “先把每条数组内部的‘最优子序列’算出来（单调栈），再想办法把两条序列合并成全局最优（贪心比较剩余字典序）”。这一步的拆解可以把看似复杂的组合问题转化为两个相对简单的子问题。