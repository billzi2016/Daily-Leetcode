# #3041. 修改后数组中连续元素的最大数量 / Maximize Consecutive Elements in an Array After Modification

> 难度：困难 · 标签：Array、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximize-consecutive-elements-in-an-array-after-modification/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array nums consisting of positive integers.
Initially, you can increase the value of any element in the array by at most 1.
After that, you need to select one or more elements from the final array such that those elements are consecutive when sorted in increasing order. For example, the elements [3, 4, 5] are consecutive while [3, 4, 6] and [1, 1, 2, 3] are not.
Return the maximum number of elements that you can select.

**Examples**

**Example 1:**

```
Input: nums = [2,1,5,1,1]
Output: 3
Explanation: We can increase the elements at indices 0 and 3. The resulting array is nums = [3,1,5,2,1].
We select the elements [3,1,5,2,1] and we sort them to obtain [1,2,3], which are consecutive.
It can be shown that we cannot select more than 3 consecutive elements.
```

**Example 2:**

```
Input: nums = [1,4,7,10]
Output: 1
Explanation: The maximum consecutive elements that we can select is 1.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 106

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的数组 `nums`，其中元素均为正整数。  
最初，你可以将数组中任意元素的值增加至多 **1**。  
完成此操作后，需要从得到的最终数组中选取一个或多个元素，使得这些元素在 **升序** 排列后是连续的。例如，`[3, 4, 5]` 是连续的，而 `[3, 4, 6]` 和 `[1, 1, 2, 3]` 则不是。  
返回你能够选取的元素的最大数量。

**示例 1**  
**输入**: `nums = [2,1,5,1,1]`  
**输出**: `3`  
**解释**: 我们可以将下标 `0` 和 `3` 处的元素各增加 `1`，得到数组 `nums = [3,1,5,2,1]`。  
选取所有元素并排序后得到 `[1,2,3]`，它们是连续的。可以证明无法选取超过 `3` 个连续元素。

**示例 2**  
**输入**: `nums = [1,4,7,10]`  
**输出**: `1`  
**解释**: 能选取的最长连续元素数量为 `1`。

**约束条件**  
- `1 <= nums.length <= 10^5`  
- `1 <= nums[i] <= 10^6`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：  
1. 先把数组 `nums` 排序，这样如果我们选出的若干个数在 **排序后** 是连续的，那么在原数组里它们的下标顺序并不重要，只要数值满足条件就行。  
2. 对每个元素 `nums[i]`，我们有两种可能的取值：`nums[i]`（不动）或 `nums[i] + 1`（把它增加 1）。  
3. 设 `dp[i]` 为 **以第 i 个元素（在排好序后的数组中）结尾** 的最长连续子序列的长度。要把 `nums[i]` 接在 `nums[j]`（`j < i`）后面，必须满足  
   - 可以从 `nums[j]` 选出的值 `y`，加上 1，得到 `nums[i]` 能选的某个值 `x`。  
   - 换句话说，`x - y = 1`，而 `x ∈ {nums[i], nums[i]+1}`，`y ∈ {nums[j], nums[j]+1}`。  

把所有可能的组合枚举一遍，就能判断 `j` 能否接在 `i` 前面。  
如果能，就把 `dp[i] = max(dp[i], dp[j] + 1)`；如果不能，就保持原来的 `dp[i]`（最小是 1，因为自己可以单独成一个长度为 1 的序列）。

> **生活化类比**：把每个数想象成一本书的两页——原页码 `a` 和可以把它翻到的下一页 `a+1`。我们要把这些书排成“一页接一页”的顺序，只有当前一本书的页码正好是前一本书页码的 **+1** 时，才能接在一起。

这个方法必然能得到正确答案，因为它穷举了所有合法的“前后衔接”方式。

#### 代码（Python）

```python
from typing import List

def max_consecutive_bruteforce(nums: List[int]) -> int:
    # 1. 排序
    a = sorted(nums)                       # O(n log n)

    n = len(a)
    dp = [1] * n                            # 每个元素至少可以单独成一个序列
    ans = 1

    # 2. 双层循环检查所有前驱 j
    for i in range(n):
        for j in range(i):
            # 下面四种组合对应 x∈{a[i],a[i]+1}，y∈{a[j],a[j]+1}
            possible = (
                a[i]   == a[j]   + 1 or   # (no inc, no inc)
                a[i]   == a[j] + 2 or     # (no inc, inc)
                a[i]+1 == a[j]   + 1 or   # (inc, no inc)
                a[i]+1 == a[j] + 2        # (inc, inc)
            )
            if possible:                     # 能接在 j 后面
                dp[i] = max(dp[i], dp[j] + 1)

        ans = max(ans, dp[i])                # 更新全局最大

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 排序 `O(n log n)` 已经可以忽略，主要的开销是两层循环 `i、j`，每对 `(i, j)` 都要做常数次比较。  
  - “`O(n²)`” 可以理解为：如果数组有 10,000 个元素，程序大概要跑 10,000 × 10,000 = 1 亿次比较，这在实际中会超时。

- **空间复杂度**：`O(n)`  
  - 只用了排序后的数组和一个长度为 `n` 的 `dp` 表，额外空间随输入规模线性增长。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈**在于我们要遍历所有前面的元素 `j` 来找能接上的最长链。  
实际上，我们只关心 **前一个数的取值**，而不需要记住是哪一个具体下标。

把每个元素看成一个**区间** `[v, v+1]`（`v = nums[i]`），我们要在这些区间里挑选一个整数，使得挑选的整数序列是 `x, x+1, x+2, …` 的形式。  

这等价于下面的模型：

> **模型**：给定 `n` 个区间 `[l_i, r_i]`（这里 `r_i = l_i + 1`），找最长的序列 `p_1 < p_2 < … < p_k`，满足 `p_t ∈ [l_{i_t}, r_{i_t}]` 且 `p_{t+1} = p_t + 1`。

因为每个区间的长度只有 2，我们只需要记录 **“以某个具体值 v 结尾的最长序列长度”**。  
设 `best[v]` 为“已经处理完前面的所有区间后，以整数 `v` 为结尾的最长序列长度”。  
遍历区间时，只需要尝试两种可能的取值：

1. **不增加**：把当前区间的左端点 `v` 当作序列的下一个数。  
   - 那么它只能接在以 `v-1` 结尾的序列后面，长度为 `best[v-1] + 1`。  

2. **增加 1**：把当前区间的右端点 `v+1` 当作序列的下一个数。  
   - 那么它只能接在以 `v` 结尾的序列后面，长度为 `best[v] + 1`。  

取两者的最大值即可得到以 `v`（或 `v+1`）结尾的新序列长度，并把它写回 `best` 表。  

> **类比**：想象每个区间是一块可以放“棋子”的格子，格子只能放在左格子（不加 1）或右格子（加 1）。我们从左到右遍历这些格子，每放一颗棋子，就看它能否紧挨着前面已经摆好的最长连线的末尾。

因为我们只关心 **当前整数值** 的最长长度，`best` 可以用 Python 的 `defaultdict(int)`（默认值 0）实现。  
遍历完所有区间后，`best` 中的最大值即为答案。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def max_consecutive(nums: List[int]) -> int:
    # 1. 把每个数视作区间 [v, v+1]，并按左端点 v 排序
    nums.sort()                               # O(n log n)

    best = defaultdict(int)   # best[v] = longest chain ending with value v
    answer = 0

    for v in nums:            # v 是区间的左端点
        # ① 不增加：取值 v，接在以 v-1 结尾的序列后面
        use_left  = best[v - 1] + 1

        # ② 增加 1：取值 v+1，接在以 v   结尾的序列后面
        use_right = best[v] + 1

        # 更新以 v、v+1 结尾的最长长度（取最大，防止被后面的区间覆盖掉更短的情况）
        if use_left > best[v]:
            best[v] = use_left
        if use_right > best[v + 1]:
            best[v + 1] = use_right

        # 维护全局最大值
        answer = max(answer, use_left, use_right)

    return answer
```

**代码要点（中文注释）**  

| 行号 | 说明 |
|------|------|
| `nums.sort()` | 先排序，保证我们从小到大“构造”序列，后面的区间只能在已经处理好的序列后面接。 |
| `best = defaultdict(int)` | 类似字典的“查字典”，键是整数值，值是以该整数结尾的最长长度，默认是 0（相当于没有前驱）。 |
| `use_left = best[v-1] + 1` | 若把当前数不加 1（取 `v`），它只能接在 `v-1` 后面。`best[v-1]` 是以 `v-1` 结尾的最长长度。 |
| `use_right = best[v] + 1` | 若把当前数加 1（取 `v+1`），它只能接在 `v` 后面。 |
| `best[v] = max(best[v], use_left)` | 可能已经有别的区间也能得到以 `v` 结尾的更长序列，取最大。 |
| `answer = max(answer, use_left, use_right)` | 实时更新全局答案。 |

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 主要是排序 `O(n log n)`，遍历一次数组并做常数次哈希查找/写入是 `O(n)`。  
  - 与暴力的 `O(n²)` 相比，`n = 10⁵` 时，这个复杂度几乎是瞬间完成的。  

- **空间复杂度**：`O(n)`（最坏情况）  
  - `best` 中可能出现的键值范围是所有可能的取值 `v` 与 `v+1`，最多是 `2n` 个，仍然是线性空间。  
  - 实际上因为值的范围受 `nums[i] ≤ 10⁶` 限制，空间上限约为 `2·10⁶`，在题目限制下完全可接受。  

---

## 心得  

- **核心技巧**：把“每个数可以增 1”转化为 **长度为 2 的区间**，然后用 **以具体值结尾的最长长度**（哈希表）来做动态规划。  
- **适用场景**：  
  1. “每个元素有若干可选取值，要求取出的序列满足相邻差固定”的问题（如把每个字符可以变成相邻字母的题目）。  
  2. “区间覆盖”类的最长递增/递减子序列问题（如每个元素可以向左或向右移动一步）。  
- **一句话总结**：把“能增 1”看成“给每个数加上一块可以自由选择左/右的格子”，只要记住每个整数值对应的最长链，就能线性完成求解。

---

## 反思  

- **第一反应**：直接枚举所有子集或所有增 1 的组合，想到 DP，却不知道该怎么设计状态。  
- **最容易踩的坑**：  
  - 忘记对数组先排序，导致后面的 “以 v‑1 结尾” 的链不一定已经计算完。  
  - 在更新 `best[v]` 与 `best[v+1]` 时使用了同一个临时变量，导致后面的更新被错误覆盖。  
  - 边界值：`v = 1` 时会访问 `best[0]`，要确保字典的默认值是 0（使用 `defaultdict(int)`）。  
- **下次思路**：看到“每个元素可以在一个小范围内自由选择”时，第一步就把它抽象成 **区间**，然后考虑 **以具体数值为状态的 DP**，而不是以下标为状态。这样往往能把二次甚至指数级的搜索压缩到线性时间。