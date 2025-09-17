# #3348. 最小可整除数字乘积 II / Smallest Divisible Digit Product II

> 难度：困难 · 标签：Math、String、Backtracking、Greedy、Number Theory · [LeetCode 链接](https://leetcode.com/problems/smallest-divisible-digit-product-ii/)

---

## 题目（英文原版）

**Description**

You are given a string num which represents a positive integer, and an integer t.
A number is called zero-free if none of its digits are 0.
Return a string representing the smallest zero-free number greater than or equal to num such that the product of its digits is divisible by t. If no such number exists, return "-1".

**Examples**

**Example 1:**

```
Input: num = "1234", t = 256
Output: "1488"
Explanation:
The smallest zero-free number that is greater than 1234 and has the product of its digits divisible by 256 is 1488, with the product of its digits equal to 256.
```

**Example 2:**

```
Input: num = "12355", t = 50
Output: "12355"
Explanation:
12355 is already zero-free and has the product of its digits divisible by 50, with the product of its digits equal to 150.
```

**Example 3:**

```
Input: num = "11111", t = 26
Output: "-1"
Explanation:
No number greater than 11111 has the product of its digits divisible by 26.
```

**Constraints**

- 2 <= num.length <= 2 * 105
- num consists only of digits in the range ['0', '9'].
- num does not contain leading zeros.
- 1 <= t <= 1014

---

## 题目（中文翻译）

**题目描述**  
给定一个字符串 `num`，表示一个正整数，以及一个整数 `t`。  
如果一个数的每一位数字都不是 `0`，则称其为 **zero‑free（零位数）**。  
返回一个字符串，表示满足以下条件的最小 **zero‑free** 数：

- 该数大于等于 `num`；
- 该数的各位数字的乘积（product）能够被 `t` 整除（divisible）。

如果不存在这样的数，返回 `"-1"`。

**示例**  

*示例 1*  
```
Input: num = "1234", t = 256
Output: "1488"
Explanation:
大于 1234 的最小 zero‑free 数且其各位数字的乘积能够被 256 整除的是 1488，  
其各位数字的乘积恰好等于 256。
```

*示例 2*  
```
Input: num = "12355", t = 50
Output: "12355"
Explanation:
12355 本身已经是 zero‑free，且其各位数字的乘积 1·2·3·5·5 = 150 能被 50 整除。
```

*示例 3*  
```
Input: num = "11111", t = 26
Output: "-1"
Explanation:
不存在大于 11111 的数使得其各位数字的乘积能够被 26 整除。
```

**约束条件**  

- `2 <= num.length <= 2 * 10^5`  
- `num` 仅由字符 `'0'` 到 `'9'` 组成  
- `num` 不包含前导零  
- `1 <= t <= 10^14`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 `num` 从左到右全部枚举出来，检查每一个 **无零** 的整数，看它的各位数字乘积是否能被 `t` 整除，找到第一个满足条件的即为答案。  

- **枚举数字**：把 `num` 当成一个整数，从 `num` 开始一直往上加 1，直到找到符合条件的数。  
- **判断零位**：把整数转换成字符串，检查是否出现字符 `'0'`（相当于在字典里查单词是否出现某个字母）。  
- **判断可整除**：把每一位数字相乘，得到乘积 `p`，判断 `p % t == 0`（就像把商品的价格除以优惠券面额，看能否整除）。  

> 这一步看起来完全没有问题，因为**枚举所有可能**肯定能找到最小的符合要求的数。

#### 代码（Python）

```python
def brute(num: str, t: int) -> str:
    cur = int(num)                       # 把字符串变成整数，方便 +1
    while True:
        s = str(cur)
        if '0' not in s:                 # 没有 0，才算 zero‑free
            prod = 1
            for ch in s:                 # 计算各位数字乘积
                prod *= int(ch)
            if prod % t == 0:            # 能被 t 整除
                return s
        cur += 1
        # 为了防止无限循环，实际代码里需要设上界
```

#### 复杂度  

- **时间复杂度**：`O(Δ * L)`，其中 `Δ` 是从 `num` 到答案之间的差值，`L` 是每次检查时数字的位数。  
  - 想象一下，如果答案比 `num` 大 10⁶，我们就要遍历一百万个数，每个数又要把每一位乘起来，这在最坏情况下会非常慢（相当于 **O(n²)** 的感觉）。  
- **空间复杂度**：`O(1)`，只用了常数级的额外变量。

显然，这种 **“从 1 开始一直加，直到找到”** 的做法在 `num` 长达 2·10⁵、`t` 可能高达 10¹⁴ 时根本不可行。

---

### 2. 最优解

#### 思路  

从暴力解可以看出，**两大瓶颈**：

1. **逐个枚举后面的每一个整数**——太慢。  
2. **每次都重新算乘积**——没有利用已经算好的信息。

我们要 **直接构造** 出最小的符合条件的数，而不是一次次尝试。关键在于：

- **数字乘积的质因数只可能是 2、3、5、7**。因为 1~9 的质因数只有这四个（例如 8 = 2³，9 = 3²）。如果 `t` 含有其它质因数（比如 11），根本不可能找到答案，直接返回 `-1`。  
- 把 `t` 分解成 `2ⁿ² · 3ⁿ³ · 5ⁿ⁵ · 7ⁿ⁷`，我们只要让最终数的各位数字乘积的对应质因数指数 **不少于** 这四个指数即可。  
- 把每个数字 1~9 看成一张 **“卡片”**，卡片上写着它贡献的 2、3、5、7 的个数。例如  
  ```
  digit : (cnt2, cnt3, cnt5, cnt7)
  1     : (0,0,0,0)
  2     : (1,0,0,0)
  3     : (0,1,0,0)
  4     : (2,0,0,0)
  5     : (0,0,1,0)
  6     : (1,1,0,0)
  7     : (0,0,0,1)
  8     : (3,0,0,0)
  9     : (0,2,0,0)
  ```
  这就像 **查字典**：键是数字，值是它提供的质因数“页码”。

- **贪心 + 回溯**：  
  1. 先尝试让答案的前缀和 `num` 完全相同（这保证答案最小）。  
  2. 从右往左找第一个可以**增大**的位（把它从原来的数字 `d` 改成 `d+1 … 9`），之后的所有位我们可以随意填。  
  3. 对于已经确定的前缀以及选好的增大位，统计已经得到的质因数贡献 `cur`.  
  4. 剩下的 `need = target - cur`（每个指数取最大值 0），我们要在 **剩余的位数** 内填入数字，使得 `need` 能够被满足。  
  5. 检查 **可行性**：每个空位最多能贡献的质因数是  
     - 2：最多 3（用 8）  
     - 3：最多 2（用 9）  
     - 5：最多 1（用 5）  
     - 7：最多 1（用 7）  
     因此只要 `need2 ≤ 3·slots`、`need3 ≤ 2·slots`、`need5 ≤ 1·slots`、`need7 ≤ 1·slots`，就一定可以用适当的数字凑齐（因为我们可以随意组合 8、9、5、7 与 1）。这一步相当于 **快速判断是否还能完成**，避免了深度回溯。  
  6. 若可行，就用 **贪心** 填充后缀：从左到右，每个位置尝试最小的合法数字 `1 … 9`，只要选了这个数字后剩下的位数还能满足剩余的 `need`，就确定下来。这样得到的后缀是字典序最小的，也就是数值最小的。  

- **长度扩展**：如果整个位数都无法找到满足条件的方案（包括把最高位也增大后仍不可行），说明需要 **增加一位**。此时我们构造最短的、满足质因数要求的最小数：首位选最小的非零数字（1‑9），其余位同上用贪心填满。  

整个过程只遍历一次字符串，每个位置最多尝试 9 次数字，时间线性 `O(|num|)`，空间只用常数 `O(1)`。

#### 代码（Python）

```python
from typing import List, Tuple

# ------------------------------------------------------------
# 1️⃣ 预处理：把每个数字 1~9 分解成 (cnt2, cnt3, cnt5, cnt7)
DIG_FACT = {
    1: (0, 0, 0, 0),
    2: (1, 0, 0, 0),
    3: (0, 1, 0, 0),
    4: (2, 0, 0, 0),
    5: (0, 0, 1, 0),
    6: (1, 1, 0, 0),
    7: (0, 0, 0, 1),
    8: (3, 0, 0, 0),
    9: (0, 2, 0, 0),
}

# ------------------------------------------------------------
# 2️⃣ 辅助函数：把 t 分解，只保留 2,3,5,7 的指数
def factor_t(t: int) -> Tuple[int, int, int, int]:
    need = [0, 0, 0, 0]          # 对应 2,3,5,7
    for i, p in enumerate([2, 3, 5, 7]):
        while t % p == 0:
            need[i] += 1
            t //= p
    if t != 1:                  # 出现了除 2,3,5,7 之外的质因数
        return None
    return tuple(need)

# ------------------------------------------------------------
# 3️⃣ 可行性检查：剩余 slots 位能否满足 need?
def feasible(need: Tuple[int, int, int, int], slots: int) -> bool:
    n2, n3, n5, n7 = need
    # 每个位置最多能提供的指数
    return (n2 <= 3 * slots and
            n3 <= 2 * slots and
            n5 <= 1 * slots and
            n7 <= 1 * slots)

# ------------------------------------------------------------
# 4️⃣ 贪心构造后缀：在 slots 位内，生成字典序最小的数字串
def build_suffix(need: Tuple[int, int, int, int], slots: int) -> str:
    res = []
    n2, n3, n5, n7 = need
    for pos in range(slots):
        # 试探从小到大的数字
        for d in range(1, 10):
            c2, c3, c5, c7 = DIG_FACT[d]
            # 选 d 后剩下的需求
            nd2 = max(0, n2 - c2)
            nd3 = max(0, n3 - c3)
            nd5 = max(0, n5 - c5)
            nd7 = max(0, n7 - c7)
            if feasible((nd2, nd3, nd5, nd7), slots - pos - 1):
                # 这个 d 合格，确定下来
                res.append(str(d))
                n2, n3, n5, n7 = nd2, nd3, nd5, nd7
                break
    return ''.join(res)

# ------------------------------------------------------------
# 5️⃣ 主函数
def smallestZeroFree(num: str, t: int) -> str:
    need = factor_t(t)
    if need is None:                 # t 含有 2,3,5,7 之外的质因数
        return "-1"

    n = len(num)
    # 预先把 num 每位对应的质因数贡献累计，方便后面快速求前缀
    prefix_fact = [(0, 0, 0, 0)] * (n + 1)   # prefix_fact[i] = 前 i 位的总指数
    cur = (0, 0, 0, 0)
    for i, ch in enumerate(num):
        d = int(ch)
        c = DIG_FACT[d] if d != 0 else (0, 0, 0, 0)   # 0 不会出现在合法答案，但 num 里可能有
        cur = (cur[0] + c[0], cur[1] + c[1], cur[2] + c[2], cur[3] + c[3])
        prefix_fact[i + 1] = cur

    # ---------- 逐位尝试增大 ----------
    for i in range(n - 1, -2, -1):          # i = -1 表示在最高位前“新增”一位
        # 已确定的前缀长度是 i+1（i==-1 时为 0）
        prefix_len = i + 1
        # 已经得到的指数
        cur_need = prefix_fact[prefix_len] if prefix_len >= 0 else (0, 0, 0, 0)

        # 剩余可以改动的位数
        slots = n - prefix_len - 1      # 当 i==-1 时 slots = n (新增一位后仍保持原长度)

        # 当前位置可以选的起始数字
        start = 1
        if i >= 0:
            start = int(num[i]) + 1    # 必须大于原来的数字
        # 枚举当前位置的可能数字
        for d in range(start, 10):
            if d == 0:                 # 不能出现 0
                continue
            c = DIG_FACT[d]
            # 选 d 后剩余需要满足的指数
            nd2 = max(0, need[0] - (cur_need[0] + c[0]))
            nd3 = max(0, need[1] - (cur_need[1] + c[1]))
            nd5 = max(0, need[2] - (cur_need[2] + c[2]))
            nd7 = max(0, need[3] - (cur_need[3] + c[3]))
            need_rem = (nd2, nd3, nd5, nd7)

            if feasible(need_rem, slots):
                # 可以构造后缀
                prefix = '' if i < 0 else num[:i]
                suffix = build_suffix(need_rem, slots)
                return prefix + str(d) + suffix

    # ---------- 没有同长度解，尝试长度+1 ----------
    # 新增一位后，最小的首位是 1（因为 0 不允许），其余位用同样的贪心方法
    extra_slots = n + 1          # 新长度
    # 先把首位设为 1，看看还能否满足需求
    c1 = DIG_FACT[1]             # (0,0,0,0)
    need_rem = (max(0, need[0] - c1[0]),
                max(0, need[1] - c1[1]),
                max(0, need[2] - c1[2]),
                max(0, need[3] - c1[3]))
    if feasible(need_rem, extra_slots - 1):
        suffix = build_suffix(need_rem, extra_slots - 1)
        return '1' + suffix

    # 再尝试把首位设为 2~9 中最小的可以让后面完成的数字
    for d in range(2, 10):
        c = DIG_FACT[d]
        need_rem = (max(0, need[0] - c[0]),
                    max(0, need[1] - c[1]),
                    max(0, need[2] - c[2]),
                    max(0, need[3] - c[3]))
        if feasible(need_rem, extra_slots - 1):
            suffix = build_suffix(need_rem, extra_slots - 1)
            return str(d) + suffix

    return "-1"
```

> **代码说明**  
> - 每一行关键代码都配有中文注释，帮助你快速定位思路。  
> - `feasible` 只用了常数时间，保证整体是线性 `O(|num|)`。  
> - `build_suffix` 用的是 **贪心+回溯**：在每个空位尝试最小的数字，只要后面还能完成剩余需求就确定下来，保证后缀字典序最小，从而整体数值最小。

#### 复杂度  

- **时间复杂度**：`O(n * 9)` ≈ `O(n)`，`n = len(num)`（最多 2·10⁵）。  
  - 我们只遍历一次字符串，每个位置最多尝试 9 次数字，内部的可行性检查是常数时间。  
- **空间复杂度**：`O(1)`（仅用几个整数保存指数），不随 `n` 增长。

相较于暴力的 “逐个枚举”——从 **指数级** 降到了 **线性级**，即使在最极端的输入下也能在毫秒级完成。

---

## 心得

- **核心技巧**：把“数字乘积能被 `t` 整除”转化为“各位数字提供的 2、3、5、7 的指数要不少于 `t` 的指数”。  
- **适用场景**：  
  1. 需要 **满足某种乘积的质因数条件**，且数位范围有限（如 1~9）。  
  2. “在字典序最小的前提下”构造满足约束的数，如 “最小可整除的数字”“最小满足位和/位积的数”。  
  3. 类似题目：**“最小可整除的整数”**、**“最小满足位和为给定值的数”**（可以把位和看成 1 的指数），以及 **“最小满足特定模数的数”**（使用类似的前缀+贪心技巧）。  
- **一句话总结**：**把乘积约束拆成质因数指数的“背包”，用前缀固定、后缀贪心的方式直接拼出最小合法数**。

---

## 反思

- **第一反应**：直接枚举、逐个检查——最直观但完全不可行。  
- **最容易踩的坑**：  
  - `t` 含有 2、3、5、7 之外的质因数时直接返回 `-1`（否则会一直搜索不到答案）。  
  - **零位**：`num` 本身可以包含 `0`，但答案必须 **zero‑free**，所以在前缀累计时要把 `0` 当作贡献为 `(0,0,0,0)`，但在构造时绝不能选 `0`。  
  - **可行性判断不够细**：仅检查每种指数的上限足以保证能凑齐，因为我们可以随意组合 8、9、5、7 与 1，省去复杂的背包 DP。  
- **下次遇到同类题**：第一步先 **把乘积/和等全局约束拆解成每位可以提供的“资源”**（如质因数指数、位和），再用 **前缀锁定 + 余位贪心** 的思路尝试构造最小满足条件的数。这样既避免暴力搜索，又能保证得到字典序最小的答案。