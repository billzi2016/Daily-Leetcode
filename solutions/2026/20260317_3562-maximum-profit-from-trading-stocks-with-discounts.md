# #3562. 折扣下的股票交易最大利润 / Maximum Profit from Trading Stocks with Discounts

> 难度：困难 · 标签：Array、Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/maximum-profit-from-trading-stocks-with-discounts/)

---

## 题目（英文原版）

**Description**

You are given an integer n, representing the number of employees in a company. Each employee is assigned a unique ID from 1 to n, and employee 1 is the CEO. You are given two 1-based integer arrays, present and future, each of length n, where:
The company's hierarchy is represented by a 2D integer array hierarchy, where hierarchy[i] = [ui, vi] means that employee ui is the direct boss of employee vi.
Additionally, you have an integer budget representing the total funds available for investment.
However, the company has a discount policy: if an employee's direct boss purchases their own stock, then the employee can buy their stock at half the original price (floor(present[v] / 2)).
Return the maximum profit that can be achieved without exceeding the given budget.
Note:

**Examples**

**Example 1:**

```
Input: n = 2, present = [1,2], future = [4,3], hierarchy = [[1,2]], budget = 3
Output: 5
Explanation:
```

**Example 2:**

```
Input: n = 2, present = [3,4], future = [5,8], hierarchy = [[1,2]], budget = 4
Output: 4
Explanation:
```

**Example 3:**

```
Input: n = 3, present = [4,6,8], future = [7,9,11], hierarchy = [[1,2],[1,3]], budget = 10
Output: 10
Explanation:
```

**Example 4:**

```
Input: n = 3, present = [5,2,3], future = [8,5,6], hierarchy = [[1,2],[2,3]], budget = 7
Output: 12
Explanation:
```

**Constraints**

- 1 <= n <= 160
- present.length, future.length == n
- 1 <= present[i], future[i] <= 50
- hierarchy.length == n - 1
- hierarchy[i] == [ui, vi]
- 1 <= ui, vi <= n
- ui != vi
- 1 <= budget <= 160
- There are no duplicate edges.
- Employee 1 is the direct or indirect boss of every employee.
- The input graph hierarchy is guaranteed to have no cycles.

---

## 题目（中文翻译）

**题目描述**  
给定一个整数 `n`，表示公司员工的数量。每位员工的唯一编号为 `1` 到 `n`，其中 `1` 号员工为 CEO。再给定两个 1‑基（1‑based）整数数组 `present` 与 `future`，长度均为 `n`，其中：

- `present[i]` 表示第 `i` 位员工当前持有的股票价格（即买入价）；
- `future[i]` 表示第 `i` 位员工未来股票的预期价格（即卖出价）。

公司的组织结构由二维整数数组 `hierarchy` 表示，`hierarchy[i] = [u_i, v_i]` 表示员工 `u_i` 是员工 `v_i` 的直接上司（direct boss）。

此外，还给定一个整数 `budget`，表示可用于购买股票的总资金上限。

公司有一项折扣政策：如果某位员工的直接上司已经购买了自己的股票，则该员工可以以原价的一半（向下取整 `floor(present[v] / 2)`）购买自己的股票。

在不超过给定 `budget` 的前提下，求能够获得的 **最大利润**（即所有购买后再以对应 `future` 价格卖出所得到的总收益减去总花费）。

**示例**  

示例 1  
```
Input: n = 2, present = [1,2], future = [4,3], hierarchy = [[1,2]], budget = 3
Output: 5
Explanation:
```

示例 2  
```
Input: n = 2, present = [3,4], future = [5,8], hierarchy = [[1,2]], budget = 4
Output: 4
Explanation:
```

示例 3  
```
Input: n = 3, present = [4,6,8], future = [7,9,11], hierarchy = [[1,2],[1,3]], budget = 10
Output: 10
Explanation:
```

示例 4  
```
Input: n = 3, present = [5,2,3], future = [8,5,6], hierarchy = [[1,2],[2,3]], budget = 7
Output: 12
Explanation:
```

**约束条件**  

- `1 <= n <= 160`
- `present.length == future.length == n`
- `1 <= present[i], future[i] <= 50`
- `hierarchy.length == n - 1`
- `hierarchy[i] == [u_i, v_i]`
- `1 <= u_i, v_i <= n`
- `u_i != v_i`
- `1 <= budget <= 160`
- 不存在重复的边
- 员工 `1` 是每个其他员工的直接或间接上司
- 输入的图 `hierarchy` 保证是 **无环**（acyclic）的树结构

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举所有可能的买入方案**，然后挑出满足预算且利润最高的那一个。  
具体做法：

1. 对每个员工 `i`，决定「买」或「不买」两种状态，用一个长度为 `n` 的二进制数组 `choose` 表示。  
2. 计算总花费：  
   - 若 `i` 的直接上司 `p` 没买，`i` 的买入价格是 `present[i]`。  
   - 若 `p` 已经买了，`i` 可以享受半价，实际价格是 `present[i] // 2`（向下取整）。  
3. 计算总利润：每买一个员工，就得到 `future[i] - 实际价格` 的收益。  
4. 检查总花费是否 ≤ `budget`，如果是，就把利润和当前答案比较，取最大值。

> **类比**：这一步就像在超市里挑选商品，想把钱花得最划算，必须尝试所有可能的挑选组合——当然，商品很多时，这种「全尝试」的办法会非常慢。

#### 代码（Python）

```python
from itertools import product
import math

def maxProfit_bruteforce(n, present, future, hierarchy, budget):
    # 建立父子关系，方便在遍历时判断是否能打折
    parent = [0] * (n + 1)          # parent[child] = its direct boss
    for u, v in hierarchy:
        parent[v] = u

    best = 0
    # 对每个员工枚举 0（不买） / 1（买） 的状态，2^n 种组合
    for mask in range(1 << n):
        cost = 0
        profit = 0
        ok = True
        for i in range(1, n + 1):
            if mask >> (i - 1) & 1:                     # 决定买 i
                # 判断上司是否已经买了
                p = parent[i]
                price = present[i - 1]
                if p != 0 and (mask >> (p - 1) & 1):   # 上司买了，打半价
                    price = price // 2
                cost += price
                profit += future[i - 1] - price
                if cost > budget:                      # 超预算，直接放弃
                    ok = False
                    break
        if ok:
            best = max(best, profit)
    return best
```

> **关键行解释**  
> - `mask >> (i - 1) & 1`：用位运算检查第 `i` 位是否为 1，代表「买」这位员工。  
> - `price // 2`：向下取整的半价，就是「打折」的规则。  

#### 复杂度  

- **时间复杂度**：`O(2^n * n)`  
  - 需要遍历所有 `2^n` 种买入组合，每种组合要遍历 `n` 个人检查费用和利润。  
  - 对于 `n = 160`，`2^n` 已经是天文数字，根本不可能在电脑上跑完。  
- **空间复杂度**：`O(n)`  
  - 只用了几个长度为 `n` 的数组来存父子关系和临时计数。

> **大白话**：`2^n` 就像把一枚硬币抛 `n` 次，所有可能的正反面组合数会翻倍增长。`n = 20` 时已经有 `1,048,576` 种，`n = 160` 更是天文数字，暴力搜索根本不行。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**对所有子集枚举**。实际上，树结构提供了**层次化的子问题**：  
- 每个员工只和自己的子树有关，子树之间互不影响。  
- 对同一子树，只需要关心**已经花了多少钱**，而不是具体买了哪些人。  

这正好适合 **树形背包（Tree DP + Knapsack）** 的思路：

1. **状态定义**  
   对每个节点 `u`，我们维护两个长度为 `budget+1` 的 DP 表：  
   - `dp0[u][c]`：在 `u` 的子树里，**父亲没有买** `u`（即没有折扣），总花费恰好是 `c` 时能够得到的**最大利润**。  
   - `dp1[u][c]`：在 `u` 的子树里，**父亲已经买** `u`（子节点可以打折），总花费恰好是 `c` 时的最大利润。  

2. **子问题的合并（背包合并）**  
   对于当前节点 `u`，先把它自己「买」或「不买」两种选择算出来（这一步不涉及子节点），得到两组「初始」DP（只含自己）。  
   然后遍历所有子节点 `v`，把 `v` 的 DP 表**合并**进 `u`：  
   - 如果在 `u` 的 **买** 场景下（即父亲已经买了 `u`），子节点 `v` 必须使用 **`dp1[v]`**（因为 `u` 已买，`v` 能打折）。  
   - 如果在 `u` 的 **不买** 场景下，子节点只能使用 **`dp0[v]`**（因为 `u` 没买，`v` 不能打折）。  
   合并过程和普通的 **0/1 背包** 完全一样：遍历当前已用的预算 `c1`，再遍历子树花费 `c2`，更新 `dp_new[c1 + c2] = max(dp_new[c1 + c2], dp_parent[c1] + dp_child[c2])`。  

3. **递归实现**  
   使用深度优先搜索（DFS）从根节点 `1` 开始，返回 `dp0[1]`（根的父亲不存在，视作「父亲没有买」）。  
   最终答案是 `max_{c ≤ budget} dp0[1][c]`，因为我们只要求总花费 **不超过** 预算，而不是恰好等于。

4. **为什么能打折**  
   - 当父亲买了，子节点的购买价格是 `present[i] // 2`，这在「买」的那一步直接用折扣后的价格计算成本和利润即可。  
   - 只要父亲买了，子树的所有后代都可以享受**连续的折扣**（因为每层的父亲都买了），这正是我们用 `dp1` 表示的意义——**子树内部的所有节点都在「父亲已买」的状态**。

> **类比**：  
> 把每棵子树想象成一个小背包，里面装的是「花费」和「对应的最大收益」两对数字。把子树背包装进父节点背包时，就像把几个小背包的物品放进一个更大的背包——要保证总重量（花费）不超过上限，同时价值（利润）最大化。

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(10000)

def maxProfit(n, present, future, hierarchy, budget):
    # ---------- 1. 建图 ----------
    g = [[] for _ in range(n + 1)]
    parent = [0] * (n + 1)
    for u, v in hierarchy:
        g[u].append(v)
        parent[v] = u

    # ---------- 2. 深度优先遍历，返回 (dp0, dp1) ----------
    # dp0 / dp1 是长度为 budget+1 的列表，-inf 表示不可达
    INF_NEG = -10**9

    def dfs(u):
        # 初始状态：只考虑自己，不考虑子树
        dp0 = [INF_NEG] * (budget + 1)   # 父亲未买 u 时的 DP
        dp1 = [INF_NEG] * (budget + 1)   # 父亲已买 u 时的 DP

        # ① 不买 u
        dp0[0] = 0          # 不花钱，利润 0
        dp1[0] = 0          # 即使父亲买了，自己不买也不花钱

        # ② 买 u
        # ① 父亲未买 → 付原价
        cost_full = present[u - 1]
        profit_full = future[u - 1] - cost_full
        if cost_full <= budget:
            dp0[cost_full] = max(dp0[cost_full], profit_full)

        # ② 父亲已买 → 打折价
        cost_half = present[u - 1] // 2
        profit_half = future[u - 1] - cost_half
        if cost_half <= budget:
            dp1[cost_half] = max(dp1[cost_half], profit_half)

        # ---------- 3. 合并子节点 ----------
        for v in g[u]:
            child_dp0, child_dp1 = dfs(v)

            # 为了不覆盖正在遍历的 dp，需要临时数组保存新状态
            new_dp0 = [INF_NEG] * (budget + 1)
            new_dp1 = [INF_NEG] * (budget + 1)

            # 合并到 dp0（父亲未买 u → 子节点只能在「父亲未买」的状态）
            for cur_cost in range(budget + 1):
                if dp0[cur_cost] == INF_NEG:
                    continue
                for add_cost in range(budget - cur_cost + 1):
                    if child_dp0[add_cost] == INF_NEG:
                        continue
                    nc = cur_cost + add_cost
                    new_dp0[nc] = max(new_dp0[nc],
                                      dp0[cur_cost] + child_dp0[add_cost])
            # 合并到 dp1（父亲已买 u → 子节点在「父亲已买」的状态）
            for cur_cost in range(budget + 1):
                if dp1[cur_cost] == INF_NEG:
                    continue
                for add_cost in range(budget - cur_cost + 1):
                    if child_dp1[add_cost] == INF_NEG:
                        continue
                    nc = cur_cost + add_cost
                    new_dp1[nc] = max(new_dp1[nc],
                                      dp1[cur_cost] + child_dp1[add_cost])

            dp0, dp1 = new_dp0, new_dp1

        return dp0, dp1

    dp0_root, _ = dfs(1)          # 根节点的父亲视作「未买」
    # ---------- 4. 取不超过预算的最大利润 ----------
    ans = max(dp0_root[:budget + 1])
    return ans
```

> **关键行解释**  
> - `dp0[0] = 0`、`dp1[0] = 0`：表示「不花钱」的基线情况。  
> - `cost_full` / `cost_half`：分别是「原价」和「折后价」。  
> - 合并子树时的双层循环 `for cur_cost`、`for add_cost`：就是普通的 0/1 背包「把两个背包的容量相加」的过程。  
> - `INF_NEG`：用一个极小值表示「这个花费不可能达到」，防止错误的 `max` 更新。  

#### 复杂度  

- **时间复杂度**：`O(n * budget²)`  
  - 对每个节点，需要把它的子树 DP（大小 `budget+1`）和当前 DP 做一次「背包合并」——这一步是 `O(budget²)`。  
  - `n ≤ 160`、`budget ≤ 160`，所以最坏约为 `160 * 160² ≈ 4 * 10⁶` 次基本操作，完全可以在一秒内跑完。  

- **空间复杂度**：`O(n * budget)`  
  - 每个节点保留两个长度为 `budget+1` 的数组（递归返回后会被父节点回收），整体峰值大约是 `2 * (budget+1) * depth`，深度 ≤ `n`，在本题约 `2 * 161 * 160 ≈ 5.1万` 个整数，几百 KB 的内存。  

> **对比暴力**：  
> 暴力是 `O(2ⁿ)`，根本不可行；而 DP 把指数级下降到多项式 `O(n·budget²)`，利用了树的层次结构和「只关心花费多少」的背包思想。

---

## 心得

- **核心技巧**：**树形背包 + 状态转移（父亲是否买）**。  
- **适用场景**  
  1. **带折扣或依赖关系的背包**（例如「父节点买了子节点半价」）。  
  2. **树上选点最大价值**（如「公司组织结构选员工参加培训」），常用 **树形 DP + 费用约束**。  
  3. **每个节点有两种状态影响子树**（如「是否开启某种功能」），需要维护 **两套 DP**。  
- **一句话总结解题钥匙**：  
  > 把每棵子树看成「花费‑收益」的背包，用父亲是否买决定子树使用的折扣状态，层层合并即可得到全局最优。

---

## 反思

- **第一反应**：看到「父亲买了可以半价」立刻想到「状态依赖」——于是想到要把「父亲是否买」作为 DP 的维度。  
- **最容易踩的坑**  
  1. **费用上限的处理**：DP 必须是「恰好花费 `c`」的最大利润，最后取「不超过」预算的最大值，别直接把数组下标当作「≤」的意思。  
  2. **折半取整**：`present[i] // 2` 必须在买入时就算好，不能在合并子树后再改。  
  3. **负利润的情况**：如果 `future[i] - price` 为负，仍然可以「买」但会降低总利润，DP 中需要保留这种可能（因为后面的子树可能带来更大收益）。  
  4. **递归深度**：`n` 最高 160，递归深度不会爆栈，但在实际实现中仍建议 `sys.setrecursionlimit` 提高上限。  
- **下次遇到同类题**：第一步先**把树拆成子问题**，确定「是否受父节点影响」的两套 DP；随后**做背包合并**，注意费用上限的循环顺序（从大到小或使用临时数组均可）。  

祝你玩转树形背包，解锁更多 Hard 级别的 LeetCode！