# #210. 课程表 II / Course Schedule II

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/course-schedule-ii/)

---

## 题目（英文原版）

**Description**

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
Return the ordering of courses you should take to finish all courses. If there are many valid answers, return any of them. If it is impossible to finish all courses, return an empty array.

**Examples**

**Example 1:**

```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: [0,1]
Explanation: There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].
```

**Example 2:**

```
Input: numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
Output: [0,2,1,3]
Explanation: There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].
```

**Example 3:**

```
Input: numCourses = 1, prerequisites = []
Output: [0]
```

**Constraints**

- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= numCourses * (numCourses - 1)
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- ai != bi
- All the pairs [ai, bi] are distinct.

---

## 题目（中文翻译）

给定 **numCourses** 门课程，编号为 `0` 到 `numCourses - 1`。另有一个数组 **prerequisites**，其中 `prerequisites[i] = [a_i, b_i]` 表示如果想修读课程 `a_i`，必须先修完课程 `b_i`（先修课程，prerequisites）。  
返回一种可以完成所有课程的学习顺序。如果存在多种合法顺序，返回任意一种；如果无法完成所有课程，则返回空数组。

## 示例

### 示例 1
**输入**: `numCourses = 2`, `prerequisites = [[1,0]]`  
**输出**: `[0,1]`  
**解释**: 共有 2 门课程。要修读课程 `1`，必须先完成课程 `0`。因此正确的课程顺序是 `[0,1]`。

### 示例 2
**输入**: `numCourses = 4`, `prerequisites = [[1,0],[2,0],[3,1],[3,2]]`  
**输出**: `[0,2,1,3]`  
**解释**: 共有 4 门课程。要修读课程 `3`，必须先完成课程 `1` 和 `2`。课程 `1`、`2` 都应在完成课程 `0` 之后修读。  
一种合法的课程顺序是 `[0,1,2,3]`，另一种合法顺序是 `[0,2,1,3]`。

### 示例 3
**输入**: `numCourses = 1`, `prerequisites = []`  
**输出**: `[0]`

## 约束条件
- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= numCourses * (numCourses - 1)`
- `prerequisites[i].length == 2`
- `0 <= a_i, b_i < numCourses`
- `a_i != b_i`
- 所有的 `[a_i, b_i]` 对均不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把所有课程的排列全枚举出来**，然后逐个检查这条排列是否满足所有先修关系。  
- **枚举排列**：可以把课程看成一副扑克牌，`[0,1,2,…,numCourses‑1]` 是一副牌的原始顺序。我们把这副牌的所有可能洗牌方式（即全排列）都列出来。  
- **检查先修关系**：先修关系 `prerequisites[i] = [a, b]` 就像字典里的“词条”。`b` 是“词”，`a` 是“页码”。如果在某个排列里，`a` 出现在 `b` 前面，那么这条先修关系就被违背了。只要所有的先修关系都满足，当前排列就是一个合法的上课顺序。  

这种方法一定能得到答案，因为我们穷举了 **所有** 可能的顺序。只要存在合法顺序，它一定会被枚举到；如果所有顺序都不合法，就返回空数组。

#### 代码（Python）

```python
import itertools
from typing import List

def findOrder_bruteforce(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    # 1. 把所有课程的全排列生成出来（等价于把 0~numCourses-1 洗牌）
    for order in itertools.permutations(range(numCourses)):
        # 2. 用一个字典记录每门课在当前排列中的下标，类似 “词典”
        pos = {course: idx for idx, course in enumerate(order)}
        # 3. 检查所有先修关系是否满足
        valid = True
        for a, b in prerequisites:               # a 需要在 b 之后
            if pos[a] < pos[b]:                  # a 出现在 b 前面 → 违背先修
                valid = False
                break
        if valid:                                 # 找到第一个合法顺序直接返回
            return list(order)
    # 4. 没有任何合法顺序，说明出现环，返回空列表
    return []
```

#### 复杂度

- **时间复杂度**：`O(n! * (n + m))`  
  - `n!` 是所有排列的数量（`n = numCourses`），每个排列我们要遍历一次所有课程（`O(n)`）建立位置表，再检查 `m` 条先修关系（`m = len(prerequisites)`）。  
  - 用大白话说，就是“先把所有可能的排队方式都尝试一遍”，当课程数稍大时，这个方法会非常慢，几乎不可用。

- **空间复杂度**：`O(n)`  
  - 只需要存放当前排列的 `pos` 字典以及递归生成排列时的临时空间，和课程数成正比。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于 **枚举所有排列**，这一步的时间指数级增长。实际上，这道题等价于在 **有向图** 中寻找 **拓扑序**（Topological Order）：

- 把每门课程看成图的一个节点。  
- 先修关系 `[a, b]` 表示一条有向边 `b → a`（先上 `b`，再上 `a`）。  
- 拓扑序就是一种线性排序，使得所有的有向边都从前指向后。  
- 如果图里出现环（循环依赖），则根本不存在拓扑序，答案为空。

**核心优化**：直接在图上做排序，而不是枚举所有排列。常用的两种算法：

1. **DFS + 逆后序**（深度优先搜索）：在遍历时把节点加入结果列表的时机恰好是「所有后继都已经访问完」的时候。  
2. **Kahn 算法（BFS）**：利用**入度**（incoming degree）——指向该节点的边数。每次挑选入度为 0 的节点（意味着它没有未完成的前置课程），放入答案并删除它的出边，循环直到所有节点处理完或出现环。

这里用 **Kahn 算法**（BFS 版）实现，因为它直观且易于解释。

**关键概念解释**  

- **入度（Indegree）**：想象每门课都有一张“待完成的前置课程清单”。清单上有多少条未完成的前置课，就说这门课的入度是多少。  
- **队列（Queue）**：把所有“清单为空”的课程（入度为 0）排成一队，按顺序上课。  
- **拓扑排序**：把课程按照“先把没有依赖的上完，再把依赖它们的上完”的顺序排成一列。

**步骤**  

1. **建图 + 统计入度**  
   - 用邻接表 `graph[b].append(a)` 表示 `b → a`。  
   - 同时维护 `indeg[a]`，记录每门课的前置课数量。  

2. **初始化队列**  
   - 把所有 `indeg[i] == 0` 的课程加入队列。它们可以立刻开始。  

3. **BFS 拓扑遍历**  
   - 从队列里弹出一个课程 `u`，放入答案列表。  
   - 对 `u` 的每个后继 `v`，把 `indeg[v]` 减 1（相当于“完成了 `u` 这门前置课”）。  
   - 如果 `indeg[v]` 变成 0，说明 `v` 的所有前置课都已经上完，加入队列。  

4. **判断是否有环**  
   - 最终答案长度若等于 `numCourses`，说明所有课程都被安排了，返回答案。  
   - 否则说明图中还有未被处理的节点（入度永远大于 0），必然存在环，返回空列表。

#### 代码（Python）

```python
from collections import deque
from typing import List

def findOrder(numCourses: int, prerequisites: List[List[int]]) -> List[int]:
    # 1️⃣ 建立邻接表（图）和入度数组
    graph = [[] for _ in range(numCourses)]      # graph[u] = 所有从 u 出发的后继课程
    indeg = [0] * numCourses                     # indeg[v] = v 的前置课程数量

    for a, b in prerequisites:                   # b -> a
        graph[b].append(a)
        indeg[a] += 1

    # 2️⃣ 把所有入度为 0 的课程放进队列
    q = deque([i for i in range(numCourses) if indeg[i] == 0])

    order = []                                    # 用来存放拓扑序

    # 3️⃣ BFS 取出队首课程，更新后继的入度
    while q:
        u = q.popleft()                           # 取出当前可以上的课程
        order.append(u)                           # 记录到答案里

        for v in graph[u]:                       # 遍历 u 的所有后继课程
            indeg[v] -= 1                         # 完成了 u，v 的待完成前置课数减 1
            if indeg[v] == 0:                     # 若全部前置课都完成，加入队列
                q.append(v)

    # 4️⃣ 检查是否出现环
    if len(order) == numCourses:
        return order
    else:                                          # 有环，无法完成所有课程
        return []
```

#### 复杂度

- **时间复杂度**：`O(V + E)`  
  - `V = numCourses` 是节点数，`E = len(prerequisites)` 是边数。  
  - 我们只遍历一次所有节点（加入队列）和所有边（更新入度），没有重复工作。  
  - 用大白话说，就是“只看一遍所有课程和所有先修关系”，比暴力的 `n!` 快很多。

- **空间复杂度**：`O(V + E)`  
  - 邻接表存放所有边，需要 `E` 的空间；入度数组和队列各占 `V` 的空间。  
  - 同样是线性空间，和输入规模成正比。

---

## 心得

- **核心技巧**：**拓扑排序**（Topological Sort），特别是 **Kahn 的 BFS 实现**。  
- **适用题型**  
  1. 课程安排类（Course Schedule 系列）  
  2. 任务调度 / 先后顺序问题（如“项目计划”）  
  3. 依赖关系检测（如“编译顺序”）  

> **一句话总结解题钥匙**：把先修关系看成有向图，用“入度为 0 的课程先上” 的规则一次遍历即可得到合法顺序，若遍历不到所有课程说明有环，返回空。

---

## 反思

- **第一反应**：看到“先修关系”，马上想到图和拓扑排序；如果没有想到，可能会先尝试递归或回溯。  
- **最容易踩的坑**  
  - **环检测**：忘记在遍历结束后检查答案长度，导致返回了不完整的顺序。  
  - **入度初始化**：把 `[a, b]` 当成 `a -> b` 写反，导致入度统计错误。  
  - **特殊情况**：`prerequisites` 为空时，所有课程都是入度 0，需要直接返回 `[0,1,...]`。  

- **下次类似题的第一步**：先把问题抽象成 **有向图 + 入度**，判断是否需要 **拓扑排序**（若要求输出顺序）或仅判断 **是否有环**（若只要可行性）。这样思路就已经锁定了最优解的方向。