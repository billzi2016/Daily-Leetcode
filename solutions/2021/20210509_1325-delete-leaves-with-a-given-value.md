# #1325. 删除指定值的叶子节点 / Delete Leaves With a Given Value

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/delete-leaves-with-a-given-value/)

---

## 题目（英文原版）

**Description**

Given a binary tree root and an integer target, delete all the leaf nodes with value target.
Note that once you delete a leaf node with value target, if its parent node becomes a leaf node and has the value target, it should also be deleted (you need to continue doing that until you cannot).

**Examples**

**Example 1:**

```
Input: root = [1,2,3,2,null,2,4], target = 2
Output: [1,null,3,null,4]
Explanation: Leaf nodes in green with value (target = 2) are removed (Picture in left). 
After removing, new nodes become leaf nodes with value (target = 2) (Picture in center).
```

**Example 2:**

```
Input: root = [1,3,3,3,2], target = 3
Output: [1,3,null,null,2]
```

**Example 3:**

```
Input: root = [1,2,null,2,null,2], target = 2
Output: [1]
Explanation: Leaf nodes in green with value (target = 2) are removed at each step.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 3000].
- 1 <= Node.val, target <= 1000

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）`root` 和一个整数 `target`，删除所有值等于 `target` 的叶子节点（leaf node）。  
需要注意的是，一旦删除了值为 `target` 的叶子节点，如果它的父节点此时变成了叶子节点且其值仍为 `target`，该父节点也必须被删除——这一过程需要持续进行，直到不存在满足条件的节点为止。

**示例 1**  

**输入**  
```
root = [1,2,3,2,null,2,4], target = 2
```
**输出**  
```
[1,null,3,null,4]
```
**解释**：绿色标记的叶子节点（值为 `target = 2`）被删除（左图）。删除后，新出现的叶子节点仍然值为 `target = 2`（中图），同样被删除。

**示例 2**  

**输入**  
```
root = [1,3,3,3,2], target = 3
```
**输出**  
```
[1,3,null,null,2]
```

**示例 3**  

**输入**  
```
root = [1,2,null,2,null,2], target = 2
```
**输出**  
```
[1]
```
**解释**：每一步都删除值为 `target = 2` 的绿色叶子节点。

**约束条件**  

- 树中节点的数量在 `[1, 3000]` 范围内。  
- `1 <= Node.val, target <= 1000`   (Node.val 表示节点的值)

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是**一次遍历整棵树，找到所有值等于 `target` 的叶子节点并删除**，然后**再从头遍历一次**，因为删除叶子后它的父节点可能变成新的叶子且恰好也等于 `target`，需要继续删。  
我们可以把这一步重复执行，直到一次遍历中没有任何节点被删除为止。  

- **数据结构**：二叉树的节点我们用 `TreeNode` 表示，遍历时使用递归（深度优先）或显式的栈。递归的过程就像我们在**树上走路**：先往左走到底，再往右走到底，最后回到父节点。  
- **为什么正确**：每一次完整遍历都会把当前所有满足条件的叶子节点删掉。由于我们不断重复，所有因父节点变成叶子而出现的新符合条件的节点也一定会在后面的遍历中被删掉，直到再也找不到目标叶子为止。  

**时间复杂度分析（大白话）**：  
- 假设树有 `n` 个节点。一次完整遍历需要查看每个节点一次，时间是 `O(n)`。  
- 但最坏情况下我们可能要遍历 `n` 次（比如一条链状的树，每删掉一个叶子，父节点才会成为新的叶子），于是总时间是 `O(n × n) = O(n²)`。可以把它想象成“把一本 3000 页的书读 `n` 次”。  

**空间复杂度分析**：  
- 递归调用栈的深度等于树的高度。最坏情况下树是链状的，高度为 `n`，所以空间 `O(n)`。如果是平衡树，高度约为 `log n`，则空间更小。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def deleteLeaves(root, target):
    """
    暴力版：反复遍历整棵树，直到一次遍历没有删除任何节点。
    返回处理后的根节点（可能为 None）。
    """
    # 辅助函数：一次遍历中把满足条件的叶子删掉，返回 (new_node, 是否删除了节点)
    def prune(node):
        if not node:
            return None, False

        # 递归处理左右子树
        node.left, _ = prune(node.left)
        node.right, _ = prune(node.right)

        # 现在 node 已经没有了目标叶子子节点
        if not node.left and not node.right and node.val == target:
            # 这就是“叶子且值等于 target”，删掉它
            return None, True
        return node, False

    while True:
        root, changed = prune(root)   # 只做一次完整遍历
        if not changed:               # 本轮没有删任何节点，说明已经完成
            break
    return root
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每次遍历 `O(n)`，最坏会进行 `n` 次。可以把它想象成“把 3000 页的书读了 3000 次”。  
- **空间复杂度**：`O(n)`（递归栈）  
  - 最坏情况下树是链状的，递归深度等于节点数。  

---  

### 2. 最优解  

#### 思路  

从暴力解我们已经知道**重复遍历的根本原因是每次只能看到当前的叶子**。如果我们在**一次遍历**里就把“叶子 → 父节点 → 父节点的父节点 …”的连锁删除全部处理掉，就不需要再循环了。  

这正好可以用**后序遍历（post‑order DFS）**来实现：  

1. 先递归处理左子树、右子树，**保证子树已经被“净化”**（即子树里已经没有目标叶子）。  
2. 当我们回到当前节点时，左、右子树已经是“干净的”。此时只要判断**当前节点是否已经变成叶子且值等于 `target`**，就可以直接删除（返回 `None`）。  
3. 这样一次递归就把所有需要删除的节点全部处理完。  

> **类比**：把树想象成一棵倒挂的挂钩链条。我们先把最底部的钩子（叶子）检查并剪掉，然后向上检查它的上一个钩子，依此类推。只要从最底层往上走一次，就能把所有需要剪掉的钩子一次性处理完。

**关键点**：  
- **后序遍历**（左 → 右 → 根）是必须的，因为只有在子树已经处理好后，才能判断父节点是否变成叶子。  
- 返回值既是**新的子树根节点**（可能为 `None`），也可以直接在函数里把 `None` 赋给父节点的 `left`/`right`。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def deleteLeaves(root, target):
    """
    最优解：一次后序 DFS 完成全部删除。
    返回处理后的根节点（可能为 None）。
    """
    def dfs(node):
        if not node:
            return None                # 空节点直接返回

        # 先递归处理左右子树，得到“清理后”的子树根
        node.left = dfs(node.left)
        node.right = dfs(node.right)

        # 此时 node 的子树已经没有目标叶子
        # 如果 node 本身成为了叶子且值等于 target，就删掉它
        if not node.left and not node.right and node.val == target:
            return None                # 删除，返回空指针给父节点
        return node                    # 否则保留当前节点

    return dfs(root)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只被访问一次，等价于“一次性把 3000 页的书看完”。相比暴力的 `O(n²)`，快了很多。  
- **空间复杂度**：`O(h)`（递归栈），`h` 为树的高度。  
  - 最坏情况（链状树）`h = n`，空间 `O(n)`；平衡树时 `h ≈ log n`，更省内存。  

---

## 心得  

- **核心技巧**：后序深度优先遍历（DFS）配合“自底向上”删除。  
- **适用的题型**：  
  1. “删除二叉树中满足某种条件的叶子”类题（如本题、`Delete Nodes And Return Forest`）。  
  2. “把树中满足条件的子树全部剪掉”类题（如 `Trim a Binary Search Tree`、`Remove Subtrees With Given Sum`）。  
- **解题钥匙**：**先处理子问题，再处理父问题**——即后序遍历。  

## 反思  

- **第一反应**：看到“删除叶子”，自然想到“遍历找叶子、删掉”。于是想到了最直接的循环删法。  
- **最容易踩的坑**：  
  - 忘记在删除叶子后继续检查父节点，导致只删了一层。  
  - 递归返回值写错，把 `node` 本身返回而不是 `None`，导致删除失效。  
  - 边界情况：根节点本身就是唯一的叶子且等于 `target`，需要返回 `None`。  
- **下次思路**：一看到“删除/剪枝”且**依赖父子关系**的题目，第一步就想到**后序遍历**，因为它天然满足“子树先干净，再决定父节点”。