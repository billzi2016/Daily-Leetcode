# #3310. 从项目中移除方法 / Remove Methods From Project

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/remove-methods-from-project/)

---

## 题目（英文原版）

**Description**

You are maintaining a project that has n methods numbered from 0 to n - 1.
You are given two integers n and k, and a 2D integer array invocations, where invocations[i] = [ai, bi] indicates that method ai invokes method bi.
There is a known bug in method k. Method k, along with any method invoked by it, either directly or indirectly, are considered suspicious and we aim to remove them.
A group of methods can only be removed if no method outside the group invokes any methods within it.
Return an array containing all the remaining methods after removing all the suspicious methods. You may return the answer in any order. If it is not possible to remove all the suspicious methods, none should be removed.

**Examples**

**Example 1:**

```
Input: n = 4, k = 1, invocations = [[1,2],[0,1],[3,2]]
Output: [0,1,2,3]
Explanation:

Method 2 and method 1 are suspicious, but they are directly invoked by methods 3 and 0, which are not suspicious. We return all elements without removing anything.
```

**Example 2:**

```
Input: n = 5, k = 0, invocations = [[1,2],[0,2],[0,1],[3,4]]
Output: [3,4]
Explanation:

Methods 0, 1, and 2 are suspicious and they are not directly invoked by any other method. We can remove them.
```

**Example 3:**

```
Input: n = 3, k = 2, invocations = [[1,2],[0,1],[2,0]]
Output: []
Explanation:

All methods are suspicious. We can remove them.
```

**Constraints**

- 1 <= n <= 105
- 0 <= k <= n - 1
- 0 <= invocations.length <= 2 * 105
- invocations[i] == [ai, bi]
- 0 <= ai, bi <= n - 1
- ai != bi
- invocations[i] != invocations[j]

---

## 题目（中文翻译）

你正在维护一个包含 n 个方法（编号从 0 到 n‑1）的项目。  
给定整数 n、k，以及一个二维整数数组 invocations，其中 `invocations[i] = [ai, bi]` 表示方法 ai 调用方法 bi。  

方法 k 存在已知缺陷。方法 k 以及所有被它直接或间接调用的方法都被视为可疑，我们需要将它们移除。  
只有当组内的所有方法都不被组外的任何方法调用时，才能将该组方法整体移除。  

返回在移除所有可疑方法后剩余的方法编号数组，答案可以按任意顺序返回。如果无法一次性移除所有可疑方法，则不应移除任何方法。

**示例 1:**  
**示例 2:**  
**示例 3:**  

**约束条件**  
- 1 ≤ n ≤ 10⁵  
- 0 ≤ k ≤ n‑1  
- 0 ≤ invocations.length ≤ 2·10⁵  
- invocations[i] == [ai, bi]  
- 0 ≤ ai, bi ≤ n‑1  
- ai ≠ bi  
- invocations[i] ≠ invocations[j]  

**示例**  

**示例 1:**  
```text
Input: n = 4, k = 1, invocations = [[1,2],[0,1],[3,2]]
Output: [0,1,2,3]
```
**解释:**  
方法 2 和方法 1 为可疑方法，但它们分别被方法 3 和方法 0 直接调用，而这两个方法本身并不可疑。因此无法满足“组外方法不调用组内方法”的条件，故不移除任何方法，返回全部元素。

**示例 2:**  
```text
Input: n = 5, k = 0, invocations = [[1,2],[0,2],[0,1],[3,4]]
Output: [3,4]
```
**解释:**  
方法 0、1、2 均为可疑方法，并且它们没有被任何其他方法直接调用。满足移除条件，可以将这三个方法全部删除，剩余方法为 3 和 4。

**示例 3:**  
```text
Input: n = 3, k = 2, invocations = [[1,2],[0,1],[2,0]]
Output: []
```
**解释:**  
所有方法均为可疑方法且相互调用。满足条件，可一次性将全部方法移除，返回空数组。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

先把 **“可疑的方法”** 想成“被病毒感染的文件”。  
- 方法 `k` 本身是病毒源头，它直接或间接 **调用**（相当于“传染”）的所有方法都是可疑的。  
- 我们可以用 **深度优先搜索（DFS）** 从 `k` 出发，把所有能走到的节点全部标记为 “被感染”。这一步就像在病毒图谱里把所有被感染的文件找出来。

接下来要判断 **能否把这些被感染的文件一起删除**。  
删除的前提是：**没有任何外部文件（不在感染集合里）依赖（调用）这些被感染的文件**。  
如果有外部文件指向感染集合中的某个文件，就好比外部文件的快捷方式指向了病毒文件，直接删掉会导致系统崩溃——因此整套文件都不能删。

暴力的做法是：

1. 用 DFS 找出所有被感染的节点 `R`（包括 `k` 本身）。  
2. 对于 **每一个** 不在 `R` 的节点 `u`，再 **一次一次** 做 DFS，看看它能否到达 `R` 中的任意节点。  
   - 只要找到一次 `u → v（v∈R）`，就说明 `u` 依赖了被感染的代码，整套都不能删。  
3. 如果所有外部节点都 **不能** 触及 `R`，则把 `R` 全部删除，返回剩余的节点集合。

> 这里把“检查是否有外部调用”拆成了 **对每个外部节点单独 DFS**，所以会非常慢。

#### 代码（Python）

```python
def remainingMethods_bruteforce(n: int, k: int, invocations):
    # 建立邻接表（有向图）
    graph = [[] for _ in range(n)]
    for a, b in invocations:
        graph[a].append(b)

    # 1️⃣ 找出所有被感染的节点 R
    R = set()
    stack = [k]
    while stack:
        node = stack.pop()
        if node in R:
            continue
        R.add(node)                     # 标记为“被感染”
        stack.extend(graph[node])       # 继续往下走

    # 2️⃣ 对每个不在 R 的节点，检查它能否到达 R
    def dfs(u, visited):
        """普通的 DFS，返回是否能碰到 R 中的节点"""
        if u in R:                     # 直接进入感染集合
            return True
        visited.add(u)
        for v in graph[u]:
            if v not in visited and dfs(v, visited):
                return True
        return False

    for u in range(n):
        if u in R:
            continue                    # 跳过已经感染的节点
        if dfs(u, set()):               # 只要一次能碰到 R，就失败
            return list(range(n))       # 不能删除，返回全部

    # 3️⃣ 没有外部依赖，删除 R，返回剩余
    return [i for i in range(n) if i not in R]
```

#### 复杂度  

- **时间复杂度**：`O(n * (n + m))`  
  - 找到 R 只要 `O(n + m)`，但对每个外部节点又要一次完整的 DFS，最坏情况下会遍历整个图 `n` 次，等价于 `n` 倍的图规模。  
  - 用“大白话”说，就是 **“每个人都要去检查一次全城的地图”**，显然太慢了。  
- **空间复杂度**：`O(n + m)`  
  - 用到了邻接表和递归栈（或显式栈），随图的规模线性增长。

---

### 2. 最优解

#### 思路  

从暴力解我们已经知道两个关键点：

1. **找出可疑集合 `R`**：从 `k` 出发的所有可达节点。  
2. **判断是否可以删除**：只要**外部没有指向 `R` 的边**，就可以安全删除。

暴力解慢的根源在于 **第二步**：我们对每个外部节点都跑一次 DFS，等价于把同一条边检查了很多遍。  
其实我们只需要 **一次遍历所有边**，直接看有没有 “外部 → R” 的边即可。

实现步骤：

1. **一次 DFS / BFS**（这里用 DFS）得到可疑集合 `R`。  
2. **遍历所有调用关系 `invocations`**：  
   - 若边 `(a, b)` 满足 `b ∈ R` 且 `a ∉ R`，说明有外部调用，**整套都不能删**，直接返回全部方法。  
3. 如果遍历结束都没有发现上述边，说明 `R` 与外部完全隔离。此时可以把 `R` 全部删除，返回 `0 … n‑1` 中不在 `R` 的节点。

> 把 “外部调用” 的检查压缩成一次遍历，就像只需要 **一次** 看完所有信件的收件人，就能判断是否有寄往 “被封锁的地址”。  

#### 代码（Python）

```python
def remainingMethods(n: int, k: int, invocations):
    """
    返回在安全删除所有可疑方法后剩余的方法编号列表。
    若无法安全删除，则返回全部方法（即不删除任何东西）。
    """
    # 1️⃣ 建立邻接表（有向图）
    graph = [[] for _ in range(n)]
    for a, b in invocations:
        graph[a].append(b)

    # 2️⃣ DFS 找到所有从 k 可达的节点（可疑集合 R）
    suspicious = set()
    stack = [k]
    while stack:
        node = stack.pop()
        if node in suspicious:
            continue
        suspicious.add(node)           # 标记为“可疑”
        stack.extend(graph[node])       # 继续往下走

    # 3️⃣ 检查是否有外部 → R 的边
    for a, b in invocations:
        if b in suspicious and a not in suspicious:
            # 有外部方法调用了可疑方法，不能删除任何东西
            return list(range(n))

    # 4️⃣ 没有外部依赖，删除 R，返回剩余方法
    return [i for i in range(n) if i not in suspicious]
```

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 一次 DFS 遍历所有节点和边得到 `R`（`O(n + m)`）。  
  - 再一次线性扫描 `invocations` 检查外部边（同样 `O(m)`）。整体线性，**比暴力解快了好几个数量级**。  
- **空间复杂度**：`O(n + m)`  
  - 邻接表占 `O(n + m)`，DFS 栈/集合占 `O(n)`，总体仍然随图规模线性。

---

## 心得

- **核心技巧**：**一次遍历找出可疑子图 + 检查外部入度**。  
- 该技巧常用于 **“删除满足某种隔离条件的节点/子图”**，比如：  
  1. **Remove Nodes From Graph**（LeetCode 1847），判断是否能删除所有入度为 0 的节点。  
  2. **Kill Process**（LeetCode 582），找出被杀死的进程及其子进程。  
  3. **Find Eventual Safe States**（LeetCode 802），利用逆向边判断安全节点。  
- **一句话总结**：**只要一次遍历把可疑集合找出来，再一次遍历检查是否有外部进入的边，就能决定是否可以安全删除**。

## 反思

- **拿到题目第一反应**：先想到“从 k 出发做遍历”，因为“直接或间接调用”自然对应图的可达性。  
- **最容易踩的坑**  
  - 忘记把 `k` 本身也算进可疑集合。  
  - 只检查 “`k` 的直接邻居是否被外部调用”，而忽略了更深层的节点可能也会被外部调用。  
  - 当所有方法都是可疑时，仍然需要返回空列表而不是全部。  
- **下次遇到同类题**：第一步先 **确定“目标子图”**（如从某节点可达的全部），第二步 **只要一次遍历检查外部入度**，而不是对每个外部节点单独搜索。这样可以把时间从指数级/平方级压到线性级。