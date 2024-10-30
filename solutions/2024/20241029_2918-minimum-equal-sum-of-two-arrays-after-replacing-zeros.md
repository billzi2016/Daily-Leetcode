# #2918. 替换 0 后两数组的最小相等和 / Minimum Equal Sum of Two Arrays After Replacing Zeros

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-equal-sum-of-two-arrays-after-replacing-zeros/)

---

## 题目（英文原版）

**Description**

You are given two arrays nums1 and nums2 consisting of positive integers.
You have to replace all the 0's in both arrays with strictly positive integers such that the sum of elements of both arrays becomes equal.
Return the minimum equal sum you can obtain, or -1 if it is impossible.

**Examples**

**Example 1:**

```
Input: nums1 = [3,2,0,1,0], nums2 = [6,5,0]
Output: 12
Explanation: We can replace 0's in the following way:
- Replace the two 0's in nums1 with the values 2 and 4. The resulting array is nums1 = [3,2,2,1,4].
- Replace the 0 in nums2 with the value 1. The resulting array is nums2 = [6,5,1].
Both arrays have an equal sum of 12. It can be shown that it is the minimum sum we can obtain.
```

**Example 2:**

```
Input: nums1 = [2,0,2,0], nums2 = [1,4]
Output: -1
Explanation: It is impossible to make the sum of both arrays equal.
```

**Constraints**

- 1 <= nums1.length, nums2.length <= 105
- 0 <= nums1[i], nums2[i] <= 106

---

## 题目（中文翻译）

给定两个只包含正整数（positive integer）的数组 `nums1` 和 `nums2`（array）。你需要将两个数组中的所有 `0` 替换为严格正整数（strictly positive integer），使得两数组的元素和相等。返回能够得到的最小相等和，如果无法实现则返回 `-1`。

**示例 1**  
**输入**: `nums1 = [3,2,0,1,0]`, `nums2 = [6,5,0]`  
**输出**: `12`  
**解释**: 我们可以按以下方式替换 `0`：  
- 将 `nums1` 中的两个 `0` 分别替换为 `2` 和 `4`，得到 `nums1 = [3,2,2,1,4]`。  
- 将 `nums2` 中的 `0` 替换为 `1`，得到 `nums2 = [6,5,1]`。  
两个数组的和均为 `12`，且可以证明这是能够得到的最小和。

**示例 2**  
**输入**: `nums1 = [2,0,2,0]`, `nums2 = [1,4]`  
**输出**: `-1`  
**解释**: 无法使两个数组的和相等。

**约束条件**  
- `1 <= nums1.length, nums2.length <= 10^5`  
- `0 <= nums1[i], nums2[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有 0 用正整数填满**，然后检查两数组的和是否相等。  
如果不相等，就**枚举所有可能的填充值**（每个 0 可以是 1、2、3……），看是否能得到相同的总和，并记录最小的相等和。

- **使用的数据结构**：  
  - 两个普通的 Python 列表（list），用来存放数组本身。  
  - 可以把“所有可能的填充值”想象成一本《数字字典》：键（key）是第几个 0，值（value）是我们给它选的正整数。我们要遍历这本字典的每一种组合。

- **为什么正确**：  
  - 我们把 **所有** 合法的填法都尝试了一遍，只要有一种能让两数组和相等，就一定会在枚举过程中被发现。

- **时间/空间复杂度**：  
  - 假设数组中一共有 `z` 个 0，每个 0 可以取 `k`（理论上无限）种正整数。即使我们把取值范围限制在 `1…M`（比如 `M = 10`），枚举的组合数也是 `M^z`，指数级增长。  
  - **时间复杂度** 大约是 **O(M^z)**，这在实际数据（`z` 可能上万）下根本不可行。  
  - **空间复杂度** 只需要保存几个变量和递归栈，约 **O(z)**，但这点并不能抵消巨大的时间开销。

#### 代码（Python）

```python
from itertools import product
from typing import List

def brute_min_equal_sum(nums1: List[int], nums2: List[int]) -> int:
    # 统计两个数组中 0 的下标
    zero_idx1 = [i for i, v in enumerate(nums1) if v == 0]
    zero_idx2 = [i for i, v in enumerate(nums2) if v == 0]

    # 如果两个数组都没有 0，直接比较原始和
    if not zero_idx1 and not zero_idx2:
        s1, s2 = sum(nums1), sum(nums2)
        return s1 if s1 == s2 else -1

    # 为了演示，这里只枚举 1~5 的可能（实际不可行）
    MAX_VAL = 5
    best = float('inf')

    # 把两个数组的 0 合在一起，统一枚举
    all_zero_idx = [(1, i) for i in zero_idx1] + [(2, i) for i in zero_idx2]

    for vals in product(range(1, MAX_VAL + 1), repeat=len(all_zero_idx)):
        # 把枚举的值填回数组
        a1, a2 = nums1[:], nums2[:]
        for (arr_id, pos), v in zip(all_zero_idx, vals):
            if arr_id == 1:
                a1[pos] = v
            else:
                a2[pos] = v
        s1, s2 = sum(a1), sum(a2)
        if s1 == s2:
            best = min(best, s1)

    return best if best != float('inf') else -1
```

> **注意**：上面的代码只用于说明思路，`MAX_VAL` 必须非常大才能覆盖所有合法解，而 `product` 的组合数会爆炸，实际跑不到 10⁵ 长度的数组。

#### 复杂度  

- **时间复杂度**：`O(M^z)`（指数级），`M` 是我们假设的最大取值，`z` 是 0 的个数。  
  - 用大白话说，就是“如果你有 10 个 0，每个可以选 1~100 的数，你得尝试 100^10 ≈ 10²⁰ 次”，根本不可能在电脑里跑完。  
- **空间复杂度**：`O(z)`，只需要保存 0 的位置和递归/迭代的临时变量。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到**枚举所有可能是不可行的**，真正的难点在于**找出最小的相等和**。  
观察可以得到以下关键事实：

1. **所有 0 必须被替换成“严格正整数”。**  
   - 正整数的最小值是 1。  
   - 因此，如果我们把每个 0 都先换成 **1**，得到的两个数组的和就是**能够得到的最小总和**（因为任何更大的数只会让总和更大）。

2. **把所有 0 换成 1 后的和**记为 `sum1`（数组 1）和 `sum2`（数组 2）。  
   - 如果 `sum1 == sum2`，说明已经达成相等，而且这是最小可能的相等和，直接返回 `sum1` 即可。

3. **如果 `sum1 != sum2`，我们只能让较小的那个和变大**（因为只能把 0 换成更大的正整数，不能让已经的和变小）。  
   - 设 `sum_small = min(sum1, sum2)`，`sum_big = max(sum1, sum2)`。  
   - 为了让两边相等，**只需要把较小那边的某个 0 的值从 1 增加到 `1 + (sum_big - sum_small)`**，即把差值全部加到同一个位置上。  
   - 这要求**较小和对应的数组中至少有一个 0**，否则我们没有任何“可以增大”的位置，只能保持原来的和，显然达不到相等。

4. **因此答案的判定非常简单**：  
   - 若两数组的最小和相等 → 返回该和。  
   - 否则，若 **较小和的数组里有至少一个 0** → 返回 `sum_big`（因为我们把差值全部补到一个 0 上，使得两边都等于 `sum_big`）。  
   - 否则 → 返回 `-1`，表示不可能。

这整个过程只需要一次遍历即可得到 `sum1`、`sum2` 以及每个数组是否含有 0，时间 **O(n)**，空间 **O(1)**。

**类比**：把每个 0 想象成一张“空白的支票”。最保守的做法是把每张支票的金额写成 1 元，这样支票的总额最小。如果两个人的支票总额已经相同，那我们就不需要再改动。如果不相同，只有拥有支票的人才能往支票上再添钱，使得两个人的总额相等。只要有一张支票，就可以一次性把差额全部填进去。

#### 代码（Python）

```python
from typing import List

def min_equal_sum(nums1: List[int], nums2: List[int]) -> int:
    """
    返回在把所有 0 替换为正整数后，两个数组能够得到的最小相等和。
    若不可能则返回 -1。
    """
    # 计算把所有 0 都换成 1 时的总和
    sum1 = sum(nums1) + nums1.count(0)  # 每个 0 额外加 1
    sum2 = sum(nums2) + nums2.count(0)

    # 两边已经相等 → 直接返回最小可能的和
    if sum1 == sum2:
        return sum1

    # 哪边更小，哪边更大
    if sum1 < sum2:
        smaller_sum, larger_sum = sum1, sum2
        smaller_has_zero = 0 in nums1
    else:
        smaller_sum, larger_sum = sum2, sum1
        smaller_has_zero = 0 in nums2

    # 只有在较小和对应的数组里还有 0，才能把差值全部加到某个 0 上
    if smaller_has_zero:
        return larger_sum          # 这是最小的相等和
    else:
        return -1                  # 没有可增大的位置， impossible
```

**代码要点解释**：

- `nums1.count(0)` 统计数组中 0 的个数，等价于把每个 0 先当成 1，实际贡献 `+1`。
- `sum(nums1) + nums1.count(0)` 就是 **“所有 0 换成 1 后的总和”**。
- `0 in nums1`（或 `nums2`）直接判断该数组是否还有 0，决定是否能增大。

#### 复杂度  

- **时间复杂度**：`O(n)`，其中 `n = len(nums1) + len(nums2)`。  
  - 只遍历两遍数组（一次求和并计数），没有嵌套循环。  
  - 与暴力解的指数级时间相比，**线性时间**意味着即使 `10⁵` 长度的数组也能在毫秒级完成。

- **空间复杂度**：`O(1)`，只使用了常数个额外变量（几个整数和布尔值），不随输入规模增长。

---

## 心得

- **核心技巧**：把所有未知的正整数先取最小可能值（1），得到“下界”。再根据差值判断是否可以通过把某个 0 增大来达成相等。  
- **该技巧适用的题型**：  
  1. 需要在若干“可调节”位置上填入正整数，使两边某种量相等的题目（如 “最小相等和” 类似题）。  
  2. “把所有未知值设为最小，随后只增大少数位置” 的贪心问题。  
  3. 只需要判断 **是否可能** 而不是枚举所有方案的题目（如 “是否可以通过一次修改让数组递增”）。
- **一句话总结解题钥匙**：先把所有可变的数取最小值，得到最小总和；若两边不相等，只要拥有可增大的位置，就把差额一次性补上。

---

## 反思

- **第一反应**：看到 “把 0 替换成正整数” 立刻想到 “把 0 当成 1 再调大”，因为 1 是正整数里最小的。  
- **最容易踩的坑**：  
  - 忽略了 **“必须严格正整数”** 的限制，误把 0 直接当作 0 填写。  
  - 没有检查较小和对应的数组是否真的还有 0，导致在没有可增大位置时错误地返回了 `larger_sum`。  
  - 处理大数时忘记 Python 的整数可以无限大，其实不需要担心溢出，但在其他语言可能要考虑。  
- **下次遇到同类题**：第一步先 **把所有可变的数设为最小值**（这里是 1），计算两边的最小总和，再比较大小并检查是否还有 “可增大” 的位置。这样可以迅速判断可行性并得到最小答案。