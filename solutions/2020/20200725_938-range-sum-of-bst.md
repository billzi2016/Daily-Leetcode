# #938. 二叉搜索树范围和 / Range Sum of BST

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Search Tree、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/range-sum-of-bst/)

---

## 题目（英文原版）

**Description**

Given the root node of a binary search tree and two integers low and high, return the sum of values of all nodes with a value in the inclusive range [low, high].

**Examples**

**Example 1:**

```
Input: root = [10,5,15,3,7,null,18], low = 7, high = 15
Output: 32
Explanation: Nodes 7, 10, and 15 are in the range [7, 15]. 7 + 10 + 15 = 32.
```

**Example 2:**

```
Input: root = [10,5,15,3,7,13,18,1,null,6], low = 6, high = 10
Output: 23
Explanation: Nodes 6, 7, and 10 are in the range [6, 10]. 6 + 7 + 10 = 23.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 2 * 104].
- 1 <= Node.val <= 105
- 1 <= low <= high <= 105
- All Node.val are unique.

---

## 题目（中文翻译）

给定一棵二叉搜索树（binary search tree）的根节点（root）以及两个整数 `low` 和 `high`，返回所有节点（node）值在闭区间 `[low, high]` 内的节点值之和。

**示例 1：**  
**示例 2：**  
**约束条件：**

示例  
示例 1:  
Input: `root = [10,5,15,3,7,null,18], low = 7, high = 15`  
Output: `32`  
Explanation: 节点 7、10 和 15 位于区间 `[7, 15]` 内。`7 + 10 + 15 = 32`。

示例 2:  
Input: `root = [10,5,15,3,7,13,18,1,null,6], low = 6, high = 10`  
Output: `23`  
Explanation: 节点 6、7 和 10 位于区间 `[6, 10]` 内。`6 + 7 + 10 = 23`。

约束条件  
- 树中节点的数量在范围 `[1, 2 * 10^4]` 内。  
- `1 <= Node.val <= 10^5`  
- `1 <= low <= high <= 10^5`  
- 所有 `Node.val` 均唯一。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把整棵二叉搜索树（BST）全部遍历一遍，**把每个节点的值都拿出来检查**，如果它落在 `[low, high]` 区间内就把它加到答案里。  
- **遍历方式**：可以用递归的深度优先搜索（DFS），也可以用显式栈的迭代 DFS，甚至层序遍历（BFS）都行。这里用最常见的递归实现。  
- **数据结构类比**：把树想象成一本层层展开的“家谱”。我们从根节点（家族的祖先）出发，依次“拜访”每个子孙（左子树、右子树），把每个人的年龄（节点值）记下来。如果年龄在我们感兴趣的区间 `[low, high]`，就把它加入“统计表”。  

这种做法一定能得到正确答案，因为我们没有漏掉任何节点。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

def rangeSumBST_brute(root: TreeNode, low: int, high: int) -> int:
    """
    暴力遍历所有节点，统计落在 [low, high] 区间的节点值之和。
    """
    if not root:                     # 空节点直接返回 0
        return 0

    # 递归遍历左子树、右子树，并把当前节点的值（如果符合条件）加进去
    left_sum = rangeSumBST_brute(root.left, low, high)
    right_sum = rangeSumBST_brute(root.right, low, high)

    cur = root.val if low <= root.val <= high else 0   # 当前节点是否计入
    return cur + left_sum + right_sum
```

#### 复杂度  

- **时间复杂度**：`O(N)`，其中 `N` 是树中节点的数量。我们要访问每个节点一次，就像把一本 200 页的书每页都翻一遍。  
- **空间复杂度**：`O(H)`，`H` 为树的高度。递归调用栈会保存从根到当前节点的路径，最坏情况下（树退化成链表）高度是 `N`，所以最坏是 `O(N)`；平均情况下（平衡树）是 `O(log N)`。

---

### 2. 最优解

#### 思路  
暴力解的“慢”点在于**我们不分青红皂白地访问了每一个节点**。而二叉搜索树有一个重要特性：

> 对于任意节点 `node`，左子树所有节点的值 **小于** `node.val`，右子树所有节点的值 **大于** `node.val`。

利用这个特性，我们可以**剪枝**（提前停止）不可能落在 `[low, high]` 区间的子树：

1. **如果 `node.val < low`**  
   - 左子树的所有值更小，肯定也小于 `low`，不需要再往左走。直接递归右子树即可。  
2. **如果 `node.val > high`**  
   - 右子树的所有值更大，肯定也大于 `high`，不需要往右走。直接递归左子树即可。  
3. **否则**（`low ≤ node.val ≤ high`）  
   - 当前节点要计入答案，同时左右子树都可能有符合区间的节点，需要继续递归两边。

这样我们只访问**可能落在区间的节点**，避免了大量无用的遍历。

#### 代码（Python）

```python
def rangeSumBST_opt(root: TreeNode, low: int, high: int) -> int:
    """
    利用 BST 的性质剪枝，只遍历可能落在区间的节点。
    """
    if not root:
        return 0

    # 情况 1：当前节点值太小，左子树全被淘汰，只看右子树
    if root.val < low:
        return rangeSumBST_opt(root.right, low, high)

    # 情况 2：当前节点值太大，右子树全被淘汰，只看左子树
    if root.val > high:
        return rangeSumBST_opt(root.left, low, high)

    # 情况 3：当前节点在区间内，左右子树都可能有贡献
    left_sum = rangeSumBST_opt(root.left, low, high)
    right_sum = rangeSumBST_opt(root.right, low, high)
    return root.val + left_sum + right_sum
```

#### 复杂度  

- **时间复杂度**：`O(M)`，`M` 为**实际访问的节点数**。在最坏情况下（`low = 1, high = 10^5`，覆盖全部节点），仍然是 `O(N)`；但在一般情况下，剪枝能显著减少访问数量，尤其当查询区间很窄时，复杂度接近 `O(log N)`。  
- **空间复杂度**：同样是递归栈的深度 `O(H)`，与暴力解相同，但因为访问的节点更少，实际占用的栈空间往往更小。

---

## 心得

- **核心技巧**：利用二叉搜索树的“左小右大”特性进行**剪枝**，只遍历可能满足条件的子树。  
- **适用的题型**：  
  1. 在 BST 中查找第 k 小/大的元素（利用子树大小剪枝）。  
  2. 在 BST 中寻找两个节点的最近公共祖先（利用大小关系决定向左还是向右）。  
- **一句话总结**：**“在有序结构里，先判断方向再递归，能省掉大半路程”。**

---

## 反思

- **第一反应**：看到是 BST，立刻想到可以利用节点大小关系来“跳过”不必要的子树，而不是盲目遍历。  
- **最容易踩的坑**：  
  - 忘记对 `root` 为 `None` 的情况提前返回，导致递归深度错误。  
  - 把剪枝条件写反（比如 `root.val < low` 时仍然去左子树），会把正确答案排除在外。  
- **下次类似题的第一步**：先确认输入结构是否有“有序”或“单调”特性（如 BST、排序数组、单调栈），再思考如何利用这些特性**提前停止**不必要的搜索。