# #662. 二叉树的最大宽度 / Maximum Width of Binary Tree

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/maximum-width-of-binary-tree/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return the maximum width of the given tree.
The maximum width of a tree is the maximum width among all levels.
The width of one level is defined as the length between the end-nodes (the leftmost and rightmost non-null nodes), where the null nodes between the end-nodes that would be present in a complete binary tree extending down to that level are also counted into the length calculation.
It is guaranteed that the answer will in the range of a 32-bit signed integer.

**Examples**

**Example 1:**

```
Input: root = [1,3,2,5,3,null,9]
Output: 4
Explanation: The maximum width exists in the third level with length 4 (5,3,null,9).
```

**Example 2:**

```
Input: root = [1,3,2,5,null,null,9,6,null,7]
Output: 7
Explanation: The maximum width exists in the fourth level with length 7 (6,null,null,null,null,null,7).
```

**Example 3:**

```
Input: root = [1,3,2,5]
Output: 2
Explanation: The maximum width exists in the second level with length 2 (3,2).
```

**Constraints**

- The number of nodes in the tree is in the range [1, 3000].
- -100 <= Node.val <= 100

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点 `root`，返回该树的最大宽度。  
树的最大宽度定义为所有层（level）中宽度的最大值。  
某一层的宽度被定义为最左侧非空节点和最右侧非空节点之间的长度，其中 **包括** 在完整二叉树（complete binary tree）延伸到该层时可能出现的所有空节点（null nodes）。  
答案保证在 32 位有符号整数（32-bit signed integer）的范围内。

**示例 1**  
**输入**: `root = [1,3,2,5,3,null,9]`  
**输出**: `4`  
**解释**: 最大宽度出现在第三层，长度为 4（节点序列为 5,3,null,9）。

**示例 2**  
**输入**: `root = [1,3,2,5,null,null,9,6,null,7]`  
**输出**: `7`  
**解释**: 最大宽度出现在第四层，长度为 7（节点序列为 6,null,null,null,null,null,7）。

**示例 3**  
**输入**: `root = [1,3,2,5]`  
**输出**: `2`  
**解释**: 最大宽度出现在第二层，长度为 2（节点序列为 3,2）。

**约束条件**  
- 树中节点的数量在 `[1, 3000]` 区间内。  
- `-100 <= Node.val <= 100`   (其中 `Node.val` 为节点的值)

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **层序遍历**（Breadth‑First Search，简称 BFS），一次把树的每一层的节点全部取出来，再把这层里「最左」和「最右」的非空节点之间的距离算出来，取所有层的最大值即为答案。

> **类比**：把二叉树想象成一排排的「座位」。每层都是一排座位，左边第一个有人坐的座位和右边最后一个有人坐的座位之间的座位数（包括中间的空位）就是该层的宽度。我们只要把每层的座位排出来，找出最左和最右的有人的座位，再算距离就行了。

实现时可以把每层的 **节点**（包括 `None`）放进一个列表 `level`，然后：

1. 记录该层最左、最右出现非空节点的下标 `l`、`r`（列表的下标就是「座位号」）。
2. 该层宽度 = `r - l + 1`（因为座位是从 0 开始计数的）。
3. 把所有非空节点的左右子树（即使是 `None` 也要加入）放进下一层的列表，继续遍历。

**为什么正确**  
宽度的定义本身就是「左端点」到「右端点」之间的长度。我们把每层完整展开（包括空位），直接找左端点和右端点的下标，就恰好等于题目要求的宽度。

**时间/空间分析**  
- 每次遍历一层会把 **所有** 节点（包括 `None`）都放进列表。最坏情况下（比如只有左子树的链状树），第 `i` 层会产生 `2^i` 个 `None`，导致总元素数接近 `2^h`，其中 `h` 为树的高度。  
- 时间复杂度：`O(N * 2^h)`，在最坏情况下相当于 `O(N^2)`（因为 `2^h` 与 `N` 同阶）。  
- 空间复杂度：同理，需要保存最多 `2^h` 个元素的列表，最坏是 `O(N)`（实际上比最优解要多很多）。

> **大白话**：`O(N²)` 就像你有 1000 个人，要和每个人分别比较 1000 次，总共要做 1,000,000 次操作，明显很慢。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def widthOfBinaryTree(root: TreeNode) -> int:
    if not root:
        return 0

    # level 保存当前层的所有节点（包括 None）
    level = [root]
    max_width = 1

    while any(node is not None for node in level):   # 只要本层还有真实节点，就继续
        # 找到本层最左、最右的非空节点下标
        left = next(i for i, n in enumerate(level) if n is not None)
        right = len(level) - 1 - next(i for i, n in enumerate(reversed(level)) if n is not None)

        # 计算宽度
        max_width = max(max_width, right - left + 1)

        # 为下一层准备节点（把 None 也加入，以保持“座位号”）
        next_level = []
        for node in level:
            if node:
                next_level.append(node.left)   # 可能是 None
                next_level.append(node.right)  # 可能是 None
            else:
                # 空位也要占位，保持座位号连续
                next_level.append(None)
                next_level.append(None)

        level = next_level

    return max_width
```

#### 复杂度

- **时间复杂度**：`O(N²)`（最坏情况），因为每层都会把大量 `None` 填进列表，导致整体遍历次数呈平方级增长。  
- **空间复杂度**：`O(N)`（最坏），需要保存整棵树的全部“座位”，其中很多是 `None`，占用的空间比实际节点多。

---

### 2. 最优解

#### 思路  

暴力解慢的根源在于 **显式地把 `None` 填进列表**，这会把本不需要的信息（空位）也当作节点来遍历。我们其实只要知道每个真实节点在「完全二叉树」中的位置编号，就能直接算出宽度，而不必真正生成所有空位。

**关键点**：在完全二叉树中，若根节点编号为 `0`（或 `1`），则  
- 左子节点的编号 = `2 * parent + 1`（或 `2 * parent`）  
- 右子节点的编号 = `2 * parent + 2`（或 `2 * parent + 1`）

只要在遍历时把每个节点的 **编号** 记录下来，就能在同一层得到：

```
宽度 = 最右节点的编号 - 最左节点的编号 + 1
```

实现方式有两种：

1. **BFS + 编号**（最常见）  
   - 使用队列一次遍历每层，队列里存 `(node, index)`。  
   - 进入新层时记录该层第一个节点的 `index`（左端点），遍历完该层后，最后一个弹出的 `index`（右端点）即为右端点。  
   - 计算宽度，更新最大值。  

2. **DFS（前序/中序）+ 编号**  
   - 递归遍历树，记录每层出现的最左编号 `first[col]`（`col` 为层数），随后每访问一个节点，就用 `index - first[col] + 1` 计算该层宽度。  

这里我们采用 **BFS + 编号**，因为思路更直观，且不需要额外的递归栈。

> **类比**：把每个节点想象成「邮递员」在一条无限长的街道上投递信件，根节点站在街道第 `0` 号位置，左孩子往左走两步（`2*i+1`），右孩子往右走两步（`2*i+2`）。我们只记录每个邮递员的街道号，就能直接知道最左和最右的邮递员之间相隔多少号，即宽度。

**为什么正确**  
编号本质上是「如果这棵树是完整二叉树，它在第几号位置」。题目要求的宽度正是这层完整二叉树中最左、最右非空节点的编号差加一。因为我们不把 `None` 放进去，编号之间的差已经天然包含了中间的空位数。

**复杂度对比**  
- 只遍历每个真实节点一次，时间 `O(N)`。  
- 只保存当前层的节点及其编号，最多 `O(width_of_tree)`，在最坏情况下仍是 `O(N)`，但常数更小。

#### 代码（Python）

```python
from collections import deque

# Definition for a binary tree node.
class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def widthOfBinaryTree(root: TreeNode) -> int:
    if not root:
        return 0

    # 队列中存 (节点, 在完全二叉树中的编号)
    # 编号从 0 开始，这样左子 = 2*i+1, 右子 = 2*i+2
    q = deque([(root, 0)])
    max_width = 0

    while q:
        level_len = len(q)
        # 记录本层第一个节点的编号，作为左端点
        _, leftmost = q[0]

        for _ in range(level_len):
            node, idx = q.popleft()
            # 右端点随时更新为当前弹出的节点编号
            # （遍历完本层后，idx 就是最右节点的编号）
            if node.left:
                q.append((node.left, 2 * idx + 1))
            if node.right:
                q.append((node.right, 2 * idx + 2))

        # 此时 q[0] 是下一层的第一个节点，q[-1] 是本层的最后一个节点
        # 计算本层宽度：最右编号 - 最左编号 + 1
        _, rightmost = q[-1] if q else (None, leftmost)  # 若下一层为空，则宽度为 1
        max_width = max(max_width, rightmost - leftmost + 1)

    return max_width
```

> **代码要点解释**  
> 1. `deque` 让我们可以在两端高效地 `popleft` 与 `append`。  
> 2. 编号采用 `0` 起始，左子 `2*i+1`、右子 `2*i+2`，对应完全二叉树的自然编号。  
> 3. 每层结束时，`leftmost` 为本层最左节点的编号，`rightmost` 为本层最右节点的编号（通过遍历时的最后一个 `idx` 得到）。  
> 4. `max_width` 在每层更新，最终返回。

#### 复杂度

- **时间复杂度**：`O(N)`，每个真实节点只被访问一次。  
- **空间复杂度**：`O(W)`，其中 `W` 为树的最大宽度（即队列中最多同时存在的节点数），最坏情况下 `W ≤ N`，但通常远小于 `N`。

---

## 心得

- **核心技巧**：给二叉树的每个节点分配「在完全二叉树中的编号」并利用这些编号直接计算宽度。  
- **适用场景**：  
  1. **Maximum Width of Binary Tree**（本题）  
  2. **Binary Tree Nodes at Distance K**（需要把树映射到数组坐标）  
  3. **Serialize and Deserialize Binary Tree**（利用完全二叉树的编号实现紧凑序列化）  
- **一句话总结**：**把树映射到「编号」的直线坐标系，左端点与右端点的差即为宽度**。

---

## 反思

- **第一反应**：直接层序遍历，想把每层的空位也补齐再计数。  
- **最容易踩的坑**：  
  - 把所有 `None` 加进队列导致指数级膨胀，超出时间限制。  
  - 编号容易越界（如果使用 `int` 直接累乘），在 Python 中整数不溢出，但在其他语言需注意 64 位。  
  - 当树非常不平衡时，需要确保只在有真实节点的层计算宽度，防止 `rightmost` 取到错误的 `None`。  
- **下次思路**：看到“宽度”“层次”“空位计数”这类描述时，第一步就想到 **为每个节点编号**（或记录层的最左/最右位置），从而把“空位”隐式计入，不必显式展开。这样通常能把 `O(N²)` 降到 `O(N)`。