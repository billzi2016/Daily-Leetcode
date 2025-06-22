# #3238. 找出获胜玩家的数量 / Find the Number of Winning Players

> 难度：简单 · 标签：Array、Hash Table、Counting · [LeetCode 链接](https://leetcode.com/problems/find-the-number-of-winning-players/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the number of players in a game and a 2D array pick where pick[i] = [xi, yi] represents that the player xi picked a ball of color yi.
Player i wins the game if they pick strictly more than i balls of the same color. In other words,
Return the number of players who win the game.
Note that multiple players can win the game.

**Examples**

**Example 1:**

```
Input: n = 4, pick = [[0,0],[1,0],[1,0],[2,1],[2,1],[2,0]]
Output: 2
Explanation:
Player 0 and player 1 win the game, while players 2 and 3 do not win.
```

**Example 2:**

```
Input: n = 5, pick = [[1,1],[1,2],[1,3],[1,4]]
Output: 0
Explanation:
No player wins the game.
```

**Example 3:**

```
Input: n = 5, pick = [[1,1],[2,4],[2,4],[2,4]]
Output: 1
Explanation:
Player 2 wins the game by picking 3 balls with color 4.
```

**Constraints**

- 2 <= n <= 10
- 1 <= pick.length <= 100
- pick[i].length == 2
- 0 <= xi <= n - 1
- 0 <= yi <= 10

---

## 题目（中文翻译）

给定一个整数 `n` 表示游戏中的玩家数量，以及一个二维数组 `pick`，其中 `pick[i] = [xi, yi]` 表示玩家 `xi` 拿到了颜色为 `yi` 的球（ball）。

玩家 `i` 若拿到同一种颜色的球的数量 **严格大于** `i`，则该玩家获胜（wins the game）。换句话说，

返回获胜的玩家数量。

注意，可能有多个玩家同时获胜。

## 示例

### 示例 1
**输入**: `n = 4`, `pick = [[0,0],[1,0],[1,0],[2,1],[2,1],[2,0]]`  
**输出**: `2`  
**解释**: 玩家 0 和玩家 1 获胜，而玩家 2 和玩家 3 未获胜。

### 示例 2
**输入**: `n = 5`, `pick = [[1,1],[1,2],[1,3],[1,4]]`  
**输出**: `0`  
**解释**: 没有玩家获胜。

### 示例 3
**输入**: `n = 5`, `pick = [[1,1],[2,4],[2,4],[2,4]]`  
**输出**: `1`  
**解释**: 玩家 2 通过拿到 3 个颜色为 4 的球而获胜。

## 约束条件
- `2 <= n <= 10`
- `1 <= pick.length <= 100`
- `pick[i].length == 2`
- `0 <= xi <= n - 1`
- `0 <= yi <= 10`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们先把题目翻译成生活化的场景：  
- 有 `n` 位玩家，每位玩家可以多次挑选颜色编号 `yi` 的球。  
- 对于第 `i` 位玩家（注意下标从 **0** 开始），如果他挑选的**同一种颜色的球数量**严格大于 `i`，就算他“赢”。  

最直接的做法是**逐个玩家**统计他每种颜色挑了多少个，然后取出数量最多的那种颜色，和玩家编号 `i` 比较大小。  

> **哈希表（字典）类比**：  
> 想象我们在查字典，**key** 是颜色，**value** 是该颜色出现的次数。对每个玩家，都建这么一本“小字典”。  

因为 `n ≤ 10`、`pick.length ≤ 100`，即使我们为每个玩家都遍历一遍 `pick`，总的操作也不会多于 `10 × 100 = 1000` 次，完全在接受范围内，所以这就是“暴力”解法。

#### 代码（Python）

```python
def winningPlayers_brute(n, pick):
    # 1️⃣ 为每个玩家准备一个空字典，用来统计颜色出现次数
    #   player_counts[i] = {color: cnt, ...}
    player_counts = [dict() for _ in range(n)]

    # 2️⃣ 遍历所有挑选记录，把对应玩家的字典里相应颜色的计数 +1
    for player, color in pick:
        cnt_dict = player_counts[player]
        cnt_dict[color] = cnt_dict.get(color, 0) + 1   # dict.get 相当于查字典，若不存在返回 0

    # 3️⃣ 统计有多少玩家满足「最多的同色球数量 > 玩家编号 i」
    win = 0
    for i in range(n):
        # 如果该玩家根本没有挑球，cnt_max 直接设为 0
        cnt_max = max(player_counts[i].values()) if player_counts[i] else 0
        if cnt_max > i:          # “严格大于 i”是赢的条件
            win += 1
    return win
```

#### 复杂度

- **时间复杂度**：`O(n * m)`，其中 `m = len(pick)`。  
  大白话：我们把每条挑选记录看一遍（`m` 次），然后对每个玩家再看一遍他的颜色计数（最坏 `n` 次），所以整体是两层循环乘起来。  
- **空间复杂度**：`O(n * k)`，`k` 是每位玩家可能出现的不同颜色种类数（这里 `k ≤ 11`，因为颜色编号 0~10）。  
  大白话：我们为每位玩家保存一个小字典，字典里装的是「颜色 → 次数」的对应关系。

---

### 2. 最优解

#### 思路  

虽然上面的暴力解已经够快，但我们可以把 **统计** 与 **判断** 融合到一次遍历里，省去第二遍遍历每个玩家字典的步骤。  

**瓶颈**：在暴力解中，需要在第 3 步对每位玩家的所有颜色计数求最大值 `max(...)`，这相当于对每个玩家再进行一次小循环。  

**优化**：在遍历 `pick` 的同时，**实时维护**每位玩家当前出现次数最多的颜色数量 `max_cnt[i]`。每当我们为玩家 `i` 的某个颜色计数加 1 时，立即更新 `max_cnt[i]`（如果这次增加的次数更大）。遍历结束后，`max_cnt[i]` 已经直接给出了该玩家的“最多同色球数量”，我们只需再比较一次 `max_cnt[i] > i` 即可。

核心数据结构仍然是**哈希表**（字典），但我们把它们的使用浓缩成一次遍历。

> **类比**：把每位玩家的字典想象成一本账本，`max_cnt[i]` 就是账本里最大的一笔记录。每记一笔（一次挑选），我们立刻检查这笔是否成为新的最大值。

#### 代码（Python）

```python
def winningPlayers_optimal(n, pick):
    # 对每位玩家维护两个信息：
    # 1) 颜色→次数 的字典
    # 2) 当前出现次数最多的颜色的次数（max_cnt）
    player_counts = [dict() for _ in range(n)]
    max_cnt = [0] * n                     # 初始最大次数都是 0

    for player, color in pick:
        cnt = player_counts[player].get(color, 0) + 1   # 这一次该颜色的累计次数
        player_counts[player][color] = cnt

        # 实时更新该玩家的最大次数
        if cnt > max_cnt[player]:
            max_cnt[player] = cnt

    # 统计赢的玩家数量
    win = sum(1 for i in range(n) if max_cnt[i] > i)
    return win
```

#### 复杂度

- **时间复杂度**：`O(m)`，只遍历一次 `pick`（`m = len(pick)`），没有额外的循环。  
  与暴力解相比省去了 `n` 次的 `max` 操作，实际运行更快。  
- **空间复杂度**：`O(n * k)`，与暴力解相同，因为仍然需要保存每位玩家的颜色计数。  

---

## 心得

- **核心技巧**：在遍历过程中**实时维护局部最值**（这里是每位玩家的最大同色球数量），避免二次遍历。  
- **适用的题型**  
  1. “统计每个元素出现次数的最大值”类题（如 LeetCode 1695 `Maximum Erasure Value` 的类似思路）。  
  2. “分组后求每组最大/最小”类题（如 LeetCode 1122 `Relative Sort Array` 中的分桶计数）。  
- **一句话总结**：**一次遍历 + 哈希表 + 实时更新最大值**，是处理“每组统计后立即比较”问题的万能钥匙。

---

## 反思

- **第一反应**：看到“玩家 i 必须挑 > i 球”，立刻想到要把每个玩家的挑球记录分组，然后在每组里找出出现次数最多的颜色。  
- **最容易踩的坑**  
  - **下标误差**：玩家编号从 `0` 开始，比较时要用 `>` 而不是 `>=`。  
  - **空玩家**：有的玩家可能根本没有挑球，需要把最大次数默认设为 `0`，否则 `max()` 会报错。  
  - **颜色范围**：颜色编号虽然小（≤10），但不能假设所有颜色都会出现，字典的 `get` 方法可以安全处理不存在的键。  
- **下次遇到同类题**，第一步应该想到：**“先把数据按玩家/分组，再在每组内部用哈希表统计频次，同时记录最高频次”。**这样既能保证正确，又能做到一次遍历完成。