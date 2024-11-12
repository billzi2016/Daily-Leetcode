# #2934. 数组中最后元素最大化的最少操作次数 / Minimum Operations to Maximize Last Elements in Arrays

> 难度：中等 · 标签：Array、Enumeration · [LeetCode 链接](https://leetcode.com/problems/minimum-operations-to-maximize-last-elements-in-arrays/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays, nums1 and nums2, both having length n.
You are allowed to perform a series of operations (possibly none).
In an operation, you select an index i in the range [0, n - 1] and swap the values of nums1[i] and nums2[i].
Your task is to find the minimum number of operations required to satisfy the following conditions:
Return an integer denoting the minimum number of operations needed to meet both conditions, or -1 if it is impossible to satisfy both conditions.

**Examples**

**Example 1:**

```
Input: nums1 = [1,2,7], nums2 = [4,5,3]
Output: 1
Explanation: In this example, an operation can be performed using index i = 2.
When nums1[2] and nums2[2] are swapped, nums1 becomes [1,2,3] and nums2 becomes [4,5,7].
Both conditions are now satisfied.
It can be shown that the minimum number of operations needed to be performed is 1.
So, the answer is 1.
```

**Example 2:**

```
Input: nums1 = [2,3,4,5,9], nums2 = [8,8,4,4,4]
Output: 2
Explanation: In this example, the following operations can be performed:
First operation using index i = 4.
When nums1[4] and nums2[4] are swapped, nums1 becomes [2,3,4,5,4], and nums2 becomes [8,8,4,4,9].
Another operation using index i = 3.
When nums1[3] and nums2[3] are swapped, nums1 becomes [2,3,4,4,4], and nums2 becomes [8,8,4,5,9].
Both conditions are now satisfied.
It can be shown that the minimum number of operations needed to be performed is 2.
So, the answer is 2.
```

**Example 3:**

```
Input: nums1 = [1,5,4], nums2 = [2,5,3]
Output: -1
Explanation: In this example, it is not possible to satisfy both conditions. 
So, the answer is -1.
```

**Constraints**

- 1 <= n == nums1.length == nums2.length <= 1000
- 1 <= nums1[i] <= 109
- 1 <= nums2[i] <= 109

---

## 题目（中文翻译）

**题目描述**  
给定两个下标从 0 开始的整数数组 `nums1` 和 `nums2`，二者长度相同，记为 `n`。  
你可以执行任意次数（包括 0 次）的以下操作：  
- 选择下标 `i`（`0 ≤ i ≤ n‑1`），交换 `nums1[i]` 与 `nums2[i]` 的值。

请你找出满足下列两条条件所需的最少操作次数：  

> - 经过所有操作后，`nums1` 的最后一个元素（即 `nums1[n‑1]`）是 `nums1` 中的最大值。  
> - 经过所有操作后，`nums2` 的最后一个元素（即 `nums2[n‑1]`）是 `nums2` 中的最大值。

返回满足上述两条条件的最小操作次数，如果无法同时满足两条条件，则返回 `-1`。

---

**示例**

**示例 1**  
```text
Input: nums1 = [1,2,7], nums2 = [4,5,3]
Output: 1
Explanation: 可以在下标 i = 2 处进行一次交换。  
交换后，`nums1` 变为 [1,2,3]，`nums2` 变为 [4,5,7]。  
此时两条条件均已满足，且所需操作次数最少为 1。
```

**示例 2**  
```text
Input: nums1 = [2,3,4,5,9], nums2 = [8,8,4,4,4]
Output: 2
Explanation: 可以按以下顺序进行两次交换：  
1. i = 4 时交换，`nums1` 变为 [2,3,4,5,4]，`nums2` 变为 [8,8,4,4,9]。  
2. i = 3 时交换，`nums1` 变为 [2,3,4,4,4]，`nums2` 变为 [8,8,4,5,9]。  
此时两条条件均已满足，且最少需要 2 次操作。
```

**示例 3**  
```text
Input: nums1 = [1,5,4], nums2 = [2,5,3]
Output: -1
Explanation: 无论如何交换，都无法同时使 `nums1[n‑1]` 成为 `nums1` 的最大值且 `nums2[n‑1]` 成为 `nums2` 的最大值。因此答案为 -1。
```

---

**约束条件**  

- `1 ≤ n = nums1.length = nums2.length ≤ 1000`  
- `1 ≤ nums1[i] ≤ 10^9`  
- `1 ≤ nums2[i] ≤ 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目要求通过在同一下标 `i` 处交换 `nums1[i]` 与 `nums2[i]`（一次操作），使得 **两条数组的最后一个元素分别成为各自数组的最大值**，即  

```
对所有 i（0 ≤ i < n）都有：
    nums1[i] ≤ nums1[n-1]   且   nums2[i] ≤ nums2[n-1]
```

最直接的想法是：**对每个下标 i（包括最后一个）都尝试“换”或“不换”，把所有可能的 0/1 组合枚举出来**，检查哪个组合满足上面的条件且换的次数最少。

- **数据结构**：我们只需要用普通的 `list` 保存两条数组，枚举时用一个整数的二进制位表示“这一次是否换”。二进制位就像字典的“钥匙”，0 表示不换，1 表示换。
- **为什么正确**：因为我们把 **所有** 可能的操作序列都穷举了，必然会覆盖最优的那一种。只要遍历完就能找出最小的换次数或判断根本没有合法方案。
- **时间/空间复杂度**：  
  - 枚举 `2ⁿ` 种可能（每个位置有 2 种选择），每种可能要遍历整个数组检查条件，故时间是 `O( n·2ⁿ )`。  
  - 只用了常数级别的额外空间（保存临时数组），空间是 `O(1)`。

> **大白话**：如果 `n = 10`，我们要尝试 `2¹⁰ = 1024` 种情况；如果 `n = 20`，情况数就已经是 `1,048,576`，明显会超时。

#### 代码（Python）

```python
from itertools import product
from copy import deepcopy
from typing import List

def min_operations_bruteforce(nums1: List[int], nums2: List[int]) -> int:
    n = len(nums1)
    best = float('inf')                     # 记录最小的换次数

    # 对每个下标 i (0~n-1) 生成 0/1，0 表示不换，1 表示换
    for mask in product([0, 1], repeat=n):
        a = deepcopy(nums1)                 # 复制一份，防止修改原数组
        b = deepcopy(nums2)

        # 按 mask 执行交换
        for i, need_swap in enumerate(mask):
            if need_swap:                    # 需要换
                a[i], b[i] = b[i], a[i]

        # 检查“最后一个元素是最大值”的条件
        if all(a[i] <= a[-1] and b[i] <= b[-1] for i in range(n)):
            best = min(best, sum(mask))      # 换的次数就是 mask 中 1 的个数

    return -1 if best == float('inf') else best
```

> 关键行解释  
> - `product([0, 1], repeat=n)`：相当于把 `0/1` 放进 `n` 位的二进制数，遍历所有组合。  
> - `a[i], b[i] = b[i], a[i]`：在 Python 中可以“一行代码”完成交换，类似把两个水杯的水倒来倒去。  
> - `all(a[i] <= a[-1] and b[i] <= b[-1] for i in range(n))`：检查每个位置的数是否都不超过各自的最后一个数。

#### 复杂度  

- **时间复杂度**：`O(n·2ⁿ)`  
  - `2ⁿ` 是所有可能的操作集合，`n` 是每次检查需要遍历的长度。  
  - 当 `n` 只有几位时还能接受，但题目 `n ≤ 1000` 时根本不可行。
- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了几个临时列表，规模不随 `n` 指数增长。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**真正的难点不在于每个位置是否换，而在于最后两个数 `nums1[n-1]` 与 `nums2[n-1]` 的取值**。因为条件只要求“所有数 ≤ 各自的最后一个数”，所以只要确定了这两个“上限”，其余位置的决定就变得非常直接。

**关键观察**：

1. **只需要考虑两种上限**  
   - 情形 A：不交换最后一位，`last1 = nums1[n-1]`、`last2 = nums2[n-1]`。  
   - 情形 B：交换最后一位，`last1 = nums2[n-1]`、`last2 = nums1[n-1]`（此时已经用了 1 次操作）。

2. 对于任意其他下标 `i (0 ≤ i < n-1)`，只有 **三种可能**（正是题目提示）：

   | 条件 | 需要做什么 |
   |------|------------|
   | `nums1[i] ≤ last1` 且 `nums2[i] ≤ last2` | **不换**，已经满足 |
   | `nums1[i] ≤ last2` 且 `nums2[i] ≤ last1` | **必须换**，换后才满足 |
   | 其它情况 | **无解**，无论换不换都达不到条件 |

   这相当于在每个位置上检查两本“字典”——`last1` 和 `last2`，看当前的两个数能否“放进对应的格子”。如果只能放进对调后的格子，就必须调换；如果两格子都装不下，那整个情形就不可能。

3. 因此，**每种情形只需要一次线性扫描**，统计必须换的次数；如果在扫描过程中出现“无解”，则该情形直接舍弃。

4. 最终答案是两种情形的换次数的最小值（记得情形 B 多算了最开始的那一次换）。

**算法步骤**（伪代码）：

```
def solve_one(last1, last2):
    swaps = 0
    for i in range(n-1):
        if nums1[i] <= last1 and nums2[i] <= last2:
            continue                # 不需要换
        elif nums1[i] <= last2 and nums2[i] <= last1:
            swaps += 1              # 必须换
        else:
            return INF              # 这一次上限不可能
    return swaps

ansA = solve_one(nums1[-1], nums2[-1])           # 不换最后一位
ansB = 1 + solve_one(nums2[-1], nums1[-1])       # 先换最后一位，再处理其余
answer = min(ansA, ansB)
if answer == INF: return -1
else: return answer
```

**为什么是最优**：

- 我们已经证明：只要确定了最后两个数的取值，其他位置的最优决策是唯一的（不换或必须换），不存在“贪心失误”。因为每个位置的约束是独立的，只受 `last1`、`last2` 影响。
- 只枚举了两种可能的上限，已经覆盖所有合法的全局解（要么最后一位保持原样，要么换一次）。
- 线性扫描一次即可得到所需换次数，时间是 `O(n)`，这是对 `n ≤ 1000` 完全足够的。

#### 代码（Python）

```python
from typing import List

INF = 10 ** 9          # 一个足够大的数，代表“不可能”

def _need_swaps(nums1: List[int], nums2: List[int],
                last1: int, last2: int) -> int:
    """
    计算在已固定的 last1（nums1 的上限） 和 last2（nums2 的上限）下，
    其余位置最少需要换几次才能满足条件。
    若出现不可满足的下标，返回 INF 表示无解。
    """
    swaps = 0
    n = len(nums1)
    for i in range(n - 1):               # 最后一个下标已经决定，不再遍历
        a, b = nums1[i], nums2[i]

        # 情形 1：直接满足，不需要换
        if a <= last1 and b <= last2:
            continue

        # 情形 2：只能在换位后满足，必须换
        if a <= last2 and b <= last1:
            swaps += 1
            continue

        # 情形 3：两种方式都不行，直接返回无解
        return INF

    return swaps


def min_operations(nums1: List[int], nums2: List[int]) -> int:
    """
    返回最少的交换次数，使得两条数组的最后一个元素分别成为各自的最大值。
    若不存在合法方案，返回 -1。
    """
    n = len(nums1)

    # 情形 A：不换最后一位
    case_a = _need_swaps(nums1, nums2, nums1[-1], nums2[-1])

    # 情形 B：先换最后一位（已经用了 1 次操作），再处理其余
    case_b = _need_swaps(nums1, nums2, nums2[-1], nums1[-1])
    if case_b != INF:                     # 只在可行时才加上那一次换
        case_b += 1

    ans = min(case_a, case_b)
    return -1 if ans == INF else ans
```

> 关键行解释  
> - `if a <= last1 and b <= last2:`：相当于检查“这两个数都能直接放进各自的抽屉”。  
> - `if a <= last2 and b <= last1:`：只能把它们互换后才放得进去，必须换一次。  
> - `return INF`：一旦出现“既不放进抽屉也不放进调换后的抽屉”，说明当前上限根本不可能实现，直接放弃该情形。  
> - `case_b += 1`：因为我们在情形 B 中已经把最后一位换了一次，这一步不能忘记计数。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历两次数组（情形 A 与 B），每次线性扫描一次。  
  - 与 `n` 成正比，`n ≤ 1000` 完全没问题。
- **空间复杂度**：`O(1)`  
  - 只用了若干整数变量，未额外开辟与输入规模相关的数组。

---

## 心得

- **核心技巧**：把“最后一个元素是最大值”转化为 **两个上限**（`last1`、`last2`），然后对每个位置进行 **分类判断**（不换 / 必须换 / 无解）。
- **适用的题型**  
  1. “使数组的最后一个元素成为最大值/最小值” 类似的约束（如 LeetCode 1722 / 1665）。  
  2. “每个位置只能在两种状态之间切换，且全局目标只依赖几条关键值” 的贪心/枚举题。  
  3. “同下标元素只能互换” 的配对问题（如 “最小交换次数让两数组相等”）。
- **一句话总结解题钥匙**：**先固定两条数组的“目标上限”，再逐个位置用“只能不换或必须换”做出唯一决定**。

---

## 反思

- **第一反应**：看到“交换同下标的两个数”就想把所有组合枚举（暴力），因为这样最直观能保证不遗漏任何情况。
- **最容易踩的坑**  
  - 忘记 **最后一位** 也可以被交换，导致只算了一种上限而漏掉另一种可能。  
  - 在判断“必须换”时，只检查了 `nums1[i] <= last2`，忘记同步检查 `nums2[i] <= last1`（两者必须同时满足）。  
  - 边界情况：`n = 1` 时，仅有最后一位，答案要么是 `0`（本身已经是最大）要么是 `1`（交换后满足），代码需正确处理。
- **下次遇到同类题**：第一步先 **确定全局目标只依赖哪些关键元素**（通常是最大/最小/目标值），随后 **枚举这些关键元素的可能取值**，对剩余元素做一次线性判断即可。这样可以把指数级搜索降到线性时间。