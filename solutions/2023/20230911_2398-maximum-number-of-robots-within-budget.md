# #2398. 预算内可运行的机器人最大数量 / Maximum Number of Robots Within Budget

> 难度：困难 · 标签：Array、Binary Search、Queue、Sliding Window、Heap (Priority Queue)、Prefix Sum、Monotonic Queue · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-robots-within-budget/)

---

## 题目（英文原版）

**Description**

You have n robots. You are given two 0-indexed integer arrays, chargeTimes and runningCosts, both of length n. The ith robot costs chargeTimes[i] units to charge and costs runningCosts[i] units to run. You are also given an integer budget.
The total cost of running k chosen robots is equal to max(chargeTimes) + k * sum(runningCosts), where max(chargeTimes) is the largest charge cost among the k robots and sum(runningCosts) is the sum of running costs among the k robots.
Return the maximum number of consecutive robots you can run such that the total cost does not exceed budget.

**Examples**

**Example 1:**

```
Input: chargeTimes = [3,6,1,3,4], runningCosts = [2,1,3,4,5], budget = 25
Output: 3
Explanation: 
It is possible to run all individual and consecutive pairs of robots within budget.
To obtain answer 3, consider the first 3 robots. The total cost will be max(3,6,1) + 3 * sum(2,1,3) = 6 + 3 * 6 = 24 which is less than 25.
It can be shown that it is not possible to run more than 3 consecutive robots within budget, so we return 3.
```

**Example 2:**

```
Input: chargeTimes = [11,12,19], runningCosts = [10,8,7], budget = 19
Output: 0
Explanation: No robot can be run that does not exceed the budget, so we return 0.
```

**Constraints**

- chargeTimes.length == runningCosts.length == n
- 1 <= n <= 5 * 104
- 1 <= chargeTimes[i], runningCosts[i] <= 105
- 1 <= budget <= 1015

---

## 题目（中文翻译）

你有 `n` 台机器人。给定两个 **0 索引** 整数数组 `chargeTimes` 和 `runningCosts`（均长度为 `n`），第 `i` 台机器人的充电费用为 `chargeTimes[i]` 单位，运行费用为 `runningCosts[i]` 单位。另给定一个整数 `budget`（预算）。

选取 `k` 台连续机器人的总费用计算公式为  

```
max(chargeTimes) + k * sum(runningCosts)
```

其中 `max(chargeTimes)` 为这 `k` 台机器人中最大的充电费用，`sum(runningCosts)` 为这 `k` 台机器人运行费用的总和。

返回在总费用不超过 `budget` 的前提下，你能够运行的 **连续机器人**（consecutive robots） 的最大数量。

---

### 示例

**示例 1**

```
Input: chargeTimes = [3,6,1,3,4], runningCosts = [2,1,3,4,5], budget = 25
Output: 3
Explanation: 
可以在预算内运行所有单个机器人以及所有相邻的两台机器人。
为了得到答案 3，考虑前 3 台机器人。总费用为 
max(3,6,1) + 3 * sum(2,1,3) = 6 + 3 * 6 = 24， 小于 25。
可以证明，无法运行超过 3 台连续机器人。
```

**示例 2**

```
Input: chargeTimes = [11,12,19], runningCosts = [10,8,7], budget = 19
Output: 0
Explanation: 没有任何一台机器人在预算内可运行，因此返回 0。
```

---

### 约束条件

- `chargeTimes.length == runningCosts.length == n`
- `1 <= n <= 5 * 10^4`
- `1 <= chargeTimes[i], runningCosts[i] <= 10^5`
- `1 <= budget <= 10^15`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：把所有 **连续** 的机器人子数组枚举出来，逐个算出它们的费用  

\[
\text{cost}= \max(\text{chargeTimes}) + k \times \sum(\text{runningCosts})
\]

只要 `cost ≤ budget`，就记录下这个子数组的长度 `k`，最后取最大的 `k`。  

- **数据结构**：  
  - `max(chargeTimes)` 可以直接在遍历子数组时用一个变量保存最大值，类似“把所有机器人收费写在一本字典里，找最大的那个词”。  
  - `sum(runningCosts)` 同理，用一个累计变量记录子数组的运行费用总和。  

- **正确性**：  
  枚举了**所有**可能的连续区间，逐个检查它们是否满足预算限制，必然不会错过最优答案。

- **复杂度**：  
  - 外层遍历 `i`（子数组左端点），内层遍历 `j`（右端点），每次都更新最大值和累计和。  
  - 时间复杂度是 **O(n²)**，因为最坏情况下会检查 `n·(n+1)/2 ≈ n²/2` 个区间。  
  - 空间复杂度只有几个临时变量，**O(1)**。  
  - 大白话解释：如果 `n = 10⁴`，`n²` 就是 1 亿次运算，Python 在 1 秒左右难以跑完，故不可接受。

#### 代码（Python）

```python
def maxRobots_bruteforce(chargeTimes, runningCosts, budget):
    n = len(chargeTimes)
    ans = 0                         # 记录最大可行长度
    for left in range(n):           # 枚举左端点
        cur_max = 0                 # 当前子数组的 max(chargeTimes)
        cur_sum = 0                 # 当前子数组的 sum(runningCosts)
        for right in range(left, n):    # 枚举右端点
            cur_max = max(cur_max, chargeTimes[right])   # 更新最大充电费用
            cur_sum += runningCosts[right]               # 更新运行费用总和
            k = right - left + 1                         # 子数组长度
            cost = cur_max + k * cur_sum                 # 计算总费用
            if cost <= budget:                           # 预算够用
                ans = max(ans, k)                         # 更新答案
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：两层循环，外层 `n` 次，内层最多 `n` 次，总共约 `n²/2` 次比较和加法。

- **空间复杂度**：`O(1)`  
  只用了常数个整型变量，没有额外的数组或容器。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历整个子数组来找最大充电费用**，这导致二次方的时间。  
我们可以把“找最大值”这一步改成 **O(1)**，只要在滑动窗口里维护一个**单调队列（deque）**，它始终把窗口内的 `chargeTimes` 按从大到小的顺序保存，队首就是窗口的最大值。  

此外，`k * sum(runningCosts)` 里的 `sum(runningCosts)` 可以用**前缀和**在 O(1) 时间得到，或者在滑动窗口里用一个累加变量实时维护。

但是即使把这两件事都做到 O(1)，仍然需要 **遍历所有窗口**，这仍是 O(n²)。  
关键是：我们并不需要检查**所有长度**，只要判断“**是否存在长度为 L 的窗口**满足预算”，就可以用二分搜索找出最大可行的 `L`。

**整体框架**

1. **二分搜索**长度 `L`（`1 … n`）。  
   - 中间值 `mid` 代表“我们尝试找是否存在长度为 `mid` 的连续机器人”。  
   - 如果能找到，说明答案至少是 `mid`，继续在更大的区间搜索；否则在更小的区间搜索。

2. **判定函数 `can(L)`**：在 O(n) 时间内判断是否存在长度为 `L` 的窗口满足预算。  
   - 使用单调队列维护当前窗口的最大 `chargeTimes`。  
   - 同时维护窗口内 `runningCosts` 的累计和 `window_sum`（滑动窗口的加减即可）。  
   - 对每个右端点 `right`，窗口左端点 `left = right - L + 1`。  
   - 计算 `cost = max_charge + L * window_sum`，若 `cost ≤ budget`，返回 `True`。  
   - 若遍历完所有窗口仍未找到，返回 `False`。

**为什么单调队列可以 O(1) 取最大？**  
想象你在排队买咖啡，队列里的人按“付费金额从大到小”站好。当有新人加入（右端点右移）时，所有比他小的人都会被他“挡在后面”，于是我们把这些更小的元素全部弹出，只留下比他大的，保证队首永远是窗口内最大的。左端点左移时，如果队首恰好是要离开的元素，就把它弹出。这样每个元素最多进出队列一次，整体是线性时间。

**复杂度对比**  
- 暴力：`O(n²)`  
- 最优：二分 `log n` 次 * 每次 O(n) 检查 = **O(n log n)** 时间，额外的单调队列占用 **O(n)** 空间（最坏情况下队列里会存所有元素）。

#### 代码（Python）

```python
from collections import deque

def maxRobots(chargeTimes, runningCosts, budget):
    """
    返回预算内可以连续运行的机器人最大数量
    """
    n = len(chargeTimes)

    # ---------- 判定函数 ----------
    def can(k):
        """
        判断是否存在长度为 k 的连续子数组，使得
        max(chargeTimes) + k * sum(runningCosts) <= budget
        """
        if k == 0:
            return True

        maxDeque = deque()          # 单调递减队列，存下标，队首是窗口最大值的下标
        window_sum = 0              # 当前窗口的 runningCosts 总和

        for right in range(n):
            # 1) 加入新元素 right
            #   - 维护单调队列
            while maxDeque and chargeTimes[maxDeque[-1]] <= chargeTimes[right]:
                maxDeque.pop()      # 弹出比新元素小的，下标更早的元素已经不可能是最大
            maxDeque.append(right)

            #   - 累加运行费用
            window_sum += runningCosts[right]

            # 2) 当窗口大小超过 k 时，收缩左端
            if right >= k:
                left = right - k
                # 移除即将离开的左端元素
                if maxDeque[0] == left:
                    maxDeque.popleft()
                window_sum -= runningCosts[left]

            # 3) 当窗口恰好大小为 k，检查预算
            if right >= k - 1:       # 窗口已满
                max_charge = chargeTimes[maxDeque[0]]   # 队首即为最大值
                cost = max_charge + k * window_sum
                if cost <= budget:
                    return True
        return False

    # ---------- 二分搜索 ----------
    lo, hi = 0, n          # 可能的答案范围是 [0, n]
    while lo < hi:
        mid = (lo + hi + 1) // 2   # 取上中位，防止死循环
        if can(mid):
            lo = mid               # mid 可行，向右找更大
        else:
            hi = mid - 1           # mid 不可行，向左收敛
    return lo
```

> **代码要点解释**  
> 1. `maxDeque` 只保存**下标**，因为我们需要在左端收缩时判断是否要弹出队首。  
> 2. `while maxDeque and chargeTimes[maxDeque[-1]] <= chargeTimes[right]`：把比新元素小的全部弹出，保持 **递减**。  
> 3. `if right >= k:` 这段把窗口大小始终维持在 `k`，左端元素离开时同步从队列和 `window_sum` 中删掉。  
> 4. 二分搜索使用上取整 `(lo + hi + 1)//2`，确保在 `lo == hi-1` 时仍能前进，防止无限循环。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 二分搜索最多进行 `log₂ n` 次（约 16 次，当 `n = 5·10⁴` 时）。  
  - 每次调用 `can(k)` 只遍历一次数组，单调队列的每个元素最多进出一次，整体是 `O(n)`。  
  - 与暴力解 `O(n²)` 相比，时间缩短了一个数量级，能轻松通过 5·10⁴ 规模的测试。

- **空间复杂度**：`O(n)`（最坏情况下单调队列会保存所有下标）  
  - 实际上平均只会保存窗口内的极少数元素，常数空间也可以接受。

---

## 心得

- **核心技巧**：  
  1. **单调队列**（Monotonic Queue）实现滑动窗口最大值的 O(1) 取值。  
  2. **二分搜索**把“求最大可行长度”转化为“判断长度是否可行”。  

- **适用的题型**（可用相同思路）：  
  - “最长子数组满足 `max(nums) - min(nums) ≤ limit`”（LeetCode 1438）。  
  - “最大子数组长度使得平均值 ≤ K” 或 “子数组和 ≤ S”。  
  - “滑动窗口内最大值/最小值” 相关的所有题目。

- **一句话总结**：  
  *把“找最大”交给单调队列，把“找最优长度”交给二分搜索，二者合力把暴力的 O(n²) 降到 O(n log n)。*

---

## 反思

- **第一反应**：看到 “max + k * sum” 直接想到枚举所有子数组，随后发现时间爆炸。  
- **最容易踩的坑**：  
  - **窗口左端的元素离开时忘记从单调队列弹出**，导致队首不是当前窗口的最大值。  
  - **整数溢出**（在某些语言），因为 `k * sum` 可能达到 `10⁵ * 10⁵ * 5·10⁴ ≈ 5·10¹⁴`，必须使用 64 位整数（Python 天然支持）。  
  - **二分搜索边界**写错，尤其是取中位数时应使用上取整，否则会出现死循环。  

- **下次遇到类似题**，第一步应该先思考：  
  - “我需要快速获取窗口内的极值吗？” → 考虑单调队列/堆。  
  - “我要找最大/最小满足条件的长度？” → 考虑二分搜索 + 判定函数。  

这样可以快速从暴力思路切换到高效实现。