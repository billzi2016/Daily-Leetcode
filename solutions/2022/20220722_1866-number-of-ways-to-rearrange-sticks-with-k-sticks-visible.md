# #1866. 重新排列棍子的方案数（可见 K 根棍子） / Number of Ways to Rearrange Sticks With K Sticks Visible

> 难度：困难 · 标签：Math、Dynamic Programming、Combinatorics · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-rearrange-sticks-with-k-sticks-visible/)

---

## 题目（英文原版）

**Description**

There are n uniquely-sized sticks whose lengths are integers from 1 to n. You want to arrange the sticks such that exactly k sticks are visible from the left. A stick is visible from the left if there are no longer sticks to the left of it.
Given n and k, return the number of such arrangements. Since the answer may be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: n = 3, k = 2
Output: 3
Explanation: [1,3,2], [2,3,1], and [2,1,3] are the only arrangements such that exactly 2 sticks are visible.
The visible sticks are underlined.
```

**Example 2:**

```
Input: n = 5, k = 5
Output: 1
Explanation: [1,2,3,4,5] is the only arrangement such that all 5 sticks are visible.
The visible sticks are underlined.
```

**Example 3:**

```
Input: n = 20, k = 11
Output: 647427950
Explanation: There are 647427950 (mod 109 + 7) ways to rearrange the sticks such that exactly 11 sticks are visible.
```

**Constraints**

- 1 <= n <= 1000
- 1 <= k <= n

---

## 题目（中文翻译）

**描述**  
有 `n` 根长度互不相同的棍子，长度为 `1` 到 `n` 的整数。要求对这些棍子进行排列，使得恰好有 `k` 根棍子**从左侧可见**（visible from the left），即在该棍子左侧不存在更长的棍子。  
给定 `n` 和 `k`，返回满足条件的排列数。由于答案可能很大，请返回其对 `10^9 + 7` 取模后的结果。

**示例**

*示例 1*  
输入: `n = 3, k = 2`  
输出: `3`  
解释: `[1,3,2]、[2,3,1]、[2,1,3]` 是唯一的三种恰好有 2 根棍子可见的排列。可见的棍子已下划线标出。

*示例 2*  
输入: `n = 5, k = 5`  
输出: `1`  
解释: `[1,2,3,4,5]` 是唯一一种所有 5 根棍子都可见的排列。可见的棍子已下划线标出。

*示例 3*  
输入: `n = 20, k = 11`  
输出: `647427950`  
解释: 恰好有 11 根棍子可见的排列共有 `647427950`（对 `10^9 + 7` 取模）种。

**约束条件**  
- `1 <= n <= 1000`  
- `1 <= k <= n`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**把所有可能的排列都列举出来**，然后逐个检查左侧可见的棍子数量是否恰好等于 `k`。  

- **数据结构**：我们可以把每一种排列看成一个列表（list），例如 `[2, 1, 3]` 表示把长度为 2 的棍子放在最左边，长度为 1 的棍子放在第二位，长度为 3 的棍子放在最右边。  
- **可见的判断**：从左往右遍历排列，维护当前出现的最大长度 `max_len`。如果当前棍子的长度大于 `max_len`，说明它“从左侧可见”，此时把可见计数加 1 并更新 `max_len`。  
- **正确性**：因为我们枚举了 **所有** `n!` 种排列，凡是满足条件的排列都会被计数，凡是不满足的都被过滤掉，所以答案一定是正确的。  

> **生活化类比**：把每根棍子想象成一本书，长度越大书越厚。把书排在左边的顺序决定了读者先看到哪本书。如果一本书比左边所有的书都厚，它就会“被看见”。我们只需要把所有排书的方式都尝试一遍，看看有多少种方式正好有 `k` 本书被看见。

#### 代码（Python）

```python
import itertools

def visible_count(arr):
    """返回排列 arr 中从左侧可见的棍子数量"""
    cnt = 0          # 可见棍子计数
    max_len = 0      # 当前左侧出现的最大长度
    for h in arr:    # 从左到右遍历
        if h > max_len:          # 更高则可见
            cnt += 1
            max_len = h
    return cnt

def brute_force(n: int, k: int) -> int:
    """暴力枚举所有排列，仅适用于 n 很小的情况（如 n ≤ 8）"""
    ans = 0
    for perm in itertools.permutations(range(1, n + 1)):
        if visible_count(perm) == k:   # 正好 k 根可见
            ans += 1
    return ans
```

> **注意**：`itertools.permutations` 会生成 `n!` 条记录，`n = 8` 时已经有 40320 条，`n = 10` 时就会爆掉。因此这段代码只能用来**验证思路**或**调试**，在正式提交时会超时。

#### 复杂度  

- **时间复杂度**：`O(n! * n)`  
  - `n!` 是所有排列的数量。对每条排列我们需要 `O(n)` 的时间来统计可见棍子。  
  - 大白话：如果把 `n!` 想象成“一堆”可能的排法，随着 `n` 增大，这个数字会“飞速”增长（比如 10! = 3,628,800），所以算法会很慢。

- **空间复杂度**：`O(n)`  
  - 递归调用 `itertools.permutations` 本身使用常数额外空间，遍历时只需要保存当前的排列（长度 `n`）和计数变量。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有排列**。我们要找一种方式**直接计算**符合条件的排列数，而不去列举它们。  

观察 **最高的棍子**（长度为 `n`）的放置位置可以把问题拆成子问题：

1. **把最高棍子放在最左边**  
   - 这根棍子一定是可见的，因为左边没有比它更高的。  
   - 剩下 `n-1` 根棍子需要形成 **恰好 `k-1` 根可见** 的排列。  
   - 方案数 = `dp[n-1][k-1]`（子问题的答案）。

2. **把最高棍子放在除最左以外的其他位置**（共有 `n-1` 种选择）  
   - 最高棍子左边一定有比它更高的棍子（因为最高棍子本身最高），所以它**不会被看到**。  
   - 可见棍子的数量仍然是 `k`。  
   - 这 `n-1` 种放法互不影响，剩下 `n-1` 根棍子仍需形成恰好 `k` 根可见的排列。  
   - 方案数 = `(n-1) * dp[n-1][k]`。

把两种情况相加得到递推式：

```
dp[n][k] = dp[n-1][k-1] + (n-1) * dp[n-1][k]
```

这正是**“无符号第一类斯特林数”**的递推公式——它既可以解释为“有 k 条左侧记录的排列数”，也可以解释为“有 k 条循环的排列数”。  

**边界条件**：

- `dp[0][0] = 1`：空集合只有一种排列，且没有可见棍子。  
- `dp[n][0] = 0`（`n>0`）：如果有棍子就不可能全部不可见。  
- `dp[n][k] = 0`（`k > n`）：可见棍子数不可能超过总数。

**实现细节**：

- 由于 `n ≤ 1000`，`O(n*k)` 的 DP 完全可以接受。  
- 题目要求对 `10^9 + 7` 取模，所有乘法、加法都要取模，防止整数溢出。  
- 为了节约空间，只需要保留上一行 `dp[n-1][*]`，即滚动数组。

> **生活化类比**：把最高的棍子想象成“一位明星”。如果明星站在最左边，所有人都会先看到他，剩下的人需要再产生 `k-1` 位明星；如果明星站在别的地方，他被左边更高的明星挡住，观众仍然只能看到左边的 `k` 位明星。我们只要把这两种情况加起来，就得到所有可能的站位方式。

#### 代码（Python）

```python
MOD = 10**9 + 7

def rearrangeSticks(n: int, k: int) -> int:
    """
    动态规划求解：恰好有 k 根棍子从左侧可见的排列数
    dp[i][j] 表示 i 根棍子恰好有 j 根可见的方案数
    """
    # dp_prev 保存 i-1 行的结果，初始化为 i=0 时的状态
    dp_prev = [0] * (k + 1)
    dp_prev[0] = 1          # 空集合，0 可见

    for i in range(1, n + 1):          # 逐步加入第 i 根棍子
        dp_cur = [0] * (k + 1)         # 本行的 dp 表
        # j 只能取到 i，且不超过 k
        upper = min(i, k)
        for j in range(1, upper + 1):
            # 情形1：最高棍子放在最左边，贡献 dp_prev[j-1]
            left_visible = dp_prev[j - 1]
            # 情形2：最高棍子放在右边的任意位置，贡献 (i-1) * dp_prev[j]
            right_hidden = (i - 1) * dp_prev[j] % MOD
            dp_cur[j] = (left_visible + right_hidden) % MOD
        dp_prev = dp_cur               # 换行，继续向前推进
    return dp_prev[k]                  # 最终答案
```

> **代码要点解释**  
> - `dp_prev` 相当于“滚动的记忆表”，只保留上一轮的结果，节约了 `O(n*k)` → `O(k)` 的空间。  
> - `upper = min(i, k)` 用来避免访问越界，因为当 `i` 小于 `k` 时，不可能出现 `k` 根可见。  
> - 每一步的乘法 `(i - 1) * dp_prev[j]` 需要先取模再相加，以防中间值超出 Python 整数范围（虽然 Python 大整数可以自动扩展，但取模可以保持数值在 1e9+7 以内，提高效率）。  

#### 复杂度  

- **时间复杂度**：`O(n * k)`  
  - 外层循环遍历 `n`（最多 1000）次，内层循环遍历 `k`（最多 `n`）次。  
  - 与暴力解的 `n!` 相比，这个复杂度是**线性**的，几乎可以在毫秒级完成。

- **空间复杂度**：`O(k)`  
  - 只保留两行 DP 表（`dp_prev` 与 `dp_cur`），空间随 `k` 增长。  
  - 对比暴力解的 `O(n)`（存放当前排列），这里的空间更小且与 `n` 的阶乘无关。

---

## 心得

- **核心技巧**：利用**最高元素的放置位置**把全局排列问题拆解为子问题，从而得到 **dp[n][k] = dp[n-1][k-1] + (n-1)·dp[n-1][k]** 的递推式。  
- **适用题型**：  
  1. “左侧可见/右侧可见” 类的排列计数（如 “Number of Ways to Rearrange Sticks With K Sticks Visible”）。  
  2. “记录数（records）” 或 “左侧最大值” 的排列计数。  
  3. 与**无符号第一类斯特林数**等价的组合计数问题（如 “Permutation with K Cycles”）。  
- **一句话总结**：**把最高的元素视作分界点，分别讨论它是否贡献可见计数，就能把指数级的枚举压缩到多项式时间的 DP。**

---

## 反思

- **第一反应**：立刻想到“枚举所有排列”，因为这最直观。随后意识到 `n!` 规模太大，需要找规律。  
- **最容易踩的坑**：  
  - **边界条件**：`dp[0][0] = 1`，`dp[i][0] = 0`（`i>0`）以及 `k > i` 时返回 0。忘记这些会导致数组越界或错误答案。  
  - **取模**：乘法 `(i-1) * dp_prev[j]` 必须在取模后再加，否则会出现 Python 大整数运算的性能问题。  
  - **滚动数组更新顺序**：如果在同一行里直接使用 `dp_cur[j]` 计算 `(i-1) * dp_cur[j]`（而不是 `dp_prev[j]`），会把已经更新的值错误地当作子问题的答案。  
- **下次第一步**：先**思考最高/最小元素的定位**，看是否可以把问题拆成“把最高放左边/不放左边”两种情况，这往往能直接得到递推式。这样就能快速转向 DP 而不是盲目枚举。