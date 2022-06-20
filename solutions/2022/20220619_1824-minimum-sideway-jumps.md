# #1824. 最小侧向跳跃 / Minimum Sideway Jumps

> 难度：中等 · 标签：Array、Dynamic Programming、Greedy · [LeetCode 链接](https://leetcode.com/problems/minimum-sideway-jumps/)

---

## 题目（英文原版）

**Description**

There is a 3 lane road of length n that consists of n + 1 points labeled from 0 to n. A frog starts at point 0 in the second lane and wants to jump to point n. However, there could be obstacles along the way.
You are given an array obstacles of length n + 1 where each obstacles[i] (ranging from 0 to 3) describes an obstacle on the lane obstacles[i] at point i. If obstacles[i] == 0, there are no obstacles at point i. There will be at most one obstacle in the 3 lanes at each point.
The frog can only travel from point i to point i + 1 on the same lane if there is not an obstacle on the lane at point i + 1. To avoid obstacles, the frog can also perform a side jump to jump to another lane (even if they are not adjacent) at the same point if there is no obstacle on the new lane.
Return the minimum number of side jumps the frog needs to reach any lane at point n starting from lane 2 at point 0.
Note: There will be no obstacles on points 0 and n.

**Examples**

**Example 1:**

```
Input: obstacles = [0,1,2,3,0]
Output: 2 
Explanation: The optimal solution is shown by the arrows above. There are 2 side jumps (red arrows).
Note that the frog can jump over obstacles only when making side jumps (as shown at point 2).
```

**Example 2:**

```
Input: obstacles = [0,1,1,3,3,0]
Output: 0
Explanation: There are no obstacles on lane 2. No side jumps are required.
```

**Example 3:**

```
Input: obstacles = [0,2,1,0,3,0]
Output: 2
Explanation: The optimal solution is shown by the arrows above. There are 2 side jumps.
```

**Constraints**

- obstacles.length == n + 1
- 1 <= n <= 5 * 105
- 0 <= obstacles[i] <= 3
- obstacles[0] == obstacles[n] == 0

---

## 题目（中文翻译）

描述  
有一条长度为 `n` 的三车道（lane）道路，包含标号从 `0` 到 `n` 的 `n + 1` 个点（point）。青蛙从点 `0` 的第二车道（lane）出发，目标是跳到点 `n`。途中可能会出现障碍物（obstacle）。

给定一个长度为 `n + 1` 的数组 `obstacles`，其中 `obstacles[i]`（取值范围 `0`~`3`）表示点 `i` 上第 `obstacles[i]` 条车道上的障碍物（obstacle）。若 `obstacles[i] == 0`，则点 `i` 没有障碍物。每个点至多有一条车道上有障碍物。

青蛙只能在同一车道上从点 `i` 前进到点 `i + 1`，前提是点 `i + 1` 的该车道没有障碍物。为避开障碍物，青蛙还可以在同一点上进行侧向跳跃（side jump）到另一条车道（即使不是相邻的车道），前提是目标车道在该点没有障碍物。

返回青蛙从点 `0` 的第 2 条车道（lane）出发，达到点 `n` 任意车道所需的最少侧向跳跃次数。  
注意：点 `0` 和点 `n` 上不会有障碍物。

示例  

示例 1  
Input: obstacles = [0,1,2,3,0]  
Output: 2  
Explanation: 如上图所示的箭头所示的路径为最优解，共需要 2 次侧向跳跃（红色箭头）。注意，青蛙只能在进行侧向跳跃时跨越障碍物（如点 2 处所示）。

示例 2  
Input: obstacles = [0,1,1,3,3,0]  
Output: 0  
Explanation: 第 2 条车道（lane）上没有障碍物，无需侧向跳跃。

示例 3  
Input: obstacles = [0,2,1,0,3,0]  
Output: 2  
Explanation: 如上图所示的箭头所示的路径为最优解，共需要 2 次侧向跳跃。

约束条件  
- `obstacles.length == n + 1`  
- `1 <= n <= 5 * 10^5`  
- `0 <= obstacles[i] <= 3`  
- `obstacles[0] == obstacles[n] == 0`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把青蛙的每一步当成一次“选择”。  
在每个位置 `i`（从 0 到 n），青蛙可能处在 **第 1、2、3 条车道** 中的任意一条，只要该车道在位置 `i` 没有障碍物。  
于是我们可以把 **状态** 定义为 `(i, lane)`，表示青蛙在位置 `i`、第 `lane` 条车道。  

从一个状态出发，有两种合法的移动方式  

1. **向前走一步**：`(i, lane) → (i+1, lane)`，前提是 `obstacles[i+1] != lane`（下一个点该车道没有障碍）。  
2. **侧跳**：`(i, lane) → (i, new_lane)`，`new_lane` 可以是任意另一条车道，只要 `obstacles[i] != new_lane`（同一点的目标车道没有障碍），这会产生 **一次** 侧跳计数。  

于是我们可以用 **广度优先搜索（BFS）** 或 **递归 + 记忆化搜索** 来遍历所有可能的路径，记录到达终点 `n` 时的最小侧跳次数。  

> **类比**：把每个状态想象成一本词典的“词条”，`i` 是章节，`lane` 是小节。我们要找一条从章节 0 第 2 小节走到章节 n 任意小节的最短“跳转”路径。

**为什么一定能得到正确答案？**  
因为 BFS 按层遍历，先到达终点的路径一定是侧跳次数最少的路径；递归 + 记忆化搜索则穷举了所有合法的走法，并且把每个子问题的最优解保存下来，避免重复计算。

**时间/空间复杂度**  
- 位置有 `n+1`（最多 5·10⁵）个，车道只有 3 条。  
- 每个状态最多产生两条边（前进或侧跳），所以状态总数是 `3·(n+1)`，遍历全部状态的时间是 **O(3·n) = O(n)**。  
- 但是如果我们不做任何剪枝，递归会产生指数级的分支，因为每到一个位置都可能尝试 2~3 条车道的侧跳，最坏情况下会出现 **O(3ⁿ)** 的搜索树，根本不可接受。  

> **大白话**：`O(n²)` 就像把 1000 张纸两两比较，需要 1,000,000 次操作；`O(3ⁿ)` 更糟，像是把 20 张纸全排列，需要 3.5×10⁹ 次操作，根本跑不完。

#### 代码（Python）  

```python
from collections import deque
from typing import List

def minSideJumps_bruteforce(obstacles: List[int]) -> int:
    n = len(obstacles) - 1               # 最后一个点的下标
    # 每个状态 (position, lane) 用 (i, l) 表示，lane 取值 1~3
    # BFS 队列里保存 (i, lane, jumps) 
    q = deque()
    q.append((0, 2, 0))                   # 起点：位置 0，第二条车道，侧跳次数 0
    visited = set()                      # 防止重复访问同一状态
    visited.add((0, 2))

    while q:
        i, lane, jumps = q.popleft()
        # 到达终点，返回当前的侧跳次数（BFS 保证是最小的）
        if i == n:
            return jumps

        # 1. 向前走一步（如果前方没有障碍）
        if i + 1 <= n and obstacles[i + 1] != lane:
            if (i + 1, lane) not in visited:
                visited.add((i + 1, lane))
                q.append((i + 1, lane, jumps))

        # 2. 侧跳到其他车道（同一点，计一次侧跳）
        for new_lane in (1, 2, 3):
            if new_lane == lane:                     # 不能跳到自己所在的车道
                continue
            if obstacles[i] == new_lane:             # 目标车道此点有障碍，不能跳
                continue
            if (i, new_lane) not in visited:
                visited.add((i, new_lane))
                q.append((i, new_lane, jumps + 1))

    # 按题意一定能到达，这行代码理论上不会执行
    return -1
```

> **关键行中文注释** 已在代码中标明。

#### 复杂度  

- **时间复杂度**：最坏情况下仍然是指数级的 `O(3ⁿ)`，因为每一步都可能尝试多条侧跳，搜索树会爆炸。  
- **空间复杂度**：队列中最多会存储所有状态，理论上是 `O(3·n)`，即 `O(n)`，但实际受指数级分支的影响会远大于此。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**状态只与当前位置和所在车道有关**，而且车道只有 3 条。  
因此我们可以用 **动态规划（DP）** 把“每一步的最优解”压缩到常数空间，而不必枚举所有路径。

**瓶颈在哪里？**  
- 暴力解在每个位置都要遍历所有可能的侧跳组合，导致指数级分支。  
- 实际上，**在同一点的侧跳次数只与“已经到达该点的三条车道的最小侧跳数”有关**，不需要记忆所有历史路径。

**核心思想**：  
- 设 `dp[l]` 为 **到达当前点 `i` 并站在车道 `l`（1‑3）时的最小侧跳次数**。  
- 初始时（点 0）：青蛙在第 2 条车道，侧跳次数为 0；如果直接在起点侧跳到第 1 或第 3 条车道，需要一次侧跳。于是  
  ```
  dp = [inf, 0, inf]   # 这里下标 0、1、2 对应车道 1、2、3
  dp[0] = dp[2] = 1    # 起点侧跳到车道 1 或 3 各需要一次
  ```
- 然后遍历每个位置 `i = 1 … n`：  
  1. **把障碍所在的车道设为不可达**（`dp[obstacle] = inf`），因为青蛙不能站在有障碍的车道上。  
  2. **在同一点进行侧跳**：如果某条车道 `l` 没有障碍，我们可以考虑从其他两条车道侧跳过来，代价是 **`其他车道的 dp + 1`**（多一次侧跳）。于是对每条可行车道执行  
     ```
     dp[l] = min(dp[l], min(dp[other1], dp[other2]) + 1)
     ```
     这一步相当于 “在当前位置，把三条车道的侧跳次数统一调平”。  
  3. **向前一步**：因为我们已经在 `dp` 中保存的是 **到达当前位置** 的最小次数，向前一步不需要额外操作，只要保证下一轮的障碍处理即可。  

遍历完所有点后，答案就是 `min(dp)`，即到达终点 `n` 时三条车道中侧跳次数最少的那条。

**为什么这一步一步的推导是对的？**  
- DP 的状态转移只依赖**当前点**的 `dp`，而不需要记忆之前的细节，因为所有可能的路径在到达同一点时已经归约为最小的侧跳次数。  
- 在每一步先“剔除障碍”，再“在同一点做最优侧跳”，等价于在**同一点**先把三条车道的侧跳次数同步到最小值，然后再向前走一步。  
- 这种顺序保证了没有遗漏任何合法的侧跳组合。

> **类比**：把三条车道想象成三根平行的跑道，`dp[l]` 就是跑到当前位置时在第 `l` 条跑道上最少需要的“换道次数”。每到一个新位置，我们先把有障碍的跑道封闭，然后让三根跑道之间相互“分享”最少的换道次数，最后继续跑向前方。

#### 代码（Python）  

```python
from typing import List

def minSideJumps(obstacles: List[int]) -> int:
    INF = 10 ** 9                     # 一个足够大的数，代表“不可能”
    # dp[0]、dp[1]、dp[2] 分别对应车道 1、2、3
    dp = [1, 0, 1]                    # 起点：在车道 2 上 0 次侧跳，车道 1/3 需要先侧跳一次

    for i in range(1, len(obstacles)):
        obs = obstacles[i]            # 该点的障碍所在车道（0 表示没有障碍）

        # 1）把有障碍的车道标记为不可达
        if obs != 0:
            dp[obs - 1] = INF         # -1 把车道编号转成列表下标

        # 2）在同一点进行必要的侧跳，使三条车道的次数同步到最小
        # 这里遍历三条车道，尝试从其他两条车道侧跳过来
        for lane in range(3):
            if obstacles[i] == lane + 1:   # 该车道此点有障碍，跳过
                continue
            # 取另外两条车道的最小值 + 1（一次侧跳）
            other_min = min(dp[(lane + 1) % 3], dp[(lane + 2) % 3]) + 1
            dp[lane] = min(dp[lane], other_min)

        # 经过上述两步，dp 已经是“到达位置 i 且站在每条车道的最小侧跳次数”
        # 向前一步不需要额外操作，因为我们已经在 dp 中记录了到达 i 的代价

    # 最后返回三条车道中最小的侧跳次数
    return min(dp)
```

> **关键行中文注释** 已在代码中标明。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 我们只遍历一次数组 `obstacles`（长度 `n+1`），每个位置内部的循环最多遍历 3 条车道，常数时间。  
  - **含义**：如果 `n = 100,000`，算法大约只需要 300,000 次简单的比较和赋值，几乎是瞬间完成。  

- **空间复杂度**：`O(1)`  
  - 只用了长度为 3 的 `dp` 数组以及若干常数变量，和 `n` 的大小无关。  
  - **含义**：不管路有多长，程序占用的内存几乎不变（几百字节），非常省空间。

---

## 心得  

- **核心技巧**：在每个位置维护三条车道的**最小侧跳次数**，并在遇到障碍时把对应车道设为不可达，再通过一次遍历把三条车道之间的侧跳次数同步到最小。  
- **适用的题型**  
  1. **多状态 DP**：如「跳跃游戏 III」的三种状态切换。  
  2. **路径最小代价问题**，但状态数极小（常数），如「最小代价爬楼梯」的 2‑状态 DP。  
  3. **有障碍的多车道最短路径**，比如「三轨铁路最少换线」等。  
- **一句话总结解题钥匙**：**只在同一点做“全局最小侧跳同步”，不必在每一步枚举所有可能的跳跃路径**。

---

## 反思  

- **第一反应**：看到只有 3 条车道，就想用 BFS 暴力搜索所有可能的跳法。  
- **最容易踩的坑**  
  1. **忘记把起点两侧车道的侧跳次数初始化为 1**，导致答案偏大。  
  2. **在同步侧跳时误把当前车道也算进最小值**，会产生错误的 `+1`。  
  3. **障碍为 0 时忘记跳过**，导致把 `dp` 设为 `INF`，程序直接报错。  
- **下次遇到同类题**，第一步应该先**确定状态数是否常数**（如只有 3 条车道），如果是，就尝试 **DP + 常数空间压缩**，而不是直接 BFS。这样既能保证正确性，又能得到线性时间的最优解。