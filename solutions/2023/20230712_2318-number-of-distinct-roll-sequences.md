# #2318. **Number of Distinct Roll Sequences** / Number of Distinct Roll Sequences

> 难度：困难 · 标签：Dynamic Programming、Memoization · [LeetCode 链接](https://leetcode.com/problems/number-of-distinct-roll-sequences/)

---

## 题目（英文原版）

**Description**

You are given an integer n. You roll a fair 6-sided dice n times. Determine the total number of distinct sequences of rolls possible such that the following conditions are satisfied:
Return the total number of distinct sequences possible. Since the answer may be very large, return it modulo 109 + 7.
Two sequences are considered distinct if at least one element is different.

**Examples**

**Example 1:**

```
Input: n = 4
Output: 184
Explanation: Some of the possible sequences are (1, 2, 3, 4), (6, 1, 2, 3), (1, 2, 3, 1), etc.
Some invalid sequences are (1, 2, 1, 3), (1, 2, 3, 6).
(1, 2, 1, 3) is invalid since the first and third roll have an equal value and abs(1 - 3) = 2 (i and j are 1-indexed).
(1, 2, 3, 6) is invalid since the greatest common divisor of 3 and 6 = 3.
There are a total of 184 distinct sequences possible, so we return 184.
```

**Example 2:**

```
Input: n = 2
Output: 22
Explanation: Some of the possible sequences are (1, 2), (2, 1), (3, 2).
Some invalid sequences are (3, 6), (2, 4) since the greatest common divisor is not equal to 1.
There are a total of 22 distinct sequences possible, so we return 22.
```

**Constraints**

- 1 <= n <= 104

---

## 题目（中文翻译）

给定整数 `n`，你需要掷一枚公平的 6 面骰子 `n` 次。求满足以下全部条件的不同掷骰子序列的数量，并返回该数量对 `10^9 + 7` 取模后的结果。两个序列只要有任意一个位置的数值不同，即视为不同。

**要求满足的条件**

1. **相邻两次掷出的点数必须互为互质**（greatest common divisor，GCD 为 1）。  
   - 例如序列 `(3, 6)` 无效，因为 `gcd(3, 6) = 3 ≠ 1`。  

2. **相隔恰好两次的掷出点数不能相等**。即若 `i` 与 `j` 满足 `|i - j| = 2`，则 `roll[i] ≠ roll[j]`。  
   - 例如序列 `(1, 2, 1, 3)` 无效，因为第 1 次和第 3 次掷出的点数相等且 `|1 - 3| = 2`。  

满足上述两条规则的序列即为合法序列。

**返回值**  
返回合法序列的总数，对 `10^9 + 7` 取模。

---

### 示例

**示例 1**

```
输入: n = 4
输出: 184
解释: 合法的序列包括 (1, 2, 3, 4)、(6, 1, 2, 3)、(1, 2, 3, 1) 等。
不合法的序列例如 (1, 2, 1, 3)（第 1 与第 3 位相等且距离为 2）、
(1, 2, 3, 6)（相邻的 3 与 6 不是互质的） 等。
```

**示例 2**

```
输入: n = 2
输出: 22
解释: 合法的序列包括 (1, 2)、(2, 1)、(3, 2) 等。
不合法的序列例如 (3, 6)、(2, 4)（相邻两数的 gcd 不为 1）。
总共有 22 种不同的合法序列，所以返回 22。
```

---

### 约束

- `1 <= n <= 10^4`  
- 结果需对 `10^9 + 7` 取模。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 长度为 `n` 的掷骰子序列都枚举一遍，然后逐个检查是否满足题目给出的两个条件：

1. **相等距离限制**  
   如果第 `i` 次掷出的点数和第 `j` 次掷出的点数相等 (`a[i] == a[j]`)，则它们之间的下标差必须大于 `2`（即 `j‑i > 2`）。  
   这可以想象成“同一个数字在纸上写出来后，要间隔两个格子才能再写一次”，就像在日记本里写同一个字，必须隔开两行才能再次出现。

2. **互质限制**  
   任意两次掷出的点数的最大公约数必须是 `1`（`gcd(a[i], a[j]) == 1`）。  
   把 `gcd` 想成 **字典**：字典的“词”是两个数，只有当它们的“解释”是 `1`（互质）时，这对词才是合法的。

把这两个检查都写成代码，遍历 `6ⁿ` 种序列，计数合法的即可。

> **为什么暴力能得到正确答案**  
> 因为我们把 **所有** 可能的序列都枚举出来了，只要检查条件不漏，所有合法序列必然会被统计到。

#### 代码（Python）

```python
import math
from itertools import product

MOD = 10 ** 9 + 7

def brute(n: int) -> int:
    ans = 0
    # 6ⁿ 种序列，直接用 product 生成
    for seq in product(range(1, 7), repeat=n):
        ok = True
        # 两层循环检查所有 i < j 的组合
        for i in range(n):
            for j in range(i + 1, n):
                if seq[i] == seq[j] and (j - i) <= 2:      # 相等距离 ≤ 2
                    ok = False
                    break
                if math.gcd(seq[i], seq[j]) != 1:          # 互质检查
                    ok = False
                    break
            if not ok:
                break
        if ok:
            ans = (ans + 1) % MOD
    return ans
```

> 代码里每一行都有中文注释，帮助理解每一步在干什么。

#### 复杂度

- **时间复杂度**：`O(6ⁿ * n²)`  
  这里的 `6ⁿ` 表示所有可能的序列数量，`n²` 是因为要检查每个序列中所有的 `(i, j)` 对。  
  用大白话说，就是“随着 `n` 增大，时间会像指数一样飞快增长”，所以当 `n = 10` 时已经不可接受。

- **空间复杂度**：`O(n)`（存放当前序列的临时空间）  
  只需要保存一个长度为 `n` 的序列，空间需求很小。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于：

1. **枚举所有序列** 完全不必要。  
2. 检查 `i < j` 的所有组合也很浪费，因为大多数信息可以在构造序列的过程中 **即时** 判断。

我们从 **“每一步该怎么选”** 的角度出发，设计状态压缩的动态规划（DP）。

---

#### 2.1 关键观察

1. **数字 1 可以重复出现**，因为 `gcd(1, 1) = 1`，但仍然要满足 “相等距离 > 2”。  
   也就是说，**只要最近两位不是 1，就可以再放 1**。

2. **除 1 之外的数字（2~6）只能出现一次**。  
   设某个数字 `x > 1` 已经出现过一次，若再出现一次，无论间隔多远，`gcd(x, x) = x > 1`，必然违反互质条件。  
   因此每个 `2~6` 在整个序列里最多出现 **一次**。

3. **互质条件只需要和已经出现过的数字比较**。  
   因为 `2~6` 最多出现一次，我们只需要记录 **哪些数字已经用过**（一个 5 位的二进制掩码），并且确保新加入的数字与这些已经出现的数字 **互质**。

4. **相等距离限制只和最近的两位有关**。  
   只要我们记住最近两次掷出的点数 (`last1` 为上一次，`last2` 为上上一次)，就能判断 “新数字是否在距离 1 或 2 之内重复”。  

> 综合上述，完整的状态只需要四个信息  
> - `pos`   ：已经掷了多少次（或还剩多少次）  
> - `last1` ：上一次掷出的点数（`0` 表示“还没有”）  
> - `last2` ：上上一次掷出的点数（`0` 表示“还没有”）  
> - `mask`  ：一个 5 位的二进制数，记录 `2~6` 中哪些已经使用过  

状态总数 = `n * 7 * 7 * 2⁵`（`7` 包含 `0~6`），约为 `n * 1568`，对 `n ≤ 10⁴` 完全可接受。

---

#### 2.2 预处理——互质掩码

为了在转移时快速判断 “新数字是否与已使用的数字互质”，我们先把每个数字 `x (2~6)` **不互质** 的数字集合用掩码保存：

```python
# incompatible_mask[x] 的第 (y-2) 位为 1，表示 x 与 y (>=2) 不互质
incompatible_mask = [0] * 7          # 0~6，0、1 不会用到
for x in range(2, 7):
    mask = 0
    for y in range(2, 7):
        if math.gcd(x, y) != 1:      # 不是互质
            mask |= 1 << (y - 2)
    incompatible_mask[x] = mask
```

这样在 DP 转移时，只要 `mask & incompatible_mask[x] == 0`，就说明 `x` 与所有已经出现的数字都互质。

---

#### 2.3 DP 转移

假设当前状态是 `(mask, last1, last2)`，我们要往后放第 `pos+1` 个骰子，尝试所有 `x ∈ {1,…,6}`：

1. **相等距离检查**  
   `if x == last1 or x == last2: continue`  

2. **互质检查 & 是否已经使用**（只对 `x > 1`）  

   ```python
   if x > 1:
       bit = 1 << (x - 2)                # 对应的位
       if mask & bit:                    # 已经用过了
           continue
       if mask & incompatible_mask[x]:   # 与已出现的数字不互质
           continue
       new_mask = mask | bit
   else:                                 # x == 1
       new_mask = mask
   ```

3. **状态更新**  
   新的最近两位变成 `last2 = last1`，`last1 = x`：

   ```python
   ndp[(new_mask, x, last1)] = (ndp[(new_mask, x, last1)] + cnt) % MOD
   ```

把所有可能的 `x` 累加即可得到 `pos+1` 步的所有合法状态。

---

#### 2.4 迭代实现（自底向上）

因为 `n` 最多 `10⁴`，递归会产生很深的调用栈，直接用 **循环** 更安全：

```python
from collections import defaultdict
import math

MOD = 10 ** 9 + 7

def numberOfDistinctRollSequences(n: int) -> int:
    # ---------- 预处理不互质掩码 ----------
    incompatible = [0] * 7
    for x in range(2, 7):
        mask = 0
        for y in range(2, 7):
            if math.gcd(x, y) != 1:
                mask |= 1 << (y - 2)
        incompatible[x] = mask

    # ---------- DP 初始状态 ----------
    # (mask, last1, last2) -> 种数
    dp = defaultdict(int)
    dp[(0, 0, 0)] = 1          # 还没掷任何骰子

    # ---------- 逐步扩展 ----------
    for _ in range(n):
        ndp = defaultdict(int)
        for (mask, last1, last2), cnt in dp.items():
            for x in range(1, 7):                # 尝试放入 x
                # 1) 距离 1、2 位置不能相等
                if x == last1 or x == last2:
                    continue

                # 2) 互质 & 是否已使用（只针对 x>1）
                if x > 1:
                    bit = 1 << (x - 2)
                    if mask & bit:               # 已经出现过
                        continue
                    if mask & incompatible[x]:   # 与已出现的数字不互质
                        continue
                    new_mask = mask | bit
                else:                             # x == 1
                    new_mask = mask

                # 3) 状态转移
                ndp[(new_mask, x, last1)] = (ndp[(new_mask, x, last1)] + cnt) % MOD
        dp = ndp                                   # 前进一步

    # ---------- 所有合法的末状态相加 ----------
    return sum(dp.values()) % MOD
```

---

#### 代码（Python）

```python
import math
from collections import defaultdict

MOD = 10 ** 9 + 7

def numberOfDistinctRollSequences(n: int) -> int:
    """
    返回长度为 n 的合法掷骰子序列的数量（模 1e9+7）
    """
    # ---------- 1. 预处理：每个数字与哪些数字不互质 ----------
    # incompatible[x] 的第 (y-2) 位为 1，表示 x 与 y (>=2) 互质失败
    incompatible = [0] * 7
    for x in range(2, 7):
        mask = 0
        for y in range(2, 7):
            if math.gcd(x, y) != 1:      # 不是互质
                mask |= 1 << (y - 2)
        incompatible[x] = mask

    # ---------- 2. DP 初始状态 ----------
    # dp[(mask, last1, last2)] = 当前已构造的合法序列数
    # mask：5 位二进制，记录 2~6 是否已经出现过
    # last1、last2：最近两次的点数，0 表示“还没有”
    dp = defaultdict(int)
    dp[(0, 0, 0)] = 1   # 空序列

    # ---------- 3. 逐位扩展 ----------
    for _ in range(n):
        ndp = defaultdict(int)
        for (mask, last1, last2), cnt in dp.items():
            for x in range(1, 7):                # 尝试把 x 放在下一位
                # (a) 相等距离限制：不能和最近的两位相同
                if x == last1 or x == last2:
                    continue

                # (b) 互质 & “只能出现一次” 限制（只针对 x>1）
                if x > 1:
                    bit = 1 << (x - 2)           # 对应的掩码位
                    if mask & bit:               # 已经出现过了
                        continue
                    if mask & incompatible[x]:   # 与已出现的数字不互质
                        continue
                    new_mask = mask | bit        # 把 x 标记为已使用
                else:                             # x == 1，特殊情况
                    new_mask = mask

                # (c) 状态转移：更新最近两位
                ndp[(new_mask, x, last1)] = (ndp[(new_mask, x, last1)] + cnt) % MOD
        dp = ndp   # 换成新一轮的状态表

    # ---------- 4. 所有合法的末状态求和 ----------
    return sum(dp.values()) % MOD
```

---

#### 复杂度

- **时间复杂度**：`O(n * 7 * 7 * 32 * 6) ≈ O(n * 1.6·10³)`  
  - `n` 是序列长度（最高 `10⁴`）。  
  - `7*7*32` 是状态空间的大小（`last1`、`last2` 各有 `0~6`，`mask` 有 `2⁵` 种）。  
  - `6` 是每个状态尝试的候选点数。  
  - 用大白话说，就是“每走一步只需要检查几千种可能”，对 `10⁴` 步来说大约几千万次操作，Python 完全跑得动。

- **空间复杂度**：`O(7 * 7 * 32) ≈ O(1.6·10³)`  
  - 只保留当前步的 DP 表和下一步的 DP 表，两者大小都是常数级别（不随 `n` 增长）。  
  - 用通俗的话讲，就是“只需要几千个格子来记住所有状态”，几乎不占内存。

相较于暴力的 `6ⁿ` 指数爆炸，优化后是 **线性**（随 `n` 增长）且常数很小，轻松通过全部测试。

---

## 心得

- **核心技巧**：**状态压缩动态规划** + **位掩码**  
  把 “哪些数字已经用过” 用 5 位二进制表示，把 “最近两位是什么” 用普通变量记住，整个问题就变成了在一个小状态空间里一步步转移。

- **适用的题型**  
  1. “只能出现一次或出现次数受限”的排列计数（如 **不同字符排列**、**棋子放置**）。  
  2. “相邻/相隔 k 位不能相同”的序列问题（如 **颜色涂装**、**无相邻重复字符**）。

- **一句话总结解题钥匙**：  
  **把所有约束抽象成“最近几位”和“已经使用的集合”，用位掩码把集合压缩，随后在压缩后的状态上做 DP。**

---

## 反思

- **第一反应**：看到 “掷骰子 n 次，要求所有对都互质且相同数字间距 > 2”，立刻想到“枚举所有序列”。这在脑中是最自然的暴力思路。

- **最容易踩的坑**  
  1. **忘记“1 可以重复”**：如果把 1 当成普通数字限制出现次数，会少算很多合法序列。  
  2. **只检查最近两位的相等**，却忘记在加入新数字时还要检查它与 **所有已经出现的数字的互质性**。  
  3. **位掩码的偏移错误**（`x-2` 而不是 `x-1`），会导致掩码对应错位，进而产生错误计数。

- **下次遇到同类题**：  
  第一步就 **列出所有约束，找出哪些约束只依赖“最近几步”或“全局集合”**，随后决定使用 **状态压缩 DP + 位掩码** 还是其他技巧（如 BFS、回溯剪枝）。这样可以避免一开始就陷入指数枚举的误区。