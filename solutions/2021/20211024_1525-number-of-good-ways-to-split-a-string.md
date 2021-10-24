# #1525. 划分字符串的好方法数 / Number of Good Ways to Split a String

> 难度：中等 · 标签：Hash Table、String、Dynamic Programming、Bit Manipulation · [LeetCode 链接](https://leetcode.com/problems/number-of-good-ways-to-split-a-string/)

---

## 题目（英文原版）

**Description**

You are given a string s.
A split is called good if you can split s into two non-empty strings sleft and sright where their concatenation is equal to s (i.e., sleft + sright = s) and the number of distinct letters in sleft and sright is the same.
Return the number of good splits you can make in s.

**Examples**

**Example 1:**

```
Input: s = "aacaba"
Output: 2
Explanation: There are 5 ways to split "aacaba" and 2 of them are good. 
("a", "acaba") Left string and right string contains 1 and 3 different letters respectively.
("aa", "caba") Left string and right string contains 1 and 3 different letters respectively.
("aac", "aba") Left string and right string contains 2 and 2 different letters respectively (good split).
("aaca", "ba") Left string and right string contains 2 and 2 different letters respectively (good split).
("aacab", "a") Left string and right string contains 3 and 1 different letters respectively.
```

**Example 2:**

```
Input: s = "abcd"
Output: 1
Explanation: Split the string as follows ("ab", "cd").
```

**Constraints**

- 1 <= s.length <= 105
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

给定一个字符串（string）`s`。  
如果可以把 `s` 划分（split）为两个非空字符串 `sleft` 和 `sright`，且它们的拼接（concatenation）等于 `s`（即 `sleft + sright = s`），并且 `sleft` 和 `sright` 中不同字母的种类数（distinct letters）相同，则称这次划分为**好划分（good split）**。  

返回 `s` 中可以形成的好划分的数量。

### 示例

**示例 1**  
```
Input: s = "aacaba"
Output: 2
Explanation: "aacaba" 有 5 种划分方式，其中 2 种是好划分。
("a", "acaba") 左侧字符串和右侧字符串分别包含 1 和 3 种不同字母。
("aa", "caba") 左侧字符串和右侧字符串分别包含 1 和 3 种不同字母。
("aac", "aba") 左侧字符串和右侧字符串分别包含 2 和 2 种不同字母（好划分）。
("aac...
```

**示例 2**  
```
Input: s = "abcd"
Output: 1
Explanation: 将字符串划分为 ("ab", "cd") 即为唯一的好划分。
```

### 约束条件
- `1 <= s.length <= 10^5`
- `s` 仅由小写英文字母组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的切分位置**，对每一种切分分别统计左半段 `sleft` 和右半段 `sright` 中出现的不同字母数量，若相等则计数。

- **数据结构**：  
  - 为了统计不同字母的种类数，我们可以使用 **哈希表**（在 Python 中用 `dict` 或 `set`），它的工作方式类似于查字典：键（key）是字母本身，值（value）可以是出现次数或直接忽略，只要把键放进去就算作“这本字典里有这个词”。  
  - 这里我们只需要知道有哪些字母出现过，所以 `set` 更合适——把每个字母加入集合，集合的大小 `len(set)` 就是不同字母的个数。

- **正确性**：  
  - 我们遍历了所有合法的切分点（从第 1 位到倒数第 2 位），每一次都完整地计算了左、右两段的不同字母数。如果它们相等，就说明这一次切分满足题目要求，计数即可。因为没有遗漏任何切分点，也没有错误的计数方式，所以结果一定正确。

- **复杂度**：  
  - **时间**：对每个切分点我们都要遍历一次左子串和一次右子串来收集不同字母。左子串长度从 `1` 到 `n‑1`，右子串长度相应从 `n‑1` 到 `1`。总的遍历次数大约是  
    \[
    1 + 2 + \dots + (n-1) \;+\; (n-1) + (n-2) + \dots + 1 \;=\; O(n^2)
    \]  
    用大白话说，就是 **随着字符串长度的增长，运算次数会像平方一样快速增长**（比如长度 10,000 时会有 100,000,000 次循环，明显太慢）。
  - **空间**：每次统计我们都新建两个 `set`，最多各装 `26`（小写英文字母的上限）个元素，空间是 **O(1)**（常数级），因为不随 `n` 增大而增长。

#### 代码（Python）

```python
def numSplits_brute(s: str) -> int:
    n = len(s)
    good = 0                     # 记录满足条件的切分次数

    # i 为左子串的长度，取值范围 [1, n-1]
    for i in range(1, n):
        left_set = set()         # 用来收集左子串的不同字母
        right_set = set()        # 用来收集右子串的不同字母

        # 统计左子串 s[0:i] 的不同字母
        for ch in s[:i]:
            left_set.add(ch)

        # 统计右子串 s[i:] 的不同字母
        for ch in s[i:]:
            right_set.add(ch)

        # 如果两边的种类数相等，就是一次“好”切分
        if len(left_set) == len(right_set):
            good += 1

    return good
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 随着字符串长度 `n` 增大，运算次数呈二次方增长，实际表现为“每增加一次字符，工作量会多很多”。
- **空间复杂度**：`O(1)` — 只用了两个最多装 26 个字母的集合，所需空间不随 `n` 变化。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于每次切分都要重新遍历左、右子串来统计不同字母，导致大量重复劳动。我们可以 **利用前缀/后缀统计** 把这些重复的遍历一次性搬到整体的预处理阶段。

1. **观察**：  
   - 当切分点从左向右移动一格时，左子串只会 **多加入一个字符**，右子串只会 **少去一个字符**。因此左、右两边的不同字母数可以**逐步更新**，而不必每次重新遍历。

2. **前缀计数**（左侧）：  
   - 用一个长度为 `n` 的数组 `pref[i]` 表示 **以第 `i` 位字符结尾的左子串**（即 `s[:i+1]`）中不同字母的数量。  
   - 维护一个大小为 26 的布尔数组 `seen_left`，记录每个字母是否已经出现过。遍历字符串一次，遇到新字母时把计数 `cnt` 加 1，并把 `cnt` 写入 `pref[i]`。

3. **后缀计数**（右侧）：  
   - 类似地，用数组 `suf[i]` 表示 **从第 `i` 位字符开始的右子串**（即 `s[i:]`）中不同字母的数量。  
   - 这次从右往左遍历，用另一个布尔数组 `seen_right` 同样记录出现情况，得到 `suf[i]`。

4. **一次遍历统计答案**：  
   - 好的切分点必须满足 `pref[i] == suf[i+1]`（左子串以 `i` 为结尾，右子串从 `i+1` 开始）。只要把这两个数组对应位置比较一次，就能得到答案。

5. **为什么使用数组而不是哈希表**？  
   - 字符都是小写英文字母，只有 26 种可能，用长度固定的数组（或列表）既省空间，又省时间（下标直接访问 O(1)），比 `dict`/`set` 更轻量。

6. **时间/空间分析**：  
   - 预处理遍历两遍字符串，都是线性时间 `O(n)`。  
   - 额外使用的数组 `pref`、`suf`、以及两个长度为 26 的布尔数组，总共 `O(n)` 的空间。

#### 代码（Python）

```python
def numSplits(s: str) -> int:
    n = len(s)
    # 1. 前缀不同字母数
    pref = [0] * n                # pref[i] = s[:i+1] 中不同字母的数量
    seen_left = [False] * 26      # 记录左侧是否出现过该字母
    cnt = 0                       # 当前不同字母的计数

    for i, ch in enumerate(s):
        idx = ord(ch) - ord('a')   # 把字符映射到 0~25 的下标
        if not seen_left[idx]:    # 第一次遇到该字母
            seen_left[idx] = True
            cnt += 1
        pref[i] = cnt

    # 2. 后缀不同字母数
    suf = [0] * n                 # suf[i] = s[i:] 中不同字母的数量
    seen_right = [False] * 26
    cnt = 0

    for i in range(n - 1, -1, -1):
        idx = ord(s[i]) - ord('a')
        if not seen_right[idx]:
            seen_right[idx] = True
            cnt += 1
        suf[i] = cnt

    # 3. 统计满足 pref[i] == suf[i+1] 的切分点
    ans = 0
    for i in range(n - 1):        # 切分点只能在 0~n-2 之间
        if pref[i] == suf[i + 1]:
            ans += 1

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历了三遍字符串（一次前缀，一次后缀，一次比较），即使 `n` 达到 10⁵ 也能毫秒级完成。相比暴力的 `O(n²)`，**快了整整 n 倍**。
- **空间复杂度**：`O(n)` — 需要两个长度为 `n` 的数组 `pref`、`suf`，以及常数大小的 26 长度布尔数组。因为 `n` 最多 10⁵，使用约 2×10⁵ 个整数（约 1.6 MB），完全可接受。

---

## 心得

- **核心技巧**：**前缀/后缀统计**（Prefix‑Suffix）结合 **位/字符映射**，把“每次都重新统计”转化为“一次遍历得到所有信息”。  
- **适用的题型**：  
  1. “统计切分点使左右子数组/子串满足某种相等关系”——如 *Number of Good Ways to Split a String*、*Split Array Largest Sum*（使用前缀和）  
  2. “求满足某种条件的子数组/子串数量”——如 *Number of Subarrays with K Different Integers*（滑动窗口+前缀计数）  
  3. “在左右两侧分别统计信息后比较”——如 *Maximum Product of Splitted Binary Tree*（左右子树信息）  

- **一句话总结解题钥匙**：**把局部重复的统计提前到全局的前缀/后缀预处理，一次遍历即可得到所有切分点的答案。**

---

## 反思

- **第一反应**：看到“切分”和“不同字母数相同”，本能想到 **遍历所有切分点并分别计数**（即暴力法），因为最直接也最容易写出来。
- **最容易踩的坑**：  
  - **边界条件**：切分必须让两段都 **非空**，所以切分点只能在 `1 … n‑1`（对应 `i` 从 `0` 到 `n‑2`）。  
  - **字符集合的实现**：使用 `set` 虽然直观，但在 `O(n²)` 的暴力中会导致额外的内存分配，影响性能。  
  - **字符映射**：忘记把字符转换成 `0‑25` 的下标会导致数组越界或错误计数。  
  - **计数同步**：在前缀/后缀统计时，记得在写入数组之前先更新计数，否则会少算当前字符。

- **下次遇到同类题**：**第一步就思考“是否可以通过一次遍历把所有需要的统计信息收集好（前缀/后缀、哈希计数、位掩码）”，再在第二遍遍历中直接比较**。这样能快速从暴力思路跳到线性解。