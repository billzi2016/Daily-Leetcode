# #99. 恢复二叉搜索树 / Recover Binary Search Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/recover-binary-search-tree/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary search tree (BST), where the values of exactly two nodes of the tree were swapped by mistake. Recover the tree without changing its structure.

**Examples**

**Example 1:**

```
Input: root = [1,3,null,null,2]
Output: [3,1,null,null,2]
Explanation: 3 cannot be a left child of 1 because 3 > 1. Swapping 1 and 3 makes the BST valid.
```

**Example 2:**

```
Input: root = [3,1,4,null,null,2]
Output: [2,1,4,null,null,3]
Explanation: 2 cannot be in the right subtree of 3 because 2 < 3. Swapping 2 and 3 makes the BST valid.
```

**Constraints**

- The number of nodes in the tree is in the range [2, 1000].
- -231 <= Node.val <= 231 - 1

---

## 题目（中文翻译）

给定一棵二叉搜索树（Binary Search Tree，BST）的根节点 `root`，其中恰好有两个节点的值被错误地交换了。请在不改变树的结构的前提下，恢复这棵二叉搜索树，使其重新满足 BST 的性质。

**示例 1**  
**输入**  
```text
root = [1,3,null,null,2]
```  
**输出**  
```text
[3,1,null,null,2]
```  
**解释**  
3 不能是 1 的左子节点，因为 3 > 1。交换 1 与 3 后，BST 恢复有效。

**示例 2**  
**输入**  
```text
root = [3,1,4,null,null,2]
```  
**输出**  
```text
[2,1,4,null,null,3]
```  
**解释**  
2 不能出现在 3 的右子树中，因为 2 < 3。交换 2 与 3 后，BST 恢复有效。

### 约束条件
- 树中节点的数量在 `[2, 1000]` 范围内。  
- `-2^31 <= Node.val <= 2^31 - 1`   (即 32 位有符号整数范围)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

我们先把二叉搜索树（BST）按照「中序遍历」的顺序全部访问一遍。  
- **中序遍历**：左子树 → 当前节点 → 右子树。  
  对于一棵合法的 BST，**中序遍历得到的节点值一定是从小到大排好的**，就像一本从 1 到 100 排序的字典。

因为题目说恰好有 **两个节点的值被互换**，所以如果我们把所有节点的值取出来放进一个列表里，再把这个列表 **排序**（就像把字典的页码重新排好顺序），最后把排好序的值再写回原来的节点，就能把树恢复成合法的 BST。

> **为什么这样一定能对？**  
> 中序遍历得到的顺序只跟「节点之间的相对大小」有关，而不是跟「节点在树中的具体位置」有关。把所有值重新排好顺序后，再按原来的遍历顺序依次写回去，树的结构不变，值的相对大小也恢复了自然递增——于是得到的就是一棵合法的 BST。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

class Solution:
    def recoverTree(self, root: TreeNode) -> None:
        """
        暴力解：把所有节点值取出来，排序后再写回去。
        由于题目要求 **原地** 修改，这里直接在原节点上改值即可。
        """
        # 1️⃣ 中序遍历，把所有节点对象保存到列表中
        inorder_nodes = []
        def inorder(node: TreeNode):
            if not node:
                return
            inorder(node.left)          # 先左
            inorder_nodes.append(node)  # 再根
            inorder(node.right)         # 最后右
        inorder(root)

        # 2️⃣ 把节点值取出来，排序
        vals = [node.val for node in inorder_nodes]  # 只取值
        vals.sort()                                   # 从小到大排好序

        # 3️⃣ 把排好序的值依次写回原来的节点
        for node, v in zip(inorder_nodes, vals):
            node.val = v   # 直接改值，不动结构
```

#### 复杂度  

- **时间复杂度**：`O(n log n)`  
  - 中序遍历本身是 `O(n)`（遍历一次所有节点）。  
  - 对 `n` 个值排序要 `O(n log n)`，这一步是瓶颈。  
  - 用大白话说，就是「先把所有数字拿出来排个序」需要的时间随节点数的对数增长。

- **空间复杂度**：`O(n)`  
  - 我们把所有节点对象存进了一个列表，需要额外的 `n` 个位置。  
  - 相当于「把树的所有节点都搬进了一个大盒子里」再处理。

---

### 2. 最优解

#### 思路  

暴力解的慢点在于 **排序**（`O(n log n)`）以及 **额外的 O(n) 列表**。  
其实我们并不需要把所有值都取出来再排，只要在一次遍历过程中直接找出 **被交换的两个节点**，随后把它们的值互换回来，就能在 `O(n)` 时间、`O(1)`（或 `O(h)`) 额外空间内完成恢复。

**关键观察**：  
- 对于合法的 BST，中序遍历的序列应该是严格递增的。  
- 现在恰好有两个节点被换位，导致序列出现 **“逆序”**（前一个值大于后一个值）。  
- 这种逆序最多出现两次：  
  1. **相邻交换**：只出现一次逆序，例如 `[1, 3, 2, 4]`（3 与 2 互换）。  
  2. **非相邻交换**：出现两次逆序，例如 `[1, 5, 3, 4, 2, 6]`（5 与 2 互换），逆序点在 `(5,3)` 与 `(4,2)`。

因此，只要在一次中序遍历中记录下**第一次出现逆序的前一个节点**（记作 `first`）和**最后一次出现逆序的后一个节点**（记作 `second`），最后把 `first.val` 与 `second.val` 交换即可。

实现方式有两种：

1. **递归 + 隐式栈**（空间 `O(h)`，`h` 为树高）——对初学者最友好。  
2. **Morris 中序遍历**（空间 `O(1)`，不使用递归或显式栈）——进阶技巧，这里简要说明但不强制要求。

下面先给出递归版的最优解，随后补充 Morris 版的实现思路。

#### 代码（Python）——递归版

```python
class Solution:
    def recoverTree(self, root: TreeNode) -> None:
        """
        最优解（递归版）：
        只遍历一次，找到两个被错误交换的节点，最后把它们的值换回来。
        额外空间只用到递归栈，最坏情况 O(h)。
        """
        # ---------- 辅助变量 ----------
        self.first = self.second = self.prev = None
        # prev 用来保存上一次遍历到的节点（在中序遍历中是前驱）

        # ---------- 中序遍历 ----------
        def inorder(node: TreeNode):
            if not node:
                return

            inorder(node.left)   # 先左

            # ---- 检查当前节点与前驱是否逆序 ----
            if self.prev and self.prev.val > node.val:
                # 第一次发现逆序，记录前驱为 first
                if not self.first:
                    self.first = self.prev
                # 每次发现逆序都更新 second（后面的逆序会覆盖前面的）
                self.second = node

            # 更新前驱为当前节点，继续向右
            self.prev = node

            inorder(node.right)   # 再右

        # 开始遍历
        inorder(root)

        # ---------- 交换两个错误节点的值 ----------
        if self.first and self.second:
            self.first.val, self.second.val = self.second.val, self.first.val
```

> **关键点解释**  
> - `prev` 相当于「字典里上一个查到的词」，我们每访问一个新节点，就把它和 `prev` 比较，看是否出现「前一个值大于后一个值」的逆序。  
> - `first` 记录第一次逆序时的「前一个」节点（应该是较大的那个），`second` 记录每次逆序时的「后一个」节点（应该是较小的那个）。如果只出现一次逆序，`first` 与 `second` 分别指向那两个相邻的错误节点；如果出现两次逆序，`first` 指向第一次逆序的前一个，`second` 指向第二次逆序的后一个——正好是被换位的那两节点。  
> - 最后只需要把这两个节点的值互换，即可恢复 BST。

#### 代码（Python）——Morris 中序遍历（进阶）

> **为什么要用 Morris？**  
> 递归/显式栈都需要额外的空间（最坏 O(n)），而 Morris 通过在树的空闲指针上做临时「线索」来实现 **O(1) 额外空间** 的中序遍历。下面给出核心思路，代码保持简洁。

```python
class Solution:
    def recoverTree(self, root: TreeNode) -> None:
        """
        Morris 中序遍历版，空间 O(1)。
        思路和递归版完全相同，只是遍历方式不同。
        """
        first = second = prev = None
        cur = root

        while cur:
            if cur.left is None:
                # 直接访问当前节点（相当于递归的中序访问点）
                if prev and prev.val > cur.val:
                    if not first:
                        first = prev
                    second = cur
                prev = cur
                cur = cur.right
            else:
                # 找到左子树的最右节点（前驱），为它建立临时线索
                pre = cur.left
                while pre.right and pre.right is not cur:
                    pre = pre.right

                if pre.right is None:          # 第一次来到 cur
                    pre.right = cur            # 线索指向 cur
                    cur = cur.left
                else:                           # 线索已经建立，第二次回到 cur
                    pre.right = None           # 恢复原状
                    if prev and prev.val > cur.val:
                        if not first:
                            first = prev
                        second = cur
                    prev = cur
                    cur = cur.right

        # 交换错误节点的值
        if first and second:
            first.val, second.val = second.val, first.val
```

> **注意**：Morris 版的核心仍是「找逆序的两个节点」这一点，只是遍历方式更省空间，代码稍微复杂一些，建议先掌握递归版再去理解。

#### 复杂度  

- **时间复杂度**：`O(n)`  
  - 只遍历一次所有节点，和树的大小呈线性关系。  
  - 用大白话说，就是「看完所有节点只需要一次，越多的节点只会让时间线性增长」。

- **空间复杂度**：  
  - 递归版：`O(h)`（`h` 为树的高度），最坏情况（树退化成链表）是 `O(n)`，但平均情况（平衡树）是 `O(log n)`。这只用到了递归栈，等价于「树的深度这么高，就需要这么多记忆」  
  - Morris 版：`O(1)`，不使用任何额外的栈或列表，只在原树上做临时指针，真正做到了「常数空间」。


---

## 心得

- **核心技巧**：利用 BST 的中序遍历「递增」特性，定位两个被错误交换的节点。  
- **适用的类似题型**：  
  1. “错误的二叉搜索树”系列（如 `Recover Binary Search Tree`）。  
  2. “找出二叉搜索树中第 K 小的元素”需要中序遍历的思路。  
  3. “验证二叉搜索树”同样依赖中序遍历判断递增。  
- **一句话总结解题钥匙**：**在一次中序遍历中捕捉逆序的前驱和后继，最后把它们的值换回来**。

---

## 反思

- **第一反应**：把树全部展开成列表，排序后再写回去——直观但不是最优。  
- **最容易踩的坑**：  
  - 没有考虑两个错误节点不相邻的情况，只交换第一次发现的两个节点会出错。  
  - 在递归实现中忘记维护 `prev`（前驱），导致比较不到逆序。  
  - 对空树或只有两个节点的极端情况没有做好边界检查。  
- **下次类似题目第一步该想到**：**先把问题转化为「序列」的属性**（这里是递增），再在一次遍历中找出不符合属性的地方。这样往往能直接定位错误，而不必额外排序或遍历多次。