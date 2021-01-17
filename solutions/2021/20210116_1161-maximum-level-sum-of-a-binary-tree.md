# #1161. 二叉树的最大层和 / Maximum Level Sum of a Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, the level of its root is 1, the level of its children is 2, and so on.
Return the smallest level x such that the sum of all the values of nodes at level x is maximal.

**Examples**

**Example 1:**

```
Input: root = [1,7,0,7,-8,null,null]
Output: 2
Explanation: 
Level 1 sum = 1.
Level 2 sum = 7 + 0 = 7.
Level 3 sum = 7 + -8 = -1.
So we return the level with the maximum sum which is level 2.
```

**Example 2:**

```
Input: root = [989,null,10250,98693,-89388,null,null,null,-32127]
Output: 2
```

**Constraints**

- The number of nodes in the tree is in the range [1, 104].
- -105 <= Node.val <= 105

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点（root），根节点所在的层（level）记为 1，根节点的子节点所在的层记为 2，依此类推。返回满足以下条件的最小层 x：该层所有节点（node）的值（value）之和最大。

约束条件：

- 树中节点的数量在区间 \[1, 10⁴\] 内。
- -10⁵ ≤ Node.val ≤ 10⁵。

示例 1:
```
Input: root = [1,7,0,7,-8,null,null]
Output: 2
Explanation: 
层 1 的和 = 1。
层 2 的和 = 7 + 0 = 7。
层 3 的和 = 7 + -8 = -1。
因此返回和最大的层，即层 2。
```

示例 2:
```
Input: root = [989,null,10250,98693,-89388,null,null,null,-32127]
Output: 2
```

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直观的想法是：**先求出树的最大深度**，然后**逐层遍历**，每遍历一层就把该层所有节点的值加起来，记录下最大和对应的层数。  

- **求深度**可以用递归：`depth = max(depth(left), depth(right)) + 1`。  
- **求某一层的和**同样用递归：从根节点出发，记录当前层数 `cur`，当 `cur == target` 时把节点值加入累计和；否则继续向左、右子树递归，层数 `cur+1`。  

这相当于“每层都重新走一遍树”。把树想象成一本书，**每查一次目录（层数）就要把整本书重新翻一遍**，所以会很慢。

**为什么这个方法一定能得到正确答案**  
因为我们把每一层的所有节点都完整地遍历了一遍并求和，层数是从 1 开始递增的，比较所有层的和后选出最大且层数最小的那一层，完全符合题意。

**复杂度分析（大白话）**  
- **时间复杂度**：如果树有 `n` 个节点，最坏情况下（比如链状的二叉树）树高为 `n`，我们会对每一层都遍历整棵树一次，导致大约 `1 + 2 + … + n = n·(n+1)/2` 次访问，记作 **O(n²)**。可以把它想象成“把 1000 本书每本都读 1000 次”，工作量会翻倍增长。  
- **空间复杂度**：递归栈的最大深度等于树的高度，最坏 O(n)（链状树），平均 O(log n)（平衡树）。额外的存储只有几个整型变量，记作 **O(1)**（不计递归栈）。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxLevelSum_bruteforce(root: TreeNode) -> int:
    # ---------- 1. 求树的最大深度 ----------
    def get_depth(node: TreeNode) -> int:
        if not node:
            return 0
        # 左右子树深度取最大值，再加上当前节点本身
        return max(get_depth(node.left), get_depth(node.right)) + 1

    max_depth = get_depth(root)

    # ---------- 2. 求指定层的节点和 ----------
    def level_sum(node: TreeNode, cur: int, target: int) -> int:
        if not node:
            return 0
        if cur == target:               # 正好到了目标层
            return node.val
        # 继续向下走，层数加 1
        return (level_sum(node.left, cur + 1, target) +
                level_sum(node.right, cur + 1, target))

    best_level = 1          # 默认答案是第 1 层
    best_sum = level_sum(root, 1, 1)   # 第 1 层的和

    # ---------- 3. 逐层遍历求和 ----------
    for lvl in range(2, max_depth + 1):
        cur_sum = level_sum(root, 1, lvl)   # 每层都重新遍历整棵树
        if cur_sum > best_sum:              # 只保留更大的和
            best_sum = cur_sum
            best_level = lvl

    return best_level
```

#### 复杂度

- **时间复杂度**：`O(n²)`  
  解释：对每一层都要遍历全部 `n` 个节点（最坏情况下），所以工作量约等于 `n × n`。
- **空间复杂度**：`O(n)`（递归栈）  
  解释：递归的最深层次等于树的高度，最坏可能是 `n`，但不需要额外的数组或哈希表。

---

### 2. 最优解

#### 思路  

暴力解的瓶颈在于**每层都要重新遍历整棵树**，导致时间呈二次方增长。我们可以在一次遍历的过程中**同步记录每一层的和**，这样每个节点只被访问一次，时间降到线性 `O(n)`。

实现思路有两种，下面用**广度优先搜索（BFS）**来说明，它的核心工具是**队列**（想象成排队买票的队列）：

1. **把根节点放进队列**，它所在的层数是 1。  
2. 进入循环，每次取出当前层的所有节点（队列的长度就是当前层的节点数），把它们的值累加得到该层的和。  
3. 同时把这些节点的左右子节点（如果有）加入队列，准备在下一轮处理——这一步相当于“把孩子们排到队尾，等前面的节点全部买完票后再轮到他们”。  
4. 记录遍历过程中出现的**最大层和**以及对应的**层数**（如果出现相同的和，保留较小的层数，因为我们是按层从上往下遍历的）。  
5. 队列为空时遍历结束，返回记录的层数。

**关键数据结构解释**  
- **队列**：类似排队买咖啡的队列，最先进去的最先出来（FIFO）。在 Python 中可以用 `collections.deque` 高效实现。  
- **层数计数**：用一个整数 `level`，每处理完一层就 `level += 1`。  

整个过程只需要一次遍历，时间线性，空间只需要保存当前层的节点（最坏情况下是树的最宽层，最多 `n/2`，记作 `O(n)`）。

#### 代码（Python）

```python
from collections import deque
from typing import Optional

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional['TreeNode'] = None,
                 right: Optional['TreeNode'] = None):
        self.val = val
        self.left = left
        self.right = right


def maxLevelSum(root: TreeNode) -> int:
    """
    BFS 一次遍历求每层和，返回和最大的最小层数。
    """
    if not root:
        return 0  # 题目保证非空，这里仅作防御式编程

    q = deque([root])   # 队列初始化，只装根节点
    level = 1            # 当前处理的层数（根层是 1）
    best_level = 1       # 记录和最大的层数
    best_sum = root.val  # 初始把根层的和设为当前最大

    # 只要队列不为空，就还有未处理的节点
    while q:
        cur_level_sum = 0               # 本层所有节点值的累计和
        for _ in range(len(q)):         # 只遍历当前层的节点数量
            node = q.popleft()          # 取出队首节点
            cur_level_sum += node.val   # 加到本层和

            # 把左右子节点加入队列，准备在下一层处理
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        # 更新最大和以及对应层数（因为是从上到下遍历，先出现的层数自然更小）
        if cur_level_sum > best_sum:
            best_sum = cur_level_sum
            best_level = level

        level += 1   # 进入下一层

    return best_level
```

#### 复杂度

- **时间复杂度**：`O(n)`  
  解释：每个节点恰好进入队列一次、弹出一次，做 `O(1)` 的加法和指针检查，总共 `n` 次操作。相比暴力的 `O(n²)`，把“每层重新遍历整棵树”这个重复工作全部消掉了。  
- **空间复杂度**：`O(w)`，这里 `w` 是树的最大宽度，最坏情况下 `w ≤ n`，即 `O(n)`。  
  解释：我们只需要同时保存当前层的所有节点，层数越宽需要的空间越多，但仍然是线性级别。

---

## 心得

- **核心技巧**：**层序遍历（BFS）一次完成所有层的统计**。  
- **适用场景**：  
  1. “求每层节点个数” / “求每层最大值” 等需要按层统计的信息。  
  2. “最左/最右节点值”——在 BFS 过程中记录每层第一个/最后一个节点即可。  
  3. “二叉树的最宽层宽度”——同样利用 BFS 统计每层节点数的最大值。  
- **一句话总结**：**只要一次遍历就能把“层”这层信息全部收集好，别再为每层单独走树而浪费时间。**

---

## 反思

- **第一反应**：看到“层”和“求和”，立刻想到 **层序遍历**（BFS）或者 **递归记录层号** 的办法。  
- **最容易踩的坑**：  
  - **负数节点**：层和可能为负，不能把初始化的最大和设为 `0`（否则会误判全部负数的情况）。  
  - **单节点树**：要确保返回层数 `1`，而不是默认的 `0`。  
  - **层数相同的最大和**：题目要求最小层数，需要在遍历时**先出现的层自动获胜**，所以只在 “>” 时更新（而不是 “>=”）。  
- **下次思路**：遇到需要“按层统计”的二叉树题目，第一步就**在脑中画一层层的队列**，决定使用 BFS（层序）还是 DFS+哈希表记录层号，两者都能一次遍历完成统计。这样可以避免重复遍历导致的 `O(n²)` 甚至更差的时间复杂度。