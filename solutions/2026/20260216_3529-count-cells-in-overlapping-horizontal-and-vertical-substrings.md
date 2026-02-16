# #3529. 重叠水平和垂直子串中的单元格计数 / Count Cells in Overlapping Horizontal and Vertical Substrings

> 难度：中等 · 标签：Array、String、Rolling Hash、String Matching、Matrix、Hash Function · [LeetCode 链接](https://leetcode.com/problems/count-cells-in-overlapping-horizontal-and-vertical-substrings/)

---

## 题目（英文原版）

**Description**

You are given an m x n matrix grid consisting of characters and a string pattern.
A horizontal substring is a contiguous sequence of characters read from left to right. If the end of a row is reached before the substring is complete, it wraps to the first column of the next row and continues as needed. You do not wrap from the bottom row back to the top.
A vertical substring is a contiguous sequence of characters read from top to bottom. If the bottom of a column is reached before the substring is complete, it wraps to the first row of the next column and continues as needed. You do not wrap from the last column back to the first.
Count the number of cells in the matrix that satisfy the following condition:
Return the count of these cells.

**Examples**

**Example 1:**

```
Input: grid = [["a","a","c","c"],["b","b","b","c"],["a","a","b","a"],["c","a","a","c"],["a","a","b","a"]], pattern = "abaca"
Output: 1
Explanation:
The pattern "abaca" appears once as a horizontal substring (colored blue) and once as a vertical substring (colored red), intersecting at one cell (colored purple).
```

**Example 2:**

```
Input: grid = [["c","a","a","a"],["a","a","b","a"],["b","b","a","a"],["a","a","b","a"]], pattern = "aba"
Output: 4
Explanation:
The cells colored above are all part of at least one horizontal and one vertical substring matching the pattern "aba" .
```

**Example 3:**

```
Input: grid = [["a"]], pattern = "a"
Output: 1
```

**Constraints**

- m == grid.length
- n == grid[i].length
- 1 <= m, n <= 1000
- 1 <= m * n <= 105
- 1 <= pattern.length <= m * n
- grid and pattern consist of only lowercase English letters.

---

## 题目（中文翻译）

给定一个大小为 `m × n` 的字符矩阵 `grid` 与一个字符串 `pattern`。  

**水平子串（horizontal substring）** 是指从左到右读取的连续字符序列。若在读取过程中到达行末但子串尚未完成，则会**换行（wrap）**到下一行的第一列继续读取。**不**会从最底部的行换回到顶部。  

**垂直子串（vertical substring）** 是指从上到下读取的连续字符序列。若在读取过程中到达列底但子串尚未完成，则会**换列（wrap）**到下一列的第一行继续读取。**不**会从最右侧的列换回到最左侧。  

统计矩阵中满足以下条件的单元格数量：该单元格同时属于至少一个匹配 `pattern` 的水平子串和至少一个匹配 `pattern` 的垂直子串。  

返回这些单元格的计数。

---

### 示例

**示例 1**

```
Input: grid = [["a","a","c","c"],
               ["b","b","b","c"],
               ["a","a","b","a"],
               ["c","a","a","c"],
               ["a","a","b","a"]], 
       pattern = "abaca"
Output: 1
Explanation:
模式 "abaca" 在矩阵中出现一次作为水平子串（蓝色标记），一次作为垂直子串（红色标记），两者在一个单元格处相交（紫色标记）。
```

**示例 2**

```
Input: grid = [["c","a","a","a"],
               ["a","a","b","a"],
               ["b","b","a","a"],
               ["a","a","b","a"]], 
       pattern = "aba"
Output: 4
Explanation:
上图标记的单元格均至少属于一个匹配模式 "aba" 的水平子串和一个匹配模式 "aba" 的垂直子串。
```

**示例 3**

```
Input: grid = [["a"]], 
       pattern = "a"
Output: 1
```

---

### 约束条件

- `m == grid.length`
- `n == grid[i].length`
- `1 ≤ m, n ≤ 1000`
- `1 ≤ m × n ≤ 10^5`
- `1 ≤ pattern.length ≤ m × n`
- `grid` 和 `pattern` 仅由小写英文字母组成。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每一个格子当作起点**，沿水平方向和竖直方向分别尝试把 `pattern` 逐字符匹配一次。  
- **水平子串**：从 `(r,c)` 向右走，走到行末时「换到下一行的第一列」继续走。  
- **垂直子串**：从 `(r,c)` 向下走，走到列底时「换到下一列的第一行」继续走。  

只要一次遍历把所有起点都检查完，就能知道哪些格子出现在**至少一个**水平匹配、**至少一个**垂直匹配中，最后统计两者都有的格子即可。

> **类比**：把网格想成一本书的页码。水平遍历像是顺序阅读整本书（从左到右、从一页的末尾直接翻到下一页的开头），而垂直遍历像是把书页重新排成列，再顺序阅读。我们只需要找出所有出现目标词的「页码」区间，然后看哪些页码在两本书里都被标记过。

**为什么正确**  
- 每一种合法的水平（或垂直）子串一定对应唯一的起点 `(r,c)`。遍历所有起点自然不会遗漏。  
- 只要匹配成功，就把子串覆盖的每个格子记下来；最后只要格子同时被水平和垂直记过，就满足题意。

**复杂度分析（大白话）**  
- 对每个格子都要尝试匹配 `len(pattern)` 次字符。假设网格有 `N = m·n` 个格子，模式长度记作 `L`。  
- 时间复杂度 ≈ `N × L`，如果 `N = 10⁵、L = 10⁵`，最坏会是 **10⁵ × 10⁵ = 10¹⁰** 步，显然会超时。  
- 空间上只需要保存网格本身和一些标记，**O(N)**（和网格大小同量级）。

#### 代码（Python）

```python
def brute_count(grid, pattern):
    m, n = len(grid), len(grid[0])
    L = len(pattern)
    # 记录每个格子是否被水平 / 垂直匹配覆盖
    hor = [[False] * n for _ in range(m)]
    ver = [[False] * n for _ in range(m)]

    # -------- 水平遍历 ----------
    for r in range(m):
        for c in range(n):
            ok = True
            cr, cc = r, c
            for k in range(L):
                if grid[cr][cc] != pattern[k]:
                    ok = False
                    break
                # 向右走一步，遇到行尾换到下一行第一列
                cc += 1
                if cc == n:
                    cc = 0
                    cr += 1
                    if cr == m:          # 已经到底，无法继续
                        ok = False
                        break
            if ok:
                # 把匹配的每个格子都标记为 True
                cr, cc = r, c
                for _ in range(L):
                    hor[cr][cc] = True
                    cc += 1
                    if cc == n:
                        cc = 0
                        cr += 1

    # -------- 垂直遍历 ----------
    for r in range(m):
        for c in range(n):
            ok = True
            cr, cc = r, c
            for k in range(L):
                if grid[cr][cc] != pattern[k]:
                    ok = False
                    break
                # 向下走一步，遇到底部换到下一列第一行
                cr += 1
                if cr == m:
                    cr = 0
                    cc += 1
                    if cc == n:          # 已经到最右列，无法继续
                        ok = False
                        break
            if ok:
                cr, cc = r, c
                for _ in range(L):
                    ver[cr][cc] = True
                    cr += 1
                    if cr == m:
                        cr = 0
                        cc += 1

    # -------- 统计交集 ----------
    ans = 0
    for i in range(m):
        for j in range(n):
            if hor[i][j] and ver[i][j]:
                ans += 1
    return ans
```

> 关键行都有中文注释，帮助读者一步步跟上思路。  

#### 复杂度

- **时间复杂度**：`O(N × L)`（`N = m·n`），因为对每个起点都要逐字符比较。  
  - 大白话：如果网格有 10 万格，模式长度也 10 万，那么这段代码要跑 **一千亿** 次字符比较，几乎不可能在 1 秒内完成。  
- **空间复杂度**：`O(N)`，只用了两个同样大小的布尔矩阵来记录水平、垂直是否覆盖。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次匹配都要逐字符比较**。我们可以把所有水平（或垂直）子串一次性预处理，利用**滚动哈希（Rolling Hash）**快速判断子串是否等于 `pattern`，而不必逐字符比较。

**核心观察**  

1. 把网格按**行主序**（左到右、行到行）展开成一维字符序列 `S_h`（长度 `N = m·n`）。  
   - 任意合法的水平子串在 `S_h` 中恰好是一个 **连续区间** `[start, start+L)`，只要 `start+L ≤ N`（不能跨到底部再回到顶部）。  
2. 把网格按**列主序**（上到下、列到列）展开成另一维字符序列 `S_v`。  
   - 任意合法的垂直子串在 `S_v` 中同样是连续区间 `[start, start+L)`，只要 `start+L ≤ N`（不能跨到最右列再回到左边）。  

这样，**水平匹配**和**垂直匹配**都转化为**在一维字符串中查找所有等长子串**的问题。

**滚动哈希**  
- 为每个字符映射一个整数（`a→1, b→2,…`），选一个基数 `B`（如 27）和一个大质数 `MOD`（如 10⁹+7）。  
- 预计算前缀哈希 `pref[i] = (pref[i-1] * B + val[i]) % MOD`，以及 `powB[k] = Bᵏ % MOD`。  
- 任意子串 `[l, r)` 的哈希可以 **O(1)** 通过  
  `hash(l,r) = (pref[r] - pref[l] * powB[r-l]) % MOD` 获得。  

于是我们只需一次线性遍历 `S_h`（和 `S_v`），检查每个起点的子串哈希是否等于模式的哈希，即可得到所有匹配的起点。

**如何高效统计被覆盖的格子**  

每一次匹配对应一段连续的下标区间 `[start, start+L)`。我们不必把这段里的每个格子都逐一标记，而是使用**差分数组 + 前缀和**的技巧：

- `diff[start]   += 1`  
- `diff[start+L] -= 1`  

遍历完所有匹配后，对 `diff` 做一次前缀累计，得到 `cover[i] > 0` 表示第 `i` 个位置被至少一次匹配覆盖。这样 **每段匹配只用 O(1) 时间** 标记，整体仍是线性 `O(N)`。

**最终计数**  

- 对水平得到的 `cover_h`（长度 `N`），对垂直得到的 `cover_v`（长度 `N`）。  
- 对每个格子 `(r,c)`，它在行主序中的下标是 `idx_h = r·n + c`，在列主序中的下标是 `idx_v = c·m + r`。  
- 若 `cover_h[idx_h]` 与 `cover_v[idx_v]` 均为 `True`，则该格子满足题意，计数+1。

整个流程：

1. 把网格分别转成行序列、列序列（O(N)）  
2. 计算模式哈希（O(L)）  
3. 对两条序列各做一次滚动哈希匹配，记录差分数组（O(N)）  
4. 前缀累计得到覆盖数组（O(N)）  
5. 逐格子检查交集计数（O(N)）  

**复杂度**  
- 时间：`O(N + L)`，线性级别。  
- 空间：`O(N)`，主要用于两条序列和差分数组。  

> 对比暴力：从 `O(N·L)` 降到 `O(N)`，在最坏 10⁵ 规模下轻松跑完。

#### 代码（Python）

```python
from typing import List

MOD = 1_000_000_007          # 大质数，防止哈希冲突
BASE = 27                    # 26 个字母 + 1

def char_val(ch: str) -> int:
    """把字符 a~z 映射到 1~26"""
    return ord(ch) - ord('a') + 1


def build_flat(grid: List[List[str]]) -> List[int]:
    """行主序展开为整数列表"""
    flat = []
    for row in grid:
        flat.extend([char_val(c) for c in row])
    return flat


def build_flat_col(grid: List[List[str]]) -> List[int]:
    """列主序展开为整数列表"""
    m, n = len(grid), len(grid[0])
    flat = []
    for c in range(n):
        for r in range(m):
            flat.append(char_val(grid[r][c]))
    return flat


def prefix_hash(arr: List[int]) -> List[int]:
    """返回前缀哈希数组，pref[0]=0，pref[i] 为前 i 个字符的哈希"""
    pref = [0] * (len(arr) + 1)
    for i, v in enumerate(arr, 1):
        pref[i] = (pref[i - 1] * BASE + v) % MOD
    return pref


def power_base(length: int) -> List[int]:
    """返回 BASE^k (mod MOD) for k = 0..length"""
    pw = [1] * (length + 1)
    for i in range(1, length + 1):
        pw[i] = (pw[i - 1] * BASE) % MOD
    return pw


def substring_hash(pref: List[int], pw: List[int], l: int, r: int) -> int:
    """返回区间 [l, r) 的哈希值（0-indexed）"""
    return (pref[r] - pref[l] * pw[r - l]) % MOD


def coverage_by_hash(seq: List[int], pat_hash: int, L: int, pw: List[int]) -> List[int]:
    """
    在整数序列 seq 中找所有长度为 L、哈希等于 pat_hash 的子串。
    使用差分数组记录每个位置是否被至少一次匹配覆盖，返回布尔列表（0/1）。
    """
    n = len(seq)
    diff = [0] * (n + 1)          # 多一个哨兵，方便写 diff[end]--
    pref = prefix_hash(seq)

    for start in range(0, n - L + 1):
        if substring_hash(pref, pw, start, start + L) == pat_hash:
            diff[start] += 1
            diff[start + L] -= 1

    cover = [0] * n
    cur = 0
    for i in range(n):
        cur += diff[i]
        cover[i] = 1 if cur > 0 else 0
    return cover


def count_cells(grid: List[List[str]], pattern: str) -> int:
    m, n = len(grid), len(grid[0])
    L = len(pattern)

    # ---------- 预处理 ----------
    # 1) 把 pattern 转成整数并求哈希
    pat_vals = [char_val(ch) for ch in pattern]
    pat_pref = prefix_hash(pat_vals)
    pw = power_base(L)                 # 只需要到 L 的幂
    pat_hash = pat_pref[L]             # 完整模式的哈希

    # 2) 行主序、列主序展开
    flat_h = build_flat(grid)          # 长度 m*n
    flat_v = build_flat_col(grid)      # 长度 m*n

    # ---------- 找匹配 ----------
    cover_h = coverage_by_hash(flat_h, pat_hash, L, pw)   # 行覆盖
    cover_v = coverage_by_hash(flat_v, pat_hash, L, pw)   # 列覆盖

    # ---------- 统计交集 ----------
    ans = 0
    for r in range(m):
        for c in range(n):
            idx_h = r * n + c          # 行主序下标
            idx_v = c * m + r          # 列主序下标
            if cover_h[idx_h] and cover_v[idx_v]:
                ans += 1
    return ans
```

**代码要点注释（中文）**  

- `char_val`：把字符映射为数字，方便哈希运算。  
- `build_flat` / `build_flat_col`：分别把网格展平成「阅读顺序」的线性数组。  
- `prefix_hash` 与 `substring_hash`：滚动哈希的核心，能够 **O(1)** 取任意子串的哈希。  
- `coverage_by_hash`：利用差分数组一次性标记所有匹配区间，最后得到每个位置是否被覆盖。  
- 主函数 `count_cells`：先求模式哈希 → 行/列展开 → 找匹配 → 用下标对应关系统计交集。

#### 复杂度

- **时间复杂度**：`O(m·n + |pattern|)`  
  - 展开两次序列、预计算前缀哈希、遍历一次找匹配、一次前缀累计、一次格子遍历，全部都是线性。  
  - 大白话：网格有 10 万格，模式 10 万字符，总共只做了几次「过一遍」的操作，毫秒级就能完成。

- **空间复杂度**：`O(m·n)`  
  - 需要保存行序列、列序列以及两条差分/覆盖数组，大小都是 `m·n`，在题目给的上限 `10⁵` 以内完全可以接受。  

> 与暴力解相比：时间从 **指数级**（`N·L`）下降到 **线性**（`N`），空间保持在同一数量级，性能提升巨大。

---

## 心得

- **核心技巧**：把二维网格的“环形读取”抽象为一维字符串的**连续子串**，再利用**滚动哈希 + 差分数组**快速定位并统计覆盖区间。  
- **适用场景**：  
  1. 在矩阵中寻找固定长度、可“换行/换列”读取的子串（如本题）。  
  2. 大规模字符串匹配，需要一次性找出所有等长匹配（如 DNA 序列的滑动窗口匹配）。  
  3. 需要统计多段区间交集或覆盖情况的题目（利用差分数组+前缀和）。  
- **一句话总结**：把二维“环形”读取化为一维连续子串，用滚动哈希一次遍历找全部匹配，再用差分数组把匹配区间高效标记。

---

## 反思

- **第一反应**：直接在二维上暴力搜索，忘记了可以把读取顺序“线性化”。  
- **最易踩的坑**  
  - **边界**：水平子串不能跨到底部再回到顶部，垂直子串不能跨到最右列再回左边。实现时必须限制 `start + L ≤ m·n`。  
  - **哈希冲突**：单模可能出现极小概率冲突，实际竞赛中可使用双模或在冲突时再做一次字符比较。这里为简洁使用单模。  
  - **差分数组的哨兵**：`diff` 长度要比序列多 1，防止 `diff[end]` 越界。  
- **下次思路**：一看到“在矩阵中按行/列读取且可以换行/换列”的描述，立刻尝试把问题转化为 **一维连续子串**，再考虑 **哈希 / KMP / Z‑algorithm** 等线性匹配算法，配合 **区间差分** 来统计覆盖。这样可以把二维的复杂度降到线性。