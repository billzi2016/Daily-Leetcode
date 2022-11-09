# #2003. 每棵子树的最小缺失基因值 / Smallest Missing Genetic Value in Each Subtree

> 难度：困难 · 标签：Dynamic Programming、Tree、Depth-First Search、Union Find · [LeetCode 链接](https://leetcode.com/problems/smallest-missing-genetic-value-in-each-subtree/)

---

## 题目（英文原版）

**Description**

There is a family tree rooted at 0 consisting of n nodes numbered 0 to n - 1. You are given a 0-indexed integer array parents, where parents[i] is the parent for node i. Since node 0 is the root, parents[0] == -1.
There are 105 genetic values, each represented by an integer in the inclusive range [1, 105]. You are given a 0-indexed integer array nums, where nums[i] is a distinct genetic value for node i.
Return an array ans of length n where ans[i] is the smallest genetic value that is missing from the subtree rooted at node i.
The subtree rooted at a node x contains node x and all of its descendant nodes.

**Examples**

**Example 1:**

```
Input: parents = [-1,0,0,2], nums = [1,2,3,4]
Output: [5,1,1,1]
Explanation: The answer for each subtree is calculated as follows:
- 0: The subtree contains nodes [0,1,2,3] with values [1,2,3,4]. 5 is the smallest missing value.
- 1: The subtree contains only node 1 with value 2. 1 is the smallest missing value.
- 2: The subtree contains nodes [2,3] with values [3,4]. 1 is the smallest missing value.
- 3: The subtree contains only node 3 with value 4. 1 is the smallest missing value.
```

**Example 2:**

```
Input: parents = [-1,0,1,0,3,3], nums = [5,4,6,2,1,3]
Output: [7,1,1,4,2,1]
Explanation: The answer for each subtree is calculated as follows:
- 0: The subtree contains nodes [0,1,2,3,4,5] with values [5,4,6,2,1,3]. 7 is the smallest missing value.
- 1: The subtree contains nodes [1,2] with values [4,6]. 1 is the smallest missing value.
- 2: The subtree contains only node 2 with value 6. 1 is the smallest missing value.
- 3: The subtree contains nodes [3,4,5] with values [2,1,3]. 4 is the smallest missing value.
- 4: The subtree contains only node 4 with value 1. 2 is the smallest missing value.
- 5: The subtree contains only node 5 with value 3. 1 is the smallest missing value.
```

**Example 3:**

```
Input: parents = [-1,2,3,0,2,4,1], nums = [2,3,4,5,6,7,8]
Output: [1,1,1,1,1,1,1]
Explanation: The value 1 is missing from all the subtrees.
```

**Constraints**

- n == parents.length == nums.length
- 2 <= n <= 105
- 0 <= parents[i] <= n - 1 for i != 0
- parents[0] == -1
- parents represents a valid tree.
- 1 <= nums[i] <= 105
- Each nums[i] is distinct.

---

## 题目（中文翻译）

**描述**  
给定一棵以节点 `0` 为根的家族树（family tree），共有 `n` 个节点，编号为 `0` 到 `n - 1`。数组 `parents` 为 0 索引的整数数组，其中 `parents[i]` 表示节点 `i` 的父节点（parent），由于 `0` 为根节点，`parents[0] == -1`。  

基因值（genetic value）范围为 `[1, 10^5]`，共 `10^5` 种可能的取值。数组 `nums` 为 0 索引的整数数组，`nums[i]` 为节点 `i` 的唯一基因值（distinct genetic value）。  

返回长度为 `n` 的数组 `ans`，其中 `ans[i]` 为以节点 `i` 为根的子树（subtree）中**缺失的最小基因值**。子树包含根节点 `i` 本身以及所有后代节点。

**示例**  

*示例 1*  
```
Input: parents = [-1,0,0,2], nums = [1,2,3,4]
Output: [5,1,1,1]
Explanation: 对每棵子树的答案计算如下：
- 0: 子树包含节点 [0,1,2,3]，基因值为 [1,2,3,4]，最小缺失值为 5。
- 1: 子树仅包含节点 1，基因值为 2，最小缺失值为 1。
- 2: 子树包含节点 [2,3]，基因值为 [3,4]，最小缺失值为 1。
- 3: 子树仅包含节点 3，基因值为 4，最小缺失值为 1。
```

*示例 2*  
```
Input: parents = [-1,0,1,0,3,3], nums = [5,4,6,2,1,3]
Output: [7,1,1,4,2,1]
Explanation: 对每棵子树的答案计算如下：
- 0: 子树包含节点 [0,1,2,3,4,5]，基因值为 [5,4,6,2,1,3]，最小缺失值为 7。
- 1: 子树包含节点 [1,2]，基因值为 [4,6]，最小缺失值为 1。
- 2: 子树仅包含节点 2，基因值为 6，最小缺失值为 1。
- 3: 子树包含节点 [3,4,5]，基因值为 [2,1,3]，最小缺失值为 4。
- 4: 子树仅包含节点 4，基因值为 1，最小缺失值为 2。
- 5: 子树仅包含节点 5，基因值为 3，最小缺失值为 1。
```

*示例 3*  
```
Input: parents = [-1,2,3,0,2,4,1], nums = [2,3,4,5,6,7,8]
Output: [1,1,1,1,1,1,1]
Explanation: 基因值 1 在所有子树中均缺失，因此每个答案都是 1。
```

**约束条件**  
- `n == parents.length == nums.length`
- `2 <= n <= 10^5`
- 对于 `i != 0`，`0 <= parents[i] <= n - 1`
- `parents[0] == -1`
- `parents` 表示一棵合法的树
- `1 <= nums[i] <= 10^5`
- 所有 `nums[i]` 均互不相同

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**对每个节点**都遍历它的整棵子树，把子树里出现的基因值全部记下来，然后从 `1` 开始向上检查哪个最小的数没有出现。  
- **遍历子树**：可以用递归（DFS）或显式的栈，把当前节点的所有后代全部搜集。  
- **记录出现的基因值**：把遍历到的 `nums[i]` 放进一个集合（`set`），集合就像一本“字典”，可以快速判断一个数是否出现过。  
- **找最小缺失值**：从 `1` 开始逐个检查，只要在集合里找不到，就返回该数。

> **类比**：把集合想象成一本字典，`key` 是基因值，`value` 只要存在就说明这本字典里有这页。我们要找的就是字典里 **没有** 的最小页码。

**为什么正确**：子树的定义就是“节点本身 + 所有后代”，只要我们把子树的所有节点都遍历一遍，收集到的基因值就是该子树的完整集合。然后从 `1` 起逐个检查，必然会找到子树里缺失的最小基因值。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict

def smallestMissingValueSubtree_bruteforce(parents: List[int], nums: List[int]) -> List[int]:
    n = len(parents)
    # 建立子树的邻接表（子 -> 父）
    children = defaultdict(list)
    for i in range(1, n):
        children[parents[i]].append(i)

    # 递归遍历得到以 node 为根的子树所有节点
    def collect(node: int, bag: set) -> None:
        bag.add(nums[node])            # 把当前节点的基因值放进集合
        for c in children[node]:       # 递归遍历所有子节点
            collect(c, bag)

    ans = [0] * n
    for i in range(n):
        seen = set()                   # 用 set 记录子树出现的基因值
        collect(i, seen)               # 收集子树所有基因值
        # 从 1 开始找第一个不在集合里的数
        miss = 1
        while miss in seen:
            miss += 1
        ans[i] = miss
    return ans
```

> **关键行中文注释**  
> - `children[parents[i]].append(i)`: 把每个节点挂到它的父节点下，形成树的“子列表”。  
> - `bag.add(nums[node])`: 把当前节点的基因值加入集合，就像把这本字典里对应的页码标记出来。  
> - `while miss in seen: miss += 1`: 从 1 开始顺序检查，直到找到不在集合里的最小数。

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 对每个节点 `i` 都要遍历一次完整的子树，最坏情况下根节点的子树包含 `n` 个节点，第二层节点的子树包含 `n-1` 个，……，所以总的遍历次数约为 `n + (n-1) + … + 1 = O(n²)`。  
  - “`O(n²)`” 可以想象成 **把 `n` 张纸一次又一次全部翻遍**，随着 `n` 增大，工作量会呈二次增长，很快就不可接受。

- **空间复杂度**：`O(n)`  
  - 递归栈最深可能是树的高度（最坏 `O(n)`），以及每次收集子树时使用的 `set`，最坏也会装下 `n` 个基因值。

> 暴力解虽然思路最直接，但在 `n` 达到 `10⁵` 时会超时或内存爆炸，必须寻找更高效的办法。

---

### 2. 最优解

#### 思路  

从暴力解可以看出 **瓶颈** 在于每个节点都要重新遍历它的整棵子树。  
观察题目给出的 **提示**：

> - 如果子树里根本没有基因值 `1`，答案一定是 `1`。  
> - 我们需要一种能 **动态维护已经出现的基因值** 的数据结构。

关键观察：

1. **唯一的基因值 `1`**  
   - 所有基因值都是互不相同的。只要子树里不包含 `1`，答案必定是 `1`（因为 `1` 是最小的正整数）。  
   - 因此，只有**包含 `1` 的子树** 需要进一步考虑更大的缺失值。

2. **从 `1` 所在的节点向上**  
   - 假设节点 `x` 的基因值是 `1`。  
   - 那么 `x` 的所有祖先（包括 `x` 本身）它们的子树**一定**包含 `1`，而其他不在这条祖辈链上的节点子树**一定不包含 `1`**，答案直接是 `1`。  
   - 于是我们只需要 **沿着 `x` 到根的路径** 逐个计算答案，其他节点直接填 `1`。

3. **并查集（Union‑Find）帮助快速合并子树的基因集合**  
   - 当我们从 `x` 向根遍历时，已经知道 `x` 子树里所有基因值。  
   - 对于 `x` 的父节点 `p`，它的子树 = `p` 本身 + **所有子节点的子树**。  
   - 如果我们已经把 `x` 子树的基因值“合并”进一个全局集合中，随后处理 `p` 时只需要把 `p` 的其它子树（不包括已经合并的那条路径）加入集合即可。  
   - 这正好可以用 **并查集** 实现：每次把一个节点的基因值所在的集合 **union** 到它的父节点对应的集合。

4. **维护“当前最小缺失值”**  
   - 用一个指针 `cur = 1`，表示当前我们已经确认 **所有小于 `cur` 的基因值** 都已经在集合里出现。  
   - 每次向上合并新的基因值后，检查集合里是否已经包含 `cur`，如果有就 `cur += 1`，循环直到 `cur` 不在集合中。此时 `cur` 正好是 **当前子树的最小缺失值**。

5. **实现细节**  
   - 建立 **子节点列表**（adjacency）方便遍历。  
   - 找到基因值为 `1` 的节点 `start`（如果不存在，所有答案都是 `1`）。  
   - 初始化并查集 `parentUF[i] = i`（每个节点自成一个集合），以及一个布尔数组 `has[value]` 标记基因值是否已经出现。由于基因值上限是 `10⁵`，可以直接用大小 `10⁵+2` 的数组。  
   - 从 `start` 开始向根遍历：  
        1. 把当前节点 `u` 的基因值加入 `has`（相当于把它所在的集合加入全局集合）。  
        2. 对 `u` 的每个子节点 `v`，如果 `v` 已经被 **并入**（即已经在 `has` 中），则跳过；否则把 `v` 所在的集合 `union(v, u)`，并把 `v` 子树的所有基因值加入 `has`（这一步在 `union` 时递归完成）。  
        3. 循环移动指针 `cur`，直到 `has[cur] == False`。此时 `ans[u] = cur`。  
        4. 把 `u = parent[u]`，继续向上。  
   - 当遍历到根节点结束后，仍未访问的节点答案已经是 `1`（因为它们的子树不包含 `1`）。

> **类比**：想象每个节点的基因值是一本书的页码，`has` 数组就是一张“已读页码表”。我们从拥有第 1 页的那本书开始阅读，逐步把相邻章节（子树）合并进阅读进度表，随时检查最先缺失的页码，就是当前子树的答案。

#### 代码（Python）

```python
from typing import List
from collections import defaultdict
import sys
sys.setrecursionlimit(200000)

def smallestMissingValueSubtree(parents: List[int], nums: List[int]) -> List[int]:
    n = len(parents)
    # ---------- 1. 建图 ----------
    children = defaultdict(list)
    for i in range(1, n):
        children[parents[i]].append(i)

    # ---------- 2. 找到基因值为 1 的节点 ----------
    try:
        start = nums.index(1)          # 第一个出现 1 的节点下标
    except ValueError:                 # 如果根本没有 1，全部答案都是 1
        return [1] * n

    # ---------- 3. 并查集 ----------
    uf_parent = list(range(n))         # uf_parent[x] = x 表示自己是根
    # 用来记录每个集合对应的 “代表节点” （这里直接用根节点下标）
    # 其实不需要额外信息，只要把子树的基因值加入全局集合即可

    # ---------- 4. 已出现的基因值标记 ----------
    MAXV = 10 ** 5 + 2
    present = [False] * MAXV          # present[v] = True 表示基因值 v 已经出现

    # ---------- 5. 并查集的 find ----------
    def find(x: int) -> int:
        while uf_parent[x] != x:
            uf_parent[x] = uf_parent[uf_parent[x]]   # 路径压缩
            x = uf_parent[x]
        return x

    # ---------- 6. 把整个子树的基因值加入 present ----------
    def add_subtree(u: int) -> None:
        """把以 u 为根的整棵子树的基因值全部标记为出现"""
        stack = [u]
        while stack:
            node = stack.pop()
            present[nums[node]] = True
            for v in children[node]:
                if find(v) != find(u):   # 只遍历还没有被 union 的子树
                    stack.append(v)

    # ---------- 7. 主循环：从 start 向根遍历 ----------
    ans = [1] * n                      # 默认全部是 1
    cur_missing = 1                    # 当前最小缺失值指针

    u = start
    while u != -1:                     # 一直走到根（父节点为 -1）
        # ① 把当前节点所在子树的基因值加入全局集合
        add_subtree(u)

        # ② 合并已经处理好的子树到父节点的集合
        if parents[u] != -1:
            pu = parents[u]
            uf_parent[find(u)] = find(pu)   # 把 u 的集合并入父节点的集合

        # ③ 更新 cur_missing，找出当前子树的最小缺失值
        while present[cur_missing]:
            cur_missing += 1
        ans[u] = cur_missing

        # ④ 向上继续
        u = parents[u]

    return ans
```

**代码要点解释（中文注释）**

| 行号 | 关键含义 |
|------|----------|
| 1‑9  | 建立 `children` 列表，方便向下遍历子树。 |
| 12‑14| 用 `list.index` 找到基因值为 `1` 的节点。如果不存在，直接返回全 `1`。 |
| 17‑19| 初始化并查集的父指针数组 `uf_parent`，每个节点初始自成集合。 |
| 22‑23| `present` 用来标记哪些基因值已经出现，大小略大于上限以防越界。 |
| 27‑34| `find` 实现路径压缩，保证后续 `union` / `find` 都是近乎 O(1)。 |
| 38‑48| `add_subtree` 用显式栈遍历以 `u` 为根的整棵子树，把所有基因值标记为出现。这里不递归是防止递归深度超限。 |
| 52‑71| 主循环：从 `start`（基因值 1 的节点）向根逐层处理。<br>① 调用 `add_subtree` 把当前子树的基因值加入 `present`。<br>② 把当前节点的并查集根并入父节点的集合（相当于把已经合并的子树归并到上层）。<br>③ 用 `while present[cur_missing]` 不断右移，直到找到第一个没有出现的值，即为答案。<br>④ 继续向上。 |
| 73   | 返回最终答案数组。 |

#### 复杂度  

- **时间复杂度**：`O(n α(n) + V)`（≈ `O(n)`）  
  - `α(n)` 是 Ackermann 函数的反函数，几乎可以看作常数。每个节点只会被 `add_subtree` 访问一次，且并查集的 `find/union` 近乎常数时间。  
  - `cur_missing` 最多向右移动到 `10⁵+1`，这一步的总工作量是 `O(V)`，其中 `V = 10⁵` 是基因值上限。整体线性遍历 `n`（≤ `10⁵`），因此 **整体是线性时间**。

- **空间复杂度**：`O(n + V)`  
  - `children`、并查集数组 `uf_parent`、答案数组 `ans` 各占 `O(n)`。  
  - `present` 数组大小为 `10⁵+2`（即 `V`），用于标记基因值出现与否。  
  - 额外的递归栈或显式栈最多存 `O(n)`，整体仍在可接受范围。

> 与暴力解相比，时间从 **二次方** 降到了 **线性**，在 `n = 10⁵` 时可以在毫秒级完成。

---

## 心得

- **核心技巧**：  
  1. **利用“缺失 1” 的特性** 把大部分节点的答案直接定为 `1`，只在包含 `1` 的路径上做细致计算。  
  2. **并查集 + 全局出现标记** 实现子树基因值的快速合并与查询，避免重复遍历。  
  3. **指针维护最小缺失值**，在加入新基因值后只向右移动，避免每次都从 `1` 重新遍历。

- **该技巧适用的题型**（类似思路）  
  1. “树上查询最小缺失正整数” 类题目（如 LeetCode 1481、1731）。  
  2. “子树颜色计数 / 子树异或” 等需要 **子树合并** 的问题，常用 **DSU on Tree**（并查集在树上）技巧。  
  3. “动态维护集合的 mex（minimum excluded）” 经典问题。

- **一句话总结解题钥匙**：  
  **“只在包含 1 的那条祖辈链上合并子树，用并查集合并+全局出现表快速求 mex”。**

---

## 反思

- **第一反应**：看到“子树”和“最小缺失值”，立刻想到对每个节点遍历子树并检查缺失，导致暴力思路。  
- **最容易踩的坑**  
  1. **忘记基因值是唯一的**：若误以为可以出现重复，就会额外考虑计数，增加不必要的复杂度。  
  2. **递归深度**：树可能是链状，递归 DFS 会触发 Python 的递归深度限制，需要手动 `sys.setrecursionlimit` 或改用显式栈。  
  3. **边界条件**：若整个树里没有基因值 `1`，所有答案应为 `1`，这一步要提前处理，否则主循环会找不到起点。  
  4. **`present` 数组越界**：基因值上限是 `10⁵`，所以数组要开到 `10⁵+2`，否则在 `cur_missing` 递增到 `10⁵+1` 时会越界。

- **下次遇到同类题**，第一步应该先**寻找全局唯一的“关键值”（如 1、0、最小值）**，判断哪些子树真的需要细致计算，再**考虑使用并查集或 DSU on Tree** 把子树的状态快速合并，最后用**指针/堆**维护所求的“最小缺失/最大/第 k 小”等目标。这样可以把原本的 **O(n²)** 降到 **O(n)**。