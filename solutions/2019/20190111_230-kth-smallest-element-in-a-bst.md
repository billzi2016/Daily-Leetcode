# #230. BST 中的第 K 小元素 / Kth Smallest Element in a BST

> 难度：中等 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/kth-smallest-element-in-a-bst/)

---

## 题目（英文原版）

**Description**

Given the root of a binary search tree, and an integer k, return the kth smallest value (1-indexed) of all the values of the nodes in the tree.
Follow up: If the BST is modified often (i.e., we can do insert and delete operations) and you need to find the kth smallest frequently, how would you optimize?

**Examples**

**Example 1:**

```
Input: root = [3,1,4,null,2], k = 1
Output: 1
```

**Example 2:**

```
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
```

**Constraints**

- The number of nodes in the tree is n.
- 1 <= k <= n <= 104
- 0 <= Node.val <= 104

---

## 题目（中文翻译）

给定一棵二叉搜索树（binary search tree）的根节点 `root`，以及一个整数 `k`，返回树中所有节点值的第 `k` 小的值（使用 **1-indexed** 编号）。

## 示例

**示例 1**

```
Input: root = [3,1,4,null,2], k = 1
Output: 1
```

**示例 2**

```
Input: root = [5,3,6,2,4,null,null,1], k = 3
Output: 3
```

## 约束条件

- 树中节点的数量为 `n`。
- `1 <= k <= n <= 10^4`
- `0 <= Node.val <= 10^4`

## 进阶

如果二叉搜索树经常被修改（即需要执行插入和删除操作），且需要频繁查询第 `k` 小的元素，应该如何优化？

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

二叉搜索树（BST）有这么一个特性：**左子树的所有节点值都比根节点小，右子树的所有节点值都比根节点大**。  
如果我们把树的节点按「从小到大」的顺序排好，一个最自然的办法就是 **中序遍历**（左 → 根 → 右），遍历的顺序恰好就是递增的。

暴力解的步骤：

1. 对整棵树做一次完整的中序遍历，**把每个节点的值依次放进一个列表**。  
   - 把列表想象成一本**电话簿**，从第一页（最小值）到最后一页（最大值）依次排好。  
2. 列表已经是从小到大的顺序了，直接返回第 `k‑1`（因为 Python 的列表是 0‑index）的元素。

> **为什么正确？**  
> 中序遍历在 BST 中恰好按照数值从小到大访问每个节点，遍历完所有节点后得到的序列就是所有节点值的升序排列。取第 `k` 小就是在这个有序序列里取第 `k` 个元素，自然正确。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def kthSmallest(root: TreeNode, k: int) -> int:
    """
    暴力解：完整中序遍历，得到所有节点的升序列表，然后直接索引第 k 小
    """
    inorder_vals = []                # 用来保存遍历得到的值，相当于“电话簿”

    def inorder(node: TreeNode):
        if not node:                  # 空节点直接返回
            return
        inorder(node.left)            # 先遍历左子树（更小的值）
        inorder_vals.append(node.val) # 访问根节点，记录下来
        inorder(node.right)           # 再遍历右子树（更大的值）

    inorder(root)                    # 从根节点开始中序遍历
    return inorder_vals[k - 1]       # 列表是 0 索引，第 k 小是第 k-1 位
```

#### 复杂度  

- **时间复杂度：** `O(n)`  
  - 我们必须把树里所有 `n` 个节点都访问一次，才能把所有值收集起来。  
  - 用大白话说，就是「遍历一次树需要的时间与树的大小成正比」。
- **空间复杂度：** `O(n)`  
  - 需要一个额外的列表保存 `n` 个节点值，最坏情况下列表会装满所有节点。  
  - 再加上递归栈的深度 `O(h)`（`h` 为树高），但 `O(n)` 已经是最大的。

---

### 2. 最优解

#### 思路  

暴力解的「慢点」在于我们 **把所有节点都遍历了一遍**，即使只需要第 `k` 小。  
如果只想要第 `k` 小，其实只需要遍历 **前 `k` 个最小的节点**，其余的可以不管。

**核心技巧：** 仍然利用 BST 的中序遍历顺序，但在遍历过程中 **实时计数**，当计数达到 `k` 时立刻返回，不必继续遍历剩余节点。

实现方式有两种：

1. **递归计数**（在递归函数里返回是否已经找到了答案）。  
2. **迭代 + 栈**：手动模拟递归过程，使用显式栈保存「左子树的路径」，每弹出一个节点就计数一次，计数到 `k` 时返回。

这里用 **迭代 + 栈**，因为它更容易控制「只遍历到第 k 小」并且不依赖系统递归深度。

> **为什么只遍历到第 k 小就能结束？**  
> 中序遍历的顺序是「最小 → 次小 → … → 最大」。当我们已经访问了 `k` 个节点，说明已经找到了第 `k` 小的那个值，后面的更大的节点对答案没有影响，直接停止即可。

#### 代码（Python）

```python
def kthSmallest(root: TreeNode, k: int) -> int:
    """
    最优解：迭代中序遍历 + 栈，最多只遍历到第 k 小的节点
    """
    stack = []               # 栈用来保存“待回溯的左子树路径”，相当于“记事本”
    node = root
    count = 0                # 已经访问（弹出）了多少个节点

    while stack or node:     # 当还有未处理的节点或栈不为空时继续
        # 一直往左走，把左子树全部压进栈
        while node:
            stack.append(node)   # 记住这条路，等左子树走完再回来
            node = node.left

        # 左子树已经到底，弹出最近的节点（这就是当前最小的未访问节点）
        node = stack.pop()
        count += 1                # 访问了一个节点
        if count == k:            # 正好是第 k 小
            return node.val       # 直接返回答案

        # 访问完当前节点后，转向右子树继续同样的过程
        node = node.right

    # 题目保证 1 <= k <= n，所以一定能在循环里返回，不会走到这里
    raise ValueError("k 超出范围")
```

#### 复杂度  

- **时间复杂度：** `O(k)`  
  - 只会弹出 `k` 次栈（即访问 `k` 个节点），其余的左子树路径最多保存 `h`（树高）个节点在栈里。  
  - 用大白话说，就是「我们只需要跑 k 步路就能找到答案」。
- **空间复杂度：** `O(h)`  
  - 栈里最多同时保存从根到当前左子树最底层的路径，长度不超过树的高度 `h`。  
  - 对于平衡 BST，`h ≈ log n`，远小于 `n`，所以空间使用更友好。

> **如果树经常被插入/删除，且要频繁查询第 k 小怎么办？**  
> 可以在每个节点上**额外维护一个子树大小计数**（`size` = 左子树节点数 + 右子树节点数 + 1），这样在查询时只需要比较 `k` 与左子树大小，就可以 **在 O(h) 时间** 直接定位到第 `k` 小，而不需要遍历。插入或删除节点时，沿路径更新 `size` 即可，整体仍保持 `O(h)`。

---

## 心得

- **核心技巧**：利用 BST 的中序遍历顺序（从小到大）配合计数/栈，做到「只遍历必要的前 k 个节点」。
- **该技巧适用的题型**  
  1. 「在 BST 中查找第 k 大/第 k 小」等顺序统计类问题。  
  2. 「在有序数组/链表中查找第 k 小」的滑动窗口或双指针变形。  
  3. 「区间第 k 小」等需要 **快速定位第 k 位** 的数据结构（如线段树、树状数组配合离线查询）。
- **一句话总结解题钥匙**：**利用 BST 的中序遍历天然的升序属性，只在遍历到第 k 个节点时止步**。

---

## 反思

- **第一反应**：看到「BST」和「第 k 小」立刻想到中序遍历，因为它本身就是升序遍历。
- **最容易踩的坑**  
  - 忘记 `k` 是 **1‑indexed**，直接返回 `list[k]` 会少算一个。  
  - 对空树或 `k` 超出范围没有做检查（虽然题目保证合法，但写代码时最好防御式编程）。  
  - 在递归实现时忘记在左子树遍历完后再计数，导致顺序错误。  
- **下次遇到同类题**：第一步先**思考是否有天然的顺序（如 BST 的中序、数组的已排序）可以直接利用，然后决定是**完整遍历**还是**提前剪枝**（只遍历到第 k）。如果还有「频繁插删」的需求，立刻考虑在节点上**维护额外信息**（子树大小）来实现 `O(log n)` 的查询与更新。