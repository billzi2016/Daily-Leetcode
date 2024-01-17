# #2551. 把弹珠放入袋子 / Put Marbles in Bags

> 难度：困难 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/put-marbles-in-bags/)

---

## 题目（英文原版）

**Description**

You have k bags. You are given a 0-indexed integer array weights where weights[i] is the weight of the ith marble. You are also given the integer k.
Divide the marbles into the k bags according to the following rules:
The score after distributing the marbles is the sum of the costs of all the k bags.
Return the difference between the maximum and minimum scores among marble distributions.

**Examples**

**Example 1:**

```
Input: weights = [1,3,5,1], k = 2
Output: 4
Explanation: 
The distribution [1],[3,5,1] results in the minimal score of (1+1) + (3+1) = 6. 
The distribution [1,3],[5,1], results in the maximal score of (1+3) + (5+1) = 10. 
Thus, we return their difference 10 - 6 = 4.
```

**Example 2:**

```
Input: weights = [1, 3], k = 2
Output: 0
Explanation: The only distribution possible is [1],[3]. 
Since both the maximal and minimal score are the same, we return 0.
```

**Constraints**

- 1 <= k <= weights.length <= 105
- 1 <= weights[i] <= 109

---

## 题目（中文翻译）

你有 `k` 个袋子。给定一个下标从 0 开始的整数数组 `weights`，其中 `weights[i]` 表示第 `i` 颗弹珠的重量。同时给定整数 `k`。  
按照以下规则将所有弹珠分配到 `k` 个袋子中：

- 每个袋子必须至少包含一颗弹珠。  
- 每个袋子的成本（cost）等于该袋子中弹珠重量的最大值与最小值之和。  
- 所有袋子的成本之和即为本次分配的得分（score）。  

返回所有可能的分配方案中，最大得分与最小得分之差。

**示例 1**  
输入: `weights = [1,3,5,1]`, `k = 2`  
输出: `4`  
解释:  
- 分配 `[1] , [3,5,1]` 的得分最小，为 `(1+1) + (3+1) = 6`。  
- 分配 `[1,3] , [5,1]` 的得分最大，为 `(1+3) + (5+1) = 10`。  
- 因此返回它们的差值 `10 - 6 = 4`。

**示例 2**  
输入: `weights = [1, 3]`, `k = 2`  
输出: `0`  
解释: 唯一的分配方式是 `[1] , [3]`。  
由于最大得分与最小得分相同，返回 `0`。

**约束条件**  
- `1 <= k <= weights.length <= 10^5`  
- `1 <= weights[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的划分** 都枚举一遍，然后把每一种划分算出得分，取最大值和最小值的差。  

- **数据结构**：我们可以用递归或回溯把 `weights` 按顺序切成 `k` 段，每段就是一个袋子。  
- **为什么正确**：只要把所有合法的划分都遍历到，必然能找到得分最高和最低的两种情况，差值自然就是答案。  
- **复杂度分析**：  
  - 把 `n`（`weights` 长度）个元素切成 `k` 段，需要在 `n‑1` 条可能的切分点里选 `k‑1` 条。组合数记作 `C(n‑1, k‑1)`，它的增长速度非常快（指数级）。  
  - 每一种划分都要遍历一次数组求每个袋子的 `first+last`，时间是 `O(n)`。  
  - 所以总时间是 `O( C(n‑1, k‑1) * n )`，在最坏情况下几乎是 `O(2^n)`，根本不可接受。  
  - 空间上只需要递归栈深度 `O(k)`，其余都是原数组，记作 `O(k)`。

> **大白话**：如果把 `n` 看成 20，`C(19,9)` 已经是 92 378，乘上 20 也有近两百万次操作；`n` 再大一点，计算量就会像坐火箭一样飞快飙升。

#### 代码（Python）

```python
from typing import List

def brute(weights: List[int], k: int) -> int:
    n = len(weights)
    ans_max = -float('inf')
    ans_min = float('inf')

    # 递归枚举所有切分点
    def dfs(pos: int, bags: List[List[int]]):
        """pos 为下一个要放入的 marble 的下标，bags 已经形成的袋子列表"""
        nonlocal ans_max, ans_min
        if len(bags) == k:                 # 已经划分出 k 个袋子
            if pos == n:                    # 正好用了完所有 marble
                score = sum(b[0] + b[-1] for b in bags)   # 每个袋子只算首尾
                ans_max = max(ans_max, score)
                ans_min = min(ans_min, score)
            return
        # 继续往当前最后一个袋子里放，或者新开一个袋子
        if not bags:                        # 第一个袋子还没创建
            dfs(pos + 1, [[weights[pos]]])
        else:
            # 1) 把当前 marble 加到最后一个袋子
            bags[-1].append(weights[pos])
            dfs(pos + 1, bags)
            bags[-1].pop()                 # 回溯

            # 2) 开新袋子（只能在已有袋子数 < k 且不是最后一个 marble 时）
            if len(bags) < k and pos < n - 1:
                dfs(pos + 1, bags + [[weights[pos]]])

    dfs(0, [])
    return ans_max - ans_min
```

> 这段代码只能在 `n ≤ 15` 左右的小数据上跑得通，足以演示“最笨的想法”。

#### 复杂度

- **时间复杂度**：`O( C(n‑1, k‑1) * n )`，组合数随 `n` 指数增长，几乎不可用。  
- **空间复杂度**：`O(k)`（递归栈 + 当前构造的袋子），其余都是原数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正决定得分的只有每个袋子的首尾**。  
把 `weights` 看成一条线段：

```
w0  w1  w2  w3 ... wn-2  wn-1
```

如果我们把第 `i`（`0 ≤ i < n‑1`）条相邻的两颗弹珠 `weights[i]` 与 `weights[i+1]` **切开**，那么这条切线会让两个相邻袋子的 **首尾** 都出现一次：

- 左边袋子以 `weights[i]` 为结尾（它的 “last”），
- 右边袋子以 `weights[i+1]` 为开头（它的 “first”）。

所以 **每一次切分都会把 `weights[i] + weights[i+1]` 加入总得分**。  
如果我们一开始把所有弹珠放进同一个袋子，得分就是：

```
first + last = weights[0] + weights[-1]
```

随后每切一次，就 **额外加上** `weights[i] + weights[i+1]`（对应的切点）。  
因为要把 `n` 个弹珠分成 `k` 袋子，**恰好需要切 `k‑1` 次**。

> **关键观察**  
> 只要知道在 `n‑1` 条相邻边中挑哪 `k‑1` 条作为切点，就能唯一确定得分。  
> 得分 = `weights[0] + weights[-1] + Σ (weights[i] + weights[i+1])`（对所有被选的切点 i）

于是问题转化为：

- **最小得分**：在所有相邻和 `s_i = weights[i] + weights[i+1]` 中，挑 **最小的 `k‑1` 个** 加进去。  
- **最大得分**：挑 **最大的 `k‑1` 个**。

这一步只涉及 **排序** 或 **堆**（优先队列），不需要任何复杂的 DP。

**为什么贪心成立？**  
因为每个切点的贡献是 **独立** 的：选不选这条边，只会决定是否把对应的 `s_i` 加到总和里，互不影响。要让总和尽可能大（或小），自然把最大的（或最小的）若干个加进去即可。

#### 代码（Python）

```python
from typing import List

def put_marbles(weights: List[int], k: int) -> int:
    """
    返回把弹珠分成 k 包后，最大得分与最小得分的差值。
    思路：先算相邻两颗弹珠的和，然后挑 k-1 个最大/最小的加到基准得分上。
    """
    n = len(weights)
    if k == 1:                # 不需要切，得分唯一
        return 0

    # 1) 计算所有相邻和 s_i = weights[i] + weights[i+1]
    adj_sums = [weights[i] + weights[i + 1] for i in range(n - 1)]

    # 2) 基准得分：只剩下一个袋子时，只会计首尾两颗弹珠
    base = weights[0] + weights[-1]

    # 3) 为了得到最小/最大得分，需要分别取 k-1 个最小/最大的 adj_sums
    #    这里直接排序，时间 O(n log n)。如果 n 很大且 k 很小，也可以用堆（O(n log k)），
    #    但排序实现更简洁。
    adj_sums.sort()

    # 取最小的 k-1 项
    min_extra = sum(adj_sums[:k - 1])
    # 取最大的 k-1 项
    max_extra = sum(adj_sums[-(k - 1):])

    min_score = base + min_extra
    max_score = base + max_extra

    return max_score - min_score
```

> **关键行解释**  
> - 第 8 行：`adj_sums` 把每条相邻边的 “双弹珠重量” 预先算好。  
> - 第 13 行：`base` 是只有一个袋子时的得分，只算最左和最右两颗弹珠。  
> - 第 18‑22 行：排序后，切点的选择变得非常直接——前 `k‑1` 为最小，后 `k‑1` 为最大。  
> - 第 26‑27 行：把基准得分加上选中的额外和，得到最小/最大总得分。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 计算相邻和是 `O(n)`，排序 `O(n log n)`，其余都是线性操作。  
  - 与暴力解相比，`log n` 只是一条很小的“斜坡”，即使 `n=10^5` 也能轻松跑完。

- **空间复杂度**：`O(n)`  
  - 需要额外的数组 `adj_sums` 保存 `n‑1` 个相邻和，其他只用常数级别的变量。  

---

## 心得

- **核心技巧**：把“把数组划分成子数组”转化为“在相邻位置挑切点”，并发现每个切点的贡献是独立的。于是问题化为 **选 `k‑1` 个最大/最小数**，直接使用排序或堆即可。
- **适用的题型**  
  1. “把数组划分成若干段，使得某种代价最小/最大”——如 *Divide Array in Sets*、*Maximum Sum of K Non‑Overlapping Subarrays*。  
  2. “相邻元素之间的选择决定整体结果”——如 *Minimum Cost to Split Array*、*Maximum Profit of Cutting Ropes*。  
- **一句话总结**：**把划分问题抽象成“挑边”问题，利用贪心选最大/最小的边即可**。

---

## 反思

- **第一反应**：看到“把弹珠放进 k 包，求最大与最小得分差”，第一时间会想到**枚举所有划分**，因为对“划分”不熟悉，直觉是“暴力搜索”。  
- **最容易踩的坑**  
  - 忽略了 **每个袋子只计首尾** 的特殊规则，误以为要把整段求和。  
  - 在实现最小/最大得分时，忘记加上 **首尾的基准** `weights[0] + weights[-1]`，导致答案偏小。  
  - 边界情况：`k = 1`（不需要切）和 `k = len(weights)`（每颗弹珠单独成袋）都应该返回 `0`，代码里要显式处理。  
- **下次思路**：遇到“把数组分成 k 段”这类题，**先问自己**：“每次切分带来哪些独立的增量？”如果增量只依赖于相邻元素，那么就可以考虑 **排序/堆** 或 **前缀和** 的贪心/滑动窗口方案，而不是直接枚举。