# #3260. 求最大的能被 K 整除的回文数 / Find the Largest Palindrome Divisible by K

> 难度：困难 · 标签：Math、String、Dynamic Programming、Greedy、Number Theory · [LeetCode 链接](https://leetcode.com/problems/find-the-largest-palindrome-divisible-by-k/)

---

## 题目（英文原版）

**Description**

You are given two positive integers n and k.
An integer x is called k-palindromic if:
Return the largest integer having n digits (as a string) that is k-palindromic.
Note that the integer must not have leading zeros.

**Examples**

**Example 1:**

```
Input: n = 3, k = 5
Output: "595"
Explanation:
595 is the largest k-palindromic integer with 3 digits.
```

**Example 2:**

```
Input: n = 1, k = 4
Output: "8"
Explanation:
4 and 8 are the only k-palindromic integers with 1 digit.
```

**Example 3:**

```
Input: n = 5, k = 6
Output: "89898"
```

**Constraints**

- 1 <= n <= 105
- 1 <= k <= 9

---

## 题目（中文翻译）

给定两个正整数 `n` 和 `k`。  
如果一个整数 `x` 同时满足以下条件，则称其为 **k-回文数**（k‑palindromic）：

1. `x` 的十进制表示是回文数（即正读和反读相同），且没有前导零；
2. `x` 能被 `k` 整除，即 `x % k == 0`。

返回 **长度恰好为 `n` 位**（以字符串形式表示）的、满足上述条件的最大整数。  
注意返回的整数不能有前导零。

## 示例

### 示例 1
**输入**  
```text
n = 3, k = 5
```
**输出**  
```text
"595"
```
**解释**  
595 是所有 3 位 k‑回文数中最大的一个。

### 示例 2
**输入**  
```text
n = 1, k = 4
```
**输出**  
```text
"8"
```
**解释**  
在 1 位数中，只有 4 和 8 能被 4 整除，8 为最大值。

### 示例 3
**输入**  
```text
n = 5, k = 6
```
**输出**  
```text
"89898"
```

## 约束条件

- `1 <= n <= 10^5`
- `1 <= k <= 9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是**枚举**所有 `n` 位的回文数，检查它们是否能被 `k` 整除，挑出最大的即可。  

- **回文数**：左边的数字序列决定右边的数字序列。比如 `n = 5` 时，只要决定前 `⌈5/2⌉ = 3` 位（记作 `a b c`），完整的回文就固定为 `a b c b a`。  
- **枚举**：我们可以把这几位从 `9` 到 `0` 逐个尝试，组合出所有可能的回文，然后把它们转成整数求余数。  
- **数据结构类比**：这里的“所有可能的回文”相当于一本**字典**，每一条记录都是一种数字组合（key），对应的整数就是我们要检查的值（value）。  

**为什么一定能找到答案？** 题目保证 `k ≤ 9`，而所有位都是 `k`（例如 `555…5`）显然是 `k` 的倍数，所以答案一定存在。

**时间/空间分析**  

- `n` 位回文数的自由位数是 `m = ⌈n/2⌉`。每一位有 `10` 种取值（首位除外不能为 `0`），所以所有组合数大约是 `9·10^{m-1}`。  
- 对每个组合我们都要把它拼成完整的回文、转成整数、做一次取模。  
- **时间复杂度**：`O(10^{m})`，即指数级，`n` 甚至为 `10` 时已经不可接受。  
- **空间复杂度**：只需要保存当前枚举的数字，`O(m)`。  

> 大白话解释：如果把 `O(10^{m})` 看成“每多一位，就要多出 10 倍的尝试”，当 `n=100000` 时根本不可能在电脑里跑完。

#### 代码（Python）

```python
def largestPalindrome_bruteforce(n: int, k: int) -> str:
    # 暴力枚举所有回文（仅作示例，实际不可用）
    from itertools import product

    half = (n + 1) // 2                # 需要自行决定的位数
    best = -1
    # 首位不能为 0，其他位可以为 0~9
    for digits in product(range(10), repeat=half):
        if digits[0] == 0:            # 不能出现前导零
            continue
        # 生成完整的回文
        left = list(digits)
        right = left[:-1] if n % 2 else left
        right = right[::-1]           # 镜像
        num = int(''.join(map(str, left + right)))
        if num % k == 0 and num > best:
            best = num
    return str(best)
```

> 这段代码可以跑通小 `n`（比如 `n ≤ 6`），但对大输入会直接超时。

#### 复杂度

- **时间复杂度**：`O(10^{⌈n/2⌉})` —— 随着位数每增加一位，尝试次数会乘以 10，极其快速地爆炸。  
- **空间复杂度**：`O(⌈n/2⌉)` —— 只保存当前正在枚举的半边数字。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈** 在于枚举所有可能的半边数字。我们需要 **剪枝**：只保留那些**有可能**最终得到可被 `k` 整除的组合。

关键观察：

1. **回文数的余数可以分段累加**。  
   - 设第 `i` 位（从左数，0‑based）上的数字为 `d`，对应的十进制权值是 `10^{n-1-i}`。  
   - 镜像位置 `j = n-1-i` 同样是 `d`，权值是 `10^{i}`。  
   - 两者对整体余数的贡献是 `d·(10^{n-1-i}+10^{i}) (mod k)`。  
   - 当 `i == j`（即 `n` 为奇数且 `i` 为中间位）时，只贡献一次 `d·10^{i}`。

   这意味着我们只要 **一次性知道每个自由位的“权重”**（模 `k` 的值），就可以在构造半边时同步累计余数。

2. **动态规划 + 贪心**。  
   - 用 DP 记录「从第 `pos` 位开始，能否得到某个余数」；  
   - 再从左到右 **贪心** 选最大的可能数字，只要后面的 DP 能保证最终余数为 `0`。  
   - 由于我们只关心余数 `0…k-1`，状态数是 `k ≤ 9`，非常小，DP 只需要 `O(n·k·10)` 的时间。

3. **实现细节**  
   - 预计算 `10^e mod k`（`e` 最高到 `n`），得到每位的权值。  
   - `m = (n+1)//2` 为需要自行决定的位数。  
   - `weight[pos]` = `(10^{n-1-pos} + 10^{pos}) % k`（若是中间位则只加一次）。  
   - **后向 DP** `can[pos][mod]`：从 `pos` 开始（包括 `pos`），是否可以得到余数 `mod`。  
     - 初始：`can[m][0] = True`（全部位已决定，余数必须是 0）。  
     - 转移：遍历所有数字 `d`（首位 `1~9`，其余 `0~9`），检查 `can[pos+1][ (mod - d*weight[pos]) % k ]` 是否为真。  

   - **重建答案**：从左到右维护当前已经累加的余数 `cur`。  
     - 对每一位尝试 `d = 9 … 0`（首位 `9 … 1`），若 `can[pos+1][ (k - (cur + d*weight[pos]) % k) % k ]` 为真，就可以把 `d` 放进去，并更新 `cur`。  
     - 最终得到半边数字数组 `half_digits`，再镜像得到完整的回文字符串。

**为什么这个方法是最优的？**  
- DP 只遍历 `k ≤ 9` 个余数，时间随 `n` 线性增长，完全可以处理 `n = 10^5`。  
- 贪心保证每一步选最大的合法数字，从而得到**字典序最大**（即数值最大）的回文。  

#### 代码（Python）

```python
def largestPalindrome(n: int, k: int) -> str:
    """
    返回长度为 n、能被 k 整除的最大回文数（字符串形式）。
    n ≤ 10^5, k ≤ 9
    """
    # ---------- 1. 预计算 10^e % k ----------
    pow10 = [1] * (n + 1)          # pow10[e] = 10^e mod k
    for e in range(1, n + 1):
        pow10[e] = (pow10[e - 1] * 10) % k

    # ---------- 2. 计算每个自由位的“权重” ----------
    m = (n + 1) // 2               # 需要自行决定的位数
    weight = [0] * m               # weight[pos] 为该位对整体余数的贡献系数（mod k）
    for pos in range(m):
        left_pow  = pow10[n - 1 - pos]   # 10^{n-1-pos} % k
        right_pow = pow10[pos]           # 10^{pos} % k
        if n - 1 - pos == pos:           # 中间位（仅在 n 为奇数时出现）
            weight[pos] = left_pow % k
        else:
            weight[pos] = (left_pow + right_pow) % k

    # ---------- 3. 后向 DP：can[pos][mod] ----------
    # can[pos][r] == True 表示：从位置 pos 开始（包括 pos）能够凑出余数 r
    can = [ [False] * k for _ in range(m + 1) ]
    can[m][0] = True                     # 所有位已确定，余数必须是 0

    for pos in range(m - 1, -1, -1):
        for r in range(k):
            # 尝试所有可能的数字 d
            start_digit = 1 if pos == 0 else 0   # 首位不能是 0
            for d in range(start_digit, 10):
                # 设当前位选 d，则剩余位需要凑出 (r - d*weight) % k
                need = (r - d * weight[pos]) % k
                if can[pos + 1][need]:
                    can[pos][r] = True
                    break   # 已经找到一种合法 d，后面不必再试
            # 若已经为 True，就不必继续检查其他 r
    # ---------- 4. 若根本不存在答案（理论上不会） ----------
    if not can[0][0]:
        return ""      # 按题意不会出现

    # ---------- 5. 贪心重建最大回文 ----------
    half = []          # 保存前半段数字（长度为 m）
    cur_mod = 0        # 已经累计的余数
    for pos in range(m):
        start_digit = 1 if pos == 0 else 0
        for d in range(9, start_digit - 1, -1):   # 从大到小尝试
            new_mod = (cur_mod + d * weight[pos]) % k
            # 剩余位需要能够凑成 (k - new_mod) % k
            need = (k - new_mod) % k
            if can[pos + 1][need]:
                half.append(str(d))
                cur_mod = new_mod
                break

    # ---------- 6. 构造完整回文 ----------
    if n % 2 == 0:
        right = half[::-1]                # 完全镜像
    else:
        right = half[:-1][::-1]           # 去掉中间位再镜像
    return ''.join(half + right)
```

**代码要点注释（中文）**

- `pow10` 用来快速得到任意位的 10 的幂模 `k`，避免每次用 `pow(10, e, k)` 产生额外的 O(log e) 开销。  
- `weight[pos]` 正是「该位的贡献系数」。如果该位是中间位，只算一次 `10^{pos}`；否则算左、右两侧的权值之和。  
- DP 的转移式 `need = (r - d * weight[pos]) % k` 表示：如果我们现在想让 **从 pos 开始的子问题** 最终得到余数 `r`，则选 `d` 后，**剩下的子问题** 必须得到余数 `need`。  
- 重建时的 `need = (k - new_mod) % k` 直接对应「后面所有位要把当前累计余数补齐到 0」。

#### 复杂度

- **时间复杂度**：`O(m * k * 10)`，其中 `m = ⌈n/2⌉ ≤ 5·10^4`，`k ≤ 9`，常数 10 来自数字枚举。  
  - 大白话：每个位我们只检查 10 次（0~9），每次只算一次模运算，整个过程随位数线性增长，`n = 100000` 也只需要几百万次操作，轻松跑完。  
- **空间复杂度**：`O(m * k)` 用于 DP 表，最多约 `5·10^4 * 9 ≈ 4.5·10^5` 个布尔值，约几百 KB，完全可以接受。

---

## 心得  

- **核心技巧**：把回文数的“每位贡献”抽象成模 `k` 的**权重**，配合**后向 DP**判断“剩余位是否可行”，再用**贪心**逐位选最大合法数字。  
- **适用场景**  
  1. 需要构造满足**数值约束 + 结构约束**（如回文、回文数列、对称矩阵）的最大/最小整数。  
  2. “给定长度，要求被某个小数除尽” 这类**取模 DP**问题（如构造最长可被 `m` 整除的子序列）。  
  3. 任何**字典序最大**（或最小）且**状态空间很小**（如模数、位数）的组合优化题。  

- **一句话总结解题钥匙**：**把每个自由位的贡献提前算好，用小范围的模 DP 过滤不可行的选择，再贪心挑最大数字**。

---

## 反思  

- **第一反应**：看到“回文”和“能被 k 整除”，本能想先生成所有回文再判断。  
- **最容易踩的坑**  
  1. **前导零**：首位必须是 `1~9`，否则得到的数字不是合法的 `n` 位数。  
  2. **奇数长度的中间位**：它只出现一次，权重计算要单独处理。  
  3. **模运算的负数**：`(a - b) % k` 在 Python 中已经是非负数，但写成 `a - b % k` 会出错。  
- **下次类似题的第一步**：先**把约束写成“每位的线性贡献模某数”**，看能否把搜索空间压到 `O(位数 × 小状态数)`，再决定是 DP 还是贪心。