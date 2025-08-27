# #3320. 计数获胜序列的数量 / Count The Number of Winning Sequences

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/count-the-number-of-winning-sequences/)

---

## 题目（英文原版）

**Description**

Alice and Bob are playing a fantasy battle game consisting of n rounds where they summon one of three magical creatures each round: a Fire Dragon, a Water Serpent, or an Earth Golem. In each round, players simultaneously summon their creature and are awarded points as follows:
You are given a string s consisting of n characters 'F', 'W', and 'E', representing the sequence of creatures Alice will summon in each round:
Bob’s sequence of moves is unknown, but it is guaranteed that Bob will never summon the same creature in two consecutive rounds. Bob beats Alice if the total number of points awarded to Bob after n rounds is strictly greater than the points awarded to Alice.
Return the number of distinct sequences Bob can use to beat Alice.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "FFF"
Output: 3
Explanation:
Bob can beat Alice by making one of the following sequences of moves: "WFW" , "FWF" , or "WEW" . Note that other winning sequences like "WWE" or "EWW" are invalid since Bob cannot make the same move twice in a row.
```

**Example 2:**

```
Input: s = "FWEFW"
Output: 18
Explanation:
Bob can beat Alice by making one of the following sequences of moves: "FWFWF" , "FWFWE" , "FWEFE" , "FWEWE" , "FEFWF" , "FEFWE" , "FEFEW" , "FEWFE" , "WFEFE" , "WFEWE" , "WEFWF" , "WEFWE" , "WEFEF" , "WEFEW" , "WEWFW" , "WEWFE" , "EWFWE" , or "EWEWE" .
```

**Constraints**

- 1 <= s.length <= 1000
- s[i] is one of 'F', 'W', or 'E'.

---

## 题目（中文翻译）

Alice 和 Bob 正在进行一场由 **n** 轮组成的幻想对战游戏。每一轮，两人各召唤一种魔法生物，三种生物分别是：

- 火龙（`F`）
- 水蛇（`W`）
- 土石魔像（`E`）

在每一轮，玩家同时召唤自己的生物并获得相应的积分，积分规则如题目所述。

已知 Alice 的召唤序列用长度为 **n** 的字符串 **s** 表示，字符仅为 `'F'`、`'W'`、`'E'`，其中第 *i* 个字符代表 Alice 第 *i* 轮召唤的生物。

Bob 的召唤序列未知，但满足以下约束：

- Bob 在相邻的两轮中 **不会** 召唤相同的生物。

在 **n** 轮结束后，如果 Bob 的总积分 **严格大于** Alice 的总积分，则称 Bob “击败” Alice。

求满足上述条件的、Bob 可以采用的 **不同** 召唤序列的数量。由于答案可能非常大，请返回 **答案对 10^9 + 7 取模**（mod）。

---

### 示例

#### 示例 1
**输入**  
`s = "FFF"`

**输出**  
`3`

**解释**  
Bob 可以通过以下任意一种序列击败 Alice：

- `"WFW"`
- `"FWF"`
- `"WEW"`

注意，诸如 `"WWE"`、`"EWW"` 等序列无效，因为 Bob 不能在相邻两轮使用相同的生物。

#### 示例 2
**输入**  
`s = "FWEFW"`

**输出**  
`18`

**解释**  
Bob 可以通过以下任意一种序列击败 Alice：

- `"FWFWF"`、`"FWFWE"`、`"FWEFE"`、`"FWEWE"`、`"FEFWF"`、`"FEFWE"`、`"FEFEW"`、`"FEWFE"`、`"WFEFE"`、`"WFEWE"`、`"WEFWF"`、`"WEFWE"`、`"WEFEF"`、`"WEFEW"`、`"WEWFW"`、`"WEWFE"`、`"EWFWE"`、`"EWEWE"`

---

### 约束

- `1 <= s.length <= 1000`
- `s[i]` 为 `'F'`、`'W'` 或 `'E'` 之一

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 满足 “相邻两轮不相同” 条件的 Bob 序列枚举出来，逐一计算与 Alice 的对局得分，然后统计得分差 (`BobScore - AliceScore`) 为正的序列个数。

- **枚举序列**：把每一轮 Bob 可以出的三种魔兽 `F、W、E` 看成 3 条路，走 `n` 步形成一条完整的路径。因为相邻两步不能相同，相当于在走路时每一步只能换到另外两条路上。
- **计算得分**：每一轮比较 Bob 出的魔兽 `b` 与 Alice 对应的 `a = s[i]`，如果 `b` 能击败 `a`（类似石头剪刀布的关系）则 Bob 得 1 分；如果 `a` 能击败 `b`，则 Alice 得 1 分；否则平局，两人都不加分。  
  这里的击败关系是  
  ```
  F beats E,   E beats W,   W beats F
  ```
- **统计**：把每条合法路径的总分差 `diff = BobScore - AliceScore` 记录下来，最后把 `diff > 0` 的路径计数相加。

> **生活化类比**：枚举所有路径就像把一张城市地图上所有可能的旅行路线画出来，再逐条检查哪条路线的风景（得分）更好，最后把风景更好的路线数目统计出来。

> **为什么正确**：我们把所有符合约束的序列都考虑到了，且每条序列的得分计算是完全按照题目规则进行的，所以统计得到的正差序列数就是答案。

#### 代码（Python）

```python
MOD = 10**9 + 7
# 三种魔兽对应的整数，方便后面做索引
CREATURES = ['F', 'W', 'E']
# 击败关系：b beats a -> 1， a beats b -> -1， otherwise 0
def outcome(b, a):
    if b == a:
        return 0
    if (b == 'F' and a == 'E') or \
       (b == 'E' and a == 'W') or \
       (b == 'W' and a == 'F'):
        return 1          # Bob 赢
    return -1             # Alice 赢

def brute(s: str) -> int:
    n = len(s)
    ans = 0

    # 递归枚举所有合法序列
    def dfs(pos: int, prev: str, diff: int):
        """pos: 当前正在决定第 pos 位（0‑based）
           prev: 前一次出过的魔兽（用于判断相邻不能相同）
           diff: 当前的分差 (Bob - Alice)"""
        nonlocal ans
        if pos == n:               # 序列已经写完
            if diff > 0:
                ans = (ans + 1) % MOD
            return
        for cur in CREATURES:
            if cur == prev:        # 不能和前一次相同
                continue
            ndiff = diff + outcome(cur, s[pos])
            dfs(pos + 1, cur, ndiff)

    # 第 0 位没有前驱，用空字符占位
    dfs(0, '', 0)
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(3 * 2^{n-1})`（每一位最多有 2 种选择，整体呈指数增长）。在最坏情况下，枚举的序列数约为 `2^{n}`，所以随 `n` 增大会非常慢。  
  > 大白话：如果 `n = 30`，我们可能要检查超过 **十亿** 条序列，显然不可接受。

- **空间复杂度**：`O(n)`（递归栈的深度为 `n`，其余只用常数级别的额外空间）。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **枚举**——我们把所有合法序列都列出来了，但实际上我们只关心每一步结束时的 **分差** 和 **上一轮出什么**，这两个信息足以决定后面的所有可能性。  

> **核心观察**：在第 `i` 轮结束后，只要知道  
> 1. 当前的分差 `diff = BobScore - AliceScore`（范围在 `[-i, i]`）  
> 2. Bob 本轮出的是哪种魔兽 `last`（`F、W、E` 中一种）  
> 那么第 `i+1` 轮的所有合法选择以及对应的分差变化都是唯一确定的。  

于是我们可以把“枚举所有序列”换成 **动态规划**（DP）：

- `dp[i][diff][last]` = 前 `i+1` 轮（即第 `0…i`）合法序列的数量，且此时分差为 `diff`，第 `i` 轮 Bob 出的魔兽是 `last`。  
- `diff` 可能为负数，为了用数组下标，需要做偏移。令 `offset = n`，则真实下标 = `diff + offset`，范围是 `0 … 2n`。  

**转移**  
从第 `i-1` 轮的状态转到第 `i` 轮，只需要遍历 **上一轮的出招** `prev`（3 种）以及 **当前可以出的招** `cur`（只能是除 `prev` 之外的另外两种），计算本轮的得分变化 `delta = outcome(cur, s[i])`，于是：

```
new_diff = old_diff + delta
dp[i][new_diff][cur] += dp[i-1][old_diff][prev]
```

**初始化**  
第 0 轮没有“上一轮”，所以我们直接把三种可能的起手（但仍要满足 “相邻不能相同”，第 0 轮没有前驱，任意都可以）放进去：

```
for cur in CREATURES:
    delta = outcome(cur, s[0])
    dp[0][delta][cur] = 1
```

**答案**  
遍历最后一轮 `i = n-1` 的所有状态，只要 `diff > 0`（Bob 的总分高于 Alice）就把对应计数累加。

**空间优化**  
注意到转移只依赖 `i-1` 那一层的数据，完全可以用 **滚动数组**（两个 2‑D 表）把空间从 `O(n * 3 * (2n+1))` 降到 `O(3 * (2n+1))`，即 `O(n)`。

> **类比**：把 DP 想成在“记分板”上记录每一轮结束时可能的“分差 + 上一招”。每轮只要看前一次记的分差和招式，就能算出本轮所有可能的记分方式，最后把正分差的记分方式加起来，就是答案。

#### 代码（Python）

```python
MOD = 10**9 + 7
CREATURES = ['F', 'W', 'E']

def outcome(b: str, a: str) -> int:
    """返回本轮分差的增量：Bob 赢 +1，Alice 赢 -1，平局 0"""
    if b == a:
        return 0
    if (b == 'F' and a == 'E') or \
       (b == 'E' and a == 'W') or \
       (b == 'W' and a == 'F'):
        return 1
    return -1

def countWinningSequences(s: str) -> int:
    n = len(s)
    offset = n                         # 用来把负数 diff 映射到数组下标
    # dp_prev[diff+offset][last]  -> 前 i 层的状态
    dp_prev = [[0] * 3 for _ in range(2 * n + 1)]

    # ---------- 初始化第 0 轮 ----------
    for idx, cur in enumerate(CREATURES):
        d = outcome(cur, s[0])          # 第 0 轮的分差
        dp_prev[d + offset][idx] = 1    # 只出现一次

    # ---------- 逐轮转移 ----------
    for i in range(1, n):
        dp_cur = [[0] * 3 for _ in range(2 * n + 1)]
        for diff in range(-i, i + 1):            # 前 i 轮可能的分差范围
            for prev_idx, prev in enumerate(CREATURES):
                cnt = dp_prev[diff + offset][prev_idx]
                if cnt == 0:
                    continue
                # 当前轮可以出的招式：除 prev 之外的另外两种
                for cur_idx, cur in enumerate(CREATURES):
                    if cur == prev:
                        continue
                    delta = outcome(cur, s[i])
                    new_diff = diff + delta
                    dp_cur[new_diff + offset][cur_idx] = \
                        (dp_cur[new_diff + offset][cur_idx] + cnt) % MOD
        dp_prev = dp_cur   # 滚动到下一层

    # ---------- 统计答案 ----------
    ans = 0
    for diff in range(1, n + 1):          # 只要 diff > 0
        for idx in range(3):
            ans = (ans + dp_prev[diff + offset][idx]) % MOD
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n * 3 * 3 * (2n+1)) = O(n²)`。  
  - 解释：外层遍历 `n` 轮；每轮我们遍历所有可能的 `diff`（最多 `2i+1 ≤ 2n+1`）和 3 种前一次的招式，再枚举最多 2 种当前合法招式。整体是二次多项式。  
  - 与暴力的指数级别相比，二次级别在 `n ≤ 1000` 时轻松跑完。

- **空间复杂度**：`O(3 * (2n+1)) = O(n)`。  
  - 只保留当前层和前一层的 DP 表，数组大小与 `n` 成线性关系。

---

## 心得

- **核心技巧**：把 “相邻不能相同 + 分差” 两个约束抽象成状态 `(last_move, diff)`，用动态规划在每一步累计可能的序列数。  
- **适用的题型**  
  1. 需要统计满足 **相邻约束** 且涉及 **累计分数/差值** 的序列（如 “统计满足不相邻相同且总和大于某值的序列”）。  
  2. 类似 **石头剪刀布** 的对局计分问题，要求 **总胜率** 或 **总分差** 的计数。  
- **一句话总结**：把“每轮的局部信息（上一次出招、当前分差）”保存下来，整个序列的计数就能递推得到。

---

## 反思

- **第一反应**：看到“相邻两轮不能相同”，立刻想到枚举所有合法序列；看到“总分差要大于 0”，想到直接比较得分。  
- **最容易踩的坑**  
  1. **分差范围**：忘记把负数 `diff` 用偏移量转化为数组下标，导致索引错误。  
  2. **相邻约束**：在转移时必须排除 `cur == prev`，否则会错误计入非法序列。  
  3. **模数运算**：累加时忘记取模，导致整数溢出。  
- **下次第一步**：先思考“状态压缩”。把题目中的约束（相邻不可相同、累计分差）抽象成可以递推的状态集合，再判断是否可以用 DP 把枚举转化为多项式时间的计算。