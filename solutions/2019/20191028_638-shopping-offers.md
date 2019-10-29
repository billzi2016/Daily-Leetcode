# #638. 购物优惠 / Shopping Offers

> 难度：中等 · 标签：Array、Dynamic Programming、Backtracking、Bit Manipulation、Memoization、Bitmask · [LeetCode 链接](https://leetcode.com/problems/shopping-offers/)

---

## 题目（英文原版）

**Description**

In LeetCode Store, there are n items to sell. Each item has a price. However, there are some special offers, and a special offer consists of one or more different kinds of items with a sale price.
You are given an integer array price where price[i] is the price of the ith item, and an integer array needs where needs[i] is the number of pieces of the ith item you want to buy.
You are also given an array special where special[i] is of size n + 1 where special[i][j] is the number of pieces of the jth item in the ith offer and special[i][n] (i.e., the last integer in the array) is the price of the ith offer.
Return the lowest price you have to pay for exactly certain items as given, where you could make optimal use of the special offers. You are not allowed to buy more items than you want, even if that would lower the overall price. You could use any of the special offers as many times as you want.

**Examples**

**Example 1:**

```
Input: price = [2,5], special = [[3,0,5],[1,2,10]], needs = [3,2]
Output: 14
Explanation: There are two kinds of items, A and B. Their prices are $2 and $5 respectively. 
In special offer 1, you can pay $5 for 3A and 0B
In special offer 2, you can pay $10 for 1A and 2B. 
You need to buy 3A and 2B, so you may pay $10 for 1A and 2B (special offer #2), and $4 for 2A.
```

**Example 2:**

```
Input: price = [2,3,4], special = [[1,1,0,4],[2,2,1,9]], needs = [1,2,1]
Output: 11
Explanation: The price of A is $2, and $3 for B, $4 for C. 
You may pay $4 for 1A and 1B, and $9 for 2A ,2B and 1C. 
You need to buy 1A ,2B and 1C, so you may pay $4 for 1A and 1B (special offer #1), and $3 for 1B, $4 for 1C. 
You cannot add more items, though only $9 for 2A ,2B and 1C.
```

**Constraints**

- n == price.length == needs.length
- 1 <= n <= 6
- 0 <= price[i], needs[i] <= 10
- 1 <= special.length <= 100
- special[i].length == n + 1
- 0 <= special[i][j] <= 50
- The input is generated that at least one of special[i][j] is non-zero for 0 <= j <= n - 1.

---

## 题目（中文翻译）

在 LeetCode Store 中，有 `n` 种商品可供销售。每种商品都有对应的价格。然而，店里提供了一些特价套餐（special offer），每个特价套餐由一种或多种不同商品组成，并且有一个优惠价。

给定整数数组 `price`，其中 `price[i]` 表示第 `i` 件商品的单价；整数数组 `needs`，其中 `needs[i]` 表示你想购买的第 `i` 件商品的数量。  
同时给定数组 `special`，其中 `special[i]` 的长度为 `n + 1`，`special[i][j]` 表示第 `i` 个特价套餐中第 `j` 件商品的数量，`special[i][n]`（即数组的最后一个整数）是该套餐的价格。

返回恰好购买 `needs` 中指定数量商品所需的最低花费，你可以合理利用特价套餐。**不允许购买超过需求的商品，即使这样可以降低总价。**任意特价套餐可以使用任意次数。

**示例 1**  
**示例 2**  
**约束条件**  

示例：
### 示例 1
**输入**  
```
price = [2,5], special = [[3,0,5],[1,2,10]], needs = [3,2]
```
**输出**  
```
14
```
**解释**  
有两种商品，记为 A 和 B，单价分别为 $2 和 $5。  
特价套餐 1：支付 $5 可获得 3 个 A 和 0 个 B。  
特价套餐 2：支付 $10 可获得 1 个 A 和 2 个 B。  
你需要购买 3 个 A 和 2 个 B，因此可以选择特价套餐 2（$10）购买 1 个 A 和 2 个 B，再单独购买 2 个 A（$4），总计 $14。

### 示例 2
**输入**  
```
price = [2,3,4], special = [[1,1,0,4],[2,2,1,9]], needs = [1,2,1]
```
**输出**  
```
11
```
**解释**  
商品 A 的单价为 $2，B 为 $3，C 为 $4。  
特价套餐 1：支付 $4 可获得 1 个 A 和 1 个 B。  
特价套餐 2：支付 $9 可获得 2 个 A、2 个 B 和 1 个 C。  
需求为 1 个 A、2 个 B、1 个 C。可以先使用特价套餐 1（$4）购买 1 个 A 和 1 个 B，再单独购买剩余的 1 个 B（$3）和 1 个 C（$4），总计 $11。  
不能使用特价套餐 2，因为它会导致购买超过需求的商品，虽然只需 $9。

**约束条件**
- `n == price.length == needs.length`
- `1 <= n <= 6`
- `0 <= price[i], needs[i] <= 10`
- `1 <= special.length <= 100`
- `special[i].length == n + 1`
- `0 <= special[i][j] <= 50`
- 输入保证对于每个 `special[i]`，在 `0 <= j <= n - 1` 范围内至少有一个 `special[i][j]` 为非零。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每一种特价套餐都当作一种“操作”，把需求 `needs` 看成一个小盒子，尝试把盒子里的东西全部“装走”。**  
我们可以用**深度优先搜索（DFS）**枚举所有可能的购买顺序：

1. **当前状态**：还有多少件每种商品需要购买，用一个长度为 `n` 的列表 `cur` 表示（比如 `[2,1,0]` 表示还需要 2 件 A、1 件 B、0 件 C）。
2. **尝试**：  
   - 直接用普通单价把剩下的全部买了，得到一种花费（这就是“最笨”的办法）。  
   - 对每一个特价套餐 `sp`，检查它的每种商品数量是否 **不超过** `cur`（即不会买多）。如果可以，就把 `sp` 用一次，得到新的剩余需求 `next = cur - sp_items`，继续递归搜索下去。
3. **递归终止**：当所有需求都变成 0 时，返回 0（不需要再花钱）。

> **类比**：想象你在超市的购物车里放了若干商品，每次你可以把**整套套餐**放进购物车（只要不超出你想买的数量），然后继续挑选下一套套餐，直到购物车里正好装满你需要的商品。  

**为什么正确**：搜索遍历了所有合法的购买组合（包括只买单价商品的组合），所以最小花费一定会被找到。

#### 代码（Python）

```python
from typing import List

def shoppingOffers_bruteforce(price: List[int],
                             special: List[List[int]],
                             needs: List[int]) -> int:
    n = len(price)

    # 递归函数：返回在当前需求 cur 下的最小花费
    def dfs(cur: List[int]) -> int:
        # 1）先算不使用任何套餐，只用单价买的花费（基准解）
        min_cost = sum(c * p for c, p in zip(cur, price))

        # 2）尝试每一个套餐
        for sp in special:
            # sp_items = 前 n 项是各商品数量，sp_price = 最后一个元素是套餐价
            sp_items, sp_price = sp[:n], sp[-1]

            # 检查套餐是否会买多：如果有任意一种商品的需求 < 套餐数量，就不能使用
            if any(sp_items[i] > cur[i] for i in range(n)):
                continue  # 直接跳过这个套餐

            # 使用一次套餐后得到的新需求
            next_cur = [cur[i] - sp_items[i] for i in range(n)]

            # 递归求解子问题，并加上本次套餐的价格
            cost_with_sp = dfs(next_cur) + sp_price
            min_cost = min(min_cost, cost_with_sp)   # 取最小

        return min_cost

    return dfs(needs)
```

- `any(sp_items[i] > cur[i] for i in range(n))` 用来判断是否会买超。
- `dfs` 每次都会尝试 **所有** 合法套餐，递归深度最多等于需求总和（每次至少买走一件商品），因此可以遍历完所有组合。

#### 复杂度  

- **时间复杂度**：  
  在最坏情况下，`needs` 中每种商品的数量最多是 10，商品种类 `n ≤ 6`。搜索会遍历所有可能的需求状态，状态数大约是  
  \[
  O\big((max\_need+1)^n\big) \le O(11^6) \approx 1.77 \times 10^6
  \]  
  再乘以每次遍历所有套餐（≤100），得到上限约为 **1.7 亿次**的操作，实际会因为大量剪枝（套餐不可用）而更少。用大白话说，就是“指数级的”，在最坏情况下会慢得让人等不及。

- **空间复杂度**：  
  递归栈的深度最多等于需求总和（≤ 60），每层保存一个长度为 `n` 的列表，故空间是 **O(n·max_need)**，即几百个整数，几乎可以忽略。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于大量重复计算：同一个需求状态（比如 `[2,1]`）会被多次递归求解。  
我们可以 **记住**（**memoization**）已经算过的状态，把它们的最小花费缓存下来，下次遇到相同需求时直接返回，避免重复搜索。

**核心技巧**：  
- 用 **哈希表**（Python 的 `dict`）把需求向量（转换成元组）映射到最小花费。  
- 同时可以 **提前过滤** 那些**不划算**的套餐：如果套餐的价格 **不低于** 用单价买同样商品的费用，就直接丢掉它，因为它永远不会帮助降低总价。

**为什么这样更快**：  
- 每一种合法需求状态只会被计算一次。状态总数仍然是 \((max\_need+1)^n\)，但不再有指数级的重复，实际运行时间接近 **几千到几万次**的递归调用，轻松在 1 秒内结束。  
- 记忆化的空间同样是状态数乘以一个整数，最多几百万个条目（在最坏情况仍可接受），但实际会更少。

**实现细节**：

1. **过滤特价**：遍历 `special`，如果 `sp_price >= sum(sp_items[i] * price[i])`，说明直接买单价更便宜，舍弃这个套餐。  
2. **递归+记忆**：`dfs(cur)` 返回 `cur` 需求的最小花费。先检查 `memo`，如果已存在直接返回。否则按前面暴力思路尝试所有合法套餐，记录最小值并保存到 `memo`。  
3. **状态表示**：把列表 `cur` 转成不可变的 `tuple(cur)` 作为字典键。

#### 代码（Python）

```python
from typing import List, Tuple

def shoppingOffers(price: List[int],
                  special: List[List[int]],
                  needs: List[int]) -> int:
    n = len(price)

    # 1️⃣ 过滤掉“划算不了”的套餐
    filtered_special = []
    for sp in special:
        sp_items, sp_price = sp[:n], sp[-1]
        # 用单价买这些商品的花费
        normal_price = sum(sp_items[i] * price[i] for i in range(n))
        if sp_price < normal_price:          # 只保留真的更便宜的套餐
            filtered_special.append(sp)
    special = filtered_special

    memo = {}  # type: dict[Tuple[int, ...], int]

    # 2️⃣ 记忆化递归
    def dfs(cur: Tuple[int, ...]) -> int:
        if cur in memo:               # 已经算过，直接返回
            return memo[cur]

        # 先算不使用任何套餐的基准费用
        min_cost = sum(cur[i] * price[i] for i in range(n))

        # 尝试每一个合法套餐
        for sp in special:
            sp_items, sp_price = sp[:n], sp[-1]

            # 检查套餐是否会买超
            if any(sp_items[i] > cur[i] for i in range(n)):
                continue

            # 计算使用套餐后的新需求（仍然是元组，方便做键）
            next_cur = tuple(cur[i] - sp_items[i] for i in range(n))

            # 递归求子状态的最小费用 + 本次套餐费用
            cost = dfs(next_cur) + sp_price
            min_cost = min(min_cost, cost)

        memo[cur] = min_cost   # 记下来，供以后复用
        return min_cost

    return dfs(tuple(needs))
```

- `filtered_special` 通过 **单价** 与 **套餐价** 的比较，把“没有优势”的套餐剔除，减少递归分支。  
- `cur` 被统一转成 `tuple`，这样可以安全地用作字典的键（类似把需求列表放进“查字典”，键是需求组合，值是对应的最小花费）。  
- `memo` 保存的每个状态只会被计算一次，实现了 **动态规划**（自顶向下的记忆化 DP）。

#### 复杂度  

- **时间复杂度**：  
  每个合法需求状态只会被计算一次，状态数上限仍是 \((max\_need+1)^n\)。在最坏情况约为 \(11^6 \approx 1.77 \times 10^6\) 种，但实际因为 **套餐过滤** 与 **需求约束**，往往只有几千到几万种。每个状态遍历所有套餐（≤100），所以整体是  
  \[
  O\big( \text{states} \times |\text{special}| \big)
  \]  
  用大白话说，就是“和暴力解相比，只是把重复的工作省掉了”，速度提升数十倍甚至上百倍。

- **空间复杂度**：  
  `memo` 保存每个状态的最小费用，最多需要存储 **states** 条记录，空间为  
  \[
  O\big((max\_need+1)^n\big)
  \]  
  这在题目给定的范围内（几 MB）是可以接受的。递归栈深度同样最多是需求总和（≤60），占用极小。

---

## 心得

- **核心技巧**：**记忆化搜索（DP + DFS）** + **套餐过滤**。  
- **适用的题型**：  
  1. 需要在“有限的资源需求”和“若干组合优惠”之间取最优解的背包类问题（如 LeetCode 638 “Shopping Offers”）。  
  2. “买东西有打折券”这类需要在多维需求上做选择的题目（如 1125 “Smallest Sufficient Team” 的状态压缩 DP）。  
  3. “多维背包”或 “组合数” 需要枚举所有状态并记忆的场景（如 464 “Can I Win?”）。
- **一句话总结解题钥匙**：**把每一次“买什么”看成状态转移，用哈希表记住每个需求的最优花费，避免重复计算**。

---

## 反思

- **第一反应**：看到“可以多次使用特价套餐”，立刻想到 **递归穷举** 所有套餐的使用次数。  
- **最容易踩的坑**：  
  - **买超**：忘记检查套餐里某商品数量是否超过当前需求，会导致非法状态。  
  - **无限循环**：如果套餐本身不消耗任何需求（全为 0），递归会无限调用，需要在过滤阶段或递归时跳过这类“无效套餐”。  
  - **状态表示错误**：使用列表直接做字典键会报错，必须转换为不可变的 `tuple`（类似查字典的“键”。）  
- **下次类似题的第一步**：先 **把需求抽象成一个状态**，思考 **“从当前状态如何一步到达下一个合法状态”**，然后判断是否需要 **记忆化**（状态空间是否会重复出现）。这样就能快速定位是暴力搜索还是 DP。