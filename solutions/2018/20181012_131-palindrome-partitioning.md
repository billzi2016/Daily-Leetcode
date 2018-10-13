# #131. 回文划分 / Palindrome Partitioning

> 难度：中等 · 标签：String、Dynamic Programming、Backtracking · [LeetCode 链接](https://leetcode.com/problems/palindrome-partitioning/)

---

## 题目（英文原版）

**Description**

Given a string s, partition s such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of s.

**Examples**

**Example 1:**

```
Input: s = "aab"
Output: [["a","a","b"],["aa","b"]]
```

**Example 2:**

```
Input: s = "a"
Output: [["a"]]
```

**Constraints**

- 1 <= s.length <= 16
- s contains only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，对 `s` 进行划分（partition），要求划分得到的每个子串（substring）都是回文（palindrome）。返回 `s` 所有可能的回文划分方案。

**示例 1**  
**输入**: `s = "aab"`  
**输出**: `[["a","a","b"],["aa","b"]]`

**示例 2**  
**输入**: `s = "a"`  
**输出**: `[["a"]]`

**约束条件**

- `1 <= s.length <= 16`
- `s` 仅包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把字符串的每一种切分方式都枚举出来**，然后把切出来的每段子串检查一下是否是回文（正着读和倒着读一样的串）。  

- **枚举切分**：可以把切分看成在字符之间放“|”。例如 `"aab"` 有两两个字符间隙，`a|a|b`、`aa|b`、`a|ab`… 只要把每个间隙决定要不要切，就能得到所有可能的分割。  
- **回文检查**：把子串当成一本小字典，正着读和倒着读要得到同一个词。这里的“哈希表”类比不需要，用最简单的双指针从两端向中间比较即可。  

为什么能得到全部答案？因为每一种“切或不切”的决定对应唯一一种分割，遍历所有决定自然遍历所有分割；而只保留所有子串都是回文的分割，就是题目要求的答案。

#### 代码（Python）

```python
def partition(s: str):
    res = []                     # 最终答案列表

    # ---------- 判断子串是否是回文 ----------
    def is_palindrome(sub: str) -> bool:
        left, right = 0, len(sub) - 1
        while left < right:
            if sub[left] != sub[right]:
                return False     # 不相等直接否定
            left += 1
            right -= 1
        return True              # 全部匹配才是回文

    # ---------- 回溯枚举所有切分 ----------
    def backtrack(start: int, path: list):
        """
        start : 当前要处理的起始下标
        path  : 已经选好的回文子串（从 0 到 start-1 的划分）
        """
        if start == len(s):      # 已经走到字符串末尾，得到一个完整划分
            res.append(path[:])  # 复制一份加入答案
            return

        # 从 start 开始往后尝试每一种可能的子串
        for end in range(start, len(s)):
            cur = s[start:end + 1]          # 取出 s[start..end]（闭区间）
            if is_palindrome(cur):          # 只在是回文时继续向下搜索
                path.append(cur)            # 选这个子串
                backtrack(end + 1, path)    # 递归处理剩余部分
                path.pop()                  # 撤销选择，尝试下一个 end

    backtrack(0, [])
    return res
```

#### 复杂度  

- **时间复杂度：**`O(n * 2^n)`  
  - `2^n` 来自所有切分方式的数量（每个间隙有切或不切两种选择）。  
  - 对每一种切分，我们会检查每个子串是否回文，最坏情况每次检查需要 `O(n)`（子串长度最多 `n`），所以整体是 `O(n * 2^n)`。  
  - 用大白话说，就是“随着字符串长度稍微长一点，可能的答案会指数级暴涨”。  

- **空间复杂度：**`O(n)`（递归栈） + `O(k)`（答案存储），其中 `k` 为所有合法划分的总字符数。递归栈的深度不会超过 `n`，因为每次都把至少一个字符放进 `path`。  



---  

### 2. 最优解

#### 思路  

从暴力解可以看到两大瓶颈：

1. **回文检查重复**  
   在回溯的过程中，同一个子串会被检查多次。例如 `"aab"` 中的 `"a"` 会在不同的递归层反复判断。  
2. **枚举子串的方式仍是指数级**，这本身是不可避免的，因为答案的数量本身就是指数级的。但我们可以把**每次判断是否回文的代价降到 O(1)**，从而让整体常数更小。

**优化手段——预处理回文表（DP）**  

- 建立一个二维布尔数组 `pal[i][j]`，表示子串 `s[i..j]` 是否是回文。  
- 递推公式：  
  - `pal[i][i] = True`（长度为 1 的子串一定是回文）  
  - `pal[i][i+1] = (s[i] == s[i+1])`（长度为 2 时，只要两个字符相同）  
  - 对于长度 ≥ 3：`pal[i][j] = (s[i] == s[j]) and pal[i+1][j-1]`  
- 只需要一次 `O(n^2)` 的遍历就能填完整个表。之后在回溯时，只要查询 `pal[start][end]` 就能瞬间知道子串是否回文，省掉每次的双指针比较。

**整体思路**  

1. **先跑 DP，得到所有子串的回文信息**（一次性 O(n²)）。  
2. **再用和暴力解相同的回溯框架**，唯一的区别是判断回文时直接查表 `pal[start][end]`（O(1)）。  
3. 这样每条递归路径只做 `O(n)` 次“切或不切”的决定，整体时间降到 `O(n * 2^n)`（与暴力的渐进相同，但常数更小），而额外的 DP 只加了 `O(n²)` 的预处理时间和空间。

#### 代码（Python）

```python
def partition(s: str):
    n = len(s)
    res = []

    # ---------- 预处理所有子串是否是回文 ----------
    pal = [[False] * n for _ in range(n)]   # pal[i][j] 表示 s[i..j] 是否回文

    for i in range(n - 1, -1, -1):           # i 从后往前，这样子问题 pal[i+1][j-1] 已经算好
        pal[i][i] = True                     # 单字符必回文
        for j in range(i + 1, n):
            if s[i] == s[j]:
                if j - i == 1:               # 长度为 2 的子串
                    pal[i][j] = True
                else:
                    pal[i][j] = pal[i + 1][j - 1]   # 参考内部子串的回文结果
            # else 默认 False

    # ---------- 回溯枚举 ----------
    def backtrack(start: int, path: list):
        if start == n:
            res.append(path[:])
            return
        for end in range(start, n):
            if pal[start][end]:               # O(1) 判断回文
                path.append(s[start:end + 1])
                backtrack(end + 1, path)
                path.pop()

    backtrack(0, [])
    return res
```

#### 复杂度  

- **时间复杂度：**`O(n² + n * 2^n)`  
  - `O(n²)` 用来构造回文表。  
  - 回溯本身仍然需要遍历所有合法切分，数量上界仍是 `2^n`，每条路径最多做 `n` 次“查表”操作，故为 `O(n * 2^n)`。  
  - 与暴力解相比，**常数大幅下降**（不再进行每次 O(n) 的回文检查），在实际运行中会快很多。  

- **空间复杂度：**`O(n²)`（回文表） + `O(n)`（递归栈）+ `O(k)`（答案），其中 `n²` 是主要开销。对 `n ≤ 16` 完全可接受。  



## 心得

- **核心技巧**：**回文子串的预处理 + 回溯**。先用动态规划把所有子串的回文信息记下来，再在回溯过程中 O(1) 判断，避免重复计算。  
- **适用题型**：  
  1. “所有划分满足某种局部约束”的题目（如 “Word Break II”）。  
  2. “在字符串上枚举子结构且需要频繁判断子结构属性”的题目（如 “Palindrome Substrings”）。  
- **解题钥匙**：**先把“判断是否满足条件”这一步变成常数时间，再去枚举**。  

## 反思

- **第一反应**：直接写回溯，遇到回文检查时想到用双指针判断。  
- **最容易踩的坑**：  
  - 忘记在回溯结束后 `pop()` 撤销选择，导致结果重复或错误。  
  - 对空字符串或长度为 1 的特殊情况处理不当（必须返回 `[[""]]` 或 `[["a"]]`）。  
  - DP 填表的遍历顺序写错，导致 `pal[i+1][j-1]` 还未计算好。  
- **下次思路**：一看到“所有子结构都要满足某种属性”，先问自己“这个属性能否提前预处理？”如果能，就先做 DP/前缀和等预处理，再进行枚举或滑动窗口。这样可以把重复判断的代价降到 O(1)。