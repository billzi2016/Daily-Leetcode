# #875. 可可吃香蕉 / Koko Eating Bananas

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/koko-eating-bananas/)

---

## 题目（英文原版）

**Description**

Koko loves to eat bananas. There are n piles of bananas, the ith pile has piles[i] bananas. The guards have gone and will come back in h hours.
Koko can decide her bananas-per-hour eating speed of k. Each hour, she chooses some pile of bananas and eats k bananas from that pile. If the pile has less than k bananas, she eats all of them instead and will not eat any more bananas during this hour.
Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.
Return the minimum integer k such that she can eat all the bananas within h hours.

**Examples**

**Example 1:**

```
Input: piles = [3,6,7,11], h = 8
Output: 4
```

**Example 2:**

```
Input: piles = [30,11,23,4,20], h = 5
Output: 30
```

**Example 3:**

```
Input: piles = [30,11,23,4,20], h = 6
Output: 23
```

**Constraints**

- 1 <= piles.length <= 104
- piles.length <= h <= 109
- 1 <= piles[i] <= 109

---

## 题目（中文翻译）

Koko（可可）喜欢吃香蕉。共有 **n** 堆（pile）香蕉，第 **i** 堆包含 `piles[i]` 根香蕉。警卫已经离开，并将在 **h** 小时后返回。

Koko 可以自行决定每小时吃香蕉的速度 **k**。每个小时，她会选择一堆香蕉并吃掉其中的 **k** 根。如果该堆的香蕉少于 **k** 根，她会把该堆的所有香蕉全部吃完，并且在此小时内不再吃其他香蕉。

Koko 喜欢慢慢吃，但仍希望在警卫返回之前吃完所有香蕉。

返回最小的整数 **k**，使得她能够在 **h** 小时内吃完所有香蕉。

### 示例

**示例 1:**
```
Input: piles = [3,6,7,11], h = 8
Output: 4
```

**示例 2:**
```
Input: piles = [30,11,23,4,20], h = 5
Output: 30
```

**示例 3:**
```
Input: piles = [30,11,23,4,20], h = 6
Output: 23
```

### 约束条件
- `1 <= piles.length <= 10^4`
- `piles.length <= h <= 10^9`
- `1 <= piles[i] <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有可能的吃速 `k`（每小时吃的香蕉数量）都枚举一遍，然后逐个验证它能否在 `h` 小时内吃完所有香蕉。

- **枚举范围**：`k` 的最小值显然是 `1`（最慢），最大值不需要超过最大的那堆香蕉 `max(piles)`，因为如果 `k` 大于等于这堆，最多一小时就能吃完它。
- **验证过程**：对于某个固定的 `k`，我们模拟 `h` 小时的吃法。每一小时，从任意一堆取 `k`（如果该堆不足 `k`，一次性吃完），统计总共用了多少小时。如果累计的小时数 ≤ `h`，说明这个 `k` 可行。
- **为什么正确**：我们把 **所有可能的速度** 都检查了一遍，只要有一个满足条件，就一定能找到最小的那个（因为我们是从小到大枚举的）。

> 类比：把 `k` 想成一本字典里查词的“页码”。我们把所有页码（1 到最大页码）一个一个尝试，看看能否在限定时间内把所有词都找到。

#### 代码（Python）

```python
from math import ceil
from typing import List

def minEatingSpeed_bruteforce(piles: List[int], h: int) -> int:
    # 最大的那堆香蕉决定了枚举的上界
    max_pile = max(piles)

    # 从最慢的速度 1 开始枚举
    for k in range(1, max_pile + 1):
        # 计算在速度 k 下，需要多少小时才能吃完全部香蕉
        # ceil(p / k) 表示把一堆 p 按每小时 k 吃，需要向上取整的小时数
        hours_needed = sum(ceil(p / k) for p in piles)

        # 如果所需小时数不超过 h，说明 k 可行，直接返回
        if hours_needed <= h:
            return k

    # 按理论这里永远不会走到这里，因为 max_pile 本身一定可行
    return max_pile
```

- `ceil(p / k)` 用来算 **一堆** 需要多少整小时才能吃完。  
- `sum(...)` 把所有堆的时间加起来，就是总共需要的小时数。

#### 复杂度

- **时间复杂度**：`O(max(piles) * n)`  
  - `max(piles)` 是我们枚举的速度次数，`n` 是每次枚举要遍历所有堆。  
  - 用大白话说：如果最大堆有 10⁹ 根香蕉，而有 10⁴ 堆，那么最坏情况下要做 10⁹ × 10⁴ ≈ 10¹³ 次计算，显然不可接受。
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举速度的次数**，它可能非常大（最高可达 10⁹）。我们需要利用题目中的**单调性**来加速搜索。

**关键观察**：  
- 当速度 `k` 增大时，吃完所有香蕉所需的时间 **单调不增**（越快越少时间）。  
- 换句话说，如果某个 `k` 能在 `h` 小时内完成，那么所有更大的 `k` 也一定能完成。

这正好符合 **二分查找**（Binary Search）的使用场景：在一个单调递减（或递增）的函数上找最小满足条件的自变量。

**步骤**：

1. **确定搜索区间**  
   - 左边界 `low = 1`（最慢）  
   - 右边界 `high = max(piles)`（最快只需要一小时吃完最大堆）

2. **二分循环**  
   - 取中点 `mid = (low + high) // 2` 作为当前的吃速 `k`。  
   - 计算在该速率下总共需要多少小时（同暴力解的 `hours_needed`）。  
   - 如果 `hours_needed ≤ h`，说明 `mid` 已经够快，尝试更小的速度：`high = mid - 1`。  
   - 否则速度太慢，需要加快：`low = mid + 1`。

3. **结束**  
   - 循环结束时，`low` 正好是满足条件的最小整数速度。

> 类比：把所有可能的速度想成一本有序的字典，从第一页到最后一页。我们不必从头到尾翻，而是每次打开中间的页码检查——如果那页已经满足条件，就往前找；否则往后找。这样只需要对数级的翻页次数。

#### 代码（Python）

```python
from math import ceil
from typing import List

def minEatingSpeed(piles: List[int], h: int) -> int:
    """
    使用二分搜索找到最小的吃速 k，使得在 h 小时内吃完所有香蕉。
    """
    low, high = 1, max(piles)          # 搜索区间 [low, high]

    while low <= high:
        mid = (low + high) // 2        # 当前尝试的速度 k
        # 计算在速度 mid 下，需要多少小时才能吃完
        hours_needed = sum(ceil(p / mid) for p in piles)

        if hours_needed <= h:          # 速度够快，尝试更小的速度
            high = mid - 1
        else:                          # 速度太慢，需要加快
            low = mid + 1

    # 循环结束时 low 指向最小可行的速度
    return low
```

- `ceil(p / mid)` 同样用于计算单堆所需小时数。  
- `while low <= high` 是二分搜索的标准写法，保证所有可能的 `k` 都被检查到。

#### 复杂度

- **时间复杂度**：`O(n * log(max(piles)))`  
  - `log(max(piles))` 是二分搜索的轮数（最多约 30 次，因为 `max(piles) ≤ 10⁹`），每轮需要遍历 `n` 堆。  
  - 用大白话说：即使有 10⁴ 堆香蕉，也只需要大约 30 × 10⁴ ≈ 3×10⁵ 次简单运算，完全可以接受。

- **空间复杂度**：`O(1)`  
  - 只使用了常数级别的变量 `low、high、mid、hours_needed`。

---

## 心得

- **核心技巧**：利用 **单调性 + 二分搜索** 在整数范围内快速定位最小满足条件的值。  
- **适用的题型**：  
  1. “在限定时间/次数内完成任务，求最小/最大速率”——如 *Minimum Speed to Arrive on Time*。  
  2. “给定阈值，求最小/最大可行的参数”——如 *Split Array Largest Sum*、*Capacity To Ship Packages Within D Days*。  
- **解题钥匙**：先判断“答案是否随参数单调变化”，再用二分把搜索空间指数级压缩。

---

## 反思

- **第一反应**：直接暴力枚举所有可能的吃速 `k`，因为思路最直接。  
- **最容易踩的坑**：  
  - **溢出**：在某些语言里 `mid = (low + high) // 2` 需要防止 `low + high` 超出整数范围（Python 不会）。  
  - **边界条件**：`h` 可能比堆的数量多很多，需要保证 `hours_needed` 的计算使用向上取整，否则会低估所需时间。  
  - **单调性误判**：必须确认“速度增大 → 所需时间不增”，否则二分会出错。  
- **下次第一步**：先检查是否存在“随参数单调变化”的关系，如果有，就立刻考虑二分搜索，而不是直接暴力。