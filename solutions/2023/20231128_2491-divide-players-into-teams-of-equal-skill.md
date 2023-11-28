# #2491. 将玩家分成技能相等的队伍 / Divide Players Into Teams of Equal Skill

> 难度：中等 · 标签：Array、Hash Table、Two Pointers、Sorting · [LeetCode 链接](https://leetcode.com/problems/divide-players-into-teams-of-equal-skill/)

---

## 题目（英文原版）

**Description**

You are given a positive integer array skill of even length n where skill[i] denotes the skill of the ith player. Divide the players into n / 2 teams of size 2 such that the total skill of each team is equal.
The chemistry of a team is equal to the product of the skills of the players on that team.
Return the sum of the chemistry of all the teams, or return -1 if there is no way to divide the players into teams such that the total skill of each team is equal.

**Examples**

**Example 1:**

```
Input: skill = [3,2,5,1,3,4]
Output: 22
Explanation: 
Divide the players into the following teams: (1, 5), (2, 4), (3, 3), where each team has a total skill of 6.
The sum of the chemistry of all the teams is: 1 * 5 + 2 * 4 + 3 * 3 = 5 + 8 + 9 = 22.
```

**Example 2:**

```
Input: skill = [3,4]
Output: 12
Explanation: 
The two players form a team with a total skill of 7.
The chemistry of the team is 3 * 4 = 12.
```

**Example 3:**

```
Input: skill = [1,1,2,3]
Output: -1
Explanation: 
There is no way to divide the players into teams such that the total skill of each team is equal.
```

**Constraints**

- 2 <= skill.length <= 105
- skill.length is even.
- 1 <= skill[i] <= 1000

---

## 题目（中文翻译）

**题目描述**  
给定一个长度为偶数 `n` 的正整数数组 `skill`，其中 `skill[i]` 表示第 `i` 名玩家的技能值。将所有玩家分成 `n / 2` 支每支 2 人的队伍（team），要求每支队伍的 **总技能（total skill）** 相等。  
一支队伍的 **化学值（chemistry）** 等于该队伍两名玩家技能值的 **乘积（product）**。  
返回所有队伍化学值的总和，如果不存在一种划分方式能够使每支队伍的总技能相等，则返回 `-1`。

**示例**  

**示例 1**  
输入: `skill = [3,2,5,1,3,4]`  
输出: `22`  
解释:  
将玩家划分为以下队伍: `(1, 5)`, `(2, 4)`, `(3, 3)`，每支队伍的总技能均为 `6`。  
所有队伍的化学值之和为: `1 * 5 + 2 * 4 + 3 * 3 = 5 + 8 + 9 = 22`。

**示例 2**  
输入: `skill = [3,4]`  
输出: `12`  
解释:  
两名玩家组成一支队伍，总技能为 `7`。  
该队伍的化学值为 `3 * 4 = 12`。

**示例 3**  
输入: `skill = [1,1,2,3]`  
输出: `-1`  
解释:  
不存在一种划分方式能够使每支队伍的总技能相等。

**约束条件**  
- `2 <= skill.length <= 10^5`  
- `skill.length` 为偶数  
- `1 <= skill[i] <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把所有玩家两两组合」——把数组 `skill` 中的每一对玩家都拿出来算一下，看能否把所有玩家恰好分成若干个 **总技能相同** 的二人小组。  
实现思路可以如下：

1. 先遍历所有可能的配对方式（组合），把每一种配对方案记下来。  
2. 对每一种配对方案，检查所有小组的 `skill[i] + skill[j]` 是否相等。  
3. 若相等，则把每组的化学值 `skill[i] * skill[j]` 加总返回；否则继续尝试下一种配对方式。  
4. 所有配对方式都试完仍找不到合法方案，返回 `-1`。

> **类比**：把配对过程想象成在一本大词典里找“搭配”。我们把每个人的技能当成词，想找出所有两两搭配的组合，就像在词典里把每个词和其他词配对。

**为什么正确**  
暴力枚举把「所有可能的分组」都列举出来，只要答案存在，就一定能在枚举的过程中被发现。因此只要实现不出错，答案必然正确。

**时间/空间复杂度**  
- 设玩家人数为 `n`（一定为偶数），要把 `n` 个人两两配对，需要把 `n` 个人分成 `n/2` 组。所有可能的配对方式数量是 **超指数级** 的（Catalan 数），直接枚举的时间复杂度大约是 `O((n-1)!!) ≈ O(n!!) ≈ O(n·(n-2)·(n-4)… )`，即 **指数级**，在最坏情况下会爆炸。  
- 为了保存当前的配对方案，需要额外的数组或列表，空间复杂度是 `O(n)`（保存一套配对），但由于递归深度最多 `n/2`，同样是线性空间。

> 用大白话说，`O(n²)` 代表「把每个人和每个人都比一遍」，而这里的复杂度比 `O(n²)` 还要大得多，几乎是「把所有可能的配对方式都列出来」——根本不可行。

#### 代码（Python）

```python
from itertools import combinations
from typing import List

def brute_force(skill: List[int]) -> int:
    n = len(skill)
    # 用一个布尔数组记录哪些玩家已经被配对
    used = [False] * n
    # 记录当前已经形成的团队总技能（第一个团队的总技能即为目标值）
    target = None
    # 记录所有团队的化学值之和
    total_chem = 0

    # 递归尝试配对
    def dfs(pair_cnt: int, cur_sum: int) -> int:
        nonlocal target, total_chem
        # 已配对完所有玩家
        if pair_cnt == n // 2:
            return cur_sum          # 成功返回化学值之和

        # 找到第一个未使用的玩家 i
        i = 0
        while i < n and used[i]:
            i += 1
        used[i] = True

        # 把 i 和后面的每个未使用玩家 j 配对尝试
        for j in range(i + 1, n):
            if used[j]:
                continue
            used[j] = True
            team_skill = skill[i] + skill[j]
            team_chem  = skill[i] * skill[j]

            # 第一次配对确定目标总技能
            if target is None:
                target = team_skill
                if dfs(pair_cnt + 1, cur_sum + team_chem) != -1:
                    return cur_sum + team_chem
                target = None
            else:
                # 必须和目标总技能相等才能继续
                if team_skill == target:
                    if dfs(pair_cnt + 1, cur_sum + team_chem) != -1:
                        return cur_sum + team_chem

            used[j] = False   # 回溯

        used[i] = False       # 回溯
        return -1

    return dfs(0, 0)
```

> 这段代码 **只能在极小规模**（比如 `n ≤ 10`）下跑得通，因为它会尝试所有配对组合。

#### 复杂度

- **时间复杂度**：`O((n-1)!!)`（超指数级），实际运行时间随 `n` 增长几乎是爆炸式的。  
- **空间复杂度**：`O(n)`，主要是递归栈和 `used` 数组的存储。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到，**瓶颈** 在于「枚举所有配对」——这一步把时间压到了指数级。我们需要找到一种 **直接决定配对方式** 的方法，而不是盲目尝试。

观察题目：

- 每支队伍的 **总技能** 必须相同，记为 `S`。  
- 如果把所有玩家的技能从小到大排好序，最小的玩家 `a` 必须找一个 **最大的** 玩家 `b` 配对，使得 `a + b = S`。因为如果把最小的 `a` 和一个不是最大的 `c`（`c < b`）配对，那么 `a + c < a + b = S`，导致无法再让剩下的玩家凑出同样的 `S`（剩下的最大玩家 `b` 必须和更大的玩家配对，但已经没有更大的了）。

> **类比**：把最弱的选手想象成“最轻的砝码”，把最强的选手想象成“最重的砝码”。要让每对砝码的总重量相等，唯一的办法就是把最轻的和最重的配对，其余的再依次这样配。

因此，**排序 + 双指针** 就能一次性得到唯一的配对方案：

1. 将 `skill` 排序得到 `sorted_skill`。  
2. 设左指针 `l = 0`（指向最小），右指针 `r = n-1`（指向最大）。  
3. 计算目标总技能 `target = sorted_skill[l] + sorted_skill[r]`（第一次配对决定 `S`）。  
4. 每次把 `sorted_skill[l]` 与 `sorted_skill[r]` 配对，检查它们的和是否仍等于 `target`。若不等，说明无法满足条件，直接返回 `-1`。  
5. 若相等，则把它们的化学值 `sorted_skill[l] * sorted_skill[r]` 加入答案。随后 `l += 1, r -= 1`，继续配对。  
6. 当左指针超过右指针时，所有玩家均已配对完毕，返回累计的化学值。

**核心数据结构**：

- **数组排序**（`list.sort()`）：把玩家按技能从小到大排列，时间复杂度 `O(n log n)`。  
- **双指针**：一次遍历数组，两端向中间收拢，时间复杂度 `O(n)`。

#### 代码（Python）

```python
from typing import List

def dividePlayers(skill: List[int]) -> int:
    """
    将玩家两两配对，使每队的总技能相同。
    若不可行返回 -1，否则返回所有队伍化学值之和。
    """
    skill.sort()                     # 1. 按技能从小到大排序
    n = len(skill)
    left, right = 0, n - 1           # 2. 双指针分别指向最小和最大
    target = skill[left] + skill[right]   # 3. 第一次配对决定目标总技能 S
    total_chem = 0                   # 累计化学值

    while left < right:
        cur_sum = skill[left] + skill[right]
        if cur_sum != target:        # 4. 若出现不等，说明无解
            return -1
        total_chem += skill[left] * skill[right]   # 5. 累加化学值
        left += 1                    # 移动指针，准备配下一个最小/最大
        right -= 1

    return total_chem                # 6. 所有配对成功，返回答案
```

> **代码要点**  
- `skill.sort()` 用原地排序，省去额外的空间。  
- `left < right` 保证每次配对恰好两个不同的玩家。  
- 只要一次出现不等，就可以提前结束，避免不必要的计算。

#### 复杂度

- **时间复杂度**：`O(n log n)`。排序是主要耗时，`n ≤ 10⁵` 时完全可接受。  
- **空间复杂度**：`O(1)`（不计排序使用的原地交换空间），只用了常数级的额外变量。

> 与暴力解相比，时间从「指数级」降到了「对数线性」，即使是最大规模的输入也能在毫秒级完成。

---

## 心得

- **核心技巧**：先排序，再用 **双指针** 把最小和最大配对，保证每对的和相同。  
- **适用题型**  
  1. “配对使每组和相等” 类题，如 **`Two Sum`** 的变形、**`Array Partition I`**。  
  2. 需要 **最小-最大配对** 的问题，例如 “最大化配对的乘积” 或 “最小化配对的绝对差”。  
- **一句话总结**：**把最弱和最强配对**，一次遍历即可得到唯一合法方案。

---

## 反思

- **第一反应**：想到枚举所有配对，直接暴力搜索。  
- **最容易踩的坑**  
  - 忘记先检查总和是否一致，导致后面配对时出现不等却仍继续计算。  
  - 对奇数长度的数组没有提前返回，导致指针相遇后仍尝试配对。  
  - 误以为只要配对成功就一定是最优解，实际上排序+双指针本身就是唯一可行解。  
- **下次遇到同类题**：第一步先 **排序**，再 **用双指针** 思考“最小+最大”是否能满足全局约束；若不行，直接返回 `-1`，否则累计所需的结果。