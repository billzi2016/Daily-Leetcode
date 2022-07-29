# #1877. 数组中最小化最大配对和 / Minimize Maximum Pair Sum in Array

> 难度：中等 · 标签：Array、Two Pointers、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimize-maximum-pair-sum-in-array/)

---

## 题目（英文原版）

**Description**

The pair sum of a pair (a,b) is equal to a + b. The maximum pair sum is the largest pair sum in a list of pairs.
Given an array nums of even length n, pair up the elements of nums into n / 2 pairs such that:
Return the minimized maximum pair sum after optimally pairing up the elements.

**Examples**

**Example 1:**

```
Input: nums = [3,5,2,3]
Output: 7
Explanation: The elements can be paired up into pairs (3,3) and (5,2).
The maximum pair sum is max(3+3, 5+2) = max(6, 7) = 7.
```

**Example 2:**

```
Input: nums = [3,5,4,2,4,6]
Output: 8
Explanation: The elements can be paired up into pairs (3,5), (4,4), and (6,2).
The maximum pair sum is max(3+5, 4+4, 6+2) = max(8, 8, 8) = 8.
```

**Constraints**

- n == nums.length
- 2 <= n <= 105
- n is even.
- 1 <= nums[i] <= 105

---

## 题目（中文翻译）

配对和（pair sum）指一对元素 \((a, b)\) 的和，即 \(a + b\)。在若干对中，**最大配对和（maximum pair sum）** 是所有配对和的最大值。  
给定一个长度为偶数 \(n\) 的数组 `nums`，请将其中的元素两两配对，形成 \(n / 2\) 对，使得 **最大配对和** 最小化。  
返回在最优配对方式下得到的最小的 **最大配对和**。

### 示例

#### 示例 1
**输入**：`nums = [3,5,2,3]`  
**输出**：`7`  
**解释**：可以将元素配对为 \((3,3)\) 和 \((5,2)\)。  
最大配对和为 \(\max(3+3, 5+2) = \max(6, 7) = 7\)。

#### 示例 2
**输入**：`nums = [3,5,4,2,4,6]`  
**输出**：`8`  
**解释**：可以将元素配对为 \((3,5)\)、\((4,4)\) 和 \((6,2)\)。  
最大配对和为 \(\max(3+5, 4+4, 6+2) = \max(8, 8, 8) = 8\)。

### 约束条件
- `n == nums.length`
- \(2 \le n \le 10^5\)
- `n` 为偶数
- \(1 \le \text{nums}[i] \le 10^5\)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接、最笨的想法是 **把所有可能的配对方式都枚举一遍**，  
对每一种配对方式：

1. 计算每一对的和 `a + b`。  
2. 取这些和的最大值 → 这就是该配对方式的 “最大配对和”。  
3. 在所有配对方式的最大配对和中找最小的那个，即为答案。

> **数据结构类比**：  
> 这里的“配对方式”可以想象成把一堆袜子两两配对。要找出“最舒适的配对”（即最大和最小），只能把每一种配法都列出来试一遍，就像把所有可能的袜子配对方案都写在纸上再逐个检查。

> **为什么它是正确的**：  
> 只要把 **所有** 合法配对方式都考虑到了，必然能找到使最大配对和最小的那一种。因此，这种穷举法必然得到正确答案。

> **复杂度分析（大白话）**：  
> - **时间**：配对的方式数量随数组长度呈指数增长。设数组长度为 `n（偶数）`，配对的种数是 `(n‑1)!! = (n‑1)*(n‑3)*…*1`，大约是 `O(n·2^{n})` 级别的，换句话说，元素稍多（比如 20）就已经跑不动了。  
> - **空间**：递归过程中需要保存已经配好的元素，最坏情况下要保存 `n/2` 对，所以是 `O(n)`。

#### 代码（Python）

```python
from typing import List

def min_max_pair_sum_bruteforce(nums: List[int]) -> int:
    """
    暴力枚举所有配对方式，返回最小的「最大配对和」。
    仅用于说明思路，实际会超时。
    """
    n = len(nums)
    used = [False] * n          # 标记哪些元素已经被配对
    best = float('inf')         # 当前找到的最小的「最大配对和」

    def backtrack(cur_max: int):
        """递归搜索配对方案，cur_max 为当前已配对对的最大和"""
        nonlocal best
        # 剪枝：如果已经超过目前最好的答案，直接返回
        if cur_max >= best:
            return
        # 找到第一个未使用的下标 i
        try:
            i = used.index(False)
        except ValueError:      # 所有元素都已经配对完
            best = min(best, cur_max)
            return

        used[i] = True
        # 把 i 与后面的每个未使用的元素 j 配对
        for j in range(i + 1, n):
            if not used[j]:
                used[j] = True
                pair_sum = nums[i] + nums[j]
                backtrack(max(cur_max, pair_sum))  # 更新当前配对的最大和
                used[j] = False
        used[i] = False

    backtrack(0)
    return best
```

> **关键行中文注释**  
> - `used = [False] * n`：像“是否已经穿好袜子”一样记录每个位置是否已被配对。  
> - `if cur_max >= best: return`：如果当前已经出现的最大和已经不比已知最优小，就可以提前放弃这条搜索枝，省点时间。  
> - `pair_sum = nums[i] + nums[j]`：计算一对的和。  
> - `backtrack(max(cur_max, pair_sum))`：把这对的和和之前的最大和取较大，传递给下一层递归。

#### 复杂度

- **时间复杂度**：`O((n‑1)!!)`（约等于 `O(n·2^{n})`）——随着 `n` 增大呈指数级爆炸，实际只能在 `n≤10` 左右的小样例跑通。  
- **空间复杂度**：`O(n)`——递归栈深度最多 `n/2`，加上 `used` 数组。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**枚举所有配对方式是最慢的环节**——  
我们每次都要在大量不必要的组合中寻找最优解。  
要把时间压到可接受的范围，需要 **直接构造最优的配对方式**，而不是去尝试所有可能。

**关键观察**：

1. **最大配对和受最大的那一对主导**。如果我们能让最大的数和尽可能小的数配对，就能降低这唯一的“大数”。  
2. 同理，第二大的数如果和第二小的数配对，也能把它的和压得不高。  
3. 于是一个直观的配对策略出现了：**把最小的数和最大的数配成一对**，然后把次小的和次大的配成一对，依次类推。  

这正是 **“双指针 + 排序”** 的经典贪心思路：

- 先把数组从小到大排好序（就像把所有袜子按长度从短到长排成一列）。  
- 用两个指针 `left`（指向最左侧）和 `right`（指向最右侧）同时向中间移动：  
  - `left` 指向当前最小的未配对元素，`right` 指向当前最大的未配对元素。  
  - 把这两个元素配对，计算它们的和，更新全局的 **最大配对和**。  
  - 然后 `left` 向右移动一格，`right` 向左移动一格，继续配对。

**为什么这种配对一定最优**（贪心证明的直观版）：

- 假设我们有最小值 `a` 与最大值 `z`（`a ≤ … ≤ z`）。若把 `z` 和其他比 `a` 更大的数 `b` 配对，得到的和 `z+b` 一定 ≥ `z+a`。  
- 于是把 `z` 和 `a` 配对可以让这对的和 **不大于** 任何把 `z` 与其他数配对的情况。  
- 剩下的数仍然保持同样的顺序，递归地对剩余子数组使用相同策略，整体最优得到保证。  

**类比**：想象把一根很长的绳子（最大数）和一根很短的绳子（最小数）绑在一起，使得这根绳子的总长度尽可能短；把第二长的和第二短的也这样绑，最后所有绳子的最长长度就是我们要最小化的目标。

#### 代码（Python）

```python
from typing import List

def min_max_pair_sum(nums: List[int]) -> int:
    """
    贪心 + 双指针：先排序，再让最小的和最大的配对。
    时间 O(n log n)（排序），空间 O(1)（原地操作）。
    """
    nums.sort()                     # 排序，复杂度 O(n log n)
    left, right = 0, len(nums) - 1  # 两个指针分别指向最左、最右
    max_pair_sum = 0                # 记录所有配对中的最大和

    while left < right:
        pair_sum = nums[left] + nums[right]  # 当前配对的和
        max_pair_sum = max(max_pair_sum, pair_sum)  # 更新全局最大和
        left += 1      # 最小的已经配对，向右移动
        right -= 1     # 最大的已经配对，向左移动

    return max_pair_sum
```

> **关键行中文注释**  
> - `nums.sort()`：把数组从小到大排好序，就像把袜子按长度排好。  
> - `pair_sum = nums[left] + nums[right]`：把最小的和最大的放在一起配。  
> - `max_pair_sum = max(max_pair_sum, pair_sum)`：维护“目前配对中出现的最大和”。  
> - `left += 1; right -= 1`：配完后，两头向中间靠拢，继续配对。

#### 复杂度

- **时间复杂度**：`O(n log n)` — 主要花在排序上，`n` 为数组长度。  
  > 大白话：如果数组有 10 万个数，排序大约需要几倍于线性遍历的时间，但仍然可以在毫秒级完成。  
- **空间复杂度**：`O(1)`（若使用原地排序）或 `O(n)`（Python 的 Timsort 需要额外的临时空间），相对于 `n` 来说是常数级别的开销。  
  > 与暴力解相比，空间几乎没有增加，时间从指数级降到了几乎最优的 `n log n`。

---

## 心得

- **核心技巧**：**贪心 + 双指针**（先排序，再把最小的和最大的配对）。  
- **适用的题型**：  
  1. “最大最小化”类配对问题，如 **“数组中的最大差值”**、**“最小化最大工作时间”**（把工作分配给两台机器）。  
  2. “两数之和”变形，需要在排序后使用双指针快速定位。  
  3. “船上最多可以装多少对重量不超过 limit” 之类的 **配对容量** 问题。  
- **一句话总结解题钥匙**：**把“大”和“小”配在一起，最大值自然被压低**。

---

## 反思

- **第一反应**：看到“最大配对和”，立刻想到“把大数和小数配对”。但最初会担心是否有更复杂的组合能更好，于是想到暴力搜索。  
- **最容易踩的坑**：  
  - 忘记数组长度是偶数，导致指针相遇时出现未配对的元素。  
  - 在实现时误把 `left <= right` 写成 `left < right`，导致最后一次配对出现重复或遗漏。  
  - 对于极端输入（全部相同或已经排好序的数组），仍然要确保代码能够正常运行。  
- **下次类似题的第一步**：先 **排序**，再思考 **“最大值怎么被压制”**——这往往提示使用 **双指针** 或 **贪心** 的配对策略。