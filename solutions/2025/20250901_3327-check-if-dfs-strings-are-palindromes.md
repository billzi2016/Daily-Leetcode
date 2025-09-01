# #3327. **检查 DFS 字符串是否为回文** / Check if DFS Strings Are Palindromes

> 难度：困难 · 标签：Array、Hash Table、String、Tree、Depth-First Search、Hash Function · [LeetCode 链接](https://leetcode.com/problems/check-if-dfs-strings-are-palindromes/)

---

## 题目（英文原版）

**Description**

You are given a tree rooted at node 0, consisting of n nodes numbered from 0 to n - 1. The tree is represented by an array parent of size n, where parent[i] is the parent of node i. Since node 0 is the root, parent[0] == -1.
You are also given a string s of length n, where s[i] is the character assigned to node i.
Consider an empty string dfsStr, and define a recursive function dfs(int x) that takes a node x as a parameter and performs the following steps in order:
Note that dfsStr is shared across all recursive calls of dfs.
You need to find a boolean array answer of size n, where for each index i from 0 to n - 1, you do the following:
Return the array answer.

**Examples**

**Example 1:**

```
Input: parent = [-1,0,0,1,1,2], s = "aababa"
Output: [true,true,false,true,true,true]
Explanation:
```

**Example 2:**

```
Input: parent = [-1,0,0,0,0], s = "aabcb"
Output: [true,true,true,true,true]
Explanation:
Every call on dfs(x) results in a palindrome string.
```

**Constraints**

- n == parent.length == s.length
- 1 <= n <= 105
- 0 <= parent[i] <= n - 1 for all i >= 1.
- parent[0] == -1
- parent represents a valid tree.
- s consists only of lowercase English letters.

---

## 题目（中文翻译）

给定一棵以节点 `0` 为根的树，树中共有 `n` 个节点，编号为 `0` 到 `n - 1`。树通过大小为 `n` 的数组 `parent` 表示，其中 `parent[i]` 为节点 `i` 的父节点。由于 `0` 为根节点，`parent[0] == -1`。

同时给定一个长度为 `n` 的字符串 `s`，其中 `s[i]` 是分配给节点 `i` 的字符。

设有一个初始为空的字符串 `dfsStr`，并定义一个递归函数 `dfs(int x)`，该函数以节点 `x` 为参数并按以下顺序执行若干步骤：

> **注意**：`dfsStr` 在所有递归调用之间是共享的。

你的任务是求出一个大小为 `n` 的布尔数组 `answer`，对每个下标 `i`（`0 ≤ i < n`）执行如下操作：

（此处应填写对 `dfs(i)` 的具体调用及对应的判断逻辑，原题描述中已省略）

返回数组 `answer`。

---

### 示例

**示例 1**  
输入：`parent = [-1,0,0,1,1,2]`, `s = "aababa"`  
输出：`[true,true,false,true,true,true]`  
解释：  
（此处为对每一次 `dfs(i)` 产生的字符串是否为回文的说明，原题中未给出具体内容）

**示例 2**  
输入：`parent = [-1,0,0,0,0]`, `s = "aabcb"`  
输出：`[true,true,true,true,true]`  
解释：  
每一次对 `dfs(x)` 的调用都得到一个回文字符串。

---

### 约束条件

- `n == parent.length == s.length`
- `1 <= n <= 10^5`
- 对所有 `i ≥ 1`，`0 <= parent[i] <= n - 1`
- `parent[0] == -1`
- `parent` 构成一棵有效的树
- `s` 只包含小写英文字母

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把树从根 `0` 按 **深度优先搜索（DFS）** 的顺序遍历一次，记录遍历过程中每访问到的节点对应的字符，得到一条大字符串 `dfsStr`（相当于把所有节点排成一行）。  
对于每个节点 `i`，它的子树里所有节点在 `dfsStr` 中出现的区间是 **连续的**（因为 DFS 先进入子树，全部走完后才回到父亲继续）。  
于是只要把这个区间切出来，检查它是不是回文字符串，就得到 `answer[i]`。

> **数据结构类比**  
> - **树的子树** 就像一本书的章节，章节内部的页码是连续的。  
> - **DFS 顺序** 相当于把整本书的页码一次性写在一条长长的纸上。  
> - **子树对应的区间** 就是这条纸上连续的一段文字。

**暴力实现**  
1. 先做一次普通的 DFS，记录每个节点的进入时间 `tin[i]`（在 `dfsStr` 中的左端点）和离开时间 `tout[i]`（右端点，左闭右开）。  
2. 对每个节点 `i`，取 `dfsStr[tin[i]:tout[i]]`，用普通的回文判断（从两端向中间比较）得到 `answer[i]`。

> **为什么正确**  
> - DFS 的特性保证子树节点在遍历序列中是连续的。  
> - 回文判断只看这段文字本身，不受其它节点影响。  

> **复杂度分析（大白话）**  
> - **时间**：对每个节点都要把它子树对应的那段文字逐字符比较一次。最坏情况下，根节点的子树就是整棵树，长度是 `n`，第二层节点各自的子树长度大约是 `n/2`，如此累加会得到 **≈ n²/2** 次比较，记作 **O(n²)**。  
> - **空间**：除了保存树结构和 `dfsStr`，只需要 `tin / tout` 两个长度为 `n` 的数组，都是 **O(n)** 的额外空间。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def brute_force(parent: List[int], s: str) -> List[bool]:
    n = len(parent)

    # ---------- 1. 建图 ----------
    tree = defaultdict(list)
    for child in range(1, n):
        p = parent[child]
        tree[p].append(child)

    # ---------- 2. DFS 收集遍历序列 ----------
    dfs_order = []          # 保存遍历时的节点编号
    tin = [0] * n           # 进入时间（左端点）
    tout = [0] * n          # 离开时间（右端点，左闭右开）

    def dfs(u: int):
        tin[u] = len(dfs_order)          # 记录左端点
        dfs_order.append(u)              # 进入 u 时写入
        for v in tree[u]:
            dfs(v)                        # 递归遍历子树
        tout[u] = len(dfs_order)         # 记录右端点

    dfs(0)                                # 从根节点开始

    # ---------- 3. 把节点编号映射成字符 ----------
    dfs_str = ''.join(s[node] for node in dfs_order)

    # ---------- 4. 暴力检查每个子树是否是回文 ----------
    ans = [False] * n
    for i in range(n):
        l, r = tin[i], tout[i]            # 子树对应的区间 [l, r)
        sub = dfs_str[l:r]                # 取出子树的字符串
        # 两端指针向中间比较
        ok = True
        left, right = 0, len(sub) - 1
        while left < right:
            if sub[left] != sub[right]:
                ok = False
                break
            left += 1
            right -= 1
        ans[i] = ok

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：最坏情况下根节点要检查 `n` 长度的子串，第二层节点各检查约 `n/2`，如此累加大约是 `n²/2` 次字符比较，仍然算作二次方时间。

- **空间复杂度**：`O(n)`  
  解释：除了原始输入外，只用了 `tree、dfs_order、tin、tout、dfs_str` 等线性大小的数组。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每个节点都要重新遍历它的子树字符串**。如果能够在 **一次遍历** 中把所有子树的回文信息算出来，就能把时间降到线性。

关键观察：

1. **子树对应的区间是连续的**（前面已经说明）。于是每个子树的回文判断只和这条长字符串的两个子区间有关。
2. 判断一个子串是否为回文，只需要它的 **前缀哈希** 与 **逆向前缀哈希** 相等。  
   - 前缀哈希就像查字典：把每个字符当成“单词”，用一个基数（比如 `131`）把左到右的字符序列压成一个唯一的数字（取模防溢出）。  
   - 逆向前缀哈希把字符顺序反过来压成数字。  
   - 两个哈希相等 → 极大概率是同一个字符串 → 回文。

3. 只要在 **DFS 期间** 记录下 `tin / tout`，并在 **遍历完所有节点后** 预先算出 **前缀哈希** 与 **逆向前缀哈希**，随后每个节点的回文判断可以 **O(1)** 完成。

下面一步步实现：

*Step 1 – DFS 收集顺序*  
和暴力解一样，做一次普通的递归 DFS，得到 `order`（节点访问顺序）以及每个节点的 `tin / tout`。  
`order` 长度恰好是 `n`，因为我们只在 **进入节点** 时写入一次字符（不写出时的“回退”字符），所以子树对应的区间正好是 `[tin, tout)`。

*Step 2 – 把节点映射成字符序列*  
`dfs_str = ''.join(s[node] for node in order)`。

*Step 3 – 预计算哈希*  
选两个大质数模数 `mod1 = 10**9+7`、`mod2 = 10**9+9`，以及基数 `base = 91138233`（任选一个大于字母表大小的整数）。  
对 `dfs_str` 计算两套前缀哈希 `pref1, pref2`（正向）和两套逆向前缀哈希 `rev1, rev2`（从右往左）。  
哈希的递推公式：

```
pref[i+1] = (pref[i] * base + code(ch)) % mod
rev[i+1]  = (rev[i]  * base + code(ch_rev)) % mod
```

其中 `code(ch) = ord(ch) - ord('a') + 1`（把字符映射到 1~26 的整数）。

我们还需要 **幂数组** `pow[i] = base^i % mod`，用来在 O(1) 内求任意子串的哈希：

```
hash(l, r) = (pref[r] - pref[l] * pow[r-l]) % mod   # 左闭右开区间 [l, r)
```

*Step 4 – O(1) 判断回文*  
对于节点 `i`，子树对应的区间是 `[L, R) = [tin[i], tout[i])`，长度 `len = R-L`。  
子串正向哈希 `h1 = get_hash(pref1, L, R, mod1)`（同理 `h2`），逆向哈希要在 **倒序字符串** 上取对应区间。  
因为倒序字符串的下标是 `n - R` 到 `n - L`，所以：

```
rh1 = get_hash(rev1, n-R, n-L, mod1)
```

如果 `(h1 == rh1) and (h2 == rh2)`，则几乎可以肯定子串是回文（双模数可以把碰撞概率压到几乎为 0）。

这样每个节点只做常数次算术运算，整体 **时间 O(n)**，**空间 O(n)**。

> **为什么 Manacher 也能做**  
> Manacher 能一次性得到每个中心的最大回文半径。若子树区间恰好以某个中心为中心且半径覆盖整个区间，则该子树是回文。实现上略显繁琐，而滚动哈希实现更直观，下面采用哈希方案。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Tuple

MOD1 = 1_000_000_007
MOD2 = 1_000_000_009
BASE = 91138233          # 任意大于 26 的正整数

def build_hash(s: str, mod: int) -> Tuple[List[int], List[int]]:
    """
    返回 (前缀哈希数组, 幂数组)。
    pref[i] = 前 i 个字符的哈希，pref[0] = 0
    pow[i]  = BASE^i % mod
    """
    n = len(s)
    pref = [0] * (n + 1)
    powb = [1] * (n + 1)
    for i, ch in enumerate(s):
        code = ord(ch) - ord('a') + 1
        pref[i + 1] = (pref[i] * BASE + code) % mod
        powb[i + 1] = (powb[i] * BASE) % mod
    return pref, powb

def get_sub_hash(pref: List[int], powb: List[int],
                 l: int, r: int, mod: int) -> int:
    """
    计算子串 s[l:r]（左闭右开）的哈希值，时间 O(1)。
    """
    return (pref[r] - pref[l] * powb[r - l]) % mod

def optimal(parent: List[int], s: str) -> List[bool]:
    n = len(parent)

    # ---------- 1. 建图 ----------
    tree = defaultdict(list)
    for child in range(1, n):
        tree[parent[child]].append(child)

    # ---------- 2. DFS，记录访问顺序 ----------
    order = []                # 记录进入节点的顺序
    tin = [0] * n
    tout = [0] * n

    def dfs(u: int):
        tin[u] = len(order)   # 进入 u 时的左端点
        order.append(u)       # 只在进入时写入一次字符
        for v in tree[u]:
            dfs(v)
        tout[u] = len(order)  # 结束时的右端点（左闭右开）

    dfs(0)

    # ---------- 3. 把节点序列映射成字符序列 ----------
    dfs_str = ''.join(s[node] for node in order)

    # ---------- 4. 预计算正向和逆向哈希 ----------
    pref1, pow1 = build_hash(dfs_str, MOD1)
    pref2, pow2 = build_hash(dfs_str, MOD2)

    rev_str = dfs_str[::-1]                     # 逆序字符串
    rpref1, _ = build_hash(rev_str, MOD1)       # 逆向哈希只需要前缀和幂
    rpref2, _ = build_hash(rev_str, MOD2)

    # ---------- 5. O(1) 判断每个子树是否为回文 ----------
    ans = [False] * n
    for i in range(n):
        L, R = tin[i], tout[i]          # 子树在 dfs_str 中的区间 [L, R)
        # 正向哈希
        h1 = get_sub_hash(pref1, pow1, L, R, MOD1)
        h2 = get_sub_hash(pref2, pow2, L, R, MOD2)

        # 逆向哈希：对应逆序字符串的区间是 [n-R, n-L)
        rh1 = get_sub_hash(rpref1, pow1, n - R, n - L, MOD1)
        rh2 = get_sub_hash(rpref2, pow2, n - R, n - L, MOD2)

        ans[i] = (h1 == rh1) and (h2 == rh2)

    return ans
```

**代码要点注释**  

- `tree`：把父数组转成邻接表，类似把“家族关系表”变成“孩子列表”。  
- `tin / tout`：记录每个节点在遍历序列中的左、右端点，**左闭右开**，方便后面切片。  
- `order`：相当于把所有节点排成一列，根在最前，子树连续。  
- `build_hash`：一次遍历算出前缀哈希和基数幂，后面取子串哈希只需要常数时间。  
- `rev_str` 与逆向哈希：把整条字符串倒过来，子树在原序列的 `[L,R)` 对应倒序的 `[n-R, n-L)`，这样就能直接比较正向哈希与逆向哈希。  
- 双模数 (`MOD1`, `MOD2`)：防止极端碰撞，几乎可以保证判断的正确性。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - DFS 遍历一次 `O(n)`。  
  - 计算两套前缀哈希、幂数组各 `O(n)`。  
  - 对每个节点做常数次算术运算 `O(n)`。  
  与暴力的二次方相比，提升到了线性。

- **空间复杂度**：`O(n)`  
  - 需要存储树的邻接表、DFS 顺序、`tin/tout`、以及四套前缀哈希和幂数组，都是线性规模。

---

## 心得

- **核心技巧**：利用 **DFS 的欧拉序（子树对应连续区间）** + **滚动哈希（双模数）** 在 O(1) 时间内判断任意子串是否为回文。  
- **适用场景**：  
  1. “子树/子数组是否满足某种可通过前缀/后缀比较判定的性质”。  
  2. “在一条长字符串中快速判断多个区间是否是回文”。  
  3. “在树或图的遍历序列上做区间查询（如最大/最小值、异或等）”。  
- **一句话总结**：把树的子树映射成 **连续的字符串区间**，再用 **前缀哈希** 把回文判断压到常数时间。

---

## 反思

- **第一反应**：看到“DFS + 子树字符串是回文”，立刻想到 **枚举子树**、**直接拼接字符串** 再判断，结果是暴力 O(n²)。  
- **最容易踩的坑**：  
  - 忘记子树在 **DFS 进入顺序** 而不是后序顺序是连续的（后序会出现交叉）。  
  - 哈希取模时出现负数，需要再加上模数再取模。  
  - 单模数哈希有极小概率冲突，使用双模数更安全。  
- **下次思路**：  
  1. 首先确认子树对应的 **区间属性**（连续/不连续）。  
  2. 判断要检查的性质是否可以 **用前缀信息** 快速得到（如回文 → 前缀哈希、子数组和 → 前缀和）。  
  3. 若可以，直接把 **区间查询** 降到 O(1)；若不行，再考虑更高级的数据结构（线段树、莫队等）。