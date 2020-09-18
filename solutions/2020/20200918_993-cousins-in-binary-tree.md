# #993. 二叉树的堂兄弟节点 / Cousins in Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/cousins-in-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree with unique values and the values of two different nodes of the tree x and y, return true if the nodes corresponding to the values x and y in the tree are cousins, or false otherwise.
Two nodes of a binary tree are cousins if they have the same depth with different parents.
Note that in a binary tree, the root node is at the depth 0, and children of each depth k node are at the depth k + 1.

**Examples**

**Example 1:**

```
Input: root = [1,2,3,4], x = 4, y = 3
Output: false
```

**Example 2:**

```
Input: root = [1,2,3,null,4,null,5], x = 5, y = 4
Output: true
```

**Example 3:**

```
Input: root = [1,2,3,null,4], x = 2, y = 3
Output: false
```

**Constraints**

- The number of nodes in the tree is in the range [2, 100].
- 1 <= Node.val <= 100
- Each node has a unique value.
- x != y
- x and y are exist in the tree.

---

## 题目（中文翻译）

给定一棵每个节点值唯一的二叉树（binary tree）的根节点 `root`，以及树中两个不同节点的值 `x` 和 `y`。如果值为 `x` 和 `y` 的两个节点是表兄弟节点，则返回 `true`，否则返回 `false`。

在二叉树中，若两个节点的深度（depth）相同且父节点（parent）不同，则它们是表兄弟节点。

注意，二叉树的根节点深度为 `0`，深度为 `k` 的节点的子节点的深度为 `k + 1`。

### 示例

**示例 1**

**输入**: `root = [1,2,3,4], x = 4, y = 3`  
**输出**: `false`

**示例 2**

**输入**: `root = [1,2,3,null,4,null,5], x = 5, y = 4`  
**输出**: `true`

**示例 3**

**输入**: `root = [1,2,3,null,4], x = 2, y = 3`  
**输出**: `false`

### 约束条件

- 树中节点的数量在 `[2, 100]` 区间内。  
- `1 <= Node.val <= 100`  
- 每个节点的值唯一。  
- `x != y`  
- `x` 和 `y` 均存在于树中。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：**把整棵树遍历一遍，记录每个节点的父节点和所在层数**。  
遍历完以后，只要比较 `x` 与 `y` 两个节点：

1. 层数相同 → 可能是表兄弟  
2. 父节点不同 → 真正是表兄弟  

这里的「遍历」可以使用 **深度优先搜索（DFS）** 或 **广度优先搜索（BFS）**，二者都可以把每个节点都访问一次。  
为了把「父节点」这个信息保存下来，我们可以在递归/循环时把当前节点的父节点当作参数传进去。  

> **类比**：把树看成一本家谱，**DFS** 就像一次次深入查看每个成员的子辈，**BFS** 则像一次次按辈分顺序查看。我们只需要记下每个人的「父亲是谁」以及「他是第几代」即可。

只要遍历完整棵树，就一定能找到 `x`、`y` 两个节点并得到它们的深度和父节点，这样的方法一定是正确的。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的值
        self.left = left        # 左子树
        self.right = right      # 右子树


def isCousins(root: TreeNode, x: int, y: int) -> bool:
    # 用来保存 x、y 的 (depth, parent) 信息
    info = {}

    # 递归遍历整棵树
    def dfs(node: TreeNode, parent: TreeNode, depth: int):
        if not node:
            return
        # 如果当前节点是 x 或 y，记录它的深度和父节点
        if node.val == x or node.val == y:
            info[node.val] = (depth, parent)
        # 继续向下遍历左右子树，深度 +1，当前节点成为子节点的父节点
        dfs(node.left, node, depth + 1)
        dfs(node.right, node, depth + 1)

    dfs(root, None, 0)          # 从根节点开始，根没有父节点，深度为 0

    # 取出记录的信息
    depth_x, parent_x = info[x]
    depth_y, parent_y = info[y]

    # 同层且父节点不同即为表兄弟
    return depth_x == depth_y and parent_x != parent_y
```

#### 复杂度

- **时间复杂度：O(N)**  
  我们需要把每个节点都访问一次（`N` 为树的节点数），所以时间随节点数线性增长。  
  大白话：如果树有 100 个节点，最多跑 100 次「看看这个节点」的操作。

- **空间复杂度：O(H)**  
  递归调用栈的深度最多等于树的高度 `H`（最坏情况是链状树，`H = N`），因此额外的空间随树的层数增长。  
  大白话：如果树有 5 层，最多会在内存里保存 5 层的「待处理」信息。

---

### 2. 最优解

#### 思路  
暴力解已经是 **O(N)** 的时间复杂度，已经是最好的时间下界，因为我们必须看到 `x`、`y` 才能判断它们的深度与父节点。  
不过我们可以把「一次完整遍历后再比较」的写法稍微简化为「在遍历的过程中一旦找齐 x、y 就可以提前结束」，从而 **在最坏情况仍是 O(N)**，但 **平均情况下更快**。

实现方式：

1. 使用 **BFS（层序遍历）**，一次遍历按层处理节点。  
2. 在遍历每一层时，检查该层是否同时出现 `x` 与 `y`。如果出现：  
   - 检查它们是否是同父节点（即它们是否是兄弟）。如果是兄弟 → 不是表兄弟，直接返回 `False`。  
   - 否则它们是表兄弟，返回 `True`。  
3. 如果遍历完一层后只找到其中一个，说明它们不在同一层，直接返回 `False`（因为后面层的深度更大，已经不可能同层）。

> **类比**：把树想象成一个公司组织结构，**BFS** 就像一次次按部门（层）召开会议，先看第 1 级员工（根），再看第 2 级员工（直接下属），如此逐层检查。只要在同一层看到两个目标员工，就能马上判断他们是否同事（父节点相同）还是同级但不同部门（表兄弟）。

#### 代码（Python）

```python
from collections import deque

def isCousins(root: TreeNode, x: int, y: int) -> bool:
    if not root:
        return False

    # 队列里保存 (节点, 父节点) 元组
    q = deque([(root, None)])

    while q:
        level_size = len(q)          # 当前层的节点数
        x_parent = y_parent = None   # 用来记录本层 x、y 的父节点

        for _ in range(level_size):
            node, parent = q.popleft()

            # 记录 x、y 的父节点
            if node.val == x:
                x_parent = parent
            if node.val == y:
                y_parent = parent

            # 将子节点加入队列，当前节点成为它们的父节点
            if node.left:
                q.append((node.left, node))
            if node.right:
                q.append((node.right, node))

        # 本层遍历结束后检查
        if x_parent and y_parent:          # 同时找到了 x、y
            # 父节点不同 → 表兄弟
            return x_parent != y_parent
        if (x_parent and not y_parent) or (y_parent and not x_parent):
            # 只找到其中一个，说明不在同层
            return False

    return False   # 遍历完仍未找到（理论上不会到这里，因为题目保证 x、y 存在）
```

#### 复杂度

- **时间复杂度：O(N)**  
  每个节点仍然只会被放进队列一次并弹出一次。即使我们可以提前结束，最坏情况下仍需看完全部 `N` 个节点。  
  与暴力解的时间复杂度相同，但实际运行时往往更快，因为一旦找到答案就不必继续遍历剩余的节点。

- **空间复杂度：O(W)**  
  BFS 需要保存当前层的所有节点，最坏情况下宽度 `W`（树的最大层宽）最多等于 `N/2`（完全二叉树的最后一层）。  
  大白话：如果树有 7 层，最宽的一层可能有 32 个节点，队列里最多会存 32 个「待检查」的节点。

---

## 心得

- **核心技巧**：在树结构中同时获取「深度」和「父节点」的信息，常用 **DFS**（递归）或 **BFS**（层序遍历）实现。  
- **适用的题型**  
  1. 判断两个节点是否是 **兄弟节点**（同层同父）  
  2. 求两节点的 **最近公共祖先**（需要父节点或深度信息）  
  3. 判断两节点是否 **在同一层**（层序遍历的典型应用）  
- **一句话总结**：`同层 + 父不同` 就是表兄弟，利用层序遍历一次性捕获这两个信息即可。

## 反思

- **第一反应**：把树全部遍历一遍，记录每个节点的层数和父节点，随后比较。  
- **最容易踩的坑**  
  - 忘记记录父节点，导致只能判断同层却判断不出是否同父。  
  - 在 BFS 实现时，若把「父节点」信息写错（比如把子节点的父节点写成自身），会导致错误的判断。  
  - 边界情况：`x` 或 `y` 正好是根节点（根没有父节点），此时必然不是表兄弟。  
- **下次遇到同类题**：第一步先想「我需要哪些信息？」——深度、父节点或两者的组合；然后选择 **DFS**（递归简洁）或 **BFS**（层序直观）来一次遍历同时收集这些信息。