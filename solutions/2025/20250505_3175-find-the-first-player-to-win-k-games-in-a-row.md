# #3175. 找到首次连胜 K 场的玩家 / Find The First Player to win K Games in a Row

> 难度：中等 · 标签：Array、Simulation · [LeetCode 链接](https://leetcode.com/problems/find-the-first-player-to-win-k-games-in-a-row/)

---

## 题目（英文原版）

**Description**

A competition consists of n players numbered from 0 to n - 1.
You are given an integer array skills of size n and a positive integer k, where skills[i] is the skill level of player i. All integers in skills are unique.
All players are standing in a queue in order from player 0 to player n - 1.
The competition process is as follows:
The winner of the competition is the first player who wins k games in a row.
Return the initial index of the winning player.

**Examples**

**Example 1:**

```
Input: skills = [4,2,6,3,9], k = 2
Output: 2
Explanation:
Initially, the queue of players is [0,1,2,3,4] . The following process happens:
Player 2 won k = 2 games in a row, so the winner is player 2.
```

**Example 2:**

```
Input: skills = [2,5,4], k = 3
Output: 1
Explanation:
Initially, the queue of players is [0,1,2] . The following process happens:
Player 1 won k = 3 games in a row, so the winner is player 1.
```

**Constraints**

- n == skills.length
- 2 <= n <= 105
- 1 <= k <= 109
- 1 <= skills[i] <= 106
- All integers in skills are unique.

---

## 题目（中文翻译）

**描述**  
一场比赛有 `n` 名玩家，编号为 `0` 到 `n - 1`。  
给定长度为 `n` 的整数数组 `skills` 和一个正整数 `k`，其中 `skills[i]` 表示玩家 `i` 的技能水平（skill level）。`skills` 中的所有整数互不相同。  
所有玩家按照编号顺序站成一条队列 (queue)，即 `[0, 1, ..., n‑1]`。  

比赛过程如下：  
- 每一轮，队列前端的两名玩家进行对决，技能水平更高的玩家获胜并继续留在队列前端，另一名玩家被移到队列尾部。  
- 若同一名玩家连续赢得 `k` 场比赛，则该玩家成为本场比赛的冠军。  

返回冠军玩家在初始队列中的下标。

---

**示例 1**  
```text
Input: skills = [4,2,6,3,9], k = 2
Output: 2
Explanation:
Initially, the queue of players is [0,1,2,3,4]. The following process happens:
Player 2 won k = 2 games in a row, so the winner is player 2.
```

**示例 2**  
```text
Input: skills = [2,5,4], k = 3
Output: 1
Explanation:
Initially, the queue of players is [0,1,2]. The following process happens:
Player 1 won k = 3 games in a row, so the winner is player 1.
```

---

**约束条件**  
- `n == skills.length`  
- `2 <= n <= 10^5`  
- `1 <= k <= 10^9`  
- `1 <= skills[i] <= 10^6`  
- `skills` 中的所有整数互不相同

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**完整地模拟比赛过程**，一步一步按照题目描述进行：

1. 先把所有玩家按下标 `[0, 1, 2, …, n‑1]` 排成一个队列。  
2. 取队首的两名玩家比较 `skills`，技能更高的获胜，另一名被送到队尾。  
3. 记录当前获胜玩家已经连胜的次数 `cnt`，如果 `cnt == k`，说明找到了答案。  
4. 若当前玩家输掉了这场比赛，则把 `cnt` 重新置为 `1`（因为新晋的胜者已经赢了一场）。  

> **类比**：把这条队列想成一条“跑步赛道”，每次两个人赛跑，输的那个人被安排到赛道的最远端重新等待。

这个方法**一定能得到正确答案**，因为我们完全遵循了题目给出的比赛规则，没有任何“偷懒”。  

**时间复杂度**  
- 最坏情况下我们可能要进行很多轮比较：每一次比较只会让**一名玩家离开队首**，而要让某人连胜 `k` 场，需要至多 `k` 次比较。  
- 当 `k` 很大（比如 `k = 10^9`）时，直接模拟会非常慢，理论上时间复杂度是 **O(k·n)**，在最坏情况下甚至会达到 **O(10^14)**，远远超出时间限制。  

**空间复杂度**  
- 需要维护一个队列（`list` 或 `deque`），保存 `n` 个下标，空间是 **O(n)**。  

#### 代码（Python）  

```python
from collections import deque

def find_winner_bruteforce(skills, k):
    n = len(skills)
    q = deque(range(n))          # 队列里保存的是玩家的下标
    cur = q.popleft()            # 先把第一个玩家拿出来，作为“当前胜者”
    cnt = 0                      # 连胜次数

    while True:
        nxt = q.popleft()        # 与下一个玩家比较
        # 谁的 skill 更高，谁就是本轮的胜者
        if skills[cur] > skills[nxt]:
            cnt += 1             # 当前胜者继续连胜
            q.append(nxt)        # 输的玩家排到队尾
        else:
            cnt = 1              # 新胜者已经赢了一场
            q.append(cur)        # 之前的胜者排到队尾
            cur = nxt            # 更新当前胜者

        if cnt == k:             # 连胜达到 k，返回下标
            return cur
```

> **注意**：上述代码在 `k` 很大时会卡死，属于**暴力解**，仅用于帮助大家理解除题思路。

#### 复杂度  

- **时间复杂度**：`O(k·n)`（最坏情况需要进行 `k` 轮，每轮都要弹出/压入队列），直观上可以把它想成“要走 `k` 步路，每走一步都要搬动一箱子”。  
- **空间复杂度**：`O(n)`，因为我们把所有玩家的编号都保存在队列里。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于不停地搬动队列**，尤其是当 `k` 很大时，我们根本不需要真的把每一场比赛都演一遍。关键在于观察**技能最高的玩家**的特殊属性：

1. **如果 `k ≥ n`**（或者更宽松的 `k ≥ n-1`），只要出现一次全局最大技能的玩家，他一定会最终赢 `k` 场。原因是：  
   - 最大技能的玩家在与任何其他玩家的对决中必胜。  
   - 他只需要连续击败 `n‑1` 个人（把所有其他玩家都“送到队尾”），此后再继续和已经被送到队尾的玩家对决，依然会赢。  
   - 因此只要 `k` 不小于玩家总数，答案必然是 **技能最大的玩家的下标**。  

2. **如果 `k < n`**，我们可以 **一次遍历**（`O(n)`）就决定答案，而不必真正维护完整的队列。思路如下：  

   - 维护两个变量：  
     - `cur`：当前连胜的玩家下标。  
     - `cnt`：`cur` 已经连续赢的次数。  
   - 从左到右依次把每个玩家 `i`（从下标 `1` 开始）与 `cur` 比较：  
     - 若 `skills[i] > skills[cur]`，说明 `i` 更强，`i` 成为新的 `cur`，并把 `cnt` 重新置为 `1`（因为 `i` 刚赢了一场）。  
     - 否则，`cur` 继续赢，`cnt += 1`。  
   - 每次更新 `cnt` 后检查 `cnt == k`，若成立立即返回 `cur`。  
   - 为什么这一步等价于完整模拟？  
     - 只要 `k < n`，**全局最大玩家**不一定会在前 `k` 场出现，但**每一次出现更大的玩家**，相当于在真实比赛中它“抢走了队首”，并把之前的胜者送到队尾。我们只需要记住最新的胜者以及它的连胜次数即可。  
   - 由于我们只遍历一次数组，时间是 **O(n)**，空间只用了常数几个变量，**O(1)**。  

> **类比**：把所有玩家排成一条直线，**我们只关心谁是目前“站在最前面、手握连胜计数”的人**，而不必把后面的人搬来搬去。  

#### 代码（Python）  

```python
def find_winner(skills, k):
    """
    返回第一个连续赢 k 场的玩家下标
    """
    n = len(skills)

    # 情况 1：k 足够大，必然是技能最高的玩家
    if k >= n - 1:                     # n-1 是安全阈值，等价于 k >= n
        # max_idx = skills.index(max(skills))  # 直接找最大值对应的下标
        # 为了 O(1) 空间，手动遍历一次即可
        max_idx = 0
        for i in range(1, n):
            if skills[i] > skills[max_idx]:
                max_idx = i
        return max_idx

    # 情况 2：k < n，使用一次遍历模拟
    cur = 0        # 当前连胜玩家（初始为下标 0）
    cnt = 0        # 连胜次数

    for i in range(1, n):
        if skills[i] > skills[cur]:
            # i 更强，取代 cur 成为新胜者
            cur = i
            cnt = 1          # 只赢了一场（与之前的 cur 的对决）
        else:
            # cur 继续赢
            cnt += 1

        if cnt == k:         # 达到 k 连胜，返回答案
            return cur

    # 按题意一定会在循环中返回，这里只是防止 IDE 报错
    return cur
```

> **关键点注释**：  
> - `if k >= n - 1:` 那一行是利用“**k 大于等于玩家数量减一**”的数学事实，直接返回全局最大。  
> - 循环里只比较两个人的技能大小，不涉及真实的队列操作，极大地提升了效率。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 当 `k >= n-1` 时，仅遍历一次数组找最大值；  
  - 当 `k < n` 时，同样只遍历一次数组。  
  - 与暴力解的 `O(k·n)` 相比，**线性**时间几乎是瞬间完成。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量 (`cur`, `cnt`, `max_idx`) ，不随 `n` 增长。  

---  

## 心得  

- **核心技巧**：**利用全局最大值的支配性 + 一次遍历维护当前连胜者**。  
- 这种技巧在“**连续胜利**”或“**连续出现**”类题目中非常常见，尤其是数组中元素唯一且有大小关系时。  

**适用的类似题型**（任选其一即可）：  
1. **LeetCode 1535. Find the Winner of an Array Game**（几乎相同的题目，只是 `k` 固定为 `n-1`）。  
2. **LeetCode 1146. Snapshot Array**（需要维护历史状态，思路类似“只记录最新状态”。）  
3. **LeetCode 2299. Strongest Password**（找全局最大/最小的技巧）。  

**一句话总结解题钥匙**：  
> “当要找连续 `k` 次胜利时，只要跟踪**当前最强者**和**它的连胜计数**，并利用 `k ≥ n` 时全局最大必胜的特性，即可在一次遍历中得到答案。”  

---  

## 反思  

- **第一反应**：直接写一个完整的模拟循环，搬来搬去的队列。  
- **最容易踩的坑**：  
  - 忽略 `k` 可能远大于 `n`，导致模拟无限循环或超时。  
  - 没有考虑 **技能唯一** 的前提，导致在相等情况下的处理错误。  
  - 忘记在 `k < n` 时仍然需要返回 **第一个** 连胜 `k` 次的玩家，而不是全局最大。  

- **下次遇到同类题**，第一步应该问自己：  
  - “是否存在一个**全局极值**（最大或最小）在某些条件下必然胜出？”  
  - “能否只用**常数空间**维护当前的**候选者**和**计数**，而不必完整模拟全部过程？”  

这样思考可以迅速定位到线性时间的最优解。