# #2096. 二叉树节点之间的逐步指令 / Step-By-Step Directions From a Binary Tree Node to Another

> 难度：中等 · 标签：String、Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree with n nodes. Each node is uniquely assigned a value from 1 to n. You are also given an integer startValue representing the value of the start node s, and a different integer destValue representing the value of the destination node t.
Find the shortest path starting from node s and ending at node t. Generate step-by-step directions of such path as a string consisting of only the uppercase letters 'L', 'R', and 'U'. Each letter indicates a specific direction:
Return the step-by-step directions of the shortest path from node s to node t.

**Examples**

**Example 1:**

```
Input: root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6
Output: "UURL"
Explanation: The shortest path is: 3 → 1 → 5 → 2 → 6.
```

**Example 2:**

```
Input: root = [2,1], startValue = 2, destValue = 1
Output: "L"
Explanation: The shortest path is: 2 → 1.
```

**Constraints**

- The number of nodes in the tree is n.
- 2 <= n <= 105
- 1 <= Node.val <= n
- All the values in the tree are unique.
- 1 <= startValue, destValue <= n
- startValue != destValue

---

## 题目（中文翻译）

给定一棵拥有 **n** 个节点的二叉树 (binary tree) 的根节点 `root`。树中的每个节点都被唯一分配了从 `1` 到 `n` 的值。另给定整数 `startValue` 表示起始节点 **s** 的值，以及不同的整数 `destValue` 表示目标节点 **t** 的值。  

请找到从节点 **s** 出发、到达节点 **t** 的最短路径，并将该路径的逐步指令生成为仅包含大写字母 `'L'`、`'R'`、`'U'` 的字符串。每个字母的含义如下：

- `'L'`：向左子节点移动  
- `'R'`：向右子节点移动  
- `'U'`：向父节点移动  

返回上述最短路径对应的逐步指令字符串。

---

### 示例

#### 示例 1
**输入**  
```
root = [5,1,2,3,null,6,4], startValue = 3, destValue = 6
```
**输出**  
```
"UURL"
```
**解释**  
最短路径为：`3 → 1 → 5 → 2 → 6`，对应的指令序列为 `U`（从 3 到其父节点 1），`U`（从 1 到其父节点 5），`R`（从 5 到右子节点 2），`L`（从 2 到左子节点 6）。

#### 示例 2
**输入**  
```
root = [2,1], startValue = 2, destValue = 1
```
**输出**  
```
"L"
```
**解释**  
最短路径为：`2 → 1`，对应的指令为 `L`（从根节点 2 向左子节点 1 移动）。

---

### 约束条件
- 树中节点的数量为 `n`。  
- `2 <= n <= 10^5`  
- `1 <= Node.val <= n`  
- 树中所有值互不相同。  
- `1 <= startValue, destValue <= n`  
- `startValue != destValue`

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是把二叉树当成一张“无向图”，每条边既可以向左走，也可以向右走，还可以向父节点走（记作 `U`）。  
1. **先把树转换成邻接表**：  
   - 对每个节点记录它的左子节点、右子节点以及父节点（如果有的话）。  
   - 这一步就像把树的每个“房间”都装上了门，左门、右门、上门。  

2. **从起点 `s` 做一次 BFS（广度优先搜索）**，直到找到目标 `t`：  
   - BFS 会层层展开，最先到达 `t` 的路径一定是最短的（因为每走一步的代价都相同）。  
   - 在 BFS 过程中，用一个 `prev` 字典记录每个访问到的节点是从哪个方向来的，这样在找到 `t` 后就可以回溯得到完整路径。  

3. **把回溯得到的路径转换成题目要求的字符**：  
   - 如果是从父节点走到左子节点，用 `'L'`；走到右子节点，用 `'R'`；从子节点走到父节点，用 `'U'`。  

> **为什么暴力解一定正确？**  
> 树本身没有环，转成无向图后仍然是连通且无环的结构。BFS 在无权图里搜索最短路径是数学上已证明的最优策略，所以得到的路径一定是最短的。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

from collections import deque

def getDirections_bruteforce(root: TreeNode, startValue: int, destValue: int) -> str:
    # ---------- 第一步：把树转成邻接表 ----------
    # 用字典保存每个节点的邻居以及对应的移动字符
    # neighbor[node] = [(next_node, move_char), ...]
    neighbor = {}
    def dfs(node, parent):
        if not node:
            return
        neighbor[node.val] = []
        if parent:
            # 父节点可以向下走（L/R），子节点可以向上走（U）
            neighbor[node.val].append((parent.val, 'U'))   # 向上走
            # 为父节点也加一条向下的边（在后面的递归里会补全）
        if node.left:
            neighbor[node.val].append((node.left.val, 'L'))
        if node.right:
            neighbor[node.val].append((node.right.val, 'R'))
        dfs(node.left, node)
        dfs(node.right, node)
    dfs(root, None)

    # ---------- 第二步：BFS 找最短路径 ----------
    q = deque([startValue])
    visited = {startValue}
    # 记录每个节点是从哪个节点、用哪个字符到达的，便于回溯
    prev = {startValue: (None, '')}
    while q:
        cur = q.popleft()
        if cur == destValue:               # 找到目标，直接退出
            break
        for nxt, ch in neighbor.get(cur, []):
            if nxt not in visited:
                visited.add(nxt)
                prev[nxt] = (cur, ch)      # 记录路径信息
                q.append(nxt)

    # ---------- 第三步：回溯得到答案 ----------
    path = []
    node = destValue
    while node != startValue:
        parent, ch = prev[node]
        path.append(ch)                    # 逆序收集字符
        node = parent
    return ''.join(reversed(path))        # 正序返回
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 构造邻接表遍历全部 `n` 个节点。  
  - BFS 最坏也会访问所有节点一次。  
  - 用大白话说就是：每个节点只被看一次，和树的大小成线性关系。  

- **空间复杂度**：`O(n)`  
  - 邻接表需要保存每个节点的最多 3 条边（左、右、父），所以占用 `O(n)` 的额外内存。  
  - BFS 队列、`visited`、`prev` 这些额外结构也都是 `O(n)`。  

---

### 2. 最优解  

#### 思路  

暴力解虽然已经是 `O(n)`，但它额外构造了完整的邻接表并做了一次 BFS，实际实现略显繁琐。  
观察二叉树的结构，可以发现**任意两个节点的最短路径必定经过它们的最近公共祖先（LCA）**。  
因此我们可以把路径分成两段：

1. **从起点 `s` 向上走到 LCA**（全部用 `'U'`）。  
2. **从 LCA 向下走到终点 `t`**（用 `'L'` / `'R'` 表示左/右子树的方向）。

关键在于**快速得到根到 `s` 与根到 `t` 的路径字符串**，再通过比较找出它们的最长公共前缀——这段前缀正是根到 LCA 的路径。  

实现步骤如下：

1. **一次 DFS（深度优先搜索）**，记录从根到每个节点的路径字符串。  
   - 递归时把当前路径 `path` 传下去，左子节点加 `'L'`，右子节点加 `'R'`。  
   - 当访问到 `startValue` 或 `destValue` 时把对应的路径保存下来。  

2. **比较两条路径**，找出公共前缀的长度 `i`。  
   - `path_s[:i]` 与 `path_t[:i]` 完全相同，这段路径对应根 → LCA。  

3. **构造答案**：  
   - `path_s[i:]` 表示从 LCA 向下走到 `s`，但我们需要相反的方向，即全部改成 `'U'`（因为要先回到 LCA）。  
   - `path_t[i:]` 正好是从 LCA 向下走到 `t`，保持原样。  
   - 最终答案 = `'U' * len(path_s[i:]) + path_t[i:]`。  

> **核心概念解释**  
> - **LCA（最近公共祖先）**：想象树是一棵家族树，两个节点的最近公共祖先就是它们最近的共同“爷爷”。所有从 `s` 到 `t` 的路必须先回到这个“爷爷”，再下去。  
> - **前缀**：把路径看成一串文字（比如 `"LRL"`），两个路径的相同开头叫前缀。最长的相同开头，就是根到 LCA 的那段路。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def getDirections(root: TreeNode, startValue: int, destValue: int) -> str:
    # ---------- 第一步：DFS 找到根到 start 和 dest 的路径 ----------
    path_to_start = path_to_dest = None   # 最终会存字符串

    def dfs(node, cur_path):
        nonlocal path_to_start, path_to_dest
        if not node:
            return
        # 到达目标节点，保存路径
        if node.val == startValue:
            path_to_start = cur_path
        if node.val == destValue:
            path_to_dest = cur_path
        # 递归左、右子树，分别在路径后面加 'L' / 'R'
        dfs(node.left, cur_path + 'L')
        dfs(node.right, cur_path + 'R')

    dfs(root, "")   # 从根开始，路径为空串

    # ---------- 第二步：找最长公共前缀 ----------
    i = 0
    # 同时遍历两条路径，直到字符不相等或其中一条走完
    while i < len(path_to_start) and i < len(path_to_dest) and \
          path_to_start[i] == path_to_dest[i]:
        i += 1          # i 最终是公共前缀的长度

    # ---------- 第三步：拼接答案 ----------
    # LCA → start 需要全部变成 'U'
    up_moves = 'U' * (len(path_to_start) - i)
    # LCA → dest 保持原来的方向
    down_moves = path_to_dest[i:]
    return up_moves + down_moves
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只进行一次 DFS，遍历所有节点一次。  
  - 与树的规模线性相关，和暴力解相同，但没有额外的 BFS 与邻接表构造，常数更小。  

- **空间复杂度**：`O(h)`（递归栈）  
  - `h` 是树的高度，最坏情况下（链状树）为 `O(n)`，但一般情况下（平衡树）只有 `O(log n)`。  
  - 只保存两条路径的字符串，长度最多 `h`，因此总体空间仍是 `O(h)`。  

---

## 心得  

- **核心技巧**：利用二叉树的 **最近公共祖先（LCA）** 把路径拆分为 “上升” + “下降”。  
- **适用场景**：  
  1. 任意两节点最短路径必须经过 LCA（如 LeetCode 236. 二叉树的最近公共祖先）。  
  2. 需要把根到某节点的路径转换为指令或序列的题目（如 2096. 从二叉树的根到所有叶子节点的路径）。  
  3. 树上距离/路径查询的变形（如 1650. 低位计数器、LCA + 距离）。  
- **一句话总结解题钥匙**：**把“从 s 到 t 的路径”看成“先回到最近公共祖先，再从祖先走向 t”。**

---

## 反思  

- **第一反应**：直接把树当成无向图，用 BFS 找最短路径。思路完整但实现略显繁琐。  
- **最容易踩的坑**：  
  - 忘记把左、右子节点的方向分别记为 `'L'`、`'R'`，导致路径顺序错误。  
  - 在找公共前缀时只比较到最短路径长度，防止索引越界。  
  - 递归深度过大时可能导致栈溢出（Python 递归深度默认约 1000），需要在极端情况下改为显式栈或提升递归深度。  
- **下次类似题的第一步**：先思考“这棵树的结构有什么天然的分割点？”——往往是 LCA、根、或是某个子树的入口。找到分割点后，再把问题拆解成更容易处理的子问题。