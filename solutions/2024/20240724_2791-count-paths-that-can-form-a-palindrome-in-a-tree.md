# #2791. 统计树中可形成回文的路径数 / Count Paths That Can Form a Palindrome in a Tree

> 难度：困难 · 标签：Dynamic Programming、Bit Manipulation、Tree、Depth-First Search、Bitmask · [LeetCode 链接](https://leetcode.com/problems/count-paths-that-can-form-a-palindrome-in-a-tree/)

---

## 题目（英文原版）

**Description**

You are given a tree (i.e. a connected, undirected graph that has no cycles) rooted at node 0 consisting of n nodes numbered from 0 to n - 1. The tree is represented by a 0-indexed array parent of size n, where parent[i] is the parent of node i. Since node 0 is the root, parent[0] == -1.
You are also given a string s of length n, where s[i] is the character assigned to the edge between i and parent[i]. s[0] can be ignored.
Return the number of pairs of nodes (u, v) such that u < v and the characters assigned to edges on the path from u to v can be rearranged to form a palindrome.
A string is a palindrome when it reads the same backwards as forwards.

**Examples**

**Example 1:**

```
Input: parent = [-1,0,0,1,1,2], s = "acaabc"
Output: 8
Explanation: The valid pairs are:
- All the pairs (0,1), (0,2), (1,3), (1,4) and (2,5) result in one character which is always a palindrome.
- The pair (2,3) result in the string "aca" which is a palindrome.
- The pair (1,5) result in the string "cac" which is a palindrome.
- The pair (3,5) result in the string "acac" which can be rearranged into the palindrome "acca".
```

**Example 2:**

```
Input: parent = [-1,0,0,0,0], s = "aaaaa"
Output: 10
Explanation: Any pair of nodes (u,v) where u < v is valid.
```

**Constraints**

- n == parent.length == s.length
- 1 <= n <= 105
- 0 <= parent[i] <= n - 1 for all i >= 1
- parent[0] == -1
- parent represents a valid tree.
- s consists of only lowercase English letters.

---

## 题目（中文翻译）

你被给定了一棵以节点 0 为根的树（tree），即一张连通的无向无环图，包含 n 个节点，编号为 0 到 n‑1。树通过一个大小为 n 的 0‑索引数组 `parent` 表示，其中 `parent[i]` 是节点 i 的父节点。由于节点 0 为根，`parent[0] == -1`。

同时给定一个长度为 n 的字符串 `s`，其中 `s[i]` 是节点 i 与其父节点 `parent[i]` 之间的边（edge）上标记的字符。`s[0]` 可忽略。

请返回满足以下条件的节点对 `(u, v)` 的数量（要求 `u < v`）：
- 从节点 u 到节点 v 的路径上所有边的字符，经过重新排列后可以组成一个回文（palindrome）。

回文是指正读和反读完全相同的字符串。

**示例 1**

```text
Input: parent = [-1,0,0,1,1,2], s = "acaabc"
Output: 8
Explanation:
满足条件的节点对有：
- 所有 (0,1)、(0,2)、(1,3)、(1,4) 与 (2,5) 这几对路径仅包含一个字符，显然是回文。
- 对 (2,3) 的路径得到字符串 "aca"，是回文。
- 对 (1,5) 的路径得到字符串 "cac"，是回文。
- 对 (3,5) 的路径得到字符串 "acac"，可以重新排列成回文。
```

**示例 2**

```text
Input: parent = [-1,0,0,0,0], s = "aaaaa"
Output: 10
Explanation:
任意满足 u < v 的节点对都有效，因为路径上的字符全为相同字符，必能组成回文。
```

**约束条件**

- `n == parent.length == s.length`
- `1 <= n <= 10^5`
- 对所有 `i >= 1`，`0 <= parent[i] <= n - 1`
- `parent[0] == -1`
- `parent` 构成一棵有效的树
- `s` 仅由小写英文字母组成

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **所有** 节点对 `(u, v)`（要求 `u < v`）都枚举一遍，求出它们之间的路径上对应的字符序列，然后判断这段序列能否重新排列成回文。

- **路径的获取**  
  树是无环的，任意两点之间的唯一路径可以通过 “向上走到公共祖先再向下” 的方式得到。我们可以把每个节点的父节点保存在 `parent` 数组里，先把 `u` 和 `v` 分别往上爬，直到两条链路相交（即找到了最近公共祖先 LCA），把沿途的字符记录下来，就是 `u → v` 的路径字符序列。

- **回文判定**  
  一个字符串能够排列成回文，当且仅当 **出现奇数次数的字符不超过 1 个**。我们可以遍历这段字符，用一个长度为 26 的计数数组统计每个字母出现的次数，最后统计奇数次数的种类数是否 ≤ 1。

- **为什么正确**  
  暴力遍历 **不遗漏** 任意合法的 `(u, v)`，对每一对都做了严格的回文判定，所以答案一定是完整的。

- **复杂度分析（大白话）**  
  - 枚举节点对的次数是 `C(n,2) = n·(n-1)/2`，大约是 `n²/2`，这就像把所有学生两两配对，人数多了配对的次数就会呈二次方增长。  
  - 对每一对我们要找公共祖先并收集路径字符，最坏情况下要走到根节点，路径长度最多 `O(n)`。于是总时间是 `O(n³)`（实际略好，因为路径长度平均会小于 `n`，但仍然远远超出题目要求）。  
  - 只用了几个计数数组和递归栈，空间是 `O(n)`（存储树和父指针），几乎不占内存。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def count_palindrome_paths_bruteforce(parent: List[int], s: str) -> int:
    n = len(parent)
    # 建立邻接表，方便向上遍历（这里只用 parent，下面直接用 parent 数组）
    ans = 0

    # 辅助函数：返回 u->v 路径上字符的列表（不包括根节点的字符）
    def get_path_chars(u: int, v: int) -> List[str]:
        # 记录从 u 到根的路径以及对应字符
        path_u, chars_u = [], []
        while u != -1:
            path_u.append(u)
            if u != 0:               # s[0] 没有意义，根到根的边不计入
                chars_u.append(s[u])
            u = parent[u]

        # 同理记录 v 到根的路径
        path_v, chars_v = [], []
        while v != -1:
            path_v.append(v)
            if v != 0:
                chars_v.append(s[v])
            v = parent[v]

        # 找到最近公共祖先（第一个相同的节点）
        i, j = len(path_u) - 1, len(path_v) - 1
        while i >= 0 and j >= 0 and path_u[i] == path_v[j]:
            i -= 1
            j -= 1

        # u→LCA 的字符（逆序），再加上 LCA→v 的字符（正序）
        # chars_u 是从 u 往上收集的，所以需要反转
        return chars_u[:i+1][::-1] + chars_v[:j+1]

    # 判定字符列表能否排列成回文
    def can_form_palindrome(chars: List[str]) -> bool:
        cnt = [0] * 26
        for ch in chars:
            cnt[ord(ch) - ord('a')] += 1
        odd = sum(c % 2 for c in cnt)
        return odd <= 1

    # 暴力枚举所有节点对
    for u in range(n):
        for v in range(u + 1, n):
            path_chars = get_path_chars(u, v)
            if can_form_palindrome(path_chars):
                ans += 1
    return ans
```

> **关键注释**  
> - `chars_u[:i+1][::-1]`：取出从 `u` 到 LCA（不包括 LCA）的字符，逆序是因为我们是从 `u` 向上走的。  
> - `odd = sum(c % 2 for c in cnt)`：统计出现奇数次的字符种类数，若 ≤ 1 即可排列成回文。

#### 复杂度

- **时间复杂度**：`O(n³)`（遍历 `≈ n²/2` 对，每对最坏走 `O(n)` 条边）  
  - “O(n³)” 其实可以想象成 “把 `n` 本书每本都和其他每本拼成三本书的组合”，数量级非常大，根本跑不完。

- **空间复杂度**：`O(n)`（保存父指针数组和递归栈）  
  - 只用了和节点数成线性关系的额外空间，基本不算多。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次都要把路径上的字符全部收集出来再检查，这导致了 `O(n³)` 的时间。  
我们需要 **在遍历一次树的过程中**，直接得到每条路径是否满足回文条件。

**关键观察 1**：  
一条字符串能否排列成回文，只和每个字母出现的 **奇偶性** 有关。  
- 把 26 个小写字母对应到 26 位二进制位，`1` 表示该字母出现了奇数次，`0` 表示出现偶数次。  
- 对于一条路径上的字符序列，用这种方式得到的二进制数我们叫 **mask**。

**关键观察 2**：  
设 `mask[x]` 为根 `0` 到节点 `x` 路径上字符的奇偶性掩码。  
则两点 `u、v` 之间的路径字符掩码等于 `mask[u] XOR mask[v]`（因为公共前缀的奇偶性会相互抵消）。  

**回文条件** 用掩码来写就是：  
`mask[u] XOR mask[v]` 中 **至多只有一位是 1**（即 0 位或 1 位的 1），因为只有 0 位或 1 位字符出现奇数次。

**关键观察 3**：  
遍历树时，如果我们已经统计了 **已经访问过的节点的 mask 出现次数**，那么对当前节点 `v`，只要找出满足下式的已有 mask，就能立即知道有多少条有效路径以 `v` 为终点：

```
mask[v] == mask[prev]                     （奇数字符为 0 个）
mask[v] == mask[prev] ^ (1 << k)   (k = 0..25)   （奇数字符为 1 个）
```

这相当于在 **哈希表**（Python 的 `defaultdict(int)`）里做 27 次查找（一次相等、26 次翻转一位），时间是常数级别。

**算法步骤**（一次深度优先搜索）：

1. 先把树的邻接表建好（因为是无向的，父子两边都要连）。
2. 初始化 `cnt = defaultdict(int)`，并把根的 mask `0` 放进去（根到根的路径为空，掩码为 0）。
3. 用 DFS 从根出发，维护当前路径的 `mask`（从根到当前节点的奇偶性）。
4. 对于当前节点 `v`：  
   - 统计 `cnt[mask]`（与之前相同的 mask）以及 `cnt[mask ^ (1<<k)]`（翻转任意一位）的总和，加到答案 `ans` 中。  
   - 然后把 `cnt[mask] += 1`，继续递归遍历子节点。  
   - 递归返回后要 **回溯**：`cnt[mask] -= 1`，否则会把已经离开的子树计入后面的查询。
5. 完成遍历后 `ans` 即为满足条件的节点对数。

**为什么正确**  
- `mask[u] XOR mask[v]` 正好是 `u→v` 路径上每个字母出现次数的奇偶性。  
- 当它的二进制表示的 **1 的个数 ≤ 1** 时，路径字符可以排列成回文。  
- 我们在遍历到 `v` 时，枚举了所有已经出现过的 `mask[u]`（即 `u` 在 `v` 的祖先或已经遍历过的其它分支），并检查了 “相等” 与 “相差一位” 两种情况，恰好覆盖了所有合法的 `u`。  
- 通过哈希表的计数，我们把 “遍历所有已出现的 `u`” 从线性变成了常数查询，保证了整体 `O(n·26)` 的时间。

**复杂度（大白话）**  
- **时间**：每个节点做 27 次哈希查找/更新，`27 ≈ 常数`，所以整体是 `O(26·n) ≈ O(n)`，和节点数成线性关系，跑得非常快。  
- **空间**：哈希表里最多存 `n` 条不同的 mask（最坏每个节点的掩码都不相同），再加递归栈深度 `O(n)`，总体 `O(n)`。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def count_palindrome_paths(parent: List[int], s: str) -> int:
    n = len(parent)

    # ---------- 1. 建图 ----------
    # 因为是无向树，父子两边都要连
    g = [[] for _ in range(n)]
    for i in range(1, n):
        p = parent[i]
        g[p].append(i)
        g[i].append(p)

    # ---------- 2. DFS + 哈希计数 ----------
    cnt = defaultdict(int)   # 已经遍历到的节点的 mask 出现次数
    cnt[0] = 1                # 根节点的 mask 为 0，先放进去（路径长度为 0 的情况）

    ans = 0

    def dfs(v: int, parent_node: int, mask: int) -> None:
        """
        v: 当前访问的节点
        parent_node: 防止回到父节点
        mask: 从根到 v 的字符奇偶性掩码
        """
        nonlocal ans

        # ---------- 3. 统计以 v 为终点的合法路径 ----------
        # ① 与已有相同 mask 的节点配对（奇数字符为 0）
        ans += cnt[mask]

        # ② 与已有 mask 只相差一位的节点配对（奇数字符为 1）
        for k in range(26):                # 逐个翻转第 k 位
            ans += cnt[mask ^ (1 << k)]

        # ---------- 4. 将当前 mask 加入统计 ----------
        cnt[mask] += 1

        # ---------- 5. 继续遍历子树 ----------
        for nxt in g[v]:
            if nxt == parent_node:
                continue
            # 计算子节点的 mask：在父路径上再加上这条边的字符
            # s[nxt] 对应的是 edge (parent[nxt], nxt)
            nxt_mask = mask ^ (1 << (ord(s[nxt]) - ord('a')))
            dfs(nxt, v, nxt_mask)

        # ---------- 6. 回溯：离开子树后把当前节点的计数减掉 ----------
        cnt[mask] -= 1

    # 从根节点 0 开始，根本身没有对应字符（s[0] 可以忽略），mask = 0
    dfs(0, -1, 0)
    return ans
```

> **代码要点解释**  
> - `mask ^ (1 << k)`：把第 `k` 位取反，相当于假设路径上只剩下字母 `k` 出现奇数次。  
> - `cnt[0] = 1`：把根自身算进去，这样在遍历根的直接子节点时，`mask == 0` 的配对会自动计入（单条边本身就是回文）。  
> - `dfs` 的 `parent_node` 参数防止在无向图里“回到父亲”。  
> - `cnt[mask] -= 1` 是必须的回溯步骤，否则后面的子树会把已经离开的节点错误地算进来。

#### 复杂度

- **时间复杂度**：`O(26·n) = O(n)`  
  - 27 次常数级哈希操作对每个节点都做一次，整体随节点数线性增长。  
  - 与暴力解的 `O(n³)` 相比，简直是“跑步”和“爬山”级别的差距。

- **空间复杂度**：`O(n)`  
  - 哈希表最多存 `n` 条不同的 mask，递归栈深度最坏为 `n`（链状树），总体线性。

---

## 心得

- **核心技巧**：**位掩码 + 前缀异或 + 哈希计数**。  
  把字符出现的奇偶性压成 26 位整数，利用前缀异或的性质把路径查询转化为 “两个前缀的异或”。随后只需检查 **0 位或 1 位** 的情况。

- **适用的题型**（类似思路）  
  1. “路径上字母出现次数最多为一次” → 例如 LeetCode 1542. **找出最长的好子串**（使用位掩码）  
  2. “树上两点路径的奇偶性满足条件” → 例如 LeetCode 2421. **好路径数**（同样用前缀异或计数）  
  3. “子数组/子序列中至多一位出现奇数次” → 例如 LeetCode 1542. **好子串**（数组版）

- **一句话总结解题钥匙**：  
  **“把路径的字符奇偶性压成位掩码，用前缀异或把路径问题变成两点掩码的相等/相差一位的计数”**。

---

## 反思

- **第一反应**：看到“回文”二字，立刻想到“奇数次数的字符 ≤ 1”。随后联想到“位运算”可以高效记录奇偶性。  
- **最容易踩的坑**  
  1. **根节点的字符**：`s[0]` 是无意义的，需要在计算子节点 mask 时使用 `s[child]` 而不是 `s[parent]`。  
  2. **计数顺序**：在统计当前节点的配对数之前 **不能先把它加入哈希表**，否则会把 `(v, v)` 这类无效对计入。  
  3. **回溯**：DFS 结束后忘记 `cnt[mask] -= 1` 会导致后续子树误把已经离开的节点算进去，答案会暴涨。  
  4. **整数位数**：Python 的整数是无限位的，直接使用位移即可，但要确保 `1 << (ord(ch)-ord('a'))` 不越界（这里 0~25 完全安全）。

- **下次遇到同类题**：  
  第一步先把“是否只关心出现次数的奇偶性”这一点写成 **位掩码**，然后思考“路径/子数组的属性能否用前缀 XOR 表示”，最后用 **哈希表**统计满足 “异或结果位数 ≤ 1” 的配对数。这样思路自然导向最优解。