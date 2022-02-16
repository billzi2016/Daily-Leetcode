# #1671. 最少删除元素使数组成为山脉数组 / Minimum Number of Removals to Make Mountain Array

> 难度：困难 · 标签：Array、Binary Search、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-number-of-removals-to-make-mountain-array/)

---

## 题目（英文原版）

**Description**

You may recall that an array arr is a mountain array if and only if:
Given an integer array nums​​​, return the minimum number of elements to remove to make nums​​​ a mountain array.

**Examples**

**Example 1:**

```
Input: nums = [1,3,1]
Output: 0
Explanation: The array itself is a mountain array so we do not need to remove any elements.
```

**Example 2:**

```
Input: nums = [2,1,1,5,6,2,3,1]
Output: 3
Explanation: One solution is to remove the elements at indices 0, 1, and 5, making the array nums = [1,5,6,3,1].
```

**Constraints**

- 3 <= nums.length <= 1000
- 1 <= nums[i] <= 109
- It is guaranteed that you can make a mountain array out of nums.

---

## 题目（中文翻译）

你可能还记得，只有满足以下条件的数组 `arr` 才称为山脉数组（mountain array）：
1. `arr.length >= 3`；
2. 存在一个下标 `i`（`0 < i < arr.length - 1`），使得  
   - `arr[0] < arr[1] < ... < arr[i]`（严格递增），且  
   - `arr[i] > arr[i + 1] > ... > arr[arr.length - 1]`（严格递减）。

给定一个整数数组 `nums`，返回为了使 `nums` 成为山脉数组而需要删除的最少元素个数。

**示例 1**  
输入：`nums = [1,3,1]`  
输出：`0`  
解释：数组本身已经是山脉数组，无需删除任何元素。

**示例 2**  
输入：`nums = [2,1,1,5,6,2,3,1]`  
输出：`3`  
解释：一种可行的方案是删除下标为 `0、1、5` 的元素，使得数组变为 `nums = [1,5,6,3,1]`，此时它是山脉数组。

**约束条件**  
- `3 <= nums.length <= 1000`  
- `1 <= nums[i] <= 10^9`  
- 保证一定可以通过删除元素得到一个山脉数组。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的山形子序列都列举出来**，然后找出最长的那一个，剩下的元素就是要删除的最少数量。  
这类似于我们在玩“挑选卡片”游戏：把原数组的每个元素看成一张卡，**要么保留，要么丢掉**，所有的保留组合就是所有子序列。  

要判断一个子序列是不是山形，需要满足：

1. 长度至少为 3（山必须有左坡、峰、右坡）。  
2. 先严格递增，然后严格递减。  

如果我们直接遍历 **2ⁿ**（n 为数组长度）种子序列，时间会爆炸。  
在这里，我们把“暴力”稍微收敛一点：**固定山峰的位置**，分别求左侧的最长严格递增子序列（LIS），右侧的最长严格递减子序列（LDS），把两者拼在一起就是以该位置为峰的最长山形。  

实现时可以使用 **动态规划（DP）**：

- `inc[i]`：以 `i` 为结尾的最长递增子序列的长度。  
- `dec[i]`：以 `i` 为起点的最长递减子序列的长度（可以把数组反过来再跑一次 LIS）。  

遍历所有 `i`（除去首尾，因为山峰不能在两端），计算 `inc[i] + dec[i] - 1`（峰算了两次），取最大值 `max_len`，答案即 `n - max_len`（删掉其余的元素）。

> **为什么正确？**  
> 对于任意山形子序列，它的峰一定是原数组中的某个位置 `i`。左边的所有保留下来的元素必须构成一个递增序列，右边的所有保留下来的元素必须构成一个递减序列。因此，若我们在每个可能的 `i` 处取左侧最长递增和右侧最长递减，它们的拼接一定不比真实的山形子序列短，从而能够得到全局最长的山形子序列。

> **时间/空间复杂度的大白话**  
> - `O(n²)`：想象有 `n` 位同学排成一列，每位同学要检查自己左边的所有同学（最坏情况是 `n` 次），于是总检查次数是 `n × n`，即 “n 的平方”。  
> - `O(n)`：我们只需要两个长度为 `n` 的数组来记录 DP 值，空间随 `n` 线性增长。

#### 代码（Python）

```python
from typing import List

def min_removals_brutal(nums: List[int]) -> int:
    n = len(nums)
    # inc[i]：以 i 为结尾的最长严格递增子序列长度
    inc = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                # 如果 j 能接到 i，看看能否把长度拉长
                inc[i] = max(inc[i], inc[j] + 1)

    # dec[i]：以 i 为起点的最长严格递减子序列长度
    dec = [1] * n
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if nums[j] < nums[i]:
                dec[i] = max(dec[i], dec[j] + 1)

    max_len = 0  # 记录最长山形子序列的长度
    for i in range(1, n - 1):          # 峰不能在两端
        if inc[i] > 1 and dec[i] > 1:  # 两边都要有递增/递减才能构成山
            max_len = max(max_len, inc[i] + dec[i] - 1)

    # 删除的最少元素数 = 总长度 - 最长山形子序列的长度
    return n - max_len
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 两层循环，每层最多遍历 `n` 次，类似“每个人检查所有前面的人”。  
- **空间复杂度**：`O(n)` — 只用了两个长度为 `n` 的数组 `inc`、`dec`。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **两个嵌套循环**，导致每个位置的 LIS/ LDS 都要重新遍历一次。  
我们可以把求 LIS 的过程 **加速到 `O(log n)`**，从而把整体时间降到 `O(n log n)`。这就是**“耐心排序（Patience Sorting）”**或**二分查找**的技巧。

**核心步骤**：

1. **一次遍历得到左侧 LIS 长度**  
   - 维护一个列表 `tails`，`tails[k]` 保存长度为 `k+1` 的递增子序列的最小可能结尾值。  
   - 对每个 `num`，在 `tails` 中二分查找第一个 **≥ num** 的位置 `idx`，把 `tails[idx] = num`。  
   - `idx+1` 就是以当前位置结尾的 LIS 长度，记录到 `inc[i]`。  
   - 类比：把 `tails` 想象成 **书架**，每本书代表一种长度的递增序列，放在最左边的空位（最小的结尾）能让以后放更多书。

2. **一次遍历得到右侧 LDS 长度**  
   - 把数组反转后，同样用上面的 **LIS** 方法得到 `rev_inc`（即从右往左的递增长度），这正好等价于原数组的 **递减长度**。  
   - 把 `rev_inc` 再反转回来，得到 `dec[i]`。

3. **合并**  
   - 对每个可能的峰 `i`（`1 ≤ i ≤ n-2`），如果 `inc[i] > 1` 且 `dec[i] > 1`，则山形长度为 `inc[i] + dec[i] - 1`。  
   - 取最大值 `max_len`，答案 `n - max_len`。

> **为什么二分可以加速？**  
> `tails` 始终保持递增序列，二分查找在有序数组里找位置的时间是 `log n`。每个元素只处理一次，所以整体是 `n·log n`。

> **时间/空间的大白话**  
> - `O(n log n)`：想象有 `n` 本书要放进书架，每本书找位置用“二分查找”只需要约 `log₂ n` 次比较。整体工作量是 “n 本 × log n 次”，比 “n² 次” 少很多。  
> - `O(n)`：我们仍然需要两个长度为 `n` 的数组来记录每个位置的 LIS/LDS 长度。

#### 代码（Python）

```python
from bisect import bisect_left
from typing import List

def min_removals(nums: List[int]) -> int:
    n = len(nums)

    # ---------- 求左侧 LIS 长度 ----------
    inc = [0] * n               # inc[i] = 以 i 为结尾的 LIS 长度
    tails = []                  # tails[k] = 长度为 k+1 的递增子序列的最小结尾
    for i, x in enumerate(nums):
        # 在 tails 中二分找第一个 >= x 的位置
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)    # 没找到，说明可以把长度加 1
        else:
            tails[idx] = x      # 用更小的结尾来更新
        inc[i] = idx + 1        # LIS 长度就是 idx+1

    # ---------- 求右侧 LDS 长度（等价于反向的 LIS） ----------
    rev = nums[::-1]            # 反转数组
    rev_inc = [0] * n
    tails.clear()
    for i, x in enumerate(rev):
        idx = bisect_left(tails, x)
        if idx == len(tails):
            tails.append(x)
        else:
            tails[idx] = x
        rev_inc[i] = idx + 1
    dec = rev_inc[::-1]         # 把结果再翻回来，对应原数组的 LDS

    # ---------- 合并得到最长山形 ----------
    max_len = 0
    for i in range(1, n - 1):   # 峰不能在两端
        if inc[i] > 1 and dec[i] > 1:   # 两侧都要有递增/递减
            max_len = max(max_len, inc[i] + dec[i] - 1)

    # 需要删除的元素数 = 总长度 - 最长山形子序列长度
    return n - max_len
```

#### 复杂度

- **时间复杂度**：`O(n log n)` — 每个元素在 `tails` 中二分搜索一次，代价是 `log n`，共 `n` 次。  
- **空间复杂度**：`O(n)` — 需要 `inc`、`dec` 两个长度为 `n` 的数组以及 `tails`（最多 `n` 长）。

---

## 心得  

- **核心技巧**：把 “把数组变成山形” 这件事转化为 “在原数组中找最长的山形子序列”。最长子序列可以用 **LIS（最长递增子序列）** 的思想求解，左侧递增、右侧递减分别对应两个 LIS。  
- **适用的题型**  
  1. “最长递增子序列”（LeetCode 300）  
  2. “最长递减子序列”或 “最长波浪序列”  
  3. “删除最少元素使数组严格递增/递减”（类似 1909）  
- **一句话总结**：**把“删”变“保”，先求最长山形子序列，再用 `n - 长度` 得到最少删除数**。

---

## 反思  

- **第一反应**：看到 “删除最少元素” 立刻想到 “保留下最长合法子序列”。  
- **最容易踩的坑**  
  - 峰不能在数组两端，必须保证左、右两侧都有长度大于 1 的递增/递减序列。  
  - 使用 `bisect_left` 时要记得 **严格递增**，所以要找第一个 `≥` 而不是 `>`。  
  - 反转数组求 LDS 时，别忘了把结果再翻回来对应原下标。  
- **下次遇到同类题**：第一步先 **把问题从 “删除” 转化为 “保留最长合法子序列”**，然后判断是否可以利用 LIS / DP / 二分等已有工具进行加速。