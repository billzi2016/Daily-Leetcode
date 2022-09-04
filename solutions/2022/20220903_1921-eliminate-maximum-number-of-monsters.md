# #1921. 消灭最多怪物数量 / Eliminate Maximum Number of Monsters

> 难度：中等 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/eliminate-maximum-number-of-monsters/)

---

## 题目（英文原版）

**Description**

You are playing a video game where you are defending your city from a group of n monsters. You are given a 0-indexed integer array dist of size n, where dist[i] is the initial distance in kilometers of the ith monster from the city.
The monsters walk toward the city at a constant speed. The speed of each monster is given to you in an integer array speed of size n, where speed[i] is the speed of the ith monster in kilometers per minute.
You have a weapon that, once fully charged, can eliminate a single monster. However, the weapon takes one minute to charge. The weapon is fully charged at the very start.
You lose when any monster reaches your city. If a monster reaches the city at the exact moment the weapon is fully charged, it counts as a loss, and the game ends before you can use your weapon.
Return the maximum number of monsters that you can eliminate before you lose, or n if you can eliminate all the monsters before they reach the city.

**Examples**

**Example 1:**

```
Input: dist = [1,3,4], speed = [1,1,1]
Output: 3
Explanation:
In the beginning, the distances of the monsters are [1,3,4]. You eliminate the first monster.
After a minute, the distances of the monsters are [X,2,3]. You eliminate the second monster.
After a minute, the distances of the monsters are [X,X,2]. You eliminate the third monster.
All 3 monsters can be eliminated.
```

**Example 2:**

```
Input: dist = [1,1,2,3], speed = [1,1,1,1]
Output: 1
Explanation:
In the beginning, the distances of the monsters are [1,1,2,3]. You eliminate the first monster.
After a minute, the distances of the monsters are [X,0,1,2], so you lose.
You can only eliminate 1 monster.
```

**Example 3:**

```
Input: dist = [3,2,4], speed = [5,3,2]
Output: 1
Explanation:
In the beginning, the distances of the monsters are [3,2,4]. You eliminate the first monster.
After a minute, the distances of the monsters are [X,0,2], so you lose.
You can only eliminate 1 monster.
```

**Constraints**

- n == dist.length == speed.length
- 1 <= n <= 105
- 1 <= dist[i], speed[i] <= 105

---

## 题目（中文翻译）

你在玩一款视频游戏，需要保卫城市免受 **n** 只怪物的侵袭。给定一个下标从 0 开始的整数数组 `dist`（distance），长度为 **n**，其中 `dist[i]` 表示第 **i** 只怪物最初距离城市的公里数。  
怪物以恒定速度向城市移动。每只怪物的速度由整数数组 `speed`（speed）给出，`speed[i]` 为第 **i** 只怪物每分钟行进的公里数。

你拥有一把武器，武器在**完全充能**（fully charged）后可以消灭（eliminate）一只怪物。但武器需要 **1 分钟** 充能一次，且在游戏开始时已经**完全充能**。  

当任意怪物抵达城市时你将失败。如果怪物在武器恰好充能的瞬间到达城市，也视为失败，游戏在你使用武器之前结束。

返回在失败之前你最多可以消灭的怪物数量；如果能够在所有怪物到达城市之前将它们全部消灭，则返回 **n**。

### 示例

#### 示例 1
```text
Input: dist = [1,3,4], speed = [1,1,1]
Output: 3
Explanation:
一开始，怪物的距离为 [1,3,4]。你消灭第 1 只怪物。
一分钟后，怪物的距离变为 [X,2,3]（X 表示已被消灭）。你消灭第 2 只怪物。
再过一分钟，距离变为 [X,X,2]。你消灭第 3 只怪物。
所有 3 只怪物都被消灭。
```

#### 示例 2
```text
Input: dist = [1,1,2,3], speed = [1,1,1,1]
Output: 1
Explanation:
一开始，怪物的距离为 [1,1,2,3]。你消灭第 1 只怪物。
一分钟后，距离变为 [X,0,1,2]，此时第 2 只怪物已抵达城市，你失败。
最多只能消灭 1 只怪物。
```

#### 示例 3
```text
Input: dist = [3,2,4], speed = [5,3,2]
Output: 1
Explanation:
一开始，怪物的距离为 [3,2,4]。你消灭第 1 只怪物。
一分钟后，距离变为 [X,0,2]，第 2 只怪物已抵达城市，你失败。
最多只能消灭 1 只怪物。
```

### 约束条件
- `n == dist.length == speed.length`
- `1 <= n <= 10^5`
- `1 <= dist[i], speed[i] <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**模拟每一分钟的战斗过程**：

1. 先算出每只怪物离城还需要多少分钟（向上取整），记为 `time[i] = ceil(dist[i] / speed[i])`。  
2. 把所有怪物放进一个列表，**每分钟**：  
   - 选取当前剩余时间最小的怪物（离城最近的），用武器把它消灭。  
   - 其它怪物的剩余时间都减 1（因为它们向城走了一分钟）。  
   - 如果此时还有怪物的剩余时间已经 ≤ 0，说明有怪物已经到达城堡，游戏结束。  

这相当于每一步都遍历一次列表找最小值，然后再遍历一次把所有时间减 1，直至游戏结束或全部怪物被消灭。

- **数据结构**：这里用的列表（array）就像一排排排队的怪物，找最小值好比在一堆书里挑出最薄的一本，时间越短的怪物越“薄”。  
- **正确性**：每分钟我们都把**离城最近的**怪物先消掉，其他怪物只能更快到城，若此时还有怪物已经到城，就说明无论怎么安排都不可能再消灭更多。  

#### 代码（Python）

```python
import math
from typing import List

def eliminateMaximum_bruteforce(dist: List[int], speed: List[int]) -> int:
    n = len(dist)
    # 计算每只怪物到达城堡需要的分钟数（向上取整）
    # ceil(a / b) 可以写成 (a + b - 1) // b，防止使用浮点数
    remain = [(dist[i] + speed[i] - 1) // speed[i] for i in range(n)]

    eliminated = 0          # 已经消灭的怪物数量
    minute = 0              # 已经过去的分钟数

    while remain:
        # 1️⃣ 找出离城最近的怪物（剩余时间最小的下标）
        min_idx = min(range(len(remain)), key=lambda i: remain[i])
        # 2️⃣ 用武器消灭它
        eliminated += 1
        del remain[min_idx]               # 把它从列表中移除

        # 3️⃣ 其它怪物都向城前进 1 分钟
        for i in range(len(remain)):
            remain[i] -= 1                # 时间-1 相当于距离-速度

        # 4️⃣ 检查是否有怪物已经到达（时间 <= 0）
        if any(t <= 0 for t in remain):
            break                         # 失败，结束循环

        minute += 1

    return eliminated
```

> **关键行中文注释**已写在代码里，直接复制运行即可。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每分钟我们要遍历一次列表找最小值（`O(k)`），`k` 是当前剩余怪物数。最坏情况下要进行 `n` 次循环，求和得到 `1 + 2 + … + n = O(n²)`。  
  - 大白话：如果有 10,000 只怪物，程序大概要做 10,000 × 5,000 ≈ 5 0⁷ 次比较，明显会超时。

- **空间复杂度**：`O(n)`  
  - 只用了一个保存剩余时间的列表，大小随怪物数线性增长。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每分钟都要遍历整个列表去找最近的怪物。  
实际上，我们只需要**一次性决定消灭顺序**，不必在每一步重新搜索。

1. **先算出每只怪物离城的“截止时间”**（即它们在第几分钟会到达城堡）：

   \[
   deadline_i = \left\lceil\frac{dist_i}{speed_i}\right\rceil
   \]

   这相当于给每只怪物贴了一个“最后通牒”，在这个时间点之前必须把它干掉，否则游戏结束。

2. **把所有通牒从小到大排序**。  
   - 排序后，第 `i` 小的通牒对应的怪物必须在第 `i` 分钟（从 0 开始计数）之前被消灭。  
   - 为什么？因为我们每分钟只能消灭 **恰好一只** 怪物，若第 `i` 分钟之前还有更早到达的怪物未被处理，必然会在第 `i` 分钟前撞城。

3. **遍历排序后的通牒**，检查是否能按顺序消灭：

   - 设当前已消灭的怪物数为 `k`（也就是我们已经用了 `k` 分钟），  
   - 若 `deadline_i > k`，说明第 `i` 只怪物还有足够时间在第 `k` 分钟被击杀，继续；  
   - 否则（`deadline_i <= k`），说明它已经“过期”，我们在第 `k` 分钟才有武器充好，却已经到城，游戏结束，返回 `k`。

4. 如果遍历完所有怪物都没有出现“过期”，说明我们可以把全部 `n` 只怪物都消灭，返回 `n`。

**核心技巧**：**贪心 + 排序**。先把最紧迫的任务排在前面，再逐个检查是否能按时间表完成。  

> 类比：想象你在机场排队办理登机手续，每个人都有最晚办理时间。你把最早到期的乘客先安排，检查每个人是否还能在自己的截止时间前完成办理。如果某个人已经错过了截止时间，你只能让后面的人等着，游戏（航班）就起飞了。

#### 代码（Python）

```python
import math
from typing import List

def eliminateMaximum(dist: List[int], speed: List[int]) -> int:
    """
    贪心 + 排序：
    1. 计算每只怪物的到达时间（向上取整）。
    2. 按到达时间从小到大排序。
    3. 按顺序检查第 i 只怪物是否还能在第 i 分钟前被消灭。
    """
    n = len(dist)
    # 1️⃣ 计算 deadline（向上取整），用整数运算避免浮点误差
    deadlines = [(dist[i] + speed[i] - 1) // speed[i] for i in range(n)]

    # 2️⃣ 排序，最早到达的排在前面
    deadlines.sort()

    # 3️⃣ 逐个检查能否按时间表消灭
    for minute, limit in enumerate(deadlines):
        # minute = 已经用了多少分钟（也等于已经消灭的怪物数）
        # limit = 第 minute 只怪物的最晚消灭时间（deadline）
        if limit <= minute:          # 已经来不及了
            return minute            # 只能消灭 minute 只怪物
    # 所有怪物都来得及消灭
    return n
```

> 代码中每一步都有中文注释，直接复制即可运行。

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 计算 `deadline` 是 `O(n)`，  
  - 排序是 `O(n log n)`（最耗时的步骤），  
  - 线性遍历检查是 `O(n)`。  
  - 与暴力解的 `O(n²)` 相比，提升显著：即使 `n = 10⁵`，`n log n` 也只在几百万次量级，能够轻松通过 LeetCode 限时。

- **空间复杂度**：`O(n)`  
  - 需要额外的数组保存 `deadline`，大小为 `n`。  
  - 这在题目限制（`n ≤ 10⁵`）下是完全可以接受的。

---

## 心得

- **核心技巧**：**把每只怪物的到达时间视为“最后期限”，对这些期限排序后按顺序检查**。这是一种典型的**贪心+排序**思路。
- **适用题型**：
  1. “任务调度”类题目，如 *Course Schedule III*（需要在截止时间前完成尽可能多的课程）。
  2. “最早完成”类题目，如 *Maximum Number of Events That Can Be Attended*（先参加最早结束的活动）。
  3. 需要“在有限资源下按时间顺序完成尽可能多任务”的场景。
- **一句话总结**：**把“最紧迫的”先排好队，再逐个检验能否按时处理，贪心就能得到最优解。**

---

## 反思

- **拿到题目第一反应**：先算每只怪物何时到达，然后想“每分钟挑最近的消灭”，于是想到模拟（暴力）实现。
- **最容易踩的坑**：
  1. **向上取整**：`dist / speed` 必须向上取整，否则会把本应在第 2 分钟到达的怪物误判为第 1 分钟。使用 `(dist + speed - 1) // speed` 能避免浮点误差。  
  2. **等于截止时间的情况**：题目说明“如果怪物在武器充好那一刻到达，算输”。因此比较时应使用 `<= minute`（而不是 `<`）。  
  3. **边界条件**：只有一只怪物时，直接返回 1；所有怪物都在同一时间到达时，只能消灭 0 只（因为第一分钟武器已经充好但怪物已经在城门口）。
- **下次遇到同类题**：第一步先**把每个对象的时间限制（deadline）算出来**，随后**排序**，最后**逐个用已用时间（minute）与 deadline 比较**，看是否还能继续。这样可以立刻把问题从“模拟”转化为“贪心检查”。