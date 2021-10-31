# #1531. 字符串压缩 II / String Compression II

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/string-compression-ii/)

---

## 题目（英文原版）

**Description**

Run-length encoding is a string compression method that works by replacing consecutive identical characters (repeated 2 or more times) with the concatenation of the character and the number marking the count of the characters (length of the run). For example, to compress the string "aabccc" we replace "aa" by "a2" and replace "ccc" by "c3". Thus the compressed string becomes "a2bc3".
Notice that in this problem, we are not adding '1' after single characters.
Given a string s and an integer k. You need to delete at most k characters from s such that the run-length encoded version of s has minimum length.
Find the minimum length of the run-length encoded version of s after deleting at most k characters.

**Examples**

**Example 1:**

```
Input: s = "aaabcccd", k = 2
Output: 4
Explanation: Compressing s without deleting anything will give us "a3bc3d" of length 6. Deleting any of the characters 'a' or 'c' would at most decrease the length of the compressed string to 5, for instance delete 2 'a' then we will have s = "abcccd" which compressed is abc3d. Therefore, the optimal way is to delete 'b' and 'd', then the compressed version of s will be "a3c3" of length 4.
```

**Example 2:**

```
Input: s = "aabbaa", k = 2
Output: 2
Explanation: If we delete both 'b' characters, the resulting compressed string would be "a4" of length 2.
```

**Example 3:**

```
Input: s = "aaaaaaaaaaa", k = 0
Output: 3
Explanation: Since k is zero, we cannot delete anything. The compressed string is "a11" of length 3.
```

**Constraints**

- 1 <= s.length <= 100
- 0 <= k <= s.length
- s contains only lowercase English letters.

---

## 题目（中文翻译）

**题目描述**  
Run-length encoding（行程编码）是一种字符串压缩方法，它通过将连续相同的字符（出现次数 ≥ 2）替换为字符本身加上表示该字符出现次数的数字（即该段的长度）来实现压缩。例如，要压缩字符串 `"aabccc"`，我们把 `"aa"` 替换为 `"a2"`，把 `"ccc"` 替换为 `"c3"`，压缩后的字符串为 `"a2bc3"`。  
需要注意的是，在本题中，对出现一次的字符 **不** 添加 `'1'`。

给定一个字符串 `s` 和一个整数 `k`，你可以最多删除 `k` 个字符。请在删除至多 `k` 个字符后，使 `s` 的行程编码（run-length encoded）结果的长度最小。返回该最小长度。

**示例**  

*示例 1*  
```
Input: s = "aaabcccd", k = 2
Output: 4
Explanation: 不进行删除时，压缩后得到 "a3bc3d"，长度为 6。  
如果只删除 `'a'` 或 `'c'` 中的字符，压缩长度最多降到 5（例如删除两个 `'a'`，得到 s = "abcccd"，压缩后为 "abc3d"）。  
最佳做法是删除字符 `'b'` 和 `'d'`，此时 s 变为 "aaaccc"，压缩后为 "a3c3"，长度为 4。
```

*示例 2*  
```
Input: s = "aabbaa", k = 2
Output: 2
Explanation: 删除两个 `'b'` 后，得到的压缩字符串为 "a4"，长度为 2。
```

*示例 3*  
```
Input: s = "aaaaaaaaaaa", k = 0
Output: 3
Explanation: k 为 0，不能删除任何字符。压缩后得到 "a11"，长度为 3。
```

**约束条件**  

- `1 <= s.length <= 100`
- `0 <= k <= s.length`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举**所有可以删掉的字符组合，然后把剩下的字符串做普通的跑长编码（run‑length encoding），取最短的编码长度。  

- **数据结构**：我们只需要一个普通的 Python `list` 或 `str` 来保存当前剩余的字符。可以把“删除字符”想象成在一段文字里挑选若干字母擦掉，剩下的文字再交给压缩机处理。  
- **正确性**：因为我们把**所有**合法的删法（最多 `k` 个）都尝试了一遍，必然能找到最优的那一种。  
- **时间/空间复杂度**：  
  - 对长度为 `n` 的字符串，最多要在 `C(n,0)+C(n,1)+…+C(n,k)` 种删法之间选择。最坏情况下（`k = n`）就是 `2^n` 种。  
  - 对每一种删法，我们要重新遍历一次剩余字符做压缩，时间是 `O(n)`。  
  - 因此整体时间是 **指数级**，记作 `O(2^n)`，这在 `n ≤ 100` 时根本不可接受。  
  - 空间只需要保存递归栈和临时字符串，都是 `O(n)`。

> **大白话**：`O(2^n)` 就像把所有可能的“是否删除每个字符”情况列出来，像把一本 100 页的书每页都可能被撕掉或不撕，组合数会天文数字。

#### 代码（Python）

```python
from itertools import combinations

def compress_len(t: str) -> int:
    """返回字符串 t 的跑长编码长度（不计入单个字符后的 '1'）。"""
    if not t:
        return 0
    res, cnt = 1, 1          # 第一个字符必然占 1 位
    for i in range(1, len(t)):
        if t[i] == t[i - 1]:
            cnt += 1
        else:
            # 结束当前连续段，加入计数字的位数
            if cnt > 1:
                res += len(str(cnt))
            cnt = 1
            res += 1          # 新字符本身占 1 位
    if cnt > 1:               # 最后一段的计数字位数
        res += len(str(cnt))
    return res

def minLength_bruteforce(s: str, k: int) -> int:
    n = len(s)
    best = float('inf')
    # 枚举要删掉的字符位置集合，大小从 0 到 k
    for del_cnt in range(k + 1):
        for idxs in combinations(range(n), del_cnt):
            del_set = set(idxs)
            remain = ''.join(ch for i, ch in enumerate(s) if i not in del_set)
            best = min(best, compress_len(remain))
    return best
```

#### 复杂度

- **时间复杂度**：`O(2^n * n)`（指数级），因为要遍历所有删除方案。  
- **空间复杂度**：`O(n)`，主要是递归/临时字符串的存储。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有删除方式**。我们需要把“删几个字符”这件事变成**状态**，用动态规划（DP）把子问题的答案记下来，避免重复计算。

**核心观察**  

1. **压缩长度只和每段相同字符的出现次数有关**。  
   - 出现 1 次 → 只写字符本身，长度 `1`。  
   - 出现 2~9 次 → 需要额外 1 位数字（`2`~`9`），长度 `2`。  
   - 出现 10~99 次 → 需要 2 位数字，长度 `3`。  
   - 出现 ≥100 次 → 需要 3 位数字，长度 `4`。  

2. **在处理前 i 个字符时，只需要知道已经删掉了多少字符**。  
   - 设 `dp[i][j]` 为**处理前 i 个字符**（即 `s[:i]`），并且**已经删掉 j 个字符**时，压缩后得到的最小长度。  
   - 最终答案是 `min_{j ≤ k} dp[n][j]`（n 为字符串长度）。

3. **转移**  
   - 对于位置 `i`（1‑based），我们可以把它归到前面已经形成的某段相同字符里，或者把它单独当成一段。  
   - 为了把 `s[i-1]` 合并到前面的同字符段，需要**删除中间不相同的字符**。这正好可以用前缀计数来求出需要删多少。

**实现细节**  

- 用 `dp = [[inf] * (k+1) for _ in range(n+1)]` 初始化，`dp[0][*] = 0`（空串压缩长度为 0）。  
- 外层遍历 `i = 1 … n`（处理到第 i 个字符）。  
- 内层遍历已删字符数 `j = 0 … k`。  
- 对于每个 `i, j`，我们尝试把第 `i` 个字符 **单独成段**（即不合并到前面的相同字符），这需要 `dp[i-1][j] + 1`（字符本身占 1 位）。  
- 更进一步，我们尝试把 `s[i-1]` **合并到前面某个位置 `p`（p < i）**，且 `s[p-1] == s[i-1]`。  
  - 统计在区间 `[p, i]` 中不同字符的数量 `del_needed`（即需要删除的字符数），如果 `j >= del_needed`，则可以在已有的 `j - del_needed` 删除预算下完成合并。  
  - 合并后，这一段的长度取决于该段最终的出现次数 `cnt = i - p + 1 - del_needed`（原长度减去删掉的字符）。  
  - 根据 `cnt` 的大小加上对应的数字位数（0 位、1 位、2 位或 3 位），得到新的压缩长度 `dp[p-1][j - del_needed] + added_len`。  
  - 取所有可能 `p` 中的最小值更新 `dp[i][j]`。

**为什么可以 O(n³)？**  

- `i` 有 `n` 种，`j` 有 `k ≤ n` 种，内部枚举左端点 `p` 最多 `i` 次。整体是 `O(n * n * n) = O(n³)`，而 `n ≤ 100`，`100³ = 1,000,000`，在 Python 中完全可以接受。

> **类比**：把 DP 想象成“在走迷宫”。每走一步（处理一个字符），我们记录下已经用了多少“炸药”（删除次数）以及到达当前位置的最短路径（压缩长度）。以后再到同一个格子时，只要看之前留下的最短路径，就不必重新探索所有可能的路线。

#### 代码（Python）

```python
import math

def get_len(cnt: int) -> int:
    """
    根据出现次数 cnt，返回该段在压缩后占用的字符数。
    1 -> 1 (只写字符)
    2~9 -> 2
    10~99 -> 3
    >=100 -> 4
    """
    if cnt == 1:
        return 1          # 只写字符本身
    if cnt < 10:
        return 2          # 字符 + 1 位数字
    if cnt < 100:
        return 3          # 字符 + 2 位数字
    return 4              # 字符 + 3 位数字（题目长度 ≤100，实际不会超过 3 位）

def minLength_dp(s: str, k: int) -> int:
    n = len(s)
    INF = math.inf
    # dp[i][j] = 处理前 i 个字符，已经删掉 j 个字符时的最小压缩长度
    dp = [[INF] * (k + 1) for _ in range(n + 1)]
    for j in range(k + 1):
        dp[0][j] = 0                     # 空串压缩长度为 0

    # 主循环
    for i in range(1, n + 1):            # i 表示处理到第 i 个字符（1‑based）
        ch = s[i - 1]                    # 当前字符
        for j in range(k + 1):           # 已经使用的删除次数
            # 1）把第 i 个字符单独成段（不合并到前面的同字符）
            dp[i][j] = min(dp[i][j], dp[i - 1][j] + 1)

            # 2）尝试把第 i 个字符合并到前面的某个相同字符位置 p
            cnt_same = 0                 # 区间内相同字符的数量（包括 i）
            del_needed = 0               # 为了把区间压缩为同字符，需要删除的不同字符数
            # 从 i 往左扫描，找所有可能的左端点 p
            for p in range(i, 0, -1):
                if s[p - 1] == ch:
                    cnt_same += 1
                else:
                    del_needed += 1      # 这个字符必须被删才能合并

                if del_needed > j:      # 删除预算不够，后面的 p 更左也不可能满足
                    break

                # 这段最终的出现次数 = cnt_same
                added_len = get_len(cnt_same)
                # 合并后，前缀长度是 dp[p-1][j - del_needed]
                dp[i][j] = min(dp[i][j],
                               dp[p - 1][j - del_needed] + added_len)

    # 在所有允许的删除次数 ≤ k 中取最小值
    return min(dp[n][j] for j in range(k + 1))
```

#### 复杂度

- **时间复杂度**：`O(n³)`，其中 `n = len(s) ≤ 100`。  
  - 与暴力解相比，指数级的 `2ⁿ` 下降到了多项式级的 `n³`，实际运行在几毫秒内。  
- **空间复杂度**：`O(n·k)`，即 `O(n²)`（因为 `k ≤ n`），用于保存 DP 表。

---

## 心得

- **核心技巧**：**动态规划 + 状态压缩**。把“已经删了多少字符”作为 DP 的维度，使得每一步只需要考虑局部的合并与删除。  
- **适用的题型**  
  1. **带删除限制的压缩/分组**（如 LeetCode 1531 String Compression II）。  
  2. **在序列上做有限次修改后求最优值**（如“删掉最多 k 个字符，使得回文子序列最长”）。  
  3. **区间合并类 DP**（如“把数组压缩成若干段，使得每段代价最小”。）  
- **一句话总结解题钥匙**：**把“删多少字符”放进状态，用 DP 把每一次“把当前字符加入哪段”转化为局部最优子问题。**

---

## 反思

- **第一反应**：直接想到枚举所有删法（暴力），因为题目只给了 `k ≤ 100`，一开始没有意识到要用 DP。  
- **最容易踩的坑**  
  1. **计数字位数**：忘记 `cnt = 1` 时不写数字，导致压缩长度计算错误。  
  2. **删除预算的更新**：在左扫时忘记累计 `del_needed`，或者在 `dp[p-1][j-del_needed]` 中使用负索引。  
  3. **边界情况**：`k = 0`（不能删）以及全部字符相同（计数可能达到两位数或三位数）时的长度计算。  
- **下次遇到同类题**：第一步先**确定 DP 的状态**——通常是“处理到哪儿” + “还剩多少操作次数”。随后思考**如何从一个状态转移到下一个状态**（合并、删除或新开段），并注意**计数/费用的离散取值**（如 1、2‑9、10‑99、≥100）对复杂度的影响。