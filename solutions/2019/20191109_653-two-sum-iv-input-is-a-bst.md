# #653. 两数之和 IV - 输入为二叉搜索树 / Two Sum IV - Input is a BST

> 难度：简单 · 标签：Hash Table、Two Pointers、Tree、Depth-First Search、Breadth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/)

---

## 题目（英文原版）

**Description**

Given the root of a binary search tree and an integer k, return true if there exist two elements in the BST such that their sum is equal to k, or false otherwise.

**Examples**

**Example 1:**

```
Input: root = [5,3,6,2,4,null,7], k = 9
Output: true
```

**Example 2:**

```
Input: root = [5,3,6,2,4,null,7], k = 28
Output: false
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -104 <= Node.val <= 104
- root is guaranteed to be a valid binary search tree.
- -105 <= k <= 105

---

## 题目（中文翻译）

给定一棵二叉搜索树（BST）的根节点 `root` 和一个整数 `k`，如果在该 BST 中存在两个节点的值之和等于 `k`，返回 `true`；否则返回 `false`。

**示例 1**

```
Input: root = [5,3,6,2,4,null,7], k = 9
Output: true
```

**示例 2**

```
Input: root = [5,3,6,2,4,null,7], k = 28
Output: false
```

**约束条件**

- 树中节点的数量在 `[1, 10⁴]` 区间内。  
- `-10⁴ <= Node.val <= 10⁴`  
- `root` 保证是一棵有效的二叉搜索树。  
- `-10⁵ <= k <= 10⁵`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的想法是把整棵二叉搜索树（BST）里的所有节点值都取出来，放进一个列表 `vals`。  
有了完整的数组后，只要遍历所有可能的两两组合，判断它们的和是否等于目标 `k` 即可。  

- **用到的数据结构**：  
  - **列表**（Array/List）就像一本电话簿，把所有电话号码（这里是节点值）排成一列，方便逐个查看。  
  - **双层循环**相当于把电话簿里每个人的号码都和后面的每个人的号码配对一次。  

- **为什么正确**：  
  因为我们检查了 **所有** 可能的两节点组合，只要有一对满足 `a + b = k`，必然会在遍历过程中被发现。

- **时间/空间复杂度**：  
  - 时间复杂度是 `O(n²)`，这里的 `n` 是树的节点数。  
    用大白话说，就是如果树有 1000 个节点，最坏情况下要比较大约 `1000 × 999 / 2 ≈ 500,000` 次。  
  - 空间复杂度是 `O(n)`，因为我们需要一个列表把所有节点值都存下来。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def findTarget_bruteforce(root: TreeNode, k: int) -> bool:
    # 1. 把所有节点值收集到列表里（这里用中序遍历，顺序不影响结果）
    vals = []
    def inorder(node: TreeNode):
        if not node:
            return
        inorder(node.left)          # 先遍历左子树
        vals.append(node.val)       # 访问当前节点
        inorder(node.right)         # 再遍历右子树
    inorder(root)

    # 2. 双层循环检查任意两数之和是否为 k
    n = len(vals)
    for i in range(n):
        for j in range(i + 1, n):   # j 从 i+1 开始，避免重复配对和自己配对
            if vals[i] + vals[j] == k:
                return True
    return False
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  两层循环导致每个节点会和其它 `n‑1` 个节点比较一次，最坏情况是平方级别的计算量。

- **空间复杂度**：`O(n)`  
  需要一个列表保存所有节点值，列表大小正好等于树的节点数。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在于 **“两层循环”**——我们把所有值都列出来后，又要逐对比较。  
其实我们不必把所有值都记下来再两两配对，只要在遍历树的过程中 **即时检查** 是否已经出现过能够组成 `k` 的另一个数即可。

**关键技巧**：使用**哈希表**（在 Python 中是 `set`），它像一本随时可以查到页码的字典，查找某个元素是否已经出现的时间是 `O(1)`（常数时间）。  

具体做法：

1. 从根节点开始深度优先遍历（DFS），可以是递归也可以是显式栈。  
2. 对每个访问到的节点 `node.val`，先计算它需要的“另一半” `complement = k - node.val`。  
3. 在哈希表 `seen` 中查询 `complement` 是否已经出现过：  
   - 如果出现，说明之前遍历到的某个节点正好可以和当前节点凑成 `k`，直接返回 `True`。  
   - 如果没有出现，则把当前节点的值加入 `seen`，继续遍历。  
4. 整棵树遍历完仍未找到配对，返回 `False`。

这样我们只遍历一次树，且每个节点的查找/插入都是常数时间，整体是线性时间 `O(n)`，空间只需要存放已经遍历过的值，最坏情况下仍是 `O(n)`（但比双层循环省掉了大量的比较）。

> **进阶优化**：如果想把空间降到 `O(h)`（`h` 为树的高度），可以利用 BST 的中序遍历特性，分别用两个迭代器实现“正向”和“逆向”遍历，类似数组的双指针。但对初学者来说，哈希表的做法已经足够好且易于理解，这里就不展开实现细节。

#### 代码（Python）

```python
def findTarget(root: TreeNode, k: int) -> bool:
    """
    使用哈希表（set）在遍历 BST 的同时检查是否存在两数之和为 k。
    """
    seen = set()               # 用来保存已经遍历过的节点值，类似“查字典”

    def dfs(node: TreeNode) -> bool:
        if not node:
            return False
        # 1. 计算当前节点需要的另一半
        complement = k - node.val
        # 2. 看看这另一半是否已经在之前的遍历里出现过
        if complement in seen:
            # 找到了！直接返回 True，后面的递归会一直向上传递这个结果
            return True
        # 3. 否则把当前值加入集合，继续遍历左右子树
        seen.add(node.val)
        # 这里先左后右，只要遍历完整棵树都能找到答案
        return dfs(node.left) or dfs(node.right)

    return dfs(root)
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  每个节点只被访问一次，哈希表的查找和插入都是常数时间，所以总体随节点数线性增长。

- **空间复杂度**：`O(n)`（最坏情况）  
  哈希表最多会保存所有节点的值。如果树非常不平衡（比如链状），递归栈的深度也会达到 `O(n)`。  
  相比暴力解的 `O(n²)` 时间，这里的空间开销已经非常合理。

---

## 心得

- **核心技巧**：利用哈希表（`set`）在遍历过程中即时查找“补数”，把两数之和的问题从 “两层循环” 降到 “一次遍历”。  
- **适用的题型**：  
  1. **Two Sum** 系列的变体（数组、链表、树等）  
  2. **相同值判断**（如判断数组中是否有重复元素）  
  3. **寻找配对**（如在链表中找两数之和、在矩阵中找配对等）  
- **一句话总结解题钥匙**：**“遍历时记住已经见过的数，用哈希表快速判断是否已有对应的补数”。**

---

## 反思

- **第一反应**：把所有节点值先收集到列表，再用双层循环检查配对。  
- **最容易踩的坑**：  
  - **遗漏负数或零**：`k`、节点值都可能是负数，必须在计算补数时直接相减，不能假设都是正数。  
  - **重复使用同一个节点**：在暴力解里要确保 `i != j`，即不要把同一个节点的值加两次。  
  - **递归深度**：如果树非常深（接近 10⁴），递归可能触发栈溢出，实际面试中可以改写为显式栈的迭代版。  
- **下次遇到同类题**，第一步应该想到：**“是否可以在遍历的过程中用哈希表记录已经看到的元素，实时检查是否已有配对”。**这样往往能立刻把时间复杂度从平方级降低到线性级。