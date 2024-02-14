# #2581. 计数可能的根节点数 / Count Number of Possible Root Nodes

> 难度：困难 · 标签：Array、Hash Table、Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/count-number-of-possible-root-nodes/)

---

## 题目（英文原版）

**Description**

Alice has an undirected tree with n nodes labeled from 0 to n - 1. The tree is represented as a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
Alice wants Bob to find the root of the tree. She allows Bob to make several guesses about her tree. In one guess, he does the following:
Bob's guesses are represented by a 2D integer array guesses where guesses[j] = [uj, vj] indicates Bob guessed uj to be the parent of vj.
Alice being lazy, does not reply to each of Bob's guesses, but just says that at least k of his guesses are true.
Given the 2D integer arrays edges, guesses and the integer k, return the number of possible nodes that can be the root of Alice's tree. If there is no such tree, return 0.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[1,2],[1,3],[4,2]], guesses = [[1,3],[0,1],[1,0],[2,4]], k = 3
Output: 3
Explanation: 
Root = 0, correct guesses = [1,3], [0,1], [2,4]
Root = 1, correct guesses = [1,3], [1,0], [2,4]
Root = 2, correct guesses = [1,3], [1,0], [2,4]
Root = 3, correct guesses = [1,0], [2,4]
Root = 4, correct guesses = [1,3], [1,0]
Considering 0, 1, or 2 as root node leads to 3 correct guesses.
```

**Example 2:**

```
Input: edges = [[0,1],[1,2],[2,3],[3,4]], guesses = [[1,0],[3,4],[2,1],[3,2]], k = 1
Output: 5
Explanation: 
Root = 0, correct guesses = [3,4]
Root = 1, correct guesses = [1,0], [3,4]
Root = 2, correct guesses = [1,0], [2,1], [3,4]
Root = 3, correct guesses = [1,0], [2,1], [3,2], [3,4]
Root = 4, correct guesses = [1,0], [2,1], [3,2]
Considering any node as root will give at least 1 correct guess.
```

**Constraints**

- edges.length == n - 1
- 2 <= n <= 105
- 1 <= guesses.length <= 105
- 0 <= ai, bi, uj, vj <= n - 1
- ai != bi
- uj != vj
- edges represents a valid tree.
- guesses[j] is an edge of the tree.
- guesses is unique.
- 0 <= k <= guesses.length

---

## 题目（中文翻译）

Alice 有一棵无向树，节点编号为 `0` 到 `n - 1`。树用长度为 `n - 1` 的二维整数数组 `edges` 表示，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条边。

Alice 想让 Bob 找出这棵树的根节点。她允许 Bob 对树进行若干次猜测。一次猜测的形式如下：

- Bob 的猜测用二维整数数组 `guesses` 表示，其中 `guesses[j] = [u_j, v_j]` 表示 Bob 猜测 `u_j` 是 `v_j` 的父节点（parent）。

Alice 很懒，不会对每一次猜测单独回复，而是统一说明 **至少** 有 `k` 条猜测是正确的。

给定二维整数数组 `edges`、`guesses` 与整数 `k`，返回可能成为 Alice 树的根节点的节点数。如果不存在满足条件的根节点，返回 `0`。

### 示例

**示例 1**

```
Input: edges = [[0,1],[1,2],[1,3],[4,2]],
       guesses = [[1,3],[0,1],[1,0],[2,4]],
       k = 3
Output: 3
Explanation:
Root = 0, correct guesses = [1,3], [0,1], [2,4]
Root = 1, correct guesses = [1,3], [1,0], [2,4]
Root = 2, correct guesses = [1,3], [1,0], [2,4]
Root = 3, correct guesses = [1,0], [2,4]
Root = 4, correct guesses = [1,3], [1,0]
考虑根节点为 0、1 或 2 时，能够得到 3 条正确的猜测。
```

**示例 2**

```
Input: edges = [[0,1],[1,2],[2,3],[3,4]],
       guesses = [[1,0],[3,4],[2,1],[3,2]],
       k = 1
Output: 5
Explanation:
Root = 0, correct guesses = [3,4]
Root = 1, correct guesses = [1,0], [3,4]
Root = 2, correct guesses = [1,0], [2,1], [3,4]
Root = 3, correct guesses = [1,0], [2,1], [3,2], [3,4]
Root = 4, correct guesses = [1,0], [2,1], [3,2]
任意节点作为根都能得到至少 1 条正确的猜测。
```

### 约束条件

- `edges.length == n - 1`
- `2 <= n <= 10^5`
- `1 <= guesses.length <= 10^5`
- `0 <= a_i, b_i, u_j, v_j <= n - 1`
- `a_i != b_i`
- `u_j != v_j`
- `edges` 构成一棵有效的树。
- `guesses[j]` 是树中的一条边。
- `guesses` 中的元素互不相同。
- `0 <= k <= guesses.length`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个节点都当作根**，重新算一遍这棵树的父子关系，然后和 `guesses` 逐个比对，看看有多少条猜测是对的。  

- **数据结构**  
  - **邻接表**：把 `edges` 用 `list[ list[int] ]` 存起来，类似于“朋友列表”，`adj[u]` 里装的是和 `u` 直接相连的节点。  
  - **哈希表（集合）**：把所有猜测 `(parent, child)` 放进 `set`，就像把字典的“词条”存进去，查找时只要看键是否存在，时间是 O(1)。  

- **为什么正确**  
  对每个可能的根 `r`，我们只要做一次 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）**，得到从 `r` 出发的 **父指针** `parent[x]`（即 `r` 为根时每个节点的直接父亲）。  
  只要 `guesses` 中的 `(u, v)` 与 `parent[v] == u` 同时成立，这条猜测就是真的。把所有真的猜测数加起来，和 `k` 比较，就能判断 `r` 能否成为合法根。  

- **时间/空间复杂度**  
  - 对每个根我们都要遍历整棵树一次，树有 `n` 个节点，所以 **时间** 为 `O(n * n)`，即 **平方级**。如果再把每条猜测都检查一遍（`g = len(guesses)`），复杂度是 `O(n * (n + g))`。  
    - **大白话**：如果树有 10 000 个节点，暴力解要跑 10 000 次遍历，每次遍历也要遍历 10 000 个节点，简直是 **100 000 000** 步，明显太慢。  
  - 我们只需要保存邻接表、父指针数组和猜测集合，**空间** 为 `O(n + g)`。  

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List, Set, Tuple

def possible_roots_bruteforce(edges: List[List[int]],
                              guesses: List[List[int]],
                              k: int) -> int:
    n = len(edges) + 1                         # 节点数
    # 1️⃣ 建图：邻接表
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    # 2️⃣ 把猜测放进集合，查找更快
    guess_set: Set[Tuple[int, int]] = { (u, v) for u, v in guesses }

    def bfs_root(root: int) -> List[int]:
        """返回以 root 为根时的父指针数组 parent[x]（root 的父亲设为 -1）"""
        parent = [-1] * n
        q = deque([root])
        while q:
            cur = q.popleft()
            for nb in adj[cur]:
                if nb == parent[cur]:          # 已经回到父节点，跳过
                    continue
                parent[nb] = cur
                q.append(nb)
        return parent

    ans = 0
    # 3️⃣ 逐个根尝试
    for r in range(n):
        parent = bfs_root(r)                    # O(n)
        # 统计满足的猜测数
        correct = sum(1 for u, v in guesses if parent[v] == u)   # O(g)
        if correct >= k:
            ans += 1
    return ans
```

#### 复杂度

- **时间复杂度**：`O(n * (n + g))`  
  - 解释：对每个根要遍历整棵树一次（`n` 步），再检查所有猜测（`g` 步），所以总步数是 `n` × (`n` + `g`)。  
- **空间复杂度**：`O(n + g)`  
  - 解释：邻接表占 `O(n)`，猜测集合占 `O(g)`，其余临时数组也都是线性级别。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于：每次把根换了以后，都要 **重新遍历整棵树** 来算父指针。  
如果我们能够在 **一次遍历** 中得到根为 `0` 时的正确猜测数，然后在 **移动根** 的过程中 **增量更新**，就能把总时间降到线性 `O(n + g)`。

**关键观察**：

1. 把树固定一个根（比如 0），用一次 DFS 计算出每个节点的父亲 `parent[x]`。  
2. 统计在这个根下，有多少猜测是正确的，记为 `cur_correct`。  
3. 当我们把根从节点 `u` 移到它的相邻节点 `v` 时，树的方向会 **翻转** 那条 `u‑v` 边：  
   - 之前 `u` 是 `v` 的父亲，之后 `v` 成为 `u` 的父亲。  
   - 这唯一的变化会影响两条可能的猜测：`(u, v)` 和 `(v, u)`。  
4. 因此 **只需要检查这两条猜测** 是否在 `guesses` 中，就能快速得到新根下的正确猜测数：  
   - 如果 `(u, v)` 本来在 `guesses`，那么把根从 `u` 移到 `v` 时，这条猜测 **不再成立**，`cur_correct` 减 1。  
   - 如果 `(v, u)` 在 `guesses`，则在新根下它 **成立**，`cur_correct` 加 1。  

这就是 **“重根 DP（rerooting DP）”** 的思路：先算一次根为 0 的答案，然后在 DFS 中 **边走边更新**，把根从父节点移动到子节点，时间只会是 `O(1)`。

**核心算法/数据结构**：

- **邻接表**（同上）  
- **集合** `guess_set` 用来 O(1) 判断一条有向边是否是猜测  
- **两次 DFS**：  
  1. 第一次 `dfs1` 计算 `parent` 并统计 `cur_correct`（根为 0）  
  2. 第二次 `dfs2` 进行 **重根转移**，每到一个节点就判断 `cur_correct >= k` 是否成立，累计答案  

**类比**：想象一棵树是一个“转盘”，根在盘子中心。我们先把盘子固定在 0 位置，记录好有多少指针指向正确的方向。然后把盘子顺时针转到相邻的格子，只会改变两根指针的方向，其余指针保持不变——所以更新很快。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List, Set, Tuple

def possible_roots_optimal(edges: List[List[int]],
                           guesses: List[List[int]],
                           k: int) -> int:
    n = len(edges) + 1
    # 1️⃣ 建图
    adj = [[] for _ in range(n)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)

    # 2️⃣ 把猜测放进集合，便于 O(1) 查询
    guess_set: Set[Tuple[int, int]] = { (u, v) for u, v in guesses }

    # 3️⃣ 第一次 DFS：算出以 0 为根时的父指针，同时统计正确猜测数
    parent = [-1] * n
    cur_correct = 0                     # root = 0 时的正确猜测数

    def dfs1(u: int, p: int):
        nonlocal cur_correct
        parent[u] = p
        for v in adj[u]:
            if v == p:
                continue
            # 若 (u, v) 在猜测里，则这条猜测在根为 0 时成立
            if (u, v) in guess_set:
                cur_correct += 1
            dfs1(v, u)

    dfs1(0, -1)

    # 4️⃣ 第二次 DFS：重根转移，边走边更新 cur_correct
    answer = 0

    def dfs2(u: int, p: int):
        nonlocal cur_correct, answer
        # 检查当前根 u 是否满足条件
        if cur_correct >= k:
            answer += 1
        for v in adj[u]:
            if v == p:
                continue
            # ---- 把根从 u 移到 v 的增量更新 ----
            # 1) 失去的猜测：如果 (u, v) 在集合里，之前算对了，现在不对了
            if (u, v) in guess_set:
                cur_correct -= 1
            # 2) 新获得的猜测：如果 (v, u) 在集合里，之前不对，现在对了
            if (v, u) in guess_set:
                cur_correct += 1

            dfs2(v, u)                     # 递归进入子树

            # ---- 回溯：恢复到进入 v 前的状态 ----
            if (u, v) in guess_set:
                cur_correct += 1
            if (v, u) in guess_set:
                cur_correct -= 1

    dfs2(0, -1)
    return answer
```

#### 复杂度

- **时间复杂度**：`O(n + g)`  
  - 第一次 DFS 访问每条边一次，统计猜测 O(g)（因为每条猜测只在判断 `(u, v) in guess_set` 时检查一次）。  
  - 第二次 DFS 仍然只遍历每条边一次，每次转移根只检查两条可能的猜测，时间是常数级别。  
  - 与暴力解相比，**把 `n` 次完整遍历压缩成了 2 次遍历**，所以即使 `n = 10^5` 也能轻松跑完。  

- **空间复杂度**：`O(n + g)`  
  - 邻接表 `O(n)`，猜测集合 `O(g)`，递归栈最坏深度为 `n`（树的高度），同样是线性级别。

---

## 心得

- **核心技巧**：**重根 DP（Rerooting DP）** —— 先算一个根的答案，再在相邻节点之间“搬动根”，利用局部增量更新把整体复杂度降到线性。  
- **适用题型**（类似思路）  
  1. LeetCode 2741 *Count Good Paths*（需要在树上移动根）  
  2. LeetCode 1519 *Number of Nodes in the Largest Component*（利用子树信息重算）  
  3. 任何涉及“在树上任选根”且判断某种属性的题目（如 “根的子树满足条件”）  
- **一句话总结解题钥匙**：**只在根移动的那一条边上检查猜测，其他部分保持不变**——这样就能在 O(1) 时间内更新答案。

---

## 反思

- **第一反应**：把每个节点都当根暴力遍历。直觉上简单，却忽视了树结构的“局部不变性”。  
- **最容易踩的坑**  
  - **忘记回溯**：在 `dfs2` 中把根从 `u` 移到 `v` 后，需要在递归返回时把 `cur_correct` 恢复，否则后面的分支会基于错误的计数继续。  
  - **猜测方向写反**：`guesses` 是有向的 `(parent, child)`，不能把它当成无向边来比较。  
  - **递归深度**：`n` 可达 `10^5`，Python 递归可能栈溢出。可以在开头加 `sys.setrecursionlimit(200000)`，或改成显式栈的迭代写法。  
- **下次遇到同类题**：先 **固定一个根**，计算完整信息；再 **思考根移动时仅会影响哪些局部结构**，利用增量更新实现线性遍历。这样可以把看似 “每个根都要遍历” 的暴力思路，变成 “一次遍历全部搞定”。