# #2458. 子树删除查询后二叉树的高度 / Height of Binary Tree After Subtree Removal Queries

> 难度：困难 · 标签：Array、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/height-of-binary-tree-after-subtree-removal-queries/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree with n nodes. Each node is assigned a unique value from 1 to n. You are also given an array queries of size m.
You have to perform m independent queries on the tree where in the ith query you do the following:
Return an array answer of size m where answer[i] is the height of the tree after performing the ith query.
Note:

**Examples**

**Example 1:**

```
Input: root = [1,3,4,2,null,6,5,null,null,null,null,null,7], queries = [4]
Output: [2]
Explanation: The diagram above shows the tree after removing the subtree rooted at node with value 4.
The height of the tree is 2 (The path 1 -> 3 -> 2).
```

**Example 2:**

```
Input: root = [5,8,9,2,1,3,7,4,6], queries = [3,2,4,8]
Output: [3,2,3,2]
Explanation: We have the following queries:
- Removing the subtree rooted at node with value 3. The height of the tree becomes 3 (The path 5 -> 8 -> 2 -> 4).
- Removing the subtree rooted at node with value 2. The height of the tree becomes 2 (The path 5 -> 8 -> 1).
- Removing the subtree rooted at node with value 4. The height of the tree becomes 3 (The path 5 -> 8 -> 2 -> 6).
- Removing the subtree rooted at node with value 8. The height of the tree becomes 2 (The path 5 -> 9 -> 3).
```

**Constraints**

- The number of nodes in the tree is n.
- 2 <= n <= 105
- 1 <= Node.val <= n
- All the values in the tree are unique.
- m == queries.length
- 1 <= m <= min(n, 104)
- 1 <= queries[i] <= n
- queries[i] != root.val

---

## 题目（中文翻译）

给定一棵包含 n 个节点的二叉树的根节点 **root**。树中的每个节点都有唯一的取值，范围为 1 到 n。另给定一个长度为 m 的数组 **queries**。

你需要对这棵树执行 m 个相互独立的查询。对于第 i 个查询，执行以下操作：

- 删除值为 queries[i] 的节点以及它所在的子树（subtree）。

返回一个长度为 m 的数组 **answer**，其中 **answer[i]** 为执行第 i 个查询后剩余树的高度（height）。

---

### 示例

#### 示例 1
**输入**  
```
root = [1,3,4,2,null,6,5,null,null,null,null,null,7], queries = [4]
```
**输出**  
```
[2]
```
**解释**  
上图展示了删除值为 4 的节点所在的子树后的树结构。此时树的高度为 2（路径为 1 -> 3 -> 2）。

#### 示例 2
**输入**  
```
root = [5,8,9,2,1,3,7,4,6], queries = [3,2,4,8]
```
**输出**  
```
[3,2,3,2]
```
**解释**  
我们依次执行以下查询：

- 删除值为 3 的节点所在的子树。此时树的高度变为 3（路径为 5 -> 8 -> 2 -> 4）。
- 删除值为 2 的节点所在的子树。此时树的高度变为 2（路径为 5 -> 8 -> 1）。
- 删除值为 4 的节点所在的子树。此时树的高度为 3（路径为 5 -> 8 -> 9 -> 7）。
- 删除值为 8 的节点所在的子树。此时树的高度为 2（路径为 5 -> 9 -> 7）。

（示例说明已截断，以上为已给出的部分翻译）

---

### 约束条件

- 树中节点的数量为 n。
- 2 ≤ n ≤ 10^5
- 1 ≤ Node.val ≤ n
- 树中所有节点的取值互不相同。
- m = queries.length
- 1 ≤ m ≤ min(n, 10^4)
- 1 ≤ queries[i] ≤ n
- queries[i] ≠ root.val

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**对每一个查询单独遍历整棵树**，把要删除的子树全部跳过，只在其余节点中找出离根最远的那个节点，根到它的距离就是“删除子树后树的高度”。  

- **数据结构**：我们只需要普通的二叉树节点 (`TreeNode`) 和一个集合 `removed` 来记录本次查询要剔除的所有节点的值。把集合想象成 **字典**，key 是节点的编号，value（这里不用）相当于字典里对应的“页码”。查字典的时间是 O(1)，这正是我们判断某个节点是否被删掉的方式。  
- **为什么正确**：树的高度定义为“根到最远叶子节点的边数”。只要把要删除的子树的所有节点都视为不存在，剩下的节点仍然保持原来的父子关系，根到每个保留下来的叶子的路径长度不变。遍历所有保留下来的节点，取最大路径长度，就是答案。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def tree_height_after_removal(root: TreeNode, queries: list[int]) -> list[int]:
    """暴力解：对每个查询 O(n)"""
    # 先把每个节点的深度算出来，后面遍历时直接使用
    depth = {}

    def dfs(node: TreeNode, d: int) -> None:
        if not node:
            return
        depth[node.val] = d                # 记录节点到根的距离
        dfs(node.left, d + 1)
        dfs(node.right, d + 1)

    dfs(root, 0)

    # 计算每个查询的答案
    ans = []
    for q in queries:
        # 把以 q 为根的子树全部加入集合（相当于“删掉”它们）
        removed = set()

        def collect(node: TreeNode) -> None:
            if not node:
                return
            removed.add(node.val)
            collect(node.left)
            collect(node.right)

        # 找到要删除的节点（这里用一次 DFS 找到对应的对象）
        def find(node: TreeNode) -> TreeNode | None:
            if not node:
                return None
            if node.val == q:
                return node
            return find(node.left) or find(node.right)

        target = find(root)
        collect(target)

        # 在剩余节点里找最大深度
        max_depth = 0
        for v, d in depth.items():
            if v not in removed:           # 只看没有被删掉的节点
                max_depth = max(max_depth, d)
        ans.append(max_depth)

    return ans
```

> **代码要点**  
> 1. 第一次 DFS 把每个节点到根的距离（`depth`）算好，后面查询时直接使用。  
> 2. `collect` 把要删除的子树的所有节点值加入集合 `removed`，相当于“把它们从树里搬走”。  
> 3. 最后遍历所有节点的深度，取最大值即为答案。

#### 复杂度  

- **时间复杂度**：`O(n·m)`  
  - 第一次遍历算深度是 `O(n)`（只做一次）。  
  - 对每个查询，我们需要把对应子树的所有节点收集进集合（最坏 `O(n)`），随后再遍历全部节点找最大深度（`O(n)`），所以每个查询 `O(n)`，共 `m` 次。  
  - 用大白话说：如果树有 10⁵ 个节点，查询有 10⁴ 条，最坏情况要跑 **10⁹ 次**的简单操作，显然会超时。  

- **空间复杂度**：`O(n)`  
  - `depth`、`removed`、递归栈等都需要线性空间。  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每次都要遍历整棵树**。其实我们可以在 **一次遍历** 里把每个节点对应的答案都算好，随后每个查询只要 O(1) 地查表即可。

关键观察：

1. **树的高度 = 根到最远叶子节点的距离**。  
2. 删除某个子树后，根仍然不变，**答案就是“根到所有不在被删子树里的节点的最大距离”**。  
3. 换句话说，我们只需要知道 **每个节点之外的最大深度**（即不在该节点子树里的节点的最大深度）。记作 `up_max_depth[node]`。  
4. `up_max_depth[node]` 可以用**树的重根 DP（reroot DP）**一次算完：  
   - 先算每个节点在自己子树里的最大深度 `sub_max_depth[node]`（等价于 `depth[node] + height_subtree[node]`）。  
   - 再从根向下传播，计算每个节点“外面的最大深度”。对某个孩子 `c` 来说，**外面的节点**有三类：  
     * 根及其祖先（已经在 `up_max_depth[parent]` 里），  
     * 父节点本身（深度 `depth[parent]`），  
     * 父节点的另一个子树（如果有），其最大深度是 `sub_max_depth[sibling]`。  
   - 取这三者的最大值，就是 `up_max_depth[c]`。  

下面把上述过程拆成两次 DFS：

| 步骤 | 目的 | 用到的变量 |
|------|------|------------|
| **第一遍 DFS** | 计算每个节点的深度 `depth` 与子树最高深度 `sub_max_depth` | `depth[v] = depth[parent] + 1`，`sub_max_depth[v] = max(sub_max_depth[left], sub_max_depth[right]) + 1` |
| **第二遍 DFS (reroot)** | 计算 `up_max_depth`，即根到所有不在该子树的节点的最大距离 | `up_max_depth[child] = max( up_max_depth[parent], depth[parent], sibling_sub_max )` |

> **类比**：把树想象成一座山，`depth` 是从山脚（根）爬到每个峰的海拔。我们想知道“如果把某座小山（子树）搬走，最高的海拔会是多少”。第一遍遍历先记录每座小山的最高海拔，第二遍遍历再把“搬走那座山后，其他山的最高海拔”传递下来。

最后答案表 `ans[node] = up_max_depth[node]`（根本身不可能被删，所以查询一定是非根节点），查询时直接返回 `ans[query]`，时间 O(1)。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def height_of_tree_after_removals(root: TreeNode, queries: list[int]) -> list[int]:
    """最优解：一次遍历预处理，随后 O(1) 回答每个查询"""
    n = 0                     # 统计节点数量（用于创建数组）
    # 先把所有节点放进字典，方便后面 O(1) 根据值找到节点对象
    nodes = {}

    def collect_nodes(node: TreeNode) -> None:
        nonlocal n
        if not node:
            return
        nodes[node.val] = node
        n += 1
        collect_nodes(node.left)
        collect_nodes(node.right)

    collect_nodes(root)

    # ---------- 第一次 DFS ----------
    depth = [0] * (n + 1)               # depth[v] : 根到 v 的距离（边数）
    sub_max = [0] * (n + 1)             # sub_max[v] : v 子树内最远节点的深度

    def dfs1(node: TreeNode, d: int) -> None:
        if not node:
            return
        v = node.val
        depth[v] = d
        # 递归左右子树
        dfs1(node.left, d + 1)
        dfs1(node.right, d + 1)

        left = node.left.val if node.left else 0
        right = node.right.val if node.right else 0
        # 子树最高深度 = max(左子树最高, 右子树最高) + 1（自己这条边）
        sub_max[v] = max(sub_max[left], sub_max[right]) + 1

    dfs1(root, 0)          # 根的深度是 0

    # ---------- 第二次 DFS (reroot) ----------
    up_max = [0] * (n + 1)          # up_max[v] : 根到所有不在 v 子树里的节点的最大深度
    # 对根来说，根本身没有“外部”，我们用 -inf 表示不存在（后面取 max 时不会影响）
    NEG_INF = -10 ** 9
    up_max[root.val] = NEG_INF

    def dfs2(node: TreeNode) -> None:
        if not node:
            return
        v = node.val
        # 先把左、右孩子的 up_max 计算好
        left = node.left.val if node.left else 0
        right = node.right.val if node.right else 0

        # 计算左孩子的 up_max
        if node.left:
            # 兄弟子树的最高深度（如果右孩子不存在则为 NEG_INF）
            sibling_best = sub_max[right] if node.right else NEG_INF
            # 三个候选：父节点的 up_max、父节点本身的深度、兄弟子树的最高深度
            cand = max(up_max[v], depth[v], sibling_best)
            # 再加上从父节点到左孩子的一条边
            up_max[left] = cand + 1
        # 计算右孩子的 up_max（对称）
        if node.right:
            sibling_best = sub_max[left] if node.left else NEG_INF
            cand = max(up_max[v], depth[v], sibling_best)
            up_max[right] = cand + 1

        # 继续向下递归
        dfs2(node.left)
        dfs2(node.right)

    dfs2(root)

    # ---------- 生成答案表 ----------
    # 删除某个子树后，树的高度就是 up_max[query]（根到外部节点的最大深度）
    # 如果 up_max 为 NEG_INF（只会在根上），说明整棵树被删除，题目保证不会出现
    answer = [0] * (n + 1)
    for v in range(1, n + 1):
        answer[v] = up_max[v]

    # ---------- 处理查询 ----------
    return [answer[q] for q in queries]
```

> **代码要点解释**  
> 1. **`depth`**：根到每个节点的距离（边数），相当于“海拔”。  
> 2. **`sub_max`**：节点所在子树里最远的那个节点的深度（包括自己），等价于 `depth[node] + height_subtree[node]`。  
> 3. **`up_max`**：根到所有**不在该节点子树**里的节点的最大深度。对根我们设为负无穷，后面取 `max` 时不会影响。  
> 4. **第二遍 DFS** 中的 `cand = max(up_max[parent], depth[parent], sibling_best)`：  
>    - `up_max[parent]` → 祖先们已经算好的“外部最大深度”。  
>    - `depth[parent]` → 父节点本身也算在外部。  
>    - `sibling_best` → 父节点另一侧子树的最高深度（如果没有兄弟子树则不贡献）。  
>    把这三者取最大，再加上一条边（父→子），就得到当前孩子的 `up_max`。  

#### 复杂度  

- **时间复杂度**：`O(n + m)`  
  - 第一次 DFS 访问每个节点一次，第二次 DFS 再访问一次，总计 `2·n`。  
  - 预处理结束后，每个查询只做一次数组下标访问 `O(1)`。  
  - 用大白话说：不管有多少查询，只要树有 10⁵ 个节点，最多跑 **两遍 10⁵** 的循环，几乎瞬间就算完。  

- **空间复杂度**：`O(n)`  
  - `depth、sub_max、up_max、nodes` 各占线性空间。  
  - 递归栈最坏深度是树的高度，最坏情况 `O(n)`（链状树），仍然在可接受范围。  

---

## 心得

- **核心技巧**：**“根到不在某子树里的节点的最大深度”**，即在树上做一次 **重根 DP（reroot DP）**，把“外部信息”从父节点向子节点传播。  
- **适用的题型**  
  1. “删除子树后树的高度/直径/最大路径和” 这类需要 **子树之外** 信息的题目。  
  2. “把每个节点视为根，求对应子树/全局信息” 如 LeetCode 2385 “Amount of Time for Binary Tree to Be Infected”。  
  3. “树上每个节点的祖先贡献最大/最小值” 例如 “Maximum Value of a Node in a Subtree”。  
- **一句话总结解题钥匙**：**先算好每个节点内部的最大深度，再用一次从根向下的传播，把“外部的最大深度”带给每个子节点，查询即可 O(1) 回答。**

---

## 反思

- **拿到题目第一反应**：想到暴力遍历每个查询的子树，直接求根到剩余节点的最大距离。  
- **最容易踩的坑**  
  1. **边界条件**：根节点不会出现在 `queries`，但若不小心把根当成普通节点处理，`up_max[root]` 为负无穷会导致错误。  
  2. **子树为空**：某个节点只有左子树或右子树时，计算兄弟子树的 `sub_max` 必须返回一个无效的极小值（如 `-inf`），否则会错误地把不存在的路径计入最大深度。  
  3. **递归深度**：树可能是链状的，递归深度达到 `10⁵`，在 Python 中需要适当调高递归限制或改写为显式栈。  
- **下次遇到同类题，第一步该想到**：**把全局信息拆成“子树内部”和“子树之外”两部分**，先用一次 DFS 计算内部信息，再用一次“从父到子”传播把外部信息补足，这样所有节点的答案一次性得到。