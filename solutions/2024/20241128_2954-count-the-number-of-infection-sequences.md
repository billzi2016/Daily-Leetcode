# #2954. **感染序列的计数** / Count the Number of Infection Sequences

> 难度：困难 · 标签：Array、Math、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-infection-sequences/)

---

## 题目（英文原版）

**Description**

You are given an integer n and an array sick sorted in increasing order, representing positions of infected people in a line of n people.
At each step, one uninfected person adjacent to an infected person gets infected. This process continues until everyone is infected.
An infection sequence is the order in which uninfected people become infected, excluding those initially infected.
Return the number of different infection sequences possible, modulo 109+7.

**Examples**

**Example 1:**

```
Input: n = 5, sick = [0,4]
Output: 4
Explanation:
There is a total of 6 different sequences overall.
```

**Example 2:**

```
Input: n = 4, sick = [1]
Output: 3
Explanation:
There is a total of 6 different sequences overall.
```

**Constraints**

- 2 <= n <= 105
- 1 <= sick.length <= n - 1
- 0 <= sick[i] <= n - 1
- sick is sorted in increasing order.

---

## 题目（中文翻译）

给定整数 `n` 与一个递增排序的数组 `sick`，其中 `sick` 表示一条长度为 `n` 的人群中已感染（infected）人的位置。  

每一步，任意一个与已感染（infected）人相邻的未感染（uninfected）人会被感染。该过程持续进行，直至所有人都被感染。  

**感染序列（infection sequence）** 指的是除最初已感染（infected）的人之外，未感染（uninfected）人被感染的顺序。  

返回不同感染序列的数量，对 `10^9+7` 取模。

**示例 1**

```text
Input: n = 5, sick = [0,4]
Output: 4
Explanation:
共有 6 种不同的序列，但只计数满足题目要求的序列数为 4。
```

**示例 2**

```text
Input: n = 4, sick = [1]
Output: 3
Explanation:
共有 6 种不同的序列，但满足题目要求的序列数为 3。
```

**约束条件**

- `2 <= n <= 10^5`
- `1 <= sick.length <= n - 1`
- `0 <= sick[i] <= n - 1`
- `sick` 按递增顺序排序。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把每一步的 **所有合法选择** 都枚举出来，逐步模拟感染过程，直到所有人都被感染为止。  
- **数据结构**：我们可以用一个长度为 `n` 的布尔数组 `infected`（或 `0/1`）来记录每个人是否已经感染。把题目里给出的 `sick` 位置先标记为 `True`。  
- **每一步的合法选择**：遍历整个数组，找出所有 **未感染且恰好与已感染的相邻位置相邻** 的人（左边或右边相邻）。把这些位置收集进列表 `candidates`。  
- **递归/回溯**：对 `candidates` 中的每一个位置，假装把它感染，然后递归继续下一步。每当所有人都感染完毕，就计数 +1。  

> **生活化类比**：把整排小朋友想象成一本词典，已经感染的词条就像已经划掉的页码。每一步只能在已经划掉的页码左右两侧挑选一个未划掉的页码来继续划掉。我们把所有可能的挑选顺序全部写下来，就是所谓的“感染序列”。

这个方法一定能得到正确答案，因为它穷举了**所有**合法的感染顺序。只要递归的终止条件（全部感染）和每一步的合法选择写对了，计数就不会漏。

#### 代码（Python）

```python
MOD = 10**9 + 7

def count_bruteforce(n: int, sick: list) -> int:
    # 用 1 表示已感染，0 表示未感染
    infected = [0] * n
    for p in sick:
        infected[p] = 1

    def dfs(cur_infected, remaining):
        """返回从当前状态继续下去的感染序列数量"""
        if remaining == 0:          # 所有人都已经感染
            return 1

        # 收集本轮所有可以感染的下标
        candidates = []
        for i in range(n):
            if cur_infected[i] == 0:
                # 只要左或右有已感染的，就可以被感染
                if (i > 0 and cur_infected[i-1] == 1) or (i < n-1 and cur_infected[i+1] == 1):
                    candidates.append(i)

        total = 0
        for idx in candidates:
            cur_infected[idx] = 1          # 假装感染了 idx
            total += dfs(cur_infected, remaining-1)
            total %= MOD
            cur_infected[idx] = 0          # 恢复现场，回溯

        return total

    return dfs(infected, n - len(sick))
```

> **注意**：这段代码仅用于说明思路，`n` 甚至几百时就会因为指数级的递归爆炸而不可用。

#### 复杂度  

- **时间复杂度**：`O(2^S)`（指数级），其中 `S = n - len(sick)` 是需要感染的人数。因为每一步至少有 1 条、至多 2 条选择，递归树的宽度大约是 `2^S`。  
  > 大白话：如果还有 20 个人没感染，理论上会有 `2^20 ≈ 1,000,000` 种不同的顺序，计算量会爆炸。  
- **空间复杂度**：`O(S)`，递归栈深度最多等于需要感染的人数。

> 结论：暴力解只能在非常小的 `n`（比如 `n ≤ 10`）下跑通，远不能满足题目 `n ≤ 10^5` 的要求。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，真正的难点不在“谁先感染”，而在 **不同段落之间的相对顺序** 与 **同一段落内部的多种选择**。我们把整排人分成若干 **连续的未感染区间**（段），每个区间的两端要么是已感染的人，要么是边界（第一个或最后一个位置）。

```
0 1 1 1 0 1 1 0 1
^   ^   ^   ^   ^
已感染位置 (sick)    →  把它们视作 “墙”
```

- **两端都有已感染** 的区间（中间段），例如 `0 1 1 1 0` 中的 `111`，在每一步可以从左端或右端感染，**相当于有 2 条分支**。  
- **仅一端有已感染** 的区间（起始段或结束段），例如最左侧的 `1110`，只能从靠已感染的一端往里感染，**只有 1 条分支**。

因此，整个过程可以抽象为：

1. **先决定每个区间内部的感染顺序**（每个区间内部的相对顺序相互独立）。  
2. **再把所有区间的“步数”混合在一起**，因为每一步我们可以任选一个还有未感染的区间继续感染。

这正好对应 **多项式系数** 与 **组合数学**：

- 设所有需要感染的孩子总数为 `S = Σ len_i`（所有区间长度之和）。  
- 把 `S` 步分配给若干区间，每个区间 `i` 必须出现 `len_i` 步。不同的分配方式数量为  

  \[
  \frac{S!}{len_1! \cdot len_2! \cdots len_m! \cdot len_{start}! \cdot len_{end}!}
  \]

  这一步是 **排列组合** 中的“多重集合排列”。

- 对于每个 **两端都有已感染** 的区间，内部的感染顺序还有额外的自由度。  
  - 区间长度为 `L`，从左或右任选一步，等价于在 `L-1` 次选择中每次都有 2 种可能（最后一步只有唯一的选择）。  
  - 所以该区间贡献 `2^{L-1}` 种内部顺序。  
  - 把所有这类区间的贡献相乘得到 `2^{k}`，其中  

    \[
    k = \sum_{i\in\text{middle}} (len_i - 1)
    \]

综上，答案公式为  

\[
\text{Ans} = \frac{S!}{\prod\limits_{i} len_i!}\times 2^{k} \pmod{10^9+7}
\]

> **类比**：把每个未感染区间想象成一盒相同颜色的弹珠，盒子之间的顺序可以随意混合（相当于把所有弹珠倒进同一个大盒子再重新排），而盒子内部如果可以从两头取弹珠，就像弹珠可以先从左边或右边滚出来，产生额外的 `2` 倍选择。

**实现细节**

1. **预处理阶乘和逆元**：`n ≤ 10^5`，需要快速计算组合数。使用模 `MOD = 10^9+7` 的 **费马小定理** 求逆元，预先算出 `fact[i]` 与 `inv_fact[i]`（`i!` 与 `(i!)^{-1}`）到 `n`。  
2. **划分区间**：遍历 `sick`，找出相邻已感染位置之间的空隙。  
   - 若 `gap = sick[i] - sick[i-1] - 1 > 0`，则这是一个 **中间段**，长度为 `gap`。  
   - 开头段：若 `sick[0] > 0`，长度为 `sick[0]`（左边界没有已感染）。  
   - 结尾段：若 `sick[-1] < n-1`，长度为 `n-1 - sick[-1]`（右边界没有已感染）。  
3. **累加**  
   - `total_len += len`（即 `S`）  
   - 对每个长度乘以对应的阶乘倒数（即除以 `len!`）  
   - 对每个中间段累加 `k += len-1`  
4. **最终答案**  

   \[
   ans = fact[total\_len] \times \Bigl(\prod inv\_fact[len]\Bigr) \times 2^{k} \pmod{MOD}
   \]

#### 代码（Python）

```python
MOD = 10**9 + 7

def precompute_factorials(limit: int):
    """返回 fact[i] = i! % MOD, inv_fact[i] = (i!)^{-1} % MOD"""
    fact = [1] * (limit + 1)
    for i in range(1, limit + 1):
        fact[i] = fact[i-1] * i % MOD

    inv_fact = [1] * (limit + 1)
    # 费马小定理：a^{MOD-2} ≡ a^{-1} (mod MOD)
    inv_fact[limit] = pow(fact[limit], MOD-2, MOD)
    for i in range(limit, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    return fact, inv_fact

def count_infection_sequences(n: int, sick: list) -> int:
    """
    最优解：利用组合数学 + 预计算阶乘
    时间 O(n)   空间 O(n)
    """
    m = n                         # 需要的阶乘上界 ≤ n
    fact, inv_fact = precompute_factorials(m)

    total_len = 0                 # S：所有未感染孩子的总数
    denominator = 1               # 用来累计 ∏ len_i!
    extra_pow = 0                 # k：中间段内部的 2^{len-1} 次方累计

    # ----- 处理开头段 -----
    if sick[0] > 0:
        start_len = sick[0]       # 位置 0~sick[0]-1 都未感染
        total_len += start_len
        denominator = denominator * fact[start_len] % MOD
        # 开头段只有一个端点可感染，不贡献 extra_pow

    # ----- 处理两两已感染之间的中间段 -----
    for i in range(1, len(sick)):
        gap = sick[i] - sick[i-1] - 1   # 两个已感染之间的空位数
        if gap == 0:
            continue
        total_len += gap
        denominator = denominator * fact[gap] % MOD
        # 中间段可以两端同时感染，贡献 2^{gap-1}
        extra_pow += gap - 1

    # ----- 处理结尾段 -----
    if sick[-1] < n-1:
        end_len = n - 1 - sick[-1]
        total_len += end_len
        denominator = denominator * fact[end_len] % MOD
        # 结尾段同开头段，只能从唯一端点感染

    # 计算组合数部分： total_len! / denominator
    ans = fact[total_len] * pow(denominator, MOD-2, MOD) % MOD

    # 乘上 2^{extra_pow}
    ans = ans * pow(2, extra_pow, MOD) % MOD
    return ans
```

**代码要点解释**  

- `precompute_factorials` 预先算出 `i!` 与其模逆，后面只需要 O(1) 时间取值。  
- `denominator` 用来累乘所有 `len!`，最后再求一次模逆相当于一次性除法，避免在循环里频繁取逆。  
- `extra_pow` 记录所有“中间段”贡献的指数，统一在最后用 `pow(2, extra_pow, MOD)` 计算。  
- 所有乘除均在模 `10^9+7` 下完成，防止整数溢出。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 预处理阶乘 O(n)  
  - 单次遍历 `sick`（长度 ≤ n）得到所有区间 O(n)  
  - 其余操作都是 O(1)  
- **空间复杂度**：`O(n)` 用于存放 `fact` 与 `inv_fact`（各 `n+1` 长度的列表）。

> 与暴力解相比，时间从指数级 `2^S` 降到了线性 `n`，即使 `n=10^5` 也能轻松跑完。

---

## 心得

- **核心技巧**：把感染过程抽象为 **区间划分 + 多重排列 + 2 的指数**，利用组合数学求解。  
- **适用的题型**  
  1. “从两端逐步填充” 类的排列计数（如“染色体扩散”“灯塔点燃”）。  
  2. 需要统计 **不同序列** 而不是具体序列的题目（如“不同的分配顺序”“不同的合并顺序”）。  
  3. 需要在 **固定区间内部有多种选择**、区间之间相互独立的组合计数问题。  
- **一句话总结解题钥匙**：**先把整体拆成独立的“区间”，再用多重排列公式乘上每个区间的内部自由度**。

---

## 反思

- **第一反应**：看到“每一步只能感染相邻的未感染”，我先想到**模拟**或**DFS**，于是写出了暴力解。  
- **最容易踩的坑**  
  1. **边界段的处理**：左端或右端没有已感染的“墙”，只能从唯一方向感染，不能误加 `2^{len-1}`。  
  2. **模运算的除法**：直接用 `/` 会出错，需要用模逆（费马小定理）来实现除法。  
  3. **指数溢出**：`2^{k}` 必须在模数下快速幂计算，不能先算出大整数再取模。  
- **下次遇到同类题**：第一步先 **划分连续的未完成子问题**（区间、块），判断每块内部有几种选择，再把所有块的步数用 **多重排列** 合并。这样可以立刻把指数级的枚举压缩到多项式级。