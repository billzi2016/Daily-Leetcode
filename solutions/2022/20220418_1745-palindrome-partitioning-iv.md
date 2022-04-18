# #1745. 回文划分 IV / Palindrome Partitioning IV

> 难度：困难 · 标签：String、Dynamic Programming · [LeetCode 链接](https://leetcode.com/problems/palindrome-partitioning-iv/)

---

## 题目（英文原版）

**Description**

Given a string s, return true if it is possible to split the string s into three non-empty palindromic substrings. Otherwise, return false.​​​​​
A string is said to be palindrome if it the same string when reversed.

**Examples**

**Example 1:**

```
Input: s = "abcbdd"
Output: true
Explanation: "abcbdd" = "a" + "bcb" + "dd", and all three substrings are palindromes.
```

**Example 2:**

```
Input: s = "bcbddxy"
Output: false
Explanation: s cannot be split into 3 palindromes.
```

**Constraints**

- 3 <= s.length <= 2000
- s​​​​​​ consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串 `s`，若可以将 `s` 拆分成 **三个非空的回文子字符串**（palindromic substrings），则返回 `true`；否则返回 `false`。  
回文（palindrome）指的是正着读和倒着读完全相同的字符串。

---

### 示例

#### 示例 1
**输入**: `s = "abcbdd"`  
**输出**: `true`  
**解释**: `"abcbdd" = "a" + "bcb" + "dd"`，其中三个子字符串均为回文。

#### 示例 2
**输入**: `s = "bcbddxy"`  
**输出**: `false`  
**解释**: `s` 无法拆分成 3 个回文子字符串。

---

### 约束条件
- `3 <= s.length <= 2000`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把字符串的每一种切法都枚举一遍**，检查三个得到的子串是不是回文。  
具体做法：

1. 选第一个切点 `i`（`1 ≤ i ≤ n‑2`），把前缀 `s[0:i]` 当作第一个子串。  
2. 再选第二个切点 `j`（`i+1 ≤ j ≤ n‑1`），把中间段 `s[i:j]` 当作第二个子串，剩下的 `s[j:n]` 当作第三个子串。  
3. 对这三个子串分别用“逐字符比较”判断是否是回文（即从左往右、从右往左同时走，看到不相同就不是回文）。  
4. 只要出现一次全部为回文的切法，就返回 `True`，遍历完都没有则返回 `False`。

> **类比**：把字符串想成一根绳子，`i`、`j` 两把剪刀把它剪成三段，然后检查每段是否“对称”。  
> **哈希表**在这里没有用到，因为我们只需要“是否相等”而不需要快速查找。

**为什么正确**：只要遍历了**所有**合法的 `(i, j)` 组合，就一定不会漏掉任何可能的三段划分。如果某个划分能满足题意，暴力搜索必定会在对应的 `(i, j)` 处发现。

#### 代码（Python）

```python
def is_palindrome(sub: str) -> bool:
    """判断一个子串是否是回文，逐字符比较。"""
    left, right = 0, len(sub) - 1
    while left < right:
        if sub[left] != sub[right]:
            return False          # 只要有一对字符不相等，就不是回文
        left += 1
        right -= 1
    return True                  # 所有字符都匹配，说明是回文

def checkPartitioning_brute(s: str) -> bool:
    n = len(s)
    # 第一个切点 i，必须保证左边至少有 1 个字符，右边至少留 2 个字符
    for i in range(1, n - 1):
        if not is_palindrome(s[:i]):        # 先判断左侧是否回文，提前剪枝
            continue
        # 第二个切点 j，必须保证中间段至少 1 个字符，右侧也至少 1 个字符
        for j in range(i + 1, n):
            if is_palindrome(s[i:j]) and is_palindrome(s[j:]):
                return True                 # 找到合法划分
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n³)`  
  - 外层两个循环各遍历 `O(n)` 次，构成 `O(n²)` 种切法。  
  - 每次检查回文最坏需要 `O(n)`（逐字符比较），所以总共是 `O(n³)`。  
  - **大白话**：如果字符串长 1000，粗暴做法大概要进行 10⁹ 次字符比较，明显太慢。

- **空间复杂度**：`O(1)`（不使用额外的数组，只用常数级别的临时变量）。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **每次都要重新遍历子串来判断回文**，导致 `O(n³)`。  
如果我们能够在 **常数时间**（`O(1)`）内判断任意区间 `[l, r]` 是否是回文，就可以把整体时间降到 `O(n²)`（遍历所有切点的次数本身就是 `O(n²)`）。

**关键点**：提前预处理所有子串的回文信息。  
这正是「回文子串 DP」的经典做法：

1. 建立二维布尔数组 `pal[l][r]`，表示子串 `s[l..r]`（左闭右闭）是否是回文。  
2. 递推公式  
   - 当 `l == r`（长度 1）时，必为回文。  
   - 当 `r == l + 1`（长度 2）时，只有当两个字符相等才是回文。  
   - 其余情况：`pal[l][r] = (s[l] == s[r]) and pal[l+1][r-1]`。  
   这相当于「先检查最外层字符是否相同，再看内部子串是否已经确认是回文」。

   我们按 **子串长度从小到大** 填表，这样 `pal[l+1][r-1]` 总是已经算好。

3. 有了 `pal`，判断任意子串是否回文只需要一次数组查表 `O(1)`。

4. 接下来枚举切点 `i、j`（仍然是 `O(n²)`），但每次检查三个子串是否回文只用常数时间：

   - 第一个子串 `s[0:i-1]` → `pal[0][i-1]`  
   - 第二个子串 `s[i:j-1]` → `pal[i][j-1]`  
   - 第三个子串 `s[j:n-1]` → `pal[j][n-1]`

   只要三者都为 `True`，立即返回 `True`。

> **类比**：把 `pal` 看成一本「回文词典」，下标是「单词的起止位置」，查询是否回文就像在词典里查页码——瞬间得到答案。

#### 代码（Python）

```python
def checkPartitioning(s: str) -> bool:
    n = len(s)
    # 1. 预处理所有子串是否是回文，pal[l][r] 为 True 表示 s[l..r] 是回文
    pal = [[False] * n for _ in range(n)]

    # 按长度从小到大填表
    for length in range(1, n + 1):          # length = 子串长度
        for l in range(0, n - length + 1):
            r = l + length - 1              # 右端点
            if length == 1:
                pal[l][r] = True            # 单字符必是回文
            elif length == 2:
                pal[l][r] = (s[l] == s[r])  # 两字符相等才是回文
            else:
                pal[l][r] = (s[l] == s[r]) and pal[l + 1][r - 1]
                # 先看最外层字符是否相同，再看内部子串是否已确定回文

    # 2. 枚举两个切点 i、j，检查三个子串是否全为回文
    # i 为第一个子串的结束位置+1，j 为第二个子串的结束位置+1
    for i in range(1, n - 1):               # 第一个切点，左侧至少 1，右侧至少留 2
        if not pal[0][i - 1]:               # 左侧不是回文，直接跳过（剪枝）
            continue
        for j in range(i + 1, n):           # 第二个切点，保证中间段非空，右侧也非空
            if pal[i][j - 1] and pal[j][n - 1]:
                return True                # 找到满足条件的划分
    return False
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 预处理回文表遍历所有 `l、r` 组合，`n²/2` 次，常数时间完成每次判断。  
  - 枚举切点的两层循环也是 `O(n²)`，但每次只做 **常数次** 的数组查询。  
  - 与暴力的 `O(n³)` 相比，速度提升了一个量级。

- **空间复杂度**：`O(n²)`  
  - `pal` 表占用 `n × n` 的布尔矩阵，大约 `4 * n²` 字节（Python 中实际更大，但概念上是二次空间）。  
  - 如果要进一步压缩空间，也可以用「中心扩展」一次遍历得到所有回文区间，只需 `O(n)` 额外空间，但实现相对复杂，这里保留 `O(n²)` 便于理解。

---

## 心得

- **核心技巧**：先**预处理所有子串的回文信息**（DP），再在 **O(1)** 时间内查询，避免重复检查。  
- **适用场景**：  
  1. “把字符串划分成若干回文子串”类问题（如 *Palindrome Partitioning I/II*）。  
  2. “统计回文子串个数”或“最长回文子串”这类需要快速判断子串是否回文的题目。  
- **解题钥匙**：**“先把子问题的答案全部算好，再在主循环里直接查表”**。

---

## 反思

- **第一反应**：直接枚举切点并逐字符判断回文——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记 **非空** 要求，导致切点选到字符串头或尾。  
  - 在暴力实现中重复检查同一个子串的回文，导致时间超限。  
  - DP 填表时顺序错误（比如先用了 `pal[l+1][r-1]` 而它还未计算）。  
- **下次类似题目**的第一步：**思考能否把“回文判定”预处理成 O(1) 的查询**，如果可以，就先写出 DP 或中心扩展的预处理代码，再进行划分或计数的主循环。