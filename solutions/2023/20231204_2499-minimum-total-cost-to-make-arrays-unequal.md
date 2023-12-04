# #2499. 最小总代价使数组不相等 / Minimum Total Cost to Make Arrays Unequal

> 难度：困难 · 标签：Array、Hash Table、Greedy、Counting · [LeetCode 链接](https://leetcode.com/problems/minimum-total-cost-to-make-arrays-unequal/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays nums1 and nums2, of equal length n.
In one operation, you can swap the values of any two indices of nums1. The cost of this operation is the sum of the indices.
Find the minimum total cost of performing the given operation any number of times such that nums1[i] != nums2[i] for all 0 <= i <= n - 1 after performing all the operations.
Return the minimum total cost such that nums1 and nums2 satisfy the above condition. In case it is not possible, return -1.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,3,4,5], nums2 = [1,2,3,4,5]
Output: 10
Explanation: 
One of the ways we can perform the operations is:
- Swap values at indices 0 and 3, incurring cost = 0 + 3 = 3. Now, nums1 = [4,2,3,1,5]
- Swap values at indices 1 and 2, incurring cost = 1 + 2 = 3. Now, nums1 = [4,3,2,1,5].
- Swap values at indices 0 and 4, incurring cost = 0 + 4 = 4. Now, nums1 =[5,3,2,1,4].
We can see that for each index i, nums1[i] != nums2[i]. The cost required here is 10.
Note that there are other ways to swap values, but it can be proven that it is not possible to obtain a cost less than 10.
```

**Example 2:**

```
Input: nums1 = [2,2,2,1,3], nums2 = [1,2,2,3,3]
Output: 10
Explanation: 
One of the ways we can perform the operations is:
- Swap values at indices 2 and 3, incurring cost = 2 + 3 = 5. Now, nums1 = [2,2,1,2,3].
- Swap values at indices 1 and 4, incurring cost = 1 + 4 = 5. Now, nums1 = [2,3,1,2,2].
The total cost needed here is 10, which is the minimum possible.
```

**Example 3:**

```
Input: nums1 = [1,2,2], nums2 = [1,2,2]
Output: -1
Explanation: 
It can be shown that it is not possible to satisfy the given conditions irrespective of the number of operations we perform.
Hence, we return -1.
```

**Constraints**

- n == nums1.length == nums2.length
- 1 <= n <= 105
- 1 <= nums1[i], nums2[i] <= n

---

## 题目（中文翻译）

给定两个下标从 0 开始的整数数组 `nums1` 和 `nums2`，两数组长度相等，记为 `n`。  
一次操作可以**交换** `nums1` 中任意两个下标的值，**代价**为这两个下标的和。  

要求在执行任意次数的上述操作后，使得对于所有 `0 ≤ i ≤ n‑1` 都满足 `nums1[i] != nums2[i]`。  
返回使上述条件成立的**最小总代价**。如果无论如何都无法实现，则返回 `-1`。

---

### 示例

**示例 1**  
```
Input: nums1 = [1,2,3,4,5], nums2 = [1,2,3,4,5]
Output: 10
Explanation: 
一种可能的操作序列如下：
- 交换下标 0 与 3 的值，代价 = 0 + 3 = 3。此时 nums1 = [4,2,3,1,5]
- 交换下标 1 与 2 的值，代价 = 1 + 2 = 3。此时 nums1 = [4,3,2,1,5]
- 交换下标 0 与 4 的值，代价 = 0 + 4 = 4。此时 nums1 = [5,3,2,1,4]
可以看到，总代价为 10，且每个位置的元素均与 `nums2` 不相等。
```

**示例 2**  
```
Input: nums1 = [2,2,2,1,3], nums2 = [1,2,2,3,3]
Output: 10
Explanation: 
一种可能的操作序列如下：
- 交换下标 2 与 3 的值，代价 = 2 + 3 = 5。此时 nums1 = [2,2,1,2,3]
- 交换下标 1 与 4 的值，代价 = 1 + 4 = 5。此时 nums1 = [2,3,1,2,2]
总代价为 10，且这是能够达到的最小代价。
```

**示例 3**  
```
Input: nums1 = [1,2,2], nums2 = [1,2,2]
Output: -1
Explanation: 
可以证明，无论进行多少次操作，都无法使得每个位置的元素互不相等。
因此返回 -1。
```

---

### 约束条件

- `n == nums1.length == nums2.length`
- `1 ≤ n ≤ 10^5`
- `1 ≤ nums1[i], nums2[i] ≤ n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有不符合要求的位置一个一个改掉**。  
- 先遍历 `nums1` 与 `nums2`，找出所有下标 `i` 使得 `nums1[i] == nums2[i]`（记作 *冲突下标*）。  
- 对每一个冲突下标 `i`，随便挑选另一个下标 `j`（`j ≠ i`），把 `nums1[i]` 与 `nums1[j]` 交换。只要交换后 `nums1[i] != nums2[i]` 且 `nums1[j] != nums2[j]`，冲突就被消除了。  
- 重复上述操作直到所有下标都满足 `nums1[i] != nums2[i]`。

> **类比**：把 `nums1` 看成一本字典，`i` 是页码，`nums1[i]` 是该页的单词。冲突就是“这本字典的第 i 页单词正好和另一本字典的第 i 页单词相同”。我们可以把两页的单词互换，费用就是两页页码之和。

**为什么能成功？**  
只要我们能找到一个不冲突的页码 `j`（即 `nums1[j] != nums2[j]`），并且 `nums1[j]` 与 `nums2[i]` 不相同，交换后两页都会变成不冲突。显然，只要数组足够大，总能找到这样的 `j`（不过实际可能会出现找不到的情况）。

**时间/空间分析**  
- 暴力做法需要**遍历所有下标**，并且每次都要**线性搜索一个合适的 `j`**。最坏情况下，每个冲突都要遍历 `n` 次，时间复杂度是 `O(n²)`。  
- 只用了几个额外的列表（冲突下标、已使用的下标），空间复杂度是 `O(n)`。

> **大白话**：`O(n²)` 就像把 10 000 条信息两两比较，时间会变得非常慢；`O(n)` 只需要把信息顺序读一遍，速度快得多。

#### 代码（Python）

```python
def minCost_bruteforce(nums1, nums2):
    n = len(nums1)
    # 记录所有冲突下标
    conflict = [i for i in range(n) if nums1[i] == nums2[i]]
    total_cost = 0

    for i in conflict:
        # 暴力寻找可以配对的下标 j
        found = False
        for j in range(n):
            if i == j:
                continue
            # 交换后两位都不相等即为合法
            if (nums1[j] != nums2[i]) and (nums1[i] != nums2[j]):
                # 交换
                nums1[i], nums1[j] = nums1[j], nums1[i]
                total_cost += i + j          # 费用是下标之和
                found = True
                break
        if not found:          # 找不到合适的 j，说明无解
            return -1
    return total_cost
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 每个冲突最多遍历一次整个数组，等价于“n × n 次比较”。  
- **空间复杂度**：`O(n)` – 只多用了一个存冲突下标的列表。

---

### 2. 最优解

#### 思路  

从暴力解可以看到**瓶颈在于每次都要线性搜索配对下标**，而且我们没有利用“下标越小费用越低”的特点。下面一步步推导出 **只需要一次遍历 + 若干排序** 的贪心解法。

1. **冲突下标集合**  
   记 `C = { i | nums1[i] == nums2[i] }`，长度记作 `m = |C|`。  
   这些下标一定要参与至少一次交换（否则它们永远冲突），所以 **每个 `i ∈ C` 至少会被计入一次费用**。

2. **能否消除所有冲突？**  
   设某个数值 `v` 在冲突位置出现了 `cnt[v]` 次。如果 `cnt[v]` 超过了数组中可以提供的“不同的值”的数量，就永远换不掉。  
   具体来说，`v` 只能被放到 **不是 `v` 的位置**，而这些位置的数量最多是 `n - cnt[v]`。  
   为了让每个冲突都有别的数填进来，需要  
   ```
   cnt[v] ≤ n - cnt[v] + 1   ⇔   cnt[v] ≤ (n + 1) // 2
   ```
   如果出现 `cnt[v] > (n + 1) // 2`，直接返回 `-1`（不可行）。

3. **配对策略——把费用最小化**  
   每次交换会把 **两个下标的费用相加**。  
   - 已知所有冲突下标 `C` 必然会被计入费用。  
   - 其余的下标 `F = {0…n‑1} \ C`（称为**安全下标**）可以 **不参与** 交换，也可以 **作为配对伙伴**。  
   为了让总费用最小，我们希望 **尽可能多地用安全下标**（因为它们本来就不需要计费），只在必要时才让冲突下标互相配对。

   设 `m = |C|`，`k = |F| = n - m`。  
   - 如果 `k ≥ m`，我们可以把每个冲突下标都和一个不同的安全下标配对，**只需要额外付出 `m` 个安全下标的费用**。  
   - 如果 `k < m`，安全下标不够，需要让部分冲突下标两两配对。每对冲突下标只能消掉 **两个冲突**，但不产生额外费用（因为这两个下标已经在 `C` 中计过一次）。此时仍然需要 **`2·m - n`** 个安全下标来完成配对。  

   因此**额外需要的安全下标数量**为  
   ```
   extra = max(0, 2*m - n)
   ```

4. **选最小的安全下标**  
   为了让费用最小，额外使用的安全下标应当是 **下标值最小的那些**。  
   - 先把所有安全下标升序排列。  
   - 取前 `extra` 个下标的和记作 `sum_extra`。  

5. **答案公式**  

   ```
   answer = sum(C) + sum_extra
   ```

   其中 `sum(C)` 是所有冲突下标的下标之和（必计），`sum_extra` 是上一步得到的最小额外费用。

6. **实现细节**  
   - 第一步遍历一次数组得到 `C`、`m`、以及每个数值的冲突计数 `cnt`。  
   - 用 `collections.Counter` 检查是否出现 `cnt[v] > (n+1)//2`。  
   - 再遍历一次把安全下标收集到列表 `free`，排序后取前 `extra` 个。  
   - 计算并返回 `answer`。

> **核心贪心**：**费用只和下标大小有关**，所以“把大的下标留在不需要计费的地方”，把“小的下标”尽可能用来配对，就能得到最小总费用。

#### 代码（Python）

```python
from collections import Counter
from typing import List

def minCost(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)

    # 1️⃣ 找出所有冲突下标以及每个数值的冲突次数
    conflict_idx = []
    cnt = Counter()
    for i in range(n):
        if nums1[i] == nums2[i]:
            conflict_idx.append(i)        # 必须参与一次交换
            cnt[nums1[i]] += 1

    m = len(conflict_idx)                # 冲突数量

    # 2️⃣ 可行性检查：任意数值的冲突次数不能超过 (n+1)//2
    limit = (n + 1) // 2
    if any(v > limit for v in cnt.values()):
        return -1                         # 无法消除冲突

    # 3️⃣ 收集安全下标（非冲突的下标）
    free_idx = [i for i in range(n) if i not in set(conflict_idx)]
    free_idx.sort()                       # 为了取最小的几个

    # 4️⃣ 需要多少额外的安全下标
    extra = max(0, 2 * m - n)             # 公式推导见思路

    # 5️⃣ 计算答案
    sum_conflict = sum(conflict_idx)      # 必须计费的部分
    sum_extra = sum(free_idx[:extra])     # 选最小的 extra 个安全下标

    return sum_conflict + sum_extra
```

> **代码注释**（每行中文解释）  
> - `conflict_idx.append(i)`：记录下标 `i` 为冲突，需要一次交换。  
> - `cnt[nums1[i]] += 1`：统计每个数值在冲突位置出现的次数，用来后面的可行性判断。  
> - `if any(v > limit for v in cnt.values())`：如果某个数出现太多次，说明没有足够的“不同的位子”来放置它，直接返回 `-1`。  
> - `free_idx = [i for i in range(n) if i not in set(conflict_idx)]`：把所有不冲突的下标挑出来。  
> - `extra = max(0, 2 * m - n)`：当安全下标不足时，需要额外使用 `extra` 个安全下标来配对。  
> - `sum_conflict + sum_extra`：冲突下标的费用 + 必须使用的最小安全下标费用，即为最小总费用。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 第一次遍历 O(n) 统计冲突。  
  - 收集安全下标后排序，最坏是对 `n‑m` 个元素排序，复杂度 `O((n‑m) log (n‑m)) ≤ O(n log n)`。  
- **空间复杂度**：`O(n)`  
  - 需要存放冲突下标、计数器以及安全下标列表，均为线性规模。

> 与暴力解相比，**只需要一次遍历加一次排序**，省去了每次线性搜索配对的 `O(n²)` 开销，速度提升几个数量级。

---

## 心得

- **核心技巧**：**把费用最小化转化为“挑最小下标”** 的贪心问题。先确定哪些下标**必然**要计费（冲突下标），再用**最小的安全下标**补足配对需求。  
- **适用场景**  
  1. “把数组变成和另一个数组在每个位置都不同” 这类**下标费用**的题目。  
  2. 需要 **最小化使用次数或代价**，且代价只与下标大小相关的 **换位/重排** 类问题（如 “最小代价使数组递增”“最小代价使数组全部相等”等）。  
- **一句话总结解题钥匙**：  
  > **“必计费用的下标不可省，剩余费用只选最小的可用下标”**。

---

## 反思

- **第一反应**：直接模拟交换，想把每个冲突都单独解决，结果是 **暴力搜索**，时间爆炸。  
- **最容易踩的坑**  
  - **可行性判断**：忽略了某个数在冲突位置出现太多导致无解的情况。  
  - **配对计数**：误以为每个冲突都必须找一个安全下标，导致在 `k < m` 的情况下错误返回 `-1`。  
  - **下标重复使用**：在计算费用时忘记每个下标只计一次（如果两冲突互换，只计一次费用）。  
- **下次类似题目第一步**：  
  > **先把“必须付费的元素”找出来（冲突下标），再分析“还能借用的资源”是否足够，最后用“最小代价的资源”完成配对**。这样就能快速定位到贪心或计数的核心思路。