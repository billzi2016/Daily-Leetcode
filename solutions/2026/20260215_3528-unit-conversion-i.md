# #3528. 单位转换 I / Unit Conversion I

> 难度：中等 · 标签：Depth-First Search、Breadth-First Search、Graph · [LeetCode 链接](https://leetcode.com/problems/unit-conversion-i/)

---

## 题目（英文原版）

**Description**

There are n types of units indexed from 0 to n - 1. You are given a 2D integer array conversions of length n - 1, where conversions[i] = [sourceUniti, targetUniti, conversionFactori]. This indicates that a single unit of type sourceUniti is equivalent to conversionFactori units of type targetUniti.
Return an array baseUnitConversion of length n, where baseUnitConversion[i] is the number of units of type i equivalent to a single unit of type 0. Since the answer may be large, return each baseUnitConversion[i] modulo 109 + 7.

**Examples**

**Example 1:**

```
Input: conversions = [[0,1,2],[1,2,3]]
Output: [1,2,6]
Explanation:
```

**Example 2:**

```
Input: conversions = [[0,1,2],[0,2,3],[1,3,4],[1,4,5],[2,5,2],[4,6,3],[5,7,4]]
Output: [1,2,3,8,10,6,30,24]
Explanation:
```

**Constraints**

- 2 <= n <= 105
- conversions.length == n - 1
- 0 <= sourceUniti, targetUniti < n
- 1 <= conversionFactori <= 109
- It is guaranteed that unit 0 can be converted into any other unit through a unique combination of conversions without using any conversions in the opposite direction.

---

## 题目（中文翻译）

有 **n** 种单位，编号从 `0` 到 `n - 1`。  
给定一个长度为 `n - 1` 的二维整数数组（2D integer array）`conversions`，其中 `conversions[i] = [sourceUniti, targetUniti, conversionFactori]`。这表示 **1** 个 `sourceUniti` 单位等价于 `conversionFactori` 个 `targetUniti` 单位。

返回一个长度为 `n` 的数组 `baseUnitConversion`，其中 `baseUnitConversion[i]` 为 **1** 个单位 `0` 等价的 `i` 类型单位的数量。由于答案可能很大，请对每个 `baseUnitConversion[i]` 取模 `10^9 + 7`。

---

**示例 1**  
```
Input: conversions = [[0,1,2],[1,2,3]]
Output: [1,2,6]
解释：
```

**示例 2**  
```
Input: conversions = [[0,1,2],[0,2,3],[1,3,4],[1,4,5],[2,5,2],[4,6,3],[5,7,4]]
Output: [1,2,3,8,10,6,30,24]
解释：
```

**约束条件**  

- `2 <= n <= 10^5`  
- `conversions.length == n - 1`  
- `0 <= sourceUniti, targetUniti < n`  
- `1 <= conversionFactori <= 10^9`  
- 保证单位 `0` 可以通过唯一的一系列正向转换（不使用相反方向的转换）转换到任意其他单位。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目给出 `n` 种单位，`conversions` 表示 **有向** 的换算关系，例如  
`[0, 1, 2]` 表示 “1 个单位 0 等价于 2 个单位 1”。  
我们要算出 **从单位 0 出发**，到每一种单位的换算倍率（即 1 个 0 等价多少个该单位），并对 `10⁹+7` 取模。

最直接的想法是：  
对每一个目标单位 `i`，从 0 开始 **逐条搜索** 所有可能的路径，找到唯一的那条（题目保证唯一），把路径上所有 `conversionFactor` 相乘，就是答案。  

可以把它想象成在一张地图上找路：  
- **节点** = 各种单位  
- **有向边** = 换算关系，边上写着“1 个 source = factor 个 target”。  
- 暴力搜索就像把每条路都走一遍，记下走过的路程（乘积），最后选出唯一的合法路。

> 为什么这种方法一定对？  
> 因为题目保证 **从 0 能到任意其他单位，且路径唯一**。只要我们能遍历到目标节点，乘积就是唯一答案。

**时间复杂度**：对每个目标 `i` 都要一次完整的遍历（最坏遍历 `n` 条边），于是 `O(n²)`。  
**空间复杂度**：递归栈或显式的 visited 数组需要 `O(n)`。

> 大白话的解释：  
> `O(n²)` 就是 “如果有 10 000 个单位，程序大概要跑 10 000 × 10 000 = 1 亿 步”，在实际中会超时。

#### 代码（Python）

```python
from collections import defaultdict, deque

MOD = 10 ** 9 + 7

def brute_force(conversions, n):
    # 建立邻接表：source -> [(target, factor), ...]
    graph = defaultdict(list)
    for s, t, f in conversions:
        graph[s].append((t, f))

    # 用 BFS/DFS 找到从 0 到 target 的唯一路径并计算乘积
    def bfs(target):
        # 队列里存 (node, current_product)
        q = deque([(0, 1)])
        visited = set([0])
        while q:
            node, prod = q.popleft()
            if node == target:          # 找到目标，返回乘积
                return prod % MOD
            for nxt, f in graph[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    q.append((nxt, (prod * f) % MOD))
        return 1  # 0 本身

    ans = [1] * n          # baseUnitConversion[0] 固定为 1
    for i in range(1, n):
        ans[i] = bfs(i)    # 对每个 i 都跑一次 BFS
    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个目标节点都要遍历整个图（最坏 `n` 条边），所以是 `n` 次 `O(n)`。  
  - 用大白话说，就是“如果单位有 10⁵，程序需要 10¹⁰ 步，根本跑不完”。  

- **空间复杂度**：`O(n)`  
  - 主要是保存邻接表和 BFS 时的 `visited`/队列，规模随节点数线性增长。

---

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于重复遍历**：我们对每个目标都重新跑一次 BFS，导致 `O(n²)`。  
实际上，**因为图是一棵有向树，且根是 0**，我们只需要遍历一次整棵树，就能把所有答案一次性算出来。

> **关键观察**  
> - `conversions` 长度为 `n‑1`，且保证“从 0 能到任意其他单位且路径唯一”。这正是 **有向树**（rooted tree）的特征。  
> - 在树上，从根出发的 **深度优先搜索（DFS）或广度优先搜索（BFS）**，每走一条边就把当前乘积乘上这条边的 `factor`，得到子节点的答案。  
> - 以后再访问子节点的子节点时，只需要在父节点的答案基础上再乘一次因子，**不需要重新遍历**。

> **类比**  
> 想象你在一棵家谱树上，从祖先（单位 0）开始记录血缘比例。你只要把每一代的比例乘下来，就能一次性得到所有后代的比例，而不必每次都从祖先重新数一遍。

**实现细节**  

1. **建图**：仍然用邻接表 `graph[source] → (target, factor)`。因为所有边都是从父指向子（没有逆向），我们直接使用有向边。  
2. **遍历**：从根节点 `0` 开始，使用 **栈**（DFS）或 **队列**（BFS）。维护一个数组 `ans[i]` 保存 “1 个 0 等价多少个 i”。  
   - 初始 `ans[0] = 1`（1 个 0 本身）。  
   - 当从 `u` 访问到子节点 `v` 时，`ans[v] = ans[u] * factor % MOD`。  
3. **取模**：因为乘积可能非常大，边乘边取模即可，防止溢出。  

整个过程只遍历每条边一次，时间 `O(n)`，空间 `O(n)`（存图 + 结果数组）。

#### 代码（Python）

```python
from collections import defaultdict, deque

MOD = 10 ** 9 + 7

def unit_conversion(conversions, n):
    """
    返回长度为 n 的数组 baseUnitConversion，
    其中 baseUnitConversion[i] 表示 1 个单位 0 等价多少个单位 i（模 1e9+7）。
    """
    # 1️⃣ 建图（有向树）
    graph = defaultdict(list)
    for s, t, f in conversions:
        graph[s].append((t, f))

    # 2️⃣ BFS（也可以用 DFS）
    ans = [0] * n
    ans[0] = 1                       # 根节点自身的倍率为 1
    q = deque([0])                   # 从根开始遍历

    while q:
        u = q.popleft()
        for v, factor in graph[u]:
            # 乘上当前边的因子，再取模，得到子节点的倍率
            ans[v] = (ans[u] * factor) % MOD
            q.append(v)               # 把子节点加入队列继续向下扩展

    return ans
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每条边只访问一次，乘一次因子，整体线性。相比暴力的 `O(n²)`，速度提升了 **n 倍**。  
  - 用大白话说：如果有 10⁵ 个单位，只需要大约 10⁵ 步就能算完，完全可以接受。

- **空间复杂度**：`O(n)`  
  - 用来存邻接表、结果数组以及 BFS 队列。和节点数同阶，属于必要空间。

---

## 心得  

- **核心技巧**：把题目抽象为“根在 0 的有向树”，利用一次 BFS/DFS 在遍历过程中累计乘积。  
- **该技巧适用的题型**  
  1. **树形累计**：如 “每个节点的值 = 父节点值 × 边权”。  
  2. **层次比例**：比如 “公司组织结构中，部门预算 = 上级预算 × 系数”。  
  3. **单源最短/最长乘积**（在无负权的乘积图中），同样可以用一次遍历累计。  
- **一句话总结解题钥匙**：**“一次遍历，边走边累乘”。**

---

## 反思  

- **第一反应**：看到“唯一路径、n‑1 条边”，立刻想到“树”。于是把问题转化为在树上做一次遍历。  
- **最容易踩的坑**  
  - **忘记取模**：乘积会在 64 位整数范围外，需要在每一步乘完后立刻 `% MOD`。  
  - **方向错误**：题目保证只能沿给出的方向走，不能反向使用转换关系。若把图当成无向的，会产生错误的路径。  
  - **节点编号不连续**：虽然题目说 0…n‑1，但在实际实现时仍需使用 `defaultdict(list)` 防止 KeyError。  
- **下次遇到同类题**：第一步先判断“图的结构”。如果是 **树**（`edges = n‑1` 且连通），就考虑 **一次 DFS/BFS 累计** 而不是对每个查询单独搜索。