# #788. 旋转数字 / Rotated Digits

> 难度：中等 · 标签：Math、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/rotated-digits/)

---

## 题目（英文原版）

**Description**

An integer x is a good if after rotating each digit individually by 180 degrees, we get a valid number that is different from x. Each digit must be rotated - we cannot choose to leave it alone.
A number is valid if each digit remains a digit after rotation. For example:
Given an integer n, return the number of good integers in the range [1, n].

**Examples**

**Example 1:**

```
Input: n = 10
Output: 4
Explanation: There are four good numbers in the range [1, 10] : 2, 5, 6, 9.
Note that 1 and 10 are not good numbers, since they remain unchanged after rotating.
```

**Example 2:**

```
Input: n = 1
Output: 0
```

**Example 3:**

```
Input: n = 2
Output: 1
```

**Constraints**

- 1 <= n <= 104

---

## 题目（中文翻译）

一个整数 `x` 若在将每个数字单独旋转 180 度后得到一个有效数字（valid number），且该数字与 `x` 不同，则称 `x` 为好整数（good integer）。**每个数字都必须旋转**，不能选择保持不变。  

如果旋转后每个数字仍然是一个合法的数字，则该数字是有效的。例如，数字 0、1、8 旋转后仍是自身，2↔5，6↔9，其他数字旋转后会变成非数字。  

给定整数 `n`，返回区间 `[1, n]` 中好整数的个数。

**示例 1：**  
**Input:** `n = 10`  
**Output:** `4`  
**Explanation:** 在区间 `[1, 10]` 内共有四个好整数：`2, 5, 6, 9`。需要注意的是 `1` 和 `10` 不是好整数，因为它们旋转后保持不变。

**示例 2：**  
**Input:** `n = 1`  
**Output:** `0`  

**示例 3：**  
**Input:** `n = 2`  
**Output:** `1`  

**约束条件：**  
- `1 <= n <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把区间 `[1, n]` 中的每一个整数都检查一遍：

1. 把整数拆成每一位的数字（就像把一本书的每一页的页码拆成十进制的每一位）。
2. 判断每一位在旋转 180° 后是否仍是合法的数字。合法数字有  
   - **不变的**：`0, 1, 8`（旋转后仍是自己）  
   - **会变的**：`2↔5, 5↔2, 6↔9, 9↔6`  
   - **非法的**：`3, 4, 7`（旋转后不是数字）。
3. 只要出现了非法数字，这个整数就直接判为 **不合格**。  
4. 如果所有位都合法，并且**至少出现一次会变的数字**（2、5、6、9），那么这个整数就是 **好数**（good number）。

> **类比**：把每一位数字当作字典里的单词，查找它对应的“旋转后”是什么。合法的词典（哈希表）可以快速判断——在代码里我们用一个 `dict` 把每个数字映射到它旋转后的结果。

#### 代码（Python）

```python
def rotatedDigits_bruteforce(n: int) -> int:
    # 旋转映射表：key 是原数字，value 是旋转后得到的数字
    rotate = {0: 0, 1: 1, 8: 8,
              2: 5, 5: 2,
              6: 9, 9: 6}
    good_cnt = 0

    for x in range(1, n + 1):                 # 遍历每一个整数
        has_rotated = False                   # 是否出现了会变的数字
        y = x
        while y > 0:                          # 按位检查
            digit = y % 10                    # 取最低位
            if digit not in rotate:           # 3、4、7 出现 → 直接淘汰
                break
            if rotate[digit] != digit:        # 2、5、6、9 会变
                has_rotated = True
            y //= 10                          # 去掉最低位，继续检查
        else:                                 # while 正常结束（没有 break）
            if has_rotated:                   # 必须至少有一个会变的位
                good_cnt += 1
    return good_cnt
```

> 关键行解释  
> - `rotate = {...}`：相当于一本“旋转字典”。  
> - `while y > 0:`：把数字逐位拆开，像拆信封一样一次取出一位。  
> - `if digit not in rotate:`：遇到非法数字直接中止本次检查。  

#### 复杂度  

- **时间复杂度**：`O(n * log₁₀ n)`  
  - `n` 是上限，`log₁₀ n` 是每个数的位数（因为我们要把每个数拆成位来检查）。  
  - 大白话：如果 `n = 10⁴`，最多检查 10 000 个数，每个数最多 5 位，约 5 万次操作，仍能跑得很快。
- **空间复杂度**：`O(1)`  
  - 只用了常数级别的额外空间（一个字典和几个临时变量），不随 `n` 增长。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **对每个数都要逐位检查**，这导致时间随 `n` 线性增长。  
其实我们只关心两件事：

1. **是否出现非法数字**（3、4、7）——出现一次就立刻失效。  
2. **是否出现至少一个会变的数字**（2、5、6、9）——只有出现才算“好”。

这两个条件只和**数字的每一位**有关，而不需要把每个完整的整数都列举出来。于是我们可以用 **数位 DP（Digit DP）** 来一次性统计所有满足条件的数字。

##### 数位 DP 基础概念（零基础解释）

- **数位 DP**：把一个整数看成一串“字符”，从高位到低位逐个决定每一位取什么。  
- **状态**：在决定第 `i` 位之前，我们需要记住：
  1. `tight`（是否仍然受到上限 `n` 的约束）：如果前面的位已经和 `n` 完全相同，那么当前位不能随意取大于 `n` 对应位的数字；否则可以随意取 0~9。
  2. `has_rotated`（是否已经出现会变的数字）：一旦出现就保持 `True`，因为后面无论怎么取都已经满足“至少出现一次”。
- **转移**：对当前位枚举所有合法的数字（0~9），如果选的数字是非法的（3、4、7）就直接跳过；否则根据是否已经出现会变的数字更新 `has_rotated`，并继续递归处理下一位。

##### 实现细节

1. **把 `n` 拆成数组 `digits`**，从最高位到最低位存放，方便按位遍历。  
2. 使用 **记忆化递归（Memoization）**：`dp(pos, tight, has_rotated)` 表示从第 `pos` 位开始往后，满足当前约束的好数个数。  
   - `pos`：当前处理的是第几位（0 表示最高位）。  
   - `tight`：布尔值，`True` 表示前面的位已经和 `n` 完全相同，当前位的取值上限是 `digits[pos]`；`False` 表示已经小于上限，可以随意取 0~9。  
   - `has_rotated`：布尔值，是否已经出现会变的数字。  
3. 递归的**结束条件**：`pos == len(digits)`（已经决定完所有位），此时如果 `has_rotated` 为 `True`，说明这条路径构成了一个好数，返回 1；否则返回 0。  
4. 由于状态空间只有 `len(digits) * 2 * 2`（最多 5*2*2=20 种），时间非常快。

##### 为什么这个 DP 正确？

- **完整性**：递归枚举了所有可能的位组合，且每一次选择都遵守“不能超过 `n`”的约束（由 `tight` 保证），所以没有漏掉合法的数。  
- **合法性**：在每一步我们都排除了非法数字（3、4、7），因此所有被计数的数必然是“旋转后仍是数字”。  
- **好数判定**：只有当 `has_rotated` 为 `True` 时才计数，正好对应“至少出现一次会变的数字”。  

#### 代码（Python）

```python
def rotatedDigits(n: int) -> int:
    # 0~9 中哪些是合法的（旋转后仍是数字），哪些会导致“好数”
    good = {2, 5, 6, 9}          # 会变的数字
    invalid = {3, 4, 7}          # 旋转后不是数字的

    digits = list(map(int, str(n)))          # 把 n 拆成高位到低位的列表
    length = len(digits)

    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dp(pos: int, tight: bool, has_rotated: bool) -> int:
        """
        pos        : 当前要决定第 pos 位（0 为最高位）
        tight      : 前面已经完全等于 n 的前缀吗？若 True，当前位最高只能取 digits[pos]
        has_rotated: 到目前为止是否已经出现过会变的数字（2,5,6,9）
        返回值     : 从 pos 开始往后能够组成的好数个数
        """
        if pos == length:               # 所有位都已经确定
            return 1 if has_rotated else 0   # 只要出现过会变的数字就算一个好数

        limit = digits[pos] if tight else 9   # 当前位的最大取值
        total = 0

        for d in range(0, limit + 1):         # 枚举当前位可以取的所有数字
            if d in invalid:                  # 直接跳过非法数字
                continue

            next_tight = tight and (d == limit)   # 只有当 tight 仍为 True 且 d 达到上限时，下一位仍受约束
            next_has = has_rotated or (d in good) # 只要选到会变的数字，就保持 True

            total += dp(pos + 1, next_tight, next_has)

        return total

    return dp(0, True, False)   # 从最高位开始，初始 tight 为 True，尚未出现会变数字
```

> 关键行解释  
> - `digits = list(map(int, str(n)))`：把整数变成“字符数组”，类似把一本书的章节号拆成单独的章节。  
> - `@lru_cache`：记忆化装饰器，像把已经算好的子问题结果存进“字典”，下次直接复用，避免重复计算。  
> - `next_tight = tight and (d == limit)`：如果前面已经比 `n` 小了（tight 为 False），后面的位就可以随意取 0~9；只有当仍然紧贴上限时才继续保持约束。  
> - `next_has = has_rotated or (d in good)`：只要出现一次会变的数字，后面再也不用担心是否出现过了。

#### 复杂度  

- **时间复杂度**：`O(L * 2 * 2 * 10) = O(L)`  
  - `L = len(str(n))`，即 `n` 的位数（本题至多 5 位，因为 `n ≤ 10⁴`）。  
  - 大白话：我们最多遍历 5 位，每位最多尝试 10 种数字，状态只有 4 种组合，整体不到几百次操作，几乎是常数时间。  
- **空间复杂度**：`O(L * 2 * 2) = O(L)`  
  - 递归栈深度为位数 `L`，加上记忆化表保存的状态数，同样是线性级别（最多 20 条记录）。  

相比暴力的 `O(n log n)`，这里把 `n` 从 **10⁴** 降到了 **5**，提升非常明显。

---

## 心得

- **核心技巧**：**数位 DP**（Digit DP）——把“大范围的整数计数”转化为“逐位决策的状态转移”。  
- **适用题型**：  
  1. 统计满足特定数位约束的整数（如不含数字 4、6，或数字和为奇数）。  
  2. 求在 `[0, n]` 区间内满足某种“数字属性”的数量（如翻转后仍是数字、回文数、完全平方数等）。  
  3. 类似 “数字计数” 的 DP 题目（如 `Number of Digit One`、`Count Special Numbers`）。  
- **一句话总结**：**把所有数字的“好坏”用位置信息抽象成状态，用 DP 按位枚举即可快速计数**。

---

## 反思

- **第一反应**：直接遍历 `[1, n]`，逐个检查每位数字是否合法并统计。  
- **最容易踩的坑**  
  1. **忘记“必须出现会变的数字”**：仅判断合法不够，还要确保至少有一个 2/5/6/9。  
  2. **边界处理**：`0` 本身不计入答案，但在 DP 中会出现，需要在结束条件里排除 `has_rotated=False` 的情况。  
  3. **紧跟上限的 `tight` 状态**：若写错 `next_tight` 的判断，会导致计数超出 `n`。  
- **下次遇到同类题**：第一步先思考 **“可以把整数拆成位吗？每一位的合法性如何决定整体结果？”**，若答案是肯定的，就立刻考虑 **数位 DP** 或 **递归记忆化** 来做计数。