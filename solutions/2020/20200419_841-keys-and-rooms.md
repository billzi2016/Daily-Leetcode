# #841. 钥匙和房间 / Keys and Rooms

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/keys-and-rooms/)

---

## 题目（英文原版）

**Description**

There are n rooms labeled from 0 to n - 1 and all the rooms are locked except for room 0. Your goal is to visit all the rooms. However, you cannot enter a locked room without having its key.
When you visit a room, you may find a set of distinct keys in it. Each key has a number on it, denoting which room it unlocks, and you can take all of them with you to unlock the other rooms.
Given an array rooms where rooms[i] is the set of keys that you can obtain if you visited room i, return true if you can visit all the rooms, or false otherwise.

**Examples**

**Example 1:**

```
Input: rooms = [[1],[2],[3],[]]
Output: true
Explanation: 
We visit room 0 and pick up key 1.
We then visit room 1 and pick up key 2.
We then visit room 2 and pick up key 3.
We then visit room 3.
Since we were able to visit every room, we return true.
```

**Example 2:**

```
Input: rooms = [[1,3],[3,0,1],[2],[0]]
Output: false
Explanation: We can not enter room number 2 since the only key that unlocks it is in that room.
```

**Constraints**

- n == rooms.length
- 2 <= n <= 1000
- 0 <= rooms[i].length <= 1000
- 1 <= sum(rooms[i].length) <= 3000
- 0 <= rooms[i][j] < n
- All the values of rooms[i] are unique.

---

## 题目（中文翻译）

描述  
共有 `n` 间房间，编号从 `0` 到 `n - 1`，除房间 `0` 外所有房间最初都是锁着的。你的目标是访问所有房间，但没有对应钥匙（key）时无法进入锁着的房间。  

当你进入某个房间时，可能会在其中找到一组互不相同的钥匙。每把钥匙上标有一个数字，表示它可以打开对应编号的房间，你可以把这些钥匙全部带走，用来打开其他房间。  

给定一个数组 `rooms`，其中 `rooms[i]` 表示访问房间 `i` 后可以获得的钥匙集合，若你能够访问所有房间则返回 `true`，否则返回 `false`。

示例  

示例 1:  
``` 
Input: rooms = [[1],[2],[3],[]]
Output: true
Explanation: 
我们先访问房间 0，拿到钥匙 1。  
随后访问房间 1，拿到钥匙 2。  
随后访问房间 2，拿到钥匙 3。  
最后访问房间 3。  
因为我们能够访问每一间房间，返回 true。
```

示例 2:  
``` 
Input: rooms = [[1,3],[3,0,1],[2],[0]]
Output: false
Explanation: 
我们无法进入编号为 2 的房间，因为唯一能打开它的钥匙就在该房间里。
```

约束条件  
- `n == rooms.length`  
- `2 <= n <= 1000`  
- `0 <= rooms[i].length <= 1000`  
- `1 <= sum(rooms[i].length) <= 3000`  
- `0 <= rooms[i][j] < n`  
- `rooms[i]` 中的所有值均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
这道题本质上是 **图的遍历**：  
- 每个房间视作图中的一个节点  
- 房间里拿到的钥匙视作从该节点指向其他节点的有向边  

最直接的想法是 **一次遍历所有钥匙**，不断尝试打开还能打开的房间，直到再也打不开新的房间为止。  
可以把它想象成 **“把所有钥匙放在桌子上”，一次检查桌子上有没有可以打开的房间，打开后再把新得到的钥匙放回桌子**。  
只要还有新钥匙可以拿，就继续循环；循环结束后看是否已经访问了所有房间。

这种做法虽然能得到正确答案，但在最坏情况下会出现**重复检查**很多次，时间会呈二次增长（≈ O(n²)），因为每次循环都要遍历所有已经得到的钥匙。

#### 代码（Python）

```python
def canVisitAllRooms_bruteforce(rooms):
    n = len(rooms)                     # 房间总数
    visited = [False] * n              # visited[i] 表示第 i 间房间是否已经进入
    visited[0] = True                  # 只能先进入 0 号房间

    keys = set(rooms[0])               # 手里已有的钥匙集合（初始为 0 号房间里的钥匙）

    # 只要本轮循环中有新房间被打开，就继续
    changed = True
    while changed:
        changed = False
        # 把当前手里所有钥匙逐一尝试打开对应的房间
        for k in list(keys):           # list(keys) 防止在遍历时修改集合导致错误
            if not visited[k]:         # 该房间还没进去
                visited[k] = True      # 进入房间
                keys.update(rooms[k])  # 把新得到的钥匙加入手中
                changed = True        # 本轮有新进展，需要再继续循环

    # 所有房间都被访问到了才返回 True
    return all(visited)
```

#### 复杂度  

- **时间复杂度：O(n²)**  
  最坏情况下，每次循环只会打开一个新房间，需要循环 `n` 次；而每次循环会遍历当前手里所有钥匙，钥匙总数最多是 `n`（每个房间最多一把钥匙指向它自己），于是总操作次数约为 `n × n`，即二次方。  
  用大白话说，就是如果有 1000 个房间，最差情况下会做接近 **100万 次**的检查。

- **空间复杂度：O(n)**  
  需要 `visited` 数组和 `keys` 集合，大小都跟房间数成正比。  

---

### 2. 最优解

#### 思路  
从暴力解可以看出，**重复遍历**是瓶颈。  
实际上，这道题只需要 **一次完整的图遍历**（深度优先或广度优先）即可确定所有可达的房间。  

核心思路：

1. 把房间视作图的节点，钥匙视作有向边。  
2. 从节点 `0` 开始，用 **栈（DFS）或队列（BFS）** 把能到达的节点全部“走遍”。  
3. 走到一个房间时，把它的钥匙（即相邻的节点）全部加入待访问的集合。  
4. 只要一个节点已经访问过，就不再重复访问，避免二次检查。  

这正好对应 **“遍历所有可达节点”** 的经典算法——**深度优先搜索（DFS）**。  
下面用栈实现 DFS，并在每一步加入中文注释帮助理解。

> **类比**：把房间看成一张地图，钥匙是通往下一张地图的路径。DFS 就像把手中的地图摊开，一张接一张往里翻，翻过的地图就标记为“已经看过”，以后再也不翻。

#### 代码（Python）

```python
def canVisitAllRooms(rooms):
    """
    使用深度优先搜索（DFS）遍历所有可达的房间
    :param rooms: List[List[int]]，rooms[i] 表示进入第 i 间房间后可以拿到的钥匙列表
    :return: bool，是否能够访问所有房间
    """
    n = len(rooms)                     # 房间总数
    visited = [False] * n              # 记录每个房间是否已经进入
    stack = [0]                         # DFS 用的栈，先把 0 号房间压进去
    visited[0] = True                  # 0 号房间一定能进

    while stack:
        cur = stack.pop()               # 取出栈顶房间
        # 把当前房间里所有钥匙对应的房间加入待访问栈
        for nxt in rooms[cur]:
            if not visited[nxt]:        # 只处理还没进过的房间，防止重复
                visited[nxt] = True
                stack.append(nxt)       # 把新房间压入栈，后面继续遍历

    # 检查是否每个房间都被标记为已访问
    return all(visited)
```

#### 复杂度  

- **时间复杂度：O(n + e)**  
  这里的 `e` 是所有钥匙的总数（即图中所有有向边的数量）。  
  每个房间只会被压栈、弹栈一次，每把钥匙也只会被遍历一次，整体线性增长。  
  用大白话说，如果有 1000 间房间、3000 把钥匙，最多只会做 **约 4000 次**操作，远远小于二次方的 100 万次。

- **空间复杂度：O(n)**  
  需要 `visited` 数组（n 大小）和栈的最坏情况大小（最多存 n 个房间），整体仍然是线性空间。  

---

## 心得

- **核心技巧**：把“钥匙和房间”抽象成 **有向图**，使用 **深度优先搜索（或广度优先搜索）** 进行遍历。  
- **适用的题型**：  
  1. **岛屿数量**（Number of Islands）——用 DFS/BFS 统计连通块。  
  2. **课程表**（Course Schedule）——判断有向图是否存在环，亦可用 DFS。  
  3. **好友关系**（Friend Circles）——同样是图的连通分量问题。  
- **一句话总结**：**“把钥匙视作边，遍历所有可达节点，就能判断是否能进入所有房间”。**

---

## 反思

- **第一反应**：把每个房间想成一个点，钥匙想成指向其他点的箭头，需要把所有能到达的点走遍。  
- **最容易踩的坑**：  
  - 忘记对已经访问过的房间做标记，导致无限循环或重复计数。  
  - 把 `rooms[i]` 当成二维数组的固定大小，实际上每个列表长度不同，需要使用 `for nxt in rooms[cur]` 迭代。  
  - 对极端输入（如所有钥匙都指向同一个房间）没有做好边界检查。  
- **下次类似题的第一步**：先 **抽象成图**（节点 + 边），判断是**连通性**还是**路径**问题，然后选用 **DFS/BFS** 进行一次完整遍历。