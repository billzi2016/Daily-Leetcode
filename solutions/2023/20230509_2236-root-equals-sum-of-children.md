# #2236. 根等于子节点之和 / Root Equals Sum of Children

> 难度：简单 · 标签：Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/root-equals-sum-of-children/)

---

## 题目（英文原版）

**Description**

You are given the root of a binary tree that consists of exactly 3 nodes: the root, its left child, and its right child.
Return true if the value of the root is equal to the sum of the values of its two children, or false otherwise.

**Examples**

**Example 1:**

```
Input: root = [10,4,6]
Output: true
Explanation: The values of the root, its left child, and its right child are 10, 4, and 6, respectively.
10 is equal to 4 + 6, so we return true.
```

**Example 2:**

```
Input: root = [5,3,1]
Output: false
Explanation: The values of the root, its left child, and its right child are 5, 3, and 1, respectively.
5 is not equal to 3 + 1, so we return false.
```

**Constraints**

- The tree consists only of the root, its left child, and its right child.
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

**题目描述**  
给定一棵二叉树的根节点 `root`，该树恰好包含 3 个节点：根节点、左子节点（left child）和右子节点（right child）。  
如果根节点的值等于其左右子节点值之和，则返回 `true`；否则返回 `false`。

**示例 1**  
```
Input: root = [10,4,6]
Output: true
Explanation: 根节点、左子节点和右子节点的值分别是 10、4、6。10 等于 4 + 6，故返回 true。
```

**示例 2**  
```
Input: root = [5,3,1]
Output: false
Explanation: 根节点、左子节点和右子节点的值分别是 5、3、1。5 不等于 3 + 1，故返回 false。
```

**约束条件**  
- 树仅包含根节点、左子节点和右子节点。  
- `-100 <= Node.val <= 100`

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

这道题只有 **恰好 3 个结点**：根节点、左孩子、右孩子。  
最直接的想法就是把这三个数读出来，直接算根节点的值是否等于左孩子值加右孩子值。

- **使用的数据结构**  
  - `TreeNode`：二叉树的结点对象。可以把它想象成一本家庭树册，`node.val` 是人的年龄，`node.left` / `node.right` 分别是左/右孩子的页面指针。  
  - 只需要访问这三个指针即可，不需要额外的容器（比如列表、哈希表），所以几乎没有“查字典”这种操作。

- **为什么正确**  
  题目已经保证树里只有这三颗结点，根一定有左、右孩子。只要把这三个数拿出来比较，答案必然是对的。

- **时间/空间复杂度**  
  - **时间复杂度**：`O(1)`。这里的 `O(1)` 表示不管树有多大（这里固定为 3），执行的操作次数都是常数次。可以想象成只要数三下手指头，就能得到答案。
  - **空间复杂度**：`O(1)`。我们只用了几个临时变量来存数值，根本不需要额外的存储空间。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 当前结点的数值
        self.left = left        # 左子结点（可能为 None）
        self.right = right      # 右子结点（可能为 None）

def checkTree(root: TreeNode) -> bool:
    """
    返回根节点的值是否等于左右子节点值之和
    """
    # 直接取出三个值
    root_val = root.val               # 根节点的值
    left_val = root.left.val if root.left else 0   # 左子节点的值（题目保证不为 None）
    right_val = root.right.val if root.right else 0 # 右子节点的值（题目保证不为 None）

    # 对比根和值之和
    return root_val == left_val + right_val
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做了几次加法和比较，和树的大小无关。  
- **空间复杂度**：`O(1)` —— 只用了几个局部变量，额外占用的内存是常数级别。

---

### 2. 最优解

#### 思路  

对于这道 **固定大小**（恰好 3 个结点）的树，**暴力解已经是最优**。  
如果把这道题放到更一般的 “根等于左右子树所有节点之和” 的情形，才会需要更复杂的遍历或递归。但在本题的约束下：

- **慢在哪里？**  
  没有慢的地方——我们只访问了三个结点，已经是最少的操作次数。

- **一步步推导**  
  1. 读取根、左、右三个值。  
  2. 计算左+右。  
  3. 比较是否相等。  

  这三个步骤已经是 **常数时间**，无法再压缩。

- **核心技巧**  
  - **直接访问**：因为树的结构已知且固定，直接点到节点属性即可。  
  - **无需遍历**：不需要递归、栈或队列等额外工具。

- **类比**  
  想象你站在一棵只有根、左、右三个枝桠的树前，只要看三根枝桠的长度就能判断根是否等于两侧之和，根本不需要走来走去检查其它枝桠。

#### 代码（Python）

```python
def checkTree(root: TreeNode) -> bool:
    # 题目保证左、右子节点一定存在
    return root.val == root.left.val + root.right.val
```

#### 复杂度

- **时间复杂度**：`O(1)` —— 只做一次加法和一次比较。和暴力解完全相同，且已经是最优。  
- **空间复杂度**：`O(1)` —— 不使用额外的数据结构。

---

## 心得

- **核心技巧**：**直接访问已知节点**，不必使用遍历或额外存储。  
- **适用的题型**  
  1. 只涉及固定数量节点的简单判断（比如 “两个节点相等吗？”）。  
  2. “根节点等于左右子树之和” 的变体（需要递归求子树和）。  
  3. 树结构已知且规模极小的题目。  
- **一句话总结解题钥匙**：**先看约束，若规模固定，就直接取值比较，别搬不必要的工具。**

---

## 反思

- **第一反应**：读题后马上想到 “把根、左、右三个数拿出来相加比较”。  
- **最容易踩的坑**  
  - 忘记题目已经保证左、右子节点一定存在，导致写了额外的空指针检查。  
  - 把 `TreeNode` 当成普通列表，误用了索引方式访问。  
- **下次遇到同类题**：第一步先确认 **树的规模和结构**，如果节点数是常数，就直接**点到点**取值；如果规模不确定，再考虑遍历或递归。