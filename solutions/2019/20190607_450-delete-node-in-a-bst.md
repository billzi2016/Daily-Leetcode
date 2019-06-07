# #450. 删除二叉搜索树中的节点 / Delete Node in a BST

> 难度：中等 · 标签：Tree、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/delete-node-in-a-bst/)

---

## 题目（英文原版）

**Description**

Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return the root node reference (possibly updated) of the BST.
Basically, the deletion can be divided into two stages:
Follow up: Could you solve it with time complexity O(height of tree)?

**Examples**

**Example 1:**

```
Input: root = [5,3,6,2,4,null,7], key = 3
Output: [5,4,6,2,null,null,7]
Explanation: Given key to delete is 3. So we find the node with value 3 and delete it.
One valid answer is [5,4,6,2,null,null,7], shown in the above BST.
Please notice that another valid answer is [5,2,6,null,4,null,7] and it's also accepted.
```

**Example 2:**

```
Input: root = [5,3,6,2,4,null,7], key = 0
Output: [5,3,6,2,4,null,7]
Explanation: The tree does not contain a node with value = 0.
```

**Example 3:**

```
Input: root = [], key = 0
Output: []
```

**Constraints**

- The number of nodes in the tree is in the range [0, 104].
- -105 <= Node.val <= 105
- Each node has a unique value.
- root is a valid binary search tree.
- -105 <= key <= 105

---

## 题目（中文翻译）

给定一棵二叉搜索树 (BST) 的根节点引用 (root node reference) 和一个键值 `key`，在 BST 中删除值等于 `key` 的节点。返回可能已经更新的根节点引用。

基本上，删除过程可以分为两个阶段：

---

## 示例

### 示例 1  
**输入**: `root = [5,3,6,2,4,null,7]`, `key = 3`  
**输出**: `[5,4,6,2,null,null,7]`  
**解释**: 给定的删除键为 3。我们找到值为 3 的节点并将其删除。  
一种合法的答案是 `[5,4,6,2,null,null,7]`，如上图所示的 BST。  
请注意，另一种合法答案是 `[5,2,6,null,4,null,7]`，同样会被接受。

### 示例 2  
**输入**: `root = [5,3,6,2,4,null,7]`, `key = 0`  
**输出**: `[5,3,6,2,4,null,7]`  
**解释**: 树中不存在值为 0 的节点。

### 示例 3  
**输入**: `root = []`, `key = 0`  
**输出**: `[]`  
**解释**: 空树直接返回空。

---

## 约束条件

- 树中节点的数量在 `[0, 10^4]` 范围内。  
- `-10^5 <= Node.val <= 10^5`  
- 每个节点的值唯一。  
- `root` 是一棵合法的二叉搜索树。  
- `-10^5 <= key <= 10^5`

---

## 进阶

能否在 **O(树的高度)**（`O(height of tree)`）的时间复杂度内完成删除操作？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是把整棵二叉搜索树 **展开成一个有序数组**（因为 BST 的中序遍历恰好是升序），  
再把要删除的 `key` 从数组里去掉，最后 **把数组重新构造成一棵 BST**。

- **展开成数组**：把树的每个节点依次放进列表，就像把一本字典的所有词条顺序抄下来。  
- **删除元素**：在列表里找 `key`，如果找不到直接返回原树；如果找到了，用 `list.remove(key)` 把它删掉。  
- **重建树**：把有序数组的中间元素设为根，左半段递归建左子树，右半段递归建右子树——这一步类似把字典的中间页作为目录，然后左边的页再继续拆分。

这种方法一定能得到一棵合法的 BST，因为我们始终保持了 **中序有序** 的特性。  

> **为什么正确？**  
> 1. 中序遍历得到的序列严格递增（题目保证节点值唯一）。  
> 2. 删除元素后序列仍然递增。  
> 3. 用递归方式把递增序列重新组织成平衡二叉搜索树，必然满足左子树 < 根 < 右子树 的 BST 条件。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def deleteNode(root: TreeNode, key: int) -> TreeNode:
    """暴力解：先把树转成有序数组，再删键，最后重建树"""

    # 1. 中序遍历收集所有节点值（得到升序数组）
    inorder_vals = []

    def inorder(node: TreeNode):
        if not node:
            return
        inorder(node.left)               # 先左
        inorder_vals.append(node.val)    # 再根
        inorder(node.right)              # 最后右

    inorder(root)

    # 2. 删除 key（如果不存在就直接返回原树）
    if key not in inorder_vals:          # “字典里根本没有这个词”
        return root
    inorder_vals.remove(key)             # 把对应的页码删掉

    # 3. 根据有序数组重建平衡 BST
    def build(lo: int, hi: int) -> TreeNode:
        """把 inorder_vals[lo:hi]（左闭右开）重建为 BST"""
        if lo >= hi:                      # 区间为空，返回空树
            return None
        mid = (lo + hi) // 2              # 取中间的元素作根
        node = TreeNode(inorder_vals[mid])
        node.left = build(lo, mid)        # 左半段递归建左子树
        node.right = build(mid + 1, hi)   # 右半段递归建右子树
        return node

    return build(0, len(inorder_vals))
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 中序遍历需要遍历所有 `n` 个节点 → `O(n)`。  
  - 列表删除元素是 `O(n)`（最坏要把后面的元素往前搬），但整体仍是线性 `O(n)`。  
  - 重建树同样要遍历一次数组 → `O(n)`。  
  所以总时间是 `n + n + n = O(n)`，也就是“跟树的大小成正比”。

- **空间复杂度**：`O(n)`  
  - 需要额外的数组保存所有节点值，大小为 `n`。  
  - 递归调用栈深度最多 `O(log n)`（因为我们把数组平衡地分割），但这在 `O(n)` 之下可以忽略。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于 **把整棵树都遍历了一遍、再重建**，这会使用 `O(n)` 的额外空间。  
实际上，删除 BST 中的一个节点只需要 **沿着搜索路径走到目标节点**，随后根据它的子树情况局部调整即可，整个过程只涉及树的高度 `h`（`h` 最坏等于 `n`，但在平衡树时大约是 `log n`）。

**关键观察**  
1. **BST 的搜索性质**：如果要找值为 `key` 的节点，只需要从根开始比较大小，向左或向右走，最多走 `h` 步。  
2. **删除节点的三种情况**  
   - **叶子节点**（没有子树）：直接把它设为 `None`。  
   - **只有左子树或只有右子树**：用唯一的子树直接替代被删节点。  
   - **左右子树都有**：需要在左子树中找最大节点（即左子树的最右侧），或在右子树中找最小节点（即右子树的最左侧），把这个“前驱/后继”值搬到被删位置，然后递归删除那个前驱/后继节点。这样可以保证 BST 的有序性不被破坏。

**为什么这样是 O(height)？**  
- 搜索阶段最多走 `h` 步。  
- 若需要找前驱/后继，只会在 **被删节点的左/右子树** 中继续向下走，深度同样不超过 `h`。  
- 所有的指针重新链接都是常数时间的操作。  
于是总时间就是 `O(h)`，空间只用递归栈 `O(h)`（最坏 `O(n)`，但符合题目“跟树高相关”）。

下面给出 **递归实现**，代码里把每一步都写上中文注释，帮助初学者理清思路。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def deleteNode(root: TreeNode, key: int) -> TreeNode:
    """在 BST 中删除 key，时间 O(height)，空间 O(height)"""

    if not root:                     # 空树直接返回 None
        return None

    # 1. 先定位要删除的节点
    if key < root.val:               # 要删的值比当前节点小 → 左子树
        root.left = deleteNode(root.left, key)   # 递归处理左子树
    elif key > root.val:             # 要删的值比当前节点大 → 右子树
        root.right = deleteNode(root.right, key) # 递归处理右子树
    else:                            # 找到了！root.val == key
        # 2. 处理三种删除情况

        # 2.1 没有左子树，直接用右子树替代（可能右子树也是 None）
        if not root.left:
            return root.right

        # 2.2 没有右子树，直接用左子树替代
        if not root.right:
            return root.left

        # 2.3 左右子树都有——找左子树的最大节点（前驱）来替代
        #    也可以找右子树的最小节点（后继），思路相同
        predecessor = root.left
        while predecessor.right:          # 一直往右走，找到最大值
            predecessor = predecessor.right

        # 把前驱的值搬到当前节点
        root.val = predecessor.val

        # 删除前驱节点（因为它的值已经被搬走了），
        # 前驱一定没有右子树，只可能有左子树
        root.left = deleteNode(root.left, predecessor.val)

    return root
```

#### 复杂度

- **时间复杂度**：`O(h)`（`h` 为树的高度）  
  - 搜索目标节点最多走 `h` 步。  
  - 若需要找前驱（左子树最大）或后继（右子树最小），最多再走 `h` 步。  
  - 所有指针修改都是常数时间，所以整体是 `O(h)`。  
  - 对于 **平衡 BST**，`h ≈ log₂ n`，因此时间大约是 `O(log n)`，比暴力 `O(n)` 快很多。

- **空间复杂度**：`O(h)`（递归调用栈）  
  - 递归深度与树的高度相同。  
  - 在最坏情况下（完全不平衡的链表形 BST），`h = n`，空间为 `O(n)`，但仍然符合 “只和高度相关” 的要求。

---

## 心得

- **核心技巧**：**在二叉搜索树中删除节点**，关键是**利用 BST 的有序性**，只在**搜索路径**上做局部调整。  
- **适用场景**：  
  1. **在 BST 中插入/删除**（平衡 BST 如 AVL、红黑树的底层操作）。  
  2. **维护有序集合**（如实现 `std::set`、`TreeSet`）。  
  3. **区间查询**（如把线段树或线段树的变体构造成 BST）。  
- **一句话总结**：  
  “删节点，只要在目标节点所在的**搜索路径**上动手，找到前驱或后继再替换，即可在 `O(树高)` 完成。”

---

## 反思

- **第一反应**：把整棵树“搬走”——先遍历成数组再重建。虽然能正确，但浪费太多时间和空间。  
- **最容易踩的坑**：  
  - **忘记处理左右子树都存在的情况**，直接把左子树或右子树接上会破坏 BST 的顺序。  
  - **前驱（或后继）节点可能还有左子树**，删除前驱时要递归处理，否则会丢失子树。  
  - **递归返回值要记得赋回父节点**（`root.left = deleteNode(...)`），否则修改不会生效。  
- **下次遇到类似题**，第一步应该想到：**利用 BST 的搜索特性定位节点**，然后**根据子树情况局部重连**，而不是整体重建。这样才能达到 `O(height)` 的最优复杂度。