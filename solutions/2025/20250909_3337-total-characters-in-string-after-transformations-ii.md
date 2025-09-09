# #3337. 转换后字符串的总字符数 II / Total Characters in String After Transformations II

> 难度：困难 · 标签：Hash Table、Math、String、Dynamic Programming、Counting · [LeetCode 链接](https://leetcode.com/problems/total-characters-in-string-after-transformations-ii/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of lowercase English letters, an integer t representing the number of transformations to perform, and an array nums of size 26. In one transformation, every character in s is replaced according to the following rules:
Return the length of the resulting string after exactly t transformations.
Since the answer may be very large, return it modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: s = "abcyy", t = 2, nums = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]
Output: 7
Explanation:
First Transformation (t = 1):
Second Transformation (t = 2):
Final Length of the string: The string is "cdeabab" , which has 7 characters.
```

**Example 2:**

```
Input: s = "azbk", t = 1, nums = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]
Output: 8
Explanation:
First Transformation (t = 1):
Final Length of the string: The string is "bcabcdlm" , which has 8 characters.
```

**Constraints**

- 1 <= s.length <= 105
- s consists only of lowercase English letters.
- 1 <= t <= 109
- nums.length == 26
- 1 <= nums[i] <= 25

---

## 题目（中文翻译）

给定一个仅由小写英文字母组成的字符串 `s`，一个表示要执行的转换次数的整数 `t`，以及一个长度为 26 的数组 `nums`。在一次 **转换**（transformation）中，`s` 中的每个字符都会按照以下规则被替换：

返回恰好进行 `t` 次转换后得到的字符串的长度。由于答案可能非常大，请返回其对 `10^9 + 7` 取模的结果。

**示例 1**  
输入: `s = "abcyy"`, `t = 2`, `nums = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2]`  
输出: `7`  
解释:  
- 第一次转换 (t = 1)：  
- 第二次转换 (t = 2)：  
- 最终字符串长度：字符串为 `"cdeabab"`，长度为 7。

**示例 2**  
输入: `s = "azbk"`, `t = 1`, `nums = [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2]`  
输出: `8`  
解释:  
- 第一次转换 (t = 1)：  
- 最终字符串长度：字符串为 `"bcabcdlm"`，长度为 8。

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 仅由小写英文字母组成。  
- `1 <= t <= 10^9`  
- `nums.length == 26`  
- `1 <= nums[i] <= 25`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**一步一步地模拟**每一次变换：

1. 统计当前字符串里每个字母出现了多少次（用一个长度为 26 的数组 `cnt`，下标 0 表示 `'a'`，下标 25 表示 `'z'`）。  
2. 对于每一个字母 `c`，查看 `nums[c]`，把它“展开”为后面的 `nums[c]` 个字母（超出 `'z'` 时回到 `'a'`），并把这些字母的计数加到新的数组里。  
3. 把新数组替换旧数组，重复 **t 次**，最后把 26 个计数加起来就是答案。

> **类比**：想象你手里有 26 种不同颜色的积木，每种颜色的积木代表一种字母。一次变换就像把每块积木拆成若干块新的颜色积木，拆出来的颜色顺序固定（后面的 `nums[i]` 个字母）。我们把所有积木重新收集，再继续拆。  

**为什么能得到正确答案**  
因为每一次变换只和当前每个字母出现的次数有关，完全不需要关心字母的具体位置。只要把每个字母的“产出”记录下来，累计到下一个回合，就等价于真正执行了字符串的替换。

**时间/空间分析**  
- 每一次变换要遍历 26 种字母，内部最多循环 `nums[i] ≤ 25` 次，时间是 `O(26·25) ≈ O(1)`（常数），但要重复 **t 次**。  
- `t` 的上限是 `10^9`，所以 **暴力模拟的时间是 O(t)**，在最坏情况下要跑十亿次，根本不可接受。  
- 空间只需要两个长度为 26 的数组，`O(1)`。

> **大白话**：如果把 `O(t)` 想成“每秒只能处理 1 次变换”，要跑十亿秒——也就是好几十年！这就是暴力解的致命瓶颈。

#### 代码（Python）

```python
MOD = 10**9 + 7

def brute(s: str, t: int, nums: list[int]) -> int:
    # 统计初始每个字母的出现次数
    cnt = [0] * 26
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    for _ in range(t):                     # 这里的循环就是暴力的根本
        nxt = [0] * 26
        for i in range(26):                # i 表示字母 i（0 为 a）
            if cnt[i] == 0:
                continue
            k = nums[i]                     # 需要展开的长度
            for d in range(1, k + 1):      # 产生后面的 k 个字母
                j = (i + d) % 26           # 超出 z 回到 a
                nxt[j] = (nxt[j] + cnt[i]) % MOD
        cnt = nxt

    return sum(cnt) % MOD
```

> 关键行都有中文注释，代码可以直接运行，只是对大 `t` 会超时。

#### 复杂度

- **时间复杂度**：`O(t·26·max(nums))` → 近似 `O(t)`，当 `t = 10^9` 时根本跑不完。  
- **空间复杂度**：`O(26)` → 常数级别。

---

### 2. 最优解

#### 思路  

从暴力解可以看到：

- 每一次变换只和 **每个字母的出现次数** 有关，和字符在字符串中的相对位置无关。  
- 对于字母 `i`，一次变换后它会产生 **恰好 `nums[i]` 个不同的字母**（分别是 `i+1, i+2, …, i+nums[i]`，模 26 循环）。  
- 这正好是一种 **线性变换**：把一个 26 维向量（每个维度代表一种字母的数量）乘以一个 26×26 的矩阵，得到下一个向量。

**关键点**：把变换过程抽象为矩阵乘法，然后利用矩阵的快速幂（指数化）把 `t` 次乘法压缩到 `O(log t)` 次。

##### 2.1 构造转移矩阵  

定义矩阵 `M`（大小 26×26）：

```
M[i][j] = 1   如果字母 i 经过一次变换会产生字母 j
M[i][j] = 0   其他情况
```

举例：若 `nums[0] = 2`（字母 `'a'`），则 `'a'` 变成 `'b'`、`'c'`，所以  
`M[0][1] = 1`，`M[0][2] = 1`，其余为 0。

构造方法：

```python
for i in range(26):
    k = nums[i]
    for d in range(1, k + 1):
        j = (i + d) % 26
        M[i][j] = 1
```

每行的 **1 的个数恰好等于 `nums[i]`**，这正对应一次变换产生的字符数。

##### 2.2 初始向量  

`cnt0` 为长度 26 的向量，`cnt0[i]` 表示原字符串里字母 `i` 的出现次数（同暴力解的第一步）。

##### 2.3 经过 t 次变换  

向量的演化公式：

```
cnt_t = cnt0  ×  (M ^ t)
```

这里 `M ^ t` 表示矩阵 `M` 的 `t` 次幂。  
因为向量左乘矩阵（行向量），我们可以先算 `P = M ^ t`，再把 `cnt0` 与 `P` 相乘得到最终向量。

##### 2.4 快速幂  

矩阵快速幂和整数快速幂完全一样：把指数二进制拆分，每次把当前矩阵平方并根据位是否为 1 来累乘答案矩阵。时间复杂度是 `O(26³·log t)`，因为每次矩阵相乘需要 `26³` 次基本运算。

- `26³ = 17,576`，非常小，乘以 `log2(10^9) ≈ 30`，总共不到 600k 次基本乘加，轻松在时间限制内完成。

##### 2.5 求答案  

`cnt_t` 已经是每种字母出现的次数，**总长度**就是它们的和：

```
ans = sum(cnt_t) % MOD
```

#### 代码（Python）

```python
MOD = 10**9 + 7
SIZE = 26                         # 字母表大小

def mat_mul(A, B):
    """返回 (A * B) % MOD，尺寸均为 26×26"""
    C = [[0] * SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        Ai = A[i]
        for k in range(SIZE):
            if Ai[k] == 0:
                continue
            aik = Ai[k]
            Bk = B[k]
            for j in range(SIZE):
                C[i][j] = (C[i][j] + aik * Bk[j]) % MOD
    return C

def mat_pow(M, power):
    """返回 M^power % MOD，使用二进制快速幂"""
    # 初始化为单位矩阵（乘以它不改变向量）
    result = [[int(i == j) for j in range(SIZE)] for i in range(SIZE)]
    base = M
    while power:
        if power & 1:
            result = mat_mul(result, base)
        base = mat_mul(base, base)
        power >>= 1
    return result

def vector_mul(vec, M):
    """行向量 vec (1×26) 与矩阵 M (26×26) 相乘，返回新向量"""
    new = [0] * SIZE
    for i in range(SIZE):
        if vec[i] == 0:
            continue
        vi = vec[i]
        Mi = M[i]
        for j in range(SIZE):
            new[j] = (new[j] + vi * Mi[j]) % MOD
    return new

def totalLength(s: str, t: int, nums: list[int]) -> int:
    # 1. 初始计数向量
    cnt = [0] * SIZE
    for ch in s:
        cnt[ord(ch) - ord('a')] += 1

    # 2. 构造转移矩阵 M
    M = [[0] * SIZE for _ in range(SIZE)]
    for i in range(SIZE):
        k = nums[i]
        for d in range(1, k + 1):
            j = (i + d) % SIZE
            M[i][j] = 1

    # 3. 计算 M^t
    Mt = mat_pow(M, t)

    # 4. 计算最终计数向量
    cnt_t = vector_mul(cnt, Mt)

    # 5. 总长度（模 1e9+7）
    return sum(cnt_t) % MOD
```

> 代码中每一步都配有中文注释，`mat_mul` 用了 “跳过 0” 的优化，让常数更小；整体思路完全基于矩阵快速幂，能够在 `O(26³·log t)` 时间内完成。

#### 复杂度

- **时间复杂度**：`O(26³·log t)` ≈ `O(log t)`，因为 26 是常数。对 `t ≤ 10⁹`，只需要约 30 次矩阵平方与乘法，极快。  
- **空间复杂度**：`O(26²)`，用于存放矩阵和中间结果，也是常数级别。

与暴力解相比，时间从线性的 `t` 降到了对数级的 `log t`，大幅提升。

---

## 心得

- **核心技巧**：把“每个字符产生若干固定字符”的过程抽象为 **线性变换 + 矩阵快速幂**。  
- **适用的题型**  
  1. “字符串/数组/状态每一步都按照固定规则线性转移”，如 *Total Characters in String After Transformations I/II*。  
  2. “图的邻接矩阵的 k 步可达数量”或 “Markov 链的 k 步转移”。  
  3. “数列的线性递推（如斐波那契）”使用矩阵幂的场景。  

> **一句话总结**：把“每次固定扩展”视作矩阵乘法，利用二进制快速幂把巨大的步数压缩到对数时间。

---

## 反思

- **第一反应**：直接模拟每一次变换，觉得只要循环 `t` 次就行。  
- **最容易踩的坑**  
  - 忘记对 **模数** (`10⁹+7`) 做取模，导致整数溢出。  
  - 在构造矩阵时没有考虑 **环绕**（`z` 后面是 `a`），会少了几条转移。  
  - `t` 为 `0` 时应该直接返回原字符串长度（这里题目保证 `t ≥ 1`，但实现时仍要兼容）。  
- **下次类似题目**：第一步就判断“状态是否可以用固定维度的向量描述”，如果可以，立刻考虑 **矩阵/线性代数** 的方式，而不是逐步模拟。这样往往能把指数级的循环降到对数级。