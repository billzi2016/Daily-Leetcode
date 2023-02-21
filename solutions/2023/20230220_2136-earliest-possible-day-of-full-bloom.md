# #2136. **最早可能的全部盛开日** / Earliest Possible Day of Full Bloom

> 难度：困难 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/earliest-possible-day-of-full-bloom/)

---

## 题目（英文原版）

**Description**

You have n flower seeds. Every seed must be planted first before it can begin to grow, then bloom. Planting a seed takes time and so does the growth of a seed. You are given two 0-indexed integer arrays plantTime and growTime, of length n each:
From the beginning of day 0, you can plant the seeds in any order.
Return the earliest possible day where all seeds are blooming.

**Examples**

**Example 1:**

```
Input: plantTime = [1,4,3], growTime = [2,3,1]
Output: 9
Explanation: The grayed out pots represent planting days, colored pots represent growing days, and the flower represents the day it blooms.
One optimal way is:
On day 0, plant the 0th seed. The seed grows for 2 full days and blooms on day 3.
On days 1, 2, 3, and 4, plant the 1st seed. The seed grows for 3 full days and blooms on day 8.
On days 5, 6, and 7, plant the 2nd seed. The seed grows for 1 full day and blooms on day 9.
Thus, on day 9, all the seeds are blooming.
```

**Example 2:**

```
Input: plantTime = [1,2,3,2], growTime = [2,1,2,1]
Output: 9
Explanation: The grayed out pots represent planting days, colored pots represent growing days, and the flower represents the day it blooms.
One optimal way is:
On day 1, plant the 0th seed. The seed grows for 2 full days and blooms on day 4.
On days 0 and 3, plant the 1st seed. The seed grows for 1 full day and blooms on day 5.
On days 2, 4, and 5, plant the 2nd seed. The seed grows for 2 full days and blooms on day 8.
On days 6 and 7, plant the 3rd seed. The seed grows for 1 full day and blooms on day 9.
Thus, on day 9, all the seeds are blooming.
```

**Example 3:**

```
Input: plantTime = [1], growTime = [1]
Output: 2
Explanation: On day 0, plant the 0th seed. The seed grows for 1 full day and blooms on day 2.
Thus, on day 2, all the seeds are blooming.
```

**Constraints**

- n == plantTime.length == growTime.length
- 1 <= n <= 105
- 1 <= plantTime[i], growTime[i] <= 104

---

## 题目（中文翻译）

你有 `n` 颗花种子。每颗种子必须先种下才能开始生长，随后才会开花。种下一颗种子需要一定的时间，种子生长也需要一定的时间。给定两个下标从 0 开始的整数数组 `plantTime` 和 `growTime`，长度均为 `n`：

- `plantTime[i]` 表示第 `i` 颗种子需要的种植时间（天）。
- `growTime[i]` 表示第 `i` 颗种子在种植完成后，需要的生长时间（天）。

从第 0 天开始，你可以按任意顺序种植这些种子。返回所有种子全部开花的**最早可能的天数**。

---

### 示例

#### 示例 1  
**输入**  
```
plantTime = [1,4,3], growTime = [2,3,1]
```
**输出**  
```
9
```
**解释**  
灰色的花盆表示种植的天数，彩色的花盆表示生长的天数，花朵表示开花的那一天。  
一种最优的安排如下：

- 第 0 天，种下第 0 颗种子。该种子生长 2 整天，**第 3 天**开花。
- 第 1 至第 4 天，种下第 1 颗种子。该种子生长 3 整天，**第 8 天**开花。
- 第 5 至第 7 天，种下第 2 颗种子。该种子生长 1 整天，**第 9 天**开花。

所有种子最早在第 9 天全部盛开。

#### 示例 2  
**输入**  
```
plantTime = [1,2,3,2], growTime = [2,1,2,1]
```
**输出**  
```
9
```
**解释**  
一种最优的安排如下：

- 第 1 天，种下第 0 颗种子。该种子生长 2 整天，**第 4 天**开花。
- 第 0 天和第 3 天，种下第 1 颗种子。该种子生长 1 整天，**第 5 天**开花。
- 第 2 天和第 5 天，种下第 2 颗种子。该种子生长 2 整天，**第 8 天**开花。
- 第 6 天和第 7 天，种下第 3 颗种子。该种子生长 1 整天，**第 9 天**开花。

所有种子最早在第 9 天全部盛开。

#### 示例 3  
**输入**  
```
plantTime = [1], growTime = [1]
```
**输出**  
```
2
```
**解释**  
第 0 天种下唯一的种子，生长 1 整天，**第 2 天**开花。于是第 2 天所有种子都已盛开。

---

### 约束条件

- `n == plantTime.length == growTime.length`
- `1 <= n <= 10^5`
- `1 <= plantTime[i], growTime[i] <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把 **所有种子种植的顺序** 全部枚举一遍，算出每一种顺序对应的“全部开花的最早天数”，然后取最小值。  
- **数据结构**：我们可以把种子的下标 `[0, 1, …, n‑1]` 看成一张“种子清单”。枚举所有排列相当于把这张清单的顺序全排出来。  
- **为什么正确**：因为我们把**每一种可能的种植顺序**都算了一遍，必然会覆盖最优的那一个，所以得到的最小天数一定是正确答案。  
- **复杂度分析**：  
  - 枚举所有排列的数量是 `n!`（阶乘），即 `1 × 2 × 3 × … × n`，随 `n` 增长非常快。  
  - 对每一种排列，我们需要遍历一次种子，累计种植天数并计算开花时间，时间是 `O(n)`。  
  - 所以总的时间复杂度是 `O(n! × n)`，这在实际中几乎不可能跑完（比如 `n=10` 时已经是 3.6 百万种排列，`n=15` 已经是 1.3 万亿）。  
  - 空间上只需要保存一个排列，`O(n)`。

> **大白话**：`O(n! )` 就像让你把所有可能的排队方式都试一遍，人数多了就根本不可能在一天之内排完。

#### 代码（Python）

```python
import itertools
from typing import List

def earliestFullBloom_bruteforce(plantTime: List[int], growTime: List[int]) -> int:
    n = len(plantTime)
    ans = float('inf')                     # 用一个很大的数保存最小答案
    # 枚举所有种植顺序（排列）
    for order in itertools.permutations(range(n)):
        cur_day = 0                         # 当前已经种完的天数
        last_bloom = 0                      # 所有种子中最晚的开花日
        for idx in order:                   # 按照这个顺序种植
            cur_day += plantTime[idx]       # 种这颗种子需要的天数
            bloom = cur_day + growTime[idx] # 这颗种子开花的天数
            last_bloom = max(last_bloom, bloom)
        ans = min(ans, last_bloom)          # 取最小的最晚开花日
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n! × n)` — 需要遍历所有排列，每个排列再遍历 `n` 次。  
- **空间复杂度**：`O(n)` — 只保存当前排列和若干计数变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**顺序**是唯一影响答案的因素。我们要找出一种顺序，使得“所有种子中最晚的开花时间”尽可能早。

**瓶颈**  
- 种植时间 `plantTime` 必须全部完成，不能并行；它们只能顺序相加，形成“累计种植天数” `prefixPlant`。  
- 对于某颗种子 `i`，它的开花日 = `（它之前所有种子的种植时间之和） + plantTime[i] + growTime[i]`。  
- 最终答案是所有种子的 **最大** 开花日。换句话说，**决定答案的关键是那颗“最晚开花”的种子**。

**关键观察**  
如果两颗种子的 `growTime` 不同，把 `growTime` 更大的种子放在前面会更好。原因如下：

- 假设有两颗种子 `A`、`B`，且 `growTime[A] > growTime[B]`。  
- 若我们把 `B` 放在 `A` 前面，`A` 必须等 `B` 的全部种植时间结束后才开始它的 `growTime`，这会把 `A` 的开花日推迟 `plantTime[B]` 天。  
- 若把 `A` 放在 `B` 前面，`B` 的开花日只会被 `plantTime[A]` 推迟，而 `A` 本身的 `growTime` 更长，提前开始可以抵消这部分推迟。  
- 于是把 **growTime 更大的种子先种**，可以让“最长的 growTime”尽可能早地开始生长，从而减小整体的最晚开花日。

**贪心策略**  
1. 把每颗种子视作 `(plantTime[i], growTime[i])`。  
2. 按 `growTime` **降序** 排序（大的在前）。如果 `growTime` 相同，顺序随意。  
3. 按排好的顺序依次种植，累计种植天数 `curPlant`。  
4. 对每颗种子，计算 `curPlant + growTime[i]`，并维护最大值 `ans`。  
5. 最终答案是 `ans`（因为 `curPlant` 已经把该种子自己的 `plantTime` 包含进去了），再加上 0 天的起始偏移即可。

**为什么这个策略最优**  
- 设最优顺序为 `S*`，其中最晚开花的种子记为 `X`。  
- 若在 `S*` 中有任何一对相邻种子 `i、j` 满足 `growTime[i] < growTime[j]`，但 `i` 在 `j` 前面，则把它们交换会让 `j` 更早开始生长，`i` 只会稍微迟一点（因为 `growTime[i]` 较小），整体最晚开花日不增大，甚至可能降低。  
- 通过不断交换，最终可以得到一种 **所有 `growTime` 按降序排列** 的顺序，而不增加答案。  
- 因此，**按 `growTime` 降序种植** 必然能得到最小的最晚开花日，即全局最优。

**类比**  
把 `growTime` 想成“花的香味持续时间”，香味越久的花应该尽早种下，这样它的香味能在整个花园里尽早弥散，整体的“最晚散完香味的时间”就会更早。

#### 代码（Python）

```python
from typing import List

def earliestFullBloom(plantTime: List[int], growTime: List[int]) -> int:
    # 1. 把每颗种子组合成 (growTime, plantTime) 便于排序
    seeds = list(zip(growTime, plantTime))          # 每个元素是 (grow, plant)

    # 2. 按 growTime 降序排列
    seeds.sort(reverse=True)                        # 大的在前

    cur_plant = 0            # 已经种完的天数（累计 plantTime）
    ans = 0                  # 当前看到的最晚开花日

    for grow, plant in seeds:
        cur_plant += plant                     # 先把这颗种子的种植时间加进来
        ans = max(ans, cur_plant + grow)      # 计算这颗种子的开花日，取最大

    return ans
```

> **代码解释**  
> - 第 4 行 `zip(growTime, plantTime)` 把两个列表对应位置的数配对，类似把每颗种子的“种植时间”和“生长时间”绑在一起。  
> - 第 7 行 `sort(reverse=True)` 就像把“生长时间长的种子排到前面”。  
> - 第 12 行 `cur_plant += plant` 表示我们已经花了这么多天在种植之前的种子以及当前这颗种子。  
> - 第 13 行 `cur_plant + grow` 是这颗种子从现在开始到开花的总天数，取所有种子中的最大值即为答案。

#### 复杂度

- **时间复杂度**：`O(n log n)` — 主要耗时在对 `n` 颗种子排序，排序的时间是 `n log n`，比暴力的 `n!` 小很多。  
- **空间复杂度**：`O(n)` — 需要存放 `seeds` 这份配对列表，额外的变量只有常数级。

---

## 心得

- **核心技巧**：**贪心 + 按 growTime 降序排序**。  
- **适用场景**：  
  1. 需要把“耗时长的后续工作”尽早开始的调度类问题（如“任务调度让最晚完成时间最小”）。  
  2. “先做影响最大的事情再做影响小的事情” 的场景，如**会议安排**（先安排最长会议），**机器加工**（先加工需要最长冷却时间的零件）。  
- **解题钥匙**：**把决定最终答案的那颗“最慢”种子提前，让它的慢部分（growTime）尽可能早地并行进行**。

---

## 反思

- **第一反应**：直接想到枚举所有顺序，写出暴力解。  
- **最容易踩的坑**：  
  - 忽视 `plantTime` 必须串行完成，误以为可以并行导致错误的时间计算。  
  - 在实现排序时忘记降序，导致答案偏大。  
  - 边界情况：`n = 1` 时仍需返回 `plantTime[0] + growTime[0]`，代码要能处理单元素列表。  
- **下次类似题目第一步**：先判断**“哪个因素决定最晚完成时间”**，再思考**如何让这个因素尽早开始**，通常会得到“按某个关键属性排序”的贪心思路。