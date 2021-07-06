# #1388. 3n 切披萨 / Pizza With 3n Slices

> 难度：困难 · 标签：Array、Dynamic Programming、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/pizza-with-3n-slices/)

---

## 题目（英文原版）

**Description**

There is a pizza with 3n slices of varying size, you and your friends will take slices of pizza as follows:
Given an integer array slices that represent the sizes of the pizza slices in a clockwise direction, return the maximum possible sum of slice sizes that you can pick.

**Examples**

**Example 1:**

```
Input: slices = [1,2,3,4,5,6]
Output: 10
Explanation: Pick pizza slice of size 4, Alice and Bob will pick slices with size 3 and 5 respectively. Then Pick slices with size 6, finally Alice and Bob will pick slice of size 2 and 1 respectively. Total = 4 + 6.
```

**Example 2:**

```
Input: slices = [8,9,8,6,1,1]
Output: 16
Explanation: Pick pizza slice of size 8 in each turn. If you pick slice with size 9 your partners will pick slices of size 8.
```

**Constraints**

- 3 * n == slices.length
- 1 <= slices.length <= 500
- 1 <= slices[i] <= 1000

---

## 题目（中文翻译）

描述  
有一块披萨被切成 **3n** 片，大小各不相同。你和你的朋友们将按照如下方式轮流取披萨片：  
给定一个 **整数数组**（integer array）`slices`，它表示披萨切片的大小，**顺时针方向**（clockwise direction）排列，返回你能够获得的切片大小之和的 **最大可能和**（maximum possible sum）。

示例 1  
**输入**: `slices = [1,2,3,4,5,6]`  
**输出**: `10`  
**解释**: 先取大小为 4 的切片，你的伙伴 Alice 和 Bob 分别取大小为 3 和 5 的切片。随后再取大小为 6 的切片，最后 Alice 和 Bob 分别取大小为 2 和 1 的切片。总和 = 4 + 6。

示例 2  
**输入**: `slices = [8,9,8,6,1,1]`  
**输出**: `16`  
**解释**: 每轮都取大小为 8 的切片。如果你取大小为 9 的切片，你的伙伴们将取大小为 8 的切片。

约束条件  
- `3 * n == slices.length`  
- `1 <= slices.length <= 500`  
- `1 <= slices[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**穷举所有合法的挑选方式**，然后挑出最大总和。  
- 这里的“合法”指的是：一共要挑 `n = len(slices)//3` 块，且任意两块不能相邻（因为相邻的两块会被你的两个朋友抢走）。  
- 为了判断相邻关系，我们可以把切片看成 **环形链表**，第 `0` 块的左邻居是最后一块，第 `len-1` 块的右邻居是第 `0` 块。  

实现时可以使用 **回溯（DFS）**：

1. 从第 `i` 块开始尝试是否选它。  
2. 如果选了，就把 `i`、`i+1`、`i-1`（环形下）这三块标记为“不可再选”。  
3. 继续递归到下一个还能选的下标。  
4. 当已经选了 `n` 块时，计算当前和，更新答案。

> **类比**：把 `slices` 当成一本字典，选词就像在字典里挑单词，挑了一个词后，前后相邻的词（上下文）就不能再挑了。我们要把所有可能的挑选方式（相当于所有可能的词组合）都列出来，再找出分值最大的那一个。

**为什么正确**：回溯遍历了**所有**满足“不相邻且正好选 n 块” 的组合，最大值必然在其中。

#### 代码（Python）

```python
from typing import List

def maxSizeSlices_bruteforce(slices: List[int]) -> int:
    m = len(slices)                 # 3 * n
    n = m // 3                      # 需要挑的块数
    best = 0                        # 记录最大和

    # 用一个长度为 m 的布尔数组标记哪些位置已经被占用（被自己选或被朋友抢）
    used = [False] * m

    def dfs(idx: int, taken: int, cur_sum: int) -> None:
        """从 idx 开始尝试，已经挑了 taken 块，当前总和为 cur_sum"""
        nonlocal best
        # 选够了 n 块，更新答案
        if taken == n:
            best = max(best, cur_sum)
            return
        # 已经遍历完所有位置，直接返回
        if idx >= m:
            return

        # 1）不选 idx，直接看下一个位置
        dfs(idx + 1, taken, cur_sum)

        # 2）尝试选 idx（前提是它没有被占用）
        if not used[idx]:
            # 选了 idx 后，环形下 idx、左邻 idx-1、右邻 idx+1 都不能再选
            left = (idx - 1) % m
            right = (idx + 1) % m
            # 暂时标记
            used[idx] = used[left] = used[right] = True
            dfs(idx + 1, taken + 1, cur_sum + slices[idx])
            # 恢复现场（回溯）
            used[idx] = used[left] = used[right] = False

    dfs(0, 0, 0)
    return best
```

> 代码里每一行都加了中文注释，帮助你跟上思路。  

#### 复杂度  

- **时间复杂度**：`O(3^n)`（指数级）  
  - 每一步最多有两种选择（选或不选），递归深度约为 `3n`，所以最坏情况是 `2^{3n}`，但因为相邻的块会被一起禁用，实际搜索树的分支更接近 `3^n`。  
  - 用大白话说，就是**随着切片数增多，计算时间会爆炸**，在 `len=30`（n=10）左右就已经不可接受了。  

- **空间复杂度**：`O(3n)`（递归栈 + used 数组）  
  - 递归深度最多 `3n`，`used` 数组占 `3n` 的空间。  

> 暴力解只能在非常小的测试数据上跑通，主要用于帮助我们**理解题目约束**，并为后面的优化提供基准。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有组合**。我们要找一种方式，只在**局部信息**上做决定，却仍能保证全局最优。  
观察题目提示可以把环形问题转化为线性问题：

> **等价转换**：在长度为 `3n` 的环形数组中挑 `n` 个不相邻的数，等价于**在长度为 `3n‑1` 的线性数组中挑 `n` 个不相邻的数**，只要我们**排除掉首尾同时被选的情况**。  
> 具体做法是分两种情况分别求解：
> 1. **不选第 0 块** → 只在子数组 `slices[1:]`（长度 `3n‑1`）中挑 `n` 块。
> 2. **不选最后一块** → 只在子数组 `slices[:-1]`（长度 `3n‑1`）中挑 `n` 块。  
> 两种情况的最大值即为答案。

于是我们把**环形**问题变成了**两次线性 DP**。  
下面来设计线性 DP：

- 设 `dp[i][j]` 为**考虑前 i 块（下标 0..i‑1）**，**恰好挑了 j 块**，且不相邻时能得到的**最大总和**。  
- 状态转移：
  - **不选第 i‑1 块**：`dp[i][j] = dp[i-1][j]`
  - **选第 i‑1 块**：由于相邻不能选，前一块（i‑2）必须被跳过，所以我们从 `dp[i-2][j-1]` 转移，并加上当前切片的大小 `slices[i-1]`  
    `dp[i][j] = max(dp[i][j], dp[i-2][j-1] + slices[i-1])`
- 初始化：
  - `dp[0][0] = 0`（什么也不选，和为 0），其余为负无穷（表示不可达）。
  - 为了防止访问负索引，`dp[-1][*]` 也视作 0（只在实现时做特殊处理）。
- 最终答案为 `dp[m][n]`，其中 `m = len(subarray)`（等于 `3n‑1`），`n = original_n`。

**空间优化**：观察转移只依赖 `i-1` 与 `i-2` 两行，可以用 **滚动数组** 把空间降到 `O(n)`。

> **类比**：把 `dp[i][j]` 想象成“在第 i 条路口，你已经买了 j 张票，能省下最多多少钱”。不买票就保持原状，买票必须跳过前一个路口（因为相邻不能买），于是只能从前前一个路口的状态转移过来。

#### 代码（Python）

```python
from typing import List

def maxSizeSlices(slices: List[int]) -> int:
    """
    主函数：返回在环形切片数组中挑 n 块（n = len(slices)//3）且不相邻的最大总和。
    思路：分两次线性 DP（不选第一个 / 不选最后一个），取最大值。
    """
    n = len(slices) // 3                     # 必须挑的块数
    # 线性 DP：在数组 arr 中挑 n 块，且不相邻，返回最大和
    def linear_dp(arr: List[int]) -> int:
        m = len(arr)                         # = 3n-1
        # dp[j] 表示在当前遍历到的位置，挑了 j 块的最大和
        # 为了使用 dp[i-2]，我们需要保留前两轮的 dp，使用两层滚动数组
        dp_prev = [0] + [-10**9] * n         # 对应 i-1（初始 i=0 时）
        dp_prev2 = [0] + [-10**9] * n        # 对应 i-2（i<2 时均视为全 0）

        for i in range(1, m + 1):            # i 表示已考虑前 i 块（1‑based）
            cur = [0] + [-10**9] * n         # 本轮的 dp
            # 不选第 i-1 块：直接沿用 dp_prev
            for j in range(0, n + 1):
                cur[j] = dp_prev[j]          # 不选

            # 选第 i-1 块：只能在 i-2 时已经挑了 j-1 块的状态上加当前值
            for j in range(1, n + 1):
                # dp_prev2[j-1] 代表“到 i-2 为止挑了 j-1 块的最大和”
                cur[j] = max(cur[j], dp_prev2[j-1] + arr[i-1])

            # 滚动：把 dp_prev2←dp_prev，dp_prev←cur，准备下一轮
            dp_prev2, dp_prev = dp_prev, cur

        return dp_prev[n]                    # 最终挑 n 块的最大和

    # 情形一：不选第 0 块 → 在 slices[1:] 上做 DP
    ans1 = linear_dp(slices[1:])
    # 情形二：不选最后一块 → 在 slices[:-1] 上做 DP
    ans2 = linear_dp(slices[:-1])
    return max(ans1, ans2)
```

> 代码中每一步都有中文注释，帮助你一步步跟踪 DP 表的变化。  

#### 复杂度  

- **时间复杂度**：`O( (3n) * n ) = O(n^2)`  
  - 外层循环遍历 `3n-1`（≈ `3n`）个切片，内层循环最多遍历 `n` 次（挑的块数）。  
  - 用大白话说：**随着切片数线性增长，计算时间会呈二次方增长**，在本题最大 `len=500`（即 `n≈166`）时也只需要几万次操作，完全可以接受。  

- **空间复杂度**：`O(n)`  
  - 只保留了两行 DP（`dp_prev`、`dp_prev2`）以及当前行 `cur`，每行大小为 `n+1`。  
  - 与暴力解相比，**只需要几百个整数的空间**，几乎可以忽略不计。

> 与暴力解相比，时间从指数级下降到平方级，空间也从 `O(3n)`（递归栈）降到 `O(n)`，这是一次质的飞跃。

---

## 心得

- **核心技巧**：把环形 “不相邻选 N 个” 转化为**两个线性 DP**（排除首尾同选的冲突），并使用**滚动数组**实现空间压缩。  
- **适用的题型**：
  1. **环形选择类**：如 “环形摆放的灯泡最大亮度” 需要挑不相邻的灯泡。  
  2. **在数组中挑不相邻的 k 个元素**：如 “Maximum Sum of k Non‑Adjacent Elements”。  
  3. **分段选择 DP**：如 “把数组分成若干段，每段选一个元素，使和最大”。  

- **一句话总结**：**把环形约束拆成“不能同时选首尾”两种线性子问题，利用 DP 把“不相邻”转化为“跳过前一个”。**

---

## 反思

- **第一反应**：看到 “3n 切片，挑 n 块且相邻会被抢” 立刻想到**穷举**或**递归回溯**。  
- **最容易踩的坑**  
  1. **环形相邻**：第 0 块与最后一块是相邻的，直接使用线性 DP 会遗漏这种冲突。  
  2. **边界条件**：`dp[i-2]` 当 `i=1` 时不存在，需要额外处理（可以把 `dp[-1]` 视为全 0）。  
  3. **负无穷初始化**：如果用 `-inf` 初始化而不注意加法，会导致溢出或错误的比较。  
- **下次遇到同类题**，第一步应该**思考是否可以把环形或循环约束拆解成若干线性子问题**，再考虑使用**动态规划**或**贪心**在每个子问题上求最优。这样往往能把指数级的搜索直接降到多项式时间。