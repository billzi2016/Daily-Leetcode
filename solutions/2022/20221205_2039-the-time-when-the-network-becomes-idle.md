# #2039. 网络空闲的时刻 / The Time When the Network Becomes Idle

> 难度：中等 · 标签：Array、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/the-time-when-the-network-becomes-idle/)

---

## 题目（英文原版）

**Description**

There is a network of n servers, labeled from 0 to n - 1. You are given a 2D integer array edges, where edges[i] = [ui, vi] indicates there is a message channel between servers ui and vi, and they can pass any number of messages to each other directly in one second. You are also given a 0-indexed integer array patience of length n.
All servers are connected, i.e., a message can be passed from one server to any other server(s) directly or indirectly through the message channels.
The server labeled 0 is the master server. The rest are data servers. Each data server needs to send its message to the master server for processing and wait for a reply. Messages move between servers optimally, so every message takes the least amount of time to arrive at the master server. The master server will process all newly arrived messages instantly and send a reply to the originating server via the reversed path the message had gone through.
At the beginning of second 0, each data server sends its message to be processed. Starting from second 1, at the beginning of every second, each data server will check if it has received a reply to the message it sent (including any newly arrived replies) from the master server:
The network becomes idle when there are no messages passing between servers or arriving at servers.
Return the earliest second starting from which the network becomes idle.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[1,2]], patience = [0,2,1]
Output: 8
Explanation:
At (the beginning of) second 0,
- Data server 1 sends its message (denoted 1A) to the master server.
- Data server 2 sends its message (denoted 2A) to the master server.

At second 1,
- Message 1A arrives at the master server. Master server processes message 1A instantly and sends a reply 1A back.
- Server 1 has not received any reply. 1 second (1 < patience[1] = 2) elapsed since this server has sent the message, therefore it does not resend the message.
- Server 2 has not received any reply. 1 second (1 == patience[2] = 1) elapsed since this server has sent the message, therefore it resends the message (denoted 2B).

At second 2,
- The reply 1A arrives at server 1. No more resending will occur from server 1.
- Message 2A arrives at the master server. Master server processes message 2A instantly and sends a reply 2A back.
- Server 2 resends the message (denoted 2C).
...
At second 4,
- The reply 2A arrives at server 2. No more resending will occur from server 2.
...
At second 7, reply 2D arrives at server 2.

Starting from the beginning of the second 8, there are no messages passing between servers or arriving at servers.
This is the time when the network becomes idle.
```

**Example 2:**

```
Input: edges = [[0,1],[0,2],[1,2]], patience = [0,10,10]
Output: 3
Explanation: Data servers 1 and 2 receive a reply back at the beginning of second 2.
From the beginning of the second 3, the network becomes idle.
```

**Constraints**

- n == patience.length
- 2 <= n <= 105
- patience[0] == 0
- 1 <= patience[i] <= 105 for 1 <= i < n
- 1 <= edges.length <= min(105, n * (n - 1) / 2)
- edges[i].length == 2
- 0 <= ui, vi < n
- ui != vi
- There are no duplicate edges.
- Each server can directly or indirectly reach another server.

---

## 题目（中文翻译）

**描述**  
有一个包含 `n` 台服务器的网络，服务器编号为 `0` 到 `n-1`。给定一个二维整数数组 `edges`，其中 `edges[i] = [ui, vi]` 表示服务器 `ui` 与服务器 `vi` 之间存在一条消息通道（message channel），它们可以在 **1 秒** 内直接相互传递任意数量的消息。另给定一个下标从 `0` 开始的整数数组 `patience`，长度为 `n`。

所有服务器都是连通的，即任意两台服务器之间都可以通过消息通道直接或间接传递消息。编号为 `0` 的服务器是 **主服务器（master server）**，其余为 **数据服务器（data server）**。每个数据服务器需要将自己的消息发送给主服务器进行处理，并等待主服务器的回复。消息在服务器之间的传递是最优的——每条消息都会以最短的时间到达主服务器。主服务器会立即处理所有新到达的消息，并沿着消息原先经过的路径的相反方向将回复发送回源服务器。

- 在第 **0 秒** 的开始时，所有数据服务器都会发送自己的消息以待处理。  
- 从第 **1 秒** 开始的每一秒的开始时，每个数据服务器会检查是否已经收到主服务器的回复（包括当秒新到达的回复）：  
  - 若已收到回复，则该数据服务器不再发送新的消息。  
  - 若未收到回复，则该数据服务器会每隔 `patience[i]` 秒重新发送一次自己的消息（即在第 `patience[i]`、`2*patience[i]`、`3*patience[i]` … 秒的开始时再次发送），直到收到回复为止。

当网络中不再有任何消息在服务器之间传递或到达任意服务器时，网络被视为 **空闲（idle）**。返回网络第一次变得空闲的 **最早秒数**（从第 0 秒开始计数）。

---

**示例 1**  
```
Input: edges = [[0,1],[1,2]], patience = [0,2,1]
Output: 8
Explanation:
在（第）第 0 秒的开始时，
- 数据服务器 1 发送消息 1A 到主服务器。
- 数据服务器 2 发送消息 2A 到主服务器。

第 1 秒时，
- 消息 1A 到达主服务器。主服务器立即处理该消息并发送回复 1A。
- 服务器 1 尚未收到回复……

（后续过程省略）
```

**示例 2**  
```
Input: edges = [[0,1],[0,2],[1,2]], patience = [0,10,10]
Output: 3
Explanation: 数据服务器 1 和 2 在第 2 秒的开始时收到回复。从第 3 秒的开始时起，网络变得空闲。
```

---

**约束条件**
- `n == patience.length`
- `2 <= n <= 10^5`
- `patience[0] == 0`
- `1 <= patience[i] <= 10^5`，对 `1 <= i < n` 成立
- `1 <= edges.length <= min(10^5, n * (n - 1) / 2)`
- `edges[i].length == 2`
- `0 <= ui, vi < n`
- `ui != vi`
- 不存在重复的边
- 任意两台服务器之间均可直接或间接到达

---

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个数据服务器都算出它到主服务器的最短路径**，再把这些最短时间代入题目给出的 “耐心 `patience[i]`” 规则，模拟它们在第几秒会再次发送消息，最后取所有服务器的“最后一次回复到达时间”最大值即可。

- **数据结构**  
  - **邻接表**：把 `edges` 组织成 `graph[u] = [v1, v2, …]`。这类似于我们在现实中查字典：键（`u`）是服务器编号，值（列表）是它直接相连的服务器们。  
  - **队列**（`collections.deque`）：在 BFS（广度优先搜索）中用来“逐层”遍历网络，类似于我们在排队买咖啡：先处理最前面的，再让后面的人依次进来。

- **为什么正确**  
  - BFS 从一个起点出发，层层向外扩散，第一次到达某个节点的步数就是**最短路径长度**（因为每条边的权重都是 1 秒）。  
  - 题目要求的“消息走的最短时间”恰好是这条最短路径的长度，乘以 2（来回）后再结合耐心公式，就能算出该服务器的最后一次回复到达时间。

- **时间/空间复杂度**  
  - 对每个服务器都跑一次 BFS，**时间**是 `O(n * (n + m))`（`m` 为边数），也就是**每次遍历整个图**，在最坏情况下会达到 **10⁵ × 10⁵**，显然会超时。  
  - **空间**主要是邻接表和 BFS 队列，`O(n + m)`，这部分还能接受。

> 大白话解释：  
> - `O(n²)` 并不是真的“n 的平方次”，而是说**随着服务器数量 n 增大，运行时间会像 n² 那样快速增长**，在 n=10⁵ 时几乎不可能在一秒内跑完。

#### 代码（Python）

```python
from collections import deque
from typing import List

def network_becomes_idle_bruteforce(edges: List[List[int]], patience: List[int]) -> int:
    n = len(patience)

    # 1️⃣ 建图（邻接表）
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 2️⃣ 对每个数据服务器单独跑 BFS，得到到 0 的最短距离
    def bfs(start: int) -> int:
        """返回 start 到 0 的最短步数"""
        visited = [False] * n
        q = deque([(start, 0)])          # (当前节点, 已走的步数)
        visited[start] = True
        while q:
            node, dist = q.popleft()
            if node == 0:                # 第一次碰到 0 就是最短距离
                return dist
            for nxt in graph[node]:
                if not visited[nxt]:
                    visited[nxt] = True
                    q.append((nxt, dist + 1))
        return -1   # 题目保证一定连通，这行永远不会执行

    max_time = 0
    for i in range(1, n):                # 0 是主服务器，不需要算
        dist = bfs(i)                    # 单点最短路
        round_trip = 2 * dist            # 来回时间
        # 计算该服务器最后一次回复到达的时刻
        if patience[i] >= round_trip:
            last_reply = round_trip
        else:
            # 发送的最后一条消息的发送时刻
            last_send = ((round_trip - 1) // patience[i]) * patience[i]
            last_reply = last_send + round_trip
        max_time = max(max_time, last_reply)

    # 网络在最后一次回复的下一秒才真正空闲
    return max_time + 1
```

> 关键行中文注释已经写在代码里，直接运行即可（只是在大数据规模下会超时）。

#### 复杂度

- **时间复杂度**：`O(n * (n + m))`  
  - 解释：对每个服务器都要遍历整张图一次，随着服务器数 `n` 增大，耗时会像 `n²` 那样快速增长。
- **空间复杂度**：`O(n + m)`  
  - 解释：存图的邻接表和 BFS 队列的大小随图的规模线性增长。

---

### 2. 最优解

#### 思路  

从暴力解我们可以看到 **“瓶颈”** 在于**对每个节点都跑一次 BFS**。事实上，所有节点的最短距离**都可以一次 BFS 同时得到**，因为所有边的权重相同（都是 1 秒），只要从主服务器 `0` 出发，层层向外遍历，就能在第一次访问到某个节点时记录它到 `0` 的最短步数。

**一步步推导**：

1. **一次 BFS 求全部最短距离**  
   - 从 `0` 开始，使用队列把距离为 `0`、`1`、`2` … 的节点依次放进来。第一次把节点 `i` 弹出时，记录 `dist[i]`。这相当于一次“全景测距”，比逐个测距省了 `n-1` 次遍历。

2. **根据 `dist[i]` 与 `patience[i]` 计算该服务器的“最后一次回复到达时间”**  
   - **往返时间** = `2 * dist[i]`（去一次 + 回一次）。
   - 若 `patience[i] >= 往返时间`，说明在第一次回复到达之前，服务器不会再次发送消息，只会等一次回复。此时**最后一次回复**恰好在 `往返时间` 秒时到达。
   - 否则，服务器会在 **每 `patience[i]` 秒** 发送一次“心跳”消息，直到收到回复为止。  
     - 设 `t = 往返时间`。服务器在 `t` 秒前的最后一次发送时间为 `last_send = floor((t-1) / patience[i]) * patience[i]`（因为在第 `t` 秒收到回复后就不再发送）。  
     - 那么 **最后一次回复到达** 的时刻 = `last_send + t`。

3. **整体网络空闲时间**  
   - 所有服务器的最后一次回复到达时间取最大值 `max_time`，网络在 **`max_time + 1`** 秒才真正没有任何消息在路上（因为第 `max_time` 秒的回复刚好到达，下一秒才“全员安静”）。

**核心算法/数据结构**  

- **广度优先搜索（BFS）**：一次遍历即可得到所有节点到源点的最短步数。  
- **整数除法取整**：`(t-1)//p * p` 用来求“不超过 t-1 的最大发送时刻”。这里的 `//` 是向下取整除法，像是把时间切成 `p` 秒一段，只取完整的段数。

**类比**：  
把网络看成一座城市的公交系统，所有站点（服务器）都要去中心站（主服务器）买票。一次 BFS 就像在地图上画出从中心站出发的**同心圆层**，每层的站点到中心的距离都是相同的。随后根据每个站点的“耐心”决定它们会不会在等票的过程中不停按铃（重复发送消息），最后找出最晚一位乘客拿到票的时间，再加上一秒，就是所有人都回到座位的时刻。

#### 代码（Python）

```python
from collections import deque
from typing import List

def networkBecomesIdle(edges: List[List[int]], patience: List[int]) -> int:
    """
    LeetCode 2039. The Time When the Network Becomes Idle
    思路：一次 BFS 求所有节点到 0 的最短距离 → 根据耐心计算每个节点的最后一次回复到达时间
    """
    n = len(patience)

    # 1️⃣ 建图（邻接表）
    graph = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # 2️⃣ 单次 BFS，得到 dist[i]（0 到 i 的最短步数）
    dist = [-1] * n          # -1 表示未访问
    q = deque([0])
    dist[0] = 0
    while q:
        cur = q.popleft()
        for nxt in graph[cur]:
            if dist[nxt] == -1:          # 第一次访问到 nxt，就一定是最短距离
                dist[nxt] = dist[cur] + 1
                q.append(nxt)

    # 3️⃣ 计算每个数据服务器的“最后一次回复到达时间”
    max_time = 0
    for i in range(1, n):                # 0 是主服务器，不需要考虑
        round_trip = 2 * dist[i]         # 去程 + 回程

        if patience[i] >= round_trip:
            # 只会发送一次，回复在 round_trip 秒时到达
            last_reply = round_trip
        else:
            # 会重复发送，计算最后一次发送的时刻
            last_send = ((round_trip - 1) // patience[i]) * patience[i]
            last_reply = last_send + round_trip

        max_time = max(max_time, last_reply)

    # 网络在最后一次回复的下一秒才真正空闲
    return max_time + 1
```

> 关键行已经加上中文注释，直接复制到 Python 环境即可运行。

#### 复杂度

- **时间复杂度**：`O(n + m)`  
  - 只进行一次 BFS，遍历所有节点和所有边一次。对每个节点再做 `O(1)` 的数学运算，整体随图的规模线性增长。  
  - 与暴力解的 `O(n * (n + m))` 相比，省掉了 `n-1` 次遍历，速度提升了 **数量级**。
- **空间复杂度**：`O(n + m)`  
  - 邻接表、距离数组、BFS 队列共占用与图规模线性相关的空间。  

---

## 心得

- **核心技巧**：**一次 BFS 求所有节点到根节点的最短距离** + **利用耐心值的整数取整公式** 计算“最后一次发送”时间。  
- **该技巧适用的题型**  
  1. **所有节点到某个源点的最短路径**（如 LeetCode 743、862 等）。  
  2. **基于最短路径再做时间/次数计算**（如“网络延迟时间”“最小传输时间”等）。  
- **一句话总结解题钥匙**：**把所有最短路一次算完，再用耐心的周期性发送规律推算出最晚的回复时间**。

---

## 反思

- **第一反应**：直接对每个节点跑 BFS（或 Dijkstra）再模拟发送过程，代码写得通俗但会超时。  
- **最容易踩的坑**  
  - **漏掉“+1”**：题目要求的是“从哪一秒开始网络全部空闲”，所以要在最大回复时间的基础上再加一秒。  
  - **耐心值等于往返时间的边界**：`patience[i] == round_trip` 时只会发送一次，不能误判为会重复发送。  
  - **整数取整的细节**：`(round_trip - 1) // patience[i]` 必须先减 1，否则会把恰好等于往返时间的那一次也算进发送次数，导致答案偏大。  
- **下次类似题的第一步**：**先判断能否一次 BFS/DFS 得到所有需要的最短距离**，再在此基础上考虑“周期性行为”或“累计时间”。这样可以把原本的指数/平方级别的暴力直接降到线性级别。