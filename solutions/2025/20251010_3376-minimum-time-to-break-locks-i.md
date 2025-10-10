# #3376. 破锁的最小时间 I / Minimum Time to Break Locks I

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Depth-First Search、Bitmask · [LeetCode 链接](https://leetcode.com/problems/minimum-time-to-break-locks-i/)

---

## 题目（英文原版）

**Description**

Bob is stuck in a dungeon and must break n locks, each requiring some amount of energy to break. The required energy for each lock is stored in an array called strength where strength[i] indicates the energy needed to break the ith lock.
To break a lock, Bob uses a sword with the following characteristics:
Your task is to determine the minimum time in minutes required for Bob to break all n locks and escape the dungeon.
Return the minimum time required for Bob to break all n locks.

**Examples**

**Example 1:**

```
Input: strength = [3,4,1], k = 1
Output: 4
Explanation:
The locks cannot be broken in less than 4 minutes; thus, the answer is 4.
```

**Example 2:**

```
Input: strength = [2,5,4], k = 2
Output: 5
Explanation:
The locks cannot be broken in less than 5 minutes; thus, the answer is 5.
```

**Constraints**

- n == strength.length
- 1 <= n <= 8
- 1 <= K <= 10
- 1 <= strength[i] <= 106

---

## 题目（中文翻译）

Bob 被困在一个地下城中，需要破开 `n` 把锁，每把锁都需要一定的能量才能打开。每把锁所需的能量存放在数组 `strength` 中，其中 `strength[i]` 表示第 `i` 把锁需要的能量。  
Bob 使用一把具有以下特性的剑来破锁：

（题目原文中未给出剑的具体特性，此处保持原样）

你的任务是计算 Bob 破开所有 `n` 把锁并逃离地下城所需的最少时间（单位：分钟），并返回该最小时间。

**示例 1**  
**输入**: `strength = [3,4,1]`, `k = 1`  
**输出**: `4`  
**解释**:  
锁在不到 4 分钟的时间内无法全部破开，因此答案为 4。

**示例 2**  
**输入**: `strength = [2,5,4]`, `k = 2`  
**输出**: `5`  
**解释**:  
锁在不到 5 分钟的时间内无法全部破开，因此答案为 5。

**约束条件**  
- `n == strength.length`  
- `1 <= n <= 8`  
- `1 <= k <= 10`  
- `1 <= strength[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题的核心在于 **“先后顺序”** 会影响总耗时。  
我们可以把每一次 “把若干把锁一次性打开” 当作一次 **操作**，  
- 这一次操作里我们可以选 **至多 `k` 把** 还没有打开的锁一起打开  
- 这一次操作需要的时间等于 **被选锁中强度最大的那把**（因为最强的那把决定了这一步最久要等多久）

> **类比**：把锁想成不同重量的箱子，你一次只能搬走不超过 `k` 个箱子，搬走这批箱子需要的时间就是最重箱子的重量。  

把所有锁全部打开，就相当于把 `strength` 数组划分成若干 **不相交的子集**（每个子集大小 ≤ `k`），
每个子集的代价是子集里最大元素，所有子集代价之和即为总耗时。  

因为 `n ≤ 8`，我们可以**枚举所有可能的打开顺序**（即所有排列），
对每一种顺序模拟把锁分批的过程，取最小的耗时即为答案。

- **正确性**：遍历了所有可能的打开顺序，必然会覆盖最优的那一种；  
 对每一种顺序，按照题目要求把锁分批（每批 ≤ `k`），代价计算方式也完全符合题意，故得到的最小值一定是全局最优。

- **时间/空间复杂度**  
  - 枚举所有排列需要 `n!` 次（`n` 最多 8，8! = 40320，完全可以接受）  
  - 对每个排列我们线性扫描一次数组，计算分批的最大值，时间 `O(n)`  
  - 所以总体时间 **`O(n!·n)`**，在最坏情况下约 `3·10⁵` 次基本运算，运行毫秒级。  
  - 只用了几个整数变量，空间 **`O(1)`**。

#### 代码（Python）

```python
from itertools import permutations
from typing import List

def minTime_bruteforce(strength: List[int], k: int) -> int:
    """
    暴力枚举所有打开顺序，计算每种顺序的总耗时，返回最小值。
    """
    n = len(strength)
    best = float('inf')                     # 当前找到的最小时间

    # 遍历所有可能的打开顺序（全排列）
    for order in permutations(range(n)):
        total = 0                            # 累计当前顺序的总耗时
        i = 0
        # 按顺序把锁分批，每批至多 k 把
        while i < n:
            # 这一次操作要打开的锁的下标集合
            batch = order[i: i + k]          # 取出最多 k 把
            # 这批锁中强度最大的决定本批耗时
            batch_max = max(strength[idx] for idx in batch)
            total += batch_max               # 累加到总时间
            i += k                           # 移动到下一批
        best = min(best, total)             # 取全局最小

    return best
```

> **关键行注释**  
> - `permutations(range(n))`：生成所有锁的打开顺序。  
> - `batch = order[i: i + k]`：一次最多挑 `k` 把锁。  
> - `batch_max = max(strength[idx] for idx in batch)`：本批所需的时间就是最强锁的强度。  

#### 复杂度

- **时间复杂度**：`O(n!·n)`  
  - `n!`：枚举所有排列。  
  - `n`：对每个排列线性扫描一次，计算每批最大值。  
  - **含义**：对 8 把锁最多要检查 40320 种顺序，每种顺序最多遍历 8 次，完全可以在毫秒级跑完。

- **空间复杂度**：`O(1)`  
  - 只用了常数个额外变量（`best、total、i`），不随 `n` 增长。  

---

### 2. 最优解

暴力解已经能在题目给出的约束下 AC，但它的核心思想（把锁划分成若干批，每批代价为最大强度）可以用 **状态压缩 DP（子集 DP）** 来直接求最小值，省去枚举全部排列的过程。  
这种写法在 `n` 更大时依然可用（比如 `n ≤ 15`），而且思路更清晰。

#### 思路  

我们用一个 **位掩码** `mask` 表示已经打开的锁的集合：

- 第 `i` 位为 `1` → 第 `i` 把锁已经打开  
- 第 `i` 位为 `0` → 第 `i` 把锁还未打开  

`dp[mask]` = **打开 `mask` 所表示的锁后，已花费的最少时间**。

状态转移：

1. 从当前状态 `mask` 出发，任选一个 **未打开的子集 `sub`**（`sub` 与 `mask` 不交），且 `sub` 的大小不超过 `k`。  
2. 把这批 `sub` 同时打开需要的时间是 `max(strength[i] for i in sub)`。  
3. 新的状态是 `mask | sub`，费用更新为  

   ```
   dp[mask | sub] = min(dp[mask | sub],
                        dp[mask] + max_strength_of_sub)
   ```

初始状态 `dp[0] = 0`（什么都没打开，耗时 0），目标状态是 `mask = (1<<n) - 1`（全部打开）。

因为 `n ≤ 8`，所有子集的数量是 `2^n ≤ 256`，遍历每个状态的子集也在可接受范围。  
我们可以 **预先枚举所有合法的子集**（大小 ≤ `k`），把它们及对应的最大强度保存下来，转移时直接使用。

> **为什么比暴力更快？**  
> 暴力要枚举 `n!` 种顺序，而 DP 只遍历 `2^n` 个状态，每个状态最多检查 `C(n, k)` 个子集，数量级从阶乘下降到指数，尤其当 `n` 增大时优势明显。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def minTime_dp(strength: List[int], k: int) -> int:
    """
    状态压缩 DP（子集 DP），时间复杂度 O(3^n) 在 n<=8 时非常快。
    """
    n = len(strength)
    full_mask = (1 << n) - 1               # 所有锁都打开时的掩码

    # 预处理：所有合法子集（大小 <= k）以及它们的最大强度
    subsets = []                           # 每个元素是 (mask_of_subset, max_strength)
    for sz in range(1, k + 1):             # 子集大小从 1 到 k
        for combo in combinations(range(n), sz):
            mask = 0
            mx = 0
            for idx in combo:
                mask |= 1 << idx
                mx = max(mx, strength[idx])
            subsets.append((mask, mx))

    # DP 表，大小为 2^n，初始为无限大
    INF = 10 ** 18
    dp = [INF] * (1 << n)
    dp[0] = 0                              # 什么都没打开，耗时 0

    # 按掩码从小到大遍历
    for mask in range(1 << n):
        if dp[mask] == INF:                # 不可达状态直接跳过
            continue
        # 尝试把任意合法子集加入当前状态
        for sub_mask, cost in subsets:
            if mask & sub_mask:            # 已经打开的锁不能再选
                continue
            new_mask = mask | sub_mask
            # 更新新状态的最小耗时
            if dp[new_mask] > dp[mask] + cost:
                dp[new_mask] = dp[mask] + cost

    return dp[full_mask]
```

> **关键行注释**  
> - `subsets`：提前把所有“本轮可以一次性打开的锁组合”算好，省去每次 DP 转移时的枚举开销。  
> - `if mask & sub_mask:`：确保本轮选的锁没有被打开过。  
> - `dp[new_mask] = min(dp[new_mask], dp[mask] + cost)`：状态转移的核心公式。  

#### 复杂度

- **时间复杂度**：`O(3^n)`（严格来说是 `O(2^n * Σ_{i=1}^k C(n,i))`，在 `n ≤ 8` 时约等于 `3^n`）  
  - `2^n` 个状态。  
  - 对每个状态遍历所有合法子集，子集总数不超过 `∑_{i=1}^{k} C(n,i) ≤ 2^n`。  
  - 因此总体在几千到几万次运算之内，远快于 `n!`。

- **空间复杂度**：`O(2^n)` 用于保存 DP 表，`n=8` 时仅 256 个整数，几乎可以忽略。

---

## 心得

- **核心技巧**：把“把若干把锁一次性打开”抽象成 **“选一个子集，代价为子集最大元素”**，然后在 **子集 DP** 中求最小划分。  
- **适用场景**：  
  1. **分批处理**，每批大小受限，批次代价取最大/最小/和等（如“分配任务到机器”“装箱”）。  
  2. **状态压缩 DP** 中常见的“每次可以选若干未完成的任务”类问题。  
  3. **位运算+枚举子集** 的技巧在 n ≤ 20（甚至 25）时也很常用。  

> **一句话总结**：把所有锁划分成若干 “一次性打开的批次”，每批代价是最强锁的强度，用子集 DP 求最小批次数之和。

---

## 反思

- **第一反应**：看到 “n ≤ 8、要求最小时间、每次可以打开 ≤ k 把锁”，立刻想到 **枚举所有顺序**（暴力）或 **背包/DP**。  
- **最容易踩的坑**：  
  - **子集大小限制**：忘记在 DP 转移时排除子集大小超过 `k` 的情况，会得到错误的更小答案。  
  - **位运算错误**：`mask & sub_mask` 判断是否有交集时，容易写成 `mask & sub_mask == 0`（需要加括号）导致逻辑错误。  
  - **初始化**：DP 表必须用一个足够大的“无穷大”初始化，防止未更新的状态误参与最小值比较。  

- **下次思路**：遇到“每次可以选若干未完成的元素并产生一定代价”这类题目，第一步就想到 **子集 DP**（状态压缩）或 **背包 DP**，再根据 `n` 的大小决定是直接枚举全部排列还是走 DP。  

---