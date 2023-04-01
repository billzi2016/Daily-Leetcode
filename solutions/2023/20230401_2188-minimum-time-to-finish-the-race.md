# #2188. **最短完成比赛的时间** / Minimum Time to Finish the Race

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-finish-the-race/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array tires where tires[i] = [fi, ri] indicates that the ith tire can finish its xth successive lap in fi * ri(x-1) seconds.
You are also given an integer changeTime and an integer numLaps.
The race consists of numLaps laps and you may start the race with any tire. You have an unlimited supply of each tire and after every lap, you may change to any given tire (including the current tire type) if you wait changeTime seconds.
Return the minimum time to finish the race.

**Examples**

**Example 1:**

```
Input: tires = [[2,3],[3,4]], changeTime = 5, numLaps = 4
Output: 21
Explanation: 
Lap 1: Start with tire 0 and finish the lap in 2 seconds.
Lap 2: Continue with tire 0 and finish the lap in 2 * 3 = 6 seconds.
Lap 3: Change tires to a new tire 0 for 5 seconds and then finish the lap in another 2 seconds.
Lap 4: Continue with tire 0 and finish the lap in 2 * 3 = 6 seconds.
Total time = 2 + 6 + 5 + 2 + 6 = 21 seconds.
The minimum time to complete the race is 21 seconds.
```

**Example 2:**

```
Input: tires = [[1,10],[2,2],[3,4]], changeTime = 6, numLaps = 5
Output: 25
Explanation: 
Lap 1: Start with tire 1 and finish the lap in 2 seconds.
Lap 2: Continue with tire 1 and finish the lap in 2 * 2 = 4 seconds.
Lap 3: Change tires to a new tire 1 for 6 seconds and then finish the lap in another 2 seconds.
Lap 4: Continue with tire 1 and finish the lap in 2 * 2 = 4 seconds.
Lap 5: Change tires to tire 0 for 6 seconds then finish the lap in another 1 second.
Total time = 2 + 4 + 6 + 2 + 4 + 6 + 1 = 25 seconds.
The minimum time to complete the race is 25 seconds.
```

**Constraints**

- 1 <= tires.length <= 105
- tires[i].length == 2
- 1 <= fi, changeTime <= 105
- 2 <= ri <= 105
- 1 <= numLaps <= 1000

---

## 题目（中文翻译）

你得到一个下标从 0 开始的二维整数数组 `tires`，其中 `tires[i] = [fi, ri]` 表示第 `i` 条轮胎（tire）在第 `x` 圈连续行驶时需要的时间为 `fi * ri^{(x-1)}` 秒。  

另给你一个整数 `changeTime` 和一个整数 `numLaps`。比赛共计 `numLaps` 圈，你可以任选一种轮胎作为起始轮胎。你拥有每种轮胎的无限供应，并且在每圈结束后，你可以选择更换为任意一种轮胎（包括仍使用当前类型的轮胎），更换过程需要等待 `changeTime` 秒。  

返回完成整场比赛的最小总时间。

---

#### 示例

**示例 1**

```
输入: tires = [[2,3],[3,4]], changeTime = 5, numLaps = 4
输出: 21
解释:
第 1 圈: 使用轮胎 0，耗时 2 秒。
第 2 圈: 继续使用轮胎 0，耗时 2 * 3 = 6 秒。
第 3 圈: 更换为新的轮胎 0，等待 5 秒，然后再用该轮胎完成本圈，耗时 2 秒。
第 4 圈: 继续使用轮胎 0，耗时 2 * 3 = 6 秒。
总时间 = 2 + 6 + 5 + 2 + 6 = 21 秒。
```

**示例 2**

```
输入: tires = [[1,10],[2,2],[3,4]], changeTime = 6, numLaps = 5
输出: 25
解释:
第 1 圈: 使用轮胎 1，耗时 2 秒。
第 2 圈: 继续使用轮胎 1，耗时 2 * 2 = 4 秒。
第 3 圈: 更换为新的轮胎 1，等待 6 秒，然后再用该轮胎完成本圈，耗时 2 秒。
第 4 圈: 继续使用轮胎 1，耗时 2 * 2 = 4 秒。
第 5 圈: 更换轮胎（具体更换哪种轮胎视最优方案而定），...
（后续过程省略，最终得到最小总时间 25 秒）
```

---

#### 约束

- `1 <= tires.length <= 10^5`
- `tires[i].length == 2`
- `1 <= fi, changeTime <= 10^5`
- `2 <= ri <= 10^5`
- `1 <= numLaps <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **模拟每一圈到底**，每走完一圈就决定是继续用当前轮胎还是换一条新轮胎。  
可以把赛道想象成一条跑道，手里有很多种轮胎（每种轮胎都有自己的“加速曲线”），我们每走一圈就要做出选择：

1. **继续用同一条轮胎**  
   - 第 x 圈的耗时 = `f_i * r_i^(x‑1)`（这里 `f_i`、`r_i` 来自 `tires[i]`）。  
   - 这就像在跑步时不换鞋子，鞋子越磨损，跑起来越慢。

2. **换轮胎**  
   - 需要先等 `changeTime` 秒换轮胎，然后再从第 1 圈的耗时 `f_i` 开始。  
   - 换轮胎相当于把鞋子换成全新的，跑起第一圈又快了。

因为我们可以**随意挑选**任意种轮胎，而且每种轮胎的数量是无限的，暴力做法就是：

- 对每一圈 **枚举** 所有可能的轮胎种类（`len(tires)` 种），  
- 对每一种轮胎决定是**继续**还是**换**，  
- 把所有选择的时间加起来，取最小值。

这其实是一个**深度优先搜索（DFS）**，把每一圈看成一层决策树，树的深度等于 `numLaps`，每层的分支数等于轮胎种类数 `|tires|`（加上换不换的二选一），所以总的搜索空间是指数级的。

> **为什么它是对的？**  
> 只要遍历了所有可能的决策序列（每一种换胎或不换的组合），必然能找到最小的总时间。只是不实际可行，因为会穷举出太多情况。

#### 代码（Python）

```python
from math import inf
from typing import List

def minimumFinishTime_bruteforce(tires: List[List[int]], changeTime: int, numLaps: int) -> int:
    n = len(tires)
    best = inf                                 # 用来保存全局最小时间

    # dfs(pos, cur_tire, cur_lap_on_this_tire, elapsed)
    # pos          : 已经完成的圈数
    # cur_tire     : 当前使用的轮胎编号
    # cur_lap_cnt  : 这条轮胎已经连续用了多少圈（从 1 开始计数）
    # elapsed      : 到目前为止已经耗费的时间
    def dfs(pos: int, cur_tire: int, cur_lap_cnt: int, elapsed: int):
        nonlocal best
        # 剪枝：如果已经超过当前最优解，就不必继续搜索
        if elapsed >= best:
            return
        # 所有圈都跑完了，更新答案
        if pos == numLaps:
            best = min(best, elapsed)
            return

        # 1. 继续用当前轮胎跑下一圈
        f, r = tires[cur_tire]
        next_time = f * (r ** (cur_lap_cnt - 1))   # 第 cur_lap_cnt 圈的耗时
        dfs(pos + 1, cur_tire, cur_lap_cnt + 1, elapsed + next_time)

        # 2. 换成任意一条新轮胎（包括换成和当前同种的轮胎）
        for new in range(n):
            f_new, _ = tires[new]
            # 换胎需要先花 changeTime 秒，再跑第 1 圈的时间 f_new
            dfs(pos + 1, new, 2, elapsed + changeTime + f_new)   # 这里把 cur_lap_cnt 设为 2，因为后面递归里会先算第 1 圈

    # 第 1 圈可以随意挑一条轮胎开始，不需要换胎时间
    for i in range(n):
        f, _ = tires[i]
        dfs(1, i, 2, f)   # 已跑 1 圈，cur_lap_cnt 为 2（下一圈如果继续用同胎就是第 2 圈）

    return best
```

> **关键行解释**  
> - `if elapsed >= best: return`  → **剪枝**：如果已经比目前找到的最优解慢，就直接回溯，省掉后面的搜索。  
> - `next_time = f * (r ** (cur_lap_cnt - 1))`  → 根据题目公式算出第 `cur_lap_cnt` 圈的时间。  
> - `for new in range(n):`  → 枚举所有可能的换胎选择（包括换成同种轮胎）。

#### 复杂度

- **时间复杂度**：`O(|tires| ^ numLaps)`（指数级）  
  解释：每跑完一圈我们都有 `|tires|` 种换胎选择（再加上“不换”这一条），所以搜索树的分支数是 `|tires| + 1`，深度是 `numLaps`，整体是指数增长。对初学者来说可以把 `O(2^n)` 想象成“每增加一圈，可能的方案翻倍”，所以很快就不可计算。

- **空间复杂度**：`O(numLaps)`（递归栈）  
  解释：递归调用的深度最多等于 `numLaps`，每层只保存常数个变量，所以占用的额外内存与圈数成线性关系。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **“不停换胎”** 和 **“连续使用同一胎跑多圈”** 两件事是交替出现的。  
真正的瓶颈在于 **枚举所有换胎时机**：每一圈都去尝试所有轮胎，导致指数级搜索。

要把它变快，需要把 **“在同一条轮胎上跑 k 圈的最短时间”** 预先算好，然后把整场比赛看成 **“把总圈数分成若干段，每段都用最优的单胎方案”**。这正是 **动态规划（DP）** 的典型模型：

1. **预计算**：  
   对每一种轮胎，计算它 **连续跑 1、2、…、k 圈的时间**（不换胎），直到出现两种情况之一：  
   - 时间已经大于 `changeTime + min_f`（换胎再跑一圈的时间），再继续跑下去只会更慢。  
   - 圈数超过 `numLaps`（没有必要跑更多）。  
   取所有轮胎在同一圈数 `k` 上的最小值，记为 `best[k]` —— “**只用一条轮胎跑 k 圈的最优时间**”。  
   这一步的复杂度是 `O(|tires| * K)`，其中 `K` 是我们实际需要枚举的最大连续圈数（后面会解释它很小，最多约 20）。

2. **动态规划**：  
   设 `dp[i]` 为跑完 **i 圈** 所需要的最少时间。  
   - 初始化 `dp[0] = 0`（跑零圈不花时间）。  
   - 对每个 `i`（1…numLaps），枚举本段最后一次 **不换胎** 能跑的圈数 `k`（1 ≤ k ≤ i 且 k ≤ K），则  
     ```
     dp[i] = min(dp[i], dp[i - k] + changeTime + best[k])
     ```
     这里 `dp[i - k]` 是前面已经跑好的时间，`changeTime` 是在第 `i - k` 圈后换胎的代价（如果 `i - k == 0`，即一开始就不需要换胎，直接省去这段 `changeTime`），`best[k]` 是本段用同一条轮胎跑 `k` 圈的最优时间。  
   - 取所有 `k` 的最小值即得到 `dp[i]`。

3. **为什么 `K`（连续跑的最大圈数）很小？**  
   - 对于任意轮胎，第 `x` 圈的耗时是 `f * r^{x-1}`，其中 `r ≥ 2`。  
   - 当 `f * r^{x-1}` 已经大于 `changeTime + min_f`（换胎再跑第一圈的时间）时，继续用同一条胎已经不划算了——此时我们宁愿换胎。  
   - 由于 `r` 至少是 2，指数增长非常快，`x` 在 **大约 20** 左右就会超过 `10^5`（题目上限），所以我们只需要考虑到 `K = 20`（实际代码中取 `min(numLaps, 20)` 即可）。

这样，时间复杂度从指数级降到了 **`O(|tires| * K + numLaps * K)`**，在本题的约束下（`|tires| ≤ 10^5`、`numLaps ≤ 1000`、`K ≤ 20`）完全可以跑完。

#### 代码（Python）

```python
from typing import List

def minimumFinishTime(tires: List[List[int]], changeTime: int, numLaps: int) -> int:
    """
    计算最短完成时间，核心思路：
    1. 预处理每条轮胎连续跑 k 圈的最小耗时（不换胎）。
    2. 用 DP 把总圈数拆分成若干段，每段使用上一步的最优单段时间。
    """
    # ---------- 1. 预处理单段最优时间 ----------
    # 对所有轮胎取最小的 “连续跑 k 圈” 的时间
    # 只需要考虑 k <= 20（或者 <= numLaps），因为后面再多就一定不划算
    max_k = min(numLaps, 20)          # 经验上 20 足够大
    best = [float('inf')] * (max_k + 1)   # best[k] = 用同一条轮胎跑 k 圈的最小时间，0 位置不用

    for f, r in tires:
        time = 0
        cur = f                      # 第 1 圈的时间
        for k in range(1, max_k + 1):
            time += cur               # 累加第 k 圈的时间
            best[k] = min(best[k], time)   # 取所有轮胎中最小的
            # 下一圈的时间会乘以 r
            cur *= r
            # 如果下一圈的时间已经比换胎再跑第一圈还慢，就可以提前退出循环
            if cur > changeTime + f:   # 换胎后再跑第一圈的时间 = changeTime + f
                break

    # ---------- 2. 动态规划 ----------
    dp = [float('inf')] * (numLaps + 1)
    dp[0] = 0                         # 0 圈不花时间

    for i in range(1, numLaps + 1):
        # 枚举本段使用同一条轮胎跑的圈数 k
        for k in range(1, min(i, max_k) + 1):
            # 前 i-k 圈的最优时间 + 换胎时间 + 本段的最优单段时间
            # 注意：如果 i-k == 0，说明本段是比赛的第一段，不需要额外的换胎时间
            cost = dp[i - k] + best[k] + (0 if i - k == 0 else changeTime)
            dp[i] = min(dp[i], cost)

    return dp[numLaps]
```

> **代码要点注释**  
> - `max_k = min(numLaps, 20)`  → 只预计算到 20 圈（或更少），因为再多就一定不划算。  
> - `cur *= r`  → 根据题目公式，连续第 `x` 圈的时间是 `f * r^{x-1}`，所以每跑完一圈就乘以 `r`。  
> - `if cur > changeTime + f: break`  → 当继续跑下一圈比“换胎再跑第一圈”更慢时，直接停止该轮胎的枚举，省掉无用计算。  
> - `dp[i - k] + best[k] + (0 if i - k == 0 else changeTime)`  → 把“前面已经跑好的时间 + 换胎代价（除非已经是第一段） + 本段最优时间”累加，取最小。

#### 复杂度

- **时间复杂度**：`O(|tires| * K + numLaps * K)`，其中 `K = min(numLaps, 20)`。  
  - 解释：第一步遍历所有轮胎，每条轮胎最多循环 `K` 次（`K` 很小），第二步 DP 对每个 `i`（最多 1000）再循环 `K` 次，所以整体是线性可接受的。对比暴力的指数级，这里可以把 `O(n²)` 想成“即使最坏也只要几千次运算”，非常快。

- **空间复杂度**：`O(numLaps + K)`。  
  - `best` 数组需要 `K`（≈20）空间，`dp` 需要 `numLaps + 1`（最多 1001）空间，都是线性级别，几乎不占内存。

---

## 心得

- **核心技巧**：  
  先**预处理**“单条轮胎连续跑 k 圈的最短时间”，再用**动态规划**把整个赛程拆分成若干段，每段使用上述预处理的最优单段时间。

- **该技巧适用的题型**（类似思路）  
  1. **分段最小成本**：如“买酒瓶子最少费用”或“分段回文最小切割”。  
  2. **限制次数的最短路径**：如“限制换乘次数的最短路线”。  
  3. **子序列/子数组的最优分割**：如“把数组分成若干子数组，使每段代价最小”。

- **一句话总结解题钥匙**：  
  *把“连续使用同一资源的代价”提前算好，然后用 DP 把全局问题拆成若干个最优的局部段落。*

---

## 反思

- **第一反应**：  
  “把每一圈都枚举所有轮胎，直接递归搜索”。这自然会想到暴力 DFS，但很快会发现 `numLaps` 达到 1000 时根本跑不完。

- **最容易踩的坑**  
  1. **无限循环**：`r` 的指数增长如果不设上限，会导致 `cur` 变得非常大，甚至溢出。需要在预处理时提前 `break`。  
  2. **换胎时间的处理**：第一段不需要 `changeTime`，而后面的每段都要加上，否则会多算一次。  
  3. **K 的取值**：若随意设成 `numLaps`（可能是 1000），预处理会变成 `O(|tires| * numLaps)`，在 `tires` 达到 10⁵ 时会超时。认识到指数增长的 “自然上限” 很关键。

- **下次遇到同类题的第一步**：  
  “先问自己：‘有没有一种子结构（比如连续跑几圈）在不变动状态时可以预先算好？’”。如果答案是肯定的，就先做预处理，再用 DP 把全局问题拼接起来。这样可以把指数级的枚举压缩成线性或准线性时间。