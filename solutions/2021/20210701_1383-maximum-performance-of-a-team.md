# #1383. 团队的最大绩效 / Maximum Performance of a Team

> 难度：困难 · 标签：Array、Greedy、Sorting、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-performance-of-a-team/)

---

## 题目（英文原版）

**Description**

You are given two integers n and k and two integer arrays speed and efficiency both of length n. There are n engineers numbered from 1 to n. speed[i] and efficiency[i] represent the speed and efficiency of the ith engineer respectively.
Choose at most k different engineers out of the n engineers to form a team with the maximum performance.
The performance of a team is the sum of its engineers' speeds multiplied by the minimum efficiency among its engineers.
Return the maximum performance of this team. Since the answer can be a huge number, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 2
Output: 60
Explanation: 
We have the maximum performance of the team by selecting engineer 2 (with speed=10 and efficiency=4) and engineer 5 (with speed=5 and efficiency=7). That is, performance = (10 + 5) * min(4, 7) = 60.
```

**Example 2:**

```
Input: n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 3
Output: 68
Explanation:
This is the same example as the first but k = 3. We can select engineer 1, engineer 2 and engineer 5 to get the maximum performance of the team. That is, performance = (2 + 10 + 5) * min(5, 4, 7) = 68.
```

**Example 3:**

```
Input: n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 4
Output: 72
```

**Constraints**

- 1 <= k <= n <= 105
- speed.length == n
- efficiency.length == n
- 1 <= speed[i] <= 105
- 1 <= efficiency[i] <= 108

---

## 题目（中文翻译）

给定两个整数 `n` 和 `k`，以及两个长度均为 `n` 的整数数组 `speed` 和 `efficiency`。共有 `n` 位工程师（engineer），编号从 `1` 到 `n`。`speed[i]` 与 `efficiency[i]` 分别表示第 `i` 位工程师的速度（speed）和效率（efficiency）。

从这 `n` 位工程师中挑选至多 `k` 位不同的工程师，组成一个团队，使该团队的绩效（performance）最大。团队的绩效定义为：**团队中所有工程师的速度之和** 乘以 **团队中工程师的最小效率**。

返回该团队能够达到的最大绩效。由于答案可能非常大，请返回其对 `10^9 + 7` 取模后的结果。

**示例 1**  
**输入**: `n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 2`  
**输出**: `60`  
**解释**:  
我们通过选择工程师 2（`speed=10, efficiency=4`）和工程师 5（`speed=5, efficiency=7`）得到最大绩效。  
绩效 = `(10 + 5) * min(4, 7) = 60`.

**示例 2**  
**输入**: `n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 3`  
**输出**: `68`  
**解释**:  
同上例，只是 `k = 3`。我们可以选择工程师 1、工程师 2 和工程师 5，得到最大绩效。  
绩效 = `(2 + 10 + 5) * min(5, 4, 7) = 68`.

**示例 3**  
**输入**: `n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 4`  
**输出**: `72`

**约束条件**  
- `1 <= k <= n <= 10^5`  
- `speed.length == n`  
- `efficiency.length == n`  
- `1 <= speed[i] <= 10^5`  
- `1 <= efficiency[i] <= 10^8`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的团队组合**，然后计算每个组合的表现值，取最大值。

- **枚举方式**：把 `n` 名工程师的下标放进一个列表，使用 `itertools.combinations`（或自己写循环）枚举出所有长度为 `1,2,…,k` 的子集。  
- **计算表现**：对每个子集，先把子集里所有工程师的 `speed` 加起来得到 `sum_speed`，再找出子集里 `efficiency` 的最小值 `min_eff`，最后 `performance = sum_speed * min_eff`。  
- **取最大**：遍历完所有子集后，记录出现过的最大 `performance` 即为答案。

> **类比**：想象你在挑选队员参加比赛，你把所有可能的挑选方式（比如挑 2 个人、挑 3 个人…）都列在纸上，逐个算出每种挑选方式的得分，最后选最高分的那种。这就是暴力枚举的思路。

> **为什么正确**：因为我们把**所有合法的组合**都算了一遍，答案一定在其中，所以必然能得到最优解。

#### 代码（Python）

```python
from itertools import combinations
from math import inf

def maxPerformance_bruteforce(n, speed, efficiency, k):
    MOD = 10**9 + 7
    ans = 0

    # 把每个工程师的信息打包成 (speed, efficiency) 的元组，方便取值
    engineers = list(zip(speed, efficiency))

    # 枚举团队大小 1~k
    for team_size in range(1, k + 1):
        # 组合出所有可能的 team_size 名工程师的下标集合
        for idxs in combinations(range(n), team_size):
            sum_speed = 0          # 速度之和
            min_eff = inf          # 效率的最小值，初始设为无限大
            for i in idxs:
                s, e = engineers[i]
                sum_speed += s
                if e < min_eff:
                    min_eff = e
            # 计算表现值
            performance = sum_speed * min_eff
            if performance > ans:
                ans = performance

    return ans % MOD
```

> 代码里每一行都有中文注释，帮助你快速定位每一步的作用。

#### 复杂度  

- **时间复杂度**：  
  枚举所有子集的复杂度是  
  \[
  \sum_{t=1}^{k} \binom{n}{t}
  \]  
  这在最坏情况下（比如 `k = n = 20`）已经是 **指数级** 的，记作 **O(2ⁿ)**。直观上可以理解为“随工程师人数的增加，组合数会爆炸”。  
- **空间复杂度**：  
  只用了常数级的额外空间（`O(1)`），因为我们没有存储所有子集，只是逐个生成并计算。

> 对于题目给出的 `n ≤ 10⁵`，暴力解根本不可行，只能用来帮助我们**理清问题**，随后寻找更快的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**“最小效率”** 是决定表现值的关键因素。  
如果我们已经确定了团队里 **效率的最小值** 为 `e_min`，那么表现值就等于 `e_min * (速度之和)`。  
于是，**我们可以把注意力放在“效率的最小值”上来逐步构造团队**。

**核心观察**：

1. **把工程师按效率从高到低排序**。  
   - 设当前遍历到的工程师的效率为 `cur_eff`，因为后面的工程师效率更低，若把它们加入团队，`min_eff` 一定会变成更小的值。  
   - 因此，当我们把某位工程师作为「最小效率」时，团队里只能选 **效率不低于它的工程师**（即排在它前面的工程师）。

2. **在已遍历的（效率更高）工程师中挑选速度最大的 `k-1` 名**（加上当前工程师共 `k` 名）。  
   - 因为 `cur_eff` 已经固定，想让 `speed_sum` 最大，只能挑速度大的工程师。  
   - 这一步需要一种**动态维护**「当前已选工程师的速度集合」的结构，能够快速插入新速度并在集合大小超过 `k` 时删除最小的速度（因为最小的速度对 `speed_sum` 的贡献最小）。

3. **使用最小堆（优先队列）维护速度**。  
   - 堆顶保存的是当前集合中 **最小的速度**。  
   - 当堆的大小超过 `k` 时，弹出堆顶，即丢掉速度最小的工程师，以保证集合里始终是速度最大的 `k` 名（或更少）。

**步骤**：

| 步骤 | 说明 |
|------|------|
| 1️⃣ | 把每个工程师的 `(efficiency, speed)` 打包，按 `efficiency` 降序排序。 |
| 2️⃣ |遍历排序后的列表，依次把当前工程师当作「最小效率」`cur_eff`。 |
| 3️⃣ | 把当前工程师的 `speed` 加入最小堆 `speed_heap`，并累计到 `speed_sum`。 |
| 4️⃣ | 若堆大小 > `k`，弹出堆顶（最小速度），并从 `speed_sum` 中减去该速度。 |
| 5️⃣ | 计算当前表现 `cur_perf = speed_sum * cur_eff`，更新全局最大 `ans`。 |
| 6️⃣ |遍历结束后，返回 `ans % MOD`。 |

> **类比**：把效率高的工程师排成一条队，先让效率最高的站在前面。我们从前往后依次挑选「最小效率」的人，然后在已经站好的人中挑出速度最快的 `k-1` 人一起组队。堆就像一个「小淘气」的保安，只负责把速度最慢的那几个人踢出去，保证队伍里永远留下速度最快的成员。

#### 代码（Python）

```python
import heapq

def maxPerformance(n, speed, efficiency, k):
    MOD = 10**9 + 7

    # 1️⃣ 把 (efficiency, speed) 打包并按效率降序排列
    engineers = list(zip(efficiency, speed))          # (eff, spd)
    engineers.sort(reverse=True)                      # 效率大的排前面

    speed_heap = []          # 最小堆，保存当前团队的速度
    speed_sum = 0            # 当前团队速度之和
    ans = 0

    # 2️⃣ 遍历每位工程师，视其为最小效率
    for cur_eff, cur_spd in engineers:
        # 3️⃣ 把当前速度加入堆和累计和
        heapq.heappush(speed_heap, cur_spd)   # 小根堆，堆顶是最小速度
        speed_sum += cur_spd

        # 4️⃣ 若超过 k 人，弹出速度最小的那位
        if len(speed_heap) > k:
            removed_spd = heapq.heappop(speed_heap)
            speed_sum -= removed_spd

        # 5️⃣ 计算以当前效率为最小效率的团队表现
        cur_perf = speed_sum * cur_eff
        if cur_perf > ans:
            ans = cur_perf

    # 6️⃣ 取模返回
    return ans % MOD
```

> - `heapq.heappush` / `heapq.heappop` 均为 **O(log k)** 的操作。  
> - 代码中的每一行都配有中文注释，帮助你一步步跟上思路。

#### 复杂度  

- **时间复杂度**：  
  - 排序需要 `O(n log n)`。  
  - 遍历 `n` 位工程师，每次堆的插入/弹出是 `O(log k)`（因为堆的大小始终 ≤ `k`）。  
  - 综合起来是 **O(n log n + n log k)**，在最坏情况下 `k ≤ n`，可以简化为 **O(n log n)**。  
  - 与暴力解的指数级时间相比，**快了几个数量级**，能够轻松处理 `n = 10⁵` 的数据。

- **空间复杂度**：  
  - 需要存储排序后的工程师列表 `O(n)`，以及大小最多为 `k` 的堆 `O(k)`。  
  - 因此总体是 **O(n + k)**，在本题中等价于 **O(n)**。

> 与暴力解相比，时间从不可接受的指数级降到了对数级别的线性，空间也保持在合理范围。

---

## 心得

- **核心技巧**：**先按效率降序遍历 + 用最小堆维护速度的前 k 大**。  
- **适用的题型**（类似思路）  
  1. “**Maximum Score from Performing Multiplication Operations**”（LeetCode 1770）——利用排序 + 堆/双指针选取最优子集。  
  2. “**Find the K Highest Sum Pairs**”——用堆维护最大/最小元素。  
  3. “**Maximum Sum of 3 Non‑Overlapping Subarrays**”——先算前缀和，再用单调队列/堆挑最优区间。  
- **一句话总结解题钥匙**：  
  > 把“最小值”固定住（这里是最小效率），剩下的只需要挑“最大值”（速度），用堆快速维护最大子集。

---

## 反思

- **第一反应**：看到“最小效率 × 速度之和”，立刻想到**先固定最小效率**，再让速度尽可能大。  
- **最容易踩的坑**  
  1. **忘记对效率降序**，导致后面加入的成员把 `min_eff` 变得更小，结果不正确。  
  2. **堆的大小控制不当**：如果忘记在堆超过 `k` 时弹出最小速度，会导致团队成员数超过限制，导致错误的 `performance`。  
  3. **取模时忘记在最终答案上取**，而不是每一步都取模，否则会出现负数或溢出。  
- **下次遇到同类题**：  
  - 第一步：**找出限制因素（最小/最大）**，并决定遍历的顺序（升序或降序）。  
  - 第二步：**使用合适的数据结构（堆、单调队列、前缀和等）**，在遍历过程中动态维护“最佳的可选集合”。  

祝你在算法的道路上越走越顺！ 🚀