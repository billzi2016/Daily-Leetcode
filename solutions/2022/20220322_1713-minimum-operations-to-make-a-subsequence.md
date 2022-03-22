# #1713. 使目标成为子序列的最少操作次数 / Minimum Operations to Make a Subsequence

> 难度：困难 · 标签：Array、Hash Table、Binary Search、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-a-subsequence/)

---

## 题目（英文原版）

**Description**

You are given an array target that consists of distinct integers and another integer array arr that can have duplicates.
In one operation, you can insert any integer at any position in arr. For example, if arr = [1,4,1,2], you can add 3 in the middle and make it [1,4,3,1,2]. Note that you can insert the integer at the very beginning or end of the array.
Return the minimum number of operations needed to make target a subsequence of arr.
A subsequence of an array is a new array generated from the original array by deleting some elements (possibly none) without changing the remaining elements' relative order. For example, [2,7,4] is a subsequence of [4,2,3,7,2,1,4] (the underlined elements), while [2,4,2] is not.

**Examples**

**Example 1:**

```
Input: target = [5,1,3], arr = [9,4,2,3,4]
Output: 2
Explanation: You can add 5 and 1 in such a way that makes arr = [5,9,4,1,2,3,4], then target will be a subsequence of arr.
```

**Example 2:**

```
Input: target = [6,4,8,1,3,2], arr = [4,7,6,2,3,8,6,1]
Output: 3
```

**Constraints**

- 1 <= target.length, arr.length <= 105
- 1 <= target[i], arr[i] <= 109
- target contains no duplicates.

---

## 题目（中文翻译）

给定一个由 **不同整数** 组成的数组 `target`，以及另一个可能包含重复元素的整数数组 `arr`。  
在一次操作中，你可以在 `arr` 的任意位置插入任意整数。例如，若 `arr = [1,4,1,2]`，你可以在中间插入 `3`，得到 `[1,4,3,1,2]`。注意，插入的位置也可以是数组的最前面或最后面。  

返回使 `target` 成为 `arr` 的 **子序列**（subsequence）的最少操作次数。  

**子序列** 的定义：从原数组中删除若干元素（可以为零），不改变其余元素的相对顺序而得到的新数组。例如，`[2,7,4]` 是 `[4,2,3,7,2,1,4]` 的子序列（下划线标出的元素），而 `[2,4,2]` 不是。

---

### 示例

#### 示例 1
```
Input: target = [5,1,3], arr = [9,4,2,3,4]
Output: 2
Explanation: 你可以依次插入 `5` 和 `1`，使得 arr 变为 [5,9,4,1,2,3,4]，此时 target 成为 arr 的子序列。
```

#### 示例 2
```
Input: target = [6,4,8,1,3,2], arr = [4,7,6,2,3,8,6,1]
Output: 3
```

---

### 约束条件
- `1 <= target.length, arr.length <= 10^5`
- `1 <= target[i], arr[i] <= 10^9`
- `target` 中不含重复元素。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把这道题看成**最长公共子序列**（Longest Common Subsequence，LCS）问题。  
- **LCS**：在两个序列中找出最长的、相对顺序都保持不变的子序列。  
- 如果我们已经知道 `target` 和 `arr` 的最长公共子序列长度 `L`，那么只要在 `arr` 中再插入 `len(target) - L` 个缺失的元素，就能让 `target` 成为 `arr` 的子序列。  

所以，**暴力解**就是直接求 LCS，然后用 `len(target) - LCS长度` 作为答案。

> **类比**：把 `target` 想象成一本词典，`arr` 是一本已经写好的笔记本。我们想在笔记本里“找出”能够拼出词典的最长单词序列（不要求连续，只要顺序对），这就是 LCS。

**为什么正确**  
- LCS 给出的子序列一定在 `arr` 中出现，且顺序与 `target` 完全一致。  
- 只要把 `target` 中不在这条 LCS 里的元素插进去，就可以把 `target` 完全变成 `arr` 的子序列，插入次数最少就是缺的元素个数。

**复杂度分析**  
- 经典的 LCS 动态规划需要一个二维表 `dp[m+1][n+1]`（`m = len(target)`，`n = len(arr)`），每个格子都要算一次，时间是 **O(m·n)**。  
- 表格大小也是 `O(m·n)`，这在最坏情况下（`10⁵ × 10⁵`）根本放不下，甚至会直接 **Memory Limit Exceeded**（内存溢出）。

> **大白话**：`O(m·n)` 就像把两个 10 万的数组全部两两比较，想象一下要做 10⁹ 次操作，电脑根本跑不完。

#### 代码（Python）

```python
def min_operations_bruteforce(target, arr):
    m, n = len(target), len(arr)
    # dp[i][j] 表示 target[:i] 与 arr[:j] 的最长公共子序列长度
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if target[i - 1] == arr[j - 1]:
                # 两个元素相等，公共子序列可以加长 1
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                # 取去掉 target 最后一个或 arr 最后一个的较大值
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    lcs_len = dp[m][n]                     # 最长公共子序列的长度
    return m - lcs_len                     # 需要插入的最少元素数
```

#### 复杂度

- **时间复杂度**：`O(m·n)` —— 需要遍历整个二维表。  
- **空间复杂度**：`O(m·n)` —— 存放整个 DP 表格。  
  > 对于本题的约束（`10⁵` 级别），这两项都不可接受。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **二维 DP**：它把两个长度都可能达到 10⁵ 的数组全部配对比较。  
观察题目可以发现：

1. `target` 中的元素**互不相同**（没有重复），这是一把重要的钥匙。  
2. 如果把 `target` 中每个数映射成它在 `target` 里的下标（位置），那么 `target` 本身就变成了 `[0, 1, 2, …]` 的递增序列。  
3. 对 `arr` 中的每个数，如果它也出现在 `target`，就把它替换成对应的下标；如果不在 `target`，直接丢掉（因为它对形成 `target` 子序列没有帮助）。

经过这一步，原问题等价于：

> 在一个只包含 `target` 下标的序列里，找出**最长严格递增子序列**（Longest Increasing Subsequence，LIS）的长度 `L`。  

因为下标的递增恰好保证了原数值的相对顺序与 `target` 完全一致。  

**最小插入次数 = len(target) - LIS长度**。

> **类比**：把 `target` 看成一本有序的字典（第 0 页、1 页、2 页…），`arr` 中出现的每个字典词都标记成它的页码。我们只关心这些页码的**递增顺序**，因为递增的页码恰好对应字典里顺序正确的词。

**如何在 O(n log n) 求 LIS**  
- 使用「**Patience Sorting（耐心排序）**」或「**二分查找维护尾数组**」的技巧。  
- 维护一个数组 `tails`，`tails[i]` 表示长度为 `i+1` 的递增子序列的最小可能结尾值。遍历序列时，用二分查找在 `tails` 中找到第一个 `≥ 当前值` 的位置并替换，若没有则追加到末尾。  
- `tails` 长度即为 LIS 长度。

**步骤概览**  

1. **构建哈希表** `pos`：`pos[value] = index in target`（相当于查字典，键是数值，值是页码）。  
2. **把 arr 转化为 index 序列** `seq`：遍历 `arr`，若元素在 `pos` 中则加入对应下标。  
3. **在 seq 上做 LIS**（二分+tails），得到 `L`.  
4. **答案** = `len(target) - L`.

#### 代码（Python）

```python
import bisect

def min_operations(target, arr):
    # 1. 哈希表：把 target 的每个数映射成它的下标（相当于查字典）
    pos = {num: idx for idx, num in enumerate(target)}   # O(len(target))

    # 2. 把 arr 中出现的、且在 target 里的数，转成对应的下标序列
    seq = []
    for num in arr:
        if num in pos:                     # 只保留有用的元素
            seq.append(pos[num])           # 用下标代替原数值

    # 3. 在 seq 上求最长严格递增子序列（LIS）
    tails = []                             # tails[i] 是长度为 i+1 的递增子序列的最小结尾
    for x in seq:
        # 二分查找：在 tails 中找第一个 >= x 的位置
        idx = bisect.bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)                # 没找到，说明可以把 x 加在末尾，长度加 1
        else:
            tails[idx] = x                 # 找到后用 x 替换，保持结尾尽可能小

    lis_len = len(tails)                   # LIS 的长度

    # 4. 最少插入次数 = 目标长度 - 已经可以保持顺序的最长子序列长度
    return len(target) - lis_len
```

> **代码说明**  
- `pos` 使用哈希表（字典），查询时间是 **O(1)**，就像在字典里查词一样快。  
- `bisect_left` 是 Python 标准库的二分查找实现，时间 **O(log k)**，其中 `k` 是当前 `tails` 长度。  
- 整体遍历 `arr` 只一次，整体复杂度是 **O(n log n)**（`n = len(arr)`）。

#### 复杂度

- **时间复杂度**：`O(m + n log n)`  
  - `m = len(target)`：构建哈希表。  
  - `n = len(arr)`：遍历并做二分查找。  
  - 对比暴力解的 `O(m·n)`，这里把指数级的配对全部砍掉，只剩 `log` 级别的查找，快得多。  

- **空间复杂度**：`O(m + L)`  
  - 哈希表占 `O(m)`，`tails` 最多保存 `L = LIS长度 ≤ m`。  
  - 只用了线性额外空间，远小于二维 DP 的 `O(m·n)`。

---

## 心得

- **核心技巧**：把「数组中出现的顺序」转化为「下标序列」后，再求 **最长递增子序列**（LIS）。  
- **适用场景**  
  1. 当一个序列的元素互不相同，另一序列可能有重复或不相关元素时（如本题）。  
  2. 「把两个序列的公共顺序转化为 LIS」的题目，如  
     - *"Longest Common Subsequence with Unique Elements"*  
     - *"Make Array Strictly Increasing"*（LeetCode 1840）  
  3. 任意需要在 **O(n log n)** 求解 LIS 的场景（比如「最长递增子序列」本身的变体）。  

- **一句话总结**：  
  > 把 `target` 当成「顺序指南」，把 `arr` 中能对应的元素映射成指南的页码，再在这些页码上找最长递增序列，缺的页码数就是最少插入次数。

---

## 反思

- **第一反应**：立刻想到 LCS，写出二维 DP。  
- **最容易踩的坑**  
  - 忘记 `target` 中的元素是唯一的，导致没有想到用哈希表映射下标。  
  - 在把 `arr` 转成下标序列时，误把不在 `target` 里的元素也加入，导致 LIS 计算错误。  
  - 实现 LIS 时使用 `bisect_right`（严格递增要用 `bisect_left`），会把相等的下标误当成可以延长的序列。  

- **下次遇到同类题**：  
  1. 先检查两条序列是否有「唯一性」或「映射」的可能。  
  2. 考虑把「相同元素的相对顺序」抽象成「下标序列」，然后求 LIS。  
  3. 用哈希表快速建立映射，再用二分维护 `tails` 完成 O(n log n) 求解。