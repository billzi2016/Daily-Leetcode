# #3207. 敌人战斗后的最大积分 / Maximum Points After Enemy Battles

> 难度：中等 · 标签：Array、Greedy · [LeetCode 链接](https://leetcode.com/problems/maximum-points-after-enemy-battles/)

---

## 题目（英文原版）

**Description**

You are given an integer array enemyEnergies denoting the energy values of various enemies.
You are also given an integer currentEnergy denoting the amount of energy you have initially.
You start with 0 points, and all the enemies are unmarked initially.
You can perform either of the following operations zero or multiple times to gain points:
Return an integer denoting the maximum points you can get in the end by optimally performing operations.

**Examples**

**Example 1:**

```
Input: enemyEnergies = [3,2,2], currentEnergy = 2
Output: 3
Explanation:
The following operations can be performed to get 3 points, which is the maximum:
```

**Example 2:**

```
Input: enemyEnergies = [2] , currentEnergy = 10
Output: 5
Explanation:
Performing the first operation 5 times on enemy 0 results in the maximum number of points.
```

**Constraints**

- 1 <= enemyEnergies.length <= 105
- 1 <= enemyEnergies[i] <= 109
- 0 <= currentEnergy <= 109

---

## 题目（中文翻译）

你得到一个整数数组 **enemyEnergies**，用于表示各个敌人的能量值。  
同时给定一个整数 **currentEnergy**，表示你初始拥有的能量。  
你从 **0 分** 开始，所有敌人初始均为未标记状态。  
你可以零次或多次执行下列两种操作中的任意一种以获取积分：  

（此处应列出两种操作的具体描述，原题中已给出）

返回一个整数，表示通过合理地执行上述操作，你最终能够获得的 **最大积分**。

**示例 1**  
```
Input: enemyEnergies = [3,2,2], currentEnergy = 2
Output: 3
Explanation:
可以通过以下操作获得 3 分，这是能够得到的最大分数：
```

**示例 2**  
```
Input: enemyEnergies = [2], currentEnergy = 10
Output: 5
Explanation:
对敌人 0 执行第一次操作 5 次即可获得最大积分。
```

**约束条件**  

- `1 <= enemyEnergies.length <= 10^5`  
- `1 <= enemyEnergies[i] <= 10^9`  
- `0 <= currentEnergy <= 10^9`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

题目给出一串敌人的能量 `enemyEnergies`，以及我们最初拥有的能量 `currentEnergy`。  
每一次我们 **可以对任意一个还没有标记的敌人** 做下面两种操作之一：

1. **战斗**  
   - 前提：`currentEnergy >= enemyEnergies[i]`  
   - 结果：得到 **1 分**，并 **消耗** `enemyEnergies[i]` 点能量（`currentEnergy -= enemyEnergies[i]`）。

2. **标记**  
   - 直接把这个敌人标记为 “已标记”。  
   - 结果：**不增加分数**，但 **获得** `enemyEnergies[i]` 点能量（`currentEnergy += enemyEnergies[i]`）。

> **类比**：把 “标记” 想成在字典里查词。字典的 **key** 是敌人的能量，**value** 是我们能从它那里“借到”的能量。  
> 把 “战斗” 想成在超市买东西，需要付出等价的金钱（能量），但可以换取一张优惠券（1 分）。

暴力的想法就是：**枚举所有可能的操作顺序**，把每一种顺序都跑一遍，记录能得到的最高分。  
因为每一次我们都有两种选择（战斗 / 标记），且每个敌人可以被操作任意次（标记一次后就不能再标记，战斗可以在有足够能量时反复进行），  
这相当于是 **指数级** 的搜索空间。

虽然暴力一定能得到正确答案（遍历完所有可能必然能找到最优），但它的运行时间会随着敌人数目爆炸式增长，根本不可接受。

#### 代码（Python）

```python
from itertools import product

def brute_force(enemyEnergies, currentEnergy):
    n = len(enemyEnergies)
    best = 0

    # 用一个位掩码表示哪些敌人已经被标记（1 表示已标记）
    # 为了演示，这里只遍历「标记」的子集，随后在每个子集里无限次“战斗”
    for mask in range(1 << n):
        energy = currentEnergy
        points = 0
        # 先执行所有标记操作
        for i in range(n):
            if mask >> i & 1:          # 第 i 个敌人被标记
                energy += enemyEnergies[i]

        # 接下来尽可能多地对所有敌人进行战斗
        # 为了简化，这里直接把每个敌人能战斗的次数算出来
        for i in range(n):
            if enemyEnergies[i] == 0:  # 防止除 0
                continue
            # 能战斗的次数 = 当前能量 / 消耗的能量
            cnt = energy // enemyEnergies[i]
            points += cnt
            energy -= cnt * enemyEnergies[i]   # 其实这里不影响后面的计数，只是演示

        best = max(best, points)

    return best
```

> **注意**：上述代码仅用于说明暴力思路，实际运行会在 `n≈20` 时就超时。

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - `2^n` 表示遍历所有可能的标记子集（每个敌人要么标记要么不标记），  
  - 对每个子集我们还要遍历 `n` 次来计算能量和分数。  
  - 用大白话说，就是**每多一个敌人，可能的情况就会翻倍**，所以只能在极小规模下使用。

- **空间复杂度**：`O(1)`（只用常数级的额外变量）。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**标记** 的唯一作用是 **把敌人的能量加到我们手里**，而 **战斗** 则是 **用能量换取 1 分**。  
所以整个过程本质上是一场 **“能量的进出”**，我们希望用尽可能少的能量换取尽可能多的分数。

**关键观察**：

1. **标记的顺序不影响最终能量**。  
   - 标记只会把对应的 `enemyEnergies[i]` 加到 `currentEnergy` 中，顺序随意。  
   - 因此我们可以一次性把所有想标记的敌人的能量相加，直接得到新的 `currentEnergy`。

2. **标记的对象应该是“除最小值之外的所有敌人”。**  
   - 把 **最小的能量** 留给 **战斗**（因为它消耗最少的能量，能让我们获得最多次的 1 分）。  
   - 其它更大的敌人如果直接用来战斗，会一次性消耗大量能量，导致后面还能战斗的次数大幅下降。  
   - 把这些大能量的敌人全部 **标记**，把它们的能量一次性塞进我们的口袋，等我们有足够的能量后再用 **最小的敌人** 来不断“买”分数。

3. **只要我们手里还有能量，就可以无限次对最小的敌人进行战斗**。  
   - 每一次战斗消耗 `minEnergy`，得到 1 分。  
   - 只要 `currentEnergy // minEnergy`（整除）不为 0，我们就还能再战斗一次。  

综上，**最优策略** 可以简化为：

1. 找到数组中的最小能量 `minE`（如果有多个，只保留一个，其他的视作“大能量”可以直接标记）。  
2. 把 **除一个 `minE` 之外的所有敌人** 全部标记，累加它们的能量到 `currentEnergy`。  
3. 最后，用 `currentEnergy // minE` 次对这个最小敌人进行战斗，得到的次数即为最大分数。  

> **为什么这样一定最优？**  
> - 把所有“大能量”标记后，我们得到的总能量是 **所有能量的和减去一个 `minE`**。  
> - 只剩下最小的敌人可以用于战斗，每一次战斗都只消耗 `minE`，因此在同样的总能量下，使用最小消耗自然能完成 **最多次数** 的战斗。  
> - 任何把一个大能量用于战斗的做法，都必然把一次 `minE` 的战斗换成一次更昂贵的战斗，从而 **降低** 能完成的总次数。  

#### 代码（Python）

```python
from typing import List

def maxPoints(enemyEnergies: List[int], currentEnergy: int) -> int:
    """
    贪心解法
    1. 找到最小能量 minE
    2. 把除一个 minE 之外的所有敌人标记，累计能量
    3. 用 minE 进行尽可能多次的战斗，得到的次数即为答案
    """
    if not enemyEnergies:
        return 0

    # 1. 最小能量
    minE = min(enemyEnergies)

    # 2. 标记所有除了一个最小值之外的敌人
    #    计算总能量（所有能量的和）减去保留下来的那个最小值
    total_energy = sum(enemyEnergies) - minE
    currentEnergy += total_energy          # 标记后我们拥有的总能量

    # 3. 用最小能量尽可能多次战斗
    #    每一次战斗消耗 minE，得到 1 分
    points = currentEnergy // minE

    return points
```

> **代码说明（每行中文注释）**  
> ```python
> if not enemyEnergies:                # 没有敌人直接返回 0 分
>     return 0
> 
> minE = min(enemyEnergies)           # 找到最小的能量值
> 
> total_energy = sum(enemyEnergies) - minE   # 把除一个最小值之外的所有能量加在一起
> currentEnergy += total_energy               # 标记后得到的总能量
> 
> points = currentEnergy // minE   # 能量除以最小消耗，得到最多可以战斗的次数
> return points
> ```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只需要一次遍历找到最小值和求和，和 `n` 成线性关系。  
  - 用大白话说，就是 **“扫一遍数组”**，即使是 10⁵ 的数据也能在毫秒级完成。

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和数组大小无关。

---

## 心得

- **核心技巧**：**把“消耗最少的”资源留给“赚钱（得分）”，把“大块资源”全部先变成“资本（能量）”。**  
- 这种思路在很多“能量/金币/体力换奖励”的题目里都通用，例如  
  1. **LeetCode 1642. 通过指令获取最大钱数**（把收益大的指令先执行）  
  2. **LeetCode 1648. 销售价值的最大化**（先把价值大的商品卖出）  
  3. **LeetCode 2215. 找出两数组的最大异或值**（把大数先用于提升位权）  
- **一句话总结**：**把最大的“能量来源”先全部收进来，再用最省能的方式反复消费，得到的分数最多。**

---

## 反思

- **第一反应**：看到“标记”和“战斗”两个互斥操作，我第一时间想到要**枚举所有顺序**，于是写了暴力搜索。  
- **最容易踩的坑**  
  1. **忘记保留一个最小能量的敌人**：如果把所有敌人都标记，最后就没有可以战斗的对象，得分永远是 0。  
  2. **整数溢出**：`enemyEnergies[i]` 最高到 `10⁹`，数组长度到 `10⁵`，求和时必须使用 64 位整数（Python 自动处理，但在 C++/Java 中要注意 `long long`）。  
  3. **边界情况**：当 `currentEnergy` 本身已经足够大时，仍然要遵循同样的“保留最小、标记其余”策略，否则可能误把本已足够的能量浪费在不必要的标记上。  
- **下次思路**：一看到“把能量/资源转化为分数”并且有“标记/收集”这种可以一次性获取全部资源的操作，我会立刻考虑 **“先收集，再用最小单位消耗”** 的贪心模型，而不是直接尝试枚举。这样往往能在 `O(n)` 时间内得到最优答案。