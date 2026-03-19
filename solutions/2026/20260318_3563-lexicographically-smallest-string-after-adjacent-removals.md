# #3563. Lexicographically Smallest String After Adjacent Removals / Lexicographically Smallest String After Adjacent Removals

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-string-after-adjacent-removals/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters.
You can perform the following operation any number of times (including zero):
Return the lexicographically smallest string that can be obtained after performing the operations optimally.
Note: Consider the alphabet as circular, thus 'a' and 'z' are consecutive.

**Examples**

**Example 1:**

```
Input: s = "abc"
Output: "a"
Explanation:
```

**Example 2:**

```
Input: s = "bcda"
Output: ""
Explanation:
```

**Example 3:**

```
Input: s = "zdce"
Output: "zdce"
Explanation:
```

**Constraints**

- 1 <= s.length <= 250
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

你得到一个只包含小写英文字母的字符串 `s`。  
你可以任意次（包括零次）执行下述操作：

- 选取字符串中两个相邻的字符，如果它们在字母表中是连续的（字母表视为循环的，即 `'a'` 与 `'z'` 也是连续的），则将这两个字符同时删除，剩余字符连接成新的字符串。

请在最优地执行上述操作后，返回能够得到的字典序（lexicographically）最小的字符串。  

**注意**：字母表是循环的，因此 `'a'` 与 `'z'` 被视为相邻。

### 示例

#### 示例 1
**输入**: `s = "abc"`  
**输出**: `"a"`  
**解释**:  

#### 示例 2
**输入**: `s = "bcda"`  
**输出**: `""`  
**解释**:  

#### 示例 3
**输入**: `s = "zdce"`  
**输出**: `"zdce"`  
**解释**:  

### 约束条件
- `1 <= s.length <= 250`
- `s` 只由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们先把题目再说一遍：  
- 给定一个只含小写字母的字符串 `s`。  
- 只要 **相邻的两个字符在字母表中是连续的**（这里把字母表当成环，`a` 与 `z` 也算连续），就可以把这两个字符一次性删掉。  
- 这种操作可以进行任意次（包括 0 次），最后我们想得到 **字典序最小** 的剩余字符串。

最直接的想法就是**枚举所有可能的删除顺序**，把每一种得到的结果记下来，最后挑最小的。  

> **类比**：想象你有一串珠子，只有颜色相邻且相差 1（环形）的两个珠子可以一起摘掉。我们把每一次摘掉的可能性都列出来，最后挑颜色最早的那串珠子。

**为什么暴力一定能得到答案**  
- 只要把每一种合法的“删除序列”都尝试一次，就不会漏掉最优解。  
- 只要一次尝试得到的字符串合法（即再也找不到可删除的相邻对），它就一定是 **一种** 可行的最终结果。  

**时间/空间复杂度**  
- 对长度为 `n` 的字符串，每一步我们都可以选择 **删** 或 **不删**（但只有相邻连续时才可以删），搜索树的高度最多是 `n/2`（每次删掉 2 个字符），分支数大约是 `2^{n/2}`，即 **指数级**。  
- 再加上递归调用栈和保存中间字符串的开销，**时间复杂度约为 O(2^{n/2})**，**空间复杂度 O(n)**（递归深度）。

> **大白话**：如果 `n=20`，最坏情况要尝试大概 2⁽¹⁰⁾≈ 1024 次；如果 `n=100`，则是 2⁽⁵⁰⁾，天文数字，根本跑不完。

#### 代码（Python）

```python
def is_consecutive(a: str, b: str) -> bool:
    """判断两个字符是否在环形字母表中相邻（a‑z 也是相邻）"""
    diff = (ord(b) - ord(a)) % 26
    return diff == 1                      # 只要差 1（正向）即为相邻

def dfs(s: str) -> str:
    """
    暴力递归：尝试所有合法的删除方式，返回字典序最小的结果。
    这里直接返回最小的字符串，递归结束时 s 已经没有可删的相邻对。
    """
    # 先找出所有可以直接删除的相邻对
    n = len(s)
    best = s                               # 至少可以不做任何删除
    i = 0
    while i < n - 1:
        if is_consecutive(s[i], s[i + 1]):
            # 删除 s[i]、s[i+1]，递归求解剩余部分的最小结果
            nxt = dfs(s[:i] + s[i + 2:])
            if nxt < best:                 # 取字典序更小的
                best = nxt
            # 为了不遗漏不同的删除顺序，继续往后找
            i += 1                         # 跳过当前的第一个字符，防止重复删除同一对
        else:
            i += 1
    return best

# 示例
print(dfs("abc"))   # -> "a"
print(dfs("bcda"))  # -> ""
print(dfs("zdce"))  # -> "zdce"
```

**关键注释**  
- `is_consecutive` 把字母表当成环，用 **模 26** 的技巧判断相邻。  
- `dfs` 每次找出所有可以直接删的相邻对，**递归** 删除后继续搜索。  
- `best` 用来保存当前子树里字典序最小的答案。

#### 复杂度

- **时间复杂度**：`O(2^{n/2})` —— 指数级搜索，随字符串长度快速爆炸。  
- **空间复杂度**：`O(n)` —— 递归调用栈的最大深度不超过 `n/2`，每层保存一个新字符串。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**大量重复的子问题**：  
- 同一个子串会被不同的删除顺序多次递归到。  
- 我们其实只关心 **“这个子串能否全部被删掉”**，以及 **“从某个位置开始，最小的结果是什么”**。

因此我们把问题拆成两层 DP：

1. **子串可删性 DP**  
   `rem[l][r] = True` 当且仅当子串 `s[l..r]`（闭区间）**可以全部消除**。  
   - 空串 (`l > r`) 显然可以删掉 → `True`。  
   - 对于非空子串，设我们想让 `s[l]` 最后和某个 `s[k]`（`l < k ≤ r`）配对删掉。  
     为了让 `s[l]` 与 `s[k]` 成为相邻，必须先把 `s[l+1..k-1]` 完全删掉。  
     此外，`s[l]` 与 `s[k]` 必须是字母表相邻（环形）。  
     剩下的右边 `s[k+1..r]` 也必须能删掉。  

   于是递推式：

   ```
   rem[l][r] = any(
        is_consecutive(s[l], s[k]) and rem[l+1][k-1] and rem[k+1][r]
        for k in range(l+1, r+1)
   )
   ```

   这是一种 **三层循环**（`l`、`r`、`k`），时间 `O(n³)`，`n ≤ 250` 完全可接受。

2. **构造最小字典序 DP**  
   记 `best[i]` 为**从下标 `i` 开始**（即子串 `s[i:]`），能够得到的字典序最小的字符串。  
   递推思路：

   - 我们可以先把 `s[i..j-1]` 完全删掉（只要 `rem[i][j-1]` 为 `True`），随后保留第 `j` 个字符 `s[j]`，再接上 `best[j+1]`。  
   - 所有合法的 `j`（`i ≤ j < n`）都可以尝试，取字典序最小者。  

   形式化：

   ```
   best[n] = ""                                   # 空串的答案
   best[i] = min( s[j] + best[j+1]                # 选第 j 个字符留下
                  for j in range(i, n)
                  if rem[i][j-1] )               # 前缀 i..j-1 必须能全删
   ```

   这里的 `rem[i][j-1]` 当 `j == i` 时对应空前缀，始终为 `True`，相当于可以直接保留 `s[i]`。

   该递推只需要 `O(n²)` 次比较，每次字符串拼接最多 `O(n)`，整体仍是 `O(n³)`。

> **类比**：把 “能删掉的子串” 看成 **可通行的桥**，我们从左到右走，每次可以跨过一段桥（删掉），然后在桥的另一端选一个字母继续前进。我们要选的路径，使得走出来的字母序列最早（字典序最小）。

#### 代码（Python）

```python
def is_consecutive(a: str, b: str) -> bool:
    """环形相邻判定：a 与 b 在字母表中相差 1（正向）"""
    return (ord(b) - ord(a)) % 26 == 1


def smallest_string(s: str) -> str:
    n = len(s)

    # ---------- 1. 子串可删性 DP ----------
    # rem[l][r] = True 表示 s[l..r] 能全部消除
    rem = [[False] * n for _ in range(n)]

    # 空串（l > r）在查询时直接视为 True，下面的循环只处理 l <= r
    for length in range(2, n + 1):          # 只可能出现偶数长度的可删子串
        for l in range(0, n - length + 1):
            r = l + length - 1
            # 尝试让 s[l] 与某个 s[k] 配对删掉
            for k in range(l + 1, r + 1):
                if is_consecutive(s[l], s[k]):
                    # 中间部分 l+1..k-1 必须全删，右侧 k+1..r 必须全删
                    left_ok = (k == l + 1) or rem[l + 1][k - 1]
                    right_ok = (k == r) or rem[k + 1][r]
                    if left_ok and right_ok:
                        rem[l][r] = True
                        break               # 已经找到一种删法即可

    # ---------- 2. 构造字典序最小的答案 ----------
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def best(i: int) -> str:
        """返回从位置 i 开始可以得到的字典序最小字符串"""
        if i == n:
            return ""                     # 已经走到末尾

        candidates = []                   # 所有可能的“保留字符 + 之后的答案”
        for j in range(i, n):
            # 判断前缀 s[i..j-1] 是否可以全部删掉
            if j == i or rem[i][j - 1]:
                # 选 s[j] 留下，再接上从 j+1 开始的最优解
                cand = s[j] + best(j + 1)
                candidates.append(cand)

        # 取字典序最小的那个
        return min(candidates)

    return best(0)


# ---------- 示例 ----------
print(smallest_string("abc"))   # -> "a"
print(smallest_string("bcda"))  # -> ""
print(smallest_string("zdce"))  # -> "zdce"
```

**关键注释**  

- `rem` 的三层循环实现了 “先删掉中间，再让两端配对” 的递推。  
- `length` 只从 2 开始，因为单个字符不可能自行消除。  
- `best` 使用 **记忆化递归**（`lru_cache`）避免重复计算子问题。  
- `candidates` 中的每一个元素都是 “把 `s[j]` 当成本段的第一个保留字符 + 后面最优解”。  
- 当 `j == i` 时 `rem[i][j-1]` 对应空前缀，等价于 **直接保留** `s[i]`。

#### 复杂度

- **时间复杂度**：  
  - 子串可删性 DP：`O(n³)`（三层循环）  
  - 构造答案 DP：`O(n²)`（每个 `i` 枚举 `j`，字符串拼接最多 `O(n)`）  
  - 综合为 **`O(n³)`**，对 `n ≤ 250` 完全可跑在毫秒级。  
  - 与暴力的指数级 `O(2^{n/2})` 相比，提升非常明显。

- **空间复杂度**：  
  - `rem` 表占 `O(n²)`（约 250² ≈ 62 500 布尔），  
  - 记忆化 `best` 需要 `O(n)`，  
  - 合计 **`O(n²)`**，远低于递归栈的指数级开销。

---

## 心得

- **核心技巧**：先用 DP 判定哪些子串可以**全部删除**，再在此基础上用「从左到右挑最小字符」的 DP 构造最小字典序。  
- **适用的题型**  
  1. “删除相邻满足条件的字符后，求最优结果”——例如 *Remove Boxes*、*Remove All Adjacent Duplicates in String*。  
  2. “先判定可消除子结构，再在其上做最优子序列/子串 DP”——如 *Burst Balloons*、*Palindrome Partitioning*（先判断子串是否是回文）。  
- **一句话总结解题钥匙**：**把“能否全部消除”抽象成布尔 DP，随后在合法的“删除区间”之间挑选最早的字符即可得到字典序最小的字符串。**

---

## 反思

- **第一反应**：直接递归枚举所有删除顺序（暴力），因为想到的都是“把每一步都尝试”。  
- **最容易踩的坑**  
  - **环形相邻判定**：忘记 `a` 与 `z` 也是相邻，需要使用模 26。  
  - **子串全删判定的递推**：容易写成只考虑 `s[l]` 与 `s[l+1]` 配对，实际上中间的子串也可能先被删掉后才配对。  
  - **空前缀的处理**：在构造答案时 `rem[i][j-1]` 当 `j == i` 时应该视为 `True`，否则会误把“直接保留第 i 个字符”排除掉。  
- **下次类似题目**：第一步先问自己  
  1. “有没有可以提前预处理的‘子结构可否消除/成立’的布尔表？”  
  2. “在此布尔表的约束下，我该如何挑选/组合剩余元素以获得最优（最小/最大）目标？”  

这样就能迅速从暴力枚举跳到结构化的动态规划。