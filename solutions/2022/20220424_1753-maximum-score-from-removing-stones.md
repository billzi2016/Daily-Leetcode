# #1753. 移除石子获得的最大分数 / Maximum Score From Removing Stones

> 难度：中等 · 标签：Math、Greedy、Heap (Priority Queue) · [LeetCode 链接](https://leetcode.com/problems/maximum-score-from-removing-stones/)

---

## 题目（英文原版）

**Description**

You are playing a solitaire game with three piles of stones of sizes a​​​​​​, b,​​​​​​ and c​​​​​​ respectively. Each turn you choose two different non-empty piles, take one stone from each, and add 1 point to your score. The game stops when there are fewer than two non-empty piles (meaning there are no more available moves).
Given three integers a​​​​​, b,​​​​​ and c​​​​​, return the maximum score you can get.

**Examples**

**Example 1:**

```
Input: a = 2, b = 4, c = 6
Output: 6
Explanation: The starting state is (2, 4, 6). One optimal set of moves is:
- Take from 1st and 3rd piles, state is now (1, 4, 5)
- Take from 1st and 3rd piles, state is now (0, 4, 4)
- Take from 2nd and 3rd piles, state is now (0, 3, 3)
- Take from 2nd and 3rd piles, state is now (0, 2, 2)
- Take from 2nd and 3rd piles, state is now (0, 1, 1)
- Take from 2nd and 3rd piles, state is now (0, 0, 0)
There are fewer than two non-empty piles, so the game ends. Total: 6 points.
```

**Example 2:**

```
Input: a = 4, b = 4, c = 6
Output: 7
Explanation: The starting state is (4, 4, 6). One optimal set of moves is:
- Take from 1st and 2nd piles, state is now (3, 3, 6)
- Take from 1st and 3rd piles, state is now (2, 3, 5)
- Take from 1st and 3rd piles, state is now (1, 3, 4)
- Take from 1st and 3rd piles, state is now (0, 3, 3)
- Take from 2nd and 3rd piles, state is now (0, 2, 2)
- Take from 2nd and 3rd piles, state is now (0, 1, 1)
- Take from 2nd and 3rd piles, state is now (0, 0, 0)
There are fewer than two non-empty piles, so the game ends. Total: 7 points.
```

**Example 3:**

```
Input: a = 1, b = 8, c = 8
Output: 8
Explanation: One optimal set of moves is to take from the 2nd and 3rd piles for 8 turns until they are empty.
After that, there are fewer than two non-empty piles, so the game ends.
```

**Constraints**

- 1 <= a, b, c <= 105

---

## 题目（中文翻译）

你在玩一个单人游戏，桌面上有大小分别为 `a`、`b`、`c` 的三堆石子（stone piles）。每回合你选择 **两个不同的非空堆**（non‑empty piles），各取走一颗石子，并且得 1 分。当剩余的非空堆少于两堆时（即没有可进行的移动），游戏结束。

给定整数 `a`、`b`、`c`，返回你能获得的 **最大分数**（maximum score）。

**示例 1**  
Input: a = 2, b = 4, c = 6  
Output: 6  
Explanation: 初始状态为 `(2, 4, 6)`。一种最优的操作序列为：  
- 从第 1 堆和第 3 堆各取一颗，状态变为 `(1, 4, 5)`  
- 从第 1 堆和第 3 堆各取一颗，状态变为 `(0, 4, 4)`  
- 从第 2 堆和第 3 堆各取一颗，状态变为 `(0, 3, 3)`  
- 从第 2 堆和第 3 堆各取一颗，状态变为 `(0, 2, 2)`  
- 从第 2 堆和第 3 堆各取一颗，状态变为 `(0, 1, 1)`  
- 从第 2 堆和第 3 堆各取一颗，状态变为 `(0, 0, 0)`  

共计 6 次操作，得到最高得分 6。

**示例 2**  
Input: a = 4, b = 4, c = 6  
Output: 7  
Explanation: 初始状态为 `(4, 4, 6)`。一种最优的操作序列为：  
- 从第 1 堆和第 2 堆各取一颗，状态变为 `(3, 3, 6)`  
- 从第 1 堆和第 3 堆各取一颗，状态变为 `(2, 3, 5)`  
- 从第 1 堆和第 3 堆各取一颗，状态变为 `(1, 3, 4)`  
- 从第 1 堆和第 3 堆各取一颗，状态变为 `(0, 3, 3)`  
- 从第 2 堆和第 3 堆各取一颗，状态变为 `(0, 2, 2)`  
- 从第 2 堆和第 3 堆各取一颗，状态变为 `(0, 1, 1)`  
- 从第 2 堆和第 3 堆各取一颗，状态变为 `(0, 0, 0)`  

共计 7 次操作，得到最高得分 7。

**示例 3**  
Input: a = 1, b = 8, c = 8  
Output: 8  
Explanation: 最优的做法是始终从第 2 堆和第 3 堆各取一颗，连续进行 8 次，直至这两堆耗尽。此时剩下的只有第 1 堆（已为空），游戏结束，累计得分为 8。

**约束条件**  
- `1 <= a, b, c <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法就是**枚举所有可能的取石顺序**，把每一步都尝试一次，记下最终得到的分数，取最大的那个。  

- **数据结构**：我们只需要三个整数 `a, b, c` 来记录三堆石子的剩余数量。可以把它们放在一个长度为 3 的列表里，类似把三本书放在一个小书架上，随时可以查看每本书还有多少页。  
- **为什么能得到正确答案**：因为我们把**所有**合法的取石方式都遍历了一遍，必然会碰到最优的那一种。  
- **复杂度分析**：  
  - 每一次取石会把总石子数减少 2，最多进行 ` (a+b+c)//2 ` 步。  
  - 在每一步我们有至多 `C(3,2)=3` 种选择（任选两堆），所以递归树的分支数是 `3^step`。  
  - 最坏情况下步数约为 `10^5`（因为每堆最多 `10^5`），于是时间复杂度是 **指数级**，写成 `O(3^{(a+b+c)/2})`，这在实际里根本不可接受。  
  - 空间上除了递归栈外，只用了常数个变量，空间复杂度是 **O(1)**（递归深度最多 ` (a+b+c)/2 `，但仍是线性）。

> **大白话**：`O(3^{50})` 就好比让你在 3 条路上每走一步都要选一次，走 50 步后会出现 **3 的 50 次方** 条不同的路线，根本不可能手算完。

#### 代码（Python）

```python
def maxScore_bruteforce(a: int, b: int, c: int) -> int:
    """暴力递归：尝试所有合法的取石顺序，返回最大得分。"""
    # 为了避免重复计算，使用记忆化（cache），否则会超时
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(x: int, y: int, z: int) -> int:
        # x, y, z 分别是三堆剩余的石子数
        # 如果两堆已经空，不能再取石，得分为 0
        if (x == 0 and y == 0) or (y == 0 and z == 0) or (x == 0 and z == 0):
            return 0

        best = 0
        # 任选两堆各取一颗，递归求后续的最大得分
        if x > 0 and y > 0:
            best = max(best, 1 + dfs(x - 1, y - 1, z))
        if x > 0 and z > 0:
            best = max(best, 1 + dfs(x - 1, y, z - 1))
        if y > 0 and z > 0:
            best = max(best, 1 + dfs(x, y - 1, z - 1))
        return best

    return dfs(a, b, c)


# 示例
print(maxScore_bruteforce(2, 4, 6))   # 6
print(maxScore_bruteforce(4, 4, 6))   # 7
print(maxScore_bruteforce(1, 8, 8))   # 8
```

> **关键行注释**  
> - `@lru_cache`：把已经算好的子问题记下来，后面再遇到相同的 `(x,y,z)` 直接返回，防止指数爆炸（相当于给递归装了个“查字典”）。  
> - `if x>0 and y>0:`：只有两堆都有石子时才能取石，这一步对应“选两本书的同一页”。  

#### 复杂度  

- **时间复杂度**：`O(3^{(a+b+c)/2})`（指数级）——即使加了记忆化，也仍然远大于线性，无法在 10⁵ 规模下通过。  
- **空间复杂度**：`O((a+b+c)/2)`——递归深度最多是总石子数的一半，另外记忆化表会占用同样数量的状态空间。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**搜索所有可能**太慢，真正的瓶颈在于 **每一步到底应该从哪两堆取石**。如果我们每次都挑 **“最大的两堆”**，能否保证最优？答案是 **可以**，原因如下：

1. **每一步只能拿走 2 颗石子**，所以游戏最多进行 `total // 2` 步（`total = a+b+c`）。这给了一个上界。  
2. 另一个上界来源于**最小的两堆**：  
   - 假设 `maxPile` 是三堆中最大的那一堆，剩下的两堆我们记作 `small1`、`small2`。  
   - 每一次取石至少要用到 **其中一堆非最大的**（因为两堆必须不同），于是最多只能进行 `small1 + small2` 步——当这两堆都被耗尽时，游戏就结束。  
3. 综合这两个上界，**真正的最大得分** = `min(total // 2, total - maxPile)`。  
   - `total // 2` 表示“石子总数除以 2”，即最多能取多少对。  
   - `total - maxPile` 等价于 “两个较小堆的和”，因为 `total - maxPile = small1 + small2`。  

这就把原本的**模拟**问题转化成了**纯数学计算**，时间复杂度直接降到 **O(1)**。

> **类比**：把三堆石子想象成三条水管，水流只能从两条不同的管子同时抽取。总共能抽多少次，取决于水管的总流量（`total//2`）以及两条最小管子的流量之和（`total - maxPile`），两者取较小者即可。

如果不想直接用公式，也可以用 **最大堆（Priority Queue）** 来每次弹出最大的两堆，减 1 后再放回去，直到不到两堆非零。该方法的时间复杂度是 `O(total log 3) ≈ O(total)`，仍然很快，且思路直观，适合作为“贪心模拟”版的实现。

#### 代码（Python）  

**方式一：直接公式（最简）**

```python
def maxScore(a: int, b: int, c: int) -> int:
    """最优解：只需要数学公式，时间 O(1)"""
    total = a + b + c
    max_pile = max(a, b, c)          # 最大的那一堆
    # 两个上界取最小值
    return min(total // 2, total - max_pile)


# 示例
print(maxScore(2, 4, 6))   # 6
print(maxScore(4, 4, 6))   # 7
print(maxScore(1, 8, 8))   # 8
```

**方式二：贪心 + 最大堆（更形象）**

```python
import heapq

def maxScore_heap(a: int, b: int, c: int) -> int:
    """贪心模拟：每次取最大的两堆，使用负数实现最大堆"""
    # Python 的 heapq 是最小堆，取负数可以当作最大堆使用
    heap = [-a, -b, -c]
    heapq.heapify(heap)               # O(3) → 常数时间
    score = 0

    while True:
        # 取出当前最大的两堆（负数最小即原数最大）
        first = heapq.heappop(heap)   # 最大的
        second = heapq.heappop(heap)  # 第二大的

        # 如果其中有一堆已经是 0（即负数是 0），说明剩余非空堆不足两堆，结束
        if first == 0 or second == 0:
            break

        # 各取走一颗石子，得分 +1
        score += 1
        first += 1   # 因为是负数，+1 相当于 -1（石子数减 1）
        second += 1

        # 把更新后的堆重新放回去
        heapq.heappush(heap, first)
        heapq.heappush(heap, second)
        # 第三堆始终在 heap 中，无需弹出再放回

    return score


# 示例
print(maxScore_heap(2, 4, 6))   # 6
print(maxScore_heap(4, 4, 6))   # 7
print(maxScore_heap(1, 8, 8))   # 8
```

> **关键行注释**  
> - `heap = [-a, -b, -c]`：把正数变负后放入最小堆，等价于最大堆。  
> - `if first == 0 or second == 0:`：只要弹出的最大堆中有 0，说明剩余非空堆不足两堆，游戏结束。  
> - `first += 1`：因为是负数，`+1` 实际是把绝对值减 1（即石子数减 1）。  

#### 复杂度  

- **时间复杂度**：  
  - 公式版 `O(1)`，只做几次加减比较。  
  - 堆版 `O(total log 3) = O(total)`，因为每一步弹出、插入堆的代价是 `log 3`（常数），最多进行 `total//2` 步。与暴力的指数级相比，快了 **几百倍以上**。  
- **空间复杂度**：`O(1)`（公式）或 `O(1)`（堆，只存 3 个整数），与输入规模无关。  

---  

## 心得  

- **核心技巧**：**贪心 + 上界分析**——每一步都取最大的两堆，等价于“让大堆尽快“陪伴”小堆”，从而避免出现“大堆剩余多、其它堆已空”导致无法继续取石的浪费。  
- **适用的题型**：  
  1. “取两个不同资源，直到不足两种”类问题（如 **"Maximum Number of K‑Same Pairs"**）。  
  2. “每次消耗两种资源，求最多操作次数”类（如 **"Maximum Number of Groups Formed From Array"**）。  
  3. “三堆/多堆资源的最优配对”类（如 **"Maximum Points From Cards"** 变形）。  
- **一句话总结解题钥匙**：**把“最多能做几次”拆成两个上界——总石子数的半数 与 两个最小堆的和，取最小者即为答案**。  

---  

## 反思  

- **第一反应**：看到“每回合取两堆石子”会想到**模拟**，甚至写递归遍历所有可能。  
- **最容易踩的坑**：  
  - 忘记 **两堆必须不同**，误把同一堆的两颗石子一起取走导致错误。  
  - 边界情况：当一堆为 0 时，必须立即停止，不能继续尝试取该堆。  
  - 公式写错：`total - maxPile` 实际等价于 “两堆较小的和”，若写成 `maxPile - (total - maxPile)` 会完全相反。  
- **下次遇到同类题**，第一步应该先**写出上界**（总资源/2 与非最大资源之和），检查两者的最小值是否已经满足要求；如果不想直接用公式，可用**最大堆贪心**快速实现。