# #2111. 最少操作使数组 K‑递增 / Minimum Operations to Make the Array K-Increasing

> 难度：困难 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-the-array-k-increasing/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed array arr consisting of n positive integers, and a positive integer k.
The array arr is called K-increasing if arr[i-k] <= arr[i] holds for every index i, where k <= i <= n-1.
In one operation, you can choose an index i and change arr[i] into any positive integer.
Return the minimum number of operations required to make the array K-increasing for the given k.

**Examples**

**Example 1:**

```
Input: arr = [5,4,3,2,1], k = 1
Output: 4
Explanation:
For k = 1, the resultant array has to be non-decreasing.
Some of the K-increasing arrays that can be formed are [5,6,7,8,9], [1,1,1,1,1], [2,2,3,4,4]. All of them require 4 operations.
It is suboptimal to change the array to, for example, [6,7,8,9,10] because it would take 5 operations.
It can be shown that we cannot make the array K-increasing in less than 4 operations.
```

**Example 2:**

```
Input: arr = [4,1,5,2,6,2], k = 2
Output: 0
Explanation:
This is the same example as the one in the problem description.
Here, for every index i where 2 <= i <= 5, arr[i-2] <= arr[i].
Since the given array is already K-increasing, we do not need to perform any operations.
```

**Example 3:**

```
Input: arr = [4,1,5,2,6,2], k = 3
Output: 2
Explanation:
Indices 3 and 5 are the only ones not satisfying arr[i-3] <= arr[i] for 3 <= i <= 5.
One of the ways we can make the array K-increasing is by changing arr[3] to 4 and arr[5] to 5.
The array will now be [4,1,5,4,6,5].
Note that there can be other ways to make the array K-increasing, but none of them require less than 2 operations.
```

**Constraints**

- 1 <= arr.length <= 105
- 1 <= arr[i], k <= arr.length

---

## 题目（中文翻译）

你得到一个下标从 0 开始的数组 (array) `arr`，其中包含 `n` 个正整数，以及一个正整数 `k`。  
如果对于每个满足 `k ≤ i ≤ n‑1` 的下标 `i` 都有 `arr[i‑k] ≤ arr[i]` 成立，则称数组 `arr` 为 **K‑递增 (K-increasing)**。

一次操作可以选择任意下标 `i`，并将 `arr[i]` 改为任意正整数。  
返回使给定的 `k` 下的数组成为 K‑递增所需的最少操作次数。

**示例 1**  
```text
Input: arr = [5,4,3,2,1], k = 1
Output: 4
Explanation:
对于 k = 1，结果数组必须是非递减的。
可以得到的 K‑递增数组示例包括 [5,6,7,8,9]、[1,1,1,1,1]、[2,2,3,4,4]，这些都需要 4 次操作。
将数组改为例如 [6,7,8,9,10] 并不是最优的，因为需要 5 次操作。
可以证明，无法用少于 4 次操作使数组满足 K‑递增。
```

**示例 2**  
```text
Input: arr = [4,1,5,2,6,2], k = 2
Output: 0
Explanation:
这正是题目描述中的示例。
对于所有满足 2 ≤ i ≤ 5 的下标 i，均有 arr[i‑2] ≤ arr[i]。
因为原数组已经是 K‑递增的，所以不需要进行任何操作。
```

**示例 3**  
```text
Input: arr = [4,1,5,2,6,2], k = 3
Output: 2
Explanation:
下标 3 和 5 是唯一不满足 arr[i‑3] ≤ arr[i]（3 ≤ i ≤ 5）的元素。
一种使数组成为 K‑递增的方式是将 arr[3] 改为 4，arr[5] 改为 5。
此时数组变为 [4,1,5,4,6,5]。
注意还有其他可能的修改方案，但没有任何方案的操作次数少于 2 次。
```

**约束条件**  

- `1 ≤ arr.length ≤ 10^5`  
- `1 ≤ arr[i], k ≤ arr.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把整个数组一次遍历检查每个位置 `i` 是否满足 `arr[i‑k] ≤ arr[i]`**。  
如果不满足，就把 `arr[i]` 随便改成一个足够大的数（比如 `arr[i‑k]` 本身），这样就能立刻让这对 `(i‑k, i)` 符合要求。  

- **使用的数据结构**：只需要原数组本身和一个计数器 `ops`，不需要额外的容器。可以把哈希表想象成一本词典，这里我们根本不需要词典，只要一张纸（数组）和一支笔（计数器）就行。  
- **为什么正确**：每次我们发现一对不满足的相邻（间隔 `k`）元素，就立刻把后面的改成前面的值或更大，这样这对就一定满足了。遍历结束后，所有对都满足，数组自然是 K‑increasing。  

然而，这种方法并没有考虑**整体最小化改动次数**。有时我们把一个位置改了，后面的很多位置就不需要再改了；相反，如果盲目改动，可能会把已经可以保留的元素也改掉，导致改动次数远大于最优。

#### 代码（Python）

```python
def min_operations_bruteforce(arr, k):
    """
    暴力思路：从左到右检查每个 i，若 arr[i-k] > arr[i] 就把 arr[i] 改成
    arr[i-k]（或更大），计数加一。返回计数。
    这只是演示最直接的想法，并不保证最小改动次数。
    """
    ops = 0                     # 记录需要的操作数
    a = arr[:]                  # 复制一份，防止修改原数组
    n = len(a)

    for i in range(k, n):
        if a[i - k] > a[i]:     # 这对不满足 K‑increasing 条件
            a[i] = a[i - k]     # 把后面的改成前面的值（最小的合法改动）
            ops += 1
    return ops
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n` 是数组长度。  
  > 大白话：如果数组有 10 000 个数，就需要检查 10 000 次。  
- **空间复杂度**：`O(1)`（不计复制的数组）—— 只用了常数个额外变量。  

> **注意**：虽然时间是线性的，但这个算法的答案往往不是最小的，因为它每次都“硬改”，没有做全局最优的考虑。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于我们一次只看一对 `(i‑k, i)`，而没有利用 **跨对之间的联系**。  
观察条件 `arr[i‑k] ≤ arr[i]`，如果把数组按下标模 `k` 分成 `k` 条 **不相交的子序列**，每条子序列内部的相邻元素正好相差 `k`，必须保持 **非递减**（即 `≤`）：

```
k = 3
原数组下标 : 0 1 2 3 4 5 6 7 8 ...
子序列0   : 0   3   6   9 ...
子序列1   : 1   4   7 ...
子序列2   : 2   5   8 ...
```

因此，**整个问题等价于**：对每条子序列，使其 **非递减**，并且 **改动的元素总数最少**。  
把每条子序列记作 `seq`，我们要在 `seq` 上做最少改动，使其非递减。

---

##### 2.1 哪些元素可以**不改**？

如果我们把 **不需要改动的元素** 看成一个子序列，那它必须已经满足非递减，即 **一个最长的非递减子序列（LNDS）**。  
- 把 LNDS 中的元素保留不动，其他位置全部改成合适的值，就能得到一个合法的非递减序列。  
- 改动次数 = `len(seq) - len(LNDS)`（因为保留的就是 LNDS，剩下的都要改）。

所以，对每条子序列，**最少改动次数 = 子序列长度 - LNDS 长度**。  
整个数组的答案就是所有子序列改动次数的 **和**。

---

##### 2.2 如何求 LNDS？

求最长非递减子序列可以使用 **“Patience Sorting” + 二分查找**（即经典的求 LIS 的 O(n log n) 方法），唯一的区别是这里允许相等（非递减而不是严格递增），所以在二分查找时使用 `bisect_right`（找到第一个大于 `x` 的位置）而不是 `bisect_left`。

具体步骤（以单条子序列 `seq` 为例）：

1. 建立一个空列表 `tails`，`tails[i]` 记录长度为 `i+1` 的非递减子序列的最小可能结尾值。  
2. 依次遍历 `seq` 中的每个数 `x`：  
   - 用 `bisect_right(tails, x)` 找到可以把 `x` 放在 `tails` 中的最右位置 `pos`。  
   - 如果 `pos` 等于 `len(tails)`，说明 `x` 可以把子序列长度延长 1，直接 `tails.append(x)`。  
   - 否则，用 `x` 替换 `tails[pos]`（因为 `x` 更小或相等，能为后续的扩展提供更大的空间）。  
3. 最终 `len(tails)` 就是 LNDS 的长度。

该过程每个元素只做一次二分查找，时间是 `O(m log m)`，`m` 为子序列长度。所有 `k` 条子序列的长度之和恰好是 `n`，所以整体时间是 `O(n log n)`。

---

#### 代码（Python）

```python
from bisect import bisect_right
from typing import List

def min_operations(arr: List[int], k: int) -> int:
    """
    最优解：
    1. 把数组按下标 % k 分成 k 条子序列。
    2. 对每条子序列求最长非递减子序列（LNDS）的长度。
    3. 该子序列需要改动的元素数 = len(seq) - LNDS_len。
    4. 所有子序列的改动数相加即为答案。
    """
    n = len(arr)
    ans = 0

    # 对每个余数 r = 0 .. k-1 形成一条子序列
    for r in range(k):
        seq = []                     # 收集下标为 r, r+k, r+2k, ... 的元素
        for i in range(r, n, k):
            seq.append(arr[i])

        # 求 seq 的最长非递减子序列长度
        tails = []                   # tails[i] = 长度为 i+1 的非递减子序列的最小结尾
        for x in seq:
            # 在 tails 中找到第一个 > x 的位置（右侧插入），等价于 bisect_right
            pos = bisect_right(tails, x)
            if pos == len(tails):
                tails.append(x)      # 可以把子序列长度延长
            else:
                tails[pos] = x       # 用更小的结尾替换，利于后续扩展

        lnds_len = len(tails)
        ans += len(seq) - lnds_len   # 需要改动的元素数

    return ans
```

> **代码要点注释**  
> - `bisect_right`：类似在有序的词典里找“比我大的第一个词”的位置，只是这里找的是数值。  
> - `tails` 列表始终保持 **递增**（严格递增），因为我们用 `bisect_right`，所以相同的数会被放到更右边，保证非递减的特性。  
> - 每条子序列独立处理，最后把所有需要改动的次数累加。

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 每个元素只参与一次二分查找，二分的代价是 `log m`，`m ≤ n`，所以整体是 `n log n`。  
  - 大白话：如果数组有 100 000 个数，`log₂100 000 ≈ 17`，所以大约要做 1.7 百万次“比较”，在机器上几毫秒就能跑完。  

- **空间复杂度**：`O(k)`（额外的 `tails` 列表最多保存一条子序列的长度，最坏情况是 `k` 条子序列中最长的那条，长度 ≤ `n/k`，但我们在循环里复用同一个列表），实际使用的额外空间是 **线性** 于单条子序列的长度，整体仍是 `O(n)` 的常数因子。  
  - 简单理解：我们只存了几个临时数组，跟原数组大小相比可以忽略不计。

---

## 心得

- **核心技巧**：把原问题拆成 `k` 条独立的“非递减序列”问题，再用 **最长非递减子序列（LNDS）** 计算最少改动数。  
- **适用的题型**  
  1. “把数组分块后每块要单调” 类似的题目，如 **“Make Array Non-decreasing by Modifying at Most K Elements”**。  
  2. 需要在子序列上做 **最少删除/修改** 使其满足单调性的问题，例如 **“Minimum Deletions to Make Sequence Increasing”**。  
  3. 任何可以 **按余数分组** 且组间约束相同的题目。  
- **一句话总结解题钥匙**：  
  > **“分组 → 每组求最长非递减子序列 → 其余全部改”。**

---

## 反思

- **第一反应**：直接遍历检查每对 `(i‑k, i)`，发现不满足就立刻改。  
- **最容易踩的坑**  
  - **忽视全局最优**：单独改每对会导致不必要的改动。  
  - **相等情况**：条件是 `≤`，所以在求 LNDS 时必须使用 **非递减**（而不是严格递增），二分时要用 `bisect_right`。  
  - **边界**：`k` 可能等于 `1`（整个数组必须非递减），也可能等于 `n`（每个元素独立，答案永远是 `0`），代码需要能兼容这两端情况。  
- **下次遇到同类题**：  
  1. **先思考能否分解**——是否可以把约束拆成若干独立子问题。  
  2. **在每个子问题中寻找最长保留序列**（LIS/LNDS），因为保留的就是不需要改动的元素。  
  3. **把子问题的答案累加**，得到全局最小改动数。