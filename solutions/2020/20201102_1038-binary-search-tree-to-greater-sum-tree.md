# #1038. 二叉搜索树转换为更大和树 / Binary Search Tree to Greater Sum Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a Binary Search Tree (BST), convert it to a Greater Tree such that every key of the original BST is changed to the original key plus the sum of all keys greater than the original key in BST.
As a reminder, a binary search tree is a tree that satisfies these constraints:
Note: This question is the same as 538: https://leetcode.com/problems/convert-bst-to-greater-tree/

**Examples**

**Example 1:**

```
Input: root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
Output: [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
```

**Example 2:**

```
Input: root = [0,null,1]
Output: [1,null,1]
```

**Constraints**

- The number of nodes in the tree is in the range [1, 100].
- 0 <= Node.val <= 100
- All the values in the tree are unique.

---

## 题目（中文翻译）

给定一棵二叉搜索树（Binary Search Tree, **BST**）的根节点 `root`，将其转换为更大和树（Greater Tree），使得原 BST 中每个节点的键（key）都被替换为 **原键 + BST 中所有大于该键的键之和**。

> 提示：二叉搜索树是一种满足以下约束的树：
> - 左子树中所有节点的键均小于根节点的键；
> - 右子树中所有节点的键均大于根节点的键；
> - 左、右子树也分别是二叉搜索树。

**示例 1：**

```
Input: root = [4,1,6,0,2,5,7,null,null,null,3,null,null,null,8]
Output: [30,36,21,36,35,26,15,null,null,null,33,null,null,null,8]
```

**示例 2：**

```
Input: root = [0,null,1]
Output: [1,null,1]
```

**约束条件：**

- 树中节点的数量在 `[1, 100]` 区间内。
- `0 <= Node.val <= 100`
- 树中所有的值互不相同。

> **注意**：本题与 538 题相同，详见 https://leetcode.com/problems/convert-bst-to-greater-tree/ 。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把树的所有节点值都取出来，放进一个**列表**（相当于把所有水果装进篮子），然后对列表进行**排序**（就像把水果按重量从小到大排好）。排好序后，我们可以从大到小遍历，累计前面的和，得到“比当前值大的所有节点之和”。最后再把每个节点的值改成 **原值 + 累计和**。

- **用到的数据结构**  
  - **列表（List）**：相当于一本字典的“词表”，把所有节点的值收集起来，方便一次性操作。  
  - **哈希表（dict）**：把原始值映射到“新值”。就像查字典时，词（原值）对应的页码（新值），查找时间是 O(1)。  

- **为什么正确**  
  1. 先把所有节点值取出来，保证每个节点都被考虑。  
  2. 排序后，后面的元素必然比前面的元素大（因为是二叉搜索树，左子树 < 根 < 右子树）。  
  3. 从大到小累计和，就正好得到“所有比当前节点大的节点值之和”。  
  4. 用哈希表把每个原始值映射到对应的新值，再把树里每个节点的值改掉即可。

- **时间/空间复杂度**  
  - 取值、排序、遍历三步：  
    - 取值遍历一次 O(n)  
    - 排序 O(n log n)（常见的排序算法，如快速排序的复杂度）  
    - 再遍历一次 O(n)  
    - 综合下来是 **O(n log n)**，这里的 `n` 是节点数量。  
  - 需要额外的列表和哈希表，都是和节点数成正比的空间，**O(n)**。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树


def bst_to_greater_tree_brute(root: TreeNode) -> TreeNode:
    """暴力解：先收集所有值，排序后再映射回树"""

    # 1. 中序遍历把所有节点值放进 list
    values = []

    def inorder(node: TreeNode):
        if not node:
            return
        inorder(node.left)
        values.append(node.val)          # 收集当前节点的值
        inorder(node.right)

    inorder(root)                       # O(n)

    # 2. 排序（虽然 BST 本身中序已经是有序的，这里演示“暴力思路”）
    values.sort()                       # O(n log n)

    # 3. 从大到小累计和，构造映射 old_val -> new_val
    suffix_sum = 0
    mapping = {}                         # 哈希表：原值 -> 新值
    for v in reversed(values):           # reversed 让我们从最大值开始
        suffix_sum += v                  # 累计比当前更大的所有值
        mapping[v] = v + suffix_sum - v  # 新值 = 原值 + (累计和 - 原值)

    # 4. 再遍历一次树，把每个节点的值替换成新值
    def replace(node: TreeNode):
        if not node:
            return
        node.val = mapping[node.val]    # O(1) 查表
        replace(node.left)
        replace(node.right)

    replace(root)                       # O(n)

    return root
```

#### 复杂度

- **时间复杂度**：`O(n log n)`  
  - 解释：`n` 是节点数。`log n` 表示“对数”，可以把它想成“把 n 分成两半、再分成两半…，最多分多少次能把它变成 1”。排序一般需要 `n log n` 次比较，所以整体是这个量级。

- **空间复杂度**：`O(n)`  
  - 解释：我们用了两个长度为 `n` 的容器（列表 `values`、哈希表 `mapping`），所以占用的额外空间和节点数成正比。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **排序** 步骤：我们把所有节点的值拿出来再排一次，其实这一步是完全不必要的。二叉搜索树本身就满足“左子树 < 根 < 右子树”，如果我们**倒序**遍历（**右子树 → 根 → 左子树**），就能一次性得到从大到小的节点顺序。

**关键观察**：  
- 在倒序遍历的过程中，**累计一个全局变量 `sum_sofar`**，它始终保存“已经访问过的（即比当前节点大的）所有节点值的和”。  
- 当我们访问到某个节点时，`sum_sofar` 正好是**“所有比它大的节点值之和”**。于是把 `node.val += sum_sofar`，再把 `sum_sofar` 更新为新的 `node.val`，即可完成转换。

这就是 **逆中序遍历 + 累加前缀和**（其实是后缀和）的技巧。只需要一次递归遍历，**时间 O(n)，空间 O(h)**（递归栈深度 `h`，在最坏情况下等于树高，平衡树时约 `log n`）。

- **核心算法/数据结构**  
  - **深度优先搜索（DFS）**：这里用递归实现的 **逆中序遍历**（右→根→左）。  
  - **全局累加变量**：相当于在遍历时随手记下的“已经收集的总价值”。  

- **类比**：想象你在一本按字母顺序排好的字典里查词，想把每个词的出现次数改成“它本身出现次数 + 所有在它后面的词的出现次数”。如果从 **后往前** 看字典，一边累计已经看到的次数，就能直接得到答案，而不需要先把所有词抄下来再排序。

#### 代码（Python）

```python
def bst_to_greater_tree(root: TreeNode) -> TreeNode:
    """最优解：逆中序遍历一次完成转换"""

    # 维护一个外部变量，记录“已经处理过的节点值之和”
    sum_sofar = 0

    def reverse_inorder(node: TreeNode):
        """右子树 → 根 → 左子树的递归遍历"""
        nonlocal sum_sofar               # 让内部函数可以修改外部的 sum_sofar
        if not node:
            return

        # 1. 先处理右子树（因为右子树的值更大）
        reverse_inorder(node.right)

        # 2. 访问根节点：把累计和加到当前节点值上
        sum_sofar += node.val            # 先把当前节点的原值加入累计和
        node.val = sum_sofar             # 再把累计和写回节点

        # 3. 最后处理左子树（更小的值）
        reverse_inorder(node.left)

    reverse_inorder(root)                # O(n) 完成全部转换
    return root
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  - 解释：我们只遍历每个节点一次，没有额外的排序或查表操作。`n` 次操作的耗时就是 `O(n)`。

- **空间复杂度**：`O(h)`  
  - 解释：递归调用会占用栈空间，深度等于树的高度 `h`。在最坏情况下（完全不平衡的链状树），`h = n`，但在一般的平衡 BST 中 `h ≈ log n`，所以空间通常远小于暴力解的 `O(n)`。

---

## 心得

- **核心技巧**：**逆中序遍历 + 累加前缀和**（或称后缀和）。利用 BST 的有序特性，直接在遍历过程中累计“大于当前节点的和”，一次遍历即可完成转换。  
- **适用的题型**  
  1. “把 BST 每个节点改成其右子树所有节点之和”——同样使用逆中序累计。  
  2. “把二叉树每个节点改成其子树所有节点之和”（**后序遍历 + 累加**）。  
  3. “在有序数组中把每个元素改成后缀和”——从右往左累计即可。  
- **一句话总结**：**利用有序结构的逆序遍历，边走边累计，就是把“更大值之和”一次搞定的钥匙。**

---

## 反思

- **第一反应**：把所有节点值收集到列表里，排序后再逐个更新（即暴力思路）。  
- **最容易踩的坑**  
  - 忘记在逆序遍历时**先累计再更新**节点值，导致累计的和少算了当前节点。  
  - 递归实现时没有使用 `nonlocal`（或全局变量），导致累计和无法在子调用之间共享。  
  - 边界情况：只有一个节点或全左/全右倾斜的树，需要确保递归基准（`if not node: return`）正确。  
- **下次遇到同类题**：第一步先思考**“是否可以利用已有的有序/层次结构一次遍历完成累计”**，若答案是“可以”，就尝试**逆序/后序遍历 + 累计变量**的方案。