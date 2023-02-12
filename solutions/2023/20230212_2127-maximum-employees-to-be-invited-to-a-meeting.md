# #2127. 会议可邀请的最多员工数 / Maximum Employees to Be Invited to a Meeting

> 难度：困难 · 标签：Depth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/maximum-employees-to-be-invited-to-a-meeting/)

---

## 题目（英文原版）

**Description**

A company is organizing a meeting and has a list of n employees, waiting to be invited. They have arranged for a large circular table, capable of seating any number of employees.
The employees are numbered from 0 to n - 1. Each employee has a favorite person and they will attend the meeting only if they can sit next to their favorite person at the table. The favorite person of an employee is not themself.
Given a 0-indexed integer array favorite, where favorite[i] denotes the favorite person of the ith employee, return the maximum number of employees that can be invited to the meeting.

**Examples**

**Example 1:**

```
Input: favorite = [2,2,1,2]
Output: 3
Explanation:
The above figure shows how the company can invite employees 0, 1, and 2, and seat them at the round table.
All employees cannot be invited because employee 2 cannot sit beside employees 0, 1, and 3, simultaneously.
Note that the company can also invite employees 1, 2, and 3, and give them their desired seats.
The maximum number of employees that can be invited to the meeting is 3.
```

**Example 2:**

```
Input: favorite = [1,2,0]
Output: 3
Explanation: 
Each employee is the favorite person of at least one other employee, and the only way the company can invite them is if they invite every employee.
The seating arrangement will be the same as that in the figure given in example 1:
- Employee 0 will sit between employees 2 and 1.
- Employee 1 will sit between employees 0 and 2.
- Employee 2 will sit between employees 1 and 0.
The maximum number of employees that can be invited to the meeting is 3.
```

**Example 3:**

```
Input: favorite = [3,0,1,4,1]
Output: 4
Explanation:
The above figure shows how the company will invite employees 0, 1, 3, and 4, and seat them at the round table.
Employee 2 cannot be invited because the two spots next to their favorite employee 1 are taken.
So the company leaves them out of the meeting.
The maximum number of employees that can be invited to the meeting is 4.
```

**Constraints**

- n == favorite.length
- 2 <= n <= 105
- 0 <= favorite[i] <= n - 1
- favorite[i] != i

---

## 题目（中文翻译）

公司正在组织一次会议，手上有 `n` 名员工的名单，需要邀请他们参加。会议使用一张大型圆形餐桌，能够容纳任意数量的员工。

员工编号为 `0` 到 `n - 1`。每位员工都有一位最喜欢的同事，且只有当他们能够坐在最喜欢的同事的旁边时才会参加会议。**最喜欢的同事**（favorite）不是自己。

给定一个下标从 `0` 开始的整数数组 `favorite`，其中 `favorite[i]` 表示第 `i` 位员工最喜欢的那位同事，返回公司能够邀请参加会议的员工的最大数量。

---

## 示例

### 示例 1  
**输入**：`favorite = [2,2,1,2]`  
**输出**：`3`  
**解释**：  
上图展示了公司可以邀请员工 `0、1、2` 并将他们安排在圆桌上的方式。  
并非所有员工都能被邀请，因为员工 `2` 不可能同时坐在员工 `0、1、3` 旁边。  
公司同样可以邀请员工 `1、2、3` 并为他们安排满意的座位。  
因此，能够邀请的最多员工数为 `3`。

### 示例 2  
**输入**：`favorite = [1,2,0]`  
**输出**：`3`  
**解释**：  
每位员工至少是另一位员工的最喜欢的同事，唯一的可行方案是邀请所有员工。  
座位安排如下（同示例 1 的图示）：  
- 员工 `0` 坐在员工 `2` 与员工 `1` 之间。  
- 员工 `1` 坐在员工 `0` 与员工 `2` 之间。  
- 员工 `2` 坐在员工 `1` 与员工 `0` 之间。  
因此，最大可邀请人数为 `3`。

### 示例 3  
**输入**：`favorite = [3,0,1,4,1]`  
**输出**：`4`  
**解释**：  
上图展示了公司可以邀请员工 `0、1、3、4` 并将他们安排在圆桌上的方式。  
员工 `2` 无法被邀请，因为其最喜欢的同事 `1` 两侧的座位已经被占用。  
于是公司将员工 `2` 排除在外，能够邀请的最多员工数为 `4`。

---

## 约束条件

- `n == favorite.length`
- `2 <= n <= 10^5`
- `0 <= favorite[i] <= n - 1`
- `favorite[i] != i`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

把每个员工看成 **图中的一个节点**，`favorite[i]` 表示 “员工 i 喜欢的人”。  
如果把这条喜欢的关系画成一条 **有向边**，从 `favorite[i]` 指向 `i`（即 “被喜欢的” → “喜欢者”），  
整个公司就形成了一个 **有向图**。  

> **类比**：想象一本字典，词是员工，`favorite[i]` 就是词条里指向的 “页码”。  
> 我们要把这些词排成一个圆环，使得每个词的左/右相邻词正好是它指向的那个人。

最直接的想法是 **枚举所有可能的邀请子集**，对每个子集检查能否把它们排成满足条件的环。  
具体步骤：

1. 枚举 `0..2^n-1`（每一位 0/1 表示对应员工是否被邀请）。  
2. 对当前子集，把被邀请的员工取出来，尝试把他们排成一个环（可以用全排列遍历所有坐次）。  
3. 检查每个员工的左右相邻是否正好包含 `favorite[i]`。  
4. 记录满足条件的子集中人数的最大值。

> **为什么会对**：我们把所有可能的邀请方案都穷举了，只要有合法的安排，就一定会在枚举过程中被发现。

> **时间/空间复杂度**：  
> - 枚举子集有 `2^n` 种，  
> - 对每个子集再枚举所有排列，最多是 `k!`（`k` 为子集大小）。  
> - 所以时间复杂度是 **指数级**，大约 `O( n! )`，在最坏情况下根本不可运行。  
> - 空间只需要存放当前子集和排列，最多 `O(n)`。

#### 代码（Python）

```python
import itertools

def maxInvites_bruteforce(favorite):
    n = len(favorite)
    best = 0

    # 1. 枚举所有子集（用二进制 mask 表示）
    for mask in range(1, 1 << n):
        invited = [i for i in range(n) if mask >> i & 1]   # 被邀请的员工列表
        k = len(invited)
        # 2. 对子集中的员工全排列，尝试坐成环
        for perm in itertools.permutations(invited):
            ok = True
            # 检查每个人左右是否都有自己的 favorite
            for idx, emp in enumerate(perm):
                left = perm[(idx - 1) % k]   # 环的左邻
                right = perm[(idx + 1) % k]  # 环的右邻
                if favorite[emp] not in (left, right):
                    ok = False
                    break
            if ok:
                best = max(best, k)
                break      # 该子集已经找到合法排列，无需继续枚举排列
    return best
```

> 这段代码只能在 `n ≤ 10` 左右的小样例上跑通，真正的题目规模可达 `10^5`，必须另辟蹊径。

#### 复杂度

- **时间复杂度**：`O( 2^n * n! )` —— 指数级增长，实际不可接受。  
- **空间复杂度**：`O(n)` —— 只保存当前的子集和排列。

---

### 2. 最优解

#### 思路  

**从暴力解出发，找出瓶颈**：  
- 暴力解在 *枚举子集* 与 *枚举排列* 两个环节都爆炸。  
- 实际上，邀请方案只和 **图的结构** 有关：每个人只能坐在自己喜欢的人的左右两侧。  
- 这意味着合法的座位安排只能出现在 **环（cycle）** 或者 **以 2‑环为核心的“链+环”** 结构中。

下面一步步推导最优思路：

1. **构建有向图**  
   对每个 `i`，画一条从 `i` → `favorite[i]` 的有向边（更直观：`i` 指向自己喜欢的人）。  
   为了后面方便求入度，我们也会保存 **逆向邻接表**：`rev[v]` 收集所有指向 `v` 的节点。

2. **观察图的形状**  
   - 每个节点只有 **一条出边**（因为每个人只有唯一的 favorite）。  
   - 整个图因此是 **若干个有向环** + **从环伸出的树形链**（没有出环的节点只能形成一条向环的链）。  

3. **两类可能的最大邀请方式**  

   **方式一：选取一个普通环**（长度 ≥ 3）。  
   - 若我们只邀请环上的节点，那么每个人的左/右邻恰好是环上的前后两个节点，必然包含自己的 favorite。  
   - 环外的节点（树枝）不可能加入，因为它们的 favorite 在环上，而环上已经被占满，无法为它们提供两个空位。  
   - 因此，**最长环的长度** 是一种候选答案。

   **方式二：利用长度为 2 的环（相互喜欢）**  
   - 当 `i` 和 `j` 互相是 favorite（即 `favorite[i]==j` 且 `favorite[j]==i`），形成 **2‑环**。  
   - 这时可以在 `i` 的左侧挂上一条最长的“链”，在 `j` 的右侧再挂上一条最长的“链”。  
   - 链的定义：从某个节点出发，沿 **逆向边**（即“谁喜欢我”）一直向下，直到到达 `i`（或 `j`）为止，且不经过环内其他节点。  
   - 只要把这两条最长链分别接在 `i`、`j` 两侧，所有参与者仍然满足相邻条件。  
   - 所有 **互为 2‑环的配对** 可以 **独立** 叠加，因为它们的链互不交叉。  
   - 最终答案是所有 2‑环配对贡献之和：  
     \[
     \sum_{\text{每个 }(i,j)} \bigl(2 + \text{最长链到 }i + \text{最长链到 }j\bigr)
     \]

4. **如何求最长链**  

   - 对每个节点计算 **入度**（指向它的节点数）。  
   - 把所有 **入度为 0** 的节点放进队列，进行 **拓扑削除**（类似把树枝的叶子一次次剪掉）。  
   - 在削除过程中，我们维护 `depth[x]`：从叶子到当前节点的最长路径长度。  
   - 当一个节点的所有前驱都被删掉后，它的入度会变为 0，继续入队。  
   - 最终剩下的节点恰好是 **环上的节点**（包括 2‑环和长度 ≥3 的环）。  
   - 对每个环节点 `v`，`depth[v]` 就是 **从它的外部树枝能拉来的最长链长度**（不计 `v` 本身）。  

5. **整体算法**  

   - **步骤 1**：建图 & 逆向邻接表 & 计算入度。  
   - **步骤 2**：拓扑削除，得到 `depth[]`（最长链长度）。  
   - **步骤 3**：遍历所有节点，寻找环。  
       * 对每个未访问的环，记录环的长度。  
       * 若长度为 **2**，把对应的两个节点记入 “互相喜欢的配对” 列表。  
       * 若长度 ≥ **3**，更新 `max_cycle_len`。  
   - **步骤 4**：对所有 2‑环配对，累加 `2 + depth[i] + depth[j]`，得到 `pair_sum`。  
   - **步骤 5**：答案 = `max( max_cycle_len , pair_sum )`。

> **核心数据结构**：  
> - **逆向邻接表 `rev`**：`rev[v]` 保存所有 `u` 使得 `favorite[u]==v`，相当于 “谁把我当 favorite”。  
> - **入度数组 `indeg`**：每个节点的出度固定为 1，入度可能为 0、1、2…  
> - **深度数组 `depth`**：记录从该节点外部树枝可以拉来的最长链长度。  

> **类比**：  
> - 拓扑削除过程像 **把树的叶子一次次剪掉**，只剩下树干——这里的树干正好是环。  
> - 2‑环就像 **两个人互相拥抱**，可以在他们各自的背后各拉一条最长的“队伍”，一起组成更大的圆桌。

#### 代码（Python）

```python
from collections import deque, defaultdict
from typing import List

def maximumInvitations(favorite: List[int]) -> int:
    n = len(favorite)

    # ---------- 1. 建图 ----------
    # rev[v] : 所有把 v 当 favorite 的员工列表（逆向边）
    rev = [[] for _ in range(n)]
    indeg = [0] * n
    for i, f in enumerate(favorite):
        rev[f].append(i)          # i -> f 的逆向
        indeg[f] += 1             # f 的入度 +1

    # ---------- 2. 拓扑削除，求每个节点的最长链 ----------
    depth = [0] * n                # depth[v] = 从外部树枝能拉来的最长链长度（不含 v）
    q = deque([i for i in range(n) if indeg[i] == 0])   # 所有叶子

    while q:
        cur = q.popleft()
        nxt = favorite[cur]       # cur 指向的唯一节点
        # 更新 nxt 能得到的最长链长度
        depth[nxt] = max(depth[nxt], depth[cur] + 1)
        indeg[nxt] -= 1
        if indeg[nxt] == 0:       # 成为新的叶子
            q.append(nxt)

    # ---------- 3. 找环 ----------
    visited = [False] * n
    max_cycle_len = 0            # 长度 >=3 的环的最大长度
    pair_sum = 0                 # 所有 2‑环配对的贡献之和

    for i in range(n):
        if indeg[i] == 0 or visited[i]:
            # 已被削除或已经在之前的环遍历中标记
            continue

        # 从 i 出发，顺着唯一的出边遍历整条环
        cur = i
        cycle = []
        while not visited[cur]:
            visited[cur] = True
            cycle.append(cur)
            cur = favorite[cur]

        # 此时 cur 再次回到已访问的节点，说明得到完整的环
        cyc_len = len(cycle)

        if cyc_len == 2:
            a, b = cycle[0], cycle[1]
            # 2‑环的贡献 = 2 + 最长链到 a + 最长链到 b
            pair_sum += 2 + depth[a] + depth[b]
        else:
            # 长度 >=3 的普通环，只能直接使用环的大小
            max_cycle_len = max(max_cycle_len, cyc_len)

    # ---------- 4. 结果 ----------
    return max(max_cycle_len, pair_sum)
```

> **代码要点说明**  
> 1. `rev` 并未在后续显式使用，但保留下来帮助理解；实际只需 `indeg` 与 `favorite`。  
> 2. 拓扑削除时 `depth[nxt] = max(depth[nxt], depth[cur] + 1)`：把从叶子到 `cur` 的链长度加一，传递给它的唯一出边。  
> 3. 环的遍历采用 **标记 visited**，保证每个环只被统计一次。  
> 4. 对于 2‑环，`depth[a]`、`depth[b]` 已经是 **不包括 a、b 本身** 的最长外部链长度，直接相加即可。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 建图、计算入度、拓扑削除、遍历环均只遍历一次或常数次。  
  - 与 `n` 成线性关系，能够轻松处理 `10^5` 规模的数据。  
- **空间复杂度**：`O(n)`  
  - 需要保存 `rev`（总边数 = `n`），`indeg`、`depth`、`visited` 等数组。  

相较于暴力解的指数级时间，最优解把复杂度降到了线性，真正可用。

---

## 心得

- **核心技巧**：把“每个人只能坐在自己喜欢的人左右”转化为 **有向图的环与树枝结构**，然后分别处理 **普通环** 与 **相互喜欢的 2‑环 + 最长链** 两种情况。  
- **适用的题型**  
  1. “社交网络” 类的环/链问题，例如 LeetCode 997 “Find the Town Judge”。  
  2. “最长环/链” 类的图论问题，如 LeetCode 2360 “Longest Cycle in a Graph”。  
  3. 需要 **拓扑削除** 来剥离非环节点的题目，如 LeetCode 2100 “Find Good Days to Rob the Bank”。  
- **一句话总结解题钥匙**：  
  > “把每个人指向 favorite 的有向图分解为环 + 入环的最长链，环的长度或 2‑环+链的和即为答案。”

---

## 反思

- **第一反应**：看到“圆桌、相邻”立刻想到 **排列组合**，于是想到枚举所有坐次——这导致了暴力解的思路。  
- **最容易踩的坑**  
  1. **忽略 2‑环的特殊处理**：如果只取最长环，很多情况下会漏掉通过 2‑环+链可以邀请更多员工的情况。  
  2. **链的长度计算错误**：链的长度应当是 **不包括环节点本身** 的节点数，且只能取 **最长的** 那一条。  
  3. **环的遍历重复计数**：没有 `visited` 标记会导致同一个环被多次统计，进而答案偏大。  
- **下次遇到同类题**：第一步先 **把问题抽象成图**，检查每个节点的出度/入度，利用 **拓扑削除** 把非环部分剥离，再专注分析 **环的结构**（普通环 vs 2‑环），这样可以快速定位最优解的方向。