# #623. 向二叉树中添加一行节点 / Add One Row to Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/add-one-row-to-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree and two integers val and depth, add a row of nodes with value val at the given depth depth.
Note that the root node is at depth 1.
The adding rule is:

**Examples**

**Example 1:**

```
Input: root = [4,2,6,3,1,5], val = 1, depth = 2
Output: [4,1,1,2,null,null,6,3,1,5]
```

**Example 2:**

```
Input: root = [4,2,null,3,1], val = 1, depth = 3
Output: [4,2,null,1,1,3,null,null,1]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- The depth of the tree is in the range [1, 104].
- -100 <= Node.val <= 100
- -105 <= val <= 105
- 1 <= depth <= the depth of tree + 1

---

## 题目（中文翻译）

**描述**  
给定一棵二叉树（binary tree）的根节点 `root`，以及两个整数 `val` 和 `depth`，在深度为 `depth` 的位置添加一行值为 `val` 的节点。  
注意，根节点（root）所在的深度为 1。

**添加规则**  
（原题目中给出的规则示例未完整列出，此处保持原文结构）

**约束条件**  
- 树中节点的数量在 `[1, 10^4]` 区间内。  
- 树的深度在 `[1, 10^4]` 区间内。  
- `-100 <= Node.val <= 100`  
- `-10^5 <= val <= 10^5`  
- `1 <= depth <= 树的深度 + 1`

**示例**  

示例 1：  
```
Input: root = [4,2,6,3,1,5], val = 1, depth = 2
Output: [4,1,1,2,null,null,6,3,1,5]
```

示例 2：  
```
Input: root = [4,2,null,3,1], val = 1, depth = 3
Output: [4,2,null,1,1,3,null,null,1]
```

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**层序遍历**（Breadth‑First Search），也就是把树看成一排排的“楼层”。  
我们从根节点（第 1 层）开始，一层一层往下走，用一个队列（想象成排队买票的队伍）把当前层的所有节点保存起来。  
当我们即将进入第 `depth‑1` 层时，队列里正好是所有需要**在它们下面插入新节点**的父节点。  

插入的规则很简单：  
- 对于每个父节点 `p`，先把 `p` 原来的左子树记作 `oldLeft`，右子树记作 `oldRight`。  
- 创建两个新节点 `newLeft`、`newRight`，它们的值都是 `val`。  
- 把 `newLeft` 挂到 `p.left`，把 `newRight` 挂到 `p.right`。  
- 再把 `oldLeft` 接到 `newLeft.left`，`oldRight` 接到 `newRight.right`。  

这样就完成了在第 `depth` 层插入一整排新节点的操作。  

**为什么正确？**  
因为我们恰好在遍历到第 `depth‑1` 层时，对每个父节点都执行了插入步骤，且只在这一层插入，其他层保持不变，正好满足题目“在指定深度插入整行节点”的要求。  

**时间/空间复杂度**  
- 我们必须把整棵树的每个节点都访问一次（因为要找第 `depth‑1` 层的所有节点），所以时间是 **O(N)**，这里的 **N** 就是树中节点的数量。可以把 **O(N)** 想象成“需要走 N 步”。  
- 层序遍历需要一个队列来保存当前层的节点，最坏情况下一层的节点数可能达到 N/2（完全二叉树的最后一层），因此额外空间是 **O(N)**。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def addOneRow(root: TreeNode, val: int, depth: int) -> TreeNode:
    """
    暴力层序遍历实现
    """
    # depth 为 1 时，直接在根节点上方加一层
    if depth == 1:
        new_root = TreeNode(val)      # 新建一个节点作为新的根
        new_root.left = root          # 原来的根挂到左子树
        return new_root

    from collections import deque
    q = deque([root])                 # 队列里先放根节点
    cur_depth = 1                     # 当前所在的层数

    # 只要还没有到达 depth-1，就继续往下层遍历
    while q and cur_depth < depth - 1:
        for _ in range(len(q)):       # 把当前层的所有节点全部弹出
            node = q.popleft()
            if node.left:
                q.append(node.left)   # 左子树加入队列，准备遍历下一层
            if node.right:
                q.append(node.right)  # 右子树加入队列
        cur_depth += 1                # 完成一层，层数+1

    # 现在 q 中的就是第 depth-1 层的所有节点
    for parent in q:
        old_left = parent.left        # 记录原来的左子树
        old_right = parent.right      # 记录原来的右子树

        parent.left = TreeNode(val)   # 新建左子节点
        parent.right = TreeNode(val)  # 新建右子节点

        parent.left.left = old_left   # 把原来的左子树接到新左节点的左侧
        parent.right.right = old_right  # 把原来的右子树接到新右节点的右侧

    return root
```

#### 复杂度  

- **时间复杂度**：`O(N)` —— 必须访问树中每个节点一次，才能确定哪一层需要插入。  
- **空间复杂度**：`O(N)` —— 队列在最坏情况下会保存整棵树最后一层的节点数。  

---  

### 2. 最优解  

#### 思路  

从暴力解可以看出，**瓶颈在于使用了额外的队列**，在极端情况下会占用 `O(N)` 的额外空间。  
如果我们改用**深度优先遍历**（DFS）递归的方式，只需要在递归栈上保存路径信息，最多只会保存树的高度 `h`（`h ≤ N`）层的节点，空间可以降到 **O(h)**，在大多数情况下会明显小于 `O(N)`。  

优化思路分三步：

1. **特殊情况**：`depth == 1` 时，需要在根节点之上再套一层新节点，这一步直接返回新根。  
2. **递归定位**：我们递归向下搜索，直到到达第 `depth‑1` 层的节点。递归的参数里带上当前层数 `cur`，每次调用 `dfs(node, cur)`。  
3. **插入新节点**：当 `cur == depth‑1` 时，和暴力解相同地创建两棵新子树并挂上原来的左右子树。随后**不再继续向下递归**（因为已经完成插入），直接返回即可。  

**核心概念——递归栈**  
可以把递归想象成“一本打开的书”，每进入一层就往书的左侧翻一页，离开一层就把这页合上。最多只会打开树的高度这么多页，空间随高度线性增长。  

#### 代码（Python）

```python
def addOneRow(root: TreeNode, val: int, depth: int) -> TreeNode:
    """
    使用深度优先递归实现，空间优化到 O(h)
    """
    # depth 为 1 时，新建根节点并把原树挂到左子树
    if depth == 1:
        new_root = TreeNode(val)
        new_root.left = root
        return new_root

    # 递归函数：在当前节点 node，当前层数 cur
    def dfs(node: TreeNode, cur: int):
        if not node:
            return
        # 当已经到达 depth-1 层时，执行插入并停止向下递归
        if cur == depth - 1:
            old_left = node.left
            old_right = node.right

            node.left = TreeNode(val)          # 新左子节点
            node.right = TreeNode(val)         # 新右子节点

            node.left.left = old_left          # 接回原左子树
            node.right.right = old_right       # 接回原右子树
            # 此处不再继续 dfs，因为新插入的节点已经是目标层
            return

        # 继续向下搜索左、右子树，层数+1
        dfs(node.left, cur + 1)
        dfs(node.right, cur + 1)

    dfs(root, 1)      # 从根节点开始，根所在层数是 1
    return root
```

#### 复杂度  

- **时间复杂度**：`O(N)` —— 仍然需要遍历整棵树一次（最坏情况是 `depth` 超过树的深度，需要访问所有节点）。  
- **空间复杂度**：`O(h)` —— 递归栈的深度等于树的高度 `h`，在平衡二叉树时约为 `log N`，在极端链状树时为 `N`，但一般情况下比 BFS 的 `O(N)` 要小。  

---  

## 心得  

- 本题考察的核心技巧是**在特定深度插入节点**，需要对**树的层次概念**和**遍历方式**（层序/深度优先）非常熟悉。  
- 这类“在某层做操作”的思路同样适用于：  
  1. **在第 K 层翻转二叉树**（LeetCode 226）  
  2. **求二叉树的层序遍历**（LeetCode 102）  
  3. **在第 K 层插入空节点**（变形题目）  
- **一句话总结**：找到第 `depth‑1` 层的所有父节点，**一次性**把新节点挂上去，就是解题钥匙。  

---  

## 反思  

- **第一反应**：把树想成一层层的楼层，先找出要插入新节点的“上一层”。  
- **最容易踩的坑**：  
  - `depth == 1` 时需要特殊处理，否则会把根节点直接当成父节点而出错。  
  - 插入后要把原来的左子树挂到新左节点的左侧、右子树挂到新右节点的右侧，别忘了方向，否则会破坏原有结构。  
  - 递归实现时要注意 **return**，防止在已完成插入的节点上继续向下遍历，导致多余的节点被错误创建。  
- **下次遇到同类题**，第一步应该先**判断目标深度是根层还是更深**，决定是“在根上方套一层”还是“在第 depth‑1 层的父节点处插入”。这一步思考可以帮助快速选取合适的遍历方式（BFS 或 DFS）。