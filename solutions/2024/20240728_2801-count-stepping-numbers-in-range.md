# #2801. 统计区间内的递增数字 / Count Stepping Numbers in Range

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-stepping-numbers-in-range/)

---

## 题目（英文原版）

**Description**

Given two positive integers low and high represented as strings, find the count of stepping numbers in the inclusive range [low, high].
A stepping number is an integer such that all of its adjacent digits have an absolute difference of exactly 1.
Return an integer denoting the count of stepping numbers in the inclusive range [low, high].
Since the answer may be very large, return it modulo 109 + 7.
Note: A stepping number should not have a leading zero.

**Examples**

**Example 1:**

```
Input: low = "1", high = "11"
Output: 10
Explanation: The stepping numbers in the range [1,11] are 1, 2, 3, 4, 5, 6, 7, 8, 9 and 10. There are a total of 10 stepping numbers in the range. Hence, the output is 10.
```

**Example 2:**

```
Input: low = "90", high = "101"
Output: 2
Explanation: The stepping numbers in the range [90,101] are 98 and 101. There are a total of 2 stepping numbers in the range. Hence, the output is 2.
```

**Constraints**

- 1 <= int(low) <= int(high) < 10100
- 1 <= low.length, high.length <= 100
- low and high consist of only digits.
- low and high don't have any leading zeros.

---

## 题目（中文翻译）

**题目描述**  
给定两个以字符串形式表示的正整数 `low` 和 `high`，求闭区间 \[low, high\] 中递增数字（stepping number）的个数。  
递增数字是指其相邻的每一位数字的绝对差恰好为 1 的整数。  
返回区间 \[low, high\] 内递增数字的个数。由于答案可能非常大，请返回 **10^9 + 7** 取模后的结果。  
**注意**：递增数字不能出现前导零。

**示例 1**  
```
Input: low = "1", high = "11"
Output: 10
Explanation: 区间 [1,11] 内的递增数字为 1, 2, 3, 4, 5, 6, 7, 8, 9 和 10。共计 10 个递增数字，故输出 10。
```

**示例 2**  
```
Input: low = "90", high = "101"
Output: 2
Explanation: 区间 [90,101] 内的递增数字为 98 和 101。共计 2 个递增数字，故输出 2。
```

**约束条件**  

- 1 ≤ int(low) ≤ int(high) < 10^100  
- 1 ≤ low.length, high.length ≤ 100  
- `low` 与 `high` 仅由数字组成  
- `low` 与 `high` 不含前导零

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的办法就是**枚举**区间 `[low, high]` 中的每一个整数，逐个判断它是否是 stepping number。  
判断方式很简单：把数字转成字符串，检查相邻两个字符的差的绝对值是否恰好等于 1。  

> **类比**：把 stepping number 想成“楼梯数”。走楼梯时只能向左或向右跨一步，数字的每一位也只能和前一位相差 1。  

如果我们把 `low`、`high` 都转成整数 `L、R`，就可以用 `for num in range(L, R+1)` 循环枚举。  
因为题目保证 `low`、`high` 最长只有 100 位，实际运行时如果 `high` 只有几百甚至几千，暴力解是可以跑通的；但当 `high` 接近 `10^100` 时，枚举的次数天文数字，根本不可行。

#### 代码（Python）

```python
MOD = 10**9 + 7

def is_stepping(num: int) -> bool:
    """判断整数 num 是否为 stepping number（相邻位差恰好为 1）"""
    s = str(num)
    for i in range(1, len(s)):
        if abs(int(s[i]) - int(s[i - 1])) != 1:
            return False
    return True

def count_stepping_brute(low: str, high: str) -> int:
    """暴力解：枚举所有整数并计数（仅适用于区间很小的情况）"""
    L, R = int(low), int(high)
    cnt = 0
    for num in range(L, R + 1):
        if is_stepping(num):
            cnt = (cnt + 1) % MOD
    return cnt
```

> **关键行解释**  
> - `str(num)`：把整数变成字符数组，方便逐位比较。  
> - `abs(int(s[i]) - int(s[i - 1])) != 1`：判断相邻位差是否为 1。  
> - `cnt = (cnt + 1) % MOD`：题目要求对 `10⁹+7` 取模。

#### 复杂度

- **时间复杂度**：`O(N * L)`  
  - `N = high - low + 1` 为枚举的次数。  
  - `L` 为每个数字的位数（最多 100），因为判断相邻位需要遍历全部位。  
  - 用“大白话”说，就是**枚举了多少个数，就要花多少时间**，如果区间是 `10⁶`，大概要跑 `10⁶ * 100` 次比较，已经很慢了。

- **空间复杂度**：`O(1)`  
  - 只用了常数级的额外变量（计数器、临时字符串），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力的瓶颈在于**枚举所有整数**。我们要把这个过程“压缩”——不逐个生成数字，而是**直接统计**满足条件的数字有多少个。  
这类“在区间里计数”的问题常用**数位 DP（Digit DP）**来解决。

**核心想法**：

1. **把问题拆成两段**  
   - 统计 `[1, high]` 中的 stepping number 数量 → `f(high)`  
   - 统计 `[1, low-1]` 中的 stepping number 数量 → `f(low-1)`  
   - 结果 = `f(high) - f(low-1)`（取模处理负数）。

2. **计数函数 `f(x)`**  
   - 首先统计所有**长度小于** `len(x)` 的 stepping number。  
   - 再统计**长度等于** `len(x)` 且 **不超过** `x` 的 stepping number。  
   - 两部分可以统一写成「**在遍历每一位时，是否已经小于上界**」的 DP。

3. **DP 状态设计**  
   - `pos`：当前处理到第几位（从左到右，0‑based）。  
   - `prev`：前一位的数字（0‑9），用来判断相邻差是否为 1。  
   - `tight`（或 `limit`）：前缀是否已经**严格小于**上界 `x`。  
     - `tight = 1` → 前面所有位都和 `x` 完全相同，当前位的取值上限受 `x[pos]` 限制。  
     - `tight = 0` → 已经小于 `x`，当前位可以自由取 0‑9。  
   - `started`：是否已经出现过非前导零。因为题目不允许**前导零**，我们要把「还在前导零阶段」单独记下来。  

   DP 的含义是：**从 `pos` 开始往后构造合法数字的方案数**。

4. **转移**  
   - 若 `started == False`（仍在前导零），可以选择 **跳过**（即在当前位放 0，保持 `started=False`），也可以从 1‑9 中选一个作为首位（此时 `started=True`，`prev` 设为该数字）。  
   - 若 `started == True`，则必须保证新选的数字 `d` 与 `prev` 的差的绝对值为 1。  

5. **结束条件**  
   - 当 `pos == len(x)` 时，已经走完所有位。  
   - 如果 `started == True`（已经选到了至少一位非零数字），这是一条合法的 stepping number，返回 1；否则返回 0（全是前导零不算数）。

6. **记忆化**  
   - `pos` ≤ 100，`prev` ≤ 10，`tight`、`started` 各 2 种状态，整体状态数约 `100 * 10 * 2 * 2 = 4000`，非常小。用 `functools.lru_cache` 直接记忆化即可。

7. **取模**  
   - 每次累加结果时都取 `% MOD`，防止整数溢出。

> **类比**：把 DP 想成“走迷宫”。  
> - `pos` 是我们在走第几步。  
> - `prev` 是我们上一步站在哪个格子（数字）。  
> - `tight` 是“是否已经走出迷宫的边界”，如果已经出界（即已经小于上界），后面的每一步都可以随意走；否则只能在限定的通道里走。  
> - `started` 判断我们是否已经正式进入迷宫（摆脱了前导零的“等待区”）。

#### 代码（Python）

```python
from functools import lru_cache

MOD = 10**9 + 7

def count_stepping_upto(x: str) -> int:
    """
    返回区间 [1, x]（含 x）内所有 stepping number 的个数，取模后返回。
    x 为非空数字字符串，且不含前导零。
    """
    n = len(x)

    @lru_cache(maxsize=None)
    def dfs(pos: int, prev: int, tight: int, started: int) -> int:
        """
        pos     : 当前处理到第 pos 位（0-index，从左到右）
        prev    : 前一位的数字 (0~9)，若 started==0 则值无意义，用 -1 占位
        tight   : 前缀是否已经严格小于 x 的对应前缀（0 否, 1 是）
        started : 是否已经选到非前导零的数字（0 否, 1 是）
        返回值 : 从当前位置开始构造合法数字的方案数（模 MOD）
        """
        if pos == n:                     # 已经走完所有位
            return 1 if started else 0   # 若至少出现过一位非零，则算一条合法数

        limit = int(x[pos]) if tight else 9   # 当前位的最大取值
        total = 0

        # 1. 仍在前导零阶段，可以选择继续放 0（仍未开始）
        if not started:
            # 放 0 继续保持未开始状态
            total += dfs(pos + 1, -1, tight and 0 == limit, 0)
            total %= MOD

            # 2. 从 1~9 中挑一个作为首位（此时 started 变为 1）
            for d in range(1, limit + 1):
                total += dfs(pos + 1, d, tight and d == limit, 1)
                total %= MOD
            return total % MOD

        # 已经开始构造数字，需要满足相邻位差为 1
        for d in range(0, limit + 1):
            if abs(d - prev) != 1:          # 不满足 stepping 条件，跳过
                continue
            total += dfs(pos + 1, d, tight and d == limit, 1)
            total %= MOD
        return total % MOD

    return dfs(0, -1, 1, 0) % MOD


def decrement_one(num: str) -> str:
    """
    计算字符串形式的整数 num - 1，返回不带前导零的结果。
    题目保证 low >= 1，所以不会出现负数。
    """
    lst = list(num)
    i = len(lst) - 1
    while i >= 0 and lst[i] == '0':
        lst[i] = '9'
        i -= 1
    lst[i] = str(int(lst[i]) - 1)          # 必定不会越界
    # 去掉可能出现的前导零
    res = ''.join(lst).lstrip('0')
    return res if res else '0'


def count_stepping_range(low: str, high: str) -> int:
    """
    主入口：统计区间 [low, high] 内的 stepping number 个数（模 1e9+7）
    """
    cnt_high = count_stepping_upto(high)
    low_minus_one = decrement_one(low)
    cnt_low = count_stepping_upto(low_minus_one) if low_minus_one != '0' else 0
    ans = (cnt_high - cnt_low) % MOD
    return ans
```

> **关键行解释**  
> - `limit = int(x[pos]) if tight else 9`：如果前缀已经小于上界，则当前位可以随意取 0‑9；否则只能取不超过上界对应位的数字。  
> - `tight and d == limit`：新一位选的数字恰好等于上界对应位时，后续仍然保持 “tight”。  
> - `abs(d - prev) != 1`：保证相邻位差为 1（stepping 条件）。  
> - `decrement_one`：把 `low` 减 1，得到 `[1, low-1]` 的上界。这里手动做减法是因为 `low` 可能非常长，直接转成整数会溢出。  
> - `ans = (cnt_high - cnt_low) % MOD`：先做差再取模，负数会自动被 Python 的 `%` 调整为正数。

#### 复杂度

- **时间复杂度**：`O(L * 10 * 2 * 2)` ≈ `O(L)`  
  - `L = len(x) ≤ 100` 为数字的位数。  
  - 每个状态最多遍历 10 个候选数字（实际因为 stepping 条件会更少），状态总数约 `4 * 10 * L`，常数很小。  
  - 与暴力解相比，**不再随区间宽度 N 线性增长**，只跟数字长度有关。

- **空间复杂度**：`O(L * 10 * 2 * 2)` ≈ `O(L)`  
  - 递归栈深度为 `L`，记忆化表保存不超过约 4000 条记录，都是常数级别的整数。  

> 与暴力解对比：  
> - 暴力 `O(N * L)`，在 `N` 极大（如 `10^100`）时根本不可跑。  
> - DP `O(L)`，即使 `L=100` 也只需要几千次运算，轻松搞定。

---

## 心得

- **核心技巧**：**数位 DP（Digit DP）**——在限定上界的情况下，逐位统计满足特定相邻关系的整数个数。  
- **适用的题型**（类似思路）  
  1. 统计区间 `[low, high]` 中满足「相邻位差 ≤ K」的数字。  
  2. 统计区间内「数字各位之和」满足某个范围的整数（如 “计数各位和为偶数的数”）。  
  3. 统计「不含连续相同数字」或「数字不递增」等限制的数。  
- **一句话总结解题钥匙**：**把「枚举」变成「计数」——用 DP 按位遍历，同时记录是否已经小于上界以及前一位的值**。

---

## 反思

- **第一反应**：看到“相邻位差恰好为 1”，自然想到**遍历每个数检查**。但很快会意识到区间长度可能高达 `10^100`，枚举不可能。  
- **最容易踩的坑**  
  1. **前导零**：题目禁止以 0 开头，需要在 DP 中额外维护 `started` 标记，否则会把 `01、001` 之类错误计入。  
  2. **取模负数**：`cnt_high - cnt_low` 可能为负，直接 `% MOD` 才能得到正确的正数答案。  
  3. **low = "1"** 时 `low-1` 为 `0`，要单独处理，防止 `decrement_one` 产生空字符串。  
  4. **递归深度**：Python 默认递归深度约 1000，位数最多 100 完全安全，但仍建议使用 `lru_cache` 而不是手写大数组，以免出现栈溢出。  
- **下次遇到同类题**：第一步立刻想到“**用数位 DP**”，先把问题拆成“统计 ≤ X”，再通过 `high - (low-1)` 得到区间答案。随后明确 DP 状态（位置、前一位、是否紧贴上界、是否已开始），就能快速搭出框架。