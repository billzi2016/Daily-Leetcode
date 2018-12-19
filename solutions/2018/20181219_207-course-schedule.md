# #207. 课程安排 / Course Schedule

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/course-schedule/)

---

## 题目（英文原版）

**Description**

There are a total of numCourses courses you have to take, labeled from 0 to numCourses - 1. You are given an array prerequisites where prerequisites[i] = [ai, bi] indicates that you must take course bi first if you want to take course ai.
Return true if you can finish all courses. Otherwise, return false.

**Examples**

**Example 1:**

```
Input: numCourses = 2, prerequisites = [[1,0]]
Output: true
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.
```

**Example 2:**

```
Input: numCourses = 2, prerequisites = [[1,0],[0,1]]
Output: false
Explanation: There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.
```

**Constraints**

- 1 <= numCourses <= 2000
- 0 <= prerequisites.length <= 5000
- prerequisites[i].length == 2
- 0 <= ai, bi < numCourses
- All the pairs prerequisites[i] are unique.

---

## 题目（中文翻译）

**题目描述**  
共有 `numCourses` 门课程需要学习，课程编号为 `0` 到 `numCourses - 1`。给定一个数组 `prerequisites`，其中 `prerequisites[i] = [ai, bi]` 表示如果想选修课程 `ai`，必须先修完课程 `bi`。  
返回 `true` 表示可以完成所有课程的学习，否则返回 `false`。

**示例 1**  
**示例 2**  
（此处省略原题中的示例标题，仅保留原始输入/输出）

**约束条件**  

- `1 <= numCourses <= 2000`
- `0 <= prerequisites.length <= 5000`
- `prerequisites[i].length == 2`
- `0 <= ai, bi < numCourses`
- 所有 `prerequisites[i]` 对均唯一  

**示例**

> **示例 1**  
> **输入**: `numCourses = 2, prerequisites = [[1,0]]`  
> **输出**: `true`  
> **解释**: 总共有 2 门课程需要学习。要选修课程 1，必须先完成课程 0。因此可以完成所有课程。

> **示例 2**  
> **输入**: `numCourses = 2, prerequisites = [[1,0],[0,1]]`  
> **输出**: `false`  
> **解释**: 总共有 2 门课程需要学习。要选修课程 1，必须先完成课程 0；而要选修课程 0，又必须先完成课程 1。出现循环依赖，无法完成所有课程。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把所有课程的可能学习顺序全部枚举出来**，然后检查每一种顺序是否满足所有先修关系。  
- **数据结构**：我们可以把课程的顺序存放在一个列表 `order` 中，先修关系 `prerequisites` 用二维数组保存。  
- **生活化类比**：把课程想象成一排不同颜色的积木，先修关系就是“红色积木必须放在蓝色积木左边”。暴力做法就是把所有积木随意排成一行，然后逐个检查“红左蓝右”是否成立。  
- **为什么正确**：只要我们把**所有**可能的排列都尝试一遍，肯定能找到一条满足所有约束的排列（如果存在的话），或者遍历完仍未找到，说明根本没有合法的学习顺序。  

显然，这种做法在课程数目稍大时就会爆炸。  
- **时间复杂度**：枚举 `n` 门课的全排列需要 `O(n!)`（阶乘）次尝试。每次检查所有先修关系需要 `O(E)`（`E` 为先修对的数量），整体是 `O(n!·E)`。  
  - 大白话：如果有 10 门课，`10! = 3,628,800`，几乎不可能在一秒内算完。  
- **空间复杂度**：递归过程中保存当前排列需要 `O(n)`，加上存放先修关系的 `O(E)`，总体 `O(n + E)`。

#### 代码（Python）  
```python
from itertools import permutations
from typing import List

def canFinish_brute(numCourses: int, prerequisites: List[List[int]]) -> bool:
    # 把所有先修关系装进集合，方便 O(1) 查找
    pre_set = { (a, b) for a, b in prerequisites }   # (课程, 必须在前的课程)

    # 枚举所有课程的排列
    for order in permutations(range(numCourses)):
        # 用一个字典记录每门课在排列中的下标，方便快速判断先后顺序
        pos = { course: idx for idx, course in enumerate(order) }
        ok = True
        # 检查每条先修关系是否满足：b 必须出现在 a 的左边
        for a, b in pre_set:
            if pos[b] > pos[a]:        # b 出现在 a 的右边，违背要求
                ok = False
                break
        if ok:                         # 找到一种合法顺序，直接返回 True
            return True
    # 所有排列都不合法
    return False
```

#### 复杂度  
- **时间复杂度**：`O(n!·E)` —— 随着课程数目 `n` 增长，计算量会呈阶乘级别爆炸。  
- **空间复杂度**：`O(n + E)` —— 只需要存放当前排列和先修关系集合。

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在于**枚举所有排列**。实际上，我们只需要判断“是否存在环”即可，因为：

- 先修关系把课程看成**有向图**（`b → a` 表示学完 `b` 后才能学 `a`）。  
- 如果这个有向图**没有环**，就可以把所有节点进行**拓扑排序**，得到一种合法的学习顺序。  
- 只要图里出现环（循环依赖），无论怎么排都不可能满足所有先修要求。

因此，核心任务是**检测有向图是否有环**。常用的两种线性时间算法：

1. **DFS（深度优先搜索）+ 三色标记**：在遍历时记录节点的“状态”，如果在当前递归栈中再次访问到正在访问的节点，说明出现环。  
2. **Kahn 算法（BFS）**：利用**入度**（指向该节点的边数）。每次把入度为 0 的节点取出（表示它已经没有未完成的前置课程），并把它的出边删掉，更新相邻节点的入度。若最终所有节点都被取出，则无环；否则剩下的节点形成环。

下面用 **Kahn 算法**（BFS）实现，因为思路直观、代码简洁，且只需要 `O(V+E)` 的时间和 `O(V+E)` 的空间。

- **数据结构类比**：  
  - **邻接表**：把每门课的后续课程装进一个列表，类似“每本教材的后续章节”。  
  - **入度数组**：把每门课需要先修的课程数记下来，像“每道菜需要的前置配料数量”。  
  - **队列**：装入度为 0 的课程，类似“已经准备好的配料”，可以立即烹饪。

#### 代码（Python）  
```python
from collections import deque
from typing import List

def canFinish(numCourses: int, prerequisites: List[List[int]]) -> bool:
    # 1. 建图（邻接表）并计算每个节点的入度
    graph = [[] for _ in range(numCourses)]   # graph[u] = [v1, v2, ...] 表示 u → v
    indegree = [0] * numCourses                # indegree[v] = 有多少条边指向 v

    for a, b in prerequisites:                 # 先修关系 b → a
        graph[b].append(a)
        indegree[a] += 1

    # 2. 把所有入度为 0 的课程放进队列
    q = deque([i for i in range(numCourses) if indegree[i] == 0])
    visited = 0                                 # 记录已经“学完”的课程数

    # 3. BFS：一次取出一个入度为 0 的课程，视作已经完成
    while q:
        cur = q.popleft()
        visited += 1                            # 这门课算完成

        # 把 cur 的所有后续课程的入度减 1
        for nxt in graph[cur]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:              # 入度降为 0，说明它的前置课都已经完成
                q.append(nxt)

    # 4. 若所有课程都被访问过，说明没有环；否则剩余的课程形成环
    return visited == numCourses
```

#### 复杂度  
- **时间复杂度**：`O(V + E)`，其中 `V = numCourses`（课程数），`E = len(prerequisites)`（先修关系数）。  
  - 大白话：我们只遍历一次所有课程和所有先修关系，线性时间非常快。  
- **空间复杂度**：`O(V + E)`，用于存放邻接表、入度数组和队列。  

与暴力解相比，时间从不可接受的阶乘级别降到了线性级别，几乎可以处理最大输入（2000 门课、5000 条先修关系）而不会超时。

---

## 心得  

- **核心技巧**：把课程的先修关系抽象成**有向图**，判断是否**存在环**。  
- **适用的题型**：  
  1. **Course Schedule II**（返回具体的学习顺序）。  
  2. **Alien Dictionary**（根据字典序判断字母的相对顺序）。  
  3. **Semesters Required**（计算完成所有课程最少的学期数）。  
- **一句话总结解题钥匙**：**“有环则不可能，无环则可以”。**只要能在有向图中找到环，就说明任务无法完成。

---

## 反思  

- **第一反应**：看到“先修课程”立刻联想到**拓扑排序**，因为它正是用来处理有向无环图（DAG）的问题。  
- **最容易踩的坑**：  
  - **遗漏孤立节点**：即没有任何先修或后续关系的课程，也要计入 `numCourses`。  
  - **入度计数错误**：先修关系是 `b → a`（先上 `b` 再上 `a`），记得在构图时把方向写对。  
  - **多余的边**：同一对先修关系不会重复出现，但若手动构图时不去重，入度会被错误累加。  
- **下次遇到同类题**：第一步先**把问题抽象成有向图**，然后**检查是否有环**（可以先用 DFS 快速判断，若需要顺序再用 BFS/Kahn）。