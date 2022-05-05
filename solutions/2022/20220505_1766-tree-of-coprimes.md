# #1766. 互质树 / Tree of Coprimes

> 难度：困难 · 标签：Array、Math、Tree、Depth-First Search、Number Theory · [LeetCode 链接](https://leetcode.com/problems/tree-of-coprimes/)

---

## 题目（英文原版）

**Description**

There is a tree (i.e., a connected, undirected graph that has no cycles) consisting of n nodes numbered from 0 to n - 1 and exactly n - 1 edges. Each node has a value associated with it, and the root of the tree is node 0.
To represent this tree, you are given an integer array nums and a 2D array edges. Each nums[i] represents the ith node's value, and each edges[j] = [uj, vj] represents an edge between nodes uj and vj in the tree.
Two values x and y are coprime if gcd(x, y) == 1 where gcd(x, y) is the greatest common divisor of x and y.
An ancestor of a node i is any other node on the shortest path from node i to the root. A node is not considered an ancestor of itself.
Return an array ans of size n, where ans[i] is the closest ancestor to node i such that nums[i] and nums[ans[i]] are coprime, or -1 if there is no such ancestor.

**Examples**

**Example 1:**

```
Input: nums = [2,3,3,2], edges = [[0,1],[1,2],[1,3]]
Output: [-1,0,0,1]
Explanation: In the above figure, each node's value is in parentheses.
- Node 0 has no coprime ancestors.
- Node 1 has only one ancestor, node 0. Their values are coprime (gcd(2,3) == 1).
- Node 2 has two ancestors, nodes 1 and 0. Node 1's value is not coprime (gcd(3,3) == 3), but node 0's
  value is (gcd(2,3) == 1), so node 0 is the closest valid ancestor.
- Node 3 has two ancestors, nodes 1 and 0. It is coprime with node 1 (gcd(3,2) == 1), so node 1 is its
  closest valid ancestor.
```

**Example 2:**

```
Input: nums = [5,6,10,2,3,6,15], edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]
Output: [-1,0,-1,0,0,0,-1]
```

**Constraints**

- nums.length == n
- 1 <= nums[i] <= 50
- 1 <= n <= 105
- edges.length == n - 1
- edges[j].length == 2
- 0 <= uj, vj < n
- uj != vj

---

## 题目（中文翻译）

给定一棵树（即 **connected**、**undirected graph**，且不存在环）包含 `n` 个节点，编号为 `0` 到 `n - 1`，恰好有 `n - 1` 条边。每个节点都有一个关联的数值，树的根节点为 `0`。

为了表示这棵树，提供了整数数组 `nums` 和二维数组 `edges`。`nums[i]` 表示第 `i` 个节点的数值，`edges[j] = [uj, vj]` 表示节点 `uj` 与节点 `vj` 之间有一条边。

如果两个数 `x` 与 `y` 的最大公约数 `gcd(x, y) == 1`（其中 `gcd(x, y)` 为 `x` 与 `y` 的 **greatest common divisor**），则称它们互质（coprime）。

节点 `i` 的 **ancestor**（祖先）指的是从节点 `i` 到根节点的最短路径上除 `i` 本身之外的所有节点。节点不视为自己的祖先。

返回长度为 `n` 的数组 `ans`，其中 `ans[i]` 为离节点 `i` 最近的祖先，使得 `nums[i]` 与 `nums[ans[i]]` 互质；如果不存在这样的祖先，则返回 `-1`。

---

## 示例

### 示例 1

**输入**  
`nums = [2,3,3,2]`  
`edges = [[0,1],[1,2],[1,3]]`

**输出**  
`[-1,0,0,1]`

**解释**  
如图所示，括号内为每个节点的数值。  
- 节点 `0` 没有互质的祖先。  
- 节点 `1` 只有一个祖先 `0`，它们的数值互质 (`gcd(2,3) == 1`)。  
- 节点 `2` 有两个祖先 `1` 与 `0`。`1` 的数值与 `2` 不互质 (`gcd(3,3) == 3`)，但 `0` 的数值互质 (`gcd(2,3) == 1`)，因此最近的满足条件的祖先是 `0`。  
- 节点 `3` 的唯一祖先 `1` 与它的数值互质 (`gcd(3,2) == 1`)，所以答案为 `1`。

---

### 示例 2

**输入**  
`nums = [5,6,10,2,3,6,15]`  
`edges = [[0,1],[0,2],[1,3],[1,4],[2,5],[2,6]]`

**输出**  
`[-1,0,-1,0,0,0,-1]`

---

## 约束条件

- `nums.length == n`
- `1 <= nums[i] <= 50`
- `1 <= n <= 10^5`
- `edges.length == n - 1`
- `edges[j].length == 2`
- `0 <= uj, vj < n`
- `uj != vj`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**对每个节点 i，沿着它到根节点 0 的路径一直往上走，逐个检查祖先节点的值是否与 `nums[i]` 互质**（即 `gcd(nums[i], nums[anc]) == 1`），找到最近的那一个就可以了。  

- **数据结构**：我们只需要一条 `parent` 数组记录每个节点的直接父亲（因为树是无环的，根是 0），相当于在“家谱表”里查找父辈。  
- **为什么正确**：路径上所有的祖先都是唯一且顺序固定的，逐个检查自然能找到最近的满足条件的祖先。  

#### 代码（Python）

```python
from math import gcd
from collections import defaultdict, deque

def closestCoprimeAncestor_bruteforce(nums, edges):
    n = len(nums)
    # 1️⃣ 建立邻接表
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 2️⃣ BFS/DFS 求出每个节点的直接父亲（根是 0，父亲设为 -1）
    parent = [-1] * n
    order = [0]               # 用栈模拟 DFS
    while order:
        cur = order.pop()
        for nxt in g[cur]:
            if nxt == parent[cur]:
                continue
            parent[nxt] = cur
            order.append(nxt)

    # 3️⃣ 对每个节点向上遍历寻找最近的互质祖先
    ans = [-1] * n
    for i in range(n):
        cur = parent[i]      # 从直接父亲开始往上走
        while cur != -1:
            if gcd(nums[i], nums[cur]) == 1:   # 互质判定
                ans[i] = cur
                break                         # 找到最近的，直接停
            cur = parent[cur]                 # 继续往上
        # 根节点 0 没有祖先，保持 -1
    return ans
```

> 关键行解释  
> - `gcd(nums[i], nums[cur]) == 1` 判断两数是否互质，类似“找出两个数的最大公约数是否为 1”。  
> - `while cur != -1:` 是沿着父指针一直往上走，直到根的父亲（-1）为止。  

#### 复杂度  

- **时间复杂度**：`O(n²)`（最坏情况是链状树，节点 i 需要检查 `i` 个祖先，累计约 `1 + 2 + … + (n‑1) = O(n²)`）。  
  - 大白话：如果有 10 000 个节点，最坏要检查大约 10 000 × 5 000 ≈ 5 千万次，比起线性算法要慢很多。  
- **空间复杂度**：`O(n)` 用来存邻接表和 `parent` 数组。  

---

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于 **每个节点都要向上遍历所有祖先**。如果我们在遍历树的过程中 **把“当前路径上每种数值最近出现的节点”记下来**，就可以 **在 O(1)（实际上是遍历所有可能的数值）内直接得到最近的互质祖先**，不必逐个回溯。  

关键观察：

1. **数值范围很小**：`1 ≤ nums[i] ≤ 50`。这意味着我们可以把所有可能的数值（1~50）当作“颜色”，在遍历时维护一个大小为 51 的数组 `last[value]`，记录当前路径（从根到当前节点）上 **最近一次出现该数值的节点编号**。  
2. **同一个数值的多个祖先只保留最近的**：如果路径上已经有两个节点的值都是 7，离当前节点更近的那个一定是答案的候选，远的可以直接忽略。  
3. **寻找最近的互质祖先**：对于当前节点 `i`，只要遍历 `v = 1 … 50`，如果 `gcd(nums[i], v) == 1` 且 `last[v] != -1`，说明路径上有一个值为 `v` 的祖先。我们挑选 **深度（即在路径中出现的顺序）最大的那个**，它就是最近的互质祖先。  

实现步骤：

- **DFS（深度优先搜索）** 从根 0 开始遍历整棵树。  
- 进入节点 `u` 前，**先在 `last` 中查找最近的互质祖先**（遍历 1~50），得到 `ans[u]`。  
- **记录**：把 `u` 的数值 `nums[u]` 对应的 `last[nums[u]]` 保存为当前节点编号（覆盖之前的值），并记下它之前的旧值，用于回溯时恢复。  
- 递归遍历所有子节点。  
- **回溯**：子树遍历完后，把 `last[nums[u]]` 恢复为进入 `u` 前的旧值，确保其他分支看到的仍是正确的最近祖先。  

这相当于在 **一条从根到当前节点的“滑动窗口”** 中，随时维护每种数值的最新出现位置。  

#### 代码（Python）

```python
from math import gcd
from collections import defaultdict
import sys
sys.setrecursionlimit(200000)          # 防止递归深度超限

def closestCoprimeAncestor(nums, edges):
    n = len(nums)
    # 1️⃣ 建图（邻接表）
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u].append(v)
        g[v].append(u)

    # 2️⃣ 用来记录「当前路径上每个数值最近出现的节点」, -1 表示还没出现过
    last = [-1] * 51                     # 索引 1~50 有效

    ans = [-1] * n                       # 最终答案

    # 3️⃣ 深度优先搜索
    def dfs(u, parent):
        # -------- 查找最近的互质祖先 ----------
        best_node = -1
        best_depth = -1                  # 深度越大越靠近
        cur_val = nums[u]

        for v in range(1, 51):           # 只要遍历 1~50
            if gcd(cur_val, v) == 1 and last[v] != -1:
                # last[v] 保存的是最近出现 v 的节点编号
                # 为了找最近的，需要比较深度，这里用节点在路径中的顺序代替
                # depth 可以用 last[v] 本身的深度记录，这里用 ans_depth dict
                # 为简化，直接把出现的顺序（DFS 进入的顺序）当作深度
                # 因为我们在同一条路径上，后出现的必然更深
                if last[v] > best_depth:
                    best_depth = last[v]
                    best_node = last[v]

        ans[u] = best_node                # 若没有找到仍为 -1

        # -------- 更新 last 并继续向下 ----------
        # 记录旧值，回溯时要恢复
        old = last[cur_val]
        last[cur_val] = u                 # 当前节点成为该数值最近的出现

        for v in g[u]:
            if v == parent:
                continue
            dfs(v, u)

        # -------- 回溯：恢复之前的最近节点 ----------
        last[cur_val] = old

    dfs(0, -1)                           # 从根节点 0 开始
    return ans
```

> 关键行中文注释  
> - `last = [-1] * 51`：把「最近出现的节点」看成一本“字典”，键是数值（1~50），值是最近一次出现的节点编号。  
> - `for v in range(1, 51):`：遍历所有可能的数值，就像在字典里逐条查找。  
> - `if gcd(cur_val, v) == 1 and last[v] != -1:`：只有当 `v` 与当前节点值互质且已经出现过时，才可能是答案。  
> - `last[cur_val] = u`：把当前节点的数值登记到字典里，覆盖旧的记录。  
> - `last[cur_val] = old`：递归返回后，把字典恢复到进入该节点前的状态，确保兄弟子树不受影响。  

#### 复杂度  

- **时间复杂度**：`O(n * V)`，其中 `V = 50`（数值上限），等价于 `O(50n) = O(n)`。  
  - 对每个节点我们遍历 1~50 的所有可能数值一次，常数 50 非常小，整体线性随节点数增长。  
  - 与暴力解相比，省去了每条路径上可能上万次的祖先回溯。  

- **空间复杂度**：`O(V + h)`，`V = 51` 用来保存 `last`，`h` 是递归栈深度（最坏 `O(n)`，链状树时）。  
  - 实际上额外的记忆只是一张 51 长的数组，几乎可以忽略不计。  

---

## 心得  

- **核心技巧**：利用「数值范围小」这一点，在 DFS 过程中维护 **每个数值最近出现的节点**（相当于「滑动窗口」的哈希表）。  
- **适用的题型**：  
  1. **路径上最近满足某种属性的祖先**（如本题的互质、或相同颜色、或满足区间条件）。  
  2. **在树/图的遍历过程中，需要快速查询路径上某类信息的最近出现位置**（如最近出现的相同字符、最近的奇数节点等）。  
- **一句话总结**：  
  “在遍历树时，用一个大小固定的数组记录路径上每种数值的最新位置，就能在 O(1)（常数遍历）内找到最近的满足条件的祖先。”  

---

## 反思  

- **第一反应**：直接想到对每个节点向上遍历检查，写出暴力解。  
- **最容易踩的坑**：  
  - 忘记 **“同一个数值的多个祖先只保留最近的”**，导致在 `last` 中保存错误的节点，进而选出错误的答案。  
  - 回溯时没有恢复 `last`，会把子树的记录污染到其他分支。  
  - 递归深度过大时忘记调大 Python 的递归限制，会出现 `RecursionError`。  
- **下次类似题的第一步**：先检查数值或属性的取值范围是否足够小，若是，就考虑 **在 DFS/DFS 过程中维护一个“最近出现映射”**，把 “遍历祖先” 的过程转化为 “查询映射”。