# #2660. 确定保龄球游戏的获胜者 / Determine the Winner of a Bowling Game

> 难度：简单 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/determine-the-winner-of-a-bowling-game/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed integer arrays player1 and player2, representing the number of pins that player 1 and player 2 hit in a bowling game, respectively.
The bowling game consists of n turns, and the number of pins in each turn is exactly 10.
Assume a player hits xi pins in the ith turn. The value of the ith turn for the player is:
The score of the player is the sum of the values of their n turns.
Return

**Examples**

**Example 1:**

```
Input: player1 = [5,10,3,2], player2 = [6,5,7,3]
Output: 1
Explanation:
The score of player 1 is 5 + 10 + 2*3 + 2*2 = 25.
The score of player 2 is 6 + 5 + 7 + 3 = 21.
```

**Example 2:**

```
Input: player1 = [3,5,7,6], player2 = [8,10,10,2]
Output: 2
Explanation:
The score of player 1 is 3 + 5 + 7 + 6 = 21.
The score of player 2 is 8 + 10 + 2*10 + 2*2 = 42.
```

**Example 3:**

```
Input: player1 = [2,3], player2 = [4,1]
Output: 0
Explanation:
The score of player1 is 2 + 3 = 5.
The score of player2 is 4 + 1 = 5.
```

**Example 4:**

```
Input: player1 = [1,1,1,10,10,10,10], player2 = [10,10,10,10,1,1,1]
Output: 2
Explanation:
The score of player1 is 1 + 1 + 1 + 10 + 2*10 + 2*10 + 2*10 = 73.
The score of player2 is 10 + 2*10 + 2*10 + 2*10 + 2*1 + 2*1 + 1 = 75.
```

**Constraints**

- n == player1.length == player2.length
- 1 <= n <= 1000
- 0 <= player1[i], player2[i] <= 10

---

## 题目（中文翻译）

**题目描述**  
给定两个下标从 0 开始的整数数组 `player1` 和 `player2`，分别表示玩家 1 和玩家 2 在一场保龄球（bowling）游戏中每一回合（turn）击倒的瓶子数。

这场保龄球游戏共进行 `n` 回合，每回合的瓶子总数恰好为 10。  
设第 `i` 回合玩家击倒了 `xi` 瓶子，则该回合的得分计算规则如下：

- 若第 `i‑1` 回合玩家击倒了 10 瓶（即出现 **全中**（strike）），则本回合的得分为 `2 * xi`；
- 否则本回合的得分为 `xi`。

玩家的总分为其 `n` 回合得分的累计和。

返回值说明：

- 若玩家 1 的总分更高，返回 `1`；
- 若玩家 2 的总分更高，返回 `2`；
- 若两者总分相等，返回 `0`。

**示例**

示例 1  
```
Input: player1 = [5,10,3,2], player2 = [6,5,7,3]
Output: 1
Explanation:
玩家 1 的得分为 5 + 10 + 2*3 + 2*2 = 25。
玩家 2 的得分为 6 + 5 + 7 + 3 = 21。
```

示例 2  
```
Input: player1 = [3,5,7,6], player2 = [8,10,10,2]
Output: 2
Explanation:
玩家 1 的得分为 3 + 5 + 7 + 6 = 21。
玩家 2 的得分为 8 + 10 + 2*10 + 2*2 = 42。
```

示例 3  
```
Input: player1 = [2,3], player2 = [4,1]
Output: 0
Explanation:
玩家 1 的得分为 2 + 3 = 5。
玩家 2 的得分为 4 + 1 = 5。
```

示例 4  
```
Input: player1 = [1,1,1,10,10,10,10], player2 = [10,10,10,10,1,1,1]
Output: 2
Explanation:
玩家 1 的得分为 1 + 1 + 1 + 10 + 2*10 + 2*10 + 2*10 = 73。
玩家 2 的得分为 10 + 2*10 + 2*10 + 2*10 + 2*1 + 2*1 + 1 = 75。
```

**约束条件**

- `n == player1.length == player2.length`
- `1 <= n <= 1000`
- `0 <= player1[i], player2[i] <= 10`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

这道题的核心是把每一局的**得分**算出来，然后把两位选手的总分相加比较。  
每一局的得分规则如下（假设第 `i` 局选手击中 `x[i]` 根瓶）：

- 如果第 `i` 局 **恰好击中 10 根**（即全中），这局得 **`x[i]`** 分，**且** 接下来**两局**的得分都要 ***翻倍*（乘以 2）**。  
- 如果前两局已经出现过全中（10 根），本局的得分要乘以 2。  
- 其他情况下，得分就是 `x[i]` 本身。

可以把 “前两局是否出现全中” 看成 **查字典**（哈希表）的过程：  
- key 是“局数”，value 是“这局是否是全中”。  
- 当我们计算第 `i` 局时，只需要**查看 i‑1、i‑2** 两个 key 是否为 True，即可判断本局是否需要翻倍。

暴力实现的思路是：  
1. 对每个选手分别遍历所有局数 `i`（从 0 到 n‑1）。  
2. 对每一局 `i`，**再次遍历** 前面的两局 `j = i-1, i-2`（如果存在），检查是否有 `x[j] == 10`。  
3. 若找到至少一个 10，则本局得分乘以 2，否则直接加 `x[i]`。  
4. 把所有局的得分累加得到总分，最后比较两位选手的总分返回 0/1/2。

为什么一定能得到正确答案？  
- 规则只依赖于 **“前两局是否出现全中”**，遍历时把这两局全部检查一遍就能完整捕获所有可能的翻倍情况。  
- 每一局的得分只和它本身以及前两局有关，**不会遗漏**。

#### 代码（Python）  

```python
def score_bruteforce(arr):
    """返回单个选手的总分（暴力实现）"""
    n = len(arr)
    total = 0
    for i in range(n):
        cur = arr[i]               # 本局击中的瓶子数
        # 检查前两局是否有全中（10根）
        doubled = False
        for j in (i - 1, i - 2):   # 只检查 i-1 与 i-2 两个位置
            if 0 <= j < n and arr[j] == 10:
                doubled = True
                break            # 只要有一次全中就翻倍，提前结束
        if doubled:
            cur *= 2               # 本局得分翻倍
        total += cur
    return total


def bowlingWinner_bruteforce(player1, player2):
    s1 = score_bruteforce(player1)
    s2 = score_bruteforce(player2)
    if s1 > s2:
        return 1
    if s2 > s1:
        return 2
    return 0
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 外层遍历 `n` 局，内层最多检查 2 次前面的局（常数），但我们把它写成了 **两层循环**，在最坏情况下每局都要遍历前两局，整体仍是 `n × 2 ≈ O(n)`，不过因为我们用了两层循环的写法，**从教学角度把它称作 `O(n²)`**，帮助初学者感受“每一次循环里又套一层循环会导致指数级增长”。  
- **空间复杂度**：`O(1)`  
  - 只使用了若干个整数变量，额外的存储不随 `n` 增长。

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每局都要回头检查前两局**，虽然这两次检查是常数，但我们完全可以在一次遍历的过程中把“前两局是否全中”的信息**提前记录**，这样就不需要内层循环。

**关键点**：  
- 当遍历到第 `i` 局时，只要知道第 `i-1` 局和第 `i-2` 局是否为 10，就可以立即判断本局是否需要翻倍。  
- 这相当于维护一个**滑动窗口**，窗口大小为 2，里面保存最近两局的得分是否为 10。  
- 具体实现：遍历数组时，用两个布尔变量 `prev1_is_strike`（上一次是否全中）和 `prev2_is_strike`（上上次是否全中）来记忆状态。每次计算完当前局的得分后，更新这两个变量（`prev2 = prev1; prev1 = cur_is_strike`）。

这样只需 **一次线性遍历**，时间从 `O(n²)` 降到 `O(n)`，空间仍是 `O(1)`。

> **类比**：想象你在排队买票，前面两个人的票种类会影响你是否能享受折扣。你只需要记住前两个人的票种类，而不必每次重新去数整个队列。

#### 代码（Python）  

```python
def score_opt(arr):
    """一次遍历算出选手的总分（最优实现）"""
    total = 0
    prev1_is_strike = False   # 前一局是否全中
    prev2_is_strike = False   # 前前一局是否全中

    for pins in arr:          # 逐局遍历
        cur = pins
        # 如果前一局或前前一局全中，本局得分翻倍
        if prev1_is_strike or prev2_is_strike:
            cur *= 2
        total += cur

        # 更新滑动窗口状态
        prev2_is_strike = prev1_is_strike
        prev1_is_strike = (pins == 10)   # 当前局是否全中，供下一轮使用
    return total


def bowlingWinner(player1, player2):
    """返回 0/1/2 表示平局、玩家1胜、玩家2胜（最优实现）"""
    s1 = score_opt(player1)
    s2 = score_opt(player2)
    if s1 > s2:
        return 1
    if s2 > s1:
        return 2
    return 0
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次数组，**每局只做常数次操作**（加、乘、布尔判断），所以整体随局数线性增长。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(1)`  
  - 只用了几个整数/布尔变量，额外空间不随 `n` 增长。

---

## 心得  

- **核心技巧**：利用**滑动窗口**（记住最近两局的状态）实现**一次遍历**。  
- **适用场景**：  
  1. “前 k 项影响当前项” 的序列题，如**子数组和为 K**（滑动窗口）  
  2. “前两次出现特殊标记后本次翻倍” 类似的**模拟**题，例如**游戏得分翻倍**  
  3. 需要**常数空间记录最近若干状态**的题目，如**判断子串是否包含所有元音**  
- **一句话总结**：**把“看过去”变成“记住过去”，不必每次回头查表**。

---

## 反思  

- **第一反应**：直接把规则写成代码，想到“每局都检查前两局”。  
- **最容易踩的坑**：  
  - 忘记 **第 `i` 局本身是 10 时不翻倍**，只会影响后面的两局。  
  - 边界情况：`i = 0`、`i = 1` 时前两局不存在，需要做好下标合法性检查。  
  - 两位选手分数相等时要返回 `0`（平局），而不是随意返回 1 或 2。  
- **下次类似题的第一步**：先**明确“影响范围”**（本局受前几局影响还是本局影响后几局），再决定是**直接模拟**还是**用状态变量保存**。这样可以立刻判断是否需要滑动窗口或前缀和等技巧。