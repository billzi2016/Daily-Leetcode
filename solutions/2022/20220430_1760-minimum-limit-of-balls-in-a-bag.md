# #1760. **袋子中球的最小上限** / Minimum Limit of Balls in a Bag

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/)

---

## 题目（英文原版）

**Description**

You are given an integer array nums where the ith bag contains nums[i] balls. You are also given an integer maxOperations.
You can perform the following operation at most maxOperations times:
Your penalty is the maximum number of balls in a bag. You want to minimize your penalty after the operations.
Return the minimum possible penalty after performing the operations.

**Examples**

**Example 1:**

```
Input: nums = [9], maxOperations = 2
Output: 3
Explanation: 
- Divide the bag with 9 balls into two bags of sizes 6 and 3. [9] -> [6,3].
- Divide the bag with 6 balls into two bags of sizes 3 and 3. [6,3] -> [3,3,3].
The bag with the most number of balls has 3 balls, so your penalty is 3 and you should return 3.
```

**Example 2:**

```
Input: nums = [2,4,8,2], maxOperations = 4
Output: 2
Explanation:
- Divide the bag with 8 balls into two bags of sizes 4 and 4. [2,4,8,2] -> [2,4,4,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,4,4,4,2] -> [2,2,2,4,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,2,2,4,4,2] -> [2,2,2,2,2,4,2].
- Divide the bag with 4 balls into two bags of sizes 2 and 2. [2,2,2,2,2,4,2] -> [2,2,2,2,2,2,2,2].
The bag with the most number of balls has 2 balls, so your penalty is 2, and you should return 2.
```

**Constraints**

- 1 <= nums.length <= 105
- 1 <= maxOperations, nums[i] <= 109

---

## 题目（中文翻译）

给定一个整数数组 `nums`，其中第 `i` 个袋子里装有 `nums[i]` 个球。同时给定一个整数 `maxOperations`。  
你可以至多执行 `maxOperations` 次以下操作：

- 选择任意一个袋子，设其球数为 `x`，将其分成两个新袋子，分别装 `⌊x/2⌋` 和 `⌈x/2⌉` 个球。

你的**惩罚**定义为所有袋子中球数的最大值。请在最多进行 `maxOperations` 次操作后，使惩罚最小化，并返回可能的最小惩罚值。

---

### 示例

#### 示例 1
```text
Input: nums = [9], maxOperations = 2
Output: 3
Explanation:
- 将装有 9 球的袋子分成 6 球和 3 球的两个袋子。 [9] → [6,3]。
- 将装有 6 球的袋子再次分成 3 球和 3 球的两个袋子。 [6,3] → [3,3,3]。
此时最大袋子中的球数为 3，惩罚为 3，返回 3。
```

#### 示例 2
```text
Input: nums = [2,4,8,2], maxOperations = 4
Output: 2
Explanation:
- 将装有 8 球的袋子分成 4 球和 4 球的两个袋子。 [2,4,8,2] → [2,4,4,4,2]。
- 将其中一个装有 4 球的袋子分成 2 球和 2 球的两个袋子。 [2,4,4,4,2] → [2,2,2,4,4,2]。
- 再将另一个装有 4 球的袋子分成 2 球和 2 球的两个袋子。 [2,2,2,4,4,2] → [2,2,2,2,2,4,2]。
- 再将剩余的装有 4 球的袋子分成 2 球和 2 球的两个袋子。最终所有袋子中的球数均不超过 2。
因此最小可能的惩罚为 2，返回 2。
```

---

### 约束

- `1 <= nums.length <= 10^5`
- `1 <= maxOperations, nums[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把每个袋子不停地拆**，直到我们已经用了不超过 `maxOperations` 次操作，然后直接看最大的袋子有多少球。  
- **数据结构**：我们只需要一个普通的 Python 列表 `nums`，把它当作“一堆装有球的袋子”。  
- **为什么能得到答案**：因为题目只限制操作次数，而没有限制我们必须一次只拆一个袋子，所以只要我们把 **所有** 袋子都拆到最小可能的大小（只要还有操作次数），最终的最大袋子大小必然是最小的。  

实现上可以把每个袋子 **一次只拆成两半**（比如 9 → 5+4），这样每拆一次就产生一个新袋子。我们把所有可能的拆法都枚举出来，直到用完 `maxOperations`，最后遍历所有袋子取最大值即为答案。

**然而**：  
- `nums[i]` 最大可达 `10^9`，而 `maxOperations` 也可能是 `10^9`。如果我们真的去“一次一次”拆，最多会产生 `O(maxOperations)` 个新袋子，根本不可能在时间限制内完成。  
- 即使我们把每个袋子一次性拆成若干均匀的小袋子（比如把 9 拆成 3、3、3），我们也需要遍历所有可能的 **拆分数**，这会导致指数级的搜索。

所以暴力方法只能作为思考的起点，实际不可行。

#### 代码（Python）

```python
def minimumPenalty_bruteforce(nums, maxOperations):
    # 暴力思路：枚举每个袋子可以拆成的份数（1~len(nums)+maxOperations），
    # 计算需要的操作数，选出最小的最大袋子大小。
    # 这里仅作概念展示，实际运行会超时。
    best = max(nums)          # 初始惩罚：不做任何操作时的最大袋子

    # 对每个可能的“目标最大袋子大小”尝试
    for target in range(1, best + 1):
        ops = 0               # 为了让所有袋子 ≤ target，需要的操作次数
        for x in nums:
            # 如果一个袋子有 x 球，想让每个子袋子 ≤ target，
            # 必须把它拆成 ceil(x / target) 个子袋子，
            # 这需要的操作次数是 (子袋子数 - 1)
            ops += (x - 1) // target   # 等价于 ceil(x/target)-1
        if ops <= maxOperations:      # 操作次数够用，target 可行
            best = target
            break                     # 已经找到最小可行的 target
    return best
```

> **关键注释**  
> - `(x - 1) // target` 等价于 `ceil(x / target) - 1`，表示把 `x` 球的袋子拆成每个不超过 `target` 所需的最少拆分次数。  

#### 复杂度  

- **时间复杂度**：`O(max(nums) * n)`，因为外层循环会遍历从 `1` 到最大袋子大小（最坏情况是 `10^9`），每次又遍历全部 `n`（`≤10^5`）个袋子。  
  - 用大白话说，就是“把每个可能的最大值都试一遍”，显然太慢。  
- **空间复杂度**：`O(1)`，只用了常数级的额外变量。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到 **关键在于判断**：  
> 给定一个**假设的最大袋子大小** `limit`，我们最少需要多少次拆分才能让所有袋子都 ≤ `limit`？

如果我们能快速计算出所需的最小操作次数 `needOps(limit)`，就可以把问题转化为：

> 找到最小的 `limit`，使得 `needOps(limit) ≤ maxOperations`。

这正好符合**单调性**：  
- 当 `limit` 越大，**需要的拆分次数越少**（因为每个袋子本身已经比较小了）。  
- 当 `limit` 越小，**需要的拆分次数越多**（必须把大袋子拆得更细）。

单调性让我们可以**二分搜索**（Binary Search）整个答案空间，而不是线性枚举。

**如何计算 `needOps(limit)`？**  
对于一个袋子里有 `x` 球，如果我们希望每个子袋子 ≤ `limit`，最少需要把它拆成 `ceil(x / limit)` 个子袋子。  
拆一次会把一个袋子变成 **两个**，所以把一个袋子拆成 `k` 个子袋子需要 `k‑1` 次操作。于是：

```
needOps(limit) = Σ (ceil(nums[i] / limit) - 1)  for all i
```

在代码里 `ceil(a / b)` 可以写成 `(a + b - 1) // b`，或者更简洁地写成 `(a - 1) // b`（因为 `ceil(a/b) - 1 = (a-1)//b`）。

**二分搜索范围**：  
- 最小可能的 `limit` 是 `1`（最极端的把所有球都拆成单个球）。  
- 最大可能的 `limit` 是原数组的最大值 `max(nums)`，因为不做任何操作时最大袋子就是它。

二分的步骤如下：

1. `lo = 1, hi = max(nums)`  
2. 取中点 `mid = (lo + hi) // 2`  
3. 计算 `needOps(mid)`  
   - 若 `needOps(mid) ≤ maxOperations`，说明 `mid` 已经够小，**可以尝试更小的**，把 `hi = mid`  
   - 否则 `mid` 太小，需要更多操作，**应该增大**，把 `lo = mid + 1`  
4. 循环结束时 `lo`（或 `hi`）就是答案。

**类比**：  
把这个过程想象成在找一把**钥匙**，钥匙孔的宽度对应 `limit`，我们想要的钥匙刚好能打开锁且不需要太多“切割”。二分搜索就像把钥匙从中间开始尝试，一次把范围减半，快速锁定最合适的尺寸。

#### 代码（Python）

```python
from typing import List

def minimumPenalty(nums: List[int], maxOperations: int) -> int:
    """
    二分搜索答案：
    - lo: 可能的最小最大袋子大小（1）
    - hi: 可能的最大最大袋子大小（原数组的最大值）
    """
    lo, hi = 1, max(nums)          # 搜索区间 [lo, hi]

    while lo < hi:                 # 只要区间大于 1 就继续
        mid = (lo + hi) // 2       # 取中间值作为当前的“假设最大袋子大小”

        # 计算如果最大袋子大小不超过 mid，需要的最少操作次数
        ops = 0
        for x in nums:
            # (x - 1) // mid  等价于 ceil(x / mid) - 1
            ops += (x - 1) // mid
            # 提前终止：如果已经超过 maxOperations，就没必要继续累加
            if ops > maxOperations:
                break

        # 根据 ops 与 maxOperations 的比较调整二分区间
        if ops <= maxOperations:   # 说明 mid 已经够大，尝试更小的上限
            hi = mid               # 把右边界收紧到 mid
        else:                       # 需要的操作次数太多，mid 太小
            lo = mid + 1           # 把左边界右移到 mid+1

    # 循环结束时 lo == hi，指向最小可行的最大袋子大小
    return lo
```

> **代码要点**  
> - `ops += (x - 1) // mid` 直接给出每个袋子拆到 `mid` 以内所需的最少操作次数。  
> - `if ops > maxOperations: break` 用来 **提前退出**，防止在 `nums` 很大、`mid` 很小的情况下累加无意义的次数，提升常数因子。  
> - 二分循环使用 `while lo < hi`，而不是 `while lo <= hi`，这样可以避免死循环并直接在 `lo == hi` 时得到答案。

#### 复杂度  

- **时间复杂度**：`O(n * log M)`，其中 `n = len(nums)`（最多 `10^5`），`M = max(nums)`（最多 `10^9`）。  
  - `log M` 大约是 30（因为 `2^30 ≈ 10^9`），所以整体约为 `3·10^6` 次基本运算，完全可以在 1 秒左右跑完。  
  - 用大白话说，就是“每次把可能的答案范围砍掉一半，只需要大约 30 次检查”，每次检查遍历一次数组。  

- **空间复杂度**：`O(1)`，只用了几个整数变量，不随输入规模增长。

---

## 心得  

- **核心技巧**：把“最小化最大值”问题转化为“给定上限，计算最少需要的操作次数”，利用**单调性 + 二分搜索**快速定位答案。  
- **适用的题型**：  
  1. “在限定次数/资源下，使得最大值最小”——如 **Split Array Largest Sum**、**Capacity To Ship Packages Within D Days**。  
  2. “在限定阈值下，最少需要多少步/次数”——如 **Minimum Size Subarray Sum**（用滑动窗口）或 **Find Minimum Speed to Arrive On Time**（二分速度）。  
- **一句话总结解题钥匙**：**把“最小化最大值”转化为“检查阈值可行性”，利用单调性二分快速逼近**。

---

## 反思  

- **第一反应**：直接想“把每个袋子不断拆，直到用完操作次数”，于是想到遍历所有拆法——这显然是暴力。  
- **最容易踩的坑**：  
  - 忽略了 `ceil(x / limit) - 1` 的推导，导致错误的操作次数计算。  
  - 二分的上下界写反了（例如把 `hi` 设成 `max(nums) + 1` 导致死循环）。  
  - 没有提前退出累加 `ops`，在极端情况下会导致不必要的时间浪费。  
- **下次遇到同类题**，第一步应该先**判断是否存在单调性**（阈值增大 → 需求操作数不增），如果有，就立刻构造“可行性检查函数”，再用二分搜索答案。