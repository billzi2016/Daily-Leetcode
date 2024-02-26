# #2594. 维修汽车的最短时间 / Minimum Time to Repair Cars

> 难度：中等 · 标签：Array、Binary Search · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-repair-cars/)

---

## 题目（英文原版）

**Description**

You are given an integer array ranks representing the ranks of some mechanics. ranksi is the rank of the ith mechanic. A mechanic with a rank r can repair n cars in r * n2 minutes.
You are also given an integer cars representing the total number of cars waiting in the garage to be repaired.
Return the minimum time taken to repair all the cars.
Note: All the mechanics can repair the cars simultaneously.

**Examples**

**Example 1:**

```
Input: ranks = [4,2,3,1], cars = 10
Output: 16
Explanation: 
- The first mechanic will repair two cars. The time required is 4 * 2 * 2 = 16 minutes.
- The second mechanic will repair two cars. The time required is 2 * 2 * 2 = 8 minutes.
- The third mechanic will repair two cars. The time required is 3 * 2 * 2 = 12 minutes.
- The fourth mechanic will repair four cars. The time required is 1 * 4 * 4 = 16 minutes.
It can be proved that the cars cannot be repaired in less than 16 minutes.​​​​​
```

**Example 2:**

```
Input: ranks = [5,1,8], cars = 6
Output: 16
Explanation: 
- The first mechanic will repair one car. The time required is 5 * 1 * 1 = 5 minutes.
- The second mechanic will repair four cars. The time required is 1 * 4 * 4 = 16 minutes.
- The third mechanic will repair one car. The time required is 8 * 1 * 1 = 8 minutes.
It can be proved that the cars cannot be repaired in less than 16 minutes.​​​​​
```

**Constraints**

- 1 <= ranks.length <= 105
- 1 <= ranks[i] <= 100
- 1 <= cars <= 106

---

## 题目（中文翻译）

**题目描述**  
给定一个整数数组 `ranks`，其中 `ranks[i]` 表示第 `i` 位机械师的等级（rank）。等级为 `r` 的机械师可以在 `r * n²` 分钟内修好 `n` 辆汽车。  
另给定一个整数 `cars`，表示车库中等待维修的汽车总数。  
返回修完所有汽车所需的最短时间。  

> 注：所有机械师可以同时进行维修。

### 示例

**示例 1**  
```text
Input: ranks = [4,2,3,1], cars = 10
Output: 16
Explanation: 
- 第一个机械师修理两辆车，所需时间为 4 * 2 * 2 = 16 分钟。  
- 第二个机械师修理两辆车，所需时间为 2 * 2 * 2 = 8 分钟。  
- 第三个机械师修理两辆车，所需时间为 3 * 2 * 2 = 12 分钟。  
- 第四个机械师修理四辆车，所需时间为 1 * 4 * 4 = 16 分钟。  
（此处省略部分过程）  
```

**示例 2**  
```text
Input: ranks = [5,1,8], cars = 6
Output: 16
Explanation: 
- 第一个机械师修理一辆车，所需时间为 5 * 1 * 1 = 5 分钟。  
- 第二个机械师修理四辆车，所需时间为 1 * 4 * 4 = 16 分钟。  
- 第三个机械师修理一辆车，所需时间为 8 * 1 * 1 = 8 分钟。  
可以证明，无法在 16 分钟以内完成所有汽车的维修。  
```

### 约束条件
- `1 <= ranks.length <= 10⁵`
- `1 <= ranks[i] <= 100`
- `1 <= cars <= 10⁶`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**从时间 1 开始往后枚举**，每枚举一个时间 `t` 就算一下在这段时间里所有机械师能修多少辆车。  
- 对于某个机械师，已知他的等级 `r`，他在 `t` 分钟内最多能修 `n` 辆车，只要满足 `r * n² ≤ t`。  
- 所以我们可以把 `t` 从 1、2、3 … 逐个递增，**把每个机械师能修的车数相加**，只要累计的车数 ≥ `cars`，当前的 `t` 就是答案。

这相当于把“最小时间”这件事**线性搜索**出来。  

> **生活化类比**：想象有几位工人，每个人的工作效率不同。我们把时间想成“一格格的钟表滴答”，每过一格就看看大家这时能完成多少任务，直到任务全部完成。  

这个办法一定能得到正确答案，因为我们把所有可能的时间都检查了一遍，必然会找到最早能完成全部维修的那一刻。

#### 代码（Python）

```python
import math

def minTime_bruteforce(ranks, cars):
    t = 1                     # 从第 1 分钟开始尝试
    while True:
        total = 0
        # 统计在 t 分钟内所有机械师合计能修多少车
        for r in ranks:
            # r * n^2 <= t  =>  n <= sqrt(t / r)
            n = int(math.isqrt(t // r))   # isqrt 直接返回整数平方根
            total += n
        if total >= cars:      # 已经够修完
            return t
        t += 1                 # 时间往后推 1 分钟
```

> **代码要点**  
> - `math.isqrt` 取整平方根，等价于 `int(math.sqrt(...))` 但更安全、不会出现浮点误差。  
> - 循环里只用了最基本的加法和除法，逻辑非常直白，适合初学者阅读。

#### 复杂度  

- **时间复杂度**：`O(T * m)`  
  - `T` 为答案的大小（最小需要的分钟数），`m = len(ranks)` 为机械师数量。  
  - 直觉上可以把 `O(T)` 想成“我们必须检查的时间格子数”。如果答案是 10⁶，循环就要跑 10⁶ 次，显然太慢。  
- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量 `t、total、n`，不随输入规模增长。

> **大白话**：暴力解相当于“一秒一秒”地数，最坏情况下要等到答案出现才停下来，时间可能会非常大，根本不可接受。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到**瓶颈**在于我们把时间一个单位一个单位地枚举。实际上，答案是 **单调递增** 的：  
- 给定一个时间 `t`，如果在 `t` 分钟能修完所有车，那么在更大的时间 `t' > t` 肯定也能修完。  
- 这正好满足**二分查找**（binary search）可以使用的前提：**单调性**。

所以我们把“在固定时间 `t` 能否修完”这个子问题抽象成一个**判定函数** `canFinish(t)`，再在一个合理的时间区间上二分搜索最小的满足条件的 `t`。

**如何实现 `canFinish(t)`**  
- 对于每个机械师等级 `r`，求最大整数 `n` 使得 `r * n² ≤ t`。  
- 这等价于 `n ≤ sqrt(t / r)`，于是 `n = floor(sqrt(t / r))`。  
- 把所有机械师的 `n` 加起来，若总和 ≥ `cars`，说明在 `t` 分钟内可以完成。

**二分搜索的上下界**  
- **左边界** `lo = 1`（最少也要 1 分钟）。  
- **右边界** `hi` 需要足够大，确保一定能修完所有车。最坏情况下只有 **最慢的机械师**（最大 `r`）单独工作，修完 `cars` 辆车需要的时间是 `r_max * cars²`（因为 `n = cars` 时 `r * cars²`）。所以 `hi = max(ranks) * cars * cars`。  
  - 这个上界虽然很大，但二分查找只需要 `log₂(hi)` 次迭代，约 60 次（因为 `hi ≤ 100 * 10⁶²` 仍在 64 位整数范围内），足够快。

**整体流程**  

1. 设 `lo = 1`，`hi = max(ranks) * cars * cars`。  
2. 当 `lo < hi` 时：  
   - `mid = (lo + hi) // 2`。  
   - 若 `canFinish(mid)` 为真 → 把右边界收缩到 `mid`（因为我们在找最小可行时间）。  
   - 否则 → 把左边界拉到 `mid + 1`。  
3. 循环结束时 `lo`（或 `hi`）就是答案。

> **类比**：把时间想成一本厚厚的书，答案所在的页码一定在某个区间。我们先把区间缩小到“最左”和“最右”，每次检查中间页，如果中间页已经能满足条件，就把右边界移到这里；否则左边界往右移。这样不断“折半”，很快就能定位到答案所在的那一页。

#### 代码（Python）

```python
import math
from typing import List

def minTime(ranks: List[int], cars: int) -> int:
    """
    二分搜索答案，时间复杂度 O(m log(max_rank * cars^2))
    """
    # ---------- 判定函数 ----------
    def can_finish(t: int) -> bool:
        """在 t 分钟内，所有机械师合计能修的车数是否 >= cars"""
        total = 0
        for r in ranks:
            # r * n^2 <= t  =>  n <= sqrt(t / r)
            n = int(math.isqrt(t // r))   # 直接得到整数平方根
            total += n
            if total >= cars:             # 提前返回，省掉不必要的循环
                return True
        return False

    # ---------- 二分搜索 ----------
    lo = 1
    hi = max(ranks) * cars * cars   # 必然可行的上界

    while lo < hi:
        mid = (lo + hi) // 2
        if can_finish(mid):
            hi = mid                 # 还能往左找更小的时间
        else:
            lo = mid + 1             # 需要更大的时间

    return lo                       # lo == hi，即最小可行时间
```

> **代码要点**  
> - `math.isqrt` 保证了全整数运算，避免浮点数精度问题。  
> - `can_finish` 在累计的车数已经达到需求时就提前 `return True`，可以显著降低常数时间。  
> - 整个函数只用了 `ranks`、`cars` 之外的常数级变量，空间开销极小。

#### 复杂度  

- **时间复杂度**：`O(m · log(max_rank·cars²))`  
  - `m = len(ranks)`（最多 10⁵），`log` 部分大约在 60 左右（因为 `max_rank·cars² ≤ 100·10¹²`），所以即使 `m` 很大也能在毫秒级完成。  
  - 与暴力解的 `O(T·m)` 相比，二分把线性的 `T`（可能是上亿）压缩成了对数级别的迭代次数，速度提升几个数量级。  

- **空间复杂度**：`O(1)`  
  - 只使用了常数个整数变量 `lo、hi、mid、total、n`，不随输入规模增长。

> **对比**：暴力解像是“一格格爬坡”，最优解像是“用望远镜先看到山顶的大致高度，再快速定位最短路径”。  

---

## 心得  

- **核心技巧**：**单调性 + 二分查找**（Binary Search on Answer）。  
- 该技巧适用于**所有需要在数值范围内寻找最小（或最大）满足条件的值**的题目，例如  
  1. **分配饼干/糖果**——在限定时间内能否完成所有任务（LeetCode 1482 `Minimum Number of Days to Make m Bouquets`）。  
  2. **划分数组**——最小化最大子数组和（LeetCode 410 `Split Array Largest Sum`）。  
- **一句话总结解题钥匙**：*把“能否在 T 时间内完成”抽象成一个单调判定函数，然后在可能的时间区间上二分搜索最小可行的 T*。

---

## 反思  

- **第一反应**：看到“机械师的维修时间是 r·n²”，立刻想到**平方根**，于是想到“在固定时间内能修多少车”。  
- **最容易踩的坑**  
  - **整数溢出**：直接使用 `r * n * n` 可能超过 32 位整数范围，Python 没问题，但在其他语言要用 64 位。  
  - **边界条件**：`t // r` 可能为 0，`isqrt(0)` 正确返回 0，别忘了处理这种情况。  
  - **上界选取**：如果上界取得太小（比如 `max(ranks) * cars`），二分会提前结束导致错误。必须使用 `max(ranks) * cars²` 才能保证一定可行。  
- **下次遇到同类题**：第一步先**检查是否存在单调性**（答案随某个变量增大而不减），再**构造判定函数**，最后**二分搜索**。  

祝你在算法的道路上越走越稳 🚀