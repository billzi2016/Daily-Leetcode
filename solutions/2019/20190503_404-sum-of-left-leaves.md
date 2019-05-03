# #404. 左叶子之和 / Sum of Left Leaves

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/sum-of-left-leaves/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the sum of all left leaves.
A leaf is a node with no children. A left leaf is a leaf that is the left child of another node.

**Examples**

**Example 1:**

```
Input: root = [3,9,20,null,null,15,7]
Output: 24
Explanation: There are two left leaves in the binary tree, with values 9 and 15 respectively.
```

**Example 2:**

```
Input: root = [1]
Output: 0
```

**Constraints**

- The number of nodes in the tree is in the range [1, 1000].
- -1000 <= Node.val <= 1000

---

## 题目（中文翻译）

给定二叉树（binary tree）的根节点 `root`，返回所有左叶子（left leaves）的值之和。  
叶子（leaf）是指没有子节点（children）的节点。左叶子（left leaf）是指作为另一个节点的左子节点（left child）的叶子节点。

**示例 1**

**示例 2**

**约束条件**

**示例**

示例 1:  
Input: root = [3,9,20,null,null,15,7]  
Output: 24  
Explanation: 二叉树中有两个左叶子，值分别为 9 和 15。

示例 2:  
Input: root = [1]  
Output: 0  
Explanation: 树中只有根节点，没有左叶子，故和为 0。

约束条件：

- 树中节点的数量在 `[1, 1000]` 范围内。
- `-1000 <= Node.val <= 1000`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是**遍历整棵二叉树**，把每个节点当作“父节点”来检查：  
- 如果它的左孩子是叶子节点（即左孩子没有左、右子树），就把左孩子的值加入答案。  
- 继续把左孩子和右孩子都递归（或循环）遍历下去，确保每个节点都被检查到。

> **数据结构类比**：遍历二叉树就像在一棵家谱树里逐层找亲戚，`TreeNode` 就是每个人，左孩子、右孩子分别对应“爸爸的左边孩子”“爸爸的右边孩子”。我们要把所有“只会站在左边、且没有子女”的人（左叶子）挑出来并把他们的“财富”（节点值）加起来。

**为什么正确**：  
- 题目要求求所有左叶子的值之和，而左叶子一定是某个节点的左孩子且本身没有子节点。只要遍历到每个节点并检查它的左孩子是否满足“是叶子”，就不会漏掉任何左叶子，也不会把非左叶子计入。

**时间/空间复杂度**（大白话）：

| 复杂度 | 含义 |
|-------|------|
| **时间** `O(n)` | `n` 是树的节点数。我们要把每个节点都看一遍，就像数一遍班级里所有同学的名字，需要 `n` 次操作。 |
| **空间** `O(h)` | 递归调用会占用栈空间，栈的深度等于树的高度 `h`（最坏情况是 `n`，相当于一条长链）。如果用显式的栈/队列，也需要同样数量的额外空间。 |

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def sumOfLeftLeaves(root: TreeNode) -> int:
    """
    暴力递归遍历整棵树，累加所有左叶子的值
    """
    if not root:                 # 空树直接返回 0
        return 0

    total = 0

    # 检查左孩子是否为叶子
    if root.left and not root.left.left and not root.left.right:
        total += root.left.val   # 左叶子 → 加上它的值

    # 递归处理左子树和右子树
    total += sumOfLeftLeaves(root.left)   # 继续往左走
    total += sumOfLeftLeaves(root.right)  # 继续往右走

    return total
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 每个节点只被访问一次，就像一次完整的点名，人数多少决定时间多少。  
- **空间复杂度**：`O(h)` —— 递归栈的深度等于树的高度，最坏情况下（完全倾斜的链）会是 `n`，但在平衡树里大约是 `log n`。

---

### 2. 最优解

#### 思路  

从暴力解来看，**慢的地方其实只有遍历本身**，因为我们已经在 `O(n)` 的时间里把所有节点检查了一遍。对这道题已经没有更快的办法（必须看每个节点才能确认它是不是左叶子），所以“最优”主要体现在：

1. **代码简洁、可读性高**  
2. **空间使用更友好**（如果不想用递归栈，可以改成显式的栈或队列）

下面给出两种等价的最优实现：

- **深度优先搜索（DFS）递归**：保持前面的递归思路，只把判断左叶子的代码抽离成一个帮助函数，让主函数更直观。  
- **广度优先搜索（BFS）迭代**：使用队列层层遍历，避免递归深度导致的栈溢出风险，空间上最多保存同一层的节点数（最坏 `O(n)`）。

> **核心概念——遍历**  
> - **DFS**：像“爬山”，一路向下到叶子再回溯。  
> - **BFS**：像“层层扫地”，一次扫完当前层的所有节点，再进入下一层。  
> 两者都能保证每个节点只被访问一次。

#### 代码（Python）

**（1）DFS 递归（更简洁）**

```python
def sumOfLeftLeaves(root: TreeNode) -> int:
    """
    递归版 DFS：把“左叶子是否满足条件”封装成一个小函数，
    主函数只负责遍历整棵树。
    """
    def is_leaf(node: TreeNode) -> bool:
        # 叶子节点：左右子树都是 None
        return node is not None and node.left is None and node.right is None

    if not root:
        return 0

    total = 0
    # 若左孩子是叶子，则计入
    if root.left and is_leaf(root.left):
        total += root.left.val

    # 继续向下遍历左、右子树
    total += sumOfLeftLeaves(root.left)
    total += sumOfLeftLeaves(root.right)
    return total
```

**（2）BFS 迭代（避免递归深度）**

```python
from collections import deque

def sumOfLeftLeaves(root: TreeNode) -> int:
    """
    队列实现的层序遍历（BFS），在遍历过程中检测左叶子。
    """
    if not root:
        return 0

    ans = 0
    q = deque([root])          # 初始把根节点放进队列

    while q:
        node = q.popleft()     # 取出当前节点

        # 检查左孩子是否为叶子
        if node.left:
            if not node.left.left and not node.left.right:  # 左叶子
                ans += node.left.val
            else:                      # 不是叶子，继续入队
                q.append(node.left)

        # 右孩子不需要判断左叶子，只要继续遍历即可
        if node.right:
            q.append(node.right)

    return ans
```

#### 复杂度

- **时间复杂度**：`O(n)` —— 无论是 DFS 还是 BFS，都必须访问每个节点一次，等价于一次完整点名。  
- **空间复杂度**：  
  - DFS 递归：`O(h)`（递归栈深度）。在平衡树里约为 `log n`，最坏情况下（链状）为 `n`。  
  - BFS 迭代：`O(w)`，其中 `w` 是树的最大宽度（同层最多节点数），最坏也可能是 `n`，但在大多数二叉树里会小于 `n`。

与暴力解相比，时间没有提升（因为已经是最底层），但代码结构更清晰，且提供了 **非递归** 的实现，降低了递归深度导致的栈溢出风险。

---

## 心得

- **核心技巧**：二叉树遍历（DFS / BFS）+ 叶子节点判定。  
- **适用的题型**  
  1. “求所有右叶子之和”（与左叶子同理）  
  2. “统计叶子节点的个数”  
  3. “求二叉树的最大深度”或“求二叉树的最小深度”——都需要遍历全部节点并在遍历过程中累计信息。  
- **一句话总结解题钥匙**：**遍历每个节点，遇到左孩子且它是叶子就加值**。

---

## 反思

- **第一反应**：看到“左叶子”这两个关键词，我立刻想到“遍历树 + 判断左孩子是否为叶子”。  
- **最容易踩的坑**  
  - 把“左叶子”误写成“左子树的所有节点”，导致错误计数。  
  - 忘记判断左孩子本身是否为叶子（只判断是否是左孩子会把左子树内部节点也算进去）。  
  - 边界情况：只有根节点（没有左叶子）时应返回 `0`。  
- **下次类似题的第一步**：先把 **遍历框架**（DFS 或 BFS）写出来，再在遍历过程中 **加上具体的判定条件**（本题是“左且是叶子”）。这样可以保证不遗漏任何节点，也避免逻辑混乱。