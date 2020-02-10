# #768. 使数组有序的最大拆分块数 II / Max Chunks To Make Sorted II

> 难度：困难 · 标签：Array、Stack、Greedy、Sorting、Monotonic Stack · [LeetCode 链接](https://leetcode.com/problems/max-chunks-to-make-sorted-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer array arr.
We split arr into some number of chunks (i.e., partitions), and individually sort each chunk. After concatenating them, the result should equal the sorted array.
Return the largest number of chunks we can make to sort the array.

**Examples**

**Example 1:**

```
Input: arr = [5,4,3,2,1]
Output: 1
Explanation:
Splitting into two or more chunks will not return the required result.
For example, splitting into [5, 4], [3, 2, 1] will result in [4, 5, 1, 2, 3], which isn't sorted.
```

**Example 2:**

```
Input: arr = [2,1,3,4,4]
Output: 4
Explanation:
We can split into two chunks, such as [2, 1], [3, 4, 4].
However, splitting into [2, 1], [3], [4], [4] is the highest number of chunks possible.
```

**Constraints**

- 1 <= arr.length <= 2000
- 0 <= arr[i] <= 108

---

## 题目（中文翻译）

给定一个整数数组 `arr`。  
我们将 `arr` 拆分成若干块（即分区），并分别对每一块进行排序。将各块排序后的结果按顺序拼接后，得到的数组应当等于已排序的数组。  
返回能够使数组有序的最大块数。

**示例 1：**  
**示例 2：**  
**约束条件：**

**示例 1：**  
输入: `arr = [5,4,3,2,1]`  
输出: `1`  
解释:  
拆分成两个或更多块都无法得到要求的结果。例如，拆分为 `[5, 4]`、`[3, 2, 1]` 会得到 `[4, 5, 1, 2, 3]`，这不是已排序的数组。

**示例 2：**  
输入: `arr = [2,1,3,4,4]`  
输出: `4`  
解释:  
我们可以拆分成两块，例如 `[2, 1]`、`[3, 4, 4]`。  
然而，将其拆分为 `[2, 1]`、`[3]`、`[4]`、`[4]` 能得到的块数最多，为 4。

**约束条件：**  
- `1 <= arr.length <= 2000`  
- `0 <= arr[i] <= 10^8`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的切分方式都穷举**，然后检验每一种切分是否合法：  

1. 先把原数组 `arr` 按照某种切分方式划分成若干块（chunk）。  
2. 对每一块单独进行 **排序**。  
3. 把排好序的块按原来的顺序拼接起来，得到一个新数组 `b`。  
4. 如果 `b` 与 `arr` 的整体排序结果 `sorted(arr)` 完全相同，则这种切分是合法的。  

把所有合法切分中块数最多的那个，就是答案。  

> **生活化类比**：  
> 想象你有一摞混乱的纸牌（`arr`），你可以把它切成若干堆，每堆单独整理（排序），最后把堆按原来的顺序重新摆好。只有当所有堆摆好后整摞牌正好是从小到大排好序时，这种切法才算合法。

**为什么暴力法一定能得到正确答案**：  
因为我们枚举了 **所有** 可能的切法，只要有一种切法能够满足题目要求，暴力搜索必然会找到它；再取块数最大的那一种，就是题目要的最大 chunk 数。

**时间/空间分析（大白话）**  

- 枚举切法的数量是指数级的：每两个相邻位置之间可以“切”也可以“不切”，所以大约有 `2^(n-1)` 种可能（`n` 是数组长度）。  
- 对每一种切法，我们都要把每块排序，排序的代价是 `O(k log k)`（`k` 是块的长度），最坏情况下相当于对整个数组排序 `O(n log n)`。  
- 因此整体时间复杂度是 **指数级**，大约 `O(2^n * n log n)`，在最坏情况下几乎不可能在 1 秒内跑完。  
- 需要的额外空间主要是存放临时的排序结果，最多 `O(n)`。

> **O(…) 的意义**：  
> - `O(2^n)` 表示随着 `n` 增大，运算次数会像 2 的 n 次方那样飞快增长，哪怕 `n` 只增加 10，运算次数就会多出 1024 倍。  
> - `O(n log n)` 表示排序的代价随 `n` 增大而稍微快一点，但比线性 `O(n)` 慢得多。

#### 代码（Python）

```python
from itertools import product
from typing import List

def max_chunks_to_sorted_bruteforce(arr: List[int]) -> int:
    n = len(arr)
    # 所有切分方式：在每两个相邻位置之间决定是否切
    # 用 0/1 表示，不切 = 0，切 = 1，长度为 n-1 的二进制序列
    best = 1                     # 至少可以整个数组算一个 chunk
    for cuts in product([0, 1], repeat=n - 1):
        # 根据 cuts 把 arr 切成块
        chunks = []
        start = 0
        for i, cut in enumerate(cuts):
            if cut:               # 在 i 和 i+1 之间切
                chunks.append(arr[start:i + 1])
                start = i + 1
        chunks.append(arr[start:])   # 最后一个块

        # 对每块排序后拼接
        rebuilt = []
        for ch in chunks:
            rebuilt.extend(sorted(ch))

        # 检查是否等于整体排序后的数组
        if rebuilt == sorted(arr):
            best = max(best, len(chunks))

    return best
```

> **关键行中文注释**  
> - `product([0, 1], repeat=n - 1)`: 生成所有“切或不切”的组合。  
> - `chunks.append(arr[start:i + 1])`: 把当前块加入列表。  
> - `rebuilt.extend(sorted(ch))`: 对块进行排序并拼接到结果里。  

#### 复杂度  

- **时间复杂度**：`O(2^n * n log n)` — 指数级爆炸，随着数组长度稍微增加就会变得不可接受。  
- **空间复杂度**：`O(n)` — 主要是存放临时的块和排序后结果。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**枚举所有切法**。其实我们不需要真的去尝试每一种切法，只要找出“可以安全切的位置”即可。  

**核心观察**：  
设 `sorted_arr` 为 `arr` 的全局升序排列。如果我们在下标 `i`（即 `i` 前面的元素是一个 chunk，`i` 之后的元素是后面的 chunk）切开，要求 **左边的所有元素在整体排序后仍然出现在左边**，也就是说左边的最大值不大于右边的最小值。  

更形式化地：

```
prefix_max[i] = max(arr[0..i])          # 前缀最大值
suffix_min[i] = min(arr[i..n-1])        # 后缀最小值
我们可以在 i 处切（i 为切点的左端最后一个位置）当且仅当
prefix_max[i] <= suffix_min[i+1]
```

因为如果左边的最大元素已经不大于右边的最小元素，即使把左边块内部排好序，左块的所有元素仍然不会“跑到”右块里，整体拼接后自然是有序的。

**如何快速得到这些信息**：

1. **一次遍历**得到 `prefix_max`：从左到右维护当前最大值。  
2. **一次遍历**得到 `suffix_min`：从右到左维护当前最小值。  
3. 再遍历一次，统计满足 `prefix_max[i] <= suffix_min[i+1]` 的位置个数，这个个数就是可以切的地方数，加上最后一个块本身，总的 chunk 数即为 **满足条件的切点数量 + 1**。

> **类比**：  
> 想象两条河流，一条从左往右流（前缀最大），另一条从右往左流（后缀最小）。只要左边的水位（最大值）不超过右边的水位（最小值），我们就可以在这两条河的交汇点建一座桥（切点），桥两侧的水仍然保持各自的高度，不会出现倒流。

**为什么这一步就能得到最大块数**：

- 每一次满足 `prefix_max[i] <= suffix_min[i+1]` 的切点都是**合法的**（可以切），并且**不会影响后面的切点**，因为后面的判断只依赖于右侧的最小值，而左侧已经被限制在不大于右侧的范围内。  
- 因此我们可以**把所有合法切点都切下去**，得到的块数就是最大的。

**另一种等价思路（计数法）**：

把 `arr` 与 `sorted_arr` 的**前缀计数**进行比较：如果到某个位置为止，两者的元素出现次数完全相同，则说明前缀已经可以独立成块。实现时可以使用 `defaultdict(int)` 来维护差值计数，差值全部为 0 时即可切。这个思路对出现重复元素的情况同样有效，和前缀/后缀极值方法本质相同，只是用**多重集合**（哈希表）来实现。

下面给出基于前缀最大 / 后缀最小的实现，代码最简洁且易于理解。

#### 代码（Python）

```python
from typing import List

def max_chunks_to_sorted(arr: List[int]) -> int:
    n = len(arr)
    if n == 0:
        return 0

    # 1) 前缀最大值数组
    prefix_max = [0] * n
    cur_max = arr[0]
    for i in range(n):
        cur_max = max(cur_max, arr[i])
        prefix_max[i] = cur_max

    # 2) 后缀最小值数组
    suffix_min = [0] * n
    cur_min = arr[-1]
    for i in range(n - 1, -1, -1):
        cur_min = min(cur_min, arr[i])
        suffix_min[i] = cur_min

    # 3) 统计合法切点
    chunks = 0
    for i in range(n - 1):                # 切点只能在 0..n-2 之间
        if prefix_max[i] <= suffix_min[i + 1]:
            chunks += 1                    # 在 i 处切下一个块

    # 最后一个块一定存在
    return chunks + 1
```

> **关键行中文注释**  
> - `prefix_max[i] = max(cur_max, arr[i])`：记录从左边到当前位置的最大值。  
> - `suffix_min[i] = min(cur_min, arr[i])`：记录从右边到当前位置的最小值。  
> - `if prefix_max[i] <= suffix_min[i + 1]`：判断左块最大是否不超过右块最小，满足则可以切。  

**计数法（哈希表）实现**（同样 O(n)）：

```python
from collections import defaultdict

def max_chunks_to_sorted_counter(arr: List[int]) -> int:
    sorted_arr = sorted(arr)
    diff = defaultdict(int)   # 记录前缀出现次数的差值
    chunks = 0

    for a, b in zip(arr, sorted_arr):
        diff[a] += 1
        diff[b] -= 1

        # 移除计数为 0 的键，保持 diff 只保存非零差值
        if diff[a] == 0:
            del diff[a]
        if diff[b] == 0:
            del diff[b]

        # 当差值全部消失，说明前缀已完全匹配，可切
        if not diff:
            chunks += 1

    return chunks
```

#### 复杂度  

- **时间复杂度**：`O(n)` — 只需要几次线性遍历，`n` 最多 2000，运行毫秒级。  
  - 与暴力解的 `O(2^n * n log n)` 相比，**线性**意味着即使 `n` 增大到几万也依然快速。  
- **空间复杂度**：`O(n)`（前缀/后缀数组）或 `O(k)`（哈希表，`k` 为不同元素个数），最坏情况下也是 `O(n)`。  

---

## 心得  

- **核心技巧**：利用**前缀最大 ≤ 后缀最小**（或前缀计数相等）来判定可以安全切分的点。  
- **适用的题型**：  
  1. “Maximum Chunks To Make Sorted I” – 只含 0…n-1 的全排列，用前缀最大判断。  
  2. “Partition Array Into Disjoint Intervals” – 需要找最左侧可以独立的子数组，同样用前缀最大/后缀最小。  
  3. “Split Array Into Consecutive Subsequences” – 需要检查前缀计数是否匹配，也可以用哈希表差值。  
- **一句话总结解题钥匙**：**只要左边的最大不超过右边的最小，就可以在这里切；把所有这样的位置全部切下来，即得到最大块数。**

---

## 反思  

- **第一反应**：看到“把数组切块、各自排序后再拼接要等于全局排序”，立刻想到“枚举所有切法”。这是一种直觉的暴力思路。  
- **最容易踩的坑**：  
  - 忽视数组中可能出现的重复元素。若只比较 `max` 与 `min` 而不考虑相等情况，仍然是正确的，但在计数法实现时必须确保 **差值全部为 0** 才能切。  
  - 边界条件：最后一个块一定存在，记得在统计合法切点后 `+1`。  
  - 当 `n = 1` 时，直接返回 1，防止访问 `suffix_min[1]` 越界。  
- **下次遇到同类题**：第一步先思考 **“是否存在一种单调/计数的全局约束，使得局部切分不影响整体有序性？”**，如果能找到类似 “前缀最大 ≤ 后缀最小” 的不等式，就能立刻得到线性时间的最优解。