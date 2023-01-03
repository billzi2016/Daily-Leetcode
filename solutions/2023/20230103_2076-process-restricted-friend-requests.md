# #2076. **处理受限的好友请求** / Process Restricted Friend Requests

> 难度：困难 · 标签：Union Find、Graph · [LeetCode 链接](https://leetcode.com/problems/process-restricted-friend-requests/)

---

## 题目（英文原版）

**Description**

You are given an integer n indicating the number of people in a network. Each person is labeled from 0 to n - 1.
You are also given a 0-indexed 2D integer array restrictions, where restrictions[i] = [xi, yi] means that person xi and person yi cannot become friends, either directly or indirectly through other people.
Initially, no one is friends with each other. You are given a list of friend requests as a 0-indexed 2D integer array requests, where requests[j] = [uj, vj] is a friend request between person uj and person vj.
A friend request is successful if uj and vj can be friends. Each friend request is processed in the given order (i.e., requests[j] occurs before requests[j + 1]), and upon a successful request, uj and vj become direct friends for all future friend requests.
Return a boolean array result, where each result[j] is true if the jth friend request is successful or false if it is not.
Note: If uj and vj are already direct friends, the request is still successful.

**Examples**

**Example 1:**

```
Input: n = 3, restrictions = [[0,1]], requests = [[0,2],[2,1]]
Output: [true,false]
Explanation:
Request 0: Person 0 and person 2 can be friends, so they become direct friends. 
Request 1: Person 2 and person 1 cannot be friends since person 0 and person 1 would be indirect friends (1--2--0).
```

**Example 2:**

```
Input: n = 3, restrictions = [[0,1]], requests = [[1,2],[0,2]]
Output: [true,false]
Explanation:
Request 0: Person 1 and person 2 can be friends, so they become direct friends.
Request 1: Person 0 and person 2 cannot be friends since person 0 and person 1 would be indirect friends (0--2--1).
```

**Example 3:**

```
Input: n = 5, restrictions = [[0,1],[1,2],[2,3]], requests = [[0,4],[1,2],[3,1],[3,4]]
Output: [true,false,true,false]
Explanation:
Request 0: Person 0 and person 4 can be friends, so they become direct friends.
Request 1: Person 1 and person 2 cannot be friends since they are directly restricted.
Request 2: Person 3 and person 1 can be friends, so they become direct friends.
Request 3: Person 3 and person 4 cannot be friends since person 0 and person 1 would be indirect friends (0--4--3--1).
```

**Constraints**

- 2 <= n <= 1000
- 0 <= restrictions.length <= 1000
- restrictions[i].length == 2
- 0 <= xi, yi <= n - 1
- xi != yi
- 1 <= requests.length <= 1000
- requests[j].length == 2
- 0 <= uj, vj <= n - 1
- uj != vj

---

## 题目（中文翻译）

你被给定一个整数 `n`，表示网络（network）中人的数量。每个人的编号为 `0` 到 `n - 1`。  
同时给定一个 **0 索引** 的二维整数数组 `restrictions（限制）`，其中 `restrictions[i] = [x_i, y_i]` 表示人 `x_i` 与人 `y_i` 不能成为好友，无论是直接还是通过其他人间接成为好友。  

最初，所有人之间都没有任何好友关系。又给定一个 **0 索引** 的二维整数数组 `requests（请求）`，其中 `requests[j] = [u_j, v_j]` 表示一次好友请求（friend request），请求让人 `u_j` 与人 `v_j` 成为好友。  

一次好友请求成功的条件是 `u_j` 与 `v_j` 能够成为好友（即不会违反任何限制）。请求按照给定顺序依次处理（即 `requests[j]` 在 `requests[j + 1]` 之前处理），若请求成功，则 `u_j` 与 `v_j` 成为 **直接好友（direct friends）**，并在后续的所有请求中保持该关系。  

返回一个 **布尔数组（boolean array）** `result`，其中 `result[j]` 为 `true` 表示第 `j` 个好友请求成功，为 `false` 表示失败。  
注意：如果 `u_j` 与 `v_j` 已经是直接好友，请求仍视为成功。

---

### 示例

**示例 1**

```text
Input: n = 3, restrictions = [[0,1]], requests = [[0,2],[2,1]]
Output: [true,false]
Explanation:
Request 0: 人 0 与人 2 可以成为好友，所以它们成为直接好友。 
Request 1: 人 2 与人 1 不能成为好友，因为这会导致人 0 与人 1 成为间接好友（1--2--0）。
```

**示例 2**

```text
Input: n = 3, restrictions = [[0,1]], requests = [[1,2],[0,2]]
Output: [true,false]
Explanation:
Request 0: 人 1 与人 2 可以成为好友，所以它们成为直接好友。
Request 1: 人 0 与人 2 不能成为好友，因为这会导致人 0 与人 1 成为间接好友（0--2--1）。
```

**示例 3**

```text
Input: n = 5, restrictions = [[0,1],[1,2],[2,3]], requests = [[0,4],[1,2],[3,1],[3,4]]
Output: [true,false,true,false]
Explanation:
Request 0: 人 0 与人 4 可以成为好友，所以它们成为直接好友。
Request 1: 人 1 与人 2 不能成为好友，因为它们之间存在直接限制。
Request 2: 人 3 与人 1 可以成为好友，所以它们成为直接好友。
Request 3: 人 3 与人 4 不能成为好友，因为...
```
（示例 3 的后续解释在题目中被截断）

---

### 约束条件

- `2 <= n <= 1000`
- `0 <= restrictions.length <= 1000`
- `restrictions[i].length == 2`
- `0 <= x_i, y_i <= n - 1`
- `x_i != y_i`
- `1 <= requests.length <= 1000`
- `requests[j].length == 2`
- `0 <= u_j, v_j <= n - 1`
- `u_j != v_j`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**每次收到一条好友请求**，我们先把这条请求加入「朋友网络」中，随后检查所有的 **限制** 是否被违反。  
- **朋友网络** 可以用 **邻接表**（list of sets）来保存，`friends[x]` 表示和 `x` 已经直接或间接相连的所有人。  
- 检查限制时，只要遍历 `restrictions`，看每一对 `[a, b]` 是否已经在同一个连通块（即 `a` 能通过朋友关系间接到达 `b`），如果是，就说明这条请求会导致违禁关系，需要撤销这次合并。

生活化类比：  
- 想象每个人是城市，朋友关系是修好的道路。  
- `restrictions` 就是「禁止两座城市之间出现任何道路（直接或间接）」。  
- 暴力做法就是每次建一条新路后，遍历所有禁令，看有没有两座禁忌城市已经被道路连通。

**为什么正确**  
- 我们在每次请求后都完整检查所有禁令，只有当所有禁令都仍然满足时才保留这条新路。于是最终得到的每一步结果必然合法。

**时间/空间复杂度**  
- 对每条请求，我们要遍历所有限制（最多 1000 条），并且每次检查连通性需要一次 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）**，最坏要遍历全部 `n`（≤1000）个人。  
- 因此时间复杂度约为 `O(requests * (restrictions * n))`，在最坏情况下是 `O(1000 * 1000 * 1000) = O(10^9)`，会超时。  
- 空间上我们保存邻接表，最多 `O(n + edges)`，这里 `edges ≤ requests`，所以 `O(n + requests)`。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def friendRequests_bruteforce(
    n: int, restrictions: List[List[int]], requests: List[List[int]]
) -> List[bool]:
    # 用邻接表存储已建立的朋友关系（无向图）
    graph = defaultdict(set)          # graph[x] = {直接相连的朋友}
    
    # 判断两个人是否已经在同一个连通块（即能间接成为朋友）
    def connected(a: int, b: int) -> bool:
        if a == b:
            return True
        visited = set()
        q = deque([a])
        while q:
            cur = q.popleft()
            if cur == b:
                return True
            for nb in graph[cur]:
                if nb not in visited:
                    visited.add(nb)
                    q.append(nb)
        return False
    
    res = []
    for u, v in requests:
        # 先假设可以加好友，暂时把两人连起来
        graph[u].add(v)
        graph[v].add(u)
        
        # 检查所有限制是否被破坏
        ok = True
        for x, y in restrictions:
            if connected(x, y):   # 如果限制中的两人已经间接相连，就违背了
                ok = False
                break
        
        if not ok:                # 违背限制，撤销这条边
            graph[u].remove(v)
            graph[v].remove(u)
        res.append(ok)
    return res
```

#### 复杂度

- **时间复杂度**：`O(requests * (restrictions * n))`  
  - 直观理解：对每条请求我们要遍历所有禁令（`restrictions`），每次禁令检查要在最坏情况下遍历全部 `n` 个人（即一次 BFS），于是乘起来就是这么多次操作。  
- **空间复杂度**：`O(n + requests)`  
  - 只保存了朋友关系的邻接表，最多 `n` 个节点加上至多 `requests` 条边。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于每次请求都要 **遍历所有限制**，并且 **搜索连通性**。  
我们需要一种数据结构，能够：

1. **快速判断两个人是否已经在同一个连通块**（即 O(α(n))，几乎是常数时间）。  
2. **在合并两个人的朋友圈后**，仍能高效检查所有限制是否被破坏。

这正是 **并查集（Union‑Find / Disjoint Set Union, DSU）** 能做到的。  
- 并查集把每个人归入一个“集合”，集合的根节点（parent）唯一标识该连通块。  
- `find(x)` 能在几乎 O(1) 的时间得到 `x` 所在集合的根。  
- `union(x, y)` 把两个集合合并。

**关键点**：在处理一次请求 `[u, v]` 时，我们只需要检查 **所有限制** 中，是否存在某对 `[x, y]` 使得：

```
find(x) == find(y)   （已经在同一个集合）   且
find(u) == find(v)   （如果把 u、v 合并后会把 x、y 拉进同一个集合）
```

更直接的做法是：**在尝试合并前**，先遍历所有限制，判断如果合并 `u`、`v`，是否会导致某个限制的两人落在同一个集合。  
因为 `find` 操作很快，遍历 `restrictions`（最多 1000 条）即可在 O(1000) 时间内完成检查。  
整体时间复杂度降为 `O(requests * restrictions * α(n))`，α 为 Ackermann 函数的反函数，几乎可以视作常数。

**并查集的实现要点**（对初学者友好）：

- **父指针数组 `parent[i]`**：`parent[i] = i` 表示自己是根。  
- **路径压缩**：`find(x)` 时把沿途的节点直接挂到根上，后面查找更快。  
- **按秩合并**（可选）：把小树挂到大树下，保持树的高度低。这里因为 `n ≤ 1000`，即使不按秩也能 AC，但加上会更稳妥。

#### 代码（Python）

```python
from typing import List

class DSU:
    """并查集（Disjoint Set Union）实现，带路径压缩"""
    def __init__(self, n: int):
        self.parent = list(range(n))   # 初始每个人自己是一个集合
        self.rank = [0] * n            # 按秩合并时使用的高度估计

    def find(self, x: int) -> int:
        """返回 x 所在集合的根节点，顺便压缩路径"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # 递归压缩
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        """把 x、y 所在的集合合并"""
        xr, yr = self.find(x), self.find(y)
        if xr == yr:      # 已经在同一个集合，无需再合并
            return
        # 按秩合并：把秩低的根挂到秩高的根下
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        elif self.rank[xr] > self.rank[yr]:
            self.parent[yr] = xr
        else:
            self.parent[yr] = xr
            self.rank[xr] += 1

def friendRequests_optimal(
    n: int, restrictions: List[List[int]], requests: List[List[int]]
) -> List[bool]:
    dsu = DSU(n)
    ans = []

    for u, v in requests:
        # 先找出 u、v 各自所在的根
        ru, rv = dsu.find(u), dsu.find(v)

        # 如果已经在同一个集合，直接成功（题目说明）
        if ru == rv:
            ans.append(True)
            continue

        # 检查所有限制，判断合并后是否会冲突
        conflict = False
        for x, y in restrictions:
            # 如果 x、y 本来就在同一个集合，说明已有冲突（理论上不可能出现，因为之前已保证合法）
            # 关键检查：合并后 x、y 会被连到一起吗？
            if (dsu.find(x) == ru and dsu.find(y) == rv) or \
               (dsu.find(x) == rv and dsu.find(y) == ru):
                conflict = True
                break

        if conflict:
            ans.append(False)          # 这条请求被拒绝，集合保持不变
        else:
            # 没有冲突，安全合并
            dsu.union(ru, rv)
            ans.append(True)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(requests * (restrictions * α(n)))`  
  - `α(n)` 是 Ackermann 反函数的极慢增长函数，对 `n ≤ 1000` 来说几乎等于 1。  
  - 直观上可以理解为：每条请求我们只遍历所有限制一次（最多 1000 次），每次检查只需要几次 `find`（常数时间），所以整体大约是 `1000 * 1000 = 10⁶` 次操作，轻松跑完。

- **空间复杂度**：`O(n + restrictions)`  
  - `parent`、`rank` 数组各占 `O(n)`，再加上存放限制的列表 `O(restrictions)`，整体线性。

---

## 心得

- **核心技巧**：使用 **并查集（Union‑Find）** 快速维护「朋友连通块」并在每次合并前检查限制。  
- **适用的题型**  
  1. **社交网络/朋友关系** 类问题（如 LeetCode 1657. 确定二分图、1971. 寻找图中是否存在路径）  
  2. **离线连通性**（如 LeetCode 1997. 访问数组的最小总时间）  
  3. **带约束的合并**（如 LeetCode 2611. 老鼠和奶酪游戏的并查集解法）  
- **一句话总结**：  
  *“把每个人看成一个集合，用并查集快速判断是否会把受限的两个人拉进同一个集合。”*

---

## 反思

- **第一反应**：看到“不能直接或间接成为朋友”就想到图的连通性，先用 BFS/DFS 暴力检查。  
- **最容易踩的坑**  
  1. **忽略已经在同一集合的请求**：题目说明即使已经是朋友也算成功，忘记这点会误判。  
  2. **检查限制时的细节**：必须在合并前判断“如果把 u、v 合并，是否会导致某对限制的根相同”。直接比较 `find(u)==find(x)` 之类的写法容易漏掉对称情况。  
  3. **路径压缩**：不加路径压缩会导致 `find` 退化成线性查找，时间会慢很多。  
- **下次遇到同类题**：  
  1. 先确认是否需要维护“连通块”。  
  2. 立即考虑并查集来实现 O(α(n)) 的合并与查询。  
  3. 在合并前检查所有“禁止同在一个集合”的约束。  

祝你玩转并查集，顺利击破所有限制类题目！