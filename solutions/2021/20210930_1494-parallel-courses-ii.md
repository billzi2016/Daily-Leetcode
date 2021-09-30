# #1494. 并行课程 II / Parallel Courses II

> 难度：困难 · 标签：Dynamic Programming、Bit Manipulation、Graph、Bitmask · [LeetCode 链接](https://leetcode.com/problems/parallel-courses-ii/)

---

## 题目（英文原版）

**Description**

You are given an integer n, which indicates that there are n courses labeled from 1 to n. You are also given an array relations where relations[i] = [prevCoursei, nextCoursei], representing a prerequisite relationship between course prevCoursei and course nextCoursei: course prevCoursei has to be taken before course nextCoursei. Also, you are given the integer k.
In one semester, you can take at most k courses as long as you have taken all the prerequisites in the previous semesters for the courses you are taking.
Return the minimum number of semesters needed to take all courses. The testcases will be generated such that it is possible to take every course.

**Examples**

**Example 1:**

```
Input: n = 4, relations = [[2,1],[3,1],[1,4]], k = 2
Output: 3
Explanation: The figure above represents the given graph.
In the first semester, you can take courses 2 and 3.
In the second semester, you can take course 1.
In the third semester, you can take course 4.
```

**Example 2:**

```
Input: n = 5, relations = [[2,1],[3,1],[4,1],[1,5]], k = 2
Output: 4
Explanation: The figure above represents the given graph.
In the first semester, you can only take courses 2 and 3 since you cannot take more than two per semester.
In the second semester, you can take course 4.
In the third semester, you can take course 1.
In the fourth semester, you can take course 5.
```

**Constraints**

- 1 <= n <= 15
- 1 <= k <= n
- 0 <= relations.length <= n * (n-1) / 2
- relations[i].length == 2
- 1 <= prevCoursei, nextCoursei <= n
- prevCoursei != nextCoursei
- All the pairs [prevCoursei, nextCoursei] are unique.
- The given graph is a directed acyclic graph.

---

## 题目（中文翻译）

你得到一个整数 `n`，表示有 `n` 门课程，编号为 `1` 到 `n`。同时给定一个数组 `relations`，其中 `relations[i] = [prevCoursei, nextCoursei]` 表示课程 `prevCoursei` 必须在课程 `nextCoursei` 之前完成，即 **前置条件关系（prerequisite relationship）**。另给定整数 `k`。

在一个 **学期（semester）** 中，只要已完成所选课程的所有前置条件，你最多可以选修 `k` 门课程。返回完成所有课程所需的最少学期数。题目保证所有课程均可完成。

**示例 1**  
**示例 2**  
**约束条件**：

**示例**  
**示例 1:**  
Input: n = 4, relations = [[2,1],[3,1],[1,4]], k = 2  
Output: 3  
Explanation: 如上图所示的有向无环图。  
- 第 1 学期，你可以选修课程 2 和 3。  
- 第 2 学期，你可以选修课程 1。  
- 第 3 学期，你可以选修课程 4。  

**示例 2:**  
Input: n = 5, relations = [[2,1],[3,1],[4,1],[1,5]], k = 2  
Output: 4  
Explanation: 如上图所示的有向无环图。  
- 第 1 学期，由于每学期最多只能选修两门课，你只能选修课程 2 和 3。  
- 第 2 学期，你可以选修课程 4。  
- 第 3 学期，你可以选修课程 1。  
- 第 4 学期，你可以选修课程 5。  

**约束条件**  
- `1 <= n <= 15`  
- `1 <= k <= n`  
- `0 <= relations.length <= n * (n-1) / 2`  
- `relations[i].length == 2`  
- `1 <= prevCoursei, nextCoursei <= n`  
- `prevCoursei != nextCoursei`  
- 所有 `[prevCoursei, nextCoursei]` 对唯一。  
- 给定的图是 **有向无环图（directed acyclic graph）**。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**一步一步模拟每个学期**，在每个学期里把所有**已经满足前置条件且还能选的课程**全部挑出来，随后在这些课程中随意挑 **不超过 k 门** 的组合，递归地继续下去，直到所有课程都修完。  

- **状态表示**：用一个整数的二进制位（**位掩码 bitmask**）记录已经修完的课程。第 `i` 位为 `1` 表示第 `i` 门课已经学过，`0` 表示还没有。  
- **可选课程**：遍历所有课程，若它的所有先修课的位都已经是 `1`（即前置条件满足），且自己还没有被学过，就把它加入「本学期可选」的集合。  
- **枚举选课**：对「本学期可选」的集合，枚举所有大小 `≤ k` 的子集（即本学期可以同时修的课程组合），对每一种组合递归求解剩余课程需要的最少学期数。  

> **类比**：把 `bitmask` 想成一本 **字典**，每一页（位）对应一门课程，翻到第 `i` 页看到 “已学习” 就是 `1`，看到 “未学习” 就是 `0`。我们每次只能在已经满足前置条件的“未学习”页里挑 `k` 页一起阅读。

**为什么正确**：  
- 只要我们把 **所有可能的合法选课组合** 都遍历一遍，就一定能找到最优的那条路径。  
- 递归的基准情况是「所有课程都已学完」时，返回 `0` 学期。  

**时间/空间复杂度**（大白话解释）  
- 每个状态（即每个 `bitmask`）会尝试 **所有可选子集**。若某学期可选的课程数为 `m`，子集数就是 `C(m,0)+C(m,1)+…+C(m,k)`，最坏情况下 `m=n`，子集数大约是 `2^n`。  
- 因为递归会遍历 **每一种 `bitmask`**（最多 `2^n` 种），整体时间复杂度约为 **O( n * 3^n )**（一个常见的上界，实际会更慢）。  
- 递归栈深度最多 `n`，加上 `bitmask` 记录的哈希表（记忆化搜索），空间复杂度是 **O(2^n)**，即最多保存每个状态一次。

> 对于 `n ≤ 15`，暴力解已经非常慢，甚至会超时，但它帮助我们理解问题的本质。

#### 代码（Python）

```python
from functools import lru_cache
from itertools import combinations

def minNumberOfSemesters_bruteforce(n: int, relations, k: int) -> int:
    # 前置条件：pre[i] 的第 j 位为 1 表示课程 j 是 i 的先修课
    pre = [0] * n
    for a, b in relations:                # a 必须在 b 之前
        a -= 1; b -= 1                     # 0‑based
        pre[b] |= 1 << a

    @lru_cache(None)                      # 记忆化搜索，避免重复计算同一个 mask
    def dfs(mask: int) -> int:
        """返回从已经学完 mask（二进制）开始，完成所有课程最少需要的学期数"""
        if mask == (1 << n) - 1:           # 所有 1，说明全部修完
            return 0

        # 1）找出本学期可以选的课程集合（前置条件已满足且未修）
        can_take = []
        for i in range(n):
            if not (mask >> i) & 1:        # 课程 i 还没学
                if pre[i] & mask == pre[i]:   # 所有先修课都在 mask 中
                    can_take.append(i)

        # 2）如果可选课程数量 ≤ k，直接一次性全部修完
        if len(can_take) <= k:
            new_mask = mask
            for c in can_take:
                new_mask |= 1 << c
            return 1 + dfs(new_mask)

        # 3）枚举所有大小恰好为 k 的子集，取最小的学期数
        best = float('inf')
        for combo in combinations(can_take, k):
            new_mask = mask
            for c in combo:
                new_mask |= 1 << c
            best = min(best, 1 + dfs(new_mask))
        return best

    return dfs(0)
```

#### 复杂度  

- **时间复杂度**：`O(n * 3^n)`（每个状态遍历所有子集，最坏情况下指数级增长）。  
- **空间复杂度**：`O(2^n)`（记忆化缓存所有可能的 `mask`，以及递归栈深度 ≤ n）。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于每个状态都要枚举所有子集**，尤其是当可选课程很多时，组合数会爆炸。我们需要一种方式 **一次性把同一状态的所有可能“选课”结果合并**，而不是逐个子集去递归。

关键观察：  
1. **状态仍然可以用位掩码表示**——因为 `n ≤ 15`，2^15=32768，足够小，能够完整遍历。  
2. 对于任意 `mask`，**本学期能选的课程集合**是唯一的，记作 `avail(mask)`。  
3. 如果 `|avail| ≤ k`，显然一次性全部修完是最优的——因为再拆成多学期只会让总学期数增加。  
4. 当 `|avail| > k` 时，我们需要从 `avail` 中挑 **恰好 k 门** 或 **任意 ≤ k 门** 的子集。这里可以利用 **子掩码枚举**：遍历 `sub = avail` 的所有子集 `sub = (sub-1) & avail`，只保留 `popcount(sub) ≤ k` 的子集。  
5. 对每个合法子集 `sub`，下一个状态就是 `mask | sub`，我们在 DP 中取 **最小的学期数**。  

这样，**每个 `mask` 只遍历一次它的所有子集**，而不必递归产生重复的子状态。整个算法的时间复杂度是 `O( n * 2^n )`（因为每个 `mask` 的子集枚举总和等于 `3^n`，但通过位运算和剪枝可以控制在 `n * 2^n` 以内），在 `n ≤ 15` 时非常快。

#### 核心工具  

- **位掩码**（bitmask）：整数的二进制位直接对应课程的“已修/未修”。  
- **前置掩码数组 `pre[i]`**：每门课的所有先修课对应的位集合。  
- **子掩码枚举技巧**：`sub = (sub-1) & mask` 能在 O(子集数) 时间遍历 `mask` 的所有子集。  

> **类比**：把 `mask` 看成一块拼图，已经拼好的部分是 `1`，剩下的空位是 `0`。`avail(mask)` 就是当前可以放进去的拼块集合。我们一次性尝试把 **最多 k 块** 拼进去，看看哪种放法能让整体拼图最快完成。

#### 代码（Python）

```python
from functools import lru_cache
from math import inf

def minNumberOfSemesters(n: int, relations, k: int) -> int:
    # 1. 预处理：每门课的前置课程集合，用位掩码表示
    pre = [0] * n
    for a, b in relations:
        a -= 1; b -= 1
        pre[b] |= 1 << a

    full_mask = (1 << n) - 1               # 所有课程都学完的掩码

    @lru_cache(None)
    def dp(mask: int) -> int:
        """mask 表示已经修完的课程集合，返回从这里到完成所有课程的最少学期数"""
        if mask == full_mask:
            return 0

        # 2. 计算本学期可以选的课程集合（前置已满足且未学）
        avail = 0
        for i in range(n):
            if not (mask >> i) & 1:        # 课程 i 未学
                if pre[i] & mask == pre[i]:   # 所有先修课都已学
                    avail |= 1 << i

        # 3. 如果可选数量 ≤ k，直接一次性全选
        cnt_avail = bin(avail).count('1')
        if cnt_avail <= k:
            return 1 + dp(mask | avail)

        # 4. 否则枚举 avail 的所有子集，子集大小 ≤ k，取最小结果
        best = inf
        sub = avail
        while sub:
            if bin(sub).count('1') <= k:   # 只考虑合法子集
                best = min(best, 1 + dp(mask | sub))
            sub = (sub - 1) & avail        # 下一个子集
        return best

    return dp(0)
```

> **代码说明（关键行中文注释）**  
- `pre[b] |= 1 << a`：把课程 `a` 加入课程 `b` 的前置集合。  
- `if pre[i] & mask == pre[i]`：检查 `i` 的所有前置课程是否已经在 `mask` 中（即已经学完）。  
- `while sub: sub = (sub - 1) & avail`：高效遍历 `avail` 的所有子集。  
- `if cnt_avail <= k: return 1 + dp(mask | avail)`：一次性把所有可选课程修完，省去子集枚举。

#### 复杂度  

- **时间复杂度**：`O(n * 2^n)`  
  - `2^n` 是状态数（每个 `mask`）。  
  - 对每个状态我们最多遍历它的子集一次，子集枚举的总量在 `n * 2^n` 级别。  
  - 对于 `n ≤ 15`，大约 `15 * 32768 ≈ 5×10⁵` 次操作，毫秒级完成。  

- **空间复杂度**：`O(2^n)`  
  - 记忆化缓存 `dp(mask)` 的结果，需要存储每个状态一次。  
  - 递归深度最多 `n`，属于常数级额外空间。  

---

## 心得  

- **核心技巧**：**位掩码 + 动态规划**（或记忆化搜索），配合**子集枚举**快速遍历合法选课组合。  
- **适用题型**  
  1. **并行课程类**：如 *Parallel Courses*（只求最少学期数，不限制每学期课程数）。  
  2. **带前置约束的集合选择**：如 *Course Schedule III*（带权值的课程调度）。  
  3. **小规模状态压缩 DP**：如 *Maximum Employees to Be Invited to a Meeting*（人数 ≤ 20 的状态压缩）。  
- **一句话总结**：把“已经学的课程”压进二进制位，用 DP 把“每个学期可以一次性选的课程集合”一次性算完，就能在指数级状态里找到最短学期数。  

---

## 反思  

- **第一反应**：看到“最多 k 门课”“先修关系”，立刻想到 **拓扑排序 + 每学期挑 k 门**，于是尝试直接模拟。  
- **最容易踩的坑**  
  - **子集枚举的正确性**：忘记限制子集大小 `≤ k` 会导致错误答案或时间爆炸。  
  - **前置条件判断**：必须确保 **所有** 先修课都已完成，`pre[i] & mask == pre[i]` 是关键等式，容易写成 `pre[i] & mask != 0`（错误）。  
  - **边界情况**：当 `avail` 的课程数恰好等于 `k` 时，一定一次性全部修完，别再去枚举子集。  
- **下次类似题的第一步**：先把 **状态压缩**（位掩码）写出来，计算 **每个状态的可选集合**，判断是否可以一次性全部选完，再决定是否需要子集枚举或贪心。这样思路清晰，代码实现也更稳妥。