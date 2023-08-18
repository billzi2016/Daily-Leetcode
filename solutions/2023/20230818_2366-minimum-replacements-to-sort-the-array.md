# #2366. 最少替换次数使数组有序 / Minimum Replacements to Sort the Array

> 难度：困难 · 标签：Array、Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-replacements-to-sort-the-array/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed integer array nums. In one operation you can replace any element of the array with any two elements that sum to it.
Return the minimum number of operations to make an array that is sorted in non-decreasing order.

**Examples**

**Example 1:**

```
Input: nums = [3,9,3]
Output: 2
Explanation: Here are the steps to sort the array in non-decreasing order:
- From [3,9,3], replace the 9 with 3 and 6 so the array becomes [3,3,6,3]
- From [3,3,6,3], replace the 6 with 3 and 3 so the array becomes [3,3,3,3,3]
There are 2 steps to sort the array in non-decreasing order. Therefore, we return 2.
```

**Example 2:**

```
Input: nums = [1,2,3,4,5]
Output: 0
Explanation: The array is already in non-decreasing order. Therefore, we return 0.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= nums[i] <= 109

---

## 题目（中文翻译）

给定一个 **0-indexed** 整数数组 **nums（array）**。在一次 **操作（operation）** 中，你可以将数组中的任意 **元素（element）** 替换为任意两个 **和等于该元素** 的新元素。返回使数组按 **非递减顺序（non-decreasing order）** 排序所需的最少操作次数。

**示例 1**

``` 
Input: nums = [3,9,3]
Output: 2
Explanation: 以下是将数组排序为非递减顺序的步骤：
- 从 [3,9,3] 开始，将 9 替换为 3 和 6，数组变为 [3,3,6,3]；
- 从 [3,3,6,3] 开始，将 6 替换为 3 和 3，数组变为 [3,3,3,3,3]。
共需要 2 步将数组排序为非递减顺序。因此返回 2。
```

**示例 2**

``` 
Input: nums = [1,2,3,4,5]
Output: 0
Explanation: 数组已经是非递减顺序，无需任何操作。返回 0。
```

**约束条件**

- 1 ≤ nums.length ≤ 10⁵
- 1 ≤ nums[i] ≤ 10⁹

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的拆分方式**，把每个元素拆成若干个正整数，使得最终得到的序列是非递减的，然后取操作次数最少的方案。  
可以把「把一个数拆成两个数」看成「把一本书拆成两本更薄的书」——每次拆分后，书的总页数不变，只是把一本厚书变成两本薄书。  
如果把所有拆分过程写成一棵树，根节点是原数组，叶子节点是最终满足排序要求的数组。我们只要在这棵树中找到**叶子节点的最小深度**（即最少操作次数）即可。

为什么这个方法是正确的？  
- 只要把每一步合法的拆分都尝试到，就一定能覆盖所有可能的最终数组。  
- 只要最终数组满足非递减条件，就算是一种可行解。  

然而，这种 **全枚举** 的搜索空间非常大：每个大于 1 的数都有无数种拆分方式，深度也可能很大。对长度 `n` 为 10⁵ 的数组根本不可行，甚至对 `n=10`、数值在 100 左右的情况也会超时。  

#### 代码（Python）  

下面的实现仅用于演示「暴力搜索」的思路，**仅适用于 n ≤ 10、数值 ≤ 20 的极小输入**。它使用递归 DFS，尝试把当前元素拆成两部分，然后继续往后拆。  

```python
def brute_min_operations(nums):
    """
    暴力搜索最少操作数（仅适用于极小规模的测试）。
    思路：深度优先遍历所有拆分方式，记录满足非递减的最小操作数。
    """
    from math import inf

    best = inf                     # 全局最小操作次数

    def dfs(idx, prev, ops, cur_arr):
        """
        idx   : 正在处理的下标
        prev  : 前一个数的最大允许值（为保证非递减）
        ops   : 已经使用的操作次数
        cur_arr: 当前数组（仅用于调试，可省略）
        """
        nonlocal best
        # 剪枝：已经超过已知最优解，无需继续
        if ops >= best:
            return
        # 已经处理完所有元素，更新最优解
        if idx == len(nums):
            best = min(best, ops)
            return

        val = nums[idx]
        # 情况一：不拆分，直接放入（前提是不破坏非递减）
        if val <= prev:
            dfs(idx + 1, val, ops, cur_arr + [val])
        # 情况二：拆分成两部分（a, b），要求 a + b = val 且 a <= b
        # 为了避免无限递归，只尝试 a 从 1 到 val//2
        for a in range(1, val // 2 + 1):
            b = val - a
            # 拆分一次后，等价于在原数组中插入 a、b 两个元素
            # 这里把 a 当作当前位，b 作为后面的“待处理”元素
            if a <= prev:                     # a 必须不大于前一个数
                # 先把 a 放进去，b 作为下一个要处理的数
                # 为了继续拆分 b，需要把它放到 nums 的后面
                # 这里用临时列表模拟插入
                new_nums = nums[:idx] + [a, b] + nums[idx+1:]
                # 递归继续处理新数组（从下一个位置开始）
                dfs(idx + 1, a, ops + 1, cur_arr + [a])
                # 注意：真正实现需要把 b 再次加入待拆分队列，这里为了简化省略
                # 完整实现相当复杂，故此代码仅作概念展示
                break   # 为了防止指数爆炸，这里只尝试最小的 a

    dfs(0, float('inf'), 0, [])
    return -1 if best == inf else best
```

> **重要提示**：上述代码仅用于说明「暴力枚举」的思路，**在实际面试或线上评测中绝对不可用**，因为它会在稍大一点的输入上立刻卡死。

#### 复杂度  

- **时间复杂度**：`O(爆炸性增长)`，在最坏情况下几乎是指数级（类似 `O(2^n)`），因为每个大于 1 的数都有多种拆分方式，需要遍历全部组合。  
- **空间复杂度**：`O(n)` 用于递归栈和临时数组，同样会随递归深度指数增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**关键的瓶颈在于每次都要尝试所有可能的拆分**。实际上我们并不需要穷举，**只要把每个元素尽可能“少拆”且仍然保持非递减顺序，就一定是最优的**。  

下面一步步推导出最简洁的贪心算法：

1. **永远不要拆最后一个元素**  
   - 最后一个元素没有右侧的约束，只要它本身不小于前面的数就已经满足非递减。拆它只会增加操作次数，却不帮助排序。  

2. **从右往左遍历**  
   - 假设我们已经处理好了下标 `i+1 … n-1`，并且它们已经是非递减的。我们只需要保证 `nums[i] ≤ nums[i+1]`（这里的 `nums[i+1]` 实际上是**经过拆分后**的最大值，记作 `bound`）。  

3. **如果 `nums[i] ≤ bound`**，直接把 `bound` 更新为 `nums[i]`，不需要任何操作。  

4. **如果 `nums[i] > bound`**，我们必须把它拆成若干块，使得每块 **不大于 `bound`**。  
   - 为了让操作次数最少，我们希望 **每块尽可能大**（这样块数最少）。  
   - 设要把 `nums[i]` 拆成 `k+1` 块（即需要 `k` 次操作），每块的最大值为 `⌊ nums[i] / (k+1) ⌋`。  
   - 为了让块的大小 ≤ `bound`，我们需要 `⌊ nums[i] / (k+1) ⌋ ≤ bound`，即 `k+1 ≥ ceil( nums[i] / bound )`。  
   - 因此 **最小的 `k`** 为 `ceil( nums[i] / bound ) - 1`。  

5. **更新**  
   - 操作次数累计 `ans += k`。  
   - 拆分后，这些块的大小都相同（或者相差 1），最大的块大小就是 `⌊ nums[i] / (k+1) ⌋`，这也将成为新的 `bound`，供左侧元素使用。  

整个过程只需要一次线性遍历，时间 O(n)，空间 O(1)。  

> **类比**：把数组看成一排高度不一的箱子，我们希望把它们重新堆叠成从左到右“高度不升”的形状。只能把箱子切成更小的箱子，且切完后左边的箱子高度不能超过右边的箱子。最好的办法是从右边的箱子开始，决定左边箱子能保留多大的高度——这正是贪心的核心。

#### 代码（Python）  

```python
import math
from typing import List

def min_replacements(nums: List[int]) -> int:
    """
    贪心算法：从右往左保证非递减，只在必要时拆分，
    每次拆分尽可能让子块保持最大（即最少拆分次数）。
    """
    n = len(nums)
    # bound 表示当前右侧已经处理好的最小“上界”，初始化为最右侧元素
    bound = nums[-1]
    ans = 0                     # 累计的最小操作次数

    # 从倒数第二个元素向左遍历
    for i in range(n - 2, -1, -1):
        cur = nums[i]

        if cur <= bound:
            # 已经不大于右侧上界，直接更新 bound 为当前值
            bound = cur
            continue

        # 需要拆分：求最少的拆分次数 k，使得每块 ≤ bound
        # 先算出需要的块数（k+1），向上取整
        pieces = math.ceil(cur / bound)        # 块数 = k + 1
        k = pieces - 1                         # 实际操作次数

        ans += k                               # 累加操作次数

        # 拆分后每块的最大值，即新的 bound
        # 这里使用整除得到每块的大小（所有块大小相等或相差 1，最大块即 floor)
        bound = cur // pieces                  # 等价于 floor(cur / (k+1))

    return ans
```

**代码要点解释**  

- `bound = nums[-1]`：最后一个元素永远不拆，直接作为右侧的基准。  
- `if cur <= bound:`：如果当前元素已经不大于右侧基准，直接把基准缩小到当前值，**不需要任何操作**。  
- `pieces = math.ceil(cur / bound)`：计算把 `cur` 拆成多少块才能让每块 ≤ `bound`（向上取整）。  
- `k = pieces - 1`：拆成 `pieces` 块需要的操作次数是 `pieces-1`（每次把一个数拆成两块）。  
- `bound = cur // pieces`：拆完后，每块的最大可能大小就是 `cur // pieces`（向下取整），这将作为左侧元素的上界。  

#### 复杂度  

- **时间复杂度**：`O(n)`。只遍历一次数组，每一步的计算都是常数时间。  
  - 与暴力解的指数级时间相比，线性时间在 `n=10⁵` 时毫秒级可跑完。  
- **空间复杂度**：`O(1)`。只使用了几个整数变量，不随 `n` 增长。  

---

## 心得  

- **核心技巧**：从右往左的**贪心** + **向上取整** 计算最少块数。  
- **适用题型**：  
  1. “把数组拆成若干块，使整体满足某种单调性”——如 *Minimum Number of Operations to Make Array Continuous*。  
  2. “每次操作只能把一个数分成两个数”，需要控制**每块的上界**——如本题。  
  3. “在限制条件下最少分割次数”——如 *Split Array Largest Sum*（思路类似的二分/贪心）。  
- **一句话总结**：**只要从右侧已确定的上界出发，尽可能少拆、让每块尽量大，就是最优的**。

---

## 反思  

- **第一反应**：看到“把一个数换成两个和为它的数”，立刻想到递归或 BFS 暴力搜索。  
- **最容易踩的坑**：  
  - 忘记 **不拆最后一个元素**，导致不必要的额外操作。  
  - 计算块数时使用整除而不是向上取整，会少算一次拆分，导致结果不正确。  
  - 当 `bound` 为 0（不可能出现，因为 `nums[i] ≥ 1`），但如果忘记检查会出现除零错误。  
- **下次类似题的第一步**：先**确定约束的方向**（是左约束还是右约束），然后**从有约束的一端逆向遍历**，用**向上取整**算最少的“分割次数”。这样往往能直接得到 O(n) 的贪心解。