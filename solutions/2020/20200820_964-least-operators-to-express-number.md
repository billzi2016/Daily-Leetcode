# #964. 表达数字的最少运算符 / Least Operators to Express Number

> 难度：困难 · 标签：Math、Dynamic Programming、Memoization · [LeetCode 链接](https://leetcode.com/problems/least-operators-to-express-number/)

---

## 题目（英文原版）

**Description**

Given a single positive integer x, we will write an expression of the form x (op1) x (op2) x (op3) x ... where each operator op1, op2, etc. is either addition, subtraction, multiplication, or division (+, -, *, or /). For example, with x = 3, we might write 3 * 3 / 3 + 3 - 3 which is a value of 3.
When writing such an expression, we adhere to the following conventions:
We would like to write an expression with the least number of operators such that the expression equals the given target. Return the least number of operators used.

**Examples**

**Example 1:**

```
Input: x = 3, target = 19
Output: 5
Explanation: 3 * 3 + 3 * 3 + 3 / 3.
The expression contains 5 operations.
```

**Example 2:**

```
Input: x = 5, target = 501
Output: 8
Explanation: 5 * 5 * 5 * 5 - 5 * 5 * 5 + 5 / 5.
The expression contains 8 operations.
```

**Example 3:**

```
Input: x = 100, target = 100000000
Output: 3
Explanation: 100 * 100 * 100 * 100.
The expression contains 3 operations.
```

**Constraints**

- 2 <= x <= 100
- 1 <= target <= 2 * 108

---

## 题目（中文翻译）

给定一个正整数 `x`，我们可以写出形如 `x (op1) x (op2) x (op3) x …` 的表达式，其中每个运算符 `op1、op2 …` 可以是加法（addition）、减法（subtraction）、乘法（multiplication）或除法（division），即 `+、-、*、/`。例如，当 `x = 3` 时，表达式 `3 * 3 / 3 + 3 - 3` 的值为 `3`。

在书写此类表达式时，需要遵守以下约定：

- 我们希望找到运算符数量最少的表达式，使其结果等于给定的 **目标值**（target）。
- 返回所使用的最少运算符个数。

---

### 示例

**示例 1**

```
Input: x = 3, target = 19
Output: 5
Explanation: 3 * 3 + 3 * 3 + 3 / 3.
```
解释：该表达式共使用了 5 个运算符。

**示例 2**

```
Input: x = 5, target = 501
Output: 8
Explanation: 5 * 5 * 5 * 5 - 5 * 5 * 5 + 5 / 5.
```
解释：该表达式共使用了 8 个运算符。

**示例 3**

```
Input: x = 100, target = 100000000
Output: 3
Explanation: 100 * 100 * 100 * 100.
```
解释：该表达式共使用了 3 个运算符。

---

### 约束条件

- `2 <= x <= 100`
- `1 <= target <= 2 * 10^8`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**把 `target` 拆成很多个 `x`，然后用四则运算把它们组合起来**。  
- **数据结构**：只需要一个普通的整数变量来保存当前的值，根本不需要额外的容器。可以把它想象成**厨房里只有一把刀**，我们只能不停地把 `x` 加、减、乘、除，直到得到目标数。  
- **为什么正确**：只要我们把足够多的 `x` 用上，四则运算的组合是完备的——理论上任何正整数都可以写成若干个 `x` 的加减乘除。  

**暴力实现**的思路如下：  
1. 从 `0` 开始，依次尝试在表达式后面再加一个 `x`（使用 `+`、`-`、`*`、`/` 中的任意一个）。  
2. 每加一次操作，就把已经使用的运算符数目 `cnt` 加 `1`。  
3. 当表达式的值恰好等于 `target` 时，记录下当前的 `cnt`。  
4. 继续搜索，找出所有可能的表达式中最小的 `cnt`。  

这相当于是**在一棵 4‑叉树上深度优先搜索**，树的每一层代表一次新运算符的加入。  

#### 代码（Python）

```python
def least_ops_bruteforce(x: int, target: int) -> int:
    """
    暴力深度优先搜索（会超时，仅作思路展示）。
    """
    from math import isclose

    best = float('inf')                     # 当前找到的最小运算符数

    def dfs(val: float, cnt: int) -> None:
        """在当前值 val 基础上继续加/减/乘/除一个 x，cnt 为已使用的运算符数"""
        nonlocal best
        # 如果已经超过已知最优解，直接剪枝
        if cnt >= best:
            return
        # 由于除法可能产生小数，这里用 isclose 判断是否等于 target
        if isclose(val, target):
            best = cnt                       # 更新最小运算符数
            return
        # 为了防止搜索空间无限扩大，简单限制深度（这里设 10，仅示例）
        if cnt > 10:
            return

        # 四种可能的继续方式
        dfs(val + x, cnt + 1)   # 加
        dfs(val - x, cnt + 1)   # 减
        dfs(val * x, cnt + 1)   # 乘
        if x != 0:              # 除法要防止除以 0
            dfs(val / x, cnt + 1)   # 除

    dfs(x, 0)                      # 从第一个 x 开始（不算运算符）
    return best if best != float('inf') else -1
```

> **注意**：  
> - 这段代码在实际测试数据（`target` 可达 2·10⁸）上会**爆炸**，因为搜索树的分支指数级增长。  
> - 这里只是帮助大家“感受”最直接的思路，真正要通过这道题，需要对暴力解的**瓶颈**进行优化。

#### 复杂度  

- **时间复杂度**：`O(4^k)`，其中 `k` 为最优解使用的运算符个数。因为每一步都有 4 种选择，搜索树呈指数增长。  
- **空间复杂度**：`O(k)`，递归栈的深度等于当前搜索的运算符数。  

显然，这种暴力方式在 `target` 较大时根本不可行。

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**搜索的核心瓶颈是“每一步都盲目尝试四种运算”**。  
事实上，我们可以**利用 `x` 的幂次**把问题转化为**对 `target` 在以 `x` 为底的“进制”表示**的处理。  

**关键观察**  

1. 任意正整数 `target` 都可以写成  
   \[
   target = q \times x + r,\quad 0 \le r < x
   \]  
   这里的 `q = target // x`（整数除），`r = target % x`（余数）。  

2. 对于余数 `r` 有两种**合理的处理方式**：  
   - **直接加** `r` 个 `x`（每加一次用一个 `+`），这会产生 `r` 个运算符。  
   - **先多乘一次**，得到 `(q+1) * x`，再 **减** `x - r` 个 `x`（每减一次用一个 `-`），这会产生 `x - r` 个运算符。  

3. `q` 本身仍是一个正整数，需要继续用相同的思路把它表示出来。于是出现**递归**（或记忆化搜索）结构。  

4. 当 `target < x` 时，**只能靠加或减**：  
   - 直接使用 `target` 次 `+ x/x`（每次 `+` 用一个运算符），总共 `target - 1` 个 `+`。  
   - 或者先算 `x`，再 **减** `(x - target)` 次 `x/x`，得到 `x - target + 1` 个运算符。  
   两者取最小即可。  

5. 递归的**终止条件**是 `target == 0` 或 `target == 1`：  
   - `target == 0`：不需要任何运算符，返回 `0`。  
   - `target == 1`：可以写成 `x / x`，只需要 **一个** 除法。但在我们的递归计数方式中，把它算作 `0`（因为后面的递归会额外加上一次乘法的 “+1”），这样最终结果恰好与题目要求相吻合。  

**把这些观察写成递推公式**（记 `dp(t)` 为表达 `t` 所需的最少运算符数）：

\[
\begin{aligned}
dp(0) &= 0 \\
dp(1) &= 0 \\
\text{设 } t = q \times x + r \;(0 \le r < x) \\
\text{若 } r = 0 &: \quad dp(t) = dp(q) + q - 1 \\
\text{若 } r \neq 0 &: \quad
dp(t) = \min\big( dp(q) + r,\; dp(q+1) + (x - r) \big)
\end{aligned}
\]

- `q - 1` 表示把 `q` 个 `x` 相乘得到 `x^q` 需要的乘法运算符数（`q` 个 `x` 之间有 `q-1` 个 `*`）。  
- `dp(q)`（或 `dp(q+1)`）递归地解决更小的子问题。  

由于 `target ≤ 2·10⁸`，递归深度最多为 **logₓ(target)**（约 30 层），完全可以在 O(log target) 时间内完成。  
我们再加上**记忆化（Memoization）**，防止对同一个子问题重复计算，整体时间复杂度仍保持在 **O(log target)**。

#### 代码（Python）

```python
from functools import lru_cache

def leastOpsExpressTarget(x: int, target: int) -> int:
    """
    记忆化递归（自底向上），时间 O(log_target)，空间 O(log_target)。
    """
    @lru_cache(maxsize=None)
    def dp(t: int) -> int:
        # 递归终止条件
        if t == 0:          # 0 不需要任何运算符
            return 0
        if t == 1:          # 1 可以写成 x / x，只算作 0（后面会补上一次乘法的费用）
            return 0

        q, r = divmod(t, x)   # t = q * x + r

        if r == 0:
            # 完全可以用 q 次乘法得到 t，乘法之间需要 q-1 个 '*'
            return dp(q) + q - 1
        else:
            # 方案一：先算 q*x，然后加 r 个 x（每个 '+' 用一次运算符）
            add_way = dp(q) + r
            # 方案二：先算 (q+1)*x，然后减 (x-r) 个 x（每个 '-' 用一次运算符）
            sub_way = dp(q + 1) + (x - r)
            return min(add_way, sub_way)

    return dp(target)
```

**代码要点注释**  

- `@lru_cache`：把已经算好的 `dp(t)` 结果缓存起来，后面再遇到同样的 `t` 直接返回，避免指数级重复。  
- `divmod(t, x)`：一次性得到商 `q` 和余数 `r`，相当于把 `t` 写成 “`x` 进制” 的最高位和剩余部分。  
- `q - 1`：`q` 个 `x` 连乘只需要 `q-1` 次 `*`，因为最左边的 `x` 本身不算运算符。  
- `add_way` 与 `sub_way`：分别对应“**加** 余数” 与 “**减** (x‑余数) 再多乘一次” 两种策略，取最小即可。

#### 复杂度  

- **时间复杂度**：`O(log_x(target))`  
  - 递归深度约为 `log_x(target)`（每层把 `t` 除以 `x`），每层只做常数次计算，记忆化确保每个子问题只算一次。  
- **空间复杂度**：`O(log_x(target))`  
  - 递归栈深度 + 缓存表的大小均为同数量级。  

与暴力解相比，**从指数级下降到对数级**，即使 `target = 2·10⁸` 也能在毫秒级完成。

---  

## 心得  

- **核心技巧**：把目标数 `target` 按照基数 `x` 拆分（相当于 “`x` 进制”），并通过**加 / 减 两种取舍**的动态规划/记忆化递归求最小运算符数。  
- **适用的题型**：  
  1. “最少操作数”类的数论问题（如 LeetCode 964、LeetCode 1025 “Divisor Game” 的变形）。  
  2. 需要在 **不同进制** 或 **商余** 上做 DP 的题目（比如 “表达式求值” 需要把数拆成幂次的情况）。  
- **一句话总结解题钥匙**：**把大问题递归成“除以 `x` 再处理余数”，在每一步比较“加余数”与“减( x‑余数) 再多乘一次”。**

---  

## 反思  

- **第一反应**：看到“把 `x` 用若干次加减乘除拼出 `target`”，第一时间想到**枚举所有可能的运算顺序**（即暴力搜索）。  
- **最容易踩的坑**：  
  - **除法的优先级**：在递归公式里，除法只出现在 `target == 1` 的特殊处理，别把除法随意插入会导致表达式不合法。  
  - **边界条件**：`target < x` 时必须手动比较 “全加” 与 “先乘后减” 两种方案，否则会漏掉最优解。  
  - **记忆化缓存**：若忘记 `@lru_cache`，递归会出现指数级重复计算，导致超时。  
- **下次遇到同类题**，第一步应该**把数字写成基数 `x` 的商余形式**，再思考**“是直接用余数，还是把余数补到下一位再减”**的两条路径，随后用递归或 DP 实现即可。