# #1043. 最大化分割后数组和 / Partition Array for Maximum Sum

> 难度：中等 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/partition-array-for-maximum-sum/)

---

## 题目（英文原版）

**Description**

Given an integer array arr, partition the array into (contiguous) subarrays of length at most k. After partitioning, each subarray has their values changed to become the maximum value of that subarray.
Return the largest sum of the given array after partitioning. Test cases are generated so that the answer fits in a 32-bit integer.

**Examples**

**Example 1:**

```
Input: arr = [1,15,7,9,2,5,10], k = 3
Output: 84
Explanation: arr becomes [15,15,15,9,10,10,10]
```

**Example 2:**

```
Input: arr = [1,4,1,5,7,3,6,1,9,9,3], k = 4
Output: 83
```

**Example 3:**

```
Input: arr = [1], k = 1
Output: 1
```

**Constraints**

- 1 <= arr.length <= 500
- 0 <= arr[i] <= 109
- 1 <= k <= arr.length

---

## 题目（中文翻译）

给定一个整数数组 `arr`，将数组划分为长度至多为 `k` 的 **连续子数组**（subarray）。划分完成后，每个子数组中的所有元素都被替换为该子数组的最大值。  
返回对数组进行上述划分后能够得到的最大总和。题目保证所有测试用例的答案均能装入 32 位整数。

## 示例

### 示例 1
**输入**  
```
arr = [1,15,7,9,2,5,10], k = 3
```
**输出**  
```
84
```
**解释**  
数组被划分后变为 `[15,15,15,9,10,10,10]`，其元素和为 84。

### 示例 2
**输入**  
```
arr = [1,4,1,5,7,3,6,1,9,9,3], k = 4
```
**输出**  
```
83
```

### 示例 3
**输入**  
```
arr = [1], k = 1
```
**输出**  
```
1
```

## 约束条件
- `1 <= arr.length <= 500`
- `0 <= arr[i] <= 10^9`
- `1 <= k <= arr.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的分段方式枚举一遍**，然后算出每种分法对应的数组和，取最大值。  
- **枚举方式**：从左到右依次决定每段的长度，长度只能是 `1 … k` 中的一个。  
- **数据结构**：只需要一个普通的 Python `list` 来保存当前的分段长度序列，类似我们在生活中把一段路程拆成若干段走，每段可以走 1、2 … k 步。  

为什么这样一定能得到正确答案？因为我们把**所有合法的分段方案**都遍历到了，最大和必然出现在其中的某一个方案里。

> 这里可以把「所有方案」想象成「所有可能的拼图方式」，只要把每一种拼法都试一次，就一定能找到最好的那块。

#### 代码（Python）

```python
from typing import List

def maxSumAfterPartitioning_bruteforce(arr: List[int], k: int) -> int:
    n = len(arr)
    best = 0                     # 保存全局最大和

    # dfs(idx, cur_sum) 递归遍历从 idx 开始的子数组的所有分段方式
    def dfs(idx: int, cur_sum: int) -> None:
        nonlocal best
        if idx == n:              # 已经走到数组末尾，更新答案
            best = max(best, cur_sum)
            return

        cur_max = 0               # 当前这段的最大值
        # 尝试把长度为 1~k 的段放在当前位置
        for length in range(1, k + 1):
            if idx + length > n:  # 超出数组范围，停止扩展
                break
            # 更新这段的最大值
            cur_max = max(cur_max, arr[idx + length - 1])
            # 这段贡献：最大值 * 长度
            added = cur_max * length
            # 继续递归处理后面的子数组
            dfs(idx + length, cur_sum + added)

    dfs(0, 0)
    return best
```

> 关键点解释  
> - `dfs` 用递归模拟「从左到右」一次一次决定段的长度。  
> - `cur_max` 维护当前这段里出现的最大元素，类似在纸上写下「这段里最大的数字」随时更新。  
> - `added = cur_max * length` 正是题目要求的「把段里所有数字都改成最大值」后贡献的和。

#### 复杂度  

- **时间复杂度**：`O(k^n)`（指数级）  
  - 每个位置我们最多有 `k` 种选择，深度为 `n`，所以最坏情况是 `k` 的 `n` 次方。  
  - 用大白话说，就是「如果你把每一步都当成一次“掷骰子”，骰子有 `k` 面，掷 `n` 次，所有可能的组合数就是 `kⁿ`」——会非常慢。

- **空间复杂度**：`O(n)`（递归栈）  
  - 递归深度最多为 `n`，每层保存一些局部变量，整体是线性的。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量的重复计算**。例如，当我们已经决定了前面 `i` 个元素的最优划分后，后面的计算并不需要重新遍历所有可能的前缀，只需要考虑「最后一段」的长度即可。

**核心想法 → 动态规划（Dynamic Programming）**  
设 `dp[i]` 表示**前 `i` 个元素（下标 `0 … i-1`）的最大和**。我们要找的是 `dp[n]`，其中 `n = len(arr)`。

从左到右填表：

- 对于当前位置 `i`（1‑based，方便写公式），我们可以把最后一段的长度设为 `j`（`1 ≤ j ≤ k`），只要 `i-j ≥ 0`。  
- 这段的元素是 `arr[i-j] … arr[i-1]`，它们会全部被改成这段的最大值 `max(arr[i-j … i-1])`。  
- 那么这段贡献的和是 `max * j`。  
- 前面已经划分好的最优和是 `dp[i-j]`。  
- 所以一种可能的总和是 `dp[i-j] + max * j`，我们在所有合法的 `j` 中取最大值，即：

```
dp[i] = max_{1 ≤ j ≤ k, i-j ≥ 0} ( dp[i-j] + max(arr[i-j … i-1]) * j )
```

这就是提示里给出的递推式。**只要把 `max(arr[i-j … i-1])` 在遍历 `j` 的过程中实时维护，就能在 O(k) 时间内算出 `dp[i]`**。

> 类比：想象你在排队买票，前面已经有若干人排好（`dp[i-j]`），你自己可以一次买 `j` 张票（`j` 长度的段），而票价是这几张票里最贵的那张乘以数量（`max * j`）。你要决定买几张票才能让整体花费最少（这里是最大化总和），于是枚举 `j` 找最优。

#### 代码（Python）

```python
from typing import List

def maxSumAfterPartitioning(arr: List[int], k: int) -> int:
    n = len(arr)
    dp = [0] * (n + 1)           # dp[0] = 0，空数组的最大和为 0

    for i in range(1, n + 1):    # 计算 dp[1] … dp[n]
        cur_max = 0              # 用来记录当前考虑的段的最大值
        # 枚举最后一段的长度 j，最多 k，且不能超过 i
        for j in range(1, min(k, i) + 1):
            cur_max = max(cur_max, arr[i - j])   # 更新段内最大值
            # dp[i-j] 为前面部分的最优和，cur_max*j 为本段贡献
            dp[i] = max(dp[i], dp[i - j] + cur_max * j)

    return dp[n]
```

> 关键行解释  
> - `cur_max = max(cur_max, arr[i - j])`：在遍历不同长度 `j` 时，只需要把新加入的左侧元素与当前最大值比较，就得到整段的最大值。相当于「把新来的水果和篮子里最大的水果比大小」来保持最大值。  
> - `dp[i] = max(dp[i], dp[i - j] + cur_max * j)`：把「前面已经划分好的最优和」和「本段的贡献」相加，取最大。

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - 外层遍历 `i = 1 … n`，内层最多枚举 `k` 种长度。  
  - 用大白话说，就是「我们只需要看每个位置前面最多 `k` 步的情况」，所以时间是线性乘以 `k`，在本题的约束（`n ≤ 500`）下非常快。

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n+1` 的数组 `dp` 来保存子问题的答案。  
  - 相比暴力解的递归栈，这里是显式的、可控的线性空间。

---

## 心得

- **核心技巧**：**动态规划 + 滑动窗口维护最大值**。  
- **适用的题型**  
  1. “分段取最大/最小/和” 类问题，如 *Partition Array for Maximum Sum*、*Divide Array in Sets of K Consecutive Numbers*（需要分段处理）。  
  2. “在区间内做某种统一操作后求最优” 的 DP，如 *Maximum Sum of a Subarray with At Most K Distinct Elements*。  
- **一句话总结解题钥匙**：**把“最后一段的长度”当作决策点，只需枚举 k 种可能并维护段内最大值，即可把指数爆炸的搜索压缩到 O(n·k)。**

---

## 反思

- **第一反应**：看到“把子数组改成最大值”，自然想到“枚举所有分段”。这会导致指数级时间，需要进一步思考如何复用子问题的答案。  
- **最容易踩的坑**  
  - **边界条件**：`i-j` 可能为 `0`，所以 `dp[0]` 必须初始化为 `0`；`j` 不能超过 `i`，否则会访问负索引。  
  - **最大值的更新**：在枚举不同 `j` 时，必须在同一个循环里实时更新 `cur_max`，否则会重复遍历导致 O(k²) 的额外开销。  
  - **整数溢出**：本题答案保证在 32 位整数范围，但在 Python 中不必担心。若换成 C/C++，要注意使用 `long long`。  
- **下次遇到同类题**：第一步先**思考“最后一步/最后一段”是什么，尝试写出 `dp[i]` 与 `dp[i-j]` 的关系，再检查是否可以在 O(k) 内维护必要的额外信息（如最大值、最小值、前缀和等）。这样可以快速定位到 DP 状态转移式，避免盲目暴力枚举。