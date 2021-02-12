# #1203. 按依赖关系对分组项目进行排序 / Sort Items by Groups Respecting Dependencies

> 难度：困难 · 标签：Depth-First Search、Breadth-First Search、Graph、Topological Sort · [LeetCode 链接](https://leetcode.com/problems/sort-items-by-groups-respecting-dependencies/)

---

## 题目（英文原版）

**Description**

There are n items each belonging to zero or one of m groups where group[i] is the group that the i-th item belongs to and it's equal to -1 if the i-th item belongs to no group. The items and the groups are zero indexed. A group can have no item belonging to it.
Return a sorted list of the items such that:
Return any solution if there is more than one solution and return an empty list if there is no solution.

**Examples**

**Example 1:**

```
Input: n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1], beforeItems = [[],[6],[5],[6],[3,6],[],[],[]]
Output: [6,3,4,1,5,2,0,7]
```

**Example 2:**

```
Input: n = 8, m = 2, group = [-1,-1,1,0,0,1,0,-1], beforeItems = [[],[6],[5],[6],[3],[],[4],[]]
Output: []
Explanation: This is the same as example 1 except that 4 needs to be before 6 in the sorted list.
```

**Constraints**

- 1 <= m <= n <= 3 * 104
- group.length == beforeItems.length == n
- -1 <= group[i] <= m - 1
- 0 <= beforeItems[i].length <= n - 1
- 0 <= beforeItems[i][j] <= n - 1
- i != beforeItems[i][j]
- beforeItems[i] does not contain duplicates elements.

---

## 题目（中文翻译）

给定 **n** 个项目，每个项目最多属于 **m** 个组中的一个，其中 `group[i]` 表示第 *i* 个项目所属的组，如果该项目不属于任何组，则 `group[i] = -1`。项目和组均使用 **0** 起始的索引。某些组可能没有任何项目。

返回一个满足以下条件的项目排序列表（sorted list）：

- 对于任意项目 *i*，若 `beforeItems[i]` 中包含项目 *j*，则在返回的列表中 **j 必须排在 i 前面**。
- 同组内的项目的相对顺序必须保持在同一组的拓扑排序中；不同组之间的顺序则由跨组的依赖决定。
- 若存在多个合法排序，返回任意一个；若不存在合法排序，返回空列表（empty list）。

示例 1：

```
输入: n = 8, m = 2,
group = [-1,-1,1,0,0,1,0,-1],
beforeItems = [[],[6],[5],[6],[3,6],[],[],[]]
输出: [6,3,4,1,5,2,0,7]
```

示例 2：

```
输入: n = 8, m = 2,
group = [-1,-1,1,0,0,1,0,-1],
beforeItems = [[],[6],[5],[6],[3],[],[4],[]]
输出: []
解释: 这与示例 1 相同，只是多了一个依赖 “4 必须在 6 前”。在这种情况下不存在满足所有依赖的排序，因此返回空列表。
```

约束条件：

- `1 <= m <= n <= 3 * 10^4`
- `group.length == beforeItems.length == n`
- `-1 <= group[i] <= m - 1`
- `0 <= beforeItems[i].length <= n - 1`
- `0 <= beforeItems[i][j] <= n - 1`
- `i != beforeItems[i][j]`
- `beforeItems[i]` 中不包含重复元素。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接、最笨的想法是**把所有物品的排列全部枚举出来**，然后逐个检查是否满足依赖关系 `beforeItems`。  
- **枚举**：把 `n` 个物品当成一副牌，所有可能的洗牌方式就是 `n!`（n 的阶乘）种。  
- **检查**：遍历每个排列，对每个物品 `i`，看它前面的所有物品里是否已经出现了 `beforeItems[i]` 中的所有前置项。如果全部出现，则这个排列合法。  

> **类比**：想象你有一堆拼图块，每块上面都有 “这块必须在 X、Y 之后” 的说明。暴力做法就是把所有块随意摆放（所有可能的摆法），然后逐个检查每块的说明是否满足——显然这种办法在块很多时几乎不可能完成。

这种方法之所以**正确**，是因为只要遍历了 **所有** 排列，就一定会找到一个满足所有依赖的排列（如果存在的话），或者遍历完后发现没有合法的排列。

#### 代码（Python）

```python
import itertools
from typing import List

def sortItems_bruteforce(n: int, m: int, group: List[int],
                         beforeItems: List[List[int]]) -> List[int]:
    # 1. 生成 0~n-1 的所有排列（暴力枚举）
    for perm in itertools.permutations(range(n)):
        # 2. 用一个集合记录已经出现过的物品，方便 O(1) 判断前置是否已出现
        seen = set()
        ok = True
        for item in perm:
            # 3. 检查当前物品的所有前置是否已经在 seen 中
            for pre in beforeItems[item]:
                if pre not in seen:          # 前置还没出现，说明排列不合法
                    ok = False
                    break
            if not ok:
                break
            seen.add(item)                  # 当前物品加入已出现集合
        if ok:                               # 找到第一个合法排列，直接返回
            return list(perm)
    # 4. 没有任何合法排列，返回空列表
    return []
```

> **注意**：这段代码只能在 `n` 极小（如 `n ≤ 8`）时跑得完。它只是帮助我们理清“如果把所有可能都尝试一次会怎样”，并不是实际可用的解法。

#### 复杂度

- **时间复杂度**：`O(n! * n)`  
  - `n!` 表示所有排列的数量，遍历每个排列时要检查最多 `n` 条依赖。  
  - “阶乘”增长非常快：`8! = 40320`，`10! = 3,628,800`，所以即使 `n = 10` 也已经不可接受。

- **空间复杂度**：`O(n)`  
  - 只用了一个长度为 `n` 的 `seen` 集合和当前排列的临时存储。

> 大白话解释：**时间复杂度** 的 `O(n!)` 就像把所有可能的钥匙都试一遍，钥匙越多，尝试的次数就会呈指数级爆炸，根本不可能在合理时间内完成。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**核心需求是找出一种满足依赖的顺序**。这正是**拓扑排序**（Topological Sort）要解决的问题：在有向无环图（DAG）中，找到一个线性序，使得每条有向边 `u -> v` 中的 `u` 都排在 `v` 前面。

本题还有一点特殊：**物品属于若干组**，组内的顺序必须满足组之间的依赖，同时组内的顺序还要满足物品之间的依赖。换句话说，我们需要 **两层** 的拓扑排序：

1. **组层面的依赖**  
   - 如果物品 `i` 属于组 `gi`，物品 `j` 属于组 `gj`，且 `i` 必须在 `j` 之前（`i` 在 `beforeItems[j]` 中），则 **组 `gi` 必须在组 `gj` 之前**（只要两组不同）。
2. **物品层面的依赖**  
   - 直接使用 `beforeItems` 建立物品之间的有向边。

如果我们先得到一个合法的 **组排序**，再在每个组内部得到一个合法的 **物品排序**，把所有组按组排序的顺序拼接起来，就得到满足全部约束的完整序列。

**关键难点**：  
- 有的物品没有所属组（`group[i] = -1`），我们可以把它们看成“独自成组”。为了统一处理，给每个这类物品 **分配一个新的唯一组编号**（例如从 `m` 开始递增），这样每个物品必然属于某个组，后面的算法就不需要特殊判断了。

**步骤概览**：

| 步骤 | 说明 |
|------|------|
| 1️⃣ 为 `group[i] = -1` 的物品分配新组编号 | 让每个物品都有组 |
| 2️⃣ 构建两张有向图 <br>① 组图（group graph）<br>② 物品图（item graph） | 用邻接表 + 入度数组 |
| 3️⃣ 对组图做拓扑排序，得到 `group_order`（如果出现环，直接返回空列表） | Kahn 算法（BFS） |
| 4️⃣ 对物品图做拓扑排序，得到 `item_order`（同样可能出现环） | 同上 |
| 5️⃣ 根据 `group_order` 把 `item_order` 中的物品归类到对应组的列表里 | 用字典 `group_to_items` |
| 6️⃣ 按 `group_order` 把每组内部的物品顺序拼接起来，得到最终答案 | 完成 |

下面我们逐步解释每一步的实现细节，并配上 **类比** 帮助理解。

---

#### 详细解释

1. **为没有组的物品“造组”**  
   - 想象你在组织一次比赛，原本有 `m` 支队伍，但有几位选手没有报名任何队伍。最简单的办法就是让他们每人单独组队，这样后面安排赛程时就不需要区分“是否有队伍”。  
   - 在代码里，用一个变量 `new_group_id = m`，遍历所有物品，如果 `group[i] == -1`，就把 `group[i] = new_group_id`，随后 `new_group_id += 1`。

2. **建图**  
   - **邻接表**：`graph[u]` 保存所有从 `u` 出发的邻居 `v`（即 `u -> v`）。  
   - **入度数组**：`indeg[v]` 记录有多少条边指向 `v`，在拓扑排序中入度为 0 的节点可以先输出。  
   - 对每个物品 `i`，遍历 `beforeItems[i]` 中的每个前置 `pre`：  
     - **物品图**：加入边 `pre -> i`，`indeg_item[i] += 1`。  
     - **组图**：如果 `group[pre] != group[i]`，说明不同组之间有先后关系，加入边 `group[pre] -> group[i]`，`indeg_group[group[i]] += 1`。  
   - 这样我们得到两张独立的有向图。

3. **拓扑排序（Kahn）**  
   - **核心思想**：一次挑选所有入度为 0 的节点（它们没有未完成的前置），放入结果序列，然后把它们的出边删掉（相当于“完成”这些节点），可能会产生新的入度为 0 的节点，继续循环。  
   - 如果最终结果长度等于节点总数，则说明图是 **无环** 的，得到合法顺序；否则出现环，说明依赖矛盾，返回空列表。  
   - 这里我们分别对 **组图**（节点数 = 总组数）和 **物品图**（节点数 = `n`）执行同样的过程。

4. **把物品放回对应组**  
   - 我们已经得到 **全局的物品拓扑序** `item_order`。但我们还需要让同一组的物品保持相对顺序（已经在 `item_order` 中保证），并且组之间按照 `group_order` 排列。  
   - 用字典 `group_to_items = {}`，遍历 `item_order`，把每个物品 `i` 加入 `group_to_items[group[i]]`（保持加入顺序不变）。  
   - 最后遍历 `group_order`，把对应组的列表依次拼接到答案中。

5. **返回答案**  
   - 若任一步骤检测到环（组图或物品图），直接返回 `[]`。否则返回拼接好的列表。

---

#### 代码（Python）

```python
from collections import defaultdict, deque
from typing import List

def sortItems(n: int, m: int, group: List[int],
              beforeItems: List[List[int]]) -> List[int]:
    """
    1. 给没有组的物品重新分配唯一的组编号
    2. 建立两张有向图：组图、物品图
    3. 分别对两张图做拓扑排序（Kahn 算法）
    4. 根据组的拓扑序把物品按组归类并拼接
    """
    # -------------------------------------------------
    # 1️⃣ 为 -1 的物品创建“新组”
    new_group_id = m                     # 新组编号从 m 开始
    for i in range(n):
        if group[i] == -1:
            group[i] = new_group_id
            new_group_id += 1
    total_groups = new_group_id          # 实际的组数量

    # -------------------------------------------------
    # 2️⃣ 建图
    # 组图
    group_adj = defaultdict(list)        # group -> list of next groups
    indeg_group = [0] * total_groups

    # 物品图
    item_adj = defaultdict(list)         # item -> list of next items
    indeg_item = [0] * n

    for i in range(n):
        for pre in beforeItems[i]:
            # 物品层面的依赖
            item_adj[pre].append(i)
            indeg_item[i] += 1

            # 组层面的依赖（只在两物品不属于同一组时建立）
            g_pre, g_cur = group[pre], group[i]
            if g_pre != g_cur:
                group_adj[g_pre].append(g_cur)
                indeg_group[g_cur] += 1

    # -------------------------------------------------
    # 3️⃣ 拓扑排序（返回空列表表示有环）
    def kahn_topo(adj: defaultdict(list), indeg: List[int]) -> List[int]:
        """Kahn 算法，适用于任意节点编号 0~len(indeg)-1 的有向图"""
        q = deque([i for i, d in enumerate(indeg) if d == 0])  # 入度为 0 的节点
        order = []
        while q:
            u = q.popleft()
            order.append(u)
            for v in adj[u]:
                indeg[v] -= 1            # 删除边 u->v
                if indeg[v] == 0:        # 若 v 成为入度 0，加入队列
                    q.append(v)
        return order

    group_order = kahn_topo(group_adj, indeg_group[:])   # 复制一份 indeg，防止被修改
    if len(group_order) != total_groups:                # 有环
        return []

    item_order = kahn_topo(item_adj, indeg_item[:])
    if len(item_order) != n:                            # 有环
        return []

    # -------------------------------------------------
    # 4️⃣ 按组归类
    group_to_items = defaultdict(list)   # 组号 -> 按拓扑顺序排列的物品列表
    for item in item_order:               # 只遍历一次，保持相对顺序
        g = group[item]
        group_to_items[g].append(item)

    # -------------------------------------------------
    # 5️⃣ 拼接得到最终答案
    answer = []
    for g in group_order:                 # 按组的拓扑顺序
        answer.extend(group_to_items[g])  # 同组内部已经是合法顺序
    return answer
```

> **关键行中文注释** 已经在代码里标明，帮助你快速定位每一步的作用。

#### 复杂度

- **时间复杂度**：`O(n + m + E)`  
  - `n`：遍历所有物品一次。  
  - `m`（实际为 `total_groups`）：遍历所有组一次。  
  - `E`：所有依赖边的数量，等于 `sum(len(beforeItems[i]))`，最多 `O(n²)` 但在题目约束下总共不超过 `3·10⁴`。  
  - 拓扑排序本身是线性时间（每条边和每个节点只访问一次），所以整体是线性级别。  
  - **大白话**：只要把所有物品、所有组、以及所有依赖一次“看一遍”，就能得到答案，跟把材料一次性搬进厨房的速度差不多。

- **空间复杂度**：`O(n + m + E)`  
  - 用了邻接表存储两张图（共 `E` 条边），以及 `indeg`、`group_to_items` 等额外数组。  
  - 同样是线性空间，随输入规模线性增长。

> 与暴力解相比，时间从 **阶乘级**（几乎不可能完成）降到了 **线性级**，在 `n = 3·10⁴` 时也能轻松跑完。

---

## 心得

- **核心技巧**：**两层拓扑排序**（先排组后排项），配合**给无组物品造组**的技巧，使得原本交叉的约束可以拆解为两张独立的有向无环图。
- **适用的题型**  
  1. “先按大类排序，再在每个大类内部排序” 的问题，如 **“课程表 II（分层课程）”**。  
  2. **“分组的任务调度”**，例如多线程任务需要先保证模块间的先后关系，再保证模块内部的执行顺序。  
  3. **“分层依赖的项目构建”**，如 Maven 多模块构建，需要先确定模块构建顺序，再确定每个模块内部的编译顺序。

- **一句话总结解题钥匙**：  
  **把“组”和“项”分别抽象成两张 DAG，分别做拓扑排序，再把结果合并。**

---

## 反思

- **第一反应**：看到 `group` 与 `beforeItems` 同时出现，立刻想到 **图**，尤其是 **拓扑排序**，因为“前置”本质上是有向边的概念。
- **最容易踩的坑**  
  1. **环检测**：忘记对组图和项图都要检测环，导致在组内部没有环但跨组出现冲突时仍返回错误答案。  
  2. **处理 `group[i] = -1`**：如果直接忽略，后面构建组图时会出现 `-1` 作为节点，导致索引错误或遗漏依赖。必须给每个无组物品单独分配唯一组号。  
  3. **顺序混淆**：在把 `item_order` 放回组时，要保持 `item_order` 的相对顺序；不能在同组内部再次随意排序，否则可能破坏项之间的依赖。  
- **下次类似题目第一步**：  
  **把所有约束抽象成有向图，先判断是否有环（能否完成），再决定是否需要分层（比如组/模块）来分别拓扑排序。**