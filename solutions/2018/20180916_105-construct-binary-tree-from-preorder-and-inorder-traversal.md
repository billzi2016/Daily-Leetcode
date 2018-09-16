# #105. 从前序和中序遍历构造二叉树 / Construct Binary Tree from Preorder and Inorder Traversal

> 难度：中等 · 标签：Array、Hash Table、Divide and Conquer、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/)

---

## 题目（英文原版）

**Description**

Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.

**Examples**

**Example 1:**

```
Input: preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
Output: [3,9,20,null,null,15,7]
```

**Example 2:**

```
Input: preorder = [-1], inorder = [-1]
Output: [-1]
```

**Constraints**

- 1 <= preorder.length <= 3000
- inorder.length == preorder.length
- -3000 <= preorder[i], inorder[i] <= 3000
- preorder and inorder consist of unique values.
- Each value of inorder also appears in preorder.
- preorder is guaranteed to be the preorder traversal of the tree.
- inorder is guaranteed to be the inorder traversal of the tree.

---

## 题目（中文翻译）

给定两个整数数组 `preorder` 和 `inorder`，其中 `preorder` 是一棵二叉树的前序遍历（preorder traversal），`inorder` 是同一棵树的中序遍历（inorder traversal），请构造并返回这棵二叉树。

**示例 1**  
**输入**: `preorder = [3,9,20,15,7]`, `inorder = [9,3,15,20,7]`  
**输出**: `[3,9,20,null,null,15,7]`  

**示例 2**  
**输入**: `preorder = [-1]`, `inorder = [-1]`  
**输出**: `[-1]`  

**约束条件**  

- `1 <= preorder.length <= 3000`  
- `inorder.length == preorder.length`  
- `-3000 <= preorder[i], inorder[i] <= 3000`  
- `preorder` 和 `inorder` 中的值互不相同。  
- `inorder` 中的每个值均出现在 `preorder` 中。  
- `preorder` 必定是该树的前序遍历。  
- `inorder` 必定是该树的中序遍历。

---

## 解题过程  

### 1. 直觉解（暴力）  

#### 思路  

- **核心想法**：先把先序遍历的第一个元素当作根节点（先序遍历的顺序是「根‑左‑右」），然后在中序遍历中找到这个根节点的位置。根左边的所有元素就是左子树的中序序列，根右边的元素就是右子树的中序序列。  
- **使用的数据结构**：  
  - **列表（Array）**：用来保存 `preorder` 与 `inorder`，就像我们平时记账本一样，顺序很重要。  
  - **递归**：把“大树”拆成“小树”一步步构造，递归的过程类似把一块大披萨切成小块再逐块吃。  
- **为什么正确**：  
  - 先序遍历保证我们每次看到的第一个数一定是当前子树的根。  
  - 中序遍历把根节点左侧的所有节点全部放在根的左边，右侧的全部放在根的右边，这正好对应二叉树的「左子树」和「右子树」的定义。只要我们把根左右两边的序列分别递归地再建树，整棵树就会被完整恢复。  
- **复杂度分析（大白话）**：  
  - 每一次递归我们都要在 `inorder` 中 **线性查找** 根节点的位置（相当于在一本字典里从头到尾找词），最坏情况下要遍历 `n` 个元素。  
  - 同时我们会 **切片**（`list[start:end]`）得到左子树和右子树的序列，这会额外复制出新的列表，复制的元素个数也和子树大小成正比。  
  - 因此整体时间大约是 `n + (n-1) + (n-2) + … ≈ n²`，空间除了递归栈外，还会因为切片产生 `O(n²)` 的临时列表。  

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x          # 节点保存的数值
        self.left = None      # 左子树指针
        self.right = None     # 右子树指针

def buildTree(preorder, inorder):
    """
    暴力递归实现
    :param preorder: 先序遍历列表
    :param inorder: 中序遍历列表
    :return: 二叉树根节点
    """
    if not preorder or not inorder:          # 空列表说明子树为空
        return None

    # 先序的第一个元素一定是根节点
    root_val = preorder[0]
    root = TreeNode(root_val)

    # 在中序序列中找根节点的位置（线性查找）
    root_index = inorder.index(root_val)     # O(n) 操作

    # 左子树的中序序列是根左边的所有元素
    left_inorder = inorder[:root_index]
    # 右子树的中序序列是根右边的所有元素
    right_inorder = inorder[root_index + 1:]

    # 由于先序是「根‑左‑右」，左子树的先序序列长度和左中序序列长度相同
    left_preorder = preorder[1: 1 + len(left_inorder)]
    right_preorder = preorder[1 + len(left_inorder):]

    # 递归构造左右子树
    root.left = buildTree(left_preorder, left_inorder)
    root.right = buildTree(right_preorder, right_inorder)

    return root
```

#### 复杂度  

- **时间复杂度**：`O(n²)`  
  - 每层递归都要在 `inorder` 中线性搜索根节点位置，且会产生切片复制，累计的工作量相当于 `1 + 2 + … + n ≈ n²`。  
- **空间复杂度**：`O(n²)`（最坏情况）  
  - 除了递归栈 `O(n)`，切片产生的临时列表总共也会占 `O(n²)` 的额外空间。  

---  

### 2. 最优解  

#### 思路  

1. **找瓶颈**：在暴力解里，最耗时的两件事是  
   - **在 `inorder` 中寻找根节点**（每次都要遍历），  
   - **对列表进行切片**（每次都复制子数组）。  
2. **如何把「找根」变快**？  
   - 由于所有节点值互不相同，我们可以在一开始把 `inorder` 中每个值对应的下标记录在 **哈希表**（字典）里。字典的查询是 `O(1)`，相当于在一本**词典**里直接翻到对应页码，省去了线性查找。  
3. **如何避免切片复制**？  
   - 递归时只传递 **下标区间**（左闭右开），不再生成新的列表。下标就像是给原始书本标记「从第几页开始到第几页结束」，不需要把纸页复制出来。  
4. **递归的核心**：  
   - 维护一个全局变量 `pre_idx`，指向当前要使用的先序根节点下标。每建好一个根，就把 `pre_idx` 往后移动一位。  
   - 递归函数 `helper(in_left, in_right)` 负责在 `inorder[in_left:in_right]` 区间内构造子树。  
   - 步骤如下：  
     1. 取 `preorder[pre_idx]` 作为根节点值，`pre_idx += 1`。  
     2. 用哈希表快速得到根节点在 `inorder` 中的下标 `idx`。  
     3. 先递归构造左子树（因为先序是根‑左‑右，左子树的根一定在后面），区间是 `[in_left, idx)`。  
     4. 再递归构造右子树，区间是 `[idx+1, in_right)`。  
   - 递归结束的条件是 `in_left == in_right`（区间为空），此时返回 `None`。  

> **为什么递归顺序要先左后右？**  
> 先序遍历的顺序是「根‑左‑右」，我们每次取根之后，接下来出现的元素必然是左子树的根（如果左子树存在），所以必须先完成左子树的构造，才能让 `pre_idx` 正确指向右子树的根。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def buildTree(preorder, inorder):
    """
    使用哈希表 + 下标区间的递归实现（时间 O(n)，空间 O(n)）
    """
    # 1️⃣ 建立值 -> 中序下标的映射（哈希表）
    idx_map = {val: i for i, val in enumerate(inorder)}  # O(n) 预处理

    # 2️⃣ 维护一个先序遍历的全局指针
    pre_idx = 0  # 这里使用 Python 的闭包特性，让内部函数可以修改它

    # 3️⃣ 递归函数，负责在 inorder[left:right] 区间内构造子树
    def helper(in_left, in_right):
        nonlocal pre_idx               # 声明要修改外层变量
        if in_left == in_right:        # 区间为空，说明子树不存在
            return None

        # 取当前先序遍历的根节点值
        root_val = preorder[pre_idx]
        pre_idx += 1                   # 指针向后移动，准备下一个根

        # 根据哈希表快速找到根在中序遍历中的位置
        idx = idx_map[root_val]

        # 创建根节点对象
        root = TreeNode(root_val)

        # 递归构造左子树：中序区间 [in_left, idx)
        root.left = helper(in_left, idx)

        # 递归构造右子树：中序区间 [idx+1, in_right)
        root.right = helper(idx + 1, in_right)

        return root

    # 整棵树对应的中序区间是 [0, len(inorder))
    return helper(0, len(inorder))
```

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 每个节点只被访问一次：一次取根值（`O(1)`），一次在哈希表中查找下标（`O(1)`），递归调用常数次。相当于一次遍历整棵树。  
- **空间复杂度**：`O(n)`  
  - 哈希表需要存储 `n` 个键值对。递归栈最深为树的高度，最坏情况下（链状树）高度为 `n`，因此额外空间为 `O(n)`。  

---  

## 心得  

- **核心技巧**：利用哈希表把「在中序中找根」的线性搜索降到常数时间；用**下标区间**代替切片，避免不必要的复制。  
- **适用场景**（类似题目）：  
  1. 从前序+中序或后序+中序恢复二叉树（本题的变形）。  
  2. 根据层序遍历和中序遍历重建树（同样需要哈希表快速定位）。  
  3. “树的序列化与反序列化”时，需要在遍历序列之间快速对应。  
- **一句话总结解题钥匙**：**“先序给根，哈希表定位根在中序的位置，递归用下标划分左右子树”。**  

## 反思  

- **第一反应**：看到“先序”和“中序”，立刻想到“根‑左‑右”和“左‑根‑右”的遍历特性，尝试用递归把两者配对。  
- **最容易踩的坑**：  
  - 忘记 **先序指针的全局移动**，导致左子树和右子树使用了相同的根节点。  
  - 在递归结束条件写错（比如 `in_left > in_right`），会出现无限递归或遗漏空子树。  
  - 对于只有一个节点的极端情况，需要确保哈希表和指针都能正常工作。  
- **下次思路**：  
  1. 先判断是否可以把“寻找根节点”用哈希表一次预处理。  
  2. 再考虑是否可以**只用下标**而不复制列表。  
  3. 最后再写递归框架，注意递归结束的区间条件。