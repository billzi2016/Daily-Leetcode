# #1815. 获取新鲜甜甜圈的最大快乐组数 / Maximum Number of Groups Getting Fresh Donuts

> 难度：困难 · 标签：Array、Dynamic Programming、Bit Manipulation、Memoization、Bitmask · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-groups-getting-fresh-donuts/)

---

## 题目（英文原版）

**Description**

There is a donuts shop that bakes donuts in batches of batchSize. They have a rule where they must serve all of the donuts of a batch before serving any donuts of the next batch. You are given an integer batchSize and an integer array groups, where groups[i] denotes that there is a group of groups[i] customers that will visit the shop. Each customer will get exactly one donut.
When a group visits the shop, all customers of the group must be served before serving any of the following groups. A group will be happy if they all get fresh donuts. That is, the first customer of the group does not receive a donut that was left over from the previous group.
You can freely rearrange the ordering of the groups. Return the maximum possible number of happy groups after rearranging the groups.

**Examples**

**Example 1:**

```
Input: batchSize = 3, groups = [1,2,3,4,5,6]
Output: 4
Explanation: You can arrange the groups as [6,2,4,5,1,3]. Then the 1st, 2nd, 4th, and 6th groups will be happy.
```

**Example 2:**

```
Input: batchSize = 4, groups = [1,3,2,5,2,2,1,6]
Output: 4
```

**Constraints**

- 1 <= batchSize <= 9
- 1 <= groups.length <= 30
- 1 <= groups[i] <= 109

---

## 题目（中文翻译）

有一家甜甜圈店一次烤制 **batchSize** 个甜甜圈，称为一批。店内有一条规则：必须在开始下一批甜甜圈之前，先把当前批次的所有甜甜圈全部送完。给定整数 **batchSize** 和整数数组 **groups**，其中 `groups[i]` 表示有一组 `groups[i]` 位顾客会光顾店铺。每位顾客恰好吃一个甜甜圈。

当一组顾客来到店铺时，必须在为该组的所有顾客服务完毕后，才能开始为后面的组服务。如果该组的第一位顾客没有收到前一组剩余的甜甜圈，即该组的所有顾客都吃到新烤的甜甜圈，则该组被认为是 **happy**（快乐）的。

你可以自由地重新排列各组的到访顺序。返回重新排列后，最多可以有多少个快乐组。

Example 1:
Input: batchSize = 3, groups = [1,2,3,4,5,6]
Output: 4
Explanation: 你可以将组的顺序安排为 [6,2,4,5,1,3]。这样第 1、2、4、6 组都会是快乐的。

Example 2:
Input: batchSize = 4, groups = [1,3,2,5,2,2,1,6]
Output: 4

约束条件：
- 1 <= batchSize <= 9
- 1 <= groups.length <= 30
- 1 <= groups[i] <= 10^9

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：把 **所有** 组的顺序全部枚举出来（全排列），然后逐个模拟店员发甜甜圈的过程，统计有多少组是“开心的”。  

- **数据结构**：我们只需要一个普通的列表 `order` 保存当前的排列顺序。  
- **生活化类比**：把每个顾客想象成排队买电影票的人，`batchSize` 就是一次只能放进去的座位数。我们要把所有人排成一列，看看每次坐满一排后，下一排的第一个人是否坐在全新的座位上。  
- **正确性**：遍历所有可能的顺序，必然会覆盖最优的那一种，所以答案一定能在枚举的结果里找到。  

> **为什么会慢**：  
> - 组数 `n` 最多 30，`n!`（阶乘）在 n=10 时已经是 3.6 M，n=12 时就爆炸到 479 M，根本不可算。  

#### 代码（Python）  

```python
from itertools import permutations
from typing import List

def maxHappyGroups_bruteforce(batchSize: int, groups: List[int]) -> int:
    # 直接把每个组的大小取模，方便后面判断是否能整除
    mods = [g % batchSize for g in groups]

    best = 0
    # 枚举所有排列（这里仅作演示，实际会超时）
    for order in permutations(mods):
        cur = 0          # 当前批次已经使用的甜甜圈数量（模 batchSize）
        happy = 0        # 统计开心的组数
        for m in order:
            # 如果当前批次剩余为 0，说明本组的第一个人能得到全新甜甜圈
            if cur == 0:
                happy += 1
            # 把本组的顾客数加进去，然后取模，得到下一个批次的剩余
            cur = (cur + m) % batchSize
        best = max(best, happy)

    return best
```

> **关键行中文注释** 已写在代码里。

#### 复杂度  

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是所有排列的数量，`n` 是遍历每个排列时的线性扫描。  
  - 用大白话说，就是“先把所有可能的排队方式全部列出来，然后每一种都要检查一次”。  
- **空间复杂度**：`O(n)`  
  - 只需要存放当前排列和几个计数变量。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**顺序本身并不重要**，真正影响“开心”与否的是每个组对 `batchSize` 的余数。  

1. **先把余数为 0 的组直接算进去**  
   - 余数 0 的组不管什么时候来，都是开心的，因为它们恰好把上一批次吃完。  

2. **统计其余组的余数分布**  
   - 设 `freq[i]` 为余数为 `i`（`1 ≤ i < batchSize`）的组的数量。  
   - 这一步相当于把“每个组的大小”压缩成“几种颜色的珠子有多少”。  

3. **动态规划 + 记忆化搜索**  
   - **状态**：`dp(freq_tuple, cur)`  
     - `freq_tuple`：长度为 `batchSize` 的元组，记录每种余数还剩多少组（把列表变成不可变的元组，方便做哈希键）。  
     - `cur`：当前已经累加的余数（相当于上一批次剩下的甜甜圈数）。范围 `0 … batchSize-1`。  
   - **意义**：从当前状态出发，最多还能再形成多少个“完整批次”。当 `cur == 0` 时，说明刚好可以把前面选的组凑成一个完整的批次，这个批次的第一个组会开心，计数 +1。  

4. **转移**  
   - 对每一种余数 `i`（`1 … batchSize-1`），如果 `freq[i] > 0`，就挑选一个余数为 `i` 的组放在当前批次的后面。  
   - 新的余数 `next_cur = (cur + i) % batchSize`。  
   - 把 `freq[i]` 减 1，递归求子问题的最优值。  

5. **记忆化**  
   - 由于 `batchSize ≤ 9`，余数种类最多 8 种，每种余数的出现次数不超过 30，状态空间是有限且相对较小的。我们用 `@lru_cache` 把已经算过的 `(freq_tuple, cur)` 记下来，避免重复计算。  

6. **答案**  
   - 初始的 `cur` 为 0（因为还没有任何剩余）。  
   - 再加上所有余数为 0 的组的数量，得到最终的最大开心组数。  

> **类比**：把每个余数想象成不同颜色的积木，`cur` 表示当前堆的“高度”。每次放一块积木后，若恰好把高度凑满（`cur==0`），就算一次“成功的搭建”。  

#### 代码（Python）  

```python
from functools import lru_cache
from typing import List, Tuple

def maxHappyGroups(batchSize: int, groups: List[int]) -> int:
    # 1️⃣ 统计余数为 0 的组，它们一定开心
    base_happy = sum(1 for g in groups if g % batchSize == 0)

    # 2️⃣ 统计其余组的余数分布
    freq = [0] * batchSize          # freq[i] 表示余数 i 的组数
    for g in groups:
        r = g % batchSize
        if r != 0:
            freq[r] += 1

    # 3️⃣ 动态规划 + 记忆化
    @lru_cache(None)
    def dp(state: Tuple[int, ...], cur: int) -> int:
        """
        state : 长度为 batchSize 的元组，记录每种余数还剩多少组
        cur   : 当前批次已经累加的余数（0~batchSize-1）
        返回   : 从此状态出发，最多还能再形成多少个完整批次
        """
        # 如果所有组都已经用完，返回 0（没有更多完整批次）
        if sum(state) == 0:
            return 0

        best = 0
        # 尝试挑选每一种余数的组作为下一个加入的组
        for i in range(1, batchSize):
            if state[i] == 0:          # 没有余数 i 的组可以选
                continue
            # 构造下一个状态：把余数 i 的计数减 1
            nxt_state = list(state)
            nxt_state[i] -= 1
            nxt_state = tuple(nxt_state)

            # 计算放入余数 i 的组后新的 cur
            nxt_cur = (cur + i) % batchSize

            # 递归求子问题的最优值
            add = 1 if nxt_cur == 0 else 0   # 若恰好凑满一批，则多出一个开心的组
            best = max(best, add + dp(nxt_state, nxt_cur))

        return best

    # 初始状态：freq 转成元组，cur 为 0
    ans = dp(tuple(freq), 0)

    # 4️⃣ 加上余数为 0 的组数，得到最终答案
    return base_happy + ans
```

**代码要点解释**  

| 行号 | 说明 |
|------|------|
| 5‑7  | 直接统计余数为 0 的组，这部分无需 DP，必然开心。 |
| 10‑13| 统计其余组的余数分布，`freq[r]` 表示余数 `r` 的出现次数。 |
| 17‑31| `dp` 函数是记忆化递归，`@lru_cache` 把已经算过的 `(state, cur)` 结果缓存。 |
| 22‑27| 对每一种还能取的余数 `i`，尝试把它放进当前批次，得到新的状态 `nxt_state` 和新的余数 `nxt_cur`。 |
| 28   | 如果放完后 `nxt_cur == 0`，说明刚好完成一个完整批次，当前组会开心，`add = 1`。 |
| 30   | 取所有可能选择中的最大值。 |
| 38   | 初始调用 `dp`，`cur = 0` 表示一开始没有剩余。 |
| 41   | 最终答案 = 直接开心的组 + DP 得到的额外开心组数。 |

#### 复杂度  

- **时间复杂度**：`O( batchSize * Π (freq[i] + 1) )`  
  - `Π (freq[i] + 1)` 是所有余数计数的组合数，上限约为 `9^30` 但实际远小，因为 `batchSize ≤ 9`，每种余数的总和不超过 30，状态数大约在几万到十几万之间，能够在毫秒级完成。  
  - 用大白话说，就是“我们把所有可能的剩余组合（每种颜色的积木还有多少）都遍历一次”，而不是遍历所有排列。  

- **空间复杂度**：`O( Π (freq[i] + 1) )`（缓存表的大小） + 递归栈深度 `O(total_groups)`。  
  - 由于使用的是哈希表缓存，实际占用的内存也在几 MB 以内。  

---

## 心得  

- **核心技巧**：把每个组的大小只保留模 `batchSize` 的余数，并用「余数计数 + 当前剩余」的 DP 进行记忆化搜索。  
- **适用的题型**  
  1. **分组配对**：如 LeetCode 1723 “完成所有工作的最短时间”，需要把任务按余数划分后 DP。  
  2. **状态压缩 DP**：如 LeetCode 1125 “最小的正整数除法”，使用余数/计数的方式进行搜索。  
- **一句话总结**：**把问题抽象成“余数的配对”，用记忆化 DP 把“剩余的甜甜圈数”当作状态，即可在指数级的搜索空间中快速找到最优解。**  

---

## 反思  

- **第一反应**：看到“必须把同一批次的甜甜圈吃完才能开始下一批”，立刻想到“模运算”和“余数”。  
- **最容易踩的坑**  
  - **忘记把余数为 0 的组直接计数**，导致 DP 里多余的状态，时间会不必要地膨胀。  
  - **状态哈希错误**：列表是可变的，不能直接做键；必须转换成元组或使用自定义编码。  
  - **递归深度**：如果直接用 `list` 复制而不做缓存，会导致指数级递归，栈溢出。  
- **下次遇到同类题**：第一步先把“关键的余数/模数信息”抽出来，看看是否能用「计数+当前余数」的 DP 来压缩状态，而不是枚举所有排列。