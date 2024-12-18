# #2977. 最小转换字符串成本 II / Minimum Cost to Convert String II

> 难度：困难 · 标签：Array、String、Dynamic Programming、Graph、Trie、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/minimum-cost-to-convert-string-ii/)

---

## 题目（英文原版）

**Description**

You are given two 0-indexed strings source and target, both of length n and consisting of lowercase English characters. You are also given two 0-indexed string arrays original and changed, and an integer array cost, where cost[i] represents the cost of converting the string original[i] to the string changed[i].
You start with the string source. In one operation, you can pick a substring x from the string, and change it to y at a cost of z if there exists any index j such that cost[j] == z, original[j] == x, and changed[j] == y. You are allowed to do any number of operations, but any pair of operations must satisfy either of these two conditions:
Return the minimum cost to convert the string source to the string target using any number of operations. If it is impossible to convert source to target, return -1.
Note that there may exist indices i, j such that original[j] == original[i] and changed[j] == changed[i].

**Examples**

**Example 1:**

```
Input: source = "abcd", target = "acbe", original = ["a","b","c","c","e","d"], changed = ["b","c","b","e","b","e"], cost = [2,5,5,1,2,20]
Output: 28
Explanation: To convert "abcd" to "acbe", do the following operations:
- Change substring source[1..1] from "b" to "c" at a cost of 5.
- Change substring source[2..2] from "c" to "e" at a cost of 1.
- Change substring source[2..2] from "e" to "b" at a cost of 2.
- Change substring source[3..3] from "d" to "e" at a cost of 20.
The total cost incurred is 5 + 1 + 2 + 20 = 28. 
It can be shown that this is the minimum possible cost.
```

**Example 2:**

```
Input: source = "abcdefgh", target = "acdeeghh", original = ["bcd","fgh","thh"], changed = ["cde","thh","ghh"], cost = [1,3,5]
Output: 9
Explanation: To convert "abcdefgh" to "acdeeghh", do the following operations:
- Change substring source[1..3] from "bcd" to "cde" at a cost of 1.
- Change substring source[5..7] from "fgh" to "thh" at a cost of 3. We can do this operation because indices [5,7] are disjoint with indices picked in the first operation.
- Change substring source[5..7] from "thh" to "ghh" at a cost of 5. We can do this operation because indices [5,7] are disjoint with indices picked in the first operation, and identical with indices picked in the second operation.
The total cost incurred is 1 + 3 + 5 = 9.
It can be shown that this is the minimum possible cost.
```

**Example 3:**

```
Input: source = "abcdefgh", target = "addddddd", original = ["bcd","defgh"], changed = ["ddd","ddddd"], cost = [100,1578]
Output: -1
Explanation: It is impossible to convert "abcdefgh" to "addddddd".
If you select substring source[1..3] as the first operation to change "abcdefgh" to "adddefgh", you cannot select substring source[3..7] as the second operation because it has a common index, 3, with the first operation.
If you select substring source[3..7] as the first operation to change "abcdefgh" to "abcddddd", you cannot select substring source[1..3] as the second operation because it has a common index, 3, with the first operation.
```

**Constraints**

- 1 <= source.length == target.length <= 1000
- source, target consist only of lowercase English characters.
- 1 <= cost.length == original.length == changed.length <= 100
- 1 <= original[i].length == changed[i].length <= source.length
- original[i], changed[i] consist only of lowercase English characters.
- original[i] != changed[i]
- 1 <= cost[i] <= 106

---

## 题目（中文翻译）

**描述**  
给定两个下标从 0 开始的字符串 `source` 和 `target`，二者长度均为 `n`，且仅包含小写英文字母。另给定两个下标从 0 开始的字符串数组 `original`、`changed`，以及整数数组 `cost`，其中 `cost[i]` 表示将字符串 `original[i]` 转换为字符串 `changed[i]` 的费用。

你从字符串 `source` 开始。一次操作可以从当前字符串中挑选一个子串（substring）`x`，并以费用 `z` 将其改为 `y`，前提是存在某个下标 `j` 满足 `cost[j] == z`、`original[j] == x` 且 `changed[j] == y`。你可以执行任意次数的操作，但任意两次操作必须满足以下两条条件之一：

* 两次操作涉及的下标集合互不相交（即没有共同的字符位置），或  
* 两次操作的子串完全相同且对应的转换规则相同（即 `original` 与 `changed` 均相同）。

返回将 `source` 转换为 `target` 所需的最小费用。如果无法完成转换，返回 `-1`。  
注意，可能存在下标 `i, j` 使得 `original[i] == original[j]` 且 `changed[i] == changed[j]`（即同一种转换规则出现多次）。

---

### 示例

#### 示例 1
```
Input: source = "abcd", target = "acbe", original = ["a","b","c","c","e","d"], changed = ["b","c","b","e","b","e"], cost = [2,5,5,1,2,20]
Output: 28
```
**解释**：将 `"abcd"` 转换为 `"acbe"` 的过程如下  
- 将子串 `source[1..1]`（即 `"b"`）以费用 5 改为 `"c"`。  
- 将子串 `source[2..2]`（即 `"c"`）以费用 1 改为 `"e"`。  
- 将子串 `source[2..2]`（即 `"e"`）以费用 2 改为 `"b"`。  
- 将子串 `source[3..3]`（即 `"d"`）以费用 20 改为 `"e"`。  
总费用为 5 + 1 + 2 + 20 = 28。

#### 示例 2
```
Input: source = "abcdefgh", target = "acdeeghh", original = ["bcd","fgh","thh"], changed = ["cde","thh","ghh"], cost = [1,3,5]
Output: 9
```
**解释**：将 `"abcdefgh"` 转换为 `"acdeeghh"` 的过程如下  
- 将子串 `source[1..3]`（即 `"bcd"`）以费用 1 改为 `"cde"`。  
- 将子串 `source[5..7]`（即 `"fgh"`）以费用 3 改为 `"thh"`。  
- 将子串 `source[6..8]`（即 `"thh"`）以费用 5 改为 `"ghh"`。  
总费用为 1 + 3 + 5 = 9。

#### 示例 3
```
Input: source = "abcdefgh", target = "addddddd", original = ["bcd","defgh"], changed = ["ddd","ddddd"], cost = [100,1578]
Output: -1
```
**解释**：无法将 `"abcdefgh"` 转换为 `"addddddd"`。  
例如，若第一步选择子串 `source[1..3]` 将 `"bcd"` 改为 `"ddd"`，得到 `"adddefgh"`，则第二步若尝试把子串 `source[3..7]`（即 `"defgh"`）改为 `"ddddd"` 会与第一步的下标 3 重叠，违反了操作之间必须不共享下标的要求。因此没有合法的操作序列可以完成全部转换。

---

### 约束条件
- `1 <= source.length == target.length <= 1000`
- `source`、`target` 仅由小写英文字母组成
- `1 <= cost.length == original.length == changed.length <= 100`
- `1 <= original[i].length == changed[i].length <= source.length`
- `original[i]`、`changed[i]` 仅由小写英文字母组成
- `original[i] != changed[i]`
- `1 <= cost[i] <= 10^6`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可能的操作序列枚举一遍**，找出能够把 `source` 变成 `target` 的最小花费。  
可以把每一次「选一个子串 `x` → `y`」看成在字符串上画一条「从左到右、不相交」的区间。  
于是整个过程就是：

1. 把 `source` 切成若干不相交的区间（每个区间可以长度为 1，也可以更长）。  
2. 对每个区间，检查是否有一条合法的转换规则 `original[i] = x`、`changed[i] = y`，如果有就把对应的费用 `cost[i]` 加进去。  
3. 所有区间都转换完后，检查得到的字符串是否恰好等于 `target`。  

如果所有区间都合法且最终得到 `target`，就记录下这套方案的总费用，取最小值。

> **类比**：把字符串想象成一条道路，规则是「把某段路的标识改成别的标识」并且要付钱。暴力做法就是把道路上每一种可能的划分方式（即每一种「分段」）都尝试一次。

**为什么会对？**  
因为题目要求的所有合法操作都可以用「若干不相交的子串转换」来表示，而我们把所有可能的划分都遍历了一遍，必然能找到最优的那一种。

**时间/空间复杂度**  
- 对长度为 `n` 的字符串，所有不相交区间的划分数是 **Catalan 数**，大约在 `O(4^n / n^{1.5})`，随 `n` 指数级增长。  
- 对每一种划分，还要检查每个子串是否出现在 `original` 中，这一步也是线性的。  
- 因此总时间复杂度是 **指数级**（`O(2^n)` 甚至更高），在 `n ≤ 1000` 时根本不可行。  
- 空间只需要保存递归/遍历时的临时状态，`O(n)`。

> **大白话**：如果把时间复杂度写成 `O(2^n)`，可以想象每增加一个字符，就要把答案的可能性翻倍，10 个字符就要尝试 1024 种，20 个字符就要 1 048 576 种，1000 个字符更是天文数字，根本跑不完。

#### 代码（Python）

下面的代码仅作概念展示，**不建议在正式提交中使用**，因为会超时。

```python
import math
from functools import lru_cache

def minCost_bruteforce(source, target, original, changed, cost):
    n = len(source)
    # 把规则存进哈希表，key = (orig, changed) , value = min cost
    rule = {}
    for o, c, w in zip(original, changed, cost):
        rule[(o, c)] = min(rule.get((o, c), math.inf), w)

    @lru_cache(None)
    def dfs(pos):
        """返回把 source[pos:] 变成 target[pos:] 的最小费用，或 INF 表示不可能"""
        if pos == n:
            return 0
        # 如果当前字符相同，可以直接跳过
        best = dfs(pos + 1) if source[pos] == target[pos] else math.inf

        # 枚举所有可能的子串长度
        for end in range(pos + 1, n + 1):
            s = source[pos:end]
            t = target[pos:end]
            if (s, t) in rule:                     # 有直接的转换规则
                nxt = dfs(end)
                if nxt != math.inf:
                    best = min(best, nxt + rule[(s, t)])
        return best

    ans = dfs(0)
    return -1 if ans == math.inf else ans
```

> 代码说明  
> - `rule` 用字典保存每条规则的最小费用，类似查字典（`key` 是单词，`value` 是页码）。  
> - `dfs(pos)` 递归求解子问题：把从 `pos` 开始的后缀转换完的最小费用。  
> - `lru_cache` 把已经算过的子问题记下来，避免重复计算（记忆化搜索），但仍然是指数级的状态数。

#### 复杂度

- **时间复杂度**：`O(2^n)`（指数级），因为每个位置都有「不转」或「转任意长度子串」两种选择。  
- **空间复杂度**：`O(n)`，递归栈深度最多 `n`，加上缓存表的大小 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解慢的根本原因是 **“枚举所有子串划分”**。  
我们其实不需要枚举划分，而是 **动态规划**：只关心「前缀已经转换好的最小费用」即可。  

核心思路分三步：

1. **把所有出现的字符串映射成整数 id**  
   - `original`、`changed`、以及后面会用到的 `source`、`target` 的子串总数不超过 `2·m ≤ 200`（`m = len(original)`），  
   - 用哈希表把每个不同的字符串映射到 `0 … K‑1`（`K` 为不同字符串的数量），相当于把「单词」变成「编号」。

2. **在这些编号之间跑 Floyd‑Warshall**  
   - 直接的转换规则是有向边 `id(original[i]) → id(changed[i])`，费用为 `cost[i]`。  
   - 允许**多步转换**（比如 `a → b → c`），所以我们需要求任意两字符串之间的**最小转换费用**。  
   - Floyd‑Warshall 在 `K ≤ 200` 时只要 `K³ ≈ 8·10⁶` 次操作，轻松跑完。

3. **前缀 DP + Trie 快速匹配子串**  
   - 设 `dp[i]` 为把 `source[0…i‑1]`（前 `i` 个字符）变成 `target[0…i‑1]` 的最小费用，`dp[0] = 0`。  
   - 对每个位置 `i`，有两种可能的来源：  
     1. **不需要转换**：如果 `source[i‑1] == target[i‑1]`，则 `dp[i] = dp[i‑1]`。  
     2. **用一次操作把一段 `[j, i‑1]` 同时改成目标**：  
        - 取子串 `x = source[j:i]`、`y = target[j:i]`。  
        - 如果 `x` 与 `y` 都在我们的编号表中，且 `dist[id(x)][id(y)]`（最小费用）不是无穷大，  
          那么 `dp[i] = min(dp[i], dp[j] + dist[id(x)][id(y)])`。  
   - 为了 **快速找到所有满足条件的 `(j,i)`**，我们把 `original` 中的所有字符串建成 **Trie**（前缀树），同理把 `changed` 也建 Trie。  
     - 在遍历 `i` 时，沿着 `source` 向左扩展，用 Trie 检查每个可能的 `x` 是否存在；  
     - 同时在 `target` 上检查对应的 `y` 是否也在 `changed` 的 Trie 中。  
     - 这样每次只需 **O(子串长度)** 的时间，整体是 `O(n²)`（`n ≤ 1000`），远快于暴力。

**关键数据结构解释**  

| 数据结构 | 类比 | 作用 |
|----------|------|------|
| 哈希表（string → id） | 查字典：单词 → 页码 | 把字符串压缩成整数，方便在矩阵里做下标 |
| 距离矩阵 `dist[K][K]` | 城市间的最短路表 | 保存任意两字符串之间的最小转换费用 |
| Floyd‑Warshall | 多站点公交换乘最省钱 | 通过中转点求出最便宜的间接转换 |
| Trie（前缀树） | 电话簿的层级索引 | 快速判断一个子串是否出现在 `original`/`changed` 中，并得到它的 id |

#### 代码（Python）

```python
import math
from collections import defaultdict, deque

INF = 10 ** 18


def minCost(source: str, target: str,
            original: list[str], changed: list[str], cost: list[int]) -> int:
    n = len(source)
    m = len(original)

    # 1️⃣ 把所有出现的字符串映射为 id
    idx = {}                     # string -> id
    def get_id(s: str) -> int:
        if s not in idx:
            idx[s] = len(idx)
        return idx[s]

    # 收集 original、changed 以及后面会出现的子串（先只收集规则里的）
    for o, c in zip(original, changed):
        get_id(o)
        get_id(c)

    K = len(idx)                 # 当前已有的唯一字符串数

    # 2️⃣ 建立最小费用矩阵，先填 INF，再写入直接规则的费用（取最小）
    dist = [[INF] * K for _ in range(K)]
    for i in range(K):
        dist[i][i] = 0           # 零费用到自身

    for o, c, w in zip(original, changed, cost):
        u, v = idx[o], idx[c]
        if w < dist[u][v]:
            dist[u][v] = w

    # 3️⃣ Floyd‑Warshall 求任意两字符串的最小转换费用
    for k in range(K):
        dk = dist[k]
        for i in range(K):
            di = dist[i]
            ik = di[k]
            if ik == INF:
                continue
            for j in range(K):
                if dk[j] == INF:
                    continue
                if ik + dk[j] < di[j]:
                    di[j] = ik + dk[j]

    # 4️⃣ 把规则里出现的字符串再次映射到可能的更大集合
    #   （因为在 DP 过程中我们会需要 source/target 的子串的 id）
    #    这里直接把所有 source、target 的前缀/后缀放进 map，省去 Trie 里再做映射。
    #    实际实现中我们使用 Trie 来枚举子串，这里只需要一个快速的查询函数。
    for i in range(n):
        # 所有可能的子串长度不超过 n，直接把它们加入 map（最多 1000*1000/2 = 5e5 次）
        # 为了不超时，这里仅在需要时动态添加（见下文的 get_id_lazy）。
        pass

    # 5️⃣ 构建 Trie，帮助在 DP 中快速枚举合法子串
    class TrieNode:
        __slots__ = ("next", "id")
        def __init__(self):
            self.next = {}
            self.id = -1

    def build_trie(strings):
        root = TrieNode()
        for s in strings:
            node = root
            for ch in s:
                if ch not in node.next:
                    node.next[ch] = TrieNode()
                node = node.next[ch]
            node.id = idx[s]          # 这里一定已经有 id
        return root

    # 只把 original 与 changed 放进 Trie（因为只这些字符串才可能作为一次操作的两端）
    trie_orig = build_trie(original)
    trie_chg  = build_trie(changed)

    # 6️⃣ DP
    dp = [INF] * (n + 1)
    dp[0] = 0

    for i in range(1, n + 1):
        # 情形 1：当前字符相同，直接继承前缀
        if source[i - 1] == target[i - 1]:
            dp[i] = min(dp[i], dp[i - 1])

        # 情形 2：尝试所有以 i-1 结尾的合法子串
        # 先在 source 上向左遍历，找所有可能的 x
        node_x = trie_orig
        for j in range(i - 1, -1, -1):
            ch = source[j]
            if ch not in node_x.next:
                break
            node_x = node_x.next[ch]
            if node_x.id == -1:          # 不是完整的 original 子串，继续向左
                continue
            id_x = node_x.id

            # 同时在 target 上检查对应的 y 是否是 changed 子串
            node_y = trie_chg
            valid = True
            for k in range(j, i):
                c = target[k]
                if c not in node_y.next:
                    valid = False
                    break
                node_y = node_y.next[c]
            if not valid or node_y.id == -1:
                continue
            id_y = node_y.id

            # 现在我们有了 (x -> y) 的最小费用
            if dist[id_x][id_y] == INF:
                continue
            dp[i] = min(dp[i], dp[j] + dist[id_x][id_y])

    return -1 if dp[n] == INF else dp[n]
```

> **代码要点注释**  
> 1. **映射 id**：`idx` 把每个出现的字符串压成整数，类似查字典。  
> 2. **Floyd‑Warshall**：三层循环 `k,i,j` 把所有间接转换的费用都算出来，保证 `dist[u][v]` 是最小的。  
> 3. **Trie**：`TrieNode.next` 保存子字符指向的子节点，`id` 保存完整单词对应的整数 id。  
> 4. **DP 循环**：对每个右端点 `i`，向左遍历（`j` 递减）并同步在 `target` 上检查对应的 `y`，只要两端都是合法的原/改字符串，就可以使用预计算好的最小费用 `dist[id_x][id_y]` 完成一次操作。  
> 5. **复杂度控制**：每次向左最多遍历 `source` 长度 `n`，而 Trie 的查找是 **O(1) 每个字符**，所以整体是 `O(n²)`（`n ≤ 1000`），配合 `K³ ≤ 8·10⁶` 的 Floyd‑Warshall，完全可以在 1 秒左右跑完。

#### 复杂度

- **时间复杂度**  
  - 建立 id 映射 + 构造 Trie：`O(m * L)`，`L` 为规则字符串的平均长度（≤ 1000）， negligible。  
  - Floyd‑Warshall：`O(K³)`，`K ≤ 2·m ≤ 200` → 最多约 `8·10⁶` 次基本运算。  
  - DP + Trie 匹配：外层遍历 `i = 1…n`，内层最坏向左遍历全部字符，时间 `O(n²)`，`n ≤ 1000` → `10⁶` 次字符访问。  
  - **总计**：`O(K³ + n²)`，在本题约为几百万次操作，轻松通过。

- **空间复杂度**  
  - `dist` 矩阵：`O(K²)`（≤ 40 000）。  
  - Trie：总字符数不超过所有规则字符串的长度之和，`O(m * L)`。  
  - DP 数组：`O(n)`。  
  - **总体**：`O(K² + n)`，几万级别的内存。

---

## 心得

- **核心技巧**：**先在所有字符串之间求最小转换费用（Floyd‑Warshall），再用前缀 DP + Trie 进行区间匹配**。  
- **适用的题型**  
  1. “字符串的最小转换成本” 系列（如 *Minimum Cost to Convert String I/II*）。  
  2. “带费用的子串替换” 或 “带费用的编辑距离” 这类需要在区间层面做最优选择的题目。  
  3. “多步转换的最短路径”——把每个状态视作图的节点，用 Floyd‑Warshall 或 SPFA 预处理最短路。

> **一句话总结**：把所有可能的单步转换抽象成图的边，先算出任意两状态的最小费用，再用 DP 按前缀把字符串一步步拼起来。

---

## 反思

- **第一反应**：直接枚举所有子串划分并尝试每条规则，导致指数级爆炸。  
- **最容易踩的坑**  
  1. **规则的间接组合**：`a → b`、`b → c` 可以合并成 `a → c`，如果不先跑 Floyd‑Warshall，DP 只能使用直接规则，得到的答案往往不是最小。  
  2. **子串不能重叠**：在 DP 中必须保证一次操作只覆盖一次区间，使用前缀 DP 自然满足这个约束。  
  3. **边界条件**：`dp[0] = 0` 必须初始化；当 `source[i‑1] == target[i‑1]` 时要记得把 `dp[i] = dp[i‑1]` 继承下来。  
  4. **哈希冲突或忘记取最小费用**：同一对 `(original, changed)` 可能出现多次，必须保存最小的 `cost`。  

- **下次类似题目第一步**：  
  1. 把所有“状态”抽象成图的节点（这里是字符串），检查是否存在**多步合并**的可能。  
  2. 先用 **全局最短路**（Floyd‑Warshall / 多源 Dijkstra）把任意两状态的最小费用算出来。  
  3. 再用 **DP**（前缀、后缀或区间）把整体问题拼接起来。