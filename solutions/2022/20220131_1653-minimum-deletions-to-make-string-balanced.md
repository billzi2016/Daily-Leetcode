# #1653. 使字符串平衡的最少删除次数 / Minimum Deletions to Make String Balanced

> 难度：中等 · 标签：String、Dynamic Programming、Stack · [LeetCode 链接](https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting only of characters 'a' and 'b'​​​​.
You can delete any number of characters in s to make s balanced. s is balanced if there is no pair of indices (i,j) such that i < j and s[i] = 'b' and s[j]= 'a'.
Return the minimum number of deletions needed to make s balanced.

**Examples**

**Example 1:**

```
Input: s = "aababbab"
Output: 2
Explanation: You can either:
Delete the characters at 0-indexed positions 2 and 6 ("aababbab" -> "aaabbb"), or
Delete the characters at 0-indexed positions 3 and 6 ("aababbab" -> "aabbbb").
```

**Example 2:**

```
Input: s = "bbaaaaabb"
Output: 2
Explanation: The only solution is to delete the first two characters.
```

**Constraints**

- 1 <= s.length <= 105
- s[i] is 'a' or 'b'​​.

---

## 题目（中文翻译）

给定一个仅由字符 `'a'` 和 `'b'` 组成的字符串 `s`。你可以删除 `s` 中任意数量的字符，使得 `s` **平衡**。若不存在满足 `i < j` 且 `s[i] = 'b'` 且 `s[j] = 'a'` 的索引对 `(i, j)`，则称 `s` 为平衡的。返回使 `s` 平衡所需的最少删除次数。

## 示例 1

**输入**  
``` 
s = "aababbab"
``` 

**输出**  
```
2
``` 

**解释**  
你可以选择以下两种方式之一：

- 删除下标为 `2` 和 `6` 的字符，使 `"aababbab"` 变为 `"aaabbb"`；  
- 删除下标为 `3` 和 `6` 的字符，使 `"aababbab"` 变为 `"aabbbb"`。

## 示例 2

**输入**  
``` 
s = "bbaaaaabb"
``` 

**输出**  
```
2
``` 

**解释**  
唯一的解法是删除前两个字符。

## 约束条件

- `1 <= s.length <= 10^5`
- `s[i]` 只能是 `'a'` 或 `'b'`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的删除方式**，然后检查删完以后字符串是否满足“平衡”。  
- **平衡的定义**：不存在下标 `i < j` 使得 `s[i] = 'b'` 且 `s[j] = 'a'`。也就是说所有的 `'a'` 必须出现在所有 `'b'` 之前，或者说字符串形如 `"aaa...bbb..."`（可以全是 `'a'` 或全是 `'b'`）。
- **暴力做法**：把字符串的每一个字符都标记为“保留”或“删除”，这相当于遍历所有的子集。对于每一种子集，把保留下来的字符拼成新串，检查它是否已经平衡，记录需要删除的字符数的最小值。

生活化类比：这就像你手里有一串珠子（只分红珠子和蓝珠子），想把它整理成“所有红珠子在前，蓝珠子在后”。暴力方法就是把每颗珠子都尝试一次“留下”或“丢掉”，然后看看整理后的顺序是否符合要求。

**为什么正确**：因为我们遍历了**所有**可能的删除组合，必然会覆盖最优的那一种，所以最终得到的最小删除数一定是答案。

#### 代码（Python）

```python
def minDeletion_bruteforce(s: str) -> int:
    n = len(s)
    best = n                     # 最坏情况：全部删掉

    # 用二进制数的每一位表示第 i 位字符是保留(1)还是删除(0)
    for mask in range(1 << n):   # 2^n 种可能，n<=10时还能接受
        kept = []                # 保存未被删除的字符
        deletions = 0
        for i in range(n):
            if mask >> i & 1:    # 第 i 位保留
                kept.append(s[i])
            else:
                deletions += 1   # 删除计数
        # 检查 kept 是否平衡：所有的 'a' 必须在所有的 'b' 前面
        ok = True
        seen_b = False
        for ch in kept:
            if ch == 'b':
                seen_b = True
            elif seen_b:          # 出现了 b 之后又出现 a，违规
                ok = False
                break
        if ok:
            best = min(best, deletions)

    return best
```

> **注意**：上述实现只能在 `len(s) ≤ 20` 左右的极小规模下跑得完，因为时间随 `2^n` 指数增长。它仅用于说明“最直接的想法”。

#### 复杂度

- **时间复杂度**：`O(2^n * n)`  
  解释：我们要遍历 `2^n` 种删除方案，每种方案要遍历一次字符串（`n` 步）来判断平衡与统计删除数。指数级的时间在实际数据（`n` 可达 10⁵）时根本不可接受。
- **空间复杂度**：`O(n)`  
  解释：主要是保存 `kept` 列表的空间，最多保存全部字符。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**关键在于找出一种删除方式，使得所有 `'a'` 都在 `'b'` 之前**。我们不必真的去枚举删除哪些字符，只要**统计**在某个位置左边保留多少 `'b'`、右边保留多少 `'a'`，就能直接算出需要删除的最小数量。

**一步步推导**：

1. **把问题转化为“分割点”**  
   想象在字符串的每个可能位置（包括最左侧、最右侧）插入一个“分割线”。左边的字符全部保留 `'b'`，右边的字符全部保留 `'a'`，这样必然平衡。  
   对于某个分割点 `i`（`0 ≤ i ≤ n`），我们需要：
   - 删除左边所有的 `'a'`（因为左边只能出现 `'b'`）；
   - 删除右边所有的 `'b'`（因为右边只能出现 `'a'`）。

   删除的总数 = **左边的 `'a'` 数** + **右边的 `'b'` 数**。

2. **前缀计数 + 后缀计数**  
   - `preA[i]`：下标 `< i`（左侧）出现的 `'a'` 的个数。可以在一次遍历中累计得到。  
   - `sufB[i]`：下标 `≥ i`（右侧）出现的 `'b'` 的个数。同样一次逆序遍历即可得到。

   那么在分割点 `i` 处的删除数 = `preA[i] + sufB[i]`。只要遍历所有 `i`，取最小值即可。

3. **一步完成**  
   事实上我们不需要同时保存两个数组，只需要在一次遍历中维护“左边的 `'a'` 数”，在另一次遍历中预先算好“右边的 `'b'` 数”。这使得时间 `O(n)`，空间 `O(1)`（只用几个计数器）。

**核心数据结构**：**前缀计数**（prefix sum）和**后缀计数**（suffix sum）。它们像一本字典的“累计页码”，可以在 O(1) 时间得到任意区间的字符数量。

#### 代码（Python）

```python
def minDeletion(s: str) -> int:
    n = len(s)

    # 1️⃣ 先算出每个位置 i 右侧（包括 i）有多少个 'b'
    # sufB[i] = number of 'b' in s[i:]
    sufB = [0] * (n + 1)          # 多一个哨兵，sufB[n] = 0（空串右侧没有 b）
    for i in range(n - 1, -1, -1):
        sufB[i] = sufB[i + 1] + (1 if s[i] == 'b' else 0)

    # 2️⃣ 再遍历一次，从左到右维护左侧出现的 'a' 的数量
    leftA = 0                     # 左边已看到的 'a' 个数（需要删除）
    ans = n                       # 最坏情况全部删除
    for i in range(n + 1):
        # 当前位置 i 作为分割点，删除数 = leftA (左侧的 a) + sufB[i] (右侧的 b)
        ans = min(ans, leftA + sufB[i])

        # 如果下一个字符是 'a'，左侧的 a 计数要加一（因为分割点会右移一位）
        if i < n and s[i] == 'a':
            leftA += 1

    return ans
```

**代码解释（逐行注释）**：

| 行号 | 代码 | 中文注释 |
|------|------|----------|
| 1 | `def minDeletion(s: str) -> int:` | 定义函数，输入只含 `'a'`、`'b'` 的字符串 |
| 2 | `n = len(s)` | 记录字符串长度 |
| 5 | `sufB = [0] * (n + 1)` | 创建后缀数组，`sufB[i]` 表示从 `i` 开始到结尾的 `'b'` 个数 |
| 6‑8 | `for i in range(n - 1, -1, -1): ...` | 逆序遍历，累计 `'b'` 的数量 |
| 7 | `sufB[i] = sufB[i + 1] + (1 if s[i] == 'b' else 0)` | 如果当前位置是 `'b'`，在后缀计数上加一 |
| 11 | `leftA = 0` | 左侧已经出现的 `'a'` 数（需要删除） |
| 12 | `ans = n` | 初始答案设为最坏情况——全部删除 |
| 13‑15 | `for i in range(n + 1): ...` | 遍历所有可能的分割点（包括最左侧 `0` 和最右侧 `n`） |
| 14 | `ans = min(ans, leftA + sufB[i])` | 当前分割点需要删除的字符数 = 左侧 `a` + 右侧 `b` |
| 17‑18 | `if i < n and s[i] == 'a': leftA += 1` | 分割点右移一步后，如果新进入左侧的是 `'a'`，计数加一 |
| 20 | `return ans` | 返回最小删除次数 |

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：我们只遍历字符串两遍（一次逆序算 `sufB`，一次正序算答案），每一步都是常数时间操作。即使 `n = 10⁵` 也毫无压力。

- **空间复杂度**：`O(n)`（如果使用 `sufB` 数组）或 `O(1)`（可以在遍历时直接累加右侧的 `'b'`，但写法会稍微复杂）。这里保留 `sufB` 只为了代码直观，额外使用的空间与字符串长度成正比，最多约 400KB，完全可接受。

---

## 心得

- **核心技巧**：把“删除使字符串平衡”转化为“在某个分割点左侧只保留 `'b'`、右侧只保留 `'a'`”，随后利用前缀/后缀计数求最小删除数。  
- **该技巧适用的题型**：
  1. **最小删除/插入使字符串满足某种单调关系**（如 `"minimum deletions to make string monotone increasing"`）。  
  2. **分割点 DP**，比如把数组分成两段分别满足不同条件的最小代价问题。  
  3. **前缀和/后缀和求最优分割**，常见于 “把数组划分为两段，使左段满足 X，右段满足 Y” 类题目。
- **一句话总结解题钥匙**：**把全局约束转化为“左/右两段独立约束”，再用前缀/后缀计数一次遍历求最小代价**。

---

## 反思

- **第一反应**：看到“没有 `b` 在 `a` 前面”就想到“所有 `a` 必须排在所有 `b` 前”，于是自然联想到“把字符串变成 `aaa…bbb…` 的形式”。  
- **最容易踩的坑**：
  1. **忘记考虑分割点在最左侧或最右侧的情况**（即全部删掉或全部保留一种字符），导致答案偏大。  
  2. **边界计数错误**：后缀数组 `sufB[i]` 必须表示从 `i` 开始（包括 `i`）的 `'b'` 数，否则在分割点恰好在字符 `i` 前后会多减或少算一次。  
  3. **把前缀计数写成 `leftA += (s[i] == 'a')` 时忘记在循环末尾更新**，导致左侧计数提前或滞后。  
- **下次遇到同类题**：第一步先**思考是否可以把约束转化为“左边满足 X、右边满足 Y”的形式**，然后**利用前缀/后缀累计**快速求最优分割点。这样往往能把指数级的暴力降到线性时间。