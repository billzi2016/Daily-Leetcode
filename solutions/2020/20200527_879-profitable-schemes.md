# #879. 盈利计划 / Profitable Schemes

> 难度：困难 · 标签：Array、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/profitable-schemes/)

---

## 题目（英文原版）

**Description**

There is a group of n members, and a list of various crimes they could commit. The ith crime generates a profit[i] and requires group[i] members to participate in it. If a member participates in one crime, that member can't participate in another crime.
Let's call a profitable scheme any subset of these crimes that generates at least minProfit profit, and the total number of members participating in that subset of crimes is at most n.
Return the number of schemes that can be chosen. Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 5, minProfit = 3, group = [2,2], profit = [2,3]
Output: 2
Explanation: To make a profit of at least 3, the group could either commit crimes 0 and 1, or just crime 1.
In total, there are 2 schemes.
```

**Example 2:**

```
Input: n = 10, minProfit = 5, group = [2,3,5], profit = [6,7,8]
Output: 7
Explanation: To make a profit of at least 5, the group could commit any crimes, as long as they commit one.
There are 7 possible schemes: (0), (1), (2), (0,1), (0,2), (1,2), and (0,1,2).
```

**Constraints**

- 1 <= n <= 100
- 0 <= minProfit <= 100
- 1 <= group.length <= 100
- 1 <= group[i] <= 100
- profit.length == group.length
- 0 <= profit[i] <= 100

---

## 题目（中文翻译）

**描述**  
有一支由 `n` 名成员组成的团队，并且有一系列不同的犯罪行为可供选择。第 `i` 种犯罪会带来 `profit[i]` 的利润，并且需要 `group[i]` 名成员参与。如果某个成员已经参加了某个犯罪，则该成员不能再参加其他犯罪。  

我们将**盈利计划**定义为：从这些犯罪中挑选的一个子集（subset），使得该子集产生的总利润至少为 `minProfit`，且参与这些犯罪的成员总数不超过 `n`。  

返回可以选择的盈利计划的数量。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

**示例 1**  
输入：`n = 5, minProfit = 3, group = [2,2], profit = [2,3]`  
输出：`2`  
解释：要获得至少 3 的利润，团队可以选择犯罪 0 与 1 同时进行，或者仅进行犯罪 1。共计有 2 种方案。

**示例 2**  
输入：`n = 10, minProfit = 5, group = [2,3,5], profit = [6,7,8]`  
输出：`7`  
解释：只要进行至少一种犯罪，就能满足利润不少于 5 的要求。可能的方案有 7 种：`(0)`, `(1)`, `(2)`, `(0,1)`, `(0,2)`, `(1,2)`, `(0,1,2)`。

**约束条件**  

- `1 <= n <= 100`
- `0 <= minProfit <= 100`
- `1 <= group.length <= 100`
- `1 <= group[i] <= 100`
- `profit.length == group.length`
- `0 <= profit[i] <= 100`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**枚举所有可能的犯罪组合**，检查每个组合是否满足：

1. 参与人数 ≤ `n`  
2. 总利润 ≥ `minProfit`  

这相当于把每个犯罪当成“要不要选”的二进制位，所有位组成一个二进制数。  
比如有 3 项犯罪，二进制 `101` 表示选第 0 项和第 2 项。  

- **用到的数据结构**：  
  - **列表（list）** 保存 `group[i]`、`profit[i]`。  
  - **递归栈**（或者显式的 `for` 循环）用来遍历每一种“选 / 不选” 的决定。  
  - **计数器** 用来累计满足条件的组合数。  

> 类比：把所有犯罪想象成一本词典，每个词条是“是否参与”。暴力枚举就像把词典的每一页都翻一遍，找出所有满足条件的页码。

- **为什么这个方法正确**：  
  枚举覆盖了 **所有** 子集（即所有可能的犯罪组合），只要在遍历过程中把符合要求的子集计数，最终得到的计数自然就是答案。

- **时间/空间复杂度**（大白话版）：  
  - 时间复杂度：`O(2^m * m)`，其中 `m = len(group)`。  
    - `2^m` 表示“所有子集的数量”。比如 `m=20`，子集数约为 `1,048,576`，已经很大了。  
    - 乘以 `m` 是因为每次检查子集时，需要把子集里所有选中的犯罪累加人数和利润。  
  - 空间复杂度：`O(m)`，只需要递归栈（最深 `m` 层）和若干计数变量。

> **直觉解适合**：`m` 很小（如 ≤ 15）时可以直接跑通；但在本题 `m` 最多 100，根本不可行，只能作为思考起点。

#### 代码（Python）

```python
MOD = 10**9 + 7

def profitableSchemes_bruteforce(n, minProfit, group, profit):
    m = len(group)
    ans = 0                     # 计数满足条件的方案数

    def dfs(idx, members_used, cur_profit):
        """深度优先搜索所有子集
        idx：当前考虑的犯罪下标
        members_used：已经使用的人数
        cur_profit：累计的利润
        """
        nonlocal ans
        # 已经遍历完所有犯罪
        if idx == m:
            if cur_profit >= minProfit:   # 利润够了就计数
                ans = (ans + 1) % MOD
            return

        # 情况1：不选第 idx 项
        dfs(idx + 1, members_used, cur_profit)

        # 情况2：选第 idx 项（前提是人数不超限）
        need = group[idx]
        if members_used + need <= n:       # 只要人数还能容下，就可以选
            dfs(idx + 1,
                members_used + need,
                cur_profit + profit[idx])
        # 否则直接跳过选这项的分支

    dfs(0, 0, 0)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(2^m * m)`  
  > 想象一下把一棵二叉树遍历完，树的高度是 `m`，节点总数约为 `2^m`，每次递归里还有一次 O(m) 的累加。  
- **空间复杂度**：`O(m)`  
  > 递归栈的深度最多 `m`，其余只用常数级的额外空间。

---

### 2. 最优解  

#### 思路  

从暴力解可以看出，**枚举子集的根本瓶颈**是“每次都要把所有已选的犯罪重新累加”。  
如果我们在遍历过程中把**“已使用的人数”和“已获得的利润”**这两个维度的状态保存下来，就可以**重复利用**已经算好的子结果，避免重复计算——这正是**动态规划（DP）**的核心思想。

**关键观察**  

1. 每个犯罪只能选或不选，顺序不重要，只要知道“用了多少人”和“赚了多少利润”。  
2. `n ≤ 100`，`minProfit ≤ 100`，这两个数都不大，完全可以把它们作为 DP 的维度。  

**状态定义**  

`dp[i][j]` = 使用 **不超过** `i` 个人，且 **赚到的利润至少** `j`（`j` 被截断到 `minProfit`）的方案数。  

- `i` 范围 `0 … n`（最多 `n` 个人）  
- `j` 范围 `0 … minProfit`（我们只关心是否达到最小利润）  

**状态转移**  

遍历每个犯罪 `(need = group[k], earn = profit[k])`，对已有的 DP 表进行“背包”式更新（**从大到小**防止同一个犯罪被重复使用）：

```
for i from n down to need:
    for j from minProfit down to 0:
        # 如果我们选了当前犯罪，之前的状态是 (i-need, j')
        # 其中 j' = max(0, j - earn)  // 因为利润可以超过 minProfit，截到 minProfit
        dp[i][j] = (dp[i][j] + dp[i-need][max(0, j-earn)]) % MOD
```

**初始化**  

- `dp[0][0] = 1`：不使用任何人，赚到 0 利润，这是一种合法的“空方案”。  
- 其它 `dp[*][*]` 初始为 0。

**答案**  

遍历完所有犯罪后，`dp[i][minProfit]`（`i = 0 … n`）的总和即为所有满足 **人数 ≤ n 且利润 ≥ minProfit** 的方案数。  

**为什么可以把利润截到 `minProfit`**  

我们只关心“是否达到或超过”目标利润。若在某一步已经赚到 ≥ `minProfit`，后面再加多少利润都不影响最终判断。于是把所有大于 `minProfit` 的利润视作等同的状态 `minProfit`，可以显著降低 DP 表的大小。

**类比**：  
把 DP 想成一个 **二维的存钱罐**，横坐标是“用了多少人”，纵坐标是“已经存了多少利润”。每加入一种犯罪，就往右上角的格子里“倒钱”，倒进去的量取决于这项犯罪需要多少人和能赚多少钱。最终我们只看最右边（用到最多人）且最高的那一行（利润 ≥ 目标）有多少种倒法。

#### 代码（Python）

```python
MOD = 10**9 + 7

def profitableSchemes(n, minProfit, group, profit):
    """
    动态规划版（二维 DP，空间 O(n * minProfit)）
    """
    m = len(group)
    # dp[i][j] 表示使用 i 个人，利润至少为 j 的方案数
    dp = [[0] * (minProfit + 1) for _ in range(n + 1)]
    dp[0][0] = 1                       # 空方案

    for idx in range(m):
        need = group[idx]               # 需要的人数
        earn = profit[idx]              # 这件事能赚的利润

        # 必须倒序遍历，防止同一件事被多次计入同一个状态
        for i in range(n, need - 1, -1):            # 人数从大到小
            for j in range(minProfit, -1, -1):      # 利润从大到小
                # 计算选了当前犯罪后，新利润的下标
                new_profit = max(0, j - earn)       # 赚的利润可能已经超出 minProfit
                dp[i][j] = (dp[i][j] + dp[i - need][new_profit]) % MOD

    # 所有使用 ≤ n 个人、利润 ≥ minProfit 的方案数之和
    ans = sum(dp[i][minProfit] for i in range(n + 1)) % MOD
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(m * n * minProfit)`  
  > `m` 是犯罪数量（最多 100），`n` ≤ 100，`minProfit` ≤ 100，三者相乘最多是 `10⁶`，在 Python 中毫秒级可跑完。  
  > 与暴力解的 `2^m` 相比，指数级下降为多项式级，速度提升数千倍甚至更多。  

- **空间复杂度**：`O(n * minProfit)`  
  > 只需要一个二维数组，大小约为 `101 * 101 ≈ 10⁴`，几乎可以忽略不计。  

---

## 心得  

- **核心技巧**：把“人数”和“利润”这两个约束一起做成 **二维背包 DP**，并对利润做上界截断。  
- **适用的题型**（类似思路）：  
  1. **《零钱兑换 II》**（组合数背包）  
  2. **《分配糖果》**（限定人数/资源的组合计数）  
  3. **《目标和》**（把状态压缩到目标阈值）  
- **一句话总结**：**把每个犯罪当成背包里的物品，用“人数”作容量，用“利润”作价值，DP 累计所有装满背包且价值够大的装法**。

---

## 反思  

- **第一反应**：直接写递归或遍历子集，想到“暴力枚举”。  
- **最容易踩的坑**：  
  - **利润上界**：忘记把利润截到 `minProfit`，导致 DP 表过大、甚至超时。  
  - **状态更新顺序**：若正序遍历 `i`，同一个犯罪会被多次计入同一方案，结果会被夸大。  
  - **模数取模**：在累加时忘记取 `% MOD`，会导致整数溢出。  
- **下次遇到同类题**：第一步先**判断约束是否足够小**，能否把关键维度（如人数、价值）做成 DP 的坐标；然后**考虑是否需要对某些维度做截断**（如本题的利润）。  

祝你玩转 DP，继续加油 🚀