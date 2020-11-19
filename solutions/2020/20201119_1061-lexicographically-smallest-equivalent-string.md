# #1061. 字典序最小等价字符串 / Lexicographically Smallest Equivalent String

> 难度：中等 · 标签：String、Union Find · [LeetCode 链接](https://leetcode.com/problems/lexicographically-smallest-equivalent-string/)

---

## 题目（英文原版）

**Description**

You are given two strings of the same length s1 and s2 and a string baseStr.
We say s1[i] and s2[i] are equivalent characters.
Equivalent characters follow the usual rules of any equivalence relation:
For example, given the equivalency information from s1 = "abc" and s2 = "cde", "acd" and "aab" are equivalent strings of baseStr = "eed", and "aab" is the lexicographically smallest equivalent string of baseStr.
Return the lexicographically smallest equivalent string of baseStr by using the equivalency information from s1 and s2.

**Examples**

**Example 1:**

```
Input: s1 = "parker", s2 = "morris", baseStr = "parser"
Output: "makkek"
Explanation: Based on the equivalency information in s1 and s2, we can group their characters as [m,p], [a,o], [k,r,s], [e,i].
The characters in each group are equivalent and sorted in lexicographical order.
So the answer is "makkek".
```

**Example 2:**

```
Input: s1 = "hello", s2 = "world", baseStr = "hold"
Output: "hdld"
Explanation: Based on the equivalency information in s1 and s2, we can group their characters as [h,w], [d,e,o], [l,r].
So only the second letter 'o' in baseStr is changed to 'd', the answer is "hdld".
```

**Example 3:**

```
Input: s1 = "leetcode", s2 = "programs", baseStr = "sourcecode"
Output: "aauaaaaada"
Explanation: We group the equivalent characters in s1 and s2 as [a,o,e,r,s,c], [l,p], [g,t] and [d,m], thus all letters in baseStr except 'u' and 'd' are transformed to 'a', the answer is "aauaaaaada".
```

**Constraints**

- 1 <= s1.length, s2.length, baseStr <= 1000
- s1.length == s2.length
- s1, s2, and baseStr consist of lowercase English letters.

---

## 题目（中文翻译）

你得到两个等长的字符串 `s1` 和 `s2`，以及一个字符串 `baseStr`。  
我们称 `s1[i]` 与 `s2[i]` 为等价字符（equivalent characters）。  
等价字符遵循等价关系的所有常规规则。  

例如，给定 `s1 = "abc"` 与 `s2 = "cde"`，则 `"acd"` 与 `"aab"` 是 `baseStr = "eed"` 的等价字符串，而 `"aab"` 是 `baseStr` 的字典序最小等价字符串。  

请利用 `s1` 与 `s2` 中的等价信息，返回 `baseStr` 的字典序最小等价字符串。

**示例 1**  
**输入**: `s1 = "parker", s2 = "morris", baseStr = "parser"`  
**输出**: `"makkek"`  
**解释**: 根据 `s1` 与 `s2` 中的等价信息，可以将字符划分为 `[m,p]`, `[a,o]`, `[k,r,s]`, `[e,i]` 四组。每组内的字符等价且按字典序排序后取最小字符。于是得到 `"makkek"`。

**示例 2**  
**输入**: `s1 = "hello", s2 = "world", baseStr = "hold"`  
**输出**: `"hdld"`  
**解释**: 根据等价信息，可将字符划分为 `[h,w]`, `[d,e,o]`, `[l,r]` 三组。`baseStr` 中的第二个字母 `'o'` 被替换为该组的最小字符 `'d'`，最终得到 `"hdld"`。

**示例 3**  
**输入**: `s1 = "leetcode", s2 = "programs", baseStr = "sourcecode"`  
**输出**: `"aauaaaaada"`  
**解释**: 等价字符分组为 `[a,o,e,r,s,c]`, `[l,p]`, `[g,t]` 和 `[d,m]`。因此 `baseStr` 中除 `'u'` 与 `'d'` 之外的所有字母均被转换为该组的最小字符 `'a'`，得到 `"aauaaaaada"`。

**约束条件**  

- `1 <= s1.length, s2.length, baseStr.length <= 1000`
- `s1.length == s2.length`
- `s1`, `s2` 与 `baseStr` 均只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有等价关系都展开成 **等价类**（相当于把字母分到若干个“朋友圈”里），然后对每个字母在 `baseStr` 中查找它所在的朋友圈，取该朋友圈里字典序最小的字母作为替换结果。

- **数据结构**：我们可以用 **邻接表**（字典的值是集合）来存储字母之间的直接等价关系，像一张“谁和谁是好朋友”的表。  
  - 把 `s1[i]` 与 `s2[i]` 视为互相认识的两个同学，两人之间建立一条无向边。  
  - 再用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）** 从任意未访问的字母出发，把所有能通过朋友关系连到的字母收集到同一个集合里，这个集合就是一个等价类。  
- **为什么正确**：等价关系满足 **传递性**（A~B 且 B~C ⇒ A~C），把所有相连的字母放进同一个集合后，集合内部的任意两个字母都可以相互替换。只要在每个集合里选出字典序最小的字母作为代表，所有可能的替换结果里最小的自然就是用这些代表字母替换后的字符串。  

#### 代码（Python）

```python
from collections import defaultdict, deque

def smallestEquivalentString_bruteforce(s1: str, s2: str, baseStr: str) -> str:
    # 1️⃣ 建立无向图（邻接表），每个字母对应 0~25 的下标
    graph = defaultdict(set)               # 类似“谁是朋友”的字典
    for a, b in zip(s1, s2):
        graph[a].add(b)
        graph[b].add(a)

    # 2️⃣ BFS/DFS 找连通分量并记录每个字母的最小代表
    #   rep[ch] = 该字母所在等价类的最小字母
    rep = {}
    visited = set()

    for ch in (chr(ord('a') + i) for i in range(26)):  # 遍历所有小写字母
        if ch in visited:
            continue
        # 只要字母出现过（或没有出现也算单独一组），就做一次遍历
        queue = deque([ch])
        component = []                # 记录当前连通分量的所有字母
        visited.add(ch)

        while queue:
            cur = queue.popleft()
            component.append(cur)
            for nb in graph[cur]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append(nb)

        # 3️⃣ 选出字典序最小的字母作为代表
        min_ch = min(component)       # Python 直接比较字符的字典序
        for c in component:
            rep[c] = min_ch

    # 4️⃣ 把 baseStr 中每个字符替换成对应的最小代表
    res = []
    for ch in baseStr:
        res.append(rep.get(ch, ch))   # 若字符根本不在图里，直接自己

    return ''.join(res)
```

> **关键行解释**  
> - `graph[a].add(b)` / `graph[b].add(a)`：把两字母互相加入朋友列表。  
> - `queue = deque([ch])`：用队列实现 BFS，层层展开朋友关系。  
> - `min(component)`：在同一个朋友圈里挑最小的字母。  
> - `rep.get(ch, ch)`：若字母没有任何等价关系，保持不变。

#### 复杂度

- **时间复杂度**：`O(26 + E + V)`，其中 `E = len(s1)` 为边数（最多 1000），`V = 26` 为字母个数。  
  - 建图 O(E)  
  - BFS 遍历所有字母和边 O(V + E)  
  - 最后遍历 `baseStr` O(|baseStr|) ≤ 1000  
  综合来看，最多约 `O(1000)`，在实际中已经很快。  
  **大白话**：我们只需要把每条等价关系看一遍，再把每个字母看一遍，整体工作量和字符串长度成正比。

- **空间复杂度**：`O(V + E)` ≈ `O(1000)`，主要是存图的邻接表和 visited 集合。  

---

### 2. 最优解

#### 思路  

暴力解已经可以接受，但它在遍历每个连通分量时需要额外的 `component` 列表、BFS 队列等，代码稍显冗长。**真正的关键在于快速查询“两个字母是否等价以及等价类的最小代表”。**  
这正是 **并查集（Union‑Find）** 的强项：

1. **把每个字母看成一个节点**（0~25）。  
2. 对于 `s1[i]` 与 `s2[i]`，执行 **union** 操作，把它们所在的集合合并。  
3. 为了保证查询最小代表时直接得到字典序最小的字母，我们在 **union** 时让根节点始终是字典序更小的那个。  
   - 例如合并集合 `{m, p}`，`m` < `p`，于是把 `p` 的父指针指向 `m`。  
4. 这样，**find(x)** 返回的根节点就是该字母所在等价类的最小字母。  
5. 最后遍历 `baseStr`，对每个字符调用 `find`，得到替换后的字符即可。

> **为什么这样更快**  
> - 并查集的 `find` 与 `union` 在**路径压缩**和**按秩合并**的优化下，摊销时间几乎是 **O(α(N))**（α 为阿克曼函数的反函数，几乎可以视作常数）。  
> - 所以整体时间只和 `s1`、`baseStr` 长度线性相关，且代码只需两层循环，没有额外的 BFS/DFS 队列。  

#### 代码（Python）

```python
class UnionFind:
    def __init__(self):
        # 父指针数组，parent[i] = i 表示自己是根
        self.parent = [i for i in range(26)]

    def find(self, x: int) -> int:
        """返回 x 所在集合的根节点（字典序最小的字符下标）"""
        if self.parent[x] != x:
            # 路径压缩：把沿途的节点直接挂到根上，后面查询更快
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: int, y: int):
        """把 x、y 所在集合合并，根节点保持字典序最小"""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return
        # 让字典序更小的字符成为根
        if rx < ry:
            self.parent[ry] = rx
        else:
            self.parent[rx] = ry


def smallestEquivalentString(s1: str, s2: str, baseStr: str) -> str:
    uf = UnionFind()

    # 1️⃣ 把等价关系并进同一个集合
    for a, b in zip(s1, s2):
        uf.union(ord(a) - ord('a'), ord(b) - ord('a'))

    # 2️⃣ 根据根节点直接得到最小代表并构造答案
    res = []
    for ch in baseStr:
        idx = ord(ch) - ord('a')
        root = uf.find(idx)                 # 根节点对应的字符下标
        smallest = chr(root + ord('a'))     # 转回字符
        res.append(smallest)

    return ''.join(res)
```

> **关键行解释**  
> - `self.parent = [i for i in range(26)]`：每个字母初始自己是根，像 26 个人各自为政。  
> - `if self.parent[x] != x: self.parent[x] = self.find(self.parent[x])`：路径压缩，把找根的路上所有人直接挂到根上，后面找根更快。  
> - `if rx < ry: self.parent[ry] = rx`：根节点保持字典序最小，保证 `find` 返回的就是最小字符。  
> - `ord(ch) - ord('a')`：把字符映射到 0~25 的整数下标，便于数组操作。  

#### 复杂度

- **时间复杂度**：`O(|s1| + |baseStr| * α(26))` → 实际上是 `O(|s1| + |baseStr|)`。  
  - `union` 进行 `|s1|` 次，每次几乎是常数。  
  - `find` 对 `baseStr` 中每个字符执行一次，同样几乎是常数。  
  **对比**：与暴力解的 BFS 同样是线性，但并查集的实现更简洁、常数更小。

- **空间复杂度**：`O(26)` → 只需要一个长度为 26 的父指针数组，几乎不占内存。

---

## 心得

- **核心技巧**：**并查集（Union‑Find）** 用来维护“等价关系”，并通过让根节点保持字典序最小，直接得到每个字符的最小替换。  
- **适用的题型**  
  1. **字母/数字等价类**（如 LeetCode 839 *Similar String Groups*）。  
  2. **网络连通性**（如判断图中两点是否在同一连通分量）。  
  3. **离线查询的集合合并**（如 “查询两个节点是否在同一集合” 系列题目）。  
- **一句话总结**：把所有等价关系用并查集合并，让每个集合的根永远是字典序最小的字符，查询时直接返回根即可得到字典序最小的等价字符串。

---

## 反思

- **第一反应**：看到“等价字符”“字典序最小”，立刻想到把字符划分到等价类，然后在每类里取最小字符。  
- **最容易踩的坑**  
  - **忽略未出现的字母**：并查集需要初始化所有 26 个字母，即使它们没有出现在 `s1`、`s2` 中，也要保证 `find` 能返回自己。  
  - **根节点不是最小字符**：若在 `union` 时随意挂树，根可能不是字典序最小的，最终会得到错误答案。必须在合并时比较下标并让较小的成为根。  
  - **路径压缩写错**：忘记递归返回根或写成 `self.parent[x] = self.find(self.parent[x])` 后没有返回值，会导致 `find` 返回 `None`。  
- **下次第一步**：先把等价关系抽象为“并查集合并”，确保合并规则保留最小字典序的根，再直接遍历 `baseStr` 进行查找。这样思路清晰、实现简洁。