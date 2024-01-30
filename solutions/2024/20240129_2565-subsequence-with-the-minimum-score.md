# #2565. 最小得分的子序列 / Subsequence With the Minimum Score

> 难度：困难 · 标签：Two Pointers、String、Binary Search · [LeetCode 链接](https://leetcode.com/problems/subsequence-with-the-minimum-score/)

---

## 题目（英文原版）

**Description**

You are given two strings s and t.
You are allowed to remove any number of characters from the string t.
The score of the string is 0 if no characters are removed from the string t, otherwise:
Then the score of the string is right - left + 1.
Return the minimum possible score to make t a subsequence of s.
A subsequence of a string is a new string that is formed from the original string by deleting some (can be none) of the characters without disturbing the relative positions of the remaining characters. (i.e., "ace" is a subsequence of "abcde" while "aec" is not).

**Examples**

**Example 1:**

```
Input: s = "abacaba", t = "bzaa"
Output: 1
Explanation: In this example, we remove the character "z" at index 1 (0-indexed).
The string t becomes "baa" which is a subsequence of the string "abacaba" and the score is 1 - 1 + 1 = 1.
It can be proven that 1 is the minimum score that we can achieve.
```

**Example 2:**

```
Input: s = "cde", t = "xyz"
Output: 3
Explanation: In this example, we remove characters "x", "y" and "z" at indices 0, 1, and 2 (0-indexed).
The string t becomes "" which is a subsequence of the string "cde" and the score is 2 - 0 + 1 = 3.
It can be proven that 3 is the minimum score that we can achieve.
```

**Constraints**

- 1 <= s.length, t.length <= 105
- s and t consist of only lowercase English letters.

---

## 题目（中文翻译）

给定两个字符串 `s` 和 `t`。  
你可以从字符串 `t` 中删除任意个字符（可以为零）。  

- 如果没有删除任何字符，则得分为 `0`；  
- 否则，得分等于 `right - left + 1`（其中 `left` 为删除后子序列在 `t` 中的最左下标，`right` 为最右下标）。  

返回使得 `t` 成为 `s` 的子序列（subsequence）时可能的最小得分。  

**子序列（subsequence）** 是指在不改变剩余字符相对顺序的前提下，从原字符串中删除若干（可以为零）字符后得到的新字符串。  
例如 `"ace"` 是 `"abcde"` 的子序列，而 `"aec"` 不是。

---

### 示例

#### 示例 1
**输入**  
``` 
s = "abacaba", t = "bzaa"
```  
**输出**  
```
1
```  
**解释**  
在此示例中，我们删除下标为 `1`（0‑基）的字符 `"z"`。  
删除后 `t` 变为 `"baa"`，它是 `s` 的子序列，得分为 `1 - 1 + 1 = 1`。  
可以证明 `1` 是能够达到的最小得分。

#### 示例 2
**输入**  
``` 
s = "cde", t = "xyz"
```  
**输出**  
```
3
```  
**解释**  
在此示例中，我们分别删除下标为 `0、1、2`（0‑基）的字符 `"x"、"y"、"z"`。  
删除后 `t` 变为空串 `""`，它是 `s` 的子序列，得分为 `2 - 0 + 1 = 3`。  
可以证明 `3` 是能够达到的最小得分。

---

### 约束条件
- `1 <= s.length, t.length <= 10^5`
- `s` 和 `t` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**枚举**在 `t` 中要删掉的字符集合，然后判断删掉后剩下的字符串是否是 `s` 的子序列，最后取最小的得分。

- **枚举**  
  把 `t` 看成一排字符，我们可以决定每个字符是“保留”还是“删除”。如果把 `t` 长度记作 `n`，那么所有可能的删除方式有 `2ⁿ` 种（每个字符两种选择），这已经是指数级的搜索，根本不可行。

- **子序列判断**  
  给定一个已经删减好的 `t'`，判断它是否是 `s` 的子序列，只需要一次线性扫描：用指针 `i` 在 `s` 上走，指针 `j` 在 `t'` 上走，遇到相同字符就把 `j` 往后移，最后看 `j` 是否走完全部字符。这个过程相当于在 **字典** 中查找词的过程——`s` 就像一本书，`t'` 是要找的词，顺序必须保持不变。

- **得分计算**  
  如果没有删除字符，得分是 `0`。否则得分是 `right - left + 1`，其中 `left`、`right` 是被删字符在原 `t` 中的最左、最右下标。直观上这就是“删掉的连续区间长度”。

**为什么暴力法能得到正确答案？**  
因为我们遍历了所有可能的删除方式，必然会覆盖最优的那一种。只要子序列判断写对了，答案就一定在遍历得到的得分集合里。

**时间/空间复杂度**  
- 枚举所有删除方式需要 `O(2ⁿ)`（指数级），即使子序列检查是 `O(|s|+|t|)`，整体仍然是指数时间，根本跑不完。  
- 空间只用了几个指针，`O(1)`。

> **大白话**：`O(2ⁿ)` 可以想象成把 `t` 每个字符都投硬币，正面保留、反面删除，所有可能的硬币组合数就是答案的搜索空间。即使我们每次检查都很快，枚举的次数也多得离谱。

#### 代码（Python）

```python
# 暴力解（仅作思路演示，实际会超时）
from itertools import product

def min_score_bruteforce(s: str, t: str) -> int:
    n = len(t)
    best = float('inf')
    # 0/1 序列表示每个字符是否删除（1 删除，0 保留）
    for mask in product([0, 1], repeat=n):
        # 计算删除区间的左、右端点
        del_idxs = [i for i, bit in enumerate(mask) if bit == 1]
        if not del_idxs:               # 没有删除
            score = 0
        else:
            left, right = del_idxs[0], del_idxs[-1]
            score = right - left + 1

        # 构造删除后的 t'
        t_prime = ''.join(ch for ch, bit in zip(t, mask) if bit == 0)

        # 判断 t' 是否是 s 的子序列
        i = j = 0
        while i < len(s) and j < len(t_prime):
            if s[i] == t_prime[j]:
                j += 1
            i += 1
        if j == len(t_prime):          # 匹配成功
            best = min(best, score)
    return best
```

> **注意**：上面的代码只能在 `t` 很短（比如 `len(t) ≤ 15`）时跑得完，主要是帮助大家理解最直接的思路。

#### 复杂度

- **时间复杂度**：`O(2ⁿ * (|s| + |t|))` ——指数级的遍历让它根本不可用。  
  *含义*：如果 `t` 长度是 20，2ⁿ 就是 1,048,576，乘上 `|s|+|t|`（可能是 10⁵）就已经是 10¹¹ 次操作，远超计算机的承受范围。

- **空间复杂度**：`O(1)` ——只用了常数个变量。

---

### 2. 最优解

#### 思路  

从暴力解我们看到，**枚举所有删除区间**是最慢的环节。其实我们只需要关注 **删除的连续子串**（因为得分只和最左、最右删除位置有关），而不是任意散开的字符集合。于是可以把问题转化为：

> 在 `t` 中挑选一个 **连续的子串** `t[l…r]`（可以为空），把它全部删掉，使得剩下的 `t[0…l‑1] + t[r+1…n‑1]` 成为 `s` 的子序列，求最小的 `r‑l+1`（如果不删字符则记作 0）。

**关键观察 1：前缀匹配 & 后缀匹配**  
- 对于 `t` 的每一个前缀 `t[0…i]`，我们可以记录在 `s` 中最早能匹配完这个前缀的位置，记作 `left[i]`（下标从 `0` 开始）。如果前缀根本匹配不到，`left[i] = INF`。  
  这相当于把 `s` 当成一本书，**从左往右**找每个字母第一次出现的位置——就像在字典里查“首次出现页码”。

- 同理，对于 `t` 的每一个后缀 `t[j…n‑1]`，我们记录在 `s` 中最晚能匹配完这个后缀的位置，记作 `right[j]`（从右往左扫描）。如果后缀匹配不到，`right[j] = -INF`。

只需要一次线性扫描就能得到这两个数组：

| 步骤 | 操作 |
|------|------|
| **左侧** | 从 `s` 开始，用指针 `p` 在 `t` 上向前推进；每当 `s[i] == t[p]`，记录 `left[p] = i`，然后 `p++`。 |
| **右侧** | 从 `s` 末尾开始，用指针 `p` 在 `t` 上向后推进；每当 `s[i] == t[p]`，记录 `right[p] = i`，然后 `p--`。 |

**关键观察 2：利用单调性做双指针/二分**  
现在我们已经知道：
- 前缀 `t[0…i]` 必须在 `s` 的位置 `≤ left[i]` 结束；
- 后缀 `t[j…n‑1]` 必须在 `s` 的位置 `≥ right[j]` 开始。

只要 **`left[i] < right[j]`**（左边的匹配结束位置在右边的匹配开始位置左侧），就说明把中间的 `t[i+1 … j‑1]` 全部删掉后，剩余两段能够顺序出现在 `s` 中，构成子序列。

于是问题变成：**在所有满足 `left[i] < right[j]` 的 `(i, j)` 中，最小化 `j - i - 1`（即被删区间长度）**。

这一步可以用 **双指针** 完成：
- 固定左指针 `i`（从 `-1` 开始，表示前缀为空），右指针 `j` 从 `0` 开始向右移动，保持 `right[j] > left[i]`。因为 `right` 是 **递减**（从右往左填的），只要 `j` 增大，`right[j]` 会逐渐变小，不会重新满足条件，所以可以一次遍历完成。

也可以用 **二分搜索**：对每个 `i` 在 `right` 中寻找第一个满足 `right[j] > left[i]` 的 `j`（因为 `right` 本身是单调递增的，从左到右看其实是递增的），时间 `O(log n)`，整体 `O(n log n)`。双指针更简洁，时间 `O(n)`。

**完整步骤**：

1. 计算 `left`（长度 `n`，`left[i]` 为匹配 `t[:i+1]` 在 `s` 中的最早结束位置）。若匹配不到，设为 `INF`。
2. 计算 `right`（长度 `n`，`right[i]` 为匹配 `t[i:]` 在 `s` 中的最晚开始位置）。若匹配不到，设为 `-INF`。
3. 初始化答案 `ans = n`（全部删掉的情况）。
4. 用双指针遍历：
   - `i` 从 `-1` 到 `n-1`（`i=-1` 表示不保留左侧任何字符，`left[-1]` 设为 `-1`）。
   - 移动 `j`（从 `0` 开始）使得 `j < n` 且 `right[j] <= left[i]` 时继续右移，直到 `right[j] > left[i]` 或 `j == n`。
   - 此时删除区间长度为 `j - i - 1`（如果 `j == n`，表示右侧全部删掉，长度为 `n - i - 1`）。
   - 更新 `ans = min(ans, j - i - 1)`。
5. 返回 `ans`。

**为什么是最优的？**  
- 前缀/后缀匹配只遍历一次 `s` 与 `t`，得到最早/最晚位置，确保任何合法删除区间都能在这两个数组里找到对应的 `i、j`。  
- 双指针只前进不回退，整体线性时间 `O(|s| + |t|)`，没有多余的枚举。  
- 空间只用两个长度为 `n` 的数组，`O(|t|)`。

#### 代码（Python）

```python
def minimumScore(s: str, t: str) -> int:
    n = len(t)
    m = len(s)

    # 1. left[i]：匹配 t[0..i] 在 s 中的最早结束位置
    left = [m] * n               # m 相当于 INF（超出 s 的下标）
    p = 0                         # t 的指针
    for i, ch in enumerate(s):
        if p < n and ch == t[p]:
            left[p] = i           # 第 p 个字符匹配成功，记录位置
            p += 1
            if p == n:            # 已经匹配完整个 t，后面不需要再记录
                break

    # 2. right[i]：匹配 t[i..n-1] 在 s 中的最晚开始位置
    right = [-1] * n              # -1 相当于 -INF
    p = n - 1                      # 从 t 末尾往前匹配
    for i in range(m - 1, -1, -1):
        if p >= 0 and s[i] == t[p]:
            right[p] = i           # 第 p 个字符匹配成功，记录位置
            p -= 1
            if p < 0:              # 已经匹配完整个 t
                break

    # 3. 双指针遍历找最小删除长度
    ans = n                       # 最坏情况：全部删掉
    j = 0                         # 右指针，表示后缀的起始下标
    # 为了统一处理“左侧为空”的情况，设 left[-1] = -1
    left_minus_one = -1

    for i in range(-1, n):        # i = -1 表示不保留任何左侧字符
        left_pos = left_minus_one if i == -1 else left[i]

        # 移动 j 直到右侧匹配位置严格大于左侧结束位置
        while j < n and right[j] <= left_pos:
            j += 1
        # 此时要删除的区间是 (i, j) 之间的字符，长度为 j - i - 1
        ans = min(ans, j - i - 1)

    return ans
```

**代码要点解释**  

- `left` 与 `right` 初始化为极端值，方便后面比较（相当于“找不到”时的哨兵）。  
- `left_minus_one = -1` 用来处理“左边不取任何字符”的特殊情况，这样 `left_pos` 在 `i = -1` 时等于 `-1`，保证 `right[0] > -1` 时可以直接得到答案。  
- 双指针的 `while` 循环只会让 `j` 单调递增，整个外层循环 `i` 也单调递增，所以时间是线性的。

#### 复杂度

- **时间复杂度**：`O(|s| + |t|)`  
  *含义*：我们只遍历了两遍字符串（一次正向一次逆向）以及一次线性遍历 `t` 的下标，整体操作次数与输入长度成正比。即使 `s`、`t` 长度都是 10⁵，也只需要几百毫秒即可完成。

- **空间复杂度**：`O(|t|)`  
  *含义*：除了输入本身，我们额外用了两个长度为 `n`（即 `t` 长度）的数组 `left`、`right`，再加几个常数级变量。存储量随 `t` 长度线性增长。

---

## 心得

- **核心技巧**：利用**前缀最早匹配位置**和**后缀最晚匹配位置**的单调性，把“删除任意子串”的问题转化为在两个单调数组上寻找满足不交条件的最小间隔。  
- **适用的题型**  
  1. **删除子串后使得另一个字符串成为子序列**（本题）。  
  2. **在两个字符串中寻找最长公共子序列的“分割点”**（如 LeetCode 1850 “Minimum Adjacent Swaps to Reach the Kth Smallest Number” 的思路）。  
  3. **删除最少字符使得字符串满足某种前后约束**（如“删除子数组使得剩余数组严格递增”）。
- **一句话总结**：**先把左侧最早匹配、右侧最晚匹配算出来，再用单调性快速找最短可删区间**。

---

## 反思

- **第一反应**：看到“删除任意字符，得分是删除区间长度”，第一时间想到了“枚举所有删除方式”。这是一种直觉的暴力思路，却忽视了输入规模（10⁵）导致不可行。
- **最容易踩的坑**  
  - **边界处理**：左侧或右侧可以全部为空，需要在代码中用 `i = -1` 或 `j = n` 的哨兵处理。  
  - **匹配不到的情况**：若某个前缀（或后缀）在 `s` 中根本匹配不到，`left[i]`（或 `right[i]`）必须设为极端值，否则后续比较会误判。  
  - **下标混淆**：`left[i]` 表示匹配到 `t[i]` 时 **结束** 的位置，而 `right[i]` 表示匹配到 `t[i]` 时 **开始** 的位置，二者的意义相反，需要清晰区分。
- **下次遇到同类题**：第一步先思考 **“把问题拆成左侧/右侧两段，各自最早/最晚能匹配到哪里”**，利用单调性或双指针把枚举空间压到线性。这样可以快速定位最优解的搜索范围，避免暴力枚举的陷阱。