# #2320. 统计放置房屋的方案数 / Count Number of Ways to Place Houses

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-number-of-ways-to-place-houses/)

---

## 题目（英文原版）

**Description**

There is a street with n * 2 plots, where there are n plots on each side of the street. The plots on each side are numbered from 1 to n. On each plot, a house can be placed.
Return the number of ways houses can be placed such that no two houses are adjacent to each other on the same side of the street. Since the answer may be very large, return it modulo 109 + 7.
Note that if a house is placed on the ith plot on one side of the street, a house can also be placed on the ith plot on the other side of the street.

**Examples**

**Example 1:**

```
Input: n = 1
Output: 4
Explanation: 
Possible arrangements:
1. All plots are empty.
2. A house is placed on one side of the street.
3. A house is placed on the other side of the street.
4. Two houses are placed, one on each side of the street.
```

**Example 2:**

```
Input: n = 2
Output: 9
Explanation: The 9 possible arrangements are shown in the diagram above.
```

**Constraints**

- 1 <= n <= 104

---

## 题目（中文翻译）

There is a street with `n * 2` **地块（plot）**，其中每侧有 `n` 块地块。每侧的地块编号为 `1` 到 `n`。在每块地块上都可以建一栋房屋。  
返回满足 **同侧相邻（adjacent）** 地块上没有两栋房屋的放置方案数。由于答案可能非常大，请返回 `10^9 + 7` 取模后的结果。  
需要注意的是，如果在某侧的第 `i` 块地块上建房，另一侧的第 `i` 块地块仍然可以建房。

**Example 1:**  
**Example 2:**  
**Constraints:**

示例  
**示例 1:**  
```
Input: n = 1
Output: 4
```
**解释:**  
可能的安排有四种：  
1. 所有地块均为空。  
2. 在街道一侧的第 1 块地块上建房。  
3. 在街道另一侧的第 1 块地块上建房。  
4. 两侧各在第 1 块地块上各建一栋房屋。

**示例 2:**  
```
Input: n = 2
Output: 9
```
**解释:** 上图展示了 9 种可能的安排。

约束条件：  
- `1 <= n <= 10^4`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把 **所有** 可能的摆放方式都列举出来，然后逐一检查是否满足“同一侧相邻格子不能同时有房子”。  

- **数据结构**：我们可以用两个长度为 `n` 的二进制字符串来表示两侧的房子分布。比如 `"010"` 表示第 2 块地上有房子，第 1、3 块空着。二进制字符串就像 **查字典**——键（`0`/`1`）直接告诉我们该格子是否被占用。  
- **遍历方式**：对每一侧都有 `2^n` 种可能（每块地要么有房子，要么没有），两侧组合就是 `2^n * 2^n = 4^n` 种。我们可以用 **位运算**（把整数的二进制位当作是否建房的标记）来枚举。  
- **正确性**：因为我们把 **所有** 合法和不合法的情况都枚举了一遍，只要把不合法的剔除，剩下的就是答案。  

#### 代码（Python）  

```python
MOD = 10**9 + 7

def count_bruteforce(n: int) -> int:
    """
    暴力枚举所有 4^n 种布局，统计满足同侧不相邻的方案数
    """
    total = 0                      # 记录合法方案数
    # 用 0 ~ (1 << (2*n)) - 1 的整数表示两排的摆放情况
    # 低 n 位表示上侧， 高 n 位表示下侧
    for mask in range(1 << (2 * n)):
        ok = True
        # 检查上侧是否出现相邻的 1
        up = mask & ((1 << n) - 1)          # 取低 n 位
        if (up & (up << 1)) != 0:           # 如果相邻位都是 1，则非法
            ok = False
        # 检查下侧是否出现相邻的 1
        down = mask >> n                    # 取高 n 位
        if (down & (down << 1)) != 0:
            ok = False
        if ok:
            total += 1
    return total % MOD
```

> **关键注释**  
> - `up & (up << 1)`：把 `up` 左移一位后再与自身做位与，若结果非零说明出现了相邻的 `1`（即相邻两块都有房子）。这一步相当于“检查字典里有没有连续出现的词”。  

#### 复杂度  

- **时间复杂度**：`O(4^n * n)`  
  - `4^n` 是所有可能的总数（因为每列有 4 种状态：空、上、下、上下），  
  - 每次检查需要遍历 `n` 位来判断相邻，故乘以 `n`。  
  - 用大白话说，就是“随着格子数增加，可能的排列会像指数一样疯狂增长，几乎不可能在实际中跑完”。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，不随 `n` 增长。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈** 在于把 **所有** 可能都枚举了一遍，而实际上我们只需要统计满足条件的组合数，不必真的把每一种列举出来。  

观察单侧（只看上面一排或下面一排）：

- 对于一排 `n` 格子，要求**没有相邻的房子**。  
- 这正是经典的 **“不相邻的 0/1 序列”**，它的计数方式和 **斐波那契数列** 完全相同。  

> **类比**：想象每块地是一本书的页面，你要在其中标记“有房子”。但标记的规则是：**不能在相邻的两页都标记**。这和“不能连续选两个相邻的数字”是同一个问题。  

设 `dp[i]` 为前 `i` 块地（从左到右）合法摆放方式的数量。  

- 当第 `i` 块 **不建房**时，前 `i‑1` 块可以随意合法摆放，方式数是 `dp[i‑1]`。  
- 当第 `i` 块 **建房**时，第 `i‑1` 块必须空着，于是前 `i‑2` 块可以随意合法摆放，方式数是 `dp[i‑2]`。  

于是得到递推式  

```
dp[i] = dp[i-1] + dp[i-2]      (i ≥ 2)
```

这正是斐波那契数列，只是起始值不同：

```
dp[0] = 1   # 空的街道算一种合法情况
dp[1] = 2   # 0 或 1，两种可能
```

所以 `dp[i] = Fib(i+2)`（这里的 `Fib(0)=0, Fib(1)=1`）。  

因为上下两侧互相独立（题目只限制同侧相邻），两侧的合法组合数相乘即为答案：

```
answer = (dp[n])^2  (mod 1e9+7)
```

**空间优化**：递推只需要前两个数，使用 **滚动变量** 把空间降到 `O(1)`。  

#### 代码（Python）  

```python
MOD = 10**9 + 7

def count_ways(n: int) -> int:
    """
    动态规划求解：单侧不相邻的方案数 = Fib(n+2)；答案为其平方。
    时间 O(n)，空间 O(1)
    """
    if n == 0:          # 虽然题目 n≥1，但防御性写法
        return 1

    # dp0 = dp[i-2]，dp1 = dp[i-1]
    dp0, dp1 = 1, 2      # 对应 dp[0]、dp[1]
    for _ in range(2, n + 1):
        dp0, dp1 = dp1, (dp0 + dp1) % MOD   # dp[i] = dp[i-1] + dp[i-2]

    single_side = dp1                      # dp[n] = Fib(n+2) (mod MOD)
    # 两侧独立，乘方后仍要取模
    return (single_side * single_side) % MOD
```

> **关键注释**  
> - `dp0, dp1 = dp1, (dp0 + dp1) % MOD`：相当于“把窗口向右滑动”，只保留最近的两个状态，省掉整张表。  
> - 最后 `single_side * single_side % MOD`：先算单侧方案数，再乘以自身得到上下两侧的组合数，最后再取模防止溢出。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历 `n` 次，每次做常数次加法和取模。相当于“走过街道一次就知道所有合法摆法”。  

- **空间复杂度**：`O(1)`  
  - 只用了几个整数变量，和街道长度无关。  

与暴力解相比，时间从指数级降到了线性级，几乎可以瞬间算出 `n=10^4` 的答案。  

---

## 心得  

- **核心技巧**：把二维问题拆解为两条**独立的**一维子问题，利用**斐波那契递推**计数。  
- **适用场景**：  
  1. “不相邻的选取”类问题，如 “没有相邻的 1 的二进制数个数”。  
  2. “独立行/列约束” 的二维网格计数，如 “独立集在二维网格的行约束”。  
  3. “每行/每列相互独立” 的组合计数，例如 “两条不相交的路径数”。  
- **一句话总结**：**把每一行当成斐波那契，最后把两行的计数相乘**。  

---

## 反思  

- **第一反应**：看到“同侧相邻不能放”，立刻想到“斐波那契”或“独立集”，因为这正是经典的**不相邻 0/1 序列**。  
- **最容易踩的坑**：  
  - 忽略 **两侧是独立的**，误以为垂直相邻也有约束，从而把状态数搞得更复杂。  
  - 计算斐波那契时忘记取模，导致在 `n=10^4` 时整数溢出。  
  - 边界 `n=1`、`n=0`（虽然题目不要求）处理不当，导致数组越界。  
- **下次类似题的第一步**：先**判断是否可以分解为独立子问题**（行/列/维度），再**在单维度上寻找递推或组合公式**（如斐波那契、组合数、前缀和等）。