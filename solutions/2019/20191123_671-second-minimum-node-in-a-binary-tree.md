# #671. 二叉树中的第二最小节点 / Second Minimum Node In a Binary Tree

> 难度：简单 · 标签：Tree、Depth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/second-minimum-node-in-a-binary-tree/)

---

## 题目（英文原版）

**Description**

Given a non-empty special binary tree consisting of nodes with the non-negative value, where each node in this tree has exactly two or zero sub-node. If the node has two sub-nodes, then this node's value is the smaller value among its two sub-nodes. More formally, the property root.val = min(root.left.val, root.right.val) always holds.
Given such a binary tree, you need to output the second minimum value in the set made of all the nodes' value in the whole tree.
If no such second minimum value exists, output -1 instead.

**Examples**

**Example 1:**

```
Input: root = [2,2,5,null,null,5,7]
Output: 5
Explanation: The smallest value is 2, the second smallest value is 5.
```

**Example 2:**

```
Input: root = [2,2,2]
Output: -1
Explanation: The smallest value is 2, but there isn't any second smallest value.
```

**Constraints**

- The number of nodes in the tree is in the range [1, 25].
- 1 <= Node.val <= 231 - 1
- root.val == min(root.left.val, root.right.val) for each internal node of the tree.

---

## 题目（中文翻译）

给定一棵非空的特殊二叉树（binary tree），其中每个节点的取值为非负整数，且每个节点恰好拥有 **两个子节点（sub-node）** 或 **零个子节点**。如果一个节点拥有两个子节点，则该节点的值等于其两个子节点值中的较小者。形式化地，下面的性质始终成立：

```
root.val = min(root.left.val, root.right.val)
```

已知这样的一棵二叉树，求整棵树中所有节点值构成的集合的**第二小的值**。如果不存在第二小的值，则返回 `-1`。

**示例 1**  
**示例 2**  
**约束条件**  

示例：  
**示例 1:**  
```
Input: root = [2,2,5,null,null,5,7]
Output: 5
Explanation: 最小的值是 2，第二小的值是 5。
```

**示例 2:**  
```
Input: root = [2,2,2]
Output: -1
Explanation: 最小的值是 2，但不存在第二小的值。
```

约束条件：
- 树中节点的数量在 `[1, 25]` 范围内。
- `1 <= Node.val <= 2^31 - 1`
- 对于树中的每个内部节点，`root.val == min(root.left.val, root.right.val)` 成立。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  
最直接的办法就是把整棵树的所有节点值都找出来，放进一个容器（比如列表），然后在这个容器里找第二小的数。

- **遍历树**：我们可以用深度优先搜索（DFS）或者广度优先搜索（BFS）把每个节点都访问一次。这里把 DFS 当成“走迷宫”，每走到一个节点就把它的值记下来。
- **收集数值**：把每个节点的 `val` 加到一个列表 `vals` 中。相当于把树里所有的“水果”装进篮子。
- **求第二小**：把 `vals` 排序（从小到大），第一个元素就是最小值，第二个不同于最小值的元素就是我们要的答案。如果整个列表里只有一种数值，则说明没有第二小，返回 `-1`。

> **为什么正确**  
> 我们把所有节点的值都列了出来，第二小的定义就是“在这堆数里，除去最小的那个，还剩下的最小”。只要遍历不漏，答案必然在列表里。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

def findSecondMinimumValue(root: TreeNode) -> int:
    # 1. 用 DFS 把所有节点值收集到列表中
    vals = []
    def dfs(node: TreeNode):
        if not node:
            return
        vals.append(node.val)          # 把当前节点的值加入列表
        dfs(node.left)                 # 递归左子树
        dfs(node.right)                # 递归右子树
    dfs(root)

    # 2. 对列表排序，找出第一个不同于最小值的数
    vals.sort()                       # 从小到大排好序
    min_val = vals[0]                 # 最小值一定在第一个位置
    for v in vals:                    # 从头遍历，找第一个不等于 min_val 的数
        if v != min_val:
            return v                  # 找到第二小，直接返回
    return -1                         # 没有第二小，返回 -1
```

#### 复杂度

- **时间复杂度**：`O(N log N)`  
  - `N` 为树的节点数。我们遍历一次得到 `O(N)`，随后对列表排序需要 `O(N log N)`。  
  - 大白话：如果树有 1000 个节点，排序大约需要 1000 × log₂1000 ≈ 1000 × 10 = 1 万次比较。

- **空间复杂度**：`O(N)`  
  - 需要一个列表把所有节点值存下来，最坏情况是把所有节点都装进去。递归栈的深度最多也是 `O(N)`（树可能是链状），所以总空间仍是 `O(N)`。

---

### 2. 最优解

#### 思路  
暴力解的瓶颈在 **排序**（`O(N log N)`）以及 **额外存储所有节点值**（`O(N)`）。  
观察题目给出的特殊属性：

> 对于每个内部节点 `root`，都有 `root.val = min(root.left.val, root.right.val)`  

也就是说，**根节点的值一定是整棵树的最小值**。我们只需要在树的其余位置找一个**大于根节点且最小的**数即可。

基于此，我们可以直接在遍历的过程中“剪枝”：

1. **记录最小值**：`min_val = root.val`（根节点的值）。
2. **DFS**：遍历每个节点，只有当节点的值 **大于** `min_val` 时，它才有可能是第二小的候选者。此时把它与当前的答案做比较，取更小的那个。
3. **剪枝**：如果节点的值等于 `min_val`，我们必须继续往下找，因为它的子树里可能藏有更大的数。但如果节点的值已经大于当前找到的第二小值，就不必继续往下搜索该子树（因为子树的所有值都不可能比当前第二小更小——树的特殊属性保证子树的根值不大于子树内部的任何值）。

这样我们只遍历一次树，**不需要额外的列表，也不需要排序**。

> **核心概念解释**  
> - **深度优先搜索（DFS）**：想象在一棵树里从根部一路往下走，走到叶子再回头，这样的遍历方式叫深度优先。代码里用递归实现，每次调用 `dfs(node)` 就相当于把“探险家”送进当前节点的子树。  
> - **剪枝**：就像在找宝藏时，已经发现了一个比之前更好的线索，就可以把不可能更好的路径直接丢掉，不再浪费时间。

#### 代码（Python）

```python
def findSecondMinimumValue(root: TreeNode) -> int:
    # 根节点的值就是全树的最小值
    min_val = root.val
    # 用一个变量记录当前找到的第二小值，初始设为无穷大
    second_min = float('inf')

    def dfs(node: TreeNode):
        nonlocal second_min
        if not node:
            return
        # 若当前节点的值大于最小值且小于当前的 second_min，更新答案
        if min_val < node.val < second_min:
            second_min = node.val
            # 已经找到更小的第二候选，可以直接返回，不必继续向下搜索
            return
        # 如果节点值等于最小值，子树里可能还有更大的数，继续搜索
        if node.val == min_val:
            dfs(node.left)
            dfs(node.right)
        # 如果节点值已经 >= second_min，则这条路径不可能产生更小的第二值，直接剪枝
        # （这里不需要显式写，因为上面的 if 已经返回了）

    dfs(root)
    # 若 second_min 没有被更新，说明不存在第二小值
    return second_min if second_min != float('inf') else -1
```

#### 复杂度

- **时间复杂度**：`O(N)`  
  - 每个节点最多访问一次，没有排序或额外遍历。  
  - 大白话：如果有 1000 个节点，我们只检查 1000 次，速度是线性的。

- **空间复杂度**：`O(H)`（递归栈深度）  
  - `H` 为树的高度。最坏情况下（树退化成链表）`H = N`，此时空间是 `O(N)`；但对平衡二叉树来说 `H ≈ log₂N`，只需要很小的栈空间。

---

## 心得

- **核心技巧**：利用题目给出的 “每个内部节点的值等于左右子节点的最小值” 这一特性，直接在遍历时寻找大于根节点且最小的数，做到 **一次遍历**。
- **适用的题型**  
  1. “在特殊二叉树中查找第二大/第二小值”  
  2. “寻找树中满足某种单调关系的第 K 小/大的元素”  
  3. “在满足父子关系约束的树结构里做范围查询”
- **一句话总结解题钥匙**：**根节点就是全局最小值，只要在树的其余位置找最小的“大于根”的数即可**。

---

## 反思

- **第一反应**：把所有节点值收集到列表再排序——这是一种“把所有东西都搬到桌面上再挑”的通用思路。
- **最容易踩的坑**  
  - 忘记根节点的值一定是最小值，导致在遍历时把根也当作候选，可能返回错误的结果。  
  - 对只含单一数值的树没有返回 `-1` 的处理。  
  - 在剪枝时误删了等于最小值的子树，导致漏掉真正的第二小值。
- **下次类似题的第一步**：**先把题目给出的结构性约束（如父子值关系、排序性质）写下来，思考这些约束能直接把搜索范围缩小到多少**。这一步往往能从 `O(N log N)` 降到 `O(N)`，甚至 `O(log N)`。