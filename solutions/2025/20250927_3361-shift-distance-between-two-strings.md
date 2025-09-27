# #3361. 两个字符串之间的移位距离 / Shift Distance Between Two Strings

> 难度：中等 · 标签：Array、String、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/shift-distance-between-two-strings/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t of the same length, and two integer arrays nextCost and previousCost.
In one operation, you can pick any index i of s, and perform either one of the following actions:
The shift distance is the minimum total cost of operations required to transform s into t.
Return the shift distance from s to t.

**Examples**

**Example 1:**

```
Input: s = "abab", t = "baba", nextCost = [100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], previousCost = [1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: 2
Explanation:
```

**Example 2:**

```
Input: s = "leet", t = "code", nextCost = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], previousCost = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
Output: 31
Explanation:
```

**Constraints**

- 1 <= s.length == t.length <= 105
- s and t consist only of lowercase English letters.
- nextCost.length == previousCost.length == 26
- 0 <= nextCost[i], previousCost[i] <= 109

---

## 题目（中文翻译）

**描述**  
给定两个等长的字符串 `s` 和 `t`，以及两个整数数组 `nextCost` 和 `previousCost`。  
在一次操作中，你可以选择 `s` 的任意下标 `i`，并执行以下两种操作之一：

*（此处原题应描述具体的 shift 操作，保留原文空缺）*

移位距离（shift distance）是将 `s` 转换为 `t` 所需的最小总操作费用。  
返回从 `s` 到 `t` 的移位距离。

**示例 1**  
```text
Input: s = "abab", t = "baba", nextCost = [100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], previousCost = [1,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
Output: 2
Explanation: 
```

**示例 2**  
```text
Input: s = "leet", t = "code", nextCost = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], previousCost = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
Output: 31
Explanation: 
```

**约束条件**  
- `1 <= s.length == t.length <= 10^5`  
- `s` 和 `t` 仅由小写英文字母组成。  
- `nextCost.length == previousCost.length == 26`  
- `0 <= nextCost[i], previousCost[i] <= 10^9`

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

把每个字符看成 **字母环**（a → b → … → z → a），  
在环上向右走叫 **next**（向后一个字母），向左走叫 **previous**（向前一个字母）。  

- `nextCost[i]`：把字母 `i`（0 表示 a，1 表示 b …）往 **右** 移动一步的花费。  
- `previousCost[i]`：把字母 `i` 往 **左** 移动一步的花费。  

要把 `s[i]` 变成 `t[i]`，我们可以不停地向右或向左走，直到走到目标字母，走的每一步都累加对应的费用。  

最直接的做法就是 **一步步模拟**：

1. 把 `s[i]` 和 `t[i]` 的字母序号记为 `a`、`b`（0‑25）。  
2. 若 `a == b`，费用为 0。  
3. 否则：  
   - 向右（next）走，从 `a` 一直加 1（模 26）到 `b`，把沿途的 `nextCost` 加起来。  
   - 向左（previous）走，从 `a` 一直减 1（模 26）到 `b`，把沿途的 `previousCost` 加起来。  
4. 两种走法的费用取最小值，就是把 `s[i]` 变成 `t[i]` 的 **最小费用**。  

把所有位置的费用相加，就是题目要求的 **shift distance**。

> **类比**：想象你在一条环形跑道上跑步，每一步都有不同的体力消耗。要从起点跑到终点，你可以顺时针或逆时针跑，选体力消耗更少的方向。

这个思路**一定正确**，因为我们枚举了唯一可能的两条最短路径（顺时针、逆时针），任意其他“拐弯”都会多走不必要的步数，只会让费用更高。

#### 代码（Python）

```python
def brute_shift_distance(s: str, t: str,
                         nextCost: list[int],
                         previousCost: list[int]) -> int:
    total = 0
    for ch_s, ch_t in zip(s, t):
        a = ord(ch_s) - ord('a')      # s[i] 在字母表中的下标
        b = ord(ch_t) - ord('a')      # t[i] 的下标

        if a == b:                    # 已经相同，费用为 0
            continue

        # -------- 向右（next）走 ----------
        cost_next = 0
        cur = a
        while cur != b:               # 循环到目标字母
            cost_next += nextCost[cur]   # 走一步的费用
            cur = (cur + 1) % 26          # 环形移动

        # -------- 向左（previous）走 ----------
        cost_prev = 0
        cur = a
        while cur != b:
            cost_prev += previousCost[cur]   # 走一步的费用
            cur = (cur - 1) % 26              # 环形移动

        total += min(cost_next, cost_prev)   # 取较小的费用
    return total
```

> 关键行都有中文注释，帮助理解每一步在做什么。

#### 复杂度  

- **时间复杂度**：`O(26 * n)`（每个字符最多走 26 步，`n = len(s)`）。  
  用大白话说，就是**每个字符最多走完整个字母环一圈**，所以最坏情况下每个字符需要 26 次循环，总共是 26 倍的字符串长度。  
- **空间复杂度**：`O(1)`（只用常数个临时变量），不随输入规模增长。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次都要**循环**去累计费用。  
实际上，**环上任意两点之间的费用**可以提前算好，随后查询时直接拿出来，用 **O(1)** 的时间得到。

**核心技巧**：**前缀和**（Prefix Sum）  
- 把 `nextCost` 看成一个长度为 26 的数组，先算出它的**累计前缀和** `preNext[i]`，表示从 `a`（下标 0）走到字母 `i`（不含 `i`）的费用总和。  
- 同理算出 `previousCost` 的累计前缀和 `prePrev[i]`。

有了前缀和，**顺时针**（next）从 `a` 到 `b` 的费用可以用两次减法得到：

```
if a < b:   forward = preNext[b] - preNext[a]
else:       forward = totalNext - (preNext[a] - preNext[b])
```

其中 `totalNext = sum(nextCost)` 是整圈走一遍的费用。  
逆时针（previous）同理：

```
if a > b:   backward = prePrev[a] - prePrev[b]
else:       backward = totalPrev - (prePrev[b] - prePrev[a])
```

（这里把「向左」的累计方向定义为从大下标往小下标走，方便写公式。）

把 **所有 26 × 26 对字符** 的最小费用预先算好，保存在 `cost[a][b]` 中。  
随后遍历字符串，只需 `cost[a][b]` 直接相加，**时间降到 O(n)**。

> **类比**：想象你在城市里查公交费用。暴力解是每次都走完整条线路去加总车费；最优解是先把每两站之间的费用算好，查询时直接看表。

#### 代码（Python）

```python
def shift_distance(s: str, t: str,
                   nextCost: list[int],
                   previousCost: list[int]) -> int:
    # ---------- 1. 前缀和 ----------
    # preNext[i] = sum(nextCost[0 .. i-1])
    preNext = [0] * 27          # 额外一个位置方便计算
    for i in range(26):
        preNext[i + 1] = preNext[i] + nextCost[i]
    totalNext = preNext[26]      # 整圈费用

    # prePrev[i] = sum(previousCost[0 .. i-1])
    prePrev = [0] * 27
    for i in range(26):
        prePrev[i + 1] = prePrev[i] + previousCost[i]
    totalPrev = prePrev[26]

    # ---------- 2. 预计算任意字符对的最小费用 ----------
    # cost[a][b] 表示把字符 a (0..25) 变成字符 b 的最小费用
    cost = [[0] * 26 for _ in range(26)]

    for a in range(26):
        for b in range(26):
            if a == b:
                cost[a][b] = 0
                continue

            # ----- forward (next) -----
            if a < b:
                forward = preNext[b] - preNext[a]
            else:  # a > b，需要环绕一圈
                forward = totalNext - (preNext[a] - preNext[b])

            # ----- backward (previous) -----
            if a > b:
                backward = prePrev[a] - prePrev[b]
            else:  # a < b，需要环绕一圈
                backward = totalPrev - (prePrev[b] - prePrev[a])

            cost[a][b] = min(forward, backward)

    # ---------- 3. 累加所有位置的费用 ----------
    ans = 0
    for ch_s, ch_t in zip(s, t):
        a = ord(ch_s) - ord('a')
        b = ord(ch_t) - ord('a')
        ans += cost[a][b]

    return ans
```

> **关键行解释**  
> - `preNext[i + 1] = preNext[i] + nextCost[i]`：把费用累计起来，类似“从起点走到第 i+1 站的总费用”。  
> - `forward = totalNext - (preNext[a] - preNext[b])`：当需要跨过字母表的结尾时，先走完一整圈的费用 `totalNext`，再减掉多走的那段。  
> - `cost[a][b] = min(forward, backward)`：在顺时针和逆时针两条最短路径中挑最省钱的那条。

#### 复杂度  

- **时间复杂度**：`O(26² + n)`  
  - 预计算 26×26 对字符的费用是常数（`26² = 676`），可以忽略不计。  
  - 主循环遍历字符串一次，`O(n)`。  
  与暴力解的 `O(26·n)` 相比，**把 26 这个常数从乘法降到了加法**，在 `n` 达到 `10⁵` 时更安全、更快。  
- **空间复杂度**：`O(26²)`（存 `cost` 表），约 676 个整数，几乎可以视作常数。  

---

## 心得  

- **核心技巧**：**前缀和 + 环形距离**  
  通过一次遍历把每一步的费用累计起来，后面查询任意两点的费用只需要两次减法（或一次加法），实现 **O(1)** 查询。  
- **适用题型**  
  1. 环形或循环结构上的最短距离（如“旋转锁”类问题）。  
  2. 需要多次查询两点之间累计值的场景（如“区间和”或“环形数组的最小代价”）。  
- **一句话总结**：**把所有可能的转移费用先算好，后面只需要表格查表，就能把每个字符的最小费用瞬间得到。**  

---

## 反思  

- **第一反应**：把每个字符一步步模拟，直接累加费用。  
- **最容易踩的坑**  
  1. **环绕计算错误**：在 a > b 或 a < b 时，需要正确处理跨越字母表末尾的情况，容易把 `totalNext`、`totalPrev` 写反。  
  2. **下标越界**：前缀和数组多加一个哨兵位（长度 27）可以避免 `pre[i]` 访问越界。  
  3. **大数相加**：费用上限 `10⁹`，字符串长度 `10⁵`，答案可能超过 32 位整数，需要使用 Python 的大整数（默认安全）或在其他语言里使用 64 位整数。  
- **下次遇到同类题**：第一步想到“**把一次性求和的过程抽象成前缀和**”，再判断是否有环形（模 26）或循环结构，进而把“遍历+累加”转化为“预处理+常数时间查询”。