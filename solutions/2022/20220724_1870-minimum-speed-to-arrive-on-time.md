# #1870. **到达目的地的最小速度** / Minimum Speed to Arrive on Time

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-speed-to-arrive-on-time/)

---

## 题目（英文原版）

**Description**

You are given a floating-point number hour, representing the amount of time you have to reach the office. To commute to the office, you must take n trains in sequential order. You are also given an integer array dist of length n, where dist[i] describes the distance (in kilometers) of the ith train ride.
Each train can only depart at an integer hour, so you may need to wait in between each train ride.
Return the minimum positive integer speed (in kilometers per hour) that all the trains must travel at for you to reach the office on time, or -1 if it is impossible to be on time.
Tests are generated such that the answer will not exceed 107 and hour will have at most two digits after the decimal point.

**Examples**

**Example 1:**

```
Input: dist = [1,3,2], hour = 6
Output: 1
Explanation: At speed 1:
- The first train ride takes 1/1 = 1 hour.
- Since we are already at an integer hour, we depart immediately at the 1 hour mark. The second train takes 3/1 = 3 hours.
- Since we are already at an integer hour, we depart immediately at the 4 hour mark. The third train takes 2/1 = 2 hours.
- You will arrive at exactly the 6 hour mark.
```

**Example 2:**

```
Input: dist = [1,3,2], hour = 2.7
Output: 3
Explanation: At speed 3:
- The first train ride takes 1/3 = 0.33333 hours.
- Since we are not at an integer hour, we wait until the 1 hour mark to depart. The second train ride takes 3/3 = 1 hour.
- Since we are already at an integer hour, we depart immediately at the 2 hour mark. The third train takes 2/3 = 0.66667 hours.
- You will arrive at the 2.66667 hour mark.
```

**Example 3:**

```
Input: dist = [1,3,2], hour = 1.9
Output: -1
Explanation: It is impossible because the earliest the third train can depart is at the 2 hour mark.
```

**Constraints**

- n == dist.length
- 1 <= n <= 105
- 1 <= dist[i] <= 105
- 1 <= hour <= 109
- There will be at most two digits after the decimal point in hour.

---

## 题目（中文翻译）

You are given a floating-point number `hour`, representing the amount of time you have to reach the office. To commute to the office, you must take `n` trains in sequential order. You are also given an integer array `dist` of length `n`, where `dist[i]` describes the distance (in kilometers) of the *i*‑th train ride.  

Each train can only depart at an integer hour, so you may need to wait in between each train ride.  

Return the minimum positive integer speed (in kilometers per hour) that all the trains must travel at for you to reach the office on time, or `-1` if it is impossible to be on time.  

Tests are generated such that the answer will not exceed `10^7` and `hour` will have at most two digits after the decimal point.  

---

### 示例

**示例 1**

```text
Input: dist = [1,3,2], hour = 6
Output: 1
```

**解释**  
在速度 `1` 时：
- 第一次列车耗时 `1/1 = 1` 小时。
- 因为已经在整数小时，所以在第 `1` 小时刻立即出发。第二次列车耗时 `3/1 = 3` 小时。
- 同理在第 `4` 小时刻立即出发。第三次列车耗时 `2/1 = 2` 小时。
- 你将在恰好第 `6` 小时到达。

**示例 2**

```text
Input: dist = [1,3,2], hour = 2.7
Output: 3
```

**解释**  
在速度 `3` 时：
- 第一次列车耗时 `1/3 = 0.33333` 小时。
- 由于此时不是整数小时，需要等到第 `1` 小时刻才出发。第二次列车耗时 `3/3 = 1` 小时。
- 此时已是整数小时，立即在第 `2` 小时刻出发。第三次列车耗时 `2/3 = 0.66667` 小时。
- 你将在第 `2.66667` 小时到达，满足 `hour = 2.7` 的要求。

**示例 3**

```text
Input: dist = [1,3,2], hour = 1.9
Output: -1
```

**解释**  
不可能准时到达，因为第三次列车最早只能在第 `2` 小时刻出发。

---

### 约束条件

- `n == dist.length`
- `1 <= n <= 10^5`
- `1 <= dist[i] <= 10^5`
- `1 <= hour <= 10^9`
- `hour` 最多保留两位小数。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举每一种可能的速度**，把速度从 `1` 开始一直往上试，直到找到第一个可以在 `hour` 小时内到达的速度（或者超过题目给出的上界 `10⁷` 仍然不行，就返回 `-1`）。

要判断某个速度 `v` 能否准时到达，需要模拟乘坐每趟火车的过程：

1. 第 `i` 趟火车的行驶时间是 `dist[i] / v`（公里 ÷ 公里/小时 = 小时）。  
2. 前 `n-1` 趟火车结束后必须**等到整数小时**才可以上车。也就是说如果 `dist[i] / v` 不是整数，就要把时间向上取整（向上取整相当于“等到下一个整点再出发”，就像公交车只在整点发车）。  
3. 最后一趟火车不需要等整点，直接把它的实际行驶时间加进去即可。  

如果把所有这些时间相加后 ≤ `hour`，说明速度 `v` 能够准时到达。

> **类比**：把每趟火车想象成一次“跑步”。跑完后如果不是整点，你只能站在原地等到下一分钟的整点才能继续跑，只有最后一次跑完后直接到达终点，不需要再等。

**为什么暴力法一定能得到答案**  
因为我们把所有可能的正整数速度都逐一尝试，必然会遍历到最小的满足条件的那个速度（如果存在的话）。  

**时间/空间复杂度**  

- 对每个速度 `v`，我们要遍历 `n` 条 `dist`，计算时间 → `O(n)`。  
- 速度最多需要尝试到 `10⁷`（题目保证答案不超过这个值），所以最坏情况下的时间是 `O(10⁷ * n)`，这在 `n ≤ 10⁵` 时根本不可接受（会超时）。  
- 只使用了常数级别的额外空间 → `O(1)`。

> **大白话**：`O(10⁷ * n)` 就像让你在十分钟内跑完十万公里，根本不可能完成。

#### 代码（Python）

```python
from math import ceil

def can_finish(speed: int, dist, hour: float) -> bool:
    """判断给定 speed 是否能在 hour 小时内到达"""
    total = 0.0
    # 前 n-1 趟需要向上取整
    for d in dist[:-1]:
        total += ceil(d / speed)          # 向上取整，相当于等到下一个整数小时
    # 最后一趟直接加实际时间
    total += dist[-1] / speed
    return total <= hour

def minSpeedOnTime_bruteforce(dist, hour):
    # 暴力枚举速度，从 1 到 10⁷
    for v in range(1, 10**7 + 1):
        if can_finish(v, dist, hour):
            return v
    return -1
```

#### 复杂度

- **时间复杂度**：`O(10⁷ * n)` —— 需要遍历每一个可能的速度，速度上限是 10⁷，每次检查要遍历全部 `n` 条路程。  
- **空间复杂度**：`O(1)` —— 只用了常数个变量。

---

### 2. 最优解

#### 思路  

暴力法的瓶颈在于**线性枚举速度**，而实际上**时间随速度单调递减**：速度越大，乘坐每趟火车所需的时间越短（且向上取整的结果也不会变大），所以总耗时只会越来越小。  

这正好满足**单调性**，我们可以用**二分查找**在速度空间里快速定位最小的可行速度。

**步骤概述**：

1. **确定搜索区间**  
   - 最小可能的速度是 `1`（题目要求正整数）。  
   - 最大可能的速度我们可以设为 `10⁷`（题目保证答案不超过它），或者更紧的上界：  
     `max_speed = ceil(max(dist) / (hour - (n - 1)))`（如果 `hour` 足够大，直接用 `10⁷` 更安全）。  
   - 设 `low = 1`, `high = 10⁷`（闭区间）。

2. **二分搜索**  
   - 取中点 `mid = (low + high) // 2`。  
   - 用与暴力法相同的 `can_finish(mid, dist, hour)` 检查 `mid` 是否可行。  
   - 若可行 → 说明答案可能更小，继续在左半边搜索 `high = mid - 1`。  
   - 若不可行 → 说明速度太慢，需要更大，搜索右半边 `low = mid + 1`。  

3. **结束条件**  
   - 当 `low` 超过 `high` 时，循环结束。  
   - 若在循环中记录了最后一次可行的 `mid`（记作 `ans`），则 `ans` 即为最小可行速度。  
   - 若没有任何可行的 `mid`，返回 `-1`。

**为什么二分能得到最小速度**  
因为总耗时随速度单调递减，满足二分查找的“左侧一定更小或等于，右侧一定更大”的性质。每次排除掉一半的速度区间，最多 `log₂(10⁷) ≈ 24` 次迭代即可确定答案。

**核心数据结构 / 算法解释**  

- **二分查找**：把一个有序（或单调）序列的搜索空间不断对半划分，快速定位目标。可以把它想象成在一本字典里找单词：先看中间页，如果单词在前面就往前翻，否则往后翻。  
- **向上取整 (`ceil`)**：把时间向上取到最近的整数小时，等价于“等到下一趟火车的发车时间”。在 Python 中 `math.ceil` 能直接完成。  

#### 代码（Python）

```python
from math import ceil

def can_finish(speed: int, dist, hour: float) -> bool:
    """判断给定 speed 是否能在 hour 小时内到达"""
    total = 0.0
    # 前 n-1 趟火车需要向上取整
    for d in dist[:-1]:
        total += ceil(d / speed)
    # 最后一趟直接加实际时间
    total += dist[-1] / speed
    return total <= hour

def minSpeedOnTime(dist, hour):
    n = len(dist)
    # 如果 hour 小于 n-1（因为前 n-1 趟至少需要等到整数小时），必定 impossible
    if hour <= n - 1:
        return -1

    low, high = 1, 10**7
    ans = -1

    while low <= high:
        mid = (low + high) // 2
        if can_finish(mid, dist, hour):
            ans = mid          # mid 可行，尝试更小的速度
            high = mid - 1
        else:
            low = mid + 1      # mid 不行，需要更快的速度

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * log M)`，其中 `M = 10⁷` 为速度上界。每次二分检查一次 `can_finish`，其内部遍历 `n` 条路程，二分最多进行 `log₂(10⁷) ≈ 24` 次迭代。  
  > 与暴力的 `O(10⁷ * n)` 相比，时间从“千万级乘以 `n`”降到了“约二十几次乘以 `n`”，快了几个数量级。  
- **空间复杂度**：`O(1)` —— 只用了几个整数/浮点数变量。

---

## 心得

- **核心技巧**：**单调性 + 二分搜索**。当问题的“可行性随某个参数单调变化”时，二分可以把线性枚举的时间压到对数级。  
- **适用的题型**  
  1. **最小/最大满足条件的数**（如 “寻找最小体积的盒子装下所有物品”、 “寻找最大子数组和不超过阈值”）。  
  2. **带有取整/向上取整的时间/成本计算**（如 “在限定时间内完成所有任务的最小速度”）。  
  3. **单调函数的逆向求值**（如 “寻找最小的容量使得可以在 K 天内运输完所有货物”）。
- **一句话总结**：**把“是否能准时”抽象成单调的布尔函数，然后用二分定位最小满足条件的整数**。

---

## 反思

- **第一反应**：看到“最小正整数速度”，立刻想到**枚举**所有速度——这是一种最自然的暴力思路。  
- **最容易踩的坑**  
  - **边界条件**：如果 `hour` 小于 `n-1`（因为前 `n-1` 趟至少需要整数小时才能上车），直接返回 `-1`，否则二分会永远找不到解。  
  - **浮点数误差**：`dist[-1] / speed` 产生小数，比较时直接用 `<= hour` 就可以，因为题目保证 `hour` 只保留两位小数，误差不会影响判断。  
  - **向上取整的实现**：不要用 `int(x)`（会向下取整），必须用 `math.ceil` 或等价的 `(x + speed - 1) // speed`（整数除法）来实现。  
- **下次类似题的第一步**：先判断**是否存在单调性**（比如速度越大，总耗时越小），然后**确定搜索区间**，再决定是否可以使用二分搜索。这样可以立刻把暴力的指数级搜索降到对数级。