# #701. 插入节点到二叉搜索树 / Insert into a Binary Search Tree

> 难度：中等 · 标签：Tree、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/insert-into-a-binary-search-tree/)

---

## 题目（英文原版）

**Description**

You are given the root node of a binary search tree (BST) and a value to insert into the tree. Return the root node of the BST after the insertion. It is guaranteed that the new value does not exist in the original BST.
Notice that there may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. You can return any of them.

**Examples**

**Example 1:**

```
Input: root = [4,2,7,1,3], val = 5
Output: [4,2,7,1,3,5]
Explanation: Another accepted tree is:
```

**Example 2:**

```
Input: root = [40,20,60,10,30,50,70], val = 25
Output: [40,20,60,10,30,50,70,null,null,25]
```

**Example 3:**

```
Input: root = [4,2,7,1,3,null,null,null,null,null,null], val = 5
Output: [4,2,7,1,3,5]
```

**Constraints**

- The number of nodes in the tree will be in the range [0, 104].
- -108 <= Node.val <= 108
- All the values Node.val are unique.
- -108 <= val <= 108
- It's guaranteed that val does not exist in the original BST.

---

## 题目（中文翻译）

给定一棵二叉搜索树（BST）的根节点 `root` 和一个待插入的数值 `val`，返回插入该数值后 BST 的根节点。题目保证该数值在原始 BST 中不存在。

注意，插入操作可能有多种合法方式，只要插入后仍保持二叉搜索树的性质即可。你可以返回任意一种合法的结果。

**示例 1**  
**输入**: `root = [4,2,7,1,3], val = 5`  
**输出**: `[4,2,7,1,3,5]`  
**解释**: 另一棵被接受的树是：

**示例 2**  
**输入**: `root = [40,20,60,10,30,50,70], val = 25`  
**输出**: `[40,20,60,10,30,50,70,null,null,25]`  

**示例 3**  
**输入**: `root = [4,2,7,1,3,null,null,null,null,null,null], val = 5`  
**输出**: `[4,2,7,1,3,5]`  

**约束条件**  
- 树中节点的数量在区间 `[0, 10^4]` 内。  
- `-10^8 <= Node.val <= 10^8`  
- 所有节点的 `Node.val` 均唯一。  
- `-10^8 <= val <= 10^8`  
- 保证 `val` 不存在于原始 BST 中。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
最直接的想法是把整棵二叉搜索树 **展开成有序序列**，再把新值插进去，最后 **把序列重新组装成一棵 BST**。  

- **展开**：对 BST 做中序遍历（左‑根‑右），得到的节点值自然是从小到大的有序列表。可以把它想成把一本字典的所有词（按字母顺序）一个个抄到纸上。  
- **插入**：在有序列表中找到合适的位置插入 `val`，这一步相当于在字典的页码里插入一个新词。  
- **重建**：把有序列表重新构造成一棵平衡的 BST（常见做法是取中间元素作为根，左半边递归建左子树，右半边递归建右子树）。这一步就像把排好序的词重新装进一本新字典，确保每页的顺序仍然正确。  

这种方法一定能得到一棵合法的 BST，因为我们始终遵循“左小右大”的顺序，只是把结构重新组织了一遍。  

#### 代码（Python）  
```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def insertIntoBST_bruteforce(root: TreeNode, val: int) -> TreeNode:
    """暴力解：先中序遍历得到有序列表，再插入并重建 BST"""

    # 1️⃣ 中序遍历，收集所有节点值（相当于把树“拆成一排”）
    inorder = []

    def dfs(node: TreeNode):
        if not node:
            return
        dfs(node.left)          # 先左子树
        inorder.append(node.val)  # 再根节点
        dfs(node.right)         # 最后右子树

    dfs(root)

    # 2️⃣ 把新值插入有序列表（保持从小到大）
    # 这里用二分搜索找到插入位置，时间 O(log n)；但整体仍是 O(n)
    lo, hi = 0, len(inorder)
    while lo < hi:
        mid = (lo + hi) // 2
        if inorder[mid] < val:
            lo = mid + 1
        else:
            hi = mid
    inorder.insert(lo, val)   # 在正确位置插入

    # 3️⃣ 根据有序列表重建 BST（取中间元素为根，递归左/右子树）
    def build(lo: int, hi: int) -> TreeNode:
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(inorder[mid])
        node.left = build(lo, mid - 1)   # 左半段
        node.right = build(mid + 1, hi)  # 右半段
        return node

    return build(0, len(inorder) - 1)
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 中序遍历需要访问每个节点一次 → `O(n)`。  
  - 插入列表是 `O(n)`（最坏情况需要把后面的元素整体右移）。  
  - 重建树同样要遍历一次列表 → `O(n)`。  
  合起来仍是线性时间。这里的 “O(n)” 可以理解为“如果树有 10 000 个节点，程序大概要跑 10 000 步”。  

- **空间复杂度**：`O(n)`  
  - 需要额外的列表保存所有节点值，长度等于节点数。  
  - 递归栈深度也会是 `O(log n)`（因为我们把序列重新平衡），但列表的空间占主导。  

---

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **“把整棵树都拆开再重装”**，这一步多余了。  
实际上，插入一个新节点只需要 **沿着 BST 的搜索路径走到底**，找到第一个为空的左/右子节点位置即可。  

- **搜索路径**：从根节点开始，比较 `val` 与当前节点的值：  
  - 若 `val < node.val`，说明新节点应该在左子树；如果左子树为空，就把新节点挂在那里；否则继续往左走。  
  - 若 `val > node.val`，同理向右子树搜索。  

这一步只访问了 **树的高度** 所对应的节点，最坏情况下高度是 `h`。  
- 对于**平衡 BST**（如 AVL、红黑树），`h ≈ log₂n`，非常快。  
- 对于**极端不平衡**（全链表）情况，`h = n`，仍然是最好的可能，因为必须检查每个节点才能确认插入位置。  

实现方式可以是 **递归**（思路更直观）或 **迭代**（更省栈空间）。这里给出递归版，配合迭代版的解释，帮助初学者更好理解。  

#### 代码（Python）  

```python
def insertIntoBST(root: TreeNode, val: int) -> TreeNode:
    """
    最优解：沿着 BST 的搜索路径找到空位，直接插入。
    递归实现，思路像在树里走迷宫：每一步决定往左还是往右。
    """
    # 1️⃣ 空树直接创建根节点
    if not root:
        return TreeNode(val)

    # 2️⃣ 根据大小关系决定往左还是往右继续搜索
    if val < root.val:                     # 应该在左子树
        if root.left:                      # 左子树已经有节点，递归下去
            root.left = insertIntoBST(root.left, val)
        else:                               # 左子树为空，直接把新节点挂上
            root.left = TreeNode(val)
    else:                                   # val > root.val，应该在右子树
        if root.right:
            root.right = insertIntoBST(root.right, val)
        else:
            root.right = TreeNode(val)

    # 3️⃣ 返回当前根节点，保持整棵树的结构不变
    return root
```

> **如果你不喜欢递归**，可以把上面的思路改写成循环：  
> ```python
> def insertIter(root, val):
>     if not root: return TreeNode(val)
>     cur = root
>     while True:
>         if val < cur.val:
>             if cur.left: cur = cur.left
>             else: cur.left = TreeNode(val); break
>         else:
>             if cur.right: cur = cur.right
>             else: cur.right = TreeNode(val); break
>     return root
> ```  
> 循环版的核心仍是“沿路径走到底”，只是把递归改成了显式的 `while` 循环，省掉了函数调用的栈空间。  

#### 复杂度  
- **时间复杂度**：`O(h)`  
  - 只遍历从根到插入位置的路径，路径长度等于树的高度 `h`。  
  - 若树近似平衡，`h ≈ log₂n`，可以想象为“只需要检查大约 14 次就能在 10 000 个节点里找到位置”。  

- **空间复杂度**：  
  - **递归版**：`O(h)`（递归调用栈的深度）。  
  - **迭代版**：`O(1)`（只用常数级的指针）。  
  与暴力解的 `O(n)` 相比，省掉了大量不必要的额外存储。  

---  

## 心得  

- **核心技巧**：利用二叉搜索树的“左小右大”特性，只在**一条路径**上进行比较即可完成插入。  
- **适用的题型**：  
  1. 在 BST 中搜索/查找（`Search in a BST`）。  
  2. 删除 BST 中的节点（`Delete Node in a BST`）。  
  3. 判断两棵树是否相同（`Same Tree`）——同样可以用递归/迭代遍历整棵树。  
- **一句话总结**：**“在 BST 中插入，就是沿着大小比较的指路牌一路走到空位”。**  

## 反思  

- **第一反应**：先想把树“扁平化”，因为把所有东西都拿出来再重组在我脑子里比较直观。  
- **最容易踩的坑**：  
  - 忘记处理根节点为空的情况（空树需要直接创建根节点）。  
  - 递归返回值忘记回传，导致父节点的左右指针没有被正确更新。  
  - 对于迭代实现，`break` 写错或忘写会导致死循环。  
- **下次遇到同类题**：第一步先**判断是否可以直接在原结构上完成**（比如只需沿路径操作），再考虑是否真的需要额外的存储或重建。