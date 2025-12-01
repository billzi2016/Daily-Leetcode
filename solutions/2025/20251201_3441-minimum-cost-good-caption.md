# #3441. 最小成本好字幕 / Minimum Cost Good Caption

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-good-caption/)

---

## 题目（英文原版）

**Description**

You are given a string caption of length n. A good caption is a string where every character appears in groups of at least 3 consecutive occurrences.
For example:
You can perform the following operation any number of times:
Choose an index i (where 0 <= i < n) and change the character at that index to either:
Your task is to convert the given caption into a good caption using the minimum number of operations, and return it. If there are multiple possible good captions, return the lexicographically smallest one among them. If it is impossible to create a good caption, return an empty string "".

**Examples**

**Example 1:**

```
Input: caption = "cdcd"
Output: "cccc"
Explanation:
It can be shown that the given caption cannot be transformed into a good caption with fewer than 2 operations. The possible good captions that can be created using exactly 2 operations are:
Since "cccc" is lexicographically smaller than "dddd" , return "cccc" .
```

**Example 2:**

```
Input: caption = "aca"
Output: "aaa"
Explanation:
It can be proven that the given caption requires at least 2 operations to be transformed into a good caption. The only good caption that can be obtained with exactly 2 operations is as follows:
Thus, return "aaa" .
```

**Example 3:**

```
Input: caption = "bc"
Output: ""
Explanation:
It can be shown that the given caption cannot be converted to a good caption by using any number of operations.
```

**Constraints**

- 1 <= caption.length <= 5 * 104
- caption consists only of lowercase English letters.

---

## 题目（中文翻译）

你得到一个长度为 `n` 的字符串 `caption`。  
**好字幕**（good caption）指的是：字符串中每个字符的出现必须以 **至少 3 个连续** 的形式出现。  

例如：

你可以无限次执行以下操作：  
选择一个下标 `i`（满足 `0 <= i < n`），将该下标处的字符更改为**任意小写字母**。

你的任务是将给定的 `caption` 转换成 **好字幕**，要求使用的操作次数最少，并返回转换后的字符串。如果存在多个满足最少操作次数的好字幕，返回字典序（lexicographically）最小的那个。如果根本无法构造好字幕，返回空字符串 `""`。

**示例 1**  
``` 
Input: caption = "cdcd"
Output: "cccc"
Explanation:
可以证明，无法用少于 2 次操作将该字幕转换为好字幕。恰好使用 2 次操作能够得到的好字幕有：
"cccc" 与 "dddd"。由于 "cccc" 的字典序小于 "dddd"，所以返回 "cccc"。
```

**示例 2**  
``` 
Input: caption = "aca"
Output: "aaa"
Explanation:
可以证明，该字幕至少需要 2 次操作才能变为好字幕。恰好使用 2 次操作唯一能得到的好字幕是：
"aaa"。因此返回 "aaa"。
```

**示例 3**  
``` 
Input: caption = "bc"
Output: ""
Explanation:
可以证明，无论进行多少次操作，都无法将该字幕转换为好字幕，所以返回空字符串。
```

**约束条件**  
- `1 <= caption.length <= 5 * 10^4`  
- `caption` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **caption** 看成若干个“块”。  
每个块必须满足：

* 块内部的字符全部相同  
* 块的长度 **≥ 3**  

于是我们可以把字符串从左到右全部枚举所有合法的切分方式，再为每个块枚举 26 种可能的字符，统计把原字符改成该字符需要的操作次数，最后取最小的总次数。

*数据结构*  
- “块”可以用 **列表** 存放 `[左端点, 右端点, 选的字符]`。  
- 为了快速算“把区间 `[l,r]` 改成字符 `c` 需要几次修改”，可以预处理每个字符的前缀和（类似查字典，字符是“词”，下标是“页码”），这样一次查询 O(1)。

*为什么正确*  
只要枚举了所有合法的块划分和所有块的字符，就一定会碰到最优解。因为每一次合法的改动都对应唯一的一套块划分+字符选择。

*复杂度*  
- 块的划分数量是指数级的（每个位置都可能是块的结束），所以时间复杂度是 **O(26ⁿ)**，在最坏情况下几乎是 **O(2ⁿ)**。  
- 空间上只需要保存前缀和，**O(26·n)**。

用大白话说，这相当于“把 5 万个糖果全都一个一个尝”，根本不可能在几秒钟内吃完。

---

### 2. 最优解  

#### 思路  

暴力的瓶颈在 **“枚举所有切分方式”**。  
实际上我们不需要一次性决定整个切分，而是 **一步步决定每个位置的字符**，只要保证**已经确定的前缀**符合 “每段长度 ≥ 3”。  

我们把 **“当前正在构造的块的状态”** 作为 DP 的状态：

| 状态 | 含义 |
|------|------|
| `len = 1` | 当前块只出现了 1 次（还不能结束） |
| `len = 2` | 当前块出现了 2 次（还不能结束） |
| `len = 0` | 当前块已经出现 **≥3 次**，此时可以**结束**块并换成新字符 |

另外，还要记录 **块的字符**（`c`），因为后面继续时要看是否相同。  
于是状态可以写成 `(i, c, len)`，表示 **处理到下标 `i`（已包括 `i`）后，以字符 `c`、长度状态 `len` 结尾的最小修改次数**。

转移只有两种：

1. **继续同一个字符**  
   *若 `len = 1 → 2`、`len = 2 → 0`、`len = 0 → 0`*。  
   只要把当前位置改成 `c`，代价是 `caption[i] != c`。

2. **换成新字符**（只能在 `len = 0` 时换）  
   选任意 `c' ≠ c`，新的状态是 `(i, c', 1)`。  
   代价同样是 `caption[i] != c'`。

因为字符只有 26 种，直接遍历所有 `c'` 会导致 `O(26²·n)`，仍然可以接受，但我们可以进一步 **用 “最小‑次小” 优化** 把换字符的代价降到 `O(1)`：

*在换字符时，只需要 `min_{pc ≠ c} dpPrev0[pc]`*（`dpPrev0` 是上一行“已经 ≥3 次”的最小值）。  
把所有 `dpPrev0` 的最小值与次小值预先算出来，就能在 `O(1)` 内得到 `c` 的最佳前驱。

**正向 DP**（从左到右）只得到前缀的最小代价。  
为了在**同等代价**时得到 **字典序最小** 的答案，需要知道“从当前位置往后最少还要花多少代价”。这可以用 **一次逆向 DP**（从右到左）得到**后缀**的最小代价，记作 `suf0/1/2[i][c]`。

有了前缀最小代价 `pre` 与后缀最小代价 `suf`，我们可以**从左到右贪心**：

*在当前位置尝试字符 `'a' … 'z'`（从小到大），看把它放进去后是否还能达到全局最小代价*。  
只要第一次满足条件，就把它写入答案，进入下一个位置。  
因为我们总是优先选最小的字符，得到的整体字符串必然是字典序最小的。

#### 关键细节  

1. **状态编码**  
   - `len = 0` → “已经 ≥3”，记作 `0`  
   - `len = 1` → 记作 `1`  
   - `len = 2` → 记作 `2`

2. **初始化**  
   - 第 0 位只能是 “长度 1”，所以 `dp1[0][c] = (caption[0] != c)`，`dp0/2` 为 `INF`。

3. **最小‑次小**  
   ```python
   best_val = min(prev0)
   best_idx = argmin(prev0)
   second_best = min(v for i,v in enumerate(prev0) if i != best_idx)
   ```
   对每个字符 `c`，换字符的最佳前驱是  
   `best_val`（如果 `c` 不是最小的下标）否则 `second_best`。

4. **逆向 DP**  
   完全对称，只是把 “前一个状态” 换成 “后一个状态”。  
   同样利用最小‑次小技巧，时间仍是 `O(26·n)`。

5. **不可行情况**  
   若最终的最小代价仍是 `INF`（我们取 `10⁹` 作为无限大），说明没有合法的划分，返回空串 `""`。

#### 复杂度  

| 步骤 | 时间 | 空间 |
|------|------|------|
| 正向 DP | `O(26·n)`（≈ 1.3 × 10⁶ 次操作） | `O(26·n)`（保存每个位置的 3 × 26 整数） |
| 逆向 DP | 同上 | 同上 |
| 重建答案 | `O(26·n)`（每位最多尝试 26 次） | 复用上面的 DP 表 |
| **总计** | **`O(26·n)`** ≈ `O(n)` | **`O(26·n)`** ≈ `O(n)` |

对 `n ≤ 5·10⁴` 完全够快，且只使用了几 MB 的内存。

---

## 心得  

* **核心技巧**：把“每段长度 ≥3”抽象成 **三种长度状态**（1、2、≥3），配合字符信息形成 DP。  
* **适用题型**  
  1. “把字符串划分为满足某种最小长度的块”——如 “删除字符使每块长度≥2”。  
  2. “字符分组且每组必须满足特定大小”——比如 “把数组分成长度≥k 的相等子数组”。  
  3. “最少修改使字符串满足局部约束”——如 “每两个相邻字符不同且每段长度≥3”。  

* **解题钥匙**：**状态压缩 + 最小‑次小优化**，把本来需要遍历 26 × 26 种组合的转移降到 O(1)。

---

## 反思  

* **第一反应**：直接枚举所有切分，立刻发现指数爆炸。  
* **最容易踩的坑**  
  - **忘记检查结尾**：最后一个块必须也 ≥3，否则答案非法。  
  - **换字符时误把自己算进去**：在 “最小‑次小” 时要排除当前字符。  
  - **字典序**：只在全局最小代价下贪心选字符，否则会得到错误的最小串。  
* **下次思路**：一看到 “每段至少 k 个相同字符” 就先想到 **“长度状态（1…k‑1、≥k）+字符”** 的 DP，随后检查是否可以用 **最小‑次小** 把 O(26²) 降到 O(26)。这样既保证最优，又能在 10⁵ 规模内跑得动。  

---  

## 代码（Python）

```python
from typing import List

INF = 10 ** 9
ALPH = 26
ORD_A = ord('a')


def minimumCostGoodCaption(caption: str) -> str:
    n = len(caption)
    # ---------- 逆向 DP（后缀） ----------
    # suf0[i][c] : 从 i 开始，已在一个长度 ≥3 的块中，块字符为 c 的最小代价
    # suf1[i][c] : 从 i 开始，已在长度为1 的块中，块字符为 c 的最小代价
    # suf2[i][c] : 从 i 开始，已在长度为2 的块中，块字符为 c 的最小代价
    suf0: List[List[int]] = [[INF] * ALPH for _ in range(n + 1)]
    suf1: List[List[int]] = [[INF] * ALPH for _ in range(n + 1)]
    suf2: List[List[int]] = [[INF] * ALPH for _ in range(n + 1)]

    # 在 i == n（已经遍历完）时，只有状态 len=0 合法，代价 0
    for c in range(ALPH):
        suf0[n][c] = 0

    # 逆向遍历
    for i in range(n - 1, -1, -1):
        # 当前位置改成字符 ch 的代价（0 表示相同，1 表示不同）
        cost = [0] * ALPH
        for ch in range(ALPH):
            cost[ch] = 0 if caption[i] == chr(ORD_A + ch) else 1

        # 为了在换字符时快速得到除自身外的最小值，预处理 next0 的最小、次小
        next0 = suf0[i + 1]
        best_val = min(next0)
        best_idx = next0.index(best_val)
        second_best = min(v for idx, v in enumerate(next0) if idx != best_idx)

        # 计算 cur1（新块长度 1）
        cur1 = [INF] * ALPH
        for ch in range(ALPH):
            # 换成字符 ch，必须把之前的块结束（所以使用 next0 的最小值，且不能是同一个字符）
            if ch == best_idx:
                min_prev = second_best
            else:
                min_prev = best_val
            cur1[ch] = min_prev + cost[ch]

        # 计算 cur2（长度 2，必须前一个状态是 len=1 且字符相同）
        cur2 = [INF] * ALPH
        for ch in range(ALPH):
            if suf1[i + 1][ch] < INF:
                cur2[ch] = suf1[i + 1][ch] + cost[ch]

        # 计算 cur0（长度 ≥3，可由 len≥3 或 len=2 延伸而来）
        cur0 = [INF] * ALPH
        for ch in range(ALPH):
            prev = min(suf0[i + 1][ch], suf2[i + 1][ch])
            if prev < INF:
                cur0[ch] = prev + cost[ch]

        # 保存到表中
        suf0[i] = cur0
        suf1[i] = cur1
        suf2[i] = cur2

    # ---------- 取全局最小代价 ----------
    total_min = min(suf1[0])          # 必须从长度 1 开始
    if total_min >= INF:             # 没有合法划分
        return ""

    # ---------- 贪心重建字典序最小的好 caption ----------
    ans = []
    i = 0
    prev_char = -1          # -1 表示“还没有前一个字符”
    prev_len = 0            # 0 代表可以随时开始新块（相当于已经 >=3）
    remain = total_min

    while i < n:
        # 依次尝试字符 'a'..'z'
        for ch in range(ALPH):
            # 判断是否合法转移
            if prev_char == -1:          # 第一个字符只能开新块
                new_len = 1
            elif ch == prev_char:
                # 继续同一字符
                if prev_len == 1:
                    new_len = 2
                elif prev_len == 2:
                    new_len = 0
                else:                   # prev_len == 0
                    new_len = 0
            else:
                # 换字符只能在前一个块已经 ≥3 时
                if prev_len != 0:
                    continue
                new_len = 1

            # 计算把位置 i 改成 ch 的即时代价
            cur_cost = 0 if caption[i] == chr(ORD_A + ch) else 1

            # 取得后缀最小代价
            if i + 1 == n:
                suffix = 0 if new_len == 0 else INF
            else:
                if new_len == 0:
                    suffix = suf0[i + 1][ch]
                elif new_len == 1:
                    suffix = suf1[i + 1][ch]
                else:   # new_len == 2
                    suffix = suf2[i + 1][ch]

            if cur_cost + suffix == remain:
                # 这个字符可以得到全局最小代价，且是字典序最小的
                ans.append(chr(ORD_A + ch))
                prev_char = ch
                prev_len = new_len
                remain -= cur_cost
                i += 1
                break   # 跳出 for 循环，进入下一位

    return ''.join(ans)


# ------------------- 示例测试 -------------------
if __name__ == "__main__":
    print(minimumCostGoodCaption("cdcd"))   # -> "cccc"
    print(minimumCostGoodCaption("aca"))    # -> "aaa"
    print(minimumCostGoodCaption("bc"))     # -> ""
```