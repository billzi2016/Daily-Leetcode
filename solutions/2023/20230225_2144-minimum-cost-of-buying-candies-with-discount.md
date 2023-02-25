# #2144. 购买糖果的最低花费（含折扣） / Minimum Cost of Buying Candies With Discount

> 难度：简单 · 标签：Array、Greedy、Sorting · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-of-buying-candies-with-discount/)

---

## 题目（英文原版）

**Description**

A shop is selling candies at a discount. For every two candies sold, the shop gives a third candy for free.
The customer can choose any candy to take away for free as long as the cost of the chosen candy is less than or equal to the minimum cost of the two candies bought.
Given a 0-indexed integer array cost, where cost[i] denotes the cost of the ith candy, return the minimum cost of buying all the candies.

**Examples**

**Example 1:**

```
Input: cost = [1,2,3]
Output: 5
Explanation: We buy the candies with costs 2 and 3, and take the candy with cost 1 for free.
The total cost of buying all candies is 2 + 3 = 5. This is the only way we can buy the candies.
Note that we cannot buy candies with costs 1 and 3, and then take the candy with cost 2 for free.
The cost of the free candy has to be less than or equal to the minimum cost of the purchased candies.
```

**Example 2:**

```
Input: cost = [6,5,7,9,2,2]
Output: 23
Explanation: The way in which we can get the minimum cost is described below:
- Buy candies with costs 9 and 7
- Take the candy with cost 6 for free
- We buy candies with costs 5 and 2
- Take the last remaining candy with cost 2 for free
Hence, the minimum cost to buy all candies is 9 + 7 + 5 + 2 = 23.
```

**Example 3:**

```
Input: cost = [5,5]
Output: 10
Explanation: Since there are only 2 candies, we buy both of them. There is not a third candy we can take for free.
Hence, the minimum cost to buy all candies is 5 + 5 = 10.
```

**Constraints**

- 1 <= cost.length <= 100
- 1 <= cost[i] <= 100

---

## 题目（中文翻译）

**题目描述**  
一家店铺正在进行糖果促销活动：每购买两颗糖果，店家会赠送一颗糖果免费。  
顾客可以任选一颗糖果免费带走，前提是该免费糖果的费用 **cost** 不超过所购买的两颗糖果中费用的最小值。  
给定一个下标从 0 开始的整数数组 `cost`，其中 `cost[i]` 表示第 `i` 颗糖果的费用，返回购买所有糖果的最小总费用。

**示例**  

*示例 1*  
```
Input: cost = [1,2,3]
Output: 5
Explanation: 我们购买费用为 2 和 3 的两颗糖果，并将费用为 1 的糖果免费带走。  
购买所有糖果的总费用为 2 + 3 = 5。这是唯一的购买方式。  
注意，不能先购买费用为 1 和 3 的糖果，然后将费用为 2 的糖果免费带走，因为免费糖果的费用必须 ≤ 所购两颗糖果费用的最小值。
```

*示例 2*  
```
Input: cost = [6,5,7,9,2,2]
Output: 23
Explanation: 达到最低费用的购买方案如下：
- 购买费用为 9 和 7 的糖果
- 将费用为 6 的糖果免费带走
- 购买费用为 5 和 2 的糖果
- 将剩余的费用为 2 的糖果免费带走
因此，购买所有糖果的最低费用为 9 + 7 + 5 + 2 = 23。
```

*示例 3*  
```
Input: cost = [5,5]
Output: 10
Explanation: 只有两颗糖果，只能将它们全部购买，无法获得免费糖果。  
所以购买所有糖果的费用为 5 + 5 = 10。
```

**约束条件**  
- `1 <= cost.length <= 100`  
- `1 <= cost[i] <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的购买/免费分组都穷举一遍**，然后挑出花费最少的那种。  
具体做法可以用递归（或回溯）：

1. 记录当前已经买了哪些糖果（用一个 `used` 布尔数组）。
2. 从剩余的糖果里任选两颗当作“买的”，再从剩余的糖果里任选一颗满足 “免费糖的价格 ≤ 两颗买的糖中较小的那颗价格” 作为“免费”。  
3. 把这三颗标记为已使用，递归求剩余糖果的最小花费。  
4. 当剩余糖果不足三颗时，只能把它们全部买下。

> **类比**：把这道题想成在超市挑选商品。暴力解相当于把超市里每一种可能的挑选顺序都试一遍，就像把所有排队买东西的顺序全部列出来再算一次总价。

**为什么一定能得到正确答案**  
因为我们枚举了**所有合法的购买方式**，最小的花费自然就在其中。只要递归实现没有遗漏，就一定不出错。

**时间/空间复杂度**  
- 时间复杂度：在最坏情况下，每一步我们要在 `n` 颗糖果中挑 2 颗买，再挑 1 颗免费，递归深度约 `n/3`。这相当于 `O( n! )`（阶乘级）甚至更高，实际只适用于 `n ≤ 10` 左右的小数据。用大白话说，就是“花的时间会随着糖果数量疯狂增长，几分钟内只能算完十几颗”。  
- 空间复杂度：递归栈最多 `n/3` 层，外加 `O(n)` 的 `used` 数组 → `O(n)`。

#### 代码（Python）

```python
from itertools import combinations
from functools import lru_cache
from typing import List

def minCost_bruteforce(cost: List[int]) -> int:
    n = len(cost)

    # 用位掩码表示哪些糖果已经买完/送完，0 表示未使用，1 表示已使用
    @lru_cache(None)
    def dfs(mask: int) -> int:
        # 统计还有多少糖果未使用
        remaining = [i for i in range(n) if not (mask >> i) & 1]

        # 剩余不到 3 颗，只能全部买下来
        if len(remaining) <= 2:
            return sum(cost[i] for i in remaining)

        best = float('inf')
        # 枚举两颗买的糖果
        for i, j in combinations(remaining, 2):
            # 两颗买的糖果的最小价格
            min_buy = min(cost[i], cost[j])
            # 在剩余的糖果中挑一颗满足免费条件的
            for k in remaining:
                if k in (i, j):
                    continue
                if cost[k] <= min_buy:          # 免费糖果必须不贵于最便宜的那颗已买糖
                    new_mask = mask | (1 << i) | (1 << j) | (1 << k)
                    cost_now = cost[i] + cost[j] + dfs(new_mask)
                    best = min(best, cost_now)
        return best

    return dfs(0)
```

> **关键行中文注释**  
> - `mask` 用二进制记录已经处理过的糖果，省空间。  
> - `combinations(remaining, 2)` 把“买的两颗”全部列举出来。  
> - `if cost[k] <= min_buy` 正是题目要求的 “免费糖果不贵于两颗买的糖中较小的那颗”。  

#### 复杂度

- **时间复杂度**：`O( n! )`（阶乘级）——因为要枚举所有合法的三元组合顺序，随着糖果数量指数级增长。  
- **空间复杂度**：`O(n)`——递归栈深度和掩码都与糖果数量线性相关。

---

### 2. 最优解

#### 思路  

从暴力解出发，我们发现 **瓶颈在于枚举所有可能的分组**，这让时间爆炸。  
观察题目规则可以发现：

- 每次“买两颗、免费一颗”，**免费糖果的价格上限是这两颗中较小的那颗**。  
- 为了让免费糖果尽可能贵（从而省钱），我们应该让 **两颗买的糖尽量贵**，而 **被免费拿走的糖尽量贵**。  

换句话说，**把所有糖果按价格从高到低排好序**，然后每 **连续三颗** 里：

- 前两颗是最贵的两颗，必须买。  
- 第三颗是这三颗里最便宜的，正好满足 “免费糖 ≤ 两颗买的最小价格”。  

这样 **每组三颗中最便宜的那颗都可以免费**，且没有更好的安排可以让更贵的糖免费——因为若把更贵的糖放进免费位置，它的左边至少有两颗比它更贵的糖，而这两颗已经被买掉了，无法再提供更高的上限。

> **类比**：把糖果想成排队的学生，老师每次挑选两名成绩最高的学生让他们交作业，成绩最低的那名学生免交。把学生按成绩从高到低排好，老师每三个人就能免掉一个最差的。这样免掉的学生成绩总是尽可能高。

**核心算法**：**贪心 + 排序**。先把数组从大到小排序，然后把每第三个（索引 2,5,8,…）的糖果视为免费，其余的累加即为最小花费。

#### 代码（Python）

```python
from typing import List

def minCost_greedy(cost: List[int]) -> int:
    # 1. 先把糖果价格从高到低排好序
    cost.sort(reverse=True)          # 逆序，相当于把贵的放前面

    total = 0
    for i, c in enumerate(cost):
        # 2. 每第 3 颗（索引 2,5,8,...）免费，不计入总花费
        if i % 3 != 2:                # i % 3 == 2 的时候是免费糖
            total += c                # 其余的都要付钱
    return total
```

> **关键行中文注释**  
> - `cost.sort(reverse=True)`：把贵的糖果排在前面，方便后面“每三颗挑一次”。  
> - `if i % 3 != 2`：利用取模判断是否是每组三个中的第三个，第三个就是免费糖。  

#### 复杂度

- **时间复杂度**：`O(n log n)`——排序是主要耗时，`n` 最多 100，完全可以接受。用大白话说，就是“把糖果从贵到便宜排个序，需要的时间和糖果数量的对数倍成正比”。  
- **空间复杂度**：`O(1)`（不计入排序的递归栈）——只用了常数级的额外变量。

---

## 心得

- **核心技巧**：**贪心 + 排序**，把“每次都让最贵的两颗买掉，最便宜的那颗免费”落实到全局。
- **适用的题型**  
  1. “买 k 件送 1 件” 类的折扣题（如买 2 件送 1 件、买 3 件送 1 件等）。  
  2. “分组后取最大/最小” 的最小化/最大化问题（如 “买家送礼物” 中的最小费用）。  
  3. “每 m 个中挑 n 个” 的组合优化（如 “每 3 件商品付 2 件价”）。
- **一句话总结**：**把所有物品从高到低排序，然后让每组的最小者免费**，这就是这类“买二送一”折扣的最优策略。

---

## 反思

- **第一反应**：看到“买两颗送一颗”，自然会想到“把最贵的两颗买了，最便宜的那颗免费”，于是想到先排序。  
- **最容易踩的坑**  
  1. **免费糖的价格限制**：必须 ≤ 两颗已买糖中较小的那颗。若不注意顺序，可能错误地把比买的两颗中最小值还贵的糖当成免费。  
  2. **边界情况**：糖果不足三颗时根本没有免费机会，需要全部买下。  
  3. **排序方向**：若误用了升序，免费位置会错位，导致费用不最小。  
- **下次第一步**：**先把数组排序**（通常是降序），然后**观察每 m 个一组的规律**，判断哪一位可以免费或必须付费。这样可以快速锁定贪心解法。