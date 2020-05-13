# #865. 包含所有最深节点的最小子树 / Smallest Subtree with all the Deepest Nodes

> 难度：中等 · 标签：Hash Table、Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, the depth of each node is the shortest distance to the root.
Return the smallest subtree such that it contains all the deepest nodes in the original tree.
A node is called the deepest if it has the largest depth possible among any node in the entire tree.
The subtree of a node is a tree consisting of that node, plus the set of all descendants of that node.
Note: This question is the same as 1123: https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/

**Examples**

**Example 1:**

```
Input: root = [3,5,1,6,2,0,8,null,null,7,4]
Output: [2,7,4]
Explanation: We return the node with value 2, colored in yellow in the diagram.
The nodes coloured in blue are the deepest nodes of the tree.
Notice that nodes 5, 3 and 2 contain the deepest nodes in the tree but node 2 is the smallest subtree among them, so we return it.
```

**Example 2:**

```
Input: root = [1]
Output: [1]
Explanation: The root is the deepest node in the tree.
```

**Example 3:**

```
Input: root = [0,1,3,null,2]
Output: [2]
Explanation: The deepest node in the tree is 2, the valid subtrees are the subtrees of nodes 2, 1 and 0 but the subtree of node 2 is the smallest.
```

**Constraints**

- The number of nodes in the tree will be in the range [1, 500].
- 0 <= Node.val <= 500
- The values of the nodes in the tree are unique.

---

## 题目（中文翻译）

**题目描述**  
给定一棵二叉树的根节点 `root`，每个节点的深度（depth）定义为从根节点到该节点的最短距离。  
返回满足以下条件的最小子树（subtree）：该子树包含原树中所有最深节点（deepest node）。  

- **最深节点**：在整棵树中深度最大的节点。  
- **子树**：以某个节点为根，包括该节点以及其所有后代节点组成的树。

**示例 1**  
**示例 2**  
**示例 3**

**约束条件**  
- 树中节点数在 `[1, 500]` 之间。  
- `0 <= Node.val <= 500`。  
- 树中所有节点的值互不相同。

**说明**  
本题与 1123 题相同：<https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/>

---

### 示例

**示例 1**  
```
Input: root = [3,5,1,6,2,0,8,null,null,7,4]
Output: [2,7,4]
Explanation: 我们返回值为 2 的节点（在示意图中用黄色标记）。图中用蓝色标记的节点是树的最深节点。可以看到节点 5、3 和 2 都包含所有最深节点，但在它们之中，节点 2 对应的子树最小，因此返回该节点。
```

**示例 2**  
```
Input: root = [1]
Output: [1]
Explanation: 整棵树的根节点本身就是最深节点。
```

**示例 3**  
```
Input: root = [0,1,3,null,2]
Output: [2]
Explanation: 树中最深的节点是 2。满足条件的子树可以是节点 2、节点 1 或节点 0 对应的子树，但节点 2 对应的子树最小，所以返回它。
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

1. **先算每个节点的深度**  
   - 深度 = 根节点到该节点的边数。  
   - 可以用一次 BFS（层序遍历）或 DFS（深度优先遍历）得到所有节点的深度。  
   - 想象成“从家走到每个亲戚家”，走的步数就是深度。  

2. **找到最大的深度，收集所有最深的节点**  
   - 记录下最大的深度 `maxDepth`，把所有深度等于它的节点放进列表 `deepest`。  
   - 这一步相当于在“字典”（哈希表）里查所有词的页码，key 是节点，value 是深度。  

3. **遍历所有节点，判断它的子树是否包含所有最深节点**  
   - 对每个节点 `cur`，做一次 DFS，统计子树里出现的最深节点数 `cnt`。  
   - 如果 `cnt` 等于 `len(deepest)`，说明 `cur` 的子树已经把所有最深节点都包进来了。  
   - 在满足条件的节点中，挑选深度最小的（也就是离根最近的）即为答案。  

**为什么暴力方法一定能得到正确答案？**  
- 我们把所有可能的子树都检查了一遍，只要子树里包含所有最深节点，它就符合题意。  
- 再挑最小深度的那个，就恰好是“最小子树”。  

**时间/空间复杂度（大白话）**  
- 第一步遍历一次树 → O(N)。  
- 第二步遍历一次树 → O(N)。  
- 第三步：对每个节点都要再遍历它的子树，最坏情况是根节点的子树是整棵树，第二个节点的子树是除根外的树，……，于是总共会出现 **≈ N + (N‑1) + … + 1 = N(N+1)/2** 次访问，时间复杂度是 **O(N²)**。  
- 空间上我们用了几个哈希表和递归栈，最坏是 O(N)。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def subtreeWithAllDeepest(root: TreeNode) -> TreeNode:
    # ---------- 1. 计算每个节点的深度 ----------
    depth = {}                     # node -> depth
    def dfs_depth(node, d):
        if not node:
            return
        depth[node] = d
        dfs_depth(node.left, d + 1)
        dfs_depth(node.right, d + 1)

    dfs_depth(root, 0)

    # ---------- 2. 找到最大深度及所有最深节点 ----------
    max_depth = max(depth.values())
    deepest = [node for node, d in depth.items() if d == max_depth]

    # ---------- 3. 检查每个节点的子树是否包含所有最深节点 ----------
    # 用一个函数返回子树里出现的 deepest 节点数量
    def count_deepest(node):
        if not node:
            return 0
        left = count_deepest(node.left)
        right = count_deepest(node.right)
        # 如果当前节点本身是最深节点，计数 +1
        self_cnt = 1 if node in deepest_set else 0
        return left + right + self_cnt

    deepest_set = set(deepest)          # 为了 O(1) 判断
    answer = None
    min_depth = float('inf')            # 记录最小深度的候选节点

    # 再遍历一次所有节点，寻找满足条件且深度最小的节点
    def traverse(node):
        nonlocal answer, min_depth
        if not node:
            return
        if count_deepest(node) == len(deepest):
            # 当前子树已经包揽所有最深节点
            if depth[node] < min_depth:
                min_depth = depth[node]
                answer = node
        traverse(node.left)
        traverse(node.right)

    traverse(root)
    return answer
```

#### 复杂度  

- **时间复杂度**：**O(N²)**  
  - 解释：对每个节点都要重新遍历它的子树，最坏会出现 N·(N+1)/2 次访问，约等于 N²。  
- **空间复杂度**：**O(N)**  
  - 解释：使用了哈希表存放深度、递归栈的最大深度是树的高度（最坏 O(N)），以及 `deepest_set`。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看到 **瓶颈在于第三步**：我们反复遍历子树来计数。  
如果能够在 **一次遍历** 中就把「子树里最深的深度」以及「包含所有最深节点的子树根」这两个信息带回去，就不需要二次遍历。

**关键观察**  

- 对于任意节点 `node`，只要知道左子树的最大深度 `dl`、右子树的最大深度 `dr`，就可以判断：
  1. 如果 `dl == dr`，说明左、右子树的最深叶子深度相同，**当前节点** 是这批最深叶子的最近公共祖先（LCA），即答案子树的根。
  2. 如果 `dl > dr`，说明更深的叶子全部在左子树，答案一定在左子树里（把左子树的结果往上带）。
  3. 同理 `dr > dl`，答案在右子树里。

- 于是我们只需要一次 **后序遍历**（先处理左右子树，再处理自己），把每棵子树返回两个值：  
  - `height`：该子树的最大深度。  
  - `subtree_root`：满足题目要求的最小子树根（如果当前子树已经满足，则返回自己，否则返回左/右子树的结果）。

**为什么后序遍历能一次搞定？**  
- 想象把树的每个节点当作「小工厂」，它们只负责把「自己下面」的最大深度和对应的子树根「包装」好交给上层。上层只需要比较左右两个包装好的结果，就能决定自己的返回值。这样信息只向上传递一次，避免了重复遍历。

**类比**  
- 这跟「找两个人的最近公共祖先」很像，只是这里的「人」是「最深叶子」的集合，而我们用「深度」这条数轴来帮助比较。

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def subtreeWithAllDeepest(root: TreeNode) -> TreeNode:
    """
    返回包含所有最深叶子的最小子树根节点
    思路：后序遍历，返回 (子树最大深度, 对应的子树根)
    """

    def dfs(node):
        if not node:
            # 空树的深度是 -1（因为叶子节点的深度算作 0）
            return -1, None

        # 递归左、右子树，得到它们的 (深度, 子树根)
        left_h, left_root = dfs(node.left)
        right_h, right_root = dfs(node.right)

        if left_h == right_h:
            # 左右子树深度相同，当前节点是这些最深叶子的最近公共祖先
            return left_h + 1, node
        elif left_h > right_h:
            # 左子树更深，答案一定在左子树里
            return left_h + 1, left_root
        else:
            # 右子树更深，答案一定在右子树里
            return right_h + 1, right_root

    # dfs 返回的第二个值就是答案
    return dfs(root)[1]
```

> **代码要点（中文注释）**  
> - `if not node: return -1, None`：空节点的深度设为 -1，便于叶子节点返回 0。  
> - `left_h + 1`、`right_h + 1`：当前节点比子树深度多走一步。  
> - 当左、右深度相等时，**当前节点** 正好是「最深叶子们的最近公共祖先」，因此直接返回 `node`。  

#### 复杂度  

- **时间复杂度**：**O(N)**  
  - 解释：每个节点只被访问一次，做常数次的比较和返回操作，整体线性。相比暴力的 O(N²)，快了很多。  
- **空间复杂度**：**O(H)**（递归栈的深度）  
  - 解释：最坏情况下树是一条链，递归深度等于节点数 N，即 O(N)。平均情况下是树的高度 H，通常 H ≈ log N（平衡树）。  

---  

## 心得  

- **核心技巧**：后序遍历 + “把子树信息向上合并”。  
- **适用的题型**  
  1. **最低公共祖先（LCA）** 类问题，例如 “二叉树的最近公共祖先”。  
  2. **子树信息汇总**，如 “求子树中节点之和最大的子树”。  
  3. **根据深度/高度决定答案**，例如 “二叉树的最大深度” 与 “最长路径”。  
- **一句话总结解题钥匙**：**在一次 DFS 中把“子树最深层信息”带回去，就能直接得到答案，避免重复遍历**。  

---  

## 反思  

- **第一反应**：先把所有节点的深度算出来，然后把最深的节点挑出来，再逐个检查子树是否包含它们。  
- **最容易踩的坑**  
  1. **空树的深度定义**：如果把叶子深度当作 1，递归返回值需要对应调整。这里我们把空树设为 -1，使叶子深度为 0，计算更直观。  
  2. **递归返回值的顺序**：一定要先比较左右子树的深度，再决定返回哪个子树根，别把 `node` 写在错误的分支里。  
  3. **栈溢出**：递归深度太大（N=500）在 Python 里仍然安全，但如果规模更大，需要改写为显式栈的迭代版。  

- **下次遇到同类题**：**先思考“能否在一次遍历中把需要的全部信息带回去”。** 如果答案是“能”，就尝试设计一个返回多个值的递归函数；如果“不能”，再考虑多次遍历或额外的数据结构。