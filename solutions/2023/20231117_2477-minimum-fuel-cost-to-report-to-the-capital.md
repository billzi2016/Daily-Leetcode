# #2477. 报告到首都的最小燃料费用 / Minimum Fuel Cost to Report to the Capital

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/minimum-fuel-cost-to-report-to-the-capital/)

---

## 题目（英文原版）

**Description**

There is a tree (i.e., a connected, undirected graph with no cycles) structure country network consisting of n cities numbered from 0 to n - 1 and exactly n - 1 roads. The capital city is city 0. You are given a 2D integer array roads where roads[i] = [ai, bi] denotes that there exists a bidirectional road connecting cities ai and bi.
There is a meeting for the representatives of each city. The meeting is in the capital city.
There is a car in each city. You are given an integer seats that indicates the number of seats in each car.
A representative can use the car in their city to travel or change the car and ride with another representative. The cost of traveling between two cities is one liter of fuel.
Return the minimum number of liters of fuel to reach the capital city.

**Examples**

**Example 1:**

```
Input: roads = [[0,1],[0,2],[0,3]], seats = 5
Output: 3
Explanation: 
- Representative1 goes directly to the capital with 1 liter of fuel.
- Representative2 goes directly to the capital with 1 liter of fuel.
- Representative3 goes directly to the capital with 1 liter of fuel.
It costs 3 liters of fuel at minimum. 
It can be proven that 3 is the minimum number of liters of fuel needed.
```

**Example 2:**

```
Input: roads = [[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]], seats = 2
Output: 7
Explanation: 
- Representative2 goes directly to city 3 with 1 liter of fuel.
- Representative2 and representative3 go together to city 1 with 1 liter of fuel.
- Representative2 and representative3 go together to the capital with 1 liter of fuel.
- Representative1 goes directly to the capital with 1 liter of fuel.
- Representative5 goes directly to the capital with 1 liter of fuel.
- Representative6 goes directly to city 4 with 1 liter of fuel.
- Representative4 and representative6 go together to the capital with 1 liter of fuel.
It costs 7 liters of fuel at minimum. 
It can be proven that 7 is the minimum number of liters of fuel needed.
```

**Example 3:**

```
Input: roads = [], seats = 1
Output: 0
Explanation: No representatives need to travel to the capital city.
```

**Constraints**

- 1 <= n <= 105
- roads.length == n - 1
- roads[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- roads represents a valid tree.
- 1 <= seats <= 105

---

## 题目（中文翻译）

描述  
给定一个 **树**（即一个连通的、无环的无向图），该树表示一个由 `n` 座城市组成的国家网络，城市编号为 `0` 到 `n - 1`，恰好有 `n - 1` 条道路。首都是城市 `0`。  
你得到一个二维整数数组 `roads`，其中 `roads[i] = [a_i, b_i]` 表示城市 `a_i` 与城市 `b_i` 之间存在一条双向道路。  

每座城市都有一位代表参加在首都举行的会议。每座城市还有一辆汽车，`seats` 表示每辆汽车的座位数。  

- 代表可以使用所在城市的汽车自行前往，也可以在途中换乘其他代表的汽车。  
- 在任意两座相邻城市之间行驶消耗 **1 升燃料**。  

返回所有代表抵达首都所需的最少燃料（升）总量。

示例  
示例 1  
```text
Input: roads = [[0,1],[0,2],[0,3]], seats = 5
Output: 3
Explanation:
- 代表 1 直接前往首都，消耗 1 升燃料。
- 代表 2 直接前往首都，消耗 1 升燃料。
- 代表 3 直接前往首都，消耗 1 升燃料。
最少共需要 3 升燃料。可以证明 3 是所需的最小燃料量。
```

示例 2  
```text
Input: roads = [[3,1],[3,2],[1,0],[0,4],[0,5],[4,6]], seats = 2
Output: 7
Explanation:
- 代表 2 直接前往城市 3，消耗 1 升燃料。
- 代表 2 与代表 3 一起前往城市 1，消耗 1 升燃料。
- 代表 2 与代表 3 一起前往首都，消耗 1 升燃料。
- 代表 1 直接前往首都，消耗 1 升燃料。
- 代表 4 与代表 5 先在城市 0 汇合，然后一起前往首都，消耗 2 升燃料。
- 代表 6 先到城市 4，与代表 4、5 会合后一起前往首都，消耗 1 升燃料。
总计需要 7 升燃料。
```

示例 3  
```text
Input: roads = [], seats = 1
Output: 0
Explanation: 没有代表需要前往首都，燃料消耗为 0。
```

约束条件  
- `1 <= n <= 10^5`  
- `roads.length == n - 1`  
- `roads[i].length == 2`  
- `0 <= a_i, b_i < n`  
- `a_i != b_i`  
- `roads` 构成一棵有效的树  
- `1 <= seats <= 10^5`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**每个城市的代表自己开车，沿着唯一的路径一路开到首都**。  
因为题目保证道路构成一棵树（没有环），所以任意两点之间只有唯一一条简单路径。  

实现时可以把树看成**邻接表**（每个城市记录它相邻的城市列表），  
对每个城市 `i (i≠0)`：

1. 用 BFS/DFS 找到从 `i` 到 `0` 的路径长度 `dist`（走几条路）。  
2. 这条路径每走一条路都要消耗 1 升油，所以该代表消耗 `dist` 升。  

把所有代表的消耗相加，就是一种可行的答案。  

> **类比**：邻接表就像城市的“通讯录”，键是城市编号，值是它的“朋友”（相邻城市）。  
> BFS/DFS 就像在这本通讯录里找“最短的亲戚关系链”。  

这种方法一定能得到一个合法的燃料消耗，因为每个人都独自完成了行程。  

#### 代码（Python）  

```python
from collections import deque, defaultdict
from math import ceil
from typing import List

def brute_fuel(roads: List[List[int]], seats: int) -> int:
    # 建立邻接表
    graph = defaultdict(list)
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)

    n = max(max(pair) for pair in roads) + 1 if roads else 1
    total = 0

    # 对每个非首都城市，单独 BFS 求到 0 的距离
    for start in range(1, n):
        # BFS 找最短路径长度（树上唯一路径的长度）
        q = deque([(start, 0)])          # (当前节点, 已走的边数)
        visited = {start}
        while q:
            node, dist = q.popleft()
            if node == 0:                # 到达首都
                total += dist            # 消耗的油等于走的边数
                break
            for nb in graph[node]:
                if nb not in visited:
                    visited.add(nb)
                    q.append((nb, dist + 1))
    return total
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  对每个城市都要一次 BFS，最坏情况下每次遍历 `O(n)` 条边，整体是 `n` 次 → `n·n = n²`。  
  大白话：如果城市有 10,000 个，暴力解大概要做 100,000,000 次“走路”操作，明显太慢。  

- **空间复杂度**：`O(n)`  
  主要是邻接表和 BFS 队列占用的空间，和城市数量成线性关系。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在 **“每个人都单独走”**，我们完全可以让几个人 **共享同一辆车**，从而减少往返的次数。  

关键观察：  
1. **树的结构决定了所有代表必须沿着树的边向上（朝根 0）移动**。  
2. 对于任意一条边 `u‑v`（假设 `v` 是离根更远的子节点），所有 **位于子树 `v` 内的代表** 必须至少经过这条边一次才能到达根。  
3. 如果子树 `v` 中有 `cnt` 个人，而每辆车只能坐 `seats` 人，则 **这 `cnt` 个人需要的车次数** 为  

\[
\text{trips} = \left\lceil \frac{cnt}{\text{seats}} \right\rceil
\]

   每一次车经过这条边都要消耗 1 升油，所以 **这条边的燃料消耗** 为 `trips`。  

于是，**只要我们知道每个子树里有多少人**（其实每个城市恰好有 1 位代表），就可以直接算出每条边需要多少次车经过，从而得到最小燃料。  

实现步骤：

1. **构造邻接表**（同上）。  
2. 任选根 `0`，用 **递归深度优先搜索（DFS）** 遍历整棵树。  
   - DFS 返回值为 **当前子树的代表人数**。  
   - 对每个子节点 `child`，在返回后得到 `sub_cnt`（子树人数）。  
   - 计算 `trips = ceil(sub_cnt / seats)`，累加到全局答案 `ans += trips`。  
   - 将 `sub_cnt` 加到父节点的计数中，继续向上传递。  
3. 最终 `ans` 即为最小燃料消耗。  

> **类比**：把每条边想象成一条“搬运带”。子树里有多少件货（代表），带子能装几件（座位），就要跑几趟。所有带子跑的次数相加，就是总油耗。  

#### 代码（Python）  

```python
from collections import defaultdict
from math import ceil
from typing import List

def minimumFuelCost(roads: List[List[int]], seats: int) -> int:
    """
    返回把所有代表送到首都（0）所需的最少燃料（升）。
    """
    if not roads:          # n == 1 的特殊情况
        return 0

    # 1. 建立邻接表（每个城市的“朋友列表”）
    graph = defaultdict(list)
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)

    ans = 0                 # 累计燃料消耗

    # 2. 深度优先搜索，返回子树中代表的数量
    def dfs(node: int, parent: int) -> int:
        nonlocal ans
        cnt = 1             # 当前城市本身有 1 位代表

        for nb in graph[node]:
            if nb == parent:    # 防止回到父节点形成循环
                continue
            sub_cnt = dfs(nb, node)        # 子树人数
            # 这条边需要的车次数 = ceil(sub_cnt / seats)
            trips = ceil(sub_cnt / seats)
            ans += trips                     # 该边消耗的油
            cnt += sub_cnt                   # 合并子树人数

        return cnt

    dfs(0, -1)   # 从根 0 开始，父节点设为 -1（不存在）
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  每条边只会被遍历一次（DFS 进出各一次），所以整体线性。  
  与暴力解 `O(n²)` 相比，提升了 **n 倍** 的效率。  

- **空间复杂度**：`O(n)`  
  递归栈深度最坏为树的高度，最坏情况下是 `n`（链状树），加上邻接表也都是 `O(n)`。  

---  

## 心得  

- **核心技巧**：利用树的“子树人数 + 车座位数”来直接算每条边需要的车次数（即 `ceil(cnt / seats)`）。  
- **适用场景**：  
  1. 所有节点都需要向根汇聚，且每次移动的费用只与经过的边数有关（如 “把所有石子搬到根”）。  
  2. 需要在树上做“分批运输”或“分批聚合”的问题（例如 LeetCode 2477 *Minimum Fuel Cost to Report to the Capital*、LC 1510 *Stone Game IV* 的树形变体）。  
- **一句话总结**：**把每条边想成搬运带，子树人数除以座位数向上取整即为该带的搬运次数**。  

## 反思  

- **第一反应**：直接让每个人单独走（暴力 BFS），因为最容易想到“每个人都要到根”。  
- **最容易踩的坑**：  
  - 忘记把 **根节点自身的代表** 也计入子树人数（导致子树计数少 1）。  
  - `seats` 可能大于子树人数，`ceil` 必须处理好除不尽的情况，否则会算成 0 次搬运。  
  - 树可能是 **单节点**（`roads` 为空），需要提前返回 0。  
- **下次思路**：看到“所有人要向同一个节点聚合”且“每次移动成本与边数有关”，立刻想到 **在树上统计子树规模**，再用 **分批运输公式** 计算每条边的费用。