# #1719. 重构树的方案数 / Number Of Ways To Reconstruct A Tree

> 难度：困难 · 标签：Tree、Graph · [LeetCode 链接](https://leetcode.com/problems/number-of-ways-to-reconstruct-a-tree/)

---

## 题目（英文原版）

**Description**

You are given an array pairs, where pairs[i] = [xi, yi], and:
Let ways be the number of rooted trees that satisfy the following conditions:
Two ways are considered to be different if there is at least one node that has different parents in both ways.
Return:
A rooted tree is a tree that has a single root node, and all edges are oriented to be outgoing from the root.
An ancestor of a node is any node on the path from the root to that node (excluding the node itself). The root has no ancestors.

**Examples**

**Example 1:**

```
Input: pairs = [[1,2],[2,3]]
Output: 1
Explanation: There is exactly one valid rooted tree, which is shown in the above figure.
```

**Example 2:**

```
Input: pairs = [[1,2],[2,3],[1,3]]
Output: 2
Explanation: There are multiple valid rooted trees. Three of them are shown in the above figures.
```

**Example 3:**

```
Input: pairs = [[1,2],[2,3],[2,4],[1,5]]
Output: 0
Explanation: There are no valid rooted trees.
```

**Constraints**

- 1 <= pairs.length <= 105
- 1 <= xi < yi <= 500
- The elements in pairs are unique.

---

## 题目（中文翻译）

你得到一个数组 `pairs`，其中 `pairs[i] = [xi, yi]`，并且满足：

设 **ways** 为满足以下条件的根树（rooted tree）的数量：

- 两棵树如果至少有一个节点在两棵树中的父节点不同，则视为不同的方案。

返回 **ways**。

根树（rooted tree）是指只有唯一根节点的树，且所有边的方向均从根向外指向子节点。  
节点的祖先（ancestor）是指从根到该节点路径上除该节点本身之外的所有节点。根节点没有祖先。

**示例 1**  
**输入**: `pairs = [[1,2],[2,3]]`  
**输出**: `1`  
**解释**: 恰好只有一棵合法的根树，如上图所示。

**示例 2**  
**输入**: `pairs = [[1,2],[2,3],[1,3]]`  
**输出**: `2`  
**解释**: 存在多棵合法的根树。上图展示了其中的三棵。

**示例 3**  
**输入**: `pairs = [[1,2],[2,3],[2,4],[1,5]]`  
**输出**: `0`  
**解释**: 不存在合法的根树。

**约束条件**
- `1 <= pairs.length <= 10^5`
- `1 <= xi < yi <= 500`
- `pairs` 中的元素唯一。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**枚举所有可能的根节点和所有可能的父子关系**，然后检查每一种树是否满足题目给出的 `pairs`。  

- **数据结构**：可以把每棵候选树用「父指针数组」`parent[i]` 来存，`parent[i]` 表示节点 `i` 的父节点。  
- **检查方式**：遍历 `pairs`，只要有一对 `(x, y)` 在这棵树里既不是祖先也不是后代（即两者不在同一条根到叶子的路径上），就说明这棵树不合法。  

> **类比**：把每棵树想成一本家庭族谱，`pairs` 就像是“我和我祖先/后代的名单”。我们要把所有可能的族谱列出来，然后逐个核对名单是否完整。

**为什么暴力能得到正确答案**：只要把 **所有** 合法的根树都遍历一遍，肯定不会漏掉任何一种可能，也不会误判不合法的树。

**为什么会超时**：  
- 节点数最多 500，根的选法有 500 种。  
- 每棵树的父指针组合数是 `n^(n-1)`（类似 Cayley 公式），即使只遍历 `2^(n-1)` 种也已经天文数字。  
- 再加上每次检查要遍历全部 `pairs`（最多 1e5 条），时间会爆炸。

**时间/空间复杂度**（大白话）：

- **时间复杂度**：`O(所有可能的树 × pairs 数)`，这在最坏情况下相当于 **指数级**，也就是“几乎不可能在一分钟内算完”。  
- **空间复杂度**：`O(n)` 保存一棵树的父指针，几乎可以忽略不计。

> **O(n²) 是什么？**  
> 把 O 看成“数量级”，O(n²) 表示“随输入规模 n 增大，运行时间会像 n 的平方一样快”。比如 n=1000 时，O(n²) 大约是 1 000 000 次基本操作。相比之下，指数级 O(2ⁿ) 在 n=30 时已经是十亿级别，远远比 O(n²) 慢得多。

---

#### 代码（Python）

```python
# 暴力枚举（仅作思路演示，实际不可直接运行通过大数据）
from itertools import product

def brute(pairs):
    # 取所有出现的节点
    nodes = sorted({x for p in pairs for x in p})
    n = len(nodes)
    ans = 0

    # 1. 枚举根节点
    for root in nodes:
        # 2. 对其余 n-1 个节点，枚举它们的父节点（只能是已经出现的节点且不能形成环）
        # 这里用 product 简化，实际要加环检测、父子合法性等，代码会非常冗长
        for parents in product(nodes, repeat=n-1):
            # parents[i] 对应 nodes[i]（除根外）的父节点
            # …… 省略大量合法性检查 ……
            if check_tree(root, parents, pairs, nodes):
                ans += 1
    return ans
```

> **注意**：上面的代码仅用于说明「暴力」思路，实际运行会因为组合数太大而根本卡不住。

#### 复杂度  

- **时间复杂度**：`O(指数级)`，因为要遍历所有可能的树结构。  
- **空间复杂度**：`O(n)`，只需要保存一棵树的父指针数组。  

---

### 2. 最优解  

#### 思路  

**从暴力解出发，找瓶颈**：  
- 暴力枚举所有父指针是最大的开销。  
- 其实我们不需要真的去枚举，只要利用 `pairs` 本身的特性，就能直接推断出每个节点的父亲是谁（或者判断根本不存在合法树）。

**关键观察**  

1. **`pairs` 包含所有祖先‑后代关系**（不管是直接父子还是更远的祖先），所以如果两个节点之间 **没有** 出现在 `pairs` 中，它们 **不可能** 是祖先‑后代关系。  
2. 对于根节点 `r`，它与 **所有** 其它节点都有祖先‑后代关系（因为根是所有节点的祖先），于是 `r` 必须出现在 **每一** 对 `pairs` 中。换句话说，根的邻接集合（在 `pairs` 构成的无向图里）应当包含所有其它节点，度数 = `n‑1`。  
3. 对于任意非根节点 `u`，它的 **父节点** `p` 必须满足两个条件  
   - `p` 与 `u` 之间必然有祖先‑后代关系（即在 `pairs` 中），所以 `p` 必须是 `u` 的邻居。  
   - `p` 的邻接集合必须 **包含** `u` 的邻接集合。原因是：如果 `x` 与 `u` 有祖先‑后代关系，那么 `x` 与 `p` 也一定有（因为 `p` 是 `u` 的直接父亲，所有 `u` 的祖先/后代同样是 `p` 的祖先/后代）。于是 `adj[u] ⊆ adj[p]`。  

   进一步地，`p` 的度数一定 **严格大于** `u` 的度数（根的度数最大，父子之间度数递增），而 **最小** 的满足上述条件的邻居就是 `u` 的唯一父亲。  

4. 如果对某个节点 `u`，**有两个** 不同的邻居同时满足「度数最小且邻接集合是 `u` 的超集」的条件，则 `u` 可以选不同的父亲，导致 **多于一种** 合法的根树。  

5. 只要出现下面两种情况，题目答案就是 `0`（没有合法树）：  
   - 没有且仅有一个度数为 `n‑1` 的节点（根）。  
   - 某个非根节点找不到满足条件的父亲。  

**算法步骤**  

1. **构造邻接集合** `adj`（哈希表 + set），把每个 `pair = [x, y]` 当成无向边加入。  
2. 统计每个节点的度数 `deg[node] = len(adj[node])`。  
3. **找根**：度数等于 `n‑1` 的节点必须唯一，否则返回 `0`。  
4. 初始化答案 `ans = 1`（先假设唯一解）。  
5. 对每个非根节点 `u`：  
   - 在 `adj[u]` 中遍历所有邻居 `v`，挑选满足 `deg[v] > deg[u]` 且 `adj[u] ⊆ adj[v]` 的候选父亲。  
   - 记录这些候选中 **最小的度数** `min_deg`，以及出现的次数 `cnt`。  
   - 如果 `cnt == 0` → 找不到父亲，直接返回 `0`。  
   - 如果 `cnt > 1` → 说明有多种父亲选择，`ans = 2`（题目只要求返回 0、1、2，2 表示「不止一种」）。  
6. 最终返回 `ans`。  

**为什么时间能接受**  

- `pairs` 的数量上限是 `1e5`，所以总的邻接条目不超过 `2·1e5`。  
- 对每个节点，我们只遍历它的邻居（度数），而集合包含关系 `adj[u] ⊆ adj[v]` 可以在 `O(min(deg[u], deg[v]))` 时间内完成。  
- 整体时间复杂度约为 `O(∑ deg[u] * avg_check)`，在最坏情况下仍然是 `O(|pairs|·log|pairs|)` 或更低，完全能够在 1 秒内跑完。  

---

#### 代码（Python）

```python
from collections import defaultdict

class Solution:
    def checkWays(self, pairs):
        """
        返回 0 / 1 / 2，分别表示
        0：不存在合法的根树
        1：唯一合法的根树
        2：存在多于一种合法的根树
        """

        # 1️⃣ 建图：邻接集合（无向图）
        adj = defaultdict(set)          # node -> set of its neighbors
        nodes = set()
        for x, y in pairs:
            adj[x].add(y)
            adj[y].add(x)
            nodes.update([x, y])

        n = len(nodes)                   # 节点总数

        # 2️⃣ 计算每个节点的度数
        deg = {node: len(adj[node]) for node in nodes}

        # 3️⃣ 找根：唯一度数为 n-1 的节点
        roots = [node for node, d in deg.items() if d == n - 1]
        if len(roots) != 1:              # 没有根或根不唯一
            return 0
        root = roots[0]

        answer = 1   # 先假设唯一

        # 4️⃣ 对每个非根节点，寻找父亲
        for u in nodes:
            if u == root:
                continue

            # 记录候选父亲的最小度数以及出现次数
            min_parent_deg = float('inf')
            cnt_min = 0

            for v in adj[u]:                     # v 必须是 u 的邻居
                if deg[v] <= deg[u]:
                    continue                     # 父亲的度数必须更大
                # 检查邻接集合的包含关系：adj[u] ⊆ adj[v] ?
                # 只要 u 本身不在 v 的集合里，就不满足（因为 u 与 v 已是邻居）
                # 使用 set.issubset 进行 O(min) 检查
                if adj[u].issubset(adj[v]):
                    if deg[v] < min_parent_deg:
                        min_parent_deg = deg[v]
                        cnt_min = 1
                    elif deg[v] == min_parent_deg:
                        cnt_min += 1

            # 4️⃣1️⃣ 没有任何满足条件的父亲 → 不合法
            if cnt_min == 0:
                return 0
            # 4️⃣2️⃣ 有多个最小度数的候选父亲 → 可能出现多种树
            if cnt_min > 1:
                answer = 2      # 只要出现一次就说明答案不是唯一

        return answer
```

> **代码要点注释**  
> - `defaultdict(set)` 相当于“字典里的每个键默认对应一个空集合”，像是 **查字典** 时自动创建新页面。  
> - `adj[u].issubset(adj[v])` 读取为“集合 `adj[u]` 是集合 `adj[v]` 的子集”，即 **所有跟 `u` 有祖先‑后代关系的节点**，在 `v` 那里也都有。  
> - `deg[v] > deg[u]` 确保父亲的邻居数比子节点多，根的度数最大，形成层层递减的 “度数梯度”。  

#### 复杂度  

- **时间复杂度**：`O(|pairs| + Σ_{u} deg[u] * min(deg[u], min_parent_deg))`，在最坏情况下约为 `O(|pairs|·log|pairs|)`，实际运行时几乎是线性的。  
  - 通俗解释：我们只遍历一次输入的所有“关系对”，再对每个节点检查它的邻居，检查的工作量和节点的邻居数量成正比。  
- **空间复杂度**：`O(|pairs|)` 用于存储邻接集合（每条关系存两次），再加上若干 `O(n)` 的辅助数组。  

---

## 心得  

- **核心技巧**：利用“度数最大的是根，父子关系通过邻接集合的包含关系唯一确定”。本质上把 **祖先‑后代对集合** 看成一种 **层级约束**，通过集合包含来推导父子。  
- **适用的题型**  
  1. **根据全部祖先‑后代关系恢复唯一树**（如本题）。  
  2. **从所有边的子集恢复树结构**（如“从部分父子对恢复唯一根树”）。  
  3. **利用度数信息判断根节点或唯一中心**（如“寻找无向树的中心节点”）。  
- **一句话总结解题钥匙**：**根的度数是 n‑1，父亲是“度数更大且邻接集合是子集的最小度数邻居”。**  

---

## 反思  

- **第一反应**：看到 “pairs 包含所有祖先‑后代对”，立刻想到把它当成无向图来处理，寻找根节点。  
- **最容易踩的坑**  
  1. **遗漏集合包含检查**：仅靠度数比较会误判，需要显式检查 `adj[u] ⊆ adj[v]`。  
  2. **根不唯一的情况**：若出现两个度数为 `n‑1` 的节点，答案必须是 `0`。  
  3. **特殊节点只有一个邻居**：此时父亲必然是唯一的邻居，但仍要验证集合包含。  
- **下次类似题的第一步**：**先把所有节点的“出现次数/度数”统计出来，找出唯一的“最大度数”节点（根），再用集合包含关系逐层确定父子**。这样可以把搜索空间从指数级直接压到线性。