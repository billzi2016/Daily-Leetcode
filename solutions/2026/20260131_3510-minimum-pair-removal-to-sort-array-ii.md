# #3510. 最小成对删除使数组有序 II / Minimum Pair Removal to Sort Array II

> 难度：困难 · 标签：Array、Hash Table、Linked List、Heap (Priority Queue)、Simulation、Doubly-Linked List、Ordered Set · [LeetCode 链接](https://leetcode.com/problems/minimum-pair-removal-to-sort-array-ii/)

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

- 1 <= nums.length <= 105
- -109 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个数组 `nums`，你可以任意次数地执行以下操作：  

返回使数组非递减所需的最少操作次数。  
如果数组中每个元素都大于或等于其前一个元素（如果前一个元素存在），则称该数组为非递减的。  

**示例 1**  

**示例 2**  

**约束条件**  

**示例**  

**示例 1:**  
输入: `nums = [5,2,3,1]`  
输出: `2`  
解释:  
数组 `nums` 在两次操作后变为非递减。  

**示例 2:**  
输入: `nums = [1,2,2]`  
输出: `0`  
解释:  
数组 `nums` 已经是有序的。  

**约束条件:**  
- `1 <= nums.length <= 10^5`  
- `-10^9 <= nums[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的删除方案**，找出其中最少的删除次数，使剩下的数组已经是非递减的。  
可以把每一次“删除”看成把数组里的一条“记录”——**下标 + 数值**——从数组中摘掉，这和把一本字典里不需要的词条（下标）和对应的解释（数值）撕掉是一样的概念。  

实现思路：

1. 用一个二进制掩码 `mask`（长度等于 `len(nums)`）表示哪些位置被保留，哪些被删除。  
2. 对每一种 `mask`，把保留下来的数按原顺序重新拼成一个新数组 `arr`。  
3. 检查 `arr` 是否已经是非递减的（即 `arr[i] <= arr[i+1]` 对所有合法 `i` 成立）。  
4. 记录满足条件的 `mask` 中 **被删除的元素个数** 最小值，即为答案。

> **为什么一定能得到正确答案？**  
> 因为我们穷举了**所有**可能的删除方式，必然会覆盖最优的那一种。只要在遍历过程中找到一组合法且删除最少的方案，就一定是全局最优。

> **时间/空间复杂度**  
> - 时间复杂度：`O(2^n * n)`。  
>   `2^n` 是所有掩码的数量，`n` 是每次检查数组是否有序要遍历一次的代价。  
>   用大白话说，就是“当数组长度稍微大一点（比如 20）时，计算量就像把 1 048 576（≈一百万）份作业都批改一遍”。  
> - 空间复杂度：`O(n)`。只需要额外存放一个临时数组 `arr`。

> 由于 `n` 最多可达 `10^5`，暴力枚举根本不可行，只能用来帮助我们**理清问题**，后面再寻找更快的办法。

#### 代码（Python）

```python
from itertools import product

def min_operations_bruteforce(nums):
    n = len(nums)
    best = n                     # 最坏情况：全部删掉
    # 0 表示删除，1 表示保留
    for mask in product([0, 1], repeat=n):
        # 计算被删除的个数，若已经不比当前 best 好，就直接跳过
        deletions = mask.count(0)
        if deletions >= best:
            continue

        # 生成保留下来的子序列
        kept = [nums[i] for i in range(n) if mask[i] == 1]

        # 检查是否已经是非递减的
        ok = all(kept[i] <= kept[i + 1] for i in range(len(kept) - 1))
        if ok:
            best = deletions          # 找到更小的答案

    return best
```

> **关键行注释**  
> - `product([0, 1], repeat=n)`：像在字典里挑词一样，遍历所有“保留/删除”的组合。  
> - `mask.count(0)`：统计本次组合中要删除多少个元素。  
> - `all(kept[i] <= kept[i + 1] ...)`：检查新数组是否已经排好序。

#### 复杂度

- **时间复杂度**：`O(2^n * n)` —— 指数级增长，`n` 稍大就会爆炸。  
- **空间复杂度**：`O(n)` —— 只用一个临时列表保存保留下来的元素。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：**我们只关心保留下来的子序列是否有序**，而不必真的去“删”元素。  
如果我们能直接求出 **最长的非递减子序列（Longest Non‑decreasing Subsequence，简称 LNDS）** 的长度 `L`，那么只需要把其余的 `n - L` 个元素删掉即可得到有序数组。  

> **瓶颈在哪里？**  
> 暴力枚举的核心是“尝试所有保留方式”，这一步的时间是指数级的。  
> 实际上，只要知道最长的合法子序列有多长，就能直接算出最少要删多少——**不必枚举**。

> **优化思路**  
> 1. **把问题转化为 LNDS**：  
>    - “保留下来的元素要保持原来相对顺序且非递减” 正好是 **子序列** 的定义。  
>    - “尽量少删” 等价于 “保留尽可能多”。  
>    - 因此 **答案 = n - (最长非递减子序列的长度)**。  
> 2. **用“耐心排序”求 LNDS**：  
>    - 这是一种 **二分查找 + 贪心** 的技巧，时间 `O(n log n)`，空间 `O(n)`。  
>    - 思路类似把扑克牌按从小到大摆成若干堆，每张牌只放在左边第一张比它大的牌上面。最终堆的数量就是最长递增子序列的长度。  
>    - 对非递减序列，只需要把“>” 换成 “≥” 即可。  

> **核心数据结构**  
> - **列表 `tails`**：`tails[i]` 保存长度为 `i+1` 的非递减子序列的最小可能结尾值。  
>   把它想象成“每一种长度的最小尾巴”，就像在字典里查词时，只记住每个词首字母对应的最短单词。  
> - **二分查找**（`bisect_right`）：在 `tails` 中快速定位可以放置当前数字的位置。  

> **一步步演示**（以 `nums = [5, 2, 3, 1]` 为例）  
> 1. `tails = []`（空）  
> 2. 处理 `5`：没有比 `5` 更大的尾巴，直接在末尾追加 → `tails = [5]`（长度 1）  
> 3. 处理 `2`：在 `tails` 中找到第一个 **>** `2` 的位置（这里是 `0`），用 `2` 替换 → `tails = [2]`（仍然长度 1）  
> 4. 处理 `3`：`3` 大于所有尾巴，追加 → `tails = [2, 3]`（长度 2）  
> 5. 处理 `1`：替换 `tails[0]` → `tails = [1, 3]`（长度仍是 2）  
> 最终 `len(tails) = 2`，说明最长非递减子序列长度为 2，最少要删 `4 - 2 = 2` 次。  

> 这正好对应示例的答案。

#### 代码（Python）

```python
import bisect

def min_operations(nums):
    """
    返回使数组非递减所需的最少删除次数。
    思路：答案 = n - 最长非递减子序列的长度（LNDS）。
    """
    tails = []                     # tails[i] = 长度为 i+1 的非递减子序列的最小结尾值

    for x in nums:
        # 在 tails 中找到第一个 > x 的位置（因为要非递减，等于也可以保留）
        # 使用 bisect_right 可以让等于 x 的元素放在右侧，从而实现 “非递减”
        idx = bisect.bisect_right(tails, x)

        if idx == len(tails):
            # 没有更大的尾巴，直接在末尾创建新长度的子序列
            tails.append(x)
        else:
            # 用更小的结尾值替换，保证后续扩展的可能性更大
            tails[idx] = x

    longest = len(tails)          # LNDS 的长度
    return len(nums) - longest    # 需要删除的最少元素个数
```

> **关键行注释**  
> - `bisect.bisect_right(tails, x)`：在已排好序的 `tails` 中，找到**最右侧**可以插入 `x` 的位置，相当于“找第一个严格大于 `x` 的位置”。这保证了子序列是 **非递减**（允许相等）。  
> - `if idx == len(tails): tails.append(x)`：如果 `x` 大于所有已有的结尾，说明可以把它放在最长子序列的后面，子序列长度 +1。  
> - `tails[idx] = x`：否则，用更小的结尾值代替，提升后面继续扩展的机会。

#### 复杂度

- **时间复杂度**：`O(n log n)`。  
  - 每个元素进行一次二分查找，查找的代价是 `log n`，共 `n` 次。  
  - 用大白话说，就是“把 100 000 个数字一次放进有序的抽屉里，每次找抽屉位置只需要翻几页（约 17 页）”，远比暴力的“一次翻遍所有抽屉”快得多。  
- **空间复杂度**：`O(n)`（实际只需要 `O(L)`，`L` 为 LNDS 长度 ≤ n）。  
  - 只保存 `tails` 列表，最多和原数组等长。

---

## 心得

- **核心技巧**：把“最少删除使数组有序”转化为“**最长非递减子序列**的长度”，再用 **耐心排序 + 二分查找** 在 `O(n log n)` 内求解。  
- **适用的题型**  
  1. *Minimum Deletions to Make Array Sorted*（删除最少元素使数组递增）  
  2. *Longest Increasing Subsequence*（求最长递增子序列）  
  3. *Make Array Non-decreasing by Removing Elements*（类似的删除/保留类问题）  
- **一句话总结解题钥匙**：**把“删多少”换算成“保多少”，然后用 LNDS 的 O(n log n) 方法直接算出最大可保留的元素数**。

---

## 反思

- **第一反应**：看到“最少操作使数组非递减”，本能地想到“把不符合顺序的元素一个一个删掉”。于是尝试了全枚举的暴力思路。  
- **最容易踩的坑**  
  - **忽视“非递减”而误写成“递增”**：两者的区别在于相等的元素是否允许保留，使用错误的二分函数（`bisect_left`）会把相等的情况当成逆序，导致答案偏大。  
  - **忘记考虑空数组或全已排序的情况**：代码必须在 `tails` 为空时正常工作，返回 `0` 删除次数。  
  - **误以为每次只能删除相邻元素**，从而写出复杂的链表/堆模拟，实际只需要一次遍历即可。  
- **下次遇到同类题**：第一步先**把问题抽象为“最长（非）递减子序列”，检查是否可以直接用 LNDS/ LIS 的已知 O(n log n) 解法；如果还能进一步简化（比如只允许删除相邻），再考虑更细粒度的贪心或双指针。