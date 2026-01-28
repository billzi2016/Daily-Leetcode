# #3507. 最小配对移除使数组有序 I / Minimum Pair Removal to Sort Array I

> 难度：简单 · 标签：Array、Hash Table、Linked List、Heap (Priority Queue)、Simulation、Doubly-Linked List、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/minimum-pair-removal-to-sort-array-i/)

---

## 题目（英文原版）

**Description**

Given an array nums, you can perform the following operation any number of times:
Return the minimum number of operations needed to make the array non-decreasing.
An array is said to be non-decreasing if each element is greater than or equal to its previous element (if it exists).

**Examples**

**Example 1:**

```
Input: nums = [5,2,3,1]
Output: 2
Explanation:
The array nums became non-decreasing in two operations.
```

**Example 2:**

```
Input: nums = [1,2,2]
Output: 0
Explanation:
The array nums is already sorted.
```

**Constraints**

- 1 <= nums.length <= 50
- -1000 <= nums[i] <= 1000

---

## 题目（中文翻译）

给定一个数组 `nums`，你可以任意次数执行下述操作：  
返回使数组变为非递减（non-decreasing）的最少操作次数。

如果数组中每个元素都大于或等于其前一个元素（若前一个元素存在），则称该数组为非递减。

**示例 1**  
**示例 2**  
**约束条件**  

**示例**

**示例 1:**  
输入: `nums = [5,2,3,1]`  
输出: `2`  
解释:  
数组 `nums` 经过两次操作后变为非递减。

**示例 2:**  
输入: `nums = [1,2,2]`  
输出: `0`  
解释:  
数组 `nums` 已经是有序的。

**约束条件**  
- `1 <= nums.length <= 50`  
- `-1000 <= nums[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的删除方式**，看哪一种能够让剩下的数组已经是非递减的，并且使用的操作次数最少。  

- **数据结构**：我们只需要用 Python 的列表来保存当前数组的状态。  
- **生活化类比**：把数组想象成一排排小球，操作就是把**相邻的两颗小球一起拿走**，就像把两个相邻的棋子一起吃掉。  
- **为什么正确**：只要把所有可能的“拿走两颗相邻小球”的组合都尝试一遍，就一定能找到最少的组合（因为我们把所有情况都穷举了）。  
- **复杂度分析**：  
  - 对每一种可能的删除方式，我们都要检查删除后数组是否非递减，这一步是线性 `O(n)`（遍历一次数组）。  
  - 删除方式的数量是指数级的：每次可以选择是否把当前位置的相邻两个元素一起删除，等价于把 `n` 个位置划分成若干对或不划分，对 `n` 个位置的划分方式大约是 `2^{n/2}`，最坏情况下接近 `2^n`。  
  - 所以整体时间复杂度是 **指数级**，记作 `O(2^n)`。空间上我们只保存若干临时列表，最多 `O(n)`。

> **大白话**：`O(2^n)` 就像把一把钥匙复制了两倍、四倍、八倍……直到可以打开所有可能的门，数量会很快爆炸，实际运行几秒钟都来不及。

#### 代码（Python）

```python
from itertools import product
from copy import deepcopy

def is_non_decreasing(arr):
    """检查数组是否已经是非递减的"""
    for i in range(1, len(arr)):
        if arr[i] < arr[i - 1]:
            return False
    return True

def brute_min_operations(nums):
    n = len(nums)
    # 用二进制位表示每一对相邻元素是否被一起删除
    # 0 表示不删除，1 表示删除这对（下标 i 与 i+1）
    # 为了避免重叠删除，只在偶数位置决定是否删除 (i, i+1)
    best = float('inf')
    # 对每一种“是否删除每对相邻元素”的选择进行遍历
    for mask in product([0, 1], repeat=n // 2 + 1):
        # 复制一份原数组，模拟删除过程
        cur = deepcopy(nums)
        # 记录已经被删除的下标，防止二次删除同一个元素
        removed = [False] * n
        ops = 0
        # 从左到右检查每一对 (2*i, 2*i+1)
        for i in range(0, n - 1, 2):
            if mask[i // 2] == 1:
                # 若这对中任意一个已经被删除，则这组操作非法，直接跳过
                if removed[i] or removed[i + 1]:
                    break
                removed[i] = removed[i + 1] = True
                ops += 1
        # 构造删除后的数组
        remain = [cur[i] for i in range(n) if not removed[i]]
        if is_non_decreasing(remain):
            best = min(best, ops)

    return best if best != float('inf') else 0

# 示例
print(brute_min_operations([5, 2, 3, 1]))   # 2
print(brute_min_operations([1, 2, 2]))      # 0
```

> 关键行注释已在代码中给出。由于 `n ≤ 50`，暴力枚举在实际运行时会超时，仅作思路演示。

#### 复杂度

- **时间复杂度**：`O(2^n)` — 指数级增长，随着数组长度稍微增加，运行时间会呈指数级飙升，实际不可接受。
- **空间复杂度**：`O(n)` — 主要是存放临时的复制数组和标记数组。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **“每一次都把所有可能的删除方式都尝试一遍”**，而我们其实可以利用题目给出的**操作特性**——一次只能删除**相邻的两个元素**，来找出一种**数学上的等价简化**，从而把搜索空间从指数级压到多项式级。

**关键观察 1：删除相邻的两个元素会把后面的所有元素向左移动 2 位**。  
这相当于“把数组的奇偶位（下标的奇偶性）保持不变”。举个例子：

```
原数组下标 : 0 1 2 3 4 5
删除 (1,2)后: 0   3 4 5   （下标 3、4、5 向左移动了 2 位，仍然保持原来的奇偶性）
```

> **类比**：想象一排排书，一次只能把相邻的两本书一起搬走。搬走后，后面的书整体向左滑动两格，但每本书原来是站在左脚还是右脚上（奇偶），仍然不变。

**关键观察 2：因为每次删除的是**「**两个**」**，最终留下的元素个数必然和原数组同奇偶**（即 `n - 2 * ops`），所以**留下的所有元素的原下标** **必须全是偶数或全是奇数**。**  
换句话说，如果我们决定保留某些元素，使得剩下的数组已经非递减，那么这些保留元素在原数组中的位置**要么全是偶数，要么全是奇数**。

因此，问题可以转化为：

> 在原数组中，挑选出 **下标全为偶数** 或 **下标全为奇数** 的最长**非递减子序列**（不要求连续），保留它们，剩下的元素全部成对删除。  
> 操作次数 = `(n - length_of_longest_subseq) / 2`

**如何求最长非递减子序列（LNDS）？**  
数组长度最多 50，使用 **动态规划 O(n²)** 完全足够。

DP 思路（以偶数下标为例）：

```
dp[i] = 以 nums[i] 结尾的最长非递减子序列的长度（i 必须是偶数）
状态转移：
    dp[i] = 1                                          # 只保留自己
    for each j < i 且 j 同样是偶数:
        if nums[j] <= nums[i]:                         # 能保持非递减
            dp[i] = max(dp[i], dp[j] + 1)
```

对奇数下标同理，取两者的最大值 `best_len`。  
最后答案 = `(n - best_len) // 2`。

**复杂度对比**：  
- 暴力 `O(2^n)` → **最优 `O(n²)`**（约 2500 次循环），几乎瞬间完成。  
- 空间从指数级降到线性 `O(n)`（只需要一个 `dp` 数组）。

#### 代码（Python）

```python
def min_operations(nums):
    """
    返回使数组非递减所需的最少相邻两数删除次数。
    思路：找下标全为偶数或全为奇数的最长非递减子序列。
    """
    n = len(nums)

    def longest_nondecreasing(parity):
        """返回下标同为 parity（0 为偶数，1 为奇数）的最长非递减子序列长度"""
        dp = [0] * n          # dp[i] 只在 i%2 == parity 时有意义
        best = 0
        for i in range(parity, n, 2):   # 只遍历对应奇偶性的下标
            dp[i] = 1                   # 至少可以只保留自身
            for j in range(parity, i, 2):
                if nums[j] <= nums[i]: # 能保持非递减
                    dp[i] = max(dp[i], dp[j] + 1)
            best = max(best, dp[i])
        return best

    # 分别求偶数位和奇数位的最长非递减子序列
    best_len = max(longest_nondecreasing(0), longest_nondecreasing(1))

    # 其余元素全部成对删除，操作次数即为删除元素数的一半
    return (n - best_len) // 2


# ------------------- 测试 -------------------
print(min_operations([5, 2, 3, 1]))   # 2
print(min_operations([1, 2, 2]))      # 0
print(min_operations([4, 3, 2, 1]))   # 2  (保留奇数位 [3,1] 已非递减，删掉两对)
```

**代码要点注释**：

- `longest_nondecreasing(parity)`：只在给定奇偶性下做 DP，避免不必要的比较。  
- `dp[i] = 1`：表示即使前面没有可以接上的元素，自己也能单独成一个合法子序列。  
- `if nums[j] <= nums[i]`：确保子序列是 **非递减**（等号允许相等）。  
- `best_len` 取两种奇偶性的最大值，因为我们可以任选一种奇偶性来保留元素。  
- 最后 `(n - best_len) // 2`：剩余的元素全部成对删除，除以 2 正好得到操作次数。

#### 复杂度

- **时间复杂度**：`O(n²)` —— 两层循环遍历最多 50×50 = 2500 次，几乎是瞬时完成的。相比暴力的指数级，快得多。  
- **空间复杂度**：`O(n)` —— 只用到了长度为 `n` 的 `dp` 数组。

---

## 心得

- **核心技巧**：把“相邻两数删除”转化为“保留下标同奇偶的最长非递减子序列”。关键在于认识到每次删除两个相邻元素会保持 **奇偶性不变**，从而把原本的组合搜索问题化简为 **最长子序列** 问题。
- **适用的题型**  
  1. “最少操作使数组有序” 类似问题（如 *Minimum Deletions to Make Array Sorted*）。  
  2. 需要 **成对删除** 或 **成对操作** 的题目（如 *Minimum Pair Removal to Sort Array II*）。  
  3. 通过 **奇偶性/模 2** 约束来简化子序列/子集问题的场景。
- **一句话总结**：**“相邻成对删除 ≈ 固定奇偶位保留 → 用最长非递减子序列求解”。**

---

## 反思

- **第一反应**：直接模拟所有删除方式，想到要枚举每一次的操作序列。  
- **最容易踩的坑**  
  - 忽视 **奇偶性不变** 的关键约束，导致思路无法收敛。  
  - 误以为可以随意删除任意两个元素，而实际上只能删除 **相邻** 的两颗。  
  - 边界情况：空数组或已经非递减的数组，需要返回 `0`，而不是除以 2 出错。  
- **下次遇到同类题**：第一步先思考 **每一次操作对索引/结构的全局影响**（如奇偶性、相对顺序），再寻找能把操作约束转化为子序列/子集的经典问题。这样往往能把指数级搜索降到多项式时间。