# #1458. **最大点积子序列** / Max Dot Product of Two Subsequences

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/max-dot-product-of-two-subsequences/)

---

## 题目（英文原版）

**Description**

Given two arrays nums1 and nums2.
Return the maximum dot product between non-empty subsequences of nums1 and nums2 with the same length.
A subsequence of a array is a new array which is formed from the original array by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (ie, [2,3,5] is a subsequence of [1,2,3,4,5] while [1,5,3] is not).

**Examples**

**Example 1:**

```
Input: nums1 = [2,1,-2,5], nums2 = [3,0,-6]
Output: 18
Explanation: Take subsequence [2,-2] from nums1 and subsequence [3,-6] from nums2.
Their dot product is (2*3 + (-2)*(-6)) = 18.
```

**Example 2:**

```
Input: nums1 = [3,-2], nums2 = [2,-6,7]
Output: 21
Explanation: Take subsequence [3] from nums1 and subsequence [7] from nums2.
Their dot product is (3*7) = 21.
```

**Example 3:**

```
Input: nums1 = [-1,-1], nums2 = [1,1]
Output: -1
Explanation: Take subsequence [-1] from nums1 and subsequence [1] from nums2.
Their dot product is -1.
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 500
- -1000 <= nums1[i], nums2[i] <= 1000

---

## 题目（中文翻译）

给定两个数组 `nums1` 和 `nums2`。  
返回 `nums1` 与 `nums2` 中长度相同的非空子序列（subsequence）之间的最大点积（dot product）。

子序列（subsequence）是指在不改变剩余元素相对顺序的前提下，通过删除原数组中的若干（可以为零）元素而得到的新数组。（例如，`[2,3,5]` 是 `[1,2,3,4,5]` 的子序列，而 `[1,5,3]` 不是）。

**示例 1**  
**输入**: `nums1 = [2,1,-2,5]`, `nums2 = [3,0,-6]`  
**输出**: `18`  
**解释**: 取 `nums1` 的子序列 `[2,-2]` 与 `nums2` 的子序列 `[3,-6]`。  
它们的点积为 `2*3 + (-2)*(-6) = 18`。

**示例 2**  
**输入**: `nums1 = [3,-2]`, `nums2 = [2,-6,7]`  
**输出**: `21`  
**解释**: 取 `nums1` 的子序列 `[3]` 与 `nums2` 的子序列 `[7]`。  
它们的点积为 `3*7 = 21`。

**示例 3**  
**输入**: `nums1 = [-1,-1]`, `nums2 = [1,1]`  
**输出**: `-1`  
**解释**: 取 `nums1` 的子序列 `[-1]` 与 `nums2` 的子序列 `[1]`。  
它们的点积为 `-1`。

**约束条件**  
- `1 <= nums1.length, nums2.length <= 500`  
- `-1000 <= nums1[i], nums2[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的子序列** 都枚举出来，随后两两配对计算点积，取最大值。

- **子序列**：把原数组的若干元素（可以不删）保留下来，顺序不变。  
  想象一本书的章节目录，你可以挑选任意几章，但章节的先后顺序不能颠倒。  
- 对于长度为 `m` 的数组，非空子序列的数量是 `2^m - 1`（每个位置“保留”或“删除”，除去全删的情况）。  
- 暴力做法就是：

  1. 用二进制掩码遍历 `nums1` 的所有子序列，记为 `sub1`。  
  2. 用二进制掩码遍历 `nums2` 的所有子序列，记为 `sub2`。  
  3. 只保留 `len(sub1) == len(sub2)` 的配对，计算点积 `sum(a*b)`，更新最大值。

**为什么正确**  
因为我们把**所有**满足“同长度且非空”的子序列配对都尝试了一遍，最大值自然不会漏掉。

**时间/空间复杂度**  

- `nums1` 长度记作 `n`，`nums2` 长度记作 `m`。  
- 子序列数量分别是 `2^n-1`、`2^m-1`，配对后最坏情况是 `O(2^n * 2^m)`，再乘上点积的线性计算 `O(min(n,m))`。  
- 简单说就是 **指数级**，在本题的约束 (`n,m ≤ 500`) 下根本不可行。  
- 空间只需要存当前的子序列，最多 `O(n+m)`。

> **大白话**：  
> `O(2^n)` 就像把一棵有 `n` 层的二叉树遍历到底，层数多了，树的节点数会翻倍增长，几分钟就会变成几千年。

#### 代码（Python）

```python
from itertools import compress
from math import inf

def maxDotProduct_bruteforce(nums1, nums2):
    n, m = len(nums1), len(nums2)
    best = -inf                     # 先设为负无穷，防止全负数时出错

    # 遍历 nums1 的所有非空子序列
    for mask1 in range(1, 1 << n):                 # 1~2^n-1，二进制位表示保留/删除
        sub1 = [nums1[i] for i in range(n) if (mask1 >> i) & 1]

        # 遍历 nums2 的所有非空子序列
        for mask2 in range(1, 1 << m):
            sub2 = [nums2[j] for j in range(m) if (mask2 >> j) & 1]

            if len(sub1) != len(sub2):            # 只能配对等长的子序列
                continue

            # 计算点积
            dot = sum(a * b for a, b in zip(sub1, sub2))
            best = max(best, dot)

    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n * 2^m * min(n,m))` —— 指数级增长，几乎不可能在 500 长度的数组上跑完。  
- **空间复杂度**：`O(n + m)` —— 只存临时子序列，和输入规模线性相关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**重复计算**：我们在遍历子序列时，不断重新计算已经算过的子序列的点积，而且子序列之间有大量重叠。  
我们需要一种方法，**一步步把问题拆解成子问题**，并且只计算一次。  

这正是**动态规划（Dynamic Programming, DP）**的思路：  
- **状态**：`dp[i][j]` 表示“以 `nums1[i]` 为结尾、`nums2[j]` 为结尾的两个非空子序列的最大点积”。  
  换句话说，子序列的最后一个元素必须分别是 `nums1[i]` 和 `nums2[j]`。  
- **转移**：要让 `dp[i][j]` 成立，最后一步一定是把 `nums1[i]` 和 `nums2[j]` 配对相乘，然后把它加入到**之前的最佳配对**中。  
  之前的配对有三种可能：

  1. **继续延伸**：把 `nums1[i]` 与 `nums2[j]` 加到已经选好的子序列后面。此时前面的最大点积是 `dp[i-1][j-1]`（两者都向左移动一位），所以候选值为 `dp[i-1][j-1] + nums1[i]*nums2[j]`。
  2. **只取当前配对**：如果前面的点积为负，直接把负值丢掉，只保留当前这对乘积 `nums1[i]*nums2[j]`。这相当于“重新开始”一个长度为 1 的子序列。
  3. **不使用当前元素**：我们可以把 `nums1[i]` 或 `nums2[j]` 丢弃，只保留之前的最佳结果。对应的就是 `dp[i-1][j]`（丢掉 `nums1[i]`）或 `dp[i][j-1]`（丢掉 `nums2[j]`）。

  综合以上，转移方程为：

  ```
  dp[i][j] = max(
      nums1[i] * nums2[j],                         # 只取当前配对
      dp[i-1][j-1] + nums1[i] * nums2[j],          # 继续延伸
      dp[i-1][j],                                   # 丢掉 nums1[i]
      dp[i][j-1]                                    # 丢掉 nums2[j]
  )
  ```

- **初始化**：`dp[0][0] = nums1[0] * nums2[0]`。第一行或第一列只可能是“只取当前配对”或“丢掉”。因此：

  ```
  dp[i][0] = max(dp[i-1][0], nums1[i] * nums2[0])
  dp[0][j] = max(dp[0][j-1], nums1[0] * nums2[j])
  ```

- **答案**：遍历完整个表后，`dp[n-1][m-1]` 即为要求的最大点积。

**为什么有效**  
动态规划把“大问题”拆成“小问题”。每个 `dp[i][j]` 只依赖左上、上、左三个已经求好的格子，保证了不会重复计算。  
此外，考虑了“重新开始”的情况，能够处理全负数的数组（如示例 3），返回最大的负数而不是错误的 0。

**空间优化**  
因为转移只依赖当前行和前一行，我们可以用两行滚动数组把空间从 `O(n*m)` 降到 `O(m)`（取较短的数组做列）。这里仍保留完整二维写法，便于初学者理解。

#### 代码（Python）

```python
def maxDotProduct(nums1, nums2):
    n, m = len(nums1), len(nums2)

    # dp[i][j] 表示以 nums1[i]、nums2[j] 为结尾的子序列的最大点积
    dp = [[0] * m for _ in range(n)]

    # 初始化左上角
    dp[0][0] = nums1[0] * nums2[0]

    # 初始化第一行（只考虑 nums1[0] 与 nums2[0..j] 的配对）
    for j in range(1, m):
        dp[0][j] = max(dp[0][j-1], nums1[0] * nums2[j])

    # 初始化第一列（只考虑 nums2[0] 与 nums1[0..i] 的配对）
    for i in range(1, n):
        dp[i][0] = max(dp[i-1][0], nums1[i] * nums2[0])

    # 填表
    for i in range(1, n):
        for j in range(1, m):
            prod = nums1[i] * nums2[j]                     # 当前两个数的乘积
            # 四种选择取最大
            dp[i][j] = max(
                prod,                                      # 只取当前配对，重新开始
                dp[i-1][j-1] + prod,                       # 在前面的最佳基础上继续延伸
                dp[i-1][j],                                # 丢掉 nums1[i]
                dp[i][j-1]                                 # 丢掉 nums2[j]
            )
    # 整个表右下角即为答案
    return dp[n-1][m-1]
```

> **关键注释**  
> - `prod = nums1[i] * nums2[j]`：把两数配对的“点”。  
> - `dp[i-1][j-1] + prod`：把这颗“点”接在已有的最佳序列后面。  
> - `max(prod, …)`：如果之前的序列点积为负，直接把它们抛掉，重新从这颗点开始。

#### 复杂度

- **时间复杂度**：`O(n * m)` —— 只遍历一次二维表，`n,m ≤ 500`，最多 `250,000` 次运算，完全可接受。  
  > 与暴力的指数级 `O(2^n * 2^m)` 相比，简直是“从爬山到坐电梯”。  
- **空间复杂度**：`O(n * m)`（若使用滚动数组可降到 `O(min(n,m))`）。  
  对于 500×500 的表，约 `250,000` 个整数，几百 KB 的内存。

---

## 心得

- **核心技巧**：二维动态规划，状态定义为“以 i、j 为结尾的子序列的最大点积”。  
- **适用的题型**  
  1. **两个序列的最长公共子序列（LCS）** – 状态同样是 `dp[i][j]`，只不过转移是 “相等则加 1”。  
  2. **最大子数组乘积（Maximum Product Subarray）** – 只是一维 DP，考虑“继续乘”或“重新开始”。  
  3. **两个序列的最大相似度（如最长递增子序列的变形）** – 也是类似的二维 DP。
- **一句话总结解题钥匙**：**把“选或不选”拆成“保留当前配对、继续前缀、丢掉左/上”四种情况，取最大即可。**

---

## 反思

- **第一反应**：看到“子序列”和“点积”，立刻想到枚举子序列——这就是暴力思路。  
- **最容易踩的坑**  
  - 忽略了**全负数**的情况，直接把 `dp` 初始化为 `0` 会导致答案错误（应允许负数）。  
  - 忘记在转移时加入“只取当前配对”这一项，导致在所有前缀点积为负时无法重新开始。  
  - 边界条件（第一行/列）写错，会产生 `IndexError` 或错误的初始值。  
- **下次遇到同类题**：  
  1. 先明确“子序列必须保持相对顺序”，考虑 **二维 DP**。  
  2. 定义状态时把 **“是否必须使用当前位置”** 写进去（本题的 `dp[i][j]` 必须以 i、j 为结尾）。  
  3. 列举所有**转移可能**（继续、重新开始、丢弃），确保不遗漏。