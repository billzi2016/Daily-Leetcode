# #1008. 从前序遍历构造二叉搜索树 / Construct Binary Search Tree from Preorder Traversal

> 难度：中等 · 标签：Array、Stack、Tree、Binary Search Tree、Monotonic Stack、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/)

---

## 题目（英文原版）

**Description**

Given an array of integers preorder, which represents the preorder traversal of a BST (i.e., binary search tree), construct the tree and return its root.
It is guaranteed that there is always possible to find a binary search tree with the given requirements for the given test cases.
A binary search tree is a binary tree where for every node, any descendant of Node.left has a value strictly less than Node.val, and any descendant of Node.right has a value strictly greater than Node.val.
A preorder traversal of a binary tree displays the value of the node first, then traverses Node.left, then traverses Node.right.

**Examples**

**Example 1:**

```
Input: preorder = [8,5,1,7,10,12]
Output: [8,5,10,1,7,null,12]
```

**Example 2:**

```
Input: preorder = [1,3]
Output: [1,null,3]
```

**Constraints**

- 1 <= preorder.length <= 100
- 1 <= preorder[i] <= 1000
- All the values of preorder are unique.

---

## 题目（中文翻译）

给定一个整数数组 `preorder`，它表示一棵二叉搜索树（BST）的前序遍历（preorder traversal），请构造这棵树并返回其根节点。

保证对给定的测试用例一定存在满足要求的二叉搜索树。

二叉搜索树是一种二叉树，满足对每个节点 `Node`，其左子树（`Node.left`）中的所有后代节点的值都严格小于 `Node.val`，而右子树（`Node.right`）中的所有后代节点的值都严格大于 `Node.val`。

前序遍历（preorder traversal）指先访问节点自身的值，然后遍历左子树，最后遍历右子树。

## 示例

### 示例 1
**输入**: `preorder = [8,5,1,7,10,12]`  
**输出**: `[8,5,10,1,7,null,12]`

### 示例 2
**输入**: `preorder = [1,3]`  
**输出**: `[1,null,3]`

## 约束

- `1 <= preorder.length <= 100`
- `1 <= preorder[i] <= 1000`
- `preorder` 中的所有值均唯一

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

最直接的想法是：**把先序遍历的序列一个一个取出来，按照二叉搜索树的插入规则放进树里**。  
- **数据结构**：我们只需要一棵二叉搜索树（BST），每个节点用 `TreeNode` 表示，结构类似“字典”里的条目：`key` 是节点的值，`value` 是指向左、右子树的指针。  
- **插入过程**：从根节点开始，若新值比当前节点小，就往左走；比当前节点大，就往右走；直到找到一个空位（`None`），把新节点挂上去。这个过程就像在 **有序的电话号码本** 中查找插入位置——不断比较大小，决定向左还是向右。  

**为什么正确**：先序遍历的第一个元素必然是整棵树的根。随后遍历的每个元素在 BST 中都有唯一的位置（因为所有值互不相同），只要遵循 BST 的左<根<右 的规则插入，就一定能恢复出一棵满足题目要求的树。

**时间/空间分析**：  
- 最坏情况下（比如输入序列是严格递增的），每插入一个新节点都要沿着右子树一直走到最底部，路径长度会是已经插入的节点数 `i`。于是总比较次数是 `1 + 2 + … + (n‑1) = O(n²)`，即 **平方级别** 的时间。  
- 额外空间只用来存放树本身（`n` 个节点）和递归栈（深度 `n`），因此是 **线性** 的 `O(n)`。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int):
        self.val = val          # 节点的值
        self.left = None        # 左子树
        self.right = None       # 右子树

def insert(root: TreeNode, val: int) -> TreeNode:
    """把 val 按 BST 规则插入到以 root 为根的子树，返回子树根节点"""
    if root is None:               # 空位，直接创建新节点
        return TreeNode(val)
    if val < root.val:             # 小于根，往左子树插
        root.left = insert(root.left, val)
    else:                          # 大于根，往右子树插
        root.right = insert(root.right, val)
    return root

def bstFromPreorder_bruteforce(preorder):
    """
    暴力实现：依次把先序遍历的值插入 BST
    """
    if not preorder:
        return None
    root = TreeNode(preorder[0])   # 第一个元素是根
    for v in preorder[1:]:
        insert(root, v)            # 逐个插入
    return root
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - `n` 为数组长度。最坏情况下每插入一次要遍历已经建好的树，形成 `1 + 2 + … + (n‑1)` 次比较。  
- **空间复杂度**：`O(n)`  
  - 需要存储 `n` 个节点的树结构，以及最坏情况下 `n` 层的递归调用栈。

---  

### 2. 最优解  

#### 思路  

暴力解的瓶颈在于**每次插入都要从根开始遍历**。其实我们可以利用先序遍历的特点一次完成构造，做到线性时间。

先序遍历的顺序是：**根 → 左子树 → 右子树**。  
在 BST 中，左子树的所有节点值都 **小于根**，右子树的所有节点值都 **大于根**。  
因此，当我们从左到右读取 `preorder` 时：

1. 当前元素 `x` 必然是最近一个比它**大的**节点的左子树的根（如果存在的话）。  
2. 这正好对应 **单调递增栈**（monotonic stack）的使用场景：栈中保存“还没有确定右子树的节点”。  
3. 当遍历到 `x` 时，**弹出**栈顶所有 **小于 x** 的节点，这些弹出的节点的右子树应该挂 `x`（因为它们的左子树已经在之前处理完了）。  
4. 栈顶（若仍然存在）就是 `x` 的父节点的左子树根，`x` 挂在父节点的 **左** 指针上。  

用图示帮助理解（文字版）：

```
preorder = [8, 5, 1, 7, 10, 12]

遍历 8：
    栈 = [8]                （8 为根）

遍历 5（5 < 8）：
    5 是 8 的左子树，挂在 8.left
    栈 = [8, 5]

遍历 1（1 < 5）：
    1 是 5 的左子树，挂在 5.left
    栈 = [8, 5, 1]

遍历 7（7 > 1）：
    弹出 1（因为 7 > 1），弹出后栈顶是 5
    7 > 5，继续弹出 5，栈顶变为 8
    7 < 8，停止弹出
    此时 7 是栈顶 8 的左子树的**右**子树，即挂在 5.right
    栈 = [8, 7]

遍历 10（10 > 7）：
    弹出 7 → 栈顶 8
    10 > 8，弹出 8 → 栈空
    栈空说明 10 是整棵树的**右**子树根，挂在 8.right
    栈 = [10]

遍历 12（12 > 10）：
    弹出 10，栈空
    12 挂在 10.right
    栈 = [12]
```

整个过程只遍历一次数组，每个元素最多进栈一次、出栈一次，时间 `O(n)`，空间 `O(n)`（栈最多存 `n` 个节点）。

> **核心概念**：**单调栈**（Monotonic Stack）——栈中元素保持单调递增（或递减），常用于“下一个更大/更小元素”等问题。这里我们利用它来确定每个节点的父节点。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int):
        self.val = val
        self.left = None
        self.right = None

def bstFromPreorder(preorder):
    """
    O(n) 单调栈实现
    """
    if not preorder:
        return None

    root = TreeNode(preorder[0])   # 第一个元素一定是根
    stack = [root]                 # 栈中保存尚未确定右子树的节点

    for value in preorder[1:]:
        node = TreeNode(value)

        # 若当前值比栈顶节点大，说明它是栈顶节点的**右子树**根
        # 一直弹出，直到找到第一个比它大的节点（或栈空）
        while stack and value > stack[-1].val:
            last = stack.pop()    # 最近弹出的节点是当前值的父节点

        # 此时有两种可能：
        # 1. 栈为空：说明 node 是整棵树的最右侧节点，挂在 last.right
        # 2. 栈非空且 value < stack[-1].val：node 是 stack[-1] 的左子树根
        if not stack:
            # 栈空时，last 必然已经弹出，是 node 的父节点
            last.right = node
        else:
            # 栈顶仍然比 value 小，说明 node 是左子树根
            stack[-1].left = node

        # 把当前节点压入栈，等待以后可能的右子树
        stack.append(node)

    return root
```

> **代码要点解释**  
> - `stack[-1]` 访问栈顶元素，相当于“查看字典里最近的条目”。  
> - `while` 循环负责弹出所有比当前值小的节点，这一步相当于“把已经确定左子树的节点交给右子树”。  
> - `last` 记录最后一次弹出的节点，它恰好是当前节点的父节点（当栈为空时）。  
> - 最后把当前节点压栈，以备后续更大的节点作为它的右子树。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个元素只进栈一次、出栈一次，整体线性遍历。相比暴力解的 `O(n²)`，速度提升显著。  
- **空间复杂度**：`O(n)`  
  - 需要保存树本身的 `n` 个节点以及最坏情况下 `n` 长度的栈（当数组严格递减时，所有节点都在栈中）。

---  

## 心得  

- **核心技巧**：**单调栈**（Monotonic Stack）配合 BST 的大小关系，用一次遍历完成树的构造。  
- **适用场景**：  
  1. “下一个更大元素”/“下一个更小元素”类问题（LeetCode 496、105）  
  2. 根据先序/后序序列重建二叉树（如本题、LeetCode 1008）  
  3. 区间划分、直方图最大矩形等需要快速找“最近更大/更小”的场景。  
- **一句话总结**：**利用先序遍历的根→左→右 顺序，用单调递增栈一次扫描即可确定每个节点的父子关系**。

---  

## 反思  

- **第一反应**：直接把每个数插进去，想到的就是普通的 BST 插入实现。  
- **最容易踩的坑**：  
  - 忘记处理 **栈空** 的情况，导致 `last` 未定义。  
  - 错把弹出后 `last` 当作左子树的父节点，导致树结构错误。  
  - 递归实现时没有维护全局索引，会出现重复使用同一元素的错误。  
- **下次思考同类题**：  
  1. 先确认遍历顺序（先序、后序、中序）与 BST 的大小约束的对应关系。  
  2. 问自己：“是否可以用单调栈/双指针一次遍历得到父子关系？”  
  3. 若答案是肯定的，就尝试设计 **单调栈** 或 **递归+上下界** 的线性解。