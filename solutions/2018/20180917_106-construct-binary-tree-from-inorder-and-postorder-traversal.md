# #106. 根据中序遍历和后序遍历构造二叉树 / Construct Binary Tree from Inorder and Postorder Traversal

> 难度：中等 · 标签：Array、Hash Table、Divide and Conquer、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/)

---

## 题目（英文原版）

**Description**

Given two integer arrays inorder and postorder where inorder is the inorder traversal of a binary tree and postorder is the postorder traversal of the same tree, construct and return the binary tree.

**Examples**

**Example 1:**

```
Input: inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
Output: [3,9,20,null,null,15,7]
```

**Example 2:**

```
Input: inorder = [-1], postorder = [-1]
Output: [-1]
```

**Constraints**

- 1 <= inorder.length <= 3000
- postorder.length == inorder.length
- -3000 <= inorder[i], postorder[i] <= 3000
- inorder and postorder consist of unique values.
- Each value of postorder also appears in inorder.
- inorder is guaranteed to be the inorder traversal of the tree.
- postorder is guaranteed to be the postorder traversal of the tree.

---

## 题目（中文翻译）

给定两个整数数组 `inorder` 和 `postorder`，其中 `inorder` 是一棵 **二叉树（binary tree）** 的中序遍历（inorder traversal），`postorder` 是同一棵树的后序遍历（postorder traversal），请构造并返回这棵二叉树。

### 示例

#### 示例 1
**输入：**  
`inorder = [9,3,15,20,7]`, `postorder = [9,15,7,20,3]`  

**输出：**  
`[3,9,20,null,null,15,7]`

#### 示例 2
**输入：**  
`inorder = [-1]`, `postorder = [-1]`  

**输出：**  
`[-1]`

### 约束条件
- `1 <= inorder.length <= 3000`
- `postorder.length == inorder.length`
- `-3000 <= inorder[i], postorder[i] <= 3000`
- `inorder` 和 `postorder` 中的值互不相同。
- `postorder` 中的每个值均出现在 `inorder` 中。
- 可以保证 `inorder` 确实是该树的中序遍历。
- 可以保证 `postorder` 确实是该树的后序遍历。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  
1. **观察遍历序列的特征**  
   - **后序遍历（postorder）**的最后一个元素一定是整棵树的根节点。  
   - **中序遍历（inorder）**把根节点分成左右两部分：左边是左子树的节点，右边是右子树的节点。  

2. **递归构造**  
   - 先取后序序列的最后一个值 `root_val` 作为根。  
   - 在中序序列里**顺序遍历**（类似在字典里找词条），找到 `root_val` 的位置 `mid`。  
   - `mid` 左侧的所有元素 belong to 左子树，右侧的所有元素 belong to 右子树。  
   - 根据左、右子树的元素个数，**切分**后序序列得到左、右子树对应的后序子数组。  
   - 对左、右子树递归执行同样的步骤，直至子数组为空。  

> **类比**：把 `inorder` 想象成一本**词典**，每个单词（节点值）都有对应的页码（下标）。我们要在词典里找到根词的页码，从而把词典左边的页码划给左子树，右边的页码划给右子树。  

**为什么正确**：  
- 后序的最后一个一定是根，这点是遍历定义决定的。  
- 中序把根左侧全是左子树、右侧全是右子树，这也是二叉树中序遍历的性质。  
- 递归地对左、右子树重复同样的划分，最终会把所有节点都放到正确的位置。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def buildTree(inorder, postorder):
    """
    暴力版：每次都在 inorder 中线性查找根节点的位置
    """
    if not inorder or not postorder:          # 空数组直接返回 None
        return None

    # 1. 后序的最后一个元素是根节点
    root_val = postorder[-1]
    root = TreeNode(root_val)

    # 2. 在 inorder 中找到根的位置（线性扫描）
    mid = 0
    while inorder[mid] != root_val:           # 类似在字典里找词
        mid += 1

    # 3. 根据 mid 划分左、右子树的 inorder
    left_in = inorder[:mid]                    # 左子树的中序
    right_in = inorder[mid + 1:]               # 右子树的中序

    # 4. 对应的 postorder 也要划分
    # 左子树的节点数就是 len(left_in)
    left_post = postorder[:len(left_in)]
    right_post = postorder[len(left_in):-1]    # 去掉根节点

    # 5. 递归构造左右子树
    root.left = buildTree(left_in, left_post)
    root.right = buildTree(right_in, right_post)

    return root
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每层递归都要在 `inorder` 中**线性扫描**一次找根的位置，最坏情况下树会退化成链表，递归层数是 `n`，于是总的比较次数约为 `n + (n‑1) + … + 1 = n·(n+1)/2 ≈ O(n²)`。  
  - 用大白话说，就是 **“每次都要翻一遍字典找词，字典越来越小，但总共要翻的页数仍然是平方级”**。  

- **空间复杂度**：`O(n)`  
  - 递归栈深度最坏为 `n`（链表形状），另外要存放返回的树节点本身也需要 `n` 的空间。  

---  

### 2. 最优解  

#### 思路  
从暴力解可以看出，**瓶颈在于每次都要线性查找根节点在 `inorder` 中的位置**。如果我们能够**一次性把所有节点的下标记录下来**，后面就可以 **O(1)** 直接拿到根的位置，整个构造过程只需要遍历一次数组。

**关键技巧：哈希表（字典）**  
- 把 `inorder` 中的每个值映射到它的下标，形成 `idx_map = {value: index}`。  
- 这相当于把“词典”一次性装进**查询表**，以后查词（找根下标）只需要一次哈希查找，时间是常数级。  

**递归构造的顺序**  
- 与暴力解相同，根节点仍然是后序数组的最后一个。  
- 为了避免每层都切割数组产生额外的拷贝，我们使用 **指针（索引）** 来标记当前子树在 `inorder`、`postorder` 中的范围。  
- 递归的**调用顺序**要先构造右子树，再构造左子树。原因是后序遍历的顺序是 **左 → 右 → 根**，我们从后往前取根，随后取的元素是右子树的根，最后才是左子树的根。  

**整体流程**  
1. 建立 `idx_map`（一次遍历 `inorder`）。  
2. 维护一个全局指针 `post_idx`，初始指向 `postorder` 最后一个元素（根）。  
3. 定义递归函数 `helper(left, right)`，表示当前子树对应的 `inorder` 区间是 `[left, right]`（左闭右闭）。  
   - 若 `left > right`，说明子树为空，返回 `None`。  
   - 取 `root_val = postorder[post_idx]`，创建根节点并 **post_idx 向左移动**。  
   - 用 `idx_map[root_val]` 在 `O(1)` 时间得到根在 `inorder` 的下标 `mid`。  
   - 先递归构造 **右子树**（`helper(mid+1, right)`），再递归构造 **左子树**（`helper(left, mid-1)`）。  
4. 最终返回根节点。  

> **类比**：把 `inorder` 当成一本已经排好序的**电话簿**，我们提前把每个人的名字（节点值）对应的页码（下标）记在小抄（哈希表）里。以后要找某个人的页码，只需要抬头看小抄，一眼就能得到，不用再翻整本电话簿。  

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def buildTree(inorder, postorder):
    """
    最优解：利用哈希表 O(1) 查找根在 inorder 中的位置，递归时使用索引避免切片
    """
    if not inorder or not postorder:
        return None

    # 1. 建立值 → 下标 的映射（一次遍历）
    idx_map = {value: i for i, value in enumerate(inorder)}   # 哈希表

    # 2. 后序遍历的指针，初始指向最后一个元素（根）
    post_idx = len(postorder) - 1

    # 3. 递归函数，构造 inorder[left : right] 区间对应的子树
    def helper(left, right):
        nonlocal post_idx                     # 让内部函数能够修改外部的指针

        # 区间为空，说明没有子树
        if left > right:
            return None

        # 取当前根节点的值
        root_val = postorder[post_idx]
        post_idx -= 1                         # 指针左移，准备下一个根

        # 根据哈希表快速定位根在 inorder 中的位置
        mid = idx_map[root_val]

        # 创建根节点
        root = TreeNode(root_val)

        # 注意：先建右子树，再建左子树（因为后序是左→右→根，倒着取根后，先取右子树根）
        root.right = helper(mid + 1, right)   # 构造右子树
        root.left = helper(left, mid - 1)     # 构造左子树

        return root

    # 从整个 inorder 区间开始构造
    return helper(0, len(inorder) - 1)
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 建立哈希表遍历一次 `inorder`：`O(n)`。  
  - 递归过程中每个节点只被创建一次，且每次只做 **常数次** 的哈希查找和指针移动。  
  - 整体相当于“只走一遍树”，所以是线性时间。  

- **空间复杂度**：`O(n)`  
  - 哈希表存放 `n` 条映射，使用 `O(n)` 空间。  
  - 递归栈深度最坏为 `O(n)`（树呈链状），加上返回的树节点本身也是 `O(n)`。  

---  

## 心得  

- **核心技巧**：利用哈希表把中序遍历的“位置查询”从线性降到常数，并结合后序遍历的根节点特性进行递归构造。  
- **适用的题型**：  
  1. “从两种遍历序列恢复二叉树”——如 `Construct Binary Tree from Preorder and Inorder`。  
  2. “根据层序遍历和中序遍历恢复树”——同样需要哈希表快速定位根。  
  3. “根据前序遍历和后序遍历恢复满二叉树”——思路类似，需要利用遍历的顺序特性。  
- **一句话总结**：**把“在中序中找根”这件事提前记下来，用哈希表一次搞定，再按后序倒着取根即可线性构树**。  

## 反思  

- **第一反应**：看到两种遍历，立刻想到根节点在后序的最后，左/右子树划分在中序。于是写出递归框架。  
- **最容易踩的坑**：  
  - **切分顺序错误**：在后序倒序取根时，需要先递归右子树再递归左子树，否则会把右子树的节点当成左子树。  
  - **忘记更新全局指针**：`post_idx` 必须是 `nonlocal`（或全局），否则每层递归会重新从末尾取根，导致错误。  
  - **数组切片带来的额外空间**：在暴力解中大量切片会导致额外的 `O(n²)` 空间，最优解通过索引避免。  
- **下次类似题的第一步**：先**确定根节点在那一种遍历序列中的位置**（通常是最后或第一个），再**利用哈希表把另一种遍历的下标快速映射**，最后按递归顺序（左/右）构造子树。