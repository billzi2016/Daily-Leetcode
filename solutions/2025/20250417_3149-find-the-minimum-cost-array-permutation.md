# #3149. 寻找最小代价数组排列 / Find the Minimum Cost Array Permutation

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/find-the-minimum-cost-array-permutation/)

---

## 题目（英文原版）

**Description**

You are given an array nums which is a permutation of [0, 1, 2, ..., n - 1]. The score of any permutation of [0, 1, 2, ..., n - 1] named perm is defined as:
score(perm) = |perm[0] - nums[perm[1]]| + |perm[1] - nums[perm[2]]| + ... + |perm[n - 1] - nums[perm[0]]|
Return the permutation perm which has the minimum possible score. If multiple permutations exist with this score, return the one that is lexicographically smallest among them.

**Examples**

**Example 1:**

```
Input: nums = [1,0,2]
Output: [0,1,2]
Explanation:

The lexicographically smallest permutation with minimum cost is [0,1,2] . The cost of this permutation is |0 - 0| + |1 - 2| + |2 - 1| = 2 .
```

**Example 2:**

```
Input: nums = [0,2,1]
Output: [0,2,1]
Explanation:

The lexicographically smallest permutation with minimum cost is [0,2,1] . The cost of this permutation is |0 - 1| + |2 - 2| + |1 - 0| = 2 .
```

**Constraints**

- 2 <= n == nums.length <= 14
- nums is a permutation of [0, 1, 2, ..., n - 1].

---

## 题目（中文翻译）

给定一个数组 `nums`，它是 `[0, 1, 2, ..., n - 1]` 的一个排列（permutation）。任意排列（permutation）`perm`（同样是 `[0, 1, 2, ..., n - 1]` 的排列）的得分（score）定义为：

```
score(perm) = |perm[0] - nums[perm[1]]| + |perm[1] - nums[perm[2]]| + ... + |perm[n - 1] - nums[perm[0]]|
```

返回得分最小的排列 `perm`。如果存在多个得分相同的排列，返回字典序（lexicographically）最小的那个。

---

### 示例

**示例 1**

```
Input: nums = [1,0,2]
Output: [0,1,2]
Explanation:
字典序最小且得分最小的排列是 [0,1,2]。该排列的得分为 |0 - 0| + |1 - 2| + |2 - 1| = 2 。
```

**示例 2**

```
Input: nums = [0,2,1]
Output: [0,2,1]
Explanation:
字典序最小且得分最小的排列是 [0,2,1]。该排列的得分为 |0 - 1| + |2 - 2| + |1 - 0| = 2 。
```

---

### 约束条件

- `2 <= n == nums.length <= 14`
- `nums` 是 `[0, 1, 2, ..., n - 1]` 的一个排列（permutation）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把所有可能的排列 `perm`（长度为 `n` 的全排列）都枚举一遍，逐个算出它们的 **score**，找出最小的那个。如果有多个得分相同的排列，就挑字典序（lexicographically）最小的。

- **数据结构**：我们只需要一个列表来保存当前枚举的排列。  
  - **全排列**可以看成“把一堆不同的球依次放进 n 个盒子”，每个盒子里只能放一个球，所有球都要放完。枚举全排列的过程类似于“把每个球尝试放进每个盒子”，这在代码里通常用递归或 `itertools.permutations` 完成。  

- **为什么正确**：因为我们把**所有**合法的 `perm` 都检查了一遍，最小的得分一定会被发现，字典序的比较也在所有最小得分的排列中挑出了最小的。

- **时间/空间复杂度**：  
  - 全排列的个数是 `n!`（n 的阶乘），每个排列需要 O(n) 的时间去计算 score，整体时间是 **O(n!·n)**。  
  - 这里的 O 符号可以想象成“随 n 增大，耗时会像 n 的阶乘一样飞快增长”，即使 n=10，10! = 3,628,800，已经非常慢了。  
  - 只用了存放一个排列的列表，空间是 **O(n)**。

#### 代码（Python）

```python
import itertools
from typing import List

def minCostPermutation_bruteforce(nums: List[int]) -> List[int]:
    n = len(nums)
    best_score = float('inf')
    best_perm = None

    # 直接遍历所有排列
    for perm in itertools.permutations(range(n)):
        # 计算 score
        score = 0
        for i in range(n):
            nxt = perm[(i + 1) % n]          # 循环到下一个位置，最后一个指向第一个
            score += abs(perm[i] - nums[nxt])
        # 更新最优解
        if score < best_score or (score == best_score and perm < best_perm):
            best_score = score
            best_perm = perm

    return list(best_perm)      # 把元组转成列表返回
```

#### 复杂度  

- **时间复杂度**：`O(n!·n)`  
  - “n!” 表示所有排列的数量，“·n” 表示对每个排列遍历一次来求和。对初学者来说，可以把它想成“先列出所有可能的排列，然后对每个排列再做一次完整的检查”。  

- **空间复杂度**：`O(n)`  
  - 只保存当前遍历的排列和几个计数器，和 n 成正比。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于“枚举所有排列”。  
`n ≤ 14`，`14!` 远远超出计算能力，但 **位运算 + 动态规划** 可以把搜索空间压到 `O(n·2^n)`，这正是 **旅行商问题（TSP）** 在 **状态压缩 DP** 中的经典做法。

**关键观察 1：**  
score 的定义是循环的：  
```
|perm[0] - nums[perm[1]]| + |perm[1] - nums[perm[2]]| + … + |perm[n-1] - nums[perm[0]]|
```
如果我们把 `perm` 看成一条环路，`perm[i]` 是环路上的第 i 个节点，`nums[perm[i+1]]` 是 **从节点 perm[i] 出发，要访问的下一个节点的“目标值”**。这和 TSP 中“从城市 A 到城市 B 的距离”非常相似，只是距离被定义为 `abs(A - nums[B])`。

**关键观察 2：**  
要得到字典序最小的答案，我们可以**固定第一个位置为 0**（因为如果把 0 放在别的地方，整体环路可以顺时针/逆时针旋转，使得 0 成为起点，而字典序会更大）。于是我们只需要在剩下的 `n-1` 个位置上安排其它数字。

**状态定义**  
- `mask`（位掩码）表示已经放进 `perm` 的元素集合，长度 `n` 位。第 `i` 位为 1 表示数字 `i` 已经被使用。  
- `last` 表示当前环路的**尾部**（即最近放进去的数字）。  
- `dp[mask][last]` 保存 **从起点 0 出发，走过 `mask` 所表示的集合，且最后一个元素是 `last` 时的最小得分**（不包括回到起点的那一段）。

**状态转移**  
从 `dp[mask][last]` 出发，尝试把一个未使用的数字 `next` 加到后面：

```
new_mask = mask | (1 << next)
cost = dp[mask][last] + abs(last - nums[next])
dp[new_mask][next] = min(dp[new_mask][next], cost)
```

这里的 `abs(last - nums[next])` 正是环路中新增的一段 “边”的代价。

**结束状态**  
当 `mask` 包含全部数字（即 `mask == (1 << n) - 1`）时，我们已经形成了一条从 0 开始、遍历所有数字的路径。还需要把最后一个节点 `last` 再连回起点 0，形成环：

```
total = dp[full_mask][last] + abs(last - nums[0])
```

把所有 `last` 的 `total` 取最小，就是答案的最小得分。

**字典序的恢复**  
仅记录最小得分还不够，我们还要返回**具体的排列**且字典序最小。做法是：

1. 在 DP 里同时记录**前驱节点**（即从哪个 `prev` 转移而来）。  
2. 当出现**相同得分**时，保留**字典序更小的路径**。因为我们是从 0 开始顺序填充的，只要在遍历 `next` 时按 **从小到大的顺序** 考虑，就能自然得到字典序最小的路径（类似 BFS 按层遍历）。  

**时间复杂度**  
- 状态数：`2^n * n`（每个子集 `mask` 乘以可能的 `last`）。  
- 每个状态转移尝试所有未使用的数字，最多 `n` 次。  
- 整体是 `O(n^2 * 2^n)`，但因为 `n ≤ 14`，`2^14 = 16384`，乘以 `14^2 ≈ 200`，完全可以在毫秒级完成。  

**空间复杂度**  
- DP 表大小同状态数：`O(n * 2^n)`。  

#### 代码（Python）

```python
from typing import List

def minCostPermutation(nums: List[int]) -> List[int]:
    n = len(nums)
    FULL = (1 << n) - 1          # 所有数字都被使用的掩码

    # dp[mask][last] = 最小得分； INF 表示尚未到达
    INF = 10 ** 9
    dp = [[INF] * n for _ in range(1 << n)]
    # 用于恢复路径的前驱指针，prev[mask][last] = 前一个节点
    prev = [[-1] * n for _ in range(1 << n)]

    # 根据提示，固定 perm[0] = 0
    dp[1 << 0][0] = 0            # 只放了 0，得分为 0

    # 遍历所有子集（mask），并且只考虑 mask 中已经包含 0 的情况
    for mask in range(1 << n):
        if not (mask & 1):       # 0 必须在子集里，否则不是合法的路径
            continue
        for last in range(n):
            if not (mask & (1 << last)):   # last 必须在子集中
                continue
            cur_score = dp[mask][last]
            if cur_score == INF:
                continue
            # 尝试把下一个未使用的数字 next 加到路径末尾
            for nxt in range(n):
                if mask & (1 << nxt):      # 已经使用过，跳过
                    continue
                new_mask = mask | (1 << nxt)
                add = abs(last - nums[nxt])
                new_score = cur_score + add
                # 若得到更小的得分，或得分相同但字典序更小（因为 nxt 按从小到大遍历）
                if new_score < dp[new_mask][nxt]:
                    dp[new_mask][nxt] = new_score
                    prev[new_mask][nxt] = last

    # 找到最小的环路得分（包含回到 0 的那段）
    best_score = INF
    last_of_best = -1
    for last in range(n):
        if dp[FULL][last] == INF:
            continue
        total = dp[FULL][last] + abs(last - nums[0])   # 回到起点的代价
        if total < best_score:
            best_score = total
            last_of_best = last

    # 依据 prev 表恢复完整的排列（逆序）
    perm = [0] * n
    mask = FULL
    cur = last_of_best
    idx = n - 1                     # 从后往前填
    while cur != -1:
        perm[idx] = cur
        idx -= 1
        prev_cur = prev[mask][cur]
        mask ^= (1 << cur)          # 把 cur 从 mask 中移除
        cur = prev_cur

    # perm[0] 必然是 0，已经填好；其余位置已经恢复
    return perm
```

#### 复杂度  

- **时间复杂度**：`O(n²·2ⁿ)`  
  - 对于每个子集 `mask`（共有 `2ⁿ` 个），我们遍历所有可能的 `last`（`n` 个），再尝试把每个未使用的 `next`（最多 `n`）加入路径。可以把它想成“先列出所有“已经走过的城市集合”，再在每个集合里尝试下一站”。对 `n=14` 来说，这个量级非常可接受。  

- **空间复杂度**：`O(n·2ⁿ)`  
  - 两个二维数组 `dp`、`prev` 各占 `n·2ⁿ` 的空间。相当于“为每一种“已经走过哪些城市”的情况，记一张表”。  

---

## 心得  

- **核心技巧**：使用 **位掩码 + 动态规划**（状态压缩 DP）把类似旅行商的环路最小化问题从指数阶暴力 (`n!`) 降到 `O(n²·2ⁿ)`。  
- **适用题型**：  
  1. **旅行商问题（TSP）**的变形，例如“最小 Hamiltonian 环路”。  
  2. **排列/子集顺序优化**，如 “最小化排列的代价” 类题。  
  3. **位运算 DP**，比如 “最小生成树的路径覆盖” 或 “按位分配资源的最优安排”。  
- **一句话总结**：把环路最小化看成“从起点出发遍历所有点的旅行”，用 **状态压缩 DP** 记住“已经走过哪些点”和“当前在何处”，即可在指数级别上高效求解。

---

## 反思  

- **第一反应**：看到循环的绝对值求和，立刻联想到“旅行商（TSP）”，因为它也是在点之间找最短环路。  
- **最容易踩的坑**：  
  - **忘记固定起点**：若不把 `perm[0]=0` 固定，返回的排列可能不是字典序最小的，需要额外比较所有环的旋转。  
  - **位运算写错**：比如 `mask & (1 << i)` 与 `mask | (1 << i)` 搞混，会导致状态转移错误或无限循环。  
  - **恢复路径时的顺序**：若在遍历 `next` 时没有按照从小到大顺序，可能得到的不是字典序最小的排列。  
- **下次遇到同类题**：第一步先 **把环路转化为“起点固定、遍历所有点”的路径问题**，再考虑 **位掩码 DP** 来记录“已经走过的点”。这样就能快速锁定解法方向。