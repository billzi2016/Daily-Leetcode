# #2097. 有效的配对排列 / Valid Arrangement of Pairs

> 难度：困难 · 标签：Depth-First Search、Graph、Eulerian Circuit · [LeetCode 链接](https://leetcode.com/problems/valid-arrangement-of-pairs/)

---

## 题目（英文原版）

**Description**

You are given a 0-indexed 2D integer array pairs where pairs[i] = [starti, endi]. An arrangement of pairs is valid if for every index i where 1 <= i < pairs.length, we have endi-1 == starti.
Return any valid arrangement of pairs.
Note: The inputs will be generated such that there exists a valid arrangement of pairs.

**Examples**

**Example 1:**

```
Input: pairs = [[5,1],[4,5],[11,9],[9,4]]
Output: [[11,9],[9,4],[4,5],[5,1]]
Explanation:
This is a valid arrangement since endi-1 always equals starti.
end0 = 9 == 9 = start1 
end1 = 4 == 4 = start2
end2 = 5 == 5 = start3
```

**Example 2:**

```
Input: pairs = [[1,3],[3,2],[2,1]]
Output: [[1,3],[3,2],[2,1]]
Explanation:
This is a valid arrangement since endi-1 always equals starti.
end0 = 3 == 3 = start1
end1 = 2 == 2 = start2
The arrangements [[2,1],[1,3],[3,2]] and [[3,2],[2,1],[1,3]] are also valid.
```

**Example 3:**

```
Input: pairs = [[1,2],[1,3],[2,1]]
Output: [[1,2],[2,1],[1,3]]
Explanation:
This is a valid arrangement since endi-1 always equals starti.
end0 = 2 == 2 = start1
end1 = 1 == 1 = start2
```

**Constraints**

- 1 <= pairs.length <= 105
- pairs[i].length == 2
- 0 <= starti, endi <= 109
- starti != endi
- No two pairs are exactly the same.
- There exists a valid arrangement of pairs.

---

## 题目（中文翻译）

**描述**  
给定一个下标从 0 开始的二维整数数组 `pairs`，其中 `pairs[i] = [start_i, end_i]`。如果对所有满足 `1 <= i < pairs.length` 的下标 `i`，都有 `end_{i-1} == start_i`，则该 **配对 (pair) 的排列 (arrangement)** 是有效的。  
返回任意一个有效的配对排列。  
> 注意：题目保证输入数据一定存在至少一种有效的配对排列。

**示例**

**示例 1**  
```
Input: pairs = [[5,1],[4,5],[11,9],[9,4]]
Output: [[11,9],[9,4],[4,5],[5,1]]
```
**解释**：  
这是一个有效的排列，因为每一次的 `end_{i-1}` 都等于 `start_i`。  
- `end0 = 9 == 9 = start1`  
- `end1 = 4 == 4 = start2`  
- `end2 = 5 == 5 = start3`

**示例 2**  
```
Input: pairs = [[1,3],[3,2],[2,1]]
Output: [[1,3],[3,2],[2,1]]
```
**解释**：  
这是一个有效的排列，因为每一次的 `end_{i-1}` 都等于 `start_i`。  
- `end0 = 3 == 3 = start1`  
- `end1 = 2 == 2 = start2`  

排列 `[[2,1],[1,3],[3,2]]` 与 `[[3,2],[2,1],[1,3]]` 也同样有效。

**示例 3**  
```
Input: pairs = [[1,2],[1,3],[2,1]]
Output: [[1,2],[2,1],[1,3]]
```
**解释**：  
这是一个有效的排列，因为每一次的 `end_{i-1}` 都等于 `start_i`。  
- `end0 = 2 == 2 = start1`  
- `end1 = 1 == 1 = start2`

**约束条件**  
- `1 <= pairs.length <= 10^5`  
- `pairs[i].length == 2`  
- `0 <= start_i, end_i <= 10^9`  
- `start_i != end_i`  
- 没有两条配对完全相同  
- 必然存在至少一种有效的配对排列

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有的 `pairs` 当成 **一张纸条**，把每张纸条都尝试放在排列的第一个位置，然后从第二张纸条开始，**遍历所有剩余的纸条**，找出满足 `前一张的结束数 == 当前纸条的起始数` 的那一张放进去。  
这个过程可以递归（深度优先搜索）完成：

1. 任选一对 `[a,b]` 作为起点。  
2. 在剩下的 `pairs` 中遍历，找到所有 `start == b` 的候选。  
3. 对每个候选继续向后搜索，直至所有纸条都被用完。  

> **类比**：想象你在玩拼图，每块拼图都有左、右两个数字，左边必须和前一块的右边数字相同。暴力法就是把所有拼图一次一次试着拼，哪怕要把已经拼好的全部拆下来重新尝试。

只要搜索成功，就得到一个合法排列。因为题目保证一定存在解，这种穷举必然可以找到答案（虽然可能非常慢）。

#### 代码（Python）

```python
from typing import List

def validArrangement_bruteforce(pairs: List[List[int]]) -> List[List[int]]:
    n = len(pairs)

    # 用 visited 标记哪些纸条已经被使用
    visited = [False] * n
    path = []                     # 当前正在构造的排列

    def dfs(last_end: int, depth: int) -> bool:
        """深度优先搜索
        - last_end: 前一条的结束数
        - depth: 已经放了多少条
        返回 True 表示找到完整排列
        """
        if depth == n:            # 所有纸条都用完了
            return True

        for i in range(n):
            if not visited[i] and pairs[i][0] == last_end:
                visited[i] = True
                path.append(pairs[i])
                # 继续往后找
                if dfs(pairs[i][1], depth + 1):
                    return True
                # 回溯
                visited[i] = False
                path.pop()
        return False

    # 任选一条作为起点尝试
    for start_idx in range(n):
        visited[start_idx] = True
        path.append(pairs[start_idx])
        if dfs(pairs[start_idx][1], 1):
            return path
        # 回溯，尝试下一个起点
        visited[start_idx] = False
        path.pop()

    # 题目保证一定有解，这行代码理论上不会被执行
    return []
```

#### 复杂度  

- **时间复杂度**：`O(n!)`（阶乘）  
  解释：每一步都要在剩余的纸条中尝试所有可能的下一条，最坏情况下会遍历所有排列的可能性。即使 `n=10` 已经是 `10! = 3,628,800`，`n=100` 的情况根本不可行。  
- **空间复杂度**：`O(n)`  
  解释：递归栈深度最多 `n`，以及 `visited`、`path` 两个长度为 `n` 的数组。

> 暴力法只能帮助我们**理解问题本质**，但在实际面试或大数据规模下不可接受。

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**瓶颈在于不停地在所有剩余纸条中搜索匹配的下一条**。如果我们把每个数字看成 **图的节点**，每条 `[start, end]` 看成 **有向边**，那么题目要求的合法排列正好是 **一次走遍所有边且每条边恰好走一次** 的路径——这就是 **欧拉路径（Eulerian Path）**，若起点与终点相同则是 **欧拉回路（Eulerian Circuit）**。

**欧拉路径的判定要点**（针对有向图）：

1. **连通性**：忽略方向后，所有出现过的节点必须在同一个连通块里。（题目已保证有解，这一步可以省略检查。）
2. **入度 / 出度**：  
   - 若所有节点的 `出度 == 入度`，则存在欧拉**回路**，起点任意。  
   - 若恰好有一个节点 `出度 = 入度 + 1`（称为 **起点**），另一个节点 `入度 = 出度 + 1`（称为 **终点**），其余节点 `入度 == 出度`，则存在欧拉**路径**，必须从起点开始。

因为 **题目保证一定有合法排列**，我们只需要根据上述规则找到起点（若不存在则随便选一个节点），然后使用 **Hierholzer 算法** 在 O(E) 时间内构造欧拉路径。

**Hierholzer 算法简述**（一步步解释）：

1. **从起点出发**，沿着未被使用的边一直走，直到走不动（即当前节点没有剩余出边）。把走过的节点记录在栈 `stack` 中。
2. 若此时还有未使用的边（说明还有分支），**在栈里找一个还有未走完出边的节点**，把它重新当作“新的起点”，继续走下去。把新走的路径插入到原来路径的相应位置。
3. 最终栈里弹出的顺序即为欧拉路径的逆序。把它反转后得到正确顺序。

在实现时，**邻接表**（字典 `adj[node]` 保存该节点所有出边的列表）配合 **列表的 pop()** 可以实现“取出未使用的边”操作，时间复杂度为 O(1)。

**关键点**：

- 为了在最终答案里保留每条原始的 `[start, end]`，我们在邻接表里保存 **完整的边对象**（即原始的列表），而不是仅保存终点。
- 由于题目要求返回 **任意合法排列**，我们不必对边进行排序，只要保证每次取出一条未使用的边即可。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def validArrangement(pairs: List[List[int]]) -> List[List[int]]:
    """
    使用 Hierholzer 算法求有向图的欧拉路径（或欧拉回路）。
    返回的顺序即为满足题目要求的合法排列。
    """
    # 1️⃣ 建图 + 统计入度、出度
    adj = defaultdict(list)   # node -> list of edges (每条边仍是 [u, v])
    indeg = defaultdict(int)
    outdeg = defaultdict(int)

    for u, v in pairs:
        adj[u].append([u, v])   # 把完整的边保存下来
        outdeg[u] += 1
        indeg[v] += 1

    # 2️⃣ 找起点
    start = pairs[0][0]          # 默认取第一条的起点
    for node in set(indeg) | set(outdeg):
        if outdeg[node] - indeg[node] == 1:   # 出度比入度多 1 → 必须是起点
            start = node
            break
        # 若没有出度比入度多 1 的节点，说明是欧拉回路，任意节点均可

    # 3️⃣ Hierholzer 主循环
    stack = [start]          # 用来模拟递归的栈
    path = []                # 最终的欧拉路径（逆序存放）

    while stack:
        v = stack[-1]        # 当前栈顶节点
        if adj[v]:           # 还有未走的出边
            # 取出一条未使用的边（pop 让时间复杂度保持 O(1)）
            edge = adj[v].pop()
            # 把这条边的终点压入栈，继续向前走
            stack.append(edge[1])
        else:
            # 当前节点已经没有出边，弹出并加入路径
            stack.pop()
            if stack:        # 当弹出的是起点时，stack 已空，不再需要记录
                # 记录从 stack[-1] 到 v 的那条边
                # 因为我们已经弹掉 v，stack[-1] 正是这条边的起点
                path.append([stack[-1], v])

    # 4️⃣ path 此时是逆序，需要翻转
    return path[::-1]
```

> **代码要点注释**  
> - `adj[u].append([u, v])`：把完整的边对象存进邻接表，后面弹出时直接得到 `[u, v]`。  
> - `while stack:` 循环模拟递归，`stack[-1]` 为当前所在的节点。  
> - 当节点 `v` 没有剩余出边时，说明这段“死路”已经走完，弹出 `v` 并把 **从前一个节点到 `v` 的边** 加入 `path`。  
> - 最终 `path` 记录的顺序是从后往前的，需要 `[::-1]` 反转。

#### 复杂度  

- **时间复杂度**：`O(E)`，其中 `E = len(pairs)`。  
  解释：每条边只会被访问一次（加入邻接表一次、弹出一次），所有操作（`pop`、`append`、字典查询）均为常数时间。  
- **空间复杂度**：`O(V + E)`，`V` 为出现过的不同数字的数量。  
  - 邻接表保存每条边占 `O(E)`。  
  - 入度、出度字典以及栈、路径各占 `O(V)`（最坏情况下 `V ≤ 2E`），整体仍是线性空间。

> 与暴力 `O(n!)` 的时间相比，线性时间是本题的 **根本突破**，完全可以处理 `10^5` 条数据。

---

## 心得

- **核心技巧**：把「起点‑终点相连」的约束转化为 **有向图的欧拉路径**，使用 **Hierholzer 算法** 在线性时间内完成遍历。  
- **适用的题型**  
  1. **重新排列有向边** 使得相邻边相连（本题）。  
  2. **拼图 / 纸条** 类问题：如 LeetCode 1175 “Prime Arrangements” 的变体。  
  3. **旅行路线** 类：LeetCode 332 “Reconstruct Itinerary”（欧拉回路的变形）。  
- **一句话总结**：**把每对数字当成有向边，寻找欧拉路径，即可得到合法排列。**

---

## 反思

- **第一反应**：看到“end[i‑1] == start[i]”，立刻想到把所有对按顺序排成链条，于是想到了暴力 DFS。  
- **最容易踩的坑**  
  - **起点的选取**：若没有 “出度 = 入度 + 1” 的节点，需要把任意出现过的节点当作起点（欧拉回路）。  
  - **边的使用记录**：如果仅保存终点而丢失原始 `[u, v]`，最终返回的结果会缺失原始顺序。  
  - **递归深度**：直接递归实现 Hierholzer 可能导致栈溢出（`10^5` 条边），所以采用显式栈的迭代写法更安全。  
- **下次遇到同类题**：第一步先判断是否可以抽象为 **图的欧拉遍历**（检查入度/出度），再决定使用 **Hierholzer** 或 **DFS** 来构造路径。这样能迅速从指数暴力跳到线性解。