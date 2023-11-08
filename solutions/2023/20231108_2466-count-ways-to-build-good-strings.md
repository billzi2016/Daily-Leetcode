# #2466. 统计构造好字符串的方法数 / Count Ways To Build Good Strings

> 难度：中等 · 标签：Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-ways-to-build-good-strings/)

---

## 题目（英文原版）

**Description**

Given the integers zero, one, low, and high, we can construct a string by starting with an empty string, and then at each step perform either of the following:
This can be performed any number of times.
A good string is a string constructed by the above process having a length between low and high (inclusive).
Return the number of different good strings that can be constructed satisfying these properties. Since the answer can be large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: low = 3, high = 3, zero = 1, one = 1
Output: 8
Explanation: 
One possible valid good string is "011". 
It can be constructed as follows: "" -> "0" -> "01" -> "011". 
All binary strings from "000" to "111" are good strings in this example.
```

**Example 2:**

```
Input: low = 2, high = 3, zero = 1, one = 2
Output: 5
Explanation: The good strings are "00", "11", "000", "110", and "011".
```

**Constraints**

- 1 <= low <= high <= 105
- 1 <= zero, one <= low

---

## 题目（中文翻译）

**描述**  
给定整数 `zero`、`one`、`low` 和 `high`，我们可以通过以下方式构造字符串：从空串开始，每一步可以执行下列两种操作之一：

- 在当前字符串末尾追加 `zero` 个 `'0'`（即连续的 `zero` 个字符 `'0'`）；
- 在当前字符串末尾追加 `one` 个 `'1'`（即连续的 `one` 个字符 `'1'`）。

上述操作可以执行任意次数。  
长度在 `low` 到 `high`（含）之间的、通过上述过程构造得到的字符串称为 **好字符串（good string）**。  
返回满足条件的不同好字符串的数量。由于答案可能很大，请返回对 `10^9 + 7` 取模后的结果。

**示例**

**示例 1**  
```
Input: low = 3, high = 3, zero = 1, one = 1
Output: 8
Explanation: 
一种可能的合法好字符串是 "011"。 
构造过程如下: "" -> "0" -> "01" -> "011"。 
在本例中，所有从 "000" 到 "111" 的二进制字符串都是好字符串。 
```

**示例 2**  
```
Input: low = 2, high = 3, zero = 1, one = 2
Output: 5
Explanation: 好字符串有 "00", "11", "000", "110", 和 "011"。 
```

**约束**  
- `1 <= low <= high <= 10^5`  
- `1 <= zero, one <= low`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是**把所有可能的二进制字符串枚举出来**，然后检查每个字符串的长度是否在 `[low, high]` 区间。  
- 这里的“枚举”可以用递归（或 BFS）实现：从空串 `""` 开始，每一步要么在后面拼 `zero` 个 `'0'`，要么拼 `one` 个 `'1'`。  
- 递归的终止条件是当前字符串长度已经超过 `high`，此时不必再继续往下扩展。  

> **类比**：把递归想象成在“树”里走路，每个节点有两条分支（加 `zero` 个 0，或加 `one` 个 1），树的深度大约是 `high / min(zero, one)`。遍历整棵树就相当于把所有可能的好字符串都列出来。

这个方法一定能得到正确答案，因为我们没有遗漏任何合法的构造步骤，也没有多算不合法的情况。  

#### 代码（Python）  
```python
MOD = 10**9 + 7

def countGoodStrings_bruteforce(low: int, high: int, zero: int, one: int) -> int:
    ans = 0                     # 累计满足长度区间的字符串个数

    def dfs(cur_len: int):
        nonlocal ans
        # 如果当前长度已经在区间内，计数一次
        if low <= cur_len <= high:
            ans = (ans + 1) % MOD
        # 超过上限就不再往下走
        if cur_len > high:
            return
        # 继续添加 zero 个 0
        dfs(cur_len + zero)
        # 继续添加 one 个 1
        dfs(cur_len + one)

    dfs(0)                      # 从空串开始
    return ans
```
*关键行解释*  
- `dfs(cur_len + zero)` / `dfs(cur_len + one)`：把当前长度加上对应的块大小，模拟“拼接”。  
- `if low <= cur_len <= high:`：只要长度落在要求范围，就算一条合法的好字符串。  

#### 复杂度  
- **时间复杂度**：`O(2^{high / min(zero, one)})`。因为每一步都有两条分支，深度约为 `high / min(zero, one)`，所以总体是指数级的。可以把 `2^k` 想象成“每走一步，选择翻硬币正反面”，k 越大，耗时越快爆炸。  
- **空间复杂度**：`O(high / min(zero, one))`，即递归栈的最大深度。  

---

### 2. 最优解  

#### 思路  
从暴力解可以看到**重复子问题**：我们只关心“当前已经构造好的长度”而不关心具体的字符串内容。  
- 设 `dp[i]` 表示**恰好长度为 `i` 的好字符串的种数**（不考虑长度范围，只要能构造出来就算）。  
- 初始时，空串长度 `0` 有一种构造方式：`dp[0] = 1`（相当于“什么也不做”）。  
- 对于任意已经知道的长度 `i`，我们可以再**追加**一段 `zero` 个 `0` 或 `one` 个 `1`，得到长度 `i+zero` 或 `i+one` 的新字符串。因此转移方程是  

\[
dp[i + zero] = (dp[i + zero] + dp[i]) \bmod M \\
dp[i + one]  = (dp[i + one]  + dp[i]) \bmod M
\]

其中 `M = 10^9 + 7` 为取模数。  

这样我们只需要一次线性遍历 `0 … high`，把所有能达到的长度都累计起来，最后把 `dp[low] … dp[high]` 加在一起即为答案。  

> **类比**：把 `dp` 看成“仓库”，`dp[i]` 是“恰好装满 i 单位货物的方案数”。每次我们可以往仓库里再放 `zero` 或 `one` 单位的货物，产生新的装满状态。  

#### 代码（Python）  
```python
MOD = 10**9 + 7

def countGoodStrings(low: int, high: int, zero: int, one: int) -> int:
    # dp[i] 表示长度恰好为 i 的好字符串个数
    dp = [0] * (high + 1)
    dp[0] = 1                     # 空串是一种“长度为 0 的构造方式”

    for i in range(high + 1):
        if dp[i] == 0:
            continue              # 没有办法到达长度 i，直接跳过
        # 往后加 zero 个 0
        nxt = i + zero
        if nxt <= high:
            dp[nxt] = (dp[nxt] + dp[i]) % MOD
        # 往后加 one 个 1
        nxt = i + one
        if nxt <= high:
            dp[nxt] = (dp[nxt] + dp[i]) % MOD

    # 把满足长度区间 [low, high] 的方案数相加
    ans = sum(dp[low:high + 1]) % MOD
    return ans
```
*关键行解释*  
- `dp = [0] * (high + 1)`：创建一个长度为 `high+1` 的列表，索引直接对应字符串长度。  
- `if dp[i] == 0: continue`：如果到达不了长度 `i`，就不必再向后转移，省掉无效的计算。  
- `dp[nxt] = (dp[nxt] + dp[i]) % MOD`：把从 `i` 到 `nxt` 的所有新方案加进去，并且取模防止整数溢出。  
- `sum(dp[low:high + 1]) % MOD`：把所有合法长度的方案累加，得到最终答案。  

#### 复杂度  
- **时间复杂度**：`O(high)`。我们只遍历一次长度区间，每次做常数次加法。相当于“走一遍 0~high 的数轴”。  
- **空间复杂度**：`O(high)`（`dp` 数组）。如果想进一步节约空间，也可以只保留两种状态的滚动数组，但这里 `high ≤ 10^5`，直接使用完整数组即可，内存开销在几百 KB 级别。  

---

## 心得  

- **核心技巧**：把“构造过程”抽象为**状态转移 DP**（长度为状态），利用“每次只能加固定长度的块”得到线性递推。  
- **适用的题型**  
  1. “只允许加固定步长” 的计数问题，例如 **“组合数的可达性”**、**“跳台阶”**（每次可跳 `a` 或 `b` 步）。  
  2. “构造满足长度区间的序列” 类似题目，如 **LeetCode 1987. Number of Unique Good Substrings**（使用前缀哈希）等。  
- **一句话总结**：把“拼字符串”看成“往长度上加步长”，用 DP 把每个长度的方案数累计，最后把区间内的结果相加即可。  

---

## 反思  

- **第一反应**：看到“每一步只能加 `zero` 个 0 或 `one` 个 1”，本能想到**递归枚举**所有可能的序列。  
- **最容易踩的坑**  
  1. **忘记取模**：答案要求 `mod 1e9+7`，在累加时一定要每一步都取模，防止 Python 整数爆炸（虽然 Python 能自动大数，但会导致运行时间激增）。  
  2. **边界条件**：`dp[0]=1` 必不可少；如果把它漏掉，后面的转移会全部得到 0。  
  3. **长度上限**：转移时要检查 `i+zero`、`i+one` 是否超出 `high`，否则会访问数组越界。  
- **下次思考的第一步**：看到“每一步固定增量”，立刻尝试**以长度为状态的 DP**，而不是直接枚举具体序列。这样往往能把指数时间压到线性时间。