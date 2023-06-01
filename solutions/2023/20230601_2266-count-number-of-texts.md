# #2266. **统计文本数量** / Count Number of Texts

> 难度：中等 · 标签：Hash Table、Math、String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-number-of-texts/)

---

## 题目（英文原版）

**Description**

Alice is texting Bob using her phone. The mapping of digits to letters is shown in the figure below.
In order to add a letter, Alice has to press the key of the corresponding digit i times, where i is the position of the letter in the key.
However, due to an error in transmission, Bob did not receive Alice's text message but received a string of pressed keys instead.
Given a string pressedKeys representing the string received by Bob, return the total number of possible text messages Alice could have sent.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: pressedKeys = "22233"
Output: 8
Explanation:
The possible text messages Alice could have sent are:
"aaadd", "abdd", "badd", "cdd", "aaae", "abe", "bae", and "ce".
Since there are 8 possible messages, we return 8.
```

**Example 2:**

```
Input: pressedKeys = "222222222222222222222222222222222222"
Output: 82876089
Explanation:
There are 2082876103 possible text messages Alice could have sent.
Since we need to return the answer modulo 109 + 7, we return 2082876103 % (109 + 7) = 82876089.
```

**Constraints**

- 1 <= pressedKeys.length <= 105
- pressedKeys only consists of digits from '2' - '9'.

---

## 题目（中文翻译）

Alice 正在使用手机给 Bob 发短信。数字到字母的映射如图所示。  
要输入一个字母，Alice 需要按对应数字键 **i** 次，其中 **i** 是该字母在该键上的位置。  

然而，由于传输错误，Bob 没有收到 Alice 的原始短信，而是收到了一个由按键组成的字符串。  
给定字符串 `pressedKeys`（表示 Bob 接收到的按键序列），返回 Alice 可能发送的文本消息的总数。  
由于答案可能非常大，请返回 **10⁹ + 7** 取模后的结果。

### 示例

**示例 1**

```text
Input: pressedKeys = "22233"
Output: 8
Explanation:
Alice 可能发送的文本消息有：
"aaadd", "abdd", "badd", "cdd", "aaae", "abe", "bae", "ce"。
共有 8 条可能的消息，因此返回 8。
```

**示例 2**

```text
Input: pressedKeys = "222222222222222222222222222222222222"
Output: 82876089
Explanation:
可能的文本消息总数为 2082876103 条。
因为需要对 **10⁹ + 7** 取模，返回 2082876103 % (10⁹ + 7) = 82876089。
```

### 约束

- `1 <= pressedKeys.length <= 10⁵`
- `pressedKeys` 仅由字符 `'2'` 到 `'9'` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把所有可能的文字组合枚举出来**，然后计数。  
- **数据结构**：我们可以用 **递归（或回溯）** 把 `pressedKeys` 按照每个连续相同的数字切分。比如 `"22233"` 可以先把前面的 `"222"` 拆成 `1~3` 次的同一个键，然后把后面的 `"33"` 拆成 `1~2` 次的同一个键。  
- **生活化类比**：想象你在看一本密码本，钥匙 `2` 对应字母 `a,b,c`，如果你看到三个 `2`，就相当于在密码本里找 “一次按 2” → `a`、 “两次按 2” → `b`、 “三次按 2” → `c`。我们把所有合法的“按键次数”组合列出来，就像把所有可能的密码本页码写在纸上。  
- **为什么正确**：只要把每一段相同数字的所有合法拆法（每段最多可以拆成 3 次或 4 次，取决于数字）全部尝试，最后把每段的选择相乘，就得到所有可能的原始文字。  
- **复杂度分析**：  
  - 对每段相同数字的长度 `L`，我们需要尝试所有把 `L` 拆成若干 `1~maxPress` 的方式，数量是指数级的（类似把 `L` 分成若干小块的组合数），最坏情况下会达到 `O(3^L)`（或 `O(4^L)`）。  
  - 整体时间复杂度因此是 **指数级**，对 `len(pressedKeys) ≤ 10^5` 完全不可接受。  
  - 空间上，只需要递归栈深度 `O(L)`，但因为时间爆炸，实际根本跑不完。

#### 代码（Python）

```python
MOD = 10**9 + 7

def brute_force(pressedKeys: str) -> int:
    """
    暴力递归：遍历所有合法的切分方式，计数。
    只适用于非常短的输入，演示思路用。
    """
    n = len(pressedKeys)

    # 每个数字对应的最大连续按键次数
    max_press = {c: 4 if c in "79" else 3 for c in "23456789"}

    from functools import lru_cache

    @lru_cache(None)
    def dfs(i: int) -> int:
        """返回从位置 i 开始的子串的可能组合数"""
        if i == n:
            return 1                     # 到末尾，算一种合法方案
        total = 0
        # 同一数字可以连续出现最多 max_press 次
        limit = max_press[pressedKeys[i]]
        # 试着把当前位置向后延伸 1~limit 次，只要字符相同即可
        for l in range(1, limit + 1):
            if i + l > n or len(set(pressedKeys[i:i + l])) != 1:
                break                    # 超出边界或出现不同数字，停止扩展
            total += dfs(i + l)          # 递归处理剩余部分
        return total % MOD

    return dfs(0)
```

> **注意**：上述代码在 `pressedKeys` 长度稍大（比如 > 20）时就会超时，纯粹用来帮助理解「枚举所有可能」的思路。

#### 复杂度  

- **时间复杂度**：`O(k^L)`（指数级），`k` 为每个数字的最大按键次数（3 或 4），`L` 为同一数字的连续长度。  
  - 大白话：如果你把一个 10 位的相同数字想成 10 块糖，每块糖可以一次、两次或三次吃完，那么所有吃法的数量会像 3 的 10 次方那样多，根本算不完。  
- **空间复杂度**：`O(L)`（递归栈深度），但实际受时间限制几乎不可能完成。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于对每段相同数字的所有拆法做指数级枚举**。我们只需要**统计每段有多少种合法拆法**，而不必把所有组合显式列出来。  

**关键观察**  

1. **每段独立**  
   - `pressedKeys` 可以分成若干“相同数字的连续块”。例如 `"22233"` → `"222"` + `"33"`。  
   - 不同块之间互不影响，整体答案 = 各块答案的乘积（对模数取模后相乘）。  

2. **单块的计数是一个经典的“限制步数的爬楼梯”问题**  
   - 把长度为 `L` 的块看成 **要走 L 步**，每一步可以一次、二次、三次（或四次）前进，具体取决于数字。  
   - 设 `f[i]` 为走到第 `i` 步的方式数，则  
     ```
     f[0] = 1
     f[i] = f[i-1] + f[i-2] + ... + f[i-maxPress]   (i >= 1)
     ```
   - 这就是 **动态规划**（DP）——把大问题拆成子问题，子问题之间只相差一步。  

3. **因为 `maxPress` 只有 3 或 4，DP 的转移可以在 O(1) 时间完成**  
   - 对每个 `i`，只需要把最近的最多 4 个前驱相加。  
   - 这样遍历一次整段即可得到 `f[L]`，即该块的合法拆法数。  

4. **整体 DP**  
   - 我们不必先把块拆出来再单独 DP，而是**在一次遍历中同时完成**：  
     - 记录当前块的长度 `cnt`。  
     - 当块结束（下一个字符不同或到字符串末尾）时，利用预先算好的 `ways[cnt]`（对应 `f[cnt]`）更新全局答案 `ans = ans * ways[cnt] % MOD`。  
   - 预计算 `ways`：因为块的长度最大可能是 `10^5`，我们只需要一次线性 DP，时间 `O(n)`，空间 `O(n)`（或滚动数组进一步压到 `O(1)`）。  

**为什么这样快**  
- 每个字符只访问一次，所有计算都是常数时间，整体 `O(n)`。  
- 不会出现指数爆炸，因为我们只统计“有多少种拆法”，不把每种拆法列举出来。

#### 代码（Python）

```python
MOD = 10**9 + 7

def countTexts(pressedKeys: str) -> int:
    """
    最优解：一次遍历 + 动态规划，时间 O(n)，空间 O(1)（只保存少量状态）。
    """
    n = len(pressedKeys)

    # 每个数字对应的最大连续按键次数
    max_press = {c: 4 if c in "79" else 3 for c in "23456789"}

    # 预先算出“长度为 i 的同一数字块有多少种合法拆法”
    # 这里的上界取 n，因为块的最长可能就是整个字符串
    dp = [0] * (n + 1)
    dp[0] = 1                     # 走完 0 步只有一种方式（什么也不做）

    # 这里我们一次性算出所有长度的方式数，使用滚动窗口加速
    for i in range(1, n + 1):
        # 对于每个 i，最多往前看 4 步（因为 7、9 的 maxPress = 4）
        dp[i] = dp[i-1]
        if i >= 2:
            dp[i] = (dp[i] + dp[i-2]) % MOD
        if i >= 3:
            dp[i] = (dp[i] + dp[i-3]) % MOD
        if i >= 4:
            # 第四步只在 maxPress 为 4 的数字才会被使用，后面会根据实际块长度裁剪
            dp[i] = (dp[i] + dp[i-4]) % MOD

    ans = 1          # 累乘每个块的结果
    i = 0
    while i < n:
        j = i
        # 找到当前相同数字的连续块 [i, j)
        while j < n and pressedKeys[j] == pressedKeys[i]:
            j += 1
        length = j - i                     # 块的长度
        limit = max_press[pressedKeys[i]]  # 该数字允许的最大按键次数

        # 只保留前 limit 步的转移，因为更长的步数在本块中是不合法的
        # 这里直接使用预先算好的 dp[length]，但要把超出 limit 的情况剔除。
        # 事实上 dp 已经把 4 步都算进去了，若 limit < 4，只需要把
        # 超过 limit 的那一项减掉（因为 dp[length] 中已经包含了所有步数）。
        ways = dp[length]
        if limit == 3:                     # 需要去掉第 4 步的贡献
            # 把所有使用了第 4 步的方案减掉
            # 方案数 = dp[length-4]（因为把最后一次走 4 步相当于在 length-4 处结束）
            if length >= 4:
                ways = (ways - dp[length-4]) % MOD
        # 当 limit == 4 时，不需要做任何调整

        ans = ans * ways % MOD
        i = j                               # 继续处理下一个块

    return ans
```

> **代码说明（逐行注释）**  
> 1. `max_press` 把每个数字映射到它对应的字母数（3 或 4）。  
> 2. `dp[i]` 表示长度为 `i` 的同一数字块可以被拆成合法子块的种数。转移只加前 1、2、3、4 步的方式数。  
> 3. 主循环 `while i < n` 按块遍历：  
>    - 用 `j` 找到连续相同字符的区间 `[i, j)`。  
>    - `length` 是该块的长度，`limit` 是该数字允许的最大按键次数。  
>    - `ways = dp[length]` 初始为所有步数（最多 4 步）的组合数。若 `limit` 为 3（即数字 2‑6、8），需要把使用了 4 步的组合剔除，即 `dp[length-4]`。  
>    - 将当前块的方案数累乘到 `ans`，并对 `MOD` 取模。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 我们只遍历一次字符串 (`n = len(pressedKeys)`) 并进行常数次算术操作。  
  - 与暴力解的指数级 `O(k^L)` 相比，**线性** 速度可以轻松处理 `10^5` 长度的输入。  

- **空间复杂度**：`O(n)`（存 `dp` 表）或进一步压缩为 `O(1)`（只保留最近四个 `dp` 值）。  
  - 这里保留完整的 `dp` 仅是为了代码易读，实际只需要四个变量即可。

---

## 心得  

- **核心技巧**：把“相同数字的连续块”视作**受步数限制的爬楼梯**，使用**动态规划**统计每块的合法拆分数，再把各块结果**相乘**。  
- **适用的题型**  
  1. **受限步长的计数**（例如 LeetCode 746. Min Cost Climbing Stairs 的计数变体）。  
  2. **按键/编码拆分**（如 “Decode Ways” 系列题目）。  
  3. **分段独立乘积**（例如统计不同字符连续出现次数的组合数）。  
- **一句话总结解题钥匙**：  
  > “把同一数字的连续出现当成受限步数的爬楼梯，用 DP 统计一种块的拆法数，再把所有块的结果相乘”。  

---

## 反思  

- **第一反应**：看到一串数字，只能想到枚举所有可能的文字组合——这导致了指数级的暴力思路。  
- **最容易踩的坑**  
  - **忽略不同数字的最大按键次数不同**（7、9 有 4 种字母，其他只有 3 种），导致计数错误。  
  - **边界条件**：块长度小于最大步长时，直接使用 `dp[length]`；长度大于等于 4 且 `limit = 3` 时，需要手动剔除使用了第 4 步的方案。  
  - **模运算**：在减去 `dp[length-4]` 时可能出现负数，需要加上 `MOD` 再取模。  
- **下次遇到同类题**，第一步应该：  
  > “先把输入划分为相同元素的连续块，分析每块的内部计数模型（如受限步数的 DP），再把块的计数结果合并（乘或加）”。