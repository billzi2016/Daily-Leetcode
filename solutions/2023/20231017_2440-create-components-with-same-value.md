# #2440. 创建价值相同的组件 / Create Components With Same Value

> 难度：困难 · 标签：Array、Math、Tree、Depth-First Search、Enumeration · [LeetCode 链接](https://leetcode.com/problems/create-components-with-same-value/)

---

## 题目（英文原版）

**Description**

There is an undirected tree with n nodes labeled from 0 to n - 1.
You are given a 0-indexed integer array nums of length n where nums[i] represents the value of the ith node. You are also given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that there is an edge between nodes ai and bi in the tree.
You are allowed to delete some edges, splitting the tree into multiple connected components. Let the value of a component be the sum of all nums[i] for which node i is in the component.
Return the maximum number of edges you can delete, such that every connected component in the tree has the same value.

**Examples**

**Example 1:**

```
Input: nums = [6,2,2,2,6], edges = [[0,1],[1,2],[1,3],[3,4]] 
Output: 2 
Explanation: The above figure shows how we can delete the edges [0,1] and [3,4]. The created components are nodes [0], [1,2,3] and [4]. The sum of the values in each component equals 6. It can be proven that no better deletion exists, so the answer is 2.
```

**Example 2:**

```
Input: nums = [2], edges = []
Output: 0
Explanation: There are no edges to be deleted.
```

**Constraints**

- 1 <= n <= 2 * 104
- nums.length == n
- 1 <= nums[i] <= 50
- edges.length == n - 1
- edges[i].length == 2
- 0 <= edges[i][0], edges[i][1] <= n - 1
- edges represents a valid tree.

---

## 题目（中文翻译）

存在一棵 **无向树（undirected tree）**，共有 `n` 个节点，编号为 `0` 到 `n - 1`。  
给定一个长度为 `n`、下标从 `0` 开始的整数数组 `nums`，其中 `nums[i]` 表示第 `i` 个 **节点（node）** 的值。  
同时给定一个长度为 `n - 1` 的二维整数数组 `edges`，其中 `edges[i] = [a_i, b_i]` 表示在树中存在一条连接节点 `a_i` 与节点 `b_i` 的 **边（edge）**。

你可以删除若干条 **边（edges）**，从而将原树划分为多个 **连通分量（connected component）**。  
定义一个 **分量（component）** 的 **值（value）** 为该分量中所有节点的 `nums[i]` 之和。

返回能够删除的 **边（edges）** 的最大数量，使得树中每个 **连通分量（connected component）** 的 **值（value）** 都相等。

---

### 示例

#### 示例 1
```
输入: nums = [6,2,2,2,6], edges = [[0,1],[1,2],[1,3],[3,4]]
输出: 2
解释: 如图所示，我们可以删除边 `[0,1]` 和 `[3,4]`。得到的分量为节点 `[0]`、`[1,2,3]` 和 `[4]`。每个分量的值之和均为 `6`。可以证明不存在更好的删除方案，因此答案为 `2`。
```

#### 示例 2
```
输入: nums = [2], edges = []
输出: 0
解释: 没有可删除的边。
```

---

### 约束条件

- `1 <= n <= 2 * 10^4`
- `nums.length == n`
- `1 <= nums[i] <= 50`
- `edges.length == n - 1`
- `edges[i].length == 2`
- `0 <= edges[i][0], edges[i][1] <= n - 1`
- `edges` 构成一棵有效的树。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把每一条边都当成可以删或不删的开关**，  
把所有的 `n‑1` 条边枚举成 0/1（不删/删）的组合，然后检查得到的每个连通块的节点值之和是否全部相等。

- **枚举方式**：用一个长度为 `n‑1` 的二进制掩码 `mask`，第 `i` 位为 1 表示删掉 `edges[i]`，为 0 表示保留这条边。  
- **连通块的获取**：枚举完一套 `mask` 后，用 **并查集（Union‑Find）** 把仍然相连的节点合并，最后每个并查集的根节点代表一个连通块。并查集就像一本“查字典”，词是节点，页码是它所属的集合根。
- **检查相等**：遍历所有节点，把它们的值累加到各自根节点对应的 `sum[root]` 中。把所有块的和放进一个集合，若集合大小为 1，则说明所有块的和相等。

**为什么正确**：  
我们穷举了 **所有可能的删边方案**，只要有一种方案满足条件，就一定会在枚举过程中被发现。于是返回的最大删边数一定是所有可行方案中最大的。

#### 代码（Python）

```python
from itertools import product

def maxDeletion_bruteforce(nums, edges):
    n = len(nums)
    m = len(edges)                     # m == n-1
    best = 0

    # 2^(m) 种删边方式，用二进制 mask 表示
    for mask in range(1 << m):
        # ---------- 并查集 ----------
        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a, b):
            ra, rb = find(a), find(b)
            if ra != rb:
                parent[rb] = ra

        # 根据 mask 合并仍然相连的节点
        for i, (u, v) in enumerate(edges):
            if not (mask >> i) & 1:          # 第 i 条边没有被删掉
                union(u, v)

        # ---------- 计算每个连通块的和 ----------
        comp_sum = {}
        for i, val in enumerate(nums):
            r = find(i)                     # 该节点所在块的根
            comp_sum[r] = comp_sum.get(r, 0) + val

        # ---------- 检查是否所有块的和相等 ----------
        sums = set(comp_sum.values())
        if len(sums) == 1:                  # 所有块的和相同
            deletions = bin(mask).count('1')
            best = max(best, deletions)

    return best
```

> 关键行注释已经写在代码里，直接跑 `maxDeletion_bruteforce(nums, edges)` 即可得到答案。

#### 复杂度

- **时间复杂度**：`O(2^{n-1} * (n + α(n)))`  
  - `2^{n-1}` 是所有可能的删边组合（每条边两种选择）。  
  - 对每个组合我们要跑一次并查集，时间近似线性 `O(n)`（`α(n)` 是 Ackermann 反函数，几乎可以当作常数）。  
  - 用大白话说，就是 **指数级**，当 `n` 超过 15 左右就已经不可接受了。

- **空间复杂度**：`O(n)`  
  - 主要是并查集的 `parent` 数组和 `comp_sum` 字典。

> 这就是“暴力”解法——思路最直白，但在实际数据规模（`n ≤ 2·10⁴`）下根本跑不完。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在 **枚举所有删边方案**，这一步的复杂度是指数级的。  
观察题目可以发现：

1. **所有连通块的和必须相同**，设为 `S`。  
2. 整棵树的总和 `T = sum(nums)` 必须能够被 `S` 整除，且 `components = T / S`。  
3. 删掉一条边只会把 **一个子树**（以被删边的下方节点为根）变成一个独立的连通块。  

所以我们不需要枚举每条边是否删掉，而是 **从根节点向下遍历**，看每个子树的累计和是否已经等于目标值 `S`：

- 如果 **子树和 == S**，说明这棵子树可以独立成块，我们可以“剪掉”连向父节点的那条边。剪掉后，这棵子树对父节点的贡献变成 0（因为已经算作一个完整块了）。
- 如果 **子树和 < S**，则这棵子树必须继续和父节点一起组成更大的块，向上返回它的和。
- 如果 **子树和 > S**，说明目标 `S` 不可能实现，直接失败。

> 这相当于把每个子树的和 “模” `S`（取余），如果最终根节点返回的余数为 0 并且恰好切出了 `components` 块，就说明 `S` 可行。

**关键点**：`S` 必须是 **total sum 的约数**。总和 `T ≤ 50 * 2·10⁴ = 10⁶`，约数的个数最多几百个（远小于 `n`），因此我们只需要尝试这些候选 `S`。

**完整步骤**：

1. 计算总和 `T = sum(nums)`。  
2. 生成 `T` 的所有约数 `S`（即可能的块和），并按 **从大到小的块数**（即 `components = T / S`）遍历——因为我们要 **最大化删边数**（等价于最大化块数）。  
3. 对每个 `S`，做一次 **DFS**（递归或栈）：
   - 返回值 `sub` 为当前子树累计的和（如果已经切掉则返回 0）。  
   - 若 `sub == S`，计数 `cnt += 1`，返回 0。  
   - 若 `sub > S`，直接返回一个大于 `S` 的标记，表示失败。  
4. DFS 结束后检查 `cnt == components`（根节点的返回值也应该是 0），若成立则 `S` 可行，答案为 `components - 1`（删边数 = 块数 - 1）。因为我们是从大块数到小块数遍历的，第一次成功的就是最大删边数。

#### 代码（Python）

```python
from collections import defaultdict
import sys
sys.setrecursionlimit(10**6)          # 防止递归太深

def maxDeletion(nums, edges):
    n = len(nums)
    # ---------- 建图 ----------
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    total = sum(nums)

    # ---------- 求所有约数 ----------
    divisors = []
    i = 1
    while i * i <= total:
        if total % i == 0:
            divisors.append(i)               # i 是约数
            if i * i != total:
                divisors.append(total // i)  # 对应的另一个约数
        i += 1

    # 按块数从大到小遍历（块数 = total // S），等价于删边数从大到小
    # 为了让「先找到最大删边数」更直观，排序时把块数（components）降序
    candidates = sorted(divisors, key=lambda s: total // s, reverse=True)

    # ---------- DFS 检查 ----------
    def can_split(target):
        """返回 (是否成功, 已经切出的块数)"""
        cnt = 0                         # 已经独立成块的子树个数

        def dfs(u, parent):
            nonlocal cnt
            cur = nums[u]               # 当前子树的和，先加上自己
            for v in g[u]:
                if v == parent:
                    continue
                sub = dfs(v, u)        # 子树返回的和
                if sub == -1:          # 下面已经发现不可能
                    return -1
                cur += sub
            if cur == target:           # 正好可以成为一个块
                cnt += 1
                return 0                # 对父节点而言贡献为 0
            if cur > target:            # 超过目标块和，直接失败
                return -1
            return cur                  # 继续向上累加

        res = dfs(0, -1)
        # 成功的必要条件：根返回 0（说明根也恰好形成块），且切出的块数等于 total//target
        return res == 0 and cnt == total // target

    # ---------- 主循环 ----------
    for s in candidates:
        if can_split(s):
            # 组件数 = total // s，删边数 = 组件数 - 1
            return total // s - 1

    # 理论上总能返回 0（不删任何边），这里作为保险
    return 0
```

**代码要点解释**：

- `g` 用邻接表存树，类似“城市的路网”。  
- `divisors` 是总和的所有约数，就像“把总钱数平分成若干份的所有可能的每份金额”。  
- `cnt` 记录已经成功切出的块数；每当子树和恰好等于目标 `target` 时，就把它视作一个完整的块并把返回值设为 `0`，相当于“把这块从父树上剪下来”。  
- `dfs` 返回值 `-1` 表示在该子树下面已经发现 **不可能**（和超过目标），一路向上快速终止。  

#### 复杂度

- **时间复杂度**：`O(n * d)`，其中 `d` 是 `total` 的约数个数。  
  - 对每个约数我们遍历一次全部 `n` 个节点做 DFS。  
  - `total ≤ 10⁶`，约数个数最多约 240（实际更少），所以最坏约为 `2·10⁴ * 240 ≈ 4.8·10⁶`，在 1 秒左右可以轻松通过。  
  - 用大白话说：我们把指数级的 **“枚举每条边”** 替换成 **“枚举几百个可能的块和”**，每次只跑一次线性遍历，速度快了好几倍。

- **空间复杂度**：`O(n)`  
  - 邻接表 `g`、递归栈（最深 `n`）以及少量辅助变量。  

> 与暴力解相比，时间从 **指数级** 降到了 **线性乘以约数个数**，这就是本题的关键优化点。

---

## 心得

- **核心技巧**：**利用总和的约数 + DFS 统计子树和**，把“能否等分”转化为“每个子树的和是否恰好等于目标”。  
- **适用的题型**  
  1. **树形分割**，要求每个连通块满足相同的数值约束（如 LeetCode 1466. Reorder Routes to Make All Paths Lead to the City Zero）。  
  2. **分割数组/链表成相同和的子段**（如“划分数组使每段和相等”）。  
  3. **分割图（尤其是森林）使每个连通块属性相同**（如“把图切成若干等权子图”）。  
- **一句话总结解题钥匙**：  
  > **“把目标块和限制为总和的约数，随后在一次 DFS 中把每个恰好等于目标的子树剪下来”。**

---

## 反思

- **第一反应**：直接想枚举删边的组合，想到“遍历所有子集”。这在小数据时可以接受，却忽视了 `n` 可达两万的规模。  
- **最容易踩的坑**  
  1. **忘记检查根节点的剩余和**：即使所有子树都成功切成块，根节点的累计和仍需等于目标，否则整体不合法。  
  2. **约数的生成顺序**：若不按 “块数从大到小”（即目标块和从小到大）遍历，可能会先得到一个不是最大删边数的答案。  
  3. **递归深度**：树是链状时递归深度会达到 `n`，需要手动调高递归限制或改用显式栈。  
  4. **整数溢出**：本题 `nums[i] ≤ 50`，总和不会超过 10⁶，Python 自然不溢出，但在某些语言需要用 `long long`。  

- **下次遇到同类题**，第一步应该：  
  > **“先把全局约束（总和、总节点数）转化为可枚举的候选目标”，再用一次线性遍历/DFS 检验每个目标是否可行”。**  

这样即可把原本指数级的搜索压缩到可接受的多项式范围。