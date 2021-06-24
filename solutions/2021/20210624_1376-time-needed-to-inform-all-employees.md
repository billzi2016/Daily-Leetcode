# #1376. 通知所有员工所需的时间 / Time Needed to Inform All Employees

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search · [LeetCode 链接](https://leetcode.com/problems/time-needed-to-inform-all-employees/)

---

## 题目（英文原版）

**Description**

A company has n employees with a unique ID for each employee from 0 to n - 1. The head of the company is the one with headID.
Each employee has one direct manager given in the manager array where manager[i] is the direct manager of the i-th employee, manager[headID] = -1. Also, it is guaranteed that the subordination relationships have a tree structure.
The head of the company wants to inform all the company employees of an urgent piece of news. He will inform his direct subordinates, and they will inform their subordinates, and so on until all employees know about the urgent news.
The i-th employee needs informTime[i] minutes to inform all of his direct subordinates (i.e., After informTime[i] minutes, all his direct subordinates can start spreading the news).
Return the number of minutes needed to inform all the employees about the urgent news.

**Examples**

**Example 1:**

```
Input: n = 1, headID = 0, manager = [-1], informTime = [0]
Output: 0
Explanation: The head of the company is the only employee in the company.
```

**Example 2:**

```
Input: n = 6, headID = 2, manager = [2,2,-1,2,2,2], informTime = [0,0,1,0,0,0]
Output: 1
Explanation: The head of the company with id = 2 is the direct manager of all the employees in the company and needs 1 minute to inform them all.
The tree structure of the employees in the company is shown.
```

**Constraints**

- 1 <= n <= 105
- 0 <= headID < n
- manager.length == n
- 0 <= manager[i] < n
- manager[headID] == -1
- informTime.length == n
- 0 <= informTime[i] <= 1000
- informTime[i] == 0 if employee i has no subordinates.
- It is guaranteed that all the employees can be informed.

---

## 题目（中文翻译）

**题目描述**  
一家公司有 `n` 名员工，员工的 ID 为 `0` 到 `n‑1`（唯一）。公司负责人（head）为 `headID`。  
每位员工都有唯一的直接上司，存于数组 `manager` 中，其中 `manager[i]` 表示第 `i` 名员工的直接上司，且 `manager[headID] = -1`。已保证上下级关系形成一棵树结构。  

公司负责人需要将一条紧急消息通知所有员工。他会先通知自己的直接下属，随后这些下属再通知他们的下属，依此类推，直至所有员工都获知消息。  
第 `i` 名员工需要 `informTime[i]` 分钟来通知所有直接下属（即在 `informTime[i]` 分钟后，他的所有直接下属即可开始传播消息）。  

请返回将紧急消息传达到所有员工所需的总分钟数。

**示例 1**  
```text
Input: n = 1, headID = 0, manager = [-1], informTime = [0]
Output: 0
Explanation: 公司负责人就是公司唯一的员工。
```

**示例 2**  
```text
Input: n = 6, headID = 2, manager = [2,2,-1,2,2,2], informTime = [0,0,1,0,0,0]
Output: 1
Explanation: ID 为 2 的负责人是公司所有员工的直接上司，通知所有人只需要 1 分钟。
```
（题目中给出了公司员工的树形结构示意图。）

**约束条件**  
- `1 <= n <= 10^5`  
- `0 <= headID < n`  
- `manager.length == n`  
- `0 <= manager[i] < n`  
- `manager[headID] == -1`  
- `informTime.length == n`  
- `0 <= informTime[i] <= 1000`  
- 若员工 `i` 没有下属，则 `informTime[i] == 0`  
- 已保证所有员工都能被通知到。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每个员工，沿着管理链一直往上找到公司总裁（headID）**，把沿途的 `informTime` 加起来，就是这位员工收到消息的时间。  
- `manager` 数组就像一本“谁是我上司”的字典，`manager[i]` 是员工 `i` 的直接上司。  
- `informTime[i]` 是这位上司把消息转发给自己的下属们需要的时间，类似于“从办公室 A 打电话到办公室 B 需要的分钟数”。  

把每位员工的“上司链”全部走一遍，找出最大的累计时间，就是所有员工都收到消息所需的最久时间。  

为什么它是正确的？  
- 每条链条都是唯一的（题目保证是树结构），所以从员工到总裁的路径唯一。  
- 信息的传播顺序正好是沿着这条唯一路径从上往下进行，累计时间就是这条路径上所有 `informTime` 的和。  

#### 代码（Python）  

```python
def numOfMinutes_bruteforce(n, headID, manager, informTime):
    # 保存每个员工收到消息的时间，初始为 -1 表示还没算过
    time_to_inform = [-1] * n

    # 对每个员工都走一遍向上的管理链
    for emp in range(n):
        total = 0            # 累计时间
        cur = emp
        # 一直往上找，直到根节点（headID）或已经算好的节点
        while cur != headID and time_to_inform[cur] == -1:
            # 把当前员工的上司的 informTime 加进去
            total += informTime[manager[cur]]
            cur = manager[cur]   # 向上跳到上司

        # 如果已经算出 cur 的时间，就可以直接累加
        if time_to_inform[cur] != -1:
            total += time_to_inform[cur]

        # 把累计结果写回
        time_to_inform[emp] = total

    # 所有员工中最大的时间就是答案
    return max(time_to_inform)
```

**关键注释**  
- `while cur != headID and time_to_inform[cur] == -1`：不停往上走，直到碰到根或者已经算好的节点，避免重复计算。  
- `total += informTime[manager[cur]]`：把当前员工的 **直接上司** 需要的转发时间加进去。  
- 最后 `max(time_to_inform)`：找出最慢的那个人，就是全公司通知完的时间。  

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 最坏情况下，每个员工都要从自己一直走到根，路径长度可能是 `n`，于是总操作数是 `n × n`。  
  - 用大白话说，就是如果公司有 10,000 人，最坏要做 10,000 × 10,000 = 1 亿次循环，显然会慢。  
- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的数组 `time_to_inform` 来存每个人的累计时间。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到，**瓶颈在于重复遍历同一条管理链**。  
- 当我们已经算出某个员工的通知时间后，所有它的下属都可以直接使用这个结果，而不必再从头往上走。  

这正好可以用 **树的深度优先遍历（DFS）** 或 **广度优先遍历（BFS）** 一次性把所有路径的累计时间算出来。  

核心思路如下：  

1. **把公司结构转成邻接表**（孩子列表）。  
   - `manager[i] = p` 表示 `p` 是 `i` 的上司，等价于在 `p` 的孩子列表里加入 `i`。  
   - 这就像把“谁是我老板”这本字典倒过来，变成“我有哪些下属”。  

2. **从根节点（headID）开始递归**，把已经花掉的时间传给子节点。  
   - 对当前节点 `u`，它已经花了 `elapsed` 分钟收到消息。  
   - 再加上 `informTime[u]`，子节点们才能开始传播。  
   - 对每个子节点 `v`，递归调用 `dfs(v, elapsed + informTime[u])`。  

3. **叶子节点（没有下属）不再继续**，它们的累计时间就是一条完整路径的耗时。  
   - 记录所有叶子节点的 `elapsed`，取最大值即为答案。  

这样每条边只会被访问一次，时间是线性的。  

#### 代码（Python）  

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)      # 防止递归层数太深导致 RecursionError

def numOfMinutes_optimal(n, headID, manager, informTime):
    # 1. 建立“上司 → 下属” 的邻接表
    subordinates = defaultdict(list)          # key: 上司, value: 直接下属列表
    for emp in range(n):
        mgr = manager[emp]
        if mgr != -1:                          # -1 表示根节点（headID）
            subordinates[mgr].append(emp)

    # 2. 深度优先搜索，返回从当前节点出发的最大耗时
    def dfs(cur, elapsed):
        """
        cur: 当前员工编号
        elapsed: 从根到 cur 已经用了多少分钟（cur 已经收到消息的时间）
        """
        # 如果没有下属了，cur 就是叶子，返回它的累计时间
        if not subordinates[cur]:
            return elapsed

        # 否则遍历所有下属，取最大的那条路径的耗时
        max_time = 0
        for child in subordinates[cur]:
            # 子节点的起始时间 = 当前节点的累计时间 + 当前节点的 informTime
            child_time = dfs(child, elapsed + informTime[cur])
            max_time = max(max_time, child_time)
        return max_time

    # 3. 从根节点（headID）开始，起始已经用了 0 分钟
    return dfs(headID, 0)
```

**关键注释**  
- `defaultdict(list)` 把每位上司对应的下属列表自动创建好，类似“每本书的目录”。  
- `if not subordinates[cur]:` 判断是否是叶子节点（没有下属）。  
- `elapsed + informTime[cur]`：当前员工花完自己的转发时间后，才把消息交给下属。  
- 递归的返回值是 **该子树里最慢的那条路径**，所以在父节点取 `max`。  

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个员工恰好被访问一次，所有 `informTime` 只加一次。  
  - 用大白话说，员工有 100,000 人，最多走 100,000 步，几乎是瞬间完成。  

- **空间复杂度**：`O(n)`  
  - 邻接表需要存每条边（恰好 `n-1` 条），再加上递归栈的深度（最坏等于树的高度 ≤ n）。  

---  

## 心得  

- **核心技巧**：把“上司-下属”关系建成树形结构，然后用 **DFS/BFS 求最长根到叶子的路径**。  
- **适用的类似题型**  
  1. *Maximum Depth of Binary Tree*（求二叉树的最大深度）  
  2. *Longest Path in a Directed Acyclic Graph*（在 DAG 中求最长路径）  
  3. *Time Needed to Burn a Binary Tree*（燃烧二叉树需要的时间）  
- **一句话总结解题钥匙**：  
  > “把组织结构转成树，沿树向下累加时间，取最深的那条路”。  

---  

## 反思  

- **第一反应**：看到 `manager` 数组就想到“把它倒过来”，即把每个人的下属收集起来，这样从根向下遍历会更自然。  
- **最容易踩的坑**  
  - **递归层数太深**：树可能是链状的，深度接近 `n`，需要 `sys.setrecursionlimit` 或改用显式栈的迭代 BFS。  
  - **忘记加上当前节点的 `informTime`**：只有子节点才能开始计时，根节点本身的时间也必须计入。  
  - **误把 `informTime` 为 0 的叶子当作内部节点**：叶子本身不需要再传播，直接返回累计时间即可。  
- **下次类似题的第一步**：  
  > “先把父→子关系整理成邻接表（树），再决定用 DFS 还是 BFS，一遍遍历得到从根到每个叶子的累计值”。