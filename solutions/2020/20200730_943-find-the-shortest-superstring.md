# #943. 最短超级串 / Find the Shortest Superstring

> 难度：困难 · 标签：Array、String、Dynamic Programming、Bit Manipulation、Bitmask · [LeetCode 链接](https://leetcode.com/problems/find-the-shortest-superstring/)

---

## 题目（英文原版）

**Description**

Given an array of strings words, return the smallest string that contains each string in words as a substring. If there are multiple valid strings of the smallest length, return any of them.
You may assume that no string in words is a substring of another string in words.

**Examples**

**Example 1:**

```
Input: words = ["alex","loves","leetcode"]
Output: "alexlovesleetcode"
Explanation: All permutations of "alex","loves","leetcode" would also be accepted.
```

**Example 2:**

```
Input: words = ["catg","ctaagt","gcta","ttca","atgcatc"]
Output: "gctaagttcatgcatc"
```

**Constraints**

- 1 <= words.length <= 12
- 1 <= words[i].length <= 20
- words[i] consists of lowercase English letters.
- All the strings of words are unique.

---

## 题目（中文翻译）

给定一个字符串数组（array of strings）`words`，返回包含 `words` 中每个字符串作为子字符串（substring）的最短字符串。如果存在多个满足最小长度的有效字符串，返回任意一个即可。  
可以假设 `words` 中不存在某个字符串是另一个字符串的子字符串。

**示例 1**  
**示例 2**  

**约束条件**  

- 1 ≤ `words.length` ≤ 12  
- 1 ≤ `words[i].length` ≤ 20  
- `words[i]` 仅由小写英文字母组成。  
- `words` 中的所有字符串互不相同。

**示例**

**示例 1**  
```
Input: words = ["alex","loves","leetcode"]
Output: "alexlovesleetcode"
Explanation: 所有 "alex"、"loves"、"leetcode" 的排列组合均为可接受答案。
```

**示例 2**  
```
Input: words = ["catg","ctaagt","gcta","ttca","atgcatc"]
Output: "gctaagttcatgcatc"
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有单词的排列全部枚举一遍，然后把相邻的两个单词尽可能“粘合”在一起（把重叠的部分省掉），得到一个完整的超字符串。  
- **枚举排列**：`words` 最多 12 个，所有排列的数量是 `12!`（约 4.79×10⁸），虽然很大，但在思考阶段我们只需要先把这个思路写出来，说明它是可行的（只要时间够），不必担心实际运行会超时。  
- **粘合两个单词**：把两个字符串 `a`、`b` 放在一起时，找出 `a` 的后缀和 `b` 的前缀的最长公共部分，然后只把 `b` 剩下的部分接到 `a` 后面。  
  - 这一步可以类比成把两块拼图拼在一起：先把能重叠的那块找出来，然后把剩余的拼到后面。

因为题目保证没有一个单词是另一个的子串，所以我们只需要处理“相邻”两个单词的重叠即可。

**为什么正确**  
遍历所有排列，必然会出现一种排列，使得把相邻单词按最长重叠方式粘合后得到的字符串长度最短。只要我们检查每一种排列，取最短的那一个，就一定能得到答案。

**时间/空间复杂度**  
- 枚举全部排列的时间是 `O(n! * n * L)`，其中 `n = len(words)`（最多 12），`L` 是单词最长长度（≤20），`n` 用来遍历每个排列，`L` 用来计算两个单词的重叠。  
  - 大白话：如果 `n=12`，`12! ≈ 4.8 亿`，每次都要做几百次字符比较，显然在实际运行时会超时。  
- 只使用了几个临时字符串，空间是 `O(n * L)`，即存放所有单词的总长度。

#### 代码（Python）

```python
import itertools

def overlap(a: str, b: str) -> int:
    """返回 a 的后缀与 b 的前缀的最长公共长度"""
    max_olap = min(len(a), len(b))
    for k in range(max_olap, 0, -1):          # 从长到短尝试
        if a[-k:] == b[:k]:                  # 能匹配就返回
            return k
    return 0

def shortestSuperstring_bruteforce(words):
    best = None                                 # 保存目前最短的答案
    for perm in itertools.permutations(words): # 枚举所有排列
        cur = perm[0]                           # 从第一个单词开始构造
        for i in range(1, len(perm)):
            ol = overlap(cur, perm[i])          # 计算当前字符串与下一个单词的重叠
            cur += perm[i][ol:]                 # 只把没有重叠的部分接上去
        if best is None or len(cur) < len(best):
            best = cur                           # 更新最短答案
    return best
```

#### 复杂度

- **时间复杂度**：`O(n! * n * L)`  
  - `n!` 表示所有排列的数量，`n` 表示每条排列中需要拼接 `n-1` 次，`L` 是比较重叠时最多遍历的字符数。  
  - 用生活化的说法：想象把 12 本书排成一排的所有可能顺序，一共有几百亿种；每种顺序我们都要逐本检查拼接，显然太慢了。  
- **空间复杂度**：`O(n * L)`  
  - 只存放原始单词和当前拼接得到的字符串，和 `n`、`L` 成正比。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**枚举所有排列**。我们可以把“排列”这个过程用**动态规划 + 位掩码**（bitmask）来压缩。核心想法：

1. **把“已经放进超字符串的单词集合” 用一个二进制整数 mask 表示**  
   - mask 的第 `i` 位为 1，表示单词 `words[i]` 已经被选进来了。  
   - 这样，一个集合只需要一个整数就能描述，省下了大量的排列空间。

2. **状态 DP[mask][i] 表示：**  
   - 已经选了 `mask` 里所有单词，且**最后一个放进去的是单词 i**，  
   - 产生的最短超字符串是什么（我们只记录字符串本身，或者记录长度加上前驱信息）。

3. **转移**  
   - 若我们已经得到 `DP[mask][i]`，想把一个新单词 `j` 加到末尾（`j` 之前不在 `mask` 中），  
   - 只需要把 `i` 与 `j` 的重叠长度 `overlap[i][j]` 加进去：  
     `new_str = DP[mask][i] + words[j][overlap[i][j]:]`  
   - 取所有可能的 `i` 中最短的那一个，保存为 `DP[mask| (1<<j)][j]`。

4. **起始状态**  
   - 只包含一个单词 `i` 时，`mask = 1<<i`，`DP[mask][i] = words[i]`。

5. **答案**  
   - 当 `mask` 包含全部单词（`mask == (1<<n)-1`）时，遍历所有可能的最后单词 `i`，取最短的 `DP[mask][i]`。

6. **预处理重叠**  
   - 为了在 DP 转移时快速得到 `overlap[i][j]`，我们先在 O(n²·L) 时间里算好每对单词的最长重叠。

**为什么快**  
- 状态数是 `2^n * n`，而 `n ≤ 12`，所以最多 `2^12 * 12 = 49152` 条记录，完全可以在毫秒级遍历完。  
- 每条记录的转移只需要 O(n) 次，整体时间是 `O(n^2 * 2^n)`，约几万次操作，远远快于 `n!`。

#### 代码（Python）

```python
def shortestSuperstring(words):
    n = len(words)

    # ---------- 1. 预处理两两之间的最长重叠 ----------
    # overlap[i][j] = words[i] 的后缀与 words[j] 前缀的最长公共长度
    overlap = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            a, b = words[i], words[j]
            max_olap = min(len(a), len(b))
            # 从长到短检查，找到最大 k 使得 a[-k:] == b[:k]
            for k in range(max_olap, 0, -1):
                if a[-k:] == b[:k]:
                    overlap[i][j] = k
                    break

    # ---------- 2. DP 表：dp[mask][i] 保存最短超字符串 ----------
    # 使用字典存放可以省去大量不必要的字符串复制
    dp = [[""] * n for _ in range(1 << n)]
    # 初始化：只包含单个单词的集合
    for i in range(n):
        dp[1 << i][i] = words[i]

    # ---------- 3. 状态转移 ----------
    for mask in range(1 << n):
        for last in range(n):
            cur_str = dp[mask][last]
            if not cur_str:               # 该状态不存在，直接跳过
                continue
            # 尝试把每一个未使用的单词 nxt 加到末尾
            for nxt in range(n):
                if mask & (1 << nxt):     # nxt 已经在集合里，不能再加
                    continue
                next_mask = mask | (1 << nxt)
                # 计算把 nxt 接到 cur_str 后面后得到的新字符串
                ol = overlap[last][nxt]
                candidate = cur_str + words[nxt][ol:]
                # 如果 dp[next_mask][nxt] 还没写，或者 candidate 更短，就更新
                if dp[next_mask][nxt] == "" or len(candidate) < len(dp[next_mask][nxt]):
                    dp[next_mask][nxt] = candidate

    # ---------- 4. 取最终答案 ----------
    full_mask = (1 << n) - 1
    ans = None
    for i in range(n):
        cand = dp[full_mask][i]
        if cand and (ans is None or len(cand) < len(ans)):
            ans = cand
    return ans
```

> **代码要点注释**（已在代码中标注）  
> - `overlap` 的预处理把“拼图的拼合方式”提前算好，后面 DP 用时只需要查表。  
> - `mask` 用二进制的每一位表示是否已经选了对应的单词，类似“打开/关闭”的开关。  
> - `dp[mask][i]` 只保存最短的字符串，省去比较多余的候选解。

#### 复杂度

- **时间复杂度**：`O(n² * 2ⁿ)`  
  - 解释：`2ⁿ` 是所有可能的子集数（最多 4096），`n²` 来自两层循环（遍历 `last`、`nxt`）以及预处理重叠的 `n²`。  
  - 与暴力的 `n!` 相比，指数从阶乘降到了 2 的指数，规模大幅缩小，实际运行非常快。  

- **空间复杂度**：`O(n * 2ⁿ)`  
  - 解释：DP 表需要存 `2ⁿ` 个子集，每个子集保存 `n` 条记录，另外还有 `overlap` 表占 `n²` 空间。整体仍然在几千到几万条记录的量级，轻松放进内存。

---

## 心得

- **核心技巧**：使用「**位掩码 + 动态规划**」把「遍历所有排列」压缩成「遍历所有子集」。
- **适用场景**：
  1. **旅行商问题（TSP）**的变形，如「最小路径覆盖」等，需要在小规模（`n ≤ 15`）的集合上寻找最优顺序。  
  2. **拼接字符串**类题目，如「拼接所有单词的最短长度」或「构造最长公共子序列」的子集 DP 版本。  
  3. **状态压缩 DP** 的典型例子，如「最小生成树的 Hamiltonian Path」或「按位集合的最优排列」。
- **一句话总结**：把「排列」用「子集 + 最后一个元素」的方式记忆，配合预处理的重叠信息，就能在指数级别的时间内找出最短的超级串。

---

## 反思

- **第一反应**：看到「所有单词必须是子串」立刻想到「枚举全排列」并把相邻单词拼起来——这是一种最直接的暴力思路。  
- **最容易踩的坑**  
  1. **重叠计算错误**：忘记从最长可能的长度开始往下检查，容易得到非最长的公共前后缀，导致最终字符串不够短。  
  2. **位掩码的写法**：`mask & (1 << nxt)` 与 `mask | (1 << nxt)` 必须写对，否则会出现重复或遗漏单词的情况。  
  3. **字符串存储**：在 DP 中直接保存完整字符串会导致拷贝次数很多，若只保存长度需要额外的「前驱」数组来恢复答案。  
- **下次类似题的第一步**：先判断 **「规模是否足够小」**（如 `n ≤ 12~15`），如果是，就立刻考虑 **「位掩码 DP」**，并把 **「两两关系」**（如重叠、距离、费用）预先算好，后面只需要查表。这样可以把原本指数级的排列枚举降到可接受的 2ⁿ 级别。