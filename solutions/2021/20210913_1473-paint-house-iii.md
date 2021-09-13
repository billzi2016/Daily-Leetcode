# #1473. 粉刷房子 III / Paint House III

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/paint-house-iii/)

---

## 题目（英文原版）

**Description**

There is a row of m houses in a small city, each house must be painted with one of the n colors (labeled from 1 to n), some houses that have been painted last summer should not be painted again.
A neighborhood is a maximal group of continuous houses that are painted with the same color.
Given an array houses, an m x n matrix cost and an integer target where:
Return the minimum cost of painting all the remaining houses in such a way that there are exactly target neighborhoods. If it is not possible, return -1.

**Examples**

**Example 1:**

```
Input: houses = [0,0,0,0,0], cost = [[1,10],[10,1],[10,1],[1,10],[5,1]], m = 5, n = 2, target = 3
Output: 9
Explanation: Paint houses of this way [1,2,2,1,1]
This array contains target = 3 neighborhoods, [{1}, {2,2}, {1,1}].
Cost of paint all houses (1 + 1 + 1 + 1 + 5) = 9.
```

**Example 2:**

```
Input: houses = [0,2,1,2,0], cost = [[1,10],[10,1],[10,1],[1,10],[5,1]], m = 5, n = 2, target = 3
Output: 11
Explanation: Some houses are already painted, Paint the houses of this way [2,2,1,2,2]
This array contains target = 3 neighborhoods, [{2,2}, {1}, {2,2}]. 
Cost of paint the first and last house (10 + 1) = 11.
```

**Example 3:**

```
Input: houses = [3,1,2,3], cost = [[1,1,1],[1,1,1],[1,1,1],[1,1,1]], m = 4, n = 3, target = 3
Output: -1
Explanation: Houses are already painted with a total of 4 neighborhoods [{3},{1},{2},{3}] different of target = 3.
```

**Constraints**

- m == houses.length == cost.length
- n == cost[i].length
- 1 <= m <= 100
- 1 <= n <= 20
- 1 <= target <= m
- 0 <= houses[i] <= n
- 1 <= cost[i][j] <= 104

---

## 题目（中文翻译）

**题目描述**  
在一条直线上有 `m` 栋房子，每栋房子必须涂上 `n` 种颜色中的一种（颜色编号为 `1` 到 `n`），其中已经在去年夏天涂好的房子不能再次涂色。  
**社区（neighborhood）** 是指颜色相同且连续的一段最大房子集合。  

给定数组 `houses`、一个 `m × n` 的矩阵 `cost` 和整数 `target`，其中：

- `houses[i] = 0` 表示第 `i` 栋房子尚未涂色，`houses[i] = c (1 ≤ c ≤ n)` 表示第 `i` 栋房子已经涂成颜色 `c`。  
- `cost[i][j]` 表示如果第 `i` 栋房子未涂色且选择涂成颜色 `j`，需要的费用。

请返回涂完所有未涂色房子且恰好形成 `target` 个社区的最小费用。如果无法满足要求，返回 `-1`。

---

### 示例

**示例 1**  
```
Input: houses = [0,0,0,0,0], cost = [[1,10],[10,1],[10,1],[1,10],[5,1]], m = 5, n = 2, target = 3
Output: 9
Explanation: 将房子按颜色序列涂成 [1,2,2,1,1]。  
该序列包含 3 个社区，分别为 [{1}, {2,2}, {1,1}]。  
涂色总费用为 (1 + 1 + 1 + 1 + 5) = 9。
```

**示例 2**  
```
Input: houses = [0,2,1,2,0], cost = [[1,10],[10,1],[10,1],[1,10],[5,1]], m = 5, n = 2, target = 3
Output: 11
Explanation: 已有部分房子被涂色，最终的颜色序列为 [2,2,1,2,2]。  
该序列包含 3 个社区，分别为 [{2,2}, {1}, {2,2}]。  
仅需要涂第 1 栋和第 5 栋房子，费用为 (10 + 1) = 11。
```

**示例 3**  
```
Input: houses = [3,1,2,3], cost = [[1,1,1],[1,1,1],[1,1,1],[1,1,1]], m = 4, n = 3, target = 3
Output: -1
Explanation: 所有房子已经被涂色，形成了 4 个社区 [{3},{1},{2},{3}]，无法达到目标社区数 target = 3。
```

---

### 约束条件

- `m == houses.length == cost.length`
- `n == cost[i].length`
- `1 <= m <= 100`
- `1 <= n <= 20`
- `1 <= target <= m`
- `0 <= houses[i] <= n`
- `1 <= cost[i][j] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有 **未上色** 的房子一次性枚举所有可能的颜色组合，然后逐一检查：

1. 组合是否合法（已经上色的房子颜色不能改）。
2. 统计形成了多少个相邻相同颜色的 **社区**（neighborhood）。
3. 如果社区数恰好等于 `target`，就把这套组合的涂色费用相加，取最小值。

> **数据结构类比**  
> - `houses` 就像一排排的房子，已经有颜色的格子相当于**已经写好的字**，不能再改。  
> - `cost[i][c]` 可以想成**字典**，键是 `(第 i 间房子, 颜色 c)`，值是“写这本字需要的笔墨”。  
> - 用 **递归** 把每一间房子当成一层“选择题”，类似“在每个空格里填字”。

因为每间未上色的房子都有 `n` 种颜色可以选，若有 `u` 间未上色，则总共会产生 `n^u` 种组合，随 `m`（最多 100）增长极快，实际上不可接受。但作为 **暴力思路**，它帮助我们确认“枚举所有可能”一定能得到正确答案，只是效率太低。

#### 代码（Python）

```python
from typing import List

def minCost_bruteforce(houses: List[int],
                       cost: List[List[int]],
                       m: int, n: int, target: int) -> int:
    INF = float('inf')
    ans = INF

    # 递归枚举第 i 间房子的颜色
    def dfs(i: int, cur_nei: int, prev_color: int, cur_cost: int):
        nonlocal ans
        # 剪枝：已经超出目标社区数或已经比当前最优更贵
        if cur_nei > target or cur_cost >= ans:
            return
        # 所有房子都决定完了
        if i == m:
            if cur_nei == target:          # 正好 target 个社区
                ans = min(ans, cur_cost)
            return

        if houses[i] != 0:                 # 已经上色，不能改
            new_nei = cur_nei + (1 if houses[i] != prev_color else 0)
            dfs(i + 1, new_nei, houses[i], cur_cost)
        else:
            # 未上色，尝试所有颜色
            for c in range(1, n + 1):
                add_cost = cost[i][c - 1]   # cost 数组是 0-index
                new_nei = cur_nei + (1 if c != prev_color else 0)
                dfs(i + 1, new_nei, c, cur_cost + add_cost)

    # 从第一间房子开始，prev_color 设为 0（表示“没有前一个颜色”）
    dfs(0, 0, 0, 0)
    return -1 if ans == INF else ans
```

> **关键行注释**  
> - `if houses[i] != 0:`：已经有颜色的房子只能沿用原颜色。  
> - `new_nei = cur_nei + (1 if c != prev_color else 0)`：如果当前颜色和前一个颜色不一样，就多形成一个社区。  
> - `if cur_nei > target or cur_cost >= ans:`：提前剪掉不可能得到更好答案的分支。

#### 复杂度

- **时间复杂度**：`O(n^u)`，其中 `u` 为未上色房子的数量。  
  > 这相当于“每间空房子都有 `n` 种选择”，指数级增长，实际运行会超时。
- **空间复杂度**：`O(m)`，递归栈最多保存 `m` 层调用。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **大量重复计算**：相同的子问题会被反复枚举。  
例如，当我们已经决定了前 `i` 间房子的颜色以及形成的社区数后，后面的选择只与当前**颜色**和**社区数**有关，和之前的具体排列无关。  

这正好符合 **动态规划（Dynamic Programming, DP）** 的使用场景：把“大问题”拆成“子问题”，把子问题的最优解保存下来，以免重复计算。

**状态定义**  
我们使用三维 DP：

```
dp[i][c][k] = 前 i 间房子（0~i-1）已经涂好，
              第 i-1 间房子的颜色恰好是 c（1~n），
              形成了 k 个社区时的最小花费。
```

- `i` 范围 `1 … m`（处理前 i 间房子），为了实现时更自然，用 `i` 表示已经处理完的房子数。
- `c` 范围 `1 … n`（第 i-1 间房子的颜色）。
- `k` 范围 `1 … target`（社区数）。

**初始状态**  
- 当 `i = 1`（只处理第一间房子）时：
  - 如果 `houses[0]` 已经有颜色 `c0`，则 `dp[1][c0][1] = 0`（不需要费用）。
  - 否则，对每种可选颜色 `c`，`dp[1][c][1] = cost[0][c-1]`。

**状态转移**  
处理第 `i`（从 2 到 m）间房子时，考虑两种情况：

1. **第 i-1 间房子已经有颜色**（`houses[i-1] != 0`），只能取这唯一颜色 `cur = houses[i-1]`。  
   - 若 `cur` 与前一个颜色 `prev` 相同，社区数不变：`k` stays.  
   - 若不同，社区数 +1。  
   - 因此：
     ```
     dp[i][cur][k] = min(
         dp[i-1][cur][k],                # 前一颜色相同，社区数不增
         min_{prev != cur} dp[i-1][prev][k-1]   # 前一颜色不同，社区数加 1
     )
     ```

2. **第 i-1 间房子未上色**（`houses[i-1] == 0`），我们可以选任意颜色 `cur`，并且要加上对应的涂色费用 `cost[i-1][cur-1]`。转移式与已上色类似，只是多了一笔费用：
   ```
   dp[i][cur][k] = min(
       dp[i-1][cur][k] + cost[i-1][cur-1],                     # 与前一颜色相同
       min_{prev != cur} dp[i-1][prev][k-1] + cost[i-1][cur-1] # 与前一颜色不同
   )
   ```

**实现技巧**  
- `dp` 中的 “无解” 用一个很大的数 `INF` 表示，避免与实际费用混淆。  
- 为了求 `min_{prev != cur}`，我们可以遍历所有 `prev`（`n ≤ 20`），时间仍然可接受（`m * n * n * target` ≤ 100 * 20 * 20 * 100 = 4e6）。  
- 最后答案是 `min_{c} dp[m][c][target]`，即处理完所有房子后，恰好形成 `target` 个社区的最小费用。若仍为 `INF`，说明不可达，返回 `-1`。

#### 代码（Python）

```python
from typing import List

def minCost(houses: List[int],
           cost: List[List[int]],
           m: int, n: int, target: int) -> int:
    INF = 10 ** 15                     # 足够大的“无解”标记

    # dp[i][c][k] 只保留前一行，空间可以压缩到二维 (c, k)
    # 为了代码直观，这里直接使用三维列表（m+1) * (n+1) * (target+1)
    dp = [[[INF] * (target + 1) for _ in range(n + 1)] for _ in range(m + 1)]

    # ---------- 初始化第一间房子 ----------
    if houses[0] != 0:                         # 已经有颜色
        c = houses[0]
        dp[1][c][1] = 0                        # 不需要费用，社区数为 1
    else:                                       # 未上色，尝试所有颜色
        for c in range(1, n + 1):
            dp[1][c][1] = cost[0][c - 1]       # 费用即 cost[0][c-1]

    # ---------- 逐房子递推 ----------
    for i in range(2, m + 1):                   # i 表示已处理 i 间房子
        cur_house_color = houses[i - 1]         # 第 i-1 间（0-index）房子颜色
        for cur_color in range(1, n + 1):       # 本次决定的颜色
            if cur_house_color != 0 and cur_color != cur_house_color:
                # 这间房子已经有颜色，且与 cur_color 不符，直接跳过
                continue

            paint_cost = 0 if cur_house_color != 0 else cost[i - 1][cur_color - 1]

            for k in range(1, target + 1):
                # ---- 情形 1：前一间房子颜色和当前颜色相同 ----
                same = dp[i - 1][cur_color][k]
                if same != INF:
                    dp[i][cur_color][k] = min(dp[i][cur_color][k],
                                             same + paint_cost)

                # ---- 情形 2：前一间房子颜色不同，社区数加 1 ----
                if k > 1:   # 需要至少有一个已有社区才能加 1
                    best = INF
                    for prev_color in range(1, n + 1):
                        if prev_color == cur_color:
                            continue
                        prev = dp[i - 1][prev_color][k - 1]
                        if prev < best:
                            best = prev
                    if best != INF:
                        dp[i][cur_color][k] = min(dp[i][cur_color][k],
                                                 best + paint_cost)

    # ---------- 取最小答案 ----------
    ans = min(dp[m][c][target] for c in range(1, n + 1))
    return -1 if ans == INF else ans
```

> **代码要点解释**  
> - `dp[i][c][k]` 用 `INF` 初始化，表示“暂时不可达”。  
> - `paint_cost`：如果该房子已经有颜色，则涂色费用为 0；否则加上对应的 `cost`。  
> - 两种转移分别对应“颜色相同”与“颜色不同”。  
> - 最外层遍历 `k`（社区数）时，只在 `k > 1` 时才考虑“颜色不同并新增社区”，因为第一个社区只能在第一间房子时产生。  
> - 最终答案取所有可能的最后颜色的最小值。

#### 复杂度

- **时间复杂度**：`O(m * n * n * target)`  
  - 外层遍历 `m`（最多 100）  
  - 内层遍历当前颜色 `n`（最多 20）  
  - 再遍历目标社区数 `target`（最多 `m`）  
  - 为了求 “前一个颜色不同” 的最小值，需要再遍历一次 `n`。  
  - 计算上限约 `100 * 20 * 20 * 100 = 4,000,000`，在 Python 中毫秒级即可跑完。

- **空间复杂度**：`O(m * n * target)`（若压缩为两层可降为 `O(n * target)`），这里使用完整三维数组，最多 `101 * 21 * 101 ≈ 2.1e5` 个整数，约几百 KB，完全可以接受。

---

## 心得

- **核心技巧**：使用三维动态规划 `dp[i][color][neighborhood]`，把“已经决定的前缀信息”压缩成“当前颜色”和“已形成的社区数”。  
- **适用的题型**  
  1. **Paint House / Paint House II**（要求最少费用的涂色问题，社区数固定为 `m`）。  
  2. **String segmentation / Word Break**（把字符串划分成若干段，每段满足条件），同样可以用 “位置 + 上一段状态” 的 DP。  
  3. **划分数组为 k 段的最小代价**（如 LeetCode 1477. 找到 k 条不相交的子数组的最大和），思路类似：`dp[i][k]` 表示前 i 项划分成 k 段的最优值。

- **一句话总结**：  
  *把“已经决定了多少社区以及最后一个颜色是什么”这两个信息保存下来，就能用 DP 高效遍历所有合法涂色方案。*

---

## 反思

- **第一反应**：看到 “社区（neighborhood）” 这个概念，我立刻想到“相邻相同颜色的连续段”。于是想到枚举所有颜色组合的暴力解。  
- **最容易踩的坑**  
  1. **边界条件**：`k = 1` 时只能从 `i = 1` 开始形成社区，转移时要防止访问 `dp[i-1][*][0]`（不存在）。  
  2. **已上色房子**：忘记在转移时把费用设为 0，会导致多算成本。  
  3. **状态初始化**：若把 `dp[0][*][*]` 也算进来，容易出现“前一颜色不存在”导致的错误，需要把第一间房子单独初始化。  
- **下次类似题的第一步**：  
  *先明确“状态”到底需要哪些信息才能唯一决定后续的最优子结构——这里是“已经处理到第几间房子、当前颜色、已经形成的社区数”。* 再据此写出 DP 转移式，避免盲目枚举。