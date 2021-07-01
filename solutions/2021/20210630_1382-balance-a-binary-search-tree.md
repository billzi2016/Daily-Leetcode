# #1382. 平衡二叉搜索树 / Balance a Binary Search Tree

> 难度：中等 · 标签：Divide and Conquer、Greedy、Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/balance-a-binary-search-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary search tree, return a balanced binary search tree with the same node values. If there is more than one answer, return any of them.
A binary search tree is balanced if the depth of the two subtrees of every node never differs by more than 1.

**Examples**

**Example 1:**

```
Input: root = [1,null,2,null,3,null,4,null,null]
Output: [2,1,3,null,null,null,4]
Explanation: This is not the only correct answer, [3,1,4,null,2] is also correct.
```

**Example 2:**

```
Input: root = [2,1,3]
Output: [2,1,3]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- 1 <= Node.val <= 105

---

## 题目（中文翻译）

给定一棵二叉搜索树（binary search tree）的根节点 `root`，返回一棵 **平衡**（balanced）的二叉搜索树，使其包含相同的节点值。若存在多个答案，返回任意一个即可。  

二叉搜索树在每个节点的左右子树深度之差不超过 1 时，被称为平衡的。

**示例 1**  
**输入**: `root = [1,null,2,null,3,null,4,null,null]`  
**输出**: `[2,1,3,null,null,null,4]`  
**解释**: 这并不是唯一的正确答案，`[3,1,4,null,2]` 也是合法的平衡二叉搜索树。

**示例 2**  
**输入**: `root = [2,1,3]`  
**输出**: `[2,1,3]`

**约束条件**

- 树中节点的数量在范围 `[1, 10^4]` 内。  
- `1 <= Node.val <= 10^5`   (节点值范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是：**先把树里的所有节点值全部取出来，再把它们一个一个插入到一棵新的二叉搜索树里**。  
- **取值**可以使用 **中序遍历**（左‑根‑右），因为二叉搜索树的中序遍历恰好是从小到大的有序序列。可以把它想成把一本字典的所有单词顺序抄下来，得到一张排好序的纸。  
- **插入**使用普通的 BST 插入算法：从根开始向左或向右走，找到空位后把新节点挂上去。这个过程就像在一本已经排好序的电话簿里 **逐个** 插入新号码，若每次都从头开始找插入点，最坏情况下会像在长队尾部一次次排队，时间会很长。  

**为什么正确**  
- 中序遍历保证我们得到的所有值和原树完全相同，只是顺序变成了从小到大。  
- BST 插入的定义正好是：左子树所有值 < 当前节点 < 右子树所有值。只要我们按任意顺序把所有值插进去，最终得到的树一定是一棵合法的二叉搜索树。  

**时间/空间复杂度**  
- 中序遍历一次遍历所有 `n` 个节点，时间 `O(n)`，空间（递归栈）`O(h)`，`h` 为原树高度，最坏 `O(n)`。  
- 插入阶段：第 `i` 次插入最多要走 `i-1` 步（因为之前已经插了 `i-1` 个节点），所以总步数约为 `1 + 2 + … + (n-1) = O(n²)`。这就是“慢在哪里”。  
- 额外存放所有节点值的列表需要 `O(n)` 空间。  

> 大白话解释：`O(n²)` 就是说如果节点有 10,000 个，最坏情况下要做大约 100,000,000 次比较，显然会很慢。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# ---------- 暴力解 ----------
def balanceBST_bruteforce(root: TreeNode) -> TreeNode:
    """把所有节点值取出来，再逐个插入新树，时间 O(n²)"""

    # 1. 中序遍历得到有序数组
    inorder_vals = []
    def inorder(node: TreeNode):
        if not node:
            return
        inorder(node.left)          # 先左子树
        inorder_vals.append(node.val)  # 再根节点
        inorder(node.right)         # 最后右子树
    inorder(root)   # 调用

    # 2. 按顺序把每个值插入到新 BST 中
    def insert(root: TreeNode, val: int) -> TreeNode:
        """普通 BST 插入，返回插入后的根节点"""
        if not root:
            return TreeNode(val)   # 空位直接创建新节点
        if val < root.val:
            root.left = insert(root.left, val)   # 插左子树
        else:
            root.right = insert(root.right, val) # 插右子树
        return root

    new_root = None
    for v in inorder_vals:          # 依次插入
        new_root = insert(new_root, v)

    return new_root
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  *解释*：第一次插入只走 0 步，第二次最坏走 1 步，…… 第 n 次最坏走 n‑1 步，所有步数加起来是等差数列，约等于 `n²/2`，所以写成 `O(n²)`。

- **空间复杂度**：`O(n)`  
  *解释*：保存所有节点值的列表需要 `n` 个整数；递归栈深度最坏是 `n`（原树可能是链表形），但这已经包含在 `O(n)` 里。

---  

### 2. 最优解

#### 思路  

从暴力解我们已经知道：**先把树变成有序数组** 是很自然的第一步。  
慢的地方在于**把有序数组再逐个插入**——每次插入都要从根往下走，导致 `O(n²)`。  

如果我们已经有了一个**有序数组**，完全可以直接利用“二分”思想一次性把它变成**平衡二叉搜索树**：

1. **取中间元素** 作为根节点。因为左边的所有元素都比它小，右边的都比它大，恰好满足 BST 的定义。  
2. **左半部分** 递归地构造左子树；**右半部分** 递归构造右子树。递归的终止条件是子数组为空。  

这一步相当于把一本排好序的字典，直接在中间把它折成两半，左半本继续折，右半本继续折，最后得到的结构就是“平衡树”。  
- **平衡**：每一次都选中间的元素，左右子树的节点数最多相差 1，正好满足题目对平衡的要求。  
- **时间**：每个节点只被创建一次，且只做了常数次的数组切片（或索引计算），所以是 `O(n)`。  
- **空间**：除了保存有序数组的 `O(n)`，递归栈深度是树的高度 `log n`（因为每次都把区间对半划分），所以总空间 `O(n)`。

#### 代码（Python）

```python
def balanceBST(root: TreeNode) -> TreeNode:
    """最优解：中序遍历 + 递归构造平衡 BST，时间 O(n)"""

    # 1. 中序遍历得到升序数组
    vals = []
    def inorder(node: TreeNode):
        if not node:
            return
        inorder(node.left)
        vals.append(node.val)
        inorder(node.right)
    inorder(root)

    # 2. 递归把有序数组转成平衡 BST
    def build(lo: int, hi: int) -> TreeNode:
        """在区间 [lo, hi) 内构造子树，返回根节点"""
        if lo >= hi:                     # 空区间，返回空
            return None
        mid = (lo + hi) // 2             # 取中间下标
        node = TreeNode(vals[mid])       # 中间元素成为根
        node.left = build(lo, mid)       # 左半段构造左子树
        node.right = build(mid + 1, hi)  # 右半段构造右子树
        return node

    return build(0, len(vals))
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  *解释*：中序遍历一次遍历 `n` 个节点，构造树的递归每个节点只创建一次，合计仍是 `n` 步，写成 `O(n)`。

- **空间复杂度**：`O(n)`  
  *解释*：存放有序数组需要 `n` 个整数；递归栈深度是 `log n`（因为每次区间对半），相对于 `n` 可以忽略不计，整体仍是 `O(n)`。

---

## 心得

- **核心技巧**：利用 **中序遍历** 把 BST 转成有序数组，再用 **分治（递归）** 把有序数组直接构造成平衡 BST。  
- **适用的题型**  
  1. “把 BST 转成有序数组” 类题目（如第 `98` 题 `Validate Binary Search Tree`）  
  2. “从有序数组/链表构造平衡 BST” 类题目（如第 `108` 题 `Convert Sorted Array to Binary Search Tree`）  
- **解题钥匙**：**“先排序，再二分”** —— 有序 ⇒ 中点 = 根，左/右递归。

## 反思

- **第一反应**：先想到把树“拍平”成列表，再想办法“重新拼装”。这一步已经把问题从树的结构转化为数组的操作，思路更清晰。  
- **最容易踩的坑**  
  - **递归边界**：区间 `[lo, hi)` 必须使用左闭右开，否则容易出现无限递归或遗漏元素。  
  - **空树**：题目保证至少有一个节点，但实现时仍要处理 `None` 的情况，否则会报错。  
  - **中点选取**：`mid = (lo + hi) // 2`（向下取整）即可，保持左右子树节点数差 ≤ 1。  
- **下次遇到同类题**：第一步立刻检查能否把结构转成 **有序序列**（中序遍历、排序等），然后考虑 **二分/分治** 直接构造平衡结构，而不是逐个插入。