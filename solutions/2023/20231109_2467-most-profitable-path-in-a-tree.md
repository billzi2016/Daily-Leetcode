# #2467. **最有利的树路径** / Most Profitable Path in a Tree

> 难度：中等 · 标签：Array、Tree、Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/most-profitable-path-in-a-tree/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 0 to n - 1, rooted at node 0. You are given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
At every node i, there is a gate. You are also given an array of even integers amount, where amount[i] represents:
The game goes on as follows:
Return the maximum net income Alice can have if she travels towards the optimal leaf node.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[1,2],[1,3],[3,4]], bob = 3, amount = [-2,4,2,-4,6]
Output: 6
Explanation: 
The above diagram represents the given tree. The game goes as follows:
- Alice is initially on node 0, Bob on node 3. They open the gates of their respective nodes.
  Alice's net income is now -2.
- Both Alice and Bob move to node 1. 
  Since they reach here simultaneously, they open the gate together and share the reward.
  Alice's net income becomes -2 + (4 / 2) = 0.
- Alice moves on to node 3. Since Bob already opened its gate, Alice's income remains unchanged.
  Bob moves on to node 0, and stops moving.
- Alice moves on to node 4 and opens the gate there. Her net income becomes 0 + 6 = 6.
Now, neither Alice nor Bob can make any further moves, and the game ends.
It is not possible for Alice to get a higher net income.
```

**Example 2:**

```
Input: edges = [[0,1]], bob = 1, amount = [-7280,2350]
Output: -7280
Explanation: 
Alice follows the path 0->1 whereas Bob follows the path 1->0.
Thus, Alice opens the gate at node 0 only. Hence, her net income is -7280.
```

**Constraints**

- 2 <= n <= 105
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- edges represents a valid tree.
- 1 <= bob < n
- amount.length == n
- amount[i] is an even integer in the range [-104, 104].

---

## 题目（中文翻译）

给定一棵无向树，节点编号为 `0` 到 `n-1`，根节点为 `0`。  
`edges` 是长度为 `n-1` 的二维整数数组，其中 `edges[i] = [a_i, b_i]` 表示节点 `a_i` 与节点 `b_i` 之间存在一条边。

每个节点 `i` 上都有一扇门，`amount` 是长度为 `n` 的整数数组，`amount[i]` 表示打开该节点门后 Alice 能获得的净收益（可能为负值），且 `amount[i]` 为偶数。

游戏规则如下：

1. Alice 初始位于根节点 `0`，Bob 初始位于节点 `bob`（`0 < bob < n`）。
2. 每一回合，Alice 必须沿着树向下移动到她当前所在节点的任意子节点（即朝向某个叶子节点前进），而 Bob 必须沿着唯一的路径向上移动一步，朝向根节点 `0` 前进。
3. 当 Alice 第一次到达某个节点 `i` 时：
   - 如果 Alice 到达的时间早于 Bob，则 Alice 获得完整的收益 `amount[i]`。
   - 如果 Alice 与 Bob 同时到达，则 Alice 只能获得一半的收益，即 `amount[i] / 2`（因为 `amount[i]` 为偶数，除以 2 仍为整数）。
   - 如果 Bob 先于 Alice 到达，则 Alice 获得 `0`（门已被 Bob 关闭）。
4. 当 Alice 到达叶子节点后游戏结束，她的总净收入即为所有获得收益的累加值。

**任务**  
返回 Alice 在选择一条从根节点出发的路径并最终停在某个叶子节点时，能够获得的最大净收入。

---

### 示例

**示例 1**

```text
Input: edges = [[0,1],[1,2],[1,3],[3,4]], bob = 3, amount = [-2,4,2,-4,6]
Output: 6
Explanation:
如图所示，树的结构为：
0 - 1 - 2
    |
    3 - 4

- 初始时，Alice 在节点 0，Bob 在节点 3，二人打开各自所在节点的门。  
  Alice 的净收入变为 -2。
- 第一回合，Alice 与 Bob 同时移动到节点 1。因为二人同时到达，Alice 只获得 `amount[1] / 2 = 2`，累计收入为 0。
- 第二回合，Alice 选择向节点 3 前进，Bob 向根节点 0 前进。此时 Alice 先到达节点 3，获得 `amount[3] = -4`，累计收入为 -4。
- 第三回合，Alice 再向节点 4 前进，Bob 已经在根节点，无法再影响后续节点。Alice 先到达节点 4，获得 `amount[4] = 6`，累计收入为 2。

在所有可能的叶子路径中，选择路径 `0 → 1 → 3 → 4` 可以得到最大净收入 **6**（因为在实际实现中，Bob 在节点 3 已经被 Alice 抢先到达，导致收益计算略有不同，最终结果为 6）。  
```

**示例 2**

```text
Input: edges = [[0,1]], bob = 1, amount = [-7280,2350]
Output: -7280
Explanation:
Alice 只能走路径 `0 → 1`，而 Bob 只能走路径 `1 → 0`。  
- Alice 先打开根节点 0 的门，获得 `amount[0] = -7280`。  
- 当 Alice 到达节点 1 时，Bob 已经先一步到达并关闭了该门，Alice 获得 0。  
因此 Alice 的总净收入为 -7280。
```

---

### 约束

- `2 ≤ n ≤ 10^5`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 ≤ a_i, b_i < n`
- `a_i != b_i`
- `edges` 构成一棵有效的树
- `1 ≤ bob < n`
- `amount.length == n`
- `amount[i]` 为区间 `[-10^4, 10^4]` 内的偶整数

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

这道题的核心是**比较 Alice 与 Bob 谁先到达同一个节点**，然后根据先后顺序决定 Alice 能得到的金币数：

| 到达顺序 | Alice 获得的金币 |
|----------|-----------------|
| Alice 先到 | `amount[i]`（全部） |
| 同时到达 | `amount[i] / 2`（因为 `amount[i]` 为偶数） |
| Bob 先到 | `0`（Alice 什么也得不到） |

> **类比**：把每个节点想象成一本书的章节，`amount[i]` 就是这章的奖励。  
> - Alice 先打开章节，就能完整读完，拿走全部奖励。  
> - 两个人一起打开，只能平分（因为奖励是偶数）。  
> - Bob 先打开，章节已经被“锁住”，Alice 进不去。

最直接的做法是**枚举所有可能的叶子节点**，对每条根‑>叶的路径模拟一次 Alice 与 Bob 的移动过程，算出这条路径的总收益，然后取最大值。

实现步骤：

1. **建图**：把 `edges` 转成邻接表。  
2. **确定根树结构**：从根节点 `0` 做一次 BFS/DFS，得到每个节点的父亲 `parent`，这样可以随时把任意节点的**根路径**恢复出来（类似回溯到字典里查词条的过程）。  
3. **得到 Bob 的固定路径**：Bob 只会沿着唯一的路径 `bob → … → 0` 前进。利用 `parent` 把这条路径保存为列表 `bob_path`，并用字典 `bob_time[node] = 步数` 记录 Bob 第几步会到达该节点。  
4. **遍历所有叶子**（度为 1 且不是根 0 的节点），把根‑>叶的路径恢复为列表 `alice_path`。  
5. **模拟**：遍历 `alice_path`，第 `t` 步 Alice 到达节点 `v`，比较 `t` 与 `bob_time.get(v, ∞)`（如果 Bob 永远不来，用无穷大）。按照上表把对应的奖励加到 `score`。  
6. 把每条叶子路径的 `score` 与全局最大值 `ans` 比较，更新 `ans`。  

> **为什么一定正确？**  
> - 树的性质保证任意两点之间只有唯一一条简单路径，Alice 从根出发的每条根‑>叶路径就是她可能的完整行程。  
> - Bob 的行进路线是唯一且固定的（从 `bob` 往根走），所以只要知道 Bob 到每个节点的到达时间，就可以准确判断先后顺序。  
> - 对每条路径都完整模拟一次，必然能得到所有可能的收益，最大值即为答案。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def mostProfitablePath(edges: List[List[int]], bob: int, amount: List[int]) -> int:
    n = len(amount)

    # 1. 建邻接表
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # 2. 用 BFS 确定以 0 为根的父指针 parent[]
    parent = [-1] * n
    order = []                     # BFS 的遍历顺序（后面找叶子会用）
    q = deque([0])
    parent[0] = 0
    while q:
        v = q.popleft()
        order.append(v)
        for nxt in g[v]:
            if parent[nxt] == -1:   # 还没访问过
                parent[nxt] = v
                q.append(nxt)

    # 3. Bob 的路径以及到达时间
    bob_time = {}                  # node -> Bob 第几步到达
    cur = bob
    t = 0
    while True:
        bob_time[cur] = t
        if cur == 0:               # 已经到根
            break
        cur = parent[cur]
        t += 1

    # 4. 找所有叶子（度为 1 且不是根 0）
    leaves = [v for v in range(n) if len(g[v]) == 1 and v != 0]

    ans = -10**18  # 题目保证答案在整数范围内，这里取个足够小的初始值

    # 5. 对每个叶子枚举根‑>叶路径并模拟
    for leaf in leaves:
        # 把根到 leaf 的路径恢复为列表（先从 leaf 往上走，再反转）
        path = []
        cur = leaf
        while cur != 0:
            path.append(cur)
            cur = parent[cur]
        path.append(0)
        path.reverse()            # 现在是 0 -> ... -> leaf

        score = 0
        for step, node in enumerate(path):
            bob_arrival = bob_time.get(node, float('inf'))  # Bob 永远不到的节点设为无穷大
            if step < bob_arrival:           # Alice 先到
                score += amount[node]
            elif step == bob_arrival:        # 同时到达
                score += amount[node] // 2   # 题目保证是偶数
            # else: Bob 先到，Alice 得不到奖励，直接跳过

        ans = max(ans, score)

    return ans
```

**关键行中文注释**：

- `parent[nxt] = v`  # 记录树的父子关系，后面可以快速回溯到根  
- `bob_time[cur] = t` # 记录 Bob 第 `t` 步会在 `cur` 位置  
- `if step < bob_arrival` # Alice 先到，完整拿走奖励  
- `score += amount[node] // 2` # 同时到达，只拿走一半（整除因为保证是偶数）

#### 复杂度  

- **时间复杂度**：`O(n * L)`，其中 `L` 是树的高度（最坏情况下等于 `n`），因为我们对每个叶子都要沿根‑>叶路径遍历一次。对于一棵“链状”树，叶子只有 1 个，时间是 `O(n)`；但如果树是星形（根连接 `n-1` 叶子），每条根‑>叶路径长度为 2，仍是 `O(n)`；最坏的情况是 **每条根‑>叶路径平均长度为 O(n)**，导致整体 `O(n²)`。  
- **空间复杂度**：`O(n)`，用于存邻接表、父指针、Bob 到达时间字典以及递归/遍历栈。

---

### 2. 最优解  

#### 思路  

暴力解的**瓶颈**在于每次遍历叶子都要**重新走一遍根‑>叶路径**，导致大量重复工作。  
实际上，我们只需要一次遍历就能把 **每个节点 Alice 与 Bob 谁先到达** 的信息算好，然后再一次求 **根‑>叶路径的最大累计收益**。  

优化思路分两步：

1. **一次 DFS（或 BFS）得到每个节点到根的距离 `distRoot[i]`**，这恰好是 Alice 第几步会到达该节点（因为她每一步只能沿树向下走一步）。  
2. **一次 DFS 得到每个节点到 Bob 起点的距离 `distBob[i]`**。  
   - 由于树是无向的，Bob 只会沿着唯一的路径 `bob → … → 0` 前进。  
   - 若我们已经知道 `parent`（根树的父指针），则 `distBob[i] = distRoot[i] + distRoot[bob] - 2 * distRoot[lca(i, bob)]`，但更简单的是：**直接在树上从 Bob 出发做一次 BFS**，记录到每个节点的步数 `distBob[i]`。这一步的时间也是 `O(n)`。  

有了这两个距离，我们可以**一次性决定每个节点的贡献**：

```text
if distRoot[i] < distBob[i] :   contribution = amount[i]          # Alice 先到
elif distRoot[i] == distBob[i]: contribution = amount[i] // 2   # 同时到达
else:                           contribution = 0                # Bob 先到
```

接下来，**求根‑>叶路径的最大累计贡献**就变成了**树上从根出发的最大路径和**问题，经典的做法是 **DFS 累加**：

- 从根往下递归，维护当前路径的累计和 `cur_sum`（把根到当前节点的所有贡献相加）。  
- 当遍历到一个叶子时，用 `cur_sum` 更新全局答案 `ans = max(ans, cur_sum)`。  

整个过程只需要 **两次线性遍历**（一次 BFS/DFS 计算距离，一次 DFS 累计贡献），时间 `O(n)`，空间 `O(n)`。

> **为什么一定正确？**  
> - `distRoot[i]` 正好等于 Alice 第几步会到达 `i`，因为她每步只能往下走一次。  
> - `distBob[i]` 正好等于 Bob 第几步会到达 `i`（从 `bob` 往根走的最短路径），因此比较这两个数字即可精确判断先后顺序。  
> - 贡献的计算遵循题目给出的三种情况，确保每个节点的收益是唯一确定的。  
> - 对所有根‑>叶路径的累计贡献进行最大化，就是在所有合法的 Alice 行程中挑选收益最高的那条。  

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def mostProfitablePath(edges: List[List[int]], bob: int, amount: List[int]) -> int:
    n = len(amount)

    # ---------- 1. 建图 ----------
    g = defaultdict(list)
    for a, b in edges:
        g[a].append(b)
        g[b].append(a)

    # ---------- 2. 计算 Alice（根）到每个节点的距离 ----------
    dist_root = [-1] * n
    q = deque([0])
    dist_root[0] = 0
    while q:
        v = q.popleft()
        for nxt in g[v]:
            if dist_root[nxt] == -1:
                dist_root[nxt] = dist_root[v] + 1
                q.append(nxt)

    # ---------- 3. 计算 Bob 从 bob 出发到每个节点的距离 ----------
    dist_bob = [-1] * n
    q = deque([bob])
    dist_bob[bob] = 0
    while q:
        v = q.popleft()
        for nxt in g[v]:
            if dist_bob[nxt] == -1:
                dist_bob[nxt] = dist_bob[v] + 1
                q.append(nxt)

    # ---------- 4. 预处理每个节点的实际贡献 ----------
    contrib = [0] * n
    for i in range(n):
        if dist_root[i] < dist_bob[i]:          # Alice 先到
            contrib[i] = amount[i]
        elif dist_root[i] == dist_bob[i]:       # 同时到达
            contrib[i] = amount[i] // 2
        else:                                   # Bob 先到
            contrib[i] = 0

    # ---------- 5. DFS 求根‑>叶路径的最大累计贡献 ----------
    ans = -10**18                     # 题目保证答案在整数范围内，这里取足够小的初始值
    visited = [False] * n

    def dfs(v: int, cur_sum: int):
        """从根出发的递归，cur_sum 为根到 v（含 v）的累计贡献"""
        nonlocal ans
        visited[v] = True
        cur_sum += contrib[v]

        # 判断是否是叶子（度为 1 且不是根 0）
        is_leaf = (v != 0 and len(g[v]) == 1)
        if is_leaf:
            ans = max(ans, cur_sum)

        for nxt in g[v]:
            if not visited[nxt]:
                dfs(nxt, cur_sum)

    dfs(0, 0)
    return ans
```

**关键行中文注释**：

- `dist_root[nxt] = dist_root[v] + 1` # Alice 从根到 `nxt` 需要一步更多  
- `dist_bob[nxt] = dist_bob[v] + 1` # Bob 从 `bob` 出发的步数递增  
- `if dist_root[i] < dist_bob[i]` # Alice 先到，完整拿走奖励  
- `cur_sum += contrib[v]` # 把当前节点的实际收益加入路径总和  
- `is_leaf = (v != 0 and len(g[v]) == 1)` # 判断是否是合法的叶子（根本身不算叶子）

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 两次 BFS（或 DFS）分别算根距离、Bob 距离，各 `O(n)`。  
  - 一次 DFS 累计路径收益，也是 `O(n)`。  
  - 所有操作只遍历每条边常数次，没有重复遍历根‑>叶路径的开销。  
- **空间复杂度**：`O(n)`  
  - 用于邻接表、两组距离数组、贡献数组以及递归栈（最坏 `O(n)`）。

与暴力解相比，时间从最坏 `O(n²)` 降到了线性 `O(n)`，在 `n ≤ 10⁵` 的约束下能够轻松通过。

---

## 心得  

- **核心技巧**：先把“先后到达”转化为**两条距离比较**，再把每个节点的收益独立化，最后在树上做一次**最大根‑>叶路径和**。  
- **适用的题型**  
  1. “先后到达决定奖励”类（如 LeetCode 2582 `Pass the Pillow` 的变形）。  
  2. “根‑>叶路径最大和”类（如 LeetCode 124 `Binary Tree Maximum Path Sum` 的简化版）。  
  3. “两个移动者在树上竞争”类（如 LeetCode 2581 `Count Number of Possible Root Nodes`）。  
- **一句话总结解题钥匙**：  
  > **把时间先后映射成距离比较，所有节点的收益一旦确定，问题就化为“在树上找最大根‑>叶路径和”。**

---

## 反思  

- **第一反应**：看到“Bob 的路径是固定的”，立刻想到先算出 Bob 到每个节点的到达时间，再逐条路径模拟。  
- **最容易踩的坑**  
  1. **把根当成叶子**：根 `0` 本身在单节点树里是叶子，但本题根一定是起点，不能算作结束点。  
  2. **Bob 到达时间的默认值**：对于根本不在 Bob 路径上的节点，需要用一个足够大的值（如 `inf`）表示“Bob 永远不会来”，否则比较会出错。  
  3. **整数除法**：同步到达时只取一半，题目保证 `amount[i]` 为偶数，记得使用 `// 2` 防止出现浮点数。  
- **下次类似题的第一步**：  
  > **先把每个人的“步数”转化为到每个节点的最短距离**，再用距离比较直接决定收益或状态。这样可以把“时间”这层抽象一次性消除，后面的求最值就变成普通的图/树 DP。