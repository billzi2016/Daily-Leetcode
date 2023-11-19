# #2478. **美丽分割的数量** / Number of Beautiful Partitions

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/number-of-beautiful-partitions/)

---

## 题目（英文原版）

**Description**

You are given a string s that consists of the digits '1' to '9' and two integers k and minLength.
A partition of s is called beautiful if:
Return the number of beautiful partitions of s. Since the answer may be very large, return it modulo 109 + 7.
A substring is a contiguous sequence of characters within a string.

**Examples**

**Example 1:**

```
Input: s = "23542185131", k = 3, minLength = 2
Output: 3
Explanation: There exists three ways to create a beautiful partition:
"2354 | 218 | 5131"
"2354 | 21851 | 31"
"2354218 | 51 | 31"
```

**Example 2:**

```
Input: s = "23542185131", k = 3, minLength = 3
Output: 1
Explanation: There exists one way to create a beautiful partition: "2354 | 218 | 5131".
```

**Example 3:**

```
Input: s = "3312958", k = 3, minLength = 1
Output: 1
Explanation: There exists one way to create a beautiful partition: "331 | 29 | 58".
```

**Constraints**

- 1 <= k, minLength <= s.length <= 1000
- s consists of the digits '1' to '9'.

---

## 题目（中文翻译）

给定一个仅由字符 `'1'` 到 `'9'` 组成的字符串 `s`，以及两个整数 `k` 和 `minLength`。  
我们把 `s` 的一次划分称为 **美丽分割**（beautiful partition），如果它满足以下全部条件：

1. 将 `s` 完全划分为恰好 `k` 个子串（子字符串，*substring*），且每个子串的长度 **不小于** `minLength`；
2. 每个子串的 **首字符** 必须是质数数字（prime digit），即 `'2'、'3'、'5'、'7'` 之一；
3. 每个子串的 **尾字符** 必须是非质数数字，即除质数数字之外的 `'1'、'4'、'6'、'8'、'9'`。

返回 `s` 的美丽分割的总数。由于答案可能非常大，请返回答案对 `10^9 + 7` 取模后的结果。

> **子串**（*substring*）是指字符串中连续的一段字符序列。

---

### 示例

**示例 1**

```text
Input: s = "23542185131", k = 3, minLength = 2
Output: 3
Explanation: 存在三种方式可以形成美丽分割：
"2354 | 218 | 5131"
"2354 | 21851 | 31"
"2354218 | 51 | 31"
```

**示例 2**

```text
Input: s = "23542185131", k = 3, minLength = 3
Output: 1
Explanation: 只有一种方式可以形成美丽分割：
"2354 | 218 | 5131"
```

**示例 3**

```text
Input: s = "3312958", k = 3, minLength = 1
Output: 1
Explanation: 只有一种方式可以形成美丽分割：
"331 | 29 | 58"
```

---

### 约束

- `1 <= k, minLength <= s.length <= 1000`
- `s` 仅由字符 `'1'` 到 `'9'` 组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把字符串 `s` 看成一串珠子，我们要把它 **从左到右** 切成 `k` 段，每段的长度都不少于 `minLength`，并且 **每段的首位必须是质数位**（2、3、5、7），**末位必须是非质数位**（1、4、6、8、9）。  

最直接的办法就是 **枚举所有可能的切割位置**，逐个验证是否满足上面的条件，符合的就计数。  

- **数据结构**：只需要一个递归函数或循环来记录当前已经切了几段、上一次切割结束的位置。  
- **生活化类比**：把切割点想象成在一根绳子上打结，暴力解就是把每根可能的绳子全部试一遍，看哪几根符合“首是红绳、尾是蓝绳”的要求。  

**为什么正确**：只要遍历了所有合法的切割组合，就不会漏掉任何一种可能，自然能得到正确答案。  

**时间/空间复杂度**：  
- 每一次切割我们都有 `O(n)` 种可能（在剩余的字符中任选一个切点），递归深度是 `k`，所以时间复杂度大约是 `O(n^k)`，在最坏情况下甚至接近 `O(2^n)`（因为每个字符都可以决定是否是切点）。  
- 递归栈最多保存 `k` 层调用，空间 `O(k)`，但整体上由于指数级的时间，这种解法只适合 `n ≤ 15` 左右的小输入。  

> **大白话**：`O(n^k)` 就好比“把一根长 1000 米的绳子，想把它切成 10 段，你要把每一米都尝试一次”，显然不可行。

#### 代码（Python）

```python
MOD = 10**9 + 7
prime_set = {'2', '3', '5', '7'}          # 质数位
non_prime_set = {'1', '4', '6', '8', '9'} # 非质数位

def is_beautiful(substr: str) -> bool:
    """判断一个子串是否满足首质数、尾非质数的条件"""
    return (substr[0] in prime_set) and (substr[-1] in non_prime_set)

def brute_force(s: str, k: int, minLength: int) -> int:
    n = len(s)

    def dfs(start: int, parts: int) -> int:
        """从下标 start 开始切，已经切了 parts 段，返回合法切法数"""
        # 已经切完 k-1 段，最后一段必须直接取到字符串末尾
        if parts == k - 1:
            if n - start >= minLength and is_beautiful(s[start:]):
                return 1
            return 0

        total = 0
        # 当前位置 start 必须是一个质数位，否则直接返回 0
        if s[start] not in prime_set:
            return 0

        # 枚举当前段的结束位置 end（包含），长度至少为 minLength
        for end in range(start + minLength - 1, n - (k - parts - 1) * minLength):
            # end 为当前段的最后一个字符下标
            if s[end] in non_prime_set and is_beautiful(s[start:end + 1]):
                total += dfs(end + 1, parts + 1)
        return total % MOD

    return dfs(0, 0)
```

#### 复杂度  

- **时间复杂度**：`O(n^k)`（指数级），因为每一段都有 `O(n)` 种切法，递归层数为 `k`。  
- **空间复杂度**：`O(k)`，递归栈的深度最多 `k`，其余使用的都是常数空间。  

---

### 2. 最优解  

#### 思路  

暴力解的 **瓶颈** 在于大量重复的子问题：相同的前缀、相同的已划分段数会被重复计算。  
我们可以把“从左到右切”这个过程抽象成 **动态规划**（DP），把每一次“到达某个位置，已经划了多少段” 的状态保存下来，后面再需要时直接查表，避免重复递归。

**核心概念**  

1. **状态定义**  
   `dp[i]` 表示 **以字符 `s[i]` 为结尾的子串**（即前缀 `s[:i+1]`）**恰好划成 `t` 段** 的方案数。这里的 `t` 会在外层循环中遍历 `1 … k`。  

2. **转移**  
   为了让第 `t` 段以 `i` 结尾，**第 `t‑1` 段必须在某个合法的切点 `j` 结束**，且 `j+1` 到 `i` 这段满足：
   - 长度 `≥ minLength`  
   - `s[j+1]` 为质数位（第 `t` 段的首字符）  
   - `s[i]` 为非质数位（第 `t` 段的尾字符）  

   那么  
   ```
   dp_t[i] = Σ dp_{t-1}[j]   (j 满足上述条件)
   ```
   直接遍历所有 `j` 会导致 `O(n^2*k)`，仍然太慢。  

3. **前缀和优化**  
   观察到条件只和 `j` 的位置有关，而不依赖于 `j` 本身的具体值，只要 `j` 落在一个 **连续区间**，它们的贡献是相同的。  
   因此我们维护一个 **前缀和数组 `pre`**，使得  
   ```
   pre[i] = (dp_{t-1}[0] + dp_{t-1}[1] + … + dp_{t-1}[i]) % MOD
   ```
   那么区间 `[L, R]` 的和可以用 `pre[R] - pre[L-1]`（注意取模）在 `O(1)` 时间得到。  

   对于当前 `i`，合法的 `j` 必须满足：
   - `j + minLength ≤ i`（保证第 `t` 段长度足够）  
   - `s[j+1]` 为质数位  
   - `s[i]` 为非质数位（如果不满足，这一整行 `dp_t[i]` 为 0）  

   我们可以在遍历 `i` 的过程中维护一个 **左指针 `left`**，指向最左边满足 `j + minLength ≤ i` 且 `s[j+1]` 为质数位 的 `j`。右指针自然是 `i - minLength`（因为 `j` 不能超过 `i - minLength`）。这样合法区间就是 `[left, i - minLength]`，求和即 `pre[i - minLength] - pre[left-1]`。  

4. **整体流程**  
   - 第一次划分（`t = 1`）时，只要前缀满足首质数、尾非质数且长度 ≥ `minLength`，计数为 1。  
   - 从 `t = 2` 到 `k`，利用上一步的 `dp` 与前缀和计算 `dp_t`。  
   - 最终答案是所有以 **字符串最后一个字符 `s[n-1]` 结尾且划成 `k` 段** 的方案数，即 `dp_k[n-1]`。  

5. **细节**  
   - 由于题目要求 **模 1e9+7**，所有加减运算都要取模。  
   - 需要提前把哪些位置是 **质数位**、**非质数位** 记下来，查询 O(1)。  

**类比**：把 DP 想成在一条路上放置 **检查站**，每个检查站记录“走到这里用了几段”。我们只关心从某个检查站出发，往前走 `minLength` 以上且首字符是红灯（质数位）的区间，这时可以一次性把这段区间的所有记录加起来，而不必一个一个检查。

#### 代码（Python）

```python
MOD = 10**9 + 7
prime = {2, 3, 5, 7}                 # 质数位对应的数字集合
prime_set = {'2', '3', '5', '7'}
non_prime_set = {'1', '4', '6', '8', '9'}

def beautifulPartitions(s: str, k: int, minLength: int) -> int:
    n = len(s)
    # 预处理：哪些位置可以作为段的起点（必须是质数位）
    can_start = [c in prime_set for c in s]
    # 哪些位置可以作为段的终点（必须是非质数位）
    can_end   = [c in non_prime_set for c in s]

    # dp_prev[i] 表示前 i+1 个字符（即 s[:i+1]）恰好划成 t-1 段的方案数
    dp_prev = [0] * n

    # ---------- 第 1 段的初始化 ----------
    # 只要前缀满足首质数、尾非质数且长度 >= minLength，计 1 种
    for i in range(minLength - 1, n):
        if can_start[0] and can_end[i]:
            dp_prev[i] = 1

    # ---------- 处理后面的段 ----------
    for t in range(2, k + 1):          # 从第 2 段到第 k 段
        dp_cur = [0] * n               # 本轮 t 段的 dp
        # 前缀和数组（对 dp_prev 取模累加）
        pre = [0] * n
        pre[0] = dp_prev[0]
        for i in range(1, n):
            pre[i] = (pre[i - 1] + dp_prev[i]) % MOD

        left = 0                        # 滑动窗口左端，指向满足 "前一段结束位置 j"
        for i in range(minLength * t - 1, n):   # i 必须至少能容纳 t 段
            if not can_end[i]:                 # 当前 i 不是合法的段尾，直接跳过
                continue

            # 更新左端：确保 j + minLength <= i 且 s[j+1] 能作为新段的首位
            # j 的取值范围是 [left, i - minLength]
            while left <= i - minLength and not can_start[left + 1]:
                left += 1
            # 此时 left 可能仍然不满足 j + minLength <= i，需要再往右移动
            while left <= i - minLength and left + minLength > i:
                left += 1

            L = left
            R = i - minLength
            if L <= R:                         # 区间合法，求和
                total = pre[R]
                if L - 1 >= 0:
                    total = (total - pre[L - 1]) % MOD
                dp_cur[i] = total

        dp_prev = dp_cur                    # 为下一轮准备

    # 最终答案：第 k 段必须以字符串最后一个字符结尾
    return dp_prev[-1] % MOD
```

> **代码要点解释**  
> - `can_start`、`can_end`：把“质数位 / 非质数位”这件事抽象成布尔数组，查表 O(1)。  
> - `pre`：前缀和，让区间求和从 `O(length)` 降到 `O(1)`。  
> - `left` 指针：滑动窗口，始终保持 “左端的下一个字符是质数位”，并且满足最小长度约束。  
> - 外层 `for t in range(2, k+1)`：逐段递推，时间复杂度是 `O(k * n)`。  

#### 复杂度  

- **时间复杂度**：`O(k * n)`，因为我们对每一段 `t` 都遍历一次字符串，内部的前缀和查询和指针移动都是 `O(1)`。  
  > 与暴力解的 `O(n^k)` 相比，这里把指数级降到了线性乘以段数，能轻松处理 `n ≤ 1000` 的规模。  
- **空间复杂度**：`O(n)`，只保存两组长度为 `n` 的 DP 数组和前缀和数组。  

---

## 心得  

- **核心技巧**：**动态规划 + 前缀和 + 滑动窗口**，把“从左到右的合法切点集合”压缩成区间求和。  
- **适用的题型**  
  1. “把字符串/数组划分成若干段，每段满足长度/首尾条件”——如 *Number of Ways to Split a String*。  
  2. “在序列中选择若干位置，使得相邻选择之间距离不少于某值”——如 *Number of Ways to Paint the Fence*（使用前缀和的 DP）。  
  3. “计数满足一定起止约束的子序列”——如 *Count Good Substrings*。  
- **一句话总结**：**把每段的合法起点看成一个连续区间，用前缀和一次性累计前一段的方案数**，即可在 `O(k·n)` 完成计数。

---

## 反思  

- **第一反应**：看到“划分”“长度≥minLength”“首质尾非”，立刻想到 **递归/回溯**，因为它直观且易实现。  
- **最容易踩的坑**  
  1. **首位/尾位检查**：忘记对每段的首字符和尾字符分别检查质数/非质数，导致计数错误。  
  2. **边界条件**：`i - minLength` 可能为负，需要在取前缀和时做好防护。  
  3. **取模负数**：`(a - b) % MOD` 在 Python 中会得到负数，需要再加 `MOD` 或使用 `% MOD` 保证非负。  
  4. **最左起点的滑动**：左指针必须保证 “下一字符是质数位”，否则会把非法区间算进去。  
- **下次思路**：遇到类似 “把序列划分成若干合法块” 的题目，**先写出 DP 状态转移**，再检查是否可以用 **前缀和/滑动窗口** 把内层循环压缩。这样往往能直接从 `O(n^2·k)` 降到 `O(n·k)`，避免超时。