# #834. 树中节点距离之和 / Sum of Distances in Tree

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/sum-of-distances-in-tree/)

---

## 题目（英文原版）

**Description**

There is an undirected connected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.
You are given the integer n and the array edges where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
Return an array answer of length n where answer[i] is the sum of the distances between the ith node in the tree and all other nodes.

**Examples**

**Example 1:**

```
Input: n = 6, edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]
Output: [8,12,6,10,10,10]
Explanation: The tree is shown above.
We can see that dist(0,1) + dist(0,2) + dist(0,3) + dist(0,4) + dist(0,5)
equals 1 + 1 + 2 + 2 + 2 = 8.
Hence, answer[0] = 8, and so on.
```

**Example 2:**

```
Input: n = 1, edges = []
Output: [0]
```

**Example 3:**

```
Input: n = 2, edges = [[1,0]]
Output: [1,1]
```

**Constraints**

- 1 <= n <= 3 * 104
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- The given input represents a valid tree.

---

## 题目（中文翻译）

存在一棵无向连通的树，包含 `n` 个节点，节点编号为 `0` 到 `n - 1`，以及 `n - 1` 条边。  
给定整数 `n` 和数组 `edges`，其中 `edges[i] = [ai, bi]` 表示节点 `ai` 与节点 `bi` 之间有一条边。  
返回长度为 `n` 的数组 `answer`，其中 `answer[i]` 为树中第 `i` 个节点到所有其他节点的距离之和（sum of distances）。

## 示例

### 示例 1
**输入:** `n = 6, edges = [[0,1],[0,2],[2,3],[2,4],[2,5]]`  
**输出:** `[8,12,6,10,10,10]`  
**解释:** 如上图所示的树。  
我们可以看到  
`dist(0,1) + dist(0,2) + dist(0,3) + dist(0,4) + dist(0,5)`  
等于 `1 + 1 + 2 + 2 + 2 = 8`。  
因此 `answer[0] = 8`，其余以此类推。

### 示例 2
**输入:** `n = 1, edges = []`  
**输出:** `[0]`

### 示例 3
**输入:** `n = 2, edges = [[1,0]]`  
**输出:** `[1,1]`

## 约束条件
- `1 <= n <= 3 * 10^4`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= ai, bi < n`
- `ai != bi`
- 给定的输入保证是一棵合法的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**把每个节点当作起点，跑一次 BFS/DFS，求它到所有其它节点的距离之和**。  

- **数据结构**：我们用 **邻接表** 来保存树的结构。邻接表类似于“通讯录”，每个节点的“联系人”就是它相邻的节点。  
- **为什么正确**：树是一种连通且无环的图，从任意节点出发进行 BFS（层序遍历），第几层访问到的节点距离就是层数，这正是我们要的最短距离。把所有层数相加就得到该节点的答案。对每个节点都这么做，最终得到完整的答案数组。  
- **时间/空间复杂度**：  
  - 对每个节点我们都要遍历整棵树一次，树有 `n` 个节点，所以总共要做 `n` 次遍历，时间复杂度是 **O(n²)**。  
    - “O(n²)” 可以想象成在一张 `n × n` 的表格里填数，每行对应一次遍历，每列对应一次访问，总共 `n·n` 次操作。  
  - 除了保存答案数组外，我们只需要 `O(n)` 的邻接表和一次 BFS 用的队列，空间复杂度是 **O(n)**。

#### 代码（Python）

```python
from collections import deque
from typing import List

def sumOfDistancesInTree_bruteforce(n: int, edges: List[List[int]]) -> List[int]:
    # 建立邻接表：node -> [neighbor, ...]
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    answer = [0] * n                     # 最终答案

    # 对每个节点都做一次 BFS
    for start in range(n):
        dist = [-1] * n                   # -1 表示未访问
        q = deque([start])
        dist[start] = 0

        while q:
            node = q.popleft()
            for nxt in graph[node]:
                if dist[nxt] == -1:       # 只访问一次，防止回到父节点
                    dist[nxt] = dist[node] + 1
                    q.append(nxt)

        # 把所有距离加起来（除去自身距离 0）
        answer[start] = sum(dist)

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 每个节点都要遍历 `n` 条边（树的边数是 `n‑1`），所以总共大约是 `n·n` 次操作。  
- **空间复杂度**：`O(n)`  
  - 邻接表 + BFS 队列 + 距离数组，都和节点数线性相关。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **重复遍历相同的子树**。  
从一个节点出发算完距离后，再换到相邻的节点时，很多路径其实已经算过，只是“根”换了位置。  
我们可以 **利用树的层次结构，做两遍 DFS**（一次后序一次前序）把这些重复工作省掉，这就是 **树形 DP + 换根（re‑root）** 的技巧。

1. **第一次 DFS（后序）**  
   - 统计每个节点子树的大小 `subSize[node]`（包括自己），相当于 “这个节点下面有多少人”。  
   - 计算 `dp[node]`：从 `node` 出发，到它子树里所有节点的距离之和。  
   - 递归返回时，父节点可以把子节点的 `subSize` 加到自己的 `subSize`，把 `dp[child] + subSize[child]` 加到自己的 `dp`（因为子树里每个节点到父节点的距离都比到子节点多 1）。

2. **第二次 DFS（前序）**  
   - 已经知道根节点 `0` 的答案 `answer[0] = dp[0]`（因为它的子树就是整棵树）。  
   - 当我们把根从 `parent` 移到 `child` 时，**距离会发生两类变化**：  
     - `child` 子树里的 `subSize[child]` 个节点，距离 **减 1**（因为根更近了）。  
     - 其余 `n - subSize[child]` 个节点，距离 **加 1**（因为根更远了）。  
   - 因此有公式  
     ```
     answer[child] = answer[parent] - subSize[child] + (n - subSize[child])
                  = answer[parent] - subSize[child] + n - subSize[child]
                  = answer[parent] + n - 2 * subSize[child]
     ```
   - 递归遍历整棵树，按上面的公式把答案从父节点“搬运”到子节点。

> **类比**：把树想象成一座城市的公交网络，`subSize` 就是某个站点覆盖的乘客数。换根相当于把总部搬到相邻站点，覆盖的乘客距离会整体向“远离”或“靠近”倾斜，这个倾斜幅度正好由子树大小决定。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def sumOfDistancesInTree(n: int, edges: List[List[int]]) -> List[int]:
    # 1️⃣ 建立邻接表
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    subSize = [1] * n          # 子树节点数，初始化为 1（自己）
    dp = [0] * n               # 子树内部距离和

    # 2️⃣ 第一次 DFS：后序遍历，计算 subSize 与 dp
    def post_order(node: int, parent: int) -> None:
        for nxt in graph[node]:
            if nxt == parent:          # 防止回到父节点形成循环
                continue
            post_order(nxt, node)      # 先处理子树
            subSize[node] += subSize[nxt]                # 子树大小累计
            dp[node] += dp[nxt] + subSize[nxt]            # 距离累计 +1（每个子树节点到 node 多一条边）

    post_order(0, -1)   # 任意选 0 为根

    answer = [0] * n
    answer[0] = dp[0]   # 根节点的答案已经算好

    # 3️⃣ 第二次 DFS：前序遍历，利用换根公式传播答案
    def pre_order(node: int, parent: int) -> None:
        for nxt in graph[node]:
            if nxt == parent:
                continue
            # 根据公式：answer[child] = answer[parent] + n - 2 * subSize[child]
            answer[nxt] = answer[node] + n - 2 * subSize[nxt]
            pre_order(nxt, node)

    pre_order(0, -1)

    return answer
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 两次遍历整棵树，每条边只会被访问常数次（一次在后序，一次在前序），所以总操作和节点数线性相关。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(n)`  
  - 邻接表、`subSize`、`dp`、`answer` 都是长度为 `n` 的数组，递归栈最坏深度是树的高度 ≤ `n`，整体仍是线性空间。

---

## 心得

- **核心技巧**：**树形 DP + 换根（re‑root）**。先在一棵树上算出子树信息（大小、内部距离），再利用这些信息把答案从一个根“搬到”相邻的根，整个过程只需线性时间。  
- **适用的题型**  
  1. **“求每个节点的子树节点数”**（如 LeetCode 2246）  
  2. **“求每个节点的子树中最大/最小值”**（如 LeetCode 814）  
  3. **“树上每条边的贡献”**（如 LeetCode 1466）  
- **一句话总结**：**把全局问题拆成“子树内部 + 子树之外”，用一次遍历把子树内部搞定，再用换根把子树之外的贡献搬运过去**。

---

## 反思

- **拿到题目第一反应**：直接想到对每个节点做一次 BFS/DFS，算所有距离——这就是暴力解。  
- **最容易踩的坑**  
  - **递归栈溢出**：`n` 可达 3·10⁴，深度递归可能超出 Python 默认递归深度，需要 `sys.setrecursionlimit(10**6)` 或改写为显式栈。  
  - **子树大小的初始化**：忘记把每个节点本身算进去，导致 `subSize` 结果少 1，进而导致答案偏差。  
  - **换根公式的符号**：`+ n - 2 * subSize[child]` 很容易写成 `- n + 2 * subSize[child]`，导致答案全是负数。  
- **下次遇到同类题**：**先问自己**——“是否可以把答案拆成‘根节点内部的贡献’ + ‘根节点外部的贡献’”，如果能，就考虑一次后序 DP + 前序换根的套路。这样就能立刻从暴力 O(n²) 跳到线性 O(n)。