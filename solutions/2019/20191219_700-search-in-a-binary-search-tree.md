# #700. 在二叉搜索树中搜索 / Search in a Binary Search Tree

> 难度：简单 · 标签：Tree、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/search-in-a-binary-search-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary search tree (BST) and an integer val.
Find the node in the BST that the node's value equals val and return the subtree rooted with that node. If such a node does not exist, return null.

**Examples**

**Example 1:**

```
Input: root = [4,2,7,1,3], val = 2
Output: [2,1,3]
```

**Example 2:**

```
Input: root = [4,2,7,1,3], val = 5
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [1, 5000].
- 1 <= Node.val <= 107
- root is a binary search tree.
- 1 <= val <= 107

---

## 题目（中文翻译）

给定一棵二叉搜索树（BST）的根节点 `root` 和一个整数 `val`。  
寻找 BST 中值等于 `val` 的节点，并返回以该节点为根的子树（subtree）。如果不存在这样的节点，返回 `null`。  

**示例 1**  
**示例 2**  

**约束条件**  
- 树中节点的数量范围为 `[1, 5000]`。  
- `1 <= Node.val <= 10^7`。  
- `root` 为一棵二叉搜索树。  
- `1 <= val <= 10^7`。  

**示例**  

**示例 1:**  
```
Input: root = [4,2,7,1,3], val = 2
Output: [2,1,3]
```

**示例 2:**  
```
Input: root = [4,2,7,1,3], val = 5
Output: []
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是「把整棵树都翻一遍」，只要找到值等于 `val` 的节点就返回它。  
这可以用 **深度优先遍历**（DFS）来实现：

* 把树看成一棵「家谱」，我们从根节点（祖先）开始，依次检查每一位亲戚的名字（节点的 `val`），如果名字对了就停下来，否则继续往下找。
* 实现上可以用递归（每次往左子树、右子树递进）或显式栈模拟递归。

这种方法不利用二叉搜索树的「左小右大」特性，只是把所有节点都检查一遍，所以一定能找到（如果存在的话），也一定能返回正确的子树。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def dfs_search(root: TreeNode, val: int) -> TreeNode:
    """
    暴力 DFS：遍历所有节点，找到值等于 val 的节点
    """
    if root is None:                     # 空节点，说明没有找到
        return None

    if root.val == val:                  # 找到了，直接返回该节点（即整棵子树的根）
        return root

    # 先在左子树里找
    left_res = dfs_search(root.left, val)
    if left_res:                         # 左子树已经找到了
        return left_res

    # 左子树没有，继续在右子树里找
    return dfs_search(root.right, val)
```

#### 复杂度  

- **时间复杂度**：`O(N)`  
  这里的 `N` 是树中节点的总数。因为最坏情况下我们要把每个节点都检查一遍（比如目标值根本不在树里），所以时间随节点数线性增长。  
  大白话：如果树有 1000 个节点，最多会看 1000 次。

- **空间复杂度**：`O(H)`（递归栈）  
  `H` 是树的高度。递归调用会占用栈空间，最深的递归层数等于从根到最深叶子的路径长度。  
  - 对于平衡树，`H ≈ log₂N`，空间大约是对数级别。  
  - 对于极端的“链表形”树，`H = N`，最坏情况需要 `N` 层栈。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **不利用二叉搜索树的顺序特性**。  
在 BST 中：

- 左子树所有节点的值 **都小于** 当前节点的值。  
- 右子树所有节点的值 **都大于** 当前节点的值。

这正好像在一本 **有序字典**（dictionary）里查单词——可以根据比较结果决定向左（更小）还是向右（更大）继续找，而不必把所有页都翻一遍。

**优化步骤**：

1. 从根节点开始比较 `val` 与当前节点的 `val`。  
2.  
   - 如果相等，直接返回当前节点。  
   - 如果 `val` 小于当前节点的值，只需要在 **左子树** 继续搜索。  
   - 如果 `val` 大于当前节点的值，只需要在 **右子树** 继续搜索。  
3. 重复上述过程，直到找到目标节点或遇到空指针（说明不存在）。

这就是 **二叉搜索** 的思想，时间只和树的高度 `H` 成正比。对一棵**平衡**的 BST，`H ≈ log₂N`，所以平均时间是对数级别，远快于遍历全部节点。

#### 代码（Python）

```python
def bst_search(root: TreeNode, val: int) -> TreeNode:
    """
    利用 BST 的性质，沿着可能的路径向下搜索。
    """
    cur = root
    while cur:                       # 只要当前节点不为空，就继续比较
        if cur.val == val:           # 找到了，直接返回整棵子树的根
            return cur
        elif val < cur.val:          # 目标更小，只能在左子树
            cur = cur.left
        else:                        # 目标更大，只能在右子树
            cur = cur.right
    # 循环结束说明没有找到
    return None
```

> **提示**：如果你更喜欢递归，也可以把上面的 `while` 改写成递归版本，逻辑完全相同，只是实现方式不同。

#### 复杂度  

- **时间复杂度**：`O(H)`，其中 `H` 是树的高度。  
  - **平均情况**（树近似平衡）`H ≈ log₂N` → `O(log N)`。  
  - **最坏情况**（树退化成链表）`H = N` → `O(N)`。  
  与暴力解相比，平衡时快了很多（对数级 vs 线性级）。

- **空间复杂度**：`O(1)`（迭代版）  
  只使用了常数级别的额外变量 `cur`，没有递归栈。  
  若改写为递归实现，则空间为 `O(H)`，和递归版暴力解相同。

---

## 心得

- **核心技巧**：利用二叉搜索树的「左小右大」性质进行**二分搜索**（类似有序数组的二分查找）。  
- **适用的题型**：  
  1. 在 BST 中插入/删除节点（`Insert into a BST`、`Delete Node in a BST`）。  
  2. 查找两节点之间的最小公共祖先（`Lowest Common Ancestor of a BST`）。  
  3. 求 BST 中第 K 小/大的元素（`Kth Smallest Element in a BST`）。  
- **一句话总结**：**在有序结构里搜索，只在可能的方向前进，别把所有元素都搬出来检查。**

---

## 反思

- **第一反应**：看到「BST」二字，马上想到「左小右大」的特性，应该用二分思路而不是全遍历。  
- **最容易踩的坑**：  
  - 忘记在搜索不到时返回 `None`（LeetCode 需要返回 `null`）。  
  - 递归版没有正确处理基准条件，会导致无限递归。  
  - 对极端不平衡的树要有心理准备，最坏情况仍然是 `O(N)`。  
- **下次类似题的第一步**：先判断数据结构是否有序（如 BST、排序数组、堆），如果有序就尝试 **二分/二叉搜索**，而不是直接遍历全部。