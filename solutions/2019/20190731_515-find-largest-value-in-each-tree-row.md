# #515. 找出每一层的最大值 / Find Largest Value in Each Tree Row

> 难度：中等 · 标签：Tree、Depth-First Search、Breadth-First Search、Binary Tree · [LeetCode 链接](https://leetcode.com/problems/find-largest-value-in-each-tree-row/)

---

## 题目（英文原版）

**Description**

Given the root of a binary tree, return an array of the largest value in each row of the tree (0-indexed).

**Examples**

**Example 1:**

```
Input: root = [1,3,2,5,3,null,9]
Output: [1,3,9]
```

**Example 2:**

```
Input: root = [1,2,3]
Output: [1,3]
```

**Constraints**

- The number of nodes in the tree will be in the range [0, 104].
- -231 <= Node.val <= 231 - 1

---

## 题目（中文翻译）

给定一棵二叉树（binary tree）的根节点（root），返回一个数组，其中第 i 行（0 索引）的最大值。

**示例 1**  
输入: `root = [1,3,2,5,3,null,9]`  
输出: `[1,3,9]`

**示例 2**  
输入: `root = [1,2,3]`  
输出: `[1,3]`

**约束条件**  

- 树中节点的数量在 `[0, 10^4]` 区间内。  
- `-2^31 <= Node.val <= 2^31 - 1` 。

---

## 解题过程

### 1. 直觉解（暴力）

#### 思路  

最直接的想法是 **层序遍历**（Breadth‑First Search，简称 BFS），也就是一次遍历树的每一层，把同一层的所有节点收集到一个列表里，再把这个列表取最大值。  
可以把树的每一层想象成 **排队买票的队伍**，我们一次只让当前排在最前面的那一批人（同一层的节点）进去查看，然后把他们的孩子（下一层的节点）排到队尾，等这批人全部处理完后，就进入下一层。

实现时我们用 **队列**（queue）来保存待处理的节点。队列的特性类似“排队买票”，**先进先出**（FIFO），正好满足层序遍历的需求。  

遍历完整棵树后，每层得到的最大值即为答案。

> **为什么正确**  
> BFS 按层访问，保证在同一次循环里处理的节点一定属于同一层。我们对每层取最大值，自然得到“每一层的最大节点值”。

#### 代码（Python）

```python
# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val          # 节点的数值
        self.left = left        # 左子树
        self.right = right      # 右子树

from collections import deque  # 引入双端队列，实现队列的 push/pop

def largestValues(root: TreeNode) -> list[int]:
    """
    暴力的层序遍历解法
    """
    if not root:                     # 空树直接返回空列表
        return []

    result = []                       # 保存每层的最大值
    q = deque([root])                 # 初始化队列，只放根节点

    while q:                          # 只要队列不空，就说明还有未访问的层
        level_size = len(q)           # 当前层有多少节点
        level_max = -float('inf')     # 设一个很小的初始值，后面会被真正的节点值覆盖

        for _ in range(level_size):   # 逐个处理本层的节点
            node = q.popleft()        # 取出队首节点
            level_max = max(level_max, node.val)   # 更新本层最大值

            # 将子节点加入队列，供下一层使用
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        result.append(level_max)      # 本层遍历完，保存最大值

    return result
```

#### 复杂度  

- **时间复杂度：** `O(N)`  
  每个节点恰好被访问一次（`N` 为树中节点数），所以运行时间和节点数成正比。  
  “O(N)” 可以理解为“如果树里有 1000 个节点，程序大概会做 1000 次基本操作”。

- **空间复杂度：** `O(W)`，`W` 为树的最大宽度（最宽层的节点数）。  
  队列里同时最多保存同一层的所有节点，最坏情况下相当于树的最宽层。例如，满二叉树第 `h` 层有 `2^{h}` 个节点，空间会随层数指数增长。但总体仍然小于 `N`。

---

### 2. 最优解

#### 思路  

虽然上面的 BFS 已经是 `O(N)` 的线性时间，但它需要 **额外的队列** 来保存每层的所有节点，最坏情况下占用 `O(W)` 的空间。  
我们可以把 “遍历顺序” 换成 **深度优先搜索**（DFS），用递归（或显式栈）一次走到底，再回溯。  

核心想法：

1. **记录当前遍历到的层号**（根节点是第 0 层，左子树/右子树分别是第 `level+1` 层）。  
2. 用一个列表 `ans` 保存每层已经找到的最大值。  
3. 当第一次到达某一层时（`len(ans) == level`），说明这层还没有任何记录，直接把当前节点值加入 `ans`。  
4. 若该层已经有记录，比较当前节点值与 `ans[level]`，取较大者保存。  

因为递归天然使用调用栈，额外空间只和树的 **深度**（`height`）有关，最坏情况下（链状树）是 `O(N)`，但在大多数平衡树中只需要 `O(log N)`，通常比 BFS 的 `O(W)` 更省空间。

> **为什么正确**  
> DFS 按“先根后左后右”（或先根后右后左）的顺序访问节点，但我们在访问每个节点时都把它所在的层号传进去。只要每层的最大值在遍历过程中被及时更新，最终 `ans` 中保存的就是每层的最大值。遍历完整棵树后，所有层都被检查过，答案自然正确。

#### 代码（Python）

```python
def largestValuesDFS(root: TreeNode) -> list[int]:
    """
    使用深度优先搜索，空间更友好（只用递归栈）
    """
    ans = []                       # ans[i] 保存第 i 层的最大值

    def dfs(node: TreeNode, level: int) -> None:
        if not node:               # 空节点直接返回
            return

        # 如果是第一次来到这一层，直接把当前值放进 ans
        if level == len(ans):
            ans.append(node.val)   # ans 长度恰好等于层号，说明还没有记录
        else:
            # 已有记录，取两者较大者
            ans[level] = max(ans[level], node.val)

        # 继续往左、右子树递归，层号+1
        dfs(node.left, level + 1)
        dfs(node.right, level + 1)

    dfs(root, 0)                   # 从根节点开始，层号 0
    return ans
```

#### 复杂度  

- **时间复杂度：** `O(N)`  
  同样每个节点只会被访问一次，只是遍历顺序从“层”改成了“深”。  

- **空间复杂度：** `O(H)`，`H` 为树的高度（递归调用栈的最大深度）。  
  对于平衡二叉树，`H ≈ log₂N`，远小于 BFS 需要的最宽层宽度。  
  在最坏的链状树里，`H = N`，此时空间与 BFS 相同，但仍然是 **最优的**（因为我们没有额外的队列）。

---

## 心得

- **核心技巧**：层序遍历（BFS）或深度优先遍历（DFS）配合“层号 + 记录每层最大值”。  
- **适用的题型**：  
  1. “每层节点的平均值 / 最小值 / 节点个数” 之类的层级统计题。  
  2. “二叉树的右视图 / 左视图” 需要按层保存特定节点。  
  3. “二叉树的层序遍历” 本身的基础练习。  
- **一句话总结**：**遍历时记住“我在第几层”，然后把该层的极值更新即可**。

## 反思

- **第一反应**：看到“每层的最大值”，立刻想到层序遍历，因为层序天然把同层节点放在一起，最直观。  
- **最容易踩的坑**：  
  - 忘记处理空树（`root` 为 `None`）导致报错。  
  - 在 BFS 中把 `level_max` 初始化得不够小（比如 0），会在所有节点值为负数时得到错误答案。  
  - 在 DFS 中忘记在第一次到达新层时 `append`，导致 `IndexError`。  
- **下次类似题的第一步**：先明确“要在同一层之间比较”，决定是用 **队列层序** 还是 **递归记录层号**，再选择最省空间的实现方式。