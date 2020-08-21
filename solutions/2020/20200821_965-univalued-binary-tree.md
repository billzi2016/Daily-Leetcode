# #965. 单值二叉树 / Univalued Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/univalued-binary-tree/)

---

## 题目（英文原版）

**Description**

A binary tree is uni-valued if every node in the tree has the same value.
Given the root of a binary tree, return true if the given tree is uni-valued, or false otherwise.

**Examples**

**Example 1:**

```
Input: root = [1,1,1,1,1,null,1]
Output: true
```

**Example 2:**

```
Input: root = [2,2,2,5,2]
Output: false
```

**Constraints**

- The number of nodes in the tree is in the range [1, 100].
- 0 <= Node.val < 100

---

## 题目（中文翻译）

二叉树（binary tree）如果其所有节点的值都相同，则称为单值二叉树。给定二叉树的根节点 `root`，若该树是单值二叉树返回 `true`，否则返回 `false`。

## 示例

### 示例 1
**输入:** `root = [1,1,1,1,1,null,1]`  
**输出:** `true`

### 示例 2
**输入:** `root = [2,2,2,5,2]`  
**输出:** `false`

## 约束条件

- 树中节点的数量在 `[1, 100]` 区间内。
- `0 <= Node.val < 100`（`Node.val` 为节点的值）。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整棵二叉树的所有节点值都收集起来，然后一次性判断这些值是否全部相同。  

- **遍历二叉树**：可以用递归（前序遍历）把每个节点的 `val` 加到一个列表 `vals` 中。递归就像把树“一层层拆开”，把左子树、右子树的值都依次放进列表。  
- **检查是否全相同**：把列表转成集合 `set(vals)`，如果集合里只有一种数（集合大小为 1），说明所有节点值相同。  
- **类比**：把树看成一本书的章节，先把每一页的文字全部抄到一张纸上（收集），再把纸上的文字全部比对一遍（检查）。  

这种方法之所以 **正确**，是因为我们把所有节点的值都完整地拿出来了，只要这些值里没有出现不同的数，就一定是单值树。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树（也是 TreeNode 或 None）
        self.right = right      # 右子树（也是 TreeNode 或 None）

def isUnivalTree_bruteforce(root: TreeNode) -> bool:
    """暴力解：先把所有节点值收集到列表，再判断是否全部相同"""

    vals = []                     # 用来保存遍历到的所有节点值

    def preorder(node: TreeNode):
        """前序遍历，把每个节点的值加入 vals"""
        if not node:              # 空节点直接返回
            return
        vals.append(node.val)     # 记录当前节点的值
        preorder(node.left)       # 递归左子树
        preorder(node.right)      # 递归右子树

    preorder(root)                # 从根节点开始遍历

    # 把列表转成集合，集合里元素唯一，若集合大小为 1 则所有值相同
    return len(set(vals)) == 1
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 必须访问树中的每个节点一次，`n` 是节点数。  
- **空间复杂度**：`O(n)` —— 额外用了一个列表 `vals` 保存所有节点值，最坏情况下要存 `n` 个数。递归栈本身也会占 `O(h)`（`h` 为树高），但这里的主导因素是列表的 `O(n)`。

---

### 2. 最优解

#### 思路  

在暴力解中，我们先把所有值全部收集完才开始比较，这会占用额外的 `O(n)` 空间，而且即使在树的上层已经出现不同的值，也要继续遍历完剩下的节点。  
**优化点** 在于**边遍历边比较**：只要发现任意一个节点的值和根节点的值不同，就可以立刻返回 `False`，不必继续遍历其余子树。

实现思路：

1. 记录根节点的值 `target = root.val`，它是我们要和所有其他节点比较的“标准”。  
2. 用 **深度优先搜索（DFS）**（递归版）或 **广度优先搜索（BFS）**（队列版）遍历整棵树。  
3. 每访问到一个节点，就立刻检查 `node.val == target`。如果不相等，直接返回 `False`。  
4. 若遍历结束都没有冲突，则返回 `True`。

- **DFS（递归）**：把树想象成一条可以一直往下走的“隧道”，每进入一个分叉点（节点），先检查再继续往左、右两边走。  
- **BFS（队列）**：把树想象成一层层的“楼层”，先检查完第 `k` 层的所有节点，再进入第 `k+1` 层。实现时用 `collections.deque` 当队列，先进先出，保证按层次遍历。

下面给出递归版（最常用），它的空间主要是递归栈，最坏情况是 `O(n)`（链状树），平均是 `O(log n)`（平衡树）。

#### 代码（Python）

```python
def isUnivalTree_opt(root: TreeNode) -> bool:
    """最优解：遍历时即时比较，发现不同立即返回"""

    target = root.val   # 所有节点都应该等于这个值

    def dfs(node: TreeNode) -> bool:
        if not node:                 # 空节点自然符合
            return True
        if node.val != target:       # 一旦发现不同，直接返回 False
            return False
        # 递归检查左、右子树，只有两边都返回 True 才算整体 True
        return dfs(node.left) and dfs(node.right)

    return dfs(root)
```

如果想用 **BFS（队列）** 也可以：

```python
from collections import deque

def isUnivalTree_bfs(root: TreeNode) -> bool:
    target = root.val
    q = deque([root])               # 初始化队列，只放根节点

    while q:
        node = q.popleft()          # 取出队首节点
        if node.val != target:      # 发现不相等立刻返回
            return False
        if node.left:
            q.append(node.left)     # 左子树加入队列
        if node.right:
            q.append(node.right)    # 右子树加入队列
    return True                     # 所有节点都相同
```

#### 复杂度  

- **时间复杂度**：`O(n)` —— 每个节点最多检查一次，和暴力解相同，但如果提前发现不相等，可能会更早结束。  
- **空间复杂度**：`O(h)`（递归版）或 `O(w)`（BFS 版），其中 `h` 是树的高度，`w` 是同层节点数（最大宽度）。在最坏的链状树中 `h = n`，但平衡树下只需要 `O(log n)` 的栈空间/队列空间。

---

## 心得

- **核心技巧**：**遍历时即时比较**（“一边走一边检查”），避免额外存储所有节点值。  
- **适用的题型**  
  1. 判断二叉树是否满足某种统一性质（例如：所有节点值都为偶数）。  
  2. 判断二叉搜索树（BST）是否合法——需要在遍历时维护上下界。  
  3. 判断是否所有叶子节点深度相同——在遍历时记录第一次出现的叶子深度并比较。  
- **一句话总结**：**“遍历即比较，出现不同立即退出”** 是解这类“全局一致性”问题的钥匙。

---

## 反思

- **第一反应**：看到“所有节点值相同”，立刻想到把所有值收集起来再统一判断。  
- **最容易踩的坑**  
  - **空树**：题目保证至少有一个节点，但如果自行扩展，需要处理 `root is None` 的情况。  
  - **递归深度**：极端不平衡的树会导致递归层数等于节点数，可能触发 Python 的递归深度限制（默认约 1000），此时可以改用显式栈或 BFS。  
- **下次类似题**：先问自己 **“是否可以在遍历的过程中直接得出答案？”**，如果答案是“可以”，就把比较/统计放在遍历里，而不是事后再统一处理。这样既省空间，又可能更早结束搜索。