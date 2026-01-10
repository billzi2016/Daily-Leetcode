# #3486. **最长特殊路径 II** / Longest Special Path II

> 难度：困难 · 标签：Array、Hash Table、Tree、Depth-First Search、Prefix Sum · [LeetCode 链接](https://leetcode.com/problems/longest-special-path-ii/)

---

## 题目（英文原版）

**Description**

You are given an undirected tree rooted at node 0, with n nodes numbered from 0 to n - 1. This is represented by a 2D array edges of length n - 1, where edges[i] = [ui, vi, lengthi] indicates an edge between nodes ui and vi with length lengthi. You are also given an integer array nums, where nums[i] represents the value at node i.
A special path is defined as a downward path from an ancestor node to a descendant node in which all node values are distinct, except for at most one value that may appear twice.
Return an array result of size 2, where result[0] is the length of the longest special path, and result[1] is the minimum number of nodes in all possible longest special paths.

**Examples**

**Example 1:**

```
Input: edges = [[0,1,1],[1,2,3],[1,3,1],[2,4,6],[4,7,2],[3,5,2],[3,6,5],[6,8,3]], nums = [1,1,0,3,1,2,1,1,0]
Output: [9,3]
Explanation:
In the image below, nodes are colored by their corresponding values in nums .

The longest special paths are 1 -> 2 -> 4 and 1 -> 3 -> 6 -> 8 , both having a length of 9. The minimum number of nodes across all longest special paths is 3.
```

**Example 2:**

```
Input: edges = [[1,0,3],[0,2,4],[0,3,5]], nums = [1,1,0,2]
Output: [5,2]
Explanation:

The longest path is 0 -> 3 consisting of 2 nodes with a length of 5.
```

**Constraints**

- 2 <= n <= 5 * 104
- edges.length == n - 1
- edges[i].length == 3
- 0 <= ui, vi < n
- 1 <= lengthi <= 103
- nums.length == n
- 0 <= nums[i] <= 5 * 104
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

给定一棵以节点 0 为根的无向树，树中共有 n 个节点，编号为 0 到 n‑1。树通过长度为 n‑1 的二维数组 `edges` 描述，其中 `edges[i] = [ui, vi, lengthi]` 表示节点 `ui` 和节点 `vi` 之间存在一条长度为 `lengthi` 的边（edge）。同时给定整数数组 `nums`，其中 `nums[i]` 表示节点 i 的取值（value）。

**特殊路径（special path）** 定义为从某个祖先节点（ancestor）向下到其后代节点（descendant）的路径，要求路径上所有节点的取值两两不同，**但至多可以出现一次重复的取值**（即最多有一个值出现两次，其余均唯一）。

返回长度为 2 的数组 `result`：

- `result[0]` 为最长特殊路径的总长度（所有边长度之和）。
- `result[1]` 为所有可能的最长特殊路径中，节点数最少的那个路径的节点数量。

---

### 示例

#### 示例 1
**输入**  
```json
edges = [[0,1,1],[1,2,3],[1,3,1],[2,4,6],[4,7,2],[3,5,2],[3,6,5],[6,8,3]],
nums = [1,1,0,3,1,2,1,1,0]
```
**输出**  
```
[9,3]
```
**解释**  
下图中，节点的颜色对应 `nums` 中的取值。

最长的特殊路径有两条：`1 → 2 → 4` 和 `1 → 3 → 6 → 8`，它们的长度均为 9。所有最长路径中节点最少的路径包含 3 个节点。

#### 示例 2
**输入**  
```json
edges = [[1,0,3],[0,2,4],[0,3,5]],
nums = [1,1,0,2]
```
**输出**  
```
[5,2]
```
**解释**  
最长路径为 `0 → 3`，该路径包含 2 个节点，总长度为 5。

---

### 约束

- `2 <= n <= 5 * 10^4`
- `edges.length == n - 1`
- `edges[i].length == 3`
- `0 <= ui, vi < n`
- `1 <= lengthi <= 10^3`
- `nums.length == n`
- `0 <= nums[i] <= 5 * 10^4`
- 输入保证 `edges` 构成一棵合法的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把树看成一张**地图**，我们想找一条「从上往下」的最长路。  
最直接的办法就是：

1. **枚举所有可能的起点**（每个节点都可以当祖先），  
2. **从该起点向下遍历**，把所有可以到达的后代逐一列出来。  
3. 对每条从祖先到后代的路径，检查路径上的节点值是否满足「最多只有一种数出现两次」的条件。  
4. 满足条件的路径就计算它的**总边长**和**节点数**，更新答案。

> **数据结构类比**  
> - 树的邻接表就像「城市之间的道路表」；  
> - 用一个 `set` / `dict` 记录已经出现过的数，就像「字典」里查单词是否出现过；  
> - 用 `list` 把路径上所有节点的值保存下来，类似「背单词本」随时回头检查。

只要把每条可能的「祖先 → 后代」路径都检查一遍，就一定能得到正确答案——因为我们把所有情况都穷举了。

#### 代码（Python）

```python
from collections import defaultdict, deque
import sys
sys.setrecursionlimit(10**6)

def longestSpecialPath_bruteforce(edges, nums):
    n = len(nums)
    # 建图（无向树）
    g = defaultdict(list)
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    # 记录从根到每个节点的父亲、深度、到根的距离（方便向上回溯）
    parent = [-1] * n
    depth   = [0] * n
    dist    = [0] * n          # 到根的边长前缀和
    order = []

    # 用 BFS/DFS 把树根在 0，得到父子关系
    stack = [(0, -1, 0, 0)]    # (node, parent, depth, dist)
    while stack:
        u, p, d, dis = stack.pop()
        parent[u] = p
        depth[u]   = d
        dist[u]    = dis
        order.append(u)
        for v, w in g[u]:
            if v == p: continue
            stack.append((v, u, d+1, dis + w))

    # 暴力枚举所有 (ancestor, descendant) 对
    best_len = -1
    best_nodes = 10**9

    # 把每个节点往上走到根，得到完整的祖先链
    for anc in range(n):
        # 记录路径上出现的次数
        cnt = defaultdict(int)
        dup_cnt = 0          # 已经出现了几种数出现了两次
        # 从 anc 向下遍历所有后代（使用 BFS）
        q = deque([anc])
        while q:
            cur = q.popleft()
            # 把 cur 加入路径检查
            val = nums[cur]
            cnt[val] += 1
            if cnt[val] == 2:
                dup_cnt += 1
            if cnt[val] > 2 or dup_cnt > 1:
                # 这条路径已经不合法，后面的子树也不可能合法（因为路径只能往下）
                # 直接剪枝
                cnt[val] -= 1
                if cnt[val] == 1: dup_cnt -= 1
                continue

            # 合法路径：anc -> cur
            cur_len = dist[cur] - dist[anc]          # 边长和
            cur_nodes = depth[cur] - depth[anc] + 1  # 节点数
            if cur_len > best_len or (cur_len == best_len and cur_nodes < best_nodes):
                best_len, best_nodes = cur_len, cur_nodes

            # 继续向下
            for nxt, w in g[cur]:
                if nxt == parent[cur] or nxt == anc:   # 只往子树方向走
                    continue
                q.append(nxt)

            # 退出子树前把 cur 的计数恢复（因为后面的其它后代仍会使用相同的 anc）
            cnt[val] -= 1
            if cnt[val] == 1: dup_cnt -= 1

    return [best_len, best_nodes]
```

> 代码说明  
> - `cnt` 用来统计当前「祖先 → 当前节点」路径上每个数出现了几次；  
> - `dup_cnt` 记录已经出现了几种数出现了两次（如果 >1 就不合法）；  
> - 当发现路径不合法时直接 `continue`，相当于在「树枝」上剪掉整条子树，避免继续遍历。

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 最坏情况下我们会检查每对祖先‑后代，树上有 `n` 个节点，约有 `n·(n-1)/2` 条路径。  
  - “`O(n²)`” 的意思是 **数量级上是 n 的平方**，比如 n=5·10⁴ 时会有约 2.5·10⁹ 条路径，显然会超时。

- **空间复杂度**：`O(n)`  
  - 主要是存图、父指针以及 BFS/DFS 栈等，和节点数线性相关。

> 暴力解虽然能帮助我们**弄清楚题意**，但在实际面试或比赛里根本跑不完，需要进一步优化。

---

### 2. 最优解

#### 思路  

我们仍然沿着「根 → 子」的方向遍历，但这次不再枚举所有起点，而是**动态维护**当前根到**当前节点**这条路径上，**最长的合法子段**（即满足「最多一种数出现两次」的后缀）。

把根到当前节点的路径想象成一条**数组** `path[0 … i]`（`i` 为当前节点在路径中的下标）。  
我们要找的是 **在这个数组中，以 `i` 为右端点，左端点尽可能靠左**，同时满足：

1. 任意数出现不超过两次。  
2. 至多有一种数出现两次。

这正好像在「滑动窗口」里找最长合法子数组，只是这里的「数组」是树的**单一路径**，而不是普通的线性数组。  
因为我们在 **深度优先遍历**（DFS）时，路径只能向下增长，回到父节点时会自动「弹出」最右端的元素，所以 **滑动窗口** 可以天然地在递归栈上实现。

关键在于**如何快速更新左端点 `left`**：

- **出现第 3 次**  
  当某个数在路径中出现了第 3 次（`cnt[value] == 3`），显然这条路径已经不合法。我们必须把左端点移动到**第 1 次出现的下一个位置**，即 `left = max(left, first_occurrence + 1)`。此时该数在窗口里只剩下后两次出现，仍然可以作为「唯一的重复数」。

- **出现第 2 次且已经有另一种数出现了第 2 次**  
  假设已有重复数 `dup_val`（出现两次），现在另一个数 `v` 也出现第二次。此时窗口里出现了 **两种重复数**，仍然不合法。我们只能把左端点移动到**两种数中第一次出现较早的那个**的下一个位置，公式为  
  `left = max(left, min(first_dup, first_v) + 1)`。  
  移动后，窗口里只能保留「出现较晚」的那种数作为合法的唯一重复数。于是我们把 `dup_val` 更新为出现较晚的那一个。

以上两条规则只涉及 **当前节点** 与 **已经记录的状态**，每次更新都是 **O(1)** 的操作。

为了快速得到「第一次出现的位置」：

- 用 **哈希表 `pos[value]`** 保存该数在当前路径中出现的所有下标（最多 3 个）。  
- `pos[value][0]` → 最早出现的下标；`pos[value][1]` → 第二次出现的下标（如果有）。

同时我们需要**快速算出两点之间的边长和**。这可以用 **前缀和** 完成：

- `pre_len[i]` = 从根到路径中第 `i` 个节点的总边长。  
- 任意子段 `[l … r]` 的长度 = `pre_len[r] - pre_len[l]`（因为 `pre_len[l]` 包含了从根到 `l` 的边长，正好被抵消）。

#### 整体算法

1. **建图**（邻接表），记录每条边的长度。  
2. **深度优先遍历**（递归或显式栈）从根 `0` 开始。遍历时维护以下全局状态（随递归进出自动回溯）：

   - `path` : 当前根到节点的节点下标列表（相当于数组下标）。
   - `pre_len` : 与 `path` 同步的前缀边长数组。
   - `pos` : `defaultdict(list)`，每个数对应出现的下标列表（最多 3 个）。
   - `left` : 当前合法窗口的左端点（下标），初始 `0`。
   - `dup_val`、`dup_first`：当前唯一出现两次的数及其第一次出现的下标（如果没有则为 `None`）。

3. **进入一个节点** `u`（下标 `i = len(path)`）：

   - 把 `u` 加入 `path`，把对应的前缀长度加入 `pre_len`。  
   - 更新 `pos[nums[u]]`（在列表尾部 `append(i)`）。  
   - 根据 `len(pos[nums[u]])` 的新值，按前面「第 3 次」或「第 2 次且已有重复」的规则 **更新 `left`、`dup_val`、`dup_first`**。  
   - 计算当前窗口 `[left … i]` 的长度 `cur_len = pre_len[i] - pre_len[left]`，节点数 `cur_nodes = i - left + 1`。  
   - 若 `cur_len` 更大，或相等且 `cur_nodes` 更少，则更新全局答案 `best_len`、`best_nodes`。

4. **递归遍历子节点**（跳过父节点），把上述状态传进去。  
5. **回溯**：离开节点时，需要恢复所有被修改的状态：

   - `pos[nums[u]].pop()`，若列表为空则删掉键。  
   - `path.pop()`、`pre_len.pop()`。  
   - `left`、`dup_val`、`dup_first` 恢复为进入该节点前的值（在递归调用前先把旧值保存到局部变量里）。

6. 最终 `best_len`、`best_nodes` 即为答案。

> **为什么是最优的？**  
> - 每个节点只进入一次、退出一次，所有操作都是 **O(1)**，所以总时间 **O(n)**。  
> - 额外的哈希表、路径栈、前缀和等只需要 **O(n)** 的空间。  
> - 与暴力的 `O(n²)` 相比，指数级的提升让 5·10⁴ 规模的数据轻松通过。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)

def longestSpecialPath(edges, nums):
    n = len(nums)
    # 1️⃣ 建图
    g = [[] for _ in range(n)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))

    # 全局答案
    best_len = -1          # 最长路径的边长和
    best_nodes = 10**9     # 对应的最少节点数

    # 维护的状态（随递归进出自动回溯）
    path = []              # 当前根到节点的下标列表，等价于数组下标
    pre_len = [0]          # 前缀边长，pre_len[i] 为根到 path[i] 的总长度
    pos = defaultdict(list)   # value -> 出现下标列表（最多 3 个）

    left = 0               # 当前合法窗口左端点（在 path 中的下标）
    dup_val = None         # 当前唯一出现两次的数
    dup_first = -1         # 该数第一次出现的下标（在 path 中）

    def dfs(u, parent):
        nonlocal best_len, best_nodes, left, dup_val, dup_first

        # ---------- 进入节点 ----------
        idx = len(path)                 # 当前节点在路径中的下标
        path.append(u)

        # 更新前缀长度（根到当前节点的边长和）
        cur_len = pre_len[-1] + (0 if parent == -1 else edge_len)  # edge_len 在后面赋值
        pre_len.append(cur_len)

        # 记录当前值出现的位置
        val = nums[u]
        pos[val].append(idx)

        # 保存旧状态，方便回溯
        old_left = left
        old_dup_val = dup_val
        old_dup_first = dup_first

        # ---------- 根据出现次数更新窗口 ----------
        occ = pos[val]
        if len(occ) == 2:                     # 第 2 次出现
            if dup_val is None:               # 还没有重复数，直接设为当前
                dup_val = val
                dup_first = occ[0]
            else:
                # 已经有一种重复数，再出现第二种 => 不合法
                new_first = occ[0]            # 这一次的第一次出现
                # 左端点必须超过较早的那一次
                left = max(left, min(dup_first, new_first) + 1)
                # 保留出现较晚的那种数作为唯一的重复数
                if dup_first < new_first:
                    dup_val, dup_first = val, new_first
                # 否则保持原来的 dup_val/dup_first 不变
        elif len(occ) == 3:                   # 第 3 次出现，必须把最早的剔除
            left = max(left, occ[0] + 1)      # 窗口左端点越过第一次出现
            # 现在该数仍然出现两次（occ[1]、occ[2]），它成为唯一的重复数
            dup_val = val
            dup_first = occ[1]

        # ---------- 更新全局答案 ----------
        # 当前合法窗口是 [left … idx]（左闭右闭）
        cur_path_len = pre_len[idx + 1] - pre_len[left]   # 边长和
        cur_nodes = idx - left + 1                       # 节点数
        if cur_path_len > best_len or (cur_path_len == best_len and cur_nodes < best_nodes):
            best_len, best_nodes = cur_path_len, cur_nodes

        # ---------- 递归子树 ----------
        for v, w in g[u]:
            if v == parent:
                continue
            # 把即将使用的 edge_len 暂存到全局变量，供子层的 pre_len 计算
            global edge_len
            edge_len = w
            dfs(v, u)

        # ---------- 回溯 ----------
        # 恢复 left、dup_val、dup_first 为进入该节点前的状态
        left, dup_val, dup_first = old_left, old_dup_val, old_dup_first
        # 删除当前节点的记录
        pos[val].pop()
        if not pos[val]:
            del pos[val]
        path.pop()
        pre_len.pop()

    # 从根开始，根没有入边，所以 edge_len 暂设 0
    edge_len = 0
    dfs(0, -1)

    return [best_len, best_nodes]
```

> **代码要点说明**  

| 行号 | 关键操作 | 中文解释 |
|------|----------|----------|
| 9‑12 | 建立邻接表 | 把树的每条边存成「城市 ↔ 城市」的列表 |
| 23‑27 | `pre_len` 前缀和 | 类似「跑步累计里程」；`pre_len[i]` = 从根到第 `i` 个节点的总路程 |
| 31‑33 | `pos` 哈希表 | 像「字典」记录每个数最近出现的下标，最多 3 条 |
| 41‑45 | 进入节点时把自己加入路径 | 相当于把「当前站点」压入「行程表」 |
| 48‑55 | 处理第一次出现、第二次出现、第三次出现的情况 | 根据「最多一种数出现两次」的规则，动态调节左端点 `left` |
| 61‑65 | 计算当前窗口的长度和节点数并更新答案 | 用前缀和快速算出「这段路有多长」 |
| 70‑73 | 递归遍历子节点 | 只往「下层」走，避免回到父节点 |
| 78‑87 | 回溯：恢复所有状态 | 递归结束后像「撤销」刚才的修改，保证兄弟节点的计算不受影响 |

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个节点只进入一次、退出一次，所有哈希表操作、指针更新都是常数时间。  
  - 「`O(n)`」的含义是 **算法执行的基本操作次数与节点数成正比**，比如 `n = 5·10⁴` 时大约只需要几万次操作，极其快。

- **空间复杂度**：`O(n)`  
  - 需要保存树的邻接表、递归栈（最坏深度 `n`），以及 `pos`、`path`、`pre_len` 等额外结构，整体随节点数线性增长。

> 与暴力解相比，时间从 **平方级** 降到 **线性级**，是这道题的关键突破。

---

## 心得

- **核心技巧**：在 **树的根到当前节点路径** 上使用 **滑动窗口**（左指针 `left`）来维持「最多一种数出现两次」的约束，并配合 **前缀和** 快速求路径长度。  
- **适用的题型**  
  1. 树上求满足「某种子数组/子路径约束」的最长路径（如「最多出现 K 次」）。  
  2. 「路径上元素唯一性」或「最多出现一次重复」的变形（比如 LeetCode 2741、2761）。  
  3. 需要在**单根路径**上做「滑动窗口」的场景（比如「树上最长递增子序列」的 O(n) 解法）。  
- **一句话总结**：**把树的根‑叶路径当成一条数组，用滑动窗口实时维护合法区间，就能在线性时间求出最长特殊路径。**

---

## 反思

- **拿到题目第一反应**：先想「枚举所有祖先‑后代对」检查合法性，结果想到要 O(n²) 的遍历，立刻感觉不行。  
- **最容易踩的坑**  
  1. **忘记「最多一种数出现两次」的细节**，只判断「没有出现三次」会得到错误答案。  
  2. **左指针更新不够精确**：出现第二个重复时必须取两种重复的**较早**出现位置，否则窗口仍会包含两个重复数。  
  3. **回溯时忘记恢复 `left`、`dup_val`、`dup_first`**，导致兄弟子树计算错误。  
  4. **前缀和的索引错误**（使用 `pre_len[i] - pre_len[left]` 而不是 `pre_len[i+1]`），会少算或多算一段边长。  
- **下次遇到类似题目**：  
  1️⃣ 先确认「路径」是否可以看成「单一路径数组」——如果是树的根到当前节点，那就可以尝试 **滑动窗口**。  
  2️⃣ 明确约束（如「最多 K 种数出现两次」），把约束转化为「左指针需要移动到哪儿」的规则。  
  3️⃣ 用 **哈希表记录出现位置**、**前缀和计算长度**，并在递归中 **保存/恢复状态**，防止跨分支污染。  

这样就能把「看似指数级」的搜索，压缩到 **线性时间** 完成。