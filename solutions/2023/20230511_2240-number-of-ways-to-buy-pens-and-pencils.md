# #2240. 购买钢笔和铅笔的方案数 / Number of Ways to Buy Pens and Pencils

> 难度：中等 · 标签：Math、Enumeration · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-buy-pens-and-pencils/)

---

## 题目（英文原版）

**Description**

You are given an integer total indicating the amount of money you have. You are also given two integers cost1 and cost2 indicating the price of a pen and pencil respectively. You can spend part or all of your money to buy multiple quantities (or none) of each kind of writing utensil.
Return the number of distinct ways you can buy some number of pens and pencils.

**Examples**

**Example 1:**

```
Input: total = 20, cost1 = 10, cost2 = 5
Output: 9
Explanation: The price of a pen is 10 and the price of a pencil is 5.
- If you buy 0 pens, you can buy 0, 1, 2, 3, or 4 pencils.
- If you buy 1 pen, you can buy 0, 1, or 2 pencils.
- If you buy 2 pens, you cannot buy any pencils.
The total number of ways to buy pens and pencils is 5 + 3 + 1 = 9.
```

**Example 2:**

```
Input: total = 5, cost1 = 10, cost2 = 10
Output: 1
Explanation: The price of both pens and pencils are 10, which cost more than total, so you cannot buy any writing utensils. Therefore, there is only 1 way: buy 0 pens and 0 pencils.
```

**Constraints**

- 1 <= total, cost1, cost2 <= 106

---

## 题目（中文翻译）

**描述**  
给定一个整数 `total`，表示你拥有的金钱总额。再给定两个整数 `cost1` 和 `cost2`，分别表示一支钢笔和一支铅笔的价格。你可以花费部分或全部金钱，购买任意数量（包括 0） 的钢笔和铅笔。  

返回购买若干支钢笔和铅笔的**不同方案数**（distinct ways）。

**示例 1**  
``` 
Input: total = 20, cost1 = 10, cost2 = 5
Output: 9
Explanation: 
- 钢笔的价格为 10，铅笔的价格为 5。  
- 若购买 0 支钢笔，则可以购买 0、1、2、3 或 4 支铅笔。  
- 若购买 1 支钢笔，则可以购买 0、1 或 2 支铅笔。  
- 若购买 2 支钢笔，则无法再购买任何铅笔。  

总的购买方案数为 5 + 3 + 1 = 9。 
```

**示例 2**  
``` 
Input: total = 5, cost1 = 10, cost2 = 10
Output: 1
Explanation: 
钢笔和铅笔的单价均为 10，均超过了可用的 `total`，因此无法购买任何文具。唯一的方案是：购买 0 支钢笔和 0 支铅笔。 
```

**约束条件**  
- `1 <= total, cost1, cost2 <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把“买笔”和“买铅笔”这两件事都枚举出来。  
- **枚举笔的数量**：从 0 支开始，一直枚举到 `total // cost1`（因为再多就买不起了）。  
- **枚举铅笔的数量**：对每一种笔的数量，再从 0 支枚举到 `remaining // cost2`（`remaining = total - pens * cost1`），表示剩余的钱还能买多少支铅笔。  

这里用到的 **循环** 就像我们在超市里一次一次尝试不同的购买组合——先决定买几支笔，再决定买几支铅笔。  

为什么这个方法一定能得到答案？因为我们把所有可能的 (笔数, 铅笔数) 配对都遍历了一遍，凡是花费不超过 `total` 的配对都会被计数。  

**时间/空间复杂度**  
- 外层循环的次数大约是 `total / cost1`，内层循环的次数大约是 `total / cost2`，两层相乘得到 **O((total / cost1) * (total / cost2))**。如果 `cost1` 和 `cost2` 都很小，这个数会接近 `total²`，在最坏情况下相当于 **O(total²)**。  
- 空间上只需要几个整型变量，**O(1)**。

> 大白话解释：  
> - **O(total²)** 可以想象成在一个 `total × total` 的大格子里逐格检查，格子越多，检查时间越长。  

#### 代码（Python）

```python
def ways_brute_force(total: int, cost1: int, cost2: int) -> int:
    """
    暴力枚举所有可能的 (笔, 铅笔) 组合
    """
    ans = 0
    # 枚举买几支笔
    for pens in range(total // cost1 + 1):          # +1 是因为要把 0 也算进去
        spent = pens * cost1                         # 已经花掉的钱
        remaining = total - spent                    # 还剩多少钱
        # 对每一种笔的数量，枚举可以买的铅笔数量
        for pencils in range(remaining // cost2 + 1):
            # 只要不超钱，就算一种合法方案
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O((total // cost1) * (total // cost2))`，在最坏情况下约等于 `O(total²)`。  
  > 这意味着如果 `total = 10⁶`，暴力解会尝试上万亿次，根本跑不完。  
- **空间复杂度**：`O(1)`，只用了常数个变量。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于「内层循环」——我们为每一种笔的数量，都要重新遍历所有可能的铅笔数量。其实我们并不需要逐个枚举铅笔，只要知道 **还能买多少支** 铅笔即可，因为每一种笔的数量对应的铅笔数量是连续的。

**关键观察**  
- 对于固定的笔数 `pens`，剩余的钱是 `remaining = total - pens * cost1`。  
- 用这剩余的钱最多能买 `remaining // cost2` 支铅笔，且可以选择买 0、1、…、`remaining // cost2` 支。  
- 因此，这种笔数对应的合法方案数是 `remaining // cost2 + 1`（+1 包含买 0 支的情况）。

这样我们只需要 **一层循环**，每次直接算出对应的方案数并累加，时间立刻从 “平方级” 降到 “线性级”。  

**进一步优化**  
如果 `cost1` 大于 `cost2`，则外层循环的次数会比较多。我们可以把 **更贵的文具设为外层循环**，把 **更便宜的文具设为内部的直接算**，这样循环次数等于 `total // max(cost1, cost2)`，是所有可能的最小值。

> 类比：  
> 想象你在超市挑选商品，先决定买最贵的商品的数量（因为买多了会迅速耗尽预算），剩下的钱再决定买多少最便宜的商品。这样一步步缩小选择空间，速度自然更快。

#### 代码（Python）

```python
def ways_optimal(total: int, cost1: int, cost2: int) -> int:
    """
    只用一层循环，直接计算每种笔数对应的铅笔方案数。
    为了让循环次数最少，始终让 cost1 是更贵的那一种。
    """
    # 把 cost1 定义为“更贵的”，cost2 为“更便宜的”
    if cost1 < cost2:          # 如果原来的笔更便宜，交换两者
        cost1, cost2 = cost2, cost1

    ans = 0
    # 只枚举更贵的文具（这里是 pens）
    max_expensive = total // cost1          # 能买的最多数量
    for expensive_cnt in range(max_expensive + 1):
        remaining = total - expensive_cnt * cost1
        # 剩余钱能买的更便宜文具的数量 + 1（包括买 0 个的情况）
        ans += remaining // cost2 + 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(total // max(cost1, cost2))`。  
  - 解释：我们只遍历了更贵文具的可能数量，最多 `total / (更贵的价格)` 次。若两者价格相同，则等于 `total / cost1`，仍然是线性级别。  
  - 与暴力解相比，时间从 **O(total²)** 降到了 **O(total)**，在 `total = 10⁶` 时只需要约一百万次循环，毫秒级可以完成。  

- **空间复杂度**：`O(1)`，只用了几个整数变量。

---

## 心得

- **核心技巧**：把“枚举 + 直接计算”结合起来。先固定一种商品的数量，然后用除法一次算出另一种商品的可选数量（因为它们是连续的）。  
- **适用的题型**  
  1. “在预算内购买不同商品的组合数”——如《买鸡蛋的方案数》  
  2. “满足线性不等式的整数解计数”——如 `ax + by ≤ C` 的非负整数解个数  
  3. “两种硬币找零的组合数”——类似硬币兑换问题的简化版  

- **一句话总结**：**先锁定一种商品的数量，用除法直接算出另一种商品的可选范围，循环次数自然最小化。**

---

## 反思

- **第一反应**：看到 “total、cost1、cost2” 立刻想到“双层循环枚举”。  
- **最容易踩的坑**  
  - 忘记把 “买 0 件” 也算进答案，导致答案少 1。  
  - 当两种商品都比预算贵时，需要返回 1（全都不买），而不是 0。  
  - 边界条件 `total // cost` 需要加 `+1` 才能把 0 包含进来。  

- **下次遇到同类题**：第一步先判断是否可以 **把其中一种商品的数量用除法一次算出**，如果可以，就直接用 “一层循环 + 直接计算” 的思路。这样既省时又不易出错。