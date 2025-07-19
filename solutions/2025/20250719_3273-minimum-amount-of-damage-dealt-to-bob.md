# #3273. Bob 所受的最小伤害总量 / Minimum Amount of Damage Dealt to Bob

> 难度：困难 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-amount-of-damage-dealt-to-bob/)

---

## 题目（英文原版）

**Description**

You are given an integer power and two integer arrays damage and health, both having length n.
Bob has n enemies, where enemy i will deal Bob damage[i] points of damage per second while they are alive (i.e. health[i] > 0).
Every second, after the enemies deal damage to Bob, he chooses one of the enemies that is still alive and deals power points of damage to them.
Determine the minimum total amount of damage points that will be dealt to Bob before all n enemies are dead.

**Examples**

**Example 1:**

```
Input: power = 4, damage = [1,2,3,4], health = [4,5,6,8]
Output: 39
Explanation:
```

**Example 2:**

```
Input: power = 1, damage = [1,1,1,1], health = [1,2,3,4]
Output: 20
Explanation:
```

**Example 3:**

```
Input: power = 8, damage = [40], health = [59]
Output: 320
```

**Constraints**

- 1 <= power <= 104
- 1 <= n == damage.length == health.length <= 105
- 1 <= damage[i], health[i] <= 104

---

## 题目（中文翻译）

你得到一个整数 `power` 和两个整数数组（array）`damage` 与 `health`，它们的长度均为 `n`。  
Bob 有 `n` 个敌人，其中第 `i` 个敌人在存活期间（即 `health[i] > 0`）会每秒对 Bob 造成 `damage[i]` 点伤害。  
每秒结束时，在敌人对 Bob 造成伤害之后，Bob 可以选择一个仍然存活的敌人，对其造成 `power` 点伤害。  
求在所有 `n` 个敌人全部死亡之前，Bob 所受到的伤害点数的**最小可能总和**。

**示例 1：**  
输入: `power = 4, damage = [1,2,3,4], health = [4,5,6,8]`  
输出: `39`  
解释：

**示例 2：**  
输入: `power = 1, damage = [1,1,1,1], health = [1,2,3,4]`  
输出: `20`  
解释：

**示例 3：**  
输入: `power = 8, damage = [40], health = [59]`  
输出: `320`  
解释：

**约束条件：**
- `1 <= power <= 10^4`
- `1 <= n == damage.length == health.length <= 10^5`
- `1 <= damage[i], health[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有可能的击杀顺序** 全部列举出来，逐个模拟战斗过程，算出每种顺序对应的总伤害，最后取最小值。

- **数据结构**  
  - `list`：保存每个敌人的 `damage[i]`、`health[i]`。  
  - `itertools.permutations`：把 `n` 个敌人全部排成 `n!` 种不同的顺序，类似把词典里所有单词的排列都写出来（字典的每一页对应一种排列）。
- **为什么正确**  
  - 因为我们把**所有**可能的顺序都算了一遍，必然能找到最优的那一个。  
- **复杂度分析（大白话）**  
  - 枚举 `n!`（n 的阶乘）种顺序：  
    - 当 `n=5` 时，`5! = 120`，还能接受；  
    - 当 `n=10` 时，`10! ≈ 3.6 百万`，已经慢得不行；  
    - 当 `n=20` 时，`20!` 天文数字，根本不可行。  
  - 对每一种顺序我们还要 **逐秒模拟**，最坏情况下要跑 `Σ ceil(health[i]/power)` 秒，约 `O(n·maxHealth/power)`。  
  - 综合下来时间复杂度是 **O(n!·n)**，空间只需要保存几个数组，**O(n)**。

> 用大 O 表示的 `O(n!·n)`，可以想象成“先把所有排列都写出来，再每个排列都跑一遍”。在实际面试里，这种做法只适合 `n ≤ 8` 的玩具题。

#### 代码（Python）

```python
import itertools
from math import ceil
from typing import List

def brute_force(power: int, damage: List[int], health: List[int]) -> int:
    """只用于 n 很小的情况，枚举所有击杀顺序求最小总伤害"""
    n = len(damage)
    # 预先算好每个敌人需要多少次攻击才能死亡
    need = [ceil(h / power) for h in health]          # 每个敌人的“处理时间”

    best = float('inf')
    # permutations 会返回所有可能的下标排列，如 (0,1,2) (0,2,1) ...
    for order in itertools.permutations(range(n)):
        cur_time = 0          # 已经过去的秒数
        total = 0             # 当前排列累计的伤害
        for idx in order:
            # 这个敌人在 cur_time+need[idx] 秒后死亡
            finish = cur_time + need[idx]
            total += damage[idx] * finish           # 该敌人对 Bob 的总伤害
            cur_time = finish                       # 时间前进
        best = min(best, total)
    return best
```

> 代码里每一行都加了中文注释，帮助初学者快速看懂。**请勿在 n 大于 8 时使用**，会卡死。

#### 复杂度

- **时间复杂度**：`O(n!·n)`  
  - “阶乘”增长速度非常快，实际只能在极小规模（n≤8）下跑得完。  
- **空间复杂度**：`O(n)`  
  - 只存几个长度为 n 的数组和递归栈（`itertools` 内部实现）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**顺序**是唯一决定答案的因素。我们要找出一种 **快速比较两位敌人先后顺序的规则**，把所有敌人按这个规则排好序后，直接算出答案。

---

##### 2.1 把战斗抽象成 “作业调度”

- 每秒钟 **先** 受到所有存活敌人的伤害 → 相当于 **每秒都有一个固定的成本**，这个成本是所有还活着的 `damage` 之和。  
- 然后 **选一个敌人攻击** → 相当于 **在机器上处理一个任务**，一次攻击只能对一个敌人。

对第 `i` 个敌人：

| 属性 | 含义 | 类比 |
|------|------|------|
| `health[i]` | 需要削掉的血量 | 任务的“工作量” |
| `power` | 每秒能削掉的血量 | 机器一次能做的工作 |
| `ceil(health[i]/power)` | 把该敌人干掉需要的秒数 | **处理时间** `p_i` |
| `damage[i]` | 每秒对 Bob 的伤害 | **权重** `w_i`（每秒的“费用”） |

**关键观察**：如果第 `i` 个敌人在第 `t` 秒仍然活着，它会让 Bob 在这秒受到 `damage[i]` 点伤害。于是 **第 `i` 个敌人对总伤害的贡献 = `damage[i] * (它死亡的时间)`**。

设 `C_i` 为敌人 `i` 死亡的秒数（即它在第 `C_i` 秒结束攻击后不再造成伤害），则

```
总伤害 = Σ damage[i] * C_i
```

这正是经典的 **单机加权完工时间最小化**（min Σ w_i·C_i）问题。

---

##### 2.2 斯密斯规则（Smith’s Rule）

在单机调度里，**要想让 Σ w_i·C_i 最小**，只需要把任务按 **“单位时间产生的费用”** 从大到小排序：

```
先处理  w_i / p_i  较大的任务
```

等价写法（避免除法的精度问题）：

```
对于 i, j 两个任务：
如果 w_i * p_j > w_j * p_i，则 i 应该排在 j 前面
```

在本题中：

- `w_i = damage[i]`
- `p_i = ceil(health[i] / power)`

所以比较两个敌人 `i`、`j` 时，只需要比较  

```
damage[i] * ceil(health[j]/power)   与   damage[j] * ceil(health[i]/power)
```

把所有敌人 **按上述比较结果从大到小排序**，得到的顺序一定是最优的。

---

##### 2.3 计算答案

排序完成后，只需一次遍历：

```
cur = 0               # 已经过去的秒数
ans = 0
for each enemy in sorted order:
    need = ceil(health / power)      # 需要多少秒杀死它
    cur += need                      # 它的死亡时间 = cur
    ans += damage * cur              # 累加它的贡献
return ans
```

---

##### 2.4 为什么贪心有效（再说一次）  

- 我们把每个敌人抽象成「处理时间」`p_i` 和「每秒费用」`w_i`。  
- 目标是 **最小化所有费用随时间累计的总和**。  
- 斯密斯规则在数学上可以证明：若两项顺序相反，则交换后总和必然不增（用交换论证），所以按 `w_i/p_i` 降序排列是全局最优。  
- 这里的 `w_i/p_i` 正好是 **“每秒能造成多少伤害”**（越大越应该先干掉），这跟直觉完全一致：先把“伤害大、血量少”的敌人先解决。

---

#### 代码（Python）

```python
from math import ceil
from typing import List

def minimum_damage(power: int, damage: List[int], health: List[int]) -> int:
    """
    最优解：先把每个敌人算出需要多少次攻击（处理时间），
    然后按 damage / need 的比值从大到小排序（斯密斯规则），
    最后一次遍历累加答案。
    """
    n = len(damage)

    # 1️⃣ 计算每个敌人需要的攻击次数（处理时间）
    need = [ceil(h / power) for h in health]      # p_i

    # 2️⃣ 按 “damage / need” 降序排序
    # 为避免浮点除法，用交叉相乘比较大小
    idx = list(range(n))
    idx.sort(key=lambda i: (-damage[i] / need[i]))   # 直接用除法也可以，Python 的 float 足够精确
    # 若想完全避免除法，可改写为：
    # idx.sort(key=lambda i: (damage[i], need[i]), reverse=True)   # 这里不等价，下面给出交叉比较实现

    # 下面是完全整数比较的写法（推荐）
    # idx.sort(key=lambda i: (damage[i], need[i]), reverse=False)  # 先不排序，后面手动比较

    # 3️⃣ 依次累加总伤害
    cur_time = 0          # 已经过去的秒数
    total = 0
    for i in idx:
        cur_time += need[i]                # 敌人 i 的死亡时间
        total += damage[i] * cur_time      # 贡献 = 每秒伤害 * 存活秒数
    return total
```

> **关键行中文注释**  
> - `need = [ceil(h / power) for h in health]` # 每个敌人需要的攻击次数  
> - `idx.sort(...)` # 按 “每秒伤害 / 需要秒数” 从大到小排序（斯密斯规则）  
> - `cur_time += need[i]` # 累计已经过去的时间，等于该敌人死亡的秒数  
> - `total += damage[i] * cur_time` # 该敌人对 Bob 造成的累计伤害

> 如果担心浮点数比较产生微小误差，可以改为 **交叉相乘** 的方式：

```python
def cmp(i, j):
    # 返回 True 表示 i 应该排在 j 前面
    return damage[i] * need[j] > damage[j] * need[i]

# Python3 中没有 cmp 参数，使用 functools.cmp_to_key
import functools
idx.sort(key=functools.cmp_to_key(lambda a, b: -1 if cmp(a, b) else (1 if cmp(b, a) else 0)))
```

---

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 计算 `need` 是 `O(n)`，排序是 `O(n log n)`，遍历一次求和是 `O(n)`。  
  - 与暴力的 `O(n!·n)` 相比，几乎瞬间完成，即使 `n=10⁵` 也能在 1 秒左右跑完。  
- **空间复杂度**：`O(n)`  
  - 需要保存 `need`、`idx` 两个长度为 `n` 的数组，以及常数级的临时变量。

---

## 心得

- **核心技巧**：把“每秒受到的伤害”视为任务的 **权重**，把“需要的攻击次数”视为任务的 **处理时间**，于是问题转化为 **单机加权完工时间最小化**，使用 **斯密斯规则（按 w/p 降序）** 贪心即可得到最优顺序。
- **适用的题型**（类似思路）  
  1. “任务调度”类：最小化 Σ w_i·C_i（例如 LeetCode 1834、1856）。  
  2. “先攻击哪只怪物”类：每只怪物有不同的血量与每秒伤害（比如《怪物消除》系列）。  
  3. “选购商品”类：每件商品的价值/重量比决定先买哪件（背包的贪心变体）。
- **一句话总结解题钥匙**：**“每秒伤害大的、血量少的先干掉”**，用 `damage[i] / ceil(health[i]/power)` 排序即可。

---

## 反思

- **第一反应**：先想枚举所有顺序，或者尝试动态规划——但很快会发现状态空间爆炸。  
- **最容易踩的坑**  
  - **向上取整**：`ceil(health/power)` 必须使用 `(health + power - 1) // power`，否则会少算一次攻击导致错误。  
  - **整数比较**：直接用浮点除法排序在大数据下仍然安全，但理论上可能出现精度误差，交叉相乘更稳妥。  
  - **大数溢出**：答案可能超过 32 位整数范围，一定要使用 Python 的大整数（默认）或在其他语言中用 `long long`。  
- **下次遇到同类题**：第一步先把每个对象抽象成「处理时间」和「每单位时间的代价」，检查是否可以套用 **加权完工时间最小化** 的贪心（斯密斯规则）框架。这样往往能立刻把暴力的指数时间压缩到 `O(n log n)`。