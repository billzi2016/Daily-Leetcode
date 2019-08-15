# #530. 二叉搜索树中的最小绝对差 / Minimum Absolute Difference in BST

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/minimum-absolute-difference-in-bst/)

---

## 题目（英文原版）

**Description**

Given the root of a Binary Search Tree (BST), return the minimum absolute difference between the values of any two different nodes in the tree.
Note: This question is the same as 783: https://leetcode.com/problems/minimum-distance-between-bst-nodes/

**Examples**

**Example 1:**

```
Input: root = [4,2,6,1,3]
Output: 1
```

**Example 2:**

```
Input: root = [1,0,48,null,null,12,49]
Output: 1
```

**Constraints**

- The number of nodes in the tree is in the range [2, 104].
- 0 <= Node.val <= 105

---

## 题目（中文翻译）

给定一棵二叉搜索树（Binary Search Tree，BST）的根节点 `root`，返回树中任意两个不同节点值之间的最小绝对差。

**示例 1**  
**示例 2**  
**约束**  
> 注意：本题与 783 题相同：<https://leetcode.com/problems/minimum-distance-between-bst-nodes/>

**示例**

**示例 1:**  
输入: `root = [4,2,6,1,3]`  
输出: `1`

**示例 2:**  
输入: `root = [1,0,48,null,null,12,49]`  
输出: `1`

**约束条件**  
- 树中节点的数量在 `[2, 10^4]` 区间内。  
- `0 <= Node.val <= 10^5`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是**把所有节点的值都找出来，放进一个列表**，然后把列表里任意两两组合，算出它们的绝对差，取最小的那个。

- **数据结构**：我们用**列表**（list）来保存遍历得到的节点值。可以把它想象成装水果的篮子，所有水果（节点值）都先放进去，之后再挑选两两比较。
- **为什么正确**：题目要求“任意两个不同节点之间的最小绝对差”。只要把所有节点值都列出来，遍历所有可能的两两组合，就一定会找到答案。
- **时间/空间复杂度**：  
  - **时间**：把所有节点值放进列表需要遍历一次，记作 `O(n)`（n 为节点数）。随后两两比较需要 `n·(n‑1)/2` 次，大约是 `O(n²)`，也就是“平方级”，当节点很多时会变得很慢。  
  - **空间**：我们额外用了一个列表来存 `n` 个值，空间是 `O(n)`。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
from typing import Optional, List
from collections import deque

# 定义二叉树节点（LeetCode 会自带）
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def get_all_values(root: Optional[TreeNode]) -> List[int]:
    """层序遍历把所有节点值收集到列表中"""
    if not root:
        return []
    q = deque([root])
    vals = []
    while q:
        node = q.popleft()
        vals.append(node.val)          # 把当前节点的值放进篮子
        if node.left:
            q.append(node.left)        # 左子树入队
        if node.right:
            q.append(node.right)       # 右子树入队
    return vals


def get_minimum_difference(root: Optional[TreeNode]) -> int:
    """暴力求最小绝对差"""
    values = get_all_values(root)      # 第一步：收集所有值
    min_diff = float('inf')            # 初始设为正无穷大
    n = len(values)
    # 两层循环遍历所有不同的两节点
    for i in range(n):
        for j in range(i + 1, n):
            diff = abs(values[i] - values[j])   # 计算绝对差
            if diff < min_diff:                 # 维护最小值
                min_diff = diff
    return min_diff
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  这里的 `n²` 可以理解为“如果有 1000 个节点，需要比较大约 500,000 次”，随着节点数增长，耗时会呈平方增长，效率很低。
- **空间复杂度**：`O(n)`  
  需要额外存储所有节点的值，和树的规模成正比。

---

### 2. 最优解

#### 思路  
BST（二叉搜索树）有一个重要特性：**中序遍历（左‑根‑右）会得到一个升序序列**。也就是说，如果我们把节点值按中序顺序排好，它们已经从小到大排好序了。

在一个升序序列里，**最小的绝对差一定出现在相邻的两个数之间**。想象一下排好队的同学，离得最近的只能是站在旁边的那两个，而不可能是隔得很远的同学。

基于这个特性，我们可以：

1. **一次中序遍历**，不需要把所有值都保存下来，只要记住**上一个访问的节点值**（prev）和**当前的最小差**（min_diff）。
2. 在遍历到每个节点时，用 `abs(node.val - prev)` 计算与前一个节点的差，更新 `min_diff`。
3. 继续遍历，直到整棵树遍历完。

这样我们只遍历一次树，**不需要额外的列表**，时间是 `O(n)`，空间只用了递归栈（最坏 `O(h)`，h 为树高），在平衡树时大约是 `O(log n)`。

> **核心概念解释**  
> - **中序遍历**：先左子树 → 再根节点 → 最后右子树。对 BST 来说，这相当于“从最小到最大依次读取”。可以把它想象成打开一本字典，从第一页一直翻到最后一页，看到的词汇天然是字母顺序的。  
> - **递归栈**：函数调用自己时，系统会为每一次调用保存一些信息（比如局部变量），这些信息放在一块叫“栈”的空间里。栈的深度等于递归的层数，也就是树的高度 `h`。

#### 代码（Python）

```python
# -*- coding: utf-8 -*-
from typing import Optional

class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def get_minimum_difference(root: Optional[TreeNode]) -> int:
    """利用 BST 的中序遍历，在线计算最小绝对差"""
    # 用非局部变量保存上一个节点的值和当前最小差
    prev = None               # 前一个访问的节点值，初始为空
    min_diff = float('inf')   # 当前最小差，初始为正无穷

    def inorder(node: Optional[TreeNode]):
        """递归实现中序遍历"""
        nonlocal prev, min_diff   # 声明要修改外层变量
        if not node:
            return
        inorder(node.left)        # 先遍历左子树

        # ---- 访问根节点的核心逻辑 ----
        if prev is not None:      # 不是第一棵节点，才有前后差
            diff = node.val - prev   # 因为是升序，直接相减即可
            if diff < min_diff:      # 更新最小差
                min_diff = diff
        prev = node.val           # 更新 prev 为当前值

        inorder(node.right)       # 再遍历右子树

    inorder(root)                 # 从根节点开始遍历
    return min_diff
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  只遍历一次所有节点，`n` 次操作就能得到答案。相比暴力的 `n²`，这里的 “一次遍历” 可以理解为“如果有 10,000 个节点，只需要走 10,000 步”，非常快。
- **空间复杂度**：`O(h)`（递归栈），在最坏情况下（树退化成链表）是 `O(n)`，在平衡树时大约是 `O(log n)`。这比暴力解额外的列表 `O(n)` 更省内存。

---

## 心得

- **核心技巧**：利用 BST 的中序遍历得到有序序列，进而只比较相邻节点的差值。
- **适用的题型**：  
  1. “寻找 BST 中的第 K 小/大元素”  
  2. “检查 BST 是否满足某种有序约束（如所有相邻节点差不超过 X）”  
  3. “把 BST 转换为有序数组”  
- **一句话总结**：**在有序序列里，最小差一定在相邻两个数之间**。

---

## 反思

- **第一反应**：直接把所有节点值收集到列表，暴力两两比较——这是一种“先把东西全部搬出来再挑”的思路。
- **最容易踩的坑**：  
  - 忘记 BST 的中序遍历是升序的，导致不必要的排序或额外存储。  
  - 在递归实现时没有正确处理 `prev` 的初始化，导致第一次比较出现错误。  
  - 对极端不平衡的树（如链表形）忘记说明空间复杂度会退化到 `O(n)`。
- **下次遇到同类题**：第一步先**思考数据结构本身是否隐藏了顺序信息**（如 BST 的中序、堆的层序），再决定是否需要额外的容器或排序。这样往往可以把时间从 “平方级” 降到 “线性级”。