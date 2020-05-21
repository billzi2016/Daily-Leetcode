# #873. 最长斐波那契子序列的长度 / Length of Longest Fibonacci Subsequence

> 难度：中等 · 标签：Array、Hash Table、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/length-of-longest-fibonacci-subsequence/)

---

## 题目（英文原版）

**Description**

A sequence x1, x2, ..., xn is Fibonacci-like if:
Given a strictly increasing array arr of positive integers forming a sequence, return the length of the longest Fibonacci-like subsequence of arr. If one does not exist, return 0.
A subsequence is derived from another sequence arr by deleting any number of elements (including none) from arr, without changing the order of the remaining elements. For example, [3, 5, 8] is a subsequence of [3, 4, 5, 6, 7, 8].

**Examples**

**Example 1:**

```
Input: arr = [1,2,3,4,5,6,7,8]
Output: 5
Explanation: The longest subsequence that is fibonacci-like: [1,2,3,5,8].
```

**Example 2:**

```
Input: arr = [1,3,7,11,12,14,18]
Output: 3
Explanation: The longest subsequence that is fibonacci-like: [1,11,12], [3,11,14] or [7,11,18].
```

**Constraints**

- 3 <= arr.length <= 1000
- 1 <= arr[i] < arr[i + 1] <= 109

---

## 题目（中文翻译）

如果一个序列 `x₁, x₂, …, xₙ` 满足对所有 `i ≥ 3` 都有 `xᵢ = xᵢ₋₁ + xᵢ₋₂`，则称其为斐波那契（Fibonacci）类序列。

给定一个 **严格递增数组（strictly increasing array）** `arr`，其中所有元素为 **正整数（positive integers）**，返回 `arr` 中最长的斐波那契类 **子序列（subsequence）** 的长度。如果不存在此类子序列，返回 `0`。

**子序列（subsequence）** 是指在保持剩余元素相对顺序不变的前提下，从原序列 `arr` 中删除任意数量（可以为零）的元素后得到的序列。例如，`[3, 5, 8]` 是 `[3, 4, 5, 6, 7, 8]` 的子序列。

### 示例

**示例 1**

```text
Input: arr = [1,2,3,4,5,6,7,8]
Output: 5
Explanation: 最长的斐波那契类子序列为 [1,2,3,5,8]。
```

**示例 2**

```text
Input: arr = [1,3,7,11,12,14,18]
Output: 3
Explanation: 最长的斐波那契类子序列可以是 [1,11,12]、[3,11,14] 或 [7,11,18] 中的任意一个。
```

### 约束条件

- `3 <= arr.length <= 1000`
- `1 <= arr[i] < arr[i + 1] <= 10⁹`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把数组 `arr` 中的每一种可能的 **子序列**（保持顺序但可以删掉元素）都枚举出来，检查它是不是 Fibonacci‑like（前两个数相加等于后一个数），如果是就记录它的长度，最后取最大值。

- **子序列**的枚举可以用递归或位掩码实现。  
- 判断一个序列是否满足 Fibonacci 条件，只需要从前往后检查 `seq[k] = seq[k‑1] + seq[k‑2]`。  

> **类比**：把数组想成一本书的章节，暴力解相当于把每一种“挑选章节的方式”（即每一种子序列）都列出来，再一本一本地翻，看哪本符合“每一章的页码等于前两章页码之和”的规则。

这个方法必然能找到最长的合法子序列，因为它遍历了**所有**可能的子序列。

#### 代码（Python）

```python
from itertools import combinations

def len_longest_fib_bruteforce(arr):
    n = len(arr)
    best = 0

    # 只枚举长度 >= 3 的子序列，因为 Fibonacci 序列至少要 3 项
    for l in range(3, n + 1):
        # combinations 会返回所有下标的组合，保持原序不变
        for idxs in combinations(range(n), l):
            seq = [arr[i] for i in idxs]

            # 检查是否满足 Fibonacci 条件
            ok = True
            for k in range(2, l):
                if seq[k] != seq[k - 1] + seq[k - 2]:
                    ok = False
                    break
            if ok:
                best = max(best, l)

    return best
```

> **关键行注释**  
> - `combinations(range(n), l)`：像在“图书目录”里挑选 `l` 本书，顺序不变。  
> - `seq[k] != seq[k-1] + seq[k-2]`：检查 “第 k 本书的页码是否等于前两本的页码之和”。  

#### 复杂度  

- **时间复杂度**：  
  - 组合数 `C(n, l)` 随 `l` 的增大而急剧上升，所有长度的组合总和是 `2^n`（每个元素保留或删除），再乘上每个子序列内部的线性检查 `O(l)`，整体是 **O(2ⁿ·n)**。  
  - 用大白话说，就是“几乎要把所有可能的子序列都翻一遍”，指数级增长，几分钟内就会超时。

- **空间复杂度**：  
  - 只保存当前枚举的子序列，最多 `O(n)`（最长子序列的长度），所以是 **O(n)**。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **“枚举所有子序列”**。我们其实不需要把序列全部列出来，只要**把每一对结尾的元素**视作 Fibonacci 序列的最后两项，就能递推出更长的序列。

核心观察：

1. 对于任意 `i > j`，如果我们知道有一个 Fibonacci‑like 子序列以 `arr[j] , arr[i]` 为最后两项，那么它的前一项必然是 `arr[i] - arr[j]`（因为 `x + y = z` ⇒ `x = z - y`）。  
2. 只要在数组里找得到这个前一项，就能把序列长度加 1。  
3. 为了**快速判断**某个数是否在数组中、以及它的下标是什么，我们可以把数组建成 **哈希表**（字典），键是数值，值是下标。查找的时间是 O(1)，相当于在字典里“查字典”，key 是词，value 是页码。

基于以上，我们可以用 **动态规划**：

- `dp[i][j]` 表示以 `arr[i]`（倒数第二个）和 `arr[j]`（最后一个）结尾的最长 Fibonacci‑like 子序列的长度。  
- 初始化时所有 `dp[i][j] = 2`（只包含这两项，长度 2 还不足以算合法序列）。  
- 对每一对 `(i, j)`（`i < j`），计算 `prev = arr[j] - arr[i]`。如果 `prev` 在数组中且对应的下标 `k < i`，则可以把 `arr[k], arr[i], arr[j]` 接在一起：  
  `dp[i][j] = dp[k][i] + 1`。  
- 在遍历过程中记录全局最大值 `ans`。最后如果 `ans` 小于 3，说明不存在合法序列，返回 0；否则返回 `ans`。

> **类比**：把每个数想成一本书的页码。我们想把两本书 `i, j` 组合成一本 “三部曲”。先查找能否找到一本前作 `k`，使得 `页码_k + 页码_i = 页码_j`。如果能，就把这三本连起来，继续往后找下一个能接上的前作。用字典查找就像在图书馆的目录里快速定位书的位置。

#### 代码（Python）

```python
def len_longest_fib(arr):
    """
    返回 arr 中最长的 Fibonacci-like 子序列的长度，若不存在返回 0。
    """
    n = len(arr)
    index = {x: i for i, x in enumerate(arr)}   # 哈希表：值 -> 下标
    dp = [[2] * n for _ in range(n)]            # dp[i][j] 初始为 2
    ans = 0

    # 枚举后两位的下标 (i, j)，i < j
    for j in range(n):
        for i in range(j):
            prev = arr[j] - arr[i]               # 期待的前一位数值
            # 必须保证 prev < arr[i]（因为数组严格递增）且在哈希表中
            if prev < arr[i] and prev in index:
                k = index[prev]                  # 前一位的下标
                dp[i][j] = dp[k][i] + 1          # 把长度延伸
                ans = max(ans, dp[i][j])         # 更新全局最大

    return ans if ans >= 3 else 0
```

> **关键行注释**  
> - `index = {x: i for i, x in enumerate(arr)}`：把数组变成“查字典”，`x` 是词，`i` 是页码。  
> - `prev = arr[j] - arr[i]`：从 “后两位” 反推出应该的前一位。  
> - `if prev < arr[i] and prev in index:`：确保前一位在数组左边（因为递增），并且真的存在。  
> - `dp[i][j] = dp[k][i] + 1`：把已经得到的以 `k,i` 结尾的序列再加上 `j`，长度加 1。  

#### 复杂度  

- **时间复杂度**：  
  - 两层循环遍历所有 `(i, j)`，共 `O(n²)` 次。  
  - 每次循环里只做 O(1) 的哈希表查找和常数操作。  
  - 因此整体是 **O(n²)**，对 `n ≤ 1000` 完全可接受。  
  - 用大白话说：我们只看每两个位置的组合，一共几千次，而不是指数级的天文数字。

- **空间复杂度**：  
  - 哈希表占 `O(n)`，`dp` 矩阵占 `O(n²)`。  
  - 所以总共是 **O(n²)** 的额外空间。若只需要返回长度，也可以把 `dp` 换成字典压缩空间，但这里保持二维数组便于理解。

---

## 心得  

- **核心技巧**：利用哈希表把“是否存在某个数”转化为 O(1) 查找，再用动态规划把每对结尾的最长长度递推出去。  
- **适用的题型**  
  1. “最长等差子序列” – 也可以用类似的 `dp[j][i] = dp[i][k] + 1` 思路。  
  2. “最长递增子序列（LIS）” – 采用 `dp[i] = max(dp[j] + 1)` 的方式。  
  3. “最长同构数列” – 需要把前后关系转化为哈希查找。  
- **一句话总结解题钥匙**：**把“前两项之和等于后项”反向写成 “后项减前项”，用哈希表快速定位前项，再用 DP 累加长度**。

---

## 反思  

- **第一反应**：直接把所有子序列枚举出来检查，想到暴力法。  
- **最容易踩的坑**  
  - 忘记数组是严格递增的，导致 `prev` 可能出现在右边，需要额外判断 `prev < arr[i]`。  
  - DP 初始值设为 2（仅两项），否则会把不存在的序列误算成更长。  
  - 当最长长度小于 3 时，需要返回 0 而不是 2。  
- **下次类似题的第一步**：先思考“能否把关系反向”并用哈希表快速定位缺失的前驱，然后在此基础上设计 DP 或双指针的递推式。