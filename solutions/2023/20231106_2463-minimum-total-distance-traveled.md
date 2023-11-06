# #2463. 最小总行驶距离 / Minimum Total Distance Traveled

> 难度：困难 · 标签：Array、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-total-distance-traveled/)

---

## 题目（英文原版）

**Description**

There are some robots and factories on the X-axis. You are given an integer array robot where robot[i] is the position of the ith robot. You are also given a 2D integer array factory where factory[j] = [positionj, limitj] indicates that positionj is the position of the jth factory and that the jth factory can repair at most limitj robots.
The positions of each robot are unique. The positions of each factory are also unique. Note that a robot can be in the same position as a factory initially.
All the robots are initially broken; they keep moving in one direction. The direction could be the negative or the positive direction of the X-axis. When a robot reaches a factory that did not reach its limit, the factory repairs the robot, and it stops moving.
At any moment, you can set the initial direction of moving for some robot. Your target is to minimize the total distance traveled by all the robots.
Return the minimum total distance traveled by all the robots. The test cases are generated such that all the robots can be repaired.
Note that

**Examples**

**Example 1:**

```
Input: robot = [0,4,6], factory = [[2,2],[6,2]]
Output: 4
Explanation: As shown in the figure:
- The first robot at position 0 moves in the positive direction. It will be repaired at the first factory.
- The second robot at position 4 moves in the negative direction. It will be repaired at the first factory.
- The third robot at position 6 will be repaired at the second factory. It does not need to move.
The limit of the first factory is 2, and it fixed 2 robots.
The limit of the second factory is 2, and it fixed 1 robot.
The total distance is |2 - 0| + |2 - 4| + |6 - 6| = 4. It can be shown that we cannot achieve a better total distance than 4.
```

**Example 2:**

```
Input: robot = [1,-1], factory = [[-2,1],[2,1]]
Output: 2
Explanation: As shown in the figure:
- The first robot at position 1 moves in the positive direction. It will be repaired at the second factory.
- The second robot at position -1 moves in the negative direction. It will be repaired at the first factory.
The limit of the first factory is 1, and it fixed 1 robot.
The limit of the second factory is 1, and it fixed 1 robot.
The total distance is |2 - 1| + |(-2) - (-1)| = 2. It can be shown that we cannot achieve a better total distance than 2.
```

**Constraints**

- 1 <= robot.length, factory.length <= 100
- factory[j].length == 2
- -109 <= robot[i], positionj <= 109
- 0 <= limitj <= robot.length
- The input will be generated such that it is always possible to repair every robot.

---

## 题目（中文翻译）

**描述**  
在 X 轴上有若干机器人（robot）和工厂（factory）。给定整数数组 `robot`，其中 `robot[i]` 表示第 `i` 台机器人的位置。还给定一个二维整数数组 `factory`，其中 `factory[j] = [position_j, limit_j]` 表示第 `j` 家工厂的位置为 `position_j`，且该工厂最多只能维修 `limit_j` 台机器人。

每台机器人的位置互不相同，每家工厂的位置也互不相同。注意，机器人最初可以与工厂位于同一位置。  

所有机器人最初都是损坏的，它们会沿着 X 轴的某个方向持续移动，该方向可以是负方向也可以是正方向。当机器人到达尚未达到维修上限的工厂时，工厂会对其进行维修，机器人随即停止移动。

在任意时刻，你可以为某些机器人设定其初始移动方向。你的目标是使所有机器人行驶的总距离最小化。

返回所有机器人行驶的最小总距离。题目保证所有机器人都能够被维修。

**示例 1**  
```text
Input: robot = [0,4,6], factory = [[2,2],[6,2]]
Output: 4
Explanation: 如图所示：
- 位置为 0 的机器人向正方向移动，会在第一家工厂维修。
- 位置为 4 的机器人向负方向移动，会在第一家工厂维修。
- 位置为 6 的机器人会在第二家工厂维修，无需移动。
```

**示例 2**  
```text
Input: robot = [1,-1], factory = [[-2,1],[2,1]]
Output: 2
Explanation: 如图所示：
- 位置为 1 的机器人向正方向移动，会在第二家工厂维修。
- 位置为 -1 的机器人向负方向移动，会在第一家工厂维修。
第一家工厂的上限为 1，正好维修了 1 台机器人；第二家工厂同理。
```

**约束条件**  
- `1 <= robot.length, factory.length <= 100`
- `factory[j].length == 2`
- `-10^9 <= robot[i], position_j <= 10^9`
- `0 <= limit_j <= robot.length`
- 输入数据保证一定可以维修所有机器人。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是 **把每个机器人随意配到一个有剩余容量的工厂**，然后把所有配对的距离相加，取最小值。  
这相当于把题目看成：

* 有 `n` 台机器人，需要把它们全部放进 `m` 台工厂的“口袋”里。  
* 每个口袋（工厂）有容量 `limit[j]`，装进去的机器人数不能超过它。  
* 放进去的代价是机器人位置到工厂位置的距离 `|robot[i] - position[j]|`。  

我们可以用递归（或回溯）枚举所有合法的配对方式：

```
dfs(i, remaining_limits):
    # i 表示当前要安排的机器人下标
    # remaining_limits[j] 表示第 j 个工厂还能接收的机器人数
    if i == n:   # 所有机器人都安排好了
        return 0
    ans = +∞
    for each factory j where remaining_limits[j] > 0:
        cost = |robot[i] - position[j]| + dfs(i+1, remaining_limits with j-1)
        ans = min(ans, cost)
    return ans
```

- **用到的数据结构**：  
  - `remaining_limits` 类似一本**查字典**（哈希表），键是工厂编号，值是还能接收的机器人数量。  
  - 递归栈记录我们当前已经走到哪一步，就像在 **树** 上走路一样。

- **为什么一定能得到答案**：  
  只要遍历了 **所有** 合法的配对组合，最小的代价必然会在其中出现。

- **时间/空间复杂度**：  
  - 每个机器人都有至多 `m` 种选择，递归深度是 `n`，所以最坏情况下会产生 `m^n` 种分支。  
  - 这就是 **指数级** 的复杂度，记作 `O(m^n)`。在实际中即使 `n=m=10`，也会有 `10^10` 种可能，根本跑不完。  
  - 空间方面只需要保存递归栈和 `remaining_limits`，深度为 `n`，所以是 `O(n)`。

> **大白话**：`O(m^n)` 就像让 10 个人每人挑 10 件衣服，所有可能的搭配数是 10 的 10 次方，天文数字，根本不可能全部尝试。

#### 代码（Python）

```python
from math import inf
from typing import List

def min_total_distance_bruteforce(robot: List[int], factory: List[List[int]]) -> int:
    n, m = len(robot), len(factory)
    limits = [f[1] for f in factory]               # 每个工厂还能接收的机器人数
    pos = [f[0] for f in factory]                  # 工厂的位置

    # 递归搜索所有合法配对
    def dfs(i: int) -> int:
        if i == n:                     # 所有机器人都已经安排好
            return 0
        best = inf
        for j in range(m):
            if limits[j] == 0:         # 这个工厂已经满了，跳过
                continue
            # 选 j 号工厂为 robot[i] 的归宿
            limits[j] -= 1
            cur = abs(robot[i] - pos[j]) + dfs(i + 1)
            best = min(best, cur)
            limits[j] += 1             # 恢复现场，回溯
        return best

    return dfs(0)
```

> 这段代码可以跑通，但只适用于极小的输入，真正的题目规模（`n, m ≤ 100`）会直接超时。

#### 复杂度  

- **时间复杂度**：`O(m^n)` —— 指数级增长，几乎不可能在合理时间内完成。  
- **空间复杂度**：`O(n)` —— 递归栈的深度等于机器人数量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **“枚举所有配对”** 是慢的根源。  
我们需要 **剪枝**：如果已经知道前面若干机器人的最优配对方式，那么后面的决策可以基于它来快速计算，而不必重新枚举。

关键观察：

1. **先把机器人和工厂按位置排序**。  
   - 排序后，机器人在数轴上的相对顺序不变，工厂也是。  
   - 设 `robot[0] ≤ robot[1] ≤ … ≤ robot[n‑1]`，`factory[0].pos ≤ factory[1].pos ≤ …`。

2. **每个工厂只会修理一段连续的机器人**。  
   - 想象把机器人排成一条直线，工厂也是排好顺序的。  
   - 如果工厂 A 修理了位置在 3、7、12 的机器人，而工厂 B 修理了 5、9，这会导致机器人 5、7、9 之间交叉，必然可以把距离再缩小（把 5、7、9 统一交给更靠近它们的工厂），所以最优解一定是“每个工厂负责一段连续区间”。  
   - 这把原本的**全排列**问题简化成了“把序列切成若干段，每段交给对应的工厂”。

3. **动态规划**：  
   - 记 `dp[i][j]` 为 **前 `i` 个机器人（下标 `0..i-1`）由前 `j` 家工厂（下标 `0..j-1`）全部修好时的最小总距离**。  
   - 转移时，我们决定第 `j‑1` 家工厂（第 `j` 家）负责最近的 `k` 个机器人（`k` 可以是 `0` 到 `limit[j‑1]`），其余机器人交给前 `j‑1` 家工厂。  

   \[
   dp[i][j] = \min_{0 \le k \le \min(limit_{j-1},\, i)} 
               \bigl( dp[i-k][j-1] + \text{cost}(i-k, i-1, j-1) \bigr)
   \]

   其中 `cost(l, r, f)` 表示把机器人下标 `l … r`（共 `k = r-l+1` 台）全部送到第 `f` 家工厂的距离和。

4. **如何快速算 `cost`**  
   - 机器人数目最多 100，工厂容量总和也不超过 100，直接 **遍历** 计算 `|robot[t] - factory_pos|` 的和即可，时间仍在可接受范围（最多 `100 × 100 = 10⁴` 次加法）。  
   - 若想更快，可预先计算前缀和 `pref[i] = Σ_{t< i} robot[t]`，利用公式  
     \[
     \text{cost}(l, r, f) = \bigl( (r-l+1)·factory\_pos[f] \bigr) - (pref[r+1] - pref[l])
     \]
     当所有机器人都在工厂左侧时成立；若在右侧则取相反符号。  
   - 为了保持代码简洁，这里直接用循环累加，仍然是 `O(limit)`。

5. **初始化与答案**  
   - `dp[0][*] = 0`（没有机器人需要修理，费用为 0）。  
   - 其它未定义的状态初始化为 `INF`（一个很大的数）。  
   - 最终答案是 `dp[n][m]`（所有机器人、所有工厂都考虑完）。

**为什么这样会快**  
- 动态规划把指数级的“所有配对”压缩成 **多项式** 的状态数：`n ≤ 100`，`m ≤ 100`，每个状态内部最多遍历 `limit ≤ 100` 次。  
- 总时间复杂度约为 `O(n * m * max_limit)`，在最坏情况下是 `100 × 100 × 100 = 10⁶`，完全可以在毫秒级跑完。

#### 代码（Python）

```python
from math import inf
from typing import List

def minimumTotalDistance(robot: List[int], factory: List[List[int]]) -> int:
    # 1️⃣ 排序
    robot.sort()
    factory.sort(key=lambda x: x[0])          # 按位置排序

    n = len(robot)
    m = len(factory)

    # 2️⃣ dp[i][j]：前 i 个机器人（0..i-1）由前 j 家工厂（0..j-1）修好时的最小距离
    dp = [[inf] * (m + 1) for _ in range(n + 1)]
    for j in range(m + 1):
        dp[0][j] = 0          # 没有机器人，费用为 0

    # 3️⃣ 主循环
    for i in range(1, n + 1):          # i 为已经安排好的机器人数量
        for j in range(1, m + 1):      # j 为考虑的工厂数量
            pos, limit = factory[j - 1]          # 第 j 家工厂的位置和容量
            # 让第 j 家工厂负责 k 台机器人（k 可以为 0，表示不使用这家工厂）
            max_k = min(limit, i)
            cur_cost = 0                # 累计把最近的 k 台机器人送到该工厂的距离
            # 从后往前枚举 k（把 robot[i-1], robot[i-2], ... 逐个加入）
            for k in range(1, max_k + 1):
                # 第 i-k 台机器人（下标 i-k）是本轮加入的那个
                cur_cost += abs(robot[i - k] - pos)
                # dp[i-k][j-1] 已经处理好前 i-k 台机器人，剩下的 k 台交给第 j 家工厂
                dp[i][j] = min(dp[i][j], dp[i - k][j - 1] + cur_cost)
            # 也可以不使用第 j 家工厂，直接继承 dp[i][j-1]
            dp[i][j] = min(dp[i][j], dp[i][j - 1])

    return dp[n][m]
```

> **代码要点注释**  
- `robot.sort()` 与 `factory.sort(...)` 把“一条直线”上的对象排好顺序。  
- `dp` 表格的行是“已经安排好的机器人数”，列是“已经考虑的工厂数”。  
- 内层的 `for k` 循环是**把第 j 家工厂负责的机器人数目从 1 到上限**逐一尝试，同时用 `cur_cost` 累计对应的距离，避免每次都重新遍历。  
- `dp[i][j] = min(dp[i][j], dp[i][j-1])` 处理“这家工厂不派任何机器人”的情况，确保所有可能都被覆盖。

#### 复杂度  

- **时间复杂度**：`O(n * m * L)`，其中 `L = max(limit_j)`，最坏情况下 `n = m = L = 100`，约为 `10⁶` 次基本运算，足够快。  
  - 与暴力解的 `O(m^n)`（指数级）相比，下降到了 **多项式级**，可以在毫秒级完成。  

- **空间复杂度**：`O(n * m)` 的 DP 表，大约 `10⁴` 个整数，约占几百 KB，完全可以接受。  

---

## 心得  

- **核心技巧**：**先排序 + 区间 DP**（每个工厂负责连续子段）。  
- **适用的题型**：  
  1. “把若干点分配给若干区间，使总费用最小”——如 *Minimum Cost to Split Array*。  
  2. “有容量限制的分配问题”——如 *Assign Cookies*、*Car Pooling*（带容量的区间调度）。  
  3. “带容量的双序列匹配”——如 *Two City Scheduling*（每个城市容量固定）。  

- **一句话总结解题钥匙**：  
  > **把“一堆随意配对”转化为“把序列切段”，用 DP 按段累加最优代价**。

---

## 反思  

- **第一反应**：看到“机器人可以向左或向右移动”，立刻想到**暴力枚举所有方向**，但很快发现搜索空间爆炸。  
- **最容易踩的坑**：  
  - 忘记对 **机器人和工厂同时排序**，导致子段连续性不成立。  
  - 在 DP 转移时遗漏 “不使用当前工厂” 的情况（`dp[i][j] = min(dp[i][j], dp[i][j-1])`），会产生错误的不可达状态。  
  - 计算 `cost` 时没有注意到机器人的位置可能在工厂左侧或右侧，直接使用 `abs` 循环是安全的；若用前缀和，需要处理符号分情况。  

- **下次类似题目第一步**：  
  - **先把所有“一维坐标”排序**，观察是否可以把“每个资源负责一段连续需求”这一结构化特性抽象出来。  

祝学习愉快，玩转 DP！