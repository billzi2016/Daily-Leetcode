# #669. 修剪二叉搜索树 / Trim a Binary Search Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/trim-a-binary-search-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary search tree and the lowest and highest boundaries as low and high, trim the tree so that all its elements lies in [low, high]. Trimming the tree should not change the relative structure of the elements that will remain in the tree (i.e., any node's descendant should remain a descendant). It can be proven that there is a unique answer.
Return the root of the trimmed binary search tree. Note that the root may change depending on the given bounds.

**Examples**

**Example 1:**

```
Input: root = [1,0,2], low = 1, high = 2
Output: [1,null,2]
```

**Example 2:**

```
Input: root = [3,0,4,null,2,null,null,1], low = 1, high = 3
Output: [3,2,null,1]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- 0 <= Node.val <= 104
- The value of each node in the tree is unique.
- root is guaranteed to be a valid binary search tree.
- 0 <= low <= high <= 104

---

## 题目（中文翻译）

给定一棵 **二叉搜索树 (binary search tree)** 的根节点 `root`，以及下界 `low` 和上界 `high`，请修剪这棵树，使得所有剩余节点的值都位于区间 **[low, high]** 内。修剪过程中不能改变仍然保留在树中的节点之间的相对结构（即任意节点的后代仍然是其后代）。可以证明，满足条件的修剪结果唯一。

返回修剪后的 **二叉搜索树 (binary search tree)** 的根节点 `root`。注意，根节点可能会因为修剪而改变。

**示例 1**

**输入**  
`root = [1,0,2], low = 1, high = 2`

**输出**  
`[1,null,2]`

**示例 2**

**输入**  
`root = [3,0,4,null,2,null,null,1], low = 1, high = 3`

**输出**  
`[3,2,null,1]`

**约束条件**

- 树中节点的数量在 `[1, 10^4]` 范围内。  
- `0 <= Node.val <= 10^4`（`Node.val` 为节点的值）。  
- 树中每个节点的值互不相同。  
- `root` 必定是一棵有效的 **二叉搜索树 (binary search tree)**。  
- `0 <= low <= high <= 10^4`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **把整棵树的所有节点都拿出来，挑出符合区间 `[low, high]` 的节点，再用这些节点重新造一棵二叉搜索树**。  
可以把这一步想象成：

1. **遍历树**：像在森林里把每棵树的所有果子都摘下来，用列表把它们装起来。遍历方式可以是前序/中序/后序，这里用中序遍历（左‑根‑右），因为二叉搜索树的中序遍历本身就是从小到大的有序序列，和我们后面“重建树”很配。
2. **过滤**：把不在 `[low, high]` 区间的果子丢掉，只留下合格的。
3. **重建 BST**：把剩下的果子一个一个插回空树，插入过程保持二叉搜索树的性质。插入就像把每个果子放进一个已经排好序的抽屉里，需要比较大小决定放左边还是右边。

> **类比**：  
> - **哈希表**像字典，`key` 是单词，`value` 是页码。  
> - **这里的列表**就像装满所有单词的纸条，**过滤**相当于把不在字母表区间的纸条撕掉，**插入新树**相当于把剩下的纸条重新装进字典里。

只要我们把所有合法节点重新插入，最终得到的树一定满足：
- 所有节点值都在 `[low, high]`；
- 插入过程本身保证了相对结构（左子树全小，右子树全大），即满足二叉搜索树的定义。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def inorder_collect(root, low, high, arr):
    """
    中序遍历整棵树，把所有节点值收集到 arr 中。
    """
    if not root:
        return
    inorder_collect(root.left, low, high, arr)   # 先左
    if low <= root.val <= high:                  # 只保留合法区间的值
        arr.append(root.val)
    inorder_collect(root.right, low, high, arr)  # 再右


def insert_into_bst(root, val):
    """
    把 val 插入到已有的二叉搜索树中，返回新的根节点。
    """
    if not root:
        return TreeNode(val)                     # 空树直接生成新节点
    if val < root.val:
        root.left = insert_into_bst(root.left, val)   # 插入左子树
    else:
        root.right = insert_into_bst(root.right, val) # 插入右子树
    return root


def trimBST_bruteforce(root, low, high):
    """
    暴力解：先收集合法节点，再逐个插入重建 BST。
    """
    vals = []                                     # 用来保存所有合法值
    inorder_collect(root, low, high, vals)       # 第一步：遍历收集

    new_root = None
    for v in vals:                                # 第二步：逐个插入
        new_root = insert_into_bst(new_root, v)
    return new_root
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 第一次中序遍历是 `O(n)`（遍历每个节点一次）。  
  - 插入每个合法节点时，平均需要走树高 `log n`（因为树是平衡的近似），共插入 `k`（`k ≤ n`）次，所以是 `O(k log n)`，最坏 `k = n`，整体 `O(n log n)`。  
  - 用大白话说，就是“先把所有水果摘下来（`n` 次），再把每个水果放进抽屉（平均 `log n` 次比较）”，所以总工作量大概是 `n × log n`。

- **空间复杂度**：`O(n)`  
  - `vals` 列表最坏会存下所有节点的值，需要 `n` 的空间。  
  - 递归遍历和插入也会使用栈空间，最深 `O(h)`，`h` 最坏是 `n`，但已经计入 `O(n)`。

---

### 2. 最优解

#### 思路  

暴力解的 **瓶颈** 在于我们把所有节点都遍历一遍后，又**重新插入**了一遍，这一步其实可以省掉。二叉搜索树本身的结构已经帮我们把“不合格的子树”提前筛掉了，只要**在遍历的同时直接裁剪**，就不需要再重建。

关键观察：

1. **如果当前节点的值 `< low`**，说明它和它的左子树全部都比 `low` 小（因为左子树的所有值都更小），这整棵左子树都不可能保留。我们直接**把当前节点换成右子树的裁剪结果**，相当于把左子树“剪掉”。  
2. **如果当前节点的值 `> high`**，同理右子树全部都太大，直接把当前节点换成左子树的裁剪结果。  
3. **否则**（`low ≤ val ≤ high`），当前节点是合法的，我们递归地**分别裁剪左右子树**，并把裁剪后的子树重新挂回当前节点。

这就是 **递归版的“剪枝”**，利用了二叉搜索树的有序性，一遍遍历即可完成裁剪。

> **类比**：  
> 想象你在一本按字母顺序排好的电话簿里找名字在 `[A, M]` 区间的联系人。  
> - 当翻到一个字母 **小于 A** 的页时，你可以直接把整本左边的（更小的）页撕掉，因为全不符合。  
> - 当翻到一个字母 **大于 M** 的页时，右边的（更大的）页也全可以撕掉。  
> - 只剩下字母在 `[A, M]` 区间的页需要细看并继续处理。  
> 这就是我们对树的“剪枝”过程。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def trimBST(root, low, high):
    """
    递归裁剪二叉搜索树，使所有节点值落在 [low, high] 区间。
    """
    if not root:                     # 空树直接返回 None
        return None

    # 1️⃣ 当前节点值太小 → 左子树全不合法，直接去右子树
    if root.val < low:
        # 把右子树继续裁剪后返回，等价于把当前节点“换成”右子树
        return trimBST(root.right, low, high)

    # 2️⃣ 当前节点值太大 → 右子树全不合法，直接去左子树
    if root.val > high:
        return trimBST(root.left, low, high)

    # 3️⃣ 当前节点合法 → 递归裁剪左右子树
    root.left = trimBST(root.left, low, high)     # 处理左子树
    root.right = trimBST(root.right, low, high)   # 处理右子树
    return root                                   # 返回已经裁剪好的根节点
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个节点最多被访问一次，裁剪过程没有额外的遍历或插入操作。用大白话说，就是“只走一次森林里每棵树的每个枝桠”，所以是线性时间。

- **空间复杂度**：`O(h)`（递归栈空间）  
  `h` 是树的高度。最坏情况下（树退化成链表）`h = n`，所以最坏是 `O(n)`；在平衡树里 `h ≈ log n`，空间需求更小。这里的空间主要是函数调用栈保存的临时信息。

---

## 心得

- **核心技巧**：利用二叉搜索树的有序性进行**递归剪枝**（或叫“区间裁剪”）。  
- **适用的题型**：  
  1. “在 BST 中查找/删除区间内的节点” 如 **LeetCode 669. Trim a Binary Search Tree**（本题）。  
  2. “在 BST 中删除一个节点” **LeetCode 450. Delete Node in a BST**。  
  3. “在 BST 中搜索区间和” **LeetCode 938. Range Sum of BST**（需要遍历并利用区间剪枝提升效率）。  
- **一句话总结**：**只要记住：值太小丢左，值太大丢右，合法的才保留并递归**，就能一次遍历搞定裁剪。

---

## 反思

- **第一反应**：先想到把所有节点收集出来再重新构造——这是一种直观但不够高效的办法。  
- **最容易踩的坑**：  
  - 忘记在 `root.val < low` 或 `> high` 时直接返回裁剪后的子树，而是继续访问已被判定为不合法的子树，导致不必要的递归。  
  - 边界条件 `low == high` 或树只有单节点时的处理，需要确保递归终止条件 `if not root` 正确。  
- **下次遇到同类题**：第一步先**思考值与区间的大小关系**，利用 BST 的左小右大的特性**立即剪掉整棵子树**，再递归处理剩余部分。这样可以把时间复杂度压到线性。