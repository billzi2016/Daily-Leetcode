# #2592. 最大化数组的伟大度 / Maximize Greatness of an Array

> 难度：中等 · 标签：Array、Two Pointers、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximize-greatness-of-an-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. You are allowed to permute nums into a new array perm of your choosing.
We define the greatness of nums be the number of indices 0 <= i < nums.length for which perm[i] > nums[i].
Return the maximum possible greatness you can achieve after permuting nums.

**Examples**

**Example 1:**

```
Input: nums = [1,3,5,2,1,3,1]
Output: 4
Explanation: One of the optimal rearrangements is perm = [2,5,1,3,3,1,1].
At indices = 0, 1, 3, and 4, perm[i] > nums[i]. Hence, we return 4.
```

**Example 2:**

```
Input: nums = [1,2,3,4]
Output: 3
Explanation: We can prove the optimal perm is [2,3,4,1].
At indices = 0, 1, and 2, perm[i] > nums[i]. Hence, we return 3.
```

**Constraints**

- 1 <= nums.length <= 105
- 0 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个下标从 0 开始的整数数组 `nums`。你可以任意排列 `nums`，得到一个新数组 `perm`（由你自行决定的排列）。  

我们将 **伟大度**（greatness）定义为满足 `perm[i] > nums[i]` 的下标数量，其中 `0 ≤ i < nums.length`。  

返回在对 `nums` 进行任意排列后，能够得到的最大可能的伟大度。

**示例 1**  
输入: `nums = [1,3,5,2,1,3,1]`  
输出: `4`  
解释: 其中一种最优的排列是 `perm = [2,5,1,3,3,1,1]`。在下标 `0、1、3、4` 处，`perm[i] > nums[i]` 成立。因此返回 `4`。

**示例 2**  
输入: `nums = [1,2,3,4]`  
输出: `3`  
解释: 我们可以证明最优的排列是 `[2,3,4,1]`。在下标 `0、1、2` 处，`perm[i] > nums[i]` 成立。因此返回 `3`。

**约束条件**  
- `1 ≤ nums.length ≤ 10^5`  
- `0 ≤ nums[i] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的排列** 都枚举出来，逐个计算它们的 “greatness”，取最大的那个。  
- **数据结构**：我们可以用 Python 标准库 `itertools.permutations` 把数组的全排列一次性生成。把每一次排列记作 `perm`，再遍历下标 `i` 判断 `perm[i] > nums[i]` 是否成立，计数即为该排列的 greatness。  
- **为什么正确**：因为我们穷举了所有合法的排列，最大值一定会出现在这些排列之中，所以返回的就是答案的上界。  
- **时间/空间复杂度**：  
  - **时间**：数组长度为 `n` 时，排列数是 `n!`（n 的阶乘），每个排列我们还要遍历 `n` 个元素去比较大小，故时间复杂度是 `O(n!·n)`。这在实际中几乎不可接受，哪怕 `n=10` 已经需要 3.6 × 10⁶ 次排列。  
  - **空间**：生成排列时会占用 `O(n)` 的递归栈空间，加上 `itertools` 迭代器本身的常数空间，总体是 `O(n)`。  

> **大白话**：`O(n!·n)` 就像把一盒子糖果全部拆开再重新装，每次装完都要数一遍糖果的颜色，糖果多了，工作量会像火箭一样爆炸。

#### 代码（Python）

```python
import itertools
from typing import List

def greatness_bruteforce(nums: List[int]) -> int:
    """暴力枚举所有排列，返回最大 greatness。仅作概念演示，实际会超时。"""
    n = len(nums)
    best = 0
    # itertools.permutations 会生成所有 n! 种排列
    for perm in itertools.permutations(nums):
        cur = 0
        # 逐个比较 perm[i] 与原数组 nums[i]
        for i in range(n):
            if perm[i] > nums[i]:
                cur += 1
        best = max(best, cur)   # 记录最大值
    return best
```

#### 复杂度

- **时间复杂度**：`O(n!·n)` —— 随着 `n` 增大，计算量呈阶乘级爆炸，几乎不可能在 10⁵ 规模的数据上跑完。  
- **空间复杂度**：`O(n)` —— 只用了常数级的额外空间（遍历时的临时变量），不随排列数量增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈** 在于我们一次又一次地去“挑选”比当前 `nums[i]` 大的数。其实我们不需要穷举，只要 **把每个位置尽可能配到一个比它大的最小元素**，就能保证最大化 “greater” 的次数。这个思路与 “advantage shuffle” / “贪心配对” 非常相似。

具体步骤：

1. **先把原数组 `nums` 排序**，得到 `sorted_nums`。排序后，较小的元素在左侧，较大的在右侧，方便我们从小到大依次配对。  
2. **准备另一个指针 `j`**，指向 `sorted_nums` 中尚未使用的最小元素。我们从 `sorted_nums` 的最左边（最小）开始，尝试为每个 `nums[i]`（同样从小到大）找到一个 **严格更大的** 元素。  
3. **双指针贪心**：  
   - 若 `sorted_nums[j] > nums[i]`，说明找到了一个可以 “赢” 的元素，`greatness` 加 1，`j` 向右移动一位（表示该元素已被使用）。  
   - 否则（`sorted_nums[j] <= nums[i]`），说明当前最小的未使用元素根本打不过 `nums[i]`，这时候我们**放弃** 用它去赢，直接把 `j` 再往右移动，去找更大的候选。  
4. 由于我们始终用 **最小的可以赢的数** 去匹配，所以不会“浪费”大数去轻易赢小数，从而保证了赢的次数最多。  

> **类比**：把 `nums` 看成一排学生的身高，`sorted_nums` 是一堆可用的球。我们希望每个学生都能拿到一个比自己高的球来“压倒”。最省力的办法就是让身高最矮的学生先挑最小的比他高的球，依次向上分配，这样球不会被浪费在本可以用更小球的学生身上。

#### 代码（Python）

```python
from typing import List

def maximize_greatness(nums: List[int]) -> int:
    """
    贪心 + 双指针
    返回在任意排列后能够得到的最大 greatness。
    """
    # 1. 对原数组和可用元素都排序
    nums_sorted = sorted(nums)          # 用于遍历的顺序
    unused = sorted(nums)               # 实际上和 nums_sorted 完全相同

    i, j = 0, 0          # i 遍历 nums_sorted，j 遍历 unused（未使用的最小元素）
    greatness = 0

    while i < len(nums_sorted) and j < len(unused):
        # 若当前最小未使用的元素能够赢过 nums_sorted[i]
        if unused[j] > nums_sorted[i]:
            greatness += 1    # 成功配对，greatness 加一
            i += 1            # 下一个待配对的 nums 元素
            j += 1            # 这个元素已使用，指针右移
        else:
            # 这个最小元素连当前 nums[i] 都打不过，直接丢掉它
            j += 1            # 继续找更大的候选
    return greatness
```

#### 复杂度

- **时间复杂度**：`O(n log n)` —— 主要耗时在两次排序（`sorted`），每次排序的复杂度是 `O(n log n)`。随后双指针只遍历一次，`O(n)`，不影响整体量级。  
  - 与暴力解的 `O(n!·n)` 相比，`log n` 只比 `n` 大一点点，几乎可以忽略不计，因而在 10⁵ 规模的数据下也能轻松跑完。  
- **空间复杂度**：`O(n)` —— 需要额外存放排序后的数组（Python 的 `sorted` 会返回新列表），其大小与输入相同。若允许原地排序，则可以把空间降到 `O(1)`（不计递归栈）。

---

## 心得

- **核心技巧**：**贪心配对 + 双指针**。把“尽可能多地让 perm[i] > nums[i]”转化为“用最小的能赢的数去匹配每个元素”。  
- **适用的题型**  
  1. *Advantage Shuffle*（LeetCode 870）——同样是让一个数组的每个元素尽量大于另一个数组对应位置的元素。  
  2. *最小不可匹配数*（类似 “匹配游戏”）——判断能否用更大的数完全覆盖另一个集合。  
  3. *分配资源类*（如 “最大化成功配对”）——把资源按需求的大小从小到大配对，使用最小满足需求的资源。  
- **一句话总结**：**用最小的“大”去抢占每一次“胜利”，别让大数浪费在本可以用小数赢的地方。**

---

## 反思

- **第一反应**：看到 “perm[i] > nums[i]”，立刻想到 “把每个位置配一个比它大的数”，于是想到全排列的暴力搜索。  
- **最容易踩的坑**  
  1. **忘记“严格大于”**：`>=` 会导致错误计数，必须是 `>`。  
  2. **忽视重复元素**：因为数组里可能有相同的数，贪心时必须保证每个元素只能使用一次（使用指针 `j` 标记已使用）。  
  3. **边界条件**：当所有元素都相等时，答案是 0；当所有元素都递增时，答案是 `n‑1`（最后一个必然被最小的数“压住”）。  
- **下次第一步**：先 **排序 + 双指针**，思考 “是否可以用最小的可用元素赢过当前目标”。如果能，就直接配对；否则放弃当前最小元素，继续寻找更大的。这样往往能迅速得到最优贪心思路。