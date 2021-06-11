# #1361. 验证二叉树节点 / Validate Binary Tree Nodes

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Union Find、Graph、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/validate-binary-tree-nodes/)

---

## 题目（英文原版）

**Description**

You have n binary tree nodes numbered from 0 to n - 1 where node i has two children leftChild[i] and rightChild[i], return true if and only if all the given nodes form exactly one valid binary tree.
If node i has no left child then leftChild[i] will equal -1, similarly for the right child.
Note that the nodes have no values and that we only use the node numbers in this problem.

**Examples**

**Example 1:**

```
Input: n = 4, leftChild = [1,-1,3,-1], rightChild = [2,-1,-1,-1]
Output: true
```

**Example 2:**

```
Input: n = 4, leftChild = [1,-1,3,-1], rightChild = [2,3,-1,-1]
Output: false
```

**Example 3:**

```
Input: n = 2, leftChild = [1,0], rightChild = [-1,-1]
Output: false
```

**Constraints**

- n == leftChild.length == rightChild.length
- 1 <= n <= 104
- -1 <= leftChild[i], rightChild[i] <= n - 1

---

## 题目（中文翻译）

你有 `n` 个二叉树节点，编号为 `0` 到 `n - 1`，其中节点 `i` 的左子节点为 `leftChild[i]`，右子节点为 `rightChild[i]`。如果且仅如果所有给定的节点恰好构成一棵合法的二叉树，则返回 `true`。  
如果节点 `i` 没有左子节点，则 `leftChild[i]` 的值为 `-1`；右子节点同理。  
注意，这些节点没有额外的数值，我们在本题中只使用节点的编号。

**示例 1**  
**输入**: `n = 4`, `leftChild = [1,-1,3,-1]`, `rightChild = [2,-1,-1,-1]`  
**输出**: `true`

**示例 2**  
**输入**: `n = 4`, `leftChild = [1,-1,3,-1]`, `rightChild = [2,3,-1,-1]`  
**输出**: `false`

**示例 3**  
**输入**: `n = 2`, `leftChild = [1,0]`, `rightChild = [-1,-1]`  
**输出**: `false`

**约束条件**  
- `n == leftChild.length == rightChild.length`  
- `1 <= n <= 10^4`  
- `-1 <= leftChild[i], rightChild[i] <= n - 1`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**把每个节点都当作根节点尝试一次**，看能否遍历到所有 `n` 个节点且没有出现环。具体步骤如下：

1. **遍历所有节点 `i`（0 … n‑1）**，把 `i` 当作根。  
2. 从根 `i` 开始，用深度优先搜索（DFS）或广度优先搜索（BFS）遍历整棵树。  
3. 记录遍历过程中访问过的节点集合 `visited`。  
4. 若遍历结束后 `visited` 的大小恰好等于 `n`，说明以 `i` 为根可以覆盖全部节点且没有重复访问（即没有环），返回 `True`。  
5. 如果所有 `i` 都不满足条件，说明不存在合法的二叉树，返回 `False`。

> **类比**：把每个节点想象成一座城市，想知道哪座城市可以作为“唯一的首都”。我们把每座城市都当成首都，看看从这座城市出发能否走遍所有其他城市且不走回头路（环）。

**为什么正确**  
如果题目要求的二叉树真的存在，那么它必然有且仅有一个根节点。遍历所有可能的根节点必然会遍历到真正的根，届时 DFS/BFS 能访问到全部 `n` 个节点且不会出现环。反之，如果没有任何根能够满足这两个条件，则不存在合法二叉树。

**时间/空间复杂度**  
- 我们对每个节点都进行一次完整的遍历。一次遍历的时间是 `O(n)`，共 `n` 次，故总时间是 `O(n²)`。  
- 每次遍历需要一个 `visited` 集合，大小最多 `n`，所以空间是 `O(n)`（不计递归栈/队列的额外开销）。

> **大白话**：`O(n²)` 就像“每个人都要检查一次所有人的名单”，如果有 10,000 人，就要做 100,000,000 次检查，显然不够高效。

#### 代码（Python）

```python
from collections import deque
from typing import List

def validateBinaryTreeNodes_bruteforce(
    n: int, leftChild: List[int], rightChild: List[int]
) -> bool:
    # ---------------------------------------------------------
    # 1️⃣ 把每个节点都当作根尝试
    # ---------------------------------------------------------
    for root in range(n):
        visited = set()                # 记录已经走过的节点
        q = deque([root])              # BFS 队列，初始只有根

        # -------------------------------------------------
        # 2️⃣ BFS：层层展开，检查左右孩子是否已经访问过
        # -------------------------------------------------
        while q:
            node = q.popleft()
            if node in visited:        # 出现环，直接放弃这棵树
                break
            visited.add(node)

            left = leftChild[node]
            right = rightChild[node]

            if left != -1:             # -1 表示没有左孩子
                q.append(left)
            if right != -1:
                q.append(right)

        # -------------------------------------------------
        # 3️⃣ 检查是否遍历到了全部 n 个节点
        # -------------------------------------------------
        if len(visited) == n:          # 成功找到合法树
            return True

    # 所有根都不行，说明不存在合法二叉树
    return False
```

#### 复杂度

- **时间复杂度**：`O(n²)` — 每个节点都要完整遍历一次，等价于“每个人检查所有人的名单”。  
- **空间复杂度**：`O(n)` — `visited` 集合最多存 `n` 个节点，队列最多也会有 `n` 个节点。  

---

### 2. 最优解

#### 思路  

从暴力解可以看到，**重复遍历是主要瓶颈**。我们其实不需要把每个节点都当根，只要找到真正的根并一次遍历即可。要做到这一点，需要两个关键观察：

1. **每个节点只能有唯一的父节点**（二叉树的定义）。  
   - 如果某个节点出现了两个不同的父节点，说明出现了“两个家长”，必然不合法。  
   - 我们可以遍历 `leftChild`、`rightChild` 两个数组，记录每个节点的父节点（如果有的话）。这一步只需要 `O(n)`。

2. **合法二叉树恰好有且仅有一个根节点**（没有父节点的节点）。  
   - 在上一步得到的父节点数组中，`parent[i] == -1` 的节点就是候选根。若根的数量不是 1，则直接返回 `False`。

3. **根节点必须能遍历到所有节点且不能出现环**。  
   - 从唯一根出发，做一次 **DFS / BFS**，统计访问到的节点数。  
   - 如果访问数正好等于 `n`，说明树是连通的且没有环。否则（访问数 < n）说明有孤立节点或出现环。

> **类比**：把父节点数组想象成“每个人的父亲是谁”。合法的家族树要求每个人（除了祖先）只有一个父亲，且只能有 **一个** 祖先。找到祖先后，只要从祖先开始拜访全家，能拜访到每个人且不走回头路，就说明这棵家族树合法。

**核心数据结构**  

- **父节点数组 `parent`**（长度 `n`，初始值 `-1`）。  
  - 类比查字典：键是子节点，值是它的父节点。  
- **队列 / 栈** 用于 BFS/DFS，帮助我们一次性遍历所有节点。

**一步步的优化过程**  

| 步骤 | 暴力做法 | 优化后做法 | 说明 |
|------|----------|-----------|------|
| 找根 | 对每个节点都尝试 | 只遍历一次 `leftChild/rightChild`，记录父节点 | O(n) 替代 O(n²) |
| 检查环/连通性 | 每次遍历都重新检查 | 从唯一根做一次 DFS/BFS，记录已访问节点 | 只需要一次遍历 |
| 复杂度 | O(n²) 时间 | O(n) 时间 | 关键在于只遍历一次所有节点 |

#### 代码（Python）

```python
from collections import deque
from typing import List

def validateBinaryTreeNodes(n: int, leftChild: List[int], rightChild: List[int]) -> bool:
    """
    O(n) 时间、O(n) 空间的最优解
    """
    # -------------------------------------------------
    # 1️⃣ 统计每个节点的父节点（如果有的话）
    # -------------------------------------------------
    parent = [-1] * n          # -1 表示当前节点还没有父节点
    for i in range(n):
        for child in (leftChild[i], rightChild[i]):
            if child == -1:    # 空孩子，跳过
                continue
            if parent[child] != -1:   # 已经有父节点，出现“双亲”，非法
                return False
            parent[child] = i          # 记录 i 为 child 的父节点

    # -------------------------------------------------
    # 2️⃣ 找唯一的根（没有父节点的节点）
    # -------------------------------------------------
    roots = [i for i, p in enumerate(parent) if p == -1]
    if len(roots) != 1:        # 根不唯一（0 个或多个），非法
        return False
    root = roots[0]

    # -------------------------------------------------
    # 3️⃣ 从根出发 BFS，检查是否能遍历到全部 n 个节点
    # -------------------------------------------------
    visited = set()
    q = deque([root])
    while q:
        node = q.popleft()
        if node in visited:    # 说明出现环，非法
            return False
        visited.add(node)

        left = leftChild[node]
        right = rightChild[node]

        if left != -1:
            q.append(left)
        if right != -1:
            q.append(right)

    # -------------------------------------------------
    # 4️⃣ 最终判断：是否恰好访问了 n 个节点
    # -------------------------------------------------
    return len(visited) == n
```

#### 复杂度

- **时间复杂度**：`O(n)` — 只遍历两遍数组（统计父节点、BFS），相当于“每个人只检查一次”。相比暴力的 `O(n²)` 快很多。  
- **空间复杂度**：`O(n)` — 需要 `parent` 数组、`visited` 集合以及 BFS 队列，最坏都占用 `n` 个位置。

---

## 心得

- **核心技巧**：**父节点唯一性 + 唯一根 + 连通性检查**。这三个条件一起恰好描述了“一棵合法的二叉树”。  
- **适用场景**：  
  1. 判断一组有向边是否构成 **树结构**（如验证有向无环图是否是树）。  
  2. 判断 **父子关系表** 是否能组成唯一的家族树（公司组织结构、文件系统等）。  
  3. 需要判断 **图是否为森林中的单棵树**（例如 LeetCode 261. Graph Valid Tree）。  
- **一句话总结**：**先确保每个节点只有一个父亲，再确认唯一根并一次遍历全图**，这就是解这类“树合法性”题的钥匙。

---

## 反思

- **第一反应**：看到 “每个节点都有左/右孩子，用数字表示”，立刻想到要检查 **父子唯一性** 和 **根的唯一性**，因为二叉树的定义本身就暗含这两点。  
- **最容易踩的坑**：  
  - **重复父节点**：忘记在遍历 `leftChild/rightChild` 时检测同一子节点出现两次，会导致环或多父错误。  
  - **根的数量**：有时候所有节点都有父节点（形成环），这时根的数量为 0，需要单独处理。  
  - **孤立节点**：即使没有环且根唯一，但若有节点未被任何父子关系覆盖，也会导致访问不到全部节点。  
- **下次遇到类似题**：第一步先 **统计每个节点的父节点**，检查 **是否有多个父亲**，再 **找唯一根**，最后 **从根做一次遍历** 验证 **连通性**。这一步骤顺序基本适用于所有“是否是一棵合法树”的判定问题。