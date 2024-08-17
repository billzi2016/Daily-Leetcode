# #2830. 最大化推销员的利润 / Maximize the Profit as the Salesman

> 难度：中等 · 标签：Array、Hash Table、Binary Search、Dynamic Programming、Sorting · [LeetCode 链接](https://leetcode.com/problems/maximize-the-profit-as-the-salesman/)

---

## 题目（英文原版）

**Description**

You are given an integer n representing the number of houses on a number line, numbered from 0 to n - 1.
Additionally, you are given a 2D integer array offers where offers[i] = [starti, endi, goldi], indicating that ith buyer wants to buy all the houses from starti to endi for goldi amount of gold.
As a salesman, your goal is to maximize your earnings by strategically selecting and selling houses to buyers.
Return the maximum amount of gold you can earn.
Note that different buyers can't buy the same house, and some houses may remain unsold.

**Examples**

**Example 1:**

```
Input: n = 5, offers = [[0,0,1],[0,2,2],[1,3,2]]
Output: 3
Explanation: There are 5 houses numbered from 0 to 4 and there are 3 purchase offers.
We sell houses in the range [0,0] to 1st buyer for 1 gold and houses in the range [1,3] to 3rd buyer for 2 golds.
It can be proven that 3 is the maximum amount of gold we can achieve.
```

**Example 2:**

```
Input: n = 5, offers = [[0,0,1],[0,2,10],[1,3,2]]
Output: 10
Explanation: There are 5 houses numbered from 0 to 4 and there are 3 purchase offers.
We sell houses in the range [0,2] to 2nd buyer for 10 golds.
It can be proven that 10 is the maximum amount of gold we can achieve.
```

**Constraints**

- 1 <= n <= 105
- 1 <= offers.length <= 105
- offers[i].length == 3
- 0 <= starti <= endi <= n - 1
- 1 <= goldi <= 103

---

## 题目（中文翻译）

你得到一个整数 `n`，表示在数轴上编号为 `0` 到 `n - 1` 的房子（houses）的数量。  
同时，给定一个二维整数数组 `offers`，其中 `offers[i] = [starti, endi, goldi]` 表示第 `i` 位买家（buyer）想以 `goldi` 金币（gold）购买从 `starti` 到 `endi` 的所有房子。  

作为推销员（salesman），你的目标是通过策略性地挑选并向买家出售房子来最大化你的收益。  
返回你能够获得的最大金币数量。  

**注意**：不同的买家不能购买同一套房子，且可以有房子不被出售。

## 示例

### 示例 1
**输入**：`n = 5, offers = [[0,0,1],[0,2,2],[1,3,2]]`  
**输出**：`3`  
**解释**：共有 5 栋房子，编号为 `0` 到 `4`，共有 3 个购买报价。  
我们将区间 `[0,0]` 的房子卖给第 1 位买家，获得 `1` 金币；将区间 `[1,3]` 的房子卖给第 3 位买家，获得 `2` 金币。  
可以证明，`3` 是能够获得的最大金币数。

### 示例 2
**输入**：`n = 5, offers = [[0,0,1],[0,2,10],[1,3,2]]`  
**输出**：`10`  
**解释**：共有 5 栋房子，编号为 `0` 到 `4`，共有 3 个购买报价。  
我们将区间 `[0,2]` 的房子卖给第 2 位买家，获得 `10` 金币。  
可以证明，`10` 是能够获得的最大金币数。

## 约束条件
- `1 <= n <= 10^5`
- `1 <= offers.length <= 10^5`
- `offers[i].length == 3`
- `0 <= starti <= endi <= n - 1`
- `1 <= goldi <= 10^3`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **每一个** 购买报价都当成「要么接受，要么不接受」的二选一决策。  
我们可以枚举所有可能的选择组合，检查组合里有没有 **冲突**（即两个报价的区间有交集），如果没有冲突就把它们的 `gold` 累加，取最大值。

- **使用的数据结构**：  
  - `offers` 本身是一个二维数组，像一本「买卖合同清单」。  
  - 在检验冲突时，我们可以把已经挑选的区间放进一个列表，逐个比较，就像把买来的房子编号写在纸上，检查新来的买家是否想要已经写好的房子。  

- **为什么正确**：  
  只要我们遍历了 **所有** 可能的挑选方式，最大收益必然出现在其中的某一次遍历。只要对每一次遍历都正确判断是否冲突并正确累计收益，最终的最大值一定是正确答案。

- **复杂度分析**：  
  - 设报价数量为 `m = len(offers)`。  
  - 枚举所有子集需要 `2^m` 种可能（每个报价有「选」或「不选」两种状态），这就是 **指数级** 的时间。  
  - 检查冲突时最坏需要遍历已经选中的所有区间，最坏是 `O(m)`，但这已经被 `2^m` 主导。  
  - 所以 **时间复杂度** 为 `O(2^m * m)`，在实际数据（`m` 可达 10^5）下根本不可用。  
  - **空间复杂度** 只需要保存递归栈或遍历时的临时列表，`O(m)`。

#### 代码（Python）

```python
from typing import List

def maxProfit_bruteforce(n: int, offers: List[List[int]]) -> int:
    m = len(offers)
    best = 0                     # 保存全局最大收益

    # 用深度优先搜索枚举每一个报价是否选取
    def dfs(idx: int, chosen: List[List[int]], cur_gold: int):
        nonlocal best
        # 已经遍历完所有报价
        if idx == m:
            best = max(best, cur_gold)
            return

        # 1️⃣ 不选第 idx 个报价
        dfs(idx + 1, chosen, cur_gold)

        # 2️⃣ 选第 idx 个报价，先检查是否与已选区间冲突
        s, e, g = offers[idx]
        conflict = False
        for cs, ce, _ in chosen:           # 与每个已选区间逐一比较
            if not (e < cs or s > ce):    # 区间有交集即冲突
                conflict = True
                break
        if not conflict:                   # 没冲突就可以选
            chosen.append(offers[idx])     # 加入已选集合
            dfs(idx + 1, chosen, cur_gold + g)
            chosen.pop()                   # 回溯，撤销选择

    dfs(0, [], 0)
    return best
```

> **关键行中文注释** 已写在代码里，帮助初学者逐行理解。

#### 复杂度

- **时间复杂度**：`O(2^m * m)`  
  - `2^m` 表示「每个报价都有选或不选两种可能」，指数级增长。即使 `m` 只有 20，`2^20 ≈ 1,048,576` 已经很大，更别提题目给的 `10^5` 了。
- **空间复杂度**：`O(m)`  
  - 递归深度最多 `m`，以及保存已选区间的列表最多也只有 `m` 条。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举所有组合**。实际上，**区间之间的冲突只和它们的起止位置有关**，我们可以把「把区间装进房子序列」的过程改写成 **动态规划**（DP），只在每个位置记录「到这里为止能得到的最大收益」即可。

下面一步步推导最优思路：

1. **把区间按左端点排序**  
   - 想象把所有报价从左到右排好队，先处理左边的报价再处理右边的。这样当我们决定「是否接受某个报价」时，已经知道了左侧所有可能的最优收益。  
   - 类比：买菜时先挑最左边的摊位，后面的摊位只需要考虑左边已经买了哪些东西。

2. **定义 DP 状态**  
   - `dp[i]` 表示「把房子编号 `[0 … i]`（包含 i）都考虑进去后，能够得到的最大金子数」。  
   - 这里的「考虑进去」指的是：我们可以选择不卖第 i 号房子，也可以卖一段以 i 为右端点的报价。

3. **状态转移**  
   - **不卖第 i 号房子**：`dp[i] = dp[i-1]`（收益不变，只是把第 i 号留空）。  
   - **卖以 i 为右端点的某个报价**：假设有报价 `[start, i, gold]`，我们必须保证 `start … i` 这段房子只能被这笔交易占用。此时左侧还能得到的最大收益是 `dp[start-1]`（如果 `start == 0`，左侧没有房子，收益为 0）。  
     所以候选值为 `dp[start-1] + gold`。我们把所有以 `i` 为右端点的报价都算一遍，取最大即可。

   公式合在一起：

   ```
   dp[i] = max( dp[i-1],
                max_{offer (start, i, gold)} ( dp[start-1] + gold ) )
   ```

4. **实现细节**  
   - 为了快速得到「所有右端点为 i 的报价」，我们可以在遍历前把报价 **按 end** 分组，存进一个字典 `offers_by_end[i]`。这一步相当于「把每个摊位的商品贴标签，方便后面直接取出」。  
   - 由于 `n` 和 `offers` 都可能高达 `10^5`，我们必须 **一次遍历** 完成 DP，整体复杂度保持在 `O(n + m log m)`（排序需要 `m log m`，DP 线性遍历 `n`，分组 `O(m)`）。

5. **为什么比暴力快**  
   - 暴力是指数级遍历所有组合；DP 只在每个房子位置保存一个最优值，**不需要记忆所有组合**，所以时间从指数级降到线性级。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def maxProfit(n: int, offers: List[List[int]]) -> int:
    """
    动态规划实现
    dp[i] : 处理完编号为 0..i 的房子后，能够得到的最大金子数
    """
    # 1️⃣ 把所有报价按照右端点 end 分组，便于 O(1) 取出
    offers_by_end = defaultdict(list)          # end -> [(start, gold), ...]
    for s, e, g in offers:
        offers_by_end[e].append((s, g))

    # 2️⃣ 初始化 dp 数组，dp[-1] 用 0 表示（处理 0 之前的房子收益为 0）
    dp = [0] * n                                 # dp[i] 对应房子 i

    for i in range(n):
        # 先把不卖第 i 号房子的情况继承下来
        if i > 0:
            dp[i] = dp[i - 1]

        # 再遍历所有右端点恰好是 i 的报价，尝试把它们卖掉
        for start, gold in offers_by_end.get(i, []):
            # left_profit = dp[start-1]（如果 start==0，则为 0）
            left_profit = dp[start - 1] if start > 0 else 0
            dp[i] = max(dp[i], left_profit + gold)

    # 最后一个位置的 dp 值就是答案
    return dp[-1]
```

**代码要点解释**  

| 行号 | 解释 |
|------|------|
| 4‑6 | 使用 `defaultdict(list)` 把所有报价按照右端点 `end` 收集，类似「把相同颜色的球放进同一个盒子」 |
| 12‑13 | 创建长度为 `n` 的 DP 表，`dp[i]` 只存一个整数，空间只和房子数量线性相关 |
| 16‑23 | 主循环：从左到右遍历每个房子编号 `i`，先把「不卖」的收益复制过来，再检查所有「以 i 为右端点」的报价 |
| 20‑21 | 计算左侧已经卖出的最大收益 `left_profit`，如果报价从第 0 号房子开始，则左侧收益为 0 |
| 22 | 用 `max` 把「不卖」和「卖这笔报价」两种情况取最大，更新 `dp[i]` |
| 26 | 循环结束后，`dp[n-1]` 保存了整个区间 `[0 … n-1]` 的最优收益 |

#### 复杂度

- **时间复杂度**：`O(n + m log m)`  
  - `m log m` 来自对 `offers` 按 `end`（或 `start`）的排序/分组。  
  - DP 主循环遍历 `n` 次，每次只检查与当前右端点对应的报价，所有报价总共只会被遍历一次，所以是线性 `O(m)`。  
  - 与暴力解的指数级 `2^m` 相比，这个复杂度在 `n,m ≤ 10^5` 时完全可接受。

- **空间复杂度**：`O(n + m)`  
  - `dp` 数组占 `O(n)`。  
  - `offers_by_end` 保存所有报价的引用，占 `O(m)`。  
  - 只用了几倍于输入规模的额外空间，符合题目限制。

---

## 心得

- **核心技巧**：把「区间不相交」的约束转化为「前缀最优」的动态规划。  
- **适用的题型**  
  1. **“房屋租赁/买卖”** 类的区间选择题（如 LeetCode 1235 `Maximum Profit in Job Scheduling`）。  
  2. **“带权区间调度”**（Weighted Interval Scheduling）问题。  
  3. **“划分区间求最优”**（如在数组上做区间 DP）的问题。  
- **一句话总结**：**把每个区间看成「把左边的最优收益 + 本区间价值」的组合，按右端点递推即可得到全局最优**。

---

## 反思

- **第一反应**：看到「不同买家不能买同一套房子」立刻想到「区间不相交」的经典调度问题，于是想到了「枚举所有子集」的暴力思路。  
- **最容易踩的坑**  
  - **遗漏空房子**：有些房子可以不卖，`dp[i]` 必须能继承 `dp[i-1]`，否则会误把必须卖完的假设写进去。  
  - **边界条件**：`start == 0` 时左侧没有房子，`dp[-1]` 不能直接取，需要手动返回 0。  
  - **分组方式**：如果把报价按 `start` 分组而在 DP 中按 `end` 查询，会导致找不到对应的区间，需要保持「右端点 → 区间」的映射。  
- **下次第一步**：先 **把区间按照结束位置排序/分组**，然后思考「当前右端点的最优是左侧最优 + 本区间价值」的递推式，这通常是区间调度类问题的关键起点。