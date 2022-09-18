# #1938. 最大基因差查询 / Maximum Genetic Difference Query

> 难度：困难 · 标签：Array、Hash Table、Bit Manipulation、Depth-First Search、Trie · [LeetCode 链接](https://leetcode.com/problems/maximum-genetic-difference-query/)

---

## 题目（英文原版）

**Description**

There is a rooted tree consisting of n nodes numbered 0 to n - 1. Each node's number denotes its unique genetic value (i.e. the genetic value of node x is x). The genetic difference between two genetic values is defined as the bitwise-XOR of their values. You are given the integer array parents, where parents[i] is the parent for node i. If node x is the root of the tree, then parents[x] == -1.
You are also given the array queries where queries[i] = [nodei, vali]. For each query i, find the maximum genetic difference between vali and pi, where pi is the genetic value of any node that is on the path between nodei and the root (including nodei and the root). More formally, you want to maximize vali XOR pi.
Return an array ans where ans[i] is the answer to the ith query.

**Examples**

**Example 1:**

```
Input: parents = [-1,0,1,1], queries = [[0,2],[3,2],[2,5]]
Output: [2,3,7]
Explanation: The queries are processed as follows:
- [0,2]: The node with the maximum genetic difference is 0, with a difference of 2 XOR 0 = 2.
- [3,2]: The node with the maximum genetic difference is 1, with a difference of 2 XOR 1 = 3.
- [2,5]: The node with the maximum genetic difference is 2, with a difference of 5 XOR 2 = 7.
```

**Example 2:**

```
Input: parents = [3,7,-1,2,0,7,0,2], queries = [[4,6],[1,15],[0,5]]
Output: [6,14,7]
Explanation: The queries are processed as follows:
- [4,6]: The node with the maximum genetic difference is 0, with a difference of 6 XOR 0 = 6.
- [1,15]: The node with the maximum genetic difference is 1, with a difference of 15 XOR 1 = 14.
- [0,5]: The node with the maximum genetic difference is 2, with a difference of 5 XOR 2 = 7.
```

**Constraints**

- 2 <= parents.length <= 105
- 0 <= parents[i] <= parents.length - 1 for every node i that is not the root.
- parents[root] == -1
- 1 <= queries.length <= 3 * 104
- 0 <= nodei <= parents.length - 1
- 0 <= vali <= 2 * 105

---

## 题目（中文翻译）

存在一棵**根树**（rooted tree），包含 `n` 个节点，编号为 `0` 到 `n - 1`。每个节点的编号即其唯一的**基因值**（genetic value），即节点 `x` 的基因值为 `x`。两个基因值之间的**基因差**（genetic difference）定义为它们的**位异或**（bitwise‑XOR）结果。

给定整数数组 `parents`，其中 `parents[i]` 表示节点 `i` 的父节点。如果节点 `x` 为根，则 `parents[x] == -1`。

另给定数组 `queries`，其中 `queries[i] = [node_i, val_i]`。对于每个查询 `i`，需要在 **从 `node_i` 到根的路径上**（包括 `node_i` 和根）任选一个节点 `p_i`，使得 `val_i XOR p_i` 最大化，其中 `p_i` 为该节点的基因值。返回数组 `ans`，其中 `ans[i]` 为第 `i` 个查询的答案。

---

### 示例

**示例 1：**

```
Input: parents = [-1,0,1,1], queries = [[0,2],[3,2],[2,5]]
Output: [2,3,7]
Explanation:
- [0,2]: 路径上唯一的节点是 0，基因差为 2 XOR 0 = 2。
- [3,2]: 路径为 3 → 1 → 0，基因差最大的节点是 1，得到 2 XOR 1 = 3。
- [2,5]: 路径为 2 → 1 → 0，基因差最大的节点是 2，得到 5 XOR 2 = 7。
```

**示例 2：**

```
Input: parents = [3,7,-1,2,0,7,0,2], queries = [[4,6],[1,15],[0,5]]
Output: [6,14,7]
Explanation:
- [4,6]: 路径为 4 → 0 → 2 → 3 → -1（根），基因差最大的节点是 0，得到 6 XOR 0 = 6。
- [1,15]: 路径为 1 → 7 → -1（根），基因差最大的节点是 1，得到 15 XOR 1 = 14。
- [0,5]: 路径为 0 → 2 → 3 → -1（根），基因差最大的节点是 2，得到 5 XOR 2 = 7。
```

---

### 约束条件

- `2 <= parents.length <= 10^5`
- 对于所有非根节点 `i`，`0 <= parents[i] <= parents.length - 1`
- `parents[root] == -1`
- `1 <= queries.length <= 3 * 10^4`
- `0 <= node_i <= parents.length - 1`
- `0 <= val_i <= 2 * 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个查询** `[node, val]`，先把从 `node` 到根节点的所有节点编号（即基因值）收集起来，然后把 `val` 和这些基因值逐个做异或，取最大值即可。

- **收集路径**：因为树是有父指针 `parents` 的，只需要不停地把当前节点的父亲取出来，直到遇到根（`parent == -1`）为止。可以把路径看成“一条向上爬的链”，就像在楼梯上往上走，每走一步就把这一步的编号记下来。
- **求最大异或**：遍历路径上的每个基因值 `p`，计算 `val ^ p`，记录最大的那个。异或运算可以直接用 Python 的 `^` 操作符。

> **为什么正确**  
> 题目要求的最大基因差就是在 **所有合法的路径节点** 中挑一个，使得 `val XOR p` 最大。暴力遍历把所有合法的 `p` 都算了一遍，自然不会错。

> **时间/空间复杂度**  
> - 对每个查询我们都要 **向上遍历一次**，最坏情况下要走到根，路径长度最多是 `n`（树的高度），所以单个查询是 `O(n)`。  
> - 查询总数是 `q`，整体时间就是 `O(q·n)`。如果 `n=10⁵，q=3·10⁴`，这已经是 **几万亿次**的计算，根本跑不完。  
> - 只用了几个数组保存父指针和答案，额外空间是 `O(1)`（不计输入本身）。

#### 代码（Python）

```python
from typing import List

def maxGeneticDifference_bruteforce(parents: List[int],
                                    queries: List[List[int]]) -> List[int]:
    ans = []
    for node, val in queries:                     # 逐个处理查询
        cur = node
        best = 0
        while cur != -1:                           # 向上走到根
            best = max(best, val ^ cur)            # 计算 xor 并取最大
            cur = parents[cur]                     # 上跳到父节点
        ans.append(best)
    return ans
```

#### 复杂度

- **时间复杂度**：`O(q · n)`  
  - `q` 是查询数，`n` 是树的节点数。  
  - 想象成“每个查询都要走一遍整棵树”，所以非常慢。

- **空间复杂度**：`O(1)`（不计输入输出）  
  - 只用了几个临时变量，额外占用的内存几乎可以忽略。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **每次都要遍历整条路径**。如果我们能够在遍历一次树的过程中，把每条路径上出现的基因值组织成一种**可以快速求最大异或**的数据结构，那么每个查询就可以 **`O(log C)`**（`C` 为基因值范围）得到答案，而不必再重复遍历。

##### 关键点 1：用 Trie（前缀树）存二进制数

- **Trie**：想象一本字典，单词是二进制位序列（从最高位到最低位），每个节点有两个分支，分别对应位 `0` 和位 `1`。  
- 把一个整数 `x` 插入 Trie 时，沿着它的二进制位从最高位走下去，若对应分支不存在就新建。  
- 当我们想找 **与 `val` 异或最大的数** 时，只要在每一位上「尽量走相反的分支」：因为 `1 ^ 0 = 1`，`0 ^ 1 = 1`，能够让该位贡献 `1`（即更大）。

> 类比：如果把二进制看成「灯的开关」，我们希望在每个灯位上让两个开关的状态不同，这样灯亮（异或为 1）得分最高。

- 查询时间是 **位数的常数**，本题基因值和 `val` 最大到 `2·10⁵`，二进制最多 18 位（`2¹⁸ = 262144`），所以每次查询 `O(18) ≈ O(1)`。

##### 关键点 2：在 DFS 中动态维护路径 Trie

- 我们对整棵树做一次 **深度优先搜索（DFS）**，从根向下遍历。  
- **进入一个节点** 时，把该节点的基因值（即节点编号）**插入**当前路径的 Trie。此时 Trie 中恰好保存了从根到当前节点的所有基因值。  
- **在该节点处理所有属于它的查询**：直接在 Trie 上查询与 `val` 异或最大的数，得到答案。  
- **离开节点（递归返回）** 时，需要把该节点的基因值 **从 Trie 中删除**，否则它会错误地出现在后面兄弟子树的路径里。  
- 删除同样只需要沿着二进制路径走一次，记录每个 Trie 节点的 **计数**（该节点被多少数经过），计数归零时把节点删掉即可。

> 这样，**每条根到任意节点的路径只被维护一次**，所有查询的总时间是 `O((n+q)·log C)`，远快于暴力。

##### 关键点 3：Trie 的实现细节

```text
class TrieNode:
    child = [None, None]   # 对应位 0 和位 1
    cnt   = 0              # 经过该节点的数的个数
```

- 插入 `x`：从最高位（第 17 位）到第 0 位，取 `bit = (x>>i) & 1`，若对应 child 为 None 则新建，随后 `node = node.child[bit]; node.cnt += 1`。
- 删除 `x`：同样遍历位，`node = node.child[bit]; node.cnt -= 1`，若 `node.cnt == 0` 可以把父节点的对应指针设为 None（可选，省内存）。
- 查询最大异或：对每一位尝试走 **相反位** 的子树（`prefer = 1-bit`），如果该子树不存在或计数为 0，只能走同位子树。一路累加得到与 `val` 异或最大的数。

##### 步骤概览

1. **构造邻接表**（因为只有父指针，需要把它转换为子节点列表，方便 DFS）。  
2. **把查询按节点分组**：`queries_by_node[node]` 保存所有 `(idx, val)`，`idx` 是原查询下标，方便把答案写回。  
3. **初始化空 Trie**，在 DFS 的根节点前先插入根的基因值（根也在路径里）。  
4. **DFS 递归**  
   - 插入当前节点值  
   - 处理该节点的所有查询（Trie 查询）  
   - 递归遍历子节点  
   - 删除当前节点值（回溯）  
5. 返回答案数组。

#### 代码（Python）

```python
from typing import List, Dict
import sys
sys.setrecursionlimit(300000)

class TrieNode:
    __slots__ = ("child", "cnt")
    def __init__(self):
        self.child = [None, None]   # 0 -> left, 1 -> right
        self.cnt = 0                # 有多少数经过这里

class Trie:
    def __init__(self, max_bit: int = 17):   # 2*10^5 < 2^18
        self.root = TrieNode()
        self.max_bit = max_bit

    def add(self, num: int, delta: int) -> None:
        """delta = +1 表示插入，-1 表示删除"""
        node = self.root
        node.cnt += delta
        for i in range(self.max_bit, -1, -1):
            bit = (num >> i) & 1
            if node.child[bit] is None:
                node.child[bit] = TrieNode()
            node = node.child[bit]
            node.cnt += delta

    def max_xor(self, num: int) -> int:
        """在 Trie 中找出使 num ^ x 最大的 x，返回该最大异或值"""
        node = self.root
        if node.cnt == 0:      # Trie 为空（理论上不会在本题出现）
            return 0
        res = 0
        for i in range(self.max_bit, -1, -1):
            bit = (num >> i) & 1
            # 想走相反的位，让异或结果在该位得到 1
            prefer = 1 - bit
            if node.child[prefer] is not None and node.child[prefer].cnt > 0:
                # 能走相反位，异或该位得到 1
                res |= (1 << i)
                node = node.child[prefer]
            else:
                # 只能走相同位
                node = node.child[bit]
        return res

def maxGeneticDifference(parents: List[int],
                         queries: List[List[int]]) -> List[int]:
    n = len(parents)
    # 1️⃣ 建立树的邻接表（子节点列表）
    children = [[] for _ in range(n)]
    root = -1
    for i, p in enumerate(parents):
        if p == -1:
            root = i
        else:
            children[p].append(i)

    # 2️⃣ 把查询按节点分组
    q_by_node: Dict[int, List[tuple]] = {i: [] for i in range(n)}
    for idx, (node, val) in enumerate(queries):
        q_by_node[node].append((idx, val))

    ans = [0] * len(queries)
    trie = Trie()                     # 全局唯一的 Trie，随 DFS 动态维护

    # 3️⃣ 深度优先搜索 + Trie 动态维护
    def dfs(u: int):
        # 进入节点 u 前，先把它的基因值加入 Trie
        trie.add(u, +1)

        # 处理所有落在 u 的查询
        for idx, val in q_by_node[u]:
            ans[idx] = trie.max_xor(val)   # 直接得到最大 xor

        # 递归遍历子节点
        for v in children[u]:
            dfs(v)

        # 离开节点 u，撤销加入的基因值
        trie.add(u, -1)

    # 从根开始遍历
    dfs(root)
    return ans
```

#### 复杂度

- **时间复杂度**：`O((n + q) · B)`，其中 `B = 18` 是二进制位数的上界。  
  - 插入/删除一次基因值需要遍历 `B` 位 → `O(B)`。  
  - 每个查询在 Trie 中寻找最大异或同样是 `O(B)`。  
  - 因为每个节点只被插入一次、删除一次，所有节点共 `O(n·B)`，所有查询共 `O(q·B)`，故总时间约为 `O((n+q)·18)`，在 10⁵ 规模下完全可接受。

- **空间复杂度**：`O(n·B)`（Trie 最多包含 `n` 条数，每条数占 `B` 个节点），约为 `n·18` 个小对象，实际约几 MB。  
  - 额外的邻接表、查询分组和答案数组共 `O(n + q)`。  
  - 与暴力解的 `O(1)` 额外空间相比，多用了一个 Trie，但仍在可接受范围。

---

## 心得

- **核心技巧**：在树的**路径上**使用 **Trie（二进制字典树）** 动态维护所有出现的数，以 **O(位数)** 完成最大异或查询。  
- **适用的题型**  
  1. “在一条路径上求最大/最小 XOR”——如 LeetCode 421 *Maximum XOR of Two Numbers in an Array*（单数组）或 1803 *Maximum XOR Secondary Query*（多次查询）。  
  2. “在子树或前缀集合中求最大异或”——如 421、421 的树形变体（本题）。  
  3. “需要在动态集合中快速求最大异或”——如在线算法、滑动窗口最大异或等。

- **一句话总结解题钥匙**：**把“路径上的所有基因值”抽象成一个随 DFS 增删的二进制 Trie，利用“异或想让位相反” 的贪心查询即可在常数时间得到答案。**

---

## 反思

- **第一反应**：看到“树 + XOR 最大化”，立刻想到 **Trie**，但最初会忘记把它和 **DFS 结合**，导致想把每个查询单独建 Trie，时间仍然爆炸。  
- **最容易踩的坑**  
  1. **忘记回溯删除**：在递归返回时不把当前节点的基因值从 Trie 中删掉，后面的兄弟子树会错误地把它当成合法路径节点。  
  2. **Trie 计数不正确**：仅用 `None/Exists` 判断会导致在同一数出现多次（如同一个基因值在不同层）时错误删除。使用 `cnt` 计数可以安全回溯。  
  3. **位数选择错误**：若取的最高位不足（比如只取到 16 位），大于 `2^16` 的数会被截断，导致答案错误。应根据约束取足够的位（这里 `2·10⁵ < 2¹⁸`，取 17~0 共 18 位）。  
- **下次遇到同类题**：**第一步**先把“所有涉及的数放进一个可以快速求最大异或的结构”——即 **构造 Trie**，随后思考 **如何在遍历树/数组的过程中动态维护这个结构**（插入、查询、删除）。这样就能把原本的 `O(n·q)` 降到 `O((n+q)·logC)`。