# #897. 递增顺序搜索树 / Increasing Order Search Tree

> 难度：简单 · 标签：Stack、Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/increasing-order-search-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary search tree, rearrange the tree in in-order so that the leftmost node in the tree is now the root of the tree, and every node has no left child and only one right child.

**Examples**

**Example 1:**

```
Input: root = [5,3,6,2,4,null,8,1,null,null,null,7,9]
Output: [1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]
```

**Example 2:**

```
Input: root = [5,1,7]
Output: [1,null,5,null,7]
```

**Constraints**

- The number of nodes in the given tree will be in the range [1, 100].
- 0 <= Node.val <= 1000

---

## 题目（中文翻译）

给定一棵二叉搜索树（binary search tree，BST）的根节点 `root`，请按中序遍历（in-order）重新排列这棵树，使得树中最左侧的节点成为新的根节点，并且每个节点都没有左子节点且仅有一个右子节点。

**示例 1**  
**示例 2**  
（上述示例标题仅用于占位，实际示例见下文）

**约束条件**  
- 给定树的节点数在 `[1, 100]` 范围内。  
- `0 <= Node.val <= 1000`

**示例**

**示例 1：**  
```
Input: root = [5,3,6,2,4,null,8,1,null,null,null,7,9]
Output: [1,null,2,null,3,null,4,null,5,null,6,null,7,null,8,null,9]
```

**示例 2：**  
```
Input: root = [5,1,7]
Output: [1,null,5,null,7]
```

**说明**  
- 通过中序遍历原始 BST，可以得到节点值的递增序列。  
- 重新构造后，新的树形如同一条单向链表，所有节点仅通过右指针相连，左指针均为 `null`。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把原来的二叉搜索树（BST）**全部遍历一遍**，把节点按照中序（左 → 根 → 右）的顺序记下来。  
- **中序遍历**在 BST 中恰好会得到从小到大的有序序列，就像把一本字典的词条从 A 到 Z 排好序一样。  
- 我们可以把遍历得到的节点放进一个 Python 列表 `nodes`，这一步相当于“把所有词条记在纸上”。  

得到有序列表后，重新**按照题目要求**把它们串起来：  
- 第一个元素（最小的节点）成为新的根。  
- 之后的每个节点只挂在前一个节点的右侧，左子树全部置为 `None`。  

这样就得到了左子树全为空、只有右子树的“递增搜索树”。  

> **为什么正确？**  
> 中序遍历保证了节点值的严格递增；我们把这些节点按照遍历顺序重新连接，恰好满足“左子树为空、右子树按递增顺序排列”的要求。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def increasingBST(root: TreeNode) -> TreeNode:
    """
    暴力解法：先中序遍历得到所有节点，随后重新链接成单链右子树。
    """
    nodes = []                     # 用列表把遍历到的节点依次存下来

    def inorder(node: TreeNode):
        """递归的中序遍历，把节点加入 nodes 列表"""
        if not node:
            return
        inorder(node.left)         # 先左
        nodes.append(node)         # 再根
        inorder(node.right)        # 最后右

    inorder(root)                  # 把整棵树的节点都放进 nodes

    # 重新组织：第一个节点是新的根，后面的节点全部只挂在前一个的右侧
    new_root = nodes[0]            # 最左侧的节点（最小值）成为根
    cur = new_root
    for nxt in nodes[1:]:
        cur.left = None            # 左子树全部置空
        cur.right = nxt            # 只保留右子树
        cur = nxt                  # 移动指针到下一个节点

    cur.left = None                # 最后一个节点的左指针也要置空
    cur.right = None               # 右指针设为 None（防止旧的右子树残留）

    return new_root
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 中序遍历一次访问每个节点 `n` 次，随后再遍历一次列表把它们重新链接，同样是 `n` 次操作。  
  - 用大白话说，就是“跟节点数量成正比”，如果有 1000 个节点，就大约要做 1000 次工作。

- **空间复杂度：** `O(n)`  
  - 需要额外的列表 `nodes` 把所有节点保存下来，最坏情况下占用和树一样多的空间。  
  - 递归栈本身也会占 `O(h)`（树的高度），但在最坏的单链树里 `h = n`，所以总体仍是 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的**瓶颈**在于需要额外的列表来存所有节点，空间浪费了 `O(n)`。  
其实我们在**中序遍历的过程中**就可以**直接把节点连起来**，不必再保存整个序列。

关键点：

1. **保持一个“指针” `prev`**，指向已经处理好的最后一个节点。  
2. 当遍历到下一个节点 `cur` 时：  
   - 把 `prev.right = cur`，让 `cur` 成为 `prev` 的右孩子。  
   - 把 `cur.left = None`，确保左子树为空。  
   - 然后把 `prev` 移动到 `cur`，继续往后处理。  

因为中序遍历天然保证了递增顺序，这样一边遍历一边“实时拼接”，就直接得到目标树。

实现方式可以是 **递归**（利用系统调用栈）或 **显式栈的迭代**。这里用递归写法，代码简洁，且递归深度最多是树的高度 `h`（`h ≤ n`），在本题约束（`n ≤ 100`）下完全安全。

> **从零解释的核心概念**  
> - **递归**：函数自己调用自己，每一次调用都相当于在纸上画一个“子问题”。当子问题规模为 0（空节点）时，递归停止并返回。  
> - **指针（引用）**：在 Python 中，变量指向对象本身。把 `prev.right = cur` 实际上是让 `prev` 所指的节点的右指针指向 `cur`，实现“把两块积木粘在一起”。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def increasingBST(root: TreeNode) -> TreeNode:
    """
    最优解：在中序遍历时直接把节点串成单右子树。
    """
    dummy = TreeNode(-1)   # 虚拟节点，方便统一处理第一个真实节点
    prev = dummy           # prev 永远指向已经拼好的链表的最后一个节点

    def inorder(node: TreeNode):
        """递归的中序遍历，同时把遍历到的节点接到 prev 的右侧"""
        nonlocal prev      # 让内部函数能够修改外层的 prev 变量
        if not node:
            return
        inorder(node.left)     # 先遍历左子树（得到更小的值）

        # ------- 下面开始“拼接” -------
        node.left = None       # 左子树必须置空
        prev.right = node      # 把当前节点接到已经排好序的链表后面
        prev = node            # 更新 prev，指向最新加入的节点
        # --------------------------------

        inorder(node.right)    # 再遍历右子树（更大的值）

    inorder(root)               # 从根开始完整的中序遍历
    return dummy.right          # dummy 的右孩子就是新树的根
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 每个节点恰好被访问一次，和暴力解一样快，只是省掉了后面的遍历列表的步骤。  
  - 用通俗的话说，就是“和节点数量成正比”，不管树有多大，时间增长速度与节点数相同。

- **空间复杂度：** `O(h)`（`h` 为树的高度）  
  - 只用了递归栈来保存遍历路径，最多等于树的深度。  
  - 在最坏的单链形 BST（高度 `n`）下会是 `O(n)`，但在平均平衡树里大约是 `O(log n)`，明显比暴力解的 `O(n)` 更省空间。  

---

## 心得

- **核心技巧**：**中序遍历 + 现场重链接**（在遍历的过程中即时修改指针）。  
- **适用的题型**：  
  1. “把 BST 改造成单链右子树” 类似题（如 LeetCode 897）。  
  2. “把二叉树展平成链表” 需要按特定顺序重连节点（如 LeetCode 114）。  
  3. “原地遍历并修改结构” 的题目（如把二叉搜索树转换为有序双向链表）。  
- **一句话总结解题钥匙**：**“遍历的顺序本身就是答案，利用它边遍历边拼接即可”。**

---

## 反思

- **第一反应**：把树全部遍历出来，保存到列表，再重新建树——这是一种“先收集、后处理”的思路。  
- **最容易踩的坑**：  
  - 忘记把每个节点的左指针设为 `None`，导致旧的左子树残留，破坏“左子树全空”的要求。  
  - 在递归实现时忘记使用 `nonlocal` 声明 `prev`，导致局部变量没有被更新。  
  - 对空树或只有一个节点的极端情况没有考虑（本题保证至少有一个节点，但写通用代码时仍要防御）。  
- **下次遇到同类题**：**第一步先明确遍历顺序是否已经是答案**（比如中序、前序、层序），随后思考是否可以在遍历过程中**直接修改指针**，而不是额外存储全部节点。这样既省空间又保持代码简洁。