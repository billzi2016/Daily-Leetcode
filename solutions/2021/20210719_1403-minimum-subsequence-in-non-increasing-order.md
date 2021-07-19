# #1403. 非递增顺序的最小子序列 / Minimum Subsequence in Non-Increasing Order

> 难度：简单 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-subsequence-in-non-increasing-order/)

---

## 题目（英文原版）

**Description**

Given the array nums, obtain a subsequence of the array whose sum of elements is strictly greater than the sum of the non included elements in such subsequence.
If there are multiple solutions, return the subsequence with minimum size and if there still exist multiple solutions, return the subsequence with the maximum total sum of all its elements. A subsequence of an array can be obtained by erasing some (possibly zero) elements from the array.
Note that the solution with the given constraints is guaranteed to be unique. Also return the answer sorted in non-increasing order.

**Examples**

**Example 1:**

```
Input: nums = [4,3,10,9,8]
Output: [10,9] 
Explanation: The subsequences [10,9] and [10,8] are minimal such that the sum of their elements is strictly greater than the sum of elements not included. However, the subsequence [10,9] has the maximum total sum of its elements.
```

**Example 2:**

```
Input: nums = [4,4,7,6,7]
Output: [7,7,6] 
Explanation: The subsequence [7,7] has the sum of its elements equal to 14 which is not strictly greater than the sum of elements not included (14 = 4 + 4 + 6). Therefore, the subsequence [7,6,7] is the minimal satisfying the conditions. Note the subsequence has to be returned in non-increasing order.
```

**Constraints**

- 1 <= nums.length <= 500
- 1 <= nums[i] <= 100

---

## 题目（中文翻译）

给定一个数组（array）`nums`，获取该数组的一个子序列（subsequence），使得该子序列中元素的和 **严格大于** 未被选入子序列的元素之和。  

如果存在多个满足条件的子序列，返回 **长度最小** 的那个；如果仍有多个，返回 **元素总和最大** 的那个。子序列可以通过删除（可能为零个）元素得到。  

题目保证在给定约束下答案唯一。返回的子序列需要按 **非递增**（non‑increasing）顺序排序。

## 示例

### 示例 1
**输入**  
`nums = [4,3,10,9,8]`

**输出**  
`[10,9]` 

**解释**  
子序列 `[10,9]` 与 `[10,8]` 都是最小的，使得其元素和严格大于未选元素的和。但 `[10,9]` 的元素总和更大，故返回该子序列。

### 示例 2
**输入**  
`nums = [4,4,7,6,7]`

**输出**  
`[7,7,6]` 

**解释**  
子序列 `[7,7]` 的元素和为 14，恰好等于未选元素的和（`4 + 4 + 6 = 14`），不满足“严格大于”的要求。因此，需要再加入一个元素，得到最小满足条件的子序列 `[7,6,7]`。按非递增顺序返回即为 `[7,7,6]`。

## 约束条件
- `1 <= nums.length <= 500`
- `1 <= nums[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的子序列都列举出来**，然后逐个检查它们是否满足  
> “子序列的元素和 > 未选元素的和”。  

如果满足，再比较子序列的长度（越小越好），长度相同的再比较总和（越大越好），最后挑出唯一答案。

- **数据结构**：  
  - 子序列可以用 **列表** 来保存。  
  - 为了遍历所有子序列，我们可以把数组的每一种“选/不选”状态看成二进制位，0 表示不选，1 表示选。  
  - 这其实和 **哈希表** 类似，哈希表把“键”映射到“值”。这里我们把“选哪几个位置”映射到“对应的子序列”。  

- **为什么正确**：  
  暴力遍历不遗漏任何一种可能的子序列，只要把所有子序列都检查一遍，必然能找到满足条件的最优解。

- **时间/空间复杂度**（大白话版）：  
  - **时间复杂度**是 `O(2^n)`。  
    想象一下，你有 `n` 把钥匙，每把钥匙可以打开或不打开，一共有 `2^n` 种开关组合。我们要把这 `2^n` 种组合全部尝试一次，所以时间会随 `n` 的指数级增长。  
  - **空间复杂度**是 `O(n)`。  
    只需要一个长度为 `n` 的临时列表来存当前的子序列，其他额外空间基本为常数。

> 由于题目限制 `n ≤ 500`，暴力解在真实测试里会 **超时**，只能用来帮助我们理解问题的本质。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def min_subsequence_bruteforce(nums: List[int]) -> List[int]:
    total = sum(nums)                     # 所有元素的和
    n = len(nums)
    best = None                           # 用来保存当前最好的子序列

    # 逐渐增大子序列的长度，从 1 到 n
    for size in range(1, n + 1):
        # itertools.combinations 会生成所有 size 大小的组合
        for comb in combinations(nums, size):
            cur_sum = sum(comb)           # 子序列的和
            rest_sum = total - cur_sum    # 未选元素的和
            if cur_sum > rest_sum:        # 必须严格大于
                # 先把子序列按非递增排序，方便后面比较
                cand = sorted(comb, reverse=True)
                if (best is None or                # 还没有答案
                    len(cand) < len(best) or       # 更小的长度
                    (len(cand) == len(best) and sum(cand) > sum(best)))):  # 同长度但更大总和
                    best = cand
        # 找到长度为 size 的解后，就可以直接返回，因为更大的长度一定不满足“最小长度”要求
        if best is not None:
            return best
    return []  # 理论上不会走到这里，因为题目保证一定有解
```

> 代码里每一行都写了中文注释，帮助你一步步跟上思路。  

#### 复杂度  

- **时间复杂度**：`O(2^n)` —— 需要尝试所有可能的子序列，随 `n` 指数增长。  
- **空间复杂度**：`O(n)` —— 只保存当前的组合以及若干常数级的临时变量。  

---

### 2. 最优解  

#### 思路  

从暴力解出发，我们发现 **“遍历所有组合” 是最慢的环节**，因为它要检查 `2^n` 种情况。  
仔细观察题目要求，会发现：

1. **我们只关心子序列的总和是否大于剩余元素的总和**。  
2. **元素的顺序不重要**（只要最终返回非递增排序即可），所以可以先把数组 **排序**。  

把数组从大到小排好后，**先取最大的几个数**，它们的和增长最快。  
我们不断把最大的数加入子序列，直到子序列的和 **已经大于** 剩余元素的和。  

为什么这一步一定能得到最小长度的子序列？

- 想象把所有数从大到小排成一列。要让子序列的和尽可能快地超过剩余的和，**先拿最大的数** 是最有效的“投资”。  
- 如果我们在某一步 **不取当前最大的数**，而去取更小的数，那么子序列的和增长会更慢，需要更多的元素才能超过剩余和，这会导致 **长度变大**，与“最小长度”目标冲突。  
- 当长度已经是最小的那一刻（第一次满足 “子序列和 > 剩余和”），如果还有其他组合同样长度，它们的总和一定不如我们选的“最大数”组合大，因为我们已经把最大的数都用了。于是**最大总和**的要求也自然满足。

> **核心技巧**：**贪心**（Greedy）——在每一步都做局部最优选择（取当前最大的数），最终得到全局最优解。

#### 代码（Python）

```python
from typing import List

def minSubsequence(nums: List[int]) -> List[int]:
    # 1. 把数组从大到小排好序
    nums.sort(reverse=True)               # 类似把字典里的单词按拼音倒序排列

    total = sum(nums)                      # 所有元素的和
    cur_sum = 0                            # 当前子序列的和
    ans = []                               # 用来保存选中的元素

    # 2. 从最大的开始依次取，直到满足条件
    for num in nums:
        cur_sum += num                     # 把这个数加入子序列
        ans.append(num)                    # 记录下来
        if cur_sum > total - cur_sum:      # 子序列和 > 未选元素和 ?
            break                           # 条件满足，直接结束循环

    # 3. ans 已经是非递增顺序，直接返回
    return ans
```

**关键行解释**：

- `nums.sort(reverse=True)`：把数组从大到小排好，就像把书架上的书按高度从高到低摆放，取最大的书最省空间。  
- `cur_sum > total - cur_sum`：左边是已经选的子序列和，右边是剩下的元素和。只要左边大，就满足题目要求。  

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 排序是最耗时的步骤，排序的复杂度是 `n log n`（`log n` 可以理解为把 `n` 分成二分的层数）。遍历一次数组是线性 `O(n)`，相比之下不占主导。  
- **空间复杂度**：`O(1)`（不计返回结果的空间）  
  - 除了几个整数变量和返回的列表本身，没有额外使用与 `n` 成正比的额外存储。  

> 与暴力解相比，时间从指数级下降到对数线性，几乎瞬间就能算完 500 个元素。

---

## 心得  

- **核心技巧**：**贪心 + 排序**，在需要“尽快超过某个阈值”且“顺序不影响结果”的场景下，先挑最大的往往是最优的。  
- **适用题型**（类似思路可复用）：  
  1. “**分割数组使子数组和最大**”（如 LeetCode 1402）  
  2. “**最少数量的硬币凑齐金额**”（经典背包的贪心版）  
  3. “**从数组中挑选最少数量的元素，使其和大于目标值**”（本题的变体）  
- **一句话总结**：**“把数从大到小排，先拿最大的，直到超过剩余总和”** 就是解这道题的钥匙。

---

## 反思  

- **第一反应**：看到“子序列和要大于剩余元素和”，本能地想到**遍历所有子序列**，因为这样最直接能检查“是否满足”。  
- **最容易踩的坑**：  
  - **忘记排序**：如果不把数组从大到小排列，随意取元素可能会导致子序列长度不是最小的。  
  - **边界条件**：当数组只有一个元素时，直接返回该元素；当所有元素相等时，需要把足够多的元素取到超过一半。  
  - **返回顺序**：题目要求返回 **非递增**（从大到小）顺序，若忘记排序或在循环中逆序添加，答案会不符合要求。  
- **下次遇到同类题**，第一步应该问自己：“**有没有一种自然的顺序（大小、时间等）可以先把‘最有价值’的东西挑出来**？”如果答案是“是”，那很可能可以用**贪心 + 排序**来快速得到最优解。