# #1123. 最深叶节点的最近公共祖先 / Lowest Common Ancestor of Deepest Leaves

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the lowest common ancestor of its deepest leaves.
Recall that:
Note: This question is the same as 865: https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/

**Examples**

**Example 1:**

```
Input: root = [3,5,1,6,2,0,8,null,null,7,4]
Output: [2,7,4]
Explanation: We return the node with value 2, colored in yellow in the diagram.
The nodes coloured in blue are the deepest leaf-nodes of the tree.
Note that nodes 6, 0, and 8 are also leaf nodes, but the depth of them is 2, but the depth of nodes 7 and 4 is 3.
```

**Example 2:**

```
Input: root = [1]
Output: [1]
Explanation: The root is the deepest node in the tree, and it's the lca of itself.
```

**Example 3:**

```
Input: root = [0,1,3,null,2]
Output: [2]
Explanation: The deepest leaf node in the tree is 2, the lca of one node is itself.
```

**Constraints**

- The number of nodes in the tree will be in the range [1, 1000].
- 0 <= Node.val <= 1000
- The values of the nodes in the tree are unique.

---

## 题目（中文翻译）

给定一棵二叉树 (binary tree) 的根节点 `root`，返回该树中最深叶节点的最近公共祖先 (lowest common ancestor, LCA)。  
回想一下：

**示例 1**  
**示例 2**  
**示例 3**  

**约束条件**  
- 题目与 LeetCode 865 题相同：<https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/>  

**示例**

**示例 1**  
```text
Input: root = [3,5,1,6,2,0,8,null,null,7,4]
Output: [2,7,4]
Explanation: 我们返回值为 2 的节点，在图中用黄色标记。蓝色标记的节点是树中最深的叶节点。需要注意的是，节点 6、0、8 也是叶节点，但它们的深度为 2，而节点 7、4 的深度为 3。```

**示例 2**  
```text
Input: root = [1]
Output: [1]
Explanation: 根节点本身就是树中最深的节点，它也是自身的最近公共祖先。```

**示例 3**  
```text
Input: root = [0,1,3,null,2]
Output: [2]
Explanation: 树中最深的叶节点是 2，单个节点的最近公共祖先就是它自身。```

**约束条件**  
- 树中节点数量在 `[1, 1000]` 区间内。  
- `0 <= Node.val <= 1000`。  
- 树中每个节点的值互不相同。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

1. **先遍历整棵树，记录每个节点的深度**  
   - 深度指的是根节点到该节点的边数（根的深度记作 0）。  
   - 可以用递归或 BFS（层序遍历）来实现。这里用 **BFS**，因为它天然一次遍历就能得到每层的节点。

2. **找出所有最深的叶子节点**  
   - 通过上一步得到的深度最大值 `max_depth`，把深度等于 `max_depth` 且没有子节点的节点挑出来，记作 `deepest_leaves`。  
   - 这些叶子就是“最深的叶子”，题目要求的 LCA 必须在它们的公共祖先里。

3. **把每个节点的父亲记录下来，形成 “哈希表”**  
   - 想象成查字典：`parent[node] = 父节点`。  
   - 这样可以从任意节点向上回溯到根。

4. **对每一对最深叶子，求它们的最近公共祖先 (LCA)**  
   - 先把第一个叶子的所有祖先（包括自己）放进一个集合 `ancestors`。  
   - 再从第二个叶子向上走，第一次碰到 `ancestors` 中的节点就是这对叶子的 LCA。  
   - 对所有叶子两两求 LCA，最后得到的 **最深层的 LCA** 即为答案。  
   - 这里的 “最深层的 LCA” 可以直接取所有叶子两两 LCA 的交集的最深节点，或者把每次求得的 LCA 继续两两合并即可。

**为什么正确**  
- 第一步保证我们知道每个节点离根的距离，进而可以定位最深的叶子。  
- 第三步的父指针让我们能够在 O(树高) 时间内从任意节点回到根，模拟 “向上找祖先”。  
- 两两求 LCA 的过程实际上在找 **所有最深叶子共同拥有的最近祖先**，这正是题目要的“最深的公共祖先”。  

**复杂度分析（大白话版）**  
- **时间**：  
  - BFS 统计深度 O(N)（N 为节点数）。  
  - 建立父指针 O(N)。  
  - 假设最深叶子有 `k` 个，两两求 LCA 需要 `C(k,2) = k·(k-1)/2` 次，每次向上走的步数最坏是树高 `h ≤ N`，所以最坏时间是 O(k²·h)。在最坏情况下 `k` 可能接近 N（比如一棵星形树），于是时间上界是 **O(N²)**。  
- **空间**：  
  - 队列、深度数组、父指针表各占 O(N)。  
  - 其余临时集合也最多 O(N)。  
  - 所以整体 **O(N)** 的额外空间。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def subtreeWithAllDeepest(root: TreeNode) -> TreeNode:
    if not root:
        return None

    # ---------- 1. BFS 统计每个节点的深度 ----------
    from collections import deque
    depth = {root: 0}          # 哈希表：节点 -> 深度
    parent = {root: None}     # 哈希表：节点 -> 父节点
    q = deque([root])
    max_depth = 0
    while q:
        node = q.popleft()
        d = depth[node]
        max_depth = max(max_depth, d)
        for child in (node.left, node.right):
            if child:
                depth[child] = d + 1
                parent[child] = node
                q.append(child)

    # ---------- 2. 找到所有最深的叶子 ----------
    deepest_leaves = [node for node, d in depth.items()
                     if d == max_depth and not node.left and not node.right]

    # ---------- 3. 两两求最近公共祖先 ----------
    def lca(a: TreeNode, b: TreeNode) -> TreeNode:
        """返回 a 与 b 的最近公共祖先（使用父指针）"""
        # 把 a 的所有祖先放进集合
        ancestors = set()
        while a:
            ancestors.add(a)
            a = parent[a]
        # 从 b 向上找第一个在 ancestors 里的节点
        while b not in ancestors:
            b = parent[b]
        return b

    # 依次合并 LCA，最终的 ans 就是所有叶子的公共祖先
    ans = deepest_leaves[0]
    for leaf in deepest_leaves[1:]:
        ans = lca(ans, leaf)

    return ans
```

#### 复杂度

- **时间复杂度**：**O(N²)**（最坏情况下需要两两比较最深叶子，类似 N 次遍历每次 O(N)）  
  - 大白话：如果树里有 1000 个节点，最坏会跑大约 1,000,000 次“向上找父亲”。  
- **空间复杂度**：**O(N)**（存储深度、父指针、队列等）  

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **两两比较** 最深叶子，这会产生二次遍历。我们可以 **在一次后序遍历（从叶子向根）中** 同时得到：

1. 当前子树的最大深度  
2. 当前子树里所有最深叶子所在的**最近公共祖先**  

后序遍历的顺序正好是 **先处理左子树、右子树，再处理根**，这让我们可以把左、右子树的结果合并：

- 若左、右子树的最大深度相同，说明最深叶子分布在两侧，**当前根节点就是它们的最近公共祖先**。  
- 若左子树更深，则最深叶子全部在左子树里，答案就是左子树返回的 LCA。右子树同理。  

这一步只遍历每个节点一次，**不需要额外的父指针或两两比较**，时间自然降到 O(N)。

**关键概念解释**  

- **后序遍历（post‑order）**：先访问左子树，再访问右子树，最后访问根。可以想象为“先把孩子们的情况都弄清楚，最后再决定自己怎么做”。  
- **返回值**：我们让递归函数返回一个二元组 `(depth, lca_node)`，其中 `depth` 表示该子树的最大深度，`lca_node` 表示该子树里所有最深叶子的最近公共祖先。  

**类比**：把树看成一座山，叶子是山顶。我们从山脚往上爬（递归返回），每次都把左、右两座小山的最高点和对应的“最小公共平台”传给父山。最高的那座山的“平台”就是答案。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def subtreeWithAllDeepest(root: TreeNode) -> TreeNode:
    """
    后序遍历一次解决：
    返回 (子树的最大深度, 该子树所有最深叶子的最近公共祖先)
    """
    def dfs(node: TreeNode):
        if not node:
            # 空子树的深度是 -1，这样叶子节点的深度会是 0
            return -1, None

        # 递归处理左、右子树
        left_depth, left_lca = dfs(node.left)
        right_depth, right_lca = dfs(node.right)

        # 根据左右子树的深度决定当前返回的内容
        if left_depth == right_depth:
            # 左右子树同样深，说明最深叶子分布在两侧
            # 当前节点就是它们的最近公共祖先
            return left_depth + 1, node
        elif left_depth > right_depth:
            # 左子树更深，最深叶子全在左边，继承左边的答案
            return left_depth + 1, left_lca
        else:  # right_depth > left_depth
            # 右子树更深，继承右边的答案
            return right_depth + 1, right_lca

    # 只关心第二个返回值（LCA）
    _, answer = dfs(root)
    return answer
```

#### 复杂度

- **时间复杂度**：**O(N)**  
  - 大白话：每个节点只被访问一次，就像一次完整的“全家福合影”。  
- **空间复杂度**：**O(H)**，其中 `H` 为树的高度（递归栈的深度）。最坏情况下（树退化成链表）是 O(N)，平均情况下是 O(log N)。  

---

## 心得

- **核心技巧**：在一次后序遍历中同时返回“子树最大深度”与“对应的 LCA”。  
- **适用场景**：  
  1. **求所有最深节点的最近公共祖先**（本题）。  
  2. **在树中寻找满足某种“最深/最远”条件的节点并返回其公共祖先**（如 LeetCode 1123 的变体）。  
  3. **在二叉树中找出满足特定深度约束的子树**（比如 “最小子树包含所有最深节点”）。
- **一句话总结**：一次后序遍历把“深度信息”和“公共祖先信息”打包返回，既省时又省力。

---

## 反思

- **第一反应**：先把所有叶子层次找出来，再逐个比较它们的祖先，想到使用父指针实现。  
- **最容易踩的坑**：  
  - 忘记把 **空子树的深度设为 -1**，导致叶子节点的深度算成 1（会影响比较）。  
  - 在暴力解里把“所有叶子两两 LCA”直接取交集会遗漏层次信息，容易得到错误的更高（更靠近根）的节点。  
  - 递归返回的 `depth` 必须加 **1** 再传给父节点，忘记这一步会让深度偏小。  
- **下次遇到同类题**：第一步想到 **“一次遍历把需要的状态一起带回去”**（比如深度、大小、是否满足条件），随后根据左右子树的状态决定当前节点的答案，而不是事后再做额外遍历。