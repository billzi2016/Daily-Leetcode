# #1537. 获得最大得分 / Get the Maximum Score

> 难度：困难 · 标签：Array、Two Pointers、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/get-the-maximum-score/)

---

## 题目（英文原版）

**Description**

You are given two sorted arrays of distinct integers nums1 and nums2.
A valid path is defined as follows:
The score is defined as the sum of unique values in a valid path.
Return the maximum score you can obtain of all possible valid paths. Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: nums1 = [2,4,5,8,10], nums2 = [4,6,8,9]
Output: 30
Explanation: Valid paths:
[2,4,5,8,10], [2,4,5,8,9], [2,4,6,8,9], [2,4,6,8,10],  (starting from nums1)
[4,6,8,9], [4,5,8,10], [4,5,8,9], [4,6,8,10]    (starting from nums2)
The maximum is obtained with the path in green [2,4,6,8,10].
```

**Example 2:**

```
Input: nums1 = [1,3,5,7,9], nums2 = [3,5,100]
Output: 109
Explanation: Maximum sum is obtained with the path [1,3,5,100].
```

**Example 3:**

```
Input: nums1 = [1,2,3,4,5], nums2 = [6,7,8,9,10]
Output: 40
Explanation: There are no common elements between nums1 and nums2.
Maximum sum is obtained with the path [6,7,8,9,10].
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 105
- 1 <= nums1[i], nums2[i] <= 107
- nums1 and nums2 are strictly increasing.

---

## 题目（中文翻译）

你得到两个已排序的数组 (sorted arrays) `nums1` 与 `nums2`，且其中的整数互不相同 (distinct integers)。  

**有效路径** 的定义如下：  
- 你可以从 `nums1` 或 `nums2` 的第一个元素开始遍历。  
- 在遍历过程中只能向前移动（即只能访问后面的元素）。  
- 仅当当前元素在两数组中都出现时，你才可以选择切换到另一条数组继续向前遍历。  

**得分** 定义为一次有效路径中所有访问到的**唯一**值的和。  

返回所有可能的有效路径中能够得到的**最大得分**。由于答案可能非常大，返回结果请对 `10^9 + 7` 取模。

---

### 示例  

#### 示例 1  
```
Input: nums1 = [2,4,5,8,10], nums2 = [4,6,8,9]
Output: 30
```
**解释**：所有可能的有效路径如下（绿色部分为得分最高的路径）  

- 从 `nums1` 开始：`[2,4,5,8,10]`、`[2,4,5,8,9]`、`[2,4,6,8,9]`、`[2,4,6,8,10]`  
- 从 `nums2` 开始：`[4,6,8,9]`、`[4,5,8,10]`、`[4,5,8,9]`、`[4,6,8,10]`  

得分最高的路径为 **[2,4,6,8,10]**，其元素和为 30。

#### 示例 2  
```
Input: nums1 = [1,3,5,7,9], nums2 = [3,5,100]
Output: 109
```
**解释**：最大得分通过路径 **[1,3,5,100]** 获得，元素和为 109。

#### 示例 3  
```
Input: nums1 = [1,2,3,4,5], nums2 = [6,7,8,9,10]
Output: 40
```
**解释**：`nums1` 与 `nums2` 没有公共元素，无法切换。最大得分来自路径 **[6,7,8,9,10]**，其和为 40。

---

### 约束条件  

- `1 <= nums1.length, nums2.length <= 10^5`  
- `1 <= nums1[i], nums2[i] <= 10^7`  
- `nums1` 与 `nums2` 均为严格递增序列（strictly increasing）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有合法路径都枚举出来，算出每条路径的分数，取最大**。  
- **合法路径**的定义：从 `nums1` 或 `nums2` 任意一个数组的开头出发，沿着递增顺序走，每次可以在两个数组的**公共元素**处“换道”。  
- 为了枚举路径，我们可以把两个数组的所有元素按出现顺序排列成一棵**选择树**：在每个公共元素处有两条分支（继续走当前数组，或跳到另一数组），在非公共元素处只能继续走当前数组。  

把这棵树遍历一遍（深度优先搜索）就能得到所有路径。  

> **类比**：想象你在两条平行的登山小路上行走，只有在两条路上出现相同的岩石时才能换到另一条路。暴力法就是把每一次“换岩石”的选择全部写下来，看看哪条路线的风景（数值）最美。

**为什么能得到正确答案**  
因为我们把**每一种可能的换道方式**都列举了，最大分数一定出现在这些枚举出来的路径里。

**时间/空间复杂度**  
- 每遇到一个公共元素就会产生一次二选一的分支。若公共元素有 `k` 个，理论上会产生 `2^k` 条路径。最坏情况下 `k` 接近 `min(len(nums1), len(nums2))`，即指数级增长。  
- **时间复杂度**：`O(2^k)`，在最坏情况下接近 `O(2^n)`（指数级），这在实际数据（长度可达 10^5）下根本不可行。  
- **空间复杂度**：递归栈深度最多 `O(n)`，但因为分支数爆炸，实际占用的内存也会非常大。

> **大白话**：指数级就像每多一个公共数字，就要把已有的所有路径翻倍，几分钟的工作会变成几年的工作。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def maxScore_bruteforce(nums1: List[int], nums2: List[int]) -> int:
    # 把两个数组合并成一个有序序列，记录每个元素来源
    merged = []
    i = j = 0
    while i < len(nums1) and j < len(nums2):
        if nums1[i] < nums2[j]:
            merged.append((nums1[i], 1))   # 1 代表来自 nums1
            i += 1
        elif nums1[i] > nums2[j]:
            merged.append((nums2[j], 2))   # 2 代表来自 nums2
            j += 1
        else:  # 公共元素
            merged.append((nums1[i], 0))   # 0 代表可以换道的公共元素
            i += 1
            j += 1
    # 余下的元素直接加入
    while i < len(nums1):
        merged.append((nums1[i], 1))
        i += 1
    while j < len(nums2):
        merged.append((nums2[j], 2))
        j += 1

    # 深度优先搜索所有路径
    best = 0
    def dfs(pos: int, cur_sum: int, cur_arr: int):
        """pos 为当前在 merged 中的下标，cur_arr 为当前所在的数组 (1 或 2)"""
        nonlocal best
        if pos == len(merged):
            best = max(best, cur_sum)
            return
        val, typ = merged[pos]
        if typ == 0:               # 公共元素，可以选择换道或不换
            # 继续走当前数组（不换道）
            dfs(pos + 1, cur_sum + val, cur_arr)
            # 换道后继续走另一条数组
            dfs(pos + 1, cur_sum + val, 3 - cur_arr)   # 3-1=2, 3-2=1
        else:
            # 只能在当前所在的数组上走
            if typ == cur_arr:
                dfs(pos + 1, cur_sum + val, cur_arr)
            else:
                # 这条路走不通，直接终止
                best = max(best, cur_sum)

    # 可以从任意数组的起点开始
    dfs(0, 0, 1)
    dfs(0, 0, 2)
    return best % MOD
```

> 以上代码仅作思路演示，**在大数据规模下会超时或栈溢出**。

#### 复杂度

- **时间复杂度**：`O(2^k)`（指数级），`k` 为公共元素的个数。实际运行会在很小的输入规模下才可接受。
- **空间复杂度**：`O(n)`（递归栈深度），`n = len(nums1) + len(nums2)`。但因为分支数爆炸，实际占用的内存也会很大。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**唯一真正产生选择的点是两个数组的公共元素**。在每段“公共元素之间的子数组”里，我们只能沿着单一数组前进，**没有分支**。因此我们可以把整个问题 **按公共元素把两条数组切成若干段**，每段内部只能取当前数组的所有元素之和。  

**关键观察**  
- 对于某一段（两段公共元素之间或数组首尾），我们可以分别计算：

  ```
  sum1 = 该段在 nums1 中所有元素的和
  sum2 = 该段在 nums2 中所有元素的和
  ```

- 当走到段的末端（遇到公共元素）时，我们可以决定 **“切换到分数更大的那条路”**，因为后面的选择只受当前累计分数的大小影响，后面的公共元素仍然提供相同的切换机会。  

- 这正好符合**动态规划**的思想：  
  - `dp1` 表示走到当前公共元素时，以 `nums1` 为当前路径的最大分数。  
  - `dp2` 表示走到当前公共元素时，以 `nums2` 为当前路径的最大分数。  
  - 当遇到公共元素 `x` 时，新的 `dp1`、`dp2` 都可以从两条路切换过来：

    ```
    new_dp1 = max(dp1 + sum1, dp2 + sum2)   # 选较大的那条路再加上公共元素 x
    new_dp2 = new_dp1                      # 两条路在公共元素处得分相同
    ```

  - 然后把 `sum1`、`sum2` 清零，继续统计下一段。

**如何高效遍历**  
因为两个数组本身已经**升序且不含重复**，我们可以使用 **双指针** 同时遍历：

- `i` 指向 `nums1`，`j` 指向 `nums2`。  
- 当 `nums1[i] < nums2[j]` 时，把 `nums1[i]` 加到 `sum1`，`i++`。  
- 当 `nums1[i] > nums2[j]` 时，把 `nums2[j]` 加到 `sum2`，`j++`。  
- 当相等时（公共元素），执行上面的状态转移，`i++`、`j++`，并把公共元素本身也加入 `new_dp`（因为路径中必须包含这个元素）。

遍历结束后，仍可能剩余一段未处理的尾部（两个数组中较大的那段），只需要把 `sum1`、`sum2` 加到对应的 `dp`，取最大即可。

**为什么是最优**  
- 每段我们只保留 **两条可能的最大累计分数**（以哪条数组结束），没有多余的状态。  
- 任何合法路径在每个公共元素处的累计分数必然不小于这两条记录中的一个，否则我们可以用记录的更大分数替代它，得到更优解。  
- 因此 DP+双指针的贪心更新能够覆盖所有可能，且只遍历一次数组，时间线性。

**类比**  
想象两条并行的跑道，跑者只能在跑道上跑，只有在两条跑道出现同一个补给站（公共元素）时才可以决定换跑道。每段跑道我们先算出在这段里跑完全程能拿到的“能量”，到补给站时我们只保留“能量更高的那条跑道的累计能量”，然后继续跑。整个过程只需要一次跑完两条跑道。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def maxScore(nums1: List[int], nums2: List[int]) -> int:
    """
    双指针 + 动态规划
    dp1 / dp2 : 到当前公共元素为止，以 nums1 / nums2 结尾的最大分数
    sum1 / sum2 : 记录自上一个公共元素之后，各自段落的元素和
    """
    i = j = 0
    dp1 = dp2 = 0          # 初始分数为 0
    sum1 = sum2 = 0        # 当前段的累计和

    while i < len(nums1) and j < len(nums2):
        if nums1[i] < nums2[j]:
            sum1 += nums1[i]   # 只在 nums1 中出现，累计到 sum1
            i += 1
        elif nums1[i] > nums2[j]:
            sum2 += nums2[j]   # 只在 nums2 中出现，累计到 sum2
            j += 1
        else:   # 找到公共元素
            # 该公共元素本身也必须计入分数
            common = nums1[i]   # == nums2[j]
            # 取两条路中累计分数更大的那条，再加上本段和以及公共元素
            best = max(dp1 + sum1, dp2 + sum2) + common
            dp1 = dp2 = best % MOD   # 在公共元素处，两条路的累计分数相同
            # 清零本段累计和，准备统计下一段
            sum1 = sum2 = 0
            i += 1
            j += 1

    # 处理剩余的尾部（只会在一条数组中出现）
    while i < len(nums1):
        sum1 += nums1[i]
        i += 1
    while j < len(nums2):
        sum2 += nums2[j]
        j += 1

    # 最终答案是两条路各自加上各自剩余段的和，取最大
    ans = max(dp1 + sum1, dp2 + sum2) % MOD
    return ans
```

> 代码中的 `% MOD` 只在最终返回时需要取模，内部的比较可以不取模（防止负数影响），但为安全起见我们在更新 `dp` 时已做模运算，避免整数溢出（Python 本身不溢出，但保持一致性）。

#### 复杂度

- **时间复杂度**：`O(m + n)`，只遍历两数组一次。  
  - `m = len(nums1)`, `n = len(nums2)`。  
  - 与暴力 `O(2^k)` 相比，线性时间几乎是瞬间完成，即使 10⁵ 长度也毫无压力。  
- **空间复杂度**：`O(1)`，只使用常数个额外变量（指针、累计和、DP 值），不依赖额外数组或递归栈。

---

## 心得

- **核心技巧**：把两个严格递增的数组按公共元素切分成若干段，利用 **双指针** 同时遍历并在每个公共元素处做 **动态规划的状态转移**（取较大累计分数）。  
- **适用的题型**  
  1. *两个有序序列的最大加权路径*（如 LeetCode 1537. Get the Maximum Score）。  
  2. *合并两条有序链表并求最大和*（类似 “Maximum Sum of Two Non‑Overlapping Subarrays”。）  
  3. *在两条路径之间切换的最优子结构*（如 “Maximum Sum Path in a Matrix”）。
- **一句话总结**：**在公共节点处只保留“更大累计和”即可，整个过程只需一次双指针遍历**。

---

## 反思

- **第一反应**：看到“两个递增数组”“换道”就想到“把公共元素当作桥”，于是想用递归枚举所有换道方案。  
- **最容易踩的坑**  
  1. **忘记把公共元素本身计入分数**，导致答案偏小。  
  2. **漏掉尾部剩余段的和**，当两数组没有公共元素时会直接返回 0。  
  3. **取模位置错误**：在 DP 更新过程中取模会影响 `max` 比较，应该在比较前使用真实数值或统一在最后取模。  
- **下次类似题的第一步**：**先定位公共元素（交点），把问题分段**；随后使用 **双指针 + DP** 在每个交点做“取最大” 的状态转移。这样即可从指数暴力直接降到线性最优。