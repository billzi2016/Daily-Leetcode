# #2541. 使数组相等的最少操作次数 II / Minimum Operations to Make Array Equal II

> 难度：中等 · 标签：Array、Math、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-make-array-equal-ii/)

---

## 题目（英文原版）

**Description**

You are given two integer arrays nums1 and nums2 of equal length n and an integer k. You can perform the following operation on nums1:
nums1 is said to be equal to nums2 if for all indices i such that 0 <= i < n, nums1[i] == nums2[i].
Return the minimum number of operations required to make nums1 equal to nums2. If it is impossible to make them equal, return -1.

**Examples**

**Example 1:**

```
Input: nums1 = [4,3,1,4], nums2 = [1,3,7,1], k = 3
Output: 2
Explanation: In 2 operations, we can transform nums1 to nums2.
1st operation: i = 2, j = 0. After applying the operation, nums1 = [1,3,4,4].
2nd operation: i = 2, j = 3. After applying the operation, nums1 = [1,3,7,1].
One can prove that it is impossible to make arrays equal in fewer operations.
```

**Example 2:**

```
Input: nums1 = [3,8,5,2], nums2 = [2,4,1,6], k = 1
Output: -1
Explanation: It can be proved that it is impossible to make the two arrays equal.
```

**Constraints**

- n == nums1.length == nums2.length
- 2 <= n <= 105
- 0 <= nums1[i], nums2[j] <= 109
- 0 <= k <= 105

---

## 题目（中文翻译）

给定两个等长的整数数组 `nums1` 和 `nums2`（长度均为 `n`），以及一个整数 `k`。你可以对 `nums1` 执行以下操作：

（原题中此处应描述具体的操作，保持原样）

当对所有满足 `0 <= i < n` 的下标 `i`，都有 `nums1[i] == nums2[i]` 时，称 `nums1` 与 `nums2` 相等。

返回使 `nums1` 等于 `nums2` 所需的最少操作次数。如果无法使两数组相等，返回 `-1`。

---

### 示例

#### 示例 1
**输入**  
`nums1 = [4,3,1,4]`, `nums2 = [1,3,7,1]`, `k = 3`  

**输出**  
`2`  

**解释**  
通过 2 次操作即可将 `nums1` 转换为 `nums2`。  
- 第一次操作：`i = 2`, `j = 0`。执行操作后，`nums1 = [1,3,4,4]`。  
- 第二次操作：`i = 2`, `j = 3`。执行操作后，`nums1 = [1,3,7,1]`。  

可以证明，使用更少的操作次数无法使两数组相等。

#### 示例 2
**输入**  
`nums1 = [3,8,5,2]`, `nums2 = [2,4,1,6]`, `k = 1`  

**输出**  
`-1`  

**解释**  
可以证明，无法通过任何次数的操作使两数组相等。

---

### 约束条件
- `n == nums1.length == nums2.length`
- `2 <= n <= 10^5`
- `0 <= nums1[i], nums2[j] <= 10^9`
- `0 <= k <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

这道题的操作其实很直观：  
> **一次操作**：选两个下标 `i`、`j`（`i ≠ j`），把 `k` 从 `nums1[j]` 转移到 `nums1[i]`。  
> 也就是 `nums1[i] += k`，`nums1[j] -= k`。

把它想象成 **把水从一个水桶倒到另一个水桶**，每次只能倒 `k` 升。  
如果某个位置的数太小，需要往里“倒进来”；如果太大，就需要把多余的“倒出去”。  

**暴力做法**：  
1. 对每个下标 `i`，计算它与目标值的差值 `diff[i] = nums2[i] - nums1[i]`。  
2. 只要还有正差（缺的）和负差（多的），就随便挑一对正负下标，进行一次转移。  
3. 重复直到所有差值都变成 `0`，或者发现无法继续（比如 `diff` 不是 `k` 的整数倍）。

**为什么正确**：  
- 每一次转移都把一个正差变小 `k`，把一个负差变大 `k`，所以总差值（所有 `diff` 的和）保持不变。  
- 当所有 `diff` 为 `0` 时，说明 `nums1` 已经等于 `nums2`。  

**时间/空间复杂度**：  
- 每一次转移只能把 **一个** 正差和 **一个** 负差各减少 `k`，所以如果正差总量是 `S`，最坏情况下需要 `S/k` 次操作。  
- 暴力实现会在每一步都遍历数组去找正负下标，导致 **时间复杂度** 大约是 `O(n * (S/k))`，在最坏情况下几乎是 `O(n²)`（因为 `S/k` 可能和 `n` 同阶）。  
- 只用了几个额外的变量，**空间复杂度** 为 `O(1)`。

> **大白话**：`O(n²)` 并不是真的 `n` 的平方，而是说“随着数据量增大，运行时间会像平方一样快”。这在 `n` 达到 `10⁵` 时根本不可接受。

#### 代码（Python）

```python
def minOperations_bruteforce(nums1, nums2, k):
    n = len(nums1)
    # 记录每个位置还差多少（正数需要增加，负数需要减少）
    diff = [nums2[i] - nums1[i] for i in range(n)]

    # 只要还有非零的差值，就不断找正负配对
    ops = 0
    while True:
        # 找到第一个正差和第一个负差
        pos = next((i for i, d in enumerate(diff) if d > 0), -1)
        neg = next((i for i, d in enumerate(diff) if d < 0), -1)

        # 全部为 0，说明已经相等
        if pos == -1 and neg == -1:
            return ops

        # 任意一方找不到配对，说明不可能完成
        if pos == -1 or neg == -1:
            return -1

        # 只能转移 k，若差值不是 k 的整数倍直接返回 -1
        if diff[pos] % k != 0 or diff[neg] % k != 0:
            return -1

        # 执行一次转移
        diff[pos] -= k   # 需要的正差减小
        diff[neg] += k   # 多余的负差增大（更接近 0）
        ops += 1
```

> 这段代码只能用来说明“最直接的想法”，在 `n=10⁵` 时会超时。

#### 复杂度  

- **时间复杂度**：`O(n * (S/k))`，最坏可视为 `O(n²)`，因为每一次循环都要遍历数组找正负下标。  
- **空间复杂度**：`O(1)`（不计输入数组本身）。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到两个**瓶颈**：

1. **每次都要遍历数组去找正负配对**——这导致 `O(n²)`。  
2. **一次只能处理 `k` 的单位**——其实我们可以一次性统计出总共需要转多少次 `k`，不必真的去模拟每一次转移。

**关键观察**  

- 对每个位置 `i`，如果 `diff[i] = nums2[i] - nums1[i]` 不是 `k` 的整数倍，那么无论怎么转移，都不可能恰好到达目标值，因为每次只能加/减 `k`。这就是 **不可达的直接判定**。  
- 整个数组的总和在一次操作前后保持不变（转移不创造也不消灭数值），所以 `sum(nums1) 必须等于 sum(nums2)`，等价于 `sum(diff) == 0`。如果不等，直接返回 `-1`。  
- 当上面两个条件都满足时，**每一次操作**恰好可以把一个 “缺 `k`” 的位置和一个 “多 `k`” 的位置配对完成。于是最少的操作次数就是 **所有缺的单位数**（或所有多的单位数）之和。  

> 用 “水桶” 的类比：  
> - 有若干水桶里水太少（缺 `k`），有若干水桶里水太多（多 `k`）。  
> - 每次我们只能把一勺 `k` 从多的倒到少的。  
> - 要把所有水桶调平，只需要把 **所有缺的勺数** 加起来，恰好等于所有多的勺数。  

**算法步骤**  

1. **特殊情况**：如果 `k == 0`，根本无法转移，只有 `nums1` 与 `nums2` 完全相等时才返回 `0`，否则返回 `-1`。  
2. 遍历数组，计算 `diff = nums2[i] - nums1[i]`。  
   - 若 `diff % k != 0` → 返回 `-1`（不可整除）。  
   - 把正的 `diff` 累加到 `pos_sum`，负的 `diff` 累加到 `neg_sum`（取绝对值）。  
3. 检查 `pos_sum` 是否等于 `neg_sum`（其实只要 `sum(diff) == 0` 即可）。若不相等返回 `-1`。  
4. 最小操作数 = `pos_sum // k`（或 `neg_sum // k`），因为 `pos_sum` 已经是缺的总量，除以一次能转多少 `k` 就是次数。  

**为什么是最优**：  
- 每一次操作只能解决 **一** 个正差单位和 **一** 个负差单位，无法一次性解决两个正差或两个负差。因此我们不可能用更少的次数完成全部转移。  
- 直接统计总缺量而不去“配对”具体下标，避免了额外的遍历，时间只需一次线性扫描。

#### 代码（Python）

```python
def minOperations(nums1, nums2, k):
    """
    返回最少的转移次数，使 nums1 变为 nums2；
    若无法完成返回 -1。
    """
    n = len(nums1)

    # k 为 0 时，根本没有转移的能力
    if k == 0:
        return 0 if nums1 == nums2 else -1

    pos_need = 0   # 所有正差的总和（缺多少）
    neg_need = 0   # 所有负差的总和（多多少）

    for a, b in zip(nums1, nums2):
        diff = b - a          # 目标 - 当前
        if diff % k != 0:     # 不能被 k 整除，必然不可能
            return -1
        if diff > 0:
            pos_need += diff  # 需要向该位置补 diff
        else:
            neg_need += -diff # 需要从该位置拿走 -diff

    # 总和必须相等（因为转移不改变整体和）
    if pos_need != neg_need:
        return -1

    # 每一次操作只能转移 k，缺多少就需要多少次
    return pos_need // k
```

> **代码解读**  
> - 第 5‑6 行处理 `k = 0` 的特殊情况。  
> - 第 11‑15 行判断 `diff` 能否被 `k` 整除——如果不能，直接返回 `-1`。  
> - 第 17‑20 行分别累计正、负差的绝对值。  
> - 第 23‑24 行利用 **总和相等** 的必要条件再次验证可行性。  
> - 第 27 行返回最少操作次数。

#### 复杂度  

- **时间复杂度**：`O(n)` —— 只遍历一次数组，`n ≤ 10⁵` 完全可接受。  
- **空间复杂度**：`O(1)` —— 只用了常数个额外变量。

---

## 心得  

- **核心技巧**：把每个位置的差值拆成 “需要增加的量” 与 “需要减少的量”，并利用 **可整除性** 与 **总和相等** 两个必要条件快速判断可行性。  
- **适用题型**：  
  1. “把数组通过固定步长的转移变成另一数组” 类题（如 LeetCode 2335 – Minimum Amount of Time to Fill Cups）。  
  2. “需要把多余的资源均匀分配” 的贪心/前缀和问题（如 1353. Maximum Number of Events That Can Be Attended）。  
  3. “只能增/减固定值的变换” 系列（如 1656. Design an Ordered Stream 中的差值检查）。  
- **一句话总结**：**把所有缺的 “k 单位” 加起来，就是最少的操作次数**。

---

## 反思  

- **第一反应**：看到“把 k 从一个位置转到另一个”，立刻想到“配对正负差”。  
- **最容易踩的坑**：  
  - 忘记检查 `diff % k == 0`，导致在不可整除时仍继续计算得到错误答案。  
  - 忽略 `k == 0` 的特殊情形，程序会出现除零错误或错误的正负配对。  
  - 只检查正差和负差是否相等，却忘记整体 `sum(nums1) == sum(nums2)`，在某些情况下会漏掉不可能的情况。  
- **下次类似题的第一步**：先 **把每个位置的差值除以步长 k**，确认是否都是整数；随后 **比较正负差的总量是否相等**，若相等答案就是总正差除以 `k`。这样可以在 O(n) 时间内得到最优解。