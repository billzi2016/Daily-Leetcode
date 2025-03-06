# #3096. 获得更多积分所需的最少关卡数 / Minimum Levels to Gain More Points

> 难度：中等 · 标签：Array、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/minimum-levels-to-gain-more-points/)

---

## 题目（英文原版）

**Description**

You are given a binary array possible of length n.
Alice and Bob are playing a game that consists of n levels. Some of the levels in the game are impossible to clear while others can always be cleared. In particular, if possible[i] == 0, then the ith level is impossible to clear for both the players. A player gains 1 point on clearing a level and loses 1 point if the player fails to clear it.
At the start of the game, Alice will play some levels in the given order starting from the 0th level, after which Bob will play for the rest of the levels.
Alice wants to know the minimum number of levels she should play to gain more points than Bob, if both players play optimally to maximize their points.
Return the minimum number of levels Alice should play to gain more points. If this is not possible, return -1.
Note that each player must play at least 1 level.

**Examples**

**Example 1:**

```
Input: possible = [1,0,1,0]
Output: 1
Explanation:
Let's look at all the levels that Alice can play up to:
Alice must play a minimum of 1 level to gain more points.
```

**Example 2:**

```
Input: possible = [1,1,1,1,1]
Output: 3
Explanation:
Let's look at all the levels that Alice can play up to:
Alice must play a minimum of 3 levels to gain more points.
```

**Example 3:**

```
Input: possible = [0,0]
Output: -1
Explanation:
The only possible way is for both players to play 1 level each. Alice plays level 0 and loses 1 point. Bob plays level 1 and loses 1 point. As both players have equal points, Alice can't gain more points than Bob.
```

**Constraints**

- 2 <= n == possible.length <= 105
- possible[i] is either 0 or 1.

---

## 题目（中文翻译）

你得到一个长度为 `n` 的二进制数组 `possible`。  
Alice 和 Bob 正在玩一个包含 `n` 关卡的游戏。某些关卡不可通关，而其他关卡总是可以通关。具体地，若 `possible[i] == 0`，则第 `i` 关对两位玩家均不可通关。玩家通关一关得 **1 分**，未通关则扣 **1 分**。  

游戏开始时，Alice 按顺序从第 `0` 关开始依次玩若干关卡，随后 Bob 接着玩剩余的关卡。每位玩家至少必须玩 **1** 关。两位玩家都会**最优**（optimal）地选择自己的玩法以使得自己的得分最大化。  

求 Alice 为了使自己的总得分**严格高于** Bob 的总得分，最少需要玩多少关卡。如果无论如何都无法实现，则返回 `-1`。  

**示例 1**  
输入: `possible = [1,0,1,0]`  
输出: `1`  
解释:  
我们枚举 Alice 可以玩到的所有关卡数：  
- 当 Alice 只玩第 0 关时，她通关得到 **+1 分**，Bob 只能从第 1 关开始玩，最多得到 **0 分**（第 1 关不可通关，后面两关各得 **+1**、**-1**，但 Bob 必须至少玩一关），此时 Alice 的分数严格大于 Bob。  
因此 Alice 至少需要玩 **1** 关。

**示例 2**  
输入: `possible = [1,1,1,1,1]`  
输出: `3`  
解释:  
枚举 Alice 可以玩到的关卡数：  
- 当 Alice 只玩 1、2、或 3 关时，她的得分分别为 `+1、+2、+3`，而 Bob 至少需要玩剩余的关卡数，最高也只能得到 `+2、+1、0`，因此只有在 Alice 玩 **3** 关时，她的得分才能严格超过 Bob。  

**示例 3**  
输入: `possible = [0,0]`  
输出: `-1`  
解释:  
唯一可行的分配是两位玩家各玩 1 关。Alice 玩第 0 关会失去 **1 分**，Bob 玩第 1 关也会失去 **1 分**。两人得分相等，Alice 无法取得更高的分数，所以返回 `-1`。  

**约束条件**  
- `2 <= n == possible.length <= 10^5`  
- `possible[i]` 只能是 `0` 或 `1`。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把题目中的 “能通关得 1 分，不能通关扣 1 分” 用一个整数数组 **score** 来表示：

* `possible[i] == 1` → `score[i] = +1`（相当于字典里查到 “好” 的词条，得到正分）  
* `possible[i] == 0` → `score[i] = -1`（相当于查到 “坏” 的词条，得到负分）  

现在 Alice 必须从左到右选 **一个非空前缀**（长度记作 `k`），Bob 接着玩剩下的 `n‑k` 关。  
两个人的得分分别是：

```
Alice  = sum(score[0 .. k-1])
Bob    = sum(score[k .. n-1])
```

Alice 想要 **得分严格大于 Bob**，于是我们可以把所有可能的 `k`（从 1 到 n‑1）枚举一遍，逐个计算这两个和，看看有没有满足条件的最小 `k`。

> **为什么这样一定能得到答案？**  
> 因为题目没有任何“策略”可选，玩家只能按照给定的数组获得固定的 +1 / -1 分。只要遍历所有合法的切分点，就一定会找到最小的满足条件的 `k`（如果存在的话）。

**时间/空间复杂度**  
* **时间**：对每个 `k` 都要重新求一次前缀和和后缀和，最坏情况是 `k = 1,2,…,n-1`，每次都要遍历 O(n) 的元素 → **O(n²)**。  
  *大白话*：如果数组有 10,000 个元素，暴力会大概算 10,000 × 10,000 = 1 亿次，加法运算，跑起来会很慢。  
* **空间**：只需要保存原数组和几个计数器 → **O(1)**。

#### 代码（Python）

```python
def minLevels_bruteforce(possible):
    # 把 0 → -1，1 → +1，便于后面直接相加
    score = [1 if x == 1 else -1 for x in possible]
    n = len(score)

    # 枚举所有合法的前缀长度 k（1 ≤ k ≤ n-1）
    for k in range(1, n):          # Alice 必须至少玩 1 关，Bob 也要至少 1 关
        alice = sum(score[:k])     # 前 k 项的和
        bob   = sum(score[k:])     # 剩余的和
        if alice > bob:            # Alice 分数严格大于 Bob
            return k               # 找到最小的 k，直接返回
    return -1                       # 没有满足条件的划分
```

#### 复杂度  

* **时间复杂度**：`O(n²)`  
  *解释*：外层循环 `n‑1` 次，内层的 `sum` 每次最坏遍历 `n` 次。  
* **空间复杂度**：`O(1)`（不计输入数组本身）  
  *解释*：只用了常数个额外变量。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**重复求前缀和和后缀和是性能瓶颈**。  
我们只需要 **一次遍历** 就能知道每个前缀的累计得分，从而直接比较 Alice 与 Bob 的得分。

设  

* `a[i] = +1`（若 `possible[i]==1`）或 `-1`（若 `possible[i]==0`）  
* `S = sum_{i=0}^{n-1} a[i]` 为全部关卡的总得分  
* `P_k = sum_{i=0}^{k-1} a[i]` 为 Alice 前 `k` 关的累计得分（即前缀和）  

Bob 的得分 = `S - P_k`（因为总分减去 Alice 已经拿到的就是 Bob 的）。  
Alice 想要 `P_k > S - P_k` → 两边同乘 2（避免出现小数）：

```
2 * P_k > S
```

因此，只要在一次遍历中维护 `P_k`，每次检查 `2*P_k > S` 并且 `k < n`（保证 Bob 至少还有一关），第一个满足条件的 `k` 就是答案。

> **核心技巧**：前缀和 + 只比较一次的线性扫描。  
> 类比：想象把所有关卡的得分写在一张纸上，然后从左往右累加“分数条”。只要这条分数条已经超过了剩下那段的两倍（因为我们把比较式子乘了 2），就说明 Alice 已经赢了。

**为什么只需要 O(n)？**  
* 计算总和 `S` 只遍历一次。  
* 再遍历一次累计前缀和 `P_k`，每一步的比较都是 O(1)。  
* 整体只是两次线性扫描 → **O(n)**。

#### 代码（Python）

```python
def minLevels(possible):
    """
    返回 Alice 必须最少玩多少关才能得分严格大于 Bob。
    若不存在这样的划分，返回 -1。
    """
    # 1. 把 0 变成 -1，1 保持为 +1
    a = [1 if x == 1 else -1 for x in possible]
    n = len(a)

    # 2. 计算全部关卡的总得分 S
    total = sum(a)                # O(n)

    # 3. 逐步累计前缀和 P_k，检查 2*P_k > total
    prefix = 0
    for i, val in enumerate(a):
        prefix += val             # 前 i+1 关的得分，即 P_{i+1}
        k = i + 1                 # Alice 已经玩了 k 关
        # 必须保证 Bob 还有至少一关（k < n）
        if k < n and 2 * prefix > total:
            return k              # 找到最小的合法 k
    return -1                     # 没有任何前缀满足条件
```

> **代码要点注释**  
> * `a` 的构造相当于把 “0 → -1” 的提示直接写进代码。  
> * `total` 是一次性算好的，总分不变。  
> * `prefix` 在循环里“滚动”，每次只加当前关卡的分数，省掉了重复求和。  
> * 条件 `k < n` 确保 Bob 至少玩一关。  

#### 复杂度  

* **时间复杂度**：`O(n)`  
  *解释*：一次遍历求总分，一次遍历累计前缀和，都是线性规模。  
* **空间复杂度**：`O(1)`（不计输入数组本身）  
  *解释*：只用了几个整数变量 `a`（可以原地改写），`total`，`prefix`，`k`。

---

## 心得  

* **核心技巧**：把二元数组映射成 `+1 / -1`，利用 **前缀和** 与 **总和的比较**（`2*prefix > total`）一次遍历求解。  
* **适用场景**  
  1. “找最短前缀，使其和大于剩余部分” 类似题目，如 *Maximum Length of Subarray With Positive Sum*。  
  2. “前缀和大于某阈值” 的划分问题，例如 *Split Array Largest Sum* 的简化版。  
  3. 任何需要比较前缀与后缀总和的情形，都可以把比较式子移项成 `2*prefix > total` 来快速判断。  

* **一句话总结**：把每关的得分映射为 `+1 / -1`，只要前缀累计得分超过整体的一半，Alice 就赢了——一次线性扫描即可找出最小的前缀长度。

---

## 反思  

* **第一反应**：把 0 当成 “负分” 直接改成 -1，随后想到要比较前缀与后缀的总分。  
* **最容易踩的坑**  
  * **边界**：两位玩家都必须至少玩一关，`k` 不能等于 `n`（否则 Bob 没关卡）。  
  * **整数比较**：直接使用 `prefix > total - prefix` 会涉及两次减法，容易写错；使用 `2*prefix > total` 更安全且避免浮点数。  
  * **全部 0 或全部 1**：如果所有关卡都是 -1，`total` 为负数，前缀和永远不可能大于后缀和，程序应返回 `-1`。  
* **下次类似题的第一步**：  
  1. 把题目中的 “得分 +1 / -1” 明确为 **数值化**（+1 / -1）。  
  2. 计算 **整体总和**，然后思考 **前缀和与后缀和的关系**，把不等式化为只涉及前缀和的形式。  
  3. 用一次遍历维护前缀和并实时检查条件。