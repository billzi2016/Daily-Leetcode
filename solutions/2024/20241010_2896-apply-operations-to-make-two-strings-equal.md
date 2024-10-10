# #2896. 对两个字符串进行操作使其相等 / Apply Operations to Make Two Strings Equal

> 难度：中等 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/apply-operations-to-make-two-strings-equal/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed binary strings s1 and s2, both of length n, and a positive integer x.
You can perform any of the following operations on the string s1 any number of times:
Return the minimum cost needed to make the strings s1 and s2 equal, or return -1 if it is impossible.
Note that flipping a character means changing it from 0 to 1 or vice-versa.

**Examples**

**Example 1:**

```
Input: s1 = "1100011000", s2 = "0101001010", x = 2
Output: 4
Explanation: We can do the following operations:
- Choose i = 3 and apply the second operation. The resulting string is s1 = "1101111000".
- Choose i = 4 and apply the second operation. The resulting string is s1 = "1101001000".
- Choose i = 0 and j = 8 and apply the first operation. The resulting string is s1 = "0101001010" = s2.
The total cost is 1 + 1 + 2 = 4. It can be shown that it is the minimum cost possible.
```

**Example 2:**

```
Input: s1 = "10110", s2 = "00011", x = 4
Output: -1
Explanation: It is not possible to make the two strings equal.
```

**Constraints**

- n == s1.length == s2.length
- 1 <= n, x <= 500
- s1 and s2 consist only of the characters '0' and '1'.

---

## 题目（中文翻译）

给定两个下标从 **0** 开始的二进制字符串 `s1` 和 `s2`（长度均为 `n`），以及一个正整数 `x`。  
你可以对字符串 `s1` 任意次数执行下列任意一种操作：

1. 选择任意下标 `i < j`，翻转（flip）`s1[i]` 与 `s1[j]`，此操作的代价为 `x`。
2. 选择下标 `i`（`0 ≤ i < n‑1`），翻转相邻的两个字符 `s1[i]` 与 `s1[i+1]`，此操作的代价为 `1`。

返回使得 `s1` 与 `s2` 相等所需的最小总代价。如果无法使两串相等，返回 `-1`。  
注意，翻转字符指的是将 `0` 改为 `1`，或将 `1` 改为 `0`。

---

### 示例

**示例 1**

```text
Input: s1 = "1100011000", s2 = "0101001010", x = 2
Output: 4
Explanation:
我们可以按如下顺序操作：
- 选取 i = 3，执行第二种操作，得到 s1 = "1101111000"。
- 选取 i = 4，执行第二种操作，得到 s1 = "1101001000"。
- 选取 i = 0, j = 8，执行第一种操作，得到 s1 = "0101001010" = s2。
总代价为 1 + 1 + 2 = 4。
```

**示例 2**

```text
Input: s1 = "10110", s2 = "00011", x = 4
Output: -1
Explanation: 无法通过上述操作使两字符串相等。
```

---

### 约束

- `n == s1.length == s2.length`
- `1 ≤ n, x ≤ 500`
- `s1` 和 `s2` 只由字符 `'0'` 与 `'1'` 组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **枚举所有可能的操作顺序**，把 `s1` 一点点变成 `s2`，记录花费的总成本，最后取最小值。  
具体可以用递归（DFS）：

1. 先找出当前 `s1` 与 `s2` 第一个不相等的位置 `i`。  
2. 对于这一次不相等，我们只能通过两种操作把其中的一个位翻转：  
   - **操作 1**：任选 `i` 与任意 `j (j≠i)`，把这两个位置同时翻转，费用 `x`。  
   - **操作 2**：只能把相邻的 `i` 与 `i+1` 同时翻转，费用 `1`（前提是 `i+1` 在字符串范围内）。  
3. 对每一种合法的选择递归下去，直到 `s1` 与 `s2` 完全相同。  

因为每一步都要尝试所有可能的 `j`（最多 `n‑1` 种）以及是否使用相邻操作，递归树的宽度会快速膨胀，时间会呈 **指数级** 增长——即 **暴力搜索**。

> **类比**：把字符串看成一排灯泡，亮的代表 `1`，灭的代表 `0`。我们每次只能同时开关两盏灯，要把它们调成目标状态。直接尝试所有开关组合，就像把所有可能的灯泡配对全列举一遍，显然不切实际。

#### 代码（Python）

```python
from functools import lru_cache

def min_cost_bruteforce(s1: str, s2: str, x: int) -> int:
    n = len(s1)

    @lru_cache(None)
    def dfs(cur: str) -> int:
        # 找到第一个不同的位置
        i = next((idx for idx in range(n) if cur[idx] != s2[idx]), -1)
        if i == -1:                     # 已经相等
            return 0

        best = float('inf')
        # 方案一：使用相邻翻转（如果 i+1 合法）
        if i + 1 < n:
            lst = list(cur)
            lst[i] = '1' if lst[i] == '0' else '0'
            lst[i + 1] = '1' if lst[i + 1] == '0' else '0'
            nxt = ''.join(lst)
            best = min(best, 1 + dfs(nxt))

        # 方案二：任意配对翻转
        for j in range(n):
            if j == i:
                continue
            lst = list(cur)
            lst[i] = '1' if lst[i] == '0' else '0'
            lst[j] = '1' if lst[j] == '0' else '0'
            nxt = ''.join(lst)
            best = min(best, x + dfs(nxt))

        return best

    ans = dfs(s1)
    return -1 if ans == float('inf') else ans
```

> **代码说明**  
> - `dfs` 用记忆化搜索 (`lru_cache`) 防止重复计算相同的字符串状态。  
> - 每次递归只关注第一个不相等的位置 `i`，因为只要把它翻转，就一定会把 `s1[i]` 与 `s2[i]` 对齐。  
> - 暴力枚举所有可能的 `j`（`O(n)`）以及相邻操作（`O(1)`），递归深度最多是 `n/2`（每次消掉两个错误位），所以时间复杂度大约是 `O( (n)^{n/2} )`——远远超出题目限制。

#### 复杂度  

- **时间复杂度**：指数级（≈`O( n^{n/2} )`），因为每一步都要遍历 `O(n)` 的配对选择，递归深度约为错误位数的一半。  
- **空间复杂度**：`O(n)` 用于递归栈和记忆化表（最坏情况下会存储所有出现过的字符串），同样不可接受。

> **大白话**：`O(n²)` 表示“随着 `n` 增大，耗时会像正方形那样快速增长”。这里的指数级则是“耗时会像火箭一样爆炸”，根本跑不完。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**我们只关心哪些位置不相等**，而不是整个字符串。  
把所有「不同」的下标记下来，得到一个数组 `diff`：

```text
diff = [ i | s1[i] != s2[i] ]
```

- 如果 `len(diff)` 为奇数，显然不可能把两位同时翻转成相等，直接返回 `-1`。  
- 其余情况 `len(diff)` 为偶数，我们只需要把这些不相等的位两两配对即可。

---

#### 关键观察 1：配对的费用只有两种可能  

设要配对的两个错误位置是 `p` 与 `q`（`p < q`），它们之间的距离 `d = q - p`。

| 配对方式 | 费用 | 何时使用 |
|----------|------|----------|
| **相邻翻转**（连续两位） | `1`（只适用于 `d = 1`） | 两个错误恰好相邻 |
| **任意配对**（一次性翻转两任意位） | `x` | 任意 `p, q` |
| **多次相邻翻转**（把远距离的两个错误搬到一起） | `d` | 用 `d` 次相邻翻转逐步“移动”错误位，费用等于距离 |

于是，配对两个错误的最小费用为  

```
cost(p, q) = 
    1                       if d == 1
    min(x, d)               if d > 1
```

> **类比**：把两个不对的灯泡想象成要搬到一起的两块砖。  
> - 直接搬（任意配对）花 `x` 元钱。  
> - 用滑轮把它们一步步拉近，每一步拉近 1 格，花 1 元。拉到相邻后再一次性翻转，花 1 元。于是总花费是距离 `d`。

---

#### 关键观察 2：最优配对不需要交叉  

假设我们把下标 `a < b < c < d` 四个错误位配成 `(a, c)` 与 `(b, d)`，  
则费用为 `cost(a,c) + cost(b,d)`。  
如果改成不交叉的配对 `(a,b)` 与 `(c,d)`，费用是 `cost(a,b) + cost(c,d)`。  
利用上表的 `cost` 定义可以证明不交叉配对的费用 **永远不大于** 交叉配对（因为 `cost` 随距离单调不减）。  

> 因此，**只需要考虑相邻的两个错误位是否配对**，不必考虑跨越更远的组合。

---

#### 动态规划

设 `m = len(diff)`（必为偶数），`dp[i]` 表示处理前 `i`（即 `diff[0..i-1]`）个错误位的最小费用。

状态转移：

```
dp[0] = 0                     # 没有错误位，费用 0
dp[2] = cost(diff[0], diff[1])   # 只剩下两位，直接配对

对于 i >= 4 且 i 为偶数：
    # 把第 i-2、i-1 两个错误配对
    dp[i] = dp[i-2] + cost(diff[i-2], diff[i-1])

    # 还有一种可能：把第 i-4、i-3 与第 i-2、i-1 两两交叉配对
    # 这相当于一次性使用两次 “任意配对” 或 “多次相邻翻转”
    # 费用为 dp[i-4] + cost(diff[i-4], diff[i-1]) + cost(diff[i-3], diff[i-2])
    dp[i] = min(dp[i], dp[i-4] + cost(diff[i-4], diff[i-1]) + cost(diff[i-3], diff[i-2]))
```

为什么要考虑 `i-4` 的情况？  
当 **恰好有两个错误且距离大于 1** 时，`cost` 已经把 “多次相邻翻转” 包含进来。  
但如果出现 **四个错误**，有时把最左和最右配对、剩下中间两位配对会更划算（比如 `x` 很小而距离很大），所以需要把 `i-4` 的状态也纳入考虑。

最终答案是 `dp[m]`。

---

#### 代码（Python）

```python
def minCost(s1: str, s2: str, x: int) -> int:
    n = len(s1)
    # 1️⃣ 统计不同下标
    diff = [i for i in range(n) if s1[i] != s2[i]]
    m = len(diff)

    # 2️⃣ 奇数个错误 → 不可能
    if m % 2 == 1:
        return -1
    if m == 0:          # 已经相等
        return 0

    # 3️⃣ 费用函数
    def pair_cost(i: int, j: int) -> int:
        d = diff[j] - diff[i]          # 距离
        if d == 1:
            return 1                  # 相邻翻转一次即可
        # 远距离：要么一次性任意配对，要么多次相邻翻转（费用 = 距离）
        return min(x, d)

    # 4️⃣ DP 初始化
    INF = 10**18
    dp = [INF] * (m + 1)
    dp[0] = 0

    # 只要有两个错误，就可以直接配对
    dp[2] = pair_cost(0, 1)

    # 5️⃣ 递推
    for i in range(4, m + 1, 2):
        # 方案 A：把最近的两个错误配对
        dp[i] = min(dp[i], dp[i - 2] + pair_cost(i - 2, i - 1))

        # 方案 B：跨越配对（考虑 i-4 的状态）
        #   把 (i-4, i-1) 与 (i-3, i-2) 配对
        dp[i] = min(dp[i],
                    dp[i - 4] + pair_cost(i - 4, i - 1) + pair_cost(i - 3, i - 2))

    return dp[m]
```

> **代码要点**  
> - `diff` 把问题规模从 `n (≤500)` 降到错误位个数 `m`，通常会更小。  
> - `pair_cost` 把 “相邻一次” 与 “任意一次 / 多次相邻” 的费用统一抽象，后面的 DP 只需要调用它。  
> - DP 只在偶数下标上更新，因为每次一定消掉两个错误位。  
> - 时间复杂度 `O(m)`（`m ≤ n ≤ 500`），空间复杂度 `O(m)`，完全满足题目限制。

#### 复杂度  

- **时间复杂度**：`O(m)`，其中 `m` 为不同字符的个数，最坏等于 `n ≤ 500`。  
  > 相比暴力的指数级，这里只需要线性遍历一次 `diff`，几乎瞬间得到答案。  
- **空间复杂度**：`O(m)` 用于存放 `diff` 与 `dp`，同样是几百个整数，几乎可以忽略不计。

---

## 心得

- **核心技巧**：把“只在意不同位置”这一事实抽象出来，用 **差异下标数组 + 动态规划** 求最小配对费用。  
- **适用场景**：  
  1. 两两配对的最小代价问题（如 “Minimum Cost to Make Array Equal”）。  
  2. 只能通过成对操作改变状态的题目（如 “Minimum Number of Flips to Make Binary String Alternating”）。  
  3. 需要在 “相邻操作” 与 “任意操作” 之间取舍的字符串/数组题目。  
- **解题钥匙**：**只配对相邻的错误位**（或把相邻错误视为基本单元），并用 `min(x, distance)` 把两种操作的费用统一化。

---

## 反思

- **第一反应**：看到“翻转两个字符”就想到“配对”。于是立刻找出所有不同的位置。  
- **最容易踩的坑**：  
  - 忽略奇数个错误导致的不可行情况。  
  - 误以为只要把相邻错误配对就够，忘记考虑跨越配对（`i‑4` 的转移），在某些 `x` 很小、距离很大的情况下会漏掉更优解。  
  - 对于只有两个错误且距离为 `1` 的特殊情况，需要单独返回 `1`，否则会错误使用 `min(x, d)` 得到 `1`（其实也是对的，但要确保代码逻辑覆盖）。  
- **下次思路**：  
  1. **先统计差异**，判断奇偶性。  
  2. **抽象费用函数** `cost(p, q) = 1 (if adjacent) else min(x, distance)`。  
  3. **只在相邻错误上做 DP**，并记得加入跨越配对的 `i‑4` 转移。  

这样一步步把问题从 “所有可能的操作序列” 简化为 “最小配对费用”，既直观又高效。