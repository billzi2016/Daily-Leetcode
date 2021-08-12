# #1434. 不同帽子佩戴方式的计数 / Number of Ways to Wear Different Hats to Each Other

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-wear-different-hats-to-each-other/)

---

## 题目（英文原版）

**Description**

There are n people and 40 types of hats labeled from 1 to 40.
Given a 2D integer array hats, where hats[i] is a list of all hats preferred by the ith person.
Return the number of ways that n people can wear different hats from each other.
Since the answer may be too large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: hats = [[3,4],[4,5],[5]]
Output: 1
Explanation: There is only one way to choose hats given the conditions. 
First person choose hat 3, Second person choose hat 4 and last one hat 5.
```

**Example 2:**

```
Input: hats = [[3,5,1],[3,5]]
Output: 4
Explanation: There are 4 ways to choose hats:
(3,5), (5,3), (1,3) and (1,5)
```

**Example 3:**

```
Input: hats = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
Output: 24
Explanation: Each person can choose hats labeled from 1 to 4.
Number of Permutations of (1,2,3,4) = 24.
```

**Constraints**

- n == hats.length
- 1 <= n <= 10
- 1 <= hats[i].length <= 40
- 1 <= hats[i][j] <= 40
- hats[i] contains a list of unique integers.

---

## 题目（中文翻译）

**描述**  
有 `n` 个人和 `40` 种帽子，编号从 `1` 到 `40`。  
给定一个二维整数数组（2D integer array）`hats`，其中 `hats[i]` 是第 `i` 个人喜欢的所有帽子编号的列表。  
返回 `n` 个人在彼此之间佩戴不同帽子的方式数。  
由于答案可能非常大，请返回对 `10^9 + 7` 取模后的结果。

**示例**

**示例 1**  
```
Input: hats = [[3,4],[4,5],[5]]
Output: 1
Explanation: 只存在唯一一种满足条件的帽子分配方式。  
第一个人选择帽子 3，第二个人选择帽子 4，第三个人选择帽子 5。
```

**示例 2**  
```
Input: hats = [[3,5,1],[3,5]]
Output: 4
Explanation: 有 4 种可行的帽子分配方式：  
(3,5), (5,3), (1,3) 和 (1,5)。
```

**示例 3**  
```
Input: hats = [[1,2,3,4],[1,2,3,4],[1,2,3,4],[1,2,3,4]]
Output: 24
Explanation: 每个人都可以选择编号为 1~4 的帽子。  
排列 (1,2,3,4) 的全排列数为 24。
```

**约束条件**  
- `n == hats.length`  
- `1 <= n <= 10`  
- `1 <= hats[i].length <= 40`  
- `1 <= hats[i][j] <= 40`  
- `hats[i]` 中的整数互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每个人的帽子选择看成一次“分配”。  
我们可以把 **每个人** 当成一个小朋友，**每顶帽子** 当成一种颜色的衣服。  
把所有人排成一列，从左到右依次给他们挑选一顶自己喜欢且还没有被别人穿过的帽子。

实现上可以使用递归（回溯）：

1. 先给第 `i` 个人挑选帽子。  
2. 遍历 `hats[i]`（第 `i` 个人喜欢的帽子列表），如果这顶帽子还没有被其他人使用，就把它标记为“已用”，递归处理下一个人。  
3. 当所有人都挑完（`i == n`）时，找到一种合法的分配方式，计数+1。  

> **哈希表**（或 Python 的 `set`）在这里就像一本“帽子使用登记册”，  
> `key` 是帽子编号，`value`（这里用 `True/False`）表示这顶帽子是否已经被别人穿上。

只要每一步都严格检查“帽子未被占用”，所有枚举出来的方案一定合法，因而答案是 **所有合法分配的数量**。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7

def numberWays_bruteforce(hats: List[List[int]]) -> int:
    n = len(hats)                     # 人数，最多 10
    used = set()                      # 已经被占用的帽子编号
    ans = 0

    def backtrack(i: int):
        """尝试为第 i 个人挑选帽子"""
        nonlocal ans
        if i == n:                    # 所有人都挑完了
            ans = (ans + 1) % MOD
            return

        for hat in hats[i]:           # 遍历第 i 个人喜欢的每顶帽子
            if hat not in used:       # 这顶帽子还没被别人穿
                used.add(hat)         # 标记为已用
                backtrack(i + 1)      # 递归处理下一个人
                used.remove(hat)      # 回溯，撤销选择

    backtrack(0)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(k^n)`（`k` 为每个人可能的帽子数，最坏情况 `k = 40`，`n ≤ 10`）。  
  这相当于“每个人都有 40 种选择”，所以总共要尝试 `40 × 40 × … × 40 = 40ⁿ` 种情况，指数级增长，实际会超时。

- **空间复杂度**：`O(n)`，递归栈深度最多 `n`（≤10），以及一个存放已使用帽子的集合，大小也不超过 `n`。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **“每个人一次挑选”** 的顺序导致大量重复计算。  
例如，两个人都喜欢帽子 1 和 2，暴力递归会分别枚举 `(1,2)` 与 `(2,1)` 两次，且在更大规模时会出现大量相同子状态的重复遍历。

我们可以 **把视角翻转**：  
> **从帽子出发**，决定每顶帽子要送给谁（如果送的话），而不是从人出发决定穿哪顶帽子。

这样可以用 **位掩码（bitmask）** 记录已经拥有帽子的人：

- 用一个整数 `mask` 的二进制位表示 10 个人的状态。  
  - 第 `i` 位为 `1` → 第 `i` 个人已经拿到帽子。  
  - 第 `i` 位为 `0` → 仍然没有帽子。

- `dp[mask]` 表示 **在已经考虑完若干顶帽子后**，当前状态为 `mask` 的分配方案数。

处理顺序：

1. 初始化 `dp[0] = 1`（还没分配任何帽子，唯一一种空方案）。  
2. 依次遍历帽子编号 `h = 1 … 40`。  
   对每顶帽子 `h`，遍历所有可能的 `mask`（从大到小遍历是为了防止本轮更新时使用了已经加入本轮的状态），
   对于每个 `mask`，尝试把帽子 `h` 送给尚未拥有帽子且 **喜欢这顶帽子** 的人 `p`：
   - 新的状态 `new_mask = mask | (1 << p)`。  
   - `dp[new_mask] += dp[mask]`（模 `10⁹+7`）。

3. 最后答案是 `dp[(1 << n) - 1]`，即所有 `n` 个人都已经拿到帽子的状态。

> **为什么这样是对的？**  
> 我们把每顶帽子看成“是否使用”，而不是“谁先挑”。  
> 当处理第 `h` 顶帽子时，所有之前的帽子已经决定了哪些人已经拿到帽子，`mask` 正好记录了这些信息。  
> 把当前帽子分配给一个新的人，只会把 `mask` 的对应位从 `0` 变成 `1`，不会影响已经确定的分配，保证了合法性且不重复计数。

#### 代码（Python）

```python
from typing import List

MOD = 10**9 + 7
MAX_HAT = 40

def numberWays(hats: List[List[int]]) -> int:
    n = len(hats)                     # 人数，≤10
    full_mask = (1 << n) - 1          # 所有人的位全是1

    # 为每顶帽子建立“喜欢它的人”列表，方便遍历
    hat_to_people = [[] for _ in range(MAX_HAT + 1)]   # 1~40
    for person, hat_list in enumerate(hats):
        for h in hat_list:
            hat_to_people[h].append(person)

    # dp[mask] = 目前已经处理完若干帽子后，mask 状态的方案数
    dp = [0] * (1 << n)
    dp[0] = 1                         # 空分配，唯一方案

    # 依次考虑每顶帽子
    for h in range(1, MAX_HAT + 1):
        # 复制一份旧的 dp，防止在同一轮里使用已经更新的值
        old = dp[:]                  # 只读的上一轮结果
        # 对每个状态尝试把帽子 h 分配给还没有帽子且喜欢它的人
        for mask in range(1 << n):
            if old[mask] == 0:       # 这个状态本轮没有来源，跳过
                continue
            for p in hat_to_people[h]:
                if not (mask >> p) & 1:          # 人 p 还没拿帽子
                    new_mask = mask | (1 << p)   # 把 p 标记为已拿帽子
                    dp[new_mask] = (dp[new_mask] + old[mask]) % MOD

    return dp[full_mask]
```

> **代码要点解释**  
> - `hat_to_people[h]` 就像一本“帽子使用手册”，告诉我们“第 h 顶帽子有哪些潜在的佩戴者”。  
> - `old = dp[:]` 相当于把“昨天的登记册”复印一份，今天只在这份复印本上做增删，防止同一顶帽子被同一个人“抢两次”。  
> - `mask >> p & 1` 检查第 `p` 位是否已经是 `1`（已经有帽子），如果是 `0` 才可以把当前帽子分配给他。  

#### 复杂度

- **时间复杂度**：`O(40 * 2^n * n)`  
  - `40` 是帽子种类上限。  
  - `2^n`（最多 `2^10 = 1024`）是所有可能的状态数。  
  - 对每个状态我们最多遍历 `n`（≤10）个人。  
  整体约 `40 * 1024 * 10 ≈ 4×10⁵` 次操作，轻松跑完。

- **空间复杂度**：`O(2^n)`  
  只需要保存一个长度为 `2^n` 的数组 `dp`，约 1024 个整数，几乎不占内存。

与暴力解相比，时间从指数级（`40ⁿ`）降到了 **线性乘以 2 的 n 次方**，在 n≤10 的范围内非常高效。

---

## 心得

- **核心技巧**：**位掩码 + 动态规划**，把“谁已经分配”压缩到一个整数里，避免显式枚举所有人‑帽子配对的组合。
- **适用场景**  
  1. “每个人只能选一种资源，且资源不能重复” 类似的匹配问题（如《分配工作岗位》《分配礼物》）。  
  2. “状态只和人数有关，人数 ≤ 20” 的子集 DP（如《分割数字》《分配任务》）。  
  3. 需要遍历 **有限种类**（如 40 种帽子）而不是 **每个人的选择** 时，倒着遍历资源往状态表里填充效果更好。
- **一句话总结**：**把“人”换成“帽子”来遍历，用位掩码记录已分配的人，就能把指数爆炸的暴力枚举压缩到几百毫秒。**

---

## 反思

- **第一反应**：看到“每个人只能穿不同的帽子”，第一时间会想到回溯枚举所有分配方式。  
- **最容易踩的坑**  
  - 忘记对答案取模 `10⁹+7`，导致整数溢出。  
  - 只遍历了 **已有的** `mask` 而没有保留上一轮的状态，导致同一顶帽子被同一个人多次使用（计数错误）。  
  - 边界条件：当 `n=0`（虽然题目不允许）或某个人的喜欢列表为空时，需要返回 0。  
- **下次类似题的第一步**：先问自己 “资源的种类是否比人数少？” 如果是，就考虑 **按资源遍历 + 位掩码 DP**；否则可以考虑 **按人遍历 + 记忆化搜索**。这样可以快速定位最合适的状态转移方向。