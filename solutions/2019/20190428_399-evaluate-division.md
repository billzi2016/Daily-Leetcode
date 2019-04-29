# #399. **除法求值** / Evaluate Division

> 难度：中等 · 标签：Array、String、Depth-First Search、Breadth-First Search、Union Find、Graph、Shortest Path · [LeetCode 链接](https://leetcode.com/problems/evaluate-division/)

---

## 题目（英文原版）

**Description**

You are given an array of variable pairs equations and an array of real numbers values, where equations[i] = [Ai, Bi] and values[i] represent the equation Ai / Bi = values[i]. Each Ai or Bi is a string that represents a single variable.
You are also given some queries, where queries[j] = [Cj, Dj] represents the jth query where you must find the answer for Cj / Dj = ?.
Return the answers to all queries. If a single answer cannot be determined, return -1.0.
Note: The input is always valid. You may assume that evaluating the queries will not result in division by zero and that there is no contradiction.
Note: The variables that do not occur in the list of equations are undefined, so the answer cannot be determined for them.

**Examples**

**Example 1:**

```
Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
Explanation: 
Given: a / b = 2.0, b / c = 3.0
queries are: a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ? 
return: [6.0, 0.5, -1.0, 1.0, -1.0 ]
note: x is undefined => -1.0
```

**Example 2:**

```
Input: equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
Output: [3.75000,0.40000,5.00000,0.20000]
```

**Example 3:**

```
Input: equations = [["a","b"]], values = [0.5], queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
Output: [0.50000,2.00000,-1.00000,-1.00000]
```

**Constraints**

- 1 <= equations.length <= 20
- equations[i].length == 2
- 1 <= Ai.length, Bi.length <= 5
- values.length == equations.length
- 0.0 < values[i] <= 20.0
- 1 <= queries.length <= 20
- queries[i].length == 2
- 1 <= Cj.length, Dj.length <= 5
- Ai, Bi, Cj, Dj consist of lower case English letters and digits.

---

## 题目（中文翻译）

给定一个变量对数组 `equations` 和一个实数数组 `values`，其中 `equations[i] = [Aᵢ, Bᵢ]` 且 `values[i]` 表示等式 `Aᵢ / Bᵢ = values[i]`。每个 `Aᵢ` 或 `Bᵢ` 是表示单个变量的字符串。

同时给定若干查询 `queries`，其中 `queries[j] = [Cⱼ, Dⱼ]` 表示第 `j` 个查询，需要求解 `Cⱼ / Dⱼ = ?`。

返回所有查询的答案。如果某个答案无法确定，返回 `-1.0`。

> **注意**  
> - 输入始终有效。可以假设求解查询时不会出现除以零的情况，且不存在矛盾的等式。  
> - 未出现在 `equations` 列表中的变量是未定义的，因此对应的答案无法确定。

### 示例

**示例 1**

```text
Input: equations = [["a","b"],["b","c"]], values = [2.0,3.0], queries = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
Output: [6.00000,0.50000,-1.00000,1.00000,-1.00000]
Explanation: 
Given: a / b = 2.0, b / c = 3.0
queries are: a / c = ?, b / a = ?, a / e = ?, a / a = ?, x / x = ? 
return: [6.0, 0.5, -1.0, 1.0, -1.0 ]
note: x is undefined => -1.0
```

**示例 2**

```text
Input: equations = [["a","b"],["b","c"],["bc","cd"]], values = [1.5,2.5,5.0], queries = [["a","c"],["c","b"],["bc","cd"],["cd","bc"]]
Output: [3.75000,0.40000,5.00000,0.20000]
```

**示例 3**

```text
Input: equations = [["a","b"]], values = [0.5], queries = [["a","b"],["b","a"],["a","c"],["x","y"]]
Output: [0.50000,2.00000,-1.00000,-1.00000]
```

### 约束条件

- `1 <= equations.length <= 20`
- `equations[i].length == 2`
- `1 <= Aᵢ.length, Bᵢ.length <= 5`
- `values.length == equations.length`
- `0.0 < values[i] <= 20.0`
- `1 <= queries.length <= 20`
- `queries[i].length == 2`
- `1 <= Cⱼ.length, Dⱼ.length <= 5`
- `Aᵢ, Bᵢ, Cⱼ, Dⱼ` 仅由小写英文字母和数字组成。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把所有已知的等式看成 **有向图** 的边：

- 每个变量（`a`, `b` …）是图中的一个节点。  
- `a / b = 2.0` 就相当于在 `a → b` 上放一条权值为 `2.0` 的有向边，  
  同时我们还可以放一条相反方向的边 `b → a`，权值为 `1/2.0`（因为 `b / a = 1 / (a / b)`）。

有了这张图，**查询** `C / D = ?` 就等价于在图中找一条从 `C` 到 `D` 的路径，路径上所有边的权值相乘即为答案。

> **类比**：想象你在城市里旅行，路口是变量，路上有指示牌写着 “从这里到下一个地点乘以 2”。  
> 只要你能走到目标地点，就把所有指示牌的倍率连乘起来，得到最终的比例。

**为什么正确**：  
因为每条已知等式本身就表达了两个变量的比例关系。把它们串成一条链，链上每一步都保持比例不变，整个链的乘积自然就是起点到终点的比例。

**暴力实现**：  
对每个查询都 **一次性** 进行深度优先搜索（DFS）或广度优先搜索（BFS），找出一条合法路径并累乘权值。若搜索不到则返回 `-1.0`。

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List, Dict, Tuple

def calcEquation(
    equations: List[List[str]],
    values: List[float],
    queries: List[List[str]]
) -> List[float]:
    # 1. 建图：邻接表 + 权值
    graph: Dict[str, List[Tuple[str, float]]] = defaultdict(list)
    for (a, b), v in zip(equations, values):
        graph[a].append((b, v))      # a / b = v
        graph[b].append((a, 1.0 / v))# b / a = 1/v

    # 2. 对每个查询做一次 BFS
    def bfs(src: str, dst: str) -> float:
        if src not in graph or dst not in graph:   # 变量根本不在图里
            return -1.0
        if src == dst:                             # 同一个变量，比例必为 1
            return 1.0

        visited = set()
        q = deque()
        q.append((src, 1.0))   # (当前节点, 从 src 累乘得到的比例)

        while q:
            node, prod = q.popleft()
            if node == dst:
                return prod
            visited.add(node)
            for neighbor, weight in graph[node]:
                if neighbor not in visited:
                    q.append((neighbor, prod * weight))
        return -1.0   # 没有找到路径

    # 3. 收集答案
    return [bfs(c, d) for c, d in queries]
```

**关键行解释**  

- `graph[a].append((b, v))`：把 `a → b` 的比例 `v` 加入邻接表。  
- `q.append((src, 1.0))`：搜索起点的累计比例初始为 `1`（因为 `src/src = 1`）。  
- `prod * weight`：沿着一条边前进时，把当前累计比例乘上这条边的权值。  

#### 复杂度  

- **时间复杂度**：`O(Q * (V + E))`  
  - 对每个查询我们最坏要遍历整张图（`V` 个节点、`E` 条边）。  
  - 对于本题的约束（`V ≤ 40`，`E ≤ 40`），完全够用。  
  - **大白话**：想象每次查询都要把整张地图从头到尾走一遍，查询多了就会“累”。

- **空间复杂度**：`O(V + E)`  
  - 用邻接表存图，需要保存所有节点和边的信息。  
  - BFS 队列和 visited 集合最多也只会占 `V` 的空间。  

---  

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次查询都重新搜索**。如果我们能够在构建图的同时，把所有变量划分到“同一连通块”，并记录它们之间的比例关系，那么查询就可以 **直接算出**，而不必再遍历。

这正是 **加权并查集（Union‑Find with weight）** 能做到的：

1. **并查集** 能快速判断两个元素是否在同一个集合（即是否有路径相连），并在 `≈ O(α(N))`（几乎是常数）时间内合并集合。  
2. **加权** 的意思是：除了记录每个节点的“父亲”，我们还记录 **该节点相对于父亲的比例**。  
   - `weight[x]` 表示 `x / parent[x]` 的值。  
   - 通过路径压缩时累乘这些比例，就可以得到 **任意节点相对于根节点的比例**。

**如何合并**  
已知等式 `a / b = v`，我们把 `a` 和 `b` 放到同一个集合里：

- 设 `ra`、`rb` 为 `a`、`b` 当前的根节点。  
- 若 `ra != rb`，我们让 `ra` 的父亲指向 `rb`（或反向），并计算出 `weight[ra]`，使得整体比例保持不变。  
- 推导公式（假设把 `ra` 接到 `rb`）：  

```
weight[ra] = (b / ra) * v
           = (weight[b] / weight[a]) * v
```

（这里 `weight[x]` 已经是 “x / root(x)”）

**查询**  
要回答 `c / d`：

- 若 `c`、`d` 不在同一个集合 → 返回 `-1.0`。  
- 否则，`c / d = (c / root) / (d / root) = weight[c] / weight[d]`。

> **类比**：把每个变量看成一根细绳的两端，根节点是绳子的“固定点”。`weight[x]` 就是从 `x` 到固定点的伸长比例。只要两根绳子连到同一个固定点，它们之间的比例就可以直接用两段伸长比例相除得到。

#### 代码（Python）

```python
from typing import List, Dict

class UnionFind:
    def __init__(self):
        self.parent: Dict[str, str] = {}   # 父节点映射
        self.weight: Dict[str, float] = {} # x / parent[x] 的比例

    def find(self, x: str) -> str:
        """
        路径压缩版的 find。
        同时把 weight[x] 更新为 x / root(x)。
        """
        if x not in self.parent:
            # 第一次出现的变量，自己是根，比例为 1
            self.parent[x] = x
            self.weight[x] = 1.0
            return x

        if self.parent[x] != x:
            orig_parent = self.parent[x]
            root = self.find(orig_parent)               # 递归找根
            # 更新 weight[x]：x / root = (x / orig_parent) * (orig_parent / root)
            self.weight[x] *= self.weight[orig_parent]
            self.parent[x] = root
        return self.parent[x]

    def union(self, a: str, b: str, value: float) -> None:
        """
        合并 a 与 b，已知 a / b = value
        """
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return

        # 把 ra 接到 rb 上，计算 weight[ra]
        # 目标是保持 a / b = value 成立
        # a / ra = weight[a], b / rb = weight[b]
        # 所以 ra / rb = (b / ra) * value
        ratio = (self.weight[b] * value) / self.weight[a]
        self.parent[ra] = rb
        self.weight[ra] = ratio

    def isConnected(self, a: str, b: str) -> bool:
        return a in self.parent and b in self.parent and self.find(a) == self.find(b)

    def getRatio(self, a: str, b: str) -> float:
        """
        前提是 a 与 b 已经在同一集合里
        返回 a / b
        """
        return self.weight[a] / self.weight[b]


def calcEquation(
    equations: List[List[str]],
    values: List[float],
    queries: List[List[str]]
) -> List[float]:
    uf = UnionFind()

    # 1. 把所有等式加入并查集
    for (a, b), v in zip(equations, values):
        uf.union(a, b, v)

    # 2. 直接回答查询
    ans = []
    for c, d in queries:
        if uf.isConnected(c, d):
            ans.append(uf.getRatio(c, d))
        else:
            ans.append(-1.0)
    return ans
```

**关键行解释**  

- `self.parent[x] = x; self.weight[x] = 1.0`：第一次遇到变量时把它当作自己的根，比例自然是 `1`。  
- `self.weight[x] *= self.weight[orig_parent]`：路径压缩时把 `x` 到根的比例累乘进去，等价于 “把两段绳子合并”。  
- `ratio = (self.weight[b] * value) / self.weight[a]`：计算把 `ra` 接到 `rb` 时需要的权重，使得原等式仍然成立。  
- `uf.getRatio(c, d) = self.weight[c] / self.weight[d]`：因为两者都相对于同一个根，直接相除得到 `c / d`。  

#### 复杂度  

- **时间复杂度**：`O(N α(N) + Q α(N))`  
  - `N` 为等式数量，`Q` 为查询数量。  
  - `α(N)` 是 Ackermann 函数的逆，几乎可以认为是常数（比如 ≤ 5）。  
  - **大白话**：相当于每条等式和每个查询只做了几次“找根”操作，几乎是瞬间完成。

- **空间复杂度**：`O(V)`  
  - 只需要为每个出现过的变量存一个父指针和一个比例，`V` 为变量总数（最多 40 左右）。  

---

## 心得

- **核心技巧**：把除法关系抽象为 **有向加权图**，进而使用 **并查集的加权版** 实现快速连通性检查与比例计算。  
- **适用的题型**  
  1. **等式求值**（本题）  
  2. **网络信任关系**：如 “A 信任 B 的程度为 0.8”，求任意两人之间的信任度。  
  3. **比例转换**：如 “1 英里 = 1.60934 公里”，多步转换的查询。  
- **一句话总结**：把变量之间的除法看成“绳子上的倍率”，用加权并查集把所有绳子连到同一个根，就能 O(1) 直接算出任意两点的比例。

---

## 反思

- **第一反应**：看到 “变量 / 变量 = 实数”，立刻想到图（节点是变量，边是比例），于是想到 BFS/DFS。  
- **最容易踩的坑**  
  - **未出现的变量**：查询中出现的变量可能根本不在等式里，需要提前判断返回 `-1.0`。  
  - **自除**：`a / a` 的答案永远是 `1.0`（只要 `a` 已知），别忘了这点。  
  - **路径压缩时的比例更新**：如果忘记把 `weight[x]` 乘上父亲的权重，后面的比例会全部错。  
- **下次思路**：遇到 “两两关系 + 多次查询” 的题目，第一步先判断能否抽象成 **并查集**（或 **图 + 预处理**）结构，尤其是“关系是可传递且可合并”的场景。这样往往可以把每次查询从 “遍历整张图” 降到 “几次找根”。