# #2035. **划分数组为两个子数组以最小化和的差值** / Partition Array Into Two Arrays to Minimize Sum Difference

> 难度：困难 · 标签：Array、Two Pointers、Binary Search、Dynamic Programming、Bit Manipulation、Ordered Set、Bitmask · [LeetCode 链接](https://leetcode.com/problems/partition-array-into-two-arrays-to-minimize-sum-difference/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums of 2 * n integers. You need to partition nums into two arrays of length n to minimize the absolute difference of the sums of the arrays. To partition nums, put each element of nums into one of the two arrays.
Return the minimum possible absolute difference.

**Examples**

**Example 1:**

```
Input: nums = [3,9,7,3]
Output: 2
Explanation: One optimal partition is: [3,9] and [7,3].
The absolute difference between the sums of the arrays is abs((3 + 9) - (7 + 3)) = 2.
```

**Example 2:**

```
Input: nums = [-36,36]
Output: 72
Explanation: One optimal partition is: [-36] and [36].
The absolute difference between the sums of the arrays is abs((-36) - (36)) = 72.
```

**Example 3:**

```
Input: nums = [2,-1,0,4,-2,-9]
Output: 0
Explanation: One optimal partition is: [2,4,-9] and [-1,0,-2].
The absolute difference between the sums of the arrays is abs((2 + 4 + -9) - (-1 + 0 + -2)) = 0.
```

**Constraints**

- 1 <= n <= 15
- nums.length == 2 * n
- -107 <= nums[i] <= 107

---

## 题目（中文翻译）

给定一个长度为 `2 * n` 的整数数组 `nums`。需要将 `nums` 划分为两个长度均为 `n` 的数组，使得两个数组的元素和之差的绝对值最小。划分时，将 `nums` 中的每个元素放入其中一个数组。

返回能够得到的最小的绝对差值。

**示例 1**  
**输入**: `nums = [3,9,7,3]`  
**输出**: `2`  
**解释**: 一种最优的划分方式是 `[3,9]` 和 `[7,3]`。两个数组的和之差的绝对值为 `abs((3 + 9) - (7 + 3)) = 2`。

**示例 2**  
**输入**: `nums = [-36,36]`  
**输出**: `72`  
**解释**: 一种最优的划分方式是 `[-36]` 和 `[36]`。两个数组的和之差的绝对值为 `abs((-36) - (36)) = 72`。

**示例 3**  
**输入**: `nums = [2,-1,0,4,-2,-9]`  
**输出**: `0`  
**解释**: 一种最优的划分方式是 `[2,4,-9]` 和 `[-1,0,-2]`。两个数组的和之差的绝对值为 `abs((2 + 4 + -9) - (-1 + 0 + -2)) = 0`。

**约束条件**

- `1 <= n <= 15`
- `nums.length == 2 * n`
- `-10^7 <= nums[i] <= 10^7`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**枚举所有可能的分法**，从 `2n` 个数里挑出恰好 `n` 个放进第一个数组，其余 `n` 个自然就进入第二个数组。  
- **数据结构**：我们可以用 **位掩码（bitmask）** 来表示一次挑选。把 `2n` 个位置看成 0/1 开关，`1` 表示该位置的元素进入第一个数组，`0` 表示进入第二个数组。位掩码就像一本字典，键是位置，值是“在不在第一组”。  
- **正确性**：遍历所有合法的位掩码（恰好有 `n` 位是 1），我们一定会碰到最优的那一种分法，计算它的两组和的差值并取最小即可。  

#### 代码（Python）  

```python
from itertools import combinations
from typing import List

def minimumDifference_bruteforce(nums: List[int]) -> int:
    n = len(nums) // 2                      # 每组的元素个数
    total = sum(nums)                       # 所有元素的和
    best = float('inf')                     # 当前找到的最小差值

    # 直接枚举所有「选 n 个」的组合
    for comb in combinations(range(2 * n), n):
        sum_first = sum(nums[i] for i in comb)   # 第一个数组的和
        sum_second = total - sum_first            # 第二个数组的和（剩下的）
        diff = abs(sum_first - sum_second)        # 绝对差值
        best = min(best, diff)                    # 维护最小值

    return best
```

> 关键点说明  
> - `combinations(range(2*n), n)` 相当于把所有位掩码里「恰好 n 位为 1」的情况枚举出来。  
> - `total - sum_first` 直接得到另一组的和，省去再次遍历的时间。  

#### 复杂度  

- **时间复杂度**：`O( C(2n, n) * n )`  
  - `C(2n, n)` 是组合数，表示「从 2n 个里挑 n 个」的种数。  
  - 每种组合我们要把选中的 `n` 个数加一次，花 `O(n)`。  
  - 直观上，这个复杂度会随着 `n` 增大而爆炸（比如 n=15 时约 155M 种），所以只能在极小规模下使用。  

- **空间复杂度**：`O(1)`（不计输入数组本身）  
  - 只用了常数个额外变量来保存临时和与最小值。  

---

### 2. 最优解  

#### 思路  

**瓶颈**  
暴力解的主要慢点在于**一次性枚举所有 `C(2n, n)` 种组合**。  
`n ≤ 15` 看似不大，但 `C(30,15) ≈ 1.55×10⁸` 已经远超一秒的计算上限。  

**优化思路：Meet-in-the-Middle（分治 + 二分）**  

1. **把数组对半分**  
   - 把原数组 `nums` 分成左半 `L`（前 `n` 个）和右半 `R`（后 `n` 个）。  
   - 每半的长度最多 15，**每半内部的子集数量只有 `2ⁿ ≤ 2¹⁵ = 32768`**，非常容易枚举。  

2. **预处理每半的“子集和表”**  
   - 对左半 `L`，枚举所有子集，并按照子集里选了多少个元素 `k`（0 ≤ k ≤ n）把对应的和放进 `sumL[k]`（一个列表）。  
   - 同理，对右半 `R` 得到 `sumR[k]`。  
   - 这一步相当于**把每半的所有可能的“局部和”**都记下来，后面再组合。  

3. **目标值**  
   - 整体所有数的和记为 `S`，两组最终的目标和应该尽量接近 `S/2`（因为差值 = `|2*sum_first - S|`）。  

4. **组合左右半的子集**  
   - 假设我们决定左半选 `k` 个数，它们的和为 `x ∈ sumL[k]`。  
   - 那么右半必须选 `n-k` 个数，和记为 `y ∈ sumR[n-k]`。  
   - 两半选完后，**第一个数组的总和**就是 `x + y`。  
   - 为了让 `x + y` 接近 `S/2`，我们只需要在 `sumR[n-k]` 中找一个 **最接近 `target - x`** 的值（`target = S/2`），这可以用**二分搜索**实现（因为我们会先把每个 `sumR[*]` 排序）。  

5. **遍历所有可能的 `k` 与 `x`**  
   - 对每个 `k`（0~n）遍历 `sumL[k]` 中的每个 `x`，在对应的 `sumR[n-k]` 中二分查找最佳 `y`，更新全局最小差值。  

**核心算法解释**  

- **位掩码枚举子集**：把一个长度为 `n` 的数组看成 `n` 位二进制数，`1` 表示取该位置的元素，`0` 表示不取。遍历 `0 … (1<<n)-1` 就能得到所有子集。  
- **二分搜索**：在已排好序的列表里找最接近某个目标值的元素。类似在字典里找最接近的页码。Python 的 `bisect` 模块可以直接完成。  

#### 代码（Python）  

```python
import bisect
from typing import List

def minimumDifference(nums: List[int]) -> int:
    """
    Meet-in-the-Middle + 二分搜索
    """
    n = len(nums) // 2                 # 每组的元素个数
    total = sum(nums)                  # 所有数的和
    target = total / 2                 # 理想的第一组和（越接近越好）

    left = nums[:n]                    # 前半
    right = nums[n:]                   # 后半

    # ---------- 1. 生成子集和表 ----------
    # sumL[k] : 所有在 left 中恰好选 k 个数的子集和（未排序）
    sumL = [[] for _ in range(n + 1)]
    sumR = [[] for _ in range(n + 1)]

    # 枚举 left 的子集
    for mask in range(1 << n):         # 0 ~ 2^n - 1
        cnt = 0                         # 选了多少个元素
        s = 0                           # 子集和
        for i in range(n):
            if mask >> i & 1:          # 第 i 位为 1，取 left[i]
                cnt += 1
                s += left[i]
        sumL[cnt].append(s)            # 放入对应的列表

    # 枚举 right 的子集（同理）
    for mask in range(1 << n):
        cnt = 0
        s = 0
        for i in range(n):
            if mask >> i & 1:
                cnt += 1
                s += right[i]
        sumR[cnt].append(s)

    # 为了二分搜索，先把每个列表排序
    for k in range(n + 1):
        sumR[k].sort()

    # ---------- 2. 组合左右半 ----------
    best = float('inf')                # 当前最小的绝对差

    for k in range(n + 1):             # left 选 k 个，right 必须选 n-k 个
        need = n - k
        for x in sumL[k]:              # 遍历所有左半的子集和
            # 我们希望 x + y 最接近 target
            # => y 最接近 target - x
            want = target - x
            idx = bisect.bisect_left(sumR[need], want)

            # 检查 idx 位置（如果在范围内）以及左侧的 idx-1，取更接近的
            for j in (idx - 1, idx):
                if 0 <= j < len(sumR[need]):
                    y = sumR[need][j]
                    cur_sum = x + y                # 第一个数组的总和
                    diff = abs(2 * cur_sum - total)  # |(sum1) - (sum2)|
                    if diff < best:
                        best = diff
            # 早停：如果已经达到 0，不能更好
            if best == 0:
                return 0

    return int(best)
```

> **代码要点注释**  
> - `mask >> i & 1`：把整数 `mask` 的第 `i` 位取出来，判断是否选该元素。  
> - `sumL` 与 `sumR` 按“选了多少个”分组，后面合并时只需要对应的 `k` 与 `n‑k`。  
> - `bisect_left` 在已排好序的 `sumR[need]` 中找到第一个 **≥ want** 的位置，左侧 `idx‑1` 则是 **< want** 的最大值，两者都是可能的最接近值。  
> - `abs(2*cur_sum - total)` 是差值的等价写法：`|sum1 - sum2| = |(sum1) - (total - sum1)| = |2*sum1 - total|`。  

#### 复杂度  

- **时间复杂度**：`O( n * 2^n + n * 2^n * log(2^n) ) ≈ O( n * 2^n )`  
  - 枚举左/右半子集各需 `2^n` 次，每次遍历 `n` 位求和 → `O(n·2^n)`。  
  - 合并时对每个左半子集和（总数也是 `2^n`）做一次二分搜索，二分的代价是 `log(2^n) = n`，于是同样是 `O(n·2^n)`。  
  - 对比暴力的 `O(C(2n,n)·n)`，这里的 `2^n`（最多 32768）远远小于 `C(30,15)`（约 1.55×10⁸），所以运行非常快。  

- **空间复杂度**：`O( n * 2^n )`  
  - 需要保存左右半的子集和表。每个表有 `n+1` 个列表，总元素数等于 `2^n`，每个元素是一个整数。对于 `n=15`，约 32768 个整数，完全可以放进内存。  

---

## 心得  

- **核心技巧**：**Meet-in-the-Middle（分半枚举） + 二分搜索**。  
- **适用题型**：  
  1. “从 2n 个数中挑 n 个，使和最接近某值”——本题。  
  2. “分割数组使两部分差值最小”——如 LeetCode 2035 “Partition Array Into Two Subsets With Minimum Difference”。  
  3. “子集和最接近目标值”——如 “Target Sum” 系列的变体。  
- **一句话总结**：把大规模的组合问题先 **对半拆**，把每半的所有可能存起来，再用 **二分** 把两半高效配对，即可把指数级的搜索压到可接受的 `2^{n/2}` 规模。  

---

## 反思  

- **第一反应**：直接想到“枚举所有选 `n` 个的组合”，因为这似乎最符合题意。  
- **最容易踩的坑**：  
  - **负数和大数的范围**：`nums[i]` 可能是负数，求和时一定使用 `int`（Python 自动大整数），但在其他语言要防止溢出。  
  - **目标是 `sum/2` 的小数**：`total` 可能是奇数，`target = total/2` 会是 0.5 的小数，二分时仍然可以用浮点数比较，只要最终差值用整数公式 `abs(2*cur_sum - total)`。  
  - **边界条件**：`k = 0` 或 `k = n` 时，需要确保 `sumR[n]` 与 `sumL[0]` 正确处理（它们分别只包含空子集的和 0）。  
- **下次类似题的第一步**：先判断 **是否可以把规模对半**（`n ≤ 30` 之类），若可以，就立刻采用 **Meet-in-the-Middle** 思路，而不是直接暴力枚举。这样往往能把不可解的问题变成可接受的复杂度。