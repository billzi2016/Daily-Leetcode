# #783. 二叉搜索树节点之间的最小距离 / Minimum Distance Between BST Nodes

> 难度：简单 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/minimum-distance-between-bst-nodes/)

---

## 题目（英文原版）

**Description**

Given the root of a Binary Search Tree (BST), return the minimum difference between the values of any two different nodes in the tree.
Note: This question is the same as 530: https://leetcode.com/problems/minimum-absolute-difference-in-bst/

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

- The number of nodes in the tree is in the range [2, 100].
- 0 <= Node.val <= 105

---

## 题目（中文翻译）

给定一棵二叉搜索树 (Binary Search Tree, BST) 的根节点 `root`，返回树中任意两个 **不同** 节点（node）的值之间的最小差值。

**示例 1**  
**示例 2**  

**说明**  
此题与 LeetCode 第 530 题 “Minimum Absolute Difference in BST” 完全相同：  
https://leetcode.com/problems/minimum-absolute-difference-in-bst/

**示例：**

**示例 1**  
输入: `root = [4,2,6,1,3]`  
输出: `1`

**示例 2**  
输入: `root = [1,0,48,null,null,12,49]`  
输出: `1`

**约束条件：**

- 树中节点的数量在 `[2, 100]` 范围内。  
- `0 <= Node.val <= 10^5`   (节点值的取值范围)

---

## 解题过程  

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是：把树里所有节点的值都取出来，放进一个列表里。  
> **类比**：把树想象成一本电话簿，先把每个人的电话号码（节点值）全部抄下来。

有了所有的值后，两两比较它们的差值，找出最小的那一个即可。  
- 为什么能得到正确答案？因为题目要求的是**任意两棵不同节点**之间的最小差值，遍历所有组合自然不会漏掉任何可能的配对。  
- 需要注意的是，节点值可能相同（虽然在 BST 中通常不允许重复，但题目没有强制），如果相同则差值为 0，就是最小的。

#### 代码（Python）  

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def minDiffInBST_bruteforce(root: TreeNode) -> int:
    """暴力解：把所有节点值收集到列表中，两两比较"""
    values = []                     # 用来存所有节点的值

    # 先做一次普通的深度优先遍历，把值装进列表
    def dfs(node: TreeNode):
        if not node:
            return
        values.append(node.val)     # 访问到一个节点，就把它的值加入列表
        dfs(node.left)              # 递归左子树
        dfs(node.right)             # 递归右子树

    dfs(root)

    # 暴力两两比较，找最小差值
    min_diff = float('inf')         # 初始设为正无穷大
    n = len(values)
    for i in range(n):
        for j in range(i + 1, n):   # 只比较 i<j 的组合，避免重复和自己和自己的比较
            diff = abs(values[i] - values[j])
            if diff < min_diff:
                min_diff = diff
    return min_diff
```

#### 复杂度  
- **时间复杂度**：`O(n²)`  
  - 解释：`n` 是节点数。我们先遍历一次树得到 `n` 个值，这一步是 `O(n)`。随后两层循环遍历所有 `C(n,2) = n·(n‑1)/2` 对组合，数量级是 `n²`，所以整体是二次方的时间。  
- **空间复杂度**：`O(n)`  
  - 解释：我们需要一个列表存放所有节点的值，列表长度正好等于树的节点数 `n`，除此之外递归栈的深度最多 `O(h)`（`h` 为树高），在最坏情况下 `h ≤ n`，所以总体仍是线性空间。

---  

### 2. 最优解  

#### 思路  
暴力解的瓶颈在 **两两比较** 那一步，需要 `O(n²)` 的时间。  
观察 BST 的一个重要性质：**中序遍历（左 → 根 → 右）会得到一个递增序列**。  
因此，如果把所有节点值按照中序遍历的顺序放进列表，列表本身已经是从小到大的排序。  
在一个已排序的数组里，最小的差值一定出现在 **相邻两个数** 之间（因为如果有更远的两个数，它们之间的差必然大于或等于相邻的某一步差）。  

基于此，我们只需要：

1. 用 **中序遍历**（递归或显式栈）一次性得到一个递增的值序列。  
2. 在遍历的过程中，**实时比较当前节点值和前一个节点值的差**，并维护最小差。这样可以省去额外的列表，只用 `O(1)` 的额外空间。

> **类比**：把 BST 看成一本已经排好序的通讯录，直接翻到相邻的两页看差距，而不是把所有页码全部摘下来再两两比。

#### 代码（Python）  

```python
def minDiffInBST(root: TreeNode) -> int:
    """最优解：中序遍历 BST，实时比较相邻节点的差值"""
    prev_val = None                 # 记录上一个访问的节点值
    min_diff = float('inf')         # 当前找到的最小差值

    def inorder(node: TreeNode):
        nonlocal prev_val, min_diff
        if not node:
            return
        inorder(node.left)          # 先遍历左子树（更小的值）

        # 访问根节点时，和前一个值比较差值
        if prev_val is not None:    # 第一个节点没有前驱，直接跳过
            diff = node.val - prev_val   # 因为中序是递增的，直接用减法即可
            if diff < min_diff:
                min_diff = diff
        prev_val = node.val         # 更新前驱为当前节点

        inorder(node.right)         # 再遍历右子树（更大的值）

    inorder(root)
    return min_diff
```

#### 复杂度  
- **时间复杂度**：`O(n)`  
  - 解释：我们只对每个节点做一次访问（一次中序遍历），所以时间随节点数线性增长。相比暴力的 `n²`，快了很多。  
- **空间复杂度**：`O(h)`（递归栈深度）  
  - 解释：除去递归调用的栈空间外，只用了常数个变量 (`prev_val`, `min_diff`)。在最坏情况下（树退化成链表）`h = n`，所以最差是 `O(n)`；在平衡树里 `h ≈ log n`，空间更小。  

---

## 心得  

- **核心技巧**：利用 BST 的中序遍历得到有序序列，进而只比较相邻元素的差值。  
- **适用的题型**：  
  1. “BST 中两节点的最小绝对差”（本题）  
  2. “BST 中两节点的最大差值”——同样可以用中序遍历，只记录最小值和最大值的差。  
  3. “有序数组中最小差值”——直接遍历相邻元素即可。  
- **一句话总结**：**BST 的中序遍历 = 排好序的列表，最小差必在相邻两个数之间。**

---

## 反思  

- **第一反应**：把所有节点值收集到列表里，两两比较——这就是暴力思路。  
- **最容易踩的坑**：  
  - 忘记 BST 的中序遍历是递增的，导致在比较差值时用了 `abs`（虽然不影响正确性，但多余）。  
  - 递归实现时忘记把 `prev_val` 声明为 `nonlocal`，导致每层递归都有自己的副本，结果错误。  
  - 边界情况：只有两个节点时直接返回它们的差值，代码仍能正常工作，因为遍历会比较一次。  
- **下次遇到同类题**：第一步先思考“这棵树/数组有没有天然的顺序？”如果有，尝试 **一次遍历 + 相邻比较**，而不是直接做所有组合的暴力枚举。