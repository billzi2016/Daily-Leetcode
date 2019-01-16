# #235. 二叉搜索树的最近公共祖先 / Lowest Common Ancestor of a Binary Search Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/)

---

## 题目（英文原版）

**Description**

Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.
According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes p and q as the lowest node in T that has both p and q as descendants (where we allow a node to be a descendant of itself).”

**Examples**

**Example 1:**

```
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
Output: 6
Explanation: The LCA of nodes 2 and 8 is 6.
```

**Example 2:**

```
Input: root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
Output: 2
Explanation: The LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself according to the LCA definition.
```

**Example 3:**

```
Input: root = [2,1], p = 2, q = 1
Output: 2
```

**Constraints**

- The number of nodes in the tree is in the range [2, 105].
- -109 <= Node.val <= 109
- All Node.val are unique.
- p != q
- p and q will exist in the BST.

---

## 题目（中文翻译）

给定一棵二叉搜索树（BST），请找出该树中两个给定节点的最近公共祖先（LCA）节点。

根据维基百科对 LCA 的定义：“最近公共祖先是指在树 T 中，能够同时作为节点 p 和节点 q 的后代（我们允许一个节点是其自身的后代）的最低的节点。”

### 示例

#### 示例 1
**输入**：`root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 8`  
**输出**：`6`  
**解释**：节点 2 和节点 8 的最近公共祖先是 6。

#### 示例 2
**输入**：`root = [6,2,8,0,4,7,9,null,null,3,5]`, `p = 2`, `q = 4`  
**输出**：`2`  
**解释**：节点 2 和节点 4 的最近公共祖先是 2，因为根据 LCA 的定义，一个节点可以是其自身的后代。

#### 示例 3
**输入**：`root = [2,1]`, `p = 2`, `q = 1`  
**输出**：`2`

### 约束条件
- 树中节点的数量在区间 `[2, 10^5]` 内。  
- `-10^9 <= Node.val <= 10^9`  
- 所有 `Node.val` 均唯一。  
- `p != q`  
- `p` 和 `q` 必定存在于该 BST 中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把 **从根节点到 p、q 的完整路径** 都记下来，然后比较这两条路径，最后一个相同的节点就是最近公共祖先。  

- **数据结构**：我们可以把路径存进列表（list），列表就像一本“旅行日志”，每走一步就往里写下当前所在的节点。  
- **为什么正确**：路径的前半段一定是两条路径的公共部分，公共部分的最后一个节点必然是离根最近、同时能到达 p 与 q 的节点，也就是题目要求的 LCA。  
- **复杂度分析**：  
  - 先找路径，需要遍历整棵树一次，最坏情况要访问所有 `n` 个节点，时间是 **O(n)**。  
  - 把路径保存下来需要额外的空间，最坏情况下路径长度可能是树的高度 `h`（在链状树里 `h = n`），所以空间是 **O(h)**，最坏 **O(n)**。  
  - 再比较两条路径，只需要线性扫描两条列表，最多 `h` 次比较，仍是 **O(h)**，不影响总体复杂度。

> **大白话**：  
> - `O(n)` 就像说“最差情况下，你得把所有节点都检查一遍”，和我们平时说的“要走 n 步”。  
> - `O(h)` 则是说“只需要保存从根到目标节点的那条路”，如果树很高（接近 n），空间就会比较大。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def lowestCommonAncestor_bruteforce(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    暴力解法：先找根到 p、q 的路径，再比较找出最后的公共节点。
    """
    # -------------------------------------------------
    # 辅助函数：返回从 root 到 target 的路径（包含 root 与 target 本身）
    # -------------------------------------------------
    def find_path(node: TreeNode, target: TreeNode, path: list) -> bool:
        if not node:
            return False
        path.append(node)                     # 走到当前节点，记下来
        if node is target:                    # 找到目标节点
            return True
        # 在左子树或右子树继续搜索
        if find_path(node.left, target, path) or find_path(node.right, target, path):
            return True
        path.pop()                            # 当前分支不通，回溯，去掉这个节点
        return False

    path_p, path_q = [], []
    find_path(root, p, path_p)                # 获得根到 p 的路径
    find_path(root, q, path_q)                # 获得根到 q 的路径

    # -------------------------------------------------
    # 比较两条路径，找到最后相同的节点
    # -------------------------------------------------
    i = 0
    while i < len(path_p) and i < len(path_q) and path_p[i] is path_q[i]:
        i += 1
    # 上一步退出时 i 指向第一个不相同的位置，所以公共祖先是 i-1
    return path_p[i - 1]
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  需要遍历整棵树两次（一次找 p，一次找 q），最坏情况每次都要访问所有节点。

- **空间复杂度**：`O(h)`（最坏 `O(n)`）  
  递归调用栈的深度是树的高度 `h`，另外要保存两条路径，各占 `O(h)` 空间。

---

### 2. 最优解

#### 思路  

BST（二叉搜索树）有一个非常重要的性质：**左子树所有节点的值都小于根节点，右子树所有节点的值都大于根节点**。利用这个特性，我们可以 **从根节点开始往下走**，一次判断：

1. 如果 `p.val` 与 `q.val` 同时小于当前节点的值，说明它们都在左子树，**向左走**。  
2. 如果它们都大于当前节点的值，说明它们都在右子树，**向右走**。  
3. 否则，说明它们分散在当前节点的左右两侧（或一个正好等于当前节点），此时 **当前节点就是最近公共祖先**。

> **瓶颈**：暴力解需要把整棵树遍历两遍并保存路径，而 BST 的有序结构让我们只需要一次遍历就能定位 LCA。

#### 关键算法/数据结构

- **二叉搜索树的有序性**：把树看成一本“有序的电话簿”，左边的号码都比当前号码小，右边的都比它大。这样我们可以像二分查找一样，快速排除不可能的分支。  
- **单指针遍历**：只需要一个指针 `node` 从根向下走，不需要额外的栈或列表，空间几乎为常数。

#### 代码（Python）

```python
def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    """
    最优解：利用 BST 的大小关系，一次遍历即可找到 LCA。
    """
    node = root
    while node:
        # 如果 p、q 都在左子树，向左走
        if p.val < node.val and q.val < node.val:
            node = node.left
        # 如果 p、q 都在右子树，向右走
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            # 分叉点就是最近公共祖先
            return node
    return None  # 题目保证一定会找到，这行只是防止类型检查报错
```

#### 复杂度

- **时间复杂度**：`O(h)`，其中 `h` 是树的高度。  
  - 在 **平衡 BST** 中，`h ≈ log₂ n`，所以时间约为 **O(log n)**，相当于二分查找的速度。  
  - 最坏情况下（树退化成链表），`h = n`，仍是 **O(n)**，但这已经是理论上不可避免的极端情况。

- **空间复杂度**：`O(1)`（常数空间）  
  只用了一个指针 `node`，没有递归栈或额外容器。

---

## 心得

- **核心技巧**：利用二叉搜索树的「左小右大」特性，把查找过程转化为类似二分查找的单向遍历。  
- **适用的题型**：  
  1. **在 BST 中查找某个值**（LeetCode 700）  
  2. **BST 的插入/删除**（LeetCode 450、450）  
  3. **在 BST 中找两个节点的距离**（变形题）  
- **一句话总结**：**只要比较目标值与当前节点的大小，就能一步步逼近最近公共祖先**。

---

## 反思

- **第一反应**：先想到「把路径记下来再比较」——这是一种通用的树上 LCA 思路，适用于任意二叉树。  
- **最容易踩的坑**：  
  - 忘记处理 **节点本身就是祖先** 的情况（如示例 2 中 p=2 本身就是 LCA）。  
  - 在实现时误把 `p.val == node.val` 当作「向左」或「向右」的条件，导致无限循环。  
- **下次遇到同类题**：第一步先问自己「这棵树有序吗？」如果是 BST，就立刻想到 **利用大小关系单向遍历**；否则才回到「记录路径」或「使用父指针」的通用方法。