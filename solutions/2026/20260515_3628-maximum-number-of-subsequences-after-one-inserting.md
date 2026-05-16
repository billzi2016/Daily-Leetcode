# #3628. 一次插入后最多的子序列数量 / Maximum Number of Subsequences After One Inserting

> 难度：中等 · 标签： · [LeetCode 链接](https://leetcode.com/problems/maximum-number-of-subsequences-after-one-inserting/)

---

## 题目（英文原版）

**Description**

You are given a string s consisting of uppercase English letters.
You are allowed to insert at most one uppercase English letter at any position (including the beginning or end) of the string.
Return the maximum number of "LCT" subsequences that can be formed in the resulting string after at most one insertion.

**Examples**

**Example 1:**

```
Input: s = "LMCT"
Output: 2
Explanation:
We can insert a "L" at the beginning of the string s to make "LLMCT" , which has 2 subsequences, at indices [0, 3, 4] and [1, 3, 4].
```

**Example 2:**

```
Input: s = "LCCT"
Output: 4
Explanation:
We can insert a "L" at the beginning of the string s to make "LLCCT" , which has 4 subsequences, at indices [0, 2, 4], [0, 3, 4], [1, 2, 4] and [1, 3, 4].
```

**Example 3:**

```
Input: s = "L"
Output: 0
Explanation:
Since it is not possible to obtain the subsequence "LCT" by inserting a single letter, the result is 0.
```

**Constraints**

- 1 <= s.length <= 105
- s consists of uppercase English letters.

---

## 题目（中文翻译）

**题目描述**  
给定一个仅包含大写英文字母（uppercase English letter）的字符串 `s`。  
你可以在字符串的任意位置（包括开头或结尾）最多插入一个大写英文字母。  
返回在至多插入一次字符后，所得字符串中可以形成的 “LCT” 子序列（subsequence）的最大数量。

**示例**

**示例 1**  
```
Input: s = "LMCT"
Output: 2
Explanation:
我们可以在字符串开头插入一个 “L”，得到 "LLMCT"。该字符串中存在 2 个 “LCT” 子序列，索引分别为 [0, 3, 4] 和 [1, 3, 4]。
```

**示例 2**  
```
Input: s = "LCCT"
Output: 4
Explanation:
我们可以在字符串开头插入一个 “L”，得到 "LLCCT"。该字符串中共有 4 个 “LCT” 子序列，索引为 [0, 2, 4]、[0, 3, 4]、[1, 2, 4]、[1, 3, 4]。
```

**示例 3**  
```
Input: s = "L"
Output: 0
Explanation:
即使插入一个字符，也无法在结果字符串中形成 “LCT” 子序列，故答案为 0。
```

**约束条件**  
- `1 <= s.length <= 10^5`  
- `s` 只包含大写英文字母（uppercase English letter）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的插入位置和所有 26 个大写字母都枚举一遍**，得到插入后的新字符串后，直接统计其中出现的 `"LCT"` 子序列个数，取最大的那个。  

- **枚举插入位置**：如果原字符串长度为 `n`，可以在 `0 … n`（共 `n+1` 个缝隙）插入字符。  
- **枚举插入字符**：因为只能插入大写字母，最多有 26 种选择。  
- **统计子序列**：遍历新字符串，用三层循环找所有满足 `i<j<k` 且 `s[i]=='L'、s[j]=='C'、s[k]=='T'` 的三元组。  

> **类比**：把字符串想象成一排座位，暴力解就是把每一位可能的“新人”都请进来，随后让所有坐在座位上的学生两两配对，找出符合 “L‑C‑T” 规则的三人组合。  

这种方法一定能得到正确答案，因为我们把**所有合法的插入方式**都尝试了一遍，并且**每一种插入方式**都完整地统计了子序列数量。

#### 代码（Python）

```python
def count_LCT(s: str) -> int:
    """统计字符串 s 中出现的 LCT 子序列个数（暴力三重循环）"""
    n = len(s)
    cnt = 0
    for i in range(n):
        if s[i] != 'L':          # 第一个字符必须是 L
            continue
        for j in range(i + 1, n):
            if s[j] != 'C':      # 第二个必须是 C
                continue
            for k in range(j + 1, n):
                if s[k] == 'T':  # 第三个必须是 T
                    cnt += 1
    return cnt


def maxSubseq_bruteforce(s: str) -> int:
    n = len(s)
    best = 0
    # 枚举插入位置（0 表示在最前面，n 表示在最后面）
    for pos in range(n + 1):
        # 枚举插入的字符
        for ch in map(chr, range(ord('A'), ord('Z') + 1)):
            # 生成插入后的新字符串
            new_s = s[:pos] + ch + s[pos:]
            # 统计 LCT 子序列数量
            cur = count_LCT(new_s)
            best = max(best, cur)
    return best
```

> 关键行中文注释已经写在代码里，直接运行即可得到答案（但会超时）。

#### 复杂度  

- **时间复杂度**：  
  - 插入位置有 `n+1` 种，字符有 26 种，总共 `O(26·(n+1)) ≈ O(n)` 次构造新字符串的操作。  
  - 对每个新字符串，我们用了三层循环遍历所有三元组，最坏情况是 `O(n³)`（因为每层最多遍历 `n` 次）。  
  - 综合起来是 **`O(26·(n+1)·n³) = O(n⁴)`**，在 `n ≤ 10⁵` 时根本不可行。  
  - **大白话**：想象我们把每一位同学都请进来，然后让每三个人组成一组检查一次，这种“全员全组”方式在人数稍大时就会炸掉。  

- **空间复杂度**：  
  - 只用了常数级别的额外变量（`cnt、best、pos、ch`），所以是 **`O(1)`**。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次插入后都重新遍历整条字符串去统计子序列**。其实我们可以在 **原字符串上预处理**，一次性算出不插入时已有的 `"LCT"` 子序列数，然后再**只计算插入一个字符带来的增量**，这样就能把复杂度降到线性 `O(n)`。

下面一步步推导：

1. **不插入时的基准值（base）**  
   - 对每个位置 `i`（`0 ≤ i < n`），如果把它当作字符 `'C'` 的位置，那么左边所有的 `'L'`（记为 `preL[i]`）可以和它配对，右边所有的 `'T'`（记为 `sufT[i]`）可以继续配对，形成 `preL[i] * sufT[i]` 条 `"LCT"`。  
   - 把所有 `i` 上的贡献累加，即得到原字符串中所有 `"LCT"` 子序列的数量：  

     `base = Σ preL[i] * sufT[i]`（只在 `s[i]=='C'` 时计数）。

2. **插入字符的增量**  
   插入一个字符只能是 `'L'、'C'、'T'`（插入别的字符不会产生新的子序列）。我们分别讨论：

   - **插入 `'L'`**：它只能充当子序列的第一个字符。放在位置 `i`（即在原字符 `s[i]` 前面），它左边没有 `'L'`（因为是新插入的），右边可以使用所有形如 `"CT"` 的子序列。  
     - 右边的 `"CT"` 数量正好是 `sufCT[i]`（从位置 `i` 开始向右统计的 `'C'` 与其右侧 `'T'` 的配对数）。  
     - 增量 = `sufCT[i]`。

   - **插入 `'C'`**：它只能充当第二个字符。左边可以选任意 `'L'`（数量 `preL[i]`），右边可以选任意 `'T'`（数量 `sufT[i]`），所以增量 = `preL[i] * sufT[i]`。

   - **插入 `'T'`**：它只能充当第三个字符。左边需要已经形成的 `"LC"`，数量正好是 `preLC[i]`（从左到右统计的 `'L'` 与其右侧 `'C'` 的配对数）。  
     - 增量 = `preLC[i]`。

   对每个插入位置 `i`（`0 … n`），我们只需要取三种字符产生的增量最大值，再加上 `base`，得到在该位置的最优结果。最终答案是所有位置的最大值以及不插入时的 `base`（因为插入可能不提升结果）。

3. **如何快速得到四个前缀/后缀数组**  

   - `preL[i]`：`i` 之前（不含 `i`）出现的 `'L'` 个数。一次遍历即可累计。  
   - `preLC[i]`：`i` 之前形成的 `"LC"` 对数。遍历时如果当前字符是 `'C'`，则把之前的 `preL` 加到 `preLC`；如果是 `'L'`，则只更新 `preL`。  
   - `sufT[i]`：`i` 之后（不含 `i`）出现的 `'T'` 个数。逆向遍历累计。  
   - `sufCT[i]`：`i` 之后形成的 `"CT"` 对数。逆向遍历时如果当前字符是 `'C'`，把之后的 `sufT` 加到 `sufCT`；如果是 `'T'`，只更新 `sufT`。

   所有数组都只需要 **一次正向 + 一次逆向** 的线性遍历，时间 `O(n)`，空间 `O(n)`（可以用 `list` 存储，或在极端情况下用滚动变量把空间压到 `O(1)`，这里为了代码简洁保留 `O(n)`）。

#### 代码（Python）

```python
def maxNumberOfLCT(s: str) -> int:
    n = len(s)

    # ---------- 前缀统计 ----------
    preL = [0] * (n + 1)      # preL[i] = s[:i] 中 L 的个数
    preLC = [0] * (n + 1)     # preLC[i] = s[:i] 中所有 "LC" 对数
    for i, ch in enumerate(s):
        preL[i + 1] = preL[i] + (ch == 'L')
        # 如果当前是 C，则它可以和左边所有的 L 组成 LC 对
        preLC[i + 1] = preLC[i] + (preL[i] if ch == 'C' else 0)

    # ---------- 后缀统计 ----------
    sufT = [0] * (n + 1)      # sufT[i] = s[i:] 中 T 的个数
    sufCT = [0] * (n + 1)     # sufCT[i] = s[i:] 中所有 "CT" 对数
    for i in range(n - 1, -1, -1):
        ch = s[i]
        sufT[i] = sufT[i + 1] + (ch == 'T')
        # 如果当前是 C，则它可以和右边所有的 T 组成 CT 对
        sufCT[i] = sufCT[i + 1] + (sufT[i + 1] if ch == 'C' else 0)

    # ---------- 1. 计算不插入时的基准值 ----------
    base = 0
    for i, ch in enumerate(s):
        if ch == 'C':
            # 左边所有 L 与右边所有 T 配对
            base += preL[i] * sufT[i + 1]

    # ---------- 2. 考虑一次插入的增量 ----------
    ans = base          # 先把不插入的情况计入答案
    for i in range(n + 1):   # 插入位置 i 表示在 s[i-1] 与 s[i] 之间
        # 插入 L 的增量 = 右侧所有 CT 对
        gain_L = sufCT[i]

        # 插入 C 的增量 = 左侧 L 数 * 右侧 T 数
        gain_C = preL[i] * sufT[i]

        # 插入 T 的增量 = 左侧所有 LC 对
        gain_T = preLC[i]

        # 取三者最大，再加上基准值
        ans = max(ans, base + gain_L, base + gain_C, base + gain_T)

    return ans
```

> 关键行已加中文注释，直接运行即可得到答案，时间复杂度线性，能够轻松通过 10⁵ 长度的极限。

#### 复杂度  

- **时间复杂度**：  
  - 正向遍历一次得到 `preL、preLC` → `O(n)`。  
  - 逆向遍历一次得到 `sufT、sufCT` → `O(n)`。  
  - 再遍历一次计算 `base` 与每个插入位置的增量 → `O(n)`。  
  - **总计 `O(n)`**，即随字符串长度线性增长。  
  - **含义**：如果字符串有 100,000 个字符，程序只会遍历大约 3 次（300,000 次基本操作），完全可以在毫秒级完成。

- **空间复杂度**：  
  - 四个长度为 `n+1` 的数组各占 `O(n)`，所以整体是 **`O(n)`**。  
  - 若想进一步压缩，可把 `preLC` 与 `preL` 合并，用滚动变量，只保留当前前缀信息；同理 `sufCT` 与 `sufT` 也可以合并，空间可降到 `O(1)`。但 `O(n)` 已经足够满足题目要求。

---

## 心得  

- **核心技巧**：利用前缀计数 + 后缀计数，把“子序列计数”拆成左侧 * 右侧 的乘积，从而在 **一次遍历** 内得到所有位置的贡献。  
- **适用的题型**：  
  1. “在字符串中插入/删除一个字符后，使某种子序列（如 `ABC`、`XYZ`）的个数最大”——如本题。  
  2. “统计所有形如 `AB`、`ABC`、`ABCD` 的子序列数量”——常用前缀/后缀乘积技巧。  
  3. “求在一个数组中插入一个元素后，使逆序对/特定三元组数量最大”——同样可以用前缀计数 + 后缀计数。  
- **一句话总结解题钥匙**：**把子序列的每一位分别放到左/右两侧，用乘法把它们“拼接”起来，然后只考虑插入字符的三种可能增量**。

---

## 反思  

- **第一反应**：直接暴力枚举所有插入方式并逐个计数，思路清晰但忽视了规模。  
- **最容易踩的坑**：  
  - 计算增量时忘记区分插入位置的左侧/右侧范围（比如 `sufCT[i]` 应该是从位置 `i` 开始往右的 CT 对，而不是包括当前位置的字符）。  
  - 在统计基准值 `base` 时，`preL[i]` 与 `sufT[i+1]` 的下标要对应好，否则会把同一字符算两次。  
  - 边界情况：字符串长度为 1 或者根本没有 `'C'`、`'T'` 时，增量可能为 0，答案应返回 `base`（有时为 0）。  
- **下次遇到同类题**：第一步先**思考如何把子序列拆成“左侧 + 当前字符 + 右侧”的形式**，并尝试用前缀/后缀计数把每一部分的贡献预先算好，这样插入/删除的增量就能在 O(1) 内得到。这样可以立刻把暴力的 `O(n³)` 降到线性的 `O(n)`。