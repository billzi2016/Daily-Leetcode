# #3600. 升级后最大化生成树的稳定性 / Maximize Spanning Tree Stability with Upgrades

> 难度：困难 · 标签：Binary Search、Greedy、Union Find、Graph、Minimum Spanning Tree · [LeetCode 链接](https://leetcode.com/problems/maximize-spanning-tree-stability-with-upgrades/)

---

## 题目（英文原版）

**Description**

You are given an integer n, representing n nodes numbered from 0 to n - 1 and a list of edges, where edges[i] = [ui, vi, si, musti]:
You are also given an integer k, the maximum number of upgrades you can perform. Each upgrade doubles the strength of an edge, and each eligible edge (with musti == 0) can be upgraded at most once.
The stability of a spanning tree is defined as the minimum strength score among all edges included in it.
Return the maximum possible stability of any valid spanning tree. If it is impossible to connect all nodes, return -1.
Note: A spanning tree of a graph with n nodes is a subset of the edges that connects all nodes together (i.e. the graph is connected) without forming any cycles, and uses exactly n - 1 edges.

**Examples**

**Example 1:**

```
Input: n = 3, edges = [[0,1,2,1],[1,2,3,0]], k = 1
Output: 2
Explanation:
```

**Example 2:**

```
Input: n = 3, edges = [[0,1,4,0],[1,2,3,0],[0,2,1,0]], k = 2
Output: 6
Explanation:
```

**Example 3:**

```
Input: n = 3, edges = [[0,1,1,1],[1,2,1,1],[2,0,1,1]], k = 0
Output: -1
Explanation:
```

**Constraints**

- 2 <= n <= 105
- 1 <= edges.length <= 105
- edges[i] = [ui, vi, si, musti]
- 0 <= ui, vi < n
- ui != vi
- 1 <= si <= 105
- musti is either 0 or 1.
- 0 <= k <= n
- There are no duplicate edges.

---

## 题目（中文翻译）

给定一个整数 `n`，表示编号为 `0` 到 `n‑1` 的 `n` 个节点；还有一个边列表 `edges`，其中 `edges[i] = [ui, vi, si, musti]`：

- `ui`、`vi` 是节点编号，`si` 表示该边的强度（strength），`musti` 为 `0` 或 `1`，`musti == 1` 的边是必须使用的边，`musti == 0` 的边可以选择升级。
- 你还得到一个整数 `k`，表示最多可以进行 `k 次升级。`每次升级会将一条可升级的边的强度翻倍（即乘以 `2`），且每条可升级的边（`musti == 0`）至多只能升级一次。

生成树（spanning tree）的**稳定性（stability）**定义为该生成树中所有边的强度的最小值。返回任意合法生成树的**最大可能稳定性**。如果无法使所有节点连通，则返回 `-1`。

> 注意：拥有 `n` 个节点的图的生成树是指恰好包含 `n‑1` 条边、连接所有节点且不形成环路的边的子集。

### 示例

**Example 1:**

```text
Input: n = 3, edges = [[0,1,2,1],[1,2,3,0]], k = 1
Output: 2
解释：
```

**Example 2:**

```text
Input: n = 3, edges = [[0,1,4,0],[1,2,3,0],[0,2,1,0]], k = 2
Output: 6
解释：
```

**Example 3:**

```text
Input: n = 3, edges = [[0,1,1,1],[1,2,1,1],[2,0,1,1]], k = 0
Output: -1
解释：
```

### 约束条件

- `2 <= n <= 10^5`
- `1 <= edges.length <= 10^5`
- `edges[i] = [ui, vi, si, musti]`
- `0 <= ui, vi < n`
- `ui != vi`
- `1 <= si <= 10^5`
- `musti` 只能为 `0` 或 `1`
- `0 <= k <= n`
- 不存在重复的边。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把所有**可能的**边组合都枚举一遍：  

1. 从 `edges` 中挑出恰好 `n‑1` 条边（因为生成树必须恰好有 `n‑1` 条边）。  
2. 对每一种挑选的方式，枚举哪些 **must = 0** 的边要升级（每条最多一次，且总升级次数 ≤ `k`）。  
3. 检查挑出的 `n‑1` 条边是否真的把所有 `n` 个节点连通且不出现环（这一步可以用 **并查集（Union‑Find）** 检测连通性）。  
4. 计算这棵生成树的 **稳定性**：所有边（升级后）强度的最小值。  
5. 记录所有合法组合的最大稳定性，即为答案。  

> **生活化类比**：把所有边想象成超市里的商品，每件商品都有一个原价 `s`，有的商品标记为 “必买”（`must = 1`），有的商品可以打一次 **2 倍** 的优惠（升级）。暴力解相当于把购物清单的每一种可能（挑哪些商品、哪些商品打优惠）都列出来，最后挑出“最贵的最便宜商品的价格最高”的那份清单。  

这种方法之所以**正确**，是因为它把**所有**合法的生成树都遍历到了，最大值自然不会错过。  

然而，这种做法的时间代价是 **指数级** 的：  

- 选 `n‑1` 条边的组合数是 `C(E, n‑1)`，`E` 最多 `10⁵`，根本不可算。  
- 对每一种组合，还要枚举升级方案（最多 `2^{(n‑1)}` 种），更是天文数字。  

**时间复杂度**：大约 `O( C(E, n‑1) * 2^{(n‑1)} )`，在最坏情况下几乎是 `O(2^{10⁵})`。  
**空间复杂度**：主要是递归/循环的临时存储，`O(n)`。  

> **大白话**：`O(2^{10⁵})` 就像把全世界的人每人都请去参加一次同一场派对，根本不可能完成。  

所以我们必须寻找**更聪明**的办法。

---

#### 代码（Python）  

下面给出一种只能在极小规模（比如 `n ≤ 10`）下跑通的暴力实现，供学习思路使用。  

```python
from itertools import combinations, product
from collections import defaultdict

# -------------------------------------------------
# 并查集（Union‑Find），用于判断是否连通且无环
class DSU:
    def __init__(self, n):
        self.fa = list(range(n))

    def find(self, x):
        # 路径压缩
        if self.fa[x] != x:
            self.fa[x] = self.find(self.fa[x])
        return self.fa[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:          # 已经在同一个集合，加入会形成环
            return False
        self.fa[ra] = rb
        return True
# -------------------------------------------------

def brute_max_stability(n, edges, k):
    """
    暴力搜索所有合法生成树，返回最大稳定性（仅适用于极小规模）。
    """
    best = -1
    # 1️⃣ 先挑出所有可能的 n-1 条边的组合
    for combo in combinations(edges, n - 1):
        # 2️⃣ 检查是否能构成树（连通且无环）
        dsu = DSU(n)
        ok = True
        for u, v, s, must in combo:
            if not dsu.union(u, v):
                ok = False          # 出现环
                break
        if not ok or len({dsu.find(i) for i in range(n)}) != 1:
            continue                # 不是一棵合法生成树

        # 3️⃣ 对所有 can‑upgrade（must==0）的边枚举升级情况
        upgradable_idx = [i for i, e in enumerate(combo) if e[3] == 0]
        for upgrade_mask in product([0, 1], repeat=len(upgradable_idx)):
            used = sum(upgrade_mask)
            if used > k:            # 超出升级上限
                continue
            # 计算每条边升级后的强度
            strengths = []
            for i, (u, v, s, must) in enumerate(combo):
                if must == 1:
                    strengths.append(s)          # 必须边不能升级
                else:
                    if upgrade_mask[upgradable_idx.index(i)] == 1:
                        strengths.append(s * 2)   # 升级一次
                    else:
                        strengths.append(s)
            stability = min(strengths)            # 最小强度即为稳定性
            best = max(best, stability)           # 取最大
    return best
```

> **注意**：上述代码仅用于演示“所有可能都要尝试”的思路，**切勿**在正式提交时使用，否则会直接超时。

---

#### 复杂度  

- **时间复杂度**：`O( C(E, n‑1) * 2^{(n‑1)} )`，指数级，实际不可接受。  
- **空间复杂度**：`O(n)`，主要是并查集的父指针数组。  

---

### 2. 最优解  

#### 思路  

从暴力解我们可以看到两个**瓶颈**：

1. **枚举组合**：我们不需要真的把所有边组合列出来，只要能够**判断**是否存在一棵满足条件的生成树即可。  
2. **枚举升级方案**：升级的本质是把某些边的强度翻倍，只要我们知道“**需要多少次升级**”就能判断可行性，而不必穷举每一种升级方式。

于是我们把问题转化为：

> 给定一个目标稳定性 `X`，**是否**能够在最多 `k` 次升级的前提下，构造一棵所有边（升级后）强度 **≥ X** 的生成树？

如果能够判断“可行/不可行”，我们就可以**二分**搜索 `X` 的最大值。  

---

##### 2.1 二分搜索 `X`  

- 稳定性最小可能是 `0`（不存在合法生成树时返回 `-1`），最大可能是 `max(s) * 2`（所有可升级的边都翻倍后）。  
- 在 `[low, high]` 区间上二分，每次取中点 `mid = (low + high + 1) // 2`（上取整），检查 `mid` 是否可行：  
  - 可行 → 把左区间收紧 `low = mid`（尝试更大）。  
  - 不可行 → 把右区间收紧 `high = mid - 1`。  
- 循环结束后，`low` 即为答案；若 `low == 0` 且连通性仍不满足，则返回 `-1`。

二分的次数是 `log₂(max(s) * 2) ≤ 18`（因为 `s ≤ 10⁵`），几乎可以忽略不计。

---

##### 2.2 检查函数 `check(X)`  

我们要判断：**在不超过 `k` 次升级的情况下，能否选出一棵所有边强度 ≥ `X` 的生成树**。  
核心思路：

1. **必须边（must = 1）**  
   - 这些边**必须**出现在生成树中（否则题目会说“必须使用”。如果它们形成环，显然不可能得到生成树）。  
   - 如果它们的原始强度 `s < X`，即使升级也不行（因为 `must = 1` 的边**不能升级**），直接返回 `False`。  
   - 使用并查集把这些必选边合并，如果出现环（`union` 失败），同样返回 `False`。  

2. **可选边（must = 0）**  
   - 对每条可选边，分三种情况：  
     - `s ≥ X` → **直接使用**（不消耗升级次数）。  
     - `s < X ≤ 2*s` → **需要升级一次**，才能满足 `X`。  
     - `X > 2*s` → **永远无法满足**，直接丢弃。  
   - 为了让升级次数尽可能少，我们**先尝试不升级的边**，再在必要时使用升级。  
   - 具体实现：把所有可选边按照原始强度 `s` **降序**排列（大强度的边更容易直接满足 `X`），遍历每条边：  
     - 若两端已经在同一个连通块，跳过（会形成环）。  
     - 否则如果 `s ≥ X`，直接 `union`。  
     - 否则（`s < X ≤ 2*s`），且还有剩余升级次数 `used < k`，升级后 `union`，并计数 `used += 1`。  
     - 否则无法使用这条边，继续遍历。  

3. **结束条件**  
   - 当已经成功加入 `n‑1` 条边（即并查集的连通块数变为 1）时，返回 `True`。  
   - 若遍历完所有边仍未连通，则返回 `False`。  

> **关键点**：  
> - **贪心**：先用“不需要升级”的边，因为它们不消耗宝贵的 `k` 次升级。  
> - **单调性**：如果某个 `X` 可行，那么所有小于 `X` 的值必定也可行；这正是二分搜索成立的依据。  

---

##### 2.3 并查集（DSU）实现  

- **路径压缩**：`find` 时把访问过的节点直接挂到根节点下，后续查询更快。  
- **按大小/秩合并**：把小集合挂到大集合下，保持树的高度尽可能低。  
- 这两点保证每次 `union`/`find` 的摊销时间为 **α(n)**（近似常数），足够快。

---

##### 2.4 完整算法流程  

```
max_weight = max(s for each edge)
high = max_weight * 2          # 可能的最大稳定性
low = 0

while low < high:
    mid = (low + high + 1) // 2   # 取上中位数，防止死循环
    if check(mid):                # 能否在 ≤k 次升级下得到强度 ≥mid 的生成树
        low = mid                 # 尝试更大
    else:
        high = mid - 1

if low == 0:          # 连通性仍然不满足
    return -1
return low
```

---

#### 代码（Python）

```python
# -------------------------------------------------
# 并查集（Union‑Find）实现
class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n          # 按大小合并

    def find(self, x):
        # 路径压缩
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:                 # 已经连通，加入会形成环
            return False
        # 按大小合并，保持树矮一点
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True
# -------------------------------------------------

def maximum_stability(n, edges, k):
    """
    返回最大可能的生成树稳定性（即所有边强度的最小值），
    若无法连通所有节点则返回 -1。
    """
    # ---------- 预处理 ----------
    max_s = max(s for _, _, s, _ in edges)
    lo, hi = 0, max_s * 2          # 稳定性取值范围

    # ---------- 检查函数 ----------
    def check(target):
        """能否在 ≤k 次升级的前提下，构造所有边强度 ≥ target 的生成树？"""
        dsu = DSU(n)
        used = 0                    # 已经使用的升级次数

        # 1️⃣ 必须边：must = 1
        for u, v, s, must in edges:
            if must == 1:
                if s < target:      # 必须边本身强度不足，直接失败
                    return False
                if not dsu.union(u, v):
                    return False    # 必须边形成环，生成树不可能

        # 2️⃣ 可选边：must = 0
        # 按原始强度降序遍历，方便先使用“大”边
        optional = [e for e in edges if e[3] == 0]
        optional.sort(key=lambda x: x[2], reverse=True)

        for u, v, s, _ in optional:
            if dsu.find(u) == dsu.find(v):
                continue            # 已经在同一个连通块，跳过防止环

            if s >= target:
                dsu.union(u, v)    # 直接使用，不消耗升级次数
            elif s * 2 >= target and used < k:
                dsu.union(u, v)    # 升级后使用
                used += 1
            # 否则这条边无论升级与否都达不到 target，直接丢弃

        # 检查是否已经连通所有节点
        # 只要根节点数量为 1 即可
        root = dsu.find(0)
        for i in range(1, n):
            if dsu.find(i) != root:
                return False
        return True

    # ---------- 二分搜索 ----------
    while lo < hi:
        mid = (lo + hi + 1) // 2    # 取上中位数，防止死循环
        if check(mid):
            lo = mid                # 目标可行，尝试更大
        else:
            hi = mid - 1            # 不可行，缩小上界

    # ---------- 结果 ----------
    return -1 if lo == 0 and not check(0) else lo
```

> **代码要点解释**  
> - `optional.sort(..., reverse=True)`：把强度大的可选边放前面，**先尝试**不需要升级的边，减少升级次数。  
> - `if s * 2 >= target and used < k`：只有在升级后能够满足目标并且还有升级额度时才使用。  
> - `check(0)` 在极端情况下用来判断图是否本身连通（即使目标为 0 也可能失败，因为必选边可能形成环），若连通则答案至少为 0，否则返回 `-1`。  

---

#### 复杂度  

- **二分搜索次数**：`O(log(max_s * 2)) ≤ 18`。  
- **每次检查 `check(X)`**：  
  - 必须边遍历一次，`O(E)`。  
  - 可选边先排序（一次 `O(E log E)`），随后线性遍历并做 `union/find`，每次摊销 `α(n)`（近似常数）。  
- **总时间复杂度**：`O(E log E * log maxWeight)`，在 `n, E ≤ 10⁵` 的限制下约为 `≈ 2·10⁶` 次操作，完全能跑在 1 秒左右。  
- **空间复杂度**：`O(n + E)`，主要是并查集的父指针数组和边的存储。  

> 与暴力解相比，时间从 **指数级** 降到了 **准线性**，是可以接受的。

---

## 心得  

- **核心技巧**：把“最大化最小值”转化为“判断阈值是否可行”，配合**二分搜索** + **贪心 + 并查集** 完成。  
- **适用场景**：  
  1. **最大化最小边权** 的生成树/路径问题（如 “最大最小路径”）。  
  2. 需要在有限资源（升级次数、费用等）约束下判断可行性的**阈值二分**。  
  3. 任何需要在 **图的连通性** 与 **资源消耗** 之间做权衡的题目（如 “最小费用连通图”）。  
- **解题钥匙**：**单调性 + 二分**。只要能证明“阈值 X 可行 ⇒ 所有更小阈值也可行”，二分搜索就能把原本的“枚举”问题压缩到对数级。

---

## 反思  

- **第一反应**：看到“最大化最小值”，自然想到**二分搜索**，因为这类“极值”往往具有单调性。  
- **最容易踩的坑**：  
  - **必选边形成环**：必须在检查函数里提前 `union`，若发现环立刻返回 `False`。  
  - **升级次数不足**：在贪心时必须先用不需要升级的边，避免提前消耗 `k`。  
  - **边界值**：`X` 可能大于所有 `2*s`，这时一定返回 `False`，二分上界要设为 `max(s)*2`。  
  - **连通性检查**：即使所有边都满足强度阈值，也可能因为必选边或升级次数限制导致仍然无法连通，需要最后遍历一次并查集确认根节点唯一。  
- **下次思路**：遇到类似“在资源限制下最大化/最小化某个阈值”的图论题目，第一步先**写出可行性检查**（常用并查集、DFS/BFS），再**二分**搜索答案。这样可以把复杂的组合搜索转化为若干次线性（或准线性）检查，极大降低时间复杂度。