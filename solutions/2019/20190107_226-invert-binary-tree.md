# #226. 翻转二叉树 / Invert Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/invert-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, invert the tree, and return its root.

**Examples**

**Example 1:**

```
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
```

**Example 2:**

```
Input: root = [2,1,3]
Output: [2,3,1]
```

**Example 3:**

```
Input: root = []
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 100].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定二叉树（binary tree）的根节点，翻转该树，并返回其根节点。

### 示例

**示例 1**

```
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
```

**示例 2**

```
Input: root = [2,1,3]
Output: [2,3,1]
```

**示例 3**

```
Input: root = []
Output: []
```

### 约束条件

- 树中节点的数量在 `[0, 100]` 范围内。  
- `-100 <= Node.val <= 100`   (节点值的取值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**遍历整棵树**，每访问到一个节点，就把它的左子树和右子树交换。  
这和我们在生活中“把左右手互换”非常类似，只要把每个节点的两个孩子互换位置，整棵树自然就翻转了。

- **用到的数据结构**：二叉树的节点结构 `TreeNode`。递归调用时会用到**函数调用栈**，它本质上就是一个“隐形的栈”，类似于我们平时查字典时把查找过程压在纸条上，等到回溯再取出来。
- **为什么正确**：树的翻转只需要对每个节点做一次左右交换。递归保证我们会 **一次遍历所有节点**，所以所有左右子树都会被交换，最终得到的就是镜像树。
- **复杂度分析**：  
  - 时间上，每个节点只被访问一次并做一次交换，记作 `O(n)`（n 是节点数）。如果把 `O(n)` 想象成“一遍遍历所有苹果”，那就是 **线性** 的意思。  
  - 空间上，递归会产生调用栈，最坏情况下（完全不平衡的树）深度等于 `n`，所以空间是 `O(n)`；在最好的平衡树情况下深度是 `log n`，即 `O(log n)`。这里统一写 `O(h)`，h 为树高。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的值
        self.left = left        # 左子树
        self.right = right      # 右子树

def invertTree(root: TreeNode) -> TreeNode:
    """
    递归版：遍历每个节点并交换左右子树
    """
    if root is None:               # 空树直接返回
        return None

    # 先递归翻转左子树和右子树
    left_inverted = invertTree(root.left)
    right_inverted = invertTree(root.right)

    # 再把翻转后的左右子树互换
    root.left = right_inverted
    root.right = left_inverted

    return root                    # 返回当前子树的根
```

#### 复杂度

- **时间复杂度**：`O(n)` — 每个节点恰好被访问一次，像“把每颗水果都检查一遍”。
- **空间复杂度**：`O(h)` — 递归栈的深度等于树的高度，最坏 `O(n)`，最优 `O(log n)`。

---

### 2. 最优解

#### 思路  

虽然递归已经是线性时间，但它会占用额外的递归栈空间。我们可以 **用显式的队列（或栈）实现迭代遍历**，把递归转成 **广度优先搜索（BFS）** 或 **深度优先搜索（DFS）**，从而把空间控制在 `O(width)` 或 `O(height)`。

- **瓶颈**：递归的调用栈在极端不平衡的树上会很深，容易导致栈溢出。  
- **优化**：使用 **队列**（BFS）一次遍历所有节点，同时只在队列里保存当前层的节点。这样空间最多是树最宽的那一层的节点数，最坏情况下仍是 `O(n)`，但对大多数平衡树来说会更省空间，而且不会因为递归深度而出错。  

**核心算法**：  
1. 把根节点放进队列。  
2. 当队列不为空时，弹出一个节点 `cur`。  
3. 交换 `cur.left` 与 `cur.right`（这一步和递归版相同）。  
4. 如果左子节点（已交换后其实是原来的右子节点）不为空，加入队列；右子节点同理。  
5. 循环结束后，整棵树已经翻转。

**类比**：把树的每一层想象成一排排的学生，老师让每个学生把左手和右手互换，然后再让所有学生排成新的一列继续下一个动作。队列就像老师手里的一张名单，记录待处理的学生。

#### 代码（Python）

```python
from collections import deque

def invertTree(root: TreeNode) -> TreeNode:
    """
    迭代版（BFS）：使用队列逐层遍历并交换左右子树
    """
    if root is None:
        return None

    q = deque([root])               # 把根节点放进队列
    while q:
        cur = q.popleft()           # 取出当前节点

        # 交换左右子树
        cur.left, cur.right = cur.right, cur.left

        # 把子节点加入队列，后面继续处理
        if cur.left:
            q.append(cur.left)
        if cur.right:
            q.append(cur.right)

    return root
```

#### 复杂度

- **时间复杂度**：`O(n)` — 每个节点仍然只被处理一次，和递归版一样，只是把“遍历”方式换成了“层层推进”。  
- **空间复杂度**：`O(w)` — `w` 为树的最大宽度（即任意一层的节点数）。在完全二叉树中，宽度约为 `n/2`，最坏仍是 `O(n)`，但对平衡树来说大约是 `O(log n)`，通常比递归栈更友好。

---

## 心得

- **核心技巧**：**遍历二叉树并在遍历过程中原地交换左右子节点**。这是一种“就地翻转”思路，适用于所有需要对每个节点进行局部修改的树形问题。  
- **适用的题型**：  
  1. **对称二叉树**（判断左右子树是否镜像）  
  2. **二叉树的层序遍历**（需要逐层访问）  
  3. **二叉树的路径求和**（需要在遍历中累计信息）  
- **一句话总结**：**遍历 + 交换**，把每个节点的左右指针互换，即可得到镜像树。

## 反思

- **第一反应**：看到“invert”，立刻想到“把左右子树调换”，于是想到了递归遍历每个节点并交换。  
- **最容易踩的坑**：  
  - 忘记在递归/迭代结束后返回根节点，导致最终结果是 `None`。  
  - 对空树（`root = None`）没有做特殊处理，会导致空指针异常。  
  - 在迭代版里，交换左右指针后 **先检查子节点是否为 None 再入队**，否则会把 `None` 加进队列，引起错误。  
- **下次第一步**：先判断树是否为空，然后决定是 **递归**（代码更简洁）还是 **迭代**（避免递归深度）来遍历整棵树；遍历时记得“**交换左右指针**”。