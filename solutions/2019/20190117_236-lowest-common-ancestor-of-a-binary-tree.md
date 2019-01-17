# #236. 二叉树的最近公共祖先 / Lowest Common Ancestor of a Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.
According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

**Examples**

**Example 1:**

```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
Output: 3
Explanation: The LCA of nodes 5 and 1 is 3.
```

**Example 2:**

```
Input: root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
Output: 5
Explanation: The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.
```

**Example 3:**

```
Input: root = [1,2], p = 1, q = 2
Output: 1
```

**Constraints**

- The number of nodes in the tree is in the range [2, 105].
- -109 <= Node.val <= 109
- All Node.val are unique.
- p != q
- p and q will exist in the tree.

---

## 题目（中文翻译）

给定一棵二叉树（binary tree），找出其中两个给定节点的最近公共祖先（lowest common ancestor，LCA）。

根据维基百科对 LCA 的定义：“最近公共祖先被定义为在树 T 中，既是节点 p 又是节点 q 的后代的最低（最深）节点（这里允许一个节点是它自身的后代）。”

**示例 1**  
**示例 2**  
**示例 3**

---

### 示例

**示例 1**  
Input: `root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1`  
Output: `3`  
Explanation: 节点 5 和节点 1 的最近公共祖先是 3。

**示例 2**  
Input: `root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4`  
Output: `5`  
Explanation: 节点 5 和节点 4 的最近公共祖先是 5，因为根据 LCA 的定义，节点可以是它自身的后代。

**示例 3**  
Input: `root = [1,2], p = 1, q = 2`  
Output: `1`  

---

### 约束条件

- 树中节点的数量在 `[2, 10^5]` 区间内。  
- `-10^9 <= Node.val <= 10^9`。  
- 所有 `Node.val` 均唯一。  
- `p != q`。  
- `p` 和 `q` 必定存在于树中。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把整棵树展开成「父 → 子」的映射表**（相当于把树的“家谱”写在一本字典里），然后分别把节点 `p`、`q` 向上追溯到根，得到两条从各自所在位置到根的路径。  
这两条路径就像两个人的血缘谱，**从根往下走的最后一个相同的祖先，就是最近公共祖先（LCA）**。  

- **用到的数据结构**  
  - **哈希表（字典）**：`parent[node] = node 的父节点`。哈希表就像一本查字典的工具书，`key` 是单词（这里是树的节点），`value` 是对应的解释（这里是它的父亲）。查找 `O(1)`，所以可以很快得到任意节点的父亲。  
  - **列表**：用来存放从 `p`、`q` 向上走的路径。列表就像装东西的盒子，顺序记录每一步的祖先。  

- **为什么正确**  
  1. 每个节点都有且仅有唯一的父亲（根节点除外），所以通过 `parent` 表可以唯一确定一条从节点到根的路径。  
  2. 两条路径一定会在根节点相交，而最近的相交点恰好是满足题意的“最低公共祖先”。  

- **复杂度大白话**  
  - **时间复杂度** `O(n)`：我们需要遍历整棵树一次来建立 `parent` 表（`n` 是节点数），随后再各走一次路径，最坏也不过是 `n` 步。  
  - **空间复杂度** `O(n)`：`parent` 表要保存每个节点的父亲，最坏需要 `n` 条记录；路径列表最多也会存 `n` 个节点。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    # 1. 用字典记录每个节点的父亲（根的父亲设为 None）
    parent = {root: None}
    stack = [root]                     # 用栈做深度优先遍历

    while stack:
        node = stack.pop()
        # 左子树
        if node.left:
            parent[node.left] = node   # 记录左子节点的父亲
            stack.append(node.left)
        # 右子树
        if node.right:
            parent[node.right] = node  # 记录右子节点的父亲
            stack.append(node.right)

    # 2. 把 p 节点一路向上放进集合 ancestors
    ancestors = set()
    while p:
        ancestors.add(p)
        p = parent[p]                  # 向上走一步

    # 3. 从 q 开始往上走，第一次碰到 ancestors 集合中的节点，就是 LCA
    while q not in ancestors:
        q = parent[q]                  # 一直向上走

    return q
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 先遍历一次树建立父指针（`n`），再各走一次路径（最多 `n`），所以整体线性。  
- **空间复杂度**：`O(n)` —— `parent` 表存每个节点的父亲，另外 `ancestors` 集合最坏也会存 `n` 个节点。  

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**需要额外的 O(n) 空间** 来保存父指针和路径集合。  
其实我们可以在一次递归遍历中直接把答案“压在递归栈”里，不需要额外的哈希表。  

核心思想：**后序遍历**（先左、后右、再根）。对每个节点，递归检查它的左子树和右子树是否已经找到了 `p` 或 `q`。  

- **三种情况**  
  1. 左子树返回非空，右子树返回非空 → 说明 `p`、`q` 分别在左右子树中，当前节点就是最近公共祖先。  
  2. 左子树返回非空，右子树为空 → 说明 `p`、`q` 都在左子树或左子树本身就是答案，直接把左子树的返回值向上传递。  
  3. 当前节点本身就是 `p` 或 `q` → 即使另一侧没有找到，只要另一侧的递归最终返回了另一个目标节点，当前节点也会成为 LCA（因为“节点可以是自己的后代”）。  

这套逻辑只需要**一次深度优先搜索**，不需要额外存储父指针，空间只用递归栈（最坏高度 `h`，在平衡树里是 `log n`，在最坏的链状树里是 `n`）。  

- **关键概念解释**  
  - **递归**：把“大问题”拆成“小问题”，让函数自己调用自己。想象把树的每个分支都交给一位“小助手”去检查，最后把结果交给上层。  
  - **后序遍历**：先让左、右两个“小助手”把信息报回，等信息齐全后再决定自己该怎么做。  

#### 代码（Python）  

```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    递归实现 LCA
    返回值有两层含义：
        - None   : 在当前子树里既没有 p 也没有 q
        - 非 None: 要么是 p/q 本身，要么是已经找到的 LCA
    """
    if not root:                 # 空树直接返回 None
        return None

    # 如果当前节点正好是 p 或 q，直接返回自己
    if root == p or root == q:
        return root

    # 递归检查左、右子树
    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    # 情况 1：左右子树各找到一个 → 当前节点就是 LCA
    if left and right:
        return root

    # 情况 2/3：只有一边找到 → 把找到的那一边向上返回
    # （如果 left 为 None，返回 right；如果 right 为 None，返回 left）
    return left if left else right
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 每个节点恰好被访问一次（递归遍历整棵树），和暴力解的时间相同，但没有额外遍历或构建表的开销。  
- **空间复杂度**：`O(h)` —— 递归栈的深度等于树的高度 `h`。在最坏情况下（树退化成链表）是 `O(n)`，在平衡树里约为 `O(log n)`，明显优于暴力解的 `O(n)` 额外空间。  

---  

## 心得  

- **核心技巧**：后序深度优先遍历（DFS）结合“信息自底向上传递”。  
- **适用的题型**  
  1. **二叉树的最近公共祖先**（本题）。  
  2. **判断两节点是否在同一子树**（如 LeetCode 236 里判断是否为子树）。  
  3. **在树中寻找满足某种条件的最近节点**（如最近的相同值节点、最近的满足属性的节点等）。  
- **一句话总结**：**让左、右子树先把“是否找到目标”这条信息报回，第一次在同一层得到两个“YES”时，就是答案所在的节点。**  

---  

## 反思  

- **第一反应**：把树展开成父指针表，分别向上找路径——直觉上很容易想到。  
- **最容易踩的坑**  
  - 忘记 “节点可以是自己的后代”——如果 `p` 是 `q` 的祖先，答案应该是 `p` 本身。递归实现只要在 `root == p or root == q` 时直接返回当前节点即可。  
  - 递归返回值的意义不清晰：返回 `None` 表示子树里没有目标，返回非 `None` 可能是目标本身也可能是已经找到的 LCA，需要在代码中统一解释。  
- **下次遇到同类题**：第一步想到 **“把子问题的答案往上合并”**（即后序遍历），再检查合并后是否满足“左右子树各出现一次目标”这种模式。这样可以直接在一次遍历中得到答案，避免额外的空间开销。