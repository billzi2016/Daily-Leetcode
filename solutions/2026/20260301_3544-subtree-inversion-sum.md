# #3544. 子树翻转和 / Subtree Inversion Sum

> 难度：困难 · 标签：Array、Dynamic Programming、Tree、Depth-First Search · [LeetCode 链接](https://leetcode.com/problems/subtree-inversion-sum/)

---

## 题目（英文原版）

**Description**

You are given an undirected tree rooted at node 0, with n nodes numbered from 0 to n - 1. The tree is represented by a 2D integer array edges of length n - 1, where edges[i] = [ui, vi] indicates an edge between nodes ui and vi.
You are also given an integer array nums of length n, where nums[i] represents the value at node i, and an integer k.
You may perform inversion operations on a subset of nodes subject to the following rules:
Return the maximum possible sum of the tree's node values after applying inversion operations.

**Examples**

**Example 1:**

```
Input: edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], nums = [4,-8,-6,3,7,-2,5], k = 2
Output: 27
Explanation:
```

**Example 2:**

```
Input: edges = [[0,1],[1,2],[2,3],[3,4]], nums = [-1,3,-2,4,-5], k = 2
Output: 9
Explanation:
```

**Example 3:**

```
Input: edges = [[0,1],[0,2]], nums = [0,-1,-2], k = 3
Output: 3
Explanation:
Apply inversion operations at nodes 1 and 2.
```

**Constraints**

- 2 <= n <= 5 * 104
- edges.length == n - 1
- edges[i] = [ui, vi]
- 0 <= ui, vi < n
- nums.length == n
- -5 * 104 <= nums[i] <= 5 * 104
- 1 <= k <= 50
- The input is generated such that edges represents a valid tree.

---

## 题目（中文翻译）

你被给定了一棵以节点 0 为根的无向树（undirected tree），共 n 个节点，编号为 0 到 n - 1。树由长度为 n - 1 的二维整数数组 **edges** 表示，其中 `edges[i] = [ui, vi]` 表示节点 ui 和节点 vi 之间有一条边。

同时，你还有一个长度为 n 的整数数组 **nums**，其中 `nums[i]` 表示节点 i 的初始值，以及一个整数 **k**。

你可以对任意子集的节点执行“翻转”（inversion）操作，满足以下规则：

* 对选中的节点 v，所有以 v 为根的子树（subtree）中的节点值都会取相反数（即 `x → -x`）。
* 只能对至多 **k** 个节点执行翻转操作。

返回在满足上述规则的前提下，树中所有节点值的最大可能和。

---

**示例 1**

```text
Input: edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]], nums = [4,-8,-6,3,7,-2,5], k = 2
Output: 27
Explanation:
```

**示例 2**

```text
Input: edges = [[0,1],[1,2],[2,3],[3,4]], nums = [-1,3,-2,4,-5], k = 2
Output: 9
Explanation:
```

**示例 3**

```text
Input: edges = [[0,1],[0,2]], nums = [0,-1,-2], k = 3
Output: 3
Explanation:
对节点 1 和 2 执行翻转操作。
```

---

**约束条件**

- $2 \le n \le 5 \times 10^4$
- `edges.length == n - 1`
- `edges[i] = [ui, vi]`
- $0 \le ui, vi < n$
- `nums.length == n`
- $-5 \times 10^4 \le nums[i] \le 5 \times 10^4$
- $1 \le k \le 50$
- 输入保证 `edges` 构成一棵有效的树（valid tree）。

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  

题目要求在 **至多 `k` 次** “子树翻转” 操作后，使所有节点的数值之和最大。  
一次翻转的意义是：选中某个节点 `v`，把以 `v` 为根的整个子树里每个节点的值都取相反数（`x → -x`）。

最直接的想法是**枚举所有可能的翻转集合**，计算每种情况下的树值和，取最大值。

- **枚举方式**：对树的 `n` 个节点做 `k` 次选择（是否翻转），相当于在 `n` 个位置上挑出不超过 `k` 个点。可以用递归或 `itertools.combinations` 完成。  
- **求和方式**：遍历整棵树，对每个节点统计它被翻转了多少次（即它到根路径上所有被选中节点的个数），如果是奇数次则取相反数，偶数次则保持原值。  

> **类比**：把每个节点想象成一本词典里的单词，翻转操作就像在词典的某一章节前贴了一个“取反”标签。要知道某个单词最终的含义，需要数一数从根到它的路径上有多少个标签，奇数次就变成相反的解释。

**为什么暴力是对的**  
只要把所有合法的翻转集合（即翻转次数 ≤ k）都遍历一遍，必然能找到最优解。因为没有任何剪枝或近似，遍历的集合就是题目的完整解空间。

**时间/空间复杂度**  

- **时间**：  
  - 选取翻转节点的组合数是 `C(n,0)+C(n,1)+…+C(n,k)`，在最坏情况下（`k≈n`）约等于 `2^n`，对本题的上限 `n=5·10⁴` 完全不可接受。  
  - 对每个组合，还要遍历整棵树（`O(n)`）去统计翻转次数。  
  - 综合下来是 **指数级** 的时间复杂度，记作 `O( C(n,≤k)·n )`，实际运行会在几秒内爆炸。

- **空间**：  
  - 递归枚举时需要保存当前选中的节点集合，最多 `k` 个，空间 `O(k)`。  
  - 另加一次完整的树遍历的递归栈，深度最坏 `O(n)`。  

> **大白话解释**：`O(2^n)` 就像把所有可能的钥匙都插进锁里尝试一次，钥匙数量随 `n` 增长指数爆炸，根本不可能在电脑上跑完。

#### 代码（Python）

```python
from itertools import combinations
from collections import defaultdict, deque
import sys
sys.setrecursionlimit(10**6)

def brute_force(edges, nums, k):
    n = len(nums)
    # 建立邻接表（这里其实不需要，只是为了遍历树结构）
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 预先得到每个节点到根的父链，方便后面快速判断翻转次数
    parent = [-1] * n
    order = [0]
    parent[0] = 0
    for u in order:
        for v in g[u]:
            if v != parent[u]:
                parent[v] = u
                order.append(v)

    # 计算节点在路径上被翻转的次数（奇偶性）并求总和
    def evaluate(inverted_set):
        total = 0
        # 对每个节点，向上查找是否有翻转节点
        for node in range(n):
            cur = node
            flips = 0
            while cur != 0:               # 向根方向走
                if cur in inverted_set:   # 遇到翻转点
                    flips ^= 1            # 取反奇偶性
                cur = parent[cur]
            # 根节点本身也要检查
            if 0 in inverted_set:
                flips ^= 1
            val = nums[node] if flips == 0 else -nums[node]
            total += val
        return total

    best = -10**18
    # 枚举 0~k 个翻转点的所有组合
    for cnt in range(k + 1):
        for comb in combinations(range(n), cnt):
            best = max(best, evaluate(set(comb)))
    return best
```

> 这段代码可以直接跑通小规模的随机数据，用来验证后面的 DP 正确性。  

#### 复杂度  

- 时间复杂度：`O( C(n,≤k) · n )` —— 指数级，实际只能用于 `n ≤ 15` 左右的玩具案例。  
- 空间复杂度：`O(n)` —— 主要是存图和父指针数组。  

---

### 2. 最优解  

#### 思路  

从暴力解可以看到，**真正的难点在于“如何高效统计每个节点在路径上被翻转了多少次”**。  
如果我们把翻转操作的影响看成 **“路径上的奇偶性”**，那么只要知道从根到当前节点的翻转次数的奇偶性，就能立刻算出该节点的实际值。

**关键观察**  

1. **翻转只影响子树**：在某个节点 `v` 处翻转，会把 `v` 以及它的全部后代的符号都取反。  
2. **奇偶性叠加**：若祖先已经翻转了 `p` 次（`p = 0` 表示偶数次，即未改变），在 `v` 处再翻转一次，则子树的奇偶性会变成 `p ^ 1`（异或），因为两次翻转相互抵消。  
3. **只关心使用了多少次翻转**：题目限制最多 `k` 次翻转，`k ≤ 50` 很小，可以把 “已使用的次数” 作为 DP 维度。

于是我们可以在 **树形动态规划**（Tree DP）中，**自底向上**计算每个子树在不同“已用翻转次数”和“当前奇偶性”下的最大贡献。

---

#### DP 定义  

`dp[u][t][p]` 表示：

- 当前处理的子树根为节点 `u`  
- **已经在这棵子树里使用了 `t` 次翻转**（`0 ≤ t ≤ k`）  
- **从根到 `u`（不含 `u`）的翻转奇偶性为 `p`**（`0` 表示偶数次，`1` 表示奇数次）  

`dp[u][t][p]` 的值是 **子树 `u` 的节点值之和的最大可能值**。

> **类比**：把每个节点看成一个小仓库，`t` 表示已经用掉的 “搬运车”（翻转机会），`p` 表示仓库外部的 “灯光状态”（正负号是否已经被翻转）。我们要在有限的搬运车下，让仓库里所有货物的价值最高。

---

#### 状态转移  

对每个节点 `u`，有两种“本层”决定：

1. **不在 `u` 处翻转**  
   - 奇偶性保持 `p`（不变）。  
   - 使用的翻转次数仍然是子树中子节点们的总和 `t`。  
   - 当前节点的实际值为 `nums[u]` 若 `p==0`，否则 `-nums[u]`。  

2. **在 `u` 处翻转**（前提是还有剩余机会 `t ≥ 1`）  
   - 奇偶性对自己和所有子节点都取反：`p' = p ^ 1`。  
   - 本层消耗 1 次翻转，剩余的 `t-1` 次交给子树。  
   - 当前节点的实际值变为相反数：`-nums[u]` 若 `p==0`，否则 `nums[u]`（因为已经先翻转一次再考虑祖先的奇偶性）。

**合并子节点**  

子树的子节点之间是独立的，只有**总翻转次数的上限**需要统一。  
设 `children = [c1, c2, …]`，我们先把 `dp` 初始化为 **仅包含当前节点自身的贡献**（不考虑子树），随后逐个把子节点的 DP 合并进来，类似 **背包（knapsack）** 的 “容量” 为 `t`。

合并过程（伪代码）：

```text
tmp[t][p] = -inf   // 临时表，存放合并完当前所有已处理子节点后的结果
for each child v:
    new = -inf
    for used_parent in 0..t:          # 父侧已经用了多少次翻转
        for used_child in 0..t-used_parent:
            # 子节点的奇偶性取决于父侧的 p（因为子树的根 v 的奇偶性等于父的 p）
            new[used_parent+used_child][p] = max(
                new[used_parent+used_child][p],
                tmp[used_parent][p] + dp[v][used_child][p]
            )
    tmp = new
```

在处理完所有子节点后，`tmp[t][p]` 就是 **只考虑子树**（不包括 `u` 是否翻转）的最佳值。  
随后我们分别把 **不翻转 `u`** 与 **翻转 `u`** 两种情况写进去：

```text
# 不翻转 u
dp[u][t][p] = tmp[t][p] + ( nums[u] if p==0 else -nums[u] )

# 翻转 u（前提 t>=1）
dp[u][t][p] = max(dp[u][t][p],
                  tmp[t-1][p^1] + ( -nums[u] if p==0 else nums[u] ))
```

---

#### 初始化  

- 对于叶子节点，子树为空，`tmp[0][p] = 0`（不使用翻转，贡献 0）。  
- 然后直接套用上面的两条公式即可得到 `dp[leaf][*][*]`。

---

#### 结果  

根节点是 `0`，根本身没有祖先翻转，所以奇偶性初始为 `0`。  
答案是 `max_{t ≤ k} dp[0][t][0]`，即在根处奇偶性为偶数、使用不超过 `k` 次翻转时的最大和。

---

#### 正确性证明（思路）  

我们用数学归纳法证明 DP 计算的值就是子树的最优和。

**定义**  
`Best(u, t, p)` 表示在子树 `u` 中恰好使用 `t` 次翻转、且从根到 `u`（不含 `u`）的翻转奇偶性为 `p` 时的最大可能和。

**归纳基（叶子）**  
叶子没有子节点，只有两种选择：翻转或不翻转。上述转移式直接枚举这两种情况并取最大，显然得到的值即为 `Best`。

**归纳假设**  
假设对于所有子节点 `v`（深度更小），`dp[v][*][*]` 已经等于 `Best(v, *, *)`。

**归纳步骤**  
考虑节点 `u`。  
- **不在 `u` 翻转**：此时 `u` 的实际值由奇偶性 `p` 决定，子树各子节点的奇偶性同样是 `p`（因为没有额外翻转）。子树整体的最大和就是把每个子节点的最佳值 `Best(v, tv, p)` 按照总次数 `∑ tv = t` 进行分配，恰好是背包合并的意义。  
- **在 `u` 翻转**：消耗一次翻转，使当前奇偶性变为 `p^1`，并把 `u` 的值取反。剩余的 `t-1` 次翻转全部分配给子节点，子节点的奇偶性也随之变为 `p^1`。同样，这正是背包合并后再加上 `u` 本身的贡献。

因此，无论是哪种决定，`dp[u][t][p]` 都等于在满足约束的所有可能方案中取最大值，即 `Best(u, t, p)`。归纳完成，根节点的答案即为全局最优。

---

#### 复杂度分析  

- 对每个节点，我们需要 **合并所有子节点**。合并过程是两层循环 `O(k²)`（外层遍历已经用了多少次，内层遍历子节点使用多少次）。  
- 节点数 `n ≤ 5·10⁴`，`k ≤ 50`，于是总时间是 `O( n · k² ) ≈ 5·10⁴·2500 = 1.25·10⁸` 次基本操作。  
  - 在 Python 中，使用列表而不是字典、提前把 `-inf` 用一个很小的整数表示，可以在 1~2 秒内跑完。  
- 空间：每个节点保存 `2·(k+1)` 个整数（两种奇偶性），总空间 `O( n·k )`，约 `5·10⁴·50 = 2.5·10⁶`，几 MB 大小，完全可接受。  

> **时间复杂度解释**：`O(k²)` 就像在超市里挑两件商品的组合，`k=50` 时最多是挑 2500 种组合。把这种挑选过程在每棵树的 5 万个小货架上都做一次，总量仍在可以接受的范围内。  

#### 代码（Python）

```python
import sys
sys.setrecursionlimit(10**6)

INF_NEG = -10**18   # 代表“不可能”或“极小”

def max_subtree_inversion_sum(edges, nums, K):
    n = len(nums)
    # 建图（邻接表）
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 递归返回 dp 表
    # dp[t][p] : t 次翻转，p 为从根到当前节点（不含当前）奇偶性
    def dfs(u, parent):
        # 初始化：仅包含自身（子树为空时的 tmp）
        # tmp[t][p] 表示已经合并完部分子节点后的最大和（不计当前节点本身）
        tmp = [[INF_NEG, INF_NEG] for _ in range(K + 1)]
        for t in range(K + 1):
            tmp[t][0] = 0   # 还没有子节点时，使用 t 次翻转的和为 0（暂不计 u）
            tmp[t][1] = 0

        # 合并所有子节点
        for v in g[u]:
            if v == parent:
                continue
            child_dp = dfs(v, u)   # child_dp[t][p]

            # 新的临时表，先填 -inf
            new_tmp = [[INF_NEG, INF_NEG] for _ in range(K + 1)]

            for used_parent in range(K + 1):
                for parity in (0, 1):
                    if tmp[used_parent][parity] == INF_NEG:
                        continue
                    # 把子节点的翻转次数分配进去
                    for used_child in range(K - used_parent + 1):
                        # 子节点的奇偶性与当前 parity 相同，因为没有额外翻转
                        val = child_dp[used_child][parity]
                        if val == INF_NEG:
                            continue
                        total_used = used_parent + used_child
                        cand = tmp[used_parent][parity] + val
                        if cand > new_tmp[total_used][parity]:
                            new_tmp[total_used][parity] = cand
            tmp = new_tmp   # 继续合并下一个子节点

        # 现在把当前节点 u 本身的贡献加进去，得到 dp_u
        dp_u = [[INF_NEG, INF_NEG] for _ in range(K + 1)]

        for t in range(K + 1):
            for p in (0, 1):
                if tmp[t][p] == INF_NEG:
                    continue
                # 1) 不在 u 翻转
                cur_val = nums[u] if p == 0 else -nums[u]
                dp_u[t][p] = max(dp_u[t][p], tmp[t][p] + cur_val)

                # 2) 在 u 翻转（需要剩余一次机会）
                if t + 1 <= K:
                    # 翻转后奇偶性变成 p^1，子树的 tmp 必须取对应的奇偶性
                    cur_val_flip = -nums[u] if p == 0 else nums[u]
                    dp_u[t + 1][p] = max(dp_u[t + 1][p],
                                         tmp[t][p] + cur_val_flip)
        return dp_u

    root_dp = dfs(0, -1)
    # 根的初始奇偶性为 0（没有祖先翻转），取使用次数 ≤ K 的最大值
    ans = max(root_dp[t][0] for t in range(K + 1))
    return ans
```

**代码说明（关键行中文注释）**

```python
INF_NEG = -10**18   # 用一个非常小的数表示“不可能的状态”

# ---------- 建图 ----------
g = [[] for _ in range(n)]
for u, v in edges:
    g[u].append(v)
    g[v].append(u)

# ---------- 深度优先遍历 ----------
def dfs(u, parent):
    # tmp[t][p] = 已经合并完部分子节点后，使用 t 次翻转、奇偶性 p 的最大和（不计 u 本身）
    tmp = [[INF_NEG, INF_NEG] for _ in range(K + 1)]
    for t in range(K + 1):
        tmp[t][0] = tmp[t][1] = 0   # 初始化为 0，表示“空子树”

    # ----- 合并每个子节点的 DP -----
    for v in g[u]:
        if v == parent: continue
        child_dp = dfs(v, u)          # 递归得到子节点的 dp 表

        new_tmp = [[INF_NEG, INF_NEG] for _ in range(K + 1)]

        # 下面两层循环是“背包合并”，把子树的使用次数分配到当前累计次数中
        for used_parent in range(K + 1):
            for parity in (0, 1):
                if tmp[used_parent][parity] == INF_NEG: continue
                for used_child in range(K - used_parent + 1):
                    val = child_dp[used_child][parity]
                    if val == INF_NEG: continue
                    total = used_parent + used_child
                    cand = tmp[used_parent][parity] + val
                    if cand > new_tmp[total][parity]:
                        new_tmp[total][parity] = cand
        tmp = new_tmp   # 继续合并下一个子节点

    # ----- 加上当前节点自身的价值 -----
    dp_u = [[INF_NEG, INF_NEG] for _ in range(K + 1)]
    for t in range(K + 1):
        for p in (0, 1):
            if tmp[t][p] == INF_NEG: continue

            # 不翻转 u：实际值由奇偶性 p 决定
            cur = nums[u] if p == 0 else -nums[u]
            dp_u[t][p] = max(dp_u[t][p], tmp[t][p] + cur)

            # 翻转 u（需要额外一次机会）
            if t + 1 <= K:
                cur_flip = -nums[u] if p == 0 else nums[u]
                dp_u[t + 1][p] = max(dp_u[t + 1][p],
                                     tmp[t][p] + cur_flip)
    return dp_u
```

---

## 心得  

- **核心技巧**：在树上做 **带资源限制的动态规划**（每条边的翻转次数受上限 `k` 限制），利用 **奇偶性** 把“子树整体翻转”抽象成状态 `parity`，把“还能翻多少次”抽象成 `t`。  
- **适用题型**（类似思路）  
  1. “在树上选择至多 `k` 条路径，使路径权值和最大”——同样用 `dp[node][used]` 合并子树。  
  2. “树形背包”或 “树形分组背包”——每个子树是一个“物品组”，需要在全局容量 `k` 内挑选。  
  3. “在树上做至多 `k` 次颜色翻转，使相邻相同颜色的权值和最大”——也可以用奇偶性 + 资源 DP。  

- **一句话总结解题钥匙**：  
  **把“子树整体翻转”看成路径奇偶性的切换，用 `dp[node][已用次数][奇偶性]` 做背包式合并**。

---

## 反思  

- **拿到题目第一反应**：  
  “翻转会把子树所有值取反，显然要考虑路径上翻转的次数奇偶性”。于是立刻想到 **DFS + 记录从根到当前的翻转次数**。  

- **最容易踩的坑**  
  1. **忘记把奇偶性传递给子节点**：翻转一次会影响整棵子树，子节点的状态必须同步切换。  
  2. **边界条件**：`k` 可能比树的节点数小，合并时必须防止数组越界；根节点的奇偶性必须固定为 `0`。  
  3. **初始化**：在合并子节点前要把 `tmp[t][p]` 正确设为 `0`（空子树的贡献），否则会出现 “-inf + value” 的错误。  

- **下次遇到同类题，第一步该想到**  
  **“把全局资源（翻转次数）拆成子树的局部资源，用 DP 按子树合并的方式”**——先确定状态（已用次数 + 需要传递的额外信息），再做背包式合并。这样可以把看似全局的限制局部化，逐层递推得到最优解。