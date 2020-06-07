# #889. 构造二叉树（Binary Tree）——根据前序（preorder）和后序（postorder）遍历 / Construct Binary Tree from Preorder and Postorder Traversal

> 难度：中等 · 标签：Array、Hash Table、Divide and Conquer、Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-postorder-traversal/)

---

## 题目（英文原版）

**Description**

Given two integer arrays, preorder and postorder where preorder is the preorder traversal of a binary tree of distinct values and postorder is the postorder traversal of the same tree, reconstruct and return the binary tree.
If there exist multiple answers, you can return any of them.

**Examples**

**Example 1:**

```
Input: preorder = [1,2,4,5,3,6,7], postorder = [4,5,2,6,7,3,1]
Output: [1,2,3,4,5,6,7]
```

**Example 2:**

```
Input: preorder = [1], postorder = [1]
Output: [1]
```

**Constraints**

- 1 <= preorder.length <= 30
- 1 <= preorder[i] <= preorder.length
- All the values of preorder are unique.
- postorder.length == preorder.length
- 1 <= postorder[i] <= postorder.length
- All the values of postorder are unique.
- It is guaranteed that preorder and postorder are the preorder traversal and postorder traversal of the same binary tree.

---

## 题目（中文翻译）

给定两个整数数组 `preorder` 和 `postorder`，其中 `preorder` 是一棵 **互不相同的值** 的二叉树的前序遍历，`postorder` 是同一棵树的后序遍历，请重建并返回该二叉树。  
如果存在多种可能的树形结构，返回任意一种即可。

---

### 示例

**示例 1**  
```text
Input: preorder = [1,2,4,5,3,6,7], postorder = [4,5,2,6,7,3,1]
Output: [1,2,3,4,5,6,7]
```

**示例 2**  
```text
Input: preorder = [1], postorder = [1]
Output: [1]
```

---

### 约束条件

- `1 <= preorder.length <= 30`
- `1 <= preorder[i] <= preorder.length`
- `preorder` 中的所有值互不相同。
- `postorder.length == preorder.length`
- `1 <= postorder[i] <= postorder.length`
- `postorder` 中的所有值互不相同。
- 已知 `preorder` 与 `postorder` 确实对应同一棵二叉树的前序遍历和后序遍历。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们先把题目翻译成生活中的场景：  
- **先序遍历（preorder）**：先把根节点记下来，然后从左子树一直记到右子树，就像我们先写“老板”，再写“左边的员工”，最后写“右边的员工”。  
- **后序遍历（postorder）**：先把左子树记下来，再记右子树，最后记根节点，类似“先完成左边的工作，后完成右边的工作，最后报老板”。  

已知这两份“工作日志”，我们要把树重新搭建出来。  

最直接的想法是：**枚举左子树的大小**，把先序序列分成「根」+「左子树」+「右子树」三段；再在后序序列里找出对应的左子树范围，递归地把左、右子树也用同样的方法恢复。  

这一步里唯一需要的工具是**查找**——在后序序列里找左子树根节点的位置。因为题目保证所有值互不相同，这个查找一定唯一。

> **类比**：把后序序列想象成一本字典，想找某个词（左子树根），就得从头往后翻，最坏要翻完整本（O(n)）。

只要我们把所有可能的左子树大小都尝试一次，就一定能找到一种合法的划分（题目保证至少有一种解）。这就是所谓的**暴力枚举**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def constructFromPrePost(preorder, postorder):
    """
    暴力版：枚举左子树的大小，递归构造
    """
    if not preorder:                     # 空序列直接返回 None
        return None

    root = TreeNode(preorder[0])          # 先序的第一个一定是根
    if len(preorder) == 1:                # 只有一个节点，直接返回根
        return root

    # 暴力尝试：左子树的大小可以是 1,2,...,len(preorder)-2
    # （因为最后一个元素是根，左子树至少要有一个节点）
    for left_size in range(1, len(preorder)):
        # 先序：根 | 左子树 | 右子树
        left_pre  = preorder[1:1+left_size]
        right_pre = preorder[1+left_size:]

        # 在后序里找左子树根的下标
        left_root_val = left_pre[0]           # 左子树根的值一定是左子树先序的第一个
        try:
            left_root_idx = postorder.index(left_root_val)
        except ValueError:                    # 找不到说明划分不合法，直接跳过
            continue

        # 后序：左子树 | 右子树 | 根
        left_post  = postorder[:left_root_idx+1]
        right_post = postorder[left_root_idx+1:-1]

        # 检查划分是否对应（长度必须相等）
        if len(left_pre) != len(left_post) or len(right_pre) != len(right_post):
            continue

        # 递归构造左右子树
        root.left  = constructFromPrePost(left_pre, left_post)
        root.right = constructFromPrePost(right_pre, right_post)
        return root                           # 找到合法划分后直接返回

    return root  # 理论上不会走到这里，因为一定有合法划分
```

> 关键行解释  
> - `root = TreeNode(preorder[0])`：先序的第一个元素就是根。  
> - `for left_size in range(1, len(preorder))`：枚举左子树可能的节点数。  
> - `postorder.index(left_root_val)`：在后序里找左子树根的位置，这一步是 **线性查找**。  
> - `if len(left_pre) != len(left_post) ...`：确保左、右子树的先序、后序长度匹配，否则说明划分不对。

#### 复杂度

- **时间复杂度**：`O(n^2)`  
  - 外层循环枚举左子树大小，最多 `n` 次。  
  - 每次枚举里要在后序数组里 `index` 查找根节点，最坏也要遍历 `n` 次。  
  - 所以最坏情况是 `n × n = n²`，用大白话说，就是“随着节点数的增长，耗时会像正方形那样快地增长”。  

- **空间复杂度**：`O(n)`（递归栈）  
  - 递归的深度最坏会达到 `n`（极端的链状树），每层递归会占用常数空间。  
  - 除此之外我们只用了几个临时切片（Python 会产生新列表），总体仍是线性级别。  

---

### 2. 最优解

#### 思路  

**暴力解慢的地方**主要有两点：

1. **左子树大小枚举**：我们把所有可能的划分都尝试了一遍，实际上大多数情况下只需要一种划分。  
2. **在后序里线性查找根节点**：每次 `index` 都要遍历整个后序数组，导致二次循环。

我们可以把这两点都 **用哈希表**（字典）一次性解决掉：

- 先把 **后序数组**的每个值映射到它的下标，形成 `pos = {value: index}`。这样查找左子树根的下标就能在 **O(1)** 时间完成（相当于在字典里直接查页码）。
- 再利用 **递归的边界** 来直接确定左子树的大小，而不需要枚举。  
  - 记 `pre[preL]` 为当前子树的根（先序的第一个），  
  - `pre[preL+1]` 必然是左子树根（因为根后面紧跟左子树的根）。  
  - 在后序里找到这个左子树根的下标 `pos[pre[preL+1]]`，设为 `leftRootIdx`。  
  - 那么左子树在后序中的范围是 `[postL, leftRootIdx]`，长度为 `leftSize = leftRootIdx - postL + 1`。  
  - 于是我们可以直接划分先序和后序的子区间：  
    - **左子树**：先序 `[preL+1, preL+leftSize]`，后序 `[postL, leftRootIdx]`  
    - **右子树**：先序 `[preL+leftSize+1, preR]`，后序 `[leftRootIdx+1, postR-1]`  

这样每一次递归只做 **一次 O(1) 查找**，递归的层数仍是 `n`，总时间降到 **O(n)**。

> **类比**：  
> - 哈希表就像一本“快速查找表”，把每本书的章节号（值）直接对应到所在的页码（下标），省去翻页的时间。  
> - 递归划分子树就像把一块巧克力按“左子树根所在的位置”一次性切成两块，而不是尝试所有可能的切法。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def constructFromPrePost(preorder, postorder):
    """
    最优解：利用哈希表 O(1) 查找左子树根位置，递归划分子区间
    """
    # 建立后序值 -> 下标 的映射，后面查找直接 O(1)
    idx_in_post = {val: i for i, val in enumerate(postorder)}

    def helper(preL, preR, postL, postR):
        """
        在 preorder[preL:preR+1] 与 postorder[postL:postR+1] 区间内构造子树
        """
        if preL > preR:               # 区间为空，返回 None
            return None
        root = TreeNode(preorder[preL])   # 当前子树根
        if preL == preR:              # 只剩一个节点，直接返回根
            return root

        # 左子树根一定是 preorder[preL+1]
        left_root_val = preorder[preL + 1]
        left_root_idx = idx_in_post[left_root_val]   # O(1) 查找

        # 左子树在后序中的范围是 [postL, left_root_idx]
        left_size = left_root_idx - postL + 1        # 左子树节点数

        # 递归构造左、右子树
        root.left = helper(preL + 1,
                           preL + left_size,
                           postL,
                           left_root_idx)

        root.right = helper(preL + left_size + 1,
                            preR,
                            left_root_idx + 1,
                            postR - 1)   # postR 为根所在位置
        return root

    n = len(preorder)
    return helper(0, n - 1, 0, n - 1)
```

> 关键行解释  
> - `idx_in_post = {val: i for i, val in enumerate(postorder)}`：一次遍历把后序的每个值对应到下标，后面查找不需要遍历。  
> - `left_root_val = preorder[preL + 1]`：先序里根后面的第一个元素必是左子树根。  
> - `left_root_idx = idx_in_post[left_root_val]`：在哈希表里直接得到左子树根在后序中的位置。  
> - `left_size = left_root_idx - postL + 1`：左子树的节点数，帮助我们划分先序子区间。  
> - 递归的四个参数分别是当前子树在 **先序** 和 **后序** 中的左右边界，保证每次只处理对应的子数组。

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 每个节点只会被创建一次，递归过程对每个节点做 **常数次** 的工作（哈希表查找、指针算术）。  
  - 用大白话说，就是“节点数再多，耗时只会线性增长”，不像正方形那样快。  

- **空间复杂度**：`O(n)`  
  - 哈希表占用 `O(n)` 的额外空间来存储值到下标的映射。  
  - 再加上递归调用栈的深度，最坏情况（链状树）也是 `O(n)`。  

---

## 心得

- **核心技巧**：利用后序遍历的哈希表实现 **O(1) 定位**，并通过递归的区间划分一次性确定左子树大小。  
- **适用的题型**  
  1. 从两种遍历序列重建树（如前序+中序、后序+中序）。  
  2. “划分子数组”类的递归问题（如分割数组求最大子段和的分治实现）。  
  3. 需要快速定位元素位置的场景（如 “从中序和后序恢复二叉搜索树”。）  
- **一句话总结解题钥匙**：**先用哈希表把“在后序里找根”这一步变成 O(1)，再用递归的区间边界直接算出左子树大小**。

---

## 反思

- **第一反应**：看到两段遍历，先想到“把根找出来，然后把左右子树的范围切分”。于是自然想到枚举左子树大小的暴力办法。  
- **最容易踩的坑**  
  - **边界条件**：只有一个节点时要及时返回，否则会出现无限递归。  
  - **左子树根的定位**：如果写成 `preorder[preL]`（根本身）而不是 `preorder[preL+1]`，划分会全部错位。  
  - **哈希表同步**：在最优解里忘记建立 `value -> index` 的映射，会导致每次 `index` 仍是 O(n)。  
- **下次遇到同类题的第一步**：**先判断是否可以用哈希表把“在另一遍历里找某个值的位置”做成 O(1)**，再基于这个定位来**递归划分子区间**。这样往往能直接把时间复杂度从 `O(n²)` 降到 `O(n)`。