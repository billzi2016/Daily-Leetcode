# #1202. 最小字符串的交换 / Smallest String With Swaps

> 难度：中等 · 标签：Array、Hash Table、String、Depth-First Search、Breadth-First Search、Union Find、Sorting · [LeetCode 链接](https://leetcode.com/problems/smallest-string-with-swaps/)

---

## 题目（英文原版）

**Description**

You are given a string s, and an array of pairs of indices in the string pairs where pairs[i] = [a, b] indicates 2 indices(0-indexed) of the string.
You can swap the characters at any pair of indices in the given pairs any number of times.
Return the lexicographically smallest string that s can be changed to after using the swaps.

**Examples**

**Example 1:**

```
Input: s = "dcab", pairs = [[0,3],[1,2]]
Output: "bacd"
Explaination: 
Swap s[0] and s[3], s = "bcad"
Swap s[1] and s[2], s = "bacd"
```

**Example 2:**

```
Input: s = "dcab", pairs = [[0,3],[1,2],[0,2]]
Output: "abcd"
Explaination: 
Swap s[0] and s[3], s = "bcad"
Swap s[0] and s[2], s = "acbd"
Swap s[1] and s[2], s = "abcd"
```

**Example 3:**

```
Input: s = "cba", pairs = [[0,1],[1,2]]
Output: "abc"
Explaination: 
Swap s[0] and s[1], s = "bca"
Swap s[1] and s[2], s = "bac"
Swap s[0] and s[1], s = "abc"
```

**Constraints**

- 1 <= s.length <= 10^5
- 0 <= pairs.length <= 10^5
- 0 <= pairs[i][0], pairs[i][1] < s.length
- s only contains lower case English letters.

---

## 题目（中文翻译）

给定一个字符串 **s**，以及一个索引对数组 **pairs**，其中 `pairs[i] = [a, b]` 表示字符串中两个下标（**0-indexed**）`a` 和 `b`。  
你可以对 **pairs** 中的任意一对下标进行任意次数的字符交换（**swap**）。  
返回在进行任意次数的交换后，**s** 能够变成的字典序（**lexicographically**）最小的字符串。

**示例 1**  
**输入**: `s = "dcab", pairs = [[0,3],[1,2]]`  
**输出**: `"bacd"`  
**解释**:  
- 交换 `s[0]` 与 `s[3]`，得到 `s = "bcad"`  
- 交换 `s[1]` 与 `s[2]`，得到 `s = "bacd"`

**示例 2**  
**输入**: `s = "dcab", pairs = [[0,3],[1,2],[0,2]]`  
**输出**: `"abcd"`  
**解释**:  
- 交换 `s[0]` 与 `s[3]`，得到 `s = "bcad"`  
- 交换 `s[0]` 与 `s[2]`，得到 `s = "acbd"`  
- 交换 `s[1]` 与 `s[2]`，得到 `s = "abcd"`

**示例 3**  
**输入**: `s = "cba", pairs = [[0,1],[1,2]]`  
**输出**: `"abc"`  
**解释**:  
- 交换 `s[0]` 与 `s[1]`，得到 `s = "bca"`  
- 交换 `s[1]` 与 `s[2]`，得到 `s = "bac"`  
- 交换 `s[0]` 与 `s[1]`，得到 `s = "abc"`

**约束条件**  
- `1 <= s.length <= 10^5`  
- `0 <= pairs.length <= 10^5`  
- `0 <= pairs[i][0], pairs[i][1] < s.length`  
- `s` 只包含小写英文字母。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把所有可以交换的下标对一次遍历一遍，反复执行交换操作，直到再也找不到可以让字符串更小的交换为止**。  

- **使用的数据结构**：  
  - `list`（字符数组）：把字符串 `s` 转成列表，方便原地修改字符。  
  - `pairs` 本身就是一张“可以直接交换的桥”。可以把它想象成 **“两座城之间的双向道路”**，只要走到同一座城，就可以随时来回换乘。

- **为什么它是对的**：  
  - 每一次我们都尝试把较大的字符换到较后面、较小的字符换到前面，这样的局部改动不会让最终答案变坏。  
  - 当所有直接相连的下标都已经按照字典序排好后，任何再做的交换（即使是跨越多条道路的间接交换）在这一步已经被包含在了“反复遍历”里。于是得到的字符串一定是 **一种** 可达的最小形式。

- **时间/空间复杂度**：  
  - 设字符串长度为 `n`，`pairs` 的数量为 `m`。  
  - 暴力方法需要 **不断遍历** `pairs`，每遍历一次都可能进行一次字符交换。最坏情况下需要 `O(n)` 次遍历才能不再产生变化（因为每次至少把一个字符往左移动一步），于是时间复杂度约为 `O(n * m)`。  
  - 用大白话说，**如果 n=10⁵、m=10⁵，这个算法会跑到 10¹⁰ 次操作，根本不可接受**。  
  - 空间上只需要存放字符数组和 `pairs`，即 `O(n + m)`，这在题目限制下是可以的。

#### 代码（Python）

```python
def smallestStringWithSwaps_bruteforce(s: str, pairs: list[list[int]]) -> str:
    # 把字符串转成列表，方便原地修改字符
    chars = list(s)
    n = len(chars)

    # 为了防止无限循环，最多遍历 n 次（每次至少把一个字符左移一位）
    for _ in range(n):
        changed = False                     # 本轮是否有实际交换发生
        for a, b in pairs:                  # 遍历所有直接可交换的下标对
            if chars[a] > chars[b]:         # 如果左边字符更大，交换让字典序更小
                chars[a], chars[b] = chars[b], chars[a]
                changed = True
        if not changed:                     # 本轮没有任何交换，说明已经最小
            break

    return ''.join(chars)
```

> **关键行解释**  
> - `if chars[a] > chars[b]`：只有左边字符比右边大时才交换，这样才会让整体字典序下降。  
> - `changed` 用来检测本轮是否有实际改动，若没有则可以提前结束循环。

#### 复杂度

- **时间复杂度**：`O(n * m)`  
  - 直观含义：如果字符串有 10⁵ 个字符、可交换对也有 10⁵ 条，算法大约要进行 10¹⁰ 次比较和可能的交换，远远超出 1 秒的时间限制。

- **空间复杂度**：`O(n + m)`  
  - 只用了字符列表和原始的 `pairs`，没有额外的“大结构”。

---

### 2. 最优解

#### 思路  

从暴力解可以看到 **瓶颈在于重复遍历所有 pair**，而实际上 **只要把同一个连通分量（connected component）里的字符自由排序，就能得到该分量的最小排列**。  

**核心观察**：

1. 把每个下标看成图中的一个节点。  
2. `pairs[i] = [a, b]` 表示节点 `a` 与节点 `b` 之间有一条**无向边**（可以直接交换）。  
3. 如果节点 `x` 与节点 `y` 之间**存在路径**（即它们在同一个连通分量），那么通过若干次合法交换，**任意** `x`、`y` 位置的字符都可以互相调换。  
   - 类比：城市之间有道路相连，只要能走通，就可以把任意一件物品从一个城市搬到另一个城市。

因此，**每个连通分量内部的字符可以完全自由排列**，我们只需要把它们按字典序从小到大排好，再放回原来的下标位置即可得到全局最小字符串。

**实现方式**：  
- **并查集（Union‑Find）**：高效维护哪些下标属于同一个连通分量。  
  - `find(x)` 返回 x 所在集合的根节点。  
  - `union(x, y)` 把两个集合合并。  
  - 并查集的时间复杂度几乎是 **常数**（α(n)），对 10⁵ 规模的数据非常友好。  
- **收集分量**：遍历所有下标，把同根的下标放进同一个列表（使用 `defaultdict(list)`）。  
- **排序**：对每个分量的字符列表和下标列表分别排序。字符升序、下标升序，然后把排好序的字符依次写回对应下标。  

**一步步的推导**：

| 步骤 | 为什么要这么做 |
|------|----------------|
| 用并查集合并所有 `pairs` 中的下标 | 把“能直接交换”的关系扩展到“能间接交换”，得到完整的连通分量 |
| 用根节点把下标分组 | 同一个根代表同一个连通分量，后面只需要在每组内部处理 |
| 把每组的字符取出来并排序 | 组内字符可以自由调换，排好序可以得到该组的最小局部结果 |
| 把排好序的字符放回原来的下标（下标也排序） | 保证最小字符放在最左（下标最小）的位子，符合字典序的定义 |

#### 代码（Python）

```python
from collections import defaultdict

class UnionFind:
    """并查集（Union‑Find）实现，支持路径压缩和按秩合并"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 每个节点最初是自己的父亲
        self.rank = [0] * n            # 用来平衡树的高度

    def find(self, x: int) -> int:
        """返回 x 所在集合的根节点，顺便压缩路径提升后续查询效率"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归找根，并把路径直接挂到根上
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """把 x、y 所在的集合合并"""
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:          # 已经在同一个集合，不需要合并
            return
        # 按秩合并：高度低的挂到高度高的下面，保持树尽量扁平
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

def smallestStringWithSwaps(s: str, pairs: list[list[int]]) -> str:
    n = len(s)
    uf = UnionFind(n)

    # 1️⃣ 把所有可以直接交换的下标合并进同一个集合
    for a, b in pairs:
        uf.union(a, b)

    # 2️⃣ 根据根节点把下标分组
    groups = defaultdict(list)          # root -> [下标列表]
    for idx in range(n):
        root = uf.find(idx)
        groups[root].append(idx)

    # 3️⃣ 对每个连通分量内部做排序
    res = list(s)                       # 最终答案的字符列表
    for idx_list in groups.values():
        # 取出这些下标对应的字符
        chars = [s[i] for i in idx_list]
        # 下标升序、字符升序分别排序
        idx_list.sort()
        chars.sort()
        # 把排好序的字符放回对应的下标位置
        for i, ch in zip(idx_list, chars):
            res[i] = ch

    return ''.join(res)
```

> **关键行解释**  
> - `uf.union(a, b)`：把可以直接交换的两个位置放进同一个集合，相当于在图里连一条无向边。  
> - `groups[root].append(idx)`：把同根的下标收集到一起，形成 **连通分量**。  
> - `chars.sort()`：因为分量内部字符可以随意调换，排成字典序最小的顺序。  
> - `for i, ch in zip(idx_list, chars): res[i] = ch`：把最小字符写回最左（下标最小）的位置，确保整体字典序最小。

#### 复杂度

- **时间复杂度**：`O(n α(n) + m α(n) + n log n)`  
  - `α(n)` 是 **阿克曼函数的反函数**，对所有实际数据几乎是常数（≈4），所以可以视作 `O(1)`。  
  - 合并所有 `pairs`：`O(m α(n))`。  
  - 找根并分组所有下标：`O(n α(n))`。  
  - 对每个连通分量分别排序，所有字符总数仍是 `n`，排序总代价是 `O(n log n)`。  
  - 用大白话说：**我们只需要一次遍历 + 若干次快如闪电的合并 + 一次整体排序**，在 10⁵ 规模下轻松跑在毫秒级。

- **空间复杂度**：`O(n)`  
  - 主要是并查集的 `parent`、`rank` 数组以及 `groups`（把下标重新组织了一遍），全部都是线性大小。

---

## 心得

- **核心技巧**：把下标看成图的节点，利用 **并查集** 找出所有互相可达的下标（连通分量），然后在每个分量内部独立排序。  
- **适用的题型**  
  1. “可以在若干对位置之间自由交换，求最小/最大排列”——如 *Lexicographically Smallest String After Swaps*（本题）。  
  2. “给定若干等价关系，求字符/数字的最小重排”——如 *Smallest String With Swaps II*、*Equations Possible*（判断是否冲突）。  
  3. “把图的连通分量分别处理”——如 *Friend Circles*、*Number of Islands*（统计岛屿）等。  
- **一句话总结解题钥匙**：**“同一连通分量内部可以任意排列，排序后放回最左位置即得全局最小”。**

---

## 反思

- **第一反应**：看到“可以任意次数交换”会想到 **遍历所有可能的交换**，于是想到暴力的“不断交换直至不再改变”。  
- **最容易踩的坑**  
  - **忽略间接可达**：只考虑直接给出的 pair，会错过通过多条边连通的下标。  
  - **忘记对下标也排序**：把字符排序后直接填回原顺序会得到错误的排列，需要先把下标从小到大排序，再对应填充。  
  - **边界条件**：`pairs` 可能为空，此时答案应直接返回原字符串；或者所有下标都在同一个分量，需要一次完整排序。  
- **下次遇到同类题的第一步**：**把题目抽象成图**——先画出节点和边，判断“连通分量”是关键，然后决定用 **并查集** 还是 **DFS/BFS** 来获取这些分量。这样思路就已经锁定，后面的排序自然水到渠成。