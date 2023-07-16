# #2322. **树上移除两条边后的最小得分** / Minimum Score After Removals on a Tree

> 难度：困难 · 标签：Array、Bit Manipulation、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/minimum-score-after-removals-on-a-tree/)

---

## 题目（英文原版）

**Description**

There is an undirected connected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.
You are given a 0-indexed integer array nums of length n where nums[i] represents the value of the ith node. You are also given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
Remove two distinct edges of the tree to form three connected components. For a pair of removed edges, the following steps are defined:
Return the minimum score of any possible pair of edge removals on the given tree.

**Examples**

**Example 1:**

```
Input: nums = [1,5,5,4,11], edges = [[0,1],[1,2],[1,3],[3,4]]
Output: 9
Explanation: The diagram above shows a way to make a pair of removals.
- The 1st component has nodes [1,3,4] with values [5,4,11]. Its XOR value is 5 ^ 4 ^ 11 = 10.
- The 2nd component has node [0] with value [1]. Its XOR value is 1 = 1.
- The 3rd component has node [2] with value [5]. Its XOR value is 5 = 5.
The score is the difference between the largest and smallest XOR value which is 10 - 1 = 9.
It can be shown that no other pair of removals will obtain a smaller score than 9.
```

**Example 2:**

```
Input: nums = [5,5,2,4,4,2], edges = [[0,1],[1,2],[5,2],[4,3],[1,3]]
Output: 0
Explanation: The diagram above shows a way to make a pair of removals.
- The 1st component has nodes [3,4] with values [4,4]. Its XOR value is 4 ^ 4 = 0.
- The 2nd component has nodes [1,0] with values [5,5]. Its XOR value is 5 ^ 5 = 0.
- The 3rd component has nodes [2,5] with values [2,2]. Its XOR value is 2 ^ 2 = 0.
The score is the difference between the largest and smallest XOR value which is 0 - 0 = 0.
We cannot obtain a smaller score than 0.
```

**Constraints**

- n == nums.length
- 3 <= n <= 1000
- 1 <= nums[i] <= 108
- edges.length == n - 1
- edges[i].length == 2
- 0 <= ai, bi < n
- ai != bi
- edges represents a valid tree.

---

## 题目（中文翻译）

给定一棵无向连通树，节点数为 `n`（编号为 `0` 到 `n‑1`），共 `n‑1` 条边。  
另给定一个下标从 `0` 开始的整数数组 `nums`（长度为 `n`），其中 `nums[i]` 表示第 `i` 个节点的值。还有一个二维整数数组 `edges`（长度为 `n‑1`），其中 `edges[i] = [a_i, b_i]` 表示在树中存在一条连接节点 `a_i` 和 `b_i` 的边。

现在需要 **移除** 两条不同的边，使得原树被划分成 **三个连通分量**（connected components）。对于任意一组被移除的两条边，定义如下步骤：

1. 对每个连通分量，计算其中所有节点值的 **异或**（XOR）结果。  
2. 三个分量的 XOR 值分别记为 `x1`, `x2`, `x3`。  
3. 该划分的 **得分** 为 `max(x1, x2, x3) - min(x1, x2, x3)`。

返回在给定树上，所有可能的两条边的移除组合中 **最小的得分**。

---

### 示例

#### 示例 1
> **输入**  
> `nums = [1,5,5,4,11]`  
> `edges = [[0,1],[1,2],[1,3],[3,4]]`  
> **输出** `9`  
> **解释**  
> 如下图所示是一种合法的移除方式：  
> - 第 1 个分量包含节点 `[1,3,4]`，对应值 `[5,4,11]`，其 XOR 为 `5 ^ 4 ^ 11 = 10`。  
> - 第 2 个分量包含节点 `[0]`，对应值 `[1]`，其 XOR 为 `1`。  
> - 第 3 个分量包含节点 `[2]`，对应值 `[5]`，其 XOR 为 `5`。  
> 得分为 `max(10, 1, 5) - min(10, 1, 5) = 10 - 1 = 9`。

#### 示例 2
> **输入**  
> `nums = [5,5,2,4,4,2]`  
> `edges = [[0,1],[1,2],[5,2],[4,3],[1,3]]`  
> **输出** `0`  
> **解释**  
> 如下图所示的一种移除方式得到：  
> - 第 1 个分量包含节点 `[3,4]`，值 `[4,4]`，XOR 为 `4 ^ 4 = 0`。  
> - 第 2 个分量包含节点 `[1,0]`，值 `[5,5]`，XOR 为 `5 ^ 5 = 0`。  
> - 第 3 个分量包含节点 `[2,5]`，值 `[2,2]`，XOR 为 `2 ^ 2 = 0`。  
> 得分为 `max(0,0,0) - min(0,0,0) = 0`。

---

### 约束条件

- `n == nums.length`
- `3 <= n <= 1000`
- `1 <= nums[i] <= 10^8`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= a_i, b_i < n`
- `a_i != b_i`
- `edges` 构成一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法就是把 **每一条边都尝试删掉**，再在剩下的图里挑第二条边删掉，最后算出得到的三个连通块的异或值，求出它们的分数（最大异或 - 最小异或），取所有可能中的最小值。

> **数据结构类比**  
> - **树**：就像一棵真正的树，节点之间只有唯一的“父子”关系。  
> - **遍历**：我们可以把它想成在树上走一遍，顺便把每个子树里所有节点的值异或起来（相当于把子树的“总价”算好）。  
> - **删除边**：把树的两根枝条剪掉，树就会分成三块，正好对应题目要求的三个连通分量。

**为什么暴力能得到正确答案**  
只要把所有合法的两条边的组合枚举完，并对每种组合准确地算出三个分量的异或值，最后取最小分数，就一定会得到全局最优。枚举是“穷举”，不遗漏任何可能。

**复杂度分析（大白话）**  

- 枚举第一条边有 `n‑1` 条（因为树有 `n‑1` 条边），枚举第二条边还有 `n‑2` 条，总共大约是 `(n‑1)·(n‑2)/2 ≈ n²/2` 种组合。  
- 对每一种组合，我们需要重新遍历整棵树一次来得到三个分量的异或值，这一步是 **O(n)**（走一遍所有节点）。  
- 所以整体时间是 **O(n³)**，在最坏情况下（`n=1000`）大约是 `10⁹` 步，显然太慢。  
- 只用到的额外空间是保存树的邻接表和一次遍历的临时变量，都是 **O(n)**。

#### 代码（Python）

```python
from collections import defaultdict, deque
from itertools import combinations
from typing import List

def minimumScore(nums: List[int], edges: List[List[int]]) -> int:
    n = len(nums)

    # ---------- 建图 ----------
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # ---------- 辅助函数：删掉两条边后，求三个连通块的异或 ----------
    def component_xors(cut1, cut2):
        """返回三个连通块的异或值，cut 为 (u, v) 形式的边"""
        # 把两条要删除的边放进集合，遍历时跳过
        banned = {tuple(cut1), tuple(cut2), tuple(cut1[::-1]), tuple(cut2[::-1])}
        seen = [False] * n
        xors = []

        for start in range(n):
            if not seen[start]:
                # BFS/DFS 只会遍历当前连通块
                stack = [start]
                cur_xor = 0
                seen[start] = True
                while stack:
                    node = stack.pop()
                    cur_xor ^= nums[node]          # 累计异或
                    for nb in g[node]:
                        if (node, nb) in banned:   # 这条边被删掉了
                            continue
                        if not seen[nb]:
                            seen[nb] = True
                            stack.append(nb)
                xors.append(cur_xor)
        return xors   # 长度必为 3

    # ---------- 枚举两条边 ----------
    best = float('inf')
    for e1, e2 in combinations(edges, 2):
        a, b = component_xors(e1, e2)
        score = max(a) - min(a)      # 题目定义的分数
        best = min(best, score)

    return best
```

> **代码要点中文注释**  
> - `g`：邻接表，用来快速得到每个节点的相邻节点。  
> - `banned`：把要删掉的两条边放进集合，遍历时直接跳过，等价于“剪枝”。  
> - `component_xors`：利用 DFS（栈实现）遍历当前连通块，顺便把该块所有节点值异或起来。  

#### 复杂度

- **时间复杂度**：`O(n³)`  
  - 解释：我们枚举了约 `n²/2` 对边，每对都要跑一次完整的 DFS（`O(n)`），于是乘起来就是 `O(n³)`。  
- **空间复杂度**：`O(n)`  
  - 解释：主要是邻接表 `g`（存 `2·(n‑1)` 条边）和 DFS 用的 `seen`/`stack`，随节点数线性增长。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于每次删边后都要重新遍历整棵树。  
如果我们提前算好每个子树的异或值，并且能够快速判断两个删掉的边之间的**祖孙关系**，就能在 **O(1)** 时间内算出三个分量的异或，从而把总体时间降到 **O(n²)**（枚举两条边仍然是必要的）。

**关键步骤**  

1. **把树根在任意节点（这里选 0）**。  
   - 这样每条边都有唯一的“父 → 子”方向，删掉这条边相当于把 **子树** 与父树分离。  

2. **一次 DFS 预处理**  
   - `sub_xor[u]`：以 `u` 为根的子树中所有节点值的异或。  
   - `parent[u]`、`depth[u]`：父节点和深度，用来判断祖孙关系。  
   - `tin[u]、tout[u]`（进入/离开时间）：如果 `tin[a] < tin[b]` 且 `tout[b] < tout[a]`，则 `a` 是 `b` 的祖先。  

3. **枚举两条边**（实际只枚举两条 **子节点**，因为每条边唯一对应它的子端）  
   - 对每条边记为 `child`（更深的那一端）。  
   - 对任意两条边 `a`、`b`，分两种情况：

   | 情况 | 解释 | 三块的异或 |
   |------|------|------------|
   | **互不相交**（既不是祖先也不是后代） | 两条边分别切掉两棵独立的子树 | `x = sub_xor[a]`<br>`y = sub_xor[b]`<br>`z = total_xor ^ x ^ y` |
   | **相交**（其中一条在另一条子树内部） | 假设 `a` 是 `b` 的祖先 | `x = sub_xor[b]`（最里面的子树）<br>`y = sub_xor[a] ^ sub_xor[b]`（祖先子树减去内部子树）<br>`z = total_xor ^ sub_xor[a]`（剩下的大块） |

   - 只要把这三块的异或值算出来，分数 = `max - min`，更新全局最小即可。

4. **为什么只要 O(n²)**  
   - 预处理是一次 DFS，**O(n)**。  
   - 枚举两条边的组合是 `C(n‑1, 2) ≈ n²/2`，每次只做常数次的异或和比较，**O(1)**。  
   - 所以总体 **O(n²)**，对 `n ≤ 1000` 完全绰绰有余。

**类比帮助理解**  

- 把树想象成一棵家族树，`sub_xor[u]` 就是“从祖先 u 到所有后代的家族财富的异或”。  
- 切掉一根枝条就把某个家族（子树）独立出来。切两根枝条就会出现三块“家族”。我们只需要知道每块的财富（异或）就能算分数。

#### 代码（Python）

```python
from collections import defaultdict
from typing import List

def minimumScore(nums: List[int], edges: List[List[int]]) -> int:
    n = len(nums)
    g = defaultdict(list)
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # ---------- 1. DFS 预处理 ----------
    parent = [-1] * n          # 父节点
    depth  = [0] * n
    sub_xor = [0] * n          # 子树异或
    tin = [0] * n              # 进入时间
    tout = [0] * n
    timer = 0

    def dfs(u: int, p: int):
        nonlocal timer
        timer += 1
        tin[u] = timer
        parent[u] = p
        cur = nums[u]          # 先把自己的值计入
        for v in g[u]:
            if v == p:
                continue
            depth[v] = depth[u] + 1
            dfs(v, u)
            cur ^= sub_xor[v]   # 把子树的异或合并进来
        sub_xor[u] = cur
        timer += 1
        tout[u] = timer

    dfs(0, -1)                 # 任意选 0 为根

    total_xor = sub_xor[0]     # 整棵树的异或

    # ---------- 2. 辅助函数：判断 a 是否是 b 的祖先 ----------
    def is_ancestor(a: int, b: int) -> bool:
        return tin[a] < tin[b] and tout[b] < tout[a]

    # ---------- 3. 把每条边映射为 “子端” ----------
    childs = []                # 存储每条边的子节点（更深的那一端）
    for u, v in edges:
        if parent[u] == v:     # v 是 u 的父亲 → 子端是 u
            childs.append(u)
        else:                  # 否则 u 是 v 的父亲 → 子端是 v
            childs.append(v)

    best = float('inf')
    m = len(childs)            # = n-1

    # ---------- 4. 枚举两条边 ----------
    for i in range(m):
        a = childs[i]
        for j in range(i + 1, m):
            b = childs[j]

            # 先判断两条边是否有祖孙关系
            if not is_ancestor(a, b) and not is_ancestor(b, a):
                # 互不相交的两棵子树
                x = sub_xor[a]
                y = sub_xor[b]
                z = total_xor ^ x ^ y
            else:
                # 必然有一种是祖先
                if is_ancestor(a, b):
                    # a 是祖先，b 在 a 的子树里
                    x = sub_xor[b]                     # 最里面的子树
                    y = sub_xor[a] ^ sub_xor[b]        # a 的子树去掉 b 的部分
                    z = total_xor ^ sub_xor[a]         # 剩下的大块
                else:
                    # b 是祖先，a 在 b 的子树里
                    x = sub_xor[a]
                    y = sub_xor[b] ^ sub_xor[a]
                    z = total_xor ^ sub_xor[b]

            cur_score = max(x, y, z) - min(x, y, z)
            best = min(best, cur_score)

    return best
```

> **代码要点中文注释**  
> - `tin / tout`：相当于给每个节点贴上“进出时间戳”，用来快速判断祖先关系（类似“进出门卡”）。  
> - `childs`：每条边只需要记住 **子端**（更深的节点），因为删掉这条边等价于把以子端为根的子树“剪掉”。  
> - 两种情况的计算式直接使用预处理得到的 `sub_xor`，不需要再次遍历。  

#### 复杂度

- **时间复杂度**：`O(n²)`  
  - 解释：一次 DFS 为 `O(n)`，随后枚举所有边对是 `C(n‑1,2) ≈ n²/2`，每对只做常数次的异或和比较。  
  - 与暴力的 `O(n³)` 相比，省掉了每次重新遍历整棵树的开销。  
- **空间复杂度**：`O(n)`  
  - 解释：邻接表、父/深度/时间戳/子树异或等数组都随节点线性增长。

---

## 心得

- **核心技巧**：一次 DFS 预计算子树异或值 + 祖先判定（时间戳），从而在 **O(1)** 时间内得到任意两条边切除后的三块异或。  
- **适用的题型**  
  1. “在树上切除若干条边，使得得到的若干连通块满足某种属性”——如 **Maximum Score After Splitting a Binary Tree**（切一条边）等。  
  2. “子树信息需要快速合并/剔除”，常用 **子树前缀和 / 前缀异或** 技巧，如 **Path Sum IV**、**Tree of Coprimes**。  
- **一句话总结解题钥匙**：**把树根下来，一次遍历把每个子树的“总异或”算好，再用时间戳快速判断两条删边是否相交，所有组合即可在 O(1) 内求得分数。**

---

## 反思

- **第一反应**：看到“删两条边得到三块”，自然想到**枚举两条边**，但没有立刻想到利用子树的异或预处理来省掉重复遍历。  
- **最容易踩的坑**  
  1. **祖先关系判断错误**：若只比较深度会出错，必须用 `tin/tout` 或者“父链”来准确判断。  
  2. **把边当作无向处理**：在计算子树异或时，需要明确哪一端是子节点，否则 `sub_xor` 的含义会混乱。  
  3. **整数异或的范围**：`nums[i] ≤ 10⁸`，异或结果仍在 32 位整数范围，Python 无需担心溢出，但在某些语言要注意。  
- **下次类似题的第一步**：先**确定根**，做一次 DFS 收集**子树聚合信息**（和、异或、最大值等），再**依据这些信息枚举操作**（切边、加边、改值），这样往往能把时间复杂度从 `O(n³)` 降到 `O(n²)` 或更低。