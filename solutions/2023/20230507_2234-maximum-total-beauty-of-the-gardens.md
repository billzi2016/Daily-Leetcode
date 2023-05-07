# #2234. 花园的最大总美感 / Maximum Total Beauty of the Gardens

> 难度：困难 · 标签：Array、Two Pointers、Binary Search、Greedy、Sorting、Enumeration、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/maximum-total-beauty-of-the-gardens/)

---

## 题目（英文原版）

**Description**

Alice is a caretaker of n gardens and she wants to plant flowers to maximize the total beauty of all her gardens.
You are given a 0-indexed integer array flowers of size n, where flowers[i] is the number of flowers already planted in the ith garden. Flowers that are already planted cannot be removed. You are then given another integer newFlowers, which is the maximum number of flowers that Alice can additionally plant. You are also given the integers target, full, and partial.
A garden is considered complete if it has at least target flowers. The total beauty of the gardens is then determined as the sum of the following:
Return the maximum total beauty that Alice can obtain after planting at most newFlowers flowers.

**Examples**

**Example 1:**

```
Input: flowers = [1,3,1,1], newFlowers = 7, target = 6, full = 12, partial = 1
Output: 14
Explanation: Alice can plant
- 2 flowers in the 0th garden
- 3 flowers in the 1st garden
- 1 flower in the 2nd garden
- 1 flower in the 3rd garden
The gardens will then be [3,6,2,2]. She planted a total of 2 + 3 + 1 + 1 = 7 flowers.
There is 1 garden that is complete.
The minimum number of flowers in the incomplete gardens is 2.
Thus, the total beauty is 1 * 12 + 2 * 1 = 12 + 2 = 14.
No other way of planting flowers can obtain a total beauty higher than 14.
```

**Example 2:**

```
Input: flowers = [2,4,5,3], newFlowers = 10, target = 5, full = 2, partial = 6
Output: 30
Explanation: Alice can plant
- 3 flowers in the 0th garden
- 0 flowers in the 1st garden
- 0 flowers in the 2nd garden
- 2 flowers in the 3rd garden
The gardens will then be [5,4,5,5]. She planted a total of 3 + 0 + 0 + 2 = 5 flowers.
There are 3 gardens that are complete.
The minimum number of flowers in the incomplete gardens is 4.
Thus, the total beauty is 3 * 2 + 4 * 6 = 6 + 24 = 30.
No other way of planting flowers can obtain a total beauty higher than 30.
Note that Alice could make all the gardens complete but in this case, she would obtain a lower total beauty.
```

**Constraints**

- 1 <= flowers.length <= 105
- 1 <= flowers[i], target <= 105
- 1 <= newFlowers <= 1010
- 1 <= full, partial <= 105

---

## 题目（中文翻译）

Alice 是 **n** 个花园的看护人，她希望通过种植花朵来使所有花园的总美感最大化。  
给定一个下标从 **0** 开始的整数数组 `flowers`，长度为 **n**，其中 `flowers[i]` 表示第 **i** 个花园当前已经种植的花朵数量。已种植的花朵 **不能** 被移除。  
再给定一个整数 `newFlowers`，表示 Alice 最多还能额外种植的花朵总数。  
还有三个整数 `target`、`full`、`partial`。

- 当一个花园的花朵数量 **不少于** `target` 时，该花园被视为 **完整**（complete）。  
- 完整花园的美感贡献为 `full`。  
- 对所有 **未完整**（incomplete）的花园，取其中 **最少** 的花朵数量 `minIncomplete`（若不存在未完整的花园，则此项贡献为 0），其美感贡献为 `partial * minIncomplete`。  

所有花园的 **总美感** 为：

```
totalBeauty = full * (完整花园的数量) + partial * minIncomplete
```

返回 Alice 在至多种植 `newFlowers` 朵花后能够得到的 **最大总美感**。

---

## 示例

### 示例 1

```
Input: flowers = [1,3,1,1], newFlowers = 7, target = 6, full = 12, partial = 1
Output: 14
```

**解释**：Alice 可以这样种植：

- 在第 0 个花园种 2 朵 → 变为 3 朵  
- 在第 1 个花园种 3 朵 → 变为 6 朵（此时已完整）  
- 在第 2 个花园种 1 朵 → 变为 2 朵  
- 在第 3 个花园种 1 朵 → 变为 2 朵  

花园最终状态为 `[3,6,2,2]`，共种植了 `2 + 3 + 1 + 1 = 7` 朵花。  

- 完整花园的数量为 **1**，贡献 `1 * 12 = 12`。  
- 未完整花园中最少的花朵数量为 **2**，贡献 `1 * 2 = 2`。  

总美感 `12 + 2 = 14`，即为最大值。

---

### 示例 2

```
Input: flowers = [2,4,5,3], newFlowers = 10, target = 5, full = 2, partial = 6
Output: 30
```

**解释**：Alice 可以这样种植：

- 在第 0 个花园种 3 朵 → 变为 5 朵（完整）  
- 第 1 个花园不种 → 仍为 4 朵  
- 第 2 个花园不种 → 仍为 5 朵（完整）  
- 在第 3 个花园种 2 朵 → 变为 5 朵（完整）  

花园最终状态为 `[5,4,5,5]`，共种植了 `3 + 0 + 0 + 2 = 5` 朵花（未用完全部 `newFlowers` 也可以）。  

- 完整花园的数量为 **3**，贡献 `3 * 2 = 6`。  
- 未完整花园中最少的花朵数量为 **4**，贡献 `6 * 4 = 24`。  

总美感 `6 + 24 = 30`，即为最大值。

---

## 约束条件

- `1 <= flowers.length <= 10^5`
- `1 <= flowers[i], target <= 10^5`
- `1 <= newFlowers <= 10^10`
- `1 <= full, partial <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的种花方案**，然后计算每种方案得到的美丽值，取最大值。  
- 我们可以把每个花园想象成一个装水的水桶，`flowers[i]` 是已经有的水量，`newFlowers` 是我们手里还能倒进去的水。  
- 暴力做法就是：对每个花园决定倒多少水（0~`newFlowers`），只要总倒的水不超过 `newFlowers`，就算出完整花园的个数以及剩余花园的最小水量，进而算出总美丽。  

**为什么正确**：因为我们遍历了**所有**合法的倒水分配方式，最大美丽一定会在其中出现。

**时间/空间复杂度**：  
- 对 `n`（≤10⁵）个花园，每个花园的倒水量有 `newFlowers+1` 种可能，组合数是天文数字，实际根本不可能跑完。  
- 用大白话说，时间复杂度大约是 `O((newFlowers+1)^n)`，即指数级爆炸。  
- 空间上只需要保存原数组和当前方案，`O(n)`。

显然，这种“全枚举”根本不可行，只能作为概念上的“暴力”解。

#### 代码（Python）

```python
# 仅作概念演示，实际运行会超时/内存爆炸
def brute_force(flowers, newFlowers, target, full, partial):
    n = len(flowers)
    best = 0

    # 用递归枚举每个花园种多少朵
    def dfs(idx, left, cur):
        nonlocal best
        if idx == n:                     # 所有花园都决定好了
            # 计算美丽
            complete = sum(1 for v in cur if v >= target)
            min_incomplete = min((v for v in cur if v < target), default=0)
            beauty = complete * full + min_incomplete * partial
            best = max(best, beauty)
            return

        # 这棵花园最多还能种 left 朵
        for add in range(left + 1):
            cur.append(flowers[idx] + add)
            dfs(idx + 1, left - add, cur)
            cur.pop()

    dfs(0, newFlowers, [])
    return best
```

#### 复杂度  

- **时间复杂度**：`O((newFlowers+1)^n)` → 指数级，几乎不可能在限制内完成。  
- **空间复杂度**：`O(n)` → 递归栈和临时数组的大小。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**枚举每个花园的种花量**是最耗时的地方。我们需要 **把搜索空间压缩**，只在关键的、可能产生最优解的状态上做枚举。

关键观察：

1. **完整花园的选择**  
   - 若我们决定让 **k**（`0 ≤ k ≤ n`）个花园达到 `target`（或更高），显然应该挑 **已经种得最多的 k 棵** 来完成，因为它们离 `target` 最近，省的花更多。  
   - 这一步只需要把 `flowers` 排序，从大到小取前 `k` 棵。

2. **其余花园的最小值**  
   - 剩下的 `n‑k` 棵花园不一定都能达到 `target`，但它们的 **最小值**（记作 `minVal`）直接决定了部分美丽 `partial * minVal`。  
   - 为了让 `minVal` 尽可能大，我们应该 **把剩余的花均匀地提升**，先把最小的几棵提升到同一个高度，再提升更高的……这正是 **前缀和 + 二分查找** 能解决的场景。

3. **整体框架**  
   - 先把 `flowers` **升序**排序（方便前缀和），记 `a[0] ≤ a[1] ≤ … ≤ a[n‑1]`。  
   - 预先计算 **前缀和** `pref[i] = a[0] + … + a[i‑1]`（`pref[0]=0`），以及 **后缀和** `suf[i] = a[i] + … + a[n‑1]`（用于快速算把后 `k` 棵提升到 `target` 所需的花）。  
   - 对每个可能的 `k`（从 `0` 到 `n`）：
     1. **把后 `k` 棵花园补齐**到 `target`：需要的花量 `needFull = k*target - (sum of last k values)`. 如果 `needFull > newFlowers`，说明 `k` 太大，直接跳过。
     2. 剩余的花 `remain = newFlowers - needFull` 用来提升前 `n‑k` 棵，使它们的最小值尽可能大。  
        - 设我们想让最小值达到 `x (≤ target‑1)`，则必须把所有 `a[i] < x`（`i` 在 `[0, n‑k)`）提升到 `x`，所需花量为 `x * cnt - sum_of_those`.  
        - 这正是单调函数，**二分搜索** `x` 能在 `O(log target)` 内找到最大可实现的 `x`。  
        - 为了快速得到 `cnt` 与 `sum_of_those`，利用 **前缀和**：在已排序数组中，用 `bisect_right` 找到第一个 `≥ x` 的位置 `pos`，则 `cnt = pos`，`sum = pref[pos]`。
     3. 计算当前美丽 `beauty = k * full + x * partial`（如果 `k == n`，则所有花园都完整，`partial` 部分可以直接取 `target`，但题目规定只算完整园的 `full`，`partial` 部分对完整园不计）。  
     4. 记录最大值。

4. **特殊情况**  
   - 当 `full` 的价值极高，可能所有花园都应该完整，此时直接检查 `k = n`（只需要 `needFull`）即可。  
   - 当 `partial` 为 0，答案只和 `k * full` 有关，直接取最大可完成的 `k`。  
   - 当 `target` 本身已经比所有 `flowers[i]` 大很多，二分搜索的上界设为 `target-1` 即可。

#### 代码（Python）

```python
from bisect import bisect_right
from typing import List

def maximumBeauty(flowers: List[int], newFlowers: int,
                  target: int, full: int, partial: int) -> int:
    n = len(flowers)
    # 1. 先排序，升序方便前缀和
    flowers.sort()
    # 前缀和，pref[i] = sum of first i elements (0-index, 不含 i)
    pref = [0] * (n + 1)
    for i in range(n):
        pref[i + 1] = pref[i] + flowers[i]

    # 后缀和，suf[i] = sum of elements from i to n-1
    suf = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        suf[i] = suf[i + 1] + flowers[i]

    # 计算把后 k 棵花园补齐到 target 所需的花量（k 从 0 到 n）
    # 为了避免重复计算，预先准备一个数组 needFull[k]
    needFull = [0] * (n + 1)   # needFull[k] 对应补齐最后 k 棵
    for k in range(1, n + 1):
        # 最后 k 棵的下标区间是 [n-k, n)
        # 已有的花总数是 suf[n-k]
        needFull[k] = k * target - (suf[n - k])

    ans = 0

    # 主循环：枚举 k（完整花园的数量）
    for k in range(0, n + 1):
        # 需要的花不能超过 newFlowers
        if needFull[k] > newFlowers:
            continue

        # 剩余的花可以用来提升前 n-k 棵
        remain = newFlowers - needFull[k]

        # 如果所有花园都已经完整，直接算答案
        if k == n:
            ans = max(ans, n * full)   # 此时 partial 不再计入
            continue

        # 二分搜索在 [flowers[0], target-1] 区间找最大的最小值 x
        lo, hi = flowers[0], target - 1
        best_x = flowers[0]   # 至少保持原来的最小值

        while lo <= hi:
            mid = (lo + hi) // 2
            # 找到前 n-k 棵中 < mid 的数量
            pos = bisect_right(flowers, mid, 0, n - k)   # 只看前 n-k
            # 需要的花量 = mid * pos - sum(first pos elements)
            need = mid * pos - pref[pos]

            if need <= remain:        # 可以达到 mid
                best_x = mid
                lo = mid + 1
            else:                     # 花不够，降低目标
                hi = mid - 1

        # 计算当前美丽
        cur = k * full + best_x * partial
        ans = max(ans, cur)

    return ans
```

> **代码要点注释**  
> - `flowers.sort()`：把花园从少到多排，好比把水桶按容量从小到大排，后面方便“先把小的提升”。  
> - `pref`、`suf`：前缀和、后缀和就像是累计的水量，能在 **O(1)** 时间内算出任意区间的总和。  
> - `needFull[k]`：把最后 `k` 棵（已经最多的）补齐到 `target` 所需的花，直接用公式 `k*target - 已有总和`。  
> - `bisect_right`：在已排好的数组里找第一个大于 `mid` 的位置，相当于“找出所有小于目标高度的水桶”。  
> - 二分搜索的判定 `need <= remain`：如果剩余的花足够把这些小于 `mid` 的花园提升到 `mid`，说明 `mid` 可以达成，尝试更高的 `mid`。  

#### 复杂度  

- **时间复杂度**：  
  - 排序 `O(n log n)`。  
  - 主循环遍历 `k = 0 … n`，每次二分搜索 `log target`（≈ `log 10⁵` ≤ 17）并在二分内部使用 `bisect_right`（`O(log n)`），所以每次 `O(log target * log n)`。  
  - 整体 `O(n log n + n * log target * log n)`，在约束 `n ≤ 10⁵` 下完全可接受。  
  - 用大白话说：先把花园排好序花一点时间（像排队），然后对每种“完整园的数量”尝试一次，每次只用几次“找位置”和“算花量”，总共不会超过几百万次操作。

- **空间复杂度**：`O(n)`  
  - 主要是存储排序后的数组以及前缀/后缀和。除去输入本身，只用了线性额外空间。

---

## 心得

- **核心技巧**：  
  1. **贪心 + 排序**：要让 `k` 棵花园完整，优先选已经最接近 `target` 的花园。  
  2. **前缀和 + 二分**：在剩余花园中寻找最大的最小值，本质是“把最小的若干元素提升到同一高度”，二分配合前缀和可以在对数时间算出所需花量。  

- **适用的题型**  
  - “把数组中若干元素提升到某个阈值，求最大最小值” 类题，如 LeetCode 1514 *Path with Maximum Probability*（思路相似的二分+前缀）。  
  - “先选若干最优元素完成目标，再对剩余做均匀提升” 类，如 1763 *Minimum Number of Operations to Make Array Empty*（贪心+前缀）。  
  - “分段完成任务，先处理成本最低的” 类，如 1799 *Maximize Score After N Operations*（排序+贪心）。

- **一句话总结解题钥匙**  
  > “先把最容易完成的园子完整，其余园子只关心最小值，用排序 + 前缀和 + 二分把这一步做得最快。”

---

## 反思

- **第一反应**：看到 “完整园数 * full + 最小值 * partial” 这种线性组合，立刻想到“先决定完整园的数量”。  
- **最容易踩的坑**  
  1. **边界条件**：`k = n` 时所有园子都完整，`partial` 不再起作用，需要单独处理。  
  2. **二分上界**：最小值不可能超过 `target-1`（因为一旦达到 `target` 就算完整），否则会多算 `full`。  
  3. **大数溢出**：`newFlowers` 可达 `10¹⁰`，在 Python 中整数无限大，但在其他语言要注意使用 64 位。  
  4. **前缀和索引**：`bisect_right` 的区间必须限制在前 `n‑k`，否则会把已经完整的园子也算进去，导致错误的花量计算。  

- **下次遇到同类题的第一步**  
  > “先把要‘完整’的元素用贪心方式选出来（排序后取最容易的），剩下的只关心‘最小值’，用二分 + 前缀和求最大可达的最小值”。